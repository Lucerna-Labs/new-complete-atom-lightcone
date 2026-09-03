#!/usr/bin/env python3
"""Apply an explicit, non-sealing coverage transition with evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from registry_lib import COVERAGE_LEDGER, COVERAGE_ORDER, ROOT, STATUS_ORDER


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=["lane", "domain", "subfield", "bridge"], required=True)
    parser.add_argument("--all-of-kind", action="store_true")
    parser.add_argument("--id", action="append", dest="ids", default=[])
    parser.add_argument("--status", choices=STATUS_ORDER, required=True)
    parser.add_argument("--axis", action="append", default=[], help="axis=status")
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--note", required=True)
    args = parser.parse_args()
    if not args.all_of_kind and not args.ids:
        parser.error("provide --all-of-kind or one or more --id")
    evidence = ROOT / args.evidence
    if not evidence.is_file():
        parser.error(f"evidence file does not exist: {evidence}")
    updates = {}
    for encoded in args.axis:
        if "=" not in encoded:
            parser.error(f"invalid --axis {encoded!r}; expected axis=status")
        axis, status = encoded.split("=", 1)
        if status not in {*COVERAGE_ORDER, "inapplicable"}:
            parser.error(f"invalid coverage status {status}")
        updates[axis] = status

    ledger = json.loads(COVERAGE_LEDGER.read_text(encoding="utf-8"))
    selected = []
    for item in ledger["items"]:
        if item["kind"] != args.kind:
            continue
        if args.all_of_kind or item["id"] in args.ids:
            selected.append(item)
    expected = len([item for item in ledger["items"] if item["kind"] == args.kind]) if args.all_of_kind else len(set(args.ids))
    if len(selected) != expected:
        found = {item["id"] for item in selected}
        parser.error(f"coverage selection mismatch; missing {sorted(set(args.ids) - found)}")
    new_rank = STATUS_ORDER.index(args.status)
    for item in selected:
        if item["status"] in STATUS_ORDER and STATUS_ORDER.index(item["status"]) > new_rank:
            parser.error(f"refusing to regress {item['id']} from {item['status']} to {args.status}")
        unknown_axes = set(updates) - set(item["coverage"])
        if unknown_axes:
            parser.error(f"unknown axes for {item['id']}: {sorted(unknown_axes)}")
        item["status"] = args.status
        for axis, status in updates.items():
            current = item["coverage"][axis]
            if current in COVERAGE_ORDER and status in COVERAGE_ORDER and COVERAGE_ORDER.index(status) < COVERAGE_ORDER.index(current):
                parser.error(f"refusing to regress {item['id']} axis {axis}")
            item["coverage"][axis] = status
        if args.evidence not in item["evidence"]:
            item["evidence"].append(args.evidence)
        if args.note not in item["notes"]:
            item["notes"].append(args.note)
    COVERAGE_LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"updated {len(selected)} {args.kind} items to {args.status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

