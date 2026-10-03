import math

def cubic_trace(events, C=0.4):
    t = 0.0
    out = []
    for event in events:
        kind = event["type"]
        if kind == "advance":
            if not event["application_limited"]:
                t += float(event["seconds"])
            out.append({"time": t, "application_limited": bool(event["application_limited"])})
        elif kind == "ack":
            wmax = float(event["wmax"])
            epoch = float(event["cwnd_epoch"])
            cwnd = float(event["cwnd"])
            k = ((wmax - epoch) / C) ** (1.0 / 3.0) if wmax > epoch else 0.0
            current = C * (t - k) ** 3 + wmax
            raw = C * (t + float(event["rtt"]) - k) ** 3 + wmax
            cubic_target = max(cwnd, min(1.5 * cwnd, raw))
            if float(event["reno_estimate"]) > current:
                target, branch = float(event["reno_estimate"]), "reno-friendly"
            else:
                target, branch = cubic_target, "cubic"
            out.append({"time": t, "k": k, "current_cubic": current, "raw_cubic": raw,
                        "cubic_target": cubic_target, "target": target,
                        "branch": branch})
        elif kind in ("packet_loss", "rto"):
            threshold = max(0.7 * float(event["flight_size"]), 2.0)
            cwnd = threshold if kind == "packet_loss" else 1.0
            out.append({"event": kind, "ssthresh": threshold, "cwnd": cwnd})
        else:
            raise ValueError("unknown event")
    return out
