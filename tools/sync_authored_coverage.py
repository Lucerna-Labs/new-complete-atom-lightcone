#!/usr/bin/env python3
"""Synchronize explicitly declared curriculum axes into the authored ledger."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from registry_lib import COVERAGE_LEDGER, COVERAGE_ORDER, ROOT, STATUS_ORDER


def collect_explicit_evidence() -> dict[tuple[str, str], dict[str, set[str]]]:
    evidence: dict[tuple[str, str], dict[str, set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )
    for path in sorted((ROOT / "curricula").rglob("*.jsonl")):
        relative = str(path.relative_to(ROOT))
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            targets = [
                ("domain", record["domain_id"]),
                ("subfield", record["subject_id"]),
                *(("lane", lane) for lane in record["lanes"]),
            ]
            for target in targets:
                for axis in record["coverage_axes"]:
                    evidence[target][axis].add(relative)
    return evidence


def synchronize(
    ledger: dict[str, Any],
    evidence: dict[tuple[str, str], dict[str, set[str]]],
    *,
    apply: bool,
) -> list[str]:
    uncredited: list[str] = []
    authored_rank = COVERAGE_ORDER.index("authored")
    for item in ledger["items"]:
        direct = evidence.get((item["kind"], item["id"]), {})
        for axis, paths in sorted(direct.items()):
            current = item["coverage"][axis]
            if current == "inapplicable" or (
                current in COVERAGE_ORDER
                and COVERAGE_ORDER.index(current) >= authored_rank
            ):
                continue
            uncredited.append(f"{item['kind']}:{item['id']}:{axis}")
            if apply:
                item["coverage"][axis] = "authored"
                for path in sorted(paths):
                    if path not in item["evidence"]:
                        item["evidence"].append(path)
        if apply and direct:
            if STATUS_ORDER.index(item["status"]) < STATUS_ORDER.index("authored"):
                item["status"] = "authored"
            note = "Authored axis credit is derived only from explicit coverage_axes declarations in cited curriculum records."
            if note not in item["notes"]:
                item["notes"].append(note)
            item["evidence"] = sorted(set(item["evidence"]))
    return uncredited


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    ledger = json.loads(COVERAGE_LEDGER.read_text(encoding="utf-8"))
    uncredited = synchronize(ledger, collect_explicit_evidence(), apply=args.apply)
    if args.apply:
        COVERAGE_LEDGER.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"credited explicit authored axes: {len(uncredited)}")
        return 0
    print(f"uncredited explicit authored axes: {len(uncredited)}")
    return 1 if uncredited else 0


if __name__ == "__main__":
    raise SystemExit(main())
