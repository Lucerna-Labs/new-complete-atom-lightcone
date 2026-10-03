def burst_handoff(rx_max, rx_packets, fixed_overhead_ns, tx_returns):
    """Account for observed burst results, not a hardware or completion model."""
    count = len(rx_packets)
    remaining = list(rx_packets)
    transferred, attempts = [], []
    for returned in tx_returns:
        submitted = list(remaining)
        accepted_count = returned
        accepted = remaining[:accepted_count]
        remaining = remaining[accepted_count:]
        transferred.extend(accepted)
        attempts.append({"submitted": submitted, "returned": returned,
                         "accepted": accepted, "remaining": list(remaining)})
    return {
        "rx": {"packets": list(rx_packets), "count": count,
               "wait_for_more": False,
               "amortized_overhead_ns": fixed_overhead_ns / count if count else None},
        "tx": {"attempts": attempts, "transferred": transferred,
               "caller_owned": remaining, "peer_delivery": "unknown"},
    }
