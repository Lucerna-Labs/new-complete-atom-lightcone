import base64,copy,json,pathlib,pickle,subprocess,sys
from fractions import Fraction
VALID=[
 (0,0,0,1,[]),
 (5,4,3,2,[{"time":2,"cost":5},{"time":2,"cost":1}]),
 (0,0,0,1,[{"time":0,"cost":1},{"time":10,"cost":1}]),
 (10,0,1,3,[{"time":1,"cost":1},{"time":1,"cost":1},{"time":4,"cost":1}]),
 (7,7,5,2,[{"time":0,"cost":7},{"time":0,"cost":1},{"time":1,"cost":2}]),
 (100,0,100,100,[{"time":1,"cost":1},{"time":1,"cost":1},{"time":2,"cost":2}]),
 (1,0,1,2,[{"time":1,"cost":1},{"time":2,"cost":1},{"time":4,"cost":1}]),
 (100,99,100,1,[{"time":0,"cost":100},{"time":1,"cost":1}]),
 (3,3,2,3,[{"time":0,"cost":1},{"time":1000000,"cost":1000}]),
 (8,0,7,5,[{"time":i,"cost":1} for i in range(128)]),
 (7,7,0,7,[{"time":0,"cost":3},{"time":0,"cost":4},{"time":0,"cost":1}]),
 (100,0,1,100,[{"time":99,"cost":1},{"time":100,"cost":1},{"time":100,"cost":1}])]
for capacity in (0,1,3,100):
 for initial in sorted({0,capacity}):
  for time in (0,2,1000000):
   VALID.append((capacity,initial,2,3,[{"time":time,"cost":3}]))
INVALID=[]
valid_args=[2,1,1,2,[]]
for i,values in enumerate([[-1,101,True,1.0],[True,-1,3,1.0],[-1,101,True,1.0],[0,101,True,1.0]]):
 for v in values:
  args=list(valid_args);args[i]=v;INVALID.append(args)
INVALID += [[2,0,1,1,items] for items in (
 None,(),{}, "not-list", [None], [{}], [{"time":0,"cost":1,"x":0}],
 [{"time":0}], [{"time":True,"cost":1}], [{"time":1.0,"cost":1}],
 [{"time":-1,"cost":1}],[{"time":1000001,"cost":1}],
 [{"time":0,"cost":True}],[{"time":0,"cost":0}],[{"time":0,"cost":1001}],
 [{"time":0,"cost":1.0}],[{"time":2,"cost":1},{"time":1,"cost":1}],
 [{"time":0,"cost":1}]*129)]
def oracle(capacity,initial,rate_num,rate_den,events):
 balance=Fraction(initial);previous=0;out=[]
 for event in events:
  balance=min(Fraction(capacity),balance+Fraction(event["time"]-previous)*Fraction(rate_num,rate_den))
  previous=event["time"];accepted=balance>=event["cost"]
  if accepted:balance-=event["cost"]
  out.append({"accepted":accepted,"balance":[balance.numerator,balance.denominator]})
 return out
assert oracle(*VALID[1])==[{"accepted":True,"balance":[0,1]},{"accepted":False,"balance":[0,1]}]
assert oracle(*VALID[3])==[{"accepted":False,"balance":[1,3]},{"accepted":False,"balance":[1,3]},{"accepted":True,"balance":[1,3]}]
assert oracle(*VALID[10])==[{"accepted":True,"balance":[4,1]},{"accepted":True,"balance":[0,1]},{"accepted":False,"balance":[0,1]}]
CALLS=[(list(v),oracle(*v),False) for v in VALID]+[(list(v),None,True) for v in INVALID]
CALLS += [(list(VALID[i]),oracle(*VALID[i]),False) for i in (1,0,9,3,0,9)]

def fp(v):
    if type(v) is dict:
        return ("dict",tuple(sorted(((fp(k),fp(x)) for k,x in v.items()),key=repr)))
    if type(v) in (list,tuple):
        return (type(v).__name__,tuple(fp(x) for x in v))
    if type(v) in (set,frozenset):
        return (type(v).__name__,tuple(sorted((fp(x) for x in v),key=repr)))
    if type(v) is float:return ("float",v.hex())
    if type(v) is bytes:return ("bytes",v.hex())
    if type(v) in (str,int,bool,type(None)):return (type(v).__name__,v)
    raise TypeError("unsupported native value")
def mutable_ids(v):
    if type(v) in (dict,list,set):
        yield id(v)
    if type(v) is dict:
        for k,x in v.items():
            yield from mutable_ids(k);yield from mutable_ids(x)
    elif type(v) in (list,tuple,set,frozenset):
        for x in v:yield from mutable_ids(x)

RUNNER="import base64,copy,importlib.util,json,pickle,sys\nspec=importlib.util.spec_from_file_location(\"candidate\",sys.argv[1]);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)\ndef fp(v):\n    if type(v) is dict:\n        return (\"dict\",tuple(sorted(((fp(k),fp(x)) for k,x in v.items()),key=repr)))\n    if type(v) in (list,tuple):\n        return (type(v).__name__,tuple(fp(x) for x in v))\n    if type(v) in (set,frozenset):\n        return (type(v).__name__,tuple(sorted((fp(x) for x in v),key=repr)))\n    if type(v) is float:return (\"float\",v.hex())\n    if type(v) is bytes:return (\"bytes\",v.hex())\n    if type(v) in (str,int,bool,type(None)):return (type(v).__name__,v)\n    raise TypeError(\"unsupported native value\")\ndef mutable_ids(v):\n    if type(v) in (dict,list,set):\n        yield id(v)\n    if type(v) is dict:\n        for k,x in v.items():\n            yield from mutable_ids(k);yield from mutable_ids(x)\n    elif type(v) in (list,tuple,set,frozenset):\n        for x in v:yield from mutable_ids(x)\n\nvalues=[];retained=[];saved=[];output_ids=set();unchanged=True;independent=True\nfor args in pickle.loads(base64.b64decode(sys.argv[2])):\n    supplied=copy.deepcopy(args);retained.append((supplied,fp(supplied)))\n    try:value=m.bucket_events(*supplied)\n    except Exception as exc:\n        values.append({\"ok\":False,\"error\":type(exc).__name__})\n    else:\n        before=fp(value);occ=list(mutable_ids(value))\n        input_ids=set()\n        for old,_ in retained:input_ids.update(mutable_ids(old))\n        independent=independent and len(occ)==len(set(occ)) and not bool(set(occ)&(output_ids|input_ids))\n        output_ids.update(occ);saved.append((value,before))\n        values.append({\"ok\":True,\"fingerprint\":before})\n    unchanged=unchanged and all(fp(old)==before for old,before in retained)\n    unchanged=unchanged and all(fp(old)==before for old,before in saved)\ninput_ids=set()\nfor old,_ in retained:input_ids.update(mutable_ids(old))\nindependent=independent and not bool(output_ids&input_ids)\nprint(\"__RESULT__\"+json.dumps({\"values\":values,\"unchanged\":unchanged,\"independent\":independent}))\n"

def run(candidate):
    payload=base64.b64encode(pickle.dumps([args for args,expected,error in CALLS],protocol=4)).decode()
    runner=RUNNER
    try:
        result=subprocess.run([sys.executable,"-B","-c",runner,str(pathlib.Path(candidate).resolve()),payload],
                              capture_output=True,text=True,timeout=5)
        lines=[line[len("__RESULT__"):] for line in result.stdout.splitlines() if line.startswith("__RESULT__")]
        if result.returncode or not lines:return False,"candidate execution/native values"
        packet=json.loads(lines[-1])
        if packet.get("unchanged") is not True:return False,"current/prior input or output mutation"
        if packet.get("independent") is not True:return False,"mutable aliasing"
        expected=[{"ok":False,"error":"ValueError"} if error else
                  {"ok":True,"fingerprint":json.loads(json.dumps(fp(value)))} for args,value,error in CALLS]
        if packet.get("values")!=expected:
            for i,(a,b) in enumerate(zip(packet.get("values",[]),expected)):
                if a!=b:return False,"case "+str(i)
            return False,"output count"
        return True,str(len(CALLS))+" deterministic calls"
    except (OSError,ValueError,TypeError,subprocess.TimeoutExpired):
        return False,"candidate execution"
if __name__=="__main__":
    ok,detail=run(sys.argv[1]) if len(sys.argv)==2 else (False,"candidate path required")
    print(("PASS: " if ok else "FAIL: ")+detail)
    sys.exit(0 if ok else 1)
