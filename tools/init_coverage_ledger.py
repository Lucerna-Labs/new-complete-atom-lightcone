#!/usr/bin/env python3
"""Create the deterministic initial coverage ledger from the catalogs."""

from __future__ import annotations

import argparse
import json

from registry_lib import COVERAGE_LEDGER, catalog_hashes, expected_items


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if COVERAGE_LEDGER.exists() and not args.force:
        parser.error(f"{COVERAGE_LEDGER} already exists; pass --force to regenerate")

    ledger = {
        "schema_version": 1,
        "open_world": True,
        "catalog_hashes": catalog_hashes(),
        "items": expected_items(),
    }
    COVERAGE_LEDGER.write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {COVERAGE_LEDGER} with {len(ledger['items'])} open coverage items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

