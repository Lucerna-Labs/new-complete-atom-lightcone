"""Naive occurs check incorrectly rejects a variable identity equation."""
def unify_types(equations):
    bindings = {}
    names = set()

    def variables(term):
        if isinstance(term, str):
            return set()
        if "var" in term:
            return {term["var"]}
        return variables(term["arrow"][0]) | variables(term["arrow"][1])

    for left, right in equations:
        names.update(variables(left))
        names.update(variables(right))

    def resolve(term):
        if isinstance(term, str):
            return term
        if "var" in term:
            name = term["var"]
            return resolve(bindings[name]) if name in bindings else {"var": name}
        return {"arrow": [resolve(child) for child in term["arrow"]]}

    def unify(left, right):
        left, right = resolve(left), resolve(right)
        if left == right:
            # Mistake: presence of the same variable is treated as a cycle.
            return not (isinstance(left, dict) and "var" in left)
        lv = left.get("var") if isinstance(left, dict) else None
        rv = right.get("var") if isinstance(right, dict) else None
        if lv is not None and rv is not None:
            bindings[max(lv, rv)] = {"var": min(lv, rv)}
            return True
        if lv is not None or rv is not None:
            name, term = (lv, right) if lv is not None else (rv, left)
            if name in variables(term):
                return False
            bindings[name] = term
            return True
        if isinstance(left, dict) and isinstance(right, dict):
            return unify(left["arrow"][0], right["arrow"][0]) and unify(left["arrow"][1], right["arrow"][1])
        return False

    for left, right in equations:
        if not unify(left, right):
            return {"ok": False, "substitution": {}}
    return {"ok": True, "substitution": {name: resolve({"var": name}) for name in sorted(names)}}
