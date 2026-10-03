import base64
import json
import pathlib
import subprocess
import sys


def machine(registers=None, stack=None):
    return {"registers": {} if registers is None else registers, "stack": [] if stack is None else stack}


def metadata(pc, values):
    return {"pc": pc, "locals": values}


def constant(value):
    return {"kind": "constant", "value": value}


def reg(name, format="u32"):
    return {"kind": "register", "name": name, "format": format}


def slot(index, format="u32"):
    return {"kind": "stack", "slot": index, "format": format}


def remat(left, right):
    return {"kind": "add", "left": left, "right": right}


def add(local, delta):
    return {"op": "add", "local": local, "delta": delta}


def emit(local, label):
    return {"op": "emit", "local": local, "label": label}


def effect(label, value):
    return {"label": label, "value": value}


def snap(pc, values=None, effects=()):
    return {"pc": pc, "locals": {} if values is None else values, "effects": list(effects)}


U = 2**32 - 1
M = -(2**31)
# Hand-authored checkpoint states; helpers format literals without interpreting
# recipes or running source instructions.
CASES = [
    ("empty", [machine(), metadata(0, {}), [], []], [snap(0)]),
    ("constant without execution", [machine(), metadata(0, {"x": constant(7)}), [], []], [snap(0, {"x": 7})]),
    ("unsigned register", [machine({"r": U}), metadata(0, {"x": reg("r")}), [], []], [snap(0, {"x": U})]),
    ("signed register", [machine({"r": U}), metadata(0, {"x": reg("r", "i32")}), [], []], [snap(0, {"x": -1})]),
    ("same word signed and unsigned", [machine({"r": 2**31}), metadata(0, {"x": reg("r", "i32"), "y": reg("r")}), [], []], [snap(0, {"x": M, "y": 2**31})]),
    ("signed positive boundary and zero", [machine({"a": 2**31 - 1, "z": 0}), metadata(0, {"x": reg("a", "i32"), "z": reg("z", "i32")}), [], []], [snap(0, {"x": 2**31 - 1, "z": 0})]),
    ("stack slot index and format", [machine(stack=[17, U]), metadata(0, {"x": slot(1, "i32"), "y": slot(0)}), [], []], [snap(0, {"x": -1, "y": 17})]),
    ("mixed leaves and pure addition recipes", [machine({"r": 5}, [88, U]), metadata(0, {"a": constant(-3), "b": reg("r"), "c": slot(1, "i32"), "d": remat(reg("r"), constant(-3)), "e": remat(slot(1, "i32"), reg("r"))}), [], []], [snap(0, {"a": -3, "b": 5, "c": -1, "d": 2, "e": 4})]),
    ("register and local namespaces differ", [machine({"x": 99, "X": 4}, [8]), metadata(0, {"x": slot(0), "X": reg("X")}), [emit("x", "x"), emit("X", "X")], []], [snap(0, {"x": 8, "X": 4}), snap(1, {"x": 8, "X": 4}, [effect("x", 8)]), snap(2, {"x": 8, "X": 4}, [effect("x", 8), effect("X", 4)])]),
    ("source add does not wrap", [machine({"r": U}), metadata(0, {"x": reg("r")}), [add("x", 1), emit("x", "answer")], []], [snap(0, {"x": U}), snap(1, {"x": 2**32}), snap(2, {"x": 2**32}, [effect("answer", 2**32)])]),
    ("source negative add does not wrap", [machine({"r": 2**31}), metadata(0, {"x": reg("r", "i32")}), [add("x", -1)], []], [snap(0, {"x": M}), snap(1, {"x": M - 1})]),
    ("prior effects are preserved", [machine(), metadata(0, {"x": constant(7)}), [emit("x", "after")], [effect("before", 9)]], [snap(0, {"x": 7}, [effect("before", 9)]), snap(1, {"x": 7}, [effect("before", 9), effect("after", 7)])]),
    ("repeated labels are distinct effects", [machine(), metadata(0, {"x": constant(2)}), [emit("x", "same"), emit("x", "same")], [effect("same", 1)]], [snap(0, {"x": 2}, [effect("same", 1)]), snap(1, {"x": 2}, [effect("same", 1), effect("same", 2)]), snap(2, {"x": 2}, [effect("same", 1), effect("same", 2), effect("same", 2)])]),
    ("resume after committed emit", [machine({"r": 5}), metadata(1, {"x": reg("r")}), [emit("x", "before"), add("x", 2), emit("x", "after")], [effect("before", 5)]], [snap(1, {"x": 5}, [effect("before", 5)]), snap(2, {"x": 7}, [effect("before", 5)]), snap(3, {"x": 7}, [effect("before", 5), effect("after", 7)])]),
    ("resume after completed add", [machine(stack=[8]), metadata(1, {"x": slot(0)}), [add("x", 3), emit("x", "v")], []], [snap(1, {"x": 8}), snap(2, {"x": 8}, [effect("v", 8)])]),
    ("resume after two effects on state", [machine(), metadata(2, {"x": constant(8)}), [add("x", 3), emit("x", "v"), add("x", -2), emit("x", "v")], [effect("v", 8)]], [snap(2, {"x": 8}, [effect("v", 8)]), snap(3, {"x": 6}, [effect("v", 8)]), snap(4, {"x": 6}, [effect("v", 8), effect("v", 6)])]),
    ("already completed program", [machine(), metadata(2, {"x": constant(8)}), [add("x", 3), emit("x", "v")], [effect("v", 8)]], [snap(2, {"x": 8}, [effect("v", 8)])]),
    ("updates affect only the named local", [machine(), metadata(0, {"x": constant(1), "y": constant(-2)}), [add("x", 4), emit("y", "y"), add("y", -3), emit("x", "x")], []], [snap(0, {"x": 1, "y": -2}), snap(1, {"x": 5, "y": -2}), snap(2, {"x": 5, "y": -2}, [effect("y", -2)]), snap(3, {"x": 5, "y": -5}, [effect("y", -2)]), snap(4, {"x": 5, "y": -5}, [effect("y", -2), effect("x", 5)])]),
    ("unused checkpoint storage is not a local", [machine({"unused": 99, "r": 2}, [77]), metadata(0, {"x": reg("r")}), [], []], [snap(0, {"x": 2})]),
    ("decode before rematerializing", [machine({"r": U}), metadata(0, {"x": remat(reg("r", "i32"), reg("r", "u32"))}), [], []], [snap(0, {"x": U - 1})]),
    ("rematerialization has no u32 truncation", [machine(stack=[U]), metadata(0, {"x": remat(slot(0), constant(U))}), [], []], [snap(0, {"x": 2 * U})]),
    ("checkpoint between identical emits", [machine(), metadata(1, {"x": constant(4)}), [emit("x", "v"), emit("x", "v"), add("x", 1)], [effect("v", 4)]], [snap(1, {"x": 4}, [effect("v", 4)]), snap(2, {"x": 4}, [effect("v", 4), effect("v", 4)]), snap(3, {"x": 5}, [effect("v", 4), effect("v", 4)])]),
    ("recipe order is not source execution", [machine({"a": 9}), metadata(0, {"z": remat(reg("a"), constant(-2)), "a": constant(3)}), [emit("z", "z"), emit("a", "a")], []], [snap(0, {"z": 7, "a": 3}), snap(1, {"z": 7, "a": 3}, [effect("z", 7)]), snap(2, {"z": 7, "a": 3}, [effect("z", 7), effect("a", 3)])]),
    ("zero add still advances continuation", [machine(), metadata(0, {"x": constant(0)}), [add("x", 0)], []], [snap(0, {"x": 0}), snap(1, {"x": 0})]),
]
# Closed-form bounded oracles, not execution of the implementation transition.
CASES.append(("sixteen exact additions", [machine(), metadata(0, {"x": constant(0)}), [add("x", 1000) for _ in range(16)], []], [snap(i, {"x": i * 1000}) for i in range(17)]))
HISTORY = [effect(f"h{i}", (2**40 if i % 2 == 0 else -(2**40))) for i in range(16)]
CASES.append(("sixteen retained historical effects", [machine(), metadata(0, {}), [], HISTORY], [snap(0, effects=HISTORY)]))
CASES.append(("eight locals and checkpoint slots", [machine({f"r{i}": i for i in range(8)}, list(range(8))), metadata(0, {f"x{i}": (reg(f"r{i}") if i < 4 else slot(i)) for i in range(8)}), [], []], [snap(0, {f"x{i}": i for i in range(8)})]))
CASES.append(("input history bound is not an output effect cap",
              [machine(), metadata(0, {"x": constant(7)}), [emit("x", "new")], HISTORY],
              [snap(0, {"x": 7}, HISTORY),
               snap(1, {"x": 7}, HISTORY + [effect("new", 7)])]))
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
    values.append(m.deopt_trace(*supplied))
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
