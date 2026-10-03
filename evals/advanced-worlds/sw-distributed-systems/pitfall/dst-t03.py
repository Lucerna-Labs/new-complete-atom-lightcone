def _validate(n, trace, pairs):
    if type(n) is not int or not 1 <= n <= 8 or type(trace) is not list or len(trace) > 64 or type(pairs) is not list or len(pairs) > 128: raise ValueError("domain")
    ids, messages, sends = set(), set(), {}
    for e in trace:
        if type(e) is not dict or type(e.get("id")) is not str or not e["id"] or len(e["id"]) > 32 or e["id"] in ids or type(e.get("process")) is not int or not 0 <= e["process"] < n or e.get("kind") not in ("local", "send", "receive"): raise ValueError("event")
        ids.add(e["id"]); kind=e["kind"]; required={"id","process","kind"}|({"message","to"} if kind=="send" else {"message"} if kind=="receive" else set())
        if set(e)!=required or (kind in ("send","receive") and (type(e["message"]) is not str or not e["message"] or len(e["message"]) > 32)): raise ValueError("fields")
        if kind=="send":
            if e["message"] in messages or type(e["to"]) is not int or not 0 <= e["to"] < n: raise ValueError("send")
            messages.add(e["message"]); sends[e["message"]]=e
        elif kind=="receive" and (e["message"] not in sends or sends[e["message"]]["to"] != e["process"]): raise ValueError("receive")
    for pair in pairs:
        if type(pair) is not list or len(pair)!=2 or any(type(x) is not str or x not in ids for x in pair): raise ValueError("pair")

def annotate_trace(n, trace, pairs):
    _validate(n, trace, pairs)
    events = []
    sends, scalar, vectors = {}, [0] * n, [[0] * n for _ in range(n)]
    for raw in trace:
        p, kind = raw["process"], raw["kind"]
        if kind == "receive":
            send = sends[raw["message"]]
            scalar[p] = max(scalar[p], send["lamport"]) + 1
            vectors[p] = [max(a, b) for a, b in zip(vectors[p], send["vector"])]
            vectors[p][p] += 1
        else:
            scalar[p] += 1
            vectors[p][p] += 1
        events.append({"id": raw["id"], "lamport": scalar[p], "vector": list(vectors[p])})
        if kind == "send":
            sends[raw["message"]] = {"lamport": scalar[p], "vector": list(vectors[p])}
    by = {e["id"]: e for e in events}
    orders = []
    for left, right in pairs:
        if left == right: orders.append("same")
        elif all(a < b for a, b in zip(by[left]["vector"], by[right]["vector"])): orders.append("before")
        elif all(a > b for a, b in zip(by[left]["vector"], by[right]["vector"])): orders.append("after")
        else: orders.append("concurrent")
    return {"events": events, "orders": orders}
