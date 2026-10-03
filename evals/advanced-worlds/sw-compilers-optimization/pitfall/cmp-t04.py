"""Pure checkpoint reconstruction and suffix execution in a symbolic source VM."""

from copy import deepcopy


def deopt_trace(machine, metadata, program, committed):
    def decode(recipe):
        kind = recipe["kind"]
        if kind == "constant":
            return recipe["value"]
        if kind == "add":
            return decode(recipe["left"]) + decode(recipe["right"])
        if kind == "register":
            word = machine["registers"][recipe["name"]]
        else:
            word = machine["stack"][recipe["slot"]]
        if recipe["format"] == "i32" and word >= 2**31:
            return word - 2**32
        return word

    local_values = {name: decode(recipe) for name, recipe in metadata["locals"].items()}
    effects = deepcopy(committed)
    pc = 0
    trace = []

    def snapshot():
        return {"pc": pc, "locals": dict(local_values), "effects": deepcopy(effects)}

    trace.append(snapshot())
    while pc < len(program):
        instruction = program[pc]
        if instruction["op"] == "add":
            local_values[instruction["local"]] += instruction["delta"]
        else:
            effects.append({"label": instruction["label"],
                            "value": local_values[instruction["local"]]})
        pc += 1
        trace.append(snapshot())
    return trace
