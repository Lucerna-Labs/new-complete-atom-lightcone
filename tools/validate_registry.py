#!/usr/bin/env python3
"""Validate the open domain/lane catalogs and exhaustive coverage ledger."""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path
from typing import Any

from registry_lib import (
    COVERAGE_AXES,
    COVERAGE_LEDGER,
    COVERAGE_ORDER,
    DOMAIN_CATALOG,
    LANE_CATALOG,
    STATUS_ORDER,
    catalog_hashes,
    expected_items,
    load_json,
)

DISCOVERY_LEDGER = Path(__file__).resolve().parents[1] / "ontology" / "discovery-ledger.jsonl"
DISCOVERY_MANIFEST = Path(__file__).resolve().parents[1] / "ontology" / "discovery-manifest.json"


ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")

REQUIRED_LANES = {
    "reasoning.deductive",
    "reasoning.inductive",
    "reasoning.abductive",
    "reasoning.analogical",
    "reasoning.causal",
    "reasoning.counterfactual",
    "reasoning.probabilistic",
    "thinking.bottom_up",
    "thinking.lateral",
    "philosophy.analysis",
    "rhetoric.analysis",
    "geometry.structural",
    "psychology.evidence",
    "neuroscience.evidence",
    "creativity.generation_selection",
    "creativity.conceptual_blending",
    "creativity.constraint_based",
    "creativity.novelty_value",
    "creativity.problem_framing",
    "creativity.tension_transformation",
    "creativity.memory_recombination",
}

REQUIRED_DOMAINS = {
    "first-principles",
    "formal-mathematics",
    "geometry",
    "probability-statistics",
    "physics",
    "quantum-science",
    "chemistry",
    "biology",
    "neuroscience-neurology",
    "psychology-cognitive-science",
    "engineering",
    "computer-science",
    "software-engineering",
    "programming-languages-compilers",
    "language-ecosystems",
    "ai-machine-learning",
    "operating-systems-systems",
    "networking",
    "cybersecurity",
    "browser-web-platform",
    "frontend-web-development",
    "mobile-android-apple",
    "information-communication",
    "typography-color-visual-design",
    "philosophy",
    "rhetoric-argumentation",
    "literature",
    "creative-writing",
    "technical-professional-writing",
    "research-scientific-method",
    "forecasting-prediction",
    "custom-rust-orchestrated-apps",
}


class Problems:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)


def unique_ids(rows: list[dict[str, Any]], label: str, problems: Problems) -> set[str]:
    ids = [row.get("id") for row in rows]
    problems.require(all(isinstance(value, str) and ID.fullmatch(value) for value in ids), f"{label} contains an invalid id")
    counts = collections.Counter(ids)
    duplicates = sorted(value for value, count in counts.items() if count > 1)
    problems.require(not duplicates, f"{label} has duplicate ids: {duplicates}")
    return {value for value in ids if isinstance(value, str)}


def validate_catalogs(problems: Problems) -> tuple[set[str], set[str], list[str]]:
    domain_catalog = load_json(DOMAIN_CATALOG)
    lane_catalog = load_json(LANE_CATALOG)
    axes_catalog = load_json(COVERAGE_AXES)

    problems.require(domain_catalog.get("schema_version") == 1, "domain catalog schema_version must be 1")
    problems.require(domain_catalog.get("open_world") is True, "domain catalog must remain open_world")
    problems.require(lane_catalog.get("schema_version") == 1, "lane catalog schema_version must be 1")
    problems.require(lane_catalog.get("open_world") is True, "lane catalog must remain open_world")
    problems.require(axes_catalog.get("schema_version") == 1, "coverage axes schema_version must be 1")

    lanes = lane_catalog.get("lanes", [])
    domains = domain_catalog.get("domains", [])
    axes = axes_catalog.get("axes", [])
    problems.require(isinstance(lanes, list) and lanes, "lane catalog must contain lanes")
    problems.require(isinstance(domains, list) and domains, "domain catalog must contain domains")
    problems.require(isinstance(axes, list) and axes, "coverage catalog must contain axes")

    lane_ids = unique_ids(lanes, "lane catalog", problems)
    domain_ids = unique_ids(domains, "domain catalog", problems)
    axis_ids = sorted(unique_ids(axes, "coverage axes", problems))
    problems.require(REQUIRED_LANES <= lane_ids, f"missing required lanes: {sorted(REQUIRED_LANES - lane_ids)}")
    problems.require(REQUIRED_DOMAINS <= domain_ids, f"missing required domains: {sorted(REQUIRED_DOMAINS - domain_ids)}")

    subfields: list[dict[str, Any]] = []
    for domain in domains:
        problems.require(domain.get("mandatory") is True, f"domain {domain.get('id')} must remain mandatory")
        problems.require(domain.get("open_children") is True, f"domain {domain.get('id')} must remain open_children")
        rows = domain.get("subfields", [])
        problems.require(isinstance(rows, list) and rows, f"domain {domain.get('id')} has no subfields")
        subfields.extend(rows)
        unknown_lanes = sorted(set(domain.get("lanes", [])) - lane_ids)
        problems.require(not unknown_lanes, f"domain {domain.get('id')} references unknown lanes: {unknown_lanes}")

    subfield_ids = unique_ids(subfields, "subfield catalog", problems)
    collisions = sorted((domain_ids | lane_ids) & subfield_ids)
    problems.require(not collisions, f"subfield ids collide with domain/lane ids: {collisions}")

    for lane in lanes:
        for field in ("label", "kind", "definition"):
            problems.require(bool(lane.get(field)), f"lane {lane.get('id')} missing {field}")
        problems.require(bool(lane.get("required_stages")), f"lane {lane.get('id')} missing required_stages")
        problems.require(bool(lane.get("required_controls")), f"lane {lane.get('id')} missing required_controls")

    return lane_ids | domain_ids | subfield_ids, domain_ids, axis_ids


def validate_ledger(all_ids: set[str], domain_ids: set[str], axis_ids: list[str], problems: Problems) -> dict[str, int]:
    ledger = load_json(COVERAGE_LEDGER)
    problems.require(ledger.get("schema_version") == 1, "coverage ledger schema_version must be 1")
    problems.require(ledger.get("open_world") is True, "coverage ledger must remain open_world")
    problems.require(ledger.get("catalog_hashes") == catalog_hashes(), "coverage ledger catalog hashes are stale; regenerate it")
    items = ledger.get("items", [])
    item_ids = unique_ids(items, "coverage ledger", problems)
    expected_ids = {item["id"] for item in expected_items()}
    problems.require(item_ids == expected_ids, f"coverage ledger item mismatch: missing={sorted(expected_ids - item_ids)} extra={sorted(item_ids - expected_ids)}")
    problems.require(item_ids == all_ids, "coverage ledger does not close over all catalog ids")

    by_id = {item.get("id"): item for item in items}
    status_counts: collections.Counter[str] = collections.Counter()
    for item in items:
        item_id = item.get("id", "<missing>")
        status = item.get("status")
        status_counts[str(status)] += 1
        problems.require(status in {*STATUS_ORDER, "blocked", "retired"}, f"{item_id} has invalid status {status}")
        coverage = item.get("coverage", {})
        problems.require(sorted(coverage) == axis_ids, f"{item_id} coverage axes differ from canonical axes")
        problems.require(all(value in {*COVERAGE_ORDER, "inapplicable"} for value in coverage.values()), f"{item_id} has invalid coverage status")
        parent = item.get("parent")
        if item.get("kind") == "subfield":
            problems.require(parent in domain_ids, f"{item_id} has invalid parent {parent}")
        if status == "sealed":
            problems.require(all(value in {"sealed", "inapplicable"} for value in coverage.values()), f"sealed item {item_id} has unsealed coverage axes")
        if item.get("kind") == "domain" and status == "sealed":
            open_children = [candidate["id"] for candidate in items if candidate.get("parent") == item_id and candidate.get("mandatory") and candidate.get("status") != "sealed"]
            problems.require(not open_children, f"sealed domain {item_id} has unsealed children: {open_children}")
        problems.require(item_id in by_id, f"internal ledger index lost {item_id}")
    return dict(sorted(status_counts.items()))


def validate_discoveries(problems: Problems) -> tuple[int, int, dict[str, int]]:
    if not DISCOVERY_LEDGER.exists() or not DISCOVERY_MANIFEST.exists():
        return 0, 0, {}
    manifest = load_json(DISCOVERY_MANIFEST)
    from registry_lib import file_hash

    problems.require(manifest.get("schema_version") == 1, "discovery manifest schema_version must be 1")
    problems.require(manifest.get("open_world") is True, "discovery manifest must remain open_world")
    problems.require(manifest.get("ledger_sha256") == file_hash(DISCOVERY_LEDGER), "discovery ledger hash differs from manifest")
    ids: set[str] = set()
    counts: collections.Counter[str] = collections.Counter()
    unresolved = 0
    total = 0
    for line_number, line in enumerate(DISCOVERY_LEDGER.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        total += 1
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            problems.errors.append(f"discovery ledger line {line_number}: {error}")
            continue
        discovery_id = record.get("discovery_id")
        problems.require(isinstance(discovery_id, str) and ID.fullmatch(discovery_id), f"discovery line {line_number} has invalid ID")
        problems.require(discovery_id not in ids, f"duplicate discovery ID {discovery_id}")
        ids.add(discovery_id)
        status = record.get("status")
        problems.require(status in {"unmapped", "mapped", "excluded"}, f"discovery {discovery_id} has invalid status")
        if status == "unmapped":
            unresolved += 1
        if status == "mapped":
            problems.require(bool(record.get("mapped_coverage_ids")), f"mapped discovery {discovery_id} has no coverage IDs")
        if status == "excluded":
            problems.require(bool(record.get("exclusion_reason")), f"excluded discovery {discovery_id} has no reason")
        counts[str(record.get("source_id"))] += 1
    problems.require(manifest.get("entry_count") == total, "discovery manifest entry_count differs")
    problems.require(manifest.get("unresolved_count") == unresolved, "discovery manifest unresolved_count differs")
    problems.require(manifest.get("counts") == dict(sorted(counts.items())), "discovery manifest source counts differ")
    return total, unresolved, dict(sorted(counts.items()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-sealed", action="store_true", help="fail while any mandatory item or axis remains open")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    problems = Problems()
    try:
        all_ids, domain_ids, axis_ids = validate_catalogs(problems)
        status_counts = validate_ledger(all_ids, domain_ids, axis_ids, problems)
        discovery_count, unresolved_discoveries, discovery_counts = validate_discoveries(problems)
    except (OSError, json.JSONDecodeError, TypeError, KeyError) as error:
        problems.errors.append(str(error))
        status_counts = {}
        discovery_count, unresolved_discoveries, discovery_counts = 0, 0, {}

    ledger = load_json(COVERAGE_LEDGER) if COVERAGE_LEDGER.exists() else {"items": []}
    mandatory_open = [
        item["id"]
        for item in ledger.get("items", [])
        if item.get("mandatory") and item.get("status") != "sealed"
    ]
    axis_gaps = sum(
        1
        for item in ledger.get("items", [])
        if item.get("mandatory")
        for value in item.get("coverage", {}).values()
        if value not in {"sealed", "inapplicable"}
    )
    if args.require_sealed:
        problems.require(not mandatory_open, f"mandatory coverage remains open: {len(mandatory_open)} items")
        problems.require(axis_gaps == 0, f"mandatory coverage-axis gaps remain: {axis_gaps}")
        problems.require(unresolved_discoveries == 0, f"authoritative taxonomy discoveries remain unmapped: {unresolved_discoveries}")

    result = {
        "structurally_valid": not problems.errors,
        "open_world": True,
        "known_items": len(ledger.get("items", [])),
        "mandatory_open_items": len(mandatory_open),
        "mandatory_axis_gaps": axis_gaps,
        "status_counts": status_counts,
        "authoritative_discoveries": discovery_count,
        "unresolved_discoveries": unresolved_discoveries,
        "discovery_counts": discovery_counts,
        "exhaustive": not mandatory_open and axis_gaps == 0 and unresolved_discoveries == 0 and not problems.errors,
        "errors": problems.errors,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"registry structurally valid: {result['structurally_valid']}")
        print(f"open-world catalog items: {result['known_items']}")
        print(f"mandatory open items: {result['mandatory_open_items']}")
        print(f"mandatory coverage-axis gaps: {result['mandatory_axis_gaps']}")
        print(f"status counts: {result['status_counts']}")
        print(f"authoritative discoveries: {result['authoritative_discoveries']}")
        print(f"unresolved discoveries: {result['unresolved_discoveries']}")
        print(f"exhaustive: {result['exhaustive']}")
        for error in problems.errors:
            print(f"ERROR: {error}", file=sys.stderr)
    return 1 if problems.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
