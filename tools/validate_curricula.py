#!/usr/bin/env python3
"""Validate curriculum identity, provenance, graph closure, and split isolation."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path
from typing import Any

from registry_lib import COVERAGE_AXES, DOMAIN_CATALOG, LANE_CATALOG, ROOT, load_json


ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
ALLOWED_FIELDS = {
    "schema_version", "record_id", "world_id", "domain_id", "subject_id", "lanes",
    "record_kind", "epistemic_class", "label", "statement", "aliases", "relation",
    "coverage_axes", "source_ids", "scope", "limitations", "as_of", "version_boundary",
    "split_group", "split", "synthetic", "tags"
}
REQUIRED_FIELDS = {
    "schema_version", "record_id", "world_id", "domain_id", "subject_id", "lanes",
    "record_kind", "epistemic_class", "statement", "split_group", "split", "source_ids"
}
SPLITS = {"train", "validation", "sealed_test", "cross_domain_holdout"}
KINDS = {"concept", "relation", "worked_example", "counterexample", "boundary", "synthetic_control"}
EPISTEMIC = {"formal", "established", "provisional", "hypothesis", "contested", "interpretive", "creative", "synthetic_control"}
RELATIONS = {"causes", "enables", "supports", "grounds", "clarifies", "qualifies", "inhibits", "prevents", "contradicts", "undercuts", "counterexample", "prerequisite", "part_of", "transforms_to", "analogous_to", "predicts", "measures", "implements"}
FOUNDATION_LANES = {
    "reasoning.deductive", "reasoning.inductive", "reasoning.abductive", "reasoning.analogical",
    "reasoning.causal", "reasoning.counterfactual", "reasoning.probabilistic", "thinking.bottom_up",
    "thinking.lateral", "philosophy.analysis", "rhetoric.analysis", "geometry.structural",
    "psychology.evidence", "neuroscience.evidence",
    "creativity.generation_selection", "creativity.conceptual_blending", "creativity.constraint_based",
    "creativity.novelty_value", "creativity.problem_framing", "creativity.tension_transformation",
    "creativity.memory_recombination"
}


def normalized_statement(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def load_records() -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for path in sorted((ROOT / "curricula").rglob("*.jsonl")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                errors.append(f"{path}:{line_number}: {error}")
                continue
            record["__location"] = f"{path.relative_to(ROOT)}:{line_number}"
            records.append(record)
    if not records:
        errors.append("no curriculum records found")
    return records, errors


def main() -> int:
    records, errors = load_records()
    lanes = {lane["id"] for lane in load_json(LANE_CATALOG)["lanes"]}
    domains_data = load_json(DOMAIN_CATALOG)["domains"]
    domains = {domain["id"] for domain in domains_data}
    subjects = {subfield["id"] for domain in domains_data for subfield in domain["subfields"]}
    axes = {axis["id"] for axis in load_json(COVERAGE_AXES)["axes"]}
    sources = {source["source_id"] for source in load_json(ROOT / "sources" / "source-registry.json")["sources"]}

    ids: dict[str, str] = {}
    split_groups: dict[str, set[str]] = collections.defaultdict(set)
    normalized: dict[str, set[str]] = collections.defaultdict(set)
    node_ids: set[str] = set()
    lane_nodes: collections.Counter[str] = collections.Counter()
    lane_controls: collections.Counter[str] = collections.Counter()
    split_counts: collections.Counter[str] = collections.Counter()
    kind_counts: collections.Counter[str] = collections.Counter()

    for record in records:
        location = record.pop("__location")
        missing = REQUIRED_FIELDS - set(record)
        extra = set(record) - ALLOWED_FIELDS
        if missing:
            errors.append(f"{location}: missing fields {sorted(missing)}")
        if extra:
            errors.append(f"{location}: extra fields {sorted(extra)}")
        record_id = record.get("record_id")
        if not isinstance(record_id, str) or not ID.fullmatch(record_id):
            errors.append(f"{location}: invalid record_id")
            continue
        if record_id in ids:
            errors.append(f"{location}: duplicate record_id also at {ids[record_id]}")
        ids[record_id] = location
        if record.get("schema_version") != 1:
            errors.append(f"{location}: schema_version must be 1")
        if record.get("domain_id") not in domains:
            errors.append(f"{location}: unknown domain {record.get('domain_id')}")
        if record.get("subject_id") not in subjects:
            errors.append(f"{location}: unknown subject {record.get('subject_id')}")
        record_lanes = record.get("lanes")
        if not isinstance(record_lanes, list) or not record_lanes or len(record_lanes) != len(set(record_lanes)):
            errors.append(f"{location}: lanes must be a non-empty unique list")
            record_lanes = []
        unknown_lanes = set(record_lanes) - lanes
        if unknown_lanes:
            errors.append(f"{location}: unknown lanes {sorted(unknown_lanes)}")
        if record.get("record_kind") not in KINDS:
            errors.append(f"{location}: invalid record_kind")
        if record.get("epistemic_class") not in EPISTEMIC:
            errors.append(f"{location}: invalid epistemic_class")
        split = record.get("split")
        if split not in SPLITS:
            errors.append(f"{location}: invalid split")
        else:
            split_counts[split] += 1
        split_group = record.get("split_group")
        if not isinstance(split_group, str) or not ID.fullmatch(split_group):
            errors.append(f"{location}: invalid split_group")
        else:
            split_groups[split_group].add(str(split))
        if not isinstance(record.get("statement"), str) or not record["statement"].strip():
            errors.append(f"{location}: empty statement")
        else:
            normalized[normalized_statement(record["statement"])].add(str(split))
        record_axes = record.get("coverage_axes", [])
        if not record_axes or len(record_axes) != len(set(record_axes)) or set(record_axes) - axes:
            errors.append(f"{location}: invalid coverage_axes")
        source_ids = record.get("source_ids")
        if not isinstance(source_ids, list) or len(source_ids) != len(set(source_ids)):
            errors.append(f"{location}: source_ids must be a unique list")
            source_ids = []
        if set(source_ids) - sources:
            errors.append(f"{location}: unknown source IDs {sorted(set(source_ids) - sources)}")
        synthetic = record.get("epistemic_class") == "synthetic_control"
        if synthetic != (record.get("synthetic") is True) or (synthetic and source_ids) or (not synthetic and not source_ids):
            errors.append(f"{location}: synthetic/evidence boundary is invalid")
        kind = record.get("record_kind")
        kind_counts[str(kind)] += 1
        if kind == "relation":
            relation = record.get("relation")
            if not isinstance(relation, dict):
                errors.append(f"{location}: relation record has no relation")
            else:
                if relation.get("kind") not in RELATIONS or relation.get("polarity") not in {-1, 0, 1} or relation.get("direction") not in {"forward", "bidirectional"}:
                    errors.append(f"{location}: invalid typed relation")
        else:
            node_ids.add(record_id)
            for lane in record_lanes:
                lane_nodes[lane] += 1
                if kind == "synthetic_control":
                    lane_controls[lane] += 1

    for group, group_splits in split_groups.items():
        if len(group_splits) > 1:
            errors.append(f"split group {group} crosses splits: {sorted(group_splits)}")
    for statement, statement_splits in normalized.items():
        if statement and len(statement_splits) > 1:
            errors.append(f"normalized statement leaks across splits {sorted(statement_splits)}: {statement[:100]}")
    for record in records:
        if record.get("record_kind") == "relation" and isinstance(record.get("relation"), dict):
            for endpoint in (record["relation"].get("source_node"), record["relation"].get("target_node")):
                if endpoint not in node_ids:
                    errors.append(f"relation {record.get('record_id')} references missing node {endpoint}")
    missing_foundations = sorted(lane for lane in FOUNDATION_LANES if lane_nodes[lane] == 0 or lane_controls[lane] == 0)
    if missing_foundations:
        errors.append(f"foundation lanes lack nodes or controls: {missing_foundations}")
    for required_split in SPLITS:
        if split_counts[required_split] == 0:
            errors.append(f"required split {required_split} is empty")

    print(f"records: {len(records)}")
    print(f"kinds: {dict(sorted(kind_counts.items()))}")
    print(f"splits: {dict(sorted(split_counts.items()))}")
    print(f"foundation lanes with nodes: {sum(lane_nodes[lane] > 0 for lane in FOUNDATION_LANES)}/{len(FOUNDATION_LANES)}")
    print(f"foundation lanes with controls: {sum(lane_controls[lane] > 0 for lane in FOUNDATION_LANES)}/{len(FOUNDATION_LANES)}")
    print(f"valid: {not errors}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

