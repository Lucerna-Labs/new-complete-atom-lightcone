#!/usr/bin/env python3
"""Validate source identity, rights lanes, and basic provenance fields."""

from __future__ import annotations

import collections
import datetime as dt
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "sources" / "source-registry.json"
ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
RIGHTS = {
    "green:cc-by-4.0",
    "green:apache-2.0",
    "green:public-domain",
    "green:cc-by-sa-4.0",
    "citation_only",
    "restricted",
    "unknown",
}


def main() -> int:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("source registry schema_version must be 1")
    rows = data.get("sources")
    if not isinstance(rows, list) or not rows:
        errors.append("source registry is empty")
        rows = []
    ids = [row.get("source_id") for row in rows]
    duplicates = [source_id for source_id, count in collections.Counter(ids).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate source IDs: {sorted(duplicates)}")
    for index, row in enumerate(rows, start=1):
        source_id = row.get("source_id")
        if not isinstance(source_id, str) or not ID.fullmatch(source_id):
            errors.append(f"row {index} has invalid source_id")
        expected = {"source_id", "title", "locator", "publisher", "version", "retrieved_at", "rights", "trust_role"}
        if set(row) != expected:
            errors.append(f"source {source_id} fields differ: missing={sorted(expected - set(row))} extra={sorted(set(row) - expected)}")
        if row.get("rights") not in RIGHTS:
            errors.append(f"source {source_id} has invalid rights lane")
        try:
            dt.date.fromisoformat(row.get("retrieved_at", ""))
        except ValueError:
            errors.append(f"source {source_id} has invalid retrieved_at")
        if not row.get("locator") or not row.get("title") or not row.get("publisher"):
            errors.append(f"source {source_id} is missing identity fields")
    print(f"sources: {len(rows)}")
    print(f"rights lanes: {dict(sorted(collections.Counter(row.get('rights') for row in rows).items()))}")
    print(f"valid: {not errors}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

