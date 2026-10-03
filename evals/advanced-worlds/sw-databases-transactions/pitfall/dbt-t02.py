import heapq


def precedence_graph(transactions, operations=None):
    edges = set()
    previous = {}
    for operation in operations or []:
        for earlier in previous.get(operation["key"], [])[-1:]:  # Error: only adjacent same-key operations.
            if earlier["tx"] != operation["tx"] and (
                    earlier["kind"] == "write" or operation["kind"] == "write"):
                edges.add((earlier["tx"], operation["tx"]))
        previous.setdefault(operation["key"], []).append(operation)
    outgoing = {tx: [] for tx in transactions}
    indegree = {tx: 0 for tx in transactions}
    for source, target in edges:
        outgoing[source].append(target)
        indegree[target] += 1
    ready = [tx for tx in transactions if indegree[tx] == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        source = heapq.heappop(ready)
        order.append(source)
        for target in outgoing[source]:
            indegree[target] -= 1
            if indegree[target] == 0:
                heapq.heappush(ready, target)
    acyclic = len(order) == len(transactions)
    return {"edges": [list(edge) for edge in sorted(edges)],
            "acyclic": acyclic, "order": order if acyclic else None}
