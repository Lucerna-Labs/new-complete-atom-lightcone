import base64
import copy
import json
import pathlib
import subprocess
import sys


def reference(kind, value):
    return {"kind": kind, "value": value}


def certificate(dns=(), ips=(), cn=None):
    return {"dns_sans": list(dns), "ip_sans": list(ips), "common_name": cn}


# Only identity matching: these cases do not assert a chain is trusted.
# '*' alone, IDNA, Unicode, root-dot normalization, and public-suffix policy
# are outside the declared input/task scope.
BASE_CASES = [
    (reference("DNS", "api.example.test"), certificate(["api.example.test"]), True),
    (reference("DNS", "API.EXAMPLE.TEST"), certificate(["api.example.test"]), True),
    (reference("DNS", "api.example.test"), certificate(["API.EXAMPLE.TEST"]), True),
    (reference("DNS", "Api.ExAmPlE.TeSt"), certificate(["aPI.eXample.tEST"]), True),
    (reference("DNS", "api.example.test"), certificate(["other.example.test"]), False),
    (reference("DNS", "api.example.test"), certificate(["api.example.test.evil.test"]), False),
    (reference("DNS", "evilapi.example.test"), certificate(["api.example.test"]), False),
    (reference("DNS", "api.notexample.test"), certificate(["*.example.test"]), False),
    (reference("DNS", "api.example.test"), certificate(["*.example.test"]), True),
    (reference("DNS", "example.test"), certificate(["*.example.test"]), False),
    (reference("DNS", "a.b.example.test"), certificate(["*.example.test"]), False),
    (reference("DNS", "API.EXAMPLE.TEST"), certificate(["*.ExAmPlE.TeSt"]), True),
    (reference("DNS", "api.example.test"), certificate(["a*.example.test"]), False),
    (reference("DNS", "api.example.test"), certificate(["*pi.example.test"]), False),
    (reference("DNS", "api.example.test"), certificate(["api.*.test"]), False),
    (reference("DNS", "api.example.test"), certificate(["*.*.test"]), False),
    (reference("DNS", "api.example.test"), certificate(["**.example.test"]), False),
    (reference("DNS", "api.test"), certificate(["*.test"]), True),
    (reference("DNS", "api.example.test"), certificate(cn="api.example.test"), False),
    (reference("DNS", "api.example.test"), certificate(["other.example.test"], cn="api.example.test"), False),
    (reference("DNS", "api.example.test"), certificate(["api.example.test"], cn="other.example.test"), True),
    (reference("DNS", "api.example.test"), certificate(["other.example.test", "api.example.test"]), True),
    (reference("DNS", "api.example.test"), certificate(["a*.example.test", "*.example.test"]), True),
    (reference("DNS", "api.example.test"), certificate(), False),
    (reference("DNS", "api.example.test"), certificate(ips=["192.0.2.8"]), False),
    (reference("IP", "192.0.2.8"), certificate(ips=["192.0.2.8"]), True),
    (reference("IP", "192.0.2.8"), certificate(ips=["192.0.2.9"]), False),
    (reference("IP", "192.0.2.8"), certificate(dns=["192.0.2.8"]), False),
    (reference("IP", "192.0.2.8"), certificate(cn="192.0.2.8"), False),
    (reference("IP", "192.0.2.8"), certificate(dns=["*.0.2.8"]), False),
    (reference("IP", "2001:db8::1"), certificate(ips=["2001:0db8:0:0:0:0:0:1"]), True),
    (reference("IP", "2001:DB8:ABCD::1"), certificate(ips=["2001:db8:abcd:0:0:0:0:1"]), True),
    (reference("IP", "2001:db8::1"), certificate(ips=["2001:db8::2"]), False),
    (reference("IP", "192.0.2.8"), certificate(ips=["::ffff:192.0.2.8"]), False),
    (reference("IP", "::ffff:192.0.2.8"), certificate(ips=["::ffff:c000:208"]), True),
    (reference("IP", "::ffff:192.0.2.8"), certificate(ips=["192.0.2.8"]), False),
    (reference("IP", "2001:db8::1"), certificate(dns=["api.example.test"], ips=["2001:db8::2", "2001:db8::1"]), True),
    (reference("IP", "192.0.2.8"), certificate(dns=["wrong.example.test"], ips=["192.0.2.8"], cn="wrong.example.test"), True),
]
CASES = list(BASE_CASES)
for identity, cert, value in BASE_CASES:
    if len(cert["dns_sans"]) > 1 or len(cert["ip_sans"]) > 1:
        reversed_cert = {**cert, "dns_sans": list(reversed(cert["dns_sans"])),
                         "ip_sans": list(reversed(cert["ip_sans"]))}
        CASES.append((identity, reversed_cert, value))
CASES.append(BASE_CASES[0])
EXPECTED = {"values": [c[2] for c in CASES], "booleans": True, "unchanged": True}


def run(candidate):
    payload = base64.b64encode(json.dumps(CASES).encode()).decode()
    runner = r'''import base64,copy,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1])
module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
cases=json.loads(base64.b64decode(sys.argv[2]));values=[];unchanged=True
for identity,certificate,_ in cases:
    a,b=copy.deepcopy(identity),copy.deepcopy(certificate)
    values.append(module.service_identity(a,b))
    unchanged=unchanged and a==identity and b==certificate
print("__RESULT__"+json.dumps({"values":values,"booleans":all(type(x) is bool for x in values),"unchanged":unchanged}))'''
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
