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

    def __init__(
        self,
        kinds: list[str],
        *,
        cross_plan: list[bool] | None = None,
    ) -> None:
        self.totals = collections.Counter(kinds)
        self.seen: collections.Counter[str] = collections.Counter()
        self.plans: dict[str, list[str]] | None = None
        if cross_plan is not None:
            if len(cross_plan) != len(kinds):
                raise ValueError("cross_plan must align one-for-one with kinds")
            positions: dict[str, list[int]] = collections.defaultdict(list)
            for index, kind in enumerate(kinds):
                positions[kind].append(index)
            plans: dict[str, list[str]] = {}
            for kind, global_positions in positions.items():
                plan = ["train"] * len(global_positions)
                for local_index, global_index in enumerate(global_positions):
                    if local_index > 0 and cross_plan[global_index]:
                        plan[local_index] = "cross_domain_holdout"
                ordinary = [
                    index
                    for index in range(1, len(plan))
                    if plan[index] == "train"
                ]
                if len(ordinary) >= 2:
                    plan[ordinary[-2]] = "validation"
                    plan[ordinary[-1]] = "sealed_test"
                plans[kind] = plan
            self.plans = plans

    def split(
        self,
        kind: str,
        *,
        cross_requested: bool = False,
    ) -> str:
        position = self.seen[kind]
        self.seen[kind] += 1
        total = self.totals[kind]
        if self.plans is not None:
            return self.plans[kind][position]
        if position == 0:
            return "train"
        if total >= 3 and position == total - 1:
            return "sealed_test"
        if total >= 3 and position == total - 2:
            return "validation"
        if cross_requested and position < total - 2:
            return "cross_domain_holdout"
        return "train"
