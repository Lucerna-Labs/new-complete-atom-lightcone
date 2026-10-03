def nagle_trace(events, mss=1000, nagle_enabled=True):
    pending = 0
    outstanding = 0
    enabled = bool(nagle_enabled)
    out = []
    for event in events:
        tx = []
        kind = event["type"]
        if kind == "write":
            pending += int(event["bytes"])
        elif kind == "ack":
            outstanding = max(0, outstanding - int(event["bytes"]))
        elif kind == "disable":
            enabled = False
        elif kind == "push":
            pass
        else:
            raise ValueError("unknown event")
        while pending >= mss:
            pending -= mss
            outstanding += mss
            tx.append(mss)
        if pending and (not enabled or outstanding == 0):
            tx.append(pending)
            outstanding += pending
            pending = 0
        out.append({"tx": tx, "pending": pending, "outstanding": outstanding,
                    "acks_sent": 0})
    return out
