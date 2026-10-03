"""Hand-specified finite-type oracles; no full compiler or external solver."""
import base64
import json
import pathlib
import subprocess
import sys


def V(name):
    return {"var": name}


def A(left, right):
    return {"arrow": [left, right]}


def ok(**bindings):
    return {"ok": True, "substitution": bindings}


FAIL = {"ok": False, "substitution": {}}
CASES = [
    ("empty", [[]], ok()),
    ("equal constants", [[["Bool", "Bool"], ["Nat", "Nat"]]], ok()),
    ("distinct constants", [[["Bool", "Nat"]]], FAIL),
    ("constructor clash", [[["Bool", A("Bool", "Nat")]]], FAIL),
    ("two independent bindings", [[[V("a"), "Bool"], ["Nat", V("b")]]], ok(a="Bool", b="Nat")),
    ("alias then constant", [[[V("a"), V("b")], [V("b"), "Bool"]]], ok(a="Bool", b="Bool")),
    ("identity after alias", [[[V("a"), V("b")], [V("b"), V("a")]]], ok(a=V("a"), b=V("a"))),
    ("substitution exposes occurs failure", [[[V("a"), V("b")], [V("b"), A("Bool", V("a"))]]], FAIL),
    ("resolve both equation sides", [[[V("a"), A(V("b"), "Bool")], [V("c"), V("a")], [V("b"), "Nat"]]],
     ok(a=A("Nat", "Bool"), b="Nat", c=A("Nat", "Bool"))),
    ("arrow child order and updated substitution", [[[A(V("a"), V("b")), A(V("b"), V("a"))]]],
     ok(a=V("a"), b=V("a"))),
    ("decompose concrete arrow", [[[A(V("a"), V("b")), A("Nat", "Bool")]]], ok(a="Nat", b="Bool")),
    ("shared variable cannot take distinct bases", [[[A(V("a"), V("a")), A("Bool", "Nat")]]], FAIL),
    ("discard partial bindings on failure", [[[V("a"), "Nat"], [V("b"), "Bool"], ["Bool", "Nat"]]], FAIL),
    ("normalize nested repeated subtrees", [[[V("a"), A(V("b"), V("b"))], [V("b"), V("c")], [V("c"), "Nat"]]],
     ok(a=A("Nat", "Nat"), b="Nat", c="Nat")),
    ("repeated whole arrow identity", [[[V("a"), A(V("b"), "Bool")], [V("a"), A(V("b"), "Bool")]]],
     ok(a=A(V("b"), "Bool"), b=V("b"))),
    ("occurs hidden in resolved arrow", [[[V("a"), A("Nat", V("b"))], [V("b"), A("Bool", V("a"))]]], FAIL),
    ("arrow versus constant after resolution", [[[V("a"), A("Nat", "Bool")], [V("a"), "Nat"]]], FAIL),
    ("all original variable keys retained", [[[A(V("a"), V("b")), A(V("c"), V("d"))]]],
     ok(a=V("a"), b=V("b"), c=V("a"), d=V("b"))),
    ("same bound concrete variable is not cyclic", [[[V("a"), "Bool"], [V("a"), V("a")]]], ok(a="Bool")),
    ("an unconstrained child is not generalized away", [[[V("a"), A(V("b"), A(V("c"), V("b")))]]],
     ok(a=A(V("b"), A(V("c"), V("b"))), b=V("b"), c=V("c"))),
]
for name in "abcdefgh":
    CASES.append(("variable identity " + name, [[[V(name), V(name)]]], ok(**{name: V(name)})))
    CASES.append(("proper domain occurrence " + name, [[[V(name), A(V(name), "Bool")]]], FAIL))
    CASES.append(("proper nested result occurrence " + name, [[[A("Nat", A("Bool", V(name))), V(name)]]], FAIL))
for left in "abcdefgh":
    for right in "abcdefgh":
        if left != right:
            representative = min(left, right)
            CASES.append(("lexical representative " + left + right, [[[V(left), V(right)]]],
                          ok(**{left: V(representative), right: V(representative)})))
chain = [[V(a), V(b)] for a, b in zip("abcdefgh", "bcdefgh")] + [[V("h"), "Nat"]]
CASES.append(("eight-variable normalization chain", [chain], ok(**dict.fromkeys("abcdefgh", "Nat"))))
CASES.append(("sixteen-equation boundary", [[["Nat", "Nat"] for _ in range(16)]], ok()))
tree = V("a")
for _ in range(4):
    tree = A(tree, tree)
CASES.append(("depth-four tree identity", [[[tree, tree]]], ok(a=V("a"))))
CALLS = CASES + [CASES[8], CASES[0], CASES[14], CASES[4], CASES[0]]


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
    if type(v) in (str,bool):
        return (type(v).__name__,v)
    raise TypeError("unsupported native type")
def containers(v):
    if type(v) is dict:
        yield id(v)
        for x in v.values(): yield from containers(x)
    elif type(v) is list:
        yield id(v)
        for x in v: yield from containers(x)
values=[];retained=[];output_ids=set();saved=[];independent=True;unchanged=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args);retained.append((supplied,fingerprint(supplied)))
    value=module.unify_types(*supplied);before=fingerprint(value)
    ids=list(containers(value))
    independent=independent and len(ids)==len(set(ids)) and not bool(set(ids)&output_ids)
    output_ids.update(ids);values.append(value);saved.append(before)
    unchanged=unchanged and all(fingerprint(old)==snap for old,snap in retained)
    unchanged=unchanged and all(fingerprint(old)==snap for old,snap in zip(values,saved))
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
            return False, "candidate execution or nonnative output"
        value = json.loads(lines[-1])
        if value.get("unchanged") is not True:
            return False, "input or prior-output mutation"
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
    passed, detail = run(sys.argv[1]) if len(sys.argv) == 2 else (False, "candidate path required")
    print(("PASS: " if passed else "FAIL: ") + detail)
    sys.exit(0 if passed else 1)
