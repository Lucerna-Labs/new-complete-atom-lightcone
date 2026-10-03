import base64
import json
import pathlib
import subprocess
import sys


def expected(t1_at, t2_at, expires_at, phase, usable):
    return {"t1_at": t1_at, "t2_at": t2_at, "expires_at": expires_at,
            "phase": phase, "usable": usable}


# Fixed expected deadlines and phases are hand-derived independently of the candidate.
CASES = [
    ([100, 107, 80, 107], {}, expected(140, 170, 180, "BOUND", True)),
    ([100, 107, 80, 139.5], {}, expected(140, 170, 180, "BOUND", True)),
    ([100, 107, 80, 140], {}, expected(140, 170, 180, "RENEWING", True)),
    ([100, 107, 80, 169.5], {}, expected(140, 170, 180, "RENEWING", True)),
    ([100, 107, 80, 170], {}, expected(140, 170, 180, "REBINDING", True)),
    ([100, 107, 80, 179.5], {}, expected(140, 170, 180, "REBINDING", True)),
    ([100, 107, 80, 180], {}, expected(140, 170, 180, "INIT", False)),
    ([100, 107, 80, 181], {}, expected(140, 170, 180, "INIT", False)),
    # ACK delay can put the point query beyond renewal, rebinding, or expiry.
    ([100, 150, 80, 150], {}, expected(140, 170, 180, "RENEWING", True)),
    ([100, 175, 80, 175], {}, expected(140, 170, 180, "REBINDING", True)),
    ([100, 180, 80, 180], {}, expected(140, 170, 180, "INIT", False)),
    ([100, 190, 80, 190], {}, expected(140, 170, 180, "INIT", False)),
    # Simultaneous request/ACK does not hide inclusive deadline boundaries.
    ([0, 0, 8, 0], {}, expected(4, 7, 8, "BOUND", True)),
    ([0, 0, 8, 4], {}, expected(4, 7, 8, "RENEWING", True)),
    ([0, 0, 8, 7], {}, expected(4, 7, 8, "REBINDING", True)),
    ([0, 0, 8, 8], {}, expected(4, 7, 8, "INIT", False)),
    # Configured timers are offsets from request time, independently optional.
    ([100, 105, 80, 109], {"t1": 10, "t2": 20}, expected(110, 120, 180, "BOUND", True)),
    ([100, 105, 80, 110], {"t1": 10, "t2": 20}, expected(110, 120, 180, "RENEWING", True)),
    ([100, 105, 80, 120], {"t1": 10, "t2": 20}, expected(110, 120, 180, "REBINDING", True)),
    ([100, 105, 80, 180], {"t1": 10, "t2": 20}, expected(110, 120, 180, "INIT", False)),
    ([100, 105, 80, 120], {"t1": 20}, expected(120, 170, 180, "RENEWING", True)),
    ([100, 105, 80, 160], {"t2": 60}, expected(140, 160, 180, "REBINDING", True)),
    # A new accepted renewal uses its new request epoch, not prior call state.
    ([130, 132, 80, 140], {}, expected(170, 200, 210, "BOUND", True)),
    ([100, 107, 80, 140], {}, expected(140, 170, 180, "RENEWING", True)),
    ([200, 201, 8, 208], {}, expected(204, 207, 208, "INIT", False)),
]


def run(candidate):
    payload = base64.b64encode(json.dumps(CASES).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
cases = json.loads(base64.b64decode(sys.argv[2]))
values = [module.lease_state(*args, **kwargs) for args, kwargs, _ in cases]
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
