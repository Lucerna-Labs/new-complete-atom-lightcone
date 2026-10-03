def ssa_availability(entry, blocks, definitions, uses, parameters=None):
    """Check only the specified SSA operand-availability rules."""
    names = set(blocks)
    predecessors = {name: set() for name in blocks}
    for source, block in blocks.items():
        for target in block["successors"]:
            predecessors[target].add(source)
    dominators = {name: {entry} if name == entry else set(names) for name in blocks}
    changed = True
    while changed:
        changed = False
        for name in blocks:
            if name == entry:
                continue
            shared = set.intersection(*(dominators[p] for p in predecessors[name]))
            updated = {name} | shared
            if updated != dominators[name]:
                dominators[name] = updated
                changed = True
    parameters = set(parameters or [])
    available = []
    for use in uses:
        if use["value"] in parameters:
            available.append(True)
            continue
        definition = definitions[use["value"]]
        site = use["predecessor"] if use["kind"] == "phi" else use["block"]
        if use["kind"] == "ordinary" and definition["block"] == site:
            ok = definition["position"] < use["position"]
        else:
            ok = definition["block"] in dominators[site]
        available.append(ok)
    return {"dominators": {name: sorted(dominators[name]) for name in sorted(blocks)},
            "available": available}
