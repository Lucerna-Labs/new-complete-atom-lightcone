"""Literal cache-state traces and independent closed-form geometry fixtures."""
import base64
from copy import deepcopy
import json
import pathlib
import subprocess
import sys


def fixture(label, addresses, states, line_bytes=16, set_count=2, ways=1, defaults=False):
    assert len(addresses) == len(states)
    rows = []
    previous_reference = []
    counts = {key: 0 for key in ("hit", "compulsory", "conflict", "capacity")}
    for address, (cache, reference, classification, evicted) in zip(addresses, states):
        block = address // line_bytes
        counts[classification] += 1
        rows.append({"address": address, "block": block, "set": block % set_count,
                     "tag": block // set_count, "hit": classification == "hit",
                     "reference_hit": block in previous_reference,
                     "classification": classification, "evicted": evicted,
                     "cache": deepcopy(cache), "reference": list(reference)})
        previous_reference = reference
    misses = len(addresses) - counts["hit"]
    final_cache = states[-1][0] if states else [[] for _ in range(set_count)]
    final_reference = states[-1][1] if states else []
    expected = {"hits": counts["hit"], "misses": misses,
                "compulsory": counts["compulsory"], "conflict": counts["conflict"],
                "capacity": counts["capacity"], "transferred_bytes": misses * line_bytes,
                "cache": deepcopy(final_cache), "reference": list(final_reference), "trace": rows}
    args = [addresses] if defaults else [addresses, line_bytes, set_count, ways]
    return label, args, expected


# Each cache/reference sequence below is written by hand. fixture() formats
# these supplied states; it never runs a replacement or reference-cache policy.
CASES = [
    fixture("empty default geometry", [], [], defaults=True),
    fixture("one cold demand", [0], [
        ([[0], []], [0], "compulsory", None)], defaults=True),
    fixture("same byte line reused", [0, 15, 1], [
        ([[0], []], [0], "compulsory", None),
        ([[0], []], [0], "hit", None),
        ([[0], []], [0], "hit", None)], defaults=True),
    fixture("direct mapped conflict trace", [0, 32, 0], [
        ([[0], []], [0], "compulsory", None),
        ([[2], []], [0, 2], "compulsory", 0),
        ([[0], []], [2, 0], "conflict", 2)]),
    fixture("fully associative capacity trace", [0, 1, 2, 0], [
        ([[0]], [0], "compulsory", None),
        ([[0, 1]], [0, 1], "compulsory", None),
        ([[1, 2]], [1, 2], "compulsory", 0),
        ([[2, 0]], [2, 0], "capacity", 1)], 1, 1, 2),
    fixture("actual hit while equal-capacity reference misses", [0, 1, 3, 0], [
        ([[0], []], [0], "compulsory", None),
        ([[0], [1]], [0, 1], "compulsory", None),
        ([[0], [3]], [1, 3], "compulsory", 1),
        ([[0], [3]], [3, 0], "hit", None)], 1, 2, 1),
    fixture("fully associative fitting set", [0, 1, 2, 0, 1, 2], [
        ([[0]], [0], "compulsory", None),
        ([[0, 1]], [0, 1], "compulsory", None),
        ([[0, 1, 2]], [0, 1, 2], "compulsory", None),
        ([[1, 2, 0]], [1, 2, 0], "hit", None),
        ([[2, 0, 1]], [2, 0, 1], "hit", None),
        ([[0, 1, 2]], [0, 1, 2], "hit", None)], 1, 1, 3),
    fixture("hit refreshes actual and reference LRU", [0, 1, 0, 2, 1], [
        ([[0]], [0], "compulsory", None),
        ([[0, 1]], [0, 1], "compulsory", None),
        ([[1, 0]], [1, 0], "hit", None),
        ([[0, 2]], [0, 2], "compulsory", 1),
        ([[2, 1]], [2, 1], "capacity", 0)], 1, 1, 2),
    fixture("set-local LRU and fitting reference", [0, 2, 0, 4, 2], [
        ([[0], []], [0], "compulsory", None),
        ([[0, 2], []], [0, 2], "compulsory", None),
        ([[2, 0], []], [2, 0], "hit", None),
        ([[0, 4], []], [2, 0, 4], "compulsory", 2),
        ([[4, 2], []], [0, 4, 2], "conflict", 0)], 1, 2, 2),
    fixture("reference hit during actual miss still refreshes recency", [0, 2, 0, 1, 2], [
        ([[0], []], [0], "compulsory", None),
        ([[2], []], [0, 2], "compulsory", 0),
        ([[0], []], [2, 0], "conflict", 2),
        ([[0], [1]], [0, 1], "compulsory", None),
        ([[2], [1]], [1, 2], "capacity", 0)], 1, 2, 1),
    fixture("offset and tag identities", [0, 3, 16, 7, 0], [
        ([[0], [], [], []], [0], "compulsory", None),
        ([[0], [], [], []], [0], "hit", None),
        ([[4], [], [], []], [0, 4], "compulsory", 0),
        ([[4], [1], [], []], [0, 4, 1], "compulsory", None),
        ([[0], [1], [], []], [4, 1, 0], "conflict", 4)], 4, 4, 1),
    fixture("minimal one-slot geometry", [0, 0, 1, 0], [
        ([[0]], [0], "compulsory", None),
        ([[0]], [0], "hit", None),
        ([[1]], [1], "compulsory", 0),
        ([[0]], [0], "capacity", 1)], 1, 1, 1),
    fixture("maximum byte address and same-line offsets", [4095, 4080, 4094], [
        ([[], [], [], [], [], [], [], [255]], [255], "compulsory", None),
        ([[], [], [], [], [], [], [], [255]], [255], "hit", None),
        ([[], [], [], [], [], [], [], [255]], [255], "hit", None)], 16, 8, 4),
]
for size in (1, 2, 4, 8, 16):
    CASES.append(fixture("line boundary size " + str(size),
        [size - 1, size, 2 * size - 1, size - 1], [
            ([[0], []], [0], "compulsory", None),
            ([[0], [1]], [0, 1], "compulsory", None),
            ([[0], [1]], [0, 1], "hit", None),
            ([[0], [1]], [1, 0], "hit", None)], size, 2, 1))

# Closed-form oracle for ascending distinct blocks: all references are first
# references. Each set retains its latest 'ways' members of an arithmetic
# progression, and the reference retains the last capacity consecutive blocks.
def ascending_fixture(label, sets, ways, length, size=4):
    capacity = sets * ways
    states = []
    for block in range(length):
        cache = [list(range(index, block + 1, sets))[-ways:] for index in range(sets)]
        reference = list(range(max(0, block - capacity + 1), block + 1))
        evicted = block - capacity if block >= capacity else None
        states.append((cache, reference, "compulsory", evicted))
    return fixture(label, [block * size for block in range(length)], states, size, sets, ways)

for sets in (1, 2, 4, 8):
    for ways in (1, 2, 3, 4):
        CASES.append(ascending_fixture("geometry " + str(sets) + "/" + str(ways),
                                      sets, ways, sets * ways + 2))
CASES.append(ascending_fixture("maximum demand count", 8, 4, 64, 16))
CALLS = CASES + [CASES[3], CASES[0], CASES[5], CASES[8], CASES[0]]


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
    if type(v) in (str,int,bool,type(None)):
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
    value=module.cache_trace(*supplied);before=fingerprint(value)
    ids=list(containers(value))
    independent=independent and len(ids)==len(set(ids)) and not bool(set(ids)&output_ids)
    output_ids.update(ids);values.append(value);saved.append(before)
    unchanged=unchanged and all(fingerprint(old)==snap for old,snap in retained)
    unchanged=unchanged and all(fingerprint(old)==snap for old,snap in zip(values,saved))
input_ids=set()
for args,_ in retained: input_ids.update(containers(args))
independent=independent and not bool(output_ids & input_ids)
fingerprint(values)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged,"independent":independent}))'''
    try:
        p = subprocess.run([sys.executable, "-B", "-c", runner,
                            str(pathlib.Path(candidate).resolve()), payload],
                           capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in p.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        if p.returncode or not lines:
            return False, "candidate execution or nonnative output"
        result = json.loads(lines[-1])
        if result.get("unchanged") is not True:
            return False, "input or prior-output mutation"
        if result.get("independent") is not True:
            return False, "mutable aliasing"
        outputs = result.get("values")
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
