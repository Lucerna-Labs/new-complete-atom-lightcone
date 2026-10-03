import base64
import json
import pathlib
import subprocess
import sys


def task(identifier, suppress=False, value=0):
    return {"id": identifier, "suppress": suppress, "value": value}


def state(identifier, status, count, received=False, value=None):
    return {"id": identifier, "state": status, "cancelling": count,
            "received_cancel": received, "value": value}


def case(name, tasks, requests, cancel_results, leaf_cancelled, states):
    return (name, {"tasks": tasks, "requests": requests},
            {"cancel_results": cancel_results, "leaf_future_cancelled": leaf_cancelled,
             "tasks": states})


# Literal outcomes from the leaf-to-root exception/normal-result path.
# The oracle builder only formats records; it does not evaluate that path.
CASES = [
    case("one pending task", [task("P")], 0, [], False,
         [state("P", "pending", 0)]),
    case("one propagating task", [task("P")], 1, [True], True,
         [state("P", "cancelled", 1, True)]),
    case("one absorbing task", [task("P", True, 7)], 1, [True], True,
         [state("P", "returned", 1, True, 7)]),
    case("zero result and five accepted requests", [task("P", True, 0)], 5,
         [True, True, True, True, True], True, [state("P", "returned", 5, True, 0)]),
    case("negative result does not clear request count", [task("P", True, -100)], 2,
         [True, True], True, [state("P", "returned", 2, True, -100)]),
    case("child absorbs before parent receives exception", [task("P", False, 99), task("C", True, 7)],
         1, [True], True,
         [state("P", "returned", 1, False, 7), state("C", "returned", 1, True, 7)]),
    case("parent absorbs child terminal cancellation", [task("P", True, 9), task("C")],
         1, [True], True,
         [state("P", "returned", 1, True, 9), state("C", "cancelled", 1, True)]),
    case("two propagators", [task("P"), task("C")], 1, [True], True,
         [state("P", "cancelled", 1, True), state("C", "cancelled", 1, True)]),
    case("parent handler is not invoked after child absorbs", [task("P", True, 9), task("C", True, 7)],
         1, [True], True,
         [state("P", "returned", 1, False, 7), state("C", "returned", 1, True, 7)]),
    case("middle task absorbs", [task("R"), task("M", True, 7), task("L")], 1, [True], True,
         [state("R", "returned", 1, False, 7), state("M", "returned", 1, True, 7),
          state("L", "cancelled", 1, True)]),
    case("root absorbs after two propagated exceptions", [task("R", True, 9), task("M"), task("L")],
         2, [True, True], True,
         [state("R", "returned", 2, True, 9), state("M", "cancelled", 2, True),
          state("L", "cancelled", 2, True)]),
    case("lowest of several handlers wins", [task("R", True, 99), task("M", True, 11), task("L", True, 7)],
         1, [True], True,
         [state("R", "returned", 1, False, 7), state("M", "returned", 1, False, 7),
          state("L", "returned", 1, True, 7)]),
    case("multiple requests still allow zero-valued child absorption", [task("R"), task("M"), task("L", True, 0)],
         3, [True, True, True], True,
         [state("R", "returned", 3, False, 0), state("M", "returned", 3, False, 0),
          state("L", "returned", 3, True, 0)]),
    case("unused middle handler does not replace result", [task("R"), task("M", True, -4), task("L", True, 6)],
         4, [True, True, True, True], True,
         [state("R", "returned", 4, False, 6), state("M", "returned", 4, False, 6),
          state("L", "returned", 4, True, 6)]),
    case("five requests do not imply five deliveries per task", [task("R"), task("M"), task("L")],
         5, [True, True, True, True, True], True,
         [state("R", "cancelled", 5, True), state("M", "cancelled", 5, True),
          state("L", "cancelled", 5, True)]),
    case("handlers do not run without cancellation", [task("R", True, 9), task("M"), task("L", True, 7)],
         0, [], False,
         [state("R", "pending", 0), state("M", "pending", 0), state("L", "pending", 0)]),
    case("eight-task propagation", [task("A"), task("B"), task("C"), task("D"),
         task("E"), task("F"), task("G"), task("H")], 2, [True, True], True,
         [state("A", "cancelled", 2, True), state("B", "cancelled", 2, True),
          state("C", "cancelled", 2, True), state("D", "cancelled", 2, True),
          state("E", "cancelled", 2, True), state("F", "cancelled", 2, True),
          state("G", "cancelled", 2, True), state("H", "cancelled", 2, True)]),
    case("eight-task leaf absorption", [task("A"), task("B"), task("C"), task("D"),
         task("E"), task("F"), task("G"), task("H", True, 100)], 1, [True], True,
         [state("A", "returned", 1, False, 100), state("B", "returned", 1, False, 100),
          state("C", "returned", 1, False, 100), state("D", "returned", 1, False, 100),
          state("E", "returned", 1, False, 100), state("F", "returned", 1, False, 100),
          state("G", "returned", 1, False, 100), state("H", "returned", 1, True, 100)]),
    case("eight-task middle absorption", [task("A"), task("B"), task("C"), task("D", True, 17),
         task("E"), task("F"), task("G"), task("H")], 3, [True, True, True], True,
         [state("A", "returned", 3, False, 17), state("B", "returned", 3, False, 17),
          state("C", "returned", 3, False, 17), state("D", "returned", 3, True, 17),
          state("E", "cancelled", 3, True), state("F", "cancelled", 3, True),
          state("G", "cancelled", 3, True), state("H", "cancelled", 3, True)]),
    case("input order and case-sensitive identifiers", [task("Root9"), task("child_a", True, -4), task("Z")],
         2, [True, True], True,
         [state("Root9", "returned", 2, False, -4), state("child_a", "returned", 2, True, -4),
          state("Z", "cancelled", 2, True)]),
    case("repeated cancellation delegates into already-cancelled leaf future", [task("P"), task("C", True, 8)],
         4, [True, True, True, True], True,
         [state("P", "returned", 4, False, 8), state("C", "returned", 4, True, 8)]),
    case("root suppression can return zero", [task("P", True, 0), task("C")], 1, [True], True,
         [state("P", "returned", 1, True, 0), state("C", "cancelled", 1, True)]),
]
CALLS = CASES + [CASES[5], CASES[0], CASES[2], CASES[5]]
EXPECTED = [value for _, _, value in CALLS]


def matches(actual):
    return json.dumps(actual, sort_keys=True) == json.dumps(
        {"values": EXPECTED, "unchanged": True}, sort_keys=True)


def run(candidate):
    payload = base64.b64encode(json.dumps([args for _, args, _ in CALLS]).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
def fingerprint(value):
    if type(value) is dict and all(type(key) is str for key in value):
        return ("dict",tuple((key,fingerprint(value[key])) for key in sorted(value)))
    if type(value) is list:
        return ("list",tuple(fingerprint(item) for item in value))
    if type(value) in (str,int,bool,type(None)):
        return (type(value).__name__,value)
    raise TypeError("value outside the exact input/output types")
values=[];unchanged=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args)
    value=module.cancellation_chain(**supplied)
    fingerprint(value)
    values.append(value)
    unchanged=unchanged and fingerprint(supplied)==fingerprint(args)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged}))'''
    try:
        result = subprocess.run([sys.executable, "-B", "-c", runner,
                                 str(pathlib.Path(candidate).resolve()), payload],
                                capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in result.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if result.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


if __name__ == "__main__":
    ok = len(sys.argv) == 2 and matches(run(sys.argv[1]))
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
