import base64
import json
import math
import pathlib
import subprocess
import sys

KEYS = ["utilization", "mean_system_count", "mean_queue_count",
        "mean_system_seconds", "mean_queue_seconds", "probability_zero_wait",
        "system_tail", "queue_tail", "system_percentile_seconds", "fanout_tail"]
# Literal oracles independently calculated with 70-digit Decimal arithmetic.
# Includes t=0's waiting atom, low/high utilization, unit scale, IID amplification,
# tiny nonzero tails, and ordinary IEEE underflow; no candidate-formula oracle.
CASES = [
    ([10,20,0,.5,1],[.5,1,.5,.1,.05,.5,1,.5,.06931471805599453,1]),
    ([10,20,.06931471805599453,.5,2],[.5,1,.5,.1,.05,.5,.5,.25,.06931471805599453,.75]),
    ([900,1000,.04605170185988091,.99,100],[.9,9,8.1,.01,.009,.1,.010000000000000004,.009000000000000003,.04605170185988092,.6339676587267706]),
    ([18,20,.5,.9,3],[.9,9,8.1,.5,.45,.1,.36787944117144233,.3310914970542981,1.151292546497023,.7474195421723528]),
    ([19,20,1,.999,10],[.95,19,18.05,1,.95,.05,.36787944117144233,.3494854691128702,6.907755278982137,.989814105967983]),
    ([.25,1,2,.75,4],[.25,.3333333333333333,.08333333333333333,1.3333333333333333,.3333333333333333,.75,.22313016014842982,.055782540037107455,1.8483924814931876,.6357554643628385]),
    ([1e-6,2e-6,1e6,1e-6,1000],[.5,1,.5,1e6,5e5,.5,.36787944117144233,.18393972058572117,1.0000005000003334,1]),
    ([999999,1000000,100,.999999,1000],[.999999,999999,999998.000001,1,.999999,1e-6,3.720075976020836e-44,3.72007225594486e-44,13.815510557964274,3.720075976020836e-41]),
    ([1,1000,1e-6,.01,1],[.001,.001001001001001001,1.001001001001001e-6,.001001001001001001,1.001001001001001e-6,.999,.9990014988343743,.0009990014988343744,1.0060396249751192e-5,.9990014988343743]),
    ([3,4,0,.8,12],[.75,3,2.25,1,.75,.25,1,.75,1.6094379124341003,1]),
    ([1,2,1000,.5,2],[.5,1,.5,1,.5,.5,0,0,.6931471805599453,0]),
    ([10,20,0,.5,1],[.5,1,.5,.1,.05,.5,1,.5,.06931471805599453,1]),
]
LITTLE = [([0,7],0),([9,900],.01),([8.1,900],.009),([3,2],1.5),
          ([1500,250],6),([.001,.0001],10),([1e6,1e-6],1e12)]


def run(candidate):
    payload=base64.b64encode(json.dumps([CASES,LITTLE]).encode()).decode()
    runner=r'''import base64,importlib.util,json,sys
spec=importlib.util.spec_from_file_location("candidate",sys.argv[1]);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
cases,little=json.loads(base64.b64decode(sys.argv[2]))
values=[m.queue_report(*args) for args,_ in cases]
defaults=m.queue_report(10,20,0,.5)
means=[m.little_mean_time(*args) for args,_ in little]
print("__RESULT__"+json.dumps({"values":values,"default":defaults,"means":means}))'''
    try:
        result=subprocess.run([sys.executable,"-c",runner,str(pathlib.Path(candidate).resolve()),payload],capture_output=True,text=True,timeout=5)
        lines=[s[len("__RESULT__"):] for s in result.stdout.splitlines() if s.startswith("__RESULT__")]
        return json.loads(lines[-1]) if result.returncode==0 and lines else None
    except (OSError,subprocess.TimeoutExpired,ValueError):
        return None


def close(actual, expected):
    return type(actual) in (int,float) and math.isfinite(actual) and math.isclose(actual,expected,rel_tol=1e-10,abs_tol=1e-300)


def report_matches(actual, expected):
    return type(actual) is dict and set(actual)==set(KEYS) and all(close(actual[k],v) for k,v in zip(KEYS,expected))


def passes(result):
    return (type(result) is dict and set(result)=={"values","default","means"}
        and type(result["values"]) is list and len(result["values"])==len(CASES)
        and all(report_matches(a,c[1]) for a,c in zip(result["values"],CASES))
        and report_matches(result["default"],CASES[0][1])
        and type(result["means"]) is list and len(result["means"])==len(LITTLE)
        and all(close(a,c[1]) for a,c in zip(result["means"],LITTLE)))


if __name__=="__main__":
    sys.exit(0 if len(sys.argv)==2 and passes(run(sys.argv[1])) else 1)
