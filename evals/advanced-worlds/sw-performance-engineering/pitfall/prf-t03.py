"""Independent exact-rational scaling and DRAM Roofline model panels."""

from fractions import Fraction


def resource_reports(cases):
    def encode(value):
        return [value.numerator, value.denominator]

    reports = []
    for case in cases:
        serial = Fraction(*case["serial"])
        parallel = Fraction(*case["parallel"])
        overhead = Fraction(*case.get("overhead", [0, 1]))
        workers = case["workers"]
        baseline = serial + parallel
        core = serial + parallel / workers
        total = core + overhead
        baseline_fraction = serial / baseline
        parallel_fraction = serial / core
        ideal_speedup = baseline / core
        scaled_speedup = workers - (workers - 1) * baseline_fraction
        charged_speedup = baseline / total
        work = Fraction(case["flops"])
        traffic = Fraction(case["dram_bytes"])
        peak = Fraction(*case["compute_peak"])
        bandwidth = Fraction(*case["bandwidth"])
        intensity = work / traffic
        memory_roof = bandwidth * intensity
        roof = min(peak, memory_roof)
        bound = max(work / peak, traffic / bandwidth)
        limiting = "compute" if peak < memory_roof else "memory" if peak > memory_roof else "tie"
        reports.append({
            "parallel": {
                "baseline_time": encode(baseline),
                "ideal_parallel_time": encode(core),
                "parallel_time_with_overhead": encode(total),
                "baseline_serial_fraction": encode(baseline_fraction),
                "ideal_parallel_serial_fraction": encode(parallel_fraction),
                "amdahl_speedup": encode(ideal_speedup),
                "gustafson_speedup": encode(scaled_speedup),
                "speedup_with_overhead": encode(charged_speedup),
                "efficiency_with_overhead": encode(charged_speedup / workers),
            },
            "roofline": {
                "operational_intensity": encode(intensity),
                "performance_ceiling": encode(roof),
                "time_lower_bound": encode(bound),
                "limiting_resource": limiting,
            },
        })
    return reports
