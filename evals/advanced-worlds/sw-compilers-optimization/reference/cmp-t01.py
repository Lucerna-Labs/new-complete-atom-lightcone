"""Tagged scalar value rules; supplied freeze choices are explicit witnesses."""


def scalar_ir(program, choices):
    values = {}
    branch = None
    ub = False

    def record(bits, kind, value=None):
        return {"bits": bits, "kind": kind, "value": value}

    for instruction in program:
        op = instruction["op"]
        if op == "literal":
            result = record(instruction["bits"], instruction["kind"], instruction["value"])
        elif op in ("add", "eq"):
            left, right = values[instruction["lhs"]], values[instruction["rhs"]]
            bits = left["bits"]
            out_bits = bits if op == "add" else 1
            if left["kind"] == "poison" or right["kind"] == "poison":
                result = record(out_bits, "poison")
            elif op == "eq":
                result = record(1, "value", int(left["value"] == right["value"]))
            else:
                modulus = 1 << bits
                sign = modulus >> 1
                a = left["value"] if left["value"] < sign else left["value"] - modulus
                b = right["value"] if right["value"] < sign else right["value"] - modulus
                overflow = instruction["nsw"] and not -sign <= a + b < sign
                result = (record(bits, "poison") if overflow else
                          record(bits, "value", (left["value"] + right["value"]) % modulus))
        elif op == "select":
            condition = values[instruction["cond"]]
            yes, no = values[instruction["yes"]], values[instruction["no"]]
            result = (record(yes["bits"], "poison") if condition["kind"] == "poison"
                      else dict(yes if condition["value"] else no))
        elif op == "freeze":
            operand = values[instruction["value"]]
            result = (dict(operand) if operand["kind"] == "value" else
                      record(operand["bits"], "value", choices[instruction["id"]]))
        else:
            condition = values[instruction["condition"]]
            ub = condition["kind"] != "value"
            branch = None if ub else bool(condition["value"])
            continue
        values[instruction["id"]] = result
    return {"values": values, "branch": branch, "ub": ub}
