#!/usr/bin/env python3
"""Create the deterministic initial coverage ledger from the catalogs."""

from __future__ import annotations

import argparse
import json

from registry_lib import COVERAGE_LEDGER, catalog_hashes, expected_items


def merge_existing(existing: dict, expected: list[dict]) -> dict:
    current = {(item["kind"], item["id"]): item for item in existing["items"]}
    wanted = {(item["kind"], item["id"]): item for item in expected}
    extra = sorted(set(current) - set(wanted))
    if extra:
        raise ValueError(f"existing ledger contains items absent from catalogs: {extra}")
    return {
        "schema_version": 1,
        "open_world": True,
        "catalog_hashes": catalog_hashes(),
        "items": [current.get(key, item) for key, item in sorted(wanted.items())],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--merge", action="store_true")
    args = parser.parse_args()
    if args.force and args.merge:
        parser.error("--force and --merge are mutually exclusive")

    if COVERAGE_LEDGER.exists() and not args.force and not args.merge:
        parser.error(f"{COVERAGE_LEDGER} already exists; pass --force to regenerate")

    expected = expected_items()
    if args.merge and COVERAGE_LEDGER.exists():
        ledger = merge_existing(
            json.loads(COVERAGE_LEDGER.read_text(encoding="utf-8")), expected
        )
    else:
        ledger = {
            "schema_version": 1,
            "open_world": True,
            "catalog_hashes": catalog_hashes(),
            "items": expected,
        }
    COVERAGE_LEDGER.write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {COVERAGE_LEDGER} with {len(ledger['items'])} open coverage items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
