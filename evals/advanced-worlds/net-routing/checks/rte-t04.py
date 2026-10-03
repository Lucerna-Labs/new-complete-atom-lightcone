import base64
import json
import pathlib
import subprocess
import sys


def feedback(family, path, mtu, validated=True, applicable=True):
    return {"type": "ipv4_feedback" if family == 4 else "ipv6_feedback",
            "path": path, "mtu": mtu, "validated": validated, "applicable": applicable}


def state(a, b=None, sent=None):
    cache = {"A": a}
    if b is not None:
        cache["B"] = b
    return {"cache": cache, "sent_size": sent}


EVENTS = [
    {"type": "init", "path": "A", "family": 4, "mtu": 1500},
    {"type": "init", "path": "B", "family": 6, "mtu": 1500},
    {"type": "send", "path": "A", "want": 1600},
    feedback(4, "A", 1400, validated=False),
    feedback(4, "A", 1400, applicable=False),
    feedback(6, "A", 1400),
    feedback(4, "A", 1400),
    feedback(4, "A", 1450),
    {"type": "send", "path": "A", "want": 1450},
    {"type": "send", "path": "A", "want": 1000},
    {"type": "unrelated_feedback", "path": "A", "mtu": 1300,
     "validated": True, "applicable": True},
    feedback(4, "B", 1300),
    feedback(6, "B", 1400, validated=False),
    feedback(6, "B", 1400, applicable=False),
    feedback(6, "B", 1400),
    feedback(6, "B", 1279),
    feedback(6, "B", 1280),
    feedback(6, "B", 1300),
    {"type": "send", "path": "B", "want": 1450},
    feedback(4, "A", 67),
    feedback(4, "A", 0),
    feedback(4, "A", 68),
    {"type": "send", "path": "A", "want": 1500},
    feedback(4, "A", 70),
    {"type": "send", "path": "B", "want": 1300},
]

# Hand-computed states keep A's IPv4 feedback isolated from B's IPv6 cache.
EXPECTED = [
    state(1500), state(1500, 1500), state(1500, 1500, 1500),
    state(1500, 1500), state(1500, 1500), state(1500, 1500),
    state(1400, 1500), state(1400, 1500), state(1400, 1500, 1400),
    state(1400, 1500, 1000), state(1400, 1500), state(1400, 1500),
    state(1400, 1500),
    state(1400, 1500), state(1400, 1400), state(1400, 1400),
    state(1400, 1280), state(1400, 1280), state(1400, 1280, 1280),
    state(1400, 1280), state(1400, 1280), state(68, 1280),
    state(68, 1280, 68), state(68, 1280),
    state(68, 1280, 1280),
]


def run(candidate):
    payload = base64.b64encode(json.dumps(EVENTS).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
events = json.loads(base64.b64decode(sys.argv[2]))
print("__RESULT__" + json.dumps(module.pmtu_trace(events)))'''
    try:
        result = subprocess.run(
            [sys.executable, "-c", runner, str(pathlib.Path(candidate).resolve()), payload],
            capture_output=True, text=True, timeout=5,
        )
        lines = [line[len("__RESULT__"):] for line in result.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if result.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) == EXPECTED else 1)
