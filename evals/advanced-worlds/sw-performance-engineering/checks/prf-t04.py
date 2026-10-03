import base64
import json
import pathlib
import subprocess
import sys


def pair(value):
    return [value, 1] if type(value) is int else list(value)


def frame(name, inclusive, own, inclusive_fraction, self_fraction):
    return {"frame": name, "inclusive": inclusive, "self": own,
            "inclusive_fraction": pair(inclusive_fraction),
            "self_fraction": pair(self_fraction)}


def result(count, frames, majority=None):
    return {"sample_count": count, "frames": frames, "majority_hotspot": majority}


# Hand counts and reduced fractions. Helpers only format explicitly supplied
# results; they do not count stacks, deduplicate recursion or select a majority.
CASES = [
    ("empty", [[]], result(0, [])),
    ("single leaf", [[['main']]], result(1, [frame('main', 1, 1, 1, 1)], 'main')),
    ("caller is not the leaf", [[['root', 'a']]], result(1, [frame('a', 1, 1, 1, 1), frame('root', 1, 0, 1, 0)], 'a')),
    ("three recursive occurrences count once", [[['f', 'f', 'f']]], result(1, [frame('f', 1, 1, 1, 1)], 'f')),
    ("recursive primary example", [[['main', 'a', 'a'], ['main', 'a', 'b'], ['main', 'b']]],
     result(3, [frame('a', 2, 1, (2, 3), (1, 3)), frame('b', 2, 2, (2, 3), (2, 3)), frame('main', 3, 0, 1, 0)], 'b')),
    ("nonadjacent recursive frame", [[['f', 'g', 'f']]], result(1, [frame('f', 1, 1, 1, 1), frame('g', 1, 0, 1, 0)], 'f')),
    ("two equal leaf shares have no strict majority", [[['root', 'a'], ['root', 'b']]], result(2, [frame('a', 1, 1, (1, 2), (1, 2)), frame('b', 1, 1, (1, 2), (1, 2)), frame('root', 2, 0, 1, 0)])),
    ("three unrelated leaves", [[['a'], ['b'], ['c']]], result(3, [frame('a', 1, 1, (1, 3), (1, 3)), frame('b', 1, 1, (1, 3), (1, 3)), frame('c', 1, 1, (1, 3), (1, 3))])),
    ("duplicate samples retain their separate weights", [[['root', 'a'], ['root', 'a']]], result(2, [frame('a', 2, 2, 1, 1), frame('root', 2, 0, 1, 0)], 'a')),
    ("recursive ancestor is not a self majority", [[['root', 'root', 'a'], ['root', 'b'], ['root', 'a']]], result(3, [frame('a', 2, 2, (2, 3), (2, 3)), frame('b', 1, 1, (1, 3), (1, 3)), frame('root', 3, 0, 1, 0)], 'a')),
    ("ordered stack ends in b", [[['a', 'b']]], result(1, [frame('a', 1, 0, 1, 0), frame('b', 1, 1, 1, 1)], 'b')),
    ("reversing a stack changes only self attribution", [[['b', 'a']]], result(1, [frame('a', 1, 1, 1, 1), frame('b', 1, 0, 1, 0)], 'a')),
    ("case-sensitive frames and ASCII order", [[['a'], ['A']]], result(2, [frame('A', 1, 1, (1, 2), (1, 2)), frame('a', 1, 1, (1, 2), (1, 2))])),
    ("lexical rather than numeric suffix ordering", [[['f2'], ['f10']]], result(2, [frame('f10', 1, 1, (1, 2), (1, 2)), frame('f2', 1, 1, (1, 2), (1, 2))])),
    ("largest share of exactly one half is not majority", [[['a'], ['a'], ['b'], ['c']]], result(4, [frame('a', 2, 2, (1, 2), (1, 2)), frame('b', 1, 1, (1, 4), (1, 4)), frame('c', 1, 1, (1, 4), (1, 4))])),
    ("three of five is strict majority", [[['a'], ['a'], ['a'], ['b'], ['c']]], result(5, [frame('a', 3, 3, (3, 5), (3, 5)), frame('b', 1, 1, (1, 5), (1, 5)), frame('c', 1, 1, (1, 5), (1, 5))], 'a')),
    ("two of five can tie without any majority", [[['a'], ['a'], ['b'], ['b'], ['c']]], result(5, [frame('a', 2, 2, (2, 5), (2, 5)), frame('b', 2, 2, (2, 5), (2, 5)), frame('c', 1, 1, (1, 5), (1, 5))])),
    ("inclusive root dominance is not leaf dominance", [[['root', 'a'], ['root', 'b'], ['root', 'c']]], result(3, [frame('a', 1, 1, (1, 3), (1, 3)), frame('b', 1, 1, (1, 3), (1, 3)), frame('c', 1, 1, (1, 3), (1, 3)), frame('root', 3, 0, 1, 0)])),
    ("a caller can also execute as a leaf", [[['root'], ['root', 'a'], ['root', 'a']]], result(3, [frame('a', 2, 2, (2, 3), (2, 3)), frame('root', 3, 1, 1, (1, 3))], 'a')),
    ("recursive caller has mixed own execution", [[['x', 'y', 'x'], ['x', 'y']]], result(2, [frame('x', 2, 1, 1, (1, 2)), frame('y', 2, 1, 1, (1, 2))])),
    ("each sample has its own recursion set", [[['a', 'a'], ['b', 'b'], ['a', 'b', 'a']]], result(3, [frame('a', 2, 2, (2, 3), (2, 3)), frame('b', 2, 1, (2, 3), (1, 3))], 'a')),
]
# Closed-form domain boundaries, with literal count/fraction consequences.
CASES.append(("maximum recursive depth", [[['deep'] * 16]], result(1, [frame('deep', 1, 1, 1, 1)], 'deep')))
CASES.append(("maximum sample count", [[['root', 'leaf'] for _ in range(64)]], result(64, [frame('leaf', 64, 64, 1, 1), frame('root', 64, 0, 1, 0)], 'leaf')))
NAMES = [f'f{i:02}' for i in range(32)]
CASES.append(("maximum distinct IDs", [[[name] for name in NAMES]], result(32, [frame(name, 1, 1, (1, 32), (1, 32)) for name in NAMES])))
CASES.append(("all three size bounds together", [[NAMES[:16] for _ in range(32)] + [NAMES[16:] for _ in range(32)]],
              result(64, [frame(name, 32, 32 if name in ('f15', 'f31') else 0, (1, 2), (1, 2) if name in ('f15', 'f31') else 0) for name in NAMES])))
CASES.extend([CASES[0], CASES[4], CASES[0]])

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
    result=m.stack_attribution(*supplied)
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
