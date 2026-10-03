import base64
import json
import pathlib
import subprocess
import sys


def ins(name, kind, *uses):
    return {"id": name, "kind": kind, "uses": list(uses)}


def block(instructions, successors=(), count=0):
    return {"instructions": instructions, "successors": list(successors), "profile_count": count}


_OMITTED = object()


def case(name, entry, blocks, reachable, kept, removed, parameters=_OMITTED):
    args = {"entry": entry, "blocks": blocks}
    if parameters is not _OMITTED:
        args["parameters"] = parameters
    return name, args, {"reachable": reachable, "kept": kept, "removed": removed}


# Literal reachability and live-instruction witnesses, not a second DCE pass.
CASES = [
    case("minimal zero-profile return and omitted parameters", "E",
         {"E": block([ins("r", "return")])}, ["E"], {"E": ["r"]}, []),
    case("unused pure result removed", "E",
         {"E": block([ins("a", "pure"), ins("r", "return")], count=7)}, ["E"], {"E": ["r"]}, ["a"]),
    case("unused pure chain removed transitively", "E",
         {"E": block([ins("z", "pure"), ins("a", "pure", "z"), ins("b", "pure", "a"), ins("r", "return")])},
         ["E"], {"E": ["r"]}, ["a", "b", "z"]),
    case("return retains full transitive producer chain", "E",
         {"E": block([ins("z", "pure"), ins("a", "pure", "z"), ins("b", "pure", "a"), ins("r", "return", "b")])},
         ["E"], {"E": ["z", "a", "b", "r"]}, []),
    case("unused effect result still retains its operand", "E",
         {"E": block([ins("c", "pure"), ins("fx", "effect", "c"), ins("dead", "pure"), ins("r", "return")])},
         ["E"], {"E": ["c", "fx", "r"]}, ["dead"]),
    case("effect with no result users remains required", "E",
         {"E": block([ins("fx", "effect"), ins("r", "return")])}, ["E"], {"E": ["fx", "r"]}, []),
    case("branch retains condition and its producers", "E",
         {"E": block([ins("p", "pure"), ins("c", "pure", "p"), ins("dead", "pure"), ins("br", "branch", "c")], ["L", "R"], 20),
          "L": block([ins("rL", "return")], count=10), "R": block([ins("rR", "return")], count=10)},
         ["E", "L", "R"], {"E": ["p", "c", "br"], "L": ["rL"], "R": ["rR"]}, ["dead"]),
    case("zero observed successor still has required effect", "E",
         {"E": block([ins("br", "branch", "p")], ["L", "R"], 100),
          "L": block([ins("rL", "return")], count=100),
          "R": block([ins("cold", "effect"), ins("rR", "return")], count=0)},
         ["E", "L", "R"], {"E": ["br"], "L": ["rL"], "R": ["cold", "rR"]}, [], ["p"]),
    case("zero observed entry is still structurally reachable", "E",
         {"E": block([ins("fx", "effect"), ins("jump", "branch")], ["B"], 0),
          "B": block([ins("r", "return")], count=0)},
         ["B", "E"], {"E": ["fx", "jump"], "B": ["r"]}, []),
    case("unreachable effects and producers are removed", "E",
         {"E": block([ins("r", "return")]),
          "U": block([ins("u", "pure"), ins("fx", "effect", "u"), ins("rU", "return")])},
         ["E"], {"E": ["r"]}, ["fx", "rU", "u"]),
    case("profile annotation cannot make disconnected code reachable", "E",
         {"E": block([ins("r", "return")]), "U": block([ins("fx", "effect"), ins("rU", "return")], count=10000)},
         ["E"], {"E": ["r"]}, ["fx", "rU"]),
    case("disconnected control cycle does not retain its effects", "E",
         {"E": block([ins("r", "return")]),
          "U": block([ins("u", "pure"), ins("fx", "effect", "u"), ins("jU", "branch")], ["V"]),
          "V": block([ins("d", "pure"), ins("jV", "branch")], ["U"])},
         ["E"], {"E": ["r"]}, ["d", "fx", "jU", "jV", "u"]),
    case("reachable loop keeps its control and repeated effect", "E",
         {"E": block([ins("jE", "branch")], ["H"]),
          "H": block([ins("dead", "pure"), ins("fx", "effect", "p"), ins("jH", "branch", "p")], ["H", "X"]),
          "X": block([ins("rX", "return")])},
         ["E", "H", "X"], {"E": ["jE"], "H": ["fx", "jH"], "X": ["rX"]}, ["dead"], ["p"]),
    case("value needed across a block boundary is retained", "E",
         {"E": block([ins("x", "pure"), ins("jE", "branch")], ["B"], 1),
          "B": block([ins("y", "pure", "x"), ins("r", "return", "y")], count=1)},
         ["B", "E"], {"E": ["x", "jE"], "B": ["y", "r"]}, []),
    case("effect result is a value producer for another effect", "E",
         {"E": block([ins("p", "pure"), ins("fx", "effect", "p"), ins("dead", "pure"),
                      ins("gx", "effect", "fx"), ins("r", "return")])},
         ["E"], {"E": ["p", "fx", "gx", "r"]}, ["dead"]),
    case("shared producer is needed by both arms", "E",
         {"E": block([ins("c", "pure"), ins("br", "branch", "p")], ["L", "R"]),
          "L": block([ins("fx", "effect", "c"), ins("rL", "return")]),
          "R": block([ins("rR", "return", "c")])},
         ["E", "L", "R"], {"E": ["c", "br"], "L": ["fx", "rL"], "R": ["rR"]}, [], ["p"]),
    case("keep original instruction order not lexical order", "E",
         {"E": block([ins("z", "pure"), ins("A", "pure", "z"), ins("m", "effect", "A"), ins("R", "return")])},
         ["E"], {"E": ["z", "A", "m", "R"]}, []),
    case("explicit None parameters", "E", {"E": block([ins("r", "return")])},
         ["E"], {"E": ["r"]}, [], None),
    case("explicit empty parameters", "E", {"E": block([ins("r", "return")])},
         ["E"], {"E": ["r"]}, [], []),
    case("duplicate operands do not duplicate kept instructions", "E",
         {"E": block([ins("c", "pure"), ins("v", "pure", "c", "c"), ins("r", "return", "v")])},
         ["E"], {"E": ["c", "v", "r"]}, []),
    case("parameter shares a block name but has no producer", "E",
         {"E": block([ins("r", "return", "E")])}, ["E"], {"E": ["r"]}, [], ["E"]),
    case("output block order is lexical while instruction order is original", "z",
         {"z": block([ins("jump", "branch")], ["A"], 1),
          "A": block([ins("unused", "pure"), ins("effect", "effect"), ins("return", "return")], count=1)},
         ["A", "z"], {"A": ["effect", "return"], "z": ["jump"]}, ["unused"]),
    case("maximum block chain carries entry value to final return", "A",
         {"A": block([ins("x", "pure"), ins("jA", "branch")], ["B"]),
          "B": block([ins("jB", "branch")], ["C"]), "C": block([ins("jC", "branch")], ["D"]),
          "D": block([ins("jD", "branch")], ["E"]), "E": block([ins("jE", "branch")], ["F"]),
          "F": block([ins("jF", "branch")], ["G"]), "G": block([ins("jG", "branch")], ["H"]),
          "H": block([ins("rH", "return", "x")])},
         list("ABCDEFGH"), {"A": ["x", "jA"], "B": ["jB"], "C": ["jC"], "D": ["jD"],
                           "E": ["jE"], "F": ["jF"], "G": ["jG"], "H": ["rH"]}, []),
]
# Closed-form boundary witness: 63 unreferenced pure constants and one return.
DEAD_IDS = [f"d{i:02}" for i in range(63)]
CASES.append(case("maximum instruction count unused constants", "E",
                  {"E": block([ins(name, "pure") for name in DEAD_IDS] + [ins("r", "return")])},
                  ["E"], {"E": ["r"]}, DEAD_IDS))
CALLS = CASES + [CASES[7], CASES[0], CASES[9], CASES[7], CASES[0]]
EXPECTED = [value for _, _, value in CALLS]


def matches(actual):
    return json.dumps(actual, sort_keys=True) == json.dumps(
        {"values": EXPECTED, "unchanged": True, "independent": True, "unaliased": True}, sort_keys=True)


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
values=[];history=[];seen=set();input_ids=set();unchanged=True;independent=True;unaliased=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args);history.append((supplied,fingerprint(supplied)));input_ids.update(mutable_ids(supplied))
    value=module.dce_slice(**supplied)
    fingerprint(value)
    ids=mutable_ids(value);independent=independent and not bool(ids & seen);seen.update(ids)
    values.append(value)
    unchanged=unchanged and all(fingerprint(prior)==old for prior,old in history)
    unaliased=unaliased and not bool(seen & input_ids)
fingerprint(values)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged,"independent":independent,"unaliased":unaliased}))'''
    try:
        result = subprocess.run([sys.executable, "-B", "-c", runner,
                                 str(pathlib.Path(candidate).resolve()), payload],
                                capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in result.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if result.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


if __name__ == "__main__":
    ok = len(sys.argv) == 2 and matches(run(sys.argv[1]))
    print("PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
