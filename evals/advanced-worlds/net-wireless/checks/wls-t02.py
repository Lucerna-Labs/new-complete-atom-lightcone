import base64
import json
import math
import pathlib
import subprocess
import sys


def pairs(values):
    return [[complex(value).real, complex(value).imag] for value in values]


def case(blocks, taps, cp_len, useful, bins, gains, covered):
    return ({"blocks": [pairs(row) for row in blocks], "taps": pairs(taps),
             "cp_len": cp_len},
            {"useful_samples": [pairs(row) for row in useful],
             "received_bins": [pairs(row) for row in bins],
             "channel_bins": pairs(gains), "prefix_covers_memory": covered})


# Hand-derived small transforms, impulses, constant waveforms, and pure tones.
# The checker does not implement the candidate's convolution or DFT algorithm.
CASES = [
    case([[2, 0]], [1], 0, [[1, 1]], [[2, 0]], [1, 1], True),
    case([[2, 0]], [1, 1], 0, [[1, 2]], [[3, -1]], [2, 0], False),
    case([[2, 0]], [1, 1], 1, [[2, 2]], [[4, 0]], [2, 0], True),
    case([[2, 0], [4, 0]], [1, 1], 0,
         [[1, 2], [3, 4]], [[3, -1], [7, -1]], [2, 0], False),
    case([[1, -1], [0, 0]], [0, 1], 0,
         [[0, 0], [1, 0]], [[0, 0], [1, 1]], [1, -1], False),
    case([[4, 0, 0, 0], [8, 0, 0, 0]], [1, 2, 3], 1,
         [[3, 6, 6, 6], [9, 12, 12, 12]],
         [[21, -3, -3, -3], [45, -3, -3, -3]],
         [6, -2-2j, 2, -2+2j], False),
    case([[4, 0, 0, 0], [8, 0, 0, 0]], [1, 2, 3], 2,
         [[6, 6, 6, 6], [12, 12, 12, 12]],
         [[24, 0, 0, 0], [48, 0, 0, 0]],
         [6, -2-2j, 2, -2+2j], True),
    case([[0, 4, 0, 0]], [1, 1], 1,
         [[1-1j, 1+1j, -1+1j, -1-1j]], [[0, 4-4j, 0, 0]],
         [2, 1-1j, 0, 1+1j], True),
    case([[0, 0, 4, 0]], [1, 1], 1,
         [[0, 0, 0, 0]], [[0, 0, 0, 0]], [2, 1-1j, 0, 1+1j], True),
    case([[2+2j, 2-2j]], [1j], 0,
         [[2j, -2]], [[-2+2j, 2+2j]], [1j, 1j], True),
    case([[1, 2, 3, 4]], [1, 0, 0, 0, 1], 4,
         [[5, -1-1j, -1, -1+1j]], [[2, 4, 6, 8]], [2, 2, 2, 2], True),
    case([[2, 2]], [1, -1], 1, [[2, -2]], [[0, 4]], [0, 2], True),
    case([[3, 0, 0]], [1, 1], 1,
         [[2, 2, 2]], [[6, 0, 0]],
         [2, 0.5-0.5j*math.sqrt(3), 0.5+0.5j*math.sqrt(3)], True),
    case([[1]*32], [1], 32, [[1]+[0]*31], [[1]*32], [1]*32, True),
    case([[0, 0], [2, 0], [0, 0], [4, 0]], [0, 1], 0,
         [[0, 0], [0, 1], [1, 0], [0, 2]],
         [[0, 0], [1, -1], [1, 1], [2, -2]], [1, -1], False),
    case([[2j, 0], [4, 0]], [1, 1j], 0,
         [[1j, -1+1j], [1, 2+2j]],
         [[-1+2j, 1], [3+2j, -1-2j]], [1+1j, 1-1j], False),
    case([[2, 0], [4, 0]], [0, 0, 1], 0,
         [[0, 0], [1, 1]], [[0, 0], [2, 0]], [1, 1], False),
    case([[0, 0, 0], [0, 0, 0]], [1, 0, -1], 0,
         [[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0]],
         [0, 1.5-0.5j*math.sqrt(3), 1.5+0.5j*math.sqrt(3)], False),
]
CALLS = CASES + CASES[:2] + list(reversed(CASES[:3]))
EXPECTED = [expected for _, expected in CALLS]


def run(candidate):
    payload = base64.b64encode(json.dumps([args for args, _ in CALLS]).encode()).decode()
    runner = r'''import base64, copy, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("candidate", sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
calls = json.loads(base64.b64decode(sys.argv[2]))
values, unchanged = [], True
for args in calls:
    supplied = copy.deepcopy(args)
    values.append(module.ofdm_blocks(**supplied))
    unchanged = unchanged and json.dumps(supplied, sort_keys=True) == json.dumps(args, sort_keys=True)
print("__RESULT__" + json.dumps({"values": values, "unchanged": unchanged}))'''
    try:
        process = subprocess.run([sys.executable, "-B", "-c", runner,
                                  str(pathlib.Path(candidate).resolve()), payload],
                                 capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if process.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


def same(actual, expected):
    if isinstance(expected, dict):
        return (isinstance(actual, dict) and set(actual) == set(expected)
                and all(same(actual[key], value) for key, value in expected.items()))
    if isinstance(expected, list):
        return (isinstance(actual, list) and len(actual) == len(expected)
                and all(same(a, e) for a, e in zip(actual, expected)))
    if isinstance(expected, bool):
        return type(actual) is bool and actual == expected
    return (type(actual) in (int, float) and math.isfinite(actual)
            and math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-9))


def passes(result):
    return (isinstance(result, dict) and set(result) == {"values", "unchanged"}
            and result["unchanged"] is True and same(result["values"], EXPECTED))


if __name__ == "__main__":
    ok = len(sys.argv) == 2 and passes(run(sys.argv[1]))
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
