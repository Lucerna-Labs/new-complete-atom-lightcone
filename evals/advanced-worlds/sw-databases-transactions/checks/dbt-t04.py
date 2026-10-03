import base64
import json
import pathlib
import subprocess
import sys


def candidate(name, index, heap, vm, visible):
    return {"id": name, "index_values": dict(index), "heap_values": dict(heap),
            "vm_all_visible": vm, "heap_visible": visible}


def result(strategy, checks, rows, trace):
    # Formatting only. Visibility outcomes, sources, counts and row order are
    # supplied as literal answers or explicit boundary closed forms below.
    return {"strategy": strategy, "heap_checks": checks,
            "rows": [{"id": name, "values": dict(values)} for name, values in rows],
            "trace": [{"id": name, "heap_checked": checked, "visible": visible,
                       "value_source": source} for name, checked, visible, source in trace]}


CASES=[
("empty default projection",[[],[],[]],result("index-only",0,[],[])),
("empty missing column path",[["a"],[],[]],result("heap",0,[],[])),
("empty unsupported path",[["a"],["a"],[],False],result("heap",0,[],[])),
("covered all-visible candidate",[["a"],["a"],[candidate("R",{"a":7},{"a":7},True,True)]],
 result("index-only",0,[("R",{"a":7})],[("R",False,True,"index")])),
("covered candidate still needs successful heap check",[["a"],["a"],[candidate("R",{"a":7},{"a":7},False,True)]],
 result("index-only",1,[("R",{"a":7})],[("R",True,True,"index")])),
("covering payload does not make invisible tuple visible",[["a"],["a"],[candidate("R",{"a":7},{"a":7},False,False)]],
 result("index-only",1,[],[("R",True,False,None)])),
("missing payload requires heap despite valid bit",[["a","b"],["a"],[candidate("R",{"a":1},{"a":1,"b":2},True,True)]],
 result("heap",1,[("R",{"a":1,"b":2})],[("R",True,True,"heap")])),
("unsupported access method needs heap despite coverage",[["a"],["a"],[candidate("R",{"a":1},{"a":1},True,True)],False],
 result("heap",1,[("R",{"a":1})],[("R",True,True,"heap")])),
("unsupported invisible candidate is filtered",[["a"],["a"],[candidate("R",{"a":1},{"a":1},False,False)],False],
 result("heap",1,[],[("R",True,False,None)])),
("mixed coverage preserves candidate order",[["a"],["a"],[candidate("z",{"a":1},{"a":1},True,True),candidate("B",{"a":2},{"a":2},False,False),candidate("a",{"a":3},{"a":3},False,True)]],
 result("index-only",2,[("z",{"a":1}),("a",{"a":3})],[("z",False,True,"index"),("B",True,False,None),("a",True,True,"index")])),
("unused index payload is not projected",[["a"],["a","b"],[candidate("R",{"a":2,"b":9},{"a":2,"b":9},True,True)]],
 result("index-only",0,[("R",{"a":2})],[("R",False,True,"index")])),
("required column order does not affect coverage",[["b","a"],["a","b"],[candidate("R",{"a":2,"b":9},{"a":2,"b":9},False,True)]],
 result("index-only",1,[("R",{"b":9,"a":2})],[("R",True,True,"index")])),
("empty projection still checks visibility",[[],["x"],[candidate("R",{"x":5},{"x":5},False,True)]],
 result("index-only",1,[("R",{})],[("R",True,True,"index")])),
("empty projection may have invisible candidates",[[],[],[candidate("R",{},{},False,False)]],
 result("index-only",1,[],[("R",True,False,None)])),
("empty unsupported projection still fetches heap",[[],[],[candidate("R",{},{},True,True)],False],
 result("heap",1,[("R",{})],[("R",True,True,"heap")])),
("equal row payloads must use independent containers",[["a"],["a"],[candidate("R1",{"a":3},{"a":3},True,True),candidate("R2",{"a":3},{"a":3},True,True)]],
 result("index-only",0,[("R1",{"a":3}),("R2",{"a":3})],[("R1",False,True,"index"),("R2",False,True,"index")])),
("signed payload boundaries and zero",[["lo","hi","zero"],["hi","zero","lo"],[candidate("R",{"lo":-1000,"hi":1000,"zero":0},{"lo":-1000,"hi":1000,"zero":0},False,True)]],
 result("index-only",1,[("R",{"lo":-1000,"hi":1000,"zero":0})],[("R",True,True,"index")])),
("column coverage is case sensitive",[["A"],["a"],[candidate("R",{"a":4},{"a":4,"A":8},True,True)]],
 result("heap",1,[("R",{"A":8})],[("R",True,True,"heap")])),
("ordinary heap path mixed visibility",[["b"],["a"],[candidate("z",{"a":1},{"a":1,"b":10},True,True),candidate("a",{"a":2},{"a":2,"b":20},False,False),candidate("M",{"a":3},{"a":3,"b":30},False,True)]],
 result("heap",3,[("z",{"b":10}),("M",{"b":30})],[("z",True,True,"heap"),("a",True,False,None),("M",True,True,"heap")])),
("explicit true support",[["a"],["a"],[candidate("R",{"a":6},{"a":6},True,True)],True],
 result("index-only",0,[("R",{"a":6})],[("R",False,True,"index")])),
("missing payload with no index columns",[["a"],[],[candidate("R",{},{"a":5},False,True)]],
 result("heap",1,[("R",{"a":5})],[("R",True,True,"heap")])),
("maximum length IDs",[["abcdefghijklmnop"],["abcdefghijklmnop"],[candidate("ABCDEFGHIJKLMNOP",{"abcdefghijklmnop":1},{"abcdefghijklmnop":1},True,True)]],
 result("index-only",0,[("ABCDEFGHIJKLMNOP",{"abcdefghijklmnop":1})],[("ABCDEFGHIJKLMNOP",False,True,"index")])),
]
# Independent interval partition:16 all-visible,8 checked-visible,8 invisible.
# Thus16 heap checks,24 rows and32 trace entries, with8 projected columns.
COLUMNS=[f'k{i}' for i in range(8)]
BIG=[candidate(f'R{i:02}',{c:8*i+j for j,c in enumerate(COLUMNS)},
               {c:8*i+j for j,c in enumerate(COLUMNS)},i<16,i<24) for i in range(32)]
CASES.append(("maximum candidates and projected columns",[COLUMNS,COLUMNS,BIG],
 result("index-only",16,[(f'R{i:02}',{c:8*i+j for j,c in enumerate(COLUMNS)}) for i in range(24)],
 [(f'R{i:02}',False,True,"index") for i in range(16)]+[(f'R{i:02}',True,True,"index") for i in range(16,24)]+[(f'R{i:02}',True,False,None) for i in range(24,32)])))
CASES.extend([CASES[0],CASES[9],CASES[0]])

def native_types(value):
    if type(value) is dict:
        if any(type(k) is not str for k in value):
            return ["unsupported-dict-key"]
        return ["dict", [[k, native_types(value[k])] for k in sorted(value)]]
    if type(value) is list:
        return ["list", [native_types(v) for v in value]]
    if value is None:
        return "none"
    if type(value) is bool:
        return "bool"
    if type(value) is int:
        return "int"
    if type(value) is str:
        return "str"
    return ["unsupported", type(value).__name__]


def run(candidate):
    payload = base64.b64encode(json.dumps([args for _, args, _ in CASES]).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys

def native_types(value):
    if type(value) is dict:
        if any(type(k) is not str for k in value): return ["unsupported-dict-key"]
        return ["dict",[[k,native_types(value[k])] for k in sorted(value)]]
    if type(value) is list: return ["list",[native_types(v) for v in value]]
    if value is None: return "none"
    if type(value) is bool: return "bool"
    if type(value) is int: return "int"
    if type(value) is str: return "str"
    return ["unsupported",type(value).__name__]

def mutable_ids(value, seen=None):
    if seen is None: seen=set()
    if type(value) not in (dict,list) or id(value) in seen: return seen
    seen.add(id(value))
    for child in (value.values() if type(value) is dict else value): mutable_ids(child,seen)
    return seen

def independent_outputs(values, forbidden):
    seen=set(forbidden)
    def visit(value):
        if type(value) not in (dict,list): return True
        if id(value) in seen: return False
        seen.add(id(value))
        return all(visit(child) for child in (value.values() if type(value) is dict else value))
    return all(visit(value) for value in values)

spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
values=[];output_history=[];inputs=[];input_ids=set();unchanged=True;independent=True;stable=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args)
    inputs.append((supplied,json.dumps(supplied,sort_keys=True),native_types(supplied)))
    input_ids.update(mutable_ids(supplied))
    result=m.index_access(*supplied)
    values.append(result)
    result_types=native_types(result)
    output_history.append((json.dumps(result,sort_keys=True),result_types))
    for prior,(before,types) in zip(values,output_history):
        stable=stable and json.dumps(prior,sort_keys=True)==before and native_types(prior)==types
    for prior,before,types in inputs:
        unchanged=unchanged and json.dumps(prior,sort_keys=True)==before and native_types(prior)==types
    independent=independent and independent_outputs(values,input_ids)
print("__RESULT__"+json.dumps({"values":values,"types":[native_types(v) for v in values],"unchanged":unchanged,"independent":independent,"stable":stable}))'''
    try:
        process = subprocess.run([sys.executable, "-B", "-c", runner,
                                  str(pathlib.Path(candidate).resolve()), payload],
                                 capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if process.returncode == 0 and lines else None
        wanted = [value for _, _, value in CASES]
        expected = {"values": wanted, "types": [native_types(v) for v in wanted],
                    "unchanged": True, "independent": True, "stable": True}
        return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return False


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
