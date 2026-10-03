"""Independent hand-worked traces and closed-form starvation families."""
import base64
import json
import pathlib
import subprocess
import sys


def out(trace=(), log=(), tasks=(), microtasks=(), status="idle"):
    return {"trace": [list(x) for x in trace], "log": list(log),
            "tasks": list(tasks), "microtasks": list(microtasks), "status": status}


CASES = [
    ("empty zero budget", [{}, [], 0], out()),
    ("empty positive budget", [{}, [], 4], out()),
    ("work retained at zero budget", [{"A": [["emit", "a"]]}, ["A"], 0],
     out(tasks=["A"], status="budget")),
    ("exact last callback finishes", [{"A": [["emit", "a"]]}, ["A"], 1],
     out([["task", "A"]], ["a"])),
    ("empty callback still counts", [{"A": []}, ["A", "A"], 1],
     out([["task", "A"]], tasks=["A"], status="budget")),
    ("repeated callback identifiers", [{"A": [["emit", "a"]]}, ["A", "A"], 2],
     out([["task", "A"], ["task", "A"]], ["a", "a"])),
]
MIXED = {
    "A": [["emit", "start"], ["micro", "M"], ["task", "B"], ["emit", "end"]],
    "M": [["emit", "m"]], "B": [["emit", "b"]], "Z": [["emit", "z"]],
}
CASES.extend([
    ("callback is atomic", [MIXED, ["A", "Z"], 1],
     out([["task", "A"]], ["start", "end"], ["Z", "B"], ["M"], "budget")),
    ("microtask precedes both queued tasks", [MIXED, ["A", "Z"], 4],
     out([["task", "A"], ["micro", "M"], ["task", "Z"], ["task", "B"]],
         ["start", "end", "m", "z", "b"])),
])
NESTED = {"A": [["micro", "M"], ["micro", "N"]], "Z": [["emit", "z"]],
          "M": [["emit", "m"], ["micro", "P"], ["task", "T"]],
          "N": [["emit", "n"]], "P": [["emit", "p"]], "T": [["emit", "t"]]}
CASES.extend([
    ("new microtask stays behind existing microtask", [NESTED, ["A", "Z"], 6],
     out([["task", "A"], ["micro", "M"], ["micro", "N"], ["micro", "P"],
          ["task", "Z"], ["task", "T"]], ["m", "n", "p", "z", "t"])),
    ("budget retains FIFO successors", [NESTED, ["A", "Z"], 2],
     out([["task", "A"], ["micro", "M"]], ["m"], ["Z", "T"], ["N", "P"], "budget")),
    ("ordinary task self enqueue", [{"T": [["emit", "tick"], ["task", "T"]]}, ["T"], 5],
     out([["task", "T"]]*5, ["tick"]*5, ["T"], status="budget")),
    ("emits preserve Unicode and empty strings", [{"a": [["emit", ""], ["emit", "α"], ["emit", "α"]]}, ["a"], 9],
     out([["task", "a"]], ["", "α", "α"])),
])
# Each cycle consumes one callback and recreates exactly one microtask.
for budget in range(1, 10):
    jobs = {"A": [["micro", "R"]], "R": [["emit", "r"], ["micro", "R"]], "Z": [["emit", "z"]]}
    CASES.append(("self replenishing checkpoint " + str(budget), [jobs, ["A", "Z"], budget],
                  out([["task", "A"]] + [["micro", "R"]]*(budget-1),
                      ["r"]*(budget-1), ["Z"], ["R"], "budget")))
# In a finite chain all n successors run before the next task. No simulator
# is used to construct this oracle; its queue and trace are closed forms.
for n in range(1, 7):
    jobs = {"A": [["micro", "m0"]], "Z": [["emit", "z"]]}
    for i in range(n):
        jobs["m"+str(i)] = [["emit", str(i)]] + ([["micro", "m"+str(i+1)]] if i+1<n else [])
    CASES.append(("finite chain " + str(n), [jobs, ["A", "Z"], n+2],
                  out([["task", "A"]] + [["micro", "m"+str(i)] for i in range(n)] + [["task", "Z"]],
                      [str(i) for i in range(n)] + ["z"])))
CASES.extend([CASES[8], CASES[0]])


def run(candidate):
    payload = base64.b64encode(json.dumps([args for _, args, _ in CASES]).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
def fingerprint(value):
    if type(value) is dict and all(type(k) is str for k in value):
        return ("dict",tuple((k,fingerprint(value[k])) for k in sorted(value)))
    if type(value) is list:
        return ("list",tuple(fingerprint(x) for x in value))
    if type(value) in (str,int,bool,type(None)):
        return (type(value).__name__,value)
    raise TypeError("unsupported native value type")
values=[];unchanged=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args)
    result=module.run_loop(*supplied)
    fingerprint(result);values.append(result)
    unchanged=unchanged and fingerprint(args)==fingerprint(supplied)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged}))'''
    try:
        process = subprocess.run([sys.executable, "-B", "-c", runner,
                                  str(pathlib.Path(candidate).resolve()), payload],
                                 capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        if process.returncode or not lines:
            return False, "candidate execution"
        actual = json.loads(lines[-1])
        if actual.get("unchanged") is not True:
            return False, "input mutation"
        values = actual.get("values")
        if not isinstance(values, list) or len(values) != len(CASES):
            return False, "output count"
        for (label, _, expected), value in zip(CASES, values):
            if json.dumps(value, sort_keys=True) != json.dumps(expected, sort_keys=True):
                return False, label
        return True, str(len(CASES)) + " deterministic calls"
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False, "candidate execution"


if __name__ == "__main__":
    ok, detail = run(sys.argv[1]) if len(sys.argv) == 2 else (False, "candidate path required")
    print(("PASS: " if ok else "FAIL: ") + detail)
    sys.exit(0 if ok else 1)
