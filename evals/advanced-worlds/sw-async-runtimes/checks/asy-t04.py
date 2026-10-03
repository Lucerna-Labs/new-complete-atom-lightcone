import base64
import json
import pathlib
import subprocess
import sys


def send(oid, value, owner="o"):
    return {"op": "send", "id": oid, "owner": owner, "value": value}


def reserve(oid, owner="o"):
    return {"op": "reserve", "id": oid, "owner": owner}


def action(op, oid):
    return {"op": op, "id": oid}


def permit_send(oid, value):
    return {"op": "permit_send", "id": oid, "value": value}


def owner_drop(owner="o"):
    return {"op": "owner_drop", "owner": owner}


def operation(kind, owner="o", value=None):
    return {"kind": kind, "owner": owner, "value": value}


def snap(op, free, owners, queue=(), operations=None, dropped=(), received=()):
    return {"op": op, "free": free, "owners": owners, "queue": list(queue),
            "operations": {} if operations is None else operations,
            "dropped": list(dropped), "received": list(received)}


RECEIVE = {"op": "receive"}

# These literal ownership/capacity oracles use the declared serial model.
# They do not infer when Tokio's scheduler or internal semaphore grants run.
CASES = [
    ("empty", [1, {}, [], []], []),
    ("send captures without enqueue", [1, {"o": ["M"]}, [], [send("s", "M")]],
     [snap("send", 1, {"o": []}, operations={"s": operation("send", value="M")})]),
    ("cancel send drops moved value", [1, {"o": ["M"]}, [], [send("s", "M"), action("cancel", "s")]],
     [snap("send", 1, {"o": []}, operations={"s": operation("send", value="M")}),
      snap("cancel", 1, {"o": []}, dropped=["M"])]),
    ("cancel send on full channel does not enqueue", [1, {"o": ["M"]}, ["Q"],
       [send("s", "M"), action("cancel", "s")]],
     [snap("send", 0, {"o": []}, ["Q"], {"s": operation("send", value="M")}),
      snap("cancel", 0, {"o": []}, ["Q"], dropped=["M"])]),
    ("send success then receipt", [1, {"o": ["M"]}, [],
       [send("s", "M"), action("send_ready", "s"), RECEIVE]],
     [snap("send", 1, {"o": []}, operations={"s": operation("send", value="M")}),
      snap("send_ready", 0, {"o": []}, ["M"]),
      snap("receive", 1, {"o": []}, received=["M"])]),
    ("cancel reserve leaves caller values", [1, {"o": ["M"]}, ["Q"],
       [reserve("r"), action("cancel", "r")]],
     [snap("reserve", 0, {"o": ["M"]}, ["Q"], {"r": operation("reserve")}),
      snap("cancel", 0, {"o": ["M"]}, ["Q"])]),
    ("reservation separates capacity from message move", [1, {"o": ["M"]}, [],
       [reserve("r"), action("reserve_ready", "r"), permit_send("r", "M"), RECEIVE]],
     [snap("reserve", 1, {"o": ["M"]}, operations={"r": operation("reserve")}),
      snap("reserve_ready", 0, {"o": ["M"]}, operations={"r": operation("permit")}),
      snap("permit_send", 0, {"o": []}, ["M"]),
      snap("receive", 1, {"o": []}, received=["M"])]),
    ("dropping permit returns capacity but keeps message", [2, {"o": ["M"]}, [],
       [reserve("r"), action("reserve_ready", "r"), action("permit_drop", "r")]],
     [snap("reserve", 2, {"o": ["M"]}, operations={"r": operation("reserve")}),
      snap("reserve_ready", 1, {"o": ["M"]}, operations={"r": operation("permit")}),
      snap("permit_drop", 2, {"o": ["M"]})]),
    ("cancelling incomplete reserve never held an exposed permit", [2, {"o": ["M", "N"]}, [],
       [reserve("r"), action("cancel", "r")]],
     [snap("reserve", 2, {"o": ["M", "N"]}, operations={"r": operation("reserve")}),
      snap("cancel", 2, {"o": ["M", "N"]})]),
    ("reserve retry retains payload across branch cancellation", [1, {"o": ["M"]}, ["Q"],
       [reserve("r"), action("cancel", "r"), RECEIVE, reserve("t"),
        action("reserve_ready", "t"), permit_send("t", "M")]],
     [snap("reserve", 0, {"o": ["M"]}, ["Q"], {"r": operation("reserve")}),
      snap("cancel", 0, {"o": ["M"]}, ["Q"]),
      snap("receive", 1, {"o": ["M"]}, received=["Q"]),
      snap("reserve", 1, {"o": ["M"]}, operations={"t": operation("reserve")}, received=["Q"]),
      snap("reserve_ready", 0, {"o": ["M"]}, operations={"t": operation("permit")}, received=["Q"]),
      snap("permit_send", 0, {"o": []}, ["M"], received=["Q"])]),
    ("drop owner after cancelled send cannot recover message", [1, {"o": ["M"]}, ["Q"],
       [send("s", "M"), action("cancel", "s"), owner_drop()]],
     [snap("send", 0, {"o": []}, ["Q"], {"s": operation("send", value="M")}),
      snap("cancel", 0, {"o": []}, ["Q"], dropped=["M"]),
      snap("owner_drop", 0, {}, ["Q"], dropped=["M"])]),
    ("owner drop destroys pending send and other local values", [1, {"o": ["M", "N"]}, ["Q"],
       [send("s", "M"), owner_drop()]],
     [snap("send", 0, {"o": ["N"]}, ["Q"], {"s": operation("send", value="M")}),
      snap("owner_drop", 0, {}, ["Q"], dropped=["M", "N"])]),
    ("whole owner drop differs from cancelling reserve branch", [1, {"o": ["M", "N"]}, ["Q"],
       [reserve("r"), owner_drop()]],
     [snap("reserve", 0, {"o": ["M", "N"]}, ["Q"], {"r": operation("reserve")}),
      snap("owner_drop", 0, {}, ["Q"], dropped=["M", "N"])]),
    ("owner drop releases permit without discarding queued values", [2, {"o": ["M"]}, ["Q"],
       [reserve("r"), action("reserve_ready", "r"), owner_drop(), RECEIVE]],
     [snap("reserve", 1, {"o": ["M"]}, ["Q"], {"r": operation("reserve")}),
      snap("reserve_ready", 0, {"o": ["M"]}, ["Q"], {"r": operation("permit")}),
      snap("owner_drop", 1, {}, ["Q"], dropped=["M"]),
      snap("receive", 2, {}, dropped=["M"], received=["Q"])]),
    ("owner drop cannot retract a successful send", [1, {"o": ["M"]}, [],
       [send("s", "M"), action("send_ready", "s"), owner_drop(), RECEIVE]],
     [snap("send", 1, {"o": []}, operations={"s": operation("send", value="M")}),
      snap("send_ready", 0, {"o": []}, ["M"]),
      snap("owner_drop", 0, {}, ["M"]), snap("receive", 1, {}, received=["M"])]),
    ("owner-specific cancellation leaves another reservation", [1, {"A": ["M"], "B": ["N"]}, [],
       [send("s", "M", "A"), reserve("r", "B"), owner_drop("A"),
        action("reserve_ready", "r"), permit_send("r", "N")]],
     [snap("send", 1, {"A": [], "B": ["N"]}, operations={"s": operation("send", "A", "M")}),
      snap("reserve", 1, {"A": [], "B": ["N"]}, operations={"s": operation("send", "A", "M"), "r": operation("reserve", "B")}),
      snap("owner_drop", 1, {"B": ["N"]}, operations={"r": operation("reserve", "B")}, dropped=["M"]),
      snap("reserve_ready", 0, {"B": ["N"]}, operations={"r": operation("permit", "B")}, dropped=["M"]),
      snap("permit_send", 0, {"B": []}, ["N"], dropped=["M"])]),
    ("two permits count separately and send exchanges one slot", [2, {"o": ["M", "N"]}, [],
       [reserve("r"), action("reserve_ready", "r"), reserve("t"), action("reserve_ready", "t"),
        permit_send("r", "M"), action("permit_drop", "t"), send("s", "N"),
        action("send_ready", "s"), RECEIVE, RECEIVE]],
     [snap("reserve", 2, {"o": ["M", "N"]}, operations={"r": operation("reserve")}),
      snap("reserve_ready", 1, {"o": ["M", "N"]}, operations={"r": operation("permit")}),
      snap("reserve", 1, {"o": ["M", "N"]}, operations={"r": operation("permit"), "t": operation("reserve")}),
      snap("reserve_ready", 0, {"o": ["M", "N"]}, operations={"r": operation("permit"), "t": operation("permit")}),
      snap("permit_send", 0, {"o": ["N"]}, ["M"], {"t": operation("permit")}),
      snap("permit_drop", 1, {"o": ["N"]}, ["M"]),
      snap("send", 1, {"o": []}, ["M"], {"s": operation("send", value="N")}),
      snap("send_ready", 0, {"o": []}, ["M", "N"]),
      snap("receive", 1, {"o": []}, ["N"], received=["M"]),
      snap("receive", 2, {"o": []}, received=["M", "N"])]),
    ("permit use order determines FIFO independently of acquisition", [3, {"o": ["M", "N"]}, ["Q"],
       [reserve("r"), action("reserve_ready", "r"), reserve("t"), action("reserve_ready", "t"),
        permit_send("t", "N"), permit_send("r", "M"), RECEIVE, RECEIVE, RECEIVE]],
     [snap("reserve", 2, {"o": ["M", "N"]}, ["Q"], {"r": operation("reserve")}),
      snap("reserve_ready", 1, {"o": ["M", "N"]}, ["Q"], {"r": operation("permit")}),
      snap("reserve", 1, {"o": ["M", "N"]}, ["Q"], {"r": operation("permit"), "t": operation("reserve")}),
      snap("reserve_ready", 0, {"o": ["M", "N"]}, ["Q"], {"r": operation("permit"), "t": operation("permit")}),
      snap("permit_send", 0, {"o": ["M"]}, ["Q", "N"], {"r": operation("permit")}),
      snap("permit_send", 0, {"o": []}, ["Q", "N", "M"]),
      snap("receive", 1, {"o": []}, ["N", "M"], received=["Q"]),
      snap("receive", 2, {"o": []}, ["M"], received=["Q", "N"]),
      snap("receive", 3, {"o": []}, received=["Q", "N", "M"])]),
    ("initial queue and receipt order are not sorted", [3, {}, ["z", "Q", "A"], [RECEIVE, RECEIVE, RECEIVE]],
     [snap("receive", 1, {}, ["Q", "A"], received=["z"]),
      snap("receive", 2, {}, ["A"], received=["z", "Q"]),
      snap("receive", 3, {}, received=["z", "Q", "A"])]),
    ("caller ownership lists are sorted case-sensitively", [1, {"o": ["z", "A", "a"]}, [],
       [reserve("r"), action("cancel", "r")]],
     [snap("reserve", 1, {"o": ["A", "a", "z"]}, operations={"r": operation("reserve")}),
      snap("cancel", 1, {"o": ["A", "a", "z"]})]),
    ("operation identities preserve case", [2, {"o": ["M", "N"]}, [],
       [send("s", "M"), send("S", "N"), action("cancel", "S"), action("send_ready", "s")]],
     [snap("send", 2, {"o": ["N"]}, operations={"s": operation("send", value="M")}),
      snap("send", 2, {"o": []}, operations={"s": operation("send", value="M"), "S": operation("send", value="N")}),
      snap("cancel", 2, {"o": []}, operations={"s": operation("send", value="M")}, dropped=["N"]),
      snap("send_ready", 1, {"o": []}, ["M"], dropped=["N"])]),
    ("incomplete send waits outside exposed capacity", [1, {"o": ["M"]}, [],
       [reserve("r"), action("reserve_ready", "r"), send("s", "M"),
        action("permit_drop", "r"), action("send_ready", "s")]],
     [snap("reserve", 1, {"o": ["M"]}, operations={"r": operation("reserve")}),
      snap("reserve_ready", 0, {"o": ["M"]}, operations={"r": operation("permit")}),
      snap("send", 0, {"o": []}, operations={"r": operation("permit"), "s": operation("send", value="M")}),
      snap("permit_drop", 1, {"o": []}, operations={"s": operation("send", value="M")}),
      snap("send_ready", 0, {"o": []}, ["M"])]),
    ("owner drop handles mixed owned states once", [3, {"o": ["M", "N", "P"]}, ["Q"],
       [send("s", "M"), reserve("r"), action("reserve_ready", "r"), reserve("t"), owner_drop()]],
     [snap("send", 2, {"o": ["N", "P"]}, ["Q"], {"s": operation("send", value="M")}),
      snap("reserve", 2, {"o": ["N", "P"]}, ["Q"], {"s": operation("send", value="M"), "r": operation("reserve")}),
      snap("reserve_ready", 1, {"o": ["N", "P"]}, ["Q"], {"s": operation("send", value="M"), "r": operation("permit")}),
      snap("reserve", 1, {"o": ["N", "P"]}, ["Q"], {"s": operation("send", value="M"), "r": operation("permit"), "t": operation("reserve")}),
      snap("owner_drop", 2, {}, ["Q"], dropped=["M", "N", "P"])]),
    ("owner identity is separate and case-sensitive", [1, {"O": ["M"], "o": ["m"]}, [],
       [reserve("r", "O"), owner_drop("o"), action("reserve_ready", "r"), permit_send("r", "M")]],
     [snap("reserve", 1, {"O": ["M"], "o": ["m"]}, operations={"r": operation("reserve", "O")}),
      snap("owner_drop", 1, {"O": ["M"]}, operations={"r": operation("reserve", "O")}, dropped=["m"]),
      snap("reserve_ready", 0, {"O": ["M"]}, operations={"r": operation("permit", "O")}, dropped=["m"]),
      snap("permit_send", 0, {"O": []}, ["M"], dropped=["m"])]),
    ("empty owner still holds and can release a permit", [4, {"o": []}, [],
       [reserve("r"), action("reserve_ready", "r"), owner_drop()]],
     [snap("reserve", 4, {"o": []}, operations={"r": operation("reserve")}),
      snap("reserve_ready", 3, {"o": []}, operations={"r": operation("permit")}),
      snap("owner_drop", 4, {})]),
    ("owner drop preserves another owner's acquired permit", [2, {"A": ["M"], "B": ["N"]}, [],
       [reserve("r", "B"), action("reserve_ready", "r"), send("s", "M", "A"),
        owner_drop("A"), permit_send("r", "N"), RECEIVE]],
     [snap("reserve", 2, {"A": ["M"], "B": ["N"]}, operations={"r": operation("reserve", "B")}),
      snap("reserve_ready", 1, {"A": ["M"], "B": ["N"]}, operations={"r": operation("permit", "B")}),
      snap("send", 1, {"A": [], "B": ["N"]}, operations={"r": operation("permit", "B"), "s": operation("send", "A", "M")}),
      snap("owner_drop", 1, {"B": ["N"]}, operations={"r": operation("permit", "B")}, dropped=["M"]),
      snap("permit_send", 1, {"B": []}, ["N"], dropped=["M"]),
      snap("receive", 2, {"B": []}, dropped=["M"], received=["N"])]),
    ("dropping one permit preserves another held slot", [2, {"o": ["M", "N"]}, [],
       [reserve("r"), action("reserve_ready", "r"), reserve("t"), action("reserve_ready", "t"),
        action("permit_drop", "r"), permit_send("t", "N")]],
     [snap("reserve", 2, {"o": ["M", "N"]}, operations={"r": operation("reserve")}),
      snap("reserve_ready", 1, {"o": ["M", "N"]}, operations={"r": operation("permit")}),
      snap("reserve", 1, {"o": ["M", "N"]}, operations={"r": operation("permit"), "t": operation("reserve")}),
      snap("reserve_ready", 0, {"o": ["M", "N"]}, operations={"r": operation("permit"), "t": operation("permit")}),
      snap("permit_drop", 1, {"o": ["M", "N"]}, operations={"t": operation("permit")}),
      snap("permit_send", 1, {"o": ["M"]}, ["N"])]),
]
CASES.extend([CASES[9], CASES[0]])


def native_types(value):
    if type(value) is dict:
        if any(type(k) is not str for k in value):
            return ["unsupported-dict-key"]
        return ["dict", [[k, native_types(value[k])] for k in sorted(value)]]
    if type(value) is list:
        return ["list", [native_types(v) for v in value]]
    if value is None:
        return "none"
    if type(value) is bool:
        return "bool"
    if type(value) is int:
        return "int"
    if type(value) is str:
        return "str"
    return ["unsupported", type(value).__name__]


def run(candidate):
    payload = base64.b64encode(json.dumps([args for _, args, _ in CASES]).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
def native_types(value):
    if type(value) is dict:
        if any(type(k) is not str for k in value): return ["unsupported-dict-key"]
        return ["dict",[[k,native_types(value[k])] for k in sorted(value)]]
    if type(value) is list: return ["list",[native_types(v) for v in value]]
    if value is None: return "none"
    if type(value) is bool: return "bool"
    if type(value) is int: return "int"
    if type(value) is str: return "str"
    return ["unsupported",type(value).__name__]
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
values=[];unchanged=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args);before=json.dumps(supplied,sort_keys=True);types=native_types(supplied)
    values.append(m.channel_ownership(*supplied))
    unchanged=unchanged and json.dumps(supplied,sort_keys=True)==before and native_types(supplied)==types
print("__RESULT__"+json.dumps({"values":values,"types":[native_types(v) for v in values],"unchanged":unchanged}))'''
    try:
        process = subprocess.run([sys.executable, "-B", "-c", runner,
                                  str(pathlib.Path(candidate).resolve()), payload],
                                 capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if process.returncode == 0 and lines else None
        wanted = [value for _, _, value in CASES]
        expected = {"values": wanted, "types": [native_types(v) for v in wanted], "unchanged": True}
        return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return False


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
