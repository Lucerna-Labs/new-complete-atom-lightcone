def slaac_update(now, remaining_valid, advertised_valid, advertised_preferred, authenticated=False):
    if advertised_valid > 7200 or advertised_valid > remaining_valid:
        valid = advertised_valid
    elif remaining_valid <= 7200:
        valid = advertised_valid if authenticated else remaining_valid
    else:
        valid = 7200
    preferred = advertised_preferred
    state = "invalid" if valid == 0 else "deprecated" if preferred == 0 else "preferred"
    return {"valid_remaining": valid, "preferred_remaining": preferred,
            "valid_until": now + valid, "preferred_until": now + preferred,
            "state": state}
