import base64
import json
import pathlib
import subprocess
import sys


def new(allocation="A", strong="s"):
    return {"op": "new", "allocation": allocation, "strong": strong}


def clone(source, handle):
    return {"op": "clone", "source": source, "handle": handle}


def down(strong="s", weak="w"):
    return {"op": "downgrade", "strong": strong, "weak": weak}


def up(weak="w", strong="u"):
    return {"op": "upgrade", "weak": weak, "strong": strong}


def act(op, handle):
    return {"op": op, "handle": handle}


def out(handle, token):
    return {"op": "into_raw", "handle": handle, "token": token}


def restore(token, handle):
    return {"op": "from_raw", "token": token, "handle": handle}


def a(s, w=0, fs=0, fw=0, alive=True, backing=True, d=0):
    return {"strong": s, "weak": w, "forgotten_strong": fs, "forgotten_weak": fw,
            "value_alive": alive, "backing_alive": backing, "destructions": d}


def strong(allocation="A"):
    return {"kind": "strong", "allocation": allocation}


def weak(allocation="A"):
    return {"kind": "weak", "allocation": allocation}


def snap(op, allocations=None, handles=None, raw=None, upgrade=None):
    return {"op": op, "upgrade_succeeded": upgrade,
            "allocations": {} if allocations is None else allocations,
            "handles": {} if handles is None else handles,
            "raw": {} if raw is None else raw}


# Literal ownership and lifetime states. Helpers only format supplied values;
# they do not infer liveness from a counter or execute a reference transition.
CASES = [
    ("empty", [[]], []),
    ("one allocation", [[new()]], [snap("new", {"A": a(1)}, {"s": strong()})]),
    ("last strong without weak releases both lifetimes", [[new(), act("drop", "s")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("drop", {"A": a(0, alive=False, backing=False, d=1)})]),
    ("strong clone shares allocation", [[new(), clone("s", "t"), act("drop", "s"), act("drop", "t")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("clone", {"A": a(2)}, {"s": strong(), "t": strong()}),
      snap("drop", {"A": a(1)}, {"t": strong()}),
      snap("drop", {"A": a(0, alive=False, backing=False, d=1)})]),
    ("downgrade leaves strong count unchanged", [[new(), down()]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("downgrade", {"A": a(1, 1)}, {"s": strong(), "w": weak()})]),
    ("weak retains only backing after final strong", [[new(), down(), act("drop", "s"), up(), act("drop", "w")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("downgrade", {"A": a(1, 1)}, {"s": strong(), "w": weak()}),
      snap("drop", {"A": a(0, 1, alive=False, d=1)}, {"w": weak()}),
      snap("upgrade", {"A": a(0, 1, alive=False, d=1)}, {"w": weak()}, upgrade=False),
      snap("drop", {"A": a(0, alive=False, backing=False, d=1)})]),
    ("weak release while strong survives", [[new(), down(), act("drop", "w"), act("drop", "s")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("downgrade", {"A": a(1, 1)}, {"s": strong(), "w": weak()}),
      snap("drop", {"A": a(1)}, {"s": strong()}),
      snap("drop", {"A": a(0, alive=False, backing=False, d=1)})]),
    ("upgrade adds a real strong owner", [[new(), down(), up("w", "t"), act("drop", "s"), act("drop", "w"), act("drop", "t")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("downgrade", {"A": a(1, 1)}, {"s": strong(), "w": weak()}),
      snap("upgrade", {"A": a(2, 1)}, {"s": strong(), "w": weak(), "t": strong()}, upgrade=True),
      snap("drop", {"A": a(1, 1)}, {"w": weak(), "t": strong()}),
      snap("drop", {"A": a(1)}, {"t": strong()}),
      snap("drop", {"A": a(0, alive=False, backing=False, d=1)})]),
    ("weak clone retains a second backing contribution", [[new(), down(), clone("w", "v"), act("drop", "s"), act("drop", "w"), up("v", "u"), act("drop", "v")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("downgrade", {"A": a(1, 1)}, {"s": strong(), "w": weak()}),
      snap("clone", {"A": a(1, 2)}, {"s": strong(), "w": weak(), "v": weak()}),
      snap("drop", {"A": a(0, 2, alive=False, d=1)}, {"w": weak(), "v": weak()}),
      snap("drop", {"A": a(0, 1, alive=False, d=1)}, {"v": weak()}),
      snap("upgrade", {"A": a(0, 1, alive=False, d=1)}, {"v": weak()}, upgrade=False),
      snap("drop", {"A": a(0, alive=False, backing=False, d=1)})]),
    ("empty weak clone upgrade drop and forget allocate nothing", [[{"op": "empty_weak", "weak": "w"}, up(), clone("w", "v"), act("drop", "w"), act("forget", "v")]],
     [snap("empty_weak", handles={"w": weak(None)}),
      snap("upgrade", handles={"w": weak(None)}, upgrade=False),
      snap("clone", handles={"w": weak(None), "v": weak(None)}),
      snap("drop", handles={"v": weak(None)}), snap("forget")]),
    ("empty weak raw round trip", [[{"op": "empty_weak", "weak": "w"}, out("w", "r"), restore("r", "v"), up("v", "u"), act("drop", "v")]],
     [snap("empty_weak", handles={"w": weak(None)}),
      snap("into_raw", raw={"r": weak(None)}),
      snap("from_raw", handles={"v": weak(None)}),
      snap("upgrade", handles={"v": weak(None)}, upgrade=False), snap("drop")]),
    ("strong raw ownership does not decrement count", [[new(), out("s", "r"), restore("r", "t"), act("drop", "t")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("into_raw", {"A": a(1)}, raw={"r": strong()}),
      snap("from_raw", {"A": a(1)}, {"t": strong()}),
      snap("drop", {"A": a(0, alive=False, backing=False, d=1)})]),
    ("raw strong enables weak upgrade without a visible strong handle", [[new(), down(), out("s", "r"), up("w", "t"), act("drop", "t"), act("drop", "w"), restore("r", "u"), act("drop", "u")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("downgrade", {"A": a(1, 1)}, {"s": strong(), "w": weak()}),
      snap("into_raw", {"A": a(1, 1)}, {"w": weak()}, {"r": strong()}),
      snap("upgrade", {"A": a(2, 1)}, {"w": weak(), "t": strong()}, {"r": strong()}, True),
      snap("drop", {"A": a(1, 1)}, {"w": weak()}, {"r": strong()}),
      snap("drop", {"A": a(1)}, raw={"r": strong()}),
      snap("from_raw", {"A": a(1)}, {"u": strong()}),
      snap("drop", {"A": a(0, alive=False, backing=False, d=1)})]),
    ("raw weak retains backing and restores after value destruction", [[new(), down(), out("w", "r"), act("drop", "s"), restore("r", "v"), up("v", "u"), act("drop", "v")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("downgrade", {"A": a(1, 1)}, {"s": strong(), "w": weak()}),
      snap("into_raw", {"A": a(1, 1)}, {"s": strong()}, {"r": weak()}),
      snap("drop", {"A": a(0, 1, alive=False, d=1)}, raw={"r": weak()}),
      snap("from_raw", {"A": a(0, 1, alive=False, d=1)}, {"v": weak()}),
      snap("upgrade", {"A": a(0, 1, alive=False, d=1)}, {"v": weak()}, upgrade=False),
      snap("drop", {"A": a(0, alive=False, backing=False, d=1)})]),
    ("forget sole strong preserves its contribution", [[new(), act("forget", "s")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("forget", {"A": a(1, fs=1)})]),
    ("forgotten strong still permits later weak upgrade", [[new(), down(), act("forget", "s"), up("w", "t"), act("drop", "t"), act("drop", "w")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("downgrade", {"A": a(1, 1)}, {"s": strong(), "w": weak()}),
      snap("forget", {"A": a(1, 1, fs=1)}, {"w": weak()}),
      snap("upgrade", {"A": a(2, 1, fs=1)}, {"w": weak(), "t": strong()}, upgrade=True),
      snap("drop", {"A": a(1, 1, fs=1)}, {"w": weak()}),
      snap("drop", {"A": a(1, fs=1)})]),
    ("forgotten weak retains backing after value is destroyed", [[new(), down(), act("forget", "w"), act("drop", "s")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("downgrade", {"A": a(1, 1)}, {"s": strong(), "w": weak()}),
      snap("forget", {"A": a(1, 1, fw=1)}, {"s": strong()}),
      snap("drop", {"A": a(0, 1, fw=1, alive=False, d=1)})]),
    ("weak clone remains possible after value destruction", [[new(), down(), act("drop", "s"), clone("w", "v"), act("drop", "w"), act("drop", "v")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("downgrade", {"A": a(1, 1)}, {"s": strong(), "w": weak()}),
      snap("drop", {"A": a(0, 1, alive=False, d=1)}, {"w": weak()}),
      snap("clone", {"A": a(0, 2, alive=False, d=1)}, {"w": weak(), "v": weak()}),
      snap("drop", {"A": a(0, 1, alive=False, d=1)}, {"v": weak()}),
      snap("drop", {"A": a(0, alive=False, backing=False, d=1)})]),
    ("forget one of two strong owners", [[new(), clone("s", "t"), act("forget", "s"), act("drop", "t")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("clone", {"A": a(2)}, {"s": strong(), "t": strong()}),
      snap("forget", {"A": a(2, fs=1)}, {"t": strong()}),
      snap("drop", {"A": a(1, fs=1)})]),
    ("last accessible weak is not last outstanding weak", [[new(), down(), clone("w", "v"), act("forget", "w"), act("drop", "s"), act("drop", "v")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("downgrade", {"A": a(1, 1)}, {"s": strong(), "w": weak()}),
      snap("clone", {"A": a(1, 2)}, {"s": strong(), "w": weak(), "v": weak()}),
      snap("forget", {"A": a(1, 2, fw=1)}, {"s": strong(), "v": weak()}),
      snap("drop", {"A": a(0, 2, fw=1, alive=False, d=1)}, {"v": weak()}),
      snap("drop", {"A": a(0, 1, fw=1, alive=False, d=1)})]),
    ("allocations are independent", [[new("A", "s"), new("B", "t"), down("s", "w"), down("t", "v"), act("drop", "s"), act("drop", "v"), act("drop", "w"), act("drop", "t")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("new", {"A": a(1), "B": a(1)}, {"s": strong(), "t": strong("B")}),
      snap("downgrade", {"A": a(1, 1), "B": a(1)}, {"s": strong(), "t": strong("B"), "w": weak()}),
      snap("downgrade", {"A": a(1, 1), "B": a(1, 1)}, {"s": strong(), "t": strong("B"), "w": weak(), "v": weak("B")}),
      snap("drop", {"A": a(0, 1, alive=False, d=1), "B": a(1, 1)}, {"t": strong("B"), "w": weak(), "v": weak("B")}),
      snap("drop", {"A": a(0, 1, alive=False, d=1), "B": a(1)}, {"t": strong("B"), "w": weak()}),
      snap("drop", {"A": a(0, alive=False, backing=False, d=1), "B": a(1)}, {"t": strong("B")}),
      snap("drop", {"A": a(0, alive=False, backing=False, d=1), "B": a(0, alive=False, backing=False, d=1)})]),
    ("allocation and handle identifiers preserve case", [[new("a", "h"), new("A", "H"), act("drop", "h")]],
     [snap("new", {"a": a(1)}, {"h": strong("a")}),
      snap("new", {"a": a(1), "A": a(1)}, {"h": strong("a"), "H": strong()}),
      snap("drop", {"a": a(0, alive=False, backing=False, d=1), "A": a(1)}, {"H": strong()})]),
    ("ownership namespaces may share textual identifiers", [[new("X", "X"), down("X", "w"), out("X", "X"), restore("X", "x"), act("drop", "x"), act("drop", "w")]],
     [snap("new", {"X": a(1)}, {"X": strong("X")}),
      snap("downgrade", {"X": a(1, 1)}, {"X": strong("X"), "w": weak("X")}),
      snap("into_raw", {"X": a(1, 1)}, {"w": weak("X")}, {"X": strong("X")}),
      snap("from_raw", {"X": a(1, 1)}, {"w": weak("X"), "x": strong("X")}),
      snap("drop", {"X": a(0, 1, alive=False, d=1)}, {"w": weak("X")}),
      snap("drop", {"X": a(0, alive=False, backing=False, d=1)})]),
    ("new allocation does not erase earlier death history", [[new(), act("drop", "s"), new("B", "t")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("drop", {"A": a(0, alive=False, backing=False, d=1)}),
      snap("new", {"A": a(0, alive=False, backing=False, d=1), "B": a(1)}, {"t": strong("B")})]),
    ("forget empty weak has no allocated resource", [[{"op": "empty_weak", "weak": "w"}, act("forget", "w")]],
     [snap("empty_weak", handles={"w": weak(None)}), snap("forget")]),
    ("restore then clone consumes token exactly once", [[new(), out("s", "r"), restore("r", "t"), clone("t", "u"), act("drop", "t"), act("drop", "u")]],
     [snap("new", {"A": a(1)}, {"s": strong()}),
      snap("into_raw", {"A": a(1)}, raw={"r": strong()}),
      snap("from_raw", {"A": a(1)}, {"t": strong()}),
      snap("clone", {"A": a(2)}, {"t": strong(), "u": strong()}),
      snap("drop", {"A": a(1)}, {"u": strong()}),
      snap("drop", {"A": a(0, alive=False, backing=False, d=1)})]),
]
CASES.extend([CASES[5], CASES[0]])


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
    result=m.rc_ownership(*supplied)
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
