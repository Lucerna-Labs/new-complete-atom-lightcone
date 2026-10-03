"""Pitfall: entry incorrectly accepts equality at the A3 threshold."""


def a3_trace(samples, config):
    entered, pending = False, None
    reports, snapshots = [], []
    enabled = config["as_security_active"] and config["cell_applicable"]
    offset = config["offset_db"]
    hysteresis = config["hysteresis_db"]
    ttt = config["ttt_ms"]

    def finish():
        nonlocal entered, pending
        kind, deadline = pending["kind"], pending["deadline_ms"]
        entered = kind == "enter"
        if entered or config["report_on_leave"]:
            reports.append({"time_ms": deadline, "reason": kind})
        pending = None

    for sample in samples:
        now, margin = sample["time_ms"], sample["margin_db"]
        if enabled:
            # Before this sample, the previous input is held constant.
            if pending is not None and pending["deadline_ms"] < now:
                finish()
            kind = "leave" if entered else "enter"
            qualifies = (margin < offset - hysteresis if entered
                         else margin >= offset + hysteresis)
            if not qualifies:
                pending = None
            elif pending is None:
                pending = {"kind": kind, "since_ms": now,
                           "deadline_ms": now + ttt}
            # At equal timestamps, the new observation has already been applied.
            if pending is not None and pending["deadline_ms"] <= now:
                finish()
        snapshots.append({"entered": entered,
                          "pending": dict(pending) if pending is not None else None,
                          "reports": [dict(report) for report in reports]})
    return snapshots
