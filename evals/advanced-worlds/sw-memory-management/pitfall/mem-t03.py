"""Serial logical Rc/Weak counts; not public introspection or real pointers."""

from copy import deepcopy


def rc_ownership(events):
    allocations = {}
    handles = {}
    raw = {}
    trace = []

    def release(allocation, kind):
        if allocation is None:
            return
        record = allocations[allocation]
        record[kind] -= 1
        if kind == "strong" and record["strong"] == 0:
            record["value_alive"] = False
            record["destructions"] += 1
        record["backing_alive"] = record["strong"] > 0

    for event in events:
        op = event["op"]
        upgraded = None
        if op == "new":
            allocation = event["allocation"]
            allocations[allocation] = {
                "strong": 1, "weak": 0, "forgotten_strong": 0, "forgotten_weak": 0,
                "value_alive": True, "backing_alive": True, "destructions": 0,
            }
            handles[event["strong"]] = {"kind": "strong", "allocation": allocation}
        elif op == "clone":
            entry = handles[event["source"]]
            handles[event["handle"]] = dict(entry)
            if entry["allocation"] is not None:
                allocations[entry["allocation"]][entry["kind"]] += 1
        elif op == "downgrade":
            allocation = handles[event["strong"]]["allocation"]
            handles[event["weak"]] = {"kind": "weak", "allocation": allocation}
            allocations[allocation]["weak"] += 1
        elif op == "empty_weak":
            handles[event["weak"]] = {"kind": "weak", "allocation": None}
        elif op == "upgrade":
            allocation = handles[event["weak"]]["allocation"]
            upgraded = allocation is not None and allocations[allocation]["strong"] > 0
            if upgraded:
                allocations[allocation]["strong"] += 1
                handles[event["strong"]] = {"kind": "strong", "allocation": allocation}
        elif op == "drop":
            entry = handles.pop(event["handle"])
            release(entry["allocation"], entry["kind"])
        elif op == "forget":
            entry = handles.pop(event["handle"])
            if entry["allocation"] is not None:
                allocations[entry["allocation"]]["forgotten_" + entry["kind"]] += 1
        elif op == "into_raw":
            raw[event["token"]] = handles.pop(event["handle"])
        elif op == "from_raw":
            handles[event["handle"]] = raw.pop(event["token"])
        trace.append({
            "op": op, "upgrade_succeeded": upgraded,
            "allocations": deepcopy(allocations), "handles": deepcopy(handles), "raw": deepcopy(raw),
        })
    return trace
