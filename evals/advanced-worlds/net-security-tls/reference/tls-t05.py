"""Chosen state-only return-packet policy over supplied validated flow records.

State creation, refresh, packet parsing, and TLS identity are outside this model.
Times are abstract nonnegative integer ticks; entries are live strictly before
expires_at. Endpoints are [canonical IPv4 address, valid port] lists. Records and
packets carry a firewall instance and protocol (tcp or udp). The packet's ACK bit
is untrusted; transition_ok is the caller's independent protocol-state result.
No independently permitted new-flow or stateless admission rule is modeled.
"""


def firewall_return_gate(packet, states, now, return_rule=True, deny_rule=False):
    """Decide one return packet without creating, refreshing, or changing state.

    Each state has instance, protocol, src, dst, and expires_at. A packet has
    instance, protocol, src, dst, ack, and transition_ok; ack is False for UDP.
    Rule flags and packet flags are booleans. A deny rule overrides all state.
    """
    if deny_rule:
        return {"admit": False, "reason": "deny-rule"}
    if not return_rule:
        return {"admit": False, "reason": "return-rule-disabled"}
    matching = any(
        state["instance"] == packet["instance"]
        and state["protocol"] == packet["protocol"]
        and state["src"] == packet["dst"]
        and state["dst"] == packet["src"]
        and now < state["expires_at"]
        for state in states
    )
    if not matching:
        return {"admit": False, "reason": "no-live-reverse-state"}
    if not packet["transition_ok"]:
        return {"admit": False, "reason": "bad-transition"}
    return {"admit": True, "reason": "state"}
