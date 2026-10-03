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
    # Plausible error: treating the highest received/SACKed byte as cumulative.
    received, retained = [], []
    ack = 0
    out = []
    for e in events:
        if e["type"] == "send":
            retained = _merge(retained + [[e["start"], e["end"]]])
        elif e["type"] == "receive":
            received = _merge(received + [[e["start"], e["end"]]])
            ack = max(ack, max(r[1] for r in received))
            retained = _subtract(retained, 0, ack)
        elif e["type"] == "ack":
            retained = _subtract(retained, 0, e["cumulative"])
        elif e["type"] == "renege":
            received = _subtract(received, e["start"], e["end"])
        sack = [[max(left, ack), right] for left, right in received if right > ack]
        out.append({"cumulative_ack": ack, "delivered": ack,
                    "sack_blocks": sack, "retained": retained})
    return out
