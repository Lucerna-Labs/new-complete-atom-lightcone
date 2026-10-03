# Semantic pitfall: clamps sub-minimum IPv6 PTB instead of discarding it.
def pmtu_trace(events):
    cache = {}
    families = {}
    out = []
    feedback_families = {"ipv4_feedback": 4, "ipv6_feedback": 6}
    minimum_mtu = {4: 68, 6: 1280}
    for event in events:
        kind = event["type"]
        sent_size = None
        if kind == "init":
            path = event["path"]
            families[path] = event["family"]
            cache[path] = event["mtu"]
        elif kind == "send":
            sent_size = min(event["want"], cache[event["path"]])
        elif kind in feedback_families:
            path = event["path"]
            family = feedback_families[kind]
            reported = event["mtu"]
            if family == 6:
                reported = max(1280, reported)
            if (event["validated"] and event["applicable"]
                    and families[path] == family
                    and reported >= minimum_mtu[family]):
                cache[path] = min(cache[path], reported)
        out.append({"cache": dict(sorted(cache.items())), "sent_size": sent_size})
    return out
