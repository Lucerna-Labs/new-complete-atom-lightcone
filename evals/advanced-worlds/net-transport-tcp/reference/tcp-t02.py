def decode_and_budget(window_field, advertiser, syn, a_shift, b_shift, cwnd, flight):
    if advertiser not in ("a", "b"):
        raise ValueError("advertiser")
    shift = 0 if syn else (a_shift if advertiser == "a" else b_shift)
    rwnd = int(window_field) * (1 << int(shift))
    budget = max(0, min(int(cwnd), rwnd) - int(flight))
    return {"rwnd": rwnd, "budget": budget}
