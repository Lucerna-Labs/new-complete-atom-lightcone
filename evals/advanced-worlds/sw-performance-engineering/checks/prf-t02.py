import base64
import json
import pathlib
import subprocess
import sys


def fixture(label, count, rows, final, misses, seed=None):
    # Each row is a hand-specified witness: pc,index,taken,prediction,before,after,miss.
    events = [{"pc": row[0], "taken": row[2]} for row in rows]
    args = [count, events] if seed is None else [count, events, seed]
    names = ("pc", "index", "taken", "prediction", "before", "after", "misprediction")
    expected = {"states": final, "mispredictions": misses,
                "trace": [dict(zip(names, row)) for row in rows]}
    return label, args, expected


# Literal transitions; the repeated constant/pair witnesses below are closed-form
# traces, not a second implementation of the indexed predictor.
CASES = [
    fixture("empty default table", 4, [], [1, 1, 1, 1], 0),
    fixture("empty zero seed", 1, [], [0], 0, 0),
    fixture("empty maximum table and seed", 16, [], [3] * 16, 0, 3),
    fixture("zero stays saturated", 1, [(0, 0, False, False, 0, 0, False)], [0], 0, 0),
    fixture("zero learns taken without changing prediction", 1, [(0, 0, True, False, 0, 1, True)], [1], 1, 0),
    fixture("weak not taken decrements", 1, [(0, 0, False, False, 1, 0, False)], [0], 0, 1),
    fixture("one to two still mispredicts", 1, [(0, 0, True, False, 1, 2, True)], [2], 1, 1),
    fixture("two to one still mispredicts", 1, [(0, 0, False, True, 2, 1, True)], [1], 1, 2),
    fixture("weak taken increments", 1, [(0, 0, True, True, 2, 3, False)], [3], 0, 2),
    fixture("strong taken decrements", 1, [(0, 0, False, True, 3, 2, True)], [2], 1, 3),
    fixture("three stays saturated", 1, [(0, 0, True, True, 3, 3, False)], [3], 0, 3),
    fixture("omitted seed is one", 1, [(0, 0, True, False, 1, 2, True)], [2], 1),
    fixture("alternation from zero", 1,
            [(0, 0, True, False, 0, 1, True), (0, 0, False, False, 1, 0, False)] * 3,
            [0], 3, 0),
    fixture("alternation from one", 1,
            [(0, 0, True, False, 1, 2, True), (0, 0, False, True, 2, 1, True)] * 3,
            [1], 6, 1),
    fixture("taken training then saturation", 1,
            [(0, 0, True, False, 0, 1, True), (0, 0, True, False, 1, 2, True),
             (0, 0, True, True, 2, 3, False), (0, 0, True, True, 3, 3, False)],
            [3], 2, 0),
    fixture("not taken training then saturation", 1,
            [(0, 0, False, True, 3, 2, True), (0, 0, False, True, 2, 1, True),
             (0, 0, False, False, 1, 0, False), (0, 0, False, False, 0, 0, False)],
            [0], 2, 3),
    fixture("unaligned byte addresses share a slot", 2,
            [(1, 0, True, False, 1, 2, True), (2, 0, False, True, 2, 1, True),
             (3, 0, True, False, 1, 2, True), (4, 1, False, False, 1, 0, False)],
            [2, 0], 3),
    fixture("non power of two indexing and maximum PC", 3,
            [(65535, 0, True, False, 1, 2, True), (65532, 0, False, True, 2, 1, True),
             (65531, 2, True, False, 1, 2, True), (4, 1, False, False, 1, 0, False)],
            [1, 0, 2], 3),
    fixture("opposed aliased sites", 2,
            [(0, 0, True, False, 1, 2, True), (8, 0, False, True, 2, 1, True)] * 3,
            [1, 1], 6),
    fixture("opposed independent sites", 2,
            [(0, 0, True, False, 1, 2, True), (4, 1, False, False, 1, 0, False),
             (0, 0, True, True, 2, 3, False), (4, 1, False, False, 0, 0, False),
             (0, 0, True, True, 3, 3, False), (4, 1, False, False, 0, 0, False)],
            [3, 0], 1),
    fixture("last entry and wrap to first", 16,
            [(60, 15, True, False, 1, 2, True), (64, 0, False, False, 1, 0, False),
             (65535, 15, False, True, 2, 1, True)],
            [0] + [1] * 15, 2),
    fixture("same outcome at distinct entries does not train every entry", 3,
            [(0, 0, True, False, 0, 1, True), (4, 1, True, False, 0, 1, True),
             (8, 2, True, False, 0, 1, True), (0, 0, True, False, 1, 2, True)],
            [2, 1, 1], 4, 0),
    fixture("maximum constant trace", 1,
            [(65535, 0, True, True, 3, 3, False)] * 128, [3], 0, 3),
    fixture("maximum alternating trace", 1,
            [(0, 0, True, False, 1, 2, True), (0, 0, False, True, 2, 1, True)] * 64,
            [1], 128),
]
CALLS = CASES + [CASES[19], CASES[0], CASES[1], CASES[19], CASES[11]]
EXPECTED = [result for _, _, result in CALLS]


def equal(actual, expected):
    if type(actual) is not type(expected):
        return False
    if type(expected) is dict:
        return actual.keys() == expected.keys() and all(equal(actual[k], v) for k, v in expected.items())
    if type(expected) is list:
        return len(actual) == len(expected) and all(equal(a, e) for a, e in zip(actual, expected))
    return actual == expected


def matches(actual):
    return equal(actual, {"values": EXPECTED, "unchanged": True,
                          "stable_outputs": True, "independent": True})


RUNNER = r'''import base64,copy,importlib.util,json,sys
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
def disjoint(values, forbidden):
    seen=set(forbidden)
    def visit(value):
        if type(value) not in (dict,list): return True
        if id(value) in seen: return False
        seen.add(id(value))
        return all(visit(item) for item in (value.values() if type(value) is dict else value))
    return all(visit(value) for value in values)
values=[];inputs=[];outputs=[];input_ids=set();unchanged=True;stable=True;independent=True
for data in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(data);inputs.append((supplied,fingerprint(supplied)));input_ids.update(mutable_ids(supplied))
    value=module.predictor_trace(*supplied)
    outputs.append((value,fingerprint(value)));values.append(value)
    unchanged=unchanged and all(fingerprint(prior)==before for prior,before in inputs)
    stable=stable and all(fingerprint(prior)==before for prior,before in outputs)
    independent=independent and disjoint(values,input_ids)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged,"stable_outputs":stable,"independent":independent}))'''


def run(candidate):
    payload = base64.b64encode(json.dumps([args for _, args, _ in CALLS]).encode()).decode()
    try:
        process = subprocess.run([sys.executable, "-B", "-c", RUNNER,
                                  str(pathlib.Path(candidate).resolve()), payload],
                                 capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if process.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


if __name__ == "__main__":
    ok = len(sys.argv) == 2 and matches(run(sys.argv[1]))
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
