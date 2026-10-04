import copy, re

def _ident(value):
    if type(value) is not str or not re.fullmatch(r"[A-Za-z0-9_-]{1,32}", value):
        raise ValueError("invalid identity")

def cache_events(events):
    if type(events) is not list or len(events)>128:
        raise ValueError("events")
    generations, entries, pending, seen, snapshots = {}, {}, {}, set(), []
    schemas={"begin":{"op","fill","key","value"}, "invalidate":{"op","key"},
             "evict":{"op","key"}, "finish":{"op","fill"}, "read":{"op","key"}}
    for event in events:
        if type(event) is not dict or type(event.get("op")) is not str:
            raise ValueError("event")
        op=event["op"]
        if op not in schemas or set(event)!=schemas[op]:
            raise ValueError("schema")
        result=None
        if op=="begin":
            _ident(event["fill"]); _ident(event["key"])
            value=event["value"]
            if type(value) is not int or not -1000<=value<=1000 or event["fill"] in seen:
                raise ValueError("fill")
            key=event["key"]; generations.setdefault(key,0)
            seen.add(event["fill"])
            pending[event["fill"]]={"key":key,"generation":generations[key],"value":value}
        elif op=="finish":
            _ident(event["fill"])
            if event["fill"] not in pending:
                raise ValueError("unknown fill")
            row=pending.pop(event["fill"])
            result=row["generation"]==generations[row["key"]]
            if result:
                entries[row["key"]]=row["value"]
        else:
            _ident(event["key"]); key=event["key"]
            generations.setdefault(key,0)
            if op=="invalidate":
                generations[key]+=1
                entries.pop(key,None)
            elif op=="evict":
                entries.pop(key,None)
            else:
                result=entries.get(key)
        snapshots.append(copy.deepcopy({"result":result,"generations":generations,
                                        "entries":entries,"pending":pending}))
    return snapshots
