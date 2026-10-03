import base64
import json
import pathlib
import subprocess
import sys


# One packet is available. Zero PRECHECK deficit is excluded by the contract;
# zero as a result of sending or replenishing is deliberately covered.
CASES = [
    ((400, 1500, 600), {"action": "send", "deficit": -200, "sent_bytes": 600, "move_old": False}),
    ((600, 1500, 600), {"action": "send", "deficit": 0, "sent_bytes": 600, "move_old": False}),
    ((2000, 1500, 500), {"action": "send", "deficit": 1500, "sent_bytes": 500, "move_old": False}),
    ((1, 1500, 1500), {"action": "send", "deficit": -1499, "sent_bytes": 1500, "move_old": False}),
    ((-200, 1500, 600), {"action": "rotate", "deficit": 1300, "sent_bytes": 0, "move_old": True}),
    ((-2000, 1500, 600), {"action": "rotate", "deficit": -500, "sent_bytes": 0, "move_old": True}),
    ((-1500, 1500, 600), {"action": "rotate", "deficit": 0, "sent_bytes": 0, "move_old": True}),
    ((-1, 1, 999), {"action": "rotate", "deficit": 0, "sent_bytes": 0, "move_old": True}),
    ((1, 1, 1000000), {"action": "send", "deficit": -999999, "sent_bytes": 1000000, "move_old": False}),
    ((-999999999, 1000000, 1), {"action": "rotate", "deficit": -998999999, "sent_bytes": 0, "move_old": True}),
    ((1000000000, 1, 1000000), {"action": "send", "deficit": 999000000, "sent_bytes": 1000000, "move_old": False}),
    ((17, 100, 5), {"action": "send", "deficit": 12, "sent_bytes": 5, "move_old": False}),
    ((17, 1, 5), {"action": "send", "deficit": 12, "sent_bytes": 5, "move_old": False}),
    ((-17, 5, 1), {"action": "rotate", "deficit": -12, "sent_bytes": 0, "move_old": True}),
    ((-17, 5, 1000000), {"action": "rotate", "deficit": -12, "sent_bytes": 0, "move_old": True}),
    ((17, 1000000, 17), {"action": "send", "deficit": 0, "sent_bytes": 17, "move_old": False}),
    ((8000, 100, 1500), {"action": "send", "deficit": 6500, "sent_bytes": 1500, "move_old": False}),
    ((-5, 10, 20), {"action": "rotate", "deficit": 5, "sent_bytes": 0, "move_old": True}),
    ((-5, 2, 20), {"action": "rotate", "deficit": -3, "sent_bytes": 0, "move_old": True}),
    ((10, 3, 11), {"action": "send", "deficit": -1, "sent_bytes": 11, "move_old": False}),
    ((10, 3, 9), {"action": "send", "deficit": 1, "sent_bytes": 9, "move_old": False}),
    ((10, 3, 10), {"action": "send", "deficit": 0, "sent_bytes": 10, "move_old": False}),
    ((-1000000000, 1, 1000000), {"action": "rotate", "deficit": -999999999, "sent_bytes": 0, "move_old": True}),
    ((-999999, 1000000, 1000000), {"action": "rotate", "deficit": 1, "sent_bytes": 0, "move_old": True}),
]
CASES.append(CASES[0])


def run(candidate):
    payload = base64.b64encode(json.dumps([args for args, _ in CASES]).encode()).decode()
    runner = r'''import base64,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
values=[module.deficit_visit(*args) for args in json.loads(base64.b64decode(sys.argv[2]))]
print("__RESULT__"+json.dumps(values))'''
    try:
        result = subprocess.run([sys.executable, "-B", "-c", runner,
                                 str(pathlib.Path(candidate).resolve()), payload],
                                capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in result.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if result.returncode == 0 and lines else None
        return json.dumps(actual, sort_keys=True) == json.dumps([value for _, value in CASES], sort_keys=True)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return False


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
