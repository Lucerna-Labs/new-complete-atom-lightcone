"""Hand-specified snapshot-view schedules; no database or SQL execution."""
import base64
import json
import pathlib
import subprocess
import sys


def B(tx, mode="rr"):
    return {"op": "begin", "tx": tx, "isolation": mode}


def R(tx, key):
    return {"op": "read", "tx": tx, "key": key}


def S(tx, minimum=0):
    return {"op": "scan", "tx": tx, "minimum": minimum}


def W(tx, key, value):
    return {"op": "write", "tx": tx, "key": key, "value": value}


def C(tx):
    return {"op": "commit", "tx": tx}


def A(tx):
    return {"op": "abort", "tx": tx}


def E(changes):
    return {"op": "external_commit", "changes": changes}


def rd(tx, epoch, key, value):
    return {"op": "read", "tx": tx, "epoch": epoch, "key": key, "value": value}


def sc(tx, epoch, pairs):
    return {"op": "scan", "tx": tx, "epoch": epoch,
            "rows": [{"key": key, "value": value} for key, value in pairs]}


def result(epoch, committed, observations=()):
    return {"epoch": epoch, "committed": committed, "observations": list(observations)}


# Expected epochs, versions and overlays are literal witnesses worked from
# each stated schedule. Helpers only construct records and do not execute it.
CASES = [
    ("empty", [{}, []], result(0, {})),
    ("initial state without events", [{"a": 10, "b": -2}, []], result(0, {"a": 10, "b": -2})),
    ("closed read-only commit advances model epoch", [{"a": 10}, [B("T", "rc"), R("T", "a"), C("T")]],
     result(1, {"a": 10}, [rd("T", 0, "a", 10)])),
    ("RR snapshot is first data statement, not BEGIN", [{"x": 10},
     [B("T"), E({"x": 12}), R("T", "x"), E({"x": 13}), R("T", "x")]],
     result(2, {"x": 13}, [rd("T", 1, "x", 12), rd("T", 1, "x", 12)])),
    ("RC gets each new command view", [{"x": 10},
     [B("T", "rc"), E({"x": 12}), R("T", "x"), E({"x": 13}), R("T", "x")]],
     result(2, {"x": 13}, [rd("T", 1, "x", 12), rd("T", 2, "x", 13)])),
    ("RR retains established old row", [{"x": 10},
     [B("T"), R("T", "x"), E({"x": 12}), R("T", "x")]],
     result(1, {"x": 12}, [rd("T", 0, "x", 10), rd("T", 0, "x", 10)])),
    ("RR scan membership excludes external changes", [{"a": 1, "b": 2},
     [B("T"), S("T", 2), E({"a": 4, "c": 3}), S("T", 2)]],
     result(1, {"a": 4, "b": 2, "c": 3},
            [sc("T", 0, [("b", 2)]), sc("T", 0, [("b", 2)])])),
    ("RC scan membership includes new committed rows", [{"a": 1, "b": 2},
     [B("T", "rc"), S("T", 2), E({"a": 4, "c": 3}), S("T", 2)]],
     result(1, {"a": 4, "b": 2, "c": 3},
            [sc("T", 0, [("b", 2)]), sc("T", 1, [("a", 4), ("b", 2), ("c", 3)])])),
    ("first RR write captures before later reads", [{"x": 10, "z": 0},
     [B("T"), W("T", "z", 7), E({"x": 12}), R("T", "x"), R("T", "z"), C("T")]],
     result(2, {"x": 12, "z": 7}, [rd("T", 0, "x", 10), rd("T", 0, "z", 7)])),
    ("first write after external commit captures later epoch", [{"x": 10, "z": 0},
     [B("T"), E({"x": 12}), W("T", "z", 7), E({"x": 13}),
      R("T", "x"), R("T", "z"), C("T")]],
     result(3, {"x": 13, "z": 7}, [rd("T", 1, "x", 12), rd("T", 1, "z", 7)])),
    ("own private write is not another transaction dirty read", [{"x": 10},
     [B("T"), W("T", "x", 11), B("U", "rc"), R("U", "x"),
      R("T", "x"), A("T"), R("U", "x")]],
     result(0, {"x": 10}, [rd("U", 0, "x", 10), rd("T", 0, "x", 11), rd("U", 0, "x", 10)])),
    ("own inserted row enters RR scan above old external view", [{"a": 1},
     [B("T"), W("T", "c", 3), E({"b": 2}), S("T", 2), C("T")]],
     result(2, {"a": 1, "b": 2, "c": 3}, [sc("T", 0, [("c", 3)])])),
    ("own deletion shadows a visible old version", [{"a": 1, "b": 2},
     [B("T"), W("T", "a", None), E({"b": 5}), R("T", "a"), S("T"), A("T")]],
     result(1, {"a": 1, "b": 5}, [rd("T", 0, "a", None), sc("T", 0, [("b", 2)])])),
    ("commit changes RC view without replacing older RR view", [{"a": 1},
     [B("Old"), R("Old", "a"), B("Writer", "rc"), W("Writer", "a", 2),
      B("Reader", "rc"), R("Reader", "a"), C("Writer"), R("Reader", "a"), R("Old", "a")]],
     result(1, {"a": 2}, [rd("Old", 0, "a", 1), rd("Reader", 0, "a", 1),
                          rd("Reader", 1, "a", 2), rd("Old", 0, "a", 1)])),
    ("abort discards all private changes", [{"a": 1},
     [B("T", "rc"), W("T", "a", 2), W("T", "c", 3), A("T"),
      B("U", "rc"), R("U", "c"), R("U", "a")]],
     result(0, {"a": 1}, [rd("U", 0, "c", None), rd("U", 0, "a", 1)])),
    ("RC external delete and reinsert", [{"a": 1},
     [B("T", "rc"), R("T", "a"), E({"a": None}), R("T", "a"), E({"a": 3}), R("T", "a")]],
     result(2, {"a": 3}, [rd("T", 0, "a", 1), rd("T", 1, "a", None), rd("T", 2, "a", 3)])),
    ("RR retains old version through delete and reinsert", [{"a": 1},
     [B("T"), R("T", "a"), E({"a": None}), R("T", "a"), E({"a": 3}), R("T", "a")]],
     result(2, {"a": 3}, [rd("T", 0, "a", 1), rd("T", 0, "a", 1), rd("T", 0, "a", 1)])),
    ("a missing-row read still establishes RR snapshot", [{},
     [E({"a": 1}), E({"b": 2}), B("T"), R("T", "q"), E({"q": 7}), R("T", "q")]],
     result(3, {"a": 1, "b": 2, "q": 7}, [rd("T", 2, "q", None), rd("T", 2, "q", None)])),
    ("two RR transactions establish independent epochs", [{"x": 1},
     [B("A"), E({"x": 2}), B("B"), R("B", "x"), E({"x": 3}), R("A", "x"), R("B", "x")]],
     result(2, {"x": 3}, [rd("B", 1, "x", 2), rd("A", 2, "x", 3), rd("B", 1, "x", 2)])),
    ("transaction and key namespaces are separate", [{"X": 4},
     [B("X"), R("X", "X"), E({"X": 5}), R("X", "X")]],
     result(1, {"X": 5}, [rd("X", 0, "X", 4), rd("X", 0, "X", 4)])),
    ("case-sensitive sorted scans and thresholds", [{"a": 1, "A": 2, "b": -3},
     [B("T", "rc"), S("T", -3), S("T", 2)]],
     result(0, {"a": 1, "A": 2, "b": -3},
            [sc("T", 0, [("A", 2), ("a", 1), ("b", -3)]), sc("T", 0, [("A", 2)])])),
    ("minimum and maximum stored values", [{"low": -1000, "mid": 0, "high": 1000},
     [B("T", "rc"), S("T", 0), S("T", 1000), R("T", "unknown")]],
     result(0, {"low": -1000, "mid": 0, "high": 1000},
            [sc("T", 0, [("high", 1000), ("mid", 0)]),
             sc("T", 0, [("high", 1000)]), rd("T", 0, "unknown", None)])),
    ("empty commits still count abstract commit events", [{},
     [B("T", "rc"), C("T"), E({}), B("U"), R("U", "z"), A("U")]],
     result(2, {}, [rd("U", 2, "z", None)])),
    ("successive private updates preserve own visibility", [{"a": 0},
     [B("T"), W("T", "a", 1), R("T", "a"), W("T", "a", 2),
      R("T", "a"), C("T"), B("U", "rc"), R("U", "a")]],
     result(1, {"a": 2}, [rd("T", 0, "a", 1), rd("T", 0, "a", 2), rd("U", 1, "a", 2)])),
    ("private update followed by delete", [{"a": 0},
     [B("T", "rc"), W("T", "a", 1), W("T", "a", None), E({"b": 2}),
      R("T", "a"), C("T")]],
     result(2, {"b": 2}, [rd("T", 1, "a", None)])),
    ("own row addition changes scan while external addition stays hidden", [{"a": 1},
     [B("T"), S("T"), E({"b": 2}), W("T", "c", 3), S("T"), C("T")]],
     result(2, {"a": 1, "b": 2, "c": 3},
            [sc("T", 0, [("a", 1)]), sc("T", 0, [("a", 1), ("c", 3)])])),
]
KEYS = list("abcdefgh")
CASES.append(("eight key boundary", [{key: i for i, key in enumerate(KEYS)},
              [B("T", "rc"), S("T"), E({key: 100 + i for i, key in enumerate(KEYS)}), S("T")]],
              result(1, {key: 100 + i for i, key in enumerate(KEYS)},
                     [sc("T", 0, list(zip(KEYS, range(8)))),
                      sc("T", 1, list(zip(KEYS, range(100, 108))))])))
TXS = ["T" + str(i) for i in range(8)]
CASES.append(("eight independent transaction boundary", [{"a": 0},
              [B(tx) for tx in TXS] + [E({"a": 1})] + [R(tx, "a") for tx in TXS] + [C(tx) for tx in TXS]],
              result(9, {"a": 1}, [rd(tx, 1, "a", 1) for tx in TXS])))
CASES.append(("sixty-four commit event boundary", [{"a": 0}, [E({"a": i}) for i in range(1, 65)]],
              result(64, {"a": 64})))
CASES.append(("sixty-four event read prefix", [{"a": 1}, [B("T")] + [R("T", "a") for _ in range(63)]],
              result(0, {"a": 1}, [rd("T", 0, "a", 1) for _ in range(63)])))
CALLS = CASES + [CASES[3], CASES[0], CASES[12], CASES[3], CASES[0]]


def run(candidate):
    payload = base64.b64encode(json.dumps([args for _, args, _ in CALLS]).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
def fingerprint(v):
    if type(v) is dict and all(type(k) is str for k in v):
        return ("dict",tuple((k,fingerprint(v[k])) for k in sorted(v)))
    if type(v) is list:
        return ("list",tuple(fingerprint(x) for x in v))
    if type(v) in (str,int,type(None)):
        return (type(v).__name__,v)
    raise TypeError("unsupported native type")
def containers(v):
    if type(v) is dict:
        yield id(v)
        for x in v.values(): yield from containers(x)
    elif type(v) is list:
        yield id(v)
        for x in v: yield from containers(x)
values=[];retained=[];output_ids=set();saved=[];independent=True;unchanged=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args);retained.append((supplied,fingerprint(supplied)))
    value=module.snapshot_views(*supplied);before=fingerprint(value)
    ids=list(containers(value))
    independent=independent and len(ids)==len(set(ids)) and not bool(set(ids)&output_ids)
    output_ids.update(ids);values.append(value);saved.append(before)
    unchanged=unchanged and all(fingerprint(old)==snap for old,snap in retained)
    unchanged=unchanged and all(fingerprint(old)==snap for old,snap in zip(values,saved))
input_ids=set()
for args,_ in retained: input_ids.update(containers(args))
independent=independent and not bool(output_ids & input_ids)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged,"independent":independent}))'''
    try:
        process = subprocess.run([sys.executable, "-B", "-c", runner,
                                  str(pathlib.Path(candidate).resolve()), payload],
                                 capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        if process.returncode or not lines:
            return False, "candidate execution or nonnative output"
        value = json.loads(lines[-1])
        if value.get("unchanged") is not True:
            return False, "input or prior-output mutation"
        if value.get("independent") is not True:
            return False, "mutable aliasing"
        outputs = value.get("values")
        if type(outputs) is not list or len(outputs) != len(CALLS):
            return False, "output count"
        for (label, _, expected), actual in zip(CALLS, outputs):
            if json.dumps(actual, sort_keys=True) != json.dumps(expected, sort_keys=True):
                return False, label
        return True, str(len(CALLS)) + " deterministic calls"
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False, "candidate execution"


if __name__ == "__main__":
    passed, detail = run(sys.argv[1]) if len(sys.argv) == 2 else (False, "candidate path required")
    print(("PASS: " if passed else "FAIL: ") + detail)
    sys.exit(0 if passed else 1)
