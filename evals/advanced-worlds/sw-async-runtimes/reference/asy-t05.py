"""Canonical completion closure of a finite closed worker/dependency model."""


def pool_completion(capacity, running, queued, dependencies):
    active = set(running)
    waiting = list(queued)
    finished = set()
    started, completed = [], []
    while True:
        ready = sorted(job for job in active
                       if all(child in finished for child in dependencies[job]))
        if ready:
            job = ready[0]
            active.remove(job)
            finished.add(job)
            completed.append(job)
        elif waiting and len(active) < capacity:
            job = waiting.pop(0)
            active.add(job)
            started.append(job)
        else:
            break
    return {"started": started, "completed": completed,
            "running": sorted(active), "queued": waiting,
            "deadlocked": bool(active or waiting)}
