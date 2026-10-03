import base64
import json
import pathlib
import subprocess
import sys


# Public synthetic inputs and literal known answers, independently produced
# with OpenSSL 3.0.13 HKDF EXPAND_ONLY / SHA256 during authoring.
# The fixed RFC9846 HkdfLabel bytes were independently decoded and checked:
# 0020 (output length), 11 (label length), ASCII 'tls13 traffic upd', 00 (empty context).
# OpenSSL is NOT used by this checker. No real TLS secrets are involved.
VECTORS = [
    ("0000000000000000000000000000000000000000000000000000000000000000", [
        "6332e2593a296a14c6899a806d3cb01f8565c17a5002e5ab4bcd2e79a6811b84",
        "5f17c07b1d2651785983ebf8803c5c643723644a21a7c364ef3c4780f84b6992",
        "a356bee02e86e62afd27023b752a124e0cec73bc86b8958f041c8bf51390ff53",
        "5c910b32ba0f3f715b164e060c16ee486da1925589eb0f290196f2d14e0caaa7",
    ]),
    ("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f", [
        "2cecd0a17506ef5fa73edc062d6e7b5397cf074ec1b4d8f99a120772932f0b45",
        "2d3fb1fe267c2e0126351cc169afb7ca25c0d8867167c55c5533e3715558a6b9",
        "103ec32e011e34d2aed3160d621f7430ec6c0722b0fff9a4da1ce4f8e004f71f",
        "e294e935757d937b68abc3642d7e0f5b26eff9ccc6c9bcf7ebc12a34fc4ef3dd",
    ]),
    ("ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", [
        "7a49d66580d757748a54c1a08b6c60e5020d15359c04eb88a6862bd15d4adc48",
        "698dc62c9074083bb8854d8e659f52ebbc909e7fa60d6f726e26624c4345da19",
        "18b8a68983b0e364e55312143d70ead8543530fd72fa4279855f91024c5673a3",
        "964649ed89d853cb5ae4effc7d5585f07cd5d19af4b6e2e386f690b0cf44ad0a",
    ]),
    ("a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5a5", [
        "b93ffb48789d070ef694e573d322979ecc2395702e86fba6fe4399a81736adde",
        "fb2ef37e1d8c4b1720b0398ad7a2567be67dfea9189c9472d397db9bb6e9a13f",
        "32f0e3c45d7c8b76b528a41b4c7a9e7686963ea6b74c60e28fe4996d521501e7",
        "6a42b8915dc5a0182ad35879c98d7148a84922bf4e7819b239959289773281cc",
    ]),
    ("1f1e1d1c1b1a191817161514131211100f0e0d0c0b0a09080706050403020100", [
        "5f23cc44bf4f75dd97667d65ae919d7baf7bfd243ea594711b23aa6cb46631df",
        "7827565d1f5684f23c643ba7eaed5ea504b221543be26de63ca75b7ee7f7dccd",
        "1244ed0b0c4cea9a40acb7d7f08cc4e954c5eae23185984365433972ca464bde",
        "cc4112bf870499c8969ee810b440aa9d0281ba27700d6466fdb0f8d48ffc4222",
    ]),
]
CASES = [(seed, count, outputs[:count])
         for seed, outputs in VECTORS for count in range(5)]
CASES += [(seed.upper(), 4, outputs) for seed, outputs in VECTORS]
CASES += [(outputs[0], 2, outputs[1:3]) for _, outputs in VECTORS]
CASES.append((VECTORS[0][0], 4, VECTORS[0][1]))
EXPECTED = {"values": [c[2] for c in CASES], "lists_of_strings": True}


def run(candidate):
    payload = base64.b64encode(json.dumps(CASES).encode()).decode()
    runner = r'''import base64,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
cases=json.loads(base64.b64decode(sys.argv[2]))
values=[module.traffic_updates(secret,count) for secret,count,_ in cases]
types=all(type(x) is list and all(type(y) is str for y in x) for x in values)
print("__RESULT__"+json.dumps({"values":values,"lists_of_strings":types}))'''
    try:
        result = subprocess.run([sys.executable, "-B", "-c", runner,
                                 str(pathlib.Path(candidate).resolve()), payload],
                                capture_output=True, text=True, timeout=5)
        lines = [line[len("__RESULT__"):] for line in result.stdout.splitlines()
                 if line.startswith("__RESULT__")]
        return json.loads(lines[-1]) if result.returncode == 0 and lines else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


if __name__ == "__main__":
    sys.exit(0 if len(sys.argv) == 2 and run(sys.argv[1]) == EXPECTED else 1)
