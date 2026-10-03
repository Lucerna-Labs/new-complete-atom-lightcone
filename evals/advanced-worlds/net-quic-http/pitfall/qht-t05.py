# Plausible semantic pitfall: Wrongly erases inherited early-data exposure after this hop finishes its own handshake.
def early_data_trace(events):
    inherited = False
    latest_rejected = False
    out = []
    for event in events:
        kind = event["type"]
        if kind == "request":
            inherited = bool(event["early_data"])
            latest_rejected = inherited and not bool(event["resource_replayable"])
            if not inherited:
                decision = "forward-1rtt"
            elif latest_rejected:
                decision = "425"
            else:
                decision = "forward-early"
            out.append({"kind": "http-response" if decision == "425" else "request",
                        "early": inherited, "decision": decision})
        elif kind == "intermediary":
            if event["own_handshake_confirmed"]:
                inherited = False
            latest_rejected = inherited and not bool(event["resource_replayable"])
            decision = "425" if latest_rejected else ("forward-early" if inherited else "forward-1rtt")
            out.append({"kind": "http-response" if decision == "425" else "request",
                        "early": inherited, "decision": decision})
        elif kind == "http_425_retry":
            inherited = False
            latest_rejected = False
            out.append({"kind": "request", "early": False, "decision": "forward-1rtt"})
        elif kind == "quic_retry":
            out.append({"kind": "quic-retry", "early": inherited, "decision": "transport-retry"})
        else:
            raise ValueError("event")
    return out
