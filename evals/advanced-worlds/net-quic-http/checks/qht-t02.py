import base64
import json
import pathlib
import subprocess
import sys

EVENTS = [
    {"type": "insert", "ordinal": 1}, {"type": "insert", "ordinal": 2}, {"type": "insert", "ordinal": 3},
    {"type": "known", "count": 1},
    {"type": "section", "stream": 1, "refs": [1]},
    {"type": "evict", "ordinal": 1},
    {"type": "section", "stream": 2, "refs": [3]},
    {"type": "section", "stream": 3, "refs": [3]},
    {"type": "section", "stream": 1, "refs": [3]},
    {"type": "cancel", "stream": 2},
    {"type": "section", "stream": 1, "refs": [3]},
    {"type": "known", "count": 2},
    {"type": "section_ack", "stream": 1},
    {"type": "section_ack", "stream": 1},
    {"type": "section_ack", "stream": 3},
    {"type": "section", "stream": 4, "refs": [2]},
    {"type": "section_ack", "stream": 4},
    {"type": "evict", "ordinal": 2},
    {"type": "evict", "ordinal": 1},
    {"type": "evict", "ordinal": 2},
    {"type": "insert", "ordinal": 4},
    {"type": "insert", "ordinal": 5},
    {"type": "section", "stream": 5, "refs": [5]},
    {"type": "section_ack", "stream": 5},
]

def state(known, progress, blocked, pending, entries, error=None):
    return {"known_received": known, "insertion_progress": progress, "blocked_streams": blocked,
            "pending_sections": pending, "entries": entries, "error": error}
def entries(*pairs):
    return [{"ordinal": n, "acknowledged": a} for n, a in pairs]

EXPECTED = [
    state(0, 1, [], 0, entries((1, False))), state(0, 2, [], 0, entries((1, False), (2, False))),
    state(0, 3, [], 0, entries((1, False), (2, False), (3, False))),
    state(1, 3, [], 0, entries((1, True), (2, False), (3, False))),
    state(1, 3, [], 1, entries((1, True), (2, False), (3, False))),
    state(1, 3, [], 1, entries((1, True), (2, False), (3, False)), "eviction"),
    state(1, 3, [2], 2, entries((1, True), (2, False), (3, False))),
    state(1, 3, [2, 3], 3, entries((1, True), (2, False), (3, False))),
    state(1, 3, [2, 3], 3, entries((1, True), (2, False), (3, False)), "blocked-limit"),
    state(1, 3, [3], 2, entries((1, True), (2, False), (3, False))),
    state(1, 3, [1, 3], 3, entries((1, True), (2, False), (3, False))),
    state(2, 3, [1, 3], 3, entries((1, True), (2, True), (3, False))),
    state(2, 3, [1, 3], 2, entries((1, True), (2, True), (3, False))),
    state(3, 3, [], 1, entries((1, True), (2, True), (3, True))),
    state(3, 3, [], 0, entries((1, True), (2, True), (3, True))),
    state(3, 3, [], 1, entries((1, True), (2, True), (3, True))),
    state(3, 3, [], 0, entries((1, True), (2, True), (3, True))),
    state(3, 3, [], 0, entries((1, True), (2, True), (3, True)), "eviction"),
    state(3, 3, [], 0, entries((2, True), (3, True))), state(3, 3, [], 0, entries((3, True))),
    state(3, 4, [], 0, entries((3, True), (4, False))),
    state(3, 5, [], 0, entries((3, True), (4, False), (5, False))),
    state(3, 5, [5], 1, entries((3, True), (4, False), (5, False))),
    state(5, 5, [], 0, entries((3, True), (4, True), (5, True))),
]

def run(candidate):
    payload = base64.b64encode(json.dumps(EVENTS).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
sys.modules["candidate"] = mod
spec.loader.exec_module(mod)
events = json.loads(base64.b64decode(sys.argv[2]))
print("__RESULT__" + json.dumps(mod.qpack_trace(events, 2), separators=(",", ":")))'''
    try:
        p = subprocess.run([sys.executable, "-c", runner, str(pathlib.Path(candidate).resolve()), payload], capture_output=True, text=True, timeout=5)
        lines = [x[len("__RESULT__"):] for x in p.stdout.splitlines() if x.startswith("__RESULT__")]
        return json.loads(lines[-1]) if p.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError, json.JSONDecodeError):
        return None

if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) == EXPECTED else 1)
