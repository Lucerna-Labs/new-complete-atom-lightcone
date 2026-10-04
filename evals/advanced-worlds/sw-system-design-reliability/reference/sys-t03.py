"""Declared serial breaker model; no remote calls or real timing."""


def breaker_events(cooldown, events):
    if type(cooldown) is not int or not 1 <= cooldown <= 1000:
        raise ValueError("cooldown")
    if type(events) is not list or len(events) > 128:
        raise ValueError("events")

    mode = "Closed"
    generation = 0
    open_until = None
    active = {}
    seen = set()
    previous_time = -1
    snapshots = []
    schemas = {
        "observe": {"op", "time"},
        "trip": {"op", "time"},
        "call": {"op", "time", "id"},
        "result": {"op", "time", "id", "outcome"},
    }

    for event in events:
        if type(event) is not dict:
            raise ValueError("event")
        op = event.get("op")
        if type(op) is not str or op not in schemas or set(event) != schemas[op]:
            raise ValueError("schema")
        now = event["time"]
        if type(now) is not int or not 0 <= now <= 1000000 or now < previous_time:
            raise ValueError("time")
        previous_time = now
        if op in ("call", "result"):
            call_id = event["id"]
            if type(call_id) is not str or not 1 <= len(call_id) <= 32:
                raise ValueError("id")
            if any(not ("a" <= c <= "z" or "A" <= c <= "Z" or "0" <= c <= "9" or c in "-_") for c in call_id):
                raise ValueError("id")
        if op == "result" and (type(event["outcome"]) is not str or event["outcome"] not in ("success", "failure")):
            raise ValueError("outcome")

        # Expiration is a controller event BEFORE the requested event, even trip/result.
        if mode == "Open" and now >= open_until:
            mode = "HalfOpen"
            generation += 1
            open_until = None

        admitted = None
        if op == "trip":
            generation += 1
            mode = "Open"
            open_until = now + cooldown
        elif op == "call":
            if call_id in seen:
                raise ValueError("reused id")
            seen.add(call_id)
            admitted = mode == "Closed" or (
                mode == "HalfOpen" and not any(
                    record["trial"] and record["generation"] == generation
                    for record in active.values()
                )
            )
            if admitted:
                active[call_id] = {"generation": generation, "trial": mode == "HalfOpen"}
        elif op == "result":
            if call_id not in active:
                raise ValueError("inactive id")
            record = active.pop(call_id)
            if record["trial"] and record["generation"] == generation and mode == "HalfOpen":
                generation += 1
                if event["outcome"] == "success":
                    mode = "Closed"
                    open_until = None
                else:
                    mode = "Open"
                    open_until = now + cooldown

        snapshots.append({
            "mode": mode,
            "generation": generation,
            "open_until": open_until,
            "result": admitted,
            "active": {key: {"generation": record["generation"], "trial": record["trial"]}
                       for key, record in active.items()},
        })
    return snapshots
