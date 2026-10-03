import base64
import json
import pathlib
import subprocess
import sys


def snap(base, owners=None, waits=None):
    return {"base": base, "owners": {} if owners is None else owners,
            "waits": {} if waits is None else waits}


# Each expected mapping is literal or the closed-form maximum of one named chain.
# No priority-propagation algorithm is used to create these oracles.
CASES = [
    ("empty input", [], []),
    ("empty snapshot", [snap({})], [{}]),
    ("free lock without tasks", [snap({}, {"free": None})], [{}]),
    ("base priorities without dependencies", [snap({"A": 5, "B": 9}, {"idle": None})],
     [{"A": 5, "B": 9}]),
    ("direct donation", [snap({"L": 1, "H": 9}, {"m": "L"}, {"H": "m"})],
     [{"L": 9, "H": 9}]),
    ("owner base remains higher", [snap({"L": 10, "H": 5}, {"m": "L"}, {"H": "m"})],
     [{"L": 10, "H": 5}]),
    ("two-hop inheritance", [snap({"A": 9, "B": 3, "C": 1},
      {"b": "B", "c": "C"}, {"A": "b", "B": "c"})], [{"A": 9, "B": 9, "C": 9}]),
    ("reverse edge iteration requires another pass", [snap({"A": 9, "B": 3, "C": 1},
      {"b": "B", "c": "C"}, {"B": "c", "A": "b"})], [{"A": 9, "B": 9, "C": 9}]),
    ("three-hop chain", [snap({"A": 9, "B": 3, "C": 2, "D": 1},
      {"b": "B", "c": "C", "d": "D"}, {"C": "d", "B": "c", "A": "b"})],
     [{"A": 9, "B": 9, "C": 9, "D": 9}]),
    ("several waiters choose maximum", [snap({"L": 1, "H": 9, "M": 7},
      {"m": "L"}, {"H": "m", "M": "m"})], [{"L": 9, "H": 9, "M": 7}]),
    ("remove dependencies one held lock at a time",
     [snap({"L": 2, "H": 9, "M": 7}, {"left": "L", "right": "L"}, {"H": "left", "M": "right"}),
      snap({"L": 2, "H": 9, "M": 7}, {"left": None, "right": "L"}, {"M": "right"}),
      snap({"L": 2, "H": 9, "M": 7}, {"left": None, "right": None})],
     [{"L": 9, "H": 9, "M": 7}, {"L": 7, "H": 9, "M": 7}, {"L": 2, "H": 9, "M": 7}]),
    ("equal remaining donation survives another release",
     [snap({"L": 2, "H": 9, "J": 9}, {"a": "L", "b": "L"}, {"H": "a", "J": "b"}),
      snap({"L": 2, "H": 9, "J": 9}, {"b": "L"}, {"J": "b"}),
      snap({"L": 2, "H": 9, "J": 9})],
     [{"L": 9, "H": 9, "J": 9}, {"L": 9, "H": 9, "J": 9}, {"L": 2, "H": 9, "J": 9}]),
    ("higher remaining donor survives weaker donor removal",
     [snap({"L": 2, "H": 7, "J": 9}, {"a": "L", "b": "L"}, {"H": "a", "J": "b"}),
      snap({"L": 2, "H": 7, "J": 9}, {"b": "L"}, {"J": "b"})],
     [{"L": 9, "H": 7, "J": 9}, {"L": 9, "H": 7, "J": 9}]),
    ("ownership handoff recomputes from base",
     [snap({"L": 1, "M": 3, "H": 10}, {"x": "L"}, {"H": "x"}),
      snap({"L": 1, "M": 3, "H": 10}, {"x": "M"}, {"H": "x"}),
      snap({"L": 1, "M": 3, "H": 10}, {"x": None})],
     [{"L": 10, "M": 3, "H": 10}, {"L": 1, "M": 10, "H": 10}, {"L": 1, "M": 3, "H": 10}]),
    ("base priority changes are fresh inputs",
     [snap({"L": 10, "H": 9}, {"x": "L"}, {"H": "x"}),
      snap({"L": 1, "H": 4}, {"x": "L"}, {"H": "x"}),
      snap({"L": 1, "H": 0}, {"x": "L"}, {"H": "x"})],
     [{"L": 10, "H": 9}, {"L": 4, "H": 4}, {"L": 1, "H": 0}]),
    ("two-node cycle reaches mathematical least fixed point",
     [snap({"A": 2, "B": 8}, {"a": "A", "b": "B"}, {"A": "b", "B": "a"})],
     [{"A": 8, "B": 8}]),
    ("cycle loses vanished external donation",
     [snap({"A": 2, "B": 8, "H": 15}, {"a": "A", "b": "B"}, {"A": "b", "B": "a", "H": "a"}),
      snap({"A": 2, "B": 8, "H": 15}, {"a": "A", "b": "B"}, {"A": "b", "B": "a"})],
     [{"A": 15, "B": 15, "H": 15}, {"A": 8, "B": 8, "H": 15}]),
    ("three-node cycle excludes unrelated high task",
     [snap({"A": 2, "B": 4, "C": 6, "U": 255},
           {"a": "A", "b": "B", "c": "C"}, {"A": "b", "B": "c", "C": "a"})],
     [{"A": 6, "B": 6, "C": 6, "U": 255}]),
    ("merged wait chains do not donate backward to other waiters",
     [snap({"A": 10, "B": 5, "C": 3, "D": 1},
           {"b": "B", "d": "D"}, {"C": "d", "B": "d", "A": "b"})],
     [{"A": 10, "B": 10, "C": 3, "D": 10}]),
    ("zero is a valid priority", [snap({"A": 0, "B": 0}, {"l": "A"}, {"B": "l"})],
     [{"A": 0, "B": 0}]),
    ("largest declared donor", [snap({"A": 0, "B": 255}, {"l": "A"}, {"B": "l"})],
     [{"A": 255, "B": 255}]),
    ("case-sensitive opaque task and lock identifiers",
     [snap({"z": 1, "A": 9, "z_1": 3}, {"L-0": "z", "l-0": "z_1"}, {"A": "L-0"})],
     [{"z": 9, "A": 9, "z_1": 3}]),
    ("task and lock ID namespaces may overlap",
     [snap({"same": 1, "Other": 9}, {"same": "same"}, {"Other": "same"})],
     [{"same": 9, "Other": 9}]),
    ("tasks can disappear between independent snapshots",
     [snap({"A": 1, "B": 9}, {"m": "A"}, {"B": "m"}), snap({"A": 1}), snap({})],
     [{"A": 9, "B": 9}, {"A": 1}, {}]),
    ("full-domain-length reverse-propagating chain",
     [snap({**{f"t{i}": i for i in range(31)}, "t31": 255},
           {f"l{i}": f"t{i}" for i in range(31)},
           {f"t{i+1}": f"l{i}" for i in range(31)})],
     [{f"t{i}": 255 for i in range(32)}]),
]
CALLS = CASES + [CASES[10], CASES[0], CASES[1], CASES[4]]
EXPECTED = [value for _, _, value in CALLS]


def matches(actual):
    expected = {"values": EXPECTED, "unchanged": True}
    return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)


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
    if type(value) in (str,int,type(None)):
        return (type(value).__name__,value)
    raise TypeError("value outside the exact input/output types")
values=[];unchanged=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args)
    value=module.priority_inheritance(supplied)
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
