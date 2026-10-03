def deficit_visit(deficit, quantum, packet_bytes):
    """One visit in the task's strictly nonzero precheck profile."""
    if deficit < 0:
        return {"action": "rotate", "deficit": deficit + quantum,
                "sent_bytes": 0, "move_old": True}
    return {"action": "send", "deficit": deficit - packet_bytes,
            "sent_bytes": packet_bytes, "move_old": False}
