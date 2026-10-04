"""Literal and closed-form oracles for the declared serial breaker policy."""
import ast
import base64
import json
import pathlib
import subprocess
import sys

ERROR = "ValueError"


def E(op, time, **fields):
    return {"op": op, "time": time, **fields}


def S(mode, generation, until=None, result=None, active=None):
    # Formatting only: the state parameters below are independently hand-derived.
    return {"mode": mode, "generation": generation, "open_until": until,
            "result": result, "active": {
                name: {"generation": pair[0], "trial": pair[1]}
                for name, pair in ({} if active is None else active).items()}}


CASES = [
    ("empty minimum", [1, []], []),
    ("closed observations", [10, [E("observe", 0), E("observe", 1000000)]],
     [S("Closed", 0), S("Closed", 0)]),
    ("ordinary failures do not trip", [5, [E("call", 0, id="a"), E("call", 0, id="b"), E("result", 0, id="a", outcome="failure"), E("result", 1, id="b", outcome="success")]],
     [S("Closed", 0, result=True, active={"a": (0, False)}), S("Closed", 0, result=True, active={"a": (0, False), "b": (0, False)}), S("Closed", 0, active={"b": (0, False)}), S("Closed", 0)]),
    ("open refusals expiry and one trial", [5, [E("trip", 2), E("call", 6, id="r"), E("observe", 6), E("observe", 7), E("observe", 100), E("call", 100, id="t"), E("call", 100, id="u"), E("result", 101, id="t", outcome="success")]],
     [S("Open", 1, 7), S("Open", 1, 7, False), S("Open", 1, 7), S("HalfOpen", 2), S("HalfOpen", 2), S("HalfOpen", 2, result=True, active={"t": (2, True)}), S("HalfOpen", 2, result=False, active={"t": (2, True)}), S("Closed", 3)]),
    ("failed trial starts fresh cooldown", [3, [E("trip", 0), E("call", 3, id="t"), E("result", 4, id="t", outcome="failure"), E("observe", 6), E("call", 7, id="next"), E("result", 7, id="next", outcome="success")]],
     [S("Open", 1, 3), S("HalfOpen", 2, result=True, active={"t": (2, True)}), S("Open", 3, 7), S("Open", 3, 7), S("HalfOpen", 4, result=True, active={"next": (4, True)}), S("Closed", 5)]),
    ("stale success cannot close a newer half open generation", [2, [E("trip", 0), E("call", 2, id="old"), E("trip", 3), E("call", 5, id="new"), E("result", 5, id="old", outcome="success"), E("call", 5, id="blocked"), E("result", 6, id="new", outcome="success")]],
     [S("Open", 1, 2), S("HalfOpen", 2, result=True, active={"old": (2, True)}), S("Open", 3, 5, active={"old": (2, True)}), S("HalfOpen", 4, result=True, active={"old": (2, True), "new": (4, True)}), S("HalfOpen", 4, active={"new": (4, True)}), S("HalfOpen", 4, result=False, active={"new": (4, True)}), S("Closed", 5)]),
    ("stale failure cannot reopen a newer half open generation", [2, [E("trip", 0), E("call", 2, id="old"), E("trip", 3), E("call", 5, id="new"), E("result", 5, id="old", outcome="failure"), E("result", 6, id="new", outcome="failure")]],
     [S("Open", 1, 2), S("HalfOpen", 2, result=True, active={"old": (2, True)}), S("Open", 3, 5, active={"old": (2, True)}), S("HalfOpen", 4, result=True, active={"old": (2, True), "new": (4, True)}), S("HalfOpen", 4, active={"new": (4, True)}), S("Open", 5, 8)]),
    ("stale trial result during open only terminates work", [5, [E("trip", 0), E("call", 5, id="old"), E("trip", 6), E("result", 7, id="old", outcome="success")]],
     [S("Open", 1, 5), S("HalfOpen", 2, result=True, active={"old": (2, True)}), S("Open", 3, 11, active={"old": (2, True)}), S("Open", 3, 11)]),
    ("stale trial result during closed preserves new ordinary calls", [1, [E("trip", 0), E("call", 1, id="old"), E("trip", 1), E("call", 2, id="new"), E("result", 2, id="new", outcome="success"), E("call", 2, id="ordinary"), E("result", 3, id="old", outcome="failure")]],
     [S("Open", 1, 1), S("HalfOpen", 2, result=True, active={"old": (2, True)}), S("Open", 3, 2, active={"old": (2, True)}), S("HalfOpen", 4, result=True, active={"old": (2, True), "new": (4, True)}), S("Closed", 5, active={"old": (2, True)}), S("Closed", 5, result=True, active={"old": (2, True), "ordinary": (5, False)}), S("Closed", 5, active={"ordinary": (5, False)})]),
    ("expiry before ordinary result", [5, [E("call", 0, id="ordinary"), E("trip", 1), E("result", 6, id="ordinary", outcome="failure"), E("call", 6, id="trial")]],
     [S("Closed", 0, result=True, active={"ordinary": (0, False)}), S("Open", 1, 6, active={"ordinary": (0, False)}), S("HalfOpen", 2), S("HalfOpen", 2, result=True, active={"trial": (2, True)})]),
    ("expiry before trip adds both generations", [3, [E("trip", 0), E("trip", 3), E("observe", 6), E("trip", 6), E("observe", 9)]],
     [S("Open", 1, 3), S("Open", 3, 6), S("HalfOpen", 4), S("Open", 5, 9), S("HalfOpen", 6)]),
    ("trip before expiry resets deadline", [5, [E("trip", 0), E("trip", 4), E("observe", 5), E("observe", 9)]],
     [S("Open", 1, 5), S("Open", 2, 9), S("Open", 2, 9), S("HalfOpen", 3)]),
    ("large time jump expires only once", [1, [E("trip", 0), E("observe", 1000000), E("observe", 1000000)]],
     [S("Open", 1, 1), S("HalfOpen", 2), S("HalfOpen", 2)]),
    ("call just before and at cooldown", [10, [E("trip", 0), E("call", 9, id="before"), E("call", 10, id="at")]],
     [S("Open", 1, 10), S("Open", 1, 10, False), S("HalfOpen", 2, result=True, active={"at": (2, True)})]),
    ("expiry before stale trial result with no new trial", [2, [E("trip", 0), E("call", 2, id="old"), E("trip", 3), E("result", 5, id="old", outcome="success"), E("call", 5, id="new")]],
     [S("Open", 1, 2), S("HalfOpen", 2, result=True, active={"old": (2, True)}), S("Open", 3, 5, active={"old": (2, True)}), S("HalfOpen", 4), S("HalfOpen", 4, result=True, active={"new": (4, True)})]),
    ("same timestamp preserves explicit event order", [1, [E("call", 0, id="a"), E("trip", 0), E("call", 0, id="b"), E("result", 0, id="a", outcome="failure"), E("observe", 1), E("call", 1, id="c"), E("result", 1, id="c", outcome="failure"), E("trip", 1), E("observe", 2)]],
     [S("Closed", 0, result=True, active={"a": (0, False)}), S("Open", 1, 1, active={"a": (0, False)}), S("Open", 1, 1, False, {"a": (0, False)}), S("Open", 1, 1), S("HalfOpen", 2), S("HalfOpen", 2, result=True, active={"c": (2, True)}), S("Open", 3, 2), S("Open", 4, 2), S("HalfOpen", 5)]),
    ("maximum cooldown and time allow later deadline", [1000, [E("trip", 1000000), E("call", 1000000, id="x")]],
     [S("Open", 1, 1001000), S("Open", 1, 1001000, False)]),
    ("maximum cooldown equality", [1000, [E("trip", 0), E("observe", 999), E("observe", 1000)]],
     [S("Open", 1, 1000), S("Open", 1, 1000), S("HalfOpen", 2)]),
    ("case sensitive and punctuation IDs", [1, [E("call", 0, id="A"), E("call", 0, id="a"), E("call", 0, id="-_09"), E("call", 0, id="Z"*32), E("result", 0, id="a", outcome="success")]],
     [S("Closed", 0, result=True, active={"A": (0, False)}), S("Closed", 0, result=True, active={"A": (0, False), "a": (0, False)}), S("Closed", 0, result=True, active={"A": (0, False), "a": (0, False), "-_09": (0, False)}), S("Closed", 0, result=True, active={"A": (0, False), "a": (0, False), "-_09": (0, False), "Z"*32: (0, False)}), S("Closed", 0, active={"A": (0, False), "-_09": (0, False), "Z"*32: (0, False)})]),
    ("ordinary successes leave half open trial untouched", [2, [E("call", 0, id="a"), E("trip", 0), E("call", 2, id="t"), E("result", 2, id="a", outcome="success"), E("call", 2, id="blocked")]],
     [S("Closed", 0, result=True, active={"a": (0, False)}), S("Open", 1, 2, active={"a": (0, False)}), S("HalfOpen", 2, result=True, active={"a": (0, False), "t": (2, True)}), S("HalfOpen", 2, active={"t": (2, True)}), S("HalfOpen", 2, result=False, active={"t": (2, True)})]),
]

WRAPS = {}


def bad(name, args, wrap=None):
    CASES.append((name, args, ERROR))
    if wrap is not None:
        WRAPS[name] = wrap


for value in (0, -1, 1001, True, False, 1.0, "1", None):
    bad("invalid cooldown " + repr(value), [value, []])
for value in ((), {}, None):
    bad("events not native list " + repr(value), [1, value])
bad("129 events", [1, [E("observe", 0) for _ in range(129)]])
for value in (None, [], "observe"):
    bad("event not dict " + repr(value), [1, [value]])
for value in ({}, {"op": "observe"}, {"time": 0}, {"op": 1, "time": 0}, {"op": [], "time": 0}, E("Observe", 0), E("reset", 0), E("observe", 0, id="extra"), E("trip", 0, outcome="failure"), E("call", 0), E("result", 0, id="a"), E("call", 0, id="a", outcome="success")):
    bad("invalid schema " + repr(value), [1, [value]])
for value in (-1, 1000001, True, 0.0, "0", None):
    bad("invalid event time " + repr(value), [1, [E("observe", value)]])
bad("decreasing time after real work", [1, [E("call", 2, id="a"), E("observe", 1)]])
for value in ("", "a"*33, "é", "a b", "a.b", "a\n", "\x00", 0, True, [], {}):
    bad("invalid id " + repr(value), [1, [E("call", 0, id=value)]])
for value in ("Success", "cancelled", "", True, 1, None, []):
    bad("invalid outcome " + repr(value), [1, [E("call", 0, id="a"), E("result", 0, id="a", outcome=value)]])
bad("unknown result", [1, [E("result", 0, id="unknown", outcome="success")]])
bad("refused result", [1, [E("trip", 0), E("call", 0, id="no"), E("result", 1, id="no", outcome="success")]])
bad("completed result", [1, [E("call", 0, id="a"), E("result", 0, id="a", outcome="failure"), E("result", 0, id="a", outcome="success")]])
bad("reused active call id", [1, [E("call", 0, id="a"), E("call", 0, id="a")]])
bad("reused completed call id", [1, [E("call", 0, id="a"), E("result", 0, id="a", outcome="success"), E("call", 1, id="a")]])
bad("reused refused call id", [1, [E("trip", 0), E("call", 0, id="a"), E("call", 1, id="a")]])
bad("reused blocked half open id", [1, [E("trip", 0), E("call", 1, id="a"), E("call", 1, id="b"), E("result", 1, id="a", outcome="success"), E("call", 2, id="b")]])
bad("malformed event after state transitions", [1, [E("trip", 0), E("call", 1, id="a"), E("observe", 1, unexpected=True)]])
# Subclasses are reconstructed only in the isolated candidate process.
bad("int subclass cooldown", [1, []], ("int", [0]))
bad("list subclass events", [1, []], ("list", [1]))
bad("dict subclass event", [1, [E("observe", 0)]], ("dict", [1, 0]))
bad("int subclass time", [1, [E("observe", 0)]], ("int", [1, 0, "time"]))
bad("str subclass operation", [1, [E("observe", 0)]], ("str", [1, 0, "op"]))
bad("str subclass id", [1, [E("call", 0, id="a")]], ("str", [1, 0, "id"]))
bad("str subclass outcome", [1, [E("call", 0, id="a"), E("result", 0, id="a", outcome="success")]], ("str", [1, 1, "outcome"]))

# Closed forms, not another FSM: unchanged observations, same-time trips, or
# distinct Closed admissions have direct index-based expected states.
CASES.extend([
    ("128 unchanged snapshots", [1, [E("observe", 0) for _ in range(128)]], [S("Closed", 0) for _ in range(128)]),
    ("128 same-time qualified trips", [1, [E("trip", 0) for _ in range(128)]], [S("Open", i, 1) for i in range(1, 129)]),
    ("128 alternating trip-expiry events", [1, [E("trip" if i % 2 == 0 else "observe", i) for i in range(128)]], [S("Open", i+1, i+1) if i % 2 == 0 else S("HalfOpen", i+1) for i in range(128)]),
    ("128 simultaneous Closed admissions", [1000, [E("call", 0, id="id"+str(i)) for i in range(128)]], [S("Closed", 0, result=True, active={"id"+str(j): (0, False) for j in range(i+1)}) for i in range(128)]),
])
# Genuine repeated nonempty call after both invalid and empty/minimal calls.
CASES.extend([CASES[0], CASES[1], CASES[5], CASES[0]])


def fingerprint(value):
    kind = type(value)
    if kind is dict:
        return ["dict", sorted([[fingerprint(k), fingerprint(v)] for k, v in value.items()], key=repr)]
    if kind in (list, tuple):
        return [kind.__name__, [fingerprint(v) for v in value]]
    if value is None:
        return ["none"]
    if kind in (bool, int, str):
        return [kind.__name__, value]
    if kind in (float, bytes):
        return [kind.__name__, repr(value)]
    return ["unsupported", kind.__module__, kind.__qualname__, repr(value)]


RUNNER = r'''import ast,base64,copy,importlib.util,json,sys
class IntChild(int): pass
class StrChild(str): pass
class ListChild(list): pass
class DictChild(dict): pass
CAST={"int":IntChild,"str":StrChild,"list":ListChild,"dict":DictChild}

def fingerprint(value):
    kind=type(value)
    if kind is dict:return ["dict",sorted([[fingerprint(k),fingerprint(v)] for k,v in value.items()],key=repr)]
    if kind in (list,tuple):return [kind.__name__,[fingerprint(v) for v in value]]
    if value is None:return ["none"]
    if kind in (bool,int,str):return [kind.__name__,value]
    if kind in (float,bytes):return [kind.__name__,repr(value)]
    return ["unsupported",kind.__module__,kind.__qualname__,repr(value)]

def mutable_objects(value,found=None):
    if found is None:found={}
    if isinstance(value,(dict,list)):
        if id(value) in found:return found
        found[id(value)]=value
    if isinstance(value,dict):
        for key,child in value.items():mutable_objects(key,found);mutable_objects(child,found)
    elif isinstance(value,(list,tuple)):
        for child in value:mutable_objects(child,found)
    return found

def independent(values,forbidden):
    seen=set(forbidden)
    def visit(value):
        if isinstance(value,(dict,list)):
            if id(value) in seen:return False
            seen.add(id(value))
        if isinstance(value,dict):return all(visit(k) and visit(v) for k,v in value.items())
        if isinstance(value,(list,tuple)):return all(visit(v) for v in value)
        return True
    return all(visit(v) for v in values)

spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
inputs=[];output_history=[];values=[];calls=[];input_objects={}
unchanged=True;stable=True;isolated=True
for args,wrap in ast.literal_eval(base64.b64decode(sys.argv[2]).decode()):
    supplied=copy.deepcopy(args)
    if wrap is not None:
        kind,path=wrap;owner=supplied
        for part in path[:-1]:owner=owner[part]
        owner[path[-1]]=CAST[kind](owner[path[-1]])
    inputs.append((supplied,fingerprint(supplied)))
    mutable_objects(supplied,input_objects)
    try:
        value=m.breaker_events(*supplied)
    except ValueError:
        calls.append({"error":"ValueError"})
    except Exception as exc:
        calls.append({"error":type(exc).__name__})
    else:
        snap=fingerprint(value)
        values.append(value);output_history.append(snap)
        calls.append({"value":snap})
    # These checks run after every successful OR failing call, before a later
    # call could restore a mutation of an older argument or returned result.
    for prior,before in inputs:
        unchanged=unchanged and fingerprint(prior)==before
        mutable_objects(prior,input_objects)
    for prior,before in zip(values,output_history):stable=stable and fingerprint(prior)==before
    isolated=isolated and independent(values,input_objects)
print("__RESULT__"+json.dumps({"calls":calls,"inputs_unchanged":unchanged,"outputs_unchanged":stable,"independent":isolated}))'''


def run(candidate):
    encoded = base64.b64encode(repr([(args, WRAPS.get(name)) for name, args, _ in CASES]).encode()).decode()
    try:
        process = subprocess.run([sys.executable, "-B", "-c", RUNNER, str(pathlib.Path(candidate).resolve()), encoded], capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines() if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if process.returncode == 0 and lines else None
        expected = {"calls": [{"error": ERROR} if value == ERROR else {"value": fingerprint(value)} for _, _, value in CASES],
                    "inputs_unchanged": True, "outputs_unchanged": True, "independent": True}
        return actual == expected
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
