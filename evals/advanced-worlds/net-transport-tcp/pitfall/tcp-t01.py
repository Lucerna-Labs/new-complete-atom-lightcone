def rto_trace(events, clock_granularity=0.1):
    srtt = None
    rttvar = None
    rto = 1.0
    used = 0
    out = []
    for event in events:
        kind = event["type"]
        if kind == "sample":
            sample = float(event["rtt"])
            if srtt is None:
                srtt, rttvar = sample, sample / 2
            else:
                srtt = 0.875 * srtt + 0.125 * sample
                rttvar = 0.75 * rttvar + 0.25 * abs(srtt - sample)
            rto = max(1.0, min(60.0, srtt + max(clock_granularity, 4 * rttvar)))
            used += 1
        elif kind == "timeout":
            rto = min(60.0, 2 * rto)
        out.append({"srtt": srtt, "rttvar": rttvar, "rto": rto, "samples_used": used})
    return out
