import base64
import json
import pathlib
import subprocess
import sys


def block(size, *successors):
    return {"size": size, "successors": list(successors)}


def definition(block, position):
    return {"block": block, "position": position}


def ordinary(value, block, position):
    return {"kind": "ordinary", "value": value, "block": block, "position": position}


def phi(value, block, predecessor):
    return {"kind": "phi", "value": value, "block": block, "predecessor": predecessor}


_OMITTED = object()


def case(name, entry, blocks, definitions, uses, dominators, available, parameters=_OMITTED):
    args = {"entry": entry, "blocks": blocks, "definitions": definitions, "uses": uses}
    if parameters is not _OMITTED:
        args["parameters"] = parameters
    return name, args, {"dominators": dominators, "available": available}


# Dominator sets and availability answers are independently hand specified.
CASES = [
    case("minimal graph and omitted parameters", "E", {"E": block(0)}, {}, [], {"E": ["E"]}, []),
    case("explicit None parameters", "E", {"E": block(0)}, {}, [], {"E": ["E"]}, [], None),
    case("explicit empty parameters", "E", {"E": block(0)}, {}, [], {"E": ["E"]}, [], []),
    case("strict same-block order", "E", {"E": block(2)}, {"v": definition("E", 0)},
         [ordinary("v", "E", 0), ordinary("v", "E", 1)], {"E": ["E"]}, [False, True]),
    case("late definition cannot serve earlier or same instruction", "E", {"E": block(4)},
         {"v": definition("E", 2)}, [ordinary("v", "E", i) for i in range(4)],
         {"E": ["E"]}, [False, False, False, True]),
    case("parameter available at first position", "E", {"E": block(1)}, {},
         [ordinary("p", "E", 0)], {"E": ["E"]}, [True], ["p"]),
    case("chain dominance and reverse unavailable use", "E",
         {"E": block(1, "B"), "B": block(1, "C"), "C": block(2)},
         {"v": definition("E", 0), "w": definition("C", 0)},
         [ordinary("v", "B", 0), ordinary("v", "C", 0), ordinary("w", "B", 0),
          ordinary("w", "C", 0), ordinary("w", "C", 1)],
         {"E": ["E"], "B": ["B", "E"], "C": ["B", "C", "E"]},
         [True, True, False, False, True]),
    case("diamond incoming edge differs from merge dominance", "E",
         {"E": block(1, "P", "Q"), "P": block(1, "M"), "Q": block(1, "M"), "M": block(2)},
         {"e": definition("E", 0), "p": definition("P", 0), "q": definition("Q", 0), "m": definition("M", 0)},
         [ordinary("p", "M", 1), ordinary("q", "M", 1), ordinary("e", "M", 1),
          phi("p", "M", "P"), phi("q", "M", "Q"), phi("p", "M", "Q"),
          phi("m", "M", "P"), ordinary("m", "M", 0), ordinary("m", "M", 1)],
         {"E": ["E"], "P": ["E", "P"], "Q": ["E", "Q"], "M": ["E", "M"]},
         [False, False, True, True, True, False, False, False, True]),
    case("phi sees predecessor end including its last definition", "E",
         {"E": block(0, "P"), "P": block(4, "M"), "M": block(1)},
         {"p": definition("P", 3)}, [phi("p", "M", "P"), ordinary("p", "P", 3), ordinary("p", "M", 0)],
         {"E": ["E"], "P": ["E", "P"], "M": ["E", "M", "P"]}, [True, False, True]),
    case("self backedge and initial entry use differ", "E",
         {"E": block(1, "H"), "H": block(2, "H", "X"), "X": block(1)},
         {"e": definition("E", 0), "h": definition("H", 0), "late": definition("H", 1)},
         [phi("h", "H", "H"), phi("h", "H", "E"), phi("e", "H", "E"),
          phi("late", "H", "H"), ordinary("h", "H", 1), ordinary("late", "X", 0)],
         {"E": ["E"], "H": ["E", "H"], "X": ["E", "H", "X"]},
         [True, False, True, True, True, True]),
    case("loop body definition is available only on the backedge", "E",
         {"E": block(1, "H"), "H": block(2, "B", "X"), "B": block(1, "H"), "X": block(1)},
         {"e": definition("E", 0), "h": definition("H", 0), "b": definition("B", 0)},
         [phi("b", "H", "B"), ordinary("b", "H", 1), phi("h", "H", "B"),
          phi("b", "H", "E"), ordinary("b", "X", 0), ordinary("h", "X", 0)],
         {"E": ["E"], "H": ["E", "H"], "B": ["B", "E", "H"], "X": ["E", "H", "X"]},
         [True, False, True, False, False, True]),
    case("reachable irreducible cycle needs a fixed point", "E",
         {"E": block(0, "A", "B"), "A": block(1, "C"), "B": block(1, "C"),
          "C": block(2, "A", "B", "X"), "X": block(1)},
         {"a": definition("A", 0), "c": definition("C", 0)},
         [phi("a", "C", "A"), ordinary("a", "C", 1), phi("a", "B", "C"),
          phi("c", "A", "C"), ordinary("c", "X", 0), ordinary("a", "X", 0)],
         {"E": ["E"], "A": ["A", "E"], "B": ["B", "E"], "C": ["C", "E"], "X": ["C", "E", "X"]},
         [True, False, False, True, True, False]),
    case("common prebranch definition dominates the join", "E",
         {"E": block(0, "D"), "D": block(1, "P", "Q"), "P": block(0, "M"), "Q": block(0, "M"), "M": block(1)},
         {"d": definition("D", 0)}, [ordinary("d", "M", 0), phi("d", "M", "P"), phi("d", "M", "Q")],
         {"E": ["E"], "D": ["D", "E"], "P": ["D", "E", "P"], "Q": ["D", "E", "Q"], "M": ["D", "E", "M"]},
         [True, True, True]),
    case("parameters work on ordinary and phi loop uses", "E",
         {"E": block(0, "H"), "H": block(1, "H", "X"), "X": block(0)}, {},
         [ordinary("p", "H", 0), phi("p", "H", "E"), phi("p", "H", "H")],
         {"E": ["E"], "H": ["E", "H"], "X": ["E", "H", "X"]}, [True, True, True], ["p"]),
    case("dictionary order and case do not replace lexical output order", "z",
         {"M": block(1), "a": block(1, "M"), "z": block(0, "B", "a"), "B": block(1, "M")},
         {"v": definition("a", 0)}, [ordinary("v", "M", 0), phi("v", "M", "a")],
         {"z": ["z"], "B": ["B", "z"], "a": ["a", "z"], "M": ["M", "z"]}, [False, True]),
    case("duplicate queries preserve answer positions", "E", {"E": block(2)}, {"v": definition("E", 0)},
         [ordinary("v", "E", 1), ordinary("v", "E", 0), ordinary("v", "E", 1)],
         {"E": ["E"]}, [True, False, True]),
    case("maximum local position is still before predecessor end", "E",
         {"E": block(0, "P"), "P": block(8, "M"), "M": block(1)}, {"v": definition("P", 7)},
         [ordinary("v", "P", 7), phi("v", "M", "P")],
         {"E": ["E"], "P": ["E", "P"], "M": ["E", "M", "P"]}, [False, True]),
    case("maximum block count chain", "A",
         {"H": block(1), "G": block(0, "H"), "F": block(0, "G"), "E": block(0, "F"),
          "D": block(1, "E"), "C": block(0, "D"), "B": block(0, "C"), "A": block(1, "B")},
         {"a": definition("A", 0), "d": definition("D", 0)}, [ordinary("a", "H", 0), ordinary("d", "H", 0)],
         {"A": ["A"], "B": ["A", "B"], "C": ["A", "B", "C"], "D": ["A", "B", "C", "D"],
          "E": ["A", "B", "C", "D", "E"], "F": ["A", "B", "C", "D", "E", "F"],
          "G": ["A", "B", "C", "D", "E", "F", "G"], "H": ["A", "B", "C", "D", "E", "F", "G", "H"]},
         [True, True]),
    case("direct entry bypass prevents ordinary availability", "E",
         {"E": block(0, "B", "C"), "B": block(1, "C"), "C": block(1)}, {"v": definition("B", 0)},
         [ordinary("v", "C", 0), phi("v", "C", "B"), phi("v", "C", "E")],
         {"E": ["E"], "B": ["B", "E"], "C": ["C", "E"]}, [False, True, False]),
    case("maximum query count remains ordered", "E", {"E": block(2)}, {"v": definition("E", 0)},
         [ordinary("v", "E", 1)] * 64, {"E": ["E"]}, [True] * 64),
    case("parameter and block namespaces may share text", "E", {"E": block(1)}, {},
         [ordinary("E", "E", 0)], {"E": ["E"]}, [True], ["E"]),
    case("intermediate predecessor dominated by branch-local definition", "E",
         {"E": block(0, "P", "Q"), "P": block(1, "R"), "R": block(0, "M"), "Q": block(0, "M"), "M": block(1)},
         {"v": definition("P", 0)}, [phi("v", "M", "R"), phi("v", "M", "Q"), ordinary("v", "M", 0)],
         {"E": ["E"], "P": ["E", "P"], "R": ["E", "P", "R"], "Q": ["E", "Q"], "M": ["E", "M"]},
         [True, False, False]),
]
CALLS = CASES + [CASES[7], CASES[0], CASES[5], CASES[10], CASES[7]]
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
    value=module.ssa_availability(**supplied)
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
