"""CPython 3.14.7 queue accounting; join is a fresh point query, not a waiter."""


def queue_accounting(capacity, events):
    queue = []
    unfinished = 0
    shutdown = False
    result = []
    for event in events:
        op = event["op"]
        value = None
        if op == "put":
            if shutdown:
                status = "shutdown"
            elif capacity > 0 and len(queue) >= capacity:
                status = "full"
            else:
                queue.append(event["item"])
                unfinished += 1
                status = "accepted"
        elif op == "get":
            if queue:
                value = queue.pop(0)
                status = "item"
            else:
                status = "shutdown" if shutdown else "empty"
        elif op == "task_done":
            if unfinished:
                unfinished -= 1
                status = "acknowledged"
            else:
                status = "underflow"
        elif op == "join":
            status = "ready" if unfinished == 0 else "waiting"
        elif op == "shutdown":
            shutdown = True
            if event["immediate"]:
                unfinished = 0
                queue.clear()
            status = "closed"
        result.append({"op": op, "status": status, "value": value,
                       "queue": list(queue), "unfinished": unfinished,
                       "shutdown": shutdown})
    return result
