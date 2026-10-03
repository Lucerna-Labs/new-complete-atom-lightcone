import base64
import json
import pathlib
import subprocess
import sys


def put(item):
    return {"op": "put", "item": item}


def shut(immediate):
    return {"op": "shutdown", "immediate": immediate}


def snap(op, status, queue=(), unfinished=0, shutdown=False, value=None):
    return {"op": op, "status": status, "value": value, "queue": list(queue),
            "unfinished": unfinished, "shutdown": shutdown}


GET = {"op": "get"}
ACK = {"op": "task_done"}
JOIN = {"op": "join"}

# Static accounting traces. The reference is never used to construct an oracle.
CASES = [
    ("empty", [1, []], []),
    ("empty queries", [0, [GET, JOIN, ACK]],
     [snap("get", "empty"), snap("join", "ready"), snap("task_done", "underflow")]),
    ("one put", [1, [put("A")]], [snap("put", "accepted", ["A"], 1)]),
    ("full put changes nothing", [1, [put("A"), put("B")]],
     [snap("put", "accepted", ["A"], 1), snap("put", "full", ["A"], 1)]),
    ("get frees occupancy but not unfinished count", [1, [put("A"), GET, put("B")]],
     [snap("put", "accepted", ["A"], 1), snap("get", "item", [], 1, value="A"),
      snap("put", "accepted", ["B"], 2)]),
    ("empty queue still has unfinished work", [1, [put("A"), GET, JOIN]],
     [snap("put", "accepted", ["A"], 1), snap("get", "item", [], 1, value="A"),
      snap("join", "waiting", [], 1)]),
    ("acknowledged dequeued work releases join", [1, [put("A"), GET, ACK, JOIN]],
     [snap("put", "accepted", ["A"], 1), snap("get", "item", [], 1, value="A"),
      snap("task_done", "acknowledged"), snap("join", "ready")]),
    ("too many acknowledgments do not make count negative", [1, [put("A"), ACK, ACK]],
     [snap("put", "accepted", ["A"], 1), snap("task_done", "acknowledged", ["A"]),
      snap("task_done", "underflow", ["A"])]),
    ("early acknowledgment is accepted by the API", [1, [put("A"), ACK, JOIN, GET, ACK]],
     [snap("put", "accepted", ["A"], 1), snap("task_done", "acknowledged", ["A"]),
      snap("join", "ready", ["A"]), snap("get", "item", value="A"),
      snap("task_done", "underflow")]),
    ("FIFO item order", [3, [put("B"), put("A"), put("C"), GET, GET]],
     [snap("put", "accepted", ["B"], 1), snap("put", "accepted", ["B", "A"], 2),
      snap("put", "accepted", ["B", "A", "C"], 3),
      snap("get", "item", ["A", "C"], 3, value="B"),
      snap("get", "item", ["C"], 3, value="A")]),
    ("duplicate values are separate entries", [2, [put("A"), put("A"), GET, GET]],
     [snap("put", "accepted", ["A"], 1), snap("put", "accepted", ["A", "A"], 2),
      snap("get", "item", ["A"], 2, value="A"), snap("get", "item", [], 2, value="A")]),
    ("zero capacity is unbounded", [0, [put("A"), put("B"), put("C")]],
     [snap("put", "accepted", ["A"], 1), snap("put", "accepted", ["A", "B"], 2),
      snap("put", "accepted", ["A", "B", "C"], 3)]),
    ("negative capacity is also unbounded", [-1, [put("A"), put("B")]],
     [snap("put", "accepted", ["A"], 1), snap("put", "accepted", ["A", "B"], 2)]),
    ("lowest allowed capacity", [-2, [put("a"), put("A"), GET]],
     [snap("put", "accepted", ["a"], 1), snap("put", "accepted", ["a", "A"], 2),
      snap("get", "item", ["A"], 2, value="a")]),
    ("graceful drain and later acknowledgments", [2, [put("A"), put("B"), shut(False),
       GET, GET, GET, JOIN, ACK, ACK, JOIN]],
     [snap("put", "accepted", ["A"], 1), snap("put", "accepted", ["A", "B"], 2),
      snap("shutdown", "closed", ["A", "B"], 2, True),
      snap("get", "item", ["B"], 2, True, "A"), snap("get", "item", [], 2, True, "B"),
      snap("get", "shutdown", [], 2, True), snap("join", "waiting", [], 2, True),
      snap("task_done", "acknowledged", [], 1, True),
      snap("task_done", "acknowledged", [], 0, True), snap("join", "ready", [], 0, True)]),
    ("shutdown takes precedence over fullness", [1, [put("A"), shut(False), put("B")]],
     [snap("put", "accepted", ["A"], 1), snap("shutdown", "closed", ["A"], 1, True),
      snap("put", "shutdown", ["A"], 1, True)]),
    ("empty graceful shutdown", [1, [shut(False), GET, JOIN, ACK]],
     [snap("shutdown", "closed", shutdown=True), snap("get", "shutdown", shutdown=True),
      snap("join", "ready", shutdown=True), snap("task_done", "underflow", shutdown=True)]),
    ("empty immediate shutdown", [1, [shut(True), GET, JOIN, put("A")]],
     [snap("shutdown", "closed", shutdown=True), snap("get", "shutdown", shutdown=True),
      snap("join", "ready", shutdown=True), snap("put", "shutdown", shutdown=True)]),
    ("immediate shutdown of queued-only work", [2, [put("A"), put("B"), shut(True), JOIN, GET]],
     [snap("put", "accepted", ["A"], 1), snap("put", "accepted", ["A", "B"], 2),
      snap("shutdown", "closed", shutdown=True), snap("join", "ready", shutdown=True),
      snap("get", "shutdown", shutdown=True)]),
    ("three puts one get leaves one unfinished after drain", [3, [put("A"), put("B"), put("C"),
       GET, shut(True), JOIN, ACK, JOIN]],
     [snap("put", "accepted", ["A"], 1), snap("put", "accepted", ["A", "B"], 2),
      snap("put", "accepted", ["A", "B", "C"], 3),
      snap("get", "item", ["B", "C"], 3, value="A"),
      snap("shutdown", "closed", [], 1, True), snap("join", "waiting", [], 1, True),
      snap("task_done", "acknowledged", [], 0, True), snap("join", "ready", [], 0, True)]),
    ("empty immediate drain cannot acknowledge in-flight work", [1, [put("A"), GET,
       shut(True), JOIN, shut(True), JOIN]],
     [snap("put", "accepted", ["A"], 1), snap("get", "item", [], 1, value="A"),
      snap("shutdown", "closed", [], 1, True), snap("join", "waiting", [], 1, True),
      snap("shutdown", "closed", [], 1, True), snap("join", "waiting", [], 1, True)]),
    ("graceful-to-immediate escalation", [2, [put("A"), put("B"), shut(False), GET,
       shut(True), JOIN]],
     [snap("put", "accepted", ["A"], 1), snap("put", "accepted", ["A", "B"], 2),
      snap("shutdown", "closed", ["A", "B"], 2, True),
      snap("get", "item", ["B"], 2, True, "A"),
      snap("shutdown", "closed", [], 1, True), snap("join", "waiting", [], 1, True)]),
    ("immediate-to-graceful cannot reopen", [1, [put("A"), shut(True), shut(False), put("B"), GET]],
     [snap("put", "accepted", ["A"], 1), snap("shutdown", "closed", shutdown=True),
      snap("shutdown", "closed", shutdown=True), snap("put", "shutdown", shutdown=True),
      snap("get", "shutdown", shutdown=True)]),
    ("drain uses zero floor after one early acknowledgment", [2, [put("A"), put("B"), ACK,
       shut(True), JOIN, ACK]],
     [snap("put", "accepted", ["A"], 1), snap("put", "accepted", ["A", "B"], 2),
      snap("task_done", "acknowledged", ["A", "B"], 1),
      snap("shutdown", "closed", shutdown=True), snap("join", "ready", shutdown=True),
      snap("task_done", "underflow", shutdown=True)]),
    ("drain when early acknowledgments already cleared count", [2, [put("A"), put("B"),
       ACK, ACK, shut(True), JOIN]],
     [snap("put", "accepted", ["A"], 1), snap("put", "accepted", ["A", "B"], 2),
      snap("task_done", "acknowledged", ["A", "B"], 1),
      snap("task_done", "acknowledged", ["A", "B"], 0),
      snap("shutdown", "closed", shutdown=True), snap("join", "ready", shutdown=True)]),
    ("join queries do not install persistent waiters", [1, [JOIN, put("A"), JOIN, ACK, JOIN]],
     [snap("join", "ready"), snap("put", "accepted", ["A"], 1),
      snap("join", "waiting", ["A"], 1), snap("task_done", "acknowledged", ["A"]),
      snap("join", "ready", ["A"])]),
    ("graceful get does not reopen queue", [1, [put("A"), shut(False), GET, put("B"), ACK]],
     [snap("put", "accepted", ["A"], 1), snap("shutdown", "closed", ["A"], 1, True),
      snap("get", "item", [], 1, True, "A"), snap("put", "shutdown", [], 1, True),
      snap("task_done", "acknowledged", [], 0, True)]),
    ("capacity eight and exact item strings", [8, [put("0"), put("A"), put("a"),
       put("-"), put("_"), put("b"), put("c"), put("abcdefghijklmnop"), put("extra")]],
     [snap("put", "accepted", ["0"], 1), snap("put", "accepted", ["0", "A"], 2),
      snap("put", "accepted", ["0", "A", "a"], 3),
      snap("put", "accepted", ["0", "A", "a", "-"], 4),
      snap("put", "accepted", ["0", "A", "a", "-", "_"], 5),
      snap("put", "accepted", ["0", "A", "a", "-", "_", "b"], 6),
      snap("put", "accepted", ["0", "A", "a", "-", "_", "b", "c"], 7),
      snap("put", "accepted", ["0", "A", "a", "-", "_", "b", "c", "abcdefghijklmnop"], 8),
      snap("put", "full", ["0", "A", "a", "-", "_", "b", "c", "abcdefghijklmnop"], 8)]),
]
CASES.extend([CASES[19], CASES[0]])


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
values=[];unchanged=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args);before=json.dumps(supplied,sort_keys=True);types=native_types(supplied)
    values.append(m.queue_accounting(*supplied))
    unchanged=unchanged and json.dumps(supplied,sort_keys=True)==before and native_types(supplied)==types
print("__RESULT__"+json.dumps({"values":values,"types":[native_types(v) for v in values],"unchanged":unchanged}))'''
    try:
        process = subprocess.run([sys.executable, "-B", "-c", runner,
                                  str(pathlib.Path(candidate).resolve()), payload],
                                 capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if process.returncode == 0 and lines else None
        wanted = [value for _, _, value in CASES]
        expected = {"values": wanted, "types": [native_types(v) for v in wanted], "unchanged": True}
        return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return False


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
