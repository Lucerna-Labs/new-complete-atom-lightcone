def compact_key(records, last_sequence, snapshots=None, deeper_overlap=False):
    horizon = min(snapshots) if snapshots else last_sequence
    preceding = None
    kept = []
    dropped = []
    for record in records:
        sequence = record["sequence"]
        if preceding is not None and preceding <= horizon:
            reason = "shadowed"
        elif record["kind"] == "delete" and sequence <= horizon:  # Error: ignores deeper ranges.
            reason = "obsolete_deletion"
        else:
            reason = None
        if reason is None:
            kept.append(dict(record))
        else:
            dropped.append({"sequence": sequence, "reason": reason})
        preceding = sequence
    return {"horizon": horizon, "kept": kept, "dropped": dropped}
