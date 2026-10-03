import ipaddress


def service_identity(reference, certificate):
    if reference["kind"] == "IP":
        wanted = ipaddress.ip_address(reference["value"])
        for presented in certificate["ip_sans"]:
            address = ipaddress.ip_address(presented)
            if address.version == wanted.version and address.packed == wanted.packed:
                return True
        return False
    wanted = reference["value"].lower().split(".")
    # Single error: admit Common Name as another DNS service identifier.
    for presented in certificate["dns_sans"] + ([certificate["common_name"]] if certificate["common_name"] is not None else []):
        labels = presented.lower().split(".")
        if "*" not in presented:
            if labels == wanted:
                return True
        elif presented.count("*") == 1 and labels[0] == "*":
            if len(labels) == len(wanted) and labels[1:] == wanted[1:] and wanted[0]:
                return True
    return False
