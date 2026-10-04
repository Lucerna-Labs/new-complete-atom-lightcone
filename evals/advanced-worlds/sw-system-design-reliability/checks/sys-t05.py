"""Exact integer oracle and literal SLO witnesses, independent of Fraction."""
import base64
import inspect
import json
from math import gcd
import pathlib
import subprocess
import sys

FUNCTION_NAME = "slo_report"
VALUE_ERROR = "ValueError"
CASES = []


def reduced(numerator, denominator):
    common = gcd(abs(numerator), denominator)
    return [numerator // common, denominator // common]


def integer_oracle(shards, target_num, target_den, exception):
    # Separate integer counts and cross products; no Fraction or floating arithmetic.
    good = 0
    bad_count = 0
    for shard in shards:
        good += shard["good"]
        bad_count += shard["eligible"] - shard["good"]
    total = good + bad_count
    surplus = good * target_den - total * target_num
    return {
        "eligible": total, "good": good, "bad": bad_count,
        "sli": reduced(good, total) if total else None,
        "allowance": reduced((target_den-target_num)*total, target_den),
        "remaining": reduced(surplus, target_den),
        "burn": reduced(bad_count*target_den, total*(target_den-target_num))
                if total and target_num < target_den else None,
        "met": good*target_den >= total*target_num if total else None,
        "release": surplus > 0 or exception}


def shard(good, eligible):
    return {"good": good, "eligible": eligible}


def report(n, g, b, sli, allowance, remaining, burn, met, release):
    return {"eligible":n,"good":g,"bad":b,"sli":sli,"allowance":allowance,
            "remaining":remaining,"burn":burn,"met":met,"release":release}


def good_case(name, args, literal=None):
    expected = integer_oracle(*args)
    if literal is not None:
        assert expected == literal, name
        expected = literal
    CASES.append((name, args, expected, []))


def bad_case(name, args, wraps=None):
    CASES.append((name, args, VALUE_ERROR, wraps or []))


good_case("empty ordinary gate", [[],1,2,False],
          report(0,0,0,None,[0,1],[0,1],None,None,False))
good_case("empty authorized exception", [[],1,2,True],
          report(0,0,0,None,[0,1],[0,1],None,None,True))
bad_case("boolean numerator between valid calls", [[],True,2,False])
good_case("unequal shards use pooled counts", [[shard(1,1),shard(0,99)],99,100,False],
          report(100,1,99,[1,100],[1,1],[-98,1],[99,1],False,False))
good_case("fractional negative remainder", [[shard(2,3)],9,10,False],
          report(3,2,1,[2,3],[3,10],[-7,10],[10,3],False,False))
good_case("fractional positive allowance is not floored", [[shard(3,3)],9,10,False],
          report(3,3,0,[1,1],[3,10],[3,10],[0,1],True,True))
good_case("target equality meets SLO but refuses ordinary release", [[shard(999,1000)],999,1000,False],
          report(1000,999,1,[999,1000],[1,1],[0,1],[1,1],True,False))
bad_case("malformed later shard", [[shard(1,1),{"good":0}],1,2,False])
good_case("exception admits without changing overspend", [[shard(2,3)],9,10,True],
          report(3,2,1,[2,3],[3,10],[-7,10],[10,3],False,True))
good_case("exception at exact zero remainder", [[shard(1,2)],1,2,True],
          report(2,1,1,[1,2],[1,1],[0,1],[1,1],True,True))
good_case("target zero all bad still meets but has no slack", [[shard(0,4)],0,1,False],
          report(4,0,4,[0,1],[4,1],[0,1],[1,1],True,False))
good_case("target zero one good leaves slack", [[shard(1,4)],0,1,False],
          report(4,1,3,[1,4],[4,1],[1,1],[3,4],True,True))
good_case("target one perfect has undefined burn and zero allowance", [[shard(4,4)],1,1,False],
          report(4,4,0,[1,1],[0,1],[0,1],None,True,False))
good_case("target one with failure keeps negative remainder", [[shard(3,4)],1,1,False],
          report(4,3,1,[3,4],[0,1],[-1,1],None,False,False))
good_case("no data with target zero", [[shard(0,0)],0,1,False],
          report(0,0,0,None,[0,1],[0,1],None,None,False))
good_case("no data with target one exception", [[shard(0,0),shard(0,0)],1000,1000,True],
          report(0,0,0,None,[0,1],[0,1],None,None,True))
good_case("unreduced target must produce reduced lists", [[shard(2,6)],2,6,False],
          report(6,2,4,[1,3],[4,1],[0,1],[1,1],True,False))
good_case("nonterminating fractions and negative remainder", [[shard(1,7)],2,3,False],
          report(7,1,6,[1,7],[7,3],[-11,3],[18,7],False,False))
good_case("zero shards do not skew pooled denominator", [[shard(0,0),shard(5,8),shard(0,0)],1,2,False],
          report(8,5,3,[5,8],[4,1],[1,1],[3,4],True,True))
good_case("same scalar pair values still require independent lists", [[shard(0,1)],0,1,False],
          report(1,0,1,[0,1],[1,1],[0,1],[1,1],True,False))
good_case("permutation preserves counts", [[shard(0,99),shard(1,1)],99,100,False])
good_case("subdivision preserves complete population", [[shard(1,1),shard(0,20),shard(0,79)],99,100,False])
# Different exact targets, weighted sizes, zero cohorts and success distributions.
for index, (num, den) in enumerate([(0,1000),(1,1000),(499,1000),(999,1000),
                                  (3,7),(6,7),(7,7),(11,13),(997,997),(2,9)]):
    cohorts = [shard(0,0),shard(index,index+1),shard(7,23),shard(1000000,1000000)]
    good_case("integer cross-product target "+str(index),[cohorts,num,den,index%2==0])

valid = [[shard(1,2)],1,2,False]
for index, label in [(1,"numerator"),(2,"denominator")]:
    for value, name in [(True,"bool"),(1.0,"float"),("1","str"),(None,"None")]:
        args = [[shard(1,2)],1,2,False]
        args[index] = value
        bad_case(label+" "+name,args)
    bad_case(label+" int subclass",[[shard(1,2)],1,2,False],[([index],"int")])
for index, value, name in [(1,-1,"negative numerator"),(1,3,"numerator above denominator"),
                           (2,0,"zero denominator"),(2,-1,"negative denominator"),
                           (2,1001,"denominator above bound")]:
    args = [[shard(1,2)],1,2,False]
    args[index] = value
    bad_case(name,args)
for value, name in [(0,"int zero"),(1,"int one"),(0.0,"float"),("false","str"),(None,"None")]:
    bad_case("exception "+name,[[shard(1,2)],1,2,value])
for value, name in [((),"tuple"),({},"dict"),(None,"None"),("","str")]:
    bad_case("shards "+name,[value,1,2,False])
bad_case("shards list subclass",[[shard(1,2)],1,2,False],[([0],"list")])
bad_case("too many shards",[[shard(0,0) for _ in range(65)],1,2,False])
for value, name in [(None,"None"),([],"list"),((1,2),"tuple"),("","str")]:
    bad_case("shard "+name,[[value],1,2,False])
bad_case("shard dict subclass",[[shard(1,2)],1,2,False],[([0,0],"dict")])
bad_case("native schema key types",[[shard(1,2)],1,2,False],[([0,0],"strkeys")])
for value, name in [({},"empty"),({"good":0},"missing eligible"),
                    ({"eligible":0},"missing good"),
                    ({"good":0,"eligible":0,"extra":0},"extra field"),
                    ({"good":0,"eligible":0,1:0},"nonstring field")]:
    bad_case("schema "+name,[[value],1,2,False])
for field in ["good","eligible"]:
    for value, name in [(True,"bool"),(0.0,"float"),("0","str"),(None,"None"),(-1,"negative")]:
        row = shard(0,0)
        row[field] = value
        bad_case(field+" "+name,[[row],1,2,False])
    bad_case(field+" int subclass",[[shard(0,0)],1,2,False],[([0,0,field],"int")])
bad_case("good exceeds eligible",[[shard(2,1)],1,2,False])
bad_case("eligible above bound",[[shard(0,1000001)],1,2,False])
bad_case("both counts above bound",[[shard(1000001,1000001)],1,2,False])
bad_case("invalid tail after valid data",[[shard(1000000,1000000),shard(False,1)],1,2,False])

good_case("64 maximum-size all-good cohorts",[[shard(1000000,1000000) for _ in range(64)],999,1000,False],
          report(64000000,64000000,0,[1,1],[64000,1],[64000,1],[0,1],True,True))
good_case("64 maximum-size all-bad cohorts",[[shard(0,1000000) for _ in range(64)],1000,1000,True],
          report(64000000,0,64000000,[0,1],[0,1],[-64000000,1],None,False,True))
good_case("maximum denominator exact equality",[[shard(999000,1000000) for _ in range(64)],999,1000,False],
          report(64000000,63936000,64000,[999,1000],[64000,1],[0,1],[1,1],True,False))
good_case("64 zero-sized cohorts",[[shard(0,0) for _ in range(64)],1,1000,False])
good_case("empty after maximum cohorts",[[],1,2,False])
bad_case("error after maximum cohorts",[[shard(True,1)],1,2,False])
good_case("repeat unequal shards after error",[[shard(1,1),shard(0,99)],99,100,False])
good_case("minimum one-good operation",[[shard(1,1)],0,1,False],
          report(1,1,0,[1,1],[1,1],[1,1],[0,1],True,True))
good_case("final empty",[[],1,2,False])

def fingerprint(value, active=None):
    if active is None:
        active = set()
    kind = type(value)
    tag = kind.__name__ if kind in (dict, list, tuple, set, frozenset, bool, int, str, float, bytes) else kind.__module__ + "." + kind.__qualname__
    if isinstance(value, (dict, list, tuple, set, frozenset)):
        if id(value) in active:
            return ["cycle"]
        active.add(id(value))
        if isinstance(value, dict):
            body = sorted([[fingerprint(k, active), fingerprint(v, active)]
                           for k, v in value.items()], key=repr)
        else:
            body = [fingerprint(v, active) for v in value]
            if isinstance(value, (set, frozenset)):
                body.sort(key=repr)
        active.remove(id(value))
        return [tag, body]
    if value is None:
        return ["none"]
    if kind in (bool, int, str):
        return [tag, value]
    if isinstance(value, int):
        return [tag, int(value)]
    if isinstance(value, str):
        return [tag, str(value)]
    return [tag, repr(value)]


def run(candidate):
    payload = base64.b64encode(repr([(args, wraps) for _, args, _, wraps in CASES]).encode()).decode()
    runner = r'''import ast,base64,copy,importlib.util,json,sys

class IntChild(int): pass
class ListChild(list): pass
class DictChild(dict): pass
class StrChild(str): pass

''' + FINGERPRINT_SOURCE + r'''
def mutable_objects(value, found):
    if isinstance(value, (dict, list, set, bytearray)):
        if id(value) in found:
            return
        found[id(value)] = value
    if isinstance(value, dict):
        for key, child in value.items():
            mutable_objects(key, found)
            mutable_objects(child, found)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for child in value:
            mutable_objects(child, found)

def independent(values, forbidden):
    seen = set(forbidden)
    def visit(value):
        if isinstance(value, (dict, list, set, bytearray)):
            if id(value) in seen:
                return False
            seen.add(id(value))
        if isinstance(value, dict):
            return all(visit(k) and visit(v) for k, v in value.items())
        if isinstance(value, (list, tuple, set, frozenset)):
            return all(visit(v) for v in value)
        return True
    return all(visit(value) for value in values)

spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
inputs=[];outputs=[];output_history=[];input_objects={};calls=[]
unchanged=True;stable=True;isolated=True
for args, wraps in ast.literal_eval(base64.b64decode(sys.argv[2]).decode()):
    supplied=copy.deepcopy(args)
    for path, kind in wraps:
        parent=supplied
        for step in path[:-1]:
            parent=parent[step]
        value=parent[path[-1]]
        if kind == "strkeys":
            parent[path[-1]]={StrChild(k): v for k,v in value.items()}
        else:
            parent[path[-1]]={"int":IntChild,"list":ListChild,"dict":DictChild,"str":StrChild}[kind](value)
    inputs.append((supplied,fingerprint(supplied)))
    mutable_objects(supplied,input_objects)
    try:
        value=getattr(m,FUNCTION_NAME)(*supplied)
    except ValueError:
        calls.append({"error":"ValueError"})
    except Exception as exc:
        calls.append({"error":type(exc).__name__})
    else:
        snap=fingerprint(value)
        outputs.append(value);output_history.append(snap)
        calls.append({"value":snap})
    for prior,before in inputs:
        if fingerprint(prior)!=before:
            unchanged=False
        mutable_objects(prior,input_objects)
    for prior,before in zip(outputs,output_history):
        if fingerprint(prior)!=before:
            stable=False
    if not independent(outputs,input_objects):
        isolated=False
print("__RESULT__"+json.dumps({"calls":calls,"inputs_unchanged":unchanged,
                             "outputs_unchanged":stable,"independent":isolated}))
'''
    runner = runner.replace("FUNCTION_NAME", repr(FUNCTION_NAME))
    try:
        process = subprocess.run(
            [sys.executable, "-B", "-c", runner, str(pathlib.Path(candidate).resolve()), payload],
            capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if process.returncode == 0 and lines else None
        expected = {
            "calls": [{"error": "ValueError"} if value == VALUE_ERROR
                      else {"value": fingerprint(value)} for _, _, value, _ in CASES],
            "inputs_unchanged": True, "outputs_unchanged": True, "independent": True}
        return actual == expected
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False


# Copy the checker-owned native fingerprint implementation into the child runner.
FINGERPRINT_SOURCE = inspect.getsource(fingerprint)

if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
