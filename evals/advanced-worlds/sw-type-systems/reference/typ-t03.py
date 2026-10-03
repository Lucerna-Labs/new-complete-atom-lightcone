"""Finite declared variance algebra, not a full compiler assignability engine."""


def assignability_matrix(parents, sources, targets, strict_function_types=True):
    def subtype(source, target):
        pending = [source]
        seen = set()
        while pending:
            current = pending.pop()
            if current == target:
                return True
            if current not in seen:
                seen.add(current)
                pending.extend(parents[current])
        return False

    def assign(source, target):
        kind = source["kind"]
        if kind != target["kind"]:
            return False
        if kind in ("value", "producer"):
            return subtype(source["type"], target["type"])
        if kind == "consumer":
            return subtype(target["type"], source["type"])
        if kind == "cell":
            return source["type"] == target["type"]
        bivariant = kind == "method" or not strict_function_types
        arguments = subtype(target["arg"], source["arg"])
        if bivariant:
            arguments = arguments or subtype(source["arg"], target["arg"])
        return arguments and subtype(source["result"], target["result"])

    return [[assign(source, target) for target in targets] for source in sources]
