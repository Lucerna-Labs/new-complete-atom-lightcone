def trace_collection(graph, roots, young=None):
    """Analyze the declared complete static graph, without releasing storage."""
    selected = set(graph) if young is None else set(young)
    incoming = set()
    if young is not None:
        for source, targets in graph.items():
            if source not in selected and source in roots:  # Pitfall: only direct-root old sources count.
                incoming.update(target for target in targets if target in selected)
    marked = set(roots) & selected
    marked.update(incoming)
    pending = list(marked)
    while pending:
        source = pending.pop()
        for target in graph[source]:
            if target in selected and target not in marked:
                marked.add(target)
                pending.append(target)
    return {"incoming": sorted(incoming), "marked": sorted(marked),
            "unmarked": sorted(selected - marked)}
