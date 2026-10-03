# Plausible semantic pitfall: Wrongly charges each received payload length instead of its highest end offset.
def _merge(ranges):
    out = []
    for left, right in sorted((int(a), int(b)) for a, b in ranges if b > a):
        if out and left <= out[-1][1]:
            out[-1][1] = max(out[-1][1], right)
        else:
            out.append([left, right])
    return out

def _advance(ranges, point):
    while True:
        hit = next((r for r in ranges if r[0] <= point < r[1]), None)
        if hit is None:
            return point
        point = hit[1]

def stream_credit_trace(events, max_data, stream_limits):
    received, state = {}, {}
    connection_used = 0
    out = []
    for event in events:
        kind, sid = event["type"], int(event.get("stream", -1))
        old_used = connection_used
        old_state = {k: dict(v) for k, v in state.items()}
        old_received = {k: [list(r) for r in v] for k, v in received.items()}
        accepted, error = True, None
        if sid not in stream_limits:
            accepted, error = False, "stream-closed"
        elif sid not in state:
            state[sid] = {"highest": 0, "delivered": 0, "final_size": None, "final_kind": None}
            received[sid] = []
        s = state.get(sid)
        if accepted and kind == "data":
            start, end = int(event["start"]), int(event["end"])
            if end < start:
                accepted, error = False, "final-size"
            elif s["final_size"] is not None and end > s["final_size"]:
                accepted, error = False, "final-size"
            elif s["final_kind"] == "reset":
                pass
            else:
                new_high = s["highest"] + (end - start)
                if new_high > stream_limits[sid] or connection_used + new_high - s["highest"] > max_data:
                    accepted, error = False, "flow-control"
                else:
                    s["highest"] = new_high
                    received[sid] = _merge(received[sid] + [[start, end]])
                    s["delivered"] = _advance(received[sid], s["delivered"])
        elif accepted and kind in ("fin", "reset"):
            final = int(event["final_size"])
            if s["final_size"] is not None:
                if s["final_size"] != final:
                    accepted, error = False, "final-size"
                elif kind == "reset":
                    # A consistent reset may overtake or follow a FIN.
                    s["final_kind"] = "reset"
                # A later consistent FIN cannot undo an accepted reset.
            elif final < s["highest"]:
                accepted, error = False, "final-size"
            elif final > stream_limits[sid] or connection_used + final - s["highest"] > max_data:
                accepted, error = False, "flow-control"
            else:
                s["highest"] = final
                s["final_size"], s["final_kind"] = final, kind
                if kind == "fin":
                    s["delivered"] = _advance(received[sid], s["delivered"])
        else:
            accepted, error = False, "stream-closed"
        if accepted:
            connection_used += state[sid]["highest"] - old_state.get(sid, {"highest": 0})["highest"]
        else:
            connection_used, state, received = old_used, old_state, old_received
        streams = {str(k): {"highest": v["highest"], "delivered": v["delivered"],
                            "final_size": v["final_size"], "final_kind": v["final_kind"]}
                   for k, v in sorted(state.items())}
        out.append({"accepted": accepted, "error": error, "connection_used": connection_used,
                    "streams": streams})
    return out
