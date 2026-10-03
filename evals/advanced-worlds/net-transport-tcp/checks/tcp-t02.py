import base64
import json
import pathlib
import subprocess
import sys

CASES = [
    (2000, "a", False, 3, 7, 12000, 3000, {"rwnd": 16000, "budget": 9000}),
    (1000, "b", False, 3, 7, 50000, 60000, {"rwnd": 128000, "budget": 0}),
    (60000, "a", True, 7, 5, 50000, 12000, {"rwnd": 60000, "budget": 38000}),
    (65535, "b", True, 7, 14, 90000, 100, {"rwnd": 65535, "budget": 65435}),
    (4096, "b", False, 2, 5, 10000, 1234, {"rwnd": 131072, "budget": 8766}),
    (0, "a", False, 0, 14, 9000, 0, {"rwnd": 0, "budget": 0}),
    (65535, "b", False, 0, 14, 200000, 12345, {"rwnd": 1073725440, "budget": 187655}),
    (65535, "a", False, 0, 14, 100000, 1000, {"rwnd": 65535, "budget": 64535}),
    (1000, "a", False, 4, 14, 90000, 1000, {"rwnd": 16000, "budget": 15000}),
]

def run(candidate):
    payload = base64.b64encode(json.dumps(CASES).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
cases = json.loads(base64.b64decode(sys.argv[2]))
out = [mod.decode_and_budget(*case[:7]) for case in cases]
print("__RESULT__" + json.dumps(out, separators=(",", ":")))'''
    try:
        p = subprocess.run([sys.executable, "-c", runner, str(pathlib.Path(candidate).resolve()), payload],
                           capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in p.stdout.splitlines() if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if p.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError, json.JSONDecodeError):
        return None

def main(candidate):
    got = run(candidate)
    return (isinstance(got, list) and all(isinstance(item, dict) and set(item) == {"rwnd", "budget"} and all(type(item[k]) is int for k in item) for item in got) and got == [case[-1] for case in CASES])

if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and main(sys.argv[1]) else 1)
