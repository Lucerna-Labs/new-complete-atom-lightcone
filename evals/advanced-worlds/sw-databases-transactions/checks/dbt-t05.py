import base64
import json
import pathlib
import subprocess
import sys


def value(sequence, text):
    return {"sequence": sequence, "kind": "value", "value": text}


def deletion(sequence):
    return {"sequence": sequence, "kind": "delete", "value": None}


def answer(horizon, kept, dropped=()):
    return {"horizon": horizon, "kept": kept,
            "dropped": [{"sequence": s, "reason": reason} for s, reason in dropped]}


# Literal decisions; these helpers only construct records, never run retention
# tests. The maximum-length cases state closed-form all-kept/all-shadowed sets.
CASES = [
    ("empty default", [[], 0], answer(0, [])),
    ("empty explicit snapshot list", [[], 100, []], answer(100, [])),
    ("empty with live snapshots", [[], 100, [90, 40]], answer(40, [])),
    ("single value at horizon", [[value(5, "x")], 5], answer(5, [value(5, "x")])),
    ("unshadowed deletion without deeper range", [[deletion(5)], 5], answer(5, [], [(5, "obsolete_deletion")])),
    ("deeper range protects newest deletion", [[deletion(5)], 5, None, True], answer(5, [deletion(5)])),
    ("old snapshot protects future deletion", [[deletion(5)], 5, [4]], answer(4, [deletion(5)])),
    ("deletion equality uses inclusive horizon", [[deletion(5)], 5, [5]], answer(5, [], [(5, "obsolete_deletion")])),
    ("no snapshots hides older value", [[value(10, "new"), value(5, "old")], 10],
     answer(10, [value(10, "new")], [(5, "shadowed")])),
    ("old snapshot needs older value", [[value(10, "new"), value(5, "old")], 10, [7]],
     answer(7, [value(10, "new"), value(5, "old")])),
    ("value exactly at oldest snapshot remains", [[value(10, "new"), value(5, "old")], 10, [5]],
     answer(5, [value(10, "new"), value(5, "old")])),
    ("snapshot older than every version", [[value(10, "new"), value(5, "old")], 10, [4]],
     answer(4, [value(10, "new"), value(5, "old")])),
    ("newer equality makes shadowing safe", [[value(10, "new"), value(5, "old")], 10, [10]],
     answer(10, [value(10, "new")], [(5, "shadowed")])),
    ("conservative retention of all versions above horizon", [[value(12, "v12"), value(10, "v10"), value(5, "v5")], 12, [7]],
     answer(7, [value(12, "v12"), value(10, "v10"), value(5, "v5")])),
    ("first below-horizon value shadows the remaining suffix", [[value(12, "v12"), value(10, "v10"), value(5, "v5"), value(3, "v3")], 12, [7]],
     answer(7, [value(12, "v12"), value(10, "v10"), value(5, "v5")], [(3, "shadowed")])),
    ("new deletion and two values preserved for oldest snapshot", [[deletion(12), value(9, "new"), value(4, "old")], 12, [6]],
     answer(6, [deletion(12), value(9, "new"), value(4, "old")])),
    ("dropped newest tombstone still shadows following values", [[deletion(10), value(5, "old")], 12],
     answer(12, [], [(10, "obsolete_deletion"), (5, "shadowed")])),
    ("retained tombstone hides old value even with deeper overlap", [[deletion(10), value(5, "old")], 12, None, True],
     answer(12, [deletion(10)], [(5, "shadowed")])),
    ("shadowed tombstone needs no base-level proof", [[value(11, "new"), deletion(10), value(5, "old")], 12, None, True],
     answer(12, [value(11, "new")], [(10, "shadowed"), (5, "shadowed")])),
    ("otherwise-unshadowed middle deletion protected by range", [[value(13, "new"), deletion(10), value(5, "old")], 13, [12], True],
     answer(12, [value(13, "new"), deletion(10)], [(5, "shadowed")])),
    ("otherwise-unshadowed middle deletion safely dropped", [[value(13, "new"), deletion(10), value(5, "old")], 13, [12], False],
     answer(12, [value(13, "new")], [(10, "obsolete_deletion"), (5, "shadowed")])),
    ("older-entry rule wins reason when both qualify", [[value(11, "new"), deletion(10)], 12],
     answer(12, [value(11, "new")], [(10, "shadowed")])),
    ("two deletions advance preceding sequence after dropping", [[deletion(11), deletion(10)], 12],
     answer(12, [], [(11, "obsolete_deletion"), (10, "shadowed")])),
    ("deeper overlap does not keep a shadowed second deletion", [[deletion(11), deletion(10)], 12, None, True],
     answer(12, [deletion(11)], [(10, "shadowed")])),
    ("unordered duplicate snapshot sequences use minimum", [[value(10, "new"), value(5, "old")], 12, [12, 7, 12]],
     answer(7, [value(10, "new"), value(5, "old")])),
    ("empty string is a value not a deletion", [[value(10, ""), value(5, "old")], 10],
     answer(10, [value(10, "")], [(5, "shadowed")])),
    ("printable payload preserved without normalization", [[value(1000000, " ~! ")], 1000000, [0]],
     answer(0, [value(1000000, " ~! ")])),
    ("maximum payload length", [[value(1, "x" * 32)], 1, [0]], answer(0, [value(1, "x" * 32)])),
    ("maximum snapshot count", [[value(15, "new"), value(10, "old"), deletion(5)], 20, [10] * 16],
     answer(10, [value(15, "new"), value(10, "old")], [(5, "shadowed")])),
    ("zero snapshot protects earliest deletion", [[deletion(1)], 1, [0]], answer(0, [deletion(1)])),
    ("maximum records all above horizon", [[value(s, "v") for s in range(64, 0, -1)], 64, [0]],
     answer(0, [value(s, "v") for s in range(64, 0, -1)])),
    ("maximum records current-only suffix removal", [[value(s, "v") for s in range(64, 0, -1)], 64],
     answer(64, [value(64, "v")], [(s, "shadowed") for s in range(63, 0, -1)])),
]
CALLS = CASES + [CASES[19], CASES[0], CASES[3], CASES[19], CASES[18]]
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
    value=module.compact_key(*supplied)
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
