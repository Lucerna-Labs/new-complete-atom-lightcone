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
EXCLUSIONS_PATH = ROOT / "sources" / "exclusions.json"
ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
RIGHTS = {
    "green:cc-by-4.0",
    "green:apache-2.0",
    "green:public-domain",
    "green:cc-by-sa-4.0",
    "green:cc-by-nc-sa-4.0",
    "green:nlm-mesh-terms",
    "citation_only",
    "restricted",
    "unknown",
}


def main() -> int:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    exclusions_data = json.loads(EXCLUSIONS_PATH.read_text(encoding="utf-8"))
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
    if exclusions_data.get("schema_version") != 1:
        errors.append("source exclusions schema_version must be 1")
    exclusions = exclusions_data.get("exclusions")
    if not isinstance(exclusions, list):
        errors.append("source exclusions must be a list")
        exclusions = []
    exclusion_ids: set[str] = set()
    exclusion_locators: set[str] = set()
    expected_exclusion_fields = {"source_id", "title", "locator", "reviewed_at", "reason"}
    for index, exclusion in enumerate(exclusions, start=1):
        if set(exclusion) != expected_exclusion_fields:
            errors.append(
                f"exclusion row {index} fields differ: "
                f"missing={sorted(expected_exclusion_fields - set(exclusion))} "
                f"extra={sorted(set(exclusion) - expected_exclusion_fields)}"
            )
        exclusion_id = exclusion.get("source_id")
        if not isinstance(exclusion_id, str) or not ID.fullmatch(exclusion_id):
            errors.append(f"exclusion row {index} has invalid source_id")
        elif exclusion_id in exclusion_ids:
            errors.append(f"duplicate exclusion source ID: {exclusion_id}")
        else:
            exclusion_ids.add(exclusion_id)
        locator = exclusion.get("locator")
        if not isinstance(locator, str) or not locator:
            errors.append(f"exclusion {exclusion_id} has invalid locator")
        elif locator in exclusion_locators:
            errors.append(f"duplicate exclusion locator: {locator}")
        else:
            exclusion_locators.add(locator)
        try:
            dt.date.fromisoformat(exclusion.get("reviewed_at", ""))
        except ValueError:
            errors.append(f"exclusion {exclusion_id} has invalid reviewed_at")
        if not isinstance(exclusion.get("reason"), str) or not exclusion["reason"].strip():
            errors.append(f"exclusion {exclusion_id} has no reason")
    overlaps = exclusion_ids & set(ids)
    if overlaps:
        errors.append(f"excluded source IDs appear in registry: {sorted(overlaps)}")
    registered_locators = {row.get("locator") for row in rows}
    locator_overlaps = exclusion_locators & registered_locators
    if locator_overlaps:
        errors.append(f"excluded locators appear in registry: {sorted(locator_overlaps)}")
    print(f"sources: {len(rows)}")
    print(f"explicit exclusions: {len(exclusions)}")
    print(f"rights lanes: {dict(sorted(collections.Counter(row.get('rights') for row in rows).items()))}")
    print(f"valid: {not errors}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
