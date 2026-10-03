def negative_lookup(entry, query, now):
    miss = {"kind": None, "ttl": 0}
    if entry is None:
        return miss
    if (entry["negative_name"].lower() != query["name"].lower()
            or entry["qclass"].upper() != query["qclass"].upper()
            or entry["view"] != query["view"]):
        return miss
    if entry["kind"] == "NODATA" and entry["qtype"].upper() != query["qtype"].upper():
        return miss
    remaining = min(entry["soa_ttl"], entry["soa_minimum"]) - (now - entry["stored_at"])
    if remaining <= 0:
        return miss
    return {"kind": entry["kind"], "ttl": remaining}
