def generalize_instantiate(inferred, environment, substitution, count=2):
    """Transform finite schemes under the declared binding-store profile."""
    def free_type(ty):
        if type(ty) is str:
            return set()
        if "var" in ty:
            return {ty["var"]}
        return free_type(ty["from"]) | free_type(ty["to"])

    def rename(ty, mapping):
        if type(ty) is str:
            return ty
        if "var" in ty:
            return {"var": mapping.get(ty["var"], ty["var"])}
        return {"from": rename(ty["from"], mapping), "to": rename(ty["to"], mapping)}

    def expand(ty):
        if type(ty) is str:
            return ty
        if "var" in ty:
            name = ty["var"]
            return expand(substitution[name]) if name in substitution else {"var": name}
        return {"from": expand(ty["from"]), "to": expand(ty["to"])}

    occupied = free_type(inferred) | set(substitution)
    for ty in substitution.values():
        occupied.update(free_type(ty))
    for scheme in environment.values():
        occupied.update(scheme["bound"])
        occupied.update(free_type(scheme["body"]))
    next_index = 0

    def fresh():
        nonlocal next_index
        while "t" + str(next_index) in occupied:
            next_index += 1
        name = "t" + str(next_index)
        next_index += 1
        occupied.add(name)
        return name

    normalized_ranges = {key: expand(ty) for key, ty in substitution.items()}
    range_free = set()
    for ty in normalized_ranges.values():
        range_free.update(free_type(ty))

    def apply_free(ty, protected):
        if type(ty) is str:
            return ty
        if "var" in ty:
            name = ty["var"]
            if name not in protected and name in normalized_ranges:
                return rename(normalized_ranges[name], {})
            return {"var": name}
        return {"from": apply_free(ty["from"], protected),
                "to": apply_free(ty["to"], protected)}

    normalized_type = apply_free(inferred, set())
    normalized_environment = {}
    for term in sorted(environment):
        scheme = environment[term]
        changes = {name: fresh() for name in scheme["bound"] if name in range_free}
        bound = [changes.get(name, name) for name in scheme["bound"]]
        body = apply_free(rename(scheme["body"], changes), set(bound))
        normalized_environment[term] = {"bound": bound, "body": body}

    def free_environment(env):
        found = set()
        for scheme in env.values():
            found.update(free_type(scheme["body"]) - set(scheme["bound"]))
        return found

    generalized = sorted(free_type(normalized_type) - free_environment(environment))  # Pitfall: generalize against the old context.
    scheme = {"bound": list(generalized), "body": rename(normalized_type, {})}
    instances = []
    for _ in range(count):
        changes = {name: fresh() for name in generalized}
        instances.append({"renaming": changes, "body": rename(normalized_type, changes)})
    return {"normalized_type": normalized_type, "environment": normalized_environment,
            "scheme": scheme, "instances": instances}
