"""Least fixed-point priority donation for independent mathematical snapshots."""


def priority_inheritance(snapshots):
    results = []
    for snapshot in snapshots:
        effective = dict(snapshot["base"])
        changed = True
        while changed:
            changed = False
            for waiter, lock in snapshot["waits"].items():
                owner = snapshot["owners"][lock]
                donated = effective[waiter]
                if donated > effective[owner]:
                    effective[owner] = donated
                    changed = True
        results.append(effective)
    return results
