def rto_trace(events, clock_granularity=0.1):
    srtt = None
    rttvar = None
    rto = 1.0
    used = 0
    out = []
    for event in events:
        kind = event["type"]
        if kind == "sample" and not event.get("ambiguous", False):
            sample = float(event["rtt"])
            if srtt is None:
                srtt, rttvar = sample, sample / 2.0
            else:
                old_srtt = srtt
                rttvar = 0.75 * rttvar + 0.25 * abs(old_srtt - sample)
                srtt = 0.875 * old_srtt + 0.125 * sample
            rto = max(1.0, min(60.0, srtt + max(float(clock_granularity), 4.0 * rttvar)))
            used += 1
        elif kind == "timeout":
            rto = min(60.0, 2.0 * rto)
        elif kind in ("sample", "duplicate_ack", "advance_ack"):
            pass
        else:
            raise ValueError("unknown event")
        out.append({"srtt": srtt, "rttvar": rttvar, "rto": rto, "samples_used": used})
    return out
