import base64
import json
import pathlib
import subprocess
import sys


def state(entered=False, pending=None, reports=()):
    return {"entered": entered,
            "pending": (None if pending is None else
                        {"kind": pending[0], "since_ms": pending[1],
                         "deadline_ms": pending[2]}),
            "reports": [{"time_ms": time, "reason": kind} for time, kind in reports]}


def case(samples, expected, **changes):
    config = {"offset_db": 3, "hysteresis_db": 2, "ttt_ms": 40,
              "as_security_active": True, "cell_applicable": True,
              "report_on_leave": True}
    config.update(changes)
    return ({"samples": [{"time_ms": t, "margin_db": d} for t, d in samples],
             "config": config}, expected)


# Literal state transitions under the declared held-input/sample-first tie model.
# There is no event evaluator or timer algorithm in these expected tables.
E40 = ((40, "enter"),)
CASES = [
    case([], []),
    case([(0, 6)], [state(pending=("enter", 0, 40))]),
    case([(0, 5), (40, 5), (100, 5)], [state(), state(), state()]),
    case([(0, 6), (39, 6), (40, 6), (80, 6)],
         [state(pending=("enter", 0, 40)), state(pending=("enter", 0, 40)),
          state(True, reports=E40), state(True, reports=E40)]),
    case([(0, 6), (40, 5), (41, 6), (81, 6)],
         [state(pending=("enter", 0, 40)), state(),
          state(pending=("enter", 41, 81)), state(True, reports=((81, "enter"),))]),
    case([(0, 6), (39, 5), (40, 6), (79, 6), (80, 6)],
         [state(pending=("enter", 0, 40)), state(),
          state(pending=("enter", 40, 80)), state(pending=("enter", 40, 80)),
          state(True, reports=((80, "enter"),))]),
    case([(0, 6), (41, 0), (81, 0)],
         [state(pending=("enter", 0, 40)),
          state(True, ("leave", 41, 81), E40),
          state(reports=((40, "enter"), (81, "leave")))]),
    case([(0, 6), (40, 0)], [state(pending=("enter", 0, 40)), state()]),
    case([(0, 6), (100, 0), (140, 0)],
         [state(pending=("enter", 0, 40)), state(True, ("leave", 100, 140), E40),
          state(reports=((40, "enter"), (140, "leave")))]),
    case([(0, 6), (40, 6), (50, 0), (90, 1), (91, 0), (131, 0)],
         [state(pending=("enter", 0, 40)), state(True, reports=E40),
          state(True, ("leave", 50, 90), E40), state(True, reports=E40),
          state(True, ("leave", 91, 131), E40),
          state(reports=((40, "enter"), (131, "leave")))]),
    case([(0, 6), (1, 1), (2, 0), (3, 5), (4, 6)],
         [state(True, reports=((0, "enter"),)),
          state(True, reports=((0, "enter"),)),
          state(reports=((0, "enter"), (2, "leave"))),
          state(reports=((0, "enter"), (2, "leave"))),
          state(True, reports=((0, "enter"), (2, "leave"), (4, "enter")))], ttt_ms=0),
    case([(0, 6), (10, 0), (20, 6)],
         [state(True, reports=((0, "enter"),)), state(reports=((0, "enter"),)),
          state(True, reports=((0, "enter"), (20, "enter")))],
         ttt_ms=0, report_on_leave=False),
    case([(0, -1), (1, 0), (41, 0), (42, -5), (43, -6), (83, -6)],
         [state(), state(pending=("enter", 1, 41)),
          state(True, reports=((41, "enter"),)),
          state(True, reports=((41, "enter"),)),
          state(True, ("leave", 43, 83), ((41, "enter"),)),
          state(reports=((41, "enter"), (83, "leave")))], offset_db=-3),
    case([(0, 0), (1, 1), (2, 0), (3, -1)],
         [state(), state(True, reports=((1, "enter"),)),
          state(True, reports=((1, "enter"),)),
          state(reports=((1, "enter"), (3, "leave")))],
         offset_db=0, hysteresis_db=0, ttt_ms=0),
    case([(0, 6), (1000, 0), (5000, 6)], [state(), state(), state()],
         as_security_active=False),
    case([(0, 6), (1000, 0), (5000, 6)], [state(), state(), state()],
         cell_applicable=False),
    case([(0, 6), (1000, 0)], [state(), state()],
         as_security_active=False, cell_applicable=False, ttt_ms=0),
    case([(0, 6), (63, 6), (64, 6), (65, 0), (129, 0)],
         [state(pending=("enter", 0, 64)), state(pending=("enter", 0, 64)),
          state(True, reports=((64, "enter"),)),
          state(True, ("leave", 65, 129), ((64, "enter"),)),
          state(reports=((64, "enter"), (129, "leave")))], ttt_ms=64),
    case([(0, 6), (5119, 6), (5120, 6), (6000, 0), (11120, 0)],
         [state(pending=("enter", 0, 5120)), state(pending=("enter", 0, 5120)),
          state(True, reports=((5120, "enter"),)),
          state(True, ("leave", 6000, 11120), ((5120, "enter"),)),
          state(reports=((5120, "enter"), (11120, "leave")))], ttt_ms=5120),
    case([(0, 0), (100000, 6)], [state(), state(pending=("enter", 100000, 100040))]),
    case([(0, 0), (1, 300), (129, 300), (200, -300), (328, -300)],
         [state(), state(pending=("enter", 1, 129)),
          state(True, reports=((129, "enter"),)),
          state(True, ("leave", 200, 328), ((129, "enter"),)),
          state(reports=((129, "enter"), (328, "leave")))],
         offset_db=-15, hysteresis_db=15, ttt_ms=128),
    case([(0, 30), (1, 31), (41, 31), (42, 0), (43, -1), (83, -1)],
         [state(), state(pending=("enter", 1, 41)),
          state(True, reports=((41, "enter"),)),
          state(True, reports=((41, "enter"),)),
          state(True, ("leave", 43, 83), ((41, "enter"),)),
          state(reports=((41, "enter"), (83, "leave")))],
         offset_db=15, hysteresis_db=15),
    case([(0, 1), (1, 1.5), (41, 1.5), (42, 0), (43, -0.5), (83, -0.5)],
         [state(), state(pending=("enter", 1, 41)),
          state(True, reports=((41, "enter"),)),
          state(True, reports=((41, "enter"),)),
          state(True, ("leave", 43, 83), ((41, "enter"),)),
          state(reports=((41, "enter"), (83, "leave")))],
         offset_db=0.5, hysteresis_db=0.5),
    case([(0, 6), (40, 6), (50, 0), (70, 3), (100, 0), (139, 0), (140, 0)],
         [state(pending=("enter", 0, 40)), state(True, reports=E40),
          state(True, ("leave", 50, 90), E40), state(True, reports=E40),
          state(True, ("leave", 100, 140), E40),
          state(True, ("leave", 100, 140), E40),
          state(reports=((40, "enter"), (140, "leave")))]),
    case([(0, 6), (40, 6), (50, 0), (90, 6)],
         [state(pending=("enter", 0, 40)), state(True, reports=E40),
          state(True, ("leave", 50, 90), E40), state(True, reports=E40)]),
    case([(0, 6), (100, 6)],
         [state(pending=("enter", 0, 40)), state(True, reports=E40)]),
    case([(i, 3) for i in range(64)], [state() for _ in range(64)]),
]
CALLS = CASES + [CASES[10], CASES[0], CASES[1], CASES[10]]
EXPECTED = [expected for _, expected in CALLS]


def run(candidate):
    payload = base64.b64encode(json.dumps([args for args, _ in CALLS]).encode()).decode()
    runner = r'''import base64, copy, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
calls = json.loads(base64.b64decode(sys.argv[2]))
values, unchanged = [], True
for args in calls:
    supplied = copy.deepcopy(args)
    values.append(module.a3_trace(**supplied))
    unchanged = unchanged and json.dumps(supplied, sort_keys=True) == json.dumps(args, sort_keys=True)
print("__RESULT__" + json.dumps({"values": values, "unchanged": unchanged}))'''
    try:
        process = subprocess.run([sys.executable, "-B", "-c", runner,
                                  str(pathlib.Path(candidate).resolve()), payload],
                                 capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if process.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


def same(actual, expected):
    if isinstance(expected, dict):
        return (isinstance(actual, dict) and set(actual) == set(expected)
                and all(same(actual[key], value) for key, value in expected.items()))
    if isinstance(expected, list):
        return (isinstance(actual, list) and len(actual) == len(expected)
                and all(same(a, e) for a, e in zip(actual, expected)))
    return type(actual) is type(expected) and actual == expected


def passes(result):
    return (isinstance(result, dict) and set(result) == {"values", "unchanged"}
            and result["unchanged"] is True and same(result["values"], EXPECTED))


if __name__ == "__main__":
    ok = len(sys.argv) == 2 and passes(run(sys.argv[1]))
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
