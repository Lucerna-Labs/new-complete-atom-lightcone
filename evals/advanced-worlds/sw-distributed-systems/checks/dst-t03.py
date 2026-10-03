import base64, copy, json, pathlib, subprocess, sys

def L(i,p): return {"id":i,"process":p,"kind":"local"}
def S(i,p,m,to): return {"id":i,"process":p,"kind":"send","message":m,"to":to}
def R(i,p,m): return {"id":i,"process":p,"kind":"receive","message":m}

VALID=[
 (1,[],[],None),
 (1,[L("one",0),S("ss",0,"m",0),R("rr",0,"m"),R("rr2",0,"m")],[["one","ss"],["ss","rr"],["rr","rr2"],["rr","ss"],["rr","rr"]],None),
 (2,[L("p0a",0),L("p0b",0),L("p1a",1)],[["p0b","p1a"],["p0a","p0b"]],None),
 (2,[S("s0",0,"m0",1),L("later",0),R("r0",1,"m0"),S("s1",1,"m1",0),L("p0",0),R("r1",0,"m1")],[["s0","later"],["s0","r0"],["later","r0"],["s1","r1"],["r0","r1"]],None),
 (3,[S("self",0,"selfm",0),R("selfr",0,"selfm"),S("lost",1,"lostm",2),L("q",2),R("dup",2,"lostm")],[["self","selfr"],["lost","dup"],["q","dup"],["selfr","lost"],["dup","dup"]],None),
]
boundary_trace=[L("e"+str(i),i%8) for i in range(64)]
boundary_pairs=[list([["e0","e56"],["e56","e0"],["e7","e63"],["e7","e1"],["e10","e10"]][i%5]) for i in range(128)]
VALID.append((8,boundary_trace,boundary_pairs,None))
VALID.append((3,[S("unreceived",0,"never",2),L("independent",1),L("after-send",0)],
              [["unreceived","independent"],["unreceived","after-send"],["after-send","independent"]],None))
VALID.append((1,[S("e"*32,0,"m"*32,0),R("r"*32,0,"m"*32)],[["e"*32,"r"*32]],None))
VALID.append((3,[S("a",0,"ab",1),S("b",1,"ba",0),R("ar",0,"ba"),R("br",1,"ab")],
              [["ar","br"],["a","br"],["b","ar"],["br","ar"],["a","b"],["ar","ar"]],None))

INVALID=[(True,[],[]),(2,[R("r",1,"missing")],[]),(2,[S("s",0,"m",1),R("r",0,"m")],[]),(2,[L("x",0),L("x",1)],[]),(2,[L("x",0)],[["unknown","x"]]),(2,[{"id":"x","process":0,"kind":"bad"}],[]),(2,[L("x"*33,0)],[]),(2,[S("s",0,"m"*33,1)],[])]

INVALID.extend([(0,[],[]),(9,[],[]),(2,[L("bad",True)],[]),
 (2,[S("a",0,"m",1),S("b",1,"m",0)],[]),
 (1,[L("z"+str(i),0) for i in range(65)],[]),
 (1,[L("a",0)],[["a","a"]]*129),
 (1,[{"id":"a","process":0,"kind":"local","extra":1}],[]),
 (2,[S("s",0,"m",True)],[]),(2,[L("bad",2)],[])])

def oracle(n,trace,pairs):
    events=[];pred={};send={};last=[None]*n
    for raw in trace:
        ps=[];p=raw["process"]
        if last[p] is not None:ps.append(last[p])
        if raw["kind"]=="receive":ps.append(send[raw["message"]]["id"])
        pred[raw["id"]]=ps;last[p]=raw["id"]
        if raw["kind"]=="send":send[raw["message"]]=raw
    def ancestors(x,seen=None):
        seen=set() if seen is None else seen
        if x in seen:return seen
        seen.add(x)
        for p in pred[x]:ancestors(p,seen)
        return seen
    process={e["id"]:e["process"] for e in trace}; order=[e["id"] for e in trace]
    events=[]
    for ident in order:
        anc=ancestors(ident); counts=[sum(process[x]==p for x in anc) for p in range(n)]
        def longest(x,memo=None):
            memo={} if memo is None else memo
            if x in memo:return memo[x]
            memo[x]=1+max((longest(p,memo) for p in pred[x]),default=0);return memo[x]
        events.append({"id":ident,"lamport":longest(ident),"vector":counts})
    def before(a,b):return a!=b and a in ancestors(b)
    orders=["same" if a==b else "before" if before(a,b) else "after" if before(b,a) else "concurrent" for a,b in pairs]
    return {"events":events,"orders":orders}

for i,(n,t,p,e) in enumerate(VALID):VALID[i]=(n,t,p,oracle(n,t,p))
EXPECTED=[{"ok":True,"v":e} for _,_,_,e in VALID]+[{"ok":False,"error":"ValueError"} for _ in INVALID]
LITERAL_EXPECTED=VALID[1][3]
assert LITERAL_EXPECTED["events"]==[{"id":"one","lamport":1,"vector":[1]}, {"id":"ss","lamport":2,"vector":[2]}, {"id":"rr","lamport":3,"vector":[3]}, {"id":"rr2","lamport":4,"vector":[4]}]
assert LITERAL_EXPECTED["orders"]==["before","before","before","after","same"]

assert VALID[-1][3]=={"events":[{"id":"a","lamport":1,"vector":[1,0,0]},
 {"id":"b","lamport":1,"vector":[0,1,0]},{"id":"ar","lamport":2,"vector":[2,1,0]},
 {"id":"br","lamport":2,"vector":[1,2,0]}],
 "orders":["concurrent","before","before","concurrent","concurrent","same"]}

# Repeated calls are interleaved AFTER invalid calls so a cached/shared result
# or mutation restored only at a later call cannot hide from per-call checks.
CALLS=[(n,t,p,e,False) for n,t,p,e in VALID]+[(n,t,p,None,True) for n,t,p in INVALID]
CALLS += [(*VALID[i],False) for i in [3,0,1,3,len(VALID)-1,0]]
def run(candidate):
    payload=base64.b64encode(json.dumps([[n,t,p,error] for n,t,p,e,error in CALLS]).encode()).decode()
    runner=r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1]);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
def fp(v):
 if type(v) is dict and all(type(k) is str for k in v):return ("dict",tuple((k,fp(v[k])) for k in sorted(v)))
 if type(v) is list:return ("list",tuple(fp(x) for x in v))
 if type(v) in (str,int,bool,type(None)):return (type(v).__name__,v)
 raise TypeError("unsupported native type")
def ids(v):
 if type(v) is dict:
  yield id(v)
  for x in v.values():yield from ids(x)
 elif type(v) is list:
  yield id(v)
  for x in v:yield from ids(x)
def shape(v,n):
 assert type(v) is dict and set(v)=={"events","orders"}
 assert type(v["events"]) is list and type(v["orders"]) is list
 for row in v["events"]:
  assert type(row) is dict and set(row)=={"id","lamport","vector"}
  assert type(row["id"]) is str and type(row["lamport"]) is int
  assert type(row["vector"]) is list and len(row["vector"])==n
  assert all(type(x) is int for x in row["vector"])
 assert all(type(x) is str and x in ("same","before","after","concurrent") for x in v["orders"])
values=[];retained=[];saved=[];output_ids=set();unchanged=True;independent=True
for n,trace,pairs,error in json.loads(base64.b64decode(sys.argv[2])):
 supplied=copy.deepcopy([n,trace,pairs]);retained.append((supplied,fp(supplied)))
 try:value=m.annotate_trace(*supplied)
 except Exception as exc:values.append({"ok":False,"error":type(exc).__name__})
 else:
  shape(value,n);before=fp(value);occ=list(ids(value))
  all_input_ids=set()
  for old,_ in retained:all_input_ids.update(ids(old))
  independent=independent and len(occ)==len(set(occ)) and not bool(set(occ)&(output_ids|all_input_ids))
  output_ids.update(occ);saved.append((value,before));values.append({"ok":True,"v":value})
 unchanged=unchanged and all(fp(old)==before for old,before in retained)
 unchanged=unchanged and all(fp(old)==before for old,before in saved)
all_input_ids=set()
for old,_ in retained:all_input_ids.update(ids(old))
independent=independent and not bool(output_ids&all_input_ids)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged,"independent":independent}))'''
    try:
        p=subprocess.run([sys.executable,"-B","-c",runner,str(pathlib.Path(candidate).resolve()),payload],
                         capture_output=True,text=True,timeout=5)
        lines=[x[len("__RESULT__"):] for x in p.stdout.splitlines() if x.startswith("__RESULT__")]
        if p.returncode or not lines:return False,"candidate execution/native schema"
        observed=json.loads(lines[-1])
        if observed.get("unchanged") is not True:return False,"input/prior-output mutation"
        if observed.get("independent") is not True:return False,"mutable aliasing"
        outputs=observed.get("values")
        if type(outputs) is not list or len(outputs)!=len(CALLS):return False,"output count"
        for i,((n,t,p,expected,error),actual) in enumerate(zip(CALLS,outputs)):
            target={"ok":False,"error":"ValueError"} if error else {"ok":True,"v":expected}
            if actual!=target:return False,f"case {i}"
        return True,f"{len(CALLS)} deterministic calls"
    except (OSError,ValueError,subprocess.TimeoutExpired):return False,"candidate execution"
if __name__=="__main__":
    ok,detail=run(sys.argv[1]) if len(sys.argv)==2 else (False,"candidate path required")
    print(("PASS: " if ok else "FAIL: ")+detail);sys.exit(0 if ok else 1)
