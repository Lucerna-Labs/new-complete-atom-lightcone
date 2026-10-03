import base64
import json
import math
import pathlib
import subprocess
import sys
from fractions import Fraction

TRACES = [
    ([], 0.1),
    ([{"type": "sample", "rtt": 2.0, "ambiguous": True},
      {"type": "duplicate_ack"}, {"type": "advance_ack"}], 0.1),
    ([{"type": "sample", "rtt": 1.0, "ambiguous": False},
      {"type": "sample", "rtt": 1.4, "ambiguous": False},
      {"type": "sample", "rtt": 0.6, "ambiguous": False}], 0.1),
    ([{"type": "sample", "rtt": 1.0, "ambiguous": False},
      {"type": "sample", "rtt": 1.0, "ambiguous": False}], 2.0),
    ([{"type": "sample", "rtt": 0.01, "ambiguous": False}], 0.1),
    ([{"type": "sample", "rtt": 100.0, "ambiguous": False}], 0.1),
    ([{"type": "sample", "rtt": 1.0, "ambiguous": False},
      {"type": "timeout"}, {"type": "duplicate_ack"},
      {"type": "advance_ack"}, {"type": "sample", "rtt": 1.2, "ambiguous": False}], 0.1),
    ([{"type": "sample", "rtt": 1.0, "ambiguous": False},
      {"type": "timeout"}, {"type": "timeout"}, {"type": "timeout"},
      {"type": "timeout"}, {"type": "timeout"}, {"type": "timeout"}], 0.1),
]

def snap(srtt, var, rto, used):
    return {"srtt": srtt, "rttvar": var, "rto": rto, "samples_used": used}

EXPECTED = [
    [],
    [snap(None, None, Fraction(1), 0), snap(None, None, Fraction(1), 0), snap(None, None, Fraction(1), 0)],
    [snap(Fraction(1), Fraction(1, 2), Fraction(3), 1),
     snap(Fraction(21, 20), Fraction(19, 40), Fraction(59, 20), 2),
     snap(Fraction(159, 160), Fraction(15, 32), Fraction(459, 160), 3)],
    [snap(Fraction(1), Fraction(1, 2), Fraction(3), 1), snap(Fraction(1), Fraction(3, 8), Fraction(3), 2)],
    [snap(Fraction(1, 100), Fraction(1, 200), Fraction(1), 1)],
    [snap(Fraction(100), Fraction(50), Fraction(60), 1)],
    [snap(Fraction(1), Fraction(1, 2), Fraction(3), 1),
     snap(Fraction(1), Fraction(1, 2), Fraction(6), 1),
     snap(Fraction(1), Fraction(1, 2), Fraction(6), 1),
     snap(Fraction(1), Fraction(1, 2), Fraction(6), 1),
     snap(Fraction(41, 40), Fraction(17, 40), Fraction(109, 40), 2)],
    [snap(Fraction(1), Fraction(1, 2), Fraction(3), 1),
     snap(Fraction(1), Fraction(1, 2), Fraction(6), 1),
     snap(Fraction(1), Fraction(1, 2), Fraction(12), 1),
     snap(Fraction(1), Fraction(1, 2), Fraction(24), 1),
     snap(Fraction(1), Fraction(1, 2), Fraction(48), 1),
     snap(Fraction(1), Fraction(1, 2), Fraction(60), 1),
     snap(Fraction(1), Fraction(1, 2), Fraction(60), 1)],
]

def run(candidate):
    payload = base64.b64encode(json.dumps(TRACES).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
traces = json.loads(base64.b64decode(sys.argv[2]))
result = [mod.rto_trace(events, clock_granularity=g) for events, g in traces]
print("__RESULT__" + json.dumps(result, separators=(",", ":")))'''
    try:
        p = subprocess.run([sys.executable, "-c", runner, str(pathlib.Path(candidate).resolve()), payload],
                           capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in p.stdout.splitlines() if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if p.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError, json.JSONDecodeError):
        return None

def equal_number(got, expected):
    if expected is None:
        return got is None
    return type(got) in (int, float) and math.isfinite(got) and math.isclose(got, float(expected), rel_tol=1e-9, abs_tol=1e-9)

def main(candidate):
    got = run(candidate)
    if not isinstance(got, list) or len(got) != len(EXPECTED):
        return False
    for actual_trace, expected_trace in zip(got, EXPECTED):
        if len(actual_trace) != len(expected_trace):
            return False
        for actual, expected in zip(actual_trace, expected_trace):
            if set(actual) != {"srtt", "rttvar", "rto", "samples_used"}:
                return False
            if type(actual["samples_used"]) is not int or actual["samples_used"] != expected["samples_used"]:
                return False
            if not all(equal_number(actual[k], expected[k]) for k in ("srtt", "rttvar", "rto")):
                return False
    return True

if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and main(sys.argv[1]) else 1)
