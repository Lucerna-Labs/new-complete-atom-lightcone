"""Unit-weight inclusive presence and leaf-self attribution, not causation."""

from collections import Counter
from fractions import Fraction


def stack_attribution(samples):
    inclusive = Counter()
    own = Counter()
    for stack in samples:
        for frame in stack:
            inclusive[frame] += 1
        own[stack[-1]] += 1
    count = len(samples)
    rows = []
    for frame in sorted(inclusive):
        inc_fraction = Fraction(inclusive[frame], count)
        self_fraction = Fraction(own[frame], count)
        rows.append({
            "frame": frame, "inclusive": inclusive[frame], "self": own[frame],
            "inclusive_fraction": [inc_fraction.numerator, inc_fraction.denominator],
            "self_fraction": [self_fraction.numerator, self_fraction.denominator],
        })
    majority = next((frame for frame in sorted(own) if 2 * own[frame] > count), None)
    return {"sample_count": count, "frames": rows, "majority_hotspot": majority}
