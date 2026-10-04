import base64,copy,json,pathlib,pickle,subprocess,sys
def B(f,k,v):return {"op":"begin","fill":f,"key":k,"value":v}
def I(k):return {"op":"invalidate","key":k}
def E(k):return {"op":"evict","key":k}
def F(f):return {"op":"finish","fill":f}
def R(k):return {"op":"read","key":k}

# Independent historical reconstruction, not the reference's mutable cache loop.
def oracle(events):
    snapshots=[]
    def epoch(key,end):return sum(e["op"]=="invalidate" and e["key"]==key for e in events[:end])
    begins={e["fill"]:(i,e) for i,e in enumerate(events) if e["op"]=="begin"}
    def accepted(i):
        row=events[i];j,begin=begins[row["fill"]]
        return epoch(begin["key"],j)==epoch(begin["key"],i)
    for end in range(1,len(events)+1):
        prefix=events[:end];keys={e["key"] for e in prefix if "key" in e}
        generations={key:epoch(key,end) for key in keys}
        finished={e["fill"] for e in prefix if e["op"]=="finish"}
        pending={e["fill"]:{"key":e["key"],"generation":epoch(e["key"],i),"value":e["value"]}
                 for i,e in enumerate(prefix) if e["op"]=="begin" and e["fill"] not in finished}
        entries={}
        for key in keys:
            changes=[]
            for i,e in enumerate(prefix):
                if e["op"] in ("invalidate","evict") and e["key"]==key:changes.append((i,None))
                elif e["op"]=="finish" and begins[e["fill"]][1]["key"]==key and accepted(i):
                    changes.append((i,begins[e["fill"]][1]["value"]))
            if changes and changes[-1][1] is not None:entries[key]=changes[-1][1]
        e=prefix[-1];result=accepted(end-1) if e["op"]=="finish" else entries.get(e["key"]) if e["op"]=="read" else None
        snapshots.append({"result":result,"generations":generations,"entries":entries,"pending":pending})
    return snapshots

VALID=[[],[R("missing")],[E("absent")],[I("absent")],
       [B("f","k",0),F("f"),R("k")],
       [B("old","k",1),I("k"),E("k"),F("old"),R("k")],
       [B("old","k",1),I("k"),B("new","k",2),F("new"),F("old"),R("k")],
       [B("a","x",-1000),B("b","y",1000),I("x"),F("b"),F("a"),R("x"),R("y")],
       [I("k"),B("a","k",4),E("k"),F("a"),R("k")],
       [B("a","k",1),B("b","k",2),F("b"),F("a"),R("k")],
       [B("f"*32,"k"*32,1),F("f"*32),R("k"*32)],
       [I("k") for _ in range(128)]]
for invalidations in range(4):
    for evictions in range(4):
        VALID.append([B("old","k",7)]+[I("k")]*invalidations+[E("k")]*evictions+
                     [B("new","k",9),F("new"),F("old"),R("k")])
assert oracle(VALID[5])[-1]=={"result":None,"generations":{"k":1},"entries":{},"pending":{}}
assert oracle(VALID[6])[-1]=={"result":2,"generations":{"k":1},"entries":{"k":2},"pending":{}}
INVALID=[None,(),{},[{}],[{"op":True}],[{"op":"bad"}],
         [{"op":"read","key":""}],[{"op":"read","key":"k"*33}],
         [{"op":"read","key":"é"}],[{"op":"read","key":1}],
         [{"op":"read","key":"k","extra":0}],[F("unknown")],
         [B("f","k",True)],[B("f","k",1.0)],[B("f","k",1001)],
         [B("f","k",-1001)],[B("","k",1)],[B("f","k",1),B("f","k",2)],
         [B("f","k",1),F("f"),B("f","k",2)],
         [B("f","k",1),F("f"),F("f")],[R("k")]*129,[I("k"),F("x")]]
CALLS=[([v],oracle(v),False) for v in VALID]+[([v],None,True) for v in INVALID]
CALLS += [([VALID[i]],oracle(VALID[i]),False) for i in (5,0,6,4,0)]

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

RUNNER="import base64,copy,importlib.util,json,pickle,sys\nspec=importlib.util.spec_from_file_location(\"candidate\",sys.argv[1]);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)\ndef fp(v):\n    if type(v) is dict:\n        return (\"dict\",tuple(sorted(((fp(k),fp(x)) for k,x in v.items()),key=repr)))\n    if type(v) in (list,tuple):\n        return (type(v).__name__,tuple(fp(x) for x in v))\n    if type(v) in (set,frozenset):\n        return (type(v).__name__,tuple(sorted((fp(x) for x in v),key=repr)))\n    if type(v) is float:return (\"float\",v.hex())\n    if type(v) is bytes:return (\"bytes\",v.hex())\n    if type(v) in (str,int,bool,type(None)):return (type(v).__name__,v)\n    raise TypeError(\"unsupported native value\")\ndef mutable_ids(v):\n    if type(v) in (dict,list,set):\n        yield id(v)\n    if type(v) is dict:\n        for k,x in v.items():\n            yield from mutable_ids(k);yield from mutable_ids(x)\n    elif type(v) in (list,tuple,set,frozenset):\n        for x in v:yield from mutable_ids(x)\n\nvalues=[];retained=[];saved=[];output_ids=set();unchanged=True;independent=True\nfor args in pickle.loads(base64.b64decode(sys.argv[2])):\n    supplied=copy.deepcopy(args);retained.append((supplied,fp(supplied)))\n    try:value=m.cache_events(*supplied)\n    except Exception as exc:\n        values.append({\"ok\":False,\"error\":type(exc).__name__})\n    else:\n        before=fp(value);occ=list(mutable_ids(value))\n        input_ids=set()\n        for old,_ in retained:input_ids.update(mutable_ids(old))\n        independent=independent and len(occ)==len(set(occ)) and not bool(set(occ)&(output_ids|input_ids))\n        output_ids.update(occ);saved.append((value,before))\n        values.append({\"ok\":True,\"fingerprint\":before})\n    unchanged=unchanged and all(fp(old)==before for old,before in retained)\n    unchanged=unchanged and all(fp(old)==before for old,before in saved)\ninput_ids=set()\nfor old,_ in retained:input_ids.update(mutable_ids(old))\nindependent=independent and not bool(output_ids&input_ids)\nprint(\"__RESULT__\"+json.dumps({\"values\":values,\"unchanged\":unchanged,\"independent\":independent}))\n"

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
