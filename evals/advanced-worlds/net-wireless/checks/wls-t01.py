import base64
import json
import math
import pathlib
import subprocess
import sys


def run(candidate):
    calls = [["radio_metrics", args] for args in RADIO] + [["ofdm_airtime", args] for args in OFDM]
    calls += [calls[-1], calls[0], calls[len(RADIO)-1]]
    payload = base64.b64encode(json.dumps(calls).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1]);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
values=[];unchanged=True
for name,args in json.loads(base64.b64decode(sys.argv[2])):
    supplied=copy.deepcopy(args);before=json.dumps(supplied,sort_keys=True)
    values.append(getattr(m,name)(*supplied));unchanged=unchanged and json.dumps(supplied,sort_keys=True)==before
print("__RESULT__"+json.dumps({"values":values,"unchanged":unchanged}))'''
    try:
        result = subprocess.run([sys.executable,"-B","-c",runner,str(pathlib.Path(candidate).resolve()),payload],
                                capture_output=True,text=True,timeout=5)
        lines = [s[len("__RESULT__"):] for s in result.stdout.splitlines() if s.startswith("__RESULT__")]
        return json.loads(lines[-1]) if result.returncode == 0 and lines else None
    except (OSError,subprocess.TimeoutExpired,ValueError):
        return None


def same_report(actual, expected):
    if type(actual) is not dict or set(actual) != set(expected):
        return False
    for key, value in expected.items():
        a = actual[key]
        if key == "symbols":
            if type(a) is not int or a != value:
                return False
        else:
            absolute = 1e-10 if key in ("snr_db","sinr_db") else 1e-300
            if type(a) not in (int,float) or not math.isfinite(a) or not math.isclose(a,value,rel_tol=1e-10,abs_tol=absolute):
                return False
    return True


def passes(result):
    expected = EXPECTED_RADIO + EXPECTED_OFDM + [EXPECTED_OFDM[-1],EXPECTED_RADIO[0],EXPECTED_RADIO[-1]]
    return (type(result) is dict and set(result) == {"values","unchanged"}
            and result["unchanged"] is True and type(result["values"]) is list
            and len(result["values"]) == len(expected)
            and all(same_report(a,e) for a,e in zip(result["values"],expected)))

# Literal oracles calculated independently with 100-digit Decimal arithmetic.
# No oracle formulas run in this checker. Inputs outside the stated domain are
# not tested; numeric output types and tiny nonzero values are checked strictly.
RADIO = [(1000000, 0, 1e-09, []),
 (1000000, -30, 1e-12, [-30, -30]),
 (1, -150, 1e-09, []),
 (1000, -60, 1e-12, []),
 (2000, -60, 1e-12, []),
 (10000, 10, 1e-13, [-20, -20, -20, -20, -20, -20, -20, -20]),
 (1000000000, -150, 1e-09, []),
 (1000000000, -30, 1e-24, [-150]),
 (500000, -40, 1e-15, [-30, -60]),
 (1, -149, 1e-24, [-149]),
 (1000000000, 40, 1e-24, [40, 40, 40, 40, 40, 40, 40, 40]),
 (1, 40, 1e-24, []),
 (1000, -60.5, 1e-12, [-60.25]),
 (1000.5, -60, 1e-12, [])]
EXPECTED_RADIO = [{'signal_watts': 0.001,
  'noise_watts': 0.001,
  'interference_watts': 0.0,
  'snr_linear': 1.0,
  'snr_db': 0.0,
  'sinr_linear': 1.0,
  'sinr_db': 0.0,
  'awgn_capacity_bps': 1000000.0},
 {'signal_watts': 1e-06,
  'noise_watts': 1e-06,
  'interference_watts': 2e-06,
  'snr_linear': 1.0,
  'snr_db': 0.0,
  'sinr_linear': 0.3333333333333333,
  'sinr_db': -4.771212547196624,
  'awgn_capacity_bps': 1000000.0},
 {'signal_watts': 1e-18,
  'noise_watts': 1e-09,
  'interference_watts': 0.0,
  'snr_linear': 1e-09,
  'snr_db': -90.0,
  'sinr_linear': 1e-09,
  'sinr_db': -90.0,
  'awgn_capacity_bps': 1.442695040167616e-09},
 {'signal_watts': 1e-09,
  'noise_watts': 1e-09,
  'interference_watts': 0.0,
  'snr_linear': 1.0,
  'snr_db': 0.0,
  'sinr_linear': 1.0,
  'sinr_db': 0.0,
  'awgn_capacity_bps': 1000.0},
 {'signal_watts': 1e-09,
  'noise_watts': 2e-09,
  'interference_watts': 0.0,
  'snr_linear': 0.5,
  'snr_db': -3.010299956639812,
  'sinr_linear': 0.5,
  'sinr_db': -3.010299956639812,
  'awgn_capacity_bps': 1169.9250014423124},
 {'signal_watts': 0.01,
  'noise_watts': 1e-09,
  'interference_watts': 8e-05,
  'snr_linear': 10000000.0,
  'snr_db': 70.0,
  'sinr_linear': 124.99843751953101,
  'sinr_db': 20.969045843609617,
  'awgn_capacity_bps': 232534.96808481033},
 {'signal_watts': 1e-18,
  'noise_watts': 1.0,
  'interference_watts': 0.0,
  'snr_linear': 1e-18,
  'snr_db': -180.0,
  'sinr_linear': 1e-18,
  'sinr_db': -180.0,
  'awgn_capacity_bps': 1.4426950408889634e-09},
 {'signal_watts': 1e-06,
  'noise_watts': 1e-15,
  'interference_watts': 1e-18,
  'snr_linear': 1000000000.0,
  'snr_db': 90.0,
  'sinr_linear': 999000999.000999,
  'sinr_db': 89.99565922520681,
  'awgn_capacity_bps': 29897352855.428955},
 {'signal_watts': 1e-07,
  'noise_watts': 5e-10,
  'interference_watts': 1.001e-06,
  'snr_linear': 200.0,
  'snr_db': 23.010299956639813,
  'sinr_linear': 0.09985022466300549,
  'sinr_db': -10.006509536295951,
  'awgn_capacity_bps': 3825525.8455894645},
 {'signal_watts': 1.2589254117941673e-18,
  'noise_watts': 1e-24,
  'interference_watts': 1.2589254117941673e-18,
  'snr_linear': 1258925.4117941672,
  'snr_db': 61.0,
  'sinr_linear': 0.9999992056723962,
  'sinr_db': -3.4497223215013247e-06,
  'awgn_capacity_bps': 20.26376252478586},
 {'signal_watts': 10.0,
  'noise_watts': 1e-15,
  'interference_watts': 80.0,
  'snr_linear': 1e+16,
  'snr_db': 160.0,
  'sinr_linear': 0.125,
  'sinr_db': -9.030899869919436,
  'awgn_capacity_bps': 53150849518.1978},
 {'signal_watts': 10.0,
  'noise_watts': 1e-24,
  'interference_watts': 0.0,
  'snr_linear': 1e+25,
  'snr_db': 250.0,
  'sinr_linear': 1e+25,
  'sinr_db': 250.0,
  'awgn_capacity_bps': 83.04820237218406},
 {'signal_watts': 8.912509381337456e-10,
  'noise_watts': 1e-09,
  'interference_watts': 9.440608762859234e-10,
  'snr_linear': 0.8912509381337456,
  'snr_db': -0.5,
  'sinr_linear': 0.45844806045192205,
  'sinr_db': -3.387098602924717,
  'awgn_capacity_bps': 919.3407980748303},
 {'signal_watts': 1e-09,
  'noise_watts': 1.0005e-09,
  'interference_watts': 0.0,
  'snr_linear': 0.9995002498750625,
  'snr_db': -0.002170929722302083,
  'sinr_linear': 0.9995002498750625,
  'sinr_db': -0.002170929722302083,
  'awgn_capacity_bps': 1000.1392811705806}]
OFDM = [(0, 96, 4.0, 20.0),
 (1, 96, 4.0, 20.0),
 (96, 96, 4.0, 20.0),
 (97, 96, 4.0, 20.0),
 (200, 192, 4.0, 20.0),
 (50, 192, 0.001, 0.0),
 (1000000, 1000000, 1000.0, 1000000.0),
 (1000000, 1, 0.001, 0),
 (0, 1, 0.001, 0),
 (999999, 1000000, 1000, 0),
 (0, 96, 4, 20.5)]
EXPECTED_OFDM = [{'symbols': 0, 'airtime_us': 20.0, 'nominal_rate_bps': 24000000.0},
 {'symbols': 1, 'airtime_us': 24.0, 'nominal_rate_bps': 24000000.0},
 {'symbols': 1, 'airtime_us': 24.0, 'nominal_rate_bps': 24000000.0},
 {'symbols': 2, 'airtime_us': 28.0, 'nominal_rate_bps': 24000000.0},
 {'symbols': 2, 'airtime_us': 28.0, 'nominal_rate_bps': 48000000.0},
 {'symbols': 1, 'airtime_us': 0.001, 'nominal_rate_bps': 192000000000.0},
 {'symbols': 1, 'airtime_us': 1001000.0, 'nominal_rate_bps': 1000000000.0},
 {'symbols': 1000000, 'airtime_us': 1000.0, 'nominal_rate_bps': 1000000000.0},
 {'symbols': 0, 'airtime_us': 0.0, 'nominal_rate_bps': 1000000000.0},
 {'symbols': 1, 'airtime_us': 1000.0, 'nominal_rate_bps': 1000000000.0},
 {'symbols': 0, 'airtime_us': 20.5, 'nominal_rate_bps': 24000000.0}]


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and passes(run(sys.argv[1])) else 1)
