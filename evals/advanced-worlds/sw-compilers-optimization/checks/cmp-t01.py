"""Literal tagged-value oracles and width-boundary cases, no LLVM invocation."""
import base64
import json
import pathlib
import subprocess
import sys


def literal(name, bits, value=None, kind="value"):
    return {"op": "literal", "id": name, "bits": bits, "kind": kind, "value": value}


def add(name, lhs, rhs, nsw=False):
    return {"op": "add", "id": name, "lhs": lhs, "rhs": rhs, "nsw": nsw}


def eq(name, lhs, rhs):
    return {"op": "eq", "id": name, "lhs": lhs, "rhs": rhs}


def freeze(name, source):
    return {"op": "freeze", "id": name, "value": source}


def select(name, condition, yes, no):
    return {"op": "select", "id": name, "cond": condition, "yes": yes, "no": no}


def br(condition):
    return {"op": "br", "condition": condition}


def v(bits, value=None, kind="value"):
    return {"bits": bits, "kind": kind, "value": value}


def p(bits):
    return v(bits, None, "poison")


def u(bits):
    return v(bits, None, "undef")


def result(values=None, branch=None, ub=False):
    return {"values": {} if values is None else values, "branch": branch, "ub": ub}


CASES = [
    ("empty", [[], {}], result()),
    ("literal widths and bit patterns", [[literal("A_1", 8, 255), literal("b", 1, 0)], {}],
     result({"A_1": v(8, 255), "b": v(1, 0)})),
    ("unflagged modular add", [[literal("a", 8, 250), literal("b", 8, 10), add("s", "a", "b"),
       literal("four", 8, 4), eq("c", "s", "four"), br("c")], {}],
     result({"a": v(8, 250), "b": v(8, 10), "s": v(8, 4), "four": v(8, 4), "c": v(1, 1)}, True)),
    ("unflagged negative bit patterns wrap", [[literal("a", 8, 128), add("s", "a", "a")], {}],
     result({"a": v(8, 128), "s": v(8, 0)})),
    ("producing poison alone is deferred", [[literal("a", 8, 127), literal("b", 8, 1), add("s", "a", "b", True)], {}],
     result({"a": v(8, 127), "b": v(8, 1), "s": p(8)})),
    ("poison reaches an i1 branch through comparison",
     [[literal("a", 8, 127), literal("b", 8, 1), add("s", "a", "b", True),
       literal("z", 8, 0), eq("c", "s", "z"), br("c")], {}],
     result({"a": v(8, 127), "b": v(8, 1), "s": p(8), "z": v(8, 0), "c": p(1)}, ub=True)),
    ("signed negative overflow", [[literal("a", 8, 128), literal("b", 8, 255), add("s", "a", "b", True)], {}],
     result({"a": v(8, 128), "b": v(8, 255), "s": p(8)})),
    ("unsigned carry is not signed overflow", [[literal("a", 4, 15), literal("b", 4, 1), add("s", "a", "b", True)], {}],
     result({"a": v(4, 15), "b": v(4, 1), "s": v(4, 0)})),
    ("largest signed result is representable", [[literal("a", 8, 126), literal("b", 8, 1), add("s", "a", "b", True)], {}],
     result({"a": v(8, 126), "b": v(8, 1), "s": v(8, 127)})),
    ("smallest signed result is representable", [[literal("a", 8, 128), literal("b", 8, 0), add("s", "a", "b", True)], {}],
     result({"a": v(8, 128), "b": v(8, 0), "s": v(8, 128)})),
    ("i1 negative addition overflows", [[literal("a", 1, 1), add("s", "a", "a", True), br("s")], {}],
     result({"a": v(1, 1), "s": p(1)}, ub=True)),
    ("i1 unflagged addition wraps", [[literal("a", 1, 1), add("s", "a", "a"), br("s")], {}],
     result({"a": v(1, 1), "s": v(1, 0)}, False)),
    ("poison propagation is not numeric arithmetic", [[literal("a", 8, kind="poison"), literal("z", 8, 0),
       add("s", "a", "z"), eq("c", "a", "a"), br("c")], {}],
     result({"a": p(8), "z": v(8, 0), "s": p(8), "c": p(1)}, ub=True)),
    ("direct poison branch", [[literal("c", 1, kind="poison"), br("c")], {}],
     result({"c": p(1)}, ub=True)),
    ("direct undef branch", [[literal("c", 1, kind="undef"), br("c")], {}],
     result({"c": u(1)}, ub=True)),
    ("freeze fixes one undef result", [[literal("x", 8, kind="undef"), freeze("f", "x"), eq("c", "f", "f"), br("c")], {"f": 77}],
     result({"x": u(8), "f": v(8, 77), "c": v(1, 1)}, True)),
    ("separate freezes may disagree", [[literal("x", 8, kind="undef"), freeze("f", "x"), freeze("g", "x"),
       eq("c", "f", "g"), br("c")], {"f": 77, "g": 78}],
     result({"x": u(8), "f": v(8, 77), "g": v(8, 78), "c": v(1, 0)}, False)),
    ("freeze preserves a concrete value", [[literal("x", 4, 3), freeze("f", "x"), eq("c", "x", "f"), br("c")], {"f": 15}],
     result({"x": v(4, 3), "f": v(4, 3), "c": v(1, 1)}, True)),
    ("false select masks true-arm poison", [[literal("c", 1, 0), literal("bad", 8, kind="poison"),
       literal("good", 8, 7), select("s", "c", "bad", "good")], {}],
     result({"c": v(1, 0), "bad": p(8), "good": v(8, 7), "s": v(8, 7)})),
    ("true select masks false-arm poison", [[literal("c", 1, 1), literal("bad", 8, kind="poison"),
       literal("good", 8, 7), select("s", "c", "good", "bad")], {}],
     result({"c": v(1, 1), "bad": p(8), "good": v(8, 7), "s": v(8, 7)})),
    ("selected poison propagates", [[literal("c", 1, 1), literal("bad", 1, kind="poison"),
       literal("good", 1, 0), select("s", "c", "bad", "good"), br("s")], {}],
     result({"c": v(1, 1), "bad": p(1), "good": v(1, 0), "s": p(1)}, ub=True)),
    ("poison select condition poisons result", [[literal("c", 1, kind="poison"), literal("a", 4, 2),
       literal("b", 4, 3), select("s", "c", "a", "b")], {}],
     result({"c": p(1), "a": v(4, 2), "b": v(4, 3), "s": p(4)})),
    ("selected undef may be frozen", [[literal("c", 1, 1), literal("a", 4, kind="undef"), literal("b", 4, 3),
       select("s", "c", "a", "b"), freeze("f", "s")], {"f": 8}],
     result({"c": v(1, 1), "a": u(4), "b": v(4, 3), "s": u(4), "f": v(4, 8)})),
    ("unselected undef is not propagated", [[literal("c", 1, 0), literal("a", 4, kind="undef"), literal("b", 4, 3),
       select("s", "c", "a", "b")], {}],
     result({"c": v(1, 0), "a": u(4), "b": v(4, 3), "s": v(4, 3)})),
    ("unused poison does not poison another branch", [[literal("unused", 8, kind="poison"), literal("c", 1, 1), br("c")], {}],
     result({"unused": p(8), "c": v(1, 1)}, True)),
]
# Known boundary fact: for widths >=2, signed maximum plus the representable
# positive one exceeds that width's signed range. No evaluator builds this oracle.
for bits in range(2, 9):
    maximum = (1 << (bits - 1)) - 1
    program = [literal("a", bits, maximum), literal("one", bits, 1), add("s", "a", "one", True)]
    CASES.append(("signed maximum boundary " + str(bits), [program, {}],
                  result({"a": v(bits, maximum), "one": v(bits, 1), "s": p(bits)})))
for choice in (0, 1):
    program = [literal("a", 8, 127), literal("one", 8, 1), add("s", "a", "one", True),
               literal("z", 8, 0), eq("c", "s", "z"), freeze("f", "c"), br("f")]
    CASES.append(("freeze poison condition choice " + str(choice), [program, {"f": choice}],
                  result({"a": v(8, 127), "one": v(8, 1), "s": p(8), "z": v(8, 0),
                          "c": p(1), "f": v(1, choice)}, bool(choice))))
CALLS = CASES + [CASES[15], CASES[0], CASES[18], CASES[0]]


def run(candidate):
    payload = base64.b64encode(json.dumps([args for _, args, _ in CALLS]).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
def fingerprint(v):
    if type(v) is dict and all(type(k) is str for k in v):
        return ("dict",tuple((k,fingerprint(v[k])) for k in sorted(v)))
    if type(v) is list:
        return ("list",tuple(fingerprint(x) for x in v))
    if type(v) in (str,int,bool,type(None)):
        return (type(v).__name__,v)
    raise TypeError("unsupported native type")
def containers(v):
    if type(v) is dict:
        yield id(v)
        for x in v.values(): yield from containers(x)
    elif type(v) is list:
        yield id(v)
        for x in v: yield from containers(x)
values=[];retained=[];output_ids=set();independent=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args);retained.append((supplied,fingerprint(supplied)))
    value=module.scalar_ir(*supplied);fingerprint(value)
    ids=list(containers(value))
    independent=independent and len(ids)==len(set(ids)) and not bool(set(ids)&output_ids)
    output_ids.update(ids);values.append(value)
unchanged=all(fingerprint(args)==before for args,before in retained)
input_ids=set()
for args,_ in retained: input_ids.update(containers(args))
independent=independent and not bool(output_ids & input_ids)
fingerprint(values)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged,"independent":independent}))'''
    try:
        p = subprocess.run([sys.executable, "-B", "-c", runner,
                            str(pathlib.Path(candidate).resolve()), payload],
                           capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in p.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        if p.returncode or not lines:
            return False, "candidate execution"
        value = json.loads(lines[-1])
        if value.get("unchanged") is not True:
            return False, "input mutation"
        if value.get("independent") is not True:
            return False, "mutable aliasing"
        outputs = value.get("values")
        if type(outputs) is not list or len(outputs) != len(CALLS):
            return False, "output count"
        for (label, _, expected), actual in zip(CALLS, outputs):
            if json.dumps(actual, sort_keys=True) != json.dumps(expected, sort_keys=True):
                return False, label
        return True, str(len(CALLS)) + " deterministic calls"
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False, "candidate execution"


if __name__ == "__main__":
    ok, detail = run(sys.argv[1]) if len(sys.argv) == 2 else (False, "candidate path required")
    print(("PASS: " if ok else "FAIL: ") + detail)
    sys.exit(0 if ok else 1)
