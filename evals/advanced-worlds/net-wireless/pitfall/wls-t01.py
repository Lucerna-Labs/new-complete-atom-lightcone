import math


def _watts(dbm):
    return 10.0 ** ((dbm - 30.0) / 10.0)


def radio_metrics(bandwidth_hz, signal_dbm, noise_density_w_hz, interferers_dbm):
    signal = _watts(signal_dbm)
    noise = noise_density_w_hz * bandwidth_hz
    interference = _watts(sum(interferers_dbm)) if interferers_dbm else 0.0
    snr = signal / noise
    sinr = signal / (noise + interference)
    return {"signal_watts": signal, "noise_watts": noise,
            "interference_watts": interference, "snr_linear": snr,
            "snr_db": 10.0 * math.log10(snr), "sinr_linear": sinr,
            "sinr_db": 10.0 * math.log10(sinr),
            "awgn_capacity_bps": bandwidth_hz * math.log1p(snr) / math.log(2.0)}


def ofdm_airtime(bit_count, bits_per_symbol, symbol_us, fixed_us):
    symbols = (bit_count + bits_per_symbol - 1) // bits_per_symbol
    return {"symbols": symbols, "airtime_us": symbols * symbol_us + fixed_us,
            "nominal_rate_bps": bits_per_symbol / (symbol_us * 1e-6)}
