"""Durable per-resource fencing floors remain separate from issued epochs."""


def run_fences(resources, events):
    def integer(value):
        return type(value) is int

    def name(value):
        return type(value) is str and 1 <= len(value) <= 32

    def shape(value, keys):
        return type(value) is dict and all(type(k) is str for k in value) and set(value) == keys

    if type(resources) is not dict or len(resources) > 8:
        raise ValueError("resources")
    for resource, record in resources.items():
        if not name(resource) or not shape(record, {"issued", "floor", "value"}):
            raise ValueError("resource schema")
        if not all(integer(record[key]) for key in ("issued", "floor", "value")):
            raise ValueError("resource integers")
        if not 0 <= record["floor"] <= record["issued"]:
            raise ValueError("resource bounds")
    if type(events) is not list or len(events) > 64:
        raise ValueError("events")
    state = {resource: dict(record) for resource, record in resources.items()}

    def snapshot():
        return {resource: dict(record) for resource, record in state.items()}

    results = []
    states = []
    schemas = {"issue": {"kind", "resource"}, "install": {"kind", "resource", "token"},
               "write": {"kind", "resource", "token", "delta"}, "crash": {"kind"}}
    for event in events:
        if type(event) is not dict or type(event.get("kind")) is not str:
            raise ValueError("event")
        kind = event["kind"]
        if kind not in schemas or not shape(event, schemas[kind]):
            raise ValueError("event schema")
        if kind == "crash":
            results.append({"kind": kind, "resource": None, "token": None, "accepted": None, "value": None})
        else:
            resource = event["resource"]
            if not name(resource) or resource not in state:
                raise ValueError("unknown resource")
            record = state[resource]
            if kind == "issue":
                record["issued"] += 1
                token = record["issued"]
                accepted = None
            else:
                token = event["token"]
                if not integer(token) or not 1 <= token <= record["issued"]:
                    raise ValueError("token")
                if kind == "write" and not integer(event["delta"]):
                    raise ValueError("delta")
                accepted = token >= record["floor"]
                if accepted:
                    record["floor"] = max(record["floor"], token)
                    if kind == "write":
                        record["value"] += event["delta"]
            results.append({"kind": kind, "resource": resource, "token": token,
                            "accepted": accepted, "value": record["value"]})
        states.append(snapshot())
    return {"results": results, "states": states, "final": snapshot()}
