def dce_slice(entry, blocks, parameters=None):
    """Conservative structural reachability and observable dependency slicing."""
    reachable = {entry}
    pending = [entry]
    while pending:
        source = pending.pop()
        for successor in blocks[source]["successors"]:
            if successor not in reachable and blocks[successor]["profile_count"] > 0:  # Pitfall: zero observations prove no future reachability.
                reachable.add(successor)
                pending.append(successor)
    instructions = {instruction["id"]: instruction
                    for block in blocks.values() for instruction in block["instructions"]}
    live = {instruction["id"] for name in reachable
            for instruction in blocks[name]["instructions"] if instruction["kind"] != "pure"}
    parameters = set(parameters or [])
    pending = list(live)
    while pending:
        for operand in instructions[pending.pop()]["uses"]:
            if operand not in parameters and operand not in live:
                live.add(operand)
                pending.append(operand)
    return {"reachable": sorted(reachable),
            "kept": {name: [instruction["id"] for instruction in blocks[name]["instructions"]
                            if instruction["id"] in live] for name in sorted(reachable)},
            "removed": sorted(set(instructions) - live)}
