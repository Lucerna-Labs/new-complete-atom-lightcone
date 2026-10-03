"""Symbolic arena lifetimes with non-nested, nontransparent replacement."""

from copy import deepcopy


def arena_lifetimes(capacity, cleanup_on_reset, events):
    cursor = 0
    objects = {}
    order = []
    refs = {}
    destructor_log = []
    trace = []

    def destroy(oid):
        record = objects[oid]
        record["state"] = "destroyed"
        if record["nested_state"] == "owned":
            record["nested_state"] = "released"
        destructor_log.append(oid)

    for event in events:
        op = event["op"]
        if op == "alloc":
            size = event["size"]
            if size > capacity - cursor:
                status = "no-space"
            else:
                end = cursor + size
                for record in objects.values():
                    if (record["state"] == "live"
                            and cursor < record["start"] + record["size"]
                            and record["start"] < end):
                        record["state"] = "reused"
                        if record["nested_state"] == "owned":
                            record["nested_state"] = "leaked"
                nested = event["nested_bytes"]
                objects[event["id"]] = {
                    "start": cursor, "size": size, "state": "live", "nested_bytes": nested,
                    "nested_state": "owned" if nested else "none",
                }
                order.append(event["id"])
                cursor = end
                status = "allocated"
        elif op == "alias":
            refs[event["ref"]] = event["object"]
            status = "aliased"
        elif op == "read":
            status = "valid" if objects[refs[event["ref"]]]["state"] == "live" else "expired"
        elif op == "drop_ref":
            refs.pop(event["ref"])
            status = "released-reference"
        elif op == "destroy":
            destroy(event["object"])
            status = "destroyed"
        elif op == "reset":
            if cleanup_on_reset:
                for oid in reversed(order):
                    if objects[oid]["state"] == "live":
                        destroy(oid)
            cursor = 0
            status = "reset"
        trace.append({
            "op": op, "status": status, "cursor": cursor,
            "objects": deepcopy(objects), "refs": dict(refs), "destructor_log": list(destructor_log),
            "live_nested_bytes": sum(r["nested_bytes"] for r in objects.values()
                                     if r["nested_state"] in ("owned", "leaked")),
            "leaked_nested_bytes": sum(r["nested_bytes"] for r in objects.values()
                                       if r["nested_state"] == "leaked"),
        })
    return trace
