import base64
import json
import pathlib
import subprocess
import sys

EVENTS_ENABLED = [
    {"type": "write", "bytes": 400},
    {"type": "write", "bytes": 300},
    {"type": "push"},
    {"type": "ack", "bytes": 0},
    {"type": "ack", "bytes": 400},
    {"type": "write", "bytes": 1000},
    {"type": "write", "bytes": 100},
    {"type": "write", "bytes": 1000},
    {"type": "push"},
    {"type": "disable"},
    {"type": "write", "bytes": 100},
    {"type": "ack", "bytes": 500},
]
EXPECTED_ENABLED = [
    {"tx": [400], "pending": 0, "outstanding": 400, "acks_sent": 0},
    {"tx": [], "pending": 300, "outstanding": 400, "acks_sent": 0},
    {"tx": [], "pending": 300, "outstanding": 400, "acks_sent": 0},
    {"tx": [], "pending": 300, "outstanding": 400, "acks_sent": 0},
    {"tx": [300], "pending": 0, "outstanding": 300, "acks_sent": 0},
    {"tx": [1000], "pending": 0, "outstanding": 1300, "acks_sent": 0},
    {"tx": [], "pending": 100, "outstanding": 1300, "acks_sent": 0},
    {"tx": [1000], "pending": 100, "outstanding": 2300, "acks_sent": 0},
    {"tx": [], "pending": 100, "outstanding": 2300, "acks_sent": 0},
    {"tx": [100], "pending": 0, "outstanding": 2400, "acks_sent": 0},
    {"tx": [100], "pending": 0, "outstanding": 2500, "acks_sent": 0},
    {"tx": [], "pending": 0, "outstanding": 2000, "acks_sent": 0},
]

EVENTS_BOUNDARY = [
    {"type": "write", "bytes": 999},
    {"type": "write", "bytes": 1000},
    {"type": "write", "bytes": 1},
    {"type": "push"},
    {"type": "ack", "bytes": 999},
    {"type": "ack", "bytes": 1000},
]
EXPECTED_BOUNDARY = [
    {"tx": [999], "pending": 0, "outstanding": 999, "acks_sent": 0},
    {"tx": [1000], "pending": 0, "outstanding": 1999, "acks_sent": 0},
    {"tx": [], "pending": 1, "outstanding": 1999, "acks_sent": 0},
    {"tx": [], "pending": 1, "outstanding": 1999, "acks_sent": 0},
    {"tx": [], "pending": 1, "outstanding": 1000, "acks_sent": 0},
    {"tx": [1], "pending": 0, "outstanding": 1, "acks_sent": 0},
]

EVENTS_DISABLED = [
    {"type": "write", "bytes": 511},
    {"type": "write", "bytes": 1},
    {"type": "ack", "bytes": 512},
    {"type": "write", "bytes": 512},
    {"type": "write", "bytes": 511},
]
EXPECTED_DISABLED = [
    {"tx": [511], "pending": 0, "outstanding": 511, "acks_sent": 0},
    {"tx": [1], "pending": 0, "outstanding": 512, "acks_sent": 0},
    {"tx": [], "pending": 0, "outstanding": 0, "acks_sent": 0},
    {"tx": [512], "pending": 0, "outstanding": 512, "acks_sent": 0},
    {"tx": [511], "pending": 0, "outstanding": 1023, "acks_sent": 0},
]

CASES = [(EVENTS_ENABLED, 1000, True), (EVENTS_BOUNDARY, 1000, True), (EVENTS_DISABLED, 512, False)]
EXPECTED = [EXPECTED_ENABLED, EXPECTED_BOUNDARY, EXPECTED_DISABLED]

def run(candidate):
    payload = base64.b64encode(json.dumps(CASES).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
cases = json.loads(base64.b64decode(sys.argv[2]))
result = [mod.nagle_trace(events, mss=mss, nagle_enabled=enabled) for events, mss, enabled in cases]
print("__RESULT__" + json.dumps(result, separators=(",", ":")))'''
    try:
        p = subprocess.run([sys.executable, "-c", runner, str(pathlib.Path(candidate).resolve()), payload],
                           capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in p.stdout.splitlines() if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if p.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError, json.JSONDecodeError):
        return None

if __name__ == "__main__":
    ok = len(sys.argv) == 2 and run(sys.argv[1]) == EXPECTED
    sys.exit(0 if ok else 1)
