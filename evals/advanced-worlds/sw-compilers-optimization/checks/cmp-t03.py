import base64
import json
import pathlib
import subprocess
import sys


def group(indices, inputs, outputs):
    return {"indices": indices, "inputs": inputs, "outputs": outputs}


def step(index, value, output):
    return {"index": index, "input": value, "output": output}


def result(path, memory, groups=(), steps=(), tail=0):
    return {"path": path, "memory": memory, "vector_groups": list(groups),
            "scalar_steps": list(steps), "tail_count": tail}


U = 2**32 - 1
# Independent hand traces; helpers format supplied values, not transitions.
CASES = [
    ("empty default", [[], 0, 0, 0], result("vector", [])),
    ("zero at one-past", [[9, 8], 2, 2, 0], result("vector", [9, 8])),
    ("zero unequal offsets", [[9, 8, 7], 0, 2, 0, 8], result("vector", [9, 8, 7])),
    ("one default tail", [[9, 4], 0, 1, 1], result("vector", [5, 4], steps=[step(0, 4, 5)], tail=1)),
    ("one reverse", [[9, 4], 1, 0, 1, 4], result("vector", [9, 10], steps=[step(0, 9, 10)], tail=1)),
    ("equal single", [[7], 0, 0, 1], result("scalar", [8], steps=[step(0, 7, 8)])),
    ("adjacent width two", [[10, 20, 0, 0], 2, 0, 2, 2], result("vector", [10, 20, 11, 21], [group([0, 1], [10, 20], [11, 21])])),
    ("two full groups", [[1, 2, 3, 4, 9, 9, 9, 9], 4, 0, 4, 2], result("vector", [1, 2, 3, 4, 2, 3, 4, 5], [group([0, 1], [1, 2], [2, 3]), group([2, 3], [3, 4], [4, 5])])),
    ("group plus tail", [[1, 2, 3, 9, 9, 9], 3, 0, 3, 2], result("vector", [1, 2, 3, 2, 3, 4], [group([0, 1], [1, 2], [2, 3])], [step(2, 3, 4)], 1)),
    ("all tail is still vector arm", [[1, 2, 3, 9, 9, 9], 3, 0, 3, 8], result("vector", [1, 2, 3, 2, 3, 4], steps=[step(0, 1, 2), step(1, 2, 3), step(2, 3, 4)], tail=3)),
    ("width one emits groups", [[1, 2, 3, 9, 9, 9], 3, 0, 3, 1], result("vector", [1, 2, 3, 2, 3, 4], [group([0], [1], [2]), group([1], [2], [3]), group([2], [3], [4])])),
    ("full group wraps", [[0, U, U - 1, 2, 9, 9, 9, 9], 4, 0, 4], result("vector", [0, U, U - 1, 2, 1, 0, U, 3], [group([0, 1, 2, 3], [0, U, U - 1, 2], [1, 0, U, 3])])),
    ("default width remainder", [[0, 1, 2, 3, 4, 9, 9, 9, 9, 9], 5, 0, 5], result("vector", [0, 1, 2, 3, 4, 1, 2, 3, 4, 5], [group([0, 1, 2, 3], [0, 1, 2, 3], [1, 2, 3, 4])], [step(4, 4, 5)], 1)),
    ("forward overlap recurrence", [[0, 0, 0, 0], 1, 0, 3, 2], result("scalar", [0, 1, 2, 3], steps=[step(0, 0, 1), step(1, 1, 2), step(2, 2, 3)])),
    ("reverse overlap conservative fallback", [[1, 2, 3, 4], 0, 1, 3, 2], result("scalar", [3, 4, 5, 4], steps=[step(0, 2, 3), step(1, 3, 4), step(2, 4, 5)])),
    ("equal multi-element ranges", [[10, 20, 30], 0, 0, 3, 2], result("scalar", [11, 21, 31], steps=[step(0, 10, 11), step(1, 20, 21), step(2, 30, 31)])),
    ("wrapped recurrence", [[U, 0, 0, 0], 1, 0, 3, 2], result("scalar", [U, 0, 1, 2], steps=[step(0, U, 0), step(1, 0, 1), step(2, 1, 2)])),
    ("two-element overlap distance", [[4, 8, 1, 2, 3, 4], 2, 0, 4, 4], result("scalar", [4, 8, 5, 9, 6, 10], steps=[step(0, 4, 5), step(1, 8, 9), step(2, 5, 6), step(3, 9, 10)])),
    ("reverse two-element overlap", [[4, 8, 1, 2, 3, 4], 0, 2, 4, 4], result("scalar", [2, 3, 4, 5, 3, 4], steps=[step(0, 1, 2), step(1, 2, 3), step(2, 3, 4), step(3, 4, 5)])),
    ("untouched surrounding storage", [[99, 1, 2, 3, 77, 0, 0, 0, 88], 5, 1, 3, 2], result("vector", [99, 1, 2, 3, 77, 2, 3, 4, 88], [group([0, 1], [1, 2], [2, 3])], [step(2, 3, 4)], 1)),
    ("untouched range gap", [[10, 0, 55, 20], 1, 3, 1], result("vector", [10, 21, 55, 20], steps=[step(0, 20, 21)], tail=1)),
    ("equal width-one fallback", [[U, 4], 0, 0, 2, 1], result("scalar", [0, 5], steps=[step(0, U, 0), step(1, 4, 5)])),
    ("adjacency reversed", [[9, 9, 9, 5, 6, 7], 0, 3, 3, 2], result("vector", [6, 7, 8, 5, 6, 7], [group([0, 1], [5, 6], [6, 7])], [step(2, 7, 8)], 1)),
    ("nonpower width three", [[1, 2, 3, 4, 0, 0, 0, 0], 4, 0, 4, 3], result("vector", [1, 2, 3, 4, 2, 3, 4, 5], [group([0, 1, 2], [1, 2, 3], [2, 3, 4])], [step(3, 4, 5)], 1)),
    ("scalar tail wraps", [[4, U, 0, 0], 2, 0, 2, 8], result("vector", [4, U, 5, 0], steps=[step(0, 4, 5), step(1, U, 0)], tail=2)),
]
# Closed-form boundary oracle: the source is its own index sequence, the output
# sequence is one greater. Two groups cover the sixteen-element upper bound.
CASES.append(("maximum count and storage", [list(range(16)) + [0] * 16, 16, 0, 16, 8],
              result("vector", list(range(16)) + list(range(1, 17)),
                     [group(list(range(8)), list(range(8)), list(range(1, 9))),
                      group(list(range(8, 16)), list(range(8, 16)), list(range(9, 17)))])))
CASES.extend([CASES[13], CASES[0]])


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
values=[];inputs=[];input_ids=set();unchanged=True;independent=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args)
    inputs.append((supplied,json.dumps(supplied,sort_keys=True),native_types(supplied)))
    input_ids.update(mutable_ids(supplied))
    values.append(m.guarded_vector_add(*supplied))
    for prior,before,types in inputs:
        unchanged=unchanged and json.dumps(prior,sort_keys=True)==before and native_types(prior)==types
    independent=independent and independent_outputs(values,input_ids)
print("__RESULT__"+json.dumps({"values":values,"types":[native_types(v) for v in values],"unchanged":unchanged,"independent":independent}))'''
    try:
        process = subprocess.run([sys.executable, "-B", "-c", runner,
                                  str(pathlib.Path(candidate).resolve()), payload],
                                 capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if process.returncode == 0 and lines else None
        wanted = [value for _, _, value in CASES]
        expected = {"values": wanted, "types": [native_types(v) for v in wanted],
                    "unchanged": True, "independent": True}
        return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return False


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
