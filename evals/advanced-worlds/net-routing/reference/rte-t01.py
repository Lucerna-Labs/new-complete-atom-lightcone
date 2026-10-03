import ipaddress
def fib_lookup(routes, destination):
    address = ipaddress.ip_address(destination)
    best = None
    best_len = -1
    for route in routes:
        network = ipaddress.ip_network(route["prefix"], strict=False)
        if address.version == network.version and address in network and network.prefixlen > best_len:
            best, best_len = route, network.prefixlen
    if best is None:
        return {"next_hop": None, "prefix": None, "prefix_length": None}
    return {"next_hop": best["next_hop"], "prefix": best["prefix"], "prefix_length": best_len}
