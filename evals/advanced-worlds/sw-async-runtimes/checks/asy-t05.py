import base64
import json
import pathlib
import subprocess
import sys


def expected(started=(), completed=(), running=(), queued=(), deadlocked=False):
    return {"started": list(started), "completed": list(completed),
            "running": list(running), "queued": list(queued), "deadlocked": deadlocked}


def case(name, capacity, running, queued, dependencies, outcome):
    return (name, {"capacity": capacity, "running": running, "queued": queued,
                   "dependencies": dependencies}, outcome)


# Literal canonical completion witnesses and closed residual wait states.
# Queued jobs are finite leaves; no reduction algorithm generates the oracles.
CASES = [
    case("empty one-worker pool", 1, [], [], {}, expected()),
    case("empty four-worker pool", 4, [], [], {}, expected()),
    case("one running finite job", 1, ["R"], [], {"R": []}, expected(completed=["R"])),
    case("one queued finite job", 1, [], ["J"], {"J": []}, expected(["J"], ["J"])),
    case("one worker waits for its queued child", 1, ["P"], ["C"], {"P": ["C"], "C": []},
         expected(running=["P"], queued=["C"], deadlocked=True)),
    case("one spare worker breaks the dependency", 2, ["P"], ["C"], {"P": ["C"], "C": []},
         expected(["C"], ["C", "P"])),
    case("two occupied parents retain every worker", 2, ["P", "Q"], ["C", "D"],
         {"P": ["C"], "Q": ["D"], "C": [], "D": []},
         expected(running=["P", "Q"], queued=["C", "D"], deadlocked=True)),
    case("third worker completes the closed children", 3, ["P", "Q"], ["C", "D"],
         {"P": ["C"], "Q": ["D"], "C": [], "D": []},
         expected(["C", "D"], ["C", "P", "D", "Q"])),
    case("ready parent releases one occupied slot", 2, ["P", "R"], ["C"],
         {"P": ["C"], "R": [], "C": []}, expected(["C"], ["R", "C", "P"])),
    case("queued starts retain FIFO rather than lexical order", 1, [], ["Z", "A", "M"],
         {"Z": [], "A": [], "M": []}, expected(["Z", "A", "M"], ["Z", "A", "M"])),
    case("ready running jobs finish before new starts", 3, ["z", "B", "A"], ["C"],
         {"z": [], "B": [], "A": [], "C": []}, expected(["C"], ["A", "B", "z", "C"])),
    case("cycle among running jobs", 2, ["Q", "P"], [], {"P": ["Q"], "Q": ["P"]},
         expected(running=["P", "Q"], deadlocked=True)),
    case("unused capacity cannot repair a running cycle", 3, ["P", "Q"], [],
         {"P": ["Q"], "Q": ["P"]}, expected(running=["P", "Q"], deadlocked=True)),
    case("self wait remains after unrelated queued work", 4, ["P"], ["X"],
         {"P": ["P"], "X": []}, expected(["X"], ["X"], ["P"], deadlocked=True)),
    case("parent chain cannot start queued leaf while full", 2, ["P", "Q"], ["C"],
         {"P": ["Q"], "Q": ["C"], "C": []},
         expected(running=["P", "Q"], queued=["C"], deadlocked=True)),
    case("spare slot resolves entire parent chain", 3, ["P", "Q"], ["C"],
         {"P": ["Q"], "Q": ["C"], "C": []}, expected(["C"], ["C", "Q", "P"])),
    case("all dependencies must complete", 2, ["P"], ["C", "D"],
         {"P": ["C", "D"], "C": [], "D": []}, expected(["C", "D"], ["C", "D", "P"])),
    case("all dependencies queued behind sole parent", 1, ["P"], ["C", "D"],
         {"P": ["C", "D"], "C": [], "D": []},
         expected(running=["P"], queued=["C", "D"], deadlocked=True)),
    case("already-running completion is not a new start", 2, ["P"], ["C", "D"],
         {"P": [], "C": [], "D": []}, expected(["C", "D"], ["P", "C", "D"])),
    case("eligible parent finishes before next queued leaf", 3, ["P", "Q"], ["X", "Y"],
         {"P": ["X"], "Q": [], "X": [], "Y": []}, expected(["X", "Y"], ["Q", "X", "P", "Y"])),
    case("lexical eligibility is reevaluated after child completion", 2, ["A", "B"], ["C", "D"],
         {"A": ["C"], "B": [], "C": [], "D": []}, expected(["C", "D"], ["B", "C", "A", "D"])),
    case("blocked residual preserves FIFO queue", 2, ["b", "A"], ["Z", "C"],
         {"b": ["C"], "A": ["Z"], "Z": [], "C": []},
         expected(running=["A", "b"], queued=["Z", "C"], deadlocked=True)),
    case("completed jobs do not make an unrelated cycle finish", 3, ["P", "Q", "R"], ["C"],
         {"P": ["Q"], "Q": ["P"], "R": [], "C": []},
         expected(["C"], ["R", "C"], ["P", "Q"], deadlocked=True)),
    case("downstream blocked job is included", 3, ["P", "Q", "R"], [],
         {"P": ["Q"], "Q": ["P"], "R": ["P"]},
         expected(running=["P", "Q", "R"], deadlocked=True)),
    case("maximum declared job count remains closed", 4, ["A", "B", "C", "D"], list("EFGHIJKL"),
         {"A": ["E", "F"], "B": ["G", "H"], "C": ["I", "J"], "D": ["K", "L"],
          "E": [], "F": [], "G": [], "H": [], "I": [], "J": [], "K": [], "L": []},
         expected(running=["A", "B", "C", "D"], queued=list("EFGHIJKL"), deadlocked=True)),
    case("maximum count of finite independent jobs", 4, ["D", "C", "B", "A"], list("EFGHIJKL"),
         {name: [] for name in "ABCDEFGHIJKL"},
         expected(list("EFGHIJKL"), list("ABCDEFGHIJKL"))),
    case("completion names need not follow dependency names", 2, ["A_1", "z"], [],
         {"A_1": ["z"], "z": []}, expected(completed=["z", "A_1"])),
]
CALLS = CASES + [CASES[6], CASES[0], CASES[3], CASES[6]]
EXPECTED = [value for _, _, value in CALLS]


def matches(actual):
    return json.dumps(actual, sort_keys=True) == json.dumps(
        {"values": EXPECTED, "unchanged": True}, sort_keys=True)


def run(candidate):
    payload = base64.b64encode(json.dumps([args for _, args, _ in CALLS]).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
def fingerprint(value):
    if type(value) is dict and all(type(key) is str for key in value):
        return ("dict",tuple((key,fingerprint(value[key])) for key in sorted(value)))
    if type(value) is list:
        return ("list",tuple(fingerprint(item) for item in value))
    if type(value) in (str,int,bool,type(None)):
        return (type(value).__name__,value)
    raise TypeError("value outside the exact input/output types")
values=[];unchanged=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args)
    value=module.pool_completion(**supplied)
    fingerprint(value)
    values.append(value)
    unchanged=unchanged and fingerprint(supplied)==fingerprint(args)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged}))'''
    try:
        result = subprocess.run([sys.executable, "-B", "-c", runner,
                                 str(pathlib.Path(candidate).resolve()), payload],
                                capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in result.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if result.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


if __name__ == "__main__":
    ok = len(sys.argv) == 2 and matches(run(sys.argv[1]))
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
