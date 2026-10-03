import base64
import json
import pathlib
import subprocess
import sys


def vrp(prefix, origin, maximum):
    return {"prefix": prefix, "origin_as": origin, "max_length": maximum}


def case(vrps, prefix, origin, reject, classification, eligible):
    return (vrps, {"prefix": prefix, "origin_as": origin}, reject,
            {"classification": classification, "eligible": eligible})


BROAD4 = vrp("10.0.0.0/8", 64500, 24)
NARROW4 = vrp("10.2.0.0/16", 64501, 16)
BROAD6 = vrp("2001:db8::/32", 64500, 64)
NARROW6 = vrp("2001:db8:1::/48", 64501, 48)
ZERO4 = vrp("10.0.0.0/8", 0, 32)

# Every expected classification and policy result is explicitly specified.
CASES = [
    case([BROAD4, NARROW4], "10.2.3.0/24", 64500, True, "valid", True),
    case([NARROW4, BROAD4], "10.2.3.0/24", 64500, False, "valid", True),
    case([BROAD4, NARROW4], "10.2.3.0/24", 64501, False, "invalid", True),
    case([BROAD4, NARROW4], "10.2.3.0/24", 64501, True, "invalid", False),
    case([BROAD4], "10.9.0.0/25", 64500, True, "invalid", False),
    case([BROAD4], "10.9.0.0/24", 64502, False, "invalid", True),
    case([BROAD4], "10.9.0.0/24", 64502, True, "invalid", False),
    case([BROAD4], "192.0.2.0/24", 64500, True, "not-found", True),
    case([], "192.0.2.0/24", 64500, False, "not-found", True),
    case([NARROW4], "10.2.0.0/16", 64501, True, "valid", True),
    case([vrp("10.2.3.0/24", 64500, 24)], "10.2.0.0/16", 64500,
         True, "not-found", True),
    case([BROAD6, NARROW6], "2001:db8:1::/64", 64500, True, "valid", True),
    case([NARROW6, BROAD6], "2001:db8:1::/64", 64500, False, "valid", True),
    case([vrp("2001:db8::/32", 64500, 48)], "2001:db8:1::/64", 64500,
         False, "invalid", True),
    case([vrp("2001:db8:1::/48", 64501, 64)], "2001:db8:1::/64", 64501,
         True, "valid", True),
    case([vrp("::/0", 64500, 128)], "10.2.3.0/24", 64500,
         True, "not-found", True),
    case([vrp("0.0.0.0/0", 64500, 32)], "2001:db8::/32", 64500,
         True, "not-found", True),
    case([BROAD4, BROAD6], "2001:db8:2::/64", 64500, True, "valid", True),
    case([ZERO4], "10.2.3.0/24", 0, False, "invalid", True),
    case([ZERO4], "10.2.3.0/24", 0, True, "invalid", False),
    case([ZERO4], "10.2.3.0/24", 64500, True, "invalid", False),
    case([BROAD4], "10.2.3.0/24", None, True, "invalid", False),
    case([BROAD6], "2001:db8:2::/64", None, False, "invalid", True),
    case([], "192.0.2.0/24", None, True, "not-found", True),
    case([], "192.0.2.0/24", 0, True, "not-found", True),
    case([ZERO4, BROAD4], "10.2.3.0/24", 64500, True, "valid", True),
]
EXPECTED = [entry[3] for entry in CASES]


def run(candidate):
    payload = base64.b64encode(json.dumps(CASES).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
cases = json.loads(base64.b64decode(sys.argv[2]))
results = [module.classify_roa(v, a, reject_invalid=r) for v, a, r, _ in cases]
print("__RESULT__" + json.dumps(results))'''
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
