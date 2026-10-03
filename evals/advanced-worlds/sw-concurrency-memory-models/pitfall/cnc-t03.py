"""Reduce current outstanding requests in the declared closed resource model."""


def reduce_resources(available, processes):
    work = list(available)
    pending = {p["id"]: p for p in processes}
    order = []
    while True:
        eligible = [pid for pid in sorted(pending)
                    if all(need <= have for need, have in
                           zip(pending[pid]["request"], work))]
        if not eligible:
            break
        pid = eligible[0]
        process = pending.pop(pid)
        # Granting and then releasing the request cancel; the prior allocation
        # is the additional capacity returned by completion.
        work = [have + held for have, held in
                zip(work, process["request"])]
        order.append(pid)
    blocked = sorted(pending)
    return {"order": order, "work": work, "blocked": blocked,
            "deficits": {pid: [max(need - have, 0) for need, have in
                                zip(pending[pid]["request"], work)]
                         for pid in blocked}}
