#!/usr/bin/env python3
"""Compile validated curriculum records into a deterministic TPU input bundle."""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
from typing import Any

from common import canonical_hash, file_hash, normalize_text, read_jsonl, write_json, write_jsonl


ROOT = Path(__file__).resolve().parents[1]
CURRICULA = ROOT / "curricula"
SOURCES = ROOT / "sources" / "source-registry.json"
ONTOLOGY_FILES = [
    ROOT / "ontology" / "coverage-axes.json",
    ROOT / "ontology" / "domain-catalog.json",
    ROOT / "ontology" / "lane-catalog.json",
]


def collect(world_id: str) -> list[dict[str, Any]]:
    records = read_jsonl(sorted(CURRICULA.rglob("*.jsonl")))
    selected = [record for record in records if record.get("world_id") == world_id]
    if not selected:
        raise ValueError(f"no curriculum records found for world {world_id}")
    for record in selected:
        record.pop("__source", None)
    return sorted(selected, key=lambda record: record["record_id"])


def compile_bundle(world_id: str, output: Path) -> dict[str, Any]:
    records = collect(world_id)
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    lexicon: dict[str, list[str]] = collections.defaultdict(list)
    graph_nodes: list[dict[str, Any]] = []
    graph_edges: list[dict[str, Any]] = []
    negative_pairs: list[dict[str, Any]] = []
    lane_roots: dict[str, str] = {}

    for record in records:
        if record["record_id"].endswith(".root"):
            for lane in record["lanes"]:
                lane_roots.setdefault(lane, record["record_id"])

    for record in records:
        if record["record_kind"] == "relation":
            relation = record["relation"]
            edge = {
                "schema_version": 1,
                "edge_id": record["record_id"],
                "source_node": relation["source_node"],
                "target_node": relation["target_node"],
                "kind": relation["kind"],
                "polarity": relation["polarity"],
                "direction": relation["direction"],
                "conditions": relation.get("conditions", []),
                "exceptions": relation.get("exceptions", []),
                "source_ids": record["source_ids"],
            }
            edges.append(edge)
            graph_edges.append({
                "edge_id": edge["edge_id"],
                "source_node": edge["source_node"],
                "target_node": edge["target_node"],
                "relation": edge["kind"],
                "polarity": edge["polarity"],
                "direction": edge["direction"],
                "split": record["split"],
                "split_group": record["split_group"],
            })
            continue

        node = {
            "schema_version": 1,
            "node_id": record["record_id"],
            "domain_id": record["domain_id"],
            "subject_id": record["subject_id"],
            "lanes": record["lanes"],
            "label": record.get("label", record["record_id"]),
            "statement": record["statement"],
            "aliases": record.get("aliases", []),
            "epistemic_class": record["epistemic_class"],
            "source_ids": record["source_ids"],
            "scope": record.get("scope", ""),
            "limitations": record.get("limitations", []),
            "as_of": record.get("as_of"),
            "version_boundary": record.get("version_boundary"),
        }
        nodes.append(node)
        graph_nodes.append({
            "node_id": node["node_id"],
            "text": f"{node['label']}\n{node['statement']}",
            "domain_id": node["domain_id"],
            "subject_id": node["subject_id"],
            "lanes": node["lanes"],
            "epistemic_class": node["epistemic_class"],
            "tags": record.get("tags", []),
            "split": record["split"],
            "split_group": record["split_group"],
        })
        terms = {normalize_text(node["label"]), *(normalize_text(alias) for alias in node["aliases"])}
        for term in sorted(term for term in terms if term):
            lexicon[term].append(node["node_id"])
        if record["record_kind"] == "synthetic_control":
            for lane in record["lanes"]:
                root = lane_roots.get(lane)
                if root:
                    negative_pairs.append({
                        "left_node": root,
                        "right_node": node["node_id"],
                        "split": record["split"],
                        "reason": "lane_negative_control",
                    })

    node_ids = {node["node_id"] for node in nodes}
    dangling = [
        edge["edge_id"]
        for edge in edges
        if edge["source_node"] not in node_ids or edge["target_node"] not in node_ids
    ]
    if dangling:
        raise ValueError(f"compiled edges reference missing nodes: {dangling}")

    source_registry = json.loads(SOURCES.read_text(encoding="utf-8"))
    used_sources = {source_id for node in nodes for source_id in node["source_ids"]}
    used_sources.update(source_id for edge in edges for source_id in edge["source_ids"])
    compiled_sources = {
        "schema_version": 1,
        "sources": [
            source for source in source_registry["sources"] if source["source_id"] in used_sources
        ],
    }
    if {source["source_id"] for source in compiled_sources["sources"]} != used_sources:
        raise ValueError("compiled source registry did not close over source IDs")

    relation_vocab = sorted({edge["relation"] for edge in graph_edges})
    domain_ids = sorted({node["domain_id"] for node in nodes})
    lane_ids = sorted({lane for node in nodes for lane in node["lanes"]})
    split_counts = collections.Counter(record["split"] for record in records)
    split_groups: dict[str, list[str]] = collections.defaultdict(list)
    for record in records:
        split_groups[record["split"]].append(record["split_group"])
    split_manifest = {
        "schema_version": 1,
        "world_id": world_id,
        "strategy": "mechanism groups fixed before accelerator training; final lane transition and alternating controls held out",
        "counts": dict(sorted(split_counts.items())),
        "groups": {split: sorted(set(groups)) for split, groups in sorted(split_groups.items())},
        "record_hash": canonical_hash(records),
    }
    unique_negative_pairs = {
        (pair["left_node"], pair["right_node"], pair["split"], pair["reason"]): pair
        for pair in negative_pairs
    }
    negative_pairs = list(unique_negative_pairs.values())
    training_graph = {
        "schema_version": 1,
        "world_id": world_id,
        "adapter_independent": True,
        "nodes": graph_nodes,
        "edges": graph_edges,
        "negative_pairs": sorted(negative_pairs, key=lambda pair: (pair["split"], pair["left_node"], pair["right_node"])),
        "relation_vocab": relation_vocab,
        "domains": domain_ids,
        "lanes": lane_ids,
        "split_manifest_hash": canonical_hash(split_manifest),
        "ontology_hash": canonical_hash({path.name: json.loads(path.read_text(encoding="utf-8")) for path in ONTOLOGY_FILES}),
    }

    output.mkdir(parents=True, exist_ok=True)
    write_jsonl(output / "records.jsonl", records)
    write_jsonl(output / "nodes.jsonl", nodes)
    write_jsonl(output / "edges.jsonl", edges)
    write_json(output / "sources.json", compiled_sources)
    write_json(output / "lexicon.json", {"schema_version": 1, "entries": {term: sorted(set(ids)) for term, ids in sorted(lexicon.items())}})
    write_json(output / "split-manifest.json", split_manifest)
    write_json(output / "training-graph.json", training_graph)
    hashes = {
        path.name: file_hash(path)
        for path in sorted(output.iterdir())
        if path.is_file() and path.name != "bundle-manifest.json"
    }
    bundle = {
        "schema_version": 1,
        "world_id": world_id,
        "adapter_independent": True,
        "record_count": len(records),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "negative_pair_count": len(negative_pairs),
        "domains": domain_ids,
        "lanes": lane_ids,
        "files": hashes,
    }
    write_json(output / "bundle-manifest.json", bundle)
    return bundle


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--world-id", default="foundation-lanes-v0")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or ROOT / "artifacts" / "staging" / args.world_id / "input"
    bundle = compile_bundle(args.world_id, output)
    print(json.dumps(bundle, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
