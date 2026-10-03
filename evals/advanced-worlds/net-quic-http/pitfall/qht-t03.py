# Plausible semantic pitfall: Wrongly treats probe timeout as proof that outstanding in-flight packets were lost.
def analyze_trace(events, granularity=0.001, srtt=0.1, latest_rtt=0.12):
    sent = {"initial": {}, "handshake": {}, "application": {}}
    acked = {"initial": set(), "handshake": set(), "application": set()}
    lost = {"initial": set(), "handshake": set(), "application": set()}
    probes = 0
    threshold = max(float(granularity), 9.0 / 8.0 * max(float(latest_rtt), float(srtt)))
    out = []
    for event in events:
        kind, space = event["type"], event.get("space")
        if kind == "sent":
            sent[space][int(event["pn"])] = (float(event["time"]), bool(event["in_flight"]))
        elif kind == "ack":
            numbers = {n for low, high in event["ranges"] for n in range(int(low), int(high) + 1)}
            acked[space].update(n for n in numbers if n in sent[space])
            later = sorted(acked[space])
            for pn, (sent_time, in_flight) in sent[space].items():
                if not in_flight or pn in acked[space] or pn in lost[space]:
                    continue
                later_acked = any(a > pn for a in later)
                if later_acked and (max(later) >= pn + 3 or float(event["time"]) - sent_time >= threshold):
                    lost[space].add(pn)
        elif kind == "pto":
            probes += 1
            lost[space].update(pn for pn, (_, inflight) in sent[space].items() if inflight and pn not in acked[space])
        else:
            raise ValueError("event")
        out.append({"acked": {s: sorted(acked[s]) for s in sent}, "lost": {s: sorted(lost[s]) for s in sent}, "probes": probes})
    return out
