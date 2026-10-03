"""Isolated write-segment access gate over a trusted registration map.

Tags and protection contexts are opaque. All offsets are valid unsigned 64-bit
integers; positive payloads and registered regions are at most 32 bytes. A
region's mathematical one-past-end may equal 2**64. This logical byte-copy model
does not execute NIC operations or infer completion, consumption, or durability.
Rejection preserves earlier placements and does not terminate later gate calls.
Each tag names an independent logical buffer, including when numeric per-tag
offset ranges overlap; physical address aliases are not part of this model.
"""


def place_segments(regions, segments):
    memory = {tag: bytearray.fromhex(region["data"])
              for tag, region in regions.items()}
    events = []
    for segment in segments:
        tag = segment["tag"]
        payload = bytes.fromhex(segment["data"])
        region = regions.get(tag)
        written = 0
        if region is None:
            status = "unknown-tag"
        elif segment["context"] != region["context"]:
            status = "wrong-context"
        elif not region["write"]:
            status = "write-denied"
        else:
            start = segment["offset"] - region["base"]
            size = len(memory[tag])
            # Subtraction compares the entire range without fixed-width wrap.
            if start < 0 or start > size or len(payload) > size - start:
                status = "out-of-bounds"
            else:
                memory[tag][start:start + len(payload)] = payload
                written = len(payload)
                status = "placed"
        events.append({"tag": tag, "status": status, "written": written})
    return {"regions": {tag: data.hex() for tag, data in memory.items()},
            "events": events}
