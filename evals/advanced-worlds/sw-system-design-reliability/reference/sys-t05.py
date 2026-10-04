"""Exact observed SLO quantities and the declared release permission gate."""

from fractions import Fraction


def slo_report(shards, target_num, target_den, exception):
    if type(shards) is not list or len(shards) > 64:
        raise ValueError("shards must be a bounded native list")
    if (type(target_num) is not int or type(target_den) is not int
            or not 1 <= target_den <= 1000
            or not 0 <= target_num <= target_den):
        raise ValueError("invalid exact target")
    if type(exception) is not bool:
        raise ValueError("exception must be a native bool")
    for shard in shards:
        if (type(shard) is not dict
                or any(type(key) is not str for key in shard)
                or set(shard) != {"good", "eligible"}):
            raise ValueError("invalid shard schema")
        good, eligible = shard["good"], shard["eligible"]
        if (type(good) is not int or type(eligible) is not int
                or not 0 <= good <= eligible <= 1000000):
            raise ValueError("invalid shard counts")

    good = sum(shard["good"] for shard in shards)
    eligible = sum(shard["eligible"] for shard in shards)
    bad = eligible - good
    target = Fraction(target_num, target_den)
    allowance = (1 - target) * eligible
    remaining = allowance - bad
    sli = Fraction(good, eligible) if eligible else None
    burn = Fraction(bad, eligible) / (1 - target) if eligible and target < 1 else None

    def pair(value):
        return None if value is None else [value.numerator, value.denominator]

    return {"eligible": eligible, "good": good, "bad": bad,
            "sli": pair(sli), "allowance": pair(allowance),
            "remaining": pair(remaining), "burn": pair(burn),
            "met": sli >= target if sli is not None else None,
            "release": remaining > 0 or exception}
