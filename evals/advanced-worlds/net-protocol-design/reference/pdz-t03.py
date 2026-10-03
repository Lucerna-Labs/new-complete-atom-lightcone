"""Nominal RFC 7252 CON-request timing and response-correlation component.

Times are integer milliseconds. The chosen initial wait r_ms is 2000..3000;
events stop before the default 247000 ms EXCHANGE_LIFETIME. Initial send is at
zero, with at most four retransmissions. All messages are predecoded and valid
apart from the correlation being tested. No application-response timer, wire
parser, security validator, or acknowledgments of separate responses are modeled.
Message give-up is historical transmission failure, not proof of nonexecution;
the request retains correlation state for a possible later final response.
The last event snapshot at a timestamp includes any equal-time timeout; earlier
same-time snapshots precede it. Bad correlation has no direct message effect,
but advancing time can still produce retransmissions or transmission failure.
"""


def coap_exchange(peer, mid, token, r_ms, events):
    transmissions, timer = [0], r_ms
    message_failed = complete = False

    def advance(now, inclusive):
        nonlocal timer, message_failed
        while timer is not None and (timer < now or (inclusive and timer == now)):
            if len(transmissions) == 5:
                message_failed, timer = True, None
            else:
                transmissions.append(timer)
                timer += r_ms * (2 ** (len(transmissions) - 1))

    def snapshot():
        return {"transmissions": list(transmissions), "next_timeout": timer,
                "message_failed": message_failed, "complete": complete}

    out = [snapshot()]
    for index, event in enumerate(events):
        now, kind = event["at_ms"], event["kind"]
        advance(now, False)
        if not complete and event.get("peer") == peer:
            if kind == "empty_ack" and event["mid"] == mid:
                timer = None
            elif (kind in ("piggyback", "separate") and event["token"] == token
                  and (kind == "separate" or event["mid"] == mid)):
                complete, timer = True, None
        # All input events at a timestamp precede a timeout at that timestamp.
        if index + 1 == len(events) or events[index + 1]["at_ms"] != now:
            advance(now, True)
        out.append(snapshot())
    return out
