"""Declared finite hysteretic queue model; no production queue is contacted."""


def queue_epochs(capacity, healthy, degraded, enter, exit, arrivals):
    limits = (capacity, healthy, degraded, enter, exit)
    if any(type(value) is not int for value in limits):
        raise ValueError("queue parameters must be native integers")
    if not (2 <= capacity <= 100 and 1 <= healthy < capacity
            and 0 <= degraded < healthy
            and 0 <= exit < enter <= capacity - healthy):
        raise ValueError("invalid queue parameters")
    if type(arrivals) is not list or len(arrivals) > 128:
        raise ValueError("arrivals must be a bounded native list")
    if any(type(value) is not int or not 0 <= value <= 1000
           for value in arrivals):
        raise ValueError("invalid offered arrival count")

    queue = 0
    mode = "Healthy"
    result = []
    for offered in arrivals:
        admitted = min(offered, capacity - queue)
        rejected = offered - admitted
        service = healthy if mode == "Healthy" or offered < healthy else degraded  # Mistake: low offered load bypasses hysteresis.
        completed = min(queue + admitted, service)
        queue += admitted - completed
        if mode == "Healthy" and queue >= enter:
            mode = "Degraded"
        elif mode == "Degraded" and queue <= exit:
            mode = "Healthy"
        result.append({"queue": queue, "mode": mode, "admitted": admitted,
                       "rejected": rejected, "completed": completed})
    return result
