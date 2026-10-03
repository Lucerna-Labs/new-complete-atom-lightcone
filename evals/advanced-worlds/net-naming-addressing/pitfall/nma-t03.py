# Semantic pitfall: confuses endpoint-independent mapping with unrestricted filtering.
def nat_trace(events, mapping_mode="eim", filter_mode="apdf", idle_timeout=5,
              external_ip="203.0.113.1", first_port=40000):
    bindings = {}
    next_port = first_port
    output = []

    def expire(now):
        for key in list(bindings):
            if bindings[key]["expires_at"] <= now:
                del bindings[key]

    for event in events:
        now = event["time"]
        expire(now)
        result, external, internal = "tick", None, None
        if event["type"] == "outbound":
            local = tuple(event["internal"])
            remote = tuple(event["remote"])
            key = (local,) if mapping_mode == "eim" else (local, remote)
            if key not in bindings:
                bindings[key] = {
                    "internal": local, "port": next_port,
                    "contacts": set(), "expires_at": now + idle_timeout,
                }
                next_port += 1
            binding = bindings[key]
            binding["contacts"].add(remote)
            binding["expires_at"] = now + idle_timeout
            result = "mapped"
            external = [external_ip, binding["port"]]
        elif event["type"] == "inbound":
            destination = event["external"]
            remote = tuple(event["remote"])
            binding = next((b for b in bindings.values()
                            if destination[0] == external_ip
                            and b["port"] == destination[1]), None)
            if binding is None:
                result = "unmapped"
            elif mapping_mode == "eim" or filter_mode == "eif" or remote in binding["contacts"]:
                result = "delivered"
                internal = list(binding["internal"])
            else:
                result = "filtered"
        elif event["type"] != "tick":
            raise ValueError("unknown event")
        # Zero-timeout bindings can translate this outbound packet, but
        # do not survive its snapshot or a later event at the same tick.
        expire(now)
        output.append({
            "result": result, "external": external, "internal": internal,
            "live_ports": sorted(b["port"] for b in bindings.values()),
        })
    return output
