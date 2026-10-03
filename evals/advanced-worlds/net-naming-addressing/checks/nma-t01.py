import base64
import copy
import json
import pathlib
import subprocess
import sys


def entry(kind="NODATA", name="host.example.", original=None, qtype="AAAA", qclass="IN", view="internal", at=100, soa_ttl=600, soa_minimum=120):
    return {"kind":kind,"negative_name":name,"queried_name":original or name,
            "qtype":qtype,"qclass":qclass,"view":view,"stored_at":at,
            "soa_ttl":soa_ttl,"soa_minimum":soa_minimum}

def query(name="host.example.", qtype="AAAA", qclass="IN", view="internal"):
    return {"name":name,"qtype":qtype,"qclass":qclass,"view":view}

def hit(kind, ttl):
    return {"kind":kind,"ttl":ttl}

MISS = {"kind":None,"ttl":0}
CASES = [
    (entry(), query(), 100, hit("NODATA",120)),
    (entry(), query(), 130, hit("NODATA",90)),
    (entry(), query(), 219, hit("NODATA",1)),
    (entry(), query(), 220, MISS),
    (entry(), query(), 900, MISS),
    (entry(soa_ttl=20,soa_minimum=120), query(), 105, hit("NODATA",15)),
    (entry(soa_ttl=120,soa_minimum=20), query(), 105, hit("NODATA",15)),
    (entry(soa_ttl=30,soa_minimum=30), query(), 100, hit("NODATA",30)),
    (entry(soa_ttl=0), query(), 100, MISS),
    (entry(soa_minimum=0), query(), 100, MISS),
    (entry(), query(qtype="A"), 110, MISS),
    (entry(), query(qtype="TXT"), 110, MISS),
    (entry(), query(qtype="aaaa"), 110, hit("NODATA",110)),
    (entry("NXDOMAIN"), query(qtype="A"), 110, hit("NXDOMAIN",110)),
    (entry("NXDOMAIN"), query(qtype="TXT"), 110, hit("NXDOMAIN",110)),
    (entry("NXDOMAIN"), query(qclass="CH"), 110, MISS),
    (entry(), query(name="HOST.EXAMPLE.",qclass="in"), 110, hit("NODATA",110)),
    (entry(), query(name="other.example."), 110, MISS),
    (entry("NXDOMAIN"), query(name="child.host.example."), 110, MISS),
    (entry(), query(view="external"), 110, MISS),
    (entry("NXDOMAIN",view="external"), query(), 110, MISS),
    (entry("NXDOMAIN",name="gone.example.",original="alias.example."), query(name="gone.example.",qtype="A"), 110, hit("NXDOMAIN",110)),
    (entry("NXDOMAIN",name="gone.example.",original="alias.example."), query(name="alias.example.",qtype="A"), 110, MISS),
    (entry("NODATA",name="target.example.",original="alias.example."), query(name="target.example."), 110, hit("NODATA",110)),
    (entry("NODATA",name="target.example.",original="alias.example."), query(name="alias.example."), 110, MISS),
    (entry(view="Internal"), query(view="internal"), 110, MISS),
    (entry(name="HOST.EXAMPLE.",qclass="in",qtype="aaaa"), query(name="host.example.",qclass="IN",qtype="AAAA"), 110, hit("NODATA",110)),
    (entry(), query(qclass="CH"), 110, MISS),
    (entry(at=10), query(), 15, hit("NODATA",115)),
    (None, query(), 0, MISS),
    # Later independent calls cannot refresh the installation epoch.
    (entry(), query(), 218, hit("NODATA",2)),
    (entry(), query(), 220, MISS),
]
EXPECTED = {"values":[c[3] for c in CASES],"unchanged":True}

def run(candidate):
    payload=base64.b64encode(json.dumps(CASES).encode()).decode()
    runner=r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
cases=json.loads(base64.b64decode(sys.argv[2]));values=[];unchanged=True
for e,q,t,_ in cases:
    a,b=copy.deepcopy(e),copy.deepcopy(q)
    values.append(module.negative_lookup(a,b,t))
    unchanged=unchanged and a==e and b==q
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged}))'''
    try:
        result=subprocess.run([sys.executable,"-c",runner,str(pathlib.Path(candidate).resolve()),payload],capture_output=True,text=True,timeout=5)
        lines=[line[len("__RESULT__"):] for line in result.stdout.splitlines() if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if result.returncode==0 and lines else None
    except (OSError,subprocess.TimeoutExpired,ValueError):
        return None

if __name__=="__main__":
    sys.exit(0 if len(sys.argv)==2 and run(sys.argv[1])==EXPECTED else 1)
