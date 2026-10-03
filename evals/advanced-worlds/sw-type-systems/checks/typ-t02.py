import base64
from copy import deepcopy
import json
import pathlib
import subprocess
import sys


def v(name):
    return {"var": name}


def arrow(left, right):
    return {"from": left, "to": right}


def scheme(bound, body):
    return {"bound": list(bound), "body": body}


def instance(renaming, body):
    return {"renaming": renaming, "body": body}


def result(ty, environment, bound, instances):
    return {"normalized_type": ty, "environment": environment,
            "scheme": scheme(bound, deepcopy(ty)), "instances": instances}


_OMITTED = object()


def case(name, inferred, environment, substitution, expected, count=_OMITTED):
    args = {"inferred": inferred, "environment": environment, "substitution": substitution}
    if count is not _OMITTED:
        args["count"] = count
    return name, args, expected


# Literal schemes, substitutions and fresh names worked independently of the
# reference. Helpers only assemble the supplied type trees and records.
CASES = [
    case("ground type with empty maps and default count", "Bool", {}, {},
         result("Bool", {}, [], [instance({}, "Bool"), instance({}, "Bool")])),
    case("zero requested instances", "Nat", {}, {}, result("Nat", {}, [], []), 0),
    case("one generalized variable", v("a"), {}, {},
         result(v("a"), {}, ["a"], [instance({"a": "t0"}, v("t0")), instance({"a": "t1"}, v("t1"))])),
    case("same bound variable replaced consistently", arrow(v("a"), v("a")), {}, {},
         result(arrow(v("a"), v("a")), {}, ["a"],
                [instance({"a": "t0"}, arrow(v("t0"), v("t0"))),
                 instance({"a": "t1"}, arrow(v("t1"), v("t1")))])),
    case("generalized binders sorted rather than occurrence order", arrow(v("b"), v("a")), {}, {},
         result(arrow(v("b"), v("a")), {}, ["a", "b"],
                [instance({"a": "t0", "b": "t1"}, arrow(v("t1"), v("t0"))),
                 instance({"a": "t2", "b": "t3"}, arrow(v("t3"), v("t2")))])),
    case("free context variable is not generalized", v("a"), {"x": scheme([], v("a"))}, {},
         result(v("a"), {"x": scheme([], v("a"))}, [], [instance({}, v("a")), instance({}, v("a"))])),
    case("substituted environment determines generalization", v("a"), {"x": scheme([], v("a"))},
         {"a": arrow(v("b"), v("b"))},
         result(arrow(v("b"), v("b")), {"x": scheme([], arrow(v("b"), v("b")))}, [],
                [instance({}, arrow(v("b"), v("b"))), instance({}, arrow(v("b"), v("b")))])),
    case("transitive variable binding store", v("a"), {}, {"a": v("b"), "b": "Nat"},
         result("Nat", {}, [], [instance({}, "Nat"), instance({}, "Nat")])),
    case("substitution leaves a different free unknown", arrow(v("a"), v("b")), {}, {"a": "Bool"},
         result(arrow("Bool", v("b")), {}, ["b"],
                [instance({"b": "t0"}, arrow("Bool", v("t0"))), instance({"b": "t1"}, arrow("Bool", v("t1")))])),
    case("scheme binder shields a substitution key", v("a"), {"id": scheme(["a"], arrow(v("a"), v("a")))},
         {"a": "Nat"}, result("Nat", {"id": scheme(["a"], arrow(v("a"), v("a")))}, [],
                              [instance({}, "Nat"), instance({}, "Nat")])),
    case("alpha-renaming prevents capture of replacement free variable", v("a"),
         {"f": scheme(["a"], arrow(v("a"), v("b")))}, {"b": v("a")},
         result(v("a"), {"f": scheme(["t0"], arrow(v("t0"), v("a")))}, [],
                [instance({}, v("a")), instance({}, v("a"))])),
    case("alpha supply is consumed before instance supply", v("c"),
         {"f": scheme(["a"], arrow(v("a"), v("b")))}, {"b": v("a")},
         result(v("c"), {"f": scheme(["t0"], arrow(v("t0"), v("a")))}, ["c"],
                [instance({"c": "t1"}, v("t1")), instance({"c": "t2"}, v("t2"))])),
    case("fully normalized ranges avoid unnecessary capture rename", v("c"),
         {"f": scheme(["a"], arrow(v("a"), v("b")))}, {"b": v("a"), "a": "Bool"},
         result(v("c"), {"f": scheme(["a"], arrow(v("a"), "Bool"))}, ["c"],
                [instance({"c": "t0"}, v("t0")), instance({"c": "t1"}, v("t1"))])),
    case("fresh supply skips existing inferred variable names", arrow(v("t0"), v("a")), {}, {},
         result(arrow(v("t0"), v("a")), {}, ["a", "t0"],
                [instance({"a": "t1", "t0": "t2"}, arrow(v("t2"), v("t1")))]), 1),
    case("even unused substitution keys reserve their names", v("a"), {}, {"t0": "Bool"},
         result(v("a"), {}, ["a"], [instance({"a": "t1"}, v("t1"))]), 1),
    case("unused bound names also reserve fresh names", v("a"), {"f": scheme(["t0"], "Bool")}, {},
         result(v("a"), {"f": scheme(["t0"], "Bool")}, ["a"],
                [instance({"a": "t1"}, v("t1")), instance({"a": "t2"}, v("t2"))])),
    case("environment traversal is lexical rather than input order", v("c"),
         {"z": scheme(["b"], arrow(v("b"), v("b"))), "a": scheme(["b"], v("b"))}, {"r": v("b")},
         result(v("c"), {"a": scheme(["t0"], v("t0")), "z": scheme(["t1"], arrow(v("t1"), v("t1")))},
                ["c"], [instance({"c": "t2"}, v("t2"))]), 1),
    case("alpha-renaming follows original binder order", "Nat",
         {"f": scheme(["b", "a"], arrow(v("a"), v("b")))}, {"x": arrow(v("a"), v("b"))},
         result("Nat", {"f": scheme(["t0", "t1"], arrow(v("t1"), v("t0")))}, [], []), 0),
    case("conservative rename includes irrelevant range collisions", "Nat",
         {"f": scheme(["a"], v("a"))}, {"x": v("a")},
         result("Nat", {"f": scheme(["t0"], v("t0"))}, [], [instance({}, "Nat")]), 1),
    case("context free set unions every binding", arrow(v("a"), v("b")),
         {"x": scheme([], v("a")), "y": scheme([], v("b"))}, {},
         result(arrow(v("a"), v("b")), {"x": scheme([], v("a")), "y": scheme([], v("b"))}, [],
                [instance({}, arrow(v("a"), v("b"))), instance({}, arrow(v("a"), v("b")))])),
    case("only eligible variable is instantiated", arrow(v("a"), v("b")), {"x": scheme([], v("a"))}, {},
         result(arrow(v("a"), v("b")), {"x": scheme([], v("a"))}, ["b"],
                [instance({"b": "t0"}, arrow(v("a"), v("t0"))), instance({"b": "t1"}, arrow(v("a"), v("t1")))])),
    case("four independent instantiations", v("a"), {}, {},
         result(v("a"), {}, ["a"], [instance({"a": "t0"}, v("t0")), instance({"a": "t1"}, v("t1")),
                                      instance({"a": "t2"}, v("t2")), instance({"a": "t3"}, v("t3"))]), 4),
    case("zero instances still normalizes environment capture", v("a"),
         {"f": scheme(["a"], arrow(v("a"), v("b")))}, {"b": v("a")},
         result(v("a"), {"f": scheme(["t0"], arrow(v("t0"), v("a")))}, [], []), 0),
    case("explicit default count", "Bool", {}, {},
         result("Bool", {}, [], [instance({}, "Bool"), instance({}, "Bool")]), 2),
    case("independent repeated expanded subtrees", v("a"), {},
         {"a": arrow(v("b"), v("b")), "b": arrow(v("c"), v("c")), "c": "Bool"},
         result(arrow(arrow("Bool", "Bool"), arrow("Bool", "Bool")), {}, [],
                [instance({}, arrow(arrow("Bool", "Bool"), arrow("Bool", "Bool"))),
                 instance({}, arrow(arrow("Bool", "Bool"), arrow("Bool", "Bool")))])),
    case("unchanged binder order is not sorted", "Bool", {"f": scheme(["b", "a"], arrow(v("a"), v("b")))}, {},
         result("Bool", {"f": scheme(["b", "a"], arrow(v("a"), v("b")))}, [], [instance({}, "Bool")]), 1),
    case("term binding names do not reserve type variable names", v("a"), {"t0": scheme([], "Bool")}, {},
         result(v("a"), {"t0": scheme([], "Bool")}, ["a"], [instance({"a": "t0"}, v("t0"))]), 1),
    case("capture avoidance preserves free range variable while generalizing another", arrow(v("a"), v("c")),
         {"x": scheme(["b"], arrow(v("a"), v("b")))}, {"a": v("b")},
         result(arrow(v("b"), v("c")), {"x": scheme(["t0"], arrow(v("b"), v("t0")))}, ["c"],
                [instance({"c": "t1"}, arrow(v("b"), v("t1"))),
                 instance({"c": "t2"}, arrow(v("b"), v("t2")))])),
    case("same spelling bound in context is not a free context constraint", v("a"),
         {"id": scheme(["a"], arrow(v("a"), v("a")))}, {},
         result(v("a"), {"id": scheme(["a"], arrow(v("a"), v("a")))}, ["a"],
                [instance({"a": "t0"}, v("t0")), instance({"a": "t1"}, v("t1"))])),
]
CALLS = CASES + [CASES[10], CASES[0], CASES[6], CASES[1], CASES[10]]
EXPECTED = [value for _, _, value in CALLS]


def matches(actual):
    return json.dumps(actual, sort_keys=True) == json.dumps(
        {"values": EXPECTED, "unchanged": True, "stable_outputs": True, "independent": True}, sort_keys=True)


def run(candidate):
    payload = base64.b64encode(json.dumps([args for _, args, _ in CALLS]).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
def fingerprint(value):
    if type(value) is dict and all(type(key) is str for key in value):
        return ("dict",tuple((key,fingerprint(value[key])) for key in sorted(value)))
    if type(value) is list:
        return ("list",tuple(fingerprint(item) for item in value))
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
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args);inputs.append((supplied,fingerprint(supplied)));input_ids.update(mutable_ids(supplied))
    value=module.generalize_instantiate(**supplied)
    outputs.append((value,fingerprint(value)));values.append(value)
    unchanged=unchanged and all(fingerprint(prior)==before for prior,before in inputs)
    stable=stable and all(fingerprint(prior)==before for prior,before in outputs)
    independent=independent and disjoint(values,input_ids)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged,"stable_outputs":stable,"independent":independent}))'''
    try:
        process = subprocess.run([sys.executable, "-B", "-c", runner,
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
