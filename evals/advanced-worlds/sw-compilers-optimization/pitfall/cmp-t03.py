"""Declared guarded wrapping-u32 loop model; no real SIMD execution."""


def guarded_vector_add(memory, dst, src, count, width=4):
    data = list(memory)
    disjoint = True
    groups = []
    scalar = []
    limit = (count // width) * width if disjoint else 0
    for first in range(0, limit, width):
        indices = list(range(first, first + width))
        inputs = [data[src + i] for i in indices]
        outputs = [(value + 1) % (2**32) for value in inputs]
        for i, value in zip(indices, outputs):
            data[dst + i] = value
        groups.append({"indices": indices, "inputs": inputs, "outputs": outputs})
    for i in range(limit, count):
        value = data[src + i]
        result = (value + 1) % (2**32)
        data[dst + i] = result
        scalar.append({"index": i, "input": value, "output": result})
    return {"path": "vector" if disjoint else "scalar", "memory": data,
            "vector_groups": groups, "scalar_steps": scalar,
            "tail_count": count % width if disjoint else 0}
