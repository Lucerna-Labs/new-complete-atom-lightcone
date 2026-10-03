def simulate_invocations(initial_counter, commands):
    """Pitfall: duplicate lookup is frozen at begin rather than atomic commit."""
    counter = initial_counter
    records, pending, events = {}, {}, []
    for command in commands:
        op = command["op"]
        if op == "begin":
            key = (command["client"], command["incarnation"], command["request"])
            pending[command["attempt"]] = {"key": key, "delta": command["delta"],
                                           "prior": records.get(key)}
            events.append({"op": op, "attempt": command["attempt"],
                           "status": "pending"})
        elif op == "commit":
            attempt = command["attempt"]
            invocation = pending.pop(attempt, None)
            reply = None
            if invocation is None:
                status = "missing"
            else:
                key, delta = invocation["key"], invocation["delta"]
                prior = invocation["prior"]
                if prior is not None:
                    if prior["delta"] != delta:
                        status = "conflict"
                    else:
                        status = "replayed"
                        if command["reply"]:
                            reply = prior["result"]
                else:
                    counter += delta
                    records[key] = {"delta": delta, "result": counter}
                    status = "committed"
                    if command["reply"]:
                        reply = counter
            events.append({"op": op, "attempt": attempt,
                           "status": status, "reply": reply})
        elif op == "crash":
            events.append({"op": op, "discarded": sorted(pending)})
            pending.clear()
        else:
            key = (command["client"], command["incarnation"], command["request"])
            removed = key in records
            records.pop(key, None)
            events.append({"op": op, "key": list(key), "removed": removed})
    return {
        "counter": counter,
        "records": [{"key": list(key), **records[key]} for key in sorted(records)],
        "pending": [{"attempt": attempt, "key": list(pending[attempt]["key"]),
                     "delta": pending[attempt]["delta"]} for attempt in sorted(pending)],
        "events": events,
    }
