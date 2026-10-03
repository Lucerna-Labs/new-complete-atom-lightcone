"""Pitfall: every Task receives cancellation even after a child absorbs it."""


def cancellation_chain(tasks, requests):
    states = []
    cancellation = requests > 0
    returned_value = None
    for task in reversed(tasks):
        received = requests > 0
        if requests == 0:
            state = "pending"
        elif received and not task["suppress"]:
            state = "cancelled"
            returned_value = None
        else:
            if received:
                returned_value = task["value"]
            state = "returned"
            cancellation = False
        states.append({"id": task["id"], "state": state,
                       "cancelling": requests, "received_cancel": received,
                       "value": returned_value})
    return {"cancel_results": [True] * requests,
            "leaf_future_cancelled": requests > 0,
            "tasks": list(reversed(states))}
