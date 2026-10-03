# Semantic pitfall: check only the exact host and ignore ancestor coverage.
import ipaddress


def _is_ip(host):
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _known(host, policies):
    if _is_ip(host):
        return False
    return host in policies


def hsts_trace(events):
    policies, out = {}, []
    for event in events:
        now, host = event["time"], event["host"].lower()
        policies = {h:p for h,p in policies.items() if p["expires_at"] > now}
        scheme = port = must_terminate = None
        if event["type"] == "header":
            if event["secure"] and event["transport_ok"] and not _is_ip(host):
                if event["max_age"] == 0:
                    policies.pop(host, None)
                else:
                    policies[host] = {"expires_at":now+event["max_age"],
                                      "include_subdomains":event["include_subdomains"]}
        elif event["type"] == "request":
            scheme, port = event["scheme"], event["port"]
            known = _known(host, policies)
            if known and scheme == "http":
                scheme = "https"
                if port == 80:
                    port = 443
            must_terminate = known and event["transport_error"]
        else:
            raise ValueError("unknown event")
        out.append({"known_hsts":_known(host,policies),"scheme":scheme,"port":port,
                    "must_terminate":must_terminate,
                    "policies":{h:dict(p) for h,p in sorted(policies.items())}})
    return out
