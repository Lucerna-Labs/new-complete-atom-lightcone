import base64
import copy
import json
import pathlib
import subprocess
import sys


PEER, MID, TOKEN = "server-a:5683", 42, "a1b2"


def tick(time):
    return {"at_ms": time, "kind": "tick"}


def ack(time, peer=PEER, mid=MID):
    return {"at_ms": time, "kind": "empty_ack", "peer": peer, "mid": mid}


def response(time, kind="separate", peer=PEER, mid=999, token=TOKEN):
    return {"at_ms": time, "kind": kind, "peer": peer, "mid": mid, "token": token}


def state(sent, timer, failed=False, complete=False):
    return {"transmissions": sent, "next_timeout": timer,
            "message_failed": failed, "complete": complete}


def case(events, expected, r_ms=2000, peer=PEER, mid=MID, token=TOKEN):
    return ({"peer": peer, "mid": mid, "token": token,
             "r_ms": r_ms, "events": events}, expected)


# Literal hand-derived schedules. Timers strictly before an input run first;
# a timer equal to the input time runs only after all inputs at that time.
CASES = [
    case([], [state([0], 2000)]),
    case([tick(0), tick(1999), tick(2000), tick(5999), tick(6000),
          tick(14000), tick(30000), tick(61999), tick(62000), tick(100000)], [
        state([0], 2000), state([0], 2000), state([0], 2000),
        state([0, 2000], 6000), state([0, 2000], 6000),
        state([0, 2000, 6000], 14000), state([0, 2000, 6000, 14000], 30000),
        state([0, 2000, 6000, 14000, 30000], 62000),
        state([0, 2000, 6000, 14000, 30000], 62000),
        state([0, 2000, 6000, 14000, 30000], None, True),
        state([0, 2000, 6000, 14000, 30000], None, True)]),
    case([tick(2500), tick(7500), tick(17500), tick(37500), tick(77500)], [
        state([0], 2500), state([0, 2500], 7500), state([0, 2500, 7500], 17500),
        state([0, 2500, 7500, 17500], 37500),
        state([0, 2500, 7500, 17500, 37500], 77500),
        state([0, 2500, 7500, 17500, 37500], None, True)], r_ms=2500),
    case([tick(2999), tick(3000), tick(9000), tick(21000), tick(45000),
          tick(92999), tick(93000)], [
        state([0], 3000), state([0], 3000), state([0, 3000], 9000),
        state([0, 3000, 9000], 21000), state([0, 3000, 9000, 21000], 45000),
        state([0, 3000, 9000, 21000, 45000], 93000),
        state([0, 3000, 9000, 21000, 45000], 93000),
        state([0, 3000, 9000, 21000, 45000], None, True)], r_ms=3000),
    case([tick(246999)], [state([0], 2001),
        state([0, 2001, 6003, 14007, 30015], None, True)], r_ms=2001),
    case([ack(1000), tick(100000), response(150000), tick(200000)], [
        state([0], 2000), state([0], None), state([0], None),
        state([0], None, complete=True), state([0], None, complete=True)]),
    case([ack(500, peer="server-a:5684"), ack(1500, mid=43), tick(2000),
          ack(2500), ack(3000), tick(100000)], [
        state([0], 2000), state([0], 2000), state([0], 2000),
        state([0, 2000], 6000), state([0, 2000], None),
        state([0, 2000], None), state([0, 2000], None)]),
    case([response(500, "piggyback", peer="other:5683", mid=MID),
          response(1000, "piggyback", mid=43),
          response(1500, "piggyback", mid=MID, token="ff"), tick(2000),
          response(2500, "piggyback", mid=MID), tick(100000)], [
        state([0], 2000), state([0], 2000), state([0], 2000), state([0], 2000),
        state([0, 2000], 6000), state([0, 2000], None, complete=True),
        state([0, 2000], None, complete=True)]),
    case([response(500, peer="server-a:5684"), response(1000, mid=MID, token="ff"),
          response(1500), ack(2200), tick(62000)], [
        state([0], 2000), state([0], 2000), state([0], 2000),
        state([0], None, complete=True), state([0], None, complete=True),
        state([0], None, complete=True)]),
    case([response(0, mid=MID), tick(62000)], [
        state([0], 2000), state([0], None, complete=True),
        state([0], None, complete=True)]),
    case([ack(2000), tick(62000)], [
        state([0], 2000), state([0], None), state([0], None)]),
    case([ack(2000, mid=43), response(2000), tick(62000)], [
        state([0], 2000), state([0], 2000), state([0], None, complete=True),
        state([0], None, complete=True)]),
    case([tick(2000), ack(2000)], [
        state([0], 2000), state([0], 2000), state([0], None)]),
    case([tick(2000), ack(2000, mid=43)], [
        state([0], 2000), state([0], 2000), state([0, 2000], 6000)]),
    case([ack(62000), tick(100000)], [
        state([0], 2000), state([0, 2000, 6000, 14000, 30000], None),
        state([0, 2000, 6000, 14000, 30000], None)]),
    case([ack(62000, peer="other:5683"), response(62001), tick(100000)], [
        state([0], 2000), state([0, 2000, 6000, 14000, 30000], None, True),
        state([0, 2000, 6000, 14000, 30000], None, True, True),
        state([0, 2000, 6000, 14000, 30000], None, True, True)]),
    case([response(2000, token="ff"), response(2001)], [
        state([0], 2000), state([0, 2000], 6000),
        state([0, 2000], None, complete=True)]),
    case([ack(1, mid=0), response(2, mid=65535, token="")], [
        state([0], 2000), state([0], None), state([0], None, complete=True)],
         mid=0, token=""),
    case([response(1, "piggyback", mid=65535, token="0011223344556677")], [
        state([0], 3000), state([0], None, complete=True)],
         r_ms=3000, mid=65535, token="0011223344556677"),
    case([], [state([0], 2000)]),
    case([ack(1), response(2, peer="remote-z:61616", mid=8, token="00")], [
        state([0], 2750), state([0], 2750), state([0], None, complete=True)],
         peer="remote-z:61616", mid=7, token="00", r_ms=2750),
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
    values.append(module.coap_exchange(**supplied))
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
    if result != EXPECTED or type(result["unchanged"]) is not bool:
        return False
    return all(type(s["message_failed"]) is bool and type(s["complete"]) is bool
               and (s["next_timeout"] is None or type(s["next_timeout"]) is int)
               and all(type(t) is int for t in s["transmissions"])
               for trace in result["values"] for s in trace)


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and passes(run(sys.argv[1])) else 1)
