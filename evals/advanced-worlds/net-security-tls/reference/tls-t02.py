"""Terminal recovery gate for a real ECH offer, not a TLS implementation.

The caller supplies completed protocol and identity validation results. Identity
means the private origin when ECH is accepted and ECHConfig.public_name otherwise.
Inputs describe valid combinations: acceptance uses TLS 1.3 and no retry_configs;
an older, locally permitted TLS version means rejection and no retry_configs.
Retry actions always require a fresh transport connection. They do not authorize
DIRECT-origin fallback or continue the rejected outer connection.
"""


def ech_recovery(ech_accepted, negotiated_tls13, handshake_ok, identity_ok,
                 retry_configs="absent", allow_non_ech_retry=False):
    """Return original_success, send_application, and a terminal action.

    retry_configs is absent, unsupported, supported, or malformed. Supported
    means a syntactically valid, usable configuration with a supported version;
    unsupported means no supported version. A supported version with unusable
    parameters is outside this bounded contract, not classified as unsupported.
    handshake_ok covers base TLS protocol/Finished checks; retry syntax and
    service identity are separate supplied facts. All flags are booleans.
    """
    action = "fail"
    if not handshake_ok or not identity_ok:
        return {"original_success": False, "send_application": False,
                "action": action}
    if ech_accepted:
        return {"original_success": True, "send_application": True,
                "action": "complete"}
    if retry_configs == "malformed":
        return {"original_success": False, "send_application": False,
                "action": action}
    if negotiated_tls13 and retry_configs == "supported":
        action = "retry-ech"
    elif allow_non_ech_retry:
        action = "retry-without-ech"
    return {"original_success": False, "send_application": False,
            "action": action}
