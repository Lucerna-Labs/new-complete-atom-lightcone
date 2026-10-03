import base64
import json
import pathlib
import subprocess
import sys


def sense(physical=False, virtual=False):
    return {"kind": "sense", "physical_busy": physical, "virtual_busy": virtual}


def elapse(us):
    return {"kind": "elapse", "us": us}


def state(time, counter, busy, idle, eligible=False):
    return {"at_us": time, "counter": counter, "joint_busy": busy,
            "idle_us": idle, "eligible": eligible}


# State timelines and CW arithmetic are hand-derived, not reference-generated.
CASES = [
    ("empty", [2, 4, 3, []], []),
    ("zero counter still waits DIFS", [0, 4, 3, [elapse(0), elapse(3), elapse(1)]],
     [state(0, 0, False, 0), state(3, 0, False, 3), state(4, 0, False, 4, True)]),
    ("whole slot required", [1, 4, 3, [elapse(4), elapse(2), elapse(1)]],
     [state(4, 1, False, 4), state(6, 1, False, 6), state(7, 0, False, 7, True)]),
    ("one interval covers three slots", [3, 4, 3, [elapse(13)]], [state(13, 0, False, 13, True)]),
    ("counter clamps without transmitting", [2, 4, 3, [elapse(100)]], [state(100, 0, False, 100, True)]),
    ("physical busy then new DIFS", [2, 4, 3, [sense(True), elapse(20), sense(), elapse(3), elapse(1), elapse(3), elapse(3)]],
     [state(0, 2, True, 0), state(20, 2, True, 0), state(20, 2, False, 0), state(23, 2, False, 3), state(24, 2, False, 4), state(27, 1, False, 7), state(30, 0, False, 10, True)]),
    ("virtual busy ignores prior physical idle", [1, 4, 3, [sense(False, True), elapse(10), sense(), elapse(4), elapse(3)]],
     [state(0, 1, True, 0), state(10, 1, True, 0), state(10, 1, False, 0), state(14, 1, False, 4), state(17, 0, False, 7, True)]),
    ("busy gate handoff remains busy", [1, 2, 2, [sense(True), elapse(5), sense(False, True), elapse(5), sense(), elapse(1), elapse(1), elapse(2)]],
     [state(0, 1, True, 0), state(5, 1, True, 0), state(5, 1, True, 0), state(10, 1, True, 0), state(10, 1, False, 0), state(11, 1, False, 1), state(12, 1, False, 2), state(14, 0, False, 4, True)]),
    ("retain decremented residual", [3, 4, 3, [elapse(7), sense(True), elapse(10), sense(), elapse(4), elapse(3), elapse(3)]],
     [state(7, 2, False, 7), state(7, 2, True, 0), state(17, 2, True, 0), state(17, 2, False, 0), state(21, 2, False, 4), state(24, 1, False, 7), state(27, 0, False, 10, True)]),
    ("discard interrupted partial slot", [1, 4, 3, [elapse(6), sense(False, True), elapse(10), sense(), elapse(5), elapse(2)]],
     [state(6, 1, False, 6), state(6, 1, True, 0), state(16, 1, True, 0), state(16, 1, False, 0), state(21, 1, False, 5), state(23, 0, False, 7, True)]),
    ("repeated idle sense preserves epoch", [1, 4, 3, [elapse(6), sense(), elapse(1)]],
     [state(6, 1, False, 6), state(6, 1, False, 6), state(7, 0, False, 7, True)]),
    ("zero counter loses eligibility when busy", [0, 4, 3, [elapse(4), sense(True), elapse(2), sense(), elapse(3), elapse(1)]],
     [state(4, 0, False, 4, True), state(4, 0, True, 0), state(6, 0, True, 0), state(6, 0, False, 0), state(9, 0, False, 3), state(10, 0, False, 4, True)]),
    ("busy interrupts incomplete DIFS", [1, 4, 3, [elapse(3), sense(True, True), elapse(1), sense(), elapse(3), elapse(1), elapse(3)]],
     [state(3, 1, False, 3), state(3, 1, True, 0), state(4, 1, True, 0), state(4, 1, False, 0), state(7, 1, False, 3), state(8, 1, False, 4), state(11, 0, False, 7, True)]),
    ("subdivided idle time accumulates", [2, 4, 3, [elapse(2), elapse(2), elapse(1), elapse(1), elapse(1), elapse(3)]],
     [state(2, 2, False, 2), state(4, 2, False, 4), state(5, 2, False, 5), state(6, 2, False, 6), state(7, 1, False, 7), state(10, 0, False, 10, True)]),
    ("completed slots are charged only once", [5, 4, 3, [elapse(7), elapse(0), elapse(1), elapse(2), elapse(3)]],
     [state(7, 4, False, 7), state(7, 4, False, 7), state(8, 4, False, 8), state(10, 3, False, 10), state(13, 2, False, 13)]),
    ("ordered boundary update closes gate", [1, 4, 3, [elapse(7), sense(True), elapse(0), sense(), elapse(4)]],
     [state(7, 0, False, 7, True), state(7, 0, True, 0), state(7, 0, True, 0), state(7, 0, False, 0), state(11, 0, False, 4, True)]),
    ("two idle indications do not restart partial slot", [2, 4, 3, [elapse(5), sense(), sense(), elapse(2)]],
     [state(5, 2, False, 5), state(5, 2, False, 5), state(5, 2, False, 5), state(7, 1, False, 7)]),
    ("named 34 and 9 microsecond profile", [2, 34, 9, [elapse(33), elapse(1), elapse(8), elapse(1), elapse(9)]],
     [state(33, 2, False, 33), state(34, 2, False, 34), state(42, 2, False, 42), state(43, 1, False, 43), state(52, 0, False, 52, True)]),
    ("unit time inputs", [3, 1, 1, [elapse(1), elapse(1), elapse(1), elapse(1), elapse(1)]],
     [state(1, 3, False, 1), state(2, 2, False, 2), state(3, 1, False, 3), state(4, 0, False, 4, True), state(5, 0, False, 5, True)]),
    ("large integer inputs", [65535, 1000000, 1000000, [elapse(1000000), elapse(1000000)]],
     [state(1000000, 65535, False, 1000000), state(2000000, 65534, False, 2000000)]),
]
CASES.append(CASES[8])
CW_CASES = [
    (("failure", 15, 15, 1023), 31), (("failure", 31, 15, 1023), 63),
    (("failure", 511, 15, 1023), 1023), (("failure", 1023, 15, 1023), 1023),
    (("success", 1023, 15, 1023), 15), (("success", 15, 15, 1023), 15),
    (("failure", 7, 3, 15), 15), (("failure", 15, 3, 15), 15),
    (("success", 7, 3, 15), 3), (("failure", 0, 0, 1), 1),
    (("failure", 1, 0, 1), 1), (("success", 1, 0, 1), 0),
    (("failure", 0, 0, 0), 0), (("success", 0, 0, 0), 0),
    (("failure", 32767, 15, 65535), 65535), (("failure", 65535, 15, 65535), 65535),
    (("success", 65535, 3, 65535), 3), (("failure", 1, 1, 65535), 3),
    (("failure", 63, 15, 1023), 127), (("success", 31, 15, 1023), 15),
]


def run(candidate):
    inputs = [[args for _, args, _ in CASES], [args for args, _ in CW_CASES]]
    payload = base64.b64encode(json.dumps(inputs).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
cases,cws=json.loads(base64.b64decode(sys.argv[2]));values=[];unchanged=True
for args in cases:
    supplied=copy.deepcopy(args);values.append(module.dcf_backoff(*supplied));unchanged=unchanged and json.dumps(supplied,sort_keys=True)==json.dumps(args,sort_keys=True)
cw_values=[module.cw_after(*args) for args in cws]
print("__RESULT__"+json.dumps({"values":values,"cws":cw_values,"unchanged":unchanged}))'''
    try:
        result = subprocess.run([sys.executable, "-B", "-c", runner,
                                 str(pathlib.Path(candidate).resolve()), payload],
                                capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in result.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if result.returncode == 0 and lines else None
        expected = {"values": [value for _, _, value in CASES],
                    "cws": [value for _, value in CW_CASES], "unchanged": True}
        return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return False


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
