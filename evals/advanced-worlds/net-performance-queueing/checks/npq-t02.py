import base64
import json
import math
import pathlib
import subprocess
import sys


def sample(now, enqueued, backlog):
    return {"now": now, "enqueued": enqueued, "backlog": backlog}


def state(deadline=0, eligible=False):
    return {"first_above_time": deadline, "eligible": eligible}


def case(samples, expected, **parameters):
    return ({"samples": samples, **parameters}, expected)


# Literal expected deadlines, including equality, rearming, and large clocks.
CASES = [
    case([], []),
    case([sample(0, None, 0), sample(5, None, 0)], [state(), state()]),
    case([sample(20, 15, 1501), sample(119, 15, 1501),
          sample(120, 15, 1501), sample(121, 15, 1501)],
         [state(120), state(120), state(120, True), state(120, True)]),
    case([sample(100, 90, 2000), sample(150, 146, 2000),
          sample(160, 155, 2000), sample(200, 190, 2000), sample(260, 250, 2000)],
         [state(200), state(), state(260), state(260), state(260, True)]),
    case([sample(100, 90, 2000), sample(200, 190, 1500),
          sample(205, 195, 1501), sample(304, 294, 1501), sample(305, 295, 1501)],
         [state(200), state(), state(305), state(305), state(305, True)]),
    case([sample(100, 90, 2000), sample(200, None, 0),
          sample(201, 191, 2000), sample(300, 290, 2000), sample(301, 291, 2000)],
         [state(200), state(), state(301), state(301), state(301, True)]),
    case([sample(100, 95, 1499), sample(110, 105, 0),
          sample(120, 116, 9999), sample(130, 125, 1501)],
         [state(), state(), state(), state(230)]),
    case([sample(10, 0, 2000), sample(110, 0, 2000),
          sample(111, 107, 2000), sample(112, 107, 2000), sample(212, 200, 2000)],
         [state(110), state(110, True), state(), state(212), state(212, True)]),
    case([sample(5, 2, 101), sample(11, 8, 101), sample(12, 9, 101),
          sample(12, 10, 101), sample(13, 10, 101), sample(20, 17, 100),
          sample(21, 18, 101), sample(28, 25, 101)],
         [state(12), state(12), state(12, True), state(), state(20), state(),
          state(28), state(28, True)], maxpacket=100, target=3, interval=7),
    case([sample(1099511627776, 1099511627771, 1501),
          sample(1099511627875, 1099511627771, 1501),
          sample(1099511627876, 1099511627771, 1501)],
         [state(1099511627876), state(1099511627876), state(1099511627876, True)]),
    case([sample(5, 0, 1501), sample(5, 0, 1501), sample(105, 0, 1501)],
         [state(105), state(105), state(105, True)]),
    case([sample(10, 0, 2000), sample(1000, 990, 2000), sample(1001, None, 0)],
         [state(110), state(110, True), state()]),
    case([sample(20, 15, 1501)], [state(120)]),
    case([sample(4294967296, 0, 1501), sample(4294967396, 0, 1501)],
         [state(4294967396), state(4294967396, True)]),
]
LAW_CASES = [
    ((500, 4), 550.0),
    ((0, 1, 100), 100.0), ((500, 4, 100), 550.0),
    ((500, 1, 100), 600.0), ((600, 4, 100), 650.0),
    ((0, 16, 100), 25.0), ((12, 9, 90), 42.0),
    ((500, 2, 100), 570.7106781186548), ((7, 100, 30), 10.0),
    ((200, 25, 5), 201.0), ((1, 4, 1), 1.5),
    ((0, 1000000, 100), 0.1),
]
EXPECTED_VALUES = [value for _, value in CASES]


def run(candidate):
    payload = base64.b64encode(json.dumps([CASES, LAW_CASES]).encode()).decode()
    runner = r'''import base64, copy, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
cases, laws = json.loads(base64.b64decode(sys.argv[2]))
values, unchanged = [], True
for kwargs, _ in cases:
    supplied = copy.deepcopy(kwargs)
    values.append(module.codel_eligibility(**supplied))
    unchanged = unchanged and supplied == kwargs
law_values = [module.control_law(*args) for args, _ in laws]
print("__RESULT__" + json.dumps({"values": values, "laws": law_values,
                                "unchanged": unchanged}))'''
    try:
        process = subprocess.run(
            [sys.executable, "-B", "-c", runner,
             str(pathlib.Path(candidate).resolve()), payload],
            capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if process.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


def passes(result):
    if (not isinstance(result, dict) or set(result) != {"values", "laws", "unchanged"}
            or result["unchanged"] is not True or result["values"] != EXPECTED_VALUES):
        return False
    if not all(type(s["first_above_time"]) is int and type(s["eligible"]) is bool
               for trace in result["values"] for s in trace):
        return False
    return (isinstance(result["laws"], list) and len(result["laws"]) == len(LAW_CASES)
            and all(type(actual) in (int, float) and math.isfinite(actual)
                    and math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12)
                    for actual, (_, expected) in zip(result["laws"], LAW_CASES)))


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and passes(run(sys.argv[1])) else 1)
