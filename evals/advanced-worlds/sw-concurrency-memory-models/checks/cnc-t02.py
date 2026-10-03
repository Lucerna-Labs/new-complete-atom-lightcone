import base64
import json
import pathlib
import subprocess
import sys


def store(identifier, thread, obj="x", value=1, order="release"):
    return {"id": identifier, "thread": thread, "kind": "store", "order": order,
            "object": obj, "value": value}


def read(identifier, thread, source, obj="x", order="acquire", kind="load"):
    return {"id": identifier, "thread": thread, "kind": kind, "order": order,
            "object": obj, "reads_from": source}


def rmw(identifier, thread, source, obj="x", value=2, order="relaxed"):
    return {**read(identifier, thread, source, obj, order, "rmw"), "value": value}


def fence(identifier, thread, order):
    return {"id": identifier, "thread": thread, "kind": "fence", "order": order}


def case(name, events, orders, sequences, pairs):
    # Only package literal witness/oracle data; no synchronization rule is run here.
    return (name, {"events": events, "modification_orders": orders},
            {"release_sequences": sequences,
             "synchronizes_with": sorted([list(pair) for pair in pairs])})


CASES = [
    case("empty", [], {}, {}, []),
    case("relaxed source supplies no release", [store("w", "p", order="relaxed"),
         read("r", "q", "w")], {"x": ["w"]}, {}, []),
    case("direct release acquire", [store("w", "p"), read("r", "q", "w")],
         {"x": ["w"]}, {"w": ["w"]}, [("w", "r")]),
    case("equal values do not identify read origin", [store("i", "p", order="relaxed"),
         store("h", "p"), read("r", "q", "i")],
         {"x": ["i", "h"]}, {"h": ["h"]}, []),
    case("same values actual release origin", [store("i", "p", order="relaxed"),
         store("h", "p"), read("r", "q", "h")],
         {"x": ["i", "h"]}, {"h": ["h"]}, [("h", "r")]),
    case("relaxed reader supplies no acquire", [store("h", "p"),
         read("r", "q", "h", order="relaxed")],
         {"x": ["h"]}, {"h": ["h"]}, []),
    case("failed CAS may acquire but never modifies", [store("h", "p"),
         read("f", "q", "h", kind="cas_fail")],
         {"x": ["h"]}, {"h": ["h"]}, [("h", "f")]),
    case("failed CAS does not break modification sequence", [store("h", "p"),
         read("f", "q", "h", kind="cas_fail"), rmw("m", "q", "h"),
         read("r", "s", "m")], {"x": ["h", "m"]},
         {"h": ["h", "m"]}, [("h", "f"), ("h", "r")]),
    case("release RMW continues older head and starts new head", [store("h", "p"),
         rmw("a", "q", "h", order="release"), rmw("b", "s", "a", value=3),
         read("r", "t", "b")], {"x": ["h", "a", "b"]},
         {"h": ["h", "a", "b"], "a": ["a", "b"]}, [("h", "r"), ("a", "r")]),
    case("acqrel RMW has both roles", [store("h", "p"),
         rmw("m", "q", "h", order="acq_rel"), read("r", "s", "m")],
         {"x": ["h", "m"]}, {"h": ["h", "m"], "m": ["m"]},
         [("h", "m"), ("h", "r"), ("m", "r")]),
    case("acquire-only RMW is no new release head", [store("h", "p"),
         rmw("m", "q", "h", order="acquire"), read("r", "s", "m")],
         {"x": ["h", "m"]}, {"h": ["h", "m"]}, [("h", "m"), ("h", "r")]),
    case("same-thread plain relaxed store breaks old head", [store("h", "p"),
         store("s", "p", value=2, order="relaxed"), rmw("m", "q", "s", value=3),
         read("r", "t", "m")], {"x": ["h", "s", "m"]}, {"h": ["h"]}, []),
    case("plain release store creates only its own new chain", [store("h", "p"),
         store("s", "p", value=2), rmw("m", "q", "s", value=3), read("r", "t", "m")],
         {"x": ["h", "s", "m"]}, {"h": ["h"], "s": ["s", "m"]}, [("s", "r")]),
    case("release RMW publishes without acquiring predecessor", [store("i", "p", value=0, order="relaxed"),
         rmw("m", "q", "i", order="release"), read("r", "s", "m")],
         {"x": ["i", "m"]}, {"m": ["m"]}, [("m", "r")]),
    case("SC write and read carry release acquire roles", [store("h", "p", order="seq_cst"),
         read("r", "q", "h", order="seq_cst")], {"x": ["h"]}, {"h": ["h"]}, [("h", "r")]),
    case("unrelated object and equal value", [store("h", "p"),
         store("y", "q", obj="y", order="relaxed"), read("r", "s", "y", obj="y")],
         {"x": ["h"], "y": ["y"]}, {"h": ["h"]}, []),
    case("release fence to acquire atomic", [fence("a", "p", "release"),
         store("x", "p", order="relaxed"), read("y", "q", "x")],
         {"x": ["x"]}, {}, [("a", "y")]),
    case("release atomic to acquire fence", [store("x", "p"),
         read("y", "q", "x", order="relaxed"), fence("b", "q", "acquire")],
         {"x": ["x"]}, {"x": ["x"]}, [("x", "b")]),
    case("fence to fence with relaxed carrier", [fence("a", "p", "release"),
         store("x", "p", order="relaxed"), read("y", "q", "x", order="relaxed"),
         fence("b", "q", "acquire")], {"x": ["x"]}, {}, [("a", "b")]),
    case("release fence after store is too late", [store("x", "p", order="relaxed"),
         fence("a", "p", "release"), read("y", "q", "x", order="relaxed"),
         fence("b", "q", "acquire")], {"x": ["x"]}, {}, []),
    case("acquire fence before load is too early", [store("x", "p"),
         fence("b", "q", "acquire"), read("y", "q", "x", order="relaxed")],
         {"x": ["x"]}, {"x": ["x"]}, []),
    case("cross-thread list order is not sequenced-before", [fence("a", "p", "release"),
         store("x", "q", order="relaxed"), read("y", "s", "x")],
         {"x": ["x"]}, {}, []),
    case("later unrelated equal store is no fence carrier", [fence("a", "p", "release"),
         store("x", "p", order="relaxed"), store("z", "q", order="relaxed"),
         read("y", "s", "z")], {"x": ["x", "z"]}, {}, []),
    case("fence carrier hypothetical sequence follows RMW", [fence("a", "p", "release"),
         store("x", "p", order="relaxed"), rmw("m", "q", "x"),
         read("y", "s", "m", order="relaxed"), fence("b", "s", "acquire")],
         {"x": ["x", "m"]}, {}, [("a", "b")]),
    case("acquire-only fence cannot publish", [fence("a", "p", "acquire"),
         store("x", "p", order="relaxed"), read("y", "q", "x")],
         {"x": ["x"]}, {}, []),
    case("release-only fence cannot acquire", [store("x", "p"),
         read("y", "q", "x", order="relaxed"), fence("b", "q", "release")],
         {"x": ["x"]}, {"x": ["x"]}, []),
    case("relaxed fences have no synchronization role", [fence("a", "p", "relaxed"),
         store("x", "p", order="relaxed"), read("y", "q", "x", order="relaxed"),
         fence("b", "q", "relaxed")], {"x": ["x"]}, {}, []),
    case("SC fences can surround relaxed carriers", [fence("a", "p", "seq_cst"),
         store("x", "p", order="relaxed"), read("y", "q", "x", order="relaxed"),
         fence("b", "q", "seq_cst")], {"x": ["x"]}, {}, [("a", "b")]),
    case("acqrel fence and acquire read give both direct edges", [fence("a", "p", "acq_rel"),
         store("x", "p", order="relaxed"), read("y", "q", "x"), fence("b", "q", "acq_rel")],
         {"x": ["x"]}, {}, [("a", "y"), ("a", "b")]),
    case("multiple qualified fences", [fence("a1", "p", "release"), fence("a2", "p", "release"),
         store("x", "p", order="relaxed"), read("y", "q", "x", order="relaxed"),
         fence("b1", "q", "acquire"), fence("b2", "q", "acquire")],
         {"x": ["x"]}, {}, [("a1", "b1"), ("a1", "b2"), ("a2", "b1"), ("a2", "b2")]),
    case("failed CAS can carry an acquire fence", [store("h", "p"),
         read("f", "q", "h", order="relaxed", kind="cas_fail"), fence("b", "q", "acquire")],
         {"x": ["h"]}, {"h": ["h"]}, [("h", "b")]),
    case("same-thread direct edges are intentionally not reported", [store("h", "p"), read("r", "p", "h")],
         {"x": ["h"]}, {"h": ["h"]}, []),
    case("same-thread RMW membership is retained", [store("h", "p"),
         rmw("m", "p", "h", order="acq_rel"), read("r", "q", "m")],
         {"x": ["h", "m"]}, {"h": ["h", "m"], "m": ["m"]}, [("h", "r"), ("m", "r")]),
    case("global event list is not modification order", [read("r", "t", "b"),
         rmw("b", "s", "a", value=3), store("h", "p"), rmw("a", "q", "h")],
         {"x": ["h", "a", "b"]}, {"h": ["h", "a", "b"]}, [("h", "r")]),
    case("do not report transitive HB as direct SW", [store("a", "p"), read("b", "q", "a"),
         store("c", "q", obj="y"), read("d", "s", "c", obj="y")],
         {"x": ["a"], "y": ["c"]}, {"a": ["a"], "c": ["c"]}, [("a", "b"), ("c", "d")]),
    case("multiple carriers deduplicate a fence pair", [fence("a", "p", "release"),
         store("x", "p", order="relaxed"), store("z", "p", obj="z", order="relaxed"),
         read("y", "q", "x", order="relaxed"), read("v", "q", "z", obj="z", order="relaxed"),
         fence("b", "q", "acquire")], {"x": ["x"], "z": ["z"]}, {}, [("a", "b")]),
    case("fences alone cannot communicate", [fence("a", "p", "release"), fence("b", "q", "acquire")],
         {}, {}, []),
    case("release head reaches fence through relaxed RMW", [store("h", "p"),
         rmw("m", "q", "h"), read("y", "s", "m", order="relaxed"), fence("b", "s", "acquire")],
         {"x": ["h", "m"]}, {"h": ["h", "m"]}, [("h", "b")]),
    case("release fence reaches acquire through hypothetical RMW chain", [fence("a", "p", "release"),
         store("x", "p", order="relaxed"), rmw("m", "q", "x"), read("y", "s", "m")],
         {"x": ["x", "m"]}, {}, [("a", "y")]),
    case("release-only RMW read can carry a later acquire fence", [store("h", "p"),
         rmw("m", "q", "h", order="release"), fence("b", "q", "acquire")],
         {"x": ["h", "m"]}, {"h": ["h", "m"], "m": ["m"]}, [("h", "b")]),
    case("acquire RMW can observe a release-fence carrier", [fence("a", "p", "release"),
         store("x", "p", order="relaxed"), rmw("m", "q", "x", order="acquire")],
         {"x": ["x", "m"]}, {}, [("a", "m")]),
    case("SC fences still need a carrier for synchronization", [fence("a", "p", "seq_cst"),
         fence("b", "q", "seq_cst")], {}, {}, []),
    case("SC stores on different objects do not synchronize each other", [store("a", "p", order="seq_cst"),
         store("b", "q", obj="y", order="seq_cst")],
         {"x": ["a"], "y": ["b"]}, {"a": ["a"], "b": ["b"]}, []),
]
CALLS = CASES + [CASES[11], CASES[0], CASES[2], CASES[11]]
EXPECTED = [value for _, _, value in CALLS]


def matches(actual):
    expected = {"values": EXPECTED, "unchanged": True}
    return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)


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
    if type(value) in (str,int,type(None)):
        return (type(value).__name__,value)
    raise TypeError("value outside the exact input/output types")
values=[];unchanged=True
for args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args)
    value=module.synchronization_witness(**supplied)
    fingerprint(value)
    values.append(value)
    unchanged=unchanged and fingerprint(supplied)==fingerprint(args)
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged}))'''
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
