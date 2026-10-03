def nagle_trace(events, mss=1000, nagle_enabled=True):
    # Plausible mistakes: block even full segments behind outstanding data,
    # but incorrectly let a PSH request bypass that hold.
    pending = outstanding = 0
    enabled = bool(nagle_enabled)
    out = []
    for event in events:
        kind = event["type"]
        if kind == "write":
            pending += event["bytes"]
        elif kind == "ack":
            outstanding = max(0, outstanding - event["bytes"])
        elif kind == "disable":
            enabled = False
        tx = []
        if pending and (not enabled or outstanding == 0 or kind == "push"):
            while pending:
                size = min(mss, pending)
                pending -= size
                outstanding += size
                tx.append(size)
        out.append({"tx": tx, "pending": pending, "outstanding": outstanding,
                    "acks_sent": 0})
    return out
