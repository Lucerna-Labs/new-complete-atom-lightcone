def qpack_trace(events, max_blocked_streams=2):
    insertion = 0
    known = 0
    entries = {}
    pending = {}
    out = []
    for event in events:
        kind = event["type"]
        error = None
        if kind == "insert":
            ordinal = int(event["ordinal"])
            if ordinal != insertion + 1:
                error = "insertion-order"
            else:
                insertion = ordinal
                entries[ordinal] = False
        elif kind == "section":
            stream = int(event["stream"])
            refs = [int(x) for x in event["refs"]]
            blocked = {s for s, sections in pending.items() if any(max(sec) > known for sec in sections)}
            required = max(refs)
            if required > insertion:
                error = "unknown-reference"
            elif required > known and stream not in blocked and len(blocked) >= max_blocked_streams:
                error = "blocked-limit"
            else:
                pending.setdefault(stream, []).append(refs)
        elif kind == "known":
            count = int(event["count"])
            if count > insertion:
                error = "known-count"
            else:
                known = max(known, count)
        elif kind == "section_ack":
            stream = int(event["stream"])
            if stream not in pending or not pending[stream]:
                error = "section-ack"
            else:
                refs = pending[stream].pop(0)
                if not pending[stream]:
                    del pending[stream]
                known = max(known, max(refs))
        elif kind == "cancel":
            pending.pop(int(event["stream"]), None)
        elif kind == "evict":
            ordinal = int(event["ordinal"])
            referenced = any(ordinal in refs for sections in pending.values() for refs in sections)
            oldest = min(entries) if entries else None
            if ordinal not in entries or not entries[ordinal] or referenced or ordinal != oldest:
                error = "eviction"
            else:
                del entries[ordinal]
        else:
            error = "event"
        # Receipt knowledge covers every insertion up to KRC, not only
        # entries directly named by an acknowledged field section.
        for ordinal in entries:
            entries[ordinal] = ordinal <= known
        blocked_streams = sorted(s for s, sections in pending.items() if any(max(sec) > known for sec in sections))
        out.append({"known_received": known, "insertion_progress": insertion,
                    "blocked_streams": blocked_streams, "pending_sections": sum(map(len, pending.values())),
                    "entries": [{"ordinal": o, "acknowledged": entries[o]} for o in sorted(entries)], "error": error})
    return out
