"""Naive reused-miss diagnosis attributes every reused miss to capacity."""
def cache_trace(addresses, line_bytes=16, set_count=2, ways=1):
    cache = [[] for _ in range(set_count)]
    reference = []
    seen = set()
    counts = {"hit": 0, "compulsory": 0, "conflict": 0, "capacity": 0}
    trace = []
    for address in addresses:
        block = address // line_bytes
        index = block % set_count
        row = cache[index]
        hit = block in row
        reference_hit = block in reference
        if hit:
            classification = "hit"
        elif block not in seen:
            classification = "compulsory"
        else:
            classification = "capacity"
        counts[classification] += 1
        evicted = None
        if hit:
            row.remove(block)
        elif len(row) == ways:
            evicted = row.pop(0)
        row.append(block)
        if reference_hit:
            reference.remove(block)
        elif len(reference) == set_count * ways:
            reference.pop(0)
        reference.append(block)
        seen.add(block)
        trace.append({"address": address, "block": block, "set": index,
                      "tag": block // set_count, "hit": hit,
                      "reference_hit": reference_hit,
                      "classification": classification, "evicted": evicted,
                      "cache": [list(r) for r in cache],
                      "reference": list(reference)})
    misses = len(addresses) - counts["hit"]
    return {"hits": counts["hit"], "misses": misses,
            "compulsory": counts["compulsory"], "conflict": counts["conflict"],
            "capacity": counts["capacity"], "transferred_bytes": misses * line_bytes,
            "cache": [list(row) for row in cache],
            "reference": list(reference), "trace": trace}
