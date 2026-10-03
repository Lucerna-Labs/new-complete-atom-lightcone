import base64
import json
import pathlib
import subprocess
import sys


def page(name, value):
    return {"kind": "page", "page": name, "value": value}


def commit(name):
    return {"kind": "commit", "tx": name}


def event(op, **fields):
    return {"op": op, **fields}


def state(written, durable, pages, acknowledged=(), commits=(), result=None,
          scanned=None, applied=(), lost=()):
    # Formatting only: every state value and recovery position below is an
    # independent literal or an explicitly stated boundary closed form.
    return {"written": written, "durable": durable,
            "pages": {name: {"lsn": pair[0], "value": pair[1]} for name, pair in pages.items()},
            "acknowledged": list(acknowledged), "durable_commits": list(commits),
            "event_result": result,
            "recovery": None if scanned is None else {"scanned": list(scanned),
                "applied": list(applied), "lost_acknowledged": list(lost)}}


P0={"p":(0,0)}
P4={"p":(1,4)}
R=[page("p",4),commit("A")]
CASES = [
("empty", [[],[]], [state(0,0,{})]),
("unmodified base page", [[],[],{"spare":7}], [state(0,0,{"spare":(0,7)})]),
("generated records are not written", [R,[]], [state(0,0,P0)]),
("volatile write and async ack are lost", [R,[event("write",through=2),event("page_write",lsn=1),event("ack",tx="A",mode="async"),event("ack",tx="A",mode="sync"),event("crash",redo_start=1)]],
 [state(0,0,P0),state(2,0,P0,result="written"),state(2,0,P0,result="wal-blocked"),state(2,0,P0,["A"],result="acknowledged"),state(2,0,P0,["A"],result="awaiting-flush"),state(0,0,P0,["A"],result="recovered",scanned=[],lost=["A"])]),
("durable commit needs page redo", [R,[event("write",through=2),event("flush",through=2),event("ack",tx="A",mode="sync"),event("crash",redo_start=1)]],
 [state(0,0,P0),state(2,0,P0,result="written"),state(2,2,P0,commits=["A"],result="flushed"),state(2,2,P0,["A"],["A"],"acknowledged"),state(2,2,P4,["A"],["A"],"recovered",[1,2],[1])]),
("partial prefix admits page but not commit", [R,[event("write",through=2),event("flush",through=1),event("page_write",lsn=1),event("ack",tx="A",mode="sync"),event("crash",redo_start=1)]],
 [state(0,0,P0),state(2,0,P0,result="written"),state(2,1,P0,result="flushed"),state(2,1,P4,result="page-written"),state(2,1,P4,result="awaiting-flush"),state(1,1,P4,result="recovered",scanned=[1])]),
("already durable page skips redo", [R,[event("write",through=2),event("flush",through=2),event("page_write",lsn=1),event("crash",redo_start=1)]],
 [state(0,0,P0),state(2,0,P0,result="written"),state(2,2,P0,commits=["A"],result="flushed"),state(2,2,P4,commits=["A"],result="page-written"),state(2,2,P4,commits=["A"],result="recovered",scanned=[1,2])]),
("checkpoint at end has no records to scan", [R,[event("write",through=2),event("flush",through=2),event("page_write",lsn=1),event("crash",redo_start=3)]],
 [state(0,0,P0),state(2,0,P0,result="written"),state(2,2,P0,commits=["A"],result="flushed"),state(2,2,P4,commits=["A"],result="page-written"),state(2,2,P4,commits=["A"],result="recovered",scanned=[])]),
("only newer page image is applied", [[page("p",10),page("p",20),commit("A")],[event("write",through=3),event("flush",through=3),event("page_write",lsn=1),event("crash",redo_start=1)]],
 [state(0,0,P0),state(3,0,P0,result="written"),state(3,3,P0,commits=["A"],result="flushed"),state(3,3,{"p":(1,10)},commits=["A"],result="page-written"),state(3,3,{"p":(2,20)},commits=["A"],result="recovered",scanned=[1,2,3],applied=[2])]),
("physical redo does not create commit marker", [[page("p",-1)],[event("write",through=1),event("flush",through=1),event("crash",redo_start=1)]],
 [state(0,0,P0),state(1,0,P0,result="written"),state(1,1,P0,result="flushed"),state(1,1,{"p":(1,-1)},result="recovered",scanned=[1],applied=[1])]),
("commit marker has no page application", [[commit("A")],[event("write",through=1),event("flush",through=1),event("ack",tx="A",mode="async"),event("crash",redo_start=1)]],
 [state(0,0,{}),state(1,0,{},result="written"),state(1,1,{},commits=["A"],result="flushed"),state(1,1,{},["A"],["A"],"acknowledged"),state(1,1,{},["A"],["A"],"recovered",[1])]),
("partial durability loses only tail acknowledgment", [[page("p",1),commit("Z"),page("q",2),commit("A")],[event("write",through=4),event("flush",through=2),event("ack",tx="Z",mode="sync"),event("ack",tx="A",mode="async"),event("crash",redo_start=1)]],
 [state(0,0,{"p":(0,0),"q":(0,0)}),state(4,0,{"p":(0,0),"q":(0,0)},result="written"),state(4,2,{"p":(0,0),"q":(0,0)},commits=["Z"],result="flushed"),state(4,2,{"p":(0,0),"q":(0,0)},["Z"],["Z"],"acknowledged"),state(4,2,{"p":(0,0),"q":(0,0)},["A","Z"],["Z"],"acknowledged"),state(2,2,{"p":(1,1),"q":(0,0)},["A","Z"],["Z"],"recovered",[1,2],[1],["A"])]),
("durable but never acknowledged", [[commit("z"),commit("A")],[event("write",through=2),event("flush",through=2),event("crash",redo_start=1)]],
 [state(0,0,{}),state(2,0,{},result="written"),state(2,2,{},commits=["A","z"],result="flushed"),state(2,2,{},commits=["A","z"],result="recovered",scanned=[1,2])]),
("prefix and ack repeats are idempotent", [R,[event("write",through=0),event("flush",through=0),event("write",through=2),event("write",through=2),event("flush",through=2),event("flush",through=2),event("ack",tx="A",mode="sync"),event("ack",tx="A",mode="sync")]],
 [state(0,0,P0),state(0,0,P0,result="written"),state(0,0,P0,result="flushed"),state(2,0,P0,result="written"),state(2,0,P0,result="written"),state(2,2,P0,commits=["A"],result="flushed"),state(2,2,P0,commits=["A"],result="flushed"),state(2,2,P0,["A"],["A"],"acknowledged"),state(2,2,P0,["A"],["A"],"acknowledged")]),
("async acknowledgment before log write", [[commit("A")],[event("ack",tx="A",mode="async"),event("ack",tx="A",mode="sync"),event("crash",redo_start=1)]],
 [state(0,0,{}),state(0,0,{},["A"],result="acknowledged"),state(0,0,{},["A"],result="awaiting-flush"),state(0,0,{},["A"],result="recovered",scanned=[],lost=["A"])]),
("page and transaction namespaces are separate", [[page("A",1000),commit("A")],[event("write",through=2),event("flush",through=2),event("crash",redo_start=1)],{"A":-1000,"spare":7}],
 [state(0,0,{"A":(0,-1000),"spare":(0,7)}),state(2,0,{"A":(0,-1000),"spare":(0,7)},result="written"),state(2,2,{"A":(0,-1000),"spare":(0,7)},commits=["A"],result="flushed"),state(2,2,{"A":(1,1000),"spare":(0,7)},commits=["A"],result="recovered",scanned=[1,2],applied=[1])]),
("blocked page does not modify nonzero base", [[page("p",-7)],[event("write",through=1),event("page_write",lsn=1),event("flush",through=1),event("page_write",lsn=1)],{"p":42}],
 [state(0,0,{"p":(0,42)}),state(1,0,{"p":(0,42)},result="written"),state(1,0,{"p":(0,42)},result="wal-blocked"),state(1,1,{"p":(0,42)},result="flushed"),state(1,1,{"p":(1,-7)},result="page-written")]),
("checkpoint skips two covered page records", [[page("p",1),page("q",2),commit("P")],[event("write",through=3),event("flush",through=3),event("page_write",lsn=1),event("page_write",lsn=2),event("crash",redo_start=3)]],
 [state(0,0,{"p":(0,0),"q":(0,0)}),state(3,0,{"p":(0,0),"q":(0,0)},result="written"),state(3,3,{"p":(0,0),"q":(0,0)},commits=["P"],result="flushed"),state(3,3,{"p":(1,1),"q":(0,0)},commits=["P"],result="page-written"),state(3,3,{"p":(1,1),"q":(2,2)},commits=["P"],result="page-written"),state(3,3,{"p":(1,1),"q":(2,2)},commits=["P"],result="recovered",scanned=[3])]),
("same page write can repeat", [[page("p",2)],[event("write",through=1),event("flush",through=1),event("page_write",lsn=1),event("page_write",lsn=1),event("crash",redo_start=1)]],
 [state(0,0,P0),state(1,0,P0,result="written"),state(1,1,P0,result="flushed"),state(1,1,{"p":(1,2)},result="page-written"),state(1,1,{"p":(1,2)},result="page-written"),state(1,1,{"p":(1,2)},result="recovered",scanned=[1])]),
("empty log operations and crash", [[],[event("write",through=0),event("flush",through=0),event("crash",redo_start=1)]],
 [state(0,0,{}),state(0,0,{},result="written"),state(0,0,{},result="flushed"),state(0,0,{},result="recovered",scanned=[])]),
("redo thresholds are per page and include intermediate images", [[page("p",10),page("q",20),page("p",30),commit("A")],[event("write",through=4),event("flush",through=4),event("page_write",lsn=2),event("crash",redo_start=1)]],
 [state(0,0,{"p":(0,0),"q":(0,0)}),state(4,0,{"p":(0,0),"q":(0,0)},result="written"),state(4,4,{"p":(0,0),"q":(0,0)},commits=["A"],result="flushed"),state(4,4,{"p":(0,0),"q":(2,20)},commits=["A"],result="page-written"),state(4,4,{"p":(3,30),"q":(2,20)},commits=["A"],result="recovered",scanned=[1,2,3,4],applied=[1,3])]),
]
# Independent boundary forms: sixteen disjoint page/commit pairs and64 no-op
# writes. No expected-state transition simulator is used.
NAMES=[f'p{i:02}' for i in range(16)]
TX=[f'T{i:02}' for i in range(16)]
BIG=[record for i in range(16) for record in (page(NAMES[i],1000-i),commit(TX[i]))]
ZERO={name:(0,0) for name in NAMES}
FINAL={name:(2*i+1,1000-i) for i,name in enumerate(NAMES)}
CASES.append(("maximum log pages and transactions",[BIG,[event("write",through=32),event("flush",through=32),event("crash",redo_start=1)]],
 [state(0,0,ZERO),state(32,0,ZERO,result="written"),state(32,32,ZERO,commits=TX,result="flushed"),state(32,32,FINAL,commits=TX,result="recovered",scanned=list(range(1,33)),applied=list(range(1,33,2)))]))
CASES.append(("maximum event count",[[],[event("write",through=0) for _ in range(64)]],
 [state(0,0,{})]+[state(0,0,{},result="written") for _ in range(64)]))
CASES.append(("explicit None base",[R,[],None],[state(0,0,P0)]))
CASES.extend([CASES[0],CASES[3],CASES[0]])

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
    result=m.wal_trace(*supplied)
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
