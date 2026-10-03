import base64
import json
import pathlib
import subprocess
import sys

EVENTS = [
    {"type": "data", "stream": 0, "start": 3, "end": 7},
    {"type": "fin", "stream": 0, "final_size": 10},
    {"type": "fin", "stream": 0, "final_size": 10},
    {"type": "data", "stream": 0, "start": 0, "end": 3},
    {"type": "data", "stream": 0, "start": 7, "end": 10},
    {"type": "fin", "stream": 0, "final_size": 9},
    {"type": "data", "stream": 0, "start": 10, "end": 11},
    {"type": "reset", "stream": 0, "final_size": 10},
    {"type": "data", "stream": 4, "start": 0, "end": 4},
    {"type": "fin", "stream": 4, "final_size": 8},
    {"type": "reset", "stream": 4, "final_size": 8},
    {"type": "data", "stream": 4, "start": 4, "end": 8},
    {"type": "reset", "stream": 4, "final_size": 8},
    {"type": "data", "stream": 4, "start": 8, "end": 9},
    {"type": "data", "stream": 8, "start": 0, "end": 3},
    {"type": "data", "stream": 8, "start": 0, "end": 3},
    {"type": "fin", "stream": 0, "final_size": 10},
    {"type": "data", "stream": 8, "start": 3, "end": 5},
    {"type": "data", "stream": 12, "start": 0, "end": 4},
    {"type": "reset", "stream": 4, "final_size": 9},
]

def state(used, streams, accepted=True, error=None):
    return {"accepted": accepted, "error": error, "connection_used": used, "streams": streams}
def s0(high, delivered, final=None, kind=None):
    return {"highest": high, "delivered": delivered, "final_size": final, "final_kind": kind}
def s4(high, delivered, final=None, kind=None):
    return {"highest": high, "delivered": delivered, "final_size": final, "final_kind": kind}

EXPECTED = [
    state(7, {"0": s0(7, 0)}),
    state(10, {"0": s0(10, 0, 10, "fin")}),
    state(10, {"0": s0(10, 0, 10, "fin")}),
    state(10, {"0": s0(10, 7, 10, "fin")}),
    state(10, {"0": s0(10, 10, 10, "fin")}),
    state(10, {"0": s0(10, 10, 10, "fin")}, False, "final-size"),
    state(10, {"0": s0(10, 10, 10, "fin")}, False, "final-size"),
    state(10, {"0": s0(10, 10, 10, "reset")}),
    state(14, {"0": s0(10, 10, 10, "reset"), "4": s4(4, 4)}),
    state(18, {"0": s0(10, 10, 10, "reset"), "4": s4(8, 4, 8, "fin")}),
    state(18, {"0": s0(10, 10, 10, "reset"), "4": s4(8, 4, 8, "reset")}),
    state(18, {"0": s0(10, 10, 10, "reset"), "4": s4(8, 4, 8, "reset")}),
    state(18, {"0": s0(10, 10, 10, "reset"), "4": s4(8, 4, 8, "reset")}),
    state(18, {"0": s0(10, 10, 10, "reset"), "4": s4(8, 4, 8, "reset")}, False, "final-size"),
    state(21, {"0": s0(10, 10, 10, "reset"), "4": s4(8, 4, 8, "reset"), "8": s4(3, 3)}),
    state(21, {"0": s0(10, 10, 10, "reset"), "4": s4(8, 4, 8, "reset"), "8": s4(3, 3)}),
    state(21, {"0": s0(10, 10, 10, "reset"), "4": s4(8, 4, 8, "reset"), "8": s4(3, 3)}),
    state(21, {"0": s0(10, 10, 10, "reset"), "4": s4(8, 4, 8, "reset"), "8": s4(3, 3)}, False, "flow-control"),
    state(21, {"0": s0(10, 10, 10, "reset"), "4": s4(8, 4, 8, "reset"), "8": s4(3, 3)}, False, "flow-control"),
    state(21, {"0": s0(10, 10, 10, "reset"), "4": s4(8, 4, 8, "reset"), "8": s4(3, 3)}, False, "final-size"),
]

def run(candidate):
    payload = base64.b64encode(json.dumps(EVENTS).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
sys.modules["candidate"] = mod
spec.loader.exec_module(mod)
events = json.loads(base64.b64decode(sys.argv[2]))
print("__RESULT__" + json.dumps(mod.stream_credit_trace(events, 22, {0: 10, 4: 8, 8: 20, 12: 2}), separators=(",", ":")))'''
    try:
        p = subprocess.run([sys.executable, "-c", runner, str(pathlib.Path(candidate).resolve()), payload], capture_output=True, text=True, timeout=5)
        lines = [x[len("__RESULT__"):] for x in p.stdout.splitlines() if x.startswith("__RESULT__")]
        return json.loads(lines[-1]) if p.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError, json.JSONDecodeError):
        return None

if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) == EXPECTED else 1)
