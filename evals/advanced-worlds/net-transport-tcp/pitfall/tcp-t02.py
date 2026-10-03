def decode_and_budget(window_field, advertiser, syn, a_shift, b_shift, cwnd, flight):
    # Wrongly uses the sender's shift and applies scaling to SYN windows.
    shift = b_shift if advertiser == "a" else a_shift
    rwnd = int(window_field) * (1 << int(shift))
    return {"rwnd": rwnd, "budget": max(0, min(int(cwnd), rwnd))}
