import base64
import json
import pathlib
import subprocess
import sys

SPACES = ('initial', 'handshake', 'application')

def snapshot(acked=None, lost=None, probes=0):
    return {'acked': {s: list((acked or {}).get(s, ())) for s in SPACES},
            'lost': {s: list((lost or {}).get(s, ())) for s in SPACES},
            'probes': probes}

# Short ages isolate packet threshold3 from the time threshold. Packet0 is
# non-flight. Gapped ACKs do not acknowledge2; its later ACK preserves history.
A = [
    {'type':'sent','space':'initial','pn':0,'time':0.0,'in_flight':False},
    {'type':'sent','space':'initial','pn':1,'time':0.001,'in_flight':True},
    {'type':'sent','space':'application','pn':1,'time':0.001,'in_flight':True},
    {'type':'sent','space':'initial','pn':2,'time':0.002,'in_flight':True},
    {'type':'sent','space':'initial','pn':3,'time':0.003,'in_flight':True},
    {'type':'sent','space':'initial','pn':4,'time':0.004,'in_flight':True},
    {'type':'sent','space':'application','pn':4,'time':0.004,'in_flight':True},
    {'type':'sent','space':'initial','pn':5,'time':0.005,'in_flight':True},
    {'type':'ack','space':'initial','ranges':[[1,1],[4,5]],'time':0.01},
    {'type':'ack','space':'initial','ranges':[[3,3]],'time':0.015},
    {'type':'ack','space':'initial','ranges':[[2,2]],'time':0.02},
    {'type':'sent','space':'handshake','pn':1,'time':0.03,'in_flight':True},
    {'type':'ack','space':'handshake','ranges':[[1,1]],'time':0.04},
    {'type':'pto','space':'application','time':0.05},
    {'type':'ack','space':'application','ranges':[[4,4]],'time':0.06},
]
EA = [snapshot() for _ in range(8)] + [
    snapshot({'initial':[1,4,5]}, {'initial':[2]}),
    snapshot({'initial':[1,3,4,5]}, {'initial':[2]}),
    snapshot({'initial':[1,2,3,4,5]}, {'initial':[2]}),
    snapshot({'initial':[1,2,3,4,5]}, {'initial':[2]}),
    snapshot({'initial':[1,2,3,4,5],'handshake':[1]}, {'initial':[2]}),
    snapshot({'initial':[1,2,3,4,5],'handshake':[1]}, {'initial':[2]},1),
    snapshot({'initial':[1,2,3,4,5],'handshake':[1],'application':[4]}, {'initial':[2],'application':[1]},1),
]

# Binary-exact times isolate the9/8 boundary. PN0 is never in flight.
B = [
    {'type':'sent','space':'application','pn':0,'time':0.0,'in_flight':False},
    {'type':'sent','space':'application','pn':1,'time':0.0,'in_flight':True},
    {'type':'sent','space':'application','pn':2,'time':1/64,'in_flight':True},
    {'type':'sent','space':'application','pn':3,'time':2/64,'in_flight':True},
    {'type':'ack','space':'application','ranges':[[2,2]],'time':143/1024},
    {'type':'ack','space':'application','ranges':[[3,3]],'time':9/64},
]
EB = [snapshot() for _ in range(4)] + [
    snapshot({'application':[2]}),
    snapshot({'application':[2,3]}, {'application':[1]}),
]

# Here granularity=.25 exceeds9/8*RTT; ignoring granularity declares loss early.
C = [
    {'type':'sent','space':'application','pn':1,'time':0.0,'in_flight':True},
    {'type':'sent','space':'application','pn':2,'time':1/32,'in_flight':True},
    {'type':'sent','space':'application','pn':3,'time':1/16,'in_flight':True},
    {'type':'ack','space':'application','ranges':[[2,2]],'time':1/8},
    {'type':'ack','space':'application','ranges':[[3,3]],'time':1/4},
]
EC = [snapshot() for _ in range(3)] + [
    snapshot({'application':[2]}),
    snapshot({'application':[2,3]}, {'application':[1]}),
]

# A newer unacknowledged packet must not be lost just because its age is large.
D = [
    {'type':'sent','space':'application','pn':1,'time':0.0,'in_flight':True},
    {'type':'sent','space':'application','pn':2,'time':0.01,'in_flight':True},
    {'type':'ack','space':'application','ranges':[[1,1]],'time':10.0},
    {'type':'pto','space':'application','time':10.1},
]
ED = [snapshot(), snapshot(), snapshot({'application':[1]}), snapshot({'application':[1]},probes=1)]
# Unequal RTT estimates ensure the larger input governs in either order.
CASES = [(A,0.001,0.125,0.125),(B,0.001,0.125,0.125),(C,0.25,0.0625,0.0625),(D,0.001,0.125,0.125),
         (B,0.001,1/16,1/8),(B,0.001,1/8,1/16)]
EXPECTED = [EA,EB,EC,ED,EB,EB]

def run(candidate):
    payload = base64.b64encode(json.dumps(CASES).encode()).decode()
    runner = r'''import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location('candidate', sys.argv[1])
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
cases = json.loads(base64.b64decode(sys.argv[2]))
values = [mod.analyze_trace(events, granularity=g, srtt=s, latest_rtt=r) for events,g,s,r in cases]
print('__RESULT__'+json.dumps(values))'''
    try:
        result = subprocess.run([sys.executable,'-c',runner,str(pathlib.Path(candidate).resolve()),payload],capture_output=True,text=True,timeout=5)
        lines = [line[len('__RESULT__'):] for line in result.stdout.splitlines() if line.startswith('__RESULT__')]
        return json.loads(lines[-1]) if result.returncode == 0 and lines else None
    except (OSError,subprocess.TimeoutExpired,ValueError):
        return None

if __name__ == '__main__':
    sys.exit(0 if len(sys.argv)==2 and run(sys.argv[1])==EXPECTED else 1)
