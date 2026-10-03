import base64
import json
import pathlib
import subprocess
import sys


def route(prefix, next_hop, metric):
    return {"prefix": prefix, "next_hop": next_hop, "metric": metric,
            "metadata": {"local_pref": 1000-metric, "as_path": [7]*(metric % 4+1)}}

ROUTES = [
    route("0.0.0.0/0", "v4-default", 1),
    route("10.0.0.0/8", "v4-aggregate", 2),
    route("10.2.0.0/16", "v4-subnet", 30),
    route("10.2.3.0/24", "v4-specific", 90),
    route("10.2.3.4/32", "v4-host", 900),
    route("::/0", "v6-default", 1),
    route("2001:db8::/32", "v6-aggregate", 2),
    route("2001:db8:2::/48", "v6-site", 30),
    route("2001:db8:2:abcd::/64", "v6-subnet", 90),
    route("2001:db8:2:abcd::9/128", "v6-host", 900),
]

def expected(index):
    r = ROUTES[index]
    return {"next_hop": r["next_hop"], "prefix": r["prefix"],
            "prefix_length": int(r["prefix"].split("/")[1])}

NO_MATCH = {"next_hop": None, "prefix": None, "prefix_length": None}
# Hand-selected routes; neither candidate nor reference lookup computes the oracle.
LOOKUPS = [
    ("10.2.3.4", 4), ("10.2.3.255", 3), ("10.2.9.1", 2),
    ("10.9.1.1", 1), ("192.0.2.55", 0),
    ("2001:db8:2:abcd::9", 9), ("2001:db8:2:abcd::a", 8),
    ("2001:db8:2:1000::1", 7), ("2001:db8:3::9", 6),
    ("2001:4860::1", 5), ("::ffff:10.2.3.4", 5),
]
ORDERS = [ROUTES, list(reversed(ROUTES)), ROUTES[3:]+ROUTES[:3],
          sorted(ROUTES, key=lambda r: (r["metric"],r["prefix"]), reverse=True)]
CASES = [(routes, destination, expected(index))
         for routes in ORDERS for destination,index in LOOKUPS]
CASES += [
    ([], "10.2.3.4", NO_MATCH),
    (ROUTES[:5], "2001:db8:2:abcd::9", NO_MATCH),
    (ROUTES[5:], "10.2.3.4", NO_MATCH),
    ([ROUTES[1]], "192.0.2.55", NO_MATCH),
    ([r for r in ROUTES if r["prefix"]!="10.2.3.4/32"], "10.2.3.4", expected(3)),
    ([r for r in ROUTES if r["prefix"] not in {"10.2.3.4/32","10.2.3.0/24"}], "10.2.3.4", expected(2)),
    ([r for r in ROUTES if r["prefix"]!="2001:db8:2:abcd::9/128"], "2001:db8:2:abcd::9", expected(8)),
]

def run(candidate_path):
    payload = base64.b64encode(json.dumps(CASES).encode()).decode()
    code = ('import base64,importlib.util,json,sys;'
            'spec=importlib.util.spec_from_file_location("candidate",sys.argv[1]);'
            'm=importlib.util.module_from_spec(spec);sys.modules["candidate"]=m;'
            'spec.loader.exec_module(m);cs=json.loads(base64.b64decode(sys.argv[2]));'
            'print("__R__"+json.dumps([m.fib_lookup(a,b) for a,b,_ in cs],separators=(",",":")))')
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
