def _merge(ranges):
    out = []
    for start, end in sorted((int(a), int(b)) for a, b in ranges if b > a):
        if out and start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out

def _subtract(ranges, start, end):
    out = []
    for left, right in ranges:
        if right <= start or left >= end:
            out.append([left, right])
        else:
            if left < start:
                out.append([left, start])
            if right > end:
                out.append([end, right])
    return _merge(out)

def reassembly_trace(events):
    received = []
    retained = []
    cumulative = 0
    delivered = 0
    out = []
    for event in events:
        kind = event["type"]
        if kind == "send":
            retained = _merge(retained + [[event["start"], event["end"]]])
        elif kind == "receive":
            received = _merge(received + [[event["start"], event["end"]]])
            while True:
                covering = next((r for r in received if r[0] <= cumulative < r[1]), None)
                if covering is None:
                    break
                cumulative = covering[1]
                received = _subtract(received, 0, cumulative)
                delivered = cumulative
        elif kind == "ack":
            ack = int(event["cumulative"])
            new_retained = []
            for left, right in retained:
                if right > ack:
                    new_retained.append([max(left, ack), right])
            retained = _merge(new_retained)
        elif kind == "renege":
            received = _subtract(received, max(cumulative, event["start"]), event["end"])
        else:
            raise ValueError("unknown event")
        sack = []
        for left, right in _merge(received):
            if right > cumulative:
                sack.append([max(left, cumulative), right])
        out.append({"cumulative_ack": cumulative, "delivered": delivered,
                    "sack_blocks": sack, "retained": _merge(retained)})
    return out
