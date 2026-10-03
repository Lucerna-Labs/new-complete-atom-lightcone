def dnssec_cache_gate(record, now):
    accepted = (
        record["algorithm_supported"]
        and record["key_trusted"]
        and record["metadata_ok"]
        and record["signature_ok"]
        and record["inception"] <= now <= record["expiration"]
    )
    if not accepted:
        return {"accepted": False, "cache_ttl": 0}
    cache_ttl = min(
        record["rrset_ttl"],
        record["rrsig_ttl"],
        record["original_ttl"],
        record["expiration"] - now,
    )
    return {"accepted": True, "cache_ttl": cache_ttl}
