import ast
import base64
import json
import pathlib
import subprocess
import sys

VALUE_ERROR="ValueError"


def state(spec):
    return {name:{"issued":v[0],"floor":v[1],"value":v[2]} for name,v in spec.items()}


def event(kind,**fields):
    return {"kind":kind,**fields}


def row(kind,resource=None,token=None,accepted=None,value=None):
    return {"kind":kind,"resource":resource,"token":token,"accepted":accepted,"value":value}


def answer(results,states,final):
    # Formatting only: all state triples/results are literal hand answers.
    return {"results":list(results),"states":[state(s) for s in states],"final":state(final)}


CASES=[
 ("empty",[{},[]],answer([],[],{})),
 ("unchanged initial floor can lag issuer",[state({"R":(2,1,7)}),[]],answer([],[],{"R":(2,1,7)})),
 ("issue does not install",[state({"R":(0,0,5)}),[event("issue",resource="R")]],answer([row("issue","R",1,None,5)],[{"R":(1,0,5)}],{"R":(1,0,5)})),
 ("issuance installation stale and equal writes",[state({"R":(1,1,0)}),[event("issue",resource="R"),event("write",resource="R",token=1,delta=5),event("install",resource="R",token=2),event("write",resource="R",token=1,delta=100),event("write",resource="R",token=2,delta=7),event("write",resource="R",token=2,delta=-2),event("crash"),event("write",resource="R",token=2,delta=0)]],
 answer([row("issue","R",2,None,0),row("write","R",1,True,5),row("install","R",2,True,5),row("write","R",1,False,5),row("write","R",2,True,12),row("write","R",2,True,10),row("crash"),row("write","R",2,True,10)],
 [{"R":(2,1,0)},{"R":(2,1,5)},{"R":(2,2,5)},{"R":(2,2,5)},{"R":(2,2,12)},{"R":(2,2,10)},{"R":(2,2,10)},{"R":(2,2,10)}],{"R":(2,2,10)})),
 ("install changes floor not value",[state({"R":(3,0,9)}),[event("install",resource="R",token=2),event("install",resource="R",token=2),event("install",resource="R",token=1),event("install",resource="R",token=3)]],
 answer([row("install","R",2,True,9),row("install","R",2,True,9),row("install","R",1,False,9),row("install","R",3,True,9)],
 [{"R":(3,2,9)},{"R":(3,2,9)},{"R":(3,2,9)},{"R":(3,3,9)}],{"R":(3,3,9)})),
 ("write itself installs its larger epoch",[state({"R":(5,0,10)}),[event("write",resource="R",token=3,delta=4),event("write",resource="R",token=2,delta=9),event("write",resource="R",token=5,delta=1),event("write",resource="R",token=3,delta=8)]],
 answer([row("write","R",3,True,14),row("write","R",2,False,14),row("write","R",5,True,15),row("write","R",3,False,15)],
 [{"R":(5,3,14)},{"R":(5,3,14)},{"R":(5,5,15)},{"R":(5,5,15)}],{"R":(5,5,15)})),
 ("resources have separate issuer and floor namespaces",[state({"A":(2,1,0),"B":(1,0,10)}),[event("issue",resource="A"),event("write",resource="B",token=1,delta=2),event("install",resource="A",token=2),event("write",resource="A",token=1,delta=5),event("write",resource="B",token=1,delta=-3)]],
 answer([row("issue","A",3,None,0),row("write","B",1,True,12),row("install","A",2,True,0),row("write","A",1,False,0),row("write","B",1,True,9)],
 [{"A":(3,1,0),"B":(1,0,10)},{"A":(3,1,0),"B":(1,1,12)},{"A":(3,2,0),"B":(1,1,12)},{"A":(3,2,0),"B":(1,1,12)},{"A":(3,2,0),"B":(1,1,9)}],{"A":(3,2,0),"B":(1,1,9)})),
 ("crash preserves all durable fields",[state({"R":(3,2,7)}),[event("crash"),event("write",resource="R",token=1,delta=99),event("write",resource="R",token=2,delta=1),event("issue",resource="R"),event("crash"),event("write",resource="R",token=4,delta=-8)]],
 answer([row("crash"),row("write","R",1,False,7),row("write","R",2,True,8),row("issue","R",4,None,8),row("crash"),row("write","R",4,True,0)],
 [{"R":(3,2,7)},{"R":(3,2,7)},{"R":(3,2,8)},{"R":(4,2,8)},{"R":(4,2,8)},{"R":(4,4,0)}],{"R":(4,4,0)})),
 ("unbounded integer epochs and values",[state({"R":(2**90,2**90-1,-2**90)}),[event("install",resource="R",token=2**90),event("write",resource="R",token=2**90,delta=2**91),event("write",resource="R",token=2**90,delta=0)]],
 answer([row("install","R",2**90,True,-2**90),row("write","R",2**90,True,2**90),row("write","R",2**90,True,2**90)],
 [{"R":(2**90,2**90,-2**90)},{"R":(2**90,2**90,2**90)},{"R":(2**90,2**90,2**90)}],{"R":(2**90,2**90,2**90)})),
 ("Unicode and whitespace resource names",[state({"雪":(1,0,1)," ":(1,1,-1)}),[event("write",resource="雪",token=1,delta=-1),event("write",resource=" ",token=1,delta=2)]],
 answer([row("write","雪",1,True,0),row("write"," ",1,True,1)],[{"雪":(1,1,0)," ":(1,1,-1)},{"雪":(1,1,0)," ":(1,1,1)}],{"雪":(1,1,0)," ":(1,1,1)})),
 ("empty resources may crash repeatedly",[{},[event("crash"),event("crash")]],answer([row("crash"),row("crash")],[{},{}],{})),
 ("maximum resource name",[state({"R"*32:(1,1,0)}),[event("write",resource="R"*32,token=1,delta=1)]],answer([row("write","R"*32,1,True,1)],[{"R"*32:(1,1,1)}],{"R"*32:(1,1,1)})),
]
# Closed forms: one write per independent resource;64 equal-epoch increments.
NAMES=[f'R{i}' for i in range(8)]
CASES.append(("maximum resources",[state({r:(1,0,i) for i,r in enumerate(NAMES)}),[event("write",resource=r,token=1,delta=1) for r in NAMES]],
 answer([row("write",r,1,True,i+1) for i,r in enumerate(NAMES)],
 [{r:(1,1 if j<=i else 0,j+1 if j<=i else j) for j,r in enumerate(NAMES)} for i in range(8)],{r:(1,1,i+1) for i,r in enumerate(NAMES)})))
CASES.append(("maximum events all equal epoch",[state({"R":(1,1,0)}),[event("write",resource="R",token=1,delta=1) for _ in range(64)]],
 answer([row("write","R",1,True,i) for i in range(1,65)],[{"R":(1,1,i)} for i in range(1,65)],{"R":(1,1,64)})))
INITIAL=state({"R":(2,1,0)})
CASES.append(("zero delta still installs and obeys the epoch gate",[state({"R":(3,1,7)}),[event("write",resource="R",token=3,delta=0),event("write",resource="R",token=2,delta=0),event("write",resource="R",token=1,delta=9)]],
 answer([row("write","R",3,True,7),row("write","R",2,False,7),row("write","R",1,False,7)],
 [{"R":(3,3,7)},{"R":(3,3,7)},{"R":(3,3,7)}],{"R":(3,3,7)})))
ERROR_CASES=[
 ("resources must dict",[[],[]]),
 ("too many resources",[state({str(i):(1,0,0) for i in range(9)}),[]]),
 ("empty resource name",[state({"":(1,0,0)}),[]]),
 ("oversized resource name",[state({"a"*33:(1,0,0)}),[]]),
 ("nonstring resource name",[state({1:(1,0,0)}),[]]),
 ("resource record must dict",[{"R":None},[]]),
 ("missing resource field",[{"R":{"issued":1,"floor":0}},[]]),
 ("extra resource field",[{"R":{"issued":1,"floor":0,"value":0,"extra":0}},[]]),
 ("negative issued",[state({"R":(-1,0,0)}),[]]),
 ("negative floor",[state({"R":(1,-1,0)}),[]]),
 ("floor above issued",[state({"R":(1,2,0)}),[]]),
 ("bool issued",[state({"R":(True,0,0)}),[]]),
 ("bool floor",[state({"R":(1,False,0)}),[]]),
 ("bool value",[state({"R":(1,0,True)}),[]]),
 ("float issued",[state({"R":(1.0,0,0)}),[]]),
 ("float floor",[state({"R":(1,0.0,0)}),[]]),
 ("float value",[state({"R":(1,0,0.0)}),[]]),
 ("events must list",[INITIAL,()]),
 ("too many events",[INITIAL,[event("crash") for _ in range(65)]]),
 ("event must dict",[INITIAL,[None]]),
 ("kind missing",[INITIAL,[{}]]),
 ("kind not string",[INITIAL,[{"kind":True}]]),
 ("unknown kind",[INITIAL,[event("reset")]]),
 ("crash has extra field",[INITIAL,[event("crash",resource="R")]]),
 ("issue missing resource",[INITIAL,[event("issue")]]),
 ("issue extra token",[INITIAL,[event("issue",resource="R",token=1)]]),
 ("unknown resource",[INITIAL,[event("issue",resource="Q")]]),
 ("nonstring event resource",[INITIAL,[event("issue",resource=["R"])]]),
 ("install missing token",[INITIAL,[event("install",resource="R")]]),
 ("write missing delta",[INITIAL,[event("write",resource="R",token=1)]]),
 ("write extra key",[INITIAL,[event("write",resource="R",token=1,delta=1,extra=0)]]),
 ("token zero",[INITIAL,[event("install",resource="R",token=0)]]),
 ("negative token",[INITIAL,[event("write",resource="R",token=-1,delta=1)]]),
 ("bool token",[INITIAL,[event("write",resource="R",token=True,delta=1)]]),
 ("float token",[INITIAL,[event("install",resource="R",token=1.0)]]),
 ("unissued token",[INITIAL,[event("install",resource="R",token=3)]]),
 ("bool delta",[INITIAL,[event("write",resource="R",token=1,delta=True)]]),
 ("float delta",[INITIAL,[event("write",resource="R",token=1,delta=1.0)]]),
 ("bad delta on stale request still invalid",[state({"R":(2,2,0)}),[event("write",resource="R",token=1,delta="bad")]]),
 ("issuance at other resource does not validate token",[state({"A":(0,0,0),"B":(0,0,0)}),[event("issue",resource="A"),event("write",resource="B",token=1,delta=1)]]),
 ("malformed later event preserves inputs",[INITIAL,[event("write",resource="R",token=1,delta=2),{"kind":"crash","bad":1}]]),
]
CASES.extend((name,args,VALUE_ERROR) for name,args in ERROR_CASES)
CASES.extend([CASES[0],CASES[3],CASES[0]])

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
        value=m.run_fences(*supplied)
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
