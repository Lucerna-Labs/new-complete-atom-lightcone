import base64
import json
import pathlib
import subprocess
import sys


def history(rows):
    return [{"tx": tx, "kind": kind, "key": key} for tx, kind, key in rows]


def answer(edges, order):
    return {"edges": [list(edge) for edge in edges],
            "acyclic": order is not None, "order": order}


# All edge sets and canonical orders below are hand specified. The helpers
# format literals; they do not derive conflicts or run a graph algorithm.
CASES = [
    ("empty default", [[]], answer([], [])),
    ("empty explicit None", [[], None], answer([], [])),
    ("empty explicit operations", [[], []], answer([], [])),
    ("isolated default vertices sorted", [["z", "a"]], answer([], ["a", "z"])),
    ("isolated explicit None vertices", [["B", "A"], None], answer([], ["A", "B"])),
    ("one transaction never conflicts with itself", [["A"], history([
        ("A", "write", "x"), ("A", "read", "x"), ("A", "write", "x")])], answer([], ["A"])),
    ("read read creates no edge", [["B", "A"], history([
        ("A", "read", "x"), ("B", "read", "x")])], answer([], ["A", "B"])),
    ("read before write", [["A", "B"], history([
        ("A", "read", "x"), ("B", "write", "x")])], answer([("A", "B")], ["A", "B"])),
    ("write before read with reversed names", [["A", "B"], history([
        ("B", "write", "x"), ("A", "read", "x")])], answer([("B", "A")], ["B", "A"])),
    ("write before write", [["B", "A"], history([
        ("A", "write", "x"), ("B", "write", "x")])], answer([("A", "B")], ["A", "B"])),
    ("different keys do not conflict", [["B", "A"], history([
        ("A", "write", "x"), ("B", "write", "y")])], answer([], ["A", "B"])),
    ("key case matters", [["B", "A"], history([
        ("A", "write", "x"), ("B", "read", "X")])], answer([], ["A", "B"])),
    ("a read gap does not hide earlier write", [["C", "B", "A"], history([
        ("A", "write", "x"), ("B", "read", "x"), ("C", "read", "x")])],
     answer([("A", "B"), ("A", "C")], ["A", "B", "C"])),
    ("same transaction interposition cannot hide conflict", [["A", "B"], history([
        ("A", "write", "x"), ("A", "read", "x"), ("B", "read", "x")])],
     answer([("A", "B")], ["A", "B"])),
    ("nonadjacent conflict closes a real precedence cycle", [["A", "B", "C"], history([
        ("A", "write", "x"), ("B", "read", "x"), ("C", "read", "x"),
        ("C", "write", "y"), ("A", "read", "y")])],
     answer([("A", "B"), ("A", "C"), ("C", "A")], None)),
    ("blind write cycle concerns conflict equivalence only", [["A", "B"], history([
        ("A", "write", "x"), ("B", "write", "x"), ("A", "write", "x")])],
     answer([("A", "B"), ("B", "A")], None)),
    ("transitive edges must still be returned", [["C", "A", "B"], history([
        ("A", "write", "x"), ("B", "write", "x"), ("C", "write", "x")])],
     answer([("A", "B"), ("A", "C"), ("B", "C")], ["A", "B", "C"])),
    ("duplicate conflict witnesses make one edge", [["A", "B"], history([
        ("A", "write", "x"), ("B", "read", "x"), ("A", "write", "y"), ("B", "read", "y")])],
     answer([("A", "B")], ["A", "B"])),
    ("lexical choice is made at each Kahn step", [["C", "B", "A"], history([
        ("C", "write", "x"), ("A", "read", "x")])], answer([("C", "A")], ["B", "C", "A"])),
    ("newly available small vertex precedes old ready vertex", [["A", "B", "C"], history([
        ("B", "write", "x"), ("A", "read", "x")])], answer([("B", "A")], ["B", "A", "C"])),
    ("disconnected cycle discards partial ordering", [["A", "B", "C"], history([
        ("A", "write", "x"), ("B", "write", "x"), ("A", "write", "x")])],
     answer([("A", "B"), ("B", "A")], None)),
    ("three-transaction cycle", [["A", "B", "C"], history([
        ("A", "write", "x"), ("B", "read", "x"), ("B", "write", "y"),
        ("C", "read", "y"), ("C", "write", "z"), ("A", "read", "z")])],
     answer([("A", "B"), ("B", "C"), ("C", "A")], None)),
    ("ASCII identifiers are opaque", [["f2", "f10", "a", "A"]], answer([], ["A", "a", "f10", "f2"])),
    ("maximum vertices and identifier length", [["H", "G", "F", "E", "D", "C", "B", "A123456789012345"], []],
     answer([], ["A123456789012345", "B", "C", "D", "E", "F", "G", "H"])),
    ("maximum operations with many identical witnesses", [["A", "B"],
      history([("A", "read", "x")] * 32 + [("B", "write", "x")] * 32)],
     answer([("A", "B")], ["A", "B"])),
    ("sixteen independent keys share the same edge", [["A", "B"],
      history([row for i in range(16) for row in [("A", "write", "k" + str(i)), ("B", "read", "k" + str(i))]])],
     answer([("A", "B")], ["A", "B"])),
]
CALLS = CASES + [CASES[14], CASES[0], CASES[4], CASES[14], CASES[18]]
EXPECTED = [value for _, _, value in CALLS]

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
    value=module.precedence_graph(*supplied)
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
