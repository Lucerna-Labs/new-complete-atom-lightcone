import ast
import base64
import json
import pathlib
import subprocess
import sys

VALUE_ERROR = "ValueError"


def report(acceptor, prepare, accepted=None):
    return {"acceptor": acceptor, "prepare_ballot": prepare,
            "accepted": None if accepted is None else {"ballot": accepted[0], "value": accepted[1]}}


def answer(ready, responders, source=None, value=None):
    return {"ready": ready, "responders": list(responders), "source_ballot": source, "value": value}


# Literal answer tables; helpers only format records, not selection rules.
CASES = [
 ("no responses", [["A"],1,"p",[]], answer(False,[])),
 ("one voter may form majority", [["A"],1,"p",[report("A",1)]], answer(True,["A"],None,"p")),
 ("one prior acceptance", [["A"],7,"other",[report("A",7,(3,"v"))]], answer(True,["A"],3,"v")),
 ("two voters need both", [["B","A"],4,"p",[report("B",4)]], answer(False,["B"])),
 ("two matching empty reports", [["B","A"],4,"p",[report("B",4),report("A",4)]], answer(True,["A","B"],None,"p")),
 ("highest report constrains two-of-three", [["A","B","C"],8,"p",[report("B",8,(6,"six")),report("A",8)]], answer(True,["A","B"],6,"six")),
 ("duplicate replies are not voters", [["A","B","C"],8,"p",[report("A",8),report("A",8),report("A",8)]], answer(False,["A"])),
 ("duplicate matching data counted once", [["A","B","C"],8,"p",[report("B",8,(4,"x")),report("A",8,(4,"x")),report("A",8,(4,"x"))]], answer(True,["A","B"],4,"x")),
 ("ignore other prepare rounds", [["A","B","C"],10,"p",[report("A",9),report("B",11),report("C",10)]], answer(False,["C"])),
 ("ignored high acceptance cannot win", [["A","B","C"],10,"p",[report("A",10,(1,"one")),report("B",10),report("C",101,(100,"future"))]], answer(True,["A","B"],1,"one")),
 ("reachable blue-four red-three witness", [["A","B","C","D","E"],5,"p",[report("A",5,(4,"blue")),report("D",5,(3,"red")),report("E",5,(3,"red"))]], answer(True,["A","D","E"],4,"blue")),
 ("highest need not arrive last", [["A","B","C"],9,"p",[report("C",9,(8,"high")),report("B",9,(2,"low")),report("A",9,(1,"low"))]], answer(True,["A","B","C"],8,"high")),
 ("use every matching report not first quorum", [["A","B","C","D","E"],10,"p",[report("A",10,(1,"red")),report("B",10),report("C",10),report("D",10,(8,"blue")),report("E",10)]], answer(True,["A","B","C","D","E"],8,"blue")),
 ("even membership half is insufficient", [["A","B","C","D"],3,"p",[report("A",3),report("B",3)]], answer(False,["A","B"])),
 ("even membership strict majority", [["A","B","C","D"],3,"p",[report("D",3),report("B",3),report("A",3)]], answer(True,["A","B","D"],None,"p")),
 ("Unicode whitespace identities remain exact", [["β","A"," "],2,"雪",[report("β",2),report(" ",2)]], answer(True,[" ","β"],None,"雪")),
 ("same value at distinct ballots", [["A","B","C"],10,"p",[report("A",10,(3,"v")),report("B",10,(8,"v"))]], answer(True,["A","B"],8,"v")),
 ("unbounded integer ballot", [["A"],2**100,"p",[report("A",2**100,(2**100-1,"big"))]], answer(True,["A"],2**100-1,"big")),
 ("whitespace preferred is nonempty", [["A"],1," ",[report("A",1)]], answer(True,["A"],None," ")),
]
NAMES=[f'm{i:02}'+"x"*29 for i in range(15)]
MAX_REPORTS=[report(name,2,(1,"v"*32)) for name in NAMES]+[report(NAMES[0],2,(1,"v"*32)) for _ in range(113)]
CASES.append(("maximum members names values and reports",[NAMES,2,"p"*32,MAX_REPORTS],answer(True,NAMES,1,"v"*32)))
CASES.append(("128 duplicates still one identity",[["A","B","C"],1,"p",[report("A",1) for _ in range(128)]],answer(False,["A"])))
CASES.append(("accepted value hidden until prepare majority",[["A","B","C"],8,"p",[report("A",8,(7,"old"))]],answer(False,["A"])))
ERROR_CASES = [
 ("members must list",[("A",),1,"p",[]]),
 ("members empty",[[],1,"p",[]]),
 ("too many members",[[str(i) for i in range(16)],1,"p",[]]),
 ("duplicate member",[["A","A"],1,"p",[]]),
 ("empty member",[[""],1,"p",[]]),
 ("oversized member",[["a"*33],1,"p",[]]),
 ("nonstring member",[[1],1,"p",[]]),
 ("boolean ballot",[["A"],True,"p",[]]),
 ("zero ballot",[["A"],0,"p",[]]),
 ("negative ballot",[["A"],-1,"p",[]]),
 ("float ballot",[["A"],1.0,"p",[]]),
 ("empty preferred",[["A"],1,"",[]]),
 ("oversized preferred",[["A"],1,"p"*33,[]]),
 ("nonstring preferred",[["A"],1,None,[]]),
 ("reports must list",[["A"],1,"p",()]),
 ("too many reports",[["A"],1,"p",[report("A",1) for _ in range(129)]]),
 ("report must dict",[["A"],1,"p",[None]]),
 ("missing report key",[["A"],1,"p",[{"acceptor":"A","prepare_ballot":1}]]),
 ("extra report key",[["A"],1,"p",[{**report("A",1),"extra":0}]]),
 ("nonstring report key",[["A"],1,"p",[{**report("A",1),1:0}]]),
 ("unknown matching acceptor",[["A"],1,"p",[report("B",1)]]),
 ("unknown ignored acceptor",[["A"],1,"p",[report("B",2)]]),
 ("nonstring acceptor",[["A"],1,"p",[report(True,1)]]),
 ("boolean prepare",[["A"],1,"p",[report("A",True)]]),
 ("zero prepare",[["A"],1,"p",[report("A",0)]]),
 ("float prepare",[["A"],1,"p",[report("A",2.0)]]),
 ("accepted must dict or None",[["A"],2,"p",[{"acceptor":"A","prepare_ballot":2,"accepted":[]}]]),
 ("missing accepted field",[["A"],2,"p",[{"acceptor":"A","prepare_ballot":2,"accepted":{"ballot":1}}]]),
 ("extra accepted field",[["A"],2,"p",[{"acceptor":"A","prepare_ballot":2,"accepted":{"ballot":1,"value":"v","extra":0}}]]),
 ("boolean accepted ballot",[["A"],2,"p",[report("A",2,(True,"v"))]]),
 ("zero accepted ballot",[["A"],2,"p",[report("A",2,(0,"v"))]]),
 ("float accepted ballot",[["A"],2,"p",[report("A",2,(1.0,"v"))]]),
 ("accepted equals prepare",[["A"],2,"p",[report("A",2,(2,"v"))]]),
 ("accepted exceeds prepare",[["A"],2,"p",[report("A",2,(3,"v"))]]),
 ("invalid accepted in ignored round",[["A"],2,"p",[report("A",3,(3,"v"))]]),
 ("empty accepted value",[["A"],2,"p",[report("A",2,(1,""))]]),
 ("oversized accepted value",[["A"],2,"p",[report("A",2,(1,"v"*33))]]),
 ("nonstring accepted value",[["A"],2,"p",[report("A",2,(1,1))]]),
 ("same voter contradicts before quorum",[["A","B","C"],3,"p",[report("A",3),report("A",3,(1,"v"))]]),
 ("same ballot differs before quorum",[["A","B","C","D","E"],3,"p",[report("A",3,(1,"x")),report("B",3,(1,"y"))]]),
 ("negative prepare ballot",[["A"],2,"p",[report("A",-1)]]),
 ("negative accepted ballot",[["A"],2,"p",[report("A",2,(-1,"v"))]]),
 ("one voter contradicts ballot while value agrees",[["A","B","C"],5,"p",[report("A",5,(2,"v")),report("A",5,(3,"v"))]]),
]
CASES.extend((name,args,VALUE_ERROR) for name,args in ERROR_CASES)
CASES.extend([CASES[0],CASES[10],CASES[0]])

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
        value=m.choose_proposal(*supplied)
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
