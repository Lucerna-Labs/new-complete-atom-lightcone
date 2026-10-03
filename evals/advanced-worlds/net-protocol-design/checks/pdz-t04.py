import base64
import json
import pathlib
import subprocess
import sys


K = ["c", "i", "r"]
Q = ["c", "i", "q"]


def begin(attempt, delta=1, key=K):
    return {"op": "begin", "attempt": attempt, "client": key[0],
            "incarnation": key[1], "request": key[2], "delta": delta}


def commit(attempt, reply=True):
    return {"op": "commit", "attempt": attempt, "reply": reply}


def evict(key=K):
    return {"op": "evict", "client": key[0], "incarnation": key[1], "request": key[2]}


def eb(attempt):
    return {"op": "begin", "attempt": attempt, "status": "pending"}


def ec(attempt, status, reply=None):
    return {"op": "commit", "attempt": attempt, "status": status, "reply": reply}


def crash(*discarded):
    return {"op": "crash", "discarded": list(discarded)}


def ee(removed, key=K):
    return {"op": "evict", "key": list(key), "removed": removed}


def record(delta, result, key=K):
    return {"key": list(key), "delta": delta, "result": result}


def pending(attempt, delta=1, key=K):
    return {"attempt": attempt, "key": list(key), "delta": delta}


def wanted(counter, records=(), pending_items=(), events=()):
    return {"counter": counter, "records": list(records),
            "pending": list(pending_items), "events": list(events)}


# Static expected events and arithmetic were derived by hand, not by the reference.
CASES = [
    ("empty", [7, []], wanted(7)),
    ("begin is not execution", [0, [begin("a", 4)]], wanted(0, pending_items=[pending("a", 4)], events=[eb("a")])),
    ("one commit", [10, [begin("a", 3), commit("a")]], wanted(13, [record(3, 13)], events=[eb("a"), ec("a", "committed", 13)])),
    ("reply loss after commit", [0, [begin("a", 7), commit("a", False)]], wanted(7, [record(7, 7)], events=[eb("a"), ec("a", "committed")])),
    ("retry after lost reply", [0, [begin("a", 7), commit("a", False), begin("b", 7), commit("b")]], wanted(7, [record(7, 7)], events=[eb("a"), ec("a", "committed"), eb("b"), ec("b", "replayed", 7)])),
    ("ordinary duplicate", [0, [begin("a", 2), commit("a"), begin("b", 2), commit("b")]], wanted(2, [record(2, 2)], events=[eb("a"), ec("a", "committed", 2), eb("b"), ec("b", "replayed", 2)])),
    ("original result not current counter", [0, [begin("a", 2), commit("a"), begin("b", 10, Q), commit("b"), begin("c", 2), commit("c")]], wanted(12, [record(10, 12, Q), record(2, 2)], events=[eb("a"), ec("a", "committed", 2), eb("b"), ec("b", "committed", 12), eb("c"), ec("c", "replayed", 2)])),
    ("changed payload conflicts", [0, [begin("a", 2), commit("a"), begin("b", 3), commit("b")]], wanted(2, [record(2, 2)], events=[eb("a"), ec("a", "committed", 2), eb("b"), ec("b", "conflict")])),
    ("two same-key begins then commits", [0, [begin("a", 4), begin("b", 4), commit("a"), commit("b")]], wanted(4, [record(4, 4)], events=[eb("a"), eb("b"), ec("a", "committed", 4), ec("b", "replayed", 4)])),
    ("competing payloads winner commits first", [0, [begin("a", 2), begin("b", 3), commit("b"), commit("a")]], wanted(3, [record(3, 3)], events=[eb("a"), eb("b"), ec("b", "committed", 3), ec("a", "conflict")])),
    ("independent commits follow commit order", [0, [begin("a", 1), begin("b", 10, Q), commit("b"), commit("a")]], wanted(11, [record(10, 10, Q), record(1, 11)], events=[eb("a"), eb("b"), ec("b", "committed", 10), ec("a", "committed", 11)])),
    ("crash drops staged work", [5, [begin("z", 2), begin("a", 3, Q), {"op": "crash"}, commit("z")]], wanted(5, events=[eb("z"), eb("a"), crash("a", "z"), ec("z", "missing")])),
    ("committed state survives crash", [0, [begin("a", 5), commit("a", False), begin("b", 5), {"op": "crash"}, begin("c", 5), commit("c")]], wanted(5, [record(5, 5)], events=[eb("a"), ec("a", "committed"), eb("b"), crash("b"), eb("c"), ec("c", "replayed", 5)])),
    ("empty crashes", [-2, [{"op": "crash"}, {"op": "crash"}]], wanted(-2, events=[crash(), crash()])),
    ("eviction permits late repeated effect", [0, [begin("a"), commit("a"), evict(), begin("b"), commit("b")]], wanted(2, [record(1, 2)], events=[eb("a"), ec("a", "committed", 1), ee(True), eb("b"), ec("b", "committed", 2)])),
    ("eviction preserves unrelated retained record", [0, [begin("a", 2), commit("a"), begin("b", 10, Q), commit("b"), evict(), begin("c", 10, Q), commit("c"), begin("d", 2), commit("d")]], wanted(14, [record(10, 12, Q), record(2, 14)], events=[eb("a"), ec("a", "committed", 2), eb("b"), ec("b", "committed", 12), ee(True), eb("c"), ec("c", "replayed", 12), eb("d"), ec("d", "committed", 14)])),
    ("evict absent key", [3, [evict()]], wanted(3, events=[ee(False)])),
    ("eviction does not discard pending", [0, [begin("a", 2), evict(), commit("a")]], wanted(2, [record(2, 2)], events=[eb("a"), ee(False), ec("a", "committed", 2)])),
    ("lookup after intervening eviction", [0, [begin("a", 2), commit("a"), begin("b", 2), evict(), commit("b")]], wanted(4, [record(2, 4)], events=[eb("a"), ec("a", "committed", 2), eb("b"), ee(True), ec("b", "committed", 4)])),
    ("client participates in key", [0, [begin("a", 1), commit("a"), begin("b", 1, ["d", "i", "r"]), commit("b")]], wanted(2, [record(1, 1), record(1, 2, ["d", "i", "r"])], events=[eb("a"), ec("a", "committed", 1), eb("b"), ec("b", "committed", 2)])),
    ("incarnation participates in key", [0, [begin("a", 1), commit("a"), begin("b", 1, ["c", "j", "r"]), commit("b")]], wanted(2, [record(1, 1), record(1, 2, ["c", "j", "r"])], events=[eb("a"), ec("a", "committed", 1), eb("b"), ec("b", "committed", 2)])),
    ("request participates in key", [0, [begin("a", 1), commit("a"), begin("b", 1, Q), commit("b")]], wanted(2, [record(1, 2, Q), record(1, 1)], events=[eb("a"), ec("a", "committed", 1), eb("b"), ec("b", "committed", 2)])),
    ("negative and zero deltas", [10, [begin("a", -3), commit("a"), begin("b", 0, Q), commit("b"), begin("c", -3), commit("c")]], wanted(7, [record(0, 7, Q), record(-3, 7)], events=[eb("a"), ec("a", "committed", 7), eb("b"), ec("b", "committed", 7), eb("c"), ec("c", "replayed", 7)])),
    ("attempt consumed by commit", [0, [begin("a"), commit("a"), commit("a")]], wanted(1, [record(1, 1)], events=[eb("a"), ec("a", "committed", 1), ec("a", "missing")])),
    ("pending sorted by attempt", [0, [begin("z", 5), begin("a", 7, Q)]], wanted(0, pending_items=[pending("a", 7, Q), pending("z", 5)], events=[eb("z"), eb("a")])),
    ("unknown commit", [8, [commit("missing")]], wanted(8, events=[ec("missing", "missing")])),
    ("zero result is still retained", [-3, [begin("a", 3), commit("a"), begin("b", 3), commit("b")]], wanted(0, [record(3, 0)], events=[eb("a"), ec("a", "committed", 0), eb("b"), ec("b", "replayed", 0)])),
    ("eviction and crash keep counter", [0, [begin("a", 4), commit("a"), evict(), {"op": "crash"}, begin("b", 4), commit("b")]], wanted(8, [record(4, 8)], events=[eb("a"), ec("a", "committed", 4), ee(True), crash(), eb("b"), ec("b", "committed", 8)])),
    ("replayed reply can also be lost", [0, [begin("a", 2), commit("a"), begin("b", 2), commit("b", False)]], wanted(2, [record(2, 2)], events=[eb("a"), ec("a", "committed", 2), eb("b"), ec("b", "replayed")])),
    ("opaque key is case sensitive", [0, [begin("a", 1), commit("a"), begin("b", 1, ["C", "i", "r"]), commit("b")]], wanted(2, [record(1, 2, ["C", "i", "r"]), record(1, 1)], events=[eb("a"), ec("a", "committed", 1), eb("b"), ec("b", "committed", 2)])),
    ("conflict also consumes attempt", [0, [begin("a", 2), commit("a"), begin("b", 3), commit("b"), commit("b")]], wanted(2, [record(2, 2)], events=[eb("a"), ec("a", "committed", 2), eb("b"), ec("b", "conflict"), ec("b", "missing")])),
]
CASES.append(CASES[8])  # No persistent state may leak between function calls.


def run(candidate):
    payload = base64.b64encode(json.dumps([case[1] for case in CASES]).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
cases=json.loads(base64.b64decode(sys.argv[2]));values=[];unchanged=True
for args in cases:
    copied=copy.deepcopy(args)
    values.append(module.simulate_invocations(*copied))
    unchanged=unchanged and copied==args
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged}))'''
    try:
        result = subprocess.run([sys.executable, "-B", "-c", runner,
                                 str(pathlib.Path(candidate).resolve()), payload],
                                capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in result.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if result.returncode == 0 and lines else None
        expected = {"values": [case[2] for case in CASES], "unchanged": True}
        return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return False


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
