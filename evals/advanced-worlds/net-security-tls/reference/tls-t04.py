import hashlib
import hmac


def traffic_updates(secret_hex, generations):
    current = bytes.fromhex(secret_hex)
    label = b"tls13 " + b"traffic upd"
    context = b""
    info = (32).to_bytes(2, "big") + bytes([len(label)]) + label + bytes([len(context)]) + context
    values = []
    for _ in range(generations):
        # Hash.length is exactly one SHA-256 HKDF-Expand block.
        current = hmac.new(current, info + b"\x01", hashlib.sha256).digest()
        values.append(current.hex())
    return values
