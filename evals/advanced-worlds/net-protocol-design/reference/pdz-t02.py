def assemble_binary(frames, frame_cap, message_cap):
    """Assemble the task's decoded RFC 6455 binary-frame profile."""
    result = {"messages": [], "pongs": [], "pending": None,
              "close_received": False, "error": None}
    pending = None

    def fail(code):
        result["pending"] = None
        result["error"] = code
        return result

    for frame in frames:
        opcode, fin = frame["opcode"], frame["fin"]
        payload = bytes.fromhex(frame["payload"])
        if len(payload) > frame_cap:
            return fail("frame_too_large")
        if opcode in (8, 9, 10):
            if not fin or len(payload) > 125:
                return fail("invalid_control")
            if opcode == 8:
                result["close_received"] = True
                result["pending"] = None
                return result
            if opcode == 9:
                result["pongs"].append(payload.hex())
            continue
        if opcode == 2:
            if pending is not None:
                return fail("unexpected_binary")
            assembled = payload
        else:
            if pending is None:
                return fail("unexpected_continuation")
            assembled = pending + payload
        if len(assembled) > message_cap:
            return fail("message_too_large")
        if fin:
            result["messages"].append(assembled.hex())
            pending = None
        else:
            pending = assembled
    result["pending"] = None if pending is None else pending.hex()
    return result
