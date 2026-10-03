import base64
import json
import pathlib
import subprocess
import sys


BASE = {
    "ech_accepted": False, "negotiated_tls13": True,
    "handshake_ok": True, "identity_ok": True,
    "retry_configs": "absent", "allow_non_ech_retry": False,
}


def case(success, action, **overrides):
    return ({**BASE, **overrides}, {
        "original_success": success, "send_application": success, "action": action,
    })


# Every answer is literal. A rejected outer connection never gains application
# permission, including when public-name authentication licenses a fresh retry.
CASES = [
    case(True, "complete", ech_accepted=True),
    case(True, "complete", ech_accepted=True, allow_non_ech_retry=True),
    case(False, "fail", ech_accepted=True, identity_ok=False),
    case(False, "fail", ech_accepted=True, handshake_ok=False),
    case(False, "fail", ech_accepted=True, identity_ok=False, handshake_ok=False),
    case(False, "fail"),
    case(False, "retry-without-ech", allow_non_ech_retry=True),
    case(False, "retry-ech", retry_configs="supported"),
    case(False, "retry-ech", retry_configs="supported", allow_non_ech_retry=True),
    case(False, "fail", retry_configs="supported", identity_ok=False),
    case(False, "fail", retry_configs="supported", handshake_ok=False),
    case(False, "fail", retry_configs="supported", identity_ok=False,
         allow_non_ech_retry=True),
    case(False, "fail", retry_configs="supported", handshake_ok=False,
         allow_non_ech_retry=True),
    case(False, "fail", retry_configs="supported", identity_ok=False,
         handshake_ok=False, allow_non_ech_retry=True),
    case(False, "fail", retry_configs="unsupported"),
    case(False, "retry-without-ech", retry_configs="unsupported",
         allow_non_ech_retry=True),
    case(False, "fail", retry_configs="unsupported", identity_ok=False,
         allow_non_ech_retry=True),
    case(False, "fail", retry_configs="unsupported", handshake_ok=False,
         allow_non_ech_retry=True),
    case(False, "fail", identity_ok=False, allow_non_ech_retry=True),
    case(False, "fail", handshake_ok=False, allow_non_ech_retry=True),
    case(False, "fail", retry_configs="malformed"),
    case(False, "fail", retry_configs="malformed", allow_non_ech_retry=True),
    case(False, "fail", retry_configs="malformed", identity_ok=False,
         allow_non_ech_retry=True),
    case(False, "fail", negotiated_tls13=False),
    case(False, "retry-without-ech", negotiated_tls13=False,
         allow_non_ech_retry=True),
    case(False, "fail", negotiated_tls13=False, identity_ok=False,
         allow_non_ech_retry=True),
    case(False, "fail", negotiated_tls13=False, handshake_ok=False,
         allow_non_ech_retry=True),
    case(True, "complete", ech_accepted=True),
    case(False, "fail", retry_configs="supported", identity_ok=False),
]
CASES += [
    ({"ech_accepted":False,"negotiated_tls13":True,"handshake_ok":True,"identity_ok":True},
     {"original_success":False,"send_application":False,"action":"fail"}),
    ({"ech_accepted":True,"negotiated_tls13":True,"handshake_ok":True,"identity_ok":True},
     {"original_success":True,"send_application":True,"action":"complete"}),
]
EXPECTED = [answer for _, answer in CASES]


def run(candidate):
    payload = base64.b64encode(json.dumps(CASES).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
values = []
for kwargs, _ in json.loads(base64.b64decode(sys.argv[2])):
    values.append(module.ech_recovery(**kwargs))
print("__RESULT__" + json.dumps(values))'''
    try:
        process = subprocess.run(
            [sys.executable, "-B", "-c", runner,
             str(pathlib.Path(candidate).resolve()), payload],
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
    return all(type(value["original_success"]) is bool
               and type(value["send_application"]) is bool
               and type(value["action"]) is str for value in result)


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and passes(run(sys.argv[1])) else 1)
