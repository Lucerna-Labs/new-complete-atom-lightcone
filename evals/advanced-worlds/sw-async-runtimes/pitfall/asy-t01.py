"""Naive scheduler gives tasks a turn after each microtask."""
from collections import deque


def run_loop(jobs, initial_tasks, budget):
    tasks = deque(initial_tasks)
    microtasks = deque()
    trace = []
    log = []
    while len(trace) < budget and (tasks or microtasks):
        kind = "micro" if microtasks and (not tasks or not trace or trace[-1][0] != "micro") else "task"
        queue = microtasks if kind == "micro" else tasks
        job = queue.popleft()
        trace.append([kind, job])
        for op, arg in jobs[job]:
            if op == "emit":
                log.append(arg)
            elif op == "micro":
                microtasks.append(arg)
            else:
                tasks.append(arg)
    return {"trace": trace, "log": log, "tasks": list(tasks),
            "microtasks": list(microtasks),
            "status": "idle" if not tasks and not microtasks else "budget"}
