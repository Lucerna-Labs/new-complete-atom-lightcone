def validate_record(value):
    """Validate only the declared own-field schema of a flat tagged object."""
    if value["tag"] != "object":
        return {"ok": False, "errors": ["object-required"], "data": None}
    own = value["own"]
    errors = []
    age_present = "age" in own and own["age"]["tag"] != "undefined"  # Pitfall: present undefined is treated as absent.
    if "name" not in own:
        errors.append("name-missing")
    elif own["name"]["tag"] != "string":
        errors.append("name-type")
    if age_present and own["age"]["tag"] != "number":
        errors.append("age-type")
    if errors:
        return {"ok": False, "errors": errors, "data": None}
    data = {"name": own["name"]["value"]}
    if age_present:
        data["age"] = own["age"]["value"]
    return {"ok": True, "errors": [], "data": data}
