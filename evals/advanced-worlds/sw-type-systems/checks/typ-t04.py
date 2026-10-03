import base64
import json
import pathlib
import subprocess
import sys


def arm(pattern, guard=None):
    return {"pattern": pattern, "guard": guard}


def value(tag, **guards):
    return {"tag": tag, "guards": guards}


def decision(selected, tested=()):
    return {"selected": selected, "tested_guards": list(tested)}


def result(missing, future, exhaustive, decisions):
    return {"missing": missing, "future_missing": future,
            "exhaustive": exhaustive, "decisions": decisions}


# Independent hand coverage sets and ordered guard traces. Formatting helpers
# do not derive coverage, select arms, or compute the exhaustive Boolean.
CASES = [
    ("empty closed domain", [[], [], []], result([], False, True, [])),
    ("empty known domain still has external future", [[], [], [value(None)], True, True], result([], True, False, [decision(None)])),
    ("wildcard covers future-only value", [[], [arm("*")], [value(None)], True, True], result([], False, True, [decision(0)])),
    ("known variants without arms", [["A", "B"], [], [value("A"), value("B")]], result(["A", "B"], False, False, [decision(None), decision(None)])),
    ("two unguarded literals", [["A", "B"], [arm("A"), arm("B")], [value("B"), value("A")]], result([], False, True, [decision(1), decision(0)])),
    ("missing literal", [["A", "B"], [arm("A")], [value("A"), value("B")]], result(["B"], False, False, [decision(0), decision(None)])),
    ("variant order is not lexical order", [["B", "A"], [arm("A")], [value("A"), value("B")]], result(["B"], False, False, [decision(0), decision(None)])),
    ("first wildcard beats later named arm", [["A", "B"], [arm("*"), arm("A")], [value("A"), value("B")]], result([], False, True, [decision(0), decision(0)])),
    ("failed named guard falls through", [["A", "B"], [arm("A", "g"), arm("A"), arm("B")], [value("A", g=False), value("A", g=True), value("B", g=True)]], result([], False, True, [decision(1, [0]), decision(0, [0]), decision(2)])),
    ("sampled true guarded literal is not coverage", [["A", "B"], [arm("A", "g"), arm("B")], [value("A", g=True), value("B", g=True)]], result(["A"], False, False, [decision(0, [0]), decision(1)])),
    ("sampled true wildcard is not coverage", [["A", "B"], [arm("*", "g")], [value("A", g=True), value("B", g=True)]], result(["A", "B"], False, False, [decision(0, [0]), decision(0, [0])])),
    ("failed wildcard before literal", [["A", "B"], [arm("*", "g"), arm("A")], [value("A", g=False), value("B", g=False)]], result(["B"], False, False, [decision(1, [0]), decision(None, [0])])),
    ("unmatched pattern never evaluates its guard", [["A", "B"], [arm("B", "b"), arm("A", "a")], [value("A", b=False, a=True), value("B", b=False, a=True)]], result(["A", "B"], False, False, [decision(1, [1]), decision(None, [0])])),
    ("repeated guard name has distinct attempted arms", [["A", "B"], [arm("A", "g"), arm("*", "g"), arm("*")], [value("A", g=False), value("B", g=False), value("A", g=True), value("B", g=True)]], result([], False, True, [decision(2, [0, 1]), decision(2, [1]), decision(0, [0]), decision(1, [1])])),
    ("listed external variants do not cover future", [["A", "B"], [arm("A"), arm("B")], [value("A"), value(None)], True, True], result([], True, False, [decision(0), decision(None)])),
    ("inside defining crate only known variants required", [["A", "B"], [arm("A"), arm("B")], [value("B")], True, False], result([], False, True, [decision(1)])),
    ("outside ordinary exhaustive enum remains closed", [["A", "B"], [arm("A"), arm("B")], [value("B")], False, True], result([], False, True, [decision(1)])),
    ("guarded future fallback does not close coverage", [["A", "B"], [arm("A"), arm("B"), arm("*", "g")], [value(None, g=True), value(None, g=False), value("A", g=True)], True, True], result([], True, False, [decision(2, [2]), decision(None, [2]), decision(0)])),
    ("unguarded future fallback closes coverage", [["A", "B"], [arm("A"), arm("*")], [value(None), value("A"), value("B")], True, True], result([], False, True, [decision(1), decision(0), decision(1)])),
    ("missing order follows declaration order", [["C", "A", "B"], [arm("A")], [value("C"), value("A"), value("B")]], result(["C", "B"], False, False, [decision(None), decision(0), decision(None)])),
    ("absence of samples is not a coverage proof", [["A"], [arm("A", "g")], []], result(["A"], False, False, [])),
    ("case-sensitive guard identities", [["A", "B"], [arm("A", "G"), arm("A", "g"), arm("*")], [value("A", G=False, g=True), value("A", G=True, g=False), value("B", G=True, g=True)]], result([], False, True, [decision(1, [0, 1]), decision(0, [0]), decision(2)])),
    ("case-sensitive variant identities", [["A", "a"], [arm("A")], [value("a"), value("A")]], result(["a"], False, False, [decision(None), decision(0)])),
    ("guard and variant namespaces are independent", [["A"], [arm("A", "A"), arm("*")], [value("A", A=False)]], result([], False, True, [decision(1, [0])])),
    ("unguarded arm stops all later guard testing", [["A"], [arm("A"), arm("A", "g"), arm("*", "h")], [value("A", g=True, h=False)]], result([], False, True, [decision(0)])),
    ("known and future both remain uncovered", [["B", "A"], [arm("A", "g")], [value(None, g=True), value("B", g=False)], True, True], result(["B", "A"], True, False, [decision(None), decision(None)])),
]
# Bounded analytic cases: each distinct literal selects its reverse position;
# eight false guarded literals fall through to their corresponding later arm;
# twelve samples alternate only one named guard's truth value.
NAMES = [f"V{i}" for i in range(8)]
CASES.append(("eight variants in reversed arm order", [NAMES, [arm(n) for n in reversed(NAMES)], [value(n) for n in NAMES]],
              result([], False, True, [decision(i) for i in [7, 6, 5, 4, 3, 2, 1, 0]])))
CASES.append(("sixteen arms preserve later fallback", [NAMES, [arm(n, "g") for n in NAMES] + [arm(n) for n in NAMES], [value(n, g=False) for n in NAMES]],
              result([], False, True, [decision(i + 8, [i]) for i in range(8)])))
CASES.append(("twelve independent decisions", [["A"], [arm("A", "g"), arm("A")], [value("A", g=bool(i % 2)) for i in range(12)]],
              result([], False, True, [decision(i, [0]) for i in [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]])))
CASES.extend([CASES[0], CASES[8], CASES[0]])

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

def mutable_ids(value, seen=None):
    if seen is None: seen=set()
    if type(value) not in (dict,list) or id(value) in seen: return seen
    seen.add(id(value))
    for child in (value.values() if type(value) is dict else value): mutable_ids(child,seen)
    return seen

def independent_outputs(values, forbidden):
    seen=set(forbidden)
    def visit(value):
        if type(value) not in (dict,list): return True
        if id(value) in seen: return False
        seen.add(id(value))
        return all(visit(child) for child in (value.values() if type(value) is dict else value))
    return all(visit(value) for value in values)

spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
values=[];output_history=[];inputs=[];input_ids=set();unchanged=True;independent=True;stable=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args)
    inputs.append((supplied,json.dumps(supplied,sort_keys=True),native_types(supplied)))
    input_ids.update(mutable_ids(supplied))
    result=m.enum_match_analysis(*supplied)
    values.append(result)
    result_types=native_types(result)
    output_history.append((json.dumps(result,sort_keys=True),result_types))
    for prior,(before,types) in zip(values,output_history):
        stable=stable and json.dumps(prior,sort_keys=True)==before and native_types(prior)==types
    for prior,before,types in inputs:
        unchanged=unchanged and json.dumps(prior,sort_keys=True)==before and native_types(prior)==types
    independent=independent and independent_outputs(values,input_ids)
print("__RESULT__"+json.dumps({"values":values,"types":[native_types(v) for v in values],"unchanged":unchanged,"independent":independent,"stable":stable}))'''
    try:
        process = subprocess.run([sys.executable, "-B", "-c", runner,
                                  str(pathlib.Path(candidate).resolve()), payload],
                                 capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in process.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        actual = json.loads(lines[-1]) if process.returncode == 0 and lines else None
        wanted = [value for _, _, value in CASES]
        expected = {"values": wanted, "types": [native_types(v) for v in wanted],
                    "unchanged": True, "independent": True, "stable": True}
        return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return False


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) else 1)
