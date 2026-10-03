import base64
import json
import pathlib
import subprocess
import sys


def region(data="00000000", context="ctx", write=True, base=100):
    return {"data": data, "context": context, "write": write, "base": base}


def segment(offset, data="ff", tag="T", context="ctx"):
    return {"tag": tag, "context": context, "offset": offset, "data": data}


def event(status, written=0, tag="T"):
    return {"tag": tag, "status": status, "written": written}


def case(regions, segments, final, events):
    return ((regions, segments), {"regions": final, "events": events})


# Literal final memory and event oracles. Positive payloads only: zero-length
# protocol-operation rules, NIC behavior, and transport termination are excluded.
CASES = [
    case({}, [], {}, []),
    case({"T": region("AaBb")}, [], {"T": "aabb"}, []),
    case({"T": region()}, [segment(101, "aabb")], {"T": "00aabb00"},
         [event("placed", 2)]),
    case({"T": region()}, [segment(100, "11223344")], {"T": "11223344"},
         [event("placed", 4)]),
    case({"T": region()}, [segment(103)], {"T": "000000ff"}, [event("placed", 1)]),
    case({"T": region()}, [segment(100)], {"T": "ff000000"}, [event("placed", 1)]),
    case({"T": region()}, [segment(99)], {"T": "00000000"}, [event("out-of-bounds")]),
    case({"T": region()}, [segment(99, "aabb")], {"T": "00000000"},
         [event("out-of-bounds")]),
    case({"T": region()}, [segment(104)], {"T": "00000000"}, [event("out-of-bounds")]),
    case({"T": region()}, [segment(102, "aabbcc")], {"T": "00000000"},
         [event("out-of-bounds")]),
    case({"T": region()}, [segment(101, tag="U")], {"T": "00000000"},
         [event("unknown-tag", tag="U")]),
    case({"T": region()}, [segment(101, context="elsewhere")], {"T": "00000000"},
         [event("wrong-context")]),
    case({"T": region(write=False)}, [segment(101)], {"T": "00000000"},
         [event("write-denied")]),
    case({"T": region(write=False)}, [segment(104, context="elsewhere")],
         {"T": "00000000"}, [event("wrong-context")]),
    case({"T": region(write=False)}, [segment(104)], {"T": "00000000"},
         [event("write-denied")]),
    case({}, [segment(18446744073709551615, "aabb", tag="U", context="elsewhere")],
         {}, [event("unknown-tag", tag="U")]),
    case({"T": region()}, [segment(100, "1122"), segment(103, "aabb"),
                            segment(102, "3344"), segment(101, "fe")],
         {"T": "11fe3344"}, [event("placed", 2), event("out-of-bounds"),
                               event("placed", 2), event("placed", 1)]),
    case({"A": region("0000", "a", base=0), "B": region("ffff", "b", base=0)},
         [segment(0, "12", "A", "b"), segment(0, "34", "B", "b"),
          segment(1, "56", "A", "a")],
         {"A": "0056", "B": "34ff"}, [event("wrong-context", tag="A"),
         event("placed", 1, "B"), event("placed", 1, "A")]),
    case({"T": region("0000", "P", base=0), "t": region("ffff", "p", base=0)},
         [segment(0, "aa", "T", "p"), segment(0, "aa", "t", "p"),
          segment(1, "bb", "T", "P")],
         {"T": "00bb", "t": "aaff"}, [event("wrong-context"),
         event("placed", 1, "t"), event("placed", 1)]),
    case({"A": region("0000", write=False, base=0), "B": region("ffff", base=0)},
         [segment(0, "aa", "A"), segment(0, "bb", "B")],
         {"A": "0000", "B": "bbff"}, [event("write-denied", tag="A"),
         event("placed", 1, "B")]),
    case({"T": region("01020304", base=200)}, [segment(202, "Ff")],
         {"T": "0102ff04"}, [event("placed", 1)]),
    case({"T": region(base=18446744073709551612)},
         [segment(18446744073709551614, "abcd"),
          segment(18446744073709551615, "ef01"),
          segment(18446744073709551615, "22"), segment(0)],
         {"T": "0000ab22"}, [event("placed", 2), event("out-of-bounds"),
                               event("placed", 1), event("out-of-bounds")]),
    case({"T": region(base=0)}, [segment(18446744073709551615, "aabb")],
         {"T": "00000000"}, [event("out-of-bounds")]),
    case({"T": region("aa", base=18446744073709551615)},
         [segment(18446744073709551615)], {"T": "ff"}, [event("placed", 1)]),
    case({"T": region("00" * 32, base=0)}, [segment(0, "ab" * 32)],
         {"T": "ab" * 32}, [event("placed", 32)]),
    case({"T": region("aa")}, [segment(100), segment(101)],
         {"T": "ff"}, [event("placed", 1), event("out-of-bounds")]),
    case({"T": region()}, [], {"T": "00000000"}, []),
    case({"A": region("0000", "a", base=0),
          "B": region("ffff", "b", write=False, base=0)},
         [segment(0, "aa", "A", "a"), segment(0, "bb", "U", "a"),
          segment(1, "cc", "A", "b"), segment(0, "dd", "B", "b"),
          segment(1, "eeff", "A", "a"), segment(1, "bb", "A", "a")],
         {"A": "aabb", "B": "ffff"}, [event("placed", 1, "A"),
         event("unknown-tag", tag="U"), event("wrong-context", tag="A"),
         event("write-denied", tag="B"), event("out-of-bounds", tag="A"),
         event("placed", 1, "A")]),
    case({"T": region()}, [segment(4294967396)], {"T": "00000000"},
         [event("out-of-bounds")]),
    case({"T": region()}, [segment(101, "aabb"), segment(100, "1122")],
         {"T": "1122bb00"}, [event("placed", 2), event("placed", 2)]),
]
EXPECTED = {"values": [value for _, value in CASES], "unchanged": True}


def run(candidate):
    payload = base64.b64encode(json.dumps(CASES).encode()).decode()
    runner = r'''import base64, copy, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
values, unchanged = [], True
for args, _ in json.loads(base64.b64decode(sys.argv[2])):
    supplied = copy.deepcopy(args)
    values.append(module.place_segments(*supplied))
    unchanged = unchanged and supplied == args
print("__RESULT__" + json.dumps({"values": values, "unchanged": unchanged}))'''
    try:
        process = subprocess.run(
            [sys.executable, "-B", "-c", runner,
             str(pathlib.Path(candidate).resolve()), payload],
            capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if process.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


def passes(result):
    if result != EXPECTED or result["unchanged"] is not True:
        return False
    return all(type(e["written"]) is int
               for value in result["values"] for e in value["events"])


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and passes(run(sys.argv[1])) else 1)
