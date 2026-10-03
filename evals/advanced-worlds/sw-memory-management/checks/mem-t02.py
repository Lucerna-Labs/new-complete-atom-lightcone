import base64
import json
import pathlib
import subprocess
import sys


def outcome(incoming=(), marked=(), unmarked=()):
    return {"incoming": list(incoming), "marked": list(marked), "unmarked": list(unmarked)}


_OMITTED = object()


def case(name, graph, roots, expected, young=_OMITTED):
    args = {"graph": graph, "roots": roots}
    if young is not _OMITTED:
        args["young"] = young
    return name, args, expected


# Hand-specified closures. No reference implementation generates expected sets.
CASES = [
    case("empty default full collection", {}, [], outcome()),
    case("empty explicit full collection", {}, [], outcome(), None),
    case("empty young selection", {}, [], outcome(), []),
    case("unrooted singleton", {"A": []}, [], outcome(unmarked=["A"])),
    case("rooted singleton", {"A": []}, ["A"], outcome(marked=["A"])),
    case("unrooted self cycle", {"A": ["A"]}, [], outcome(unmarked=["A"])),
    case("rooted self cycle duplicates", {"A": ["A", "A"]}, ["A", "A"], outcome(marked=["A"])),
    case("rooted and isolated cycles", {"A": ["B"], "B": ["C"], "C": ["B"], "D": ["D"]},
         ["A"], outcome(marked=["A", "B", "C"], unmarked=["D"])),
    case("canonical mixed case order", {"z": [], "A_1": ["b"], "b": []},
         ["z", "A_1", "z"], outcome(marked=["A_1", "b", "z"])),
    case("duplicate edges do not duplicate output", {"A": ["B", "B", "C"], "B": ["C"], "C": []},
         ["A", "A"], outcome(marked=["A", "B", "C"])),
    case("full young set matches full marking", {"A": ["B"], "B": [], "C": []},
         ["A"], outcome(marked=["A", "B"], unmarked=["C"]), ["C", "B", "A"]),
    case("empty young set ignores all objects", {"A": ["B"], "B": []},
         ["A"], outcome(), []),
    case("direct young root", {"O": [], "Y": ["Z"], "Z": []},
         ["Y"], outcome(marked=["Y", "Z"]), ["Y", "Z"]),
    case("rooted old source", {"O": ["Y"], "Y": [], "Z": []},
         ["O"], outcome(["Y"], ["Y"], ["Z"]), ["Y", "Z"]),
    case("old source reached through another old object", {"O": ["P"], "P": ["Y"], "Y": []},
         ["O"], outcome(["Y"], ["Y"]), ["Y"]),
    case("unreachable old source conservatively retains young", {"O": ["Y"], "Y": []},
         [], outcome(["Y"], ["Y"]), ["Y"]),
    case("same unreachable graph in full mode", {"O": ["Y"], "Y": []},
         [], outcome(unmarked=["O", "Y"])),
    case("incoming root closes a young cycle", {"O": ["X"], "X": ["Y"], "Y": ["X"], "Z": []},
         [], outcome(["X"], ["X", "Y"], ["Z"]), ["X", "Y", "Z"]),
    case("unseeded young cycle remains unmarked", {"O": [], "X": ["Y"], "Y": ["X"]},
         ["O"], outcome(unmarked=["X", "Y"]), ["X", "Y"]),
    case("young edge to old does not add old to marked", {"Y": ["O"], "O": [], "Z": []},
         ["Y"], outcome(marked=["Y"], unmarked=["Z"]), ["Z", "Y"]),
    case("old return edge is incoming even with young origin", {"Y": ["O"], "O": ["Z"], "Z": []},
         ["Y"], outcome(["Z"], ["Y", "Z"]), ["Y", "Z"]),
    case("promotion-created incoming edge snapshot", {"P": ["Z"], "Z": []},
         ["P"], outcome(["Z"], ["Z"]), ["Z"]),
    case("same parent before promotion belongs to selected set", {"P": ["Z"], "Z": []},
         ["P"], outcome(marked=["P", "Z"]), ["P", "Z"]),
    case("incoming identity deduplicated and sorted", {"O": ["z", "A", "z"], "P": ["A"], "A": [], "z": [], "x": []},
         [], outcome(["A", "z"], ["A", "z"], ["x"]), ["z", "x", "A"]),
    case("incoming means direct targets not their closure", {"O": ["A"], "A": ["B"], "B": ["C"], "C": []},
         [], outcome(["A"], ["A", "B", "C"]), ["A", "B", "C"]),
    case("all graph objects may be uncollected", {"O": ["P"], "P": ["O"]},
         ["O", "P"], outcome(), []),
    case("maximum object count full chain", {"A": ["B"], "B": ["C"], "C": ["D"], "D": ["E"],
         "E": ["F"], "F": ["G"], "G": ["H"], "H": ["I"], "I": ["J"], "J": ["K"],
         "K": ["L"], "L": ["M"], "M": ["N"], "N": ["O"], "O": ["P"], "P": []},
         ["A"], outcome(marked=list("ABCDEFGHIJKLMNOP"))),
    case("unrooted old chain tail remains conservative", {"A": ["B"], "B": ["C"], "C": ["D"], "D": ["E"],
         "E": ["F"], "F": ["G"], "G": ["H"], "H": ["I"], "I": ["J"], "J": ["K"],
         "K": ["L"], "L": ["M"], "M": ["N"], "N": ["O"], "O": ["P"], "P": []},
         [], outcome(["I"], list("IJKLMNOP")), list("IJKLMNOP")),
    case("maximum duplicate root and field lengths", {"A": ["B"] * 32, "B": []},
         ["A"] * 32, outcome(marked=["A", "B"])),
]
CALLS = CASES + [CASES[15], CASES[0], CASES[4], CASES[15]]
EXPECTED = [value for _, _, value in CALLS]


def matches(actual):
    return json.dumps(actual, sort_keys=True) == json.dumps(
        {"values": EXPECTED, "unchanged": True, "separate": True}, sort_keys=True)


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
values=[];inputs=[];before=[];seen=set();separate=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args);inputs.append(supplied);before.append(fingerprint(supplied))
    value=module.trace_collection(**supplied)
    fingerprint(value)
    ids=mutable_ids(value);separate=separate and not bool(ids & seen);seen.update(ids)
    values.append(value)
unchanged=all(fingerprint(value)==old for value,old in zip(inputs,before))
fingerprint(values)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged,"separate":separate}))'''
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
