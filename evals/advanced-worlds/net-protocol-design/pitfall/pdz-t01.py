# Semantic pitfall: count the last-fragment flag as part of the length.
def decode_rpc_chunks(chunks, max_fragment=16, max_record=32, eof=True):
    buffer = b""
    assembly = bytearray()
    expected = None
    last = False
    active = False
    records = []

    def failed(reason):
        return {"records": records, "pending": False, "error": reason}

    for chunk in chunks:
        buffer += bytes.fromhex(chunk)
        while True:
            if expected is None:
                if len(buffer) < 4:
                    break
                marker = int.from_bytes(buffer[:4], "big")
                buffer = buffer[4:]
                length = marker
                last = bool(marker & 0x80000000)
                if length > max_fragment:
                    return failed("fragment-limit")
                if len(assembly) + length > max_record:
                    return failed("record-limit")
                expected = length
                active = True
            if len(buffer) < expected:
                break
            assembly.extend(buffer[:expected])
            buffer = buffer[expected:]
            expected = None
            if last:
                records.append(assembly.hex())
                assembly.clear()
                active = False
    incomplete = bool(buffer) or expected is not None or active
    if eof and incomplete:
        return failed("truncated")
    return {"records":records,"pending":bool(incomplete),"error":None}
