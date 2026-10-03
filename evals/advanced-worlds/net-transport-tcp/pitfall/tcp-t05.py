def cubic_trace(events, C=0.4):
    t = 0.0
    out = []
    for e in events:
        if e["type"] == "advance":
            t += e["seconds"]
            out.append({"time": t, "application_limited": e["application_limited"]})
        elif e["type"] == "ack":
            k = ((e["wmax"] - e["cwnd_epoch"]) / C) ** (1 / 3)
            raw = C * (t - k) ** 3 + e["wmax"]
            out.append({"time": t, "k": k, "current_cubic": raw, "raw_cubic": raw,
                        "cubic_target": raw, "target": raw, "branch": "cubic"})
        elif e["type"] in ("packet_loss", "rto"):
            threshold = max(0.5 * e["flight_size"], 2)
            out.append({"event": e["type"], "ssthresh": threshold,
                        "cwnd": threshold})
    return out
