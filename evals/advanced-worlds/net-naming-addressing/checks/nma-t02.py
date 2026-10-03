import base64
import json
import pathlib
import subprocess
import sys

BASE = {
    "rrset_ttl": 80, "rrsig_ttl": 70, "original_ttl": 60,
    "inception": 90, "expiration": 200,
    "algorithm_supported": True, "key_trusted": True,
    "metadata_ok": True, "signature_ok": True,
}


def case(now, accepted, ttl, **overrides):
    return ({**BASE, **overrides}, now, {"accepted": accepted, "cache_ttl": ttl})


# Literal answers independently exercise every acceptance and TTL bound.
CASES = [
    case(100, True, 60),
    case(100, True, 9, rrset_ttl=9),
    case(100, True, 8, rrsig_ttl=8),
    case(100, True, 7, original_ttl=7),
    case(100, True, 5, expiration=105),
    case(100, False, 0, algorithm_supported=False),
    case(100, False, 0, key_trusted=False),
    case(100, False, 0, metadata_ok=False),
    case(100, False, 0, signature_ok=False),
    case(89, False, 0),
    case(90, True, 60),
    case(199, True, 1),
    case(200, True, 0),
    case(201, False, 0),
    case(100, True, 0, rrset_ttl=0),
    case(100, True, 0, rrsig_ttl=0),
    case(100, True, 0, original_ttl=0),
    case(100, True, 0, inception=100, expiration=100),
    case(100, True, 10, rrset_ttl=10, rrsig_ttl=10,
         original_ttl=10, expiration=110),
]
EXPECTED = {"values": [c[2] for c in CASES], "unchanged": True}


def run(candidate):
    payload = base64.b64encode(json.dumps(CASES).encode()).decode()
    runner = r'''import base64, copy, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
values, unchanged = [], True
for record, now, _ in json.loads(base64.b64decode(sys.argv[2])):
    given = copy.deepcopy(record)
    values.append(module.dnssec_cache_gate(given, now))
    unchanged = unchanged and given == record
print("__RESULT__" + json.dumps({"values": values, "unchanged": unchanged}))'''
    try:
        process = subprocess.run(
            [sys.executable, "-c", runner, str(pathlib.Path(candidate).resolve()), payload],
            capture_output=True, text=True, timeout=5,
        )
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if process.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


def passes(result):
    if result != EXPECTED:
        return False
    return all(type(value["accepted"]) is bool and type(value["cache_ttl"]) is int
               for value in result["values"])


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and passes(run(sys.argv[1])) else 1)
