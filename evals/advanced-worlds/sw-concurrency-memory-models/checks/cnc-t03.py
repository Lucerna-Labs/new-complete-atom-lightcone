import base64
import json
import pathlib
import subprocess
import sys


def process(pid, allocation, request):
    return {"id": pid, "allocation": allocation, "request": request}


def expected(order, work, blocked=(), deficits=None):
    return {"order": order, "work": work, "blocked": list(blocked),
            "deficits": {} if deficits is None else deficits}


# Literal witnesses and residual deficits, derived from current outstanding
# requests. These are not maximum-claim Banker inputs or minimal-cycle oracles.
CASES = [
    ("empty zero pool", [[0], []], expected([], [0])),
    ("empty mixed pool", [[2, 0], []], expected([], [2, 0])),
    ("empty process completes", [[0], [process("A", [0], [0])]],
     expected(["A"], [0])),
    ("held resources returned", [[0], [process("A", [3], [0])]],
     expected(["A"], [3])),
    ("request exactly available", [[1], [process("A", [1], [1])]],
     expected(["A"], [2])),
    ("vector exact equality", [[2, 1], [process("A", [1, 2], [2, 1])]],
     expected(["A"], [3, 3])),
    ("single instance closed cycle", [[0, 0], [process("A", [1, 0], [0, 1]),
                                                process("B", [0, 1], [1, 0])]],
     expected([], [0, 0], ["A", "B"], {"A": [0, 1], "B": [1, 0]})),
    ("spare instance breaks resource type cycle", [[1, 0], [process("A", [1, 0], [0, 1]),
                                                            process("B", [0, 1], [1, 0])]],
     expected(["B", "A"], [2, 1])),
    ("three instances permit two holders", [[1], [process("B", [1], [1]),
                                                process("A", [1], [1])]],
     expected(["A", "B"], [3])),
    ("two instances cannot satisfy two holders", [[0], [process("A", [1], [1]),
                                                       process("B", [1], [1])]],
     expected([], [0], ["A", "B"], {"A": [1], "B": [1]})),
    ("finishing holder releases extra instance", [[0], [process("A", [1], [1]),
                                                        process("B", [1], [1]),
                                                        process("Z", [1], [0])]],
     expected(["Z", "A", "B"], [3])),
    ("restart lexical eligibility", [[0], [process("A", [0], [1]),
                                           process("Z", [0], [0]),
                                           process("C", [1], [0])]],
     expected(["C", "A", "Z"], [1])),
    ("grants do not create resources", [[2], [process("A", [0], [1]),
                                              process("B", [0], [2])]],
     expected(["A", "B"], [2])),
    ("allocation greater than request", [[1], [process("A", [3], [1])]],
     expected(["A"], [4])),
    ("request greater than allocation", [[3], [process("A", [1], [3])]],
     expected(["A"], [4])),
    ("zero holder waits downstream of cycle", [[0, 0], [process("C", [0, 0], [1, 0]),
                                                        process("B", [0, 1], [1, 0]),
                                                        process("A", [1, 0], [0, 1])]],
     expected([], [0, 0], ["A", "B", "C"],
              {"A": [0, 1], "B": [1, 0], "C": [1, 0]})),
    ("independent completion leaves cycle", [[0, 0, 0], [process("A", [1, 0, 0], [0, 1, 0]),
                                                         process("B", [0, 1, 0], [1, 0, 0]),
                                                         process("C", [0, 0, 2], [0, 0, 0])]],
     expected(["C"], [0, 0, 2], ["A", "B"],
              {"A": [0, 1, 0], "B": [1, 0, 0]})),
    ("multi-resource AND and partial deficits", [[1, 0], [process("A", [0, 2], [2, 0]),
                                                         process("B", [2, 0], [0, 2])]],
     expected([], [1, 0], ["A", "B"], {"A": [1, 0], "B": [0, 2]})),
    ("available in every dimension matters", [[1, 0], [process("A", [0, 1], [1, 0]),
                                                        process("B", [1, 0], [0, 1])]],
     expected(["A", "B"], [2, 1])),
    ("case sensitive lexical order", [[0], [process("a", [1], [0]),
                                            process("B", [1], [0]),
                                            process("A", [1], [0])]],
     expected(["A", "B", "a"], [3])),
    ("request order is not size order", [[3], [process("B", [1], [1]),
                                               process("A", [0], [3])]],
     expected(["A", "B"], [4])),
    ("unused zero capacity dimension", [[1, 0, 2], [process("A", [1, 0, 0], [1, 0, 2])]],
     expected(["A"], [2, 0, 2])),
    ("three resource closed ring", [[0, 0, 0], [process("A", [1, 0, 0], [0, 1, 0]),
                                                 process("B", [0, 1, 0], [0, 0, 1]),
                                                 process("C", [0, 0, 1], [1, 0, 0])]],
     expected([], [0, 0, 0], ["A", "B", "C"],
              {"A": [0, 1, 0], "B": [0, 0, 1], "C": [1, 0, 0]})),
    ("three resource ring with spare", [[0, 0, 1], [process("A", [1, 0, 0], [0, 1, 0]),
                                                    process("B", [0, 1, 0], [0, 0, 1]),
                                                    process("C", [0, 0, 1], [1, 0, 0])]],
     expected(["B", "A", "C"], [1, 1, 2])),
    ("finish does not surrender another allocation", [[0, 0], [process("A", [1, 0], [0, 0]),
                                                               process("B", [0, 1], [1, 0]),
                                                               process("C", [0, 0], [0, 1])]],
     expected(["A", "B", "C"], [1, 1])),
    ("resource return remains vector valued", [[1, 0, 1], [process("A", [0, 2, 0], [1, 0, 1]),
                                                          process("B", [3, 0, 4], [0, 2, 0])]],
     expected(["A", "B"], [4, 2, 5])),
    ("deficits recomputed after all possible completions", [[0, 0], [process("A", [1, 0], [0, 2]),
                                                                    process("B", [0, 2], [2, 0]),
                                                                    process("Z", [1, 1], [0, 0])]],
     expected(["Z"], [1, 1], ["A", "B"], {"A": [0, 1], "B": [1, 0]})),
    ("eight resource types", [[0] * 8, [process("A", [1, 2, 3, 4, 5, 6, 7, 8], [0] * 8)]],
     expected(["A"], [1, 2, 3, 4, 5, 6, 7, 8])),
    ("maximum process count and per-field values", [[1000], [process(pid, [1000], [1000])
                                                            for pid in "LKJIHGFEDCBA"]],
     expected(list("ABCDEFGHIJKL"), [13000])),
]
CASES.append(CASES[7])  # Calls are independent, including repeated inputs.


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
    if type(value) in (str,int,type(None)):
        return (type(value).__name__,value)
    raise TypeError("value outside the exact input/output types")
values=[];unchanged=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args)
    value=module.reduce_resources(*supplied)
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
