"""Finite job-list oracle and literal witnesses for the declared queue model."""
import base64
from collections import deque
import inspect
import json
import pathlib
import subprocess
import sys

FUNCTION_NAME = "queue_epochs"
VALUE_ERROR = "ValueError"
CASES = []


def job_oracle(capacity, healthy, degraded, enter, exit, arrivals):
    """Track actual individual jobs rather than the reference's count recurrence."""
    jobs = deque()
    next_job = 0
    degraded_mode = False
    answer = []
    for offered in arrivals:
        accepted_ids = []
        refused_ids = []
        for _ in range(offered):
            job = next_job
            next_job += 1
            if len(jobs) == capacity:
                refused_ids.append(job)
            else:
                jobs.append(job)
                accepted_ids.append(job)
        finished_ids = []
        slots = degraded if degraded_mode else healthy
        for _ in range(slots):
            if not jobs:
                break
            finished_ids.append(jobs.popleft())
        if degraded_mode:
            if len(jobs) <= exit:
                degraded_mode = False
        elif len(jobs) >= enter:
            degraded_mode = True
        answer.append({"queue": len(jobs),
                       "mode": "Degraded" if degraded_mode else "Healthy",
                       "admitted": len(accepted_ids), "rejected": len(refused_ids),
                       "completed": len(finished_ids)})
    return answer


def states(rows):
    return [{"queue": q, "mode": mode, "admitted": a, "rejected": r, "completed": c}
            for q, mode, a, r, c in rows]


def good(name, args, literal=None):
    expected = job_oracle(*args)
    if literal is not None:
        assert expected == states(literal), name
        expected = states(literal)
    CASES.append((name, args, expected, []))


def bad(name, args, wraps=None):
    CASES.append((name, args, VALUE_ERROR, wraps or []))


H, D = "Healthy", "Degraded"
good("empty minimum", [2,1,0,1,0,[]], [])
good("zero and one job stay healthy", [2,1,0,1,0,[0,1,0,1]],
     [(0,H,0,0,0),(0,H,1,0,1),(0,H,0,0,0),(0,H,1,0,1)])
bad("bool capacity between valid calls", [True,1,0,1,0,[]])
good("zero service retains degradation after trigger", [2,1,0,1,0,[2,0,1,1000,0]],
     [(1,D,2,0,1),(1,D,0,0,0),(2,D,1,0,0),(2,D,0,1000,0),(2,D,0,0,0)])
good("service precedes entry and exit transitions", [8,5,1,3,1,[8,0,0,0,8]],
     [(3,D,8,0,5),(2,D,0,0,1),(1,H,0,0,1),(0,H,0,0,1),(3,D,8,0,5)])
good("entry equality is distinct from below threshold", [9,4,1,4,0,[7,1,8]],
     [(3,H,7,0,4),(0,H,1,0,4),(4,D,8,0,4)])
bad("malformed later arrival", [8,5,1,3,1,[8,0,False]])
good("17 to 1 recovery and healthy restoration",
     [20,10,3,8,2,[6,20,6,6,6,6]+[1]*8+[6]],
     [(0,H,6,0,6),(10,D,20,0,10),(13,D,6,0,3),(16,D,6,0,3),
      (17,D,4,2,3),(17,D,3,3,3),
      (15,D,1,0,3),(13,D,1,0,3),(11,D,1,0,3),(9,D,1,0,3),
      (7,D,1,0,3),(5,D,1,0,3),(3,D,1,0,3),(1,H,1,0,3),(0,H,6,0,7)])
good("drain to zero needs degraded service until exit", [5,3,1,2,0,[5,0,0,4]],
     [(2,D,5,0,3),(1,D,0,0,1),(0,H,0,0,1),(1,H,4,0,3)])
good("exit equality restores next epoch only", [7,4,2,3,1,[7,0,4]],
     [(3,D,7,0,4),(1,H,0,0,2),(1,H,4,0,4)])
good("admission uses free waiting slots before service", [6,2,1,4,1,[1000,1000,1000]],
     [(4,D,6,994,2),(5,D,2,998,1),(5,D,1,999,1)])
good("ordinary arrivals equal degraded capacity do not drain", [9,5,2,4,1,[9,2,2,2]],
     [(4,D,9,0,5),(4,D,2,0,2),(4,D,2,0,2),(4,D,2,0,2)])
good("one below and above exit", [10,6,1,4,2,[10,0,0,6]],
     [(4,D,10,0,6),(3,D,0,0,1),(2,H,0,0,1),(2,H,6,0,6)])
good("retrigger after complete recovery", [6,3,2,3,0,[6,0,0,6,0,0]],
     [(3,D,6,0,3),(1,D,0,0,2),(0,H,0,0,1),
      (3,D,6,0,3),(1,D,0,0,2),(0,H,0,0,1)])

# Distinct small profiles exercise different threshold gaps and sequences.
profiles = [
 (3,1,0,2,0),(4,2,1,2,1),(5,1,0,1,0),(5,4,3,1,0),
 (6,2,0,3,2),(7,3,2,4,2),(8,6,4,2,0),(9,2,1,5,3),
 (10,7,0,3,1),(12,6,5,6,0),(15,4,2,9,7),(20,10,9,10,9)]
for i, profile in enumerate(profiles):
    cap, healthy, degraded, enter, exit = profile
    offered = [0, healthy, cap, degraded, 0, cap+1, healthy-1, 1, 0, 0, 1000, 0]
    good("job-oracle profile " + str(i), [*profile, offered])

valid = [6,3,1,3,1,[6,0,0]]
# Every parameter rejects native-type mistakes, including subclasses.
for index, label in enumerate(["capacity","healthy","degraded","enter","exit"]):
    for value, kind in [(True,"bool"),(1.0,"float"),("1","str"),(None,"None")]:
        args = [*valid[:5], list(valid[5])]
        args[index] = value
        bad(label+" "+kind, args)
    bad(label+" int subclass", [*valid[:5],list(valid[5])], [([index],"int")])
    args = [*valid[:5], []]
    args[index] = float(valid[index])
    bad(label+" float with otherwise valid magnitude", args)
bad("boolean healthy with otherwise valid domain", [3,True,0,2,0,[]])
bad("boolean entry with otherwise valid domain", [6,3,1,True,0,[]])

for name, index, value in [
 ("capacity low",0,1),("capacity high",0,101),("healthy zero",1,0),
 ("healthy reaches capacity",1,6),("degraded negative",2,-1),
 ("degraded reaches healthy",2,3),("entry zero",3,0),
 ("entry above post-service bound",3,4),("exit negative",4,-1),
 ("exit equals entry",4,3)]:
    args = [*valid[:5],list(valid[5])]
    args[index] = value
    bad(name,args)

for value, name in [((), "tuple"),({}, "dict"),(None,"None"),("0","str")]:
    bad("arrivals "+name,[*valid[:5],value])
bad("arrivals list subclass",[*valid[:5],[0]], [([5],"list")])
bad("too many epochs",[*valid[:5],[0]*129])
for value, name in [(-1,"negative"),(1001,"large"),(True,"bool"),(0.0,"float"),
                    ("0","str"),(None,"None")]:
    bad("arrival "+name,[*valid[:5],[6,value]])
bad("arrival int subclass",[*valid[:5],[6,0]], [([5,1],"int")])

# Maximum sequence/population domains, followed by fresh calls and errors.
good("maximum epochs and offered count", [100,99,0,1,0,[1000]*128])
good("maximum healthy and degraded capacities", [100,99,98,1,0,[100,0,1000,0,1,0]])
good("maximum threshold range", [100,1,0,99,98,[100,0,0,1000]])
good("128 empty epochs have independent equal snapshots", [100,50,49,50,49,[0]*128])
good("empty after large trace", [2,1,0,1,0,[]], [])
bad("error after large trace", [2,1,0,1,0,[False]])
good("repeat service-before-transition after error", [8,5,1,3,1,[8,0,0,0,8]])
good("repeat minimum after nonempty", [2,1,0,1,0,[1]])
good("final empty", [2,1,0,1,0,[]], [])

def fingerprint(value, active=None):
    if active is None:
        active = set()
    kind = type(value)
    tag = kind.__name__ if kind in (dict, list, tuple, set, frozenset, bool, int, str, float, bytes) else kind.__module__ + "." + kind.__qualname__
    if isinstance(value, (dict, list, tuple, set, frozenset)):
        if id(value) in active:
            return ["cycle"]
        active.add(id(value))
        if isinstance(value, dict):
            body = sorted([[fingerprint(k, active), fingerprint(v, active)]
                           for k, v in value.items()], key=repr)
        else:
            body = [fingerprint(v, active) for v in value]
            if isinstance(value, (set, frozenset)):
                body.sort(key=repr)
        active.remove(id(value))
        return [tag, body]
    if value is None:
        return ["none"]
    if kind in (bool, int, str):
        return [tag, value]
    if isinstance(value, int):
        return [tag, int(value)]
    if isinstance(value, str):
        return [tag, str(value)]
    return [tag, repr(value)]


def run(candidate):
    payload = base64.b64encode(repr([(args, wraps) for _, args, _, wraps in CASES]).encode()).decode()
    runner = r'''import ast,base64,copy,importlib.util,json,sys

class IntChild(int): pass
class ListChild(list): pass
class DictChild(dict): pass
class StrChild(str): pass

''' + FINGERPRINT_SOURCE + r'''
def mutable_objects(value, found):
    if isinstance(value, (dict, list, set, bytearray)):
        if id(value) in found:
            return
        found[id(value)] = value
    if isinstance(value, dict):
        for key, child in value.items():
            mutable_objects(key, found)
            mutable_objects(child, found)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for child in value:
            mutable_objects(child, found)

def independent(values, forbidden):
    seen = set(forbidden)
    def visit(value):
        if isinstance(value, (dict, list, set, bytearray)):
            if id(value) in seen:
                return False
            seen.add(id(value))
        if isinstance(value, dict):
            return all(visit(k) and visit(v) for k, v in value.items())
        if isinstance(value, (list, tuple, set, frozenset)):
            return all(visit(v) for v in value)
        return True
    return all(visit(value) for value in values)

spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
inputs=[];outputs=[];output_history=[];input_objects={};calls=[]
unchanged=True;stable=True;isolated=True
for args, wraps in ast.literal_eval(base64.b64decode(sys.argv[2]).decode()):
    supplied=copy.deepcopy(args)
    for path, kind in wraps:
        parent=supplied
        for step in path[:-1]:
            parent=parent[step]
        value=parent[path[-1]]
        if kind == "strkeys":
            parent[path[-1]]={StrChild(k): v for k,v in value.items()}
        else:
            parent[path[-1]]={"int":IntChild,"list":ListChild,"dict":DictChild,"str":StrChild}[kind](value)
    inputs.append((supplied,fingerprint(supplied)))
    mutable_objects(supplied,input_objects)
    try:
        value=getattr(m,FUNCTION_NAME)(*supplied)
    except ValueError:
        calls.append({"error":"ValueError"})
    except Exception as exc:
        calls.append({"error":type(exc).__name__})
    else:
        snap=fingerprint(value)
        outputs.append(value);output_history.append(snap)
        calls.append({"value":snap})
    for prior,before in inputs:
        if fingerprint(prior)!=before:
            unchanged=False
        mutable_objects(prior,input_objects)
    for prior,before in zip(outputs,output_history):
        if fingerprint(prior)!=before:
            stable=False
    if not independent(outputs,input_objects):
        isolated=False
print("__RESULT__"+json.dumps({"calls":calls,"inputs_unchanged":unchanged,
                             "outputs_unchanged":stable,"independent":isolated}))
'''
    runner = runner.replace("FUNCTION_NAME", repr(FUNCTION_NAME))
    try:
        process = subprocess.run(
            [sys.executable, "-B", "-c", runner, str(pathlib.Path(candidate).resolve()), payload],
            capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if process.returncode == 0 and lines else None
        expected = {
            "calls": [{"error": "ValueError"} if value == VALUE_ERROR
                      else {"value": fingerprint(value)} for _, _, value, _ in CASES],
            "inputs_unchanged": True, "outputs_unchanged": True, "independent": True}
        return actual == expected
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False


# Copy the checker-owned native fingerprint implementation into the child runner.
FINGERPRINT_SOURCE = inspect.getsource(fingerprint)

if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
