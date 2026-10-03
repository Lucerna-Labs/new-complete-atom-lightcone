"""Covering payload eligibility and separate candidate visibility checks."""


def index_access(required_columns, index_columns, candidates, supports_index_only=True):
    eligible = supports_index_only and set(required_columns) <= set(index_columns)
    rows = []
    trace = []
    heap_checks = 0
    for candidate in candidates:
        check_heap = not eligible
        heap_checks += int(check_heap)
        visible = candidate["heap_visible"] if check_heap else True
        source = ("index" if eligible else "heap") if visible else None
        if visible:
            values = candidate["index_values"] if eligible else candidate["heap_values"]
            rows.append({"id": candidate["id"], "values": {key: values[key] for key in required_columns}})
        trace.append({"id": candidate["id"], "heap_checked": check_heap,
                      "visible": visible, "value_source": source})
    return {"strategy": "index-only" if eligible else "heap", "heap_checks": heap_checks,
            "rows": rows, "trace": trace}
