def analyze_links(links, powers, noise, cca, thresholds):
    """Pitfall: local receiver success is mistaken for two-link safe reuse."""
    states = []
    for i, link in enumerate(links):
        sender, receiver = link["sender"], link["receiver"]
        other = links[1 - i]["sender"]
        signal = powers[sender][receiver]
        alone = signal / noise[receiver]
        overlap = signal / (noise[receiver] + powers[other][receiver])
        states.append({"sender": sender, "receiver": receiver,
                       "carrier_busy": powers[other][sender] >= cca[sender],
                       "snr_alone": alone, "sinr_overlap": overlap,
                       "decodes_alone": alone >= thresholds[i],
                       "decodes_overlap": overlap >= thresholds[i]})
    feasible = all(state["decodes_overlap"] for state in states)
    for state in states:
        state["hidden_harm"] = (not state["carrier_busy"]
                                and state["decodes_alone"]
                                and not state["decodes_overlap"])
        state["exposed_deferral"] = state["carrier_busy"] and state["decodes_overlap"]
    return {"links": states, "simultaneous_feasible": feasible,
            "mutually_unsensed": not any(state["carrier_busy"] for state in states)}
