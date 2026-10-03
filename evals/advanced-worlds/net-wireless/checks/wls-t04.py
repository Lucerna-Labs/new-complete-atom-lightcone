import base64
import json
import math
import pathlib
import subprocess
import sys


DEFAULT_LINKS = [{"sender": "A", "receiver": "R"}, {"sender": "B", "receiver": "S"}]
SHARED_LINKS = [{"sender": "A", "receiver": "R"}, {"sender": "B", "receiver": "R"}]


def separate(pab=0, pba=0, signals=(10, 10), cross=(0, 0),
             noises=(1, 1), senses=(1, 1), thresholds=(2, 2),
             names=("A", "R", "B", "S")):
    a, r, b, s = names
    # cross[0] is B->R; cross[1] is A->S. No reciprocal values are inferred.
    return [[{"sender": a, "receiver": r}, {"sender": b, "receiver": s}],
            {a: {b: pab, r: signals[0], s: cross[1]},
             b: {a: pba, r: cross[0], s: signals[1]}},
            {r: noises[0], s: noises[1]}, {a: senses[0], b: senses[1]},
            list(thresholds)]


def shared(pa, pb, pab=0, pba=0, noise=1, senses=(1, 1), thresholds=(2, 2)):
    return [SHARED_LINKS, {"A": {"B": pab, "R": pa}, "B": {"A": pba, "R": pb}},
            {"R": noise}, {"A": senses[0], "B": senses[1]}, list(thresholds)]


def wanted(busy, solo, overlap, solo_ok, overlap_ok, hidden, exposed,
           feasible, mutual, links=DEFAULT_LINKS):
    # This only formats the literal hand-derived oracle vectors supplied below.
    return {"links": [
        {"sender": links[i]["sender"], "receiver": links[i]["receiver"],
         "carrier_busy": busy[i], "snr_alone": solo[i], "sinr_overlap": overlap[i],
         "decodes_alone": solo_ok[i], "decodes_overlap": overlap_ok[i],
         "hidden_harm": hidden[i], "exposed_deferral": exposed[i]}
        for i in range(2)], "simultaneous_feasible": feasible,
        "mutually_unsensed": mutual}


TT, FF, TF, FT = (True, True), (False, False), (True, False), (False, True)
MIXED_LINKS = [{"sender": "b", "receiver": "z"}, {"sender": "A", "receiver": "x"}]
CASES = [
    ("unsensed isolated links", separate(),
     wanted(FF, (10, 10), (10, 10), TT, TT, FF, FF, True, True)),
    ("both links exposed", separate(pab=2, pba=2),
     wanted(TT, (10, 10), (10, 10), TT, TT, FF, TT, True, False)),
    ("hidden harmful overlap at both receivers", separate(cross=(10, 10)),
     wanted(FF, (10, 10), (10 / 11, 10 / 11), TT, FF, TT, FF, False, True)),
    ("sensed harmful overlap", separate(pab=2, pba=2, cross=(10, 10)),
     wanted(TT, (10, 10), (10 / 11, 10 / 11), TT, FF, FF, FF, False, False)),
    ("directed carrier sensing", separate(pab=3, pba=0.5),
     wanted(FT, (10, 10), (10, 10), TT, TT, FF, FT, True, False)),
    ("carrier threshold equality is busy", separate(pab=1, pba=1),
     wanted(TT, (10, 10), (10, 10), TT, TT, FF, TT, True, False)),
    ("decode threshold equality succeeds", separate(pab=2, pba=2, signals=(6, 6), cross=(2, 2)),
     wanted(TT, (6, 6), (2, 2), TT, TT, FF, TT, True, False)),
    ("below decoding requirement", separate(signals=(6, 6), cross=(2, 2), thresholds=(2.1, 2.1)),
     wanted(FF, (6, 6), (2, 2), TT, FF, TT, FF, False, True)),
    ("first receiver passes but second fails", separate(pab=2, pba=2, cross=(1, 20), thresholds=(4, 4)),
     wanted(TT, (10, 10), (5, 10 / 21), TT, TF, FF, FF, False, False)),
    ("second receiver passes but first fails", separate(pab=2, pba=2, cross=(20, 1), thresholds=(4, 4)),
     wanted(TT, (10, 10), (10 / 21, 5), TT, FT, FF, FF, False, False)),
    ("unsensed link survives while sensed one fails", separate(pab=0, pba=2, cross=(20, 1), thresholds=(4, 4)),
     wanted(TF, (10, 10), (10 / 21, 5), TT, FT, FF, FF, False, False)),
    ("one potential hidden harm", separate(pab=0, pba=2, cross=(1, 20), thresholds=(4, 4)),
     wanted(TF, (10, 10), (5, 10 / 21), TT, TF, FT, FF, False, False)),
    ("already bad alone is not new hidden harm", separate(signals=(1, 10), cross=(10, 10)),
     wanted(FF, (1, 10), (1 / 11, 10 / 11), FT, FF, FT, FF, False, True)),
    ("zero desired powers", separate(signals=(0, 0), cross=(10, 10)),
     wanted(FF, (0, 0), (0, 0), FF, FF, FF, FF, False, True)),
    ("receiver-specific noise", separate(pab=1, pba=0, signals=(12, 12), cross=(2, 2), noises=(1, 4), thresholds=(4, 3)),
     wanted(FT, (12, 3), (4, 2), TT, TF, FF, FF, False, False)),
    ("receiver-specific decoder thresholds", separate(pab=2, pba=2, cross=(1, 1), thresholds=(4, 6)),
     wanted(TT, (10, 10), (5, 5), TT, TF, FF, FF, False, False)),
    ("sender-specific CCA thresholds", separate(pab=3, pba=3, senses=(2, 4)),
     wanted(TF, (10, 10), (10, 10), TT, TT, FF, TF, True, False)),
    ("bounded large ratio and strict decision", separate(signals=(1000000, 1000000), cross=(1000000, 0), noises=(0.000001, 0.000001), thresholds=(1, 1)),
     wanted(FF, (1000000000000, 1000000000000), (1000000000000 / 1000000000001, 1000000000000), TT, FT, TF, FF, False, True)),
    ("small linear powers", separate(pab=0.000001, pba=0, signals=(0.000001, 0.000002), cross=(0, 0.000001), noises=(0.000001, 0.000001), senses=(0.000001, 0.000001), thresholds=(1, 1)),
     wanted(FT, (1, 2), (1, 1), TT, TT, FF, FT, True, False)),
    ("opaque IDs and input link order", separate(pab=2, pba=0, signals=(4, 6), cross=(0, 2), noises=(1, 2), thresholds=(3, 2), names=("b", "z", "A", "x")),
     wanted(FT, (4, 3), (4, 1.5), TT, TF, FF, FF, False, False, MIXED_LINKS)),
    ("shared receiver both fail", shared(10, 10),
     wanted(FF, (10, 10), (10 / 11, 10 / 11), TT, FF, TT, FF, False, True, SHARED_LINKS)),
    ("shared receiver capture", shared(20, 5, thresholds=(3, 4)),
     wanted(FF, (20, 5), (10 / 3, 5 / 21), TT, TF, FT, FF, False, True, SHARED_LINKS)),
    ("capture does not prove exposed reuse", shared(20, 5, pba=2, thresholds=(3, 4)),
     wanted(TF, (20, 5), (10 / 3, 5 / 21), TT, TF, FT, FF, False, False, SHARED_LINKS)),
    ("shared receiver independent threshold tests", shared(1, 1, pab=1, pba=1, thresholds=(0.25, 0.25)),
     wanted(TT, (1, 1), (0.5, 0.5), TT, TT, FF, TT, True, False, SHARED_LINKS)),
    ("shared receiver absent desired signal", shared(0, 10),
     wanted(FF, (0, 10), (0, 10), FT, FT, FF, FF, False, True, SHARED_LINKS)),
]
CASES.append(CASES[8])


def matches(result):
    try:
        if (type(result) is not dict or set(result) != {"values", "unchanged"}
                or result["unchanged"] is not True or type(result["values"]) is not list
                or len(result["values"]) != len(CASES)):
            return False
        for value, (_, _, expected) in zip(result["values"], CASES):
            normalized = json.loads(json.dumps(value))
            if len(value["links"]) != 2:
                return False
            for i in range(2):
                for key in ("snr_alone", "sinr_overlap"):
                    actual, target = value["links"][i][key], expected["links"][i][key]
                    if (type(actual) not in (int, float) or not math.isfinite(actual)
                            or not math.isclose(actual, target, rel_tol=1e-12, abs_tol=1e-12)):
                        return False
                    normalized["links"][i][key] = target
            if json.dumps(normalized, sort_keys=True) != json.dumps(expected, sort_keys=True):
                return False
        return True
    except (KeyError, TypeError, ValueError, OverflowError):
        return False


def run(candidate):
    payload = base64.b64encode(json.dumps([args for _, args, _ in CASES]).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
values=[];unchanged=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args);values.append(module.analyze_links(*supplied));unchanged=unchanged and json.dumps(supplied,sort_keys=True)==json.dumps(args,sort_keys=True)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged}))'''
    try:
        result = subprocess.run([sys.executable, "-B", "-c", runner,
                                 str(pathlib.Path(candidate).resolve()), payload],
                                capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in result.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if result.returncode == 0 and lines else None
        return matches(actual)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return False


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
