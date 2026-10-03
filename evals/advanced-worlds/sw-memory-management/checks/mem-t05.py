import base64
import json
import pathlib
import subprocess
import sys


def state(gray=(), black=(), white=(), finished=False, missed=()):
    return {"gray": list(gray), "black": list(black), "white": list(white),
            "finished": finished, "missed": list(missed)}


def scan():
    return {"op": "scan"}


def finish():
    return {"op": "finish"}


def store(source, index, target):
    return {"op": "store", "object": source, "index": index, "target": target}


_OMITTED = object()


def case(name, graph, roots, events, expected, barrier=_OMITTED):
    args = {"graph": graph, "roots": roots, "events": events}
    if barrier is not _OMITTED:
        args["barrier"] = barrier
    return name, args, expected


# Each color/queue state below was worked from the stated atomic events.
# No marking algorithm is used to construct the expected snapshots.
CASES = [
    case("empty initial snapshot", {}, [], [], [state()]),
    case("empty completion", {}, [], [finish()], [state(), state(finished=True)]),
    case("empty scan is a no-op", {}, [], [scan(), finish()],
         [state(), state(), state(finished=True)]),
    case("initial root is gray not black", {"A": []}, ["A"], [], [state(["A"])]),
    case("one root scan then finish", {"A": []}, ["A"], [scan(), finish()],
         [state(["A"]), state(black=["A"]), state(black=["A"], finished=True)]),
    case("nonempty frontier blocks completion", {"A": []}, ["A"], [finish(), scan(), finish()],
         [state(["A"]), state(["A"]), state(black=["A"]), state(black=["A"], finished=True)]),
    case("unrooted self cycle can remain white", {"A": ["A"]}, [], [finish()],
         [state(white=["A"]), state(white=["A"], finished=True)]),
    case("duplicate roots retain first occurrence queue order", {"z": [], "A_1": [], "B": []},
         ["z", "A_1", "z"], [scan(), scan(), finish()],
         [state(["z", "A_1"], white=["B"]), state(["A_1"], ["z"], ["B"]),
          state(black=["A_1", "z"], white=["B"]), state(black=["A_1", "z"], white=["B"], finished=True)]),
    case("field scan order and duplicate discovery", {"R": ["Z", "A", "Z", None], "A": [], "Z": []},
         ["R"], [scan(), scan(), scan(), finish()],
         [state(["R"], white=["A", "Z"]), state(["Z", "A"], ["R"]), state(["A"], ["R", "Z"]),
          state(black=["A", "R", "Z"]), state(black=["A", "R", "Z"], finished=True)]),
    case("rooted two object cycle terminates", {"A": ["B"], "B": ["A"]},
         ["A"], [scan(), scan(), finish()],
         [state(["A"], white=["B"]), state(["B"], ["A"]), state(black=["A", "B"]),
          state(black=["A", "B"], finished=True)]),
    case("default barrier protects the moved gray path", {"B": [None], "G": ["W"], "W": []},
         ["B", "G"], [scan(), store("B", 0, "W"), store("G", 0, None), scan(), scan(), finish()],
         [state(["B", "G"], white=["W"]), state(["G"], ["B"], ["W"]), state(["G", "W"], ["B"]),
          state(["G", "W"], ["B"]), state(["W"], ["B", "G"]), state(black=["B", "G", "W"]),
          state(black=["B", "G", "W"], finished=True)]),
    case("disabled barrier diagnoses the moved gray path", {"B": [None], "G": ["W"], "W": []},
         ["B", "G"], [scan(), store("B", 0, "W"), store("G", 0, None), scan(), scan(), finish()],
         [state(["B", "G"], white=["W"]), state(["G"], ["B"], ["W"]), state(["G"], ["B"], ["W"]),
          state(["G"], ["B"], ["W"]), state(black=["B", "G"], white=["W"]),
          state(black=["B", "G"], white=["W"]), state(black=["B", "G"], white=["W"], finished=True, missed=["W"])], False),
    case("gray store waits for atomic scan rather than shading early", {"A": [None], "W": []},
         ["A"], [store("A", 0, "W"), scan(), scan(), finish()],
         [state(["A"], white=["W"]), state(["A"], white=["W"]), state(["W"], ["A"]),
          state(black=["A", "W"]), state(black=["A", "W"], finished=True)], True),
    case("white source does not create a discovery", {"R": [], "X": [None], "W": []},
         ["R"], [store("X", 0, "W"), scan(), finish()],
         [state(["R"], white=["W", "X"]), state(["R"], white=["W", "X"]),
          state(black=["R"], white=["W", "X"]), state(black=["R"], white=["W", "X"], finished=True)]),
    case("already gray target is not queued twice", {"A": ["B"], "B": []},
         ["A", "B"], [scan(), store("A", 0, "B"), scan(), finish()],
         [state(["A", "B"]), state(["B"], ["A"]), state(["B"], ["A"]),
          state(black=["A", "B"]), state(black=["A", "B"], finished=True)]),
    case("black target remains black", {"A": [None], "B": []},
         ["A", "B"], [scan(), scan(), store("A", 0, "B"), finish()],
         [state(["A", "B"]), state(["B"], ["A"]), state(black=["A", "B"]),
          state(black=["A", "B"]), state(black=["A", "B"], finished=True)]),
    case("black self edge does not reopen frontier", {"A": [None]},
         ["A"], [scan(), store("A", 0, "A"), finish()],
         [state(["A"]), state(black=["A"]), state(black=["A"]), state(black=["A"], finished=True)]),
    case("deleting before discovery can leave white garbage", {"A": ["W"], "W": []},
         ["A"], [store("A", 0, None), scan(), finish()],
         [state(["A"], white=["W"]), state(["A"], white=["W"]), state(black=["A"], white=["W"]),
          state(black=["A"], white=["W"], finished=True)]),
    case("discovered object remains retained after path deletion", {"A": ["W"], "W": []},
         ["A"], [scan(), store("A", 0, None), scan(), finish()],
         [state(["A"], white=["W"]), state(["W"], ["A"]), state(["W"], ["A"]),
          state(black=["A", "W"]), state(black=["A", "W"], finished=True)]),
    case("stores use requested field and queue in store order", {"R": [None, None], "A": [], "B": []},
         ["R"], [scan(), store("R", 1, "B"), store("R", 0, "A"), scan(), scan(), finish()],
         [state(["R"], white=["A", "B"]), state(black=["R"], white=["A", "B"]),
          state(["B"], ["R"], ["A"]), state(["B", "A"], ["R"]), state(["A"], ["B", "R"]),
          state(black=["A", "B", "R"]), state(black=["A", "B", "R"], finished=True)]),
    case("blocked finish leaves later store legal", {"A": [None], "W": []},
         ["A"], [finish(), store("A", 0, "W"), scan(), scan(), finish()],
         [state(["A"], white=["W"]), state(["A"], white=["W"]), state(["A"], white=["W"]),
          state(["W"], ["A"]), state(black=["A", "W"]), state(black=["A", "W"], finished=True)]),
    case("missed diagnostic includes reachable descendants", {"B": [None], "G": ["W"], "W": ["X"], "X": []},
         ["B", "G"], [scan(), store("B", 0, "W"), store("G", 0, None), scan(), finish()],
         [state(["B", "G"], white=["W", "X"]), state(["G"], ["B"], ["W", "X"]),
          state(["G"], ["B"], ["W", "X"]), state(["G"], ["B"], ["W", "X"]),
          state(black=["B", "G"], white=["W", "X"]),
          state(black=["B", "G"], white=["W", "X"], finished=True, missed=["W", "X"])], False),
    case("disabled barrier still scans gray source normally", {"A": [None], "W": []},
         ["A"], [store("A", 0, "W"), scan(), scan(), finish()],
         [state(["A"], white=["W"]), state(["A"], white=["W"]), state(["W"], ["A"]),
          state(black=["A", "W"]), state(black=["A", "W"], finished=True)], False),
    case("missed is not all white objects", {"B": [None], "W": [], "Z": []},
         ["B"], [scan(), store("B", 0, "W"), finish()],
         [state(["B"], white=["W", "Z"]), state(black=["B"], white=["W", "Z"]),
          state(black=["B"], white=["W", "Z"]),
          state(black=["B"], white=["W", "Z"], finished=True, missed=["W"])], False),
    case("unfinished trace does not report missed diagnostic", {"B": [None], "W": []},
         ["B"], [scan(), store("B", 0, "W")],
         [state(["B"], white=["W"]), state(black=["B"], white=["W"]),
          state(black=["B"], white=["W"])], False),
    case("maximum field count deduplicates discovery", {"A": ["B"] * 8, "B": []},
         ["A"] * 24, [scan(), scan(), finish()],
         [state(["A"], white=["B"]), state(["B"], ["A"]), state(black=["A", "B"]),
          state(black=["A", "B"], finished=True)]),
    case("maximum object count no roots", {name: [] for name in "ABCDEFGHIJKL"}, [], [finish()],
         [state(white=list("ABCDEFGHIJKL")), state(white=list("ABCDEFGHIJKL"), finished=True)]),
    case("maximum event count of empty scans", {}, [], [scan() for _ in range(64)],
         [state() for _ in range(65)]),
    case("store preserves the other unscanned field", {"A": ["W", None], "W": [], "X": []},
         ["A"], [store("A", 1, "X"), scan(), scan(), scan(), finish()],
         [state(["A"], white=["W", "X"]), state(["A"], white=["W", "X"]),
          state(["W", "X"], ["A"]), state(["X"], ["A", "W"]), state(black=["A", "W", "X"]),
          state(black=["A", "W", "X"], finished=True)]),
]
CALLS = CASES + [CASES[10], CASES[0], CASES[3], CASES[11], CASES[10]]
EXPECTED = [value for _, _, value in CALLS]


def matches(actual):
    return json.dumps(actual, sort_keys=True) == json.dumps(
        {"values": EXPECTED, "unchanged": True, "separate": True}, sort_keys=True)


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
    raise TypeError("value outside exact native types")
def mutable_ids(value):
    if type(value) is dict:
        return {id(value)}.union(*(mutable_ids(item) for item in value.values()))
    if type(value) is list:
        return {id(value)}.union(*(mutable_ids(item) for item in value))
    return set()
values=[];inputs=[];before=[];seen=set();separate=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args);inputs.append(supplied);before.append(fingerprint(supplied))
    value=module.marking_trace(**supplied)
    fingerprint(value)
    if type(value) is not list:
        raise TypeError("trace must be a native list")
    if id(value) in seen:
        separate=False
    seen.add(id(value))
    for snapshot in value:
        ids=mutable_ids(snapshot);separate=separate and not bool(ids & seen);seen.update(ids)
    values.append(value)
unchanged=all(fingerprint(value)==old for value,old in zip(inputs,before))
fingerprint(values)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged,"separate":separate}))'''
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
