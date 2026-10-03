"""A bounded physical WAL-prefix model, not a database or visibility engine."""


def wal_trace(records, events, initial_pages=None):
    names = {record["page"] for record in records if record["kind"] == "page"}
    base = {name: 0 for name in names} if initial_pages is None else dict(initial_pages)
    pages = {name: {"lsn": 0, "value": value} for name, value in base.items()}
    commits = {record["tx"]: i for i, record in enumerate(records, 1)
               if record["kind"] == "commit"}
    written = 0
    durable = 0
    acknowledged = set()

    def snapshot(result=None, recovery=None):
        return {
            "written": written, "durable": durable,
            "pages": {name: dict(page) for name, page in pages.items()},
            "acknowledged": sorted(acknowledged),
            "durable_commits": sorted(tx for tx, lsn in commits.items() if lsn <= durable),
            "event_result": result,
            "recovery": None if recovery is None else {key: list(value) for key, value in recovery.items()},
        }

    output = [snapshot()]
    for event in events:
        recovery = None
        op = event["op"]
        if op == "write":
            written = event["through"]
            result = "written"
        elif op == "flush":
            durable = event["through"]
            result = "flushed"
        elif op == "page_write":
            lsn = event["lsn"]
            record = records[lsn - 1]
            if durable >= lsn:
                pages[record["page"]] = {"lsn": lsn, "value": record["value"]}
                result = "page-written"
            else:
                result = "wal-blocked"
        elif op == "ack":
            if event["mode"] == "async" or durable >= commits[event["tx"]]:
                acknowledged.add(event["tx"])
                result = "acknowledged"
            else:
                result = "awaiting-flush"
        else:
            written = durable
            scanned = list(range(event["redo_start"], durable + 1))
            applied = []
            for lsn in scanned:
                record = records[lsn - 1]
                if record["kind"] == "page" and lsn > pages[record["page"]]["lsn"]:
                    pages[record["page"]] = {"lsn": lsn, "value": record["value"]}
                    applied.append(lsn)
            recovery = {"scanned": scanned, "applied": applied,
                        "lost_acknowledged": sorted(tx for tx in acknowledged if commits[tx] > durable)}
            result = "recovered"
        output.append(snapshot(result, recovery))
    return output
