import base64
import json
import math
import pathlib
import subprocess
import sys


def attempt(submitted, returned, accepted, remaining):
    return {"submitted": list(submitted), "returned": returned,
            "accepted": list(accepted), "remaining": list(remaining)}


def wanted(packets, count, overhead, attempts=(), transferred=(), caller_owned=()):
    return {"rx": {"packets": list(packets), "count": count,
                   "wait_for_more": False, "amortized_overhead_ns": overhead},
            "tx": {"attempts": list(attempts), "transferred": list(transferred),
                   "caller_owned": list(caller_owned), "peer_delivery": "unknown"}}


# Expected prefixes, ownership sets, and cost denominators are specified by hand.
CASES = [
    ("empty RX return", [32, [], 120, []], wanted([], 0, None)),
    ("empty RX and zero cost", [1, [], 0, []], wanted([], 0, None)),
    ("underfilled observed burst", [8, ["a", "b", "c"], 120, []], wanted(["a", "b", "c"], 3, 40, caller_owned=["a", "b", "c"])),
    ("same count at full maximum", [3, ["a", "b", "c"], 120, []], wanted(["a", "b", "c"], 3, 40, caller_owned=["a", "b", "c"])),
    ("single packet accepted", [64, ["x"], 7, [1]], wanted(["x"], 1, 7, [attempt(["x"], 1, ["x"], [])], ["x"])),
    ("partial acceptance", [8, ["a", "b", "c"], 90, [1]], wanted(["a", "b", "c"], 3, 30, [attempt(["a", "b", "c"], 1, ["a"], ["b", "c"])], ["a"], ["b", "c"])),
    ("zero acceptance retains every packet", [8, ["a", "b", "c"], 90, [0]], wanted(["a", "b", "c"], 3, 30, [attempt(["a", "b", "c"], 0, [], ["a", "b", "c"])], caller_owned=["a", "b", "c"])),
    ("retry only unaccepted suffix", [8, ["a", "b", "c"], 90, [1, 2]], wanted(["a", "b", "c"], 3, 30, [attempt(["a", "b", "c"], 1, ["a"], ["b", "c"]), attempt(["b", "c"], 2, ["b", "c"], [])], ["a", "b", "c"])),
    ("zero return between partial attempts", [8, ["a", "b", "c", "d"], 80, [1, 0, 2]], wanted(["a", "b", "c", "d"], 4, 20, [attempt(["a", "b", "c", "d"], 1, ["a"], ["b", "c", "d"]), attempt(["b", "c", "d"], 0, [], ["b", "c", "d"]), attempt(["b", "c", "d"], 2, ["b", "c"], ["d"])], ["a", "b", "c"], ["d"])),
    ("whole observed burst accepted", [8, ["a", "b", "c"], 30, [3]], wanted(["a", "b", "c"], 3, 10, [attempt(["a", "b", "c"], 3, ["a", "b", "c"], [])], ["a", "b", "c"])),
    ("repeated zero returns", [8, ["a", "b", "c"], 30, [0, 0]], wanted(["a", "b", "c"], 3, 10, [attempt(["a", "b", "c"], 0, [], ["a", "b", "c"]), attempt(["a", "b", "c"], 0, [], ["a", "b", "c"])], caller_owned=["a", "b", "c"])),
    ("zero then full return", [8, ["a", "b", "c"], 30, [0, 3]], wanted(["a", "b", "c"], 3, 10, [attempt(["a", "b", "c"], 0, [], ["a", "b", "c"]), attempt(["a", "b", "c"], 3, ["a", "b", "c"], [])], ["a", "b", "c"])),
    ("four advancing prefixes", [9, ["a", "b", "c", "d", "e"], 100, [2, 1, 1, 1]], wanted(["a", "b", "c", "d", "e"], 5, 20, [attempt(["a", "b", "c", "d", "e"], 2, ["a", "b"], ["c", "d", "e"]), attempt(["c", "d", "e"], 1, ["c"], ["d", "e"]), attempt(["d", "e"], 1, ["d"], ["e"]), attempt(["e"], 1, ["e"], [])], ["a", "b", "c", "d", "e"])),
    ("zero fixed overhead is defined for nonempty return", [8, ["a", "b"], 0, [1]], wanted(["a", "b"], 2, 0, [attempt(["a", "b"], 1, ["a"], ["b"])], ["a"], ["b"])),
    ("fractional cost uses actual count", [100, ["a", "b", "c"], 10, []], wanted(["a", "b", "c"], 3, 10 / 3, caller_owned=["a", "b", "c"])),
    ("large requested maximum is not a denominator", [256, ["x"], 1000000, []], wanted(["x"], 1, 1000000, caller_owned=["x"])),
    ("packet order is not sorted", [8, ["z", "a", "m"], 12, [1, 1]], wanted(["z", "a", "m"], 3, 4, [attempt(["z", "a", "m"], 1, ["z"], ["a", "m"]), attempt(["a", "m"], 1, ["a"], ["m"])], ["z", "a"], ["m"])),
    ("opaque IDs are case sensitive", [8, ["x", "X"], 6, [1]], wanted(["x", "X"], 2, 3, [attempt(["x", "X"], 1, ["x"], ["X"])], ["x"], ["X"])),
    ("zeros do not reset retry ownership", [8, ["a", "b"], 20, [0, 1, 0, 1]], wanted(["a", "b"], 2, 10, [attempt(["a", "b"], 0, [], ["a", "b"]), attempt(["a", "b"], 1, ["a"], ["b"]), attempt(["b"], 0, [], ["b"]), attempt(["b"], 1, ["b"], [])], ["a", "b"])),
    ("eight submitted five accepted", [32, ["a", "b", "c", "d", "e", "f", "g", "h"], 800, [5]], wanted(["a", "b", "c", "d", "e", "f", "g", "h"], 8, 100, [attempt(["a", "b", "c", "d", "e", "f", "g", "h"], 5, ["a", "b", "c", "d", "e"], ["f", "g", "h"])], ["a", "b", "c", "d", "e"], ["f", "g", "h"])),
    ("two partial returns leave final suffix", [8, ["a", "b", "c", "d", "e", "f"], 60, [2, 2]], wanted(["a", "b", "c", "d", "e", "f"], 6, 10, [attempt(["a", "b", "c", "d", "e", "f"], 2, ["a", "b"], ["c", "d", "e", "f"]), attempt(["c", "d", "e", "f"], 2, ["c", "d"], ["e", "f"])], ["a", "b", "c", "d"], ["e", "f"])),
]
CASES.append(CASES[7])


def matches(actual, expected):
    try:
        if (type(actual) is not dict or type(actual.get("unchanged")) is not bool
                or not actual["unchanged"] or actual.get("snapshot_stable") is not True):
            return False
        if type(actual.get("values")) is not list or len(actual["values"]) != len(expected):
            return False
        for value, wanted_value in zip(actual["values"], expected):
            a = value["rx"]["amortized_overhead_ns"]
            e = wanted_value["rx"]["amortized_overhead_ns"]
            if e is None:
                if a is not None:
                    return False
            elif type(a) not in (int, float) or not math.isfinite(a) or not math.isclose(a, e, rel_tol=1e-12, abs_tol=1e-12):
                return False
            # All ownership, ordering, counts, and booleans require exact types
            # and values; only the modeled division permits numeric tolerance.
            normalized = json.loads(json.dumps(value))
            normalized["rx"]["amortized_overhead_ns"] = e
            if json.dumps(normalized, sort_keys=True) != json.dumps(wanted_value, sort_keys=True):
                return False
        return set(actual) == {"values", "unchanged", "snapshot_stable"}
    except (KeyError, TypeError, ValueError, OverflowError):
        return False


def run(candidate):
    payload = base64.b64encode(json.dumps([args for _, args, _ in CASES]).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
values=[];unchanged=True;snapshot_stable=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    copied=copy.deepcopy(args);value=module.burst_handoff(*copied);values.append(value);unchanged=unchanged and copied==args
    before=json.dumps(value,sort_keys=True);copied[1].append("_postcall_rx_");copied[3].append(0)
    snapshot_stable=snapshot_stable and json.dumps(value,sort_keys=True)==before
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged,"snapshot_stable":snapshot_stable}))'''
    try:
        result = subprocess.run([sys.executable, "-B", "-c", runner,
                                 str(pathlib.Path(candidate).resolve()), payload],
                                capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in result.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if result.returncode == 0 and lines else None
        return matches(actual, [value for _, _, value in CASES])
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return False


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
