import base64
import json
import pathlib
import subprocess
import sys

EVENTS = [
    {"type": "receive", "path": "old", "bytes": 100},
    {"type": "send", "path": "old", "bytes": 300},
    {"type": "send", "path": "old", "bytes": 1},
    {"type": "receive", "path": "old", "bytes": 5},
    {"type": "send", "path": "old", "bytes": 15},
    {"type": "send", "path": "old", "bytes": 1},
    {"type": "receive", "path": "new", "bytes": 10},
    {"type": "cid", "path": "new"},
    {"type": "ack", "path": "new"},
    {"type": "send", "path": "new", "bytes": 30},
    {"type": "send", "path": "new", "bytes": 1},
    {"type": "challenge", "path": "new", "token": "tok-one"},
    {"type": "challenge", "path": "new", "token": "tok-two"},
    {"type": "response", "path": "old", "challenged": "new", "token": "wrong"},
    {"type": "response", "path": "old", "challenged": "new", "token": "tok-one"},
    {"type": "send", "path": "new", "bytes": 100},
    {"type": "receive", "path": "other", "bytes": 20},
    {"type": "send", "path": "other", "bytes": 60},
    {"type": "send", "path": "other", "bytes": 1},
]

def s(rec, sent, valid, accepted=True, error=None):
    return {"accepted": accepted, "error": error, "received": rec, "sent": sent, "validated": valid}

EXPECTED = [
    s({"old": 100}, {}, []), s({"old": 100}, {"old": 300}, []), s({"old": 100}, {"old": 300}, [], False, "amplification"),
    s({"old": 105}, {"old": 300}, []), s({"old": 105}, {"old": 315}, []),
    s({"old": 105}, {"old": 315}, [], False, "amplification"),
    s({"new": 10, "old": 105}, {"old": 315}, []), s({"new": 10, "old": 105}, {"old": 315}, []),
    s({"new": 10, "old": 105}, {"old": 315}, []),
    s({"new": 10, "old": 105}, {"new": 30, "old": 315}, []), s({"new": 10, "old": 105}, {"new": 30, "old": 315}, [], False, "amplification"),
    s({"new": 10, "old": 105}, {"new": 30, "old": 315}, []), s({"new": 10, "old": 105}, {"new": 30, "old": 315}, []),
    s({"new": 10, "old": 105}, {"new": 30, "old": 315}, []), s({"new": 10, "old": 105}, {"new": 30, "old": 315}, ["new"]),
    s({"new": 10, "old": 105}, {"new": 130, "old": 315}, ["new"]), s({"new": 10, "old": 105, "other": 20}, {"new": 130, "old": 315}, ["new"]),
    s({"new": 10, "old": 105, "other": 20}, {"new": 130, "old": 315, "other": 60}, ["new"]),
    s({"new": 10, "old": 105, "other": 20}, {"new": 130, "old": 315, "other": 60}, ["new"], False, "amplification"),
]

def run(candidate):
    payload = base64.b64encode(json.dumps(EVENTS).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
sys.modules["candidate"] = mod
spec.loader.exec_module(mod)
events = json.loads(base64.b64decode(sys.argv[2]))
print("__RESULT__" + json.dumps(mod.path_budget_trace(events, 3), separators=(",", ":")))'''
    try:
        p = subprocess.run([sys.executable, "-c", runner, str(pathlib.Path(candidate).resolve()), payload], capture_output=True, text=True, timeout=5)
        lines = [x[len("__RESULT__"):] for x in p.stdout.splitlines() if x.startswith("__RESULT__")]
        return json.loads(lines[-1]) if p.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError, json.JSONDecodeError):
        return None

if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) == EXPECTED else 1)
