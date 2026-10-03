import base64
import copy
import json
import pathlib
import subprocess
import sys

SNAPSHOT = {
    "A": {"next_hop": "B", "local": False},
    "B": {"next_hop": "D", "local": False},
    "D": {"next_hop": None, "local": True},
    "X": {"next_hop": None, "local": False},
}
TO_A = {"router": "B", "next_hop": "A", "local": False}
TO_D = {"router": "A", "next_hop": "D", "local": False}
LOCAL_A = {"router": "A", "next_hop": None, "local": True}

def result(hops, delivered=False, expired=False):
    return {"hops": hops, "delivered": delivered, "expired": expired}

# Independent probes after each specified update batch; each starts from SNAPSHOT.
CASES = [
    ("D", 3, [], "A", result(["A", "B", "D"], True)),
    ("D", 2, [], "A", result(["A", "B"], expired=True)),
    ("D", 1, [], "A", result(["A"], expired=True)),
    ("D", 0, [], "A", result(["A"], expired=True)),
    ("D", 5, [TO_A], "A", result(["A", "B", "A", "B", "A"], expired=True)),
    ("D", 4, [TO_A], "A", result(["A", "B", "A", "B"], expired=True)),
    ("D", 2, [TO_D], "A", result(["A", "D"], True)),
    ("D", 3, [TO_A, TO_D], "B", result(["B", "A", "D"], True)),
    ("D", 3, [TO_D, TO_A], "B", result(["B", "A", "D"], True)),
    ("A", 0, [LOCAL_A], "A", result(["A"], True)),
    ("D", 0, [], "D", result(["D"], True)),
    ("D", 8, [], "X", result(["X"])),
    ("D", 8, [{"router":"A","next_hop":"X","local":False}], "A", result(["A", "X"])),
    ("D", 2, [{"router":"A","next_hop":"X","local":False}, TO_D], "A", result(["A", "D"], True)),
    ("X", 0, [], "X", result(["X"])),
    ("D", 4, [], "MISSING", result(["MISSING"])),
    ("D", 3, [], "A", result(["A", "B", "D"], True)),
    # None here instructs the checker to omit the optional start argument.
    ("D", 3, [], None, result(["A", "B", "D"], True)),
]
EXPECTED = {"values": [case[4] for case in CASES], "unchanged": True}

def run(candidate):
    payload = base64.b64encode(json.dumps([SNAPSHOT, CASES]).encode()).decode()
    runner = r'''import base64, copy, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
snapshot, cases = json.loads(base64.b64decode(sys.argv[2]))
values, unchanged = [], True
for destination, ttl, updates, start, _ in cases:
    table = copy.deepcopy(snapshot)
    changes = copy.deepcopy(updates)
    if start is None:
        values.append(module.convergence_probe(table, destination, ttl, changes))
    else:
        values.append(module.convergence_probe(table, destination, ttl, changes, start=start))
    unchanged = unchanged and table == snapshot and changes == updates
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged}))'''
    try:
        process = subprocess.run([sys.executable,"-c",runner,str(pathlib.Path(candidate).resolve()),payload],capture_output=True,text=True,timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines() if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if process.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None

if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) == EXPECTED else 1)
