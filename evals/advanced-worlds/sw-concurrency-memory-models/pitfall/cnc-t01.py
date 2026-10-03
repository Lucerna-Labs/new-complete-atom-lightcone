"""Lexicographic SC witness for the task's fixed straight-line load/store model."""
import heapq


def sc_witness(threads, modification_order):
    operations = {op["id"]: op for sequence in threads.values() for op in sequence}
    following = {key: set() for key in operations}
    incoming = {key: 0 for key in operations}

    def edge(before, after):
        if after not in following[before]:
            following[before].add(after)
            incoming[after] += 1

    # Mistake: retain program order separately per object, losing its cross-object edges.
    for obj in modification_order:
        for sequence in threads.values():
            local = [op for op in sequence if op["object"] == obj]
            for before, after in zip(local, local[1:]):
                edge(before["id"], after["id"])
    for writes in modification_order.values():
        for before, after in zip(writes, writes[1:]):
            edge(before, after)
    for name, op in operations.items():
        if op["kind"] != "load":
            continue
        writes = modification_order[op["object"]]
        source = op["reads_from"]
        start = 0
        if source is not None:
            edge(source, name)
            start = writes.index(source) + 1
        # The named source must be this load's latest preceding modification.
        for later in writes[start:]:
            edge(name, later)

    ready = [name for name in operations if incoming[name] == 0]
    heapq.heapify(ready)
    result = []
    while ready:
        name = heapq.heappop(ready)
        result.append(name)
        for after in following[name]:
            incoming[after] -= 1
            if incoming[after] == 0:
                heapq.heappush(ready, after)
    return result if len(result) == len(operations) else None
