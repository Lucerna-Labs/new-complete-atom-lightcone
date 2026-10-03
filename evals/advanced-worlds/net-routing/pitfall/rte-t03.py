# Semantic pitfall: only the most-specific covering VRPs are considered.
import ipaddress


def classify_roa(vrps, announcement, reject_invalid=False):
    route = ipaddress.ip_network(announcement["prefix"], strict=False)
    origin = announcement["origin_as"]
    covering = []
    for vrp in vrps:
        network = ipaddress.ip_network(vrp["prefix"], strict=False)
        if network.version == route.version and route.subnet_of(network):
            covering.append(vrp)
    if covering:
        longest = max(ipaddress.ip_network(v["prefix"], strict=False).prefixlen for v in covering)
        covering = [v for v in covering if ipaddress.ip_network(v["prefix"], strict=False).prefixlen == longest]
    # AS 0 and an unknown origin cannot match any authorization.
    valid = origin is not None and origin != 0 and any(
        vrp["origin_as"] == origin and route.prefixlen <= vrp["max_length"]
        for vrp in covering
    )
    classification = "valid" if valid else ("invalid" if covering else "not-found")
    return {
        "classification": classification,
        "eligible": not (reject_invalid and classification == "invalid"),
    }
