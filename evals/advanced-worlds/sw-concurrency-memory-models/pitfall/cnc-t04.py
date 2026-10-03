"""Symbolic SC hazard lifecycle monitor; no real pointer dereference occurs."""

from copy import deepcopy


def hazard_trace(nodes, source, events):
    readers = {}
    retired = set()
    reclaimed = set()
    trace = []
    for event in events:
        op = event["op"]
        result = None
        if "reader" in event:
            reader = readers.setdefault(event["reader"], {
                "candidate": None, "hazard": None, "validated": False})
        if op == "load":
            reader["candidate"] = source
            reader["validated"] = False
            result = source
        elif op == "publish":
            reader["hazard"] = reader["candidate"]
            reader["validated"] = False
            result = reader["hazard"]
        elif op == "validate":
            candidate = reader["candidate"]
            reader["validated"] = (candidate is not None
                                   and candidate == reader["hazard"]
                                   and candidate == source
                                   and candidate not in reclaimed)
            result = reader["validated"]
        elif op == "clear":
            reader["hazard"] = None
            reader["validated"] = False
        elif op == "set_source":
            source = event["node"]
        elif op == "retire":
            retired.add(event["node"])
        elif op == "scan":
            protected = {r["hazard"] for r in readers.values()}
            result = sorted(retired - protected)
            retired.difference_update(result)
            reclaimed.update(result)
        elif op == "use":
            candidate = reader["candidate"]
            if candidate is None:
                result = "empty"
            elif candidate in reclaimed:
                result = "reclaimed"
            elif reader["hazard"] != candidate:
                result = "unprotected"
            else:
                result = "safe"
        trace.append({"op": op, "result": result, "source": source,
                      "retired": sorted(retired),
                      "reclaimed": sorted(reclaimed),
                      "readers": deepcopy(readers)})
    return trace
