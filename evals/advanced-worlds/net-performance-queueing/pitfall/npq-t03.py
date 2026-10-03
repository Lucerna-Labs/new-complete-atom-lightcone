def deficit_visit(deficit, quantum, packet_bytes):
    """Pitfall: replenishment erases existing debt instead of adding credit."""
    if deficit < 0:
        return {"action": "rotate", "deficit": quantum,
                "sent_bytes": 0, "move_old": True}
    return {"action": "send", "deficit": deficit - packet_bytes,
            "sent_bytes": packet_bytes, "move_old": False}
