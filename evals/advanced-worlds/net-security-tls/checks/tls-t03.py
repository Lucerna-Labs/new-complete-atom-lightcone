import base64
import json
import pathlib
import subprocess
import sys


def header(t, host, age, include=False, secure=True, ok=True):
    return {"type":"header","time":t,"host":host,"max_age":age,
            "include_subdomains":include,"secure":secure,"transport_ok":ok}

def request(t, host, port=None, scheme="http", error=False):
    return {"type":"request","time":t,"host":host,"scheme":scheme,
            "port":port,"transport_error":error}

def policy(expiry, include):
    return {"expires_at":expiry,"include_subdomains":include}

E = {"example.test":policy(101,True)}
EA = {"example.test":policy(101,True),"a.example.test":policy(17,False)}
E33 = {"example.test":policy(33,False)}
EC30 = {"example.test":policy(33,False),"child.a.example.test":policy(30,False)}
EC27 = {"example.test":policy(33,False),"child.a.example.test":policy(27,True)}
ROOT32 = {"root.test":policy(32,True)}
E38 = {"example.test":policy(38,True)}

def answer(policies, known, scheme=None, port=None, terminate=None):
    return {"known_hsts":known,"scheme":scheme,"port":port,
            "must_terminate":terminate,"policies":policies}

# Expected policies and results are literal independent state calculations.
EVENTS = [
    header(0,"example.test",100,True,secure=False),
    header(1,"ExAmPlE.test",100,True),
    request(2,"a.example.test",80), request(3,"a.example.test",8080),
    request(4,"a.example.test"), request(5,"badexample.test",80),
    request(6,"a.example.test",443,"https",True),
    header(7,"a.example.test",10), header(8,"a.example.test",0),
    request(9,"a.example.test",443),
    header(10,"example.test",0,secure=False),
    header(11,"example.test",0,ok=False),
    request(12,"example.test",80,error=True),
    header(13,"EXAMPLE.TEST",20,False),
    request(14,"a.example.test",80), request(15,"example.test"),
    header(16,"192.0.2.1",100,True), request(17,"192.0.2.1",80,error=True),
    header(18,"2001:db8::1",100,True), request(19,"2001:db8::1",8080),
    header(20,"child.a.example.test",10,False),
    request(21,"x.child.a.example.test"),
    header(22,"child.a.example.test",5,True),
    request(23,"x.child.a.example.test"),
    header(24,"else.test",0), request(27,"x.child.a.example.test"),
    header(28,"example.test",0),
    request(29,"example.test",443,"https",True),
    header(31,"root.test",1,True), request(32,"x.root.test"),
    header(33,"example.test",5,True),
    request(34,"example.test.evil"), request(35,"notexample.test"),
    request(36,"Sub.EXAMPLE.test"), request(38,"example.test"),
]
EXPECTED_VALUES = [
    answer({},False), answer(E,True),
    answer(E,True,"https",443,False), answer(E,True,"https",8080,False),
    answer(E,True,"https",None,False), answer(E,False,"http",80,False),
    answer(E,True,"https",443,True), answer(EA,True), answer(E,True),
    answer(E,True,"https",443,False), answer(E,True), answer(E,True),
    answer(E,True,"https",443,True), answer(E33,True),
    answer(E33,False,"http",80,False), answer(E33,True,"https",None,False),
    answer(E33,False), answer(E33,False,"http",80,False),
    answer(E33,False), answer(E33,False,"http",8080,False),
    answer(EC30,True), answer(EC30,False,"http",None,False),
    answer(EC27,True), answer(EC27,True,"https",None,False),
    answer(EC27,False), answer(E33,False,"http",None,False),
    answer({},False), answer({},False,"https",443,False),
    answer(ROOT32,True), answer({},False,"http",None,False),
    answer(E38,True), answer(E38,False,"http",None,False),
    answer(E38,False,"http",None,False), answer(E38,True,"https",None,False),
    answer({},False,"http",None,False),
]
EXTRA_HEADER = [header(0,"persist.test",10)]
EXTRA_REQUEST = [request(1,"persist.test")]
PARENT = {"parent.test":policy(100,True)}
PARENT_CHILD = {"parent.test":policy(100,True),"kid.parent.test":policy(51,False)}
CHILD = {"kid.parent.test":policy(51,False)}
EXTRA_TRACE = [header(0,"parent.test",100,True), header(1,"kid.parent.test",50),
    header(2,"parent.test",0), request(3,"kid.parent.test",80),
    request(4,"sibling.parent.test",80), request(5,"kid.parent.test",80,"https"),
    header(6,"failed.test",100,True,ok=False), request(7,"failed.test")]
EXTRA_EXPECTED = [answer(PARENT,True), answer(PARENT_CHILD,True), answer(CHILD,False),
    answer(CHILD,True,"https",443,False), answer(CHILD,False,"http",80,False),
    answer(CHILD,True,"https",80,False), answer(CHILD,False),
    answer(CHILD,False,"http",None,False)]
TRACES = [EVENTS, EVENTS, [], EXTRA_HEADER, EXTRA_REQUEST, EXTRA_TRACE]
EXPECTED = {"values":[EXPECTED_VALUES,EXPECTED_VALUES,[],
    [answer({"persist.test":policy(10,False)},True)],
    [answer({},False,"http",None,False)], EXTRA_EXPECTED],"unchanged":True}

def run(candidate):
    payload=base64.b64encode(json.dumps(TRACES).encode()).decode()
    runner=r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1]);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
traces=json.loads(base64.b64decode(sys.argv[2]));values=[];unchanged=True
for events in traces:
    given=copy.deepcopy(events);values.append(m.hsts_trace(given));unchanged=unchanged and given==events
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged}))'''
    try:
        p=subprocess.run([sys.executable,"-c",runner,str(pathlib.Path(candidate).resolve()),payload],capture_output=True,text=True,timeout=5)
        lines=[line[len("__RESULT__"):] for line in p.stdout.splitlines() if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if p.returncode==0 and lines else None
    except (OSError,subprocess.TimeoutExpired,ValueError):return None

def passes(result):
    if result != EXPECTED:
        return False
    return all(type(row["known_hsts"]) is bool
        and (row["must_terminate"] is None or type(row["must_terminate"]) is bool)
        and (row["port"] is None or type(row["port"]) is int)
        and all(type(p["expires_at"]) is int and type(p["include_subdomains"]) is bool
                for p in row["policies"].values())
        for trace in result["values"] for row in trace)

if __name__=="__main__":
    sys.exit(0 if len(sys.argv)==2 and passes(run(sys.argv[1])) else 1)
