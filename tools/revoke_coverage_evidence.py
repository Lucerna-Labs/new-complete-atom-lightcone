#!/usr/bin/env python3
"""Revoke invalid evidence and explicitly downgrade affected coverage claims."""

from __future__ import annotations

import argparse
import json

from registry_lib import COVERAGE_LEDGER, COVERAGE_ORDER, ROOT, STATUS_ORDER


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--affected-evidence", required=True)
    parser.add_argument("--revocation", required=True)
    parser.add_argument("--replacement-evidence", required=True)
    parser.add_argument("--status", choices=STATUS_ORDER, required=True)
    parser.add_argument("--coverage", choices=COVERAGE_ORDER, required=True)
    parser.add_argument("--note", required=True)
    args = parser.parse_args()

    for relative in (args.affected_evidence, args.revocation, args.replacement_evidence):
        if not (ROOT / relative).is_file():
            parser.error(f"evidence file does not exist: {relative}")

    ledger = json.loads(COVERAGE_LEDGER.read_text(encoding="utf-8"))
    selected = [
        item for item in ledger["items"] if args.affected_evidence in item.get("evidence", [])
    ]
    if not selected:
        parser.error("no coverage items reference the affected evidence")

    replacement_rank = COVERAGE_ORDER.index(args.coverage)
    for item in selected:
        item["status"] = args.status
        for axis, value in item["coverage"].items():
            if value in COVERAGE_ORDER and COVERAGE_ORDER.index(value) > replacement_rank:
                item["coverage"][axis] = args.coverage
        for evidence in (args.revocation, args.replacement_evidence):
            if evidence not in item["evidence"]:
                item["evidence"].append(evidence)
        if args.note not in item["notes"]:
            item["notes"].append(args.note)

    COVERAGE_LEDGER.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"revoked evidence for {len(selected)} coverage items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
