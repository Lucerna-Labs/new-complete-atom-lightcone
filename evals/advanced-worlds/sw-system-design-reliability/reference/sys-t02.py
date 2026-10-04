from math import gcd

def _validate(capacity, initial, rate_num, rate_den, events):
    vals=(capacity,initial,rate_num,rate_den)
    if any(type(x) is not int for x in vals): raise ValueError("integer")
    if not 0<=capacity<=100 or not 0<=initial<=capacity or not 0<=rate_num<=100 or not 1<=rate_den<=100: raise ValueError("range")
    if type(events) is not list or len(events)>128: raise ValueError("events")
    previous=0
    for e in events:
        if type(e) is not dict or set(e)!={"time","cost"} or type(e["time"]) is not int or type(e["cost"]) is not int: raise ValueError("event")
        if not 0<=e["time"]<=1000000 or not 1<=e["cost"]<=1000 or e["time"]<previous: raise ValueError("event range")
        previous=e["time"]

def bucket_events(capacity, initial, rate_num, rate_den, events):
    _validate(capacity,initial,rate_num,rate_den,events)
    denominator=rate_den; balance=initial*denominator; previous=0; out=[]
    for event in events:
        balance += (event["time"]-previous)*rate_num
        balance=min(balance,capacity*denominator); previous=event["time"]
        accepted=balance>=event["cost"]*denominator
        if accepted: balance-=event["cost"]*denominator
        divisor=gcd(balance,denominator)
        out.append({"accepted":accepted,"balance":[balance//divisor,denominator//divisor]})
    return out
