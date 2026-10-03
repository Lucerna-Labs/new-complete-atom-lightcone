import base64
import json
import pathlib
import subprocess
import sys


def text(value):
    return {"tag": "string", "value": value}


def number(value):
    return {"tag": "number", "value": value}


def boolean(value):
    return {"tag": "boolean", "value": value}


def undefined():
    return {"tag": "undefined"}


def null():
    return {"tag": "null"}


def obj(own=None, inherited=None):
    return {"tag": "object", "own": {} if own is None else own,
            "inherited": {} if inherited is None else inherited}


_ABSENT = object()


def accepted(name, age=_ABSENT):
    data = {"name": name}
    if age is not _ABSENT:
        data["age"] = age
    return {"ok": True, "errors": [], "data": data}


def rejected(*errors):
    return {"ok": False, "errors": list(errors), "data": None}


# Literal policy decisions and projections; no validator computes the oracles.
CASES = [
    ("undefined is not a plain object", undefined(), rejected("object-required")),
    ("null is not a plain object", null(), rejected("object-required")),
    ("boolean is not a plain object", boolean(False), rejected("object-required")),
    ("number is not a plain object", number(0), rejected("object-required")),
    ("string is not a plain object", text("Ada"), rejected("object-required")),
    ("empty own map lacks name", obj(), rejected("name-missing")),
    ("inherited string name is insufficient", obj(inherited={"name": text("Ada")}), rejected("name-missing")),
    ("own undefined name is present but mistyped", obj({"name": undefined()}), rejected("name-type")),
    ("own null name is mistyped", obj({"name": null()}), rejected("name-type")),
    ("own numeric name is not coerced", obj({"name": number(7)}), rejected("name-type")),
    ("own boolean name is not coerced", obj({"name": boolean(True)}), rejected("name-type")),
    ("own string and absent age", obj({"name": text("Ada")}), accepted("Ada")),
    ("empty string name is allowed", obj({"name": text("")}), accepted("")),
    ("present undefined age is not absence", obj({"name": text("Ada"), "age": undefined()}), rejected("age-type")),
    ("present null age is not absence", obj({"name": text("Ada"), "age": null()}), rejected("age-type")),
    ("numeric text age is not coerced", obj({"name": text("Ada"), "age": text("10")}), rejected("age-type")),
    ("boolean age is not a numeric tagged value", obj({"name": text("Ada"), "age": boolean(True)}), rejected("age-type")),
    ("zero numeric age remains present", obj({"name": text("Ada"), "age": number(0)}), accepted("Ada", 0)),
    ("negative age passes this type-only gate", obj({"name": text("Ada"), "age": number(-1)}), accepted("Ada", -1)),
    ("minimum numeric payload", obj({"name": text("Ada"), "age": number(-1000)}), accepted("Ada", -1000)),
    ("maximum numeric payload", obj({"name": text("Ada"), "age": number(1000)}), accepted("Ada", 1000)),
    ("missing name and present undefined age collect both errors", obj({"age": undefined()}), rejected("name-missing", "age-type")),
    ("error order ignores own map insertion order", obj({"age": undefined(), "name": boolean(False)}), rejected("name-type", "age-type")),
    ("mistyped own name is not repaired by inherited name", obj({"name": number(7)}, {"name": text("Ada")}), rejected("name-type")),
    ("own name overrides irrelevant inherited name", obj({"name": text("Ada")}, {"name": number(7)}), accepted("Ada")),
    ("inherited undefined age is ignored", obj({"name": text("Ada")}, {"age": undefined()}), accepted("Ada")),
    ("inherited string age is ignored", obj({"name": text("Ada")}, {"age": text("bad")}), accepted("Ada")),
    ("inherited numeric age is not projected", obj({"name": text("Ada")}, {"age": number(42)}), accepted("Ada")),
    ("valid own age is not displaced by inherited value", obj({"name": text("Ada"), "age": number(5)}, {"age": text("bad")}), accepted("Ada", 5)),
    ("inherited number cannot repair own undefined age", obj({"name": text("Ada"), "age": undefined()}, {"age": number(5)}), rejected("age-type")),
    ("extra own properties are ignored and not projected", obj({"name": text("Ada"), "extra": undefined(), "__proto__": text("data")}), accepted("Ada")),
    ("property names are case sensitive", obj({"Name": text("Ada"), "Age": number(5)}), rejected("name-missing")),
    ("string payload is preserved without trimming", obj({"name": text(" Ada "), "age": number(5)}), accepted(" Ada ", 5)),
    ("maximum field maps preserve only the two validated own fields",
     obj({"name": text("A" * 32), "age": number(8), "p0": number(1), "p1": text("x"),
          "p2": boolean(False), "p3": null(), "p4": undefined(), "p5": number(2)},
         {"name": text("other"), "age": undefined(), "p0": null(), "p1": boolean(True),
          "p2": number(3), "p3": text("q"), "p4": null(), "p5": number(4)}),
     accepted("A" * 32, 8)),
    ("valid age cannot compensate for missing own name", obj({"age": number(3)}, {"name": text("Ada")}), rejected("name-missing")),
    ("own undefined name and numeric age have one error", obj({"name": undefined(), "age": number(3)}), rejected("name-type")),
]
CALLS = CASES + [CASES[17], CASES[5], CASES[0], CASES[17], CASES[13]]
EXPECTED = [value for _, _, value in CALLS]


def matches(actual):
    return json.dumps(actual, sort_keys=True) == json.dumps(
        {"values": EXPECTED, "unchanged": True, "stable_outputs": True, "independent": True}, sort_keys=True)


def run(candidate):
    payload = base64.b64encode(json.dumps([value for _, value, _ in CALLS]).encode()).decode()
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
for data in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(data);inputs.append((supplied,fingerprint(supplied)));input_ids.update(mutable_ids(supplied))
    value=module.validate_record(supplied)
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
