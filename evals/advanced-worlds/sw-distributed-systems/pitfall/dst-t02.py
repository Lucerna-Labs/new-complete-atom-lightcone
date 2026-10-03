"""Validated fixed-membership, single-decree Paxos phase-one selection."""


def choose_proposal(members, ballot, preferred, reports):
    def name(value):
        return type(value) is str and 1 <= len(value) <= 32

    def integer(value):
        return type(value) is int and value > 0

    def shape(value, keys):
        return type(value) is dict and all(type(k) is str for k in value) and set(value) == keys

    if type(members) is not list or not 1 <= len(members) <= 15:
        raise ValueError("members")
    if not all(name(member) for member in members) or len(set(members)) != len(members):
        raise ValueError("member identities")
    if not integer(ballot) or not name(preferred):
        raise ValueError("proposal")
    if type(reports) is not list or len(reports) > 128:
        raise ValueError("reports")
    matching = {}
    values_by_ballot = {}
    for report in reports:
        if not shape(report, {"acceptor", "prepare_ballot", "accepted"}):
            raise ValueError("report schema")
        acceptor = report["acceptor"]
        preparation = report["prepare_ballot"]
        accepted = report["accepted"]
        if not name(acceptor) or acceptor not in members or not integer(preparation):
            raise ValueError("report identity")
        if accepted is not None:
            if not shape(accepted, {"ballot", "value"}):
                raise ValueError("accepted schema")
            if not integer(accepted["ballot"]) or accepted["ballot"] >= preparation or not name(accepted["value"]):
                raise ValueError("accepted proposal")
        if preparation != ballot:
            continue
        if acceptor in matching and matching[acceptor] != accepted:
            raise ValueError("contradictory acceptor reports")
        matching[acceptor] = accepted
        if accepted is not None:
            number, value = accepted["ballot"], accepted["value"]
            if number in values_by_ballot and values_by_ballot[number] != value:
                raise ValueError("one value per ballot")
            values_by_ballot[number] = value
    responders = sorted(matching)
    ready = len(responders) >= len(members) // 2 + 1
    source_ballot = None
    value = None
    if ready:
        accepted = [(record["ballot"], record["value"]) for record in matching.values() if record is not None]
        if accepted:
            source_ballot, value = max(accepted, key=lambda pair: (sum(v == pair[1] for _, v in accepted), pair[0]))
        else:
            value = preferred
    return {"ready": ready, "responders": responders, "source_ballot": source_ballot, "value": value}
