def abba_measurements(base_a, base_b, drift, trials, resolution=1):
    records = []
    for i, (variant, trial) in enumerate(zip("ABBA", trials)):
        base = base_a if variant == "A" else base_b
        elapsed = trial["operations"] * (base + drift * i)
        start = trial["start"]
        end = start + elapsed
        measured = resolution * (end // resolution - start // resolution)
        records.append({"variant": variant, "position": i,
                        "elapsed": elapsed, "measured": measured,
                        "error": measured - elapsed,
                        "per_op": measured / trial["operations"]})
    mean_a = (records[0]["per_op"] + records[3]["per_op"]) / 2
    mean_b = (records[1]["per_op"] + records[2]["per_op"]) / 2
    same_position_ratio = (base_a + 1.5 * drift) / (base_b + 1.5 * drift)
    return {"trials": records, "mean_a": mean_a, "mean_b": mean_b,
            "measured_ratio": mean_a / mean_b if mean_b > 0 else None,
            "same_position_ratio": same_position_ratio,
            "time_zero_ratio": base_a / base_b}
