import base64
import json
import pathlib
import subprocess
import sys


def path(identifier, *, lp=100, asp=(7,1), origin="IGP", med=0,
         ebgp=True, cost=10, resolvable=True):
    return {"id":identifier, "local_pref":lp, "as_path":list(asp),
            "origin":origin, "med":med, "ebgp":ebgp, "igp_cost":cost,
            "next_hop_resolvable":resolvable, "neighbor_as":asp[0]}

def answer(selected, eligible=("a","b")):
    return {"selected":selected, "eligible":list(eligible)}

# Winning IDs are hand-derived. Later criteria oppose earlier ones to expose
# incorrect precedence, and reversing the inputs must preserve each answer.
BASE_CASES = [
    # LOCAL_PREF before AS count and all later stages.
    ([path("a",lp=200,asp=(7,8,9),origin="INCOMPLETE",med=90,ebgp=False,cost=90),
      path("b",lp=100,asp=(8,),origin="IGP",med=0,ebgp=True,cost=1)],65000,answer("a")),
    # AS count before ORIGIN and external status.
    ([path("a",asp=(7,),origin="INCOMPLETE",ebgp=False,cost=90),
      path("b",asp=(8,9),origin="IGP",ebgp=True,cost=1)],65000,answer("a")),
    # ORIGIN ranks, deliberately opposing eBGP preference.
    ([path("a",asp=(7,9),origin="IGP",ebgp=False,cost=90),
      path("b",asp=(8,9),origin="EGP",ebgp=True,cost=1)],65000,answer("a")),
    ([path("a",asp=(7,9),origin="EGP",ebgp=False,cost=90),
      path("b",asp=(8,9),origin="INCOMPLETE",ebgp=True,cost=1)],65000,answer("a")),
    # Same-AS MED, including a route received via iBGP, before eBGP status.
    ([path("a",asp=(7,1),med=5,ebgp=False,cost=90),
      path("b",asp=(7,2),med=50,ebgp=True,cost=1)],65000,answer("a")),
    ([path("a",asp=(7,1),med=50,cost=1),
      path("b",asp=(7,2),med=5,cost=90)],65000,answer("b")),
    # Different ASes: MED cannot defeat external status or interior cost.
    ([path("a",asp=(7,1),med=99,ebgp=True,cost=90),
      path("b",asp=(8,1),med=0,ebgp=False,cost=1)],65000,answer("a")),
    ([path("a",asp=(7,1),med=0,cost=90),
      path("b",asp=(8,1),med=50,cost=1)],65000,answer("b")),
    # Missing MED equals zero.
    ([path("a",asp=(7,1),med=None,ebgp=False,cost=90),
      path("b",asp=(7,2),med=5,ebgp=True,cost=1)],65000,answer("a")),
    ([path("a",asp=(7,1),med=None,ebgp=False),
      path("b",asp=(7,2),med=0,ebgp=True)],65000,answer("b")),
    # External status, then interior cost, then synthetic lexicographic tie.
    ([path("a",ebgp=True,cost=90),path("b",ebgp=False,cost=1)],65000,answer("a")),
    ([path("a",cost=90),path("b",cost=1)],65000,answer("b")),
    ([path("b"),path("a")],65000,answer("a")),
    # Admission precedes ranking; loop detection uses actual AS_SEQUENCE.
    ([path("a",lp=900,asp=(7,65000,9)),path("b")],65000,answer("b",("b",))),
    ([path("a",lp=900,resolvable=False),path("b")],65000,answer("b",("b",))),
    ([path("a",asp=(7,65000)),path("b",resolvable=False)],65000,answer(None,())),
    # local_as must not be hard-coded.
    ([path("a",lp=900,asp=(7,65000,9)),path("b")],65010,answer("a")),
    ([path("a",lp=900,asp=(7,65010,9)),path("b")],65010,answer("b",("b",))),
]
CASES = [(paths,local_as,expected) for paths,local_as,expected in BASE_CASES]
CASES += [(list(reversed(paths)),local_as,expected)
          for paths,local_as,expected in BASE_CASES]

def run(candidate_path):
    payload = base64.b64encode(json.dumps(CASES).encode()).decode()
    code = ('import base64,importlib.util,json,sys;'
            'spec=importlib.util.spec_from_file_location("candidate",sys.argv[1]);'
            'm=importlib.util.module_from_spec(spec);sys.modules["candidate"]=m;'
            'spec.loader.exec_module(m);cs=json.loads(base64.b64decode(sys.argv[2]));'
            'print("__R__"+json.dumps([m.select_bgp_path(a,b) for a,b,_ in cs],separators=(",",":")))')
    try:
        result = subprocess.run([sys.executable, "-B", "-c", code,
                                 str(pathlib.Path(candidate_path).resolve()), payload],
                                capture_output=True, text=True, timeout=5)
        lines = [line[5:] for line in result.stdout.splitlines() if line.startswith("__R__")]
        return json.loads(lines[-1]) if result.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError, json.JSONDecodeError):
        return None

if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) == [c[2] for c in CASES] else 1)
