import base64
import json
import math
import pathlib
import subprocess
import sys

EVENTS = [
    {"type": "advance", "seconds": 2.0, "application_limited": False},
    {"type": "advance", "seconds": 5.0, "application_limited": True},
    {"type": "ack", "wmax": 100.0, "cwnd_epoch": 70.0, "cwnd": 90.0,
     "rtt": 1.0, "reno_estimate": 90.0},
    {"type": "ack", "wmax": 100.0, "cwnd_epoch": 70.0, "cwnd": 90.0,
     "rtt": 1.0, "reno_estimate": 97.0},
    {"type": "advance", "seconds": 1.0, "application_limited": False},
    {"type": "ack", "wmax": 100.0, "cwnd_epoch": 0.0, "cwnd": 100.0,
     "rtt": 0.1, "reno_estimate": 0.0},
    {"type": "ack", "wmax": 100.0, "cwnd_epoch": 0.0, "cwnd": 50.0,
     "rtt": 20.0, "reno_estimate": 0.0},
    {"type": "ack", "wmax": 120.0, "cwnd_epoch": 90.0, "cwnd": 100.0,
     "rtt": 0.5, "reno_estimate": 160.0},
    {"type": "packet_loss", "flight_size": 50.0},
    {"type": "rto", "flight_size": 50.0},
    {"type": "packet_loss", "flight_size": 1.0},
    {"type": "rto", "flight_size": 1.0},
]

def run(candidate):
    payload = base64.b64encode(json.dumps(EVENTS).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
events = json.loads(base64.b64decode(sys.argv[2]))
print("__RESULT__" + json.dumps(mod.cubic_trace(events, C=0.4), separators=(",", ":")))'''
    try:
        p = subprocess.run([sys.executable, "-c", runner, str(pathlib.Path(candidate).resolve()), payload],
                           capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in p.stdout.splitlines() if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if p.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError, json.JSONDecodeError):
        return None

def close(a, b):
    return type(a) in (int, float) and math.isfinite(a) and math.isclose(a, float(b), rel_tol=1e-8, abs_tol=1e-8)

def check_ack(actual, wmax, epoch, cwnd, rtt, reno, t, branch, target):
    if set(actual) != {"time", "k", "current_cubic", "raw_cubic", "cubic_target", "target", "branch"}:
        return False
    k = ((wmax - epoch) / 0.4) ** (1 / 3)
    current = 0.4 * (t - k) ** 3 + wmax
    raw = 0.4 * (t + rtt - k) ** 3 + wmax
    cubic_target = max(cwnd, min(1.5 * cwnd, raw))
    return (close(actual["time"], t) and close(actual["k"], k) and
            close(actual["current_cubic"], current) and close(actual["raw_cubic"], raw) and
            close(actual["cubic_target"], cubic_target) and close(actual["target"], target) and
            actual["branch"] == branch)

def main(candidate):
    got = run(candidate)
    if not isinstance(got, list) or len(got) != len(EVENTS):
        return False
    if set(got[0]) != {"time", "application_limited"} or got[0] != {"time": 2.0, "application_limited": False}:
        return False
    if got[1] != {"time": 2.0, "application_limited": True}:
        return False
    k0 = ((100.0 - 70.0) / 0.4) ** (1 / 3)
    raw0 = 0.4 * (3.0 - k0) ** 3 + 100.0
    if not check_ack(got[2], 100.0, 70.0, 90.0, 1.0, 90.0, 2.0, "cubic", max(90.0, min(135.0, raw0))):
        return False
    k = ((100.0 - 70.0) / 0.4) ** (1 / 3)
    current = 0.4 * (2.0 - k) ** 3 + 100.0
    raw = 0.4 * (3.0 - k) ** 3 + 100.0
    clamped = max(90.0, min(135.0, raw))
    if not (current < 97.0 < clamped):
        return False
    if not check_ack(got[3], 100.0, 70.0, 90.0, 1.0, 97.0, 2.0, "reno-friendly", 97.0):
        return False
    if got[4] != {"time": 3.0, "application_limited": False}:
        return False
    kl = ((100.0 - 0.0) / 0.4) ** (1 / 3)
    raw_low = 0.4 * (3.0 + 0.1 - kl) ** 3 + 100.0
    if not (raw_low < 100.0):
        return False
    if not check_ack(got[5], 100.0, 0.0, 100.0, 0.1, 0.0, 3.0, "cubic", 100.0):
        return False
    raw_high = 0.4 * (3.0 + 20.0 - kl) ** 3 + 100.0
    if not (raw_high > 1.5 * 50.0):
        return False
    if not check_ack(got[6], 100.0, 0.0, 50.0, 20.0, 0.0, 3.0, "cubic", 75.0):
        return False
    if not check_ack(got[7], 120.0, 90.0, 100.0, 0.5, 160.0, 3.0, "reno-friendly", 160.0):
        return False
    if got[8] != {"event": "packet_loss", "ssthresh": 35.0, "cwnd": 35.0}:
        return False
    if got[9] != {"event": "rto", "ssthresh": 35.0, "cwnd": 1.0}:
        return False
    if got[10] != {"event": "packet_loss", "ssthresh": 2.0, "cwnd": 2.0}:
        return False
    if got[11] != {"event": "rto", "ssthresh": 2.0, "cwnd": 1.0}:
        return False
    return True

if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and main(sys.argv[1]) else 1)
