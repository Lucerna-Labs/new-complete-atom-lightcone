def marking_trace(graph, roots, events, barrier=True):
    """Execute only the declared fixed-root, no-allocation interleaving model."""
    fields = {name: list(targets) for name, targets in graph.items()}
    colors = {name: "white" for name in graph}
    gray = []
    finished = False
    missed = []

    def shade(target):
        if target is not None and colors[target] == "white":
            colors[target] = "gray"
            gray.append(target)

    def snapshot():
        return {"gray": list(gray),
                "black": sorted(name for name in graph if colors[name] == "black"),
                "white": sorted(name for name in graph if colors[name] == "white"),
                "finished": finished, "missed": list(missed)}

    for root in roots:
        shade(root)
    result = [snapshot()]
    for event in events:
        if event["op"] == "scan":
            if gray:
                source = gray.pop(0)
                for target in fields[source]:
                    shade(target)
                colors[source] = "black"
        elif event["op"] == "store":
            source, target = event["object"], event["target"]
            if barrier and colors[source] == "black":
                shade(target)
            fields[source][event["index"]] = target
        elif not gray:
            finished = True
            reachable = set(roots)
            pending = list(roots)
            while pending:
                for target in fields[pending.pop()]:
                    if target is not None and target not in reachable:
                        reachable.add(target)
                        pending.append(target)
            missed = sorted(name for name in reachable if colors[name] == "white")
        result.append(snapshot())
    return result
