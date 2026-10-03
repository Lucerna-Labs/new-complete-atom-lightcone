import ast
import base64
import json
import pathlib
import subprocess
import sys

VALUE_ERROR="ValueError"


def event(kind,**fields):
    return {"kind":kind,**fields}


def snapshot(total,entries):
    return {"total":total,"ledger":[{"client":c,"request":i,"delta":d,"reply":r} for c,i,d,r in entries]}


def answer(results,states,final):
    # Format hand-supplied totals, original replies and sorted ledger tuples.
    return {"results":[{"kind":k,"status":s,"reply":r} for k,s,r in results],
            "snapshots":[snapshot(total,entries) for total,entries in states],
            "final":snapshot(final[0],final[1])}


CASES=[
 ("empty",[0,[]],answer([],[],(0,[]))),
 ("negative initial without events",[-7,[]],answer([],[],(-7,[]))),
 ("new request commits",[0,[event("request",client="c",request=0,delta=5)]],answer([("request","executed",5)],[(5,[("c",0,5,5)])],(5,[("c",0,5,5)]))),
 ("retained retry and crash",[0,[event("request",client="c",request=0,delta=5),event("request",client="c",request=0,delta=5),event("crash")]],
 answer([("request","executed",5),("request","replayed",5),("crash","recovered",None)],[(5,[("c",0,5,5)]),(5,[("c",0,5,5)]),(5,[("c",0,5,5)])],(5,[("c",0,5,5)]))),
 ("interleaved totals original replies and conflicts",[0,[event("request",client="c1",request=1,delta=5),event("request",client="c1",request=2,delta=7),event("request",client="c1",request=1,delta=5),event("request",client="c1",request=1,delta=8),event("crash"),event("request",client="c2",request=1,delta=-2),event("request",client="c1",request=2,delta=7)]],
 answer([("request","executed",5),("request","executed",12),("request","replayed",5),("request","conflict",None),("crash","recovered",None),("request","executed",10),("request","replayed",12)],
 [(5,[("c1",1,5,5)]),(12,[("c1",1,5,5),("c1",2,7,12)]),(12,[("c1",1,5,5),("c1",2,7,12)]),(12,[("c1",1,5,5),("c1",2,7,12)]),(12,[("c1",1,5,5),("c1",2,7,12)]),(10,[("c1",1,5,5),("c1",2,7,12),("c2",1,-2,10)]),(10,[("c1",1,5,5),("c1",2,7,12),("c2",1,-2,10)])],
 (10,[("c1",1,5,5),("c1",2,7,12),("c2",1,-2,10)]))),
 ("full identity separates clients and request numbers",[10,[event("request",client="a",request=0,delta=1),event("request",client="b",request=0,delta=1),event("request",client="a",request=1,delta=1),event("request",client="b",request=0,delta=1)]],
 answer([("request","executed",11),("request","executed",12),("request","executed",13),("request","replayed",12)],
 [(11,[("a",0,1,11)]),(12,[("a",0,1,11),("b",0,1,12)]),(13,[("a",0,1,11),("a",1,1,13),("b",0,1,12)]),(13,[("a",0,1,11),("a",1,1,13),("b",0,1,12)])],
 (13,[("a",0,1,11),("a",1,1,13),("b",0,1,12)]))),
 ("ledger IDs sort numerically within client",[0,[event("request",client="c",request=10,delta=1),event("request",client="c",request=2,delta=2),event("request",client="c",request=0,delta=3)]],
 answer([("request","executed",1),("request","executed",3),("request","executed",6)],[(1,[("c",10,1,1)]),(3,[("c",2,2,3),("c",10,1,1)]),(6,[("c",0,3,6),("c",2,2,3),("c",10,1,1)])],(6,[("c",0,3,6),("c",2,2,3),("c",10,1,1)]))),
 ("Unicode and whitespace client namespaces",[0,[event("request",client="β",request=0,delta=1),event("request",client=" ",request=0,delta=2),event("request",client="A",request=0,delta=3),event("request",client="β",request=0,delta=1)]],
 answer([("request","executed",1),("request","executed",3),("request","executed",6),("request","replayed",1)],[(1,[("β",0,1,1)]),(3,[(" ",0,2,3),("β",0,1,1)]),(6,[(" ",0,2,3),("A",0,3,6),("β",0,1,1)]),(6,[(" ",0,2,3),("A",0,3,6),("β",0,1,1)])],(6,[(" ",0,2,3),("A",0,3,6),("β",0,1,1)]))),
 ("zero reply is still retained",[0,[event("request",client="c",request=0,delta=0),event("request",client="c",request=0,delta=0),event("request",client="c",request=0,delta=1)]],
 answer([("request","executed",0),("request","replayed",0),("request","conflict",None)],[(0,[("c",0,0,0)]),(0,[("c",0,0,0)]),(0,[("c",0,0,0)])],(0,[("c",0,0,0)]))),
 ("negative deltas preserve original negative reply",[5,[event("request",client="a",request=0,delta=-8),event("request",client="a",request=1,delta=-2),event("request",client="a",request=0,delta=-8)]],
 answer([("request","executed",-3),("request","executed",-5),("request","replayed",-3)],[( -3,[("a",0,-8,-3)]),(-5,[("a",0,-8,-3),("a",1,-2,-5)]),(-5,[("a",0,-8,-3),("a",1,-2,-5)])],(-5,[("a",0,-8,-3),("a",1,-2,-5)]))),
 ("forget absent and empty crash",[7,[event("forget",client="c",request=0),event("crash")]],answer([("forget","absent",None),("crash","recovered",None)],[(7,[]),(7,[])],(7,[]))),
 ("eviction ends dedup retention without undo",[0,[event("request",client="c",request=0,delta=5),event("forget",client="c",request=0),event("request",client="c",request=0,delta=5),event("request",client="c",request=0,delta=5)]],
 answer([("request","executed",5),("forget","forgotten",None),("request","executed",10),("request","replayed",10)],[(5,[("c",0,5,5)]),(5,[]),(10,[("c",0,5,10)]),(10,[("c",0,5,10)])],(10,[("c",0,5,10)]))),
 ("single-key eviction retains unrelated original reply",[0,[event("request",client="a",request=0,delta=2),event("request",client="b",request=0,delta=10),event("forget",client="a",request=0),event("request",client="b",request=0,delta=10),event("request",client="a",request=0,delta=2),event("request",client="b",request=0,delta=10)]],
 answer([("request","executed",2),("request","executed",12),("forget","forgotten",None),("request","replayed",12),("request","executed",14),("request","replayed",12)],[(2,[("a",0,2,2)]),(12,[("a",0,2,2),("b",0,10,12)]),(12,[("b",0,10,12)]),(12,[("b",0,10,12)]),(14,[("a",0,2,14),("b",0,10,12)]),(14,[("a",0,2,14),("b",0,10,12)])],(14,[("a",0,2,14),("b",0,10,12)]))),
 ("new payload allowed after forgetting old association",[0,[event("request",client="c",request=0,delta=1),event("forget",client="c",request=0),event("request",client="c",request=0,delta=-3),event("request",client="c",request=0,delta=-3)]],
 answer([("request","executed",1),("forget","forgotten",None),("request","executed",-2),("request","replayed",-2)],[(1,[("c",0,1,1)]),(1,[]),(-2,[("c",0,-3,-2)]),(-2,[("c",0,-3,-2)])],(-2,[("c",0,-3,-2)]))),
 ("conflict preserves old payload and reply",[0,[event("request",client="c",request=0,delta=2),event("request",client="c",request=0,delta=7),event("request",client="c",request=1,delta=10),event("request",client="c",request=0,delta=2)]],
 answer([("request","executed",2),("request","conflict",None),("request","executed",12),("request","replayed",2)],[(2,[("c",0,2,2)]),(2,[("c",0,2,2)]),(12,[("c",0,2,2),("c",1,10,12)]),(12,[("c",0,2,2),("c",1,10,12)])],(12,[("c",0,2,2),("c",1,10,12)]))),
 ("crash preserves present and evicted state",[4,[event("request",client="c",request=0,delta=3),event("crash"),event("request",client="c",request=0,delta=3),event("forget",client="c",request=0),event("crash"),event("request",client="c",request=0,delta=3)]],
 answer([("request","executed",7),("crash","recovered",None),("request","replayed",7),("forget","forgotten",None),("crash","recovered",None),("request","executed",10)],[(7,[("c",0,3,7)]),(7,[("c",0,3,7)]),(7,[("c",0,3,7)]),(7,[]),(7,[]),(10,[("c",0,3,10)])],(10,[("c",0,3,10)]))),
 ("unbounded totals request IDs and payloads",[2**80,[event("request",client="c",request=2**100,delta=-2**81),event("request",client="c",request=2**100+1,delta=2**82),event("request",client="c",request=2**100,delta=-2**81)]],
 answer([("request","executed",-2**80),("request","executed",3*2**80),("request","replayed",-2**80)],
 [(-2**80,[("c",2**100,-2**81,-2**80)]),(3*2**80,[("c",2**100,-2**81,-2**80),("c",2**100+1,2**82,3*2**80)]),(3*2**80,[("c",2**100,-2**81,-2**80),("c",2**100+1,2**82,3*2**80)])],
 (3*2**80,[("c",2**100,-2**81,-2**80),("c",2**100+1,2**82,3*2**80)]))),
 ("maximum client name",[0,[event("request",client="c"*32,request=0,delta=1)]],answer([("request","executed",1)],[(1,[("c"*32,0,1,1)])],(1,[("c"*32,0,1,1)]))),
 ("equal empty snapshots must be independent",[0,[event("crash"),event("crash")]],answer([("crash","recovered",None),("crash","recovered",None)],[(0,[]),(0,[])],(0,[]))),
]
CASES.append(("same-client exact eviction counts a zero reply as present",[0,[event("request",client="c",request=0,delta=0),event("request",client="c",request=1,delta=5),event("forget",client="c",request=0),event("request",client="c",request=1,delta=5),event("forget",client="c",request=0),event("request",client="c",request=0,delta=2)]],
 answer([("request","executed",0),("request","executed",5),("forget","forgotten",None),("request","replayed",5),("forget","absent",None),("request","executed",7)],
 [(0,[("c",0,0,0)]),(5,[("c",0,0,0),("c",1,5,5)]),(5,[("c",1,5,5)]),(5,[("c",1,5,5)]),(5,[("c",1,5,5)]),(7,[("c",0,2,7),("c",1,5,5)])],
 (7,[("c",0,2,7),("c",1,5,5)]))))
ERROR_CASES=[
 ("initial bool",[True,[]]),("initial float",[0.0,[]]),("initial str",["0",[]]),("initial None",[None,[]]),
 ("events must list",[0,()]),("too many events",[0,[event("crash") for _ in range(65)]]),
 ("event must dict",[0,[[]]]),("missing kind",[0,[{}]]),("kind must string",[0,[{"kind":True}]]),("unknown kind",[0,[event("reset")]]),
 ("extra crash field",[0,[event("crash",client="c")]]),
 ("missing request client",[0,[event("request",request=0,delta=1)]]),
 ("missing request ID",[0,[event("request",client="c",delta=1)]]),
 ("missing request delta",[0,[event("request",client="c",request=0)]]),
 ("extra request field",[0,[event("request",client="c",request=0,delta=1,extra=0)]]),
 ("nonstring event key",[0,[{**event("request",client="c",request=0,delta=1),1:0}]]),
 ("missing forget ID",[0,[event("forget",client="c")]]),
 ("extra forget delta",[0,[event("forget",client="c",request=0,delta=1)]]),
 ("empty request client",[0,[event("request",client="",request=0,delta=1)]]),
 ("empty forget client",[0,[event("forget",client="",request=0)]]),
 ("oversized client",[0,[event("request",client="c"*33,request=0,delta=1)]]),
 ("nonstring client",[0,[event("request",client=1,request=0,delta=1)]]),
 ("nonstring forget client",[0,[event("forget",client=["c"],request=0)]]),
 ("negative request ID",[0,[event("request",client="c",request=-1,delta=1)]]),
 ("negative forgotten ID",[0,[event("forget",client="c",request=-1)]]),
 ("boolean request ID",[0,[event("request",client="c",request=True,delta=1)]]),
 ("float request ID",[0,[event("forget",client="c",request=0.0)]]),
 ("string request ID",[0,[event("request",client="c",request="0",delta=1)]]),
 ("boolean delta",[0,[event("request",client="c",request=0,delta=True)]]),
 ("float delta",[0,[event("request",client="c",request=0,delta=1.0)]]),
 ("string delta",[0,[event("request",client="c",request=0,delta="1")]]),
 ("None delta",[0,[event("request",client="c",request=0,delta=None)]]),
 ("invalid retry payload still malformed",[0,[event("request",client="c",request=0,delta=1),event("request",client="c",request=0,delta=True)]]),
 ("malformed later event",[0,[event("request",client="c",request=0,delta=2),event("forget",client="c",request=0,bad=1)]]),
]
CASES.extend((name,args,VALUE_ERROR) for name,args in ERROR_CASES)
# Closed-form boundaries placed after errors so history validation stays small.
CASES.append(("64 distinct commits",[0,[event("request",client="c",request=i,delta=1) for i in range(64)]],
 answer([("request","executed",i+1) for i in range(64)],[(i+1,[("c",j,1,j+1) for j in range(i+1)]) for i in range(64)],(64,[("c",j,1,j+1) for j in range(64)]))))
CASES.append(("64 retained attempts one effect",[0,[event("request",client="c",request=0,delta=1) for _ in range(64)]],
 answer([("request","executed",1)]+[("request","replayed",1) for _ in range(63)],[(1,[("c",0,1,1)]) for _ in range(64)],(1,[("c",0,1,1)]))))
CASES.extend([CASES[0],CASES[4],CASES[0]])

def fingerprint(value):
    kind=type(value)
    if kind is dict:
        return ["dict",sorted([[fingerprint(k),fingerprint(v)] for k,v in value.items()],key=repr)]
    if kind in (list,tuple): return [kind.__name__,[fingerprint(v) for v in value]]
    if kind in (set,frozenset): return [kind.__name__,sorted([fingerprint(v) for v in value],key=repr)]
    if value is None:return ["none"]
    if kind in (bool,int,str):return [kind.__name__,value]
    if kind in (float,bytes):return [kind.__name__,repr(value)]
    return ["unsupported",kind.__module__,kind.__qualname__]


def run(candidate):
    payload=base64.b64encode(repr([args for _,args,_ in CASES]).encode()).decode()
    runner=r'''import ast,base64,copy,importlib.util,json,sys

def fingerprint(value):
    kind=type(value)
    if kind is dict:return ["dict",sorted([[fingerprint(k),fingerprint(v)] for k,v in value.items()],key=repr)]
    if kind in (list,tuple):return [kind.__name__,[fingerprint(v) for v in value]]
    if kind in (set,frozenset):return [kind.__name__,sorted([fingerprint(v) for v in value],key=repr)]
    if value is None:return ["none"]
    if kind in (bool,int,str):return [kind.__name__,value]
    if kind in (float,bytes):return [kind.__name__,repr(value)]
    return ["unsupported",kind.__module__,kind.__qualname__]

def mutable_objects(value,found=None):
    if found is None:found={}
    if type(value) in (dict,list):
        if id(value) in found:return found
        found[id(value)]=value
    if type(value) is dict:
        for key,child in value.items():mutable_objects(key,found);mutable_objects(child,found)
    elif type(value) in (list,tuple,set,frozenset):
        for child in value:mutable_objects(child,found)
    return found

def independent(values,forbidden):
    seen=set(forbidden)
    def visit(value):
        if type(value) in (dict,list):
            if id(value) in seen:return False
            seen.add(id(value))
        if type(value) is dict:return all(visit(k) and visit(v) for k,v in value.items())
        if type(value) in (list,tuple):return all(visit(v) for v in value)
        return True
    return all(visit(v) for v in values)

spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
inputs=[];output_history=[];values=[];calls=[];input_objects={}
unchanged=True;stable=True;isolated=True
for args in ast.literal_eval(base64.b64decode(sys.argv[2]).decode()):
    supplied=copy.deepcopy(args)
    inputs.append((supplied,fingerprint(supplied)))
    mutable_objects(supplied,input_objects)
    try:
        value=m.run_invocations(*supplied)
    except ValueError:
        calls.append({"error":"ValueError"})
    except Exception as exc:
        calls.append({"error":type(exc).__name__})
    else:
        snap=fingerprint(value)
        values.append(value);output_history.append(snap)
        calls.append({"value":snap})
    for prior,before in inputs:
        unchanged=unchanged and fingerprint(prior)==before
        mutable_objects(prior,input_objects)
    for prior,before in zip(values,output_history):stable=stable and fingerprint(prior)==before
    isolated=isolated and independent(values,input_objects)
print("__RESULT__"+json.dumps({"calls":calls,"inputs_unchanged":unchanged,"outputs_unchanged":stable,"independent":isolated}))'''
    try:
        process=subprocess.run([sys.executable,"-B","-c",runner,str(pathlib.Path(candidate).resolve()),payload],capture_output=True,text=True,timeout=5)
        lines=[line[len("__RESULT__"):] for line in process.stdout.splitlines() if line.startswith("__RESULT__")]
        actual=json.loads(lines[-1]) if process.returncode==0 and lines else None
        expected={"calls":[{"error":"ValueError"} if value==VALUE_ERROR else {"value":fingerprint(value)} for _,_,value in CASES],
                  "inputs_unchanged":True,"outputs_unchanged":True,"independent":True}
        return actual==expected
    except (OSError,ValueError,subprocess.TimeoutExpired):return False


if __name__=="__main__":
    sys.exit(0 if len(sys.argv)==2 and run(sys.argv[1]) else 1)
