"""Pitfall: obsolete same-thread plain-store release-sequence continuation."""


def synchronization_witness(events, modification_orders):
    by_id = {event["id"]: event for event in events}
    positions = {event["id"]: index for index, event in enumerate(events)}
    acquire_orders = {"acquire", "acq_rel", "seq_cst"}
    release_orders = {"release", "acq_rel", "seq_cst"}
    modifications = [event for event in events if event["kind"] in ("store", "rmw")]
    reads = [event for event in events if event["kind"] in ("load", "rmw", "cas_fail")]
    fences = [event for event in events if event["kind"] == "fence"]

    def before(left, right):
        return (left["thread"] == right["thread"]
                and positions[left["id"]] < positions[right["id"]])

    # Every modification can be a hypothetical fence-carrier release head.
    continuations = {}
    for order in modification_orders.values():
        for index, identifier in enumerate(order):
            members = [identifier]
            for following in order[index + 1:]:
                if (by_id[following]["kind"] != "rmw"
                        and by_id[following]["thread"] != by_id[identifier]["thread"]):
                    break
                members.append(following)
            continuations[identifier] = members
    sequences = {event["id"]: continuations[event["id"]]
                 for event in modifications if event["order"] in release_orders}
    pairs = set()

    def emit(left, right):
        if left["thread"] != right["thread"]:
            pairs.add((left["id"], right["id"]))

    for head, members in sequences.items():
        source = by_id[head]
        for read in reads:
            if read["reads_from"] not in members:
                continue
            if read["order"] in acquire_orders:
                emit(source, read)
            for fence in fences:
                if fence["order"] in acquire_orders and before(read, fence):
                    emit(source, fence)

    for release in fences:
        if release["order"] not in release_orders:
            continue
        for carrier in modifications:
            if not before(release, carrier):
                continue
            for read in reads:
                if read["reads_from"] not in continuations[carrier["id"]]:
                    continue
                if read["order"] in acquire_orders:
                    emit(release, read)
                for acquire in fences:
                    if acquire["order"] in acquire_orders and before(read, acquire):
                        emit(release, acquire)
    return {"release_sequences": sequences,
            "synchronizes_with": [list(pair) for pair in sorted(pairs)]}
