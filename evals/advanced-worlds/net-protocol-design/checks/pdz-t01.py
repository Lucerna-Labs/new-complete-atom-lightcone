import base64
import json
import pathlib
import subprocess
import sys


def answer(records=(), pending=False, error=None):
    return {"records":list(records),"pending":pending,"error":error}

HELLO = "8000000568656c6c6f"
SPLIT = "00000002616280000003636465"
# Literal byte encodings and expected payloads are independent of the parser.
CASES = [
    ([HELLO], {}, answer(["68656c6c6f"])),
    ([HELLO[i:i+2] for i in range(0,len(HELLO),2)], {}, answer(["68656c6c6f"])),
    (["80","00000568","656c","6c6f"], {}, answer(["68656c6c6f"])),
    (["8000000568","","656c6c6f"], {}, answer(["68656c6c6f"])),
    (["80","","00000568656c6c6f"], {}, answer(["68656c6c6f"])),
    ([SPLIT], {}, answer(["6162636465"])),
    (["0000000261","628000","0003","636465"], {}, answer(["6162636465"])),
    (["8000000161800000026263"], {}, answer(["61","6263"])),
    (["80000000"], {}, answer([""])),
    (["0000000080000003616263"], {}, answer(["616263"])),
    (["00000000"], {}, answer(error="truncated")),
    (["00000000"], {"eof":False}, answer(pending=True)),
    (["8000"], {}, answer(error="truncated")),
    (["8000"], {"eof":False}, answer(pending=True)),
    (["800000056865"], {}, answer(error="truncated")),
    (["800000056865"], {"eof":False}, answer(pending=True)),
    (["80000001618000000362"], {"eof":False}, answer(["61"],True)),
    (["80000001618000000362"], {}, answer(["61"],error="truncated")),
    ([SPLIT], {"max_fragment":3,"max_record":5}, answer(["6162636465"])),
    ([HELLO], {"max_fragment":5,"max_record":5}, answer(["68656c6c6f"])),
    (["80000005"], {"max_fragment":4,"eof":False}, answer(error="fragment-limit")),
    (["00000002616280000003"], {"max_fragment":3,"max_record":4,"eof":False}, answer(error="record-limit")),
    (["80000005"], {"max_fragment":5,"max_record":4,"eof":False}, answer(error="record-limit")),
    (["80000005"], {"max_fragment":4,"max_record":4}, answer(error="fragment-limit")),
    (["80000000"], {"max_fragment":0,"max_record":0}, answer([""])),
    (["0000000080000000"], {"max_fragment":0,"max_record":0}, answer([""])),
    ([], {}, answer()), (["", ""], {}, answer()),
    (["8000000161"], {"eof":False}, answer(["61"])),
    ([], {"eof":False}, answer()),
    (["000000026162800000026364800000026566"], {"max_fragment":2,"max_record":4}, answer(["61626364","6566"])),
    (["8000000400ff0a80"], {}, answer(["00ff0a80"])),
    (["80000002C3A9"], {}, answer(["c3a9"])),
    (["ffffffff"], {}, answer(error="fragment-limit")),
    (["8000000161800000066162636465668000000162"], {"max_fragment":5}, answer(["61"],error="fragment-limit")),
    (["00000003616263"], {}, answer(error="truncated")),
    (["00000003616263"], {"eof":False}, answer(pending=True)),
    ([HELLO], {}, answer(["68656c6c6f"])),
]
EXPECTED = {"values":[c[2] for c in CASES],"unchanged":True}

def run(candidate):
    payload=base64.b64encode(json.dumps(CASES).encode()).decode()
    runner=r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1]);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
values=[];unchanged=True
for chunks,kwargs,_ in json.loads(base64.b64decode(sys.argv[2])):
    a,b=copy.deepcopy(chunks),copy.deepcopy(kwargs);values.append(m.decode_rpc_chunks(a,**b));unchanged=unchanged and a==chunks and b==kwargs
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged}))'''
    try:
        p=subprocess.run([sys.executable,"-c",runner,str(pathlib.Path(candidate).resolve()),payload],capture_output=True,text=True,timeout=5)
        lines=[line[len("__RESULT__"):] for line in p.stdout.splitlines() if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if p.returncode==0 and lines else None
    except (OSError,subprocess.TimeoutExpired,ValueError):return None

def passes(value):
    return value==EXPECTED and all(type(x["pending"]) is bool and type(x["records"]) is list
        and all(type(y) is str for y in x["records"]) for x in value["values"])

if __name__=="__main__":
    sys.exit(0 if len(sys.argv)==2 and passes(run(sys.argv[1])) else 1)
