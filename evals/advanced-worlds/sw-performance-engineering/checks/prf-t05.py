import base64
import json
import math
import pathlib
import subprocess
import sys


def trials(starts, operations=(1, 1, 1, 1)):
    return [{"start": start, "operations": count} for start, count in zip(starts, operations)]


def expected(rows, mean_a, mean_b, ratio, same_position, zero):
    # Rows are literal elapsed, measured, error, per-operation witnesses.
    records = [{"variant": variant, "position": i, "elapsed": row[0],
                "measured": row[1], "error": row[2], "per_op": row[3]}
               for i, (variant, row) in enumerate(zip("ABBA", rows))]
    return {"trials": records, "mean_a": mean_a, "mean_b": mean_b,
            "measured_ratio": ratio, "same_position_ratio": same_position,
            "time_zero_ratio": zero}


# All observations/means are hand calculated. Fractions below are exact
# closed-form expected constants, not calls into the reference algorithm.
CASES = [
    ("minimal default resolution", [1, 1, 0, trials([0, 1, 2, 3])],
     expected([(1, 1, 0, 1.0)] * 4, 1.0, 1.0, 1.0, 1.0, 1.0)),
    ("ABBA balances at position one and a half", [10, 20, 2, trials([0, 100, 200, 300])],
     expected([(10, 10, 0, 10.0), (22, 22, 0, 22.0), (24, 24, 0, 24.0), (16, 16, 0, 16.0)],
              13.0, 23.0, 13 / 23, 13 / 23, 0.5)),
    ("negative shared drift", [20, 30, -2, trials([0, 100, 200, 300])],
     expected([(20, 20, 0, 20.0), (28, 28, 0, 28.0), (26, 26, 0, 26.0), (14, 14, 0, 14.0)],
              17.0, 27.0, 17 / 27, 17 / 27, 2 / 3)),
    ("zero drift explicit resolution", [10, 20, 0, trials([0, 100, 200, 300]), 1],
     expected([(10, 10, 0, 10.0), (20, 20, 0, 20.0), (20, 20, 0, 20.0), (10, 10, 0, 10.0)],
              10.0, 20.0, 0.5, 0.5, 0.5)),
    ("normalize unequal counts before averaging", [10, 20, 2, trials([0, 100, 200, 300], [2, 3, 4, 5])],
     expected([(20, 20, 0, 10.0), (66, 66, 0, 22.0), (96, 96, 0, 24.0), (80, 80, 0, 16.0)],
              13.0, 23.0, 13 / 23, 13 / 23, 0.5)),
    ("unequal counts and quantizer phase", [10, 20, 2, trials([0, 100, 200, 300], [2, 3, 4, 5]), 7],
     expected([(20, 14, -6, 7.0), (66, 63, -3, 21.0), (96, 98, 2, 24.5), (80, 84, 4, 16.8)],
              11.9, 22.75, 11.9 / 22.75, 13 / 23, 0.5)),
    ("floor endpoints separately", [10, 20, 0, trials([1, 101, 201, 301]), 6],
     expected([(10, 6, -4, 6.0), (20, 24, 4, 24.0), (20, 18, -2, 18.0), (10, 6, -4, 6.0)],
              6.0, 21.0, 2 / 7, 0.5, 0.5)),
    ("all measured intervals zero", [1, 1, 0, trials([0, 1, 2, 3]), 10],
     expected([(1, 0, -1, 0.0)] * 4, 0.0, 0.0, None, 1.0, 1.0)),
    ("positive measured numerator and zero denominator", [10, 1, 0, trials([0, 10, 11, 20]), 10],
     expected([(10, 10, 0, 10.0), (1, 0, -1, 0.0), (1, 0, -1, 0.0), (10, 10, 0, 10.0)],
              10.0, 0.0, None, 10.0, 10.0)),
    ("zero measured numerator is a numeric ratio", [1, 10, 0, trials([0, 10, 20, 30]), 10],
     expected([(1, 0, -1, 0.0), (10, 10, 0, 10.0), (10, 10, 0, 10.0), (1, 0, -1, 0.0)],
              0.0, 10.0, 0.0, 0.1, 0.1)),
    ("both near-one-tick error signs", [11, 9, 0, trials([9, 20, 30, 40]), 10],
     expected([(11, 20, 9, 20.0), (9, 0, -9, 0.0), (9, 0, -9, 0.0), (11, 10, -1, 10.0)],
              15.0, 0.0, None, 11 / 9, 11 / 9)),
    ("one-unit intervals straddle selected boundaries", [1, 1, 0, trials([9, 11, 19, 21]), 10],
     expected([(1, 10, 9, 10.0), (1, 0, -1, 0.0), (1, 10, 9, 10.0), (1, 0, -1, 0.0)],
              5.0, 5.0, 1.0, 1.0, 1.0)),
    ("timestamp gaps do not change index drift", [10, 20, 2, trials([0, 100000000, 200000000, 999999999000])],
     expected([(10, 10, 0, 10.0), (22, 22, 0, 22.0), (24, 24, 0, 24.0), (16, 16, 0, 16.0)],
              13.0, 23.0, 13 / 23, 13 / 23, 0.5)),
    ("maximum base drift counts and resolution", [1000000, 1000000, 1000,
      trials([0, 100000000000, 200000000000, 300000000000], [10000] * 4), 1000000],
     expected([(10000000000, 10000000000, 0, 1000000.0),
               (10010000000, 10010000000, 0, 1001000.0),
               (10020000000, 10020000000, 0, 1002000.0),
               (10030000000, 10030000000, 0, 1003000.0)],
              1001500.0, 1001500.0, 1.0, 1.0, 1.0)),
    ("minimum drift leaves positive costs", [3001, 2001, -1000, trials([0, 10000, 20000, 30000])],
     expected([(3001, 3001, 0, 3001.0), (1001, 1001, 0, 1001.0), (1, 1, 0, 1.0), (1, 1, 0, 1.0)],
              1501.0, 501.0, 1501 / 501, 1501 / 501, 3001 / 2001)),
    ("maximum resolution can hide positive work", [1, 1, 0, trials([0, 1, 2, 3]), 1000000],
     expected([(1, 0, -1, 0.0)] * 4, 0.0, 0.0, None, 1.0, 1.0)),
    ("maximum end timestamp", [1, 1, 0, trials([999999999996, 999999999997, 999999999998, 999999999999])],
     expected([(1, 1, 0, 1.0)] * 4, 1.0, 1.0, 1.0, 1.0, 1.0)),
    ("large integer timestamps keep their quantizer phase", [1, 1, 0,
      trials([999999999996, 999999999997, 999999999998, 999999999999]), 7],
     expected([(1, 0, -1, 0.0), (1, 0, -1, 0.0), (1, 7, 6, 7.0), (1, 0, -1, 0.0)],
              0.0, 3.5, 0.0, 1.0, 1.0)),
    ("exact contiguous resolution multiples", [3, 6, 0, trials([0, 3, 9, 15]), 3],
     expected([(3, 3, 0, 3.0), (6, 6, 0, 6.0), (6, 6, 0, 6.0), (3, 3, 0, 3.0)],
              3.0, 6.0, 0.5, 0.5, 0.5)),
    ("equal bases remain equal after shared drift", [3, 3, 1, trials([0, 10, 20, 30])],
     expected([(3, 3, 0, 3.0), (4, 4, 0, 4.0), (5, 5, 0, 5.0), (6, 6, 0, 6.0)],
              4.5, 4.5, 1.0, 1.0, 1.0)),
    ("negative drift and fractional normalized observations", [8, 9, -1,
      trials([0, 40, 50, 80], [4, 1, 3, 2]), 5],
     expected([(32, 30, -2, 7.5), (8, 5, -3, 5.0), (21, 20, -1, 20 / 3), (10, 10, 0, 5.0)],
              6.25, 35 / 6, 15 / 14, 13 / 15, 8 / 9)),
    ("large unequal operation credits", [2, 3, 0,
      trials([0, 10, 40000, 50000], [1, 10000, 2, 10000])],
     expected([(2, 2, 0, 2.0), (30000, 30000, 0, 3.0), (6, 6, 0, 3.0), (20000, 20000, 0, 2.0)],
              2.0, 3.0, 2 / 3, 2 / 3, 2 / 3)),
    ("extreme signed integer quantization errors", [1, 999999, 0,
      trials([999999, 1000000, 2000000, 2999999]), 1000000],
     expected([(1, 1000000, 999999, 1000000.0), (999999, 0, -999999, 0.0),
               (999999, 0, -999999, 0.0), (1, 1000000, 999999, 1000000.0)],
              1000000.0, 0.0, None, 1 / 999999, 1 / 999999)),
]
CALLS = CASES + [CASES[5], CASES[0], CASES[7], CASES[5], CASES[1]]
EXPECTED = [result for _, _, result in CALLS]


def equal(actual, wanted):
    if type(actual) is not type(wanted):
        return False
    if type(wanted) is float:
        return math.isfinite(actual) and math.isclose(actual, wanted, rel_tol=1e-12, abs_tol=1e-12)
    if type(wanted) is dict:
        return actual.keys() == wanted.keys() and all(equal(actual[k], v) for k, v in wanted.items())
    if type(wanted) is list:
        return len(actual) == len(wanted) and all(equal(a, e) for a, e in zip(actual, wanted))
    return actual == wanted


def matches(actual):
    return equal(actual, {"values": EXPECTED, "unchanged": True,
                          "stable_outputs": True, "independent": True})


RUNNER = r'''import base64,copy,importlib.util,json,math,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
def fingerprint(value):
    if type(value) is dict and all(type(key) is str for key in value):
        return ("dict",tuple((key,fingerprint(value[key])) for key in sorted(value)))
    if type(value) is list:
        return ("list",tuple(fingerprint(item) for item in value))
    if type(value) is float:
        if not math.isfinite(value): raise TypeError("nonfinite float")
        return ("float",value)
    if type(value) in (str,int,bool,type(None)):
        return (type(value).__name__,value)
    raise TypeError("value outside exact native types")
def mutable_ids(value):
    if type(value) is dict:
        return {id(value)}.union(*(mutable_ids(item) for item in value.values()))
    if type(value) is list:
        return {id(value)}.union(*(mutable_ids(item) for item in value))
    return set()
def disjoint(values, forbidden):
    seen=set(forbidden)
    def visit(value):
        if type(value) not in (dict,list): return True
        if id(value) in seen: return False
        seen.add(id(value))
        return all(visit(item) for item in (value.values() if type(value) is dict else value))
    return all(visit(value) for value in values)
values=[];inputs=[];outputs=[];input_ids=set();unchanged=True;stable=True;independent=True
for data in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(data);inputs.append((supplied,fingerprint(supplied)));input_ids.update(mutable_ids(supplied))
    value=module.abba_measurements(*supplied)
    outputs.append((value,fingerprint(value)));values.append(value)
    unchanged=unchanged and all(fingerprint(prior)==before for prior,before in inputs)
    stable=stable and all(fingerprint(prior)==before for prior,before in outputs)
    independent=independent and disjoint(values,input_ids)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged,"stable_outputs":stable,"independent":independent}))'''


def run(candidate):
    payload = base64.b64encode(json.dumps([args for _, args, _ in CALLS]).encode()).decode()
    try:
        process = subprocess.run([sys.executable, "-B", "-c", RUNNER,
                                  str(pathlib.Path(candidate).resolve()), payload],
                                 capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if process.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


if __name__ == "__main__":
    ok = len(sys.argv) == 2 and matches(run(sys.argv[1]))
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
