"""Serial abstract ownership ledger, not Tokio's internal wakeup scheduler."""


def channel_ownership(capacity, owners, initial_queue, events):
    owned = {owner: set(values) for owner, values in owners.items()}
    queue = list(initial_queue)
    operations = {}
    dropped = set()
    received = []
    trace = []
    for event in events:
        op = event["op"]
        if op == "send":
            owner, value = event["owner"], event["value"]
            owned[owner].remove(value)
            operations[event["id"]] = {"kind": "send", "owner": owner, "value": value}
        elif op == "reserve":
            operations[event["id"]] = {"kind": "reserve", "owner": event["owner"], "value": None}
        elif op == "send_ready":
            operation = operations.pop(event["id"])
            queue.append(operation["value"])
        elif op == "reserve_ready":
            operations[event["id"]]["kind"] = "permit"
        elif op == "cancel":
            operation = operations.pop(event["id"])
            if operation["kind"] == "send":
                dropped.add(operation["value"])
        elif op == "permit_send":
            operation = operations.pop(event["id"])
            value = event["value"]
            owned[operation["owner"]].remove(value)
            queue.append(value)
        elif op == "permit_drop":
            operations.pop(event["id"])
        elif op == "receive":
            received.append(queue.pop(0))
        elif op == "owner_drop":
            owner = event["owner"]
            dropped.update(owned.pop(owner))
            for oid in list(operations):
                if operations[oid]["owner"] == owner:
                    operation = operations.pop(oid)
                    if operation["kind"] == "send":
                        dropped.add(operation["value"])
        trace.append({
            "op": op, "queue": list(queue),
            "owners": {owner: sorted(values) for owner, values in sorted(owned.items())},
            "operations": {oid: dict(value) for oid, value in sorted(operations.items())},
            "dropped": sorted(dropped), "received": list(received),
            "free": capacity - len(queue) - sum(x["kind"] == "permit" for x in operations.values()),
        })
    return trace
