# Plausible pitfall: treat TTL as the number of additional edges allowed.
def convergence_probe(snapshot, destination, ttl, updates, start="A"):
    state = {router: dict(entry) for router, entry in snapshot.items()}
    for update in updates:
        state[update["router"]] = {"next_hop": update["next_hop"], "local": update["local"]}
    current, left, hops = start, ttl, []
    while True:
        hops.append(current)
        entry = state.get(current, {})
        if current == destination and entry.get("local", False):
            return {"hops": hops, "delivered": True, "expired": False}
        next_hop = entry.get("next_hop")
        if next_hop is None:
            return {"hops": hops, "delivered": False, "expired": False}
        # An IPv4 router cannot forward a packet after decrementing TTL to zero.
        if left == 0:
            return {"hops": hops, "delivered": False, "expired": True}
        left -= 1
        current = next_hop
