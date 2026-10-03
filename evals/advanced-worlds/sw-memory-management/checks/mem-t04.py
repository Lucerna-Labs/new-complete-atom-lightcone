import base64
import json
import pathlib
import subprocess
import sys


def alloc(oid, size, nested=0):
    return {"op": "alloc", "id": oid, "size": size, "nested_bytes": nested}


def alias(ref, oid):
    return {"op": "alias", "ref": ref, "object": oid}


def read(ref):
    return {"op": "read", "ref": ref}


def destroy(oid):
    return {"op": "destroy", "object": oid}


def obj(start, size, nested=0, state="live", resource="none"):
    return {"start": start, "size": size, "state": state,
            "nested_bytes": nested, "nested_state": resource}


def snap(op, status, cursor, objects=None, refs=None, log=(), live=0, leaked=0):
    return {"op": op, "status": status, "cursor": cursor,
            "objects": {} if objects is None else objects,
            "refs": {} if refs is None else refs, "destructor_log": list(log),
            "live_nested_bytes": live, "leaked_nested_bytes": leaked}


RESET = {"op": "reset"}

# Literal state and resource oracles. Raw rewind is deliberately not lifetime
# invalidation; only the contract's destruction or incompatible overlap is.
CASES = [
    ("empty raw trace", [8, False, []], []),
    ("one object without nested allocation", [8, False, [alloc("A", 4)]],
     [snap("alloc", "allocated", 4, {"A": obj(0, 4)})]),
    ("one object owns a separate buffer", [8, False, [alloc("A", 4, 8)]],
     [snap("alloc", "allocated", 4, {"A": obj(0, 4, 8, resource="owned")}, live=8)]),
    ("nonowning reference release does not destroy", [8, False,
       [alloc("A", 2, 9), alias("r", "A"), read("r"), {"op": "drop_ref", "ref": "r"}]],
     [snap("alloc", "allocated", 2, {"A": obj(0, 2, 9, resource="owned")}, live=9),
      snap("alias", "aliased", 2, {"A": obj(0, 2, 9, resource="owned")}, {"r": "A"}, live=9),
      snap("read", "valid", 2, {"A": obj(0, 2, 9, resource="owned")}, {"r": "A"}, live=9),
      snap("drop_ref", "released-reference", 2, {"A": obj(0, 2, 9, resource="owned")}, live=9)]),
    ("destruction leaves cursor and expired alias", [8, False,
       [alloc("A", 3, 7), alias("r", "A"), destroy("A"), read("r"), alloc("B", 6, 9)]],
     [snap("alloc", "allocated", 3, {"A": obj(0, 3, 7, resource="owned")}, live=7),
      snap("alias", "aliased", 3, {"A": obj(0, 3, 7, resource="owned")}, {"r": "A"}, live=7),
      snap("destroy", "destroyed", 3, {"A": obj(0, 3, 7, "destroyed", "released")}, {"r": "A"}, ["A"]),
      snap("read", "expired", 3, {"A": obj(0, 3, 7, "destroyed", "released")}, {"r": "A"}, ["A"]),
      snap("alloc", "no-space", 3, {"A": obj(0, 3, 7, "destroyed", "released")}, {"r": "A"}, ["A"])]),
    ("raw rewind alone leaves lifetime and cleanup possible", [8, False,
       [alloc("A", 4, 8), alias("r", "A"), RESET, read("r"), destroy("A"), read("r")]],
     [snap("alloc", "allocated", 4, {"A": obj(0, 4, 8, resource="owned")}, live=8),
      snap("alias", "aliased", 4, {"A": obj(0, 4, 8, resource="owned")}, {"r": "A"}, live=8),
      snap("reset", "reset", 0, {"A": obj(0, 4, 8, resource="owned")}, {"r": "A"}, live=8),
      snap("read", "valid", 0, {"A": obj(0, 4, 8, resource="owned")}, {"r": "A"}, live=8),
      snap("destroy", "destroyed", 0, {"A": obj(0, 4, 8, "destroyed", "released")}, {"r": "A"}, ["A"]),
      snap("read", "expired", 0, {"A": obj(0, 4, 8, "destroyed", "released")}, {"r": "A"}, ["A"])]),
    ("tracking reset ends lifetime immediately", [8, True,
       [alloc("A", 4, 8), alias("r", "A"), RESET, read("r")]],
     [snap("alloc", "allocated", 4, {"A": obj(0, 4, 8, resource="owned")}, live=8),
      snap("alias", "aliased", 4, {"A": obj(0, 4, 8, resource="owned")}, {"r": "A"}, live=8),
      snap("reset", "reset", 0, {"A": obj(0, 4, 8, "destroyed", "released")}, {"r": "A"}, ["A"]),
      snap("read", "expired", 0, {"A": obj(0, 4, 8, "destroyed", "released")}, {"r": "A"}, ["A"])]),
    ("raw reuse leaks former buffer and never retargets alias", [8, False,
       [alloc("A", 4, 10), alias("r", "A"), RESET, alloc("B", 4, 2), read("r"), destroy("B"), RESET]],
     [snap("alloc", "allocated", 4, {"A": obj(0, 4, 10, resource="owned")}, live=10),
      snap("alias", "aliased", 4, {"A": obj(0, 4, 10, resource="owned")}, {"r": "A"}, live=10),
      snap("reset", "reset", 0, {"A": obj(0, 4, 10, resource="owned")}, {"r": "A"}, live=10),
      snap("alloc", "allocated", 4, {"A": obj(0, 4, 10, "reused", "leaked"), "B": obj(0, 4, 2, resource="owned")}, {"r": "A"}, live=12, leaked=10),
      snap("read", "expired", 4, {"A": obj(0, 4, 10, "reused", "leaked"), "B": obj(0, 4, 2, resource="owned")}, {"r": "A"}, live=12, leaked=10),
      snap("destroy", "destroyed", 4, {"A": obj(0, 4, 10, "reused", "leaked"), "B": obj(0, 4, 2, "destroyed", "released")}, {"r": "A"}, ["B"], 10, 10),
      snap("reset", "reset", 0, {"A": obj(0, 4, 10, "reused", "leaked"), "B": obj(0, 4, 2, "destroyed", "released")}, {"r": "A"}, ["B"], 10, 10)]),
    ("tracking reuse has no former nested leak", [8, True,
       [alloc("A", 4, 10), alias("r", "A"), RESET, alloc("B", 4, 2), read("r"), RESET]],
     [snap("alloc", "allocated", 4, {"A": obj(0, 4, 10, resource="owned")}, live=10),
      snap("alias", "aliased", 4, {"A": obj(0, 4, 10, resource="owned")}, {"r": "A"}, live=10),
      snap("reset", "reset", 0, {"A": obj(0, 4, 10, "destroyed", "released")}, {"r": "A"}, ["A"]),
      snap("alloc", "allocated", 4, {"A": obj(0, 4, 10, "destroyed", "released"), "B": obj(0, 4, 2, resource="owned")}, {"r": "A"}, ["A"], 2),
      snap("read", "expired", 4, {"A": obj(0, 4, 10, "destroyed", "released"), "B": obj(0, 4, 2, resource="owned")}, {"r": "A"}, ["A"], 2),
      snap("reset", "reset", 0, {"A": obj(0, 4, 10, "destroyed", "released"), "B": obj(0, 4, 2, "destroyed", "released")}, {"r": "A"}, ["A", "B"])]),
    ("partial overlap ends complete old lifetime", [8, False,
       [alloc("A", 8, 5), alias("r", "A"), RESET, alloc("B", 2), read("r")]],
     [snap("alloc", "allocated", 8, {"A": obj(0, 8, 5, resource="owned")}, live=5),
      snap("alias", "aliased", 8, {"A": obj(0, 8, 5, resource="owned")}, {"r": "A"}, live=5),
      snap("reset", "reset", 0, {"A": obj(0, 8, 5, resource="owned")}, {"r": "A"}, live=5),
      snap("alloc", "allocated", 2, {"A": obj(0, 8, 5, "reused", "leaked"), "B": obj(0, 2)}, {"r": "A"}, live=5, leaked=5),
      snap("read", "expired", 2, {"A": obj(0, 8, 5, "reused", "leaked"), "B": obj(0, 2)}, {"r": "A"}, live=5, leaked=5)]),
    ("touching intervals do not overlap", [8, False,
       [alloc("A", 4, 3), alloc("B", 4, 5), alias("r", "A"), alias("s", "B"), RESET,
        alloc("C", 4), read("r"), read("s"), destroy("B")]],
     [snap("alloc", "allocated", 4, {"A": obj(0, 4, 3, resource="owned")}, live=3),
      snap("alloc", "allocated", 8, {"A": obj(0, 4, 3, resource="owned"), "B": obj(4, 4, 5, resource="owned")}, live=8),
      snap("alias", "aliased", 8, {"A": obj(0, 4, 3, resource="owned"), "B": obj(4, 4, 5, resource="owned")}, {"r": "A"}, live=8),
      snap("alias", "aliased", 8, {"A": obj(0, 4, 3, resource="owned"), "B": obj(4, 4, 5, resource="owned")}, {"r": "A", "s": "B"}, live=8),
      snap("reset", "reset", 0, {"A": obj(0, 4, 3, resource="owned"), "B": obj(4, 4, 5, resource="owned")}, {"r": "A", "s": "B"}, live=8),
      snap("alloc", "allocated", 4, {"A": obj(0, 4, 3, "reused", "leaked"), "B": obj(4, 4, 5, resource="owned"), "C": obj(0, 4)}, {"r": "A", "s": "B"}, live=8, leaked=3),
      snap("read", "expired", 4, {"A": obj(0, 4, 3, "reused", "leaked"), "B": obj(4, 4, 5, resource="owned"), "C": obj(0, 4)}, {"r": "A", "s": "B"}, live=8, leaked=3),
      snap("read", "valid", 4, {"A": obj(0, 4, 3, "reused", "leaked"), "B": obj(4, 4, 5, resource="owned"), "C": obj(0, 4)}, {"r": "A", "s": "B"}, live=8, leaked=3),
      snap("destroy", "destroyed", 4, {"A": obj(0, 4, 3, "reused", "leaked"), "B": obj(4, 4, 5, "destroyed", "released"), "C": obj(0, 4)}, {"r": "A", "s": "B"}, ["B"], 3, 3)]),
    ("one replacement overlaps two old objects", [8, False,
       [alloc("A", 3, 4), alloc("B", 3, 7), RESET, alloc("C", 5, 1)]],
     [snap("alloc", "allocated", 3, {"A": obj(0, 3, 4, resource="owned")}, live=4),
      snap("alloc", "allocated", 6, {"A": obj(0, 3, 4, resource="owned"), "B": obj(3, 3, 7, resource="owned")}, live=11),
      snap("reset", "reset", 0, {"A": obj(0, 3, 4, resource="owned"), "B": obj(3, 3, 7, resource="owned")}, live=11),
      snap("alloc", "allocated", 5, {"A": obj(0, 3, 4, "reused", "leaked"), "B": obj(3, 3, 7, "reused", "leaked"), "C": obj(0, 5, 1, resource="owned")}, live=12, leaked=11)]),
    ("tracking destruction follows reverse allocation not lexical order", [8, True,
       [alloc("Z", 2, 1), alloc("A", 2, 2), alloc("M", 2, 3), RESET]],
     [snap("alloc", "allocated", 2, {"Z": obj(0, 2, 1, resource="owned")}, live=1),
      snap("alloc", "allocated", 4, {"Z": obj(0, 2, 1, resource="owned"), "A": obj(2, 2, 2, resource="owned")}, live=3),
      snap("alloc", "allocated", 6, {"Z": obj(0, 2, 1, resource="owned"), "A": obj(2, 2, 2, resource="owned"), "M": obj(4, 2, 3, resource="owned")}, live=6),
      snap("reset", "reset", 0, {"Z": obj(0, 2, 1, "destroyed", "released"), "A": obj(2, 2, 2, "destroyed", "released"), "M": obj(4, 2, 3, "destroyed", "released")}, log=["M", "A", "Z"])]),
    ("tracking reset skips already destroyed objects", [8, True,
       [alloc("A", 2, 4), alloc("B", 2, 5), alloc("C", 2, 6), destroy("B"), RESET]],
     [snap("alloc", "allocated", 2, {"A": obj(0, 2, 4, resource="owned")}, live=4),
      snap("alloc", "allocated", 4, {"A": obj(0, 2, 4, resource="owned"), "B": obj(2, 2, 5, resource="owned")}, live=9),
      snap("alloc", "allocated", 6, {"A": obj(0, 2, 4, resource="owned"), "B": obj(2, 2, 5, resource="owned"), "C": obj(4, 2, 6, resource="owned")}, live=15),
      snap("destroy", "destroyed", 6, {"A": obj(0, 2, 4, resource="owned"), "B": obj(2, 2, 5, "destroyed", "released"), "C": obj(4, 2, 6, resource="owned")}, log=["B"], live=10),
      snap("reset", "reset", 0, {"A": obj(0, 2, 4, "destroyed", "released"), "B": obj(2, 2, 5, "destroyed", "released"), "C": obj(4, 2, 6, "destroyed", "released")}, log=["B", "C", "A"])]),
    ("repeat tracking reset has no duplicate destruction", [4, True,
       [alloc("A", 2), RESET, RESET, alloc("B", 2), RESET]],
     [snap("alloc", "allocated", 2, {"A": obj(0, 2)}),
      snap("reset", "reset", 0, {"A": obj(0, 2, state="destroyed")}, log=["A"]),
      snap("reset", "reset", 0, {"A": obj(0, 2, state="destroyed")}, log=["A"]),
      snap("alloc", "allocated", 2, {"A": obj(0, 2, state="destroyed"), "B": obj(0, 2)}, log=["A"]),
      snap("reset", "reset", 0, {"A": obj(0, 2, state="destroyed"), "B": obj(0, 2, state="destroyed")}, log=["A", "B"])]),
    ("repeat raw reset is metadata only", [4, False, [alloc("A", 2, 4), RESET, RESET]],
     [snap("alloc", "allocated", 2, {"A": obj(0, 2, 4, resource="owned")}, live=4),
      snap("reset", "reset", 0, {"A": obj(0, 2, 4, resource="owned")}, live=4),
      snap("reset", "reset", 0, {"A": obj(0, 2, 4, resource="owned")}, live=4)]),
    ("failed replacement does not invalidate old object", [4, False,
       [alloc("A", 4, 3), alias("r", "A"), RESET, alloc("B", 5, 9), read("r")]],
     [snap("alloc", "allocated", 4, {"A": obj(0, 4, 3, resource="owned")}, live=3),
      snap("alias", "aliased", 4, {"A": obj(0, 4, 3, resource="owned")}, {"r": "A"}, live=3),
      snap("reset", "reset", 0, {"A": obj(0, 4, 3, resource="owned")}, {"r": "A"}, live=3),
      snap("alloc", "no-space", 0, {"A": obj(0, 4, 3, resource="owned")}, {"r": "A"}, live=3),
      snap("read", "valid", 0, {"A": obj(0, 4, 3, resource="owned")}, {"r": "A"}, live=3)]),
    ("no-space creates no object or nested allocation", [4, False, [alloc("A", 4, 3), alloc("B", 1, 64)]],
     [snap("alloc", "allocated", 4, {"A": obj(0, 4, 3, resource="owned")}, live=3),
      snap("alloc", "no-space", 4, {"A": obj(0, 4, 3, resource="owned")}, live=3)]),
    ("exact end fits again after tracking reset", [4, True,
       [alloc("A", 4, 1), alloc("B", 1), RESET, alloc("C", 4, 2)]],
     [snap("alloc", "allocated", 4, {"A": obj(0, 4, 1, resource="owned")}, live=1),
      snap("alloc", "no-space", 4, {"A": obj(0, 4, 1, resource="owned")}, live=1),
      snap("reset", "reset", 0, {"A": obj(0, 4, 1, "destroyed", "released")}, log=["A"]),
      snap("alloc", "allocated", 4, {"A": obj(0, 4, 1, "destroyed", "released"), "C": obj(0, 4, 2, resource="owned")}, log=["A"], live=2)]),
    ("zero capacity cannot create a positive-size object", [0, True, [alloc("A", 1, 64), RESET, alloc("B", 32)]],
     [snap("alloc", "no-space", 0), snap("reset", "reset", 0), snap("alloc", "no-space", 0)]),
    ("external buffers are not bounded by arena capacity", [64, False,
       [alloc("A", 32, 64), alloc("B", 32, 64), RESET, alloc("C", 32)]],
     [snap("alloc", "allocated", 32, {"A": obj(0, 32, 64, resource="owned")}, live=64),
      snap("alloc", "allocated", 64, {"A": obj(0, 32, 64, resource="owned"), "B": obj(32, 32, 64, resource="owned")}, live=128),
      snap("reset", "reset", 0, {"A": obj(0, 32, 64, resource="owned"), "B": obj(32, 32, 64, resource="owned")}, live=128),
      snap("alloc", "allocated", 32, {"A": obj(0, 32, 64, "reused", "leaked"), "B": obj(32, 32, 64, resource="owned"), "C": obj(0, 32)}, live=128, leaked=64)]),
    ("reuse preserves prior destroyed history", [4, False,
       [alloc("A", 4, 6), destroy("A"), RESET, alloc("B", 4)]],
     [snap("alloc", "allocated", 4, {"A": obj(0, 4, 6, resource="owned")}, live=6),
      snap("destroy", "destroyed", 4, {"A": obj(0, 4, 6, "destroyed", "released")}, log=["A"]),
      snap("reset", "reset", 0, {"A": obj(0, 4, 6, "destroyed", "released")}, log=["A"]),
      snap("alloc", "allocated", 4, {"A": obj(0, 4, 6, "destroyed", "released"), "B": obj(0, 4)}, log=["A"])]),
    ("object and reference namespaces are separate", [4, False,
       [alloc("A", 2), alias("A", "A"), read("A"), {"op": "drop_ref", "ref": "A"}, destroy("A")]],
     [snap("alloc", "allocated", 2, {"A": obj(0, 2)}),
      snap("alias", "aliased", 2, {"A": obj(0, 2)}, {"A": "A"}),
      snap("read", "valid", 2, {"A": obj(0, 2)}, {"A": "A"}),
      snap("drop_ref", "released-reference", 2, {"A": obj(0, 2)}),
      snap("destroy", "destroyed", 2, {"A": obj(0, 2, state="destroyed")}, log=["A"])]),
    ("case-sensitive identities and independent aliases", [4, False,
       [alloc("A", 2, 3), alloc("a", 2, 5), alias("r", "A"), alias("R", "a"), destroy("A"), read("r"), read("R")]],
     [snap("alloc", "allocated", 2, {"A": obj(0, 2, 3, resource="owned")}, live=3),
      snap("alloc", "allocated", 4, {"A": obj(0, 2, 3, resource="owned"), "a": obj(2, 2, 5, resource="owned")}, live=8),
      snap("alias", "aliased", 4, {"A": obj(0, 2, 3, resource="owned"), "a": obj(2, 2, 5, resource="owned")}, {"r": "A"}, live=8),
      snap("alias", "aliased", 4, {"A": obj(0, 2, 3, resource="owned"), "a": obj(2, 2, 5, resource="owned")}, {"r": "A", "R": "a"}, live=8),
      snap("destroy", "destroyed", 4, {"A": obj(0, 2, 3, "destroyed", "released"), "a": obj(2, 2, 5, resource="owned")}, {"r": "A", "R": "a"}, ["A"], 5),
      snap("read", "expired", 4, {"A": obj(0, 2, 3, "destroyed", "released"), "a": obj(2, 2, 5, resource="owned")}, {"r": "A", "R": "a"}, ["A"], 5),
      snap("read", "valid", 4, {"A": obj(0, 2, 3, "destroyed", "released"), "a": obj(2, 2, 5, resource="owned")}, {"r": "A", "R": "a"}, ["A"], 5)]),
]

# Independent closed-form boundary oracle: sixteen one-byte objects fill a
# sixteen-byte region, each with one nested byte, then tracking reset reverses
# their construction order. It uses no implementation transition function.
NAMES = [f"n{i:02}" for i in range(16)]
MAX_EVENTS = [alloc(name, 1, 1) for name in NAMES] + [RESET]
MAX_EXPECTED = [snap("alloc", "allocated", i + 1,
                    {name: obj(j, 1, 1, resource="owned") for j, name in enumerate(NAMES[:i + 1])},
                    live=i + 1) for i in range(16)]
MAX_EXPECTED.append(snap("reset", "reset", 0,
                         {name: obj(j, 1, 1, "destroyed", "released") for j, name in enumerate(NAMES)},
                         log=list(reversed(NAMES))))
CASES.append(("all sixteen registrations must be destroyed", [16, True, MAX_EVENTS], MAX_EXPECTED))
CASES.extend([CASES[7], CASES[0]])


def native_types(value):
    if type(value) is dict:
        if any(type(k) is not str for k in value):
            return ["unsupported-dict-key"]
        return ["dict", [[k, native_types(value[k])] for k in sorted(value)]]
    if type(value) is list:
        return ["list", [native_types(v) for v in value]]
    if value is None:
        return "none"
    if type(value) is bool:
        return "bool"
    if type(value) is int:
        return "int"
    if type(value) is str:
        return "str"
    return ["unsupported", type(value).__name__]


def run(candidate):
    payload = base64.b64encode(json.dumps([args for _, args, _ in CASES]).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
def native_types(value):
    if type(value) is dict:
        if any(type(k) is not str for k in value): return ["unsupported-dict-key"]
        return ["dict",[[k,native_types(value[k])] for k in sorted(value)]]
    if type(value) is list: return ["list",[native_types(v) for v in value]]
    if value is None: return "none"
    if type(value) is bool: return "bool"
    if type(value) is int: return "int"
    if type(value) is str: return "str"
    return ["unsupported",type(value).__name__]
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
def mutable_ids(value, seen=None):
    if seen is None: seen=set()
    if type(value) not in (dict,list) or id(value) in seen: return seen
    seen.add(id(value))
    for child in (value.values() if type(value) is dict else value):
        mutable_ids(child,seen)
    return seen
values=[];input_history=[];unchanged=True;independent=True;seen_outputs=set()
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args)
    input_history.append((supplied,json.dumps(supplied,sort_keys=True),native_types(supplied)))
    result=m.arena_lifetimes(*supplied)
    values.append(result)
    # Retain every argument and check it after later calls as well as its own.
    for prior,before,types in input_history:
        unchanged=unchanged and json.dumps(prior,sort_keys=True)==before and native_types(prior)==types
    # Mutable containers may be reused inside one snapshot, but never across
    # independent snapshots/calls. Keep outer trace lists separate as well.
    groups=[{id(result)}] if type(result) is list else []
    if type(result) is list: groups.extend(mutable_ids(snapshot) for snapshot in result)
    for identities in groups:
        independent=independent and not (identities & seen_outputs)
        seen_outputs.update(identities)
print("__RESULT__"+json.dumps({"values":values,"types":[native_types(v) for v in values],"unchanged":unchanged,"independent":independent}))'''
    try:
        process = subprocess.run([sys.executable, "-B", "-c", runner,
                                  str(pathlib.Path(candidate).resolve()), payload],
                                 capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if process.returncode == 0 and lines else None
        wanted = [value for _, _, value in CASES]
        expected = {"values": wanted, "types": [native_types(v) for v in wanted], "unchanged": True, "independent": True}
        return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return False


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
