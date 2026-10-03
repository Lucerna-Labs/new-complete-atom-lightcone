import base64
import json
import pathlib
import subprocess
import sys

IP = "203.0.113.1"
I = ["10.0.0.2", 12345]
J = ["10.0.0.3", 12345]
I_OTHER_PORT = ["10.0.0.2", 12346]
STUN = ["198.51.100.1", 3478]
PEER = ["198.51.100.2", 5000]
PEER_OTHER_PORT = ["198.51.100.2", 5001]
OTHER_PEER = ["198.51.100.3", 5000]


def outbound(time, internal, remote):
    return {"type": "outbound", "time": time, "internal": internal, "remote": remote}


def inbound(time, port, remote, ip=IP):
    return {"type": "inbound", "time": time, "external": [ip, port], "remote": remote}


def tick(time):
    return {"type": "tick", "time": time}


def answer(result, live, external=None, internal=None):
    return {"result": result, "external": external, "internal": internal, "live_ports": live}


def mapped(port, live, ip=IP):
    return answer("mapped", live, external=[ip, port])


def delivered(internal, live):
    return answer("delivered", live, internal=internal)


def case(mapping, filtering, timeout, events, expected, ip=IP, first=40000):
    return ({"mapping_mode": mapping, "filter_mode": filtering, "idle_timeout": timeout,
             "external_ip": ip, "first_port": first}, events, expected)


# Fixed expected outputs are hand-computed, not obtained from the reference.
A = [
    outbound(0, I, STUN), inbound(0, 40000, STUN), inbound(1, 40000, PEER),
    outbound(1, I, PEER), inbound(1, 40000, PEER),
    inbound(2, 40000, PEER_OTHER_PORT), inbound(2, 40000, OTHER_PEER),
    inbound(2, 40000, STUN, "203.0.113.99"), tick(5), inbound(5, 40000, PEER),
    tick(6), inbound(6, 40000, PEER), outbound(6, I, STUN),
    inbound(6, 40001, PEER), inbound(6, 40000, STUN),
    outbound(7, J, STUN), inbound(7, 40002, STUN),
    outbound(7, I_OTHER_PORT, STUN), inbound(7, 40003, STUN),
    tick(11), inbound(11, 40002, STUN), tick(12),
]
EA = [
    mapped(40000, [40000]), delivered(I, [40000]), answer("filtered", [40000]),
    mapped(40000, [40000]), delivered(I, [40000]), answer("filtered", [40000]),
    answer("filtered", [40000]), answer("unmapped", [40000]), answer("tick", [40000]),
    delivered(I, [40000]), answer("tick", []), answer("unmapped", []),
    mapped(40001, [40001]), answer("filtered", [40001]), answer("unmapped", [40001]),
    mapped(40002, [40001, 40002]), delivered(J, [40001, 40002]),
    mapped(40003, [40001, 40002, 40003]), delivered(I_OTHER_PORT, [40001, 40002, 40003]),
    answer("tick", [40002, 40003]), delivered(J, [40002, 40003]), answer("tick", []),
]
B = [outbound(0, I, STUN), inbound(0, 40000, PEER), outbound(1, I, PEER),
     inbound(2, 40000, OTHER_PEER), tick(3)]
EB = [mapped(40000, [40000]), delivered(I, [40000]), mapped(40000, [40000]),
      delivered(I, [40000]), answer("tick", [])]
C = [
    outbound(0, I, STUN), outbound(1, I, PEER), inbound(1, 40000, PEER),
    inbound(1, 40001, PEER), outbound(2, I, PEER_OTHER_PORT),
    inbound(2, 40001, PEER_OTHER_PORT), inbound(2, 40002, PEER_OTHER_PORT),
    inbound(2, 40000, STUN), outbound(3, I, STUN), tick(5),
    inbound(5, 40002, PEER), tick(6), tick(7),
]
EC = [
    mapped(40000, [40000]), mapped(40001, [40000, 40001]),
    answer("filtered", [40000, 40001]), delivered(I, [40000, 40001]),
    mapped(40002, [40000, 40001, 40002]), answer("filtered", [40000, 40001, 40002]),
    delivered(I, [40000, 40001, 40002]), delivered(I, [40000, 40001, 40002]),
    mapped(40000, [40000, 40001, 40002]), answer("tick", [40000, 40002]),
    answer("filtered", [40000, 40002]), answer("tick", [40000]), answer("tick", []),
]
D = [outbound(0, I, STUN), inbound(0, 40000, PEER), outbound(0, I, PEER),
     inbound(1, 40001, OTHER_PEER), tick(2)]
ED = [mapped(40000, [40000]), delivered(I, [40000]),
      mapped(40001, [40000, 40001]), delivered(I, [40000, 40001]), answer("tick", [])]
E = [outbound(0, I, STUN), inbound(0, 40000, STUN), outbound(0, I, STUN), tick(1)]
EE = [mapped(40000, []), answer("unmapped", []), mapped(40001, []), answer("tick", [])]
CUSTOM_IP = "198.18.0.1"
F = [outbound(0, I, STUN), inbound(0, 41000, STUN, CUSTOM_IP),
     inbound(1, 41000, STUN, CUSTOM_IP), outbound(1, I, STUN), outbound(1, I, PEER),
     inbound(1, 41001, PEER, CUSTOM_IP), tick(2)]
EF = [mapped(41000, [41000], CUSTOM_IP), delivered(I, [41000]), answer("unmapped", []),
      mapped(41001, [41001], CUSTOM_IP), mapped(41001, [41001], CUSTOM_IP),
      delivered(I, [41001]), answer("tick", [])]
CASES = [
    case("eim", "apdf", 5, A, EA), case("eim", "eif", 2, B, EB),
    case("apdm", "apdf", 4, C, EC), case("apdm", "eif", 2, D, ED),
    case("eim", "apdf", 0, E, EE),
    case("eim", "apdf", 1, F, EF, CUSTOM_IP, 41000),
    case("eim", "apdf", 5, [], []),
    ({}, A, EA),  # Also call the API using its declared defaults.
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
for kwargs, events, _ in json.loads(base64.b64decode(sys.argv[2])):
    given = copy.deepcopy(events)
    options = copy.deepcopy(kwargs)
    values.append(module.nat_trace(given, **options))
    unchanged = unchanged and given == events and options == kwargs
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


def endpoint(value):
    return value is None or (type(value) is list and len(value) == 2
                             and type(value[0]) is str and type(value[1]) is int)


def passes(result):
    if result != EXPECTED:
        return False
    return all(type(row["result"]) is str
               and endpoint(row["external"]) and endpoint(row["internal"])
               and type(row["live_ports"]) is list
               and all(type(port) is int for port in row["live_ports"])
               for trace in result["values"] for row in trace)


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and passes(run(sys.argv[1])) else 1)
