"""RFC 8289 persistence eligibility and mathematical scheduling components.

Sample clocks are nonwrapping integer milliseconds; backlog is the number of
bytes remaining after dequeue. None as the enqueue timestamp denotes an empty
dequeue. This models helper state, not packet dropping or the full controller.
The bounded contract limits clocks to 2**48-1 and control-law count to 2**32-1;
law base is at most 10**9 and target/interval are at most 10**6 milliseconds.
"""

import math


def codel_eligibility(samples, maxpacket=1500, target=5, interval=100):
    first_above_time = 0
    result = []
    for sample in samples:
        eligible = False
        now, enqueued = sample["now"], sample["enqueued"]
        if (enqueued is None or now - enqueued < target
                or sample["backlog"] <= maxpacket):
            first_above_time = 0
        elif first_above_time == 0:
            first_above_time = now + interval
        else:
            eligible = now >= first_above_time
        result.append({"first_above_time": first_above_time, "eligible": eligible})
    return result


def control_law(base, count, interval=100):
    """Return an unquantized deadline from the explicitly supplied schedule base."""
    return base + interval / math.sqrt(count)
