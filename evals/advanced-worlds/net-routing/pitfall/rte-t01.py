import ipaddress
def fib_lookup(routes, destination):
    address = ipaddress.ip_address(destination)
    for route in routes:
        network = ipaddress.ip_network(route["prefix"], strict=False)
        if address.version == network.version and address in network:
            return {"next_hop": route["next_hop"], "prefix": route["prefix"], "prefix_length": network.prefixlen}
    return {"next_hop": None, "prefix": None, "prefix_length": None}
