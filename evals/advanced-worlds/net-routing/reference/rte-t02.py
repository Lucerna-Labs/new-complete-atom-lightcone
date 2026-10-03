def select_bgp_path(paths, local_as):
    eligible = [p for p in paths if local_as not in p["as_path"] and p["next_hop_resolvable"]]
    if not eligible:
        return {"selected": None, "eligible": []}
    med_enabled = len(eligible) == 2 and eligible[0]["neighbor_as"] == eligible[1]["neighbor_as"]
    def key(p):
        med = p["med"] if p["med"] is not None else 0
        return (-p["local_pref"], len(p["as_path"]),
                {"IGP": 0, "EGP": 1, "INCOMPLETE": 2}[p["origin"]],
                med if med_enabled else 0, -int(p["ebgp"]), p["igp_cost"], p["id"])
    return {"selected": min(eligible, key=key)["id"],
            "eligible": sorted(p["id"] for p in eligible)}
