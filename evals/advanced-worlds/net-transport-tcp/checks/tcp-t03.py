import base64
import json
import pathlib
import subprocess
import sys

EVENTS = [
    {"type": "send", "start": 0, "end": 5},
    {"type": "send", "start": 5, "end": 10},
    {"type": "send", "start": 10, "end": 15},
    {"type": "send", "start": 15, "end": 21},
    {"type": "receive", "start": 5, "end": 10},
    {"type": "receive", "start": 5, "end": 10},
    {"type": "renege", "start": 7, "end": 9},
    {"type": "renege", "start": 5, "end": 7},
    {"type": "renege", "start": 9, "end": 10},
    {"type": "receive", "start": 0, "end": 5},
    {"type": "ack", "cumulative": 5},
    {"type": "receive", "start": 15, "end": 20},
    {"type": "receive", "start": 15, "end": 21},
    {"type": "receive", "start": 20, "end": 21},
    {"type": "receive", "start": 5, "end": 10},
    {"type": "receive", "start": 10, "end": 15},
    {"type": "ack", "cumulative": 20},
    {"type": "ack", "cumulative": 21},
]

EXPECTED = [
    {"cumulative_ack": 0, "delivered": 0, "sack_blocks": [], "retained": [[0, 5]]},
    {"cumulative_ack": 0, "delivered": 0, "sack_blocks": [], "retained": [[0, 10]]},
    {"cumulative_ack": 0, "delivered": 0, "sack_blocks": [], "retained": [[0, 15]]},
    {"cumulative_ack": 0, "delivered": 0, "sack_blocks": [], "retained": [[0, 21]]},
    {"cumulative_ack": 0, "delivered": 0, "sack_blocks": [[5, 10]], "retained": [[0, 21]]},
    {"cumulative_ack": 0, "delivered": 0, "sack_blocks": [[5, 10]], "retained": [[0, 21]]},
    {"cumulative_ack": 0, "delivered": 0, "sack_blocks": [[5, 7], [9, 10]], "retained": [[0, 21]]},
    {"cumulative_ack": 0, "delivered": 0, "sack_blocks": [[9, 10]], "retained": [[0, 21]]},
    {"cumulative_ack": 0, "delivered": 0, "sack_blocks": [], "retained": [[0, 21]]},
    {"cumulative_ack": 5, "delivered": 5, "sack_blocks": [], "retained": [[0, 21]]},
    {"cumulative_ack": 5, "delivered": 5, "sack_blocks": [], "retained": [[5, 21]]},
    {"cumulative_ack": 5, "delivered": 5, "sack_blocks": [[15, 20]], "retained": [[5, 21]]},
    {"cumulative_ack": 5, "delivered": 5, "sack_blocks": [[15, 21]], "retained": [[5, 21]]},
    {"cumulative_ack": 5, "delivered": 5, "sack_blocks": [[15, 21]], "retained": [[5, 21]]},
    {"cumulative_ack": 10, "delivered": 10, "sack_blocks": [[15, 21]], "retained": [[5, 21]]},
    {"cumulative_ack": 21, "delivered": 21, "sack_blocks": [], "retained": [[5, 21]]},
    {"cumulative_ack": 21, "delivered": 21, "sack_blocks": [], "retained": [[20, 21]]},
    {"cumulative_ack": 21, "delivered": 21, "sack_blocks": [], "retained": []},
]

def run(candidate):
    payload = base64.b64encode(json.dumps(EVENTS).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
events = json.loads(base64.b64decode(sys.argv[2]))
print("__RESULT__" + json.dumps(mod.reassembly_trace(events), separators=(",", ":")))'''
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
