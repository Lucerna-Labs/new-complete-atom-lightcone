"""Pitfall: released extents are sorted but never coalesced."""
import copy


def _coalesce(extents):
    merged = []
    for begin, end in sorted(extents):
        if merged and merged[-1][1] == begin:
            merged[-1][1] = end
        else:
            merged.append([begin, end])
    return merged


def allocator_trace(free_extents, header, events):
    free = _coalesce(free_extents)
    live = {}
    trace = []
    for event in events:
        op, identifier = event["op"], event["id"]
        address = None
        if op == "alloc":
            status = "failed"
            size, alignment = event["size"], event["align"]
            for index, (begin, end) in enumerate(free):
                payload = ((begin + header + alignment - 1) // alignment) * alignment
                stop = payload + size
                if stop <= end:
                    free[index:index + 1] = [[stop, end]] if stop < end else []
                    live[identifier] = {"extent": [begin, stop], "payload": payload, "size": size}
                    address = payload
                    status = "allocated"
                    break
        else:
            block = live.pop(identifier)
            free = sorted(free + [block["extent"]])
            status = "freed"
        trace.append(copy.deepcopy({"op": op, "id": identifier, "status": status,
                                    "address": address, "free": free, "live": live}))
    return trace
