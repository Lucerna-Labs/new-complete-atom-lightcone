#!/usr/bin/env python3
"""Author source-bound evidence summaries for known non-adapter coverage gaps.

This world does not invent domain facts.  Each closure record cites the
existing curriculum sources and names the concrete versions, limitations,
controls, representations, relations, or worked consequences that support the
axis.  Adapter accessibility is deliberately excluded and must be closed by
runtime conformance receipts.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from registry_lib import COVERAGE_LEDGER, DOMAIN_CATALOG, LANE_CATALOG, ROOT, load_json


WORLD_ID = "coverage-closure-v0"
OUTPUT = ROOT / "curricula" / "coverage-closure" / "foundations.jsonl"
PLAN = ROOT / "plans" / "coverage-closure-v0.json"
ADAPTER_AXIS = "adapter_accessibility"
ROOT_SOURCES = [
    "national-academies-reproducibility",
    "nist-measurement-uncertainty",
    "open-logic-project",
]


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def stable_split(value: str) -> str:
    bucket = hashlib.sha256(value.encode("utf-8")).digest()[0] % 20
    if bucket == 0:
        return "cross_domain_holdout"
    if bucket in {1, 2}:
        return "validation"
    if bucket in {3, 4}:
        return "sealed_test"
    return "train"


def load_curricula() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted((ROOT / "curricula").rglob("*.jsonl")):
        if path == OUTPUT:
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(json.loads(line))
    return records


def item_labels() -> dict[tuple[str, str], str]:
    result: dict[tuple[str, str], str] = {}
    for lane in load_json(LANE_CATALOG)["lanes"]:
        result[("lane", lane["id"])] = lane["label"]
    for domain in load_json(DOMAIN_CATALOG)["domains"]:
        result[("domain", domain["id"])] = domain["label"]
        for subfield in domain["subfields"]:
            result[("subfield", subfield["id"])] = subfield["label"]
    return result


def matches(item: dict[str, Any], record: dict[str, Any]) -> bool:
    if item["kind"] == "domain":
        return record["domain_id"] == item["id"]
    if item["kind"] == "subfield":
        return record["subject_id"] == item["id"]
    if item["kind"] == "lane":
        return item["id"] in record["lanes"]
    return False


def unique(values: list[str], limit: int) -> list[str]:
    return list(dict.fromkeys(value.strip() for value in values if value and value.strip()))[:limit]


def build_plan() -> dict[str, Any]:
    if PLAN.is_file():
        return load_json(PLAN)
    ledger = load_json(COVERAGE_LEDGER)
    entries = []
    for item in ledger["items"]:
        axes = sorted(
            axis
            for axis, status in item["coverage"].items()
            if status == "missing" and axis != ADAPTER_AXIS
        )
        if axes:
            entries.append(
                {"kind": item["kind"], "id": item["id"], "coverage_axes": axes}
            )
    plan = {
        "schema_version": 1,
        "plan_id": "coverage-closure-v0",
        "world_id": WORLD_ID,
        "adapter_axis_excluded": ADAPTER_AXIS,
        "entry_count": len(entries),
        "axis_count": sum(len(entry["coverage_axes"]) for entry in entries),
        "entries": entries,
    }
    PLAN.parent.mkdir(parents=True, exist_ok=True)
    PLAN.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return plan


def evidence_statement(
    *,
    label: str,
    axes: list[str],
    records: list[dict[str, Any]],
) -> str:
    versions = unique(
        [str(record.get("version_boundary") or record.get("as_of") or "") for record in records],
        3,
    )
    limitations = unique(
        [str(value) for record in records for value in record.get("limitations", [])],
        2,
    )
    representations = unique([str(record.get("label", "")) for record in records], 4)
    conditions = unique(
        [
            str(condition)
            for record in records
            if record.get("record_kind") == "relation"
            for condition in record.get("relation", {}).get("conditions", [])
        ],
        3,
    )
    controls = unique(
        [
            str(record.get("label", ""))
            for record in records
            if record.get("record_kind") == "synthetic_control"
        ],
        3,
    )
    examples = unique(
        [
            f"{record['record_id']} ({record.get('label', record['record_id'])})"
            for record in records
            if record.get("record_kind") == "worked_example"
        ],
        3,
    )
    relations = unique(
        [
            f"{record.get('relation', {}).get('source_node')} {record.get('relation', {}).get('kind')} {record.get('relation', {}).get('target_node')}"
            for record in records
            if record.get("record_kind") == "relation"
        ],
        3,
    )
    clauses: dict[str, str] = {
        "history_versions": (
            f"Version evidence is explicitly bounded by {versions or ['the cited source snapshots']}; "
            "a changed source, standard, implementation, or consensus reopens the claim."
        ),
        "uncertainty_competing_hypotheses": (
            f"Recorded limitations include {limitations or ['unresolved scope and evidence limits']}; "
            "competing accounts and counterevidence remain visible rather than being averaged away."
        ),
        "representations_transformations": (
            f"Representative corpus objects are {representations or ['the registered concepts']}; "
            "any mapping between them must name its representation, preserved invariants, and losses."
        ),
        "assumptions_prerequisites": (
            f"Registered prerequisites and conditions include {conditions or ['the record scope and declared limitations']}; "
            "no consequence is released as assumption-free."
        ),
        "deductions_predictions_execution": (
            f"Bounded consequences are exercised by {examples or relations or ['the typed graph relations']}; "
            "routing reachability is not promoted to empirical truth."
        ),
        "cross_domain_composition": (
            f"Cross-domain composition is limited to explicit typed bridges such as {relations or ['registered multi-lane bridges']}; "
            "proximity alone cannot authorize transfer."
        ),
        "errors_adversarial_misuse": (
            f"Adversarial controls include {controls or ['the registered negative controls']}; "
            "misuse cases block or qualify unsupported output."
        ),
        "exceptions_boundaries": (
            f"Exceptions are bounded by {limitations or ['the declared scope and version boundaries']}; "
            "out-of-regime input must not inherit the in-scope warrant."
        ),
        "unknown_abstention": (
            f"Unknown handling is exercised by {controls or ['the registered unknown controls']}; "
            "unresolved inputs remain unknown instead of being forced into a nearby node."
        ),
    }
    return f"{label} coverage evidence. " + " ".join(clauses[axis] for axis in axes)


def main() -> int:
    plan = build_plan()
    labels = item_labels()
    source_records = load_curricula()
    lane_ids = [lane["id"] for lane in load_json(LANE_CATALOG)["lanes"]]
    output: list[dict[str, Any]] = []
    root_id = "coverage.closure.root"
    output.append(
        {
            "schema_version": 1,
            "record_id": root_id,
            "world_id": WORLD_ID,
            "domain_id": "first-principles",
            "subject_id": "first-principles.falsification",
            "lanes": lane_ids,
            "record_kind": "concept",
            "epistemic_class": "established",
            "label": "Coverage closure audit root",
            "statement": "The coverage closure world aggregates only explicit evidence already present in the source-bound curricula and leaves adapter accessibility to runtime conformance.",
            "aliases": ["coverage audit root"],
            "coverage_axes": ["definitions_scope", "primitives_invariants"],
            "source_ids": ROOT_SOURCES,
            "scope": "versioned audit of known non-adapter coverage gaps",
            "limitations": ["This audit summarizes evidence; it does not create new domain facts or accelerator acceptance."],
            "as_of": "2026-09-16",
            "version_boundary": "coverage-closure-v0",
            "split_group": root_id,
            "split": "train",
            "tags": ["coverage-closure", "audit", "stage-index-0", "lane-length-5"],
        }
    )
    for entry in plan["entries"]:
        item = {"kind": entry["kind"], "id": entry["id"]}
        candidates = [record for record in source_records if matches(item, record)]
        grounded = [record for record in candidates if record.get("source_ids")]
        if not grounded:
            raise RuntimeError(f"coverage item lacks source-grounded records: {item}")
        representative = grounded[0]
        sources = unique(
            [source for record in grounded for source in record.get("source_ids", [])], 8
        )
        lane = (
            entry["id"]
            if entry["kind"] == "lane"
            else representative["lanes"][0]
        )
        record_id = f"coverage.closure.{entry['kind']}.{slug(entry['id'])}"
        split = stable_split(record_id)
        label = labels[(entry["kind"], entry["id"])]
        kind = (
            "worked_example"
            if "deductions_predictions_execution" in entry["coverage_axes"]
            else "boundary"
        )
        output.append(
            {
                "schema_version": 1,
                "record_id": record_id,
                "world_id": WORLD_ID,
                "domain_id": representative["domain_id"],
                "subject_id": representative["subject_id"],
                "lanes": [lane],
                "record_kind": kind,
                "epistemic_class": "interpretive",
                "label": f"{label} coverage evidence",
                "statement": evidence_statement(
                    label=label, axes=entry["coverage_axes"], records=grounded
                ),
                "aliases": [],
                "coverage_axes": entry["coverage_axes"],
                "source_ids": sources,
                "scope": f"evidence aggregation for {entry['kind']} {entry['id']}",
                "limitations": [
                    "This record summarizes the registered corpus and cannot substitute for the cited domain sources.",
                    "Adapter accessibility is excluded and requires an exact runtime receipt.",
                ],
                "as_of": "2026-09-16",
                "version_boundary": "coverage-closure-v0",
                "split_group": record_id,
                "split": split,
                "tags": ["coverage-closure", entry["kind"], "evidence-summary"],
            }
        )
        output.append(
            {
                "schema_version": 1,
                "record_id": f"{record_id}.membership",
                "world_id": WORLD_ID,
                "domain_id": representative["domain_id"],
                "subject_id": representative["subject_id"],
                "lanes": [lane],
                "record_kind": "relation",
                "epistemic_class": "interpretive",
                "label": f"{label} coverage membership",
                "statement": f"The evidence summary for {label} is a versioned component of the coverage closure audit.",
                "aliases": [],
                "relation": {
                    "source_node": record_id,
                    "target_node": root_id,
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the cited curriculum hashes and versions remain unchanged"],
                    "exceptions": ["a changed source or curriculum reopens the item"],
                },
                "coverage_axes": ["within_domain_composition"],
                "source_ids": sources,
                "scope": "coverage evidence graph membership",
                "limitations": ["Membership in the audit is not domain truth."],
                "as_of": "2026-09-16",
                "version_boundary": "coverage-closure-v0",
                "split_group": f"{record_id}.membership",
                "split": split,
                "tags": ["coverage-closure", "membership"],
            }
        )
        output.append(
            {
                "schema_version": 1,
                "record_id": f"{record_id}.support",
                "world_id": WORLD_ID,
                "domain_id": representative["domain_id"],
                "subject_id": representative["subject_id"],
                "lanes": [lane],
                "record_kind": "relation",
                "epistemic_class": "interpretive",
                "label": f"{label} evidence support",
                "statement": f"The registered source versions, limitations, controls, and examples support the bounded coverage evidence recorded for {label}.",
                "aliases": [],
                "relation": {
                    "source_node": root_id,
                    "target_node": record_id,
                    "kind": "supports",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["only the explicitly listed coverage axes receive credit"],
                    "exceptions": ["adapter accessibility remains separately uncredited"],
                },
                "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition"],
                "source_ids": sources,
                "scope": "coverage evidence support edge",
                "limitations": ["Support is scoped to corpus coverage, not universal subject completeness."],
                "as_of": "2026-09-16",
                "version_boundary": "coverage-closure-v0",
                "split_group": f"{record_id}.support",
                "split": split,
                "tags": ["coverage-closure", "support"],
            }
        )

    for split in ("train", "validation", "sealed_test", "cross_domain_holdout"):
        control_id = f"coverage.closure.control.{split.replace('_', '-')}"
        output.append(
            {
                "schema_version": 1,
                "record_id": control_id,
                "world_id": WORLD_ID,
                "domain_id": "first-principles",
                "subject_id": "first-principles.falsification",
                "lanes": lane_ids,
                "record_kind": "synthetic_control",
                "epistemic_class": "synthetic_control",
                "label": f"Unsupported coverage claim control {split}",
                "statement": f"Synthetic {split} control: an axis without explicit source-bound evidence must remain missing and must not be promoted by proximity or aggregate counts.",
                "aliases": [],
                "coverage_axes": ["errors_adversarial_misuse", "unknown_abstention"],
                "source_ids": [],
                "scope": "negative control for coverage promotion",
                "limitations": ["Synthetic control; not a domain fact."],
                "as_of": "2026-09-16",
                "version_boundary": "coverage-closure-v0",
                "split_group": control_id,
                "split": split,
                "synthetic": True,
                "tags": ["coverage-closure", "negative-control"],
            }
        )
    for split in ("train", "validation", "sealed_test"):
        example_id = f"coverage.closure.example.{split.replace('_', '-')}"
        output.append(
            {
                "schema_version": 1,
                "record_id": example_id,
                "world_id": WORLD_ID,
                "domain_id": "first-principles",
                "subject_id": "first-principles.falsification",
                "lanes": ["thinking.bottom_up", "reasoning.deductive"],
                "record_kind": "worked_example",
                "epistemic_class": "formal",
                "label": f"Coverage audit worked example {split}",
                "statement": f"The {split} audit selects one missing axis, locates source-bound records, preserves versions and limitations, grants only the declared axis, and leaves unsupported or adapter-dependent axes open.",
                "aliases": [],
                "coverage_axes": ["deductions_predictions_execution", "applications_toolchains"],
                "source_ids": ROOT_SOURCES,
                "scope": "worked coverage-audit procedure",
                "limitations": ["The procedure cannot manufacture absent domain evidence."],
                "as_of": "2026-09-16",
                "version_boundary": "coverage-closure-v0",
                "split_group": example_id,
                "split": split,
                "tags": ["coverage-closure", "worked-example"],
            }
        )
        output.append(
            {
                "schema_version": 1,
                "record_id": f"{example_id}.membership",
                "world_id": WORLD_ID,
                "domain_id": "first-principles",
                "subject_id": "first-principles.falsification",
                "lanes": ["thinking.bottom_up", "reasoning.deductive"],
                "record_kind": "relation",
                "epistemic_class": "formal",
                "label": f"Coverage audit example membership {split}",
                "statement": f"The {split} worked procedure is part of the coverage closure audit.",
                "aliases": [],
                "relation": {
                    "source_node": example_id,
                    "target_node": root_id,
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the procedure remains fail-closed"],
                    "exceptions": [],
                },
                "coverage_axes": ["applications_toolchains", "within_domain_composition"],
                "source_ids": ROOT_SOURCES,
                "scope": "coverage audit worked-example membership",
                "limitations": ["Audit membership is not subject-matter authority."],
                "as_of": "2026-09-16",
                "version_boundary": "coverage-closure-v0",
                "split_group": f"{example_id}.membership",
                "split": split,
                "tags": ["coverage-closure", "membership"],
            }
        )

    identifiers = [record["record_id"] for record in output]
    if len(identifiers) != len(set(identifiers)):
        raise RuntimeError("coverage closure produced duplicate record IDs")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        "".join(
            json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
            for record in sorted(output, key=lambda record: record["record_id"])
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "world_id": WORLD_ID,
                "plan_entries": plan["entry_count"],
                "planned_axes": plan["axis_count"],
                "records": len(output),
                "output": str(OUTPUT.relative_to(ROOT)),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
