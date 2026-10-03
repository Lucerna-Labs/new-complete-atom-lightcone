import base64
import json
import pathlib
import subprocess
import sys


def start(t,c,p,d):return {"kind":"start","at":t,"connection":c,"probe":p,"timeout":d}
def pong(t,c,p):return {"kind":"pong","at":t,"connection":c,"probe":p}
def tick(t):return {"kind":"tick","at":t}
def pending(c,p,d):return {"connection":c,"probe":p,"deadline":d}
def state(s,p=None,a=None):return {"suspected":s,"pending":p,"pong_accepted":a}

A = [start(0,"c1","a",5), pong(1,"c1","wrong"), pong(2,"c2","a"),
     start(3,"c1","b",4), pong(4,"c1","a"), tick(6), tick(7), pong(8,"c1","b"),
     start(9,"c1","c",3), pong(10,"c1","a"), pong(11,"c1","c"), tick(12),
     pong(13,"c1","c"), start(14,"c2","a",2), pong(15,"c1","a"),
     pong(16,"c2","a"), start(16,"c2","b",1), pong(16,"c2","b"), tick(17)]
EA = [state(False,pending("c1","a",5)), state(False,pending("c1","a",5),False),
      state(False,pending("c1","a",5),False), state(False,pending("c1","b",7)),
      state(False,pending("c1","b",7),False), state(False,pending("c1","b",7)),
      state(True), state(True,None,False), state(True,pending("c1","c",12)),
      state(True,pending("c1","c",12),False), state(False,None,True), state(False),
      state(False,None,False), state(False,pending("c2","a",16)),
      state(False,pending("c2","a",16),False), state(True,None,False),
      state(True,pending("c2","b",17)), state(False,None,True), state(False)]
B = [start(0,"A","q1",2), start(1,"A","q2",4), tick(2),
     pong(3,"A","q1"), pong(4,"A","q2")]
EB = [state(False,pending("A","q1",2)),state(False,pending("A","q2",5)),
      state(False,pending("A","q2",5)),state(False,pending("A","q2",5),False),
      state(False,None,True)]
C = [pong(0,"unknown","none"),tick(10)]
EC = [state(False,None,False),state(False)]
D = [start(0,"persist","p",1),tick(1)]
ED = [state(False,pending("persist","p",1)),state(True)]
E = [start(0,"replace","old",2), start(3,"replace","new",4)]
EE = [state(False,pending("replace","old",2)),state(True,pending("replace","new",7))]
F = [start(0,"exact","old",2), start(2,"exact","new",4)]
EF = [state(False,pending("exact","old",2)),state(True,pending("exact","new",6))]
G = [start(0,"Case","Probe",4),pong(1,"case","Probe"),
     pong(2,"Case","probe"),pong(3,"Case","Probe")]
EG = [state(False,pending("Case","Probe",4)),state(False,pending("Case","Probe",4),False),
      state(False,pending("Case","Probe",4),False),state(False,None,True)]
TRACES = [A,B,[],C,D,[tick(0)],A,E,F,G]
EXPECTED = {"values":[EA,EB,[],EC,ED,[state(False)],EA,EE,EF,EG],"unchanged":True}


def run(candidate):
    payload=base64.b64encode(json.dumps(TRACES).encode()).decode()
    runner=r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1]);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
values=[];unchanged=True
for events in json.loads(base64.b64decode(sys.argv[2])):
    given=copy.deepcopy(events);values.append(m.heartbeat_trace(given));unchanged=unchanged and given==events
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged}))'''
    try:
        p=subprocess.run([sys.executable,"-c",runner,str(pathlib.Path(candidate).resolve()),payload],capture_output=True,text=True,timeout=5)
        lines=[line[len("__RESULT__"):] for line in p.stdout.splitlines() if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if p.returncode==0 and lines else None
    except (OSError,subprocess.TimeoutExpired,ValueError):return None


def passes(value):
    if value!=EXPECTED:return False
    return all(type(row["suspected"]) is bool
        and (row["pong_accepted"] is None or type(row["pong_accepted"]) is bool)
        and (row["pending"] is None or type(row["pending"]["deadline"]) is int)
        for trace in value["values"] for row in trace)

if __name__=="__main__":
    sys.exit(0 if len(sys.argv)==2 and passes(run(sys.argv[1])) else 1)
