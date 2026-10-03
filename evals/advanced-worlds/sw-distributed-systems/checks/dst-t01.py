"""Literal Raft witnesses plus an independent replication order-statistic oracle."""
import base64,json,pathlib,subprocess,sys
def result(new,committed=(),eligible=()):
    return {"new_commit":new,"newly_committed":list(committed),"eligible_current_term":list(eligible)}
CASES=[
 ("empty single member",[1,[],[0],0],result(0),False),
 ("old term majority does not commit",[3,[1,2],[2,2,0],0],result(0),False),
 ("old known commit never regresses",[3,[1,2],[2,0,0],1],result(1),False),
 ("current anchor commits old prefix",[3,[1,2,3],[3,3,0],0],result(3,[1,2,3],[3]),False),
 ("current entries require distinct-member majority",[3,[1,3,3],[3,1,1,0,0],0],result(0),False),
 ("one current entry gets majority",[3,[1,3,3],[3,2,2,0,0],0],result(2,[1,2],[2]),False),
 ("two current entries supported",[3,[1,3,3],[3,3,3,0,0],1],result(3,[2,3],[2,3]),False),
 ("even membership needs strict majority",[2,[2,2],[2,2,0,0],0],result(0),False),
 ("even membership reaches three",[2,[2,2],[2,2,2,0],0],result(2,[1,2],[1,2]),False),
 ("one member still needs current term",[4,[1,2,3],[3],0],result(0),False),
 ("one member current anchor",[4,[1,2,4],[3],0],result(3,[1,2,3],[3]),False),
 ("all already committed",[2,[1,2],[2,2,2],2],result(2),False),
]
# Sorted matching positions independently determine the largest replicated
# prefix. Nondecreasing entry terms make its current-term suffix contiguous.
def oracle(term,terms,matches,old):
    supported=sorted(matches,reverse=True)[len(matches)//2]
    new=supported if supported>old and terms[supported-1]==term else old
    eligible=[i for i in range(old+1,supported+1) if terms[i-1]==term]
    return result(new,range(old+1,new+1),eligible)
for n in [1,2,3,4,5,7,31]:
 for term,terms in [(1,[]),(3,[1,2]),(3,[1,2,3]),(4,[1,2,4,4]),(4,[4]*64)]:
    length=len(terms);q=n//2+1
    patterns=[[length]*n,[length]+[0]*(n-1),
              [length]*q+[0]*(n-q),
              [length]*max(1,q-1)+[0]*(n-max(1,q-1))]
    for j,matches in enumerate(patterns):
        old=length//2 if j%2 else 0
        args=[term,list(terms),list(matches),old]
        CASES.append((f"order-stat N{n} L{length} pattern{j}",args,oracle(*args),False))
BAD=[
 [True,[],[0],0],[0,[],[0],0],[1,[],[],0],
 [1,[1],[0],0],[1,[2],[1],0],[3,[2,1],[2],0],
 [1,[1],[1,2],0],[1,[1],[1],2],[1,[1],[1],True],
 [1,[True],[1],0],[1,[],[0]*32,0],[1,[1]*65,[65],0],
 [1,"bad",[0],0],[1,[],[False],0],[1,[],[0],-1],
]
for j,args in enumerate(BAD):CASES.append((f"invalid domain {j}",args,None,True))
CALLS=CASES+[CASES[1],CASES[3],CASES[0],CASES[3],CASES[1]]
def run(candidate):
    payload=base64.b64encode(json.dumps([[args,error] for _,args,_,error in CALLS]).encode()).decode()
    runner=r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
def fingerprint(v):
    if type(v) is dict and all(type(k) is str for k in v):
        return ("dict",tuple((k,fingerprint(v[k])) for k in sorted(v)))
    if type(v) is list:return ("list",tuple(fingerprint(x) for x in v))
    if type(v) in (str,int,bool,type(None)):return (type(v).__name__,v)
    raise TypeError("unsupported native type")
def containers(v):
    if type(v) is dict:
        yield id(v)
        for x in v.values():yield from containers(x)
    elif type(v) is list:
        yield id(v)
        for x in v:yield from containers(x)
def schema(v):
    assert type(v) is dict and set(v)=={"new_commit","newly_committed","eligible_current_term"}
    assert type(v["new_commit"]) is int
    for k in ["newly_committed","eligible_current_term"]:
        assert type(v[k]) is list and all(type(x) is int for x in v[k])
values=[];retained=[];output_ids=set();saved=[];independent=True;unchanged=True
for args,expects_error in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args);retained.append((supplied,fingerprint(supplied)))
    try:
        value=module.advance_commit(*supplied)
    except ValueError:
        values.append({"raised":True,"value":None})
    else:
        schema(value);before=fingerprint(value);ids=list(containers(value))
        independent=independent and len(ids)==len(set(ids)) and not bool(set(ids)&output_ids)
        output_ids.update(ids);saved.append((value,before));values.append({"raised":False,"value":value})
    unchanged=unchanged and all(fingerprint(old)==snap for old,snap in retained)
    unchanged=unchanged and all(fingerprint(old)==snap for old,snap in saved)
input_ids=set()
for args,_ in retained:input_ids.update(containers(args))
independent=independent and not bool(output_ids & input_ids)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged,"independent":independent}))'''
    try:
        p=subprocess.run([sys.executable,"-B","-c",runner,str(pathlib.Path(candidate).resolve()),payload],
                         capture_output=True,text=True,timeout=5)
        lines=[x[len("__RESULT__"):] for x in p.stdout.splitlines() if x.startswith("__RESULT__")]
        if p.returncode or not lines:return False,"candidate execution or native schema"
        observed=json.loads(lines[-1])
        if observed.get("unchanged") is not True:return False,"input/prior-output mutation"
        if observed.get("independent") is not True:return False,"mutable aliasing"
        outputs=observed.get("values")
        if type(outputs) is not list or len(outputs)!=len(CALLS):return False,"output count"
        for (label,args,expected,error),actual in zip(CALLS,outputs):
            if actual["raised"] is not error:return False,label+" exception policy"
            if not error and actual["value"]!=expected:return False,label
        return True,f"{len(CALLS)} deterministic calls"
    except (OSError,ValueError,subprocess.TimeoutExpired):return False,"candidate execution"
if __name__=="__main__":
    ok,detail=run(sys.argv[1]) if len(sys.argv)==2 else (False,"candidate path required")
    print(("PASS: " if ok else "FAIL: ")+detail);sys.exit(0 if ok else 1)
