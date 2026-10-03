def dcf_backoff(initial_counter, difs_us, slot_us, events):
    """Pitfall: busy sensing resets the draw instead of retaining its residual."""
    now = 0
    counter = initial_counter
    joint_busy = False
    idle_start = 0
    accounted_slots = 0
    states = []
    for event in events:
        if event["kind"] == "sense":
            next_busy = event["physical_busy"] or event["virtual_busy"]
            if next_busy:
                counter = initial_counter
                idle_start = None
                accounted_slots = 0
            elif joint_busy:
                idle_start = now
                accounted_slots = 0
            joint_busy = next_busy
        else:
            now += event["us"]
            if not joint_busy:
                complete = max(0, now - idle_start - difs_us) // slot_us
                counter = max(0, counter - (complete - accounted_slots))
                accounted_slots = complete
        idle_us = 0 if joint_busy else now - idle_start
        states.append({"at_us": now, "counter": counter,
                       "joint_busy": joint_busy, "idle_us": idle_us,
                       "eligible": not joint_busy and idle_us >= difs_us and counter == 0})
    return states


def cw_after(outcome, cw, cw_min, cw_max):
    if outcome == "success":
        return cw_min
    return min(2 * (cw + 1) - 1, cw_max)
