import base64
import copy
import json
import pathlib
import subprocess
import sys


FLOW = {
    "instance": "fw-a", "protocol": "tcp",
    "src": ["192.0.2.10", 40000], "dst": ["198.51.100.20", 443],
    "expires_at": 10,
}
PACKET = {
    "instance": "fw-a", "protocol": "tcp",
    "src": ["198.51.100.20", 443], "dst": ["192.0.2.10", 40000],
    "ack": True, "transition_ok": True,
}


def case(admit, reason, packet=None, states=None, now=5, **rules):
    return ({"packet": copy.deepcopy(PACKET if packet is None else packet),
             "states": copy.deepcopy([FLOW] if states is None else states),
             "now": now, **rules}, {"admit": admit, "reason": reason})


# Literal hand-oracles. The ACK flag is never a substitute for a matching state;
# transition_ok is a separate supplied protocol result, including for ACK-free
# TCP packets that the upstream protocol validator permits (for example a RST).
CASES = [
    case(True, "state"),
    case(True, "state", packet={**PACKET, "ack": False}),
    case(False, "no-live-reverse-state", states=[]),
    case(False, "no-live-reverse-state", states=[], packet={**PACKET, "ack": False}),
    case(True, "state", now=9),
    case(False, "no-live-reverse-state", now=10),
    case(False, "no-live-reverse-state", now=11),
    case(False, "no-live-reverse-state", now=0, states=[{**FLOW, "expires_at": 0}]),
    case(True, "state", now=0, states=[{**FLOW, "expires_at": 1}]),
    case(False, "no-live-reverse-state", now=1, states=[{**FLOW, "expires_at": 1}]),
    case(False, "no-live-reverse-state", packet={**PACKET, "instance": "fw-b"}),
    case(True, "state", packet={**PACKET, "instance": "fw-b"},
         states=[FLOW, {**FLOW, "instance": "fw-b"}]),
    case(False, "no-live-reverse-state", states=[{**FLOW, "instance": "fw-b"}]),
    case(False, "no-live-reverse-state", packet={**PACKET, "protocol": "udp", "ack": False}),
    case(False, "no-live-reverse-state", states=[{**FLOW, "protocol": "udp"}]),
    case(True, "state", packet={**PACKET, "protocol": "udp", "ack": False},
         states=[{**FLOW, "protocol": "udp"}]),
    case(False, "no-live-reverse-state", packet={**PACKET, "src": ["198.51.100.21", 443]}),
    case(False, "no-live-reverse-state", packet={**PACKET, "dst": ["192.0.2.11", 40000]}),
    case(False, "no-live-reverse-state", packet={**PACKET, "src": ["198.51.100.20", 444]}),
    case(False, "no-live-reverse-state", packet={**PACKET, "dst": ["192.0.2.10", 40001]}),
    case(False, "no-live-reverse-state", packet={**PACKET, "src": FLOW["src"], "dst": FLOW["dst"]}),
    case(False, "bad-transition", packet={**PACKET, "transition_ok": False}),
    case(False, "bad-transition", packet={**PACKET, "ack": False, "transition_ok": False}),
    case(False, "bad-transition", packet={**PACKET, "protocol": "udp", "ack": False,
                                         "transition_ok": False},
         states=[{**FLOW, "protocol": "udp"}]),
    case(False, "deny-rule", deny_rule=True),
    case(False, "return-rule-disabled", return_rule=False),
    case(False, "deny-rule", deny_rule=True, return_rule=False),
    case(False, "deny-rule", states=[], deny_rule=True),
    case(False, "return-rule-disabled", states=[], return_rule=False),
    case(False, "no-live-reverse-state", states=[], packet={**PACKET, "transition_ok": False}),
    case(False, "deny-rule", deny_rule=True, packet={**PACKET, "transition_ok": False}),
    case(False, "return-rule-disabled", return_rule=False,
         packet={**PACKET, "transition_ok": False}),
    case(True, "state", states=[{**FLOW, "instance": "fw-b"},
                                {**FLOW, "expires_at": 3}, FLOW]),
    case(True, "state", states=[FLOW, {**FLOW, "instance": "fw-b"},
                                {**FLOW, "expires_at": 3}]),
    case(False, "no-live-reverse-state", states=[{**FLOW, "expires_at": 3},
                                                {**FLOW, "instance": "fw-b"}]),
    case(True, "state", now=0),
    case(False, "no-live-reverse-state", states=[]),
    case(True, "state"),
]
EXPECTED = {"values": [answer for _, answer in CASES], "unchanged": True}


def run(candidate):
    payload = base64.b64encode(json.dumps(CASES).encode()).decode()
    runner = r'''import base64, copy, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
values, unchanged = [], True
for kwargs, _ in json.loads(base64.b64decode(sys.argv[2])):
    supplied = copy.deepcopy(kwargs)
    values.append(module.firewall_return_gate(**supplied))
    unchanged = unchanged and supplied == kwargs
print("__RESULT__" + json.dumps({"values": values, "unchanged": unchanged}))'''
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
    return (type(result["unchanged"]) is bool
            and all(type(value["admit"]) is bool and type(value["reason"]) is str
                    for value in result["values"]))


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and passes(run(sys.argv[1])) else 1)
