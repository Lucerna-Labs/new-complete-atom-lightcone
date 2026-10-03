import base64
import json
import pathlib
import subprocess
import sys


def pair(value):
    return [value, 1] if type(value) is int else list(value)


def case(ts, tp, workers, work=1, traffic=1, peak=1, bandwidth=1, overhead=None):
    record = {"serial": pair(ts), "parallel": pair(tp), "workers": workers,
              "flops": work, "dram_bytes": traffic, "compute_peak": pair(peak),
              "bandwidth": pair(bandwidth)}
    if overhead is not None:
        record["overhead"] = pair(overhead)
    return record


def report(parallel, roofline):
    # These arguments are independently supplied literal answers. The helper
    # only formats pairs; it does not derive scaling or resource formulas.
    t1, core, total, serial, alpha, ideal, charged, efficiency = parallel
    intensity, ceiling, bound, resource = roofline
    return {"parallel": {
        "baseline_time": pair(t1), "ideal_parallel_time": pair(core),
        "parallel_time_with_overhead": pair(total),
        "baseline_serial_fraction": pair(serial),
        "ideal_parallel_serial_fraction": pair(alpha),
        "amdahl_speedup": pair(ideal), "gustafson_speedup": pair(ideal),
        "speedup_with_overhead": pair(charged),
        "efficiency_with_overhead": pair(efficiency),
    }, "roofline": {
        "operational_intensity": pair(intensity), "performance_ceiling": pair(ceiling),
        "time_lower_bound": pair(bound), "limiting_resource": resource,
    }}


BASE = (2, (3, 2), (3, 2), (1, 2), (2, 3), (4, 3), (4, 3), (2, 3))
MIXED = (10, (13, 4), (13, 4), (1, 10), (4, 13), (40, 13), (40, 13), (10, 13))
CHARGED = (10, (13, 4), (15, 4), (1, 10), (4, 13), (40, 13), (8, 3), (2, 3))
MINIMAL = (1, 1, 1, 1, 1, 1, 1, 1)
ROOF = (2, 8, 8, "memory")
# Literal rational oracles. Equal ideal Amdahl/Gustafson answers are independently
# derived for the SAME work; the helper merely writes that shared literal twice.
CASES = [
    ("empty", [[]], []),
    ("minimal serial and tie", [[case(1, 0, 1)]], [report(MINIMAL, (1, 1, 1, "tie"))]),
    ("serial only with four workers", [[case(2, 0, 4, 8, 4, 16, 4)]], [report((2, 2, 2, 1, 1, 1, 1, (1, 4)), (2, 8, 1, "memory"))]),
    ("parallel only and compute bound", [[case(0, 8, 4, 16, 4, 2, 4)]], [report((8, 2, 2, 0, 0, 4, 4, 1), (4, 2, 8, "compute"))]),
    ("mixed same-work fraction conversion", [[case(1, 9, 4, 64, 32, 16, 4)]], [report(MIXED, ROOF)]),
    ("overhead does not enter ideal alpha", [[case(1, 9, 4, 64, 32, 16, 4, (1, 2))]], [report(CHARGED, ROOF)]),
    ("large overhead can produce slowdown", [[case(1, 9, 4, 64, 32, 16, 4, 20)]], [report((10, (13, 4), (93, 4), (1, 10), (4, 13), (40, 13), (40, 93), (10, 93)), ROOF)]),
    ("one worker still pays supplied overhead", [[case(2, 3, 1, 9, 3, 3, 1, 1)]], [report((5, 5, 6, (2, 5), (2, 5), 1, (5, 6), (5, 6)), (3, 3, 3, "tie"))]),
    ("rational bandwidth and compute rate", [[case(2, 6, 2, 3, 2, (3, 2), (1, 2))]], [report((8, 5, 5, (1, 4), (2, 5), (8, 5), (8, 5), (4, 5)), ((3, 2), (3, 4), 4, "memory"))]),
    ("fractional times and overhead", [[case((1, 3), (2, 3), 2, 1, 3, (2, 3), (1, 6), (1, 6))]], [report((1, (2, 3), (5, 6), (1, 3), (1, 2), (3, 2), (6, 5), (3, 5)), ((1, 3), (1, 18), 18, "memory"))]),
    ("three-worker mixed case", [[case((1, 2), (3, 2), 3, 2, 1, 4, 2)]], [report((2, 1, 1, (1, 4), (1, 2), 2, 2, (2, 3)), (2, 4, (1, 2), "tie"))]),
    ("unreduced input pairs normalize", [[case((2, 4), (6, 4), 3, 2, 1, (8, 2), (4, 2), (0, 7))]], [report((2, 1, 1, (1, 4), (1, 2), 2, 2, (2, 3)), (2, 4, (1, 2), "tie"))]),
    ("all zero fractions use denominator one", [[case((0, 99), (4, 2), 1, 1, 1, (2, 2), (3, 3), (0, 13))]], [report((2, 2, 2, 0, 0, 1, 1, 1), (1, 1, 1, "tie"))]),
    ("maximum workers without serial work", [[case(0, 1, 64, 1, 1, 64, 64)]], [report((1, (1, 64), (1, 64), 0, 0, 64, 64, 1), (1, 64, (1, 64), "tie"))]),
    ("panels are not automatically combined", [[case(1, 0, 64, 1, 64, 1, 1, 1)]], [report((1, 1, 2, 1, 1, 1, (1, 2), (1, 128)), ((1, 64), (1, 64), 64, "memory"))]),
    ("exact tie across differently written rates", [[case(1, 1, 2, 4, 3, (4, 6), (1, 2))]], [report(BASE, ((4, 3), (2, 3), 6, "tie"))]),
    ("small rational costs and rates", [[case((1, 1000000), (1, 1000000), 2, 1, 1, (1, 1000000), (1, 1000000))]], [report(((1, 500000), (3, 2000000), (3, 2000000), (1, 2), (2, 3), (4, 3), (4, 3), (2, 3)), (1, (1, 1000000), 1000000, "tie"))]),
    ("derived values exceed input numeric bounds", [[case(1, 1, 2, 1, 1000000, 1, (1, 1000000))]], [report(BASE, ((1, 1000000), (1, 1000000000000), 1000000000000, "memory"))]),
    ("maximum input numerators and denominators", [[case(1000000, (0, 1000000), 64, 1000000, 1000000, (1000000, 1000000), 1000000, 1000000)]], [report((1000000, 1000000, 2000000, 1, 1, 1, (1, 2), (1, 128)), (1, 1, 1000000, "compute"))]),
    ("positive overhead with zero serial fraction", [[case(0, 8, 4, 16, 4, 2, 4, 2)]], [report((8, 2, 4, 0, 0, 4, 2, (1, 2)), (4, 2, 8, "compute"))]),
    ("same ceiling different limiting resource", [[case(1, 1, 2, 64, 16, 8, 4), case(1, 1, 2, 64, 16, 32, 2)]], [report(BASE, (4, 8, 8, "compute")), report(BASE, (4, 8, 8, "memory"))]),
    ("low intensity can remain compute limited", [[case(1, 1, 2, 1, 4, (1, 16), (1, 2))]], [report(BASE, ((1, 4), (1, 16), 16, "compute"))]),
    ("mixed batch preserves order and local state", [[case(1, 9, 4, 64, 32, 16, 4, (1, 2)), case(0, 8, 4, 16, 4, 2, 4), case(1, 0, 1)]], [report(CHARGED, ROOF), report((8, 2, 2, 0, 0, 4, 4, 1), (4, 2, 8, "compute")), report(MINIMAL, (1, 1, 1, "tie"))]),
    ("equal reports need independent containers", [[case(1, 9, 4, 64, 32, 16, 4), case(1, 9, 4, 64, 32, 16, 4)]], [report(MIXED, ROOF), report(MIXED, ROOF)]),
]
# Closed-form maximum batch: twelve independent repetitions of the unit case.
CASES.append(("twelve reports", [[case(1, 0, 1) for _ in range(12)]],
              [report(MINIMAL, (1, 1, 1, "tie")) for _ in range(12)]))
CASES.extend([CASES[0], CASES[5], CASES[0]])

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
    result=m.resource_reports(*supplied)
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
