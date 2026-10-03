"""Atomic symbolic counter effects with retained original invocation replies."""


def run_invocations(initial, events):
    def integer(value):
        return type(value) is int

    def name(value):
        return type(value) is str and 1 <= len(value) <= 32

    def shape(value, keys):
        return type(value) is dict and all(type(k) is str for k in value) and set(value) == keys

    if not integer(initial) or type(events) is not list or len(events) > 64:
        raise ValueError("arguments")
    total = initial
    ledger = {}
    results = []
    snapshots = []

    def snapshot():
        return {"total": total, "ledger": [
            {"client": client, "request": request, "delta": ledger[(client, request)]["delta"],
             "reply": ledger[(client, request)]["reply"]}
            for client, request in sorted(ledger)
        ]}

    schemas = {"request": {"kind", "client", "request", "delta"},
               "forget": {"kind", "client", "request"}, "crash": {"kind"}}
    for event in events:
        if type(event) is not dict or type(event.get("kind")) is not str:
            raise ValueError("event")
        kind = event["kind"]
        if kind not in schemas or not shape(event, schemas[kind]):
            raise ValueError("event schema")
        reply = None
        if kind == "crash":
            status = "recovered"
        else:
            client, request = event["client"], event["request"]
            if not name(client) or not integer(request) or request < 0:
                raise ValueError("identity")
            key = (client, request)
            if kind == "forget":
                status = "forgotten" if key in ledger else "absent"
                ledger.pop(key, None)
            else:
                delta = event["delta"]
                if not integer(delta):
                    raise ValueError("payload")
                if key not in ledger:
                    total += delta
                    ledger[key] = {"delta": delta, "reply": total}
                    status = "executed"
                    reply = total
                elif ledger[key]["delta"] == delta:
                    status = "replayed"
                    reply = total
                else:
                    status = "conflict"
        results.append({"kind": kind, "status": status, "reply": reply})
        snapshots.append(snapshot())
    return {"results": results, "snapshots": snapshots, "final": snapshot()}
