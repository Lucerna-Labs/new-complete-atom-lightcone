import base64
import json
import pathlib
import subprocess
import sys


def item(kind, name):
    return {"kind": kind, "type": name}


def function(kind, arg, result):
    return {"kind": kind, "arg": arg, "result": result}


def table(*rows):
    assert all(set(row) <= {"0", "1"} for row in rows)
    return [[cell == "1" for cell in row] for row in rows]


PARENTS = {"Animal": [], "Dog": ["Animal"], "Cat": ["Animal"],
           "Poodle": ["Dog"], "Rock": []}
NAMES = ["Animal", "Dog", "Cat", "Poodle", "Rock"]
INPUTS = ["Animal", "Dog", "Cat", "Rock"]
PROP_ARGS = [function("property", name, "Animal") for name in INPUTS]
METHOD_ARGS = [function("method", name, "Animal") for name in INPUTS]
PROP_RETURNS = [function("property", "Animal", name) for name in NAMES]
METHOD_RETURNS = [function("method", "Animal", name) for name in NAMES]
PROP_MIXED = [function("property", a, r) for a, r in
              [("Animal", "Animal"), ("Animal", "Dog"), ("Dog", "Animal"), ("Dog", "Dog")]]
METHOD_MIXED = [function("method", a, r) for a, r in
                [("Animal", "Animal"), ("Animal", "Dog"), ("Dog", "Animal"), ("Dog", "Dog")]]
KINDS = [item(k, "Animal") for k in ("value", "producer", "consumer", "cell")] + [
    function("property", "Animal", "Animal"), function("method", "Animal", "Animal")]
DIAMOND = {"Top": [], "Left": ["Top"], "Right": ["Top"],
           "Bottom": ["Left", "Right"], "Alone": []}
DIAMOND_VALUES = [item("value", n) for n in ["Top", "Left", "Right", "Bottom", "Alone"]]
# Matrices below are literal truth tables. table() only decodes written bits;
# it does not traverse the subtype graph or implement a variance rule.
CASES = [
    ("entirely empty", [{}, [], []], []),
    ("no sources", [PARENTS, [], [item("value", "Animal")]], []),
    ("independent empty rows", [PARENTS, [item("value", "Animal"), item("value", "Dog")], []], [[], []]),
    ("ordinary reflexive transitive subtyping", [PARENTS, [item("value", n) for n in NAMES], [item("value", n) for n in NAMES]], table("10000", "11000", "10100", "11010", "00001")),
    ("producer covariance", [PARENTS, [item("producer", n) for n in NAMES], [item("producer", n) for n in NAMES]], table("10000", "11000", "10100", "11010", "00001")),
    ("consumer contravariance", [PARENTS, [item("consumer", n) for n in NAMES], [item("consumer", n) for n in NAMES]], table("11110", "01010", "00100", "00010", "00001")),
    ("cell invariance", [PARENTS, [item("cell", n) for n in NAMES], [item("cell", n) for n in NAMES]], table("10000", "01000", "00100", "00010", "00001")),
    ("strict property inputs", [PARENTS, PROP_ARGS, PROP_ARGS], table("1110", "0100", "0010", "0001")),
    ("method exception under default strictness", [PARENTS, METHOD_ARGS, METHOD_ARGS], table("1110", "1100", "1010", "0001")),
    ("nonstrict property inputs", [PARENTS, PROP_ARGS, PROP_ARGS, False], table("1110", "1100", "1010", "0001")),
    ("nonstrict method inputs", [PARENTS, METHOD_ARGS, METHOD_ARGS, False], table("1110", "1100", "1010", "0001")),
    ("strict property results remain covariant", [PARENTS, PROP_RETURNS, PROP_RETURNS, True], table("10000", "11000", "10100", "11010", "00001")),
    ("method results remain covariant", [PARENTS, METHOD_RETURNS, METHOD_RETURNS, True], table("10000", "11000", "10100", "11010", "00001")),
    ("both strict function positions matter", [PARENTS, PROP_MIXED, PROP_MIXED, True], table("1010", "1111", "0010", "0011")),
    ("method input exception does not erase result check", [PARENTS, METHOD_MIXED, METHOD_MIXED, True], table("1010", "1111", "1010", "1111")),
    ("constructor kinds are disjoint in this model", [PARENTS, KINDS, KINDS], table("100000", "010000", "001000", "000100", "000010", "000001")),
    ("both branches of a subtype diamond", [DIAMOND, DIAMOND_VALUES, DIAMOND_VALUES], table("10000", "11000", "10100", "11110", "00001")),
    ("case-sensitive type identities", [{"Node": [], "node": []}, [item("value", "Node"), item("value", "node")], [item("value", "Node"), item("value", "node")]], table("10", "01")),
    ("source and target order is preserved", [PARENTS, [item("value", "Rock"), item("value", "Dog")], [item("value", n) for n in ["Cat", "Animal", "Rock", "Dog"]]], table("0010", "0101")),
    ("no implicit Object supertype", [{"Object": [], "Dog": []}, [item("value", "Dog")], [item("value", "Object")]], table("0")),
]
# Two bounded analytic fixtures: a linear eight-type hierarchy is a finite
# total order; twelve identical method descriptors give twelve independent rows.
CHAIN = {f"T{i}": ([f"T{i-1}"] if i else []) for i in range(8)}
CHAIN_VALUES = [item("value", f"T{i}") for i in range(8)]
CASES.append(("eight-type transitive depth", [CHAIN, CHAIN_VALUES, CHAIN_VALUES],
              table("10000000", "11000000", "11100000", "11110000", "11111000", "11111100", "11111110", "11111111")))
CASES.append(("maximum matrix dimensions and independent equal rows", [PARENTS,
              [function("method", "Dog", "Animal") for _ in range(12)],
              [function("method", "Animal", "Animal") for _ in range(12)]],
              table(*(["111111111111"] * 12))))
CASES.extend([CASES[0], CASES[8], CASES[0]])

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

def mutable_ids(value, seen=None):
    if seen is None: seen=set()
    if type(value) not in (dict,list) or id(value) in seen: return seen
    seen.add(id(value))
    for child in (value.values() if type(value) is dict else value): mutable_ids(child,seen)
    return seen

def independent_outputs(values, forbidden):
    seen=set(forbidden)
    def visit(value):
        if type(value) not in (dict,list): return True
        if id(value) in seen: return False
        seen.add(id(value))
        return all(visit(child) for child in (value.values() if type(value) is dict else value))
    return all(visit(value) for value in values)

spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
values=[];output_history=[];inputs=[];input_ids=set();unchanged=True;independent=True;stable=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args)
    inputs.append((supplied,json.dumps(supplied,sort_keys=True),native_types(supplied)))
    input_ids.update(mutable_ids(supplied))
    result=m.assignability_matrix(*supplied)
    values.append(result)
    result_types=native_types(result)
    output_history.append((json.dumps(result,sort_keys=True),result_types))
    for prior,(before,types) in zip(values,output_history):
        stable=stable and json.dumps(prior,sort_keys=True)==before and native_types(prior)==types
    for prior,before,types in inputs:
        unchanged=unchanged and json.dumps(prior,sort_keys=True)==before and native_types(prior)==types
    independent=independent and independent_outputs(values,input_ids)
print("__RESULT__"+json.dumps({"values":values,"types":[native_types(v) for v in values],"unchanged":unchanged,"independent":independent,"stable":stable}))'''
    try:
        process = subprocess.run([sys.executable, "-B", "-c", runner,
                                  str(pathlib.Path(candidate).resolve()), payload],
                                 capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if process.returncode == 0 and lines else None
        wanted = [value for _, _, value in CASES]
        expected = {"values": wanted, "types": [native_types(v) for v in wanted],
                    "unchanged": True, "independent": True, "stable": True}
        return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return False


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
