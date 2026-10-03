def lease_state(request_sent, ack_received, lease_duration, now, t1=None, t2=None):
    epoch = request_sent
    t1_at = epoch + (lease_duration * 0.5 if t1 is None else t1)
    t2_at = epoch + (lease_duration * 0.875 if t2 is None else t2)
    expires_at = epoch + lease_duration
    if now >= expires_at:
        phase = "INIT"
    elif now >= t2_at:
        phase = "REBINDING"
    elif now >= t1_at:
        phase = "RENEWING"
    else:
        phase = "BOUND"
    return {"t1_at": t1_at, "t2_at": t2_at, "expires_at": expires_at,
            "phase": phase, "usable": phase != "INIT"}
