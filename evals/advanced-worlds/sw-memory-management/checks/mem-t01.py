"""Independent literal allocator traces with bounded candidate execution."""
import base64
import json
import pathlib
import subprocess
import sys


def alloc(identifier, size, alignment=1):
    return {"op": "alloc", "id": identifier, "size": size, "align": alignment}


def release(identifier):
    return {"op": "free", "id": identifier}


def block(begin, end, payload, size):
    return {"extent": [begin, end], "payload": payload, "size": size}


def snap(event, status, address, free, live):
    return {"op": event["op"], "id": event["id"], "status": status,
            "address": address, "free": free, "live": live}


A4, A8, A16 = alloc("A", 4), alloc("A", 8), alloc("A", 16)
A25 = alloc("A", 25, 16)
FA, FB = release("A"), release("B")
# The expected snapshots are stated directly, without running the reference.
CASES = [
    ("empty events", [[[100, 180]], 8, []], []),
    ("empty free map", [[], 0, [alloc("A", 1)]],
     [snap(alloc("A", 1), "failed", None, [], {})]),
    ("zero is a valid model address", [[[0, 16]], 0, [A4]],
     [snap(A4, "allocated", 0, [[4, 16]], {"A": block(0, 4, 0, 4)})]),
    ("exact extent exhaustion", [[[0, 16]], 0, [A16]],
     [snap(A16, "allocated", 0, [], {"A": block(0, 16, 0, 16)})]),
    ("header then payload alignment", [[[100, 180]], 8, [A25]],
     [snap(A25, "allocated", 112, [[137, 180]], {"A": block(100, 137, 112, 25)})]),
    ("payload and header fit but padding does not", [[[100, 136]], 8, [A25]],
     [snap(A25, "failed", None, [[100, 136]], {})]),
    ("failed request leaves the extent for a smaller request",
     [[[100, 136]], 8, [A25, alloc("B", 24, 16)]],
     [snap(A25, "failed", None, [[100, 136]], {}),
      snap(alloc("B", 24, 16), "allocated", 112, [], {"B": block(100, 136, 112, 24)})]),
    ("first fitting address not input order",
     [[[64, 100], [0, 8], [24, 48]], 0, [alloc("A", 16, 16)]],
     [snap(alloc("A", 16, 16), "allocated", 32, [[0, 8], [64, 100]],
           {"A": block(24, 48, 32, 16)})]),
    ("header alone prevents a fit", [[[0, 8]], 8, [alloc("A", 1)]],
     [snap(alloc("A", 1), "failed", None, [[0, 8]], {})]),
    ("alignment can skip a positive free interval",
     [[[1, 8], [16, 32]], 0, [alloc("A", 1, 8)]],
     [snap(alloc("A", 1, 8), "allocated", 16, [[1, 8], [17, 32]],
           {"A": block(16, 17, 16, 1)})]),
    ("release bridges both neighboring extents",
     [[[0, 64]], 0, [A16, alloc("B", 16), FA, FB, alloc("C", 64)]],
     [snap(A16, "allocated", 0, [[16, 64]], {"A": block(0, 16, 0, 16)}),
      snap(alloc("B", 16), "allocated", 16, [[32, 64]],
           {"A": block(0, 16, 0, 16), "B": block(16, 32, 16, 16)}),
      snap(FA, "freed", None, [[0, 16], [32, 64]], {"B": block(16, 32, 16, 16)}),
      snap(FB, "freed", None, [[0, 64]], {}),
      snap(alloc("C", 64), "allocated", 0, [], {"C": block(0, 64, 0, 64)})]),
    ("release joins the following remainder", [[[0, 32]], 0, [A8, FA]],
     [snap(A8, "allocated", 0, [[8, 32]], {"A": block(0, 8, 0, 8)}),
      snap(FA, "freed", None, [[0, 32]], {})]),
    ("release restores header and padding too",
     [[[100, 180]], 8, [A25, FA, alloc("B", 60, 16)]],
     [snap(A25, "allocated", 112, [[137, 180]], {"A": block(100, 137, 112, 25)}),
      snap(FA, "freed", None, [[100, 180]], {}),
      snap(alloc("B", 60, 16), "allocated", 112, [[172, 180]],
           {"B": block(100, 172, 112, 60)})]),
    ("coalescing cannot bridge unavailable positions",
     [[[0, 8], [16, 24]], 0, [A8, alloc("B", 8), FA, FB, alloc("C", 12)]],
     [snap(A8, "allocated", 0, [[16, 24]], {"A": block(0, 8, 0, 8)}),
      snap(alloc("B", 8), "allocated", 16, [],
           {"A": block(0, 8, 0, 8), "B": block(16, 24, 16, 8)}),
      snap(FA, "freed", None, [[0, 8]], {"B": block(16, 24, 16, 8)}),
      snap(FB, "freed", None, [[0, 8], [16, 24]], {}),
      snap(alloc("C", 12), "failed", None, [[0, 8], [16, 24]], {})]),
    ("initial intervals are transitively normalized",
     [[[16, 24], [0, 8], [8, 16]], 0, [alloc("A", 24), FA]],
     [snap(alloc("A", 24), "allocated", 0, [], {"A": block(0, 24, 0, 24)}),
      snap(FA, "freed", None, [[0, 24]], {})]),
    ("maximum header and requested alignment",
     [[[1, 256]], 16, [alloc("A", 128, 128)]],
     [snap(alloc("A", 128, 128), "allocated", 128, [], {"A": block(1, 256, 128, 128)})]),
    ("upper endpoint and one-past aligned failure",
     [[[4095, 4096]], 0, [alloc("A", 1), FA, alloc("B", 1, 128)]],
     [snap(alloc("A", 1), "allocated", 4095, [], {"A": block(4095, 4096, 4095, 1)}),
      snap(FA, "freed", None, [[4095, 4096]], {}),
      snap(alloc("B", 1, 128), "failed", None, [[4095, 4096]], {})]),
    ("first fit is not best fit",
     [[[0, 64], [128, 144]], 0, [A16]],
     [snap(A16, "allocated", 0, [[16, 64], [128, 144]], {"A": block(0, 16, 0, 16)})]),
    ("one-byte remainder stays available",
     [[[3, 13]], 0, [alloc("A", 9), alloc("a", 1)]],
     [snap(alloc("A", 9), "allocated", 3, [[12, 13]], {"A": block(3, 12, 3, 9)}),
      snap(alloc("a", 1), "allocated", 12, [],
           {"A": block(3, 12, 3, 9), "a": block(12, 13, 12, 1)})]),
    ("failure preserves a live allocation",
     [[[0, 16]], 0, [A8, alloc("B", 9), FA]],
     [snap(A8, "allocated", 0, [[8, 16]], {"A": block(0, 8, 0, 8)}),
      snap(alloc("B", 9), "failed", None, [[8, 16]], {"A": block(0, 8, 0, 8)}),
      snap(FA, "freed", None, [[0, 16]], {})]),
]
CALLS = CASES + [CASES[10], CASES[0], CASES[4], CASES[0]]


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
def mutable_ids(v):
    if type(v) is dict:
        return {id(v)}.union(*(mutable_ids(x) for x in v.values()))
    if type(v) is list:
        return {id(v)}.union(*(mutable_ids(x) for x in v))
    return set()
values=[];retained=[];seen=set();separate=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args)
    retained.append((supplied,fingerprint(supplied)))
    result=module.allocator_trace(*supplied)
    fingerprint(result)
    if type(result) is not list: raise TypeError("trace must be a native list")
    separate=separate and id(result) not in seen;seen.add(id(result))
    for snapshot in result:
        ids=mutable_ids(snapshot);separate=separate and not bool(ids & seen);seen.update(ids)
    values.append(result)
unchanged=all(fingerprint(args)==before for args,before in retained)
for value in values: fingerprint(value)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged,"separate":separate}))'''
    try:
        p = subprocess.run([sys.executable, "-B", "-c", runner,
                            str(pathlib.Path(candidate).resolve()), payload],
                           capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in p.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        if p.returncode or not lines:
            return False, "candidate execution"
        result = json.loads(lines[-1])
        if result.get("unchanged") is not True:
            return False, "input mutation"
        if result.get("separate") is not True:
            return False, "shared mutable snapshots or call results"
        values = result.get("values")
        if type(values) is not list or len(values) != len(CALLS):
            return False, "output count"
        for (name, _, expected), value in zip(CALLS, values):
            if json.dumps(value, sort_keys=True) != json.dumps(expected, sort_keys=True):
                return False, name
        return True, str(len(CALLS)) + " deterministic calls"
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False, "candidate execution"


if __name__ == "__main__":
    ok, detail = run(sys.argv[1]) if len(sys.argv) == 2 else (False, "candidate path required")
    print(("PASS: " if ok else "FAIL: ") + detail)
    sys.exit(0 if ok else 1)
