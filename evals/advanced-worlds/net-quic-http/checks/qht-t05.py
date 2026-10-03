import base64
import json
import pathlib
import subprocess
import sys

EVENTS = [
    {"type": "request", "early_data": True, "resource_replayable": False},
    {"type": "quic_retry"},
    {"type": "http_425_retry"},
    {"type": "request", "early_data": False, "resource_replayable": False},
    {"type": "intermediary", "own_handshake_confirmed": True, "resource_replayable": False},
    {"type": "request", "early_data": True, "resource_replayable": True},
    {"type": "intermediary", "own_handshake_confirmed": True, "resource_replayable": True},
    {"type": "intermediary", "own_handshake_confirmed": True, "resource_replayable": False},
    {"type": "http_425_retry"},
    {"type": "request", "early_data": False, "resource_replayable": False},
]
EXPECTED = [
    {"kind": "http-response", "early": True, "decision": "425"},
    {"kind": "quic-retry", "early": True, "decision": "transport-retry"},
    {"kind": "request", "early": False, "decision": "forward-1rtt"},
    {"kind": "request", "early": False, "decision": "forward-1rtt"},
    {"kind": "request", "early": False, "decision": "forward-1rtt"},
    {"kind": "request", "early": True, "decision": "forward-early"},
    {"kind": "request", "early": True, "decision": "forward-early"},
    {"kind": "http-response", "early": True, "decision": "425"},
    {"kind": "request", "early": False, "decision": "forward-1rtt"},
    {"kind": "request", "early": False, "decision": "forward-1rtt"},
]

def run(candidate):
    payload = base64.b64encode(json.dumps(EVENTS).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
sys.modules["candidate"] = mod
spec.loader.exec_module(mod)
events = json.loads(base64.b64decode(sys.argv[2]))
print("__RESULT__" + json.dumps(mod.early_data_trace(events), separators=(",", ":")))'''
    try:
        p = subprocess.run([sys.executable, "-c", runner, str(pathlib.Path(candidate).resolve()), payload], capture_output=True, text=True, timeout=5)
        lines = [x[len("__RESULT__"):] for x in p.stdout.splitlines() if x.startswith("__RESULT__")]
        return json.loads(lines[-1]) if p.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError, json.JSONDecodeError):
        return None

if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) == EXPECTED else 1)
