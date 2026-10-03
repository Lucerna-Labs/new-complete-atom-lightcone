import base64
import json
import pathlib
import subprocess
import sys


def expected(valid, preferred, valid_until, preferred_until, state):
    return {"valid_remaining": valid, "preferred_remaining": preferred,
            "valid_until": valid_until, "preferred_until": preferred_until,
            "state": state}


# Inputs: now, R, V, P, and optionally authenticated. All answers are hand-derived.
CASES = [
    # First branch is OR, and precedes the remaining-lifetime branch.
    ([100, 10000, 8000, 7000], {}, expected(8000, 7000, 8100, 7100, "preferred")),
    ([100, 1000, 2000, 1500], {}, expected(2000, 1500, 2100, 1600, "preferred")),
    ([100, 1000, 7200, 7000], {}, expected(7200, 7000, 7300, 7100, "preferred")),
    ([100, 10000, 10001, 1], {}, expected(10001, 1, 10101, 101, "preferred")),
    # Remaining exactly two hours takes branch two, including its auth exception.
    ([100, 7200, 1800, 0], {}, expected(7200, 0, 7300, 100, "deprecated")),
    ([100, 7200, 1800, 0, True], {}, expected(1800, 0, 1900, 100, "deprecated")),
    ([100, 7199, 1800, 1200], {}, expected(7199, 1200, 7299, 1300, "preferred")),
    ([100, 7199, 1800, 1200], {"authenticated": True}, expected(1800, 1200, 1900, 1300, "preferred")),
    # Above two hours takes branch three even for an authenticated RA.
    ([100, 7201, 1800, 1200], {}, expected(7200, 1200, 7300, 1300, "preferred")),
    ([100, 7201, 1800, 1200, True], {}, expected(7200, 1200, 7300, 1300, "preferred")),
    ([100, 10000, 0, 0, True], {}, expected(7200, 0, 7300, 100, "deprecated")),
    ([100, 10000, 0, 0], {}, expected(7200, 0, 7300, 100, "deprecated")),
    # Preferred lifetime updates even when the valid-lifetime reduction is ignored.
    ([100, 5400, 1800, 0], {}, expected(5400, 0, 5500, 100, "deprecated")),
    ([100, 5400, 0, 0], {}, expected(5400, 0, 5500, 100, "deprecated")),
    ([100, 5400, 0, 0, True], {}, expected(0, 0, 100, 100, "invalid")),
    ([100, 5400, 1800, 0, True], {}, expected(1800, 0, 1900, 100, "deprecated")),
    # Equality and absolute-deadline arithmetic, including now=0.
    ([100, 10000, 7200, 7200], {}, expected(7200, 7200, 7300, 7300, "preferred")),
    ([100, 1000, 1000, 1000], {}, expected(1000, 1000, 1100, 1100, "preferred")),
    ([0, 10000, 0, 0, True], {}, expected(7200, 0, 7200, 0, "deprecated")),
    ([100000, 5400, 1800, 0], {}, expected(5400, 0, 105400, 100000, "deprecated")),
    ([100, 1000, 2000, 1500], {}, expected(2000, 1500, 2100, 1600, "preferred")),
]


def run(candidate):
    payload = base64.b64encode(json.dumps(CASES).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
cases = json.loads(base64.b64decode(sys.argv[2]))
values = [module.slaac_update(*args, **kwargs) for args, kwargs, _ in cases]
print("__RESULT__" + json.dumps(values))'''
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
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) == [c[2] for c in CASES] else 1)
