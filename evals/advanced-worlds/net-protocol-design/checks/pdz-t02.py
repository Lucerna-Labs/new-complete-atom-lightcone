import base64
import json
import pathlib
import subprocess
import sys


def frame(opcode, payload="", fin=True):
    return {"opcode": opcode, "fin": fin, "payload": payload}


def wanted(messages=(), pongs=(), pending=None, close=False, error=None):
    return {"messages": list(messages), "pongs": list(pongs), "pending": pending,
            "close_received": close, "error": error}


# Expected results are hand-derived; this file does not invoke a reference oracle.
CASES = [
    ("empty input", [[], 10, 10], wanted()),
    ("empty complete binary", [[frame(2)], 0, 0], wanted([""])),
    ("binary bytes", [[frame(2, "00ff41")], 3, 3], wanted(["00ff41"])),
    ("two messages", [[frame(2, "41"), frame(2, "42")], 1, 1], wanted(["41", "42"])),
    ("unfinished binary", [[frame(2, "4142", False)], 2, 2], wanted(pending="4142")),
    ("empty unfinished binary", [[frame(2, "", False)], 0, 0], wanted(pending="")),
    ("Ping inside fragmentation", [[frame(2, "41", False), frame(9, "7f"), frame(0, "42")], 2, 2], wanted(["4142"], ["7f"])),
    ("multiple controls preserve fragments", [[frame(2, "01", False), frame(9, "aa"), frame(0, "02", False), frame(10, "bb"), frame(9, "cc"), frame(0, "03")], 3, 3], wanted(["010203"], ["aa", "cc"])),
    ("unsolicited Pong has no reply", [[frame(10, "ff")], 1, 0], wanted()),
    ("empty Ping", [[frame(9)], 0, 0], wanted(pongs=[""])),
    ("hex normalization", [[frame(2, "AaFF"), frame(9, "Bc")], 2, 2], wanted(["aaff"], ["bc"])),
    ("control boundary 125", [[frame(9, "ab" * 125)], 125, 0], wanted(pongs=["ab" * 125])),
    ("control 126", [[frame(9, "00" * 126)], 200, 200], wanted(error="invalid_control")),
    ("fragmented Ping", [[frame(9, "", False)], 10, 10], wanted(error="invalid_control")),
    ("fragmented Pong", [[frame(10, "", False)], 10, 10], wanted(error="invalid_control")),
    ("fragmented Close", [[frame(8, "", False)], 10, 10], wanted(error="invalid_control")),
    ("frame cap before message cap", [[frame(2, "010203")], 2, 9], wanted(error="frame_too_large")),
    ("single-frame message cap", [[frame(2, "010203")], 9, 2], wanted(error="message_too_large")),
    ("aggregate cap", [[frame(2, "0102", False), frame(0, "0304")], 2, 3], wanted(error="message_too_large")),
    ("aggregate exact cap", [[frame(2, "0102", False), frame(0, "0304")], 2, 4], wanted(["01020304"])),
    ("aggregate across four fragments", [[frame(2, "01", False), frame(0, "02", False), frame(0, "03", False), frame(0, "04")], 1, 3], wanted(error="message_too_large")),
    ("empty fragments remain active", [[frame(2, "", False), frame(0, "", False), frame(0)], 0, 0], wanted([""])),
    ("orphan final continuation", [[frame(0, "41")], 1, 1], wanted(error="unexpected_continuation")),
    ("orphan nonfinal continuation", [[frame(0, "", False)], 0, 0], wanted(error="unexpected_continuation")),
    ("new binary inside fragmented binary", [[frame(2, "01", False), frame(2, "02")], 2, 2], wanted(error="unexpected_binary")),
    ("empty pending is not no pending", [[frame(2, "", False), frame(2)], 0, 0], wanted(error="unexpected_binary")),
    ("zero message budget", [[frame(2, "01")], 1, 0], wanted(error="message_too_large")),
    ("Ping is outside message budget", [[frame(2, "", False), frame(9, "abcd"), frame(0)], 2, 0], wanted([""], ["abcd"])),
    ("preserve completed message before failure", [[frame(2, "41"), frame(0, "42")], 1, 2], wanted(["41"], error="unexpected_continuation")),
    ("preserve scheduled Pong before failure", [[frame(9, "ff"), frame(0)], 1, 1], wanted(pongs=["ff"], error="unexpected_continuation")),
    ("Close stops before later data", [[frame(8), frame(2, "41")], 1, 1], wanted(close=True)),
    ("Close discards pending and preserves prior output", [[frame(2, "41"), frame(2, "42", False), frame(9, "aa"), frame(8, "03e8"), frame(0, "43")], 2, 2], wanted(["41"], ["aa"], close=True)),
    ("post-Close malformed control ignored", [[frame(8), frame(9, "aa" * 126, False)], 1, 1], wanted(close=True)),
    ("valid Close status and reason", [[frame(8, "03e86f6b")], 4, 0], wanted(close=True)),
    ("invalid Close does not close", [[frame(8, "03e8" + "41" * 124)], 200, 200], wanted(error="invalid_control")),
    ("frame error outranks invalid control", [[frame(9, "aa" * 126, False)], 125, 200], wanted(error="frame_too_large")),
    ("state error outranks aggregate cap", [[frame(2, "", False), frame(2, "01")], 1, 0], wanted(error="unexpected_binary")),
    ("orphan state error outranks message cap", [[frame(0, "01")], 1, 0], wanted(error="unexpected_continuation")),
    ("frame cap also governs controls", [[frame(9, "aabb")], 1, 100], wanted(error="frame_too_large")),
    ("Pong does not complete pending", [[frame(2, "01", False), frame(10, "02")], 2, 2], wanted(pending="01")),
    ("error stops later frames", [[frame(0), frame(2, "01"), frame(8)], 1, 1], wanted(error="unexpected_continuation")),
    ("next message gets independent cap", [[frame(2, "0102", False), frame(0, "0304"), frame(2, "05060708")], 4, 4], wanted(["01020304", "05060708"])),
]
CASES.append(CASES[6])  # The helper must start fresh on every call.


def run(candidate):
    payload = base64.b64encode(json.dumps([case[1] for case in CASES]).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
cases=json.loads(base64.b64decode(sys.argv[2]));values=[];unchanged=True
for args in cases:
    copied=copy.deepcopy(args)
    values.append(module.assemble_binary(*copied))
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
