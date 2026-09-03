"""Deterministic relation-family split assignment for authored curricula."""

from __future__ import annotations

import collections


class RelationSplitter:
    """Keep first evidence for every relation in train before any holdout.

    Relation families with at least three examples contribute one validation
    and one sealed example. A requested cross-domain holdout is permitted only
    after the family has training support and before its reserved validation
    and sealed examples.
    """

    def __init__(self, kinds: list[str]) -> None:
        self.totals = collections.Counter(kinds)
        self.seen: collections.Counter[str] = collections.Counter()

    def split(self, kind: str, *, cross_requested: bool = False) -> str:
        position = self.seen[kind]
        self.seen[kind] += 1
        total = self.totals[kind]
        if position == 0:
            return "train"
        if total >= 3 and position == total - 1:
            return "sealed_test"
        if total >= 3 and position == total - 2:
            return "validation"
        if cross_requested and position < total - 2:
            return "cross_domain_holdout"
        return "train"

