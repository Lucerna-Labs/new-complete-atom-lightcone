"""Naive Repeatable Read model captures its snapshot at BEGIN."""
def snapshot_views(initial, events):
    epoch = 0
    versions = {key: [(0, value)] for key, value in initial.items()}
    active = {}
    observations = []

    def capture(tx):
        if tx["isolation"] == "rr":
            if tx["snapshot"] is None:
                tx["snapshot"] = epoch
            return tx["snapshot"]
        return epoch

    def visible(tx, at):
        view = {}
        for key, history in versions.items():
            value = None
            for revision, candidate in history:
                if revision <= at:
                    value = candidate
                else:
                    break
            if value is not None:
                view[key] = value
        for key, value in tx["private"].items():
            if value is None:
                view.pop(key, None)
            else:
                view[key] = value
        return view

    def publish(changes):
        nonlocal epoch
        epoch += 1
        for key, value in changes.items():
            versions.setdefault(key, []).append((epoch, value))

    for event in events:
        op = event["op"]
        if op == "begin":
            active[event["tx"]] = {"isolation": event["isolation"],
                                   "snapshot": epoch if event["isolation"] == "rr" else None, "private": {}}
        elif op == "external_commit":
            publish(event["changes"])
        elif op == "commit":
            publish(active[event["tx"]]["private"])
            del active[event["tx"]]
        elif op == "abort":
            del active[event["tx"]]
        else:
            tx = active[event["tx"]]
            at = capture(tx)
            if op == "write":
                tx["private"][event["key"]] = event["value"]
            elif op == "read":
                view = visible(tx, at)
                observations.append({"op": "read", "tx": event["tx"],
                                     "epoch": at, "key": event["key"],
                                     "value": view.get(event["key"])})
            elif op == "scan":
                view = visible(tx, at)
                observations.append({"op": "scan", "tx": event["tx"],
                                     "epoch": at,
                                     "rows": [{"key": key, "value": view[key]}
                                              for key in sorted(view)
                                              if view[key] >= event["minimum"]]})
    latest = {}
    for key, history in versions.items():
        value = history[-1][1]
        if value is not None:
            latest[key] = value
    return {"epoch": epoch, "committed": latest, "observations": observations}
