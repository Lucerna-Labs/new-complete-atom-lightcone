"""Finite streamed OFDM/FIR model; values cross the API as [real, imag]."""

import cmath
import math


def ofdm_blocks(blocks, taps, cp_len):
    n = len(blocks[0])
    channel = [complex(*value) for value in taps]
    transmitted = []
    for block in blocks:
        frequencies = [complex(*value) for value in block]
        useful = [sum(frequencies[k] * cmath.exp(2j * math.pi * k * t / n)
                      for k in range(n)) / n for t in range(n)]
        transmitted.extend(useful[-cp_len:] if cp_len else [])
        transmitted.extend(useful)
    received = [sum(tap * transmitted[t - lag]
                    for lag, tap in enumerate(channel) if t >= lag)
                for t in range(len(transmitted))]
    useful_blocks, frequency_blocks = [], []
    for index in range(len(blocks)):
        start = index * (n + cp_len) + cp_len
        useful = received[start:start + n]
        frequencies = [sum(useful[t] * cmath.exp(-2j * math.pi * k * t / n)
                           for t in range(n)) for k in range(n)]
        useful_blocks.append([[value.real, value.imag] for value in useful])
        frequency_blocks.append([[value.real, value.imag] for value in frequencies])
    gains = [sum(tap * cmath.exp(-2j * math.pi * k * lag / n)
                 for lag, tap in enumerate(channel)) for k in range(n)]
    return {"useful_samples": useful_blocks, "received_bins": frequency_blocks,
            "channel_bins": [[value.real, value.imag] for value in gains],
            "prefix_covers_memory": cp_len >= len(channel) - 1}
