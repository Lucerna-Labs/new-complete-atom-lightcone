def path_budget_trace(events, factor=3):
    received, sent, validated, challenges = {}, {}, set(), {}
    out = []
    for event in events:
        kind = event["type"]
        accepted, error = True, None
        if kind == "receive":
            path = event["path"]
            received[path] = received.get(path, 0) + int(event["bytes"])
        elif kind == "send":
            path, amount = event["path"], int(event["bytes"])
            new_sent = sent.get(path, 0) + amount
            if path not in validated and new_sent > factor * received.get(path, 0):
                accepted, error = False, "amplification"
            else:
                sent[path] = new_sent
        elif kind == "challenge":
            challenges.setdefault(event["path"], []).append(event["token"])
        elif kind == "response":
            path = event["challenged"]
            tokens = challenges.get(path, [])
            if event["token"] in tokens:
                validated.add(path)
                tokens.remove(event["token"])
        elif kind in ("cid", "ack"):
            pass
        else:
            accepted, error = False, "event"
        out.append({"accepted": accepted, "error": error, "received": dict(sorted(received.items())),
                    "sent": dict(sorted(sent.items())), "validated": sorted(validated)})
    return out
