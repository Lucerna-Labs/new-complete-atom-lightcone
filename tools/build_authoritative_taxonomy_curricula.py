#!/usr/bin/env python3
"""Materialize every planned MSC/MeSH discovery as a source-bound world record.

The generated records preserve what the source actually establishes.  A MeSH
scope note is retained as a versioned descriptor definition; an MSC row is
retained as a classification statement.  Neither is promoted to causal truth.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from registry_lib import ROOT, file_hash, load_json


DOWNLOADS = ROOT / "artifacts" / "downloads" / "taxonomies"
SHARDS = ROOT / "plans" / "taxonomy-training-shards"
OUTPUT = ROOT / "curricula" / "authoritative-taxonomies"
DISCOVERY = ROOT / "ontology" / "discovery-ledger.jsonl"
DISCOVERY_MANIFEST = ROOT / "ontology" / "discovery-manifest.json"


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def canonical_jsonl(records: list[dict[str, Any]]) -> str:
    return "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
        for record in sorted(records, key=lambda item: item["record_id"])
    )


def mesh_details(path: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    with gzip.open(path, "rb") as handle:
        for _event, element in ET.iterparse(handle, events=("end",)):
            if element.tag != "DescriptorRecord":
                continue
            ui = element.findtext("DescriptorUI")
            label = element.findtext("DescriptorName/String")
            if not ui or not label:
                element.clear()
                continue
            preferred = None
            concepts = element.findall("ConceptList/Concept")
            for concept in concepts:
                if concept.get("PreferredConceptYN") == "Y":
                    preferred = concept
                    break
            if preferred is None:
                preferred = concepts[0] if concepts else None
            scope_note = preferred.findtext("ScopeNote") if preferred is not None else None
            aliases = sorted(
                {
                    term.text.strip()
                    for term in element.findall("ConceptList/Concept/TermList/Term/String")
                    if term.text and term.text.strip() and term.text.strip() != label.strip()
                }
            )
            introduced = element.find("DateIntroduced")
            updated = element.find("LastUpdated")

            def date_value(node: ET.Element | None) -> str | None:
                if node is None:
                    return None
                year = node.findtext("Year")
                month = node.findtext("Month") or "01"
                day = node.findtext("Day") or "01"
                return f"{year}-{month}-{day}" if year else None

            result[f"mesh2026.{ui.lower()}"] = {
                "label": label.strip(),
                "description": scope_note.strip() if scope_note else None,
                "aliases": aliases,
                "introduced": date_value(introduced),
                "updated": date_value(updated),
            }
            element.clear()
    return result


def msc_details(path: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="iso-8859-1", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            code = row["code"].strip()
            result[f"msc2020.{slug(code)}"] = {
                "label": row["text"].strip(),
                "description": row["description"].strip(),
                "aliases": [],
                "introduced": "2020-01-01",
                "updated": "2020-01-01",
            }
    return result


def subject_router() -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    catalog = load_json(ROOT / "ontology" / "domain-catalog.json")
    subjects = {
        domain["id"]: [subfield["id"] for subfield in domain["subfields"]]
        for domain in catalog["domains"]
    }
    lanes = {domain["id"]: domain["lanes"] for domain in catalog["domains"]}
    return subjects, lanes


def route_subject(domain_id: str, text: str, subjects: dict[str, list[str]]) -> str:
    candidates = subjects[domain_id]
    words = set(re.findall(r"[a-z0-9]+", text.lower()))
    ranked: list[tuple[int, int, str]] = []
    for index, candidate in enumerate(candidates):
        label_words = set(re.findall(r"[a-z0-9]+", candidate.rsplit(".", 1)[-1]))
        ranked.append((len(words & label_words), -index, candidate))
    return max(ranked)[2]


def split_for(index: int) -> str:
    position = index % 20
    if position == 0:
        return "train"
    if position == 1:
        return "validation"
    if position == 2:
        return "sealed_test"
    if position == 3:
        return "cross_domain_holdout"
    return "train"


def record_base(
    *,
    record_id: str,
    world_id: str,
    domain_id: str,
    subject_id: str,
    lanes: list[str],
    kind: str,
    epistemic_class: str,
    statement: str,
    split: str,
    source_id: str | None,
    coverage_axes: list[str],
    label: str,
    limitations: list[str],
) -> dict[str, Any]:
    record = {
        "schema_version": 1,
        "record_id": record_id,
        "world_id": world_id,
        "domain_id": domain_id,
        "subject_id": subject_id,
        "lanes": lanes,
        "record_kind": kind,
        "epistemic_class": epistemic_class,
        "label": label,
        "statement": statement,
        "aliases": [],
        "coverage_axes": coverage_axes,
        "source_ids": [source_id] if source_id else [],
        "scope": "authoritative taxonomy coverage and routing",
        "limitations": limitations,
        "as_of": "2026-09-03",
        "version_boundary": f"{source_id or 'synthetic'}-taxonomy-v0",
        "split_group": record_id,
        "split": split,
        "tags": ["authoritative-taxonomy", domain_id],
    }
    if epistemic_class == "synthetic_control":
        record["synthetic"] = True
    return record


def relation_record(
    *,
    record_id: str,
    world_id: str,
    domain_id: str,
    subject_id: str,
    lanes: list[str],
    source_id: str,
    source_node: str,
    target_node: str,
    relation: str,
    statement: str,
    split: str,
    cross_domain: bool = False,
) -> dict[str, Any]:
    record = record_base(
        record_id=record_id,
        world_id=world_id,
        domain_id=domain_id,
        subject_id=subject_id,
        lanes=lanes,
        kind="relation",
        epistemic_class="formal" if source_id == "msc2020" else "established",
        statement=statement,
        split=split,
        source_id=source_id,
        coverage_axes=[
            "cross_domain_composition" if cross_domain else "within_domain_composition",
            "representations_transformations",
        ],
        label=record_id.rsplit(".", 1)[-1].replace("-", " "),
        limitations=[
            "The edge records a published classification relation, not a universal causal or physical part-whole claim."
        ],
    )
    record["relation"] = {
        "source_node": source_node,
        "target_node": target_node,
        "kind": relation,
        "polarity": 1,
        "direction": "forward",
        "conditions": ["the declared taxonomy version is the interpretation boundary"],
        "exceptions": ["later taxonomy revisions may relocate or retire the descriptor"],
    }
    return record


def main() -> int:
    input_manifest = load_json(ROOT / "sources" / "taxonomy-inputs.json")
    for item in input_manifest["inputs"]:
        path = DOWNLOADS / item["local_name"]
        if file_hash(path) != item["sha256"]:
            raise RuntimeError(f"authoritative input hash mismatch for {item['source_id']}")
    details = {
        **msc_details(DOWNLOADS / "MSC_2020.csv"),
        **mesh_details(DOWNLOADS / "desc2026.gz"),
    }
    discoveries = {
        record["discovery_id"]: record
        for record in (
            json.loads(line) for line in DISCOVERY.read_text(encoding="utf-8").splitlines() if line.strip()
        )
    }
    if set(details) != set(discoveries):
        raise RuntimeError(
            f"taxonomy detail closure mismatch: details={len(details)} discoveries={len(discoveries)}"
        )
    subjects, domain_lanes = subject_router()
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    shard_index = load_json(SHARDS / "index.json")
    index_rows: list[dict[str, Any]] = []
    mapped: set[str] = set()
    total_records = 0
    total_scope_notes = 0
    for row in shard_index["shards"]:
        shard_path = SHARDS / row["path"]
        shard = load_json(shard_path)
        world_id = f"taxonomy-{shard['shard_id']}-v0"
        source_id = shard["source_id"]
        domain_id = shard["domain_hint"]
        lanes = list(dict.fromkeys([*domain_lanes[domain_id], "geometry.structural", "thinking.bottom_up"]))
        source_title = "MSC 2020" if source_id == "msc2020" else "MeSH 2026"
        limitations = [
            f"This world preserves the {source_title} classification boundary and is not a substitute for specialist primary literature.",
            "Taxonomy hierarchy is not automatically a causal, compositional, diagnostic, or treatment claim.",
            "Open-world discovery continues after this versioned inventory closes.",
        ]
        entries = shard["entries"]
        local_ids = {entry["discovery_id"] for entry in entries}
        root_id = f"taxonomy.{shard['shard_id']}.root"
        default_subject = route_subject(domain_id, shard["domain_hint"], subjects)
        records: list[dict[str, Any]] = [
            record_base(
                record_id=root_id,
                world_id=world_id,
                domain_id=domain_id,
                subject_id=default_subject,
                lanes=lanes,
                kind="concept",
                epistemic_class="formal" if source_id == "msc2020" else "established",
                statement=f"{source_title} shard {shard['shard_id']} is a versioned routing world containing {len(entries)} published taxonomy entries.",
                split="train",
                source_id=source_id,
                coverage_axes=["definitions_scope", "representations_transformations", "history_versions"],
                label=f"{source_title} {domain_id} shard root",
                limitations=limitations,
            )
        ]
        concept_ids: dict[str, str] = {}
        routed_subjects: dict[str, str] = {}
        splits: dict[str, str] = {}
        for index, entry in enumerate(entries):
            discovery_id = entry["discovery_id"]
            discovery = discoveries[discovery_id]
            detail = details[discovery_id]
            subject_id = route_subject(
                domain_id,
                f"{detail['label']} {detail.get('description') or ''}",
                subjects,
            )
            split = split_for(index)
            node_id = f"taxonomy.{source_id}.{slug(discovery['external_id'])}"
            concept_ids[discovery_id] = node_id
            routed_subjects[discovery_id] = subject_id
            splits[discovery_id] = split
            description = detail.get("description")
            if source_id == "mesh2026" and description:
                statement = (
                    f"{detail['label']} ({discovery['external_id']}) — MeSH 2026 scope note: {description}"
                )
                total_scope_notes += 1
            else:
                statement = (
                    f"{detail['label']} ({discovery['external_id']}) — {source_title} registers this published classification entry: "
                    f"{description or detail['label']}."
                )
            concept = record_base(
                record_id=node_id,
                world_id=world_id,
                domain_id=domain_id,
                subject_id=subject_id,
                lanes=lanes,
                kind="concept",
                epistemic_class="formal" if source_id == "msc2020" else "established",
                statement=statement,
                split=split,
                source_id=source_id,
                coverage_axes=["definitions_scope", "representations_transformations", "history_versions"],
                label=detail["label"],
                limitations=limitations,
            )
            concept["aliases"] = detail["aliases"][:64]
            concept["as_of"] = detail.get("updated") or "2026-09-03"
            records.append(concept)
            routing_id = f"{node_id}.evidence"
            routing = record_base(
                record_id=routing_id,
                world_id=world_id,
                domain_id=domain_id,
                subject_id=subject_id,
                lanes=lanes,
                kind="concept",
                epistemic_class="formal" if source_id == "msc2020" else "established",
                statement=(
                    f"Routing evidence for {detail['label']} ({discovery['external_id']}): "
                    f"use the versioned identifier, preferred label, declared aliases, source, and hierarchy while preserving the taxonomy limitations."
                ),
                split=split,
                source_id=source_id,
                coverage_axes=["definitions_scope", "representations_transformations", "applications_toolchains"],
                label=f"Routing evidence for {detail['label']}",
                limitations=limitations,
            )
            records.append(routing)
            records.append(
                relation_record(
                    record_id=f"{node_id}.membership",
                    world_id=world_id,
                    domain_id=domain_id,
                    subject_id=subject_id,
                    lanes=lanes,
                    source_id=source_id,
                    source_node=node_id,
                    target_node=root_id,
                    relation="part_of",
                    statement=f"{detail['label']} ({discovery['external_id']}) is included in authoritative shard {shard['shard_id']}.",
                    split=split,
                )
            )
            records.append(
                relation_record(
                    record_id=f"{node_id}.routing",
                    world_id=world_id,
                    domain_id=domain_id,
                    subject_id=subject_id,
                    lanes=lanes,
                    source_id=source_id,
                    source_node=routing_id,
                    target_node=node_id,
                    relation="supports",
                    statement=f"The {source_title} label, identifier, aliases, and scope support routing to {detail['label']} ({discovery['external_id']}).",
                    split=split,
                )
            )
            discovery["status"] = "mapped"
            discovery["mapped_coverage_ids"] = [domain_id, subject_id]
            discovery["exclusion_reason"] = None
            mapped.add(discovery_id)

        anchor_ids: dict[str, str] = {}
        for entry in entries:
            discovery_id = entry["discovery_id"]
            discovery = discoveries[discovery_id]
            for parent_external_id in discovery.get("parent_external_ids", []):
                parent_discovery_id = f"{source_id}.{slug(parent_external_id)}"
                if parent_discovery_id not in discoveries:
                    continue
                if parent_discovery_id in local_ids:
                    parent_node = concept_ids[parent_discovery_id]
                else:
                    parent_node = anchor_ids.get(parent_discovery_id)
                    if parent_node is None:
                        parent = discoveries[parent_discovery_id]
                        parent_detail = details[parent_discovery_id]
                        parent_node = f"taxonomy.{shard['shard_id']}.anchor.{source_id}.{slug(parent_external_id)}"
                        anchor_ids[parent_discovery_id] = parent_node
                        parent_subject = route_subject(
                            domain_id,
                            f"{parent_detail['label']} {parent_detail.get('description') or ''}",
                            subjects,
                        )
                        records.append(
                            record_base(
                                record_id=parent_node,
                                world_id=world_id,
                                domain_id=domain_id,
                                subject_id=parent_subject,
                                lanes=lanes,
                                kind="concept",
                                epistemic_class="formal" if source_id == "msc2020" else "established",
                                statement=f"{parent_detail['label']} ({parent_external_id}) is retained as an external {source_title} parent anchor for shard {shard['shard_id']}.",
                                split="train",
                                source_id=source_id,
                                coverage_axes=["definitions_scope", "representations_transformations", "history_versions"],
                                label=parent_detail["label"],
                                limitations=limitations,
                            )
                        )
                child_node = concept_ids[discovery_id]
                child_detail = details[discovery_id]
                parent_detail = details[parent_discovery_id]
                records.append(
                    relation_record(
                        record_id=f"{child_node}.parent.{slug(parent_external_id)}.{slug(shard['shard_id'])}",
                        world_id=world_id,
                        domain_id=domain_id,
                        subject_id=routed_subjects[discovery_id],
                        lanes=lanes,
                        source_id=source_id,
                        source_node=parent_node,
                        target_node=child_node,
                        relation="qualifies",
                        statement=f"In {source_title}, parent {parent_detail['label']} ({parent_external_id}) qualifies the classification scope of {child_detail['label']} ({discovery['external_id']}).",
                        split=splits[discovery_id],
                    )
                )

        for split in ("train", "validation", "sealed_test", "cross_domain_holdout"):
            control_id = f"taxonomy.{shard['shard_id']}.control.{split.replace('_', '-')}"
            records.append(
                record_base(
                    record_id=control_id,
                    world_id=world_id,
                    domain_id=domain_id,
                    subject_id=default_subject,
                    lanes=lanes,
                    kind="synthetic_control",
                    epistemic_class="synthetic_control",
                    statement=f"Synthetic unknown control {shard['shard_id']} {split}: an unregistered label must remain unknown rather than being forced into a nearby taxonomy descriptor.",
                    split=split,
                    source_id=None,
                    coverage_axes=["unknown_abstention", "errors_adversarial_misuse", "exceptions_boundaries"],
                    label=f"Unknown taxonomy control {split}",
                    limitations=["Synthetic negative control; it is not a sourced domain fact."],
                )
            )

        for split in ("train", "validation", "sealed_test"):
            candidate = next(
                entry for entry in entries if splits[entry["discovery_id"]] == split
            )
            discovery_id = candidate["discovery_id"]
            detail = details[discovery_id]
            example_id = f"taxonomy.{shard['shard_id']}.example.{split.replace('_', '-')}"
            records.append(
                record_base(
                    record_id=example_id,
                    world_id=world_id,
                    domain_id=domain_id,
                    subject_id=routed_subjects[discovery_id],
                    lanes=lanes,
                    kind="worked_example",
                    epistemic_class="formal" if source_id == "msc2020" else "established",
                    statement=f"Worked routing example {shard['shard_id']} {split}: match {detail['label']} ({discoveries[discovery_id]['external_id']}) to its versioned descriptor, retain its provenance and limitations, and do not convert hierarchy into causal proof.",
                    split=split,
                    source_id=source_id,
                    coverage_axes=["applications_toolchains", "deductions_predictions_execution", "unknown_abstention"],
                    label=f"Taxonomy routing example {split}",
                    limitations=limitations,
                )
            )
            records.append(
                relation_record(
                    record_id=f"{example_id}.evidence",
                    world_id=world_id,
                    domain_id=domain_id,
                    subject_id=routed_subjects[discovery_id],
                    lanes=lanes,
                    source_id=source_id,
                    source_node=concept_ids[discovery_id],
                    target_node=example_id,
                    relation="supports",
                    statement=f"The published descriptor {detail['label']} ({discoveries[discovery_id]['external_id']}) supports its bounded routing example in shard {shard['shard_id']} {split}.",
                    split=split,
                )
            )

        output_path = OUTPUT / f"{shard['shard_id']}.jsonl"
        output_path.write_text(canonical_jsonl(records), encoding="utf-8")
        total_records += len(records)
        shard["status"] = "authored"
        shard["world_id"] = world_id
        shard["curriculum_path"] = str(output_path.relative_to(ROOT))
        shard["curriculum_sha256"] = file_hash(output_path)
        shard["record_count"] = len(records)
        shard["mapped_entry_count"] = len(entries)
        shard_path.write_text(
            json.dumps(shard, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        index_rows.append(
            {
                **row,
                "status": "authored",
                "world_id": world_id,
                "curriculum_path": str(output_path.relative_to(ROOT)),
                "curriculum_sha256": file_hash(output_path),
                "record_count": len(records),
                "mapped_entry_count": len(entries),
                "sha256": file_hash(shard_path),
            }
        )

    if mapped != set(discoveries):
        raise RuntimeError(
            f"not every discovery was authored: missing={len(set(discoveries) - mapped)}"
        )
    DISCOVERY.write_text(
        "".join(
            json.dumps(discoveries[key], ensure_ascii=False, sort_keys=True) + "\n"
            for key in sorted(discoveries)
        ),
        encoding="utf-8",
    )
    manifest = load_json(DISCOVERY_MANIFEST)
    manifest["unresolved_count"] = 0
    manifest["mapped_count"] = len(mapped)
    manifest["ledger_sha256"] = file_hash(DISCOVERY)
    DISCOVERY_MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    shard_index["discovery_ledger_sha256"] = file_hash(DISCOVERY)
    shard_index["shards"] = index_rows
    shard_index["authored_shard_count"] = len(index_rows)
    shard_index["authored_record_count"] = total_records
    (SHARDS / "index.json").write_text(
        json.dumps(shard_index, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    curricula_manifest = {
        "schema_version": 1,
        "source_input_hashes": {
            item["source_id"]: item["sha256"] for item in input_manifest["inputs"]
        },
        "discovery_ledger_sha256": file_hash(DISCOVERY),
        "shard_index_sha256": file_hash(SHARDS / "index.json"),
        "world_count": len(index_rows),
        "discovery_count": len(mapped),
        "record_count": total_records,
        "mesh_scope_note_count": total_scope_notes,
        "files": {
            path.name: file_hash(path) for path in sorted(OUTPUT.glob("*.jsonl"))
        },
    }
    (OUTPUT / "manifest.json").write_text(
        json.dumps(curricula_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(curricula_manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
