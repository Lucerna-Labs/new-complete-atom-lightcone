def predictor_trace(entry_count, events, initial_state=1):
    states = [initial_state] * entry_count
    trace = []
    total = 0
    for event in events:
        pc, taken = event["pc"], event["taken"]
        index = (pc // 4) % entry_count
        before = states[index]
        prediction = before >= 2
        after = min(3, before + 1) if taken else max(0, before - 1)
        mismatch = prediction != taken
        states[index] = after
        total += int(mismatch)
        trace.append({"pc": pc, "index": index, "taken": taken,
                      "prediction": prediction, "before": before,
                      "after": after, "misprediction": mismatch})
    return {"states": states, "mispredictions": total, "trace": trace}
