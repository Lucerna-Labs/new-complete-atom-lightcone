def heartbeat_trace(events):
    pending = None
    suspected = False
    out = []
    for event in events:
        now = event["at"]
        if pending is not None and now >= pending["deadline"]:
            suspected = True
            pending = None
        accepted = None
        if event["kind"] == "start":
            pending = {"connection":event["connection"], "probe":event["probe"],
                       "deadline":now + event["timeout"]}
        elif event["kind"] == "pong":
            accepted = False
            if (pending is not None and event["connection"] == pending["connection"]
                    and event["probe"] == pending["probe"]):
                suspected = False
                pending = None
                accepted = True
        elif event["kind"] != "tick":
            raise ValueError("unknown event")
        out.append({"suspected":suspected,
                    "pending":dict(pending) if pending is not None else None,
                    "pong_accepted":accepted})
    return out
