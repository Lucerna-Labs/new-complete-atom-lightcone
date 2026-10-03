import base64
import json
import pathlib
import subprocess
import sys


def event(op, reader="r"):
    return {"op": op, "reader": reader}


def source(node):
    return {"op": "set_source", "node": node}


def retire(node):
    return {"op": "retire", "node": node}


def state(candidate=None, hazard=None, validated=False):
    return {"candidate": candidate, "hazard": hazard, "validated": validated}


def snap(op, result, source, readers=None, retired=(), reclaimed=()):
    return {"op": op, "result": result, "source": source,
            "readers": {} if readers is None else readers,
            "retired": list(retired), "reclaimed": list(reclaimed)}


SCAN = {"op": "scan"}

# Every snapshot is a hand-specified protocol-state oracle. "safe" denotes
# the stated gates, not an iff assertion about physical use-after-free.
CASES = [
    ("empty trace", [[], None, []], []),
    ("empty source and missing candidate", [[], None,
       [event("use"), event("publish"), event("validate"), event("clear"), event("load")]],
     [snap("use", "empty", None, {"r": state()}),
      snap("publish", None, None, {"r": state()}),
      snap("validate", False, None, {"r": state()}),
      snap("clear", None, None, {"r": state()}),
      snap("load", None, None, {"r": state()})]),
    ("load does not publish", [["A"], "A", [event("load"), event("use")]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("use", "unprotected", "A", {"r": state("A")})]),
    ("publication does not validate", [["A"], "A",
       [event("load"), event("publish"), event("use")]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("use", "unvalidated", "A", {"r": state("A", "A")})]),
    ("ordered publish validate use", [["A"], "A",
       [event("load"), event("publish"), event("validate"), event("use")]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("validate", True, "A", {"r": state("A", "A", True)}),
      snap("use", "safe", "A", {"r": state("A", "A", True)})]),
    ("validate requires a published matching slot", [["A"], "A",
       [event("load"), event("validate"), event("use")]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("validate", False, "A", {"r": state("A")}),
      snap("use", "unprotected", "A", {"r": state("A")})]),
    ("publishing again resets validation", [["A"], "A",
       [event("load"), event("publish"), event("validate"), event("publish"), event("use")]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("validate", True, "A", {"r": state("A", "A", True)}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("use", "unvalidated", "A", {"r": state("A", "A")})]),
    ("new load resets validation but retains hazard", [["A"], "A",
       [event("load"), event("publish"), event("validate"), event("load"), event("use")]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("validate", True, "A", {"r": state("A", "A", True)}),
      snap("load", "A", "A", {"r": state("A", "A")}),
      snap("use", "unvalidated", "A", {"r": state("A", "A")})]),
    ("protected use remains valid after source changes", [["A", "B"], "A",
       [event("load"), event("publish"), event("validate"), source("B"), event("use")]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("validate", True, "A", {"r": state("A", "A", True)}),
      snap("set_source", None, "B", {"r": state("A", "A", True)}),
      snap("use", "safe", "B", {"r": state("A", "A", True)})]),
    ("retirement does not reclaim protected storage", [["A", "B"], "A",
       [event("load"), event("publish"), event("validate"), source("B"),
        retire("A"), SCAN, event("use"), event("clear"), SCAN, event("use")]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("validate", True, "A", {"r": state("A", "A", True)}),
      snap("set_source", None, "B", {"r": state("A", "A", True)}),
      snap("retire", None, "B", {"r": state("A", "A", True)}, ["A"]),
      snap("scan", [], "B", {"r": state("A", "A", True)}, ["A"]),
      snap("use", "safe", "B", {"r": state("A", "A", True)}, ["A"]),
      snap("clear", None, "B", {"r": state("A")}, ["A"]),
      snap("scan", ["A"], "B", {"r": state("A")}, reclaimed=["A"]),
      snap("use", "reclaimed", "B", {"r": state("A")}, reclaimed=["A"])]),
    ("late publication cannot resurrect reclaimed candidate", [["A", "B"], "A",
       [event("load"), source("B"), retire("A"), SCAN, event("publish"),
        event("validate"), event("use"), SCAN]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("set_source", None, "B", {"r": state("A")}),
      snap("retire", None, "B", {"r": state("A")}, ["A"]),
      snap("scan", ["A"], "B", {"r": state("A")}, reclaimed=["A"]),
      snap("publish", "A", "B", {"r": state("A", "A")}, reclaimed=["A"]),
      snap("validate", False, "B", {"r": state("A", "A")}, reclaimed=["A"]),
      snap("use", "reclaimed", "B", {"r": state("A", "A")}, reclaimed=["A"]),
      snap("scan", [], "B", {"r": state("A", "A")}, reclaimed=["A"])]),
    ("unvalidated publication still participates in scan", [["A", "B"], "A",
       [event("load"), event("publish"), source("B"), retire("A"), SCAN,
        event("validate"), event("use"), event("clear"), SCAN]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("set_source", None, "B", {"r": state("A", "A")}),
      snap("retire", None, "B", {"r": state("A", "A")}, ["A"]),
      snap("scan", [], "B", {"r": state("A", "A")}, ["A"]),
      snap("validate", False, "B", {"r": state("A", "A")}, ["A"]),
      snap("use", "unvalidated", "B", {"r": state("A", "A")}, ["A"]),
      snap("clear", None, "B", {"r": state("A")}, ["A"]),
      snap("scan", ["A"], "B", {"r": state("A")}, reclaimed=["A"])]),
    ("new candidate does not silently clear old hazard", [["A", "B"], "A",
       [event("load"), event("publish"), event("validate"), source("B"),
        event("load"), retire("A"), SCAN, event("use"), event("publish"),
        SCAN, event("validate"), event("use")]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("validate", True, "A", {"r": state("A", "A", True)}),
      snap("set_source", None, "B", {"r": state("A", "A", True)}),
      snap("load", "B", "B", {"r": state("B", "A")}),
      snap("retire", None, "B", {"r": state("B", "A")}, ["A"]),
      snap("scan", [], "B", {"r": state("B", "A")}, ["A"]),
      snap("use", "unprotected", "B", {"r": state("B", "A")}, ["A"]),
      snap("publish", "B", "B", {"r": state("B", "B")}, ["A"]),
      snap("scan", ["A"], "B", {"r": state("B", "B")}, reclaimed=["A"]),
      snap("validate", True, "B", {"r": state("B", "B", True)}, reclaimed=["A"]),
      snap("use", "safe", "B", {"r": state("B", "B", True)}, reclaimed=["A"])]),
    ("all readers must release a protected address", [["A"], "A",
       [event("load", "r"), event("publish", "r"), event("load", "s"),
        event("publish", "s"), source(None), retire("A"), event("clear", "r"),
        SCAN, event("clear", "s"), SCAN]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("load", "A", "A", {"r": state("A", "A"), "s": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A"), "s": state("A", "A")}),
      snap("set_source", None, None, {"r": state("A", "A"), "s": state("A", "A")}),
      snap("retire", None, None, {"r": state("A", "A"), "s": state("A", "A")}, ["A"]),
      snap("clear", None, None, {"r": state("A"), "s": state("A", "A")}, ["A"]),
      snap("scan", [], None, {"r": state("A"), "s": state("A", "A")}, ["A"]),
      snap("clear", None, None, {"r": state("A"), "s": state("A")}, ["A"]),
      snap("scan", ["A"], None, {"r": state("A"), "s": state("A")}, reclaimed=["A"])]),
    ("scan reclaims only unprotected retired nodes", [["A", "B", "C"], "A",
       [event("load"), event("publish"), source("B"), retire("C"), retire("A"), SCAN]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("set_source", None, "B", {"r": state("A", "A")}),
      snap("retire", None, "B", {"r": state("A", "A")}, ["C"]),
      snap("retire", None, "B", {"r": state("A", "A")}, ["A", "C"]),
      snap("scan", ["C"], "B", {"r": state("A", "A")}, ["A"], ["C"])]),
    ("logical ABA is not lifetime rejection", [["A", "B"], "A",
       [event("load"), source("B"), source("A"), event("publish"), event("validate"), event("use")]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("set_source", None, "B", {"r": state("A")}),
      snap("set_source", None, "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("validate", True, "A", {"r": state("A", "A", True)}),
      snap("use", "safe", "A", {"r": state("A", "A", True)})]),
    ("scan all retired nodes in case sensitive order", [["b", "A", "a"], None,
       [retire("b"), retire("a"), retire("A"), SCAN, SCAN]],
     [snap("retire", None, None, retired=["b"]),
      snap("retire", None, None, retired=["a", "b"]),
      snap("retire", None, None, retired=["A", "a", "b"]),
      snap("scan", ["A", "a", "b"], None, reclaimed=["A", "a", "b"]),
      snap("scan", [], None, reclaimed=["A", "a", "b"])]),
    ("clear removes validation before any reclamation", [["A"], "A",
       [event("load"), event("publish"), event("validate"), event("clear"), event("use")]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("validate", True, "A", {"r": state("A", "A", True)}),
      snap("clear", None, "A", {"r": state("A")}),
      snap("use", "unprotected", "A", {"r": state("A")})]),
    ("source mismatch fails validation without clearing hazard", [["A", "B"], "A",
       [event("load"), event("publish"), source("B"), event("validate"), event("use")]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("set_source", None, "B", {"r": state("A", "A")}),
      snap("validate", False, "B", {"r": state("A", "A")}),
      snap("use", "unvalidated", "B", {"r": state("A", "A")})]),
    ("readers have separate candidate and protection state", [["A", "B"], "A",
       [event("load", "R"), event("publish", "R"), event("validate", "R"),
        source("B"), event("load", "r"), event("use", "R"), event("use", "r")]],
     [snap("load", "A", "A", {"R": state("A")}),
      snap("publish", "A", "A", {"R": state("A", "A")}),
      snap("validate", True, "A", {"R": state("A", "A", True)}),
      snap("set_source", None, "B", {"R": state("A", "A", True)}),
      snap("load", "B", "B", {"R": state("A", "A", True), "r": state("B")}),
      snap("use", "safe", "B", {"R": state("A", "A", True), "r": state("B")}),
      snap("use", "unprotected", "B", {"R": state("A", "A", True), "r": state("B")})]),
    ("explicit failed revalidation replaces prior success", [["A", "B"], "A",
       [event("load"), event("publish"), event("validate"), source("B"),
        event("validate"), event("use")]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("validate", True, "A", {"r": state("A", "A", True)}),
      snap("set_source", None, "B", {"r": state("A", "A", True)}),
      snap("validate", False, "B", {"r": state("A", "A")}),
      snap("use", "unvalidated", "B", {"r": state("A", "A")})]),
    ("distinct protected retired objects are released independently", [["A", "B"], "A",
       [event("load", "r"), event("publish", "r"), source("B"),
        event("load", "s"), event("publish", "s"), source(None),
        retire("A"), retire("B"), SCAN, event("clear", "r"), SCAN,
        event("clear", "s"), SCAN]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("set_source", None, "B", {"r": state("A", "A")}),
      snap("load", "B", "B", {"r": state("A", "A"), "s": state("B")}),
      snap("publish", "B", "B", {"r": state("A", "A"), "s": state("B", "B")}),
      snap("set_source", None, None, {"r": state("A", "A"), "s": state("B", "B")}),
      snap("retire", None, None, {"r": state("A", "A"), "s": state("B", "B")}, ["A"]),
      snap("retire", None, None, {"r": state("A", "A"), "s": state("B", "B")}, ["A", "B"]),
      snap("scan", [], None, {"r": state("A", "A"), "s": state("B", "B")}, ["A", "B"]),
      snap("clear", None, None, {"r": state("A"), "s": state("B", "B")}, ["A", "B"]),
      snap("scan", ["A"], None, {"r": state("A"), "s": state("B", "B")}, ["B"], ["A"]),
      snap("clear", None, None, {"r": state("A"), "s": state("B")}, ["B"], ["A"]),
      snap("scan", ["B"], None, {"r": state("A"), "s": state("B")}, reclaimed=["A", "B"])]),
    ("null reload retains old protection until publication replaces it", [["A"], "A",
       [event("load"), event("publish"), source(None), event("load"),
        event("use"), retire("A"), SCAN, event("publish"), SCAN]],
     [snap("load", "A", "A", {"r": state("A")}),
      snap("publish", "A", "A", {"r": state("A", "A")}),
      snap("set_source", None, None, {"r": state("A", "A")}),
      snap("load", None, None, {"r": state(None, "A")}),
      snap("use", "empty", None, {"r": state(None, "A")}),
      snap("retire", None, None, {"r": state(None, "A")}, ["A"]),
      snap("scan", [], None, {"r": state(None, "A")}, ["A"]),
      snap("publish", None, None, {"r": state()}, ["A"]),
      snap("scan", ["A"], None, {"r": state()}, reclaimed=["A"])]),
]
CASES.append(CASES[9])  # No state may leak into an independent repeated call.
CASES.append(CASES[0])  # Empty after nonempty must not reuse an earlier trace.


def run(candidate):
    payload = base64.b64encode(json.dumps([args for _, args, _ in CASES]).encode()).decode()
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
    value=module.hazard_trace(*supplied)
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
        actual = json.loads(lines[-1]) if result.returncode == 0 and lines else None
        wanted = {"values": [value for _, _, value in CASES], "unchanged": True}
        return json.dumps(actual, sort_keys=True) == json.dumps(wanted, sort_keys=True)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return False


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
