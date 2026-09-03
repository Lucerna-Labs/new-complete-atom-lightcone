#!/usr/bin/env python3
"""Partition authoritative discoveries into deterministic curriculum work shards."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

from registry_lib import COVERAGE_AXES, ROOT, load_json


DISCOVERY = ROOT / "ontology" / "discovery-ledger.jsonl"
OUTPUT = ROOT / "plans" / "taxonomy-training-shards"


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_discoveries() -> list[dict[str, Any]]:
    return [json.loads(line) for line in DISCOVERY.read_text(encoding="utf-8").splitlines() if line.strip()]


def profile_for(source_id: str, domain_hint: str) -> str:
    if source_id == "msc2020":
        return "formal-mathematics-proof-and-example-v1"
    if domain_hint in {"medicine-health", "psychology-cognitive-science", "neuroscience-neurology"}:
        return "biomedical-evidence-and-clinical-boundary-v1"
    return "sourced-causal-world-v1"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=256)
    args = parser.parse_args()
    if not 32 <= args.size <= 2048:
        parser.error("--size must be within 32..=2048")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    axes = [axis["id"] for axis in load_json(COVERAGE_AXES)["axes"]]
    groups: dict[tuple[str, str], list[dict[str, Any]]] = collections.defaultdict(list)
    for record in read_discoveries():
        groups[(record["source_id"], record["domain_hint"])].append(record)
    index_rows = []
    seen: set[str] = set()
    for (source_id, domain_hint), records in sorted(groups.items()):
        records.sort(key=lambda record: record["discovery_id"])
        for part, start in enumerate(range(0, len(records), args.size), start=1):
            chunk = records[start : start + args.size]
            shard_id = f"{source_id}-{domain_hint}-{part:04d}"
            entries = []
            for record in chunk:
                discovery_id = record["discovery_id"]
                if discovery_id in seen:
                    raise RuntimeError(f"discovery repeated across shards: {discovery_id}")
                seen.add(discovery_id)
                entries.append({
                    "discovery_id": discovery_id,
                    "external_id": record["external_id"],
                    "label": record["label"],
                    "parent_external_ids": record.get("parent_external_ids", []),
                })
            shard = {
                "schema_version": 1,
                "shard_id": shard_id,
                "status": "planned",
                "source_id": source_id,
                "domain_hint": domain_hint,
                "curriculum_profile": profile_for(source_id, domain_hint),
                "entry_count": len(entries),
                "entries": entries,
                "required_coverage_axes": axes,
                "required_splits": ["train", "validation", "sealed_test", "cross_domain_holdout"],
                "required_controls": [
                    "definition_and_scope",
                    "positive_mechanism",
                    "counterexample_or_boundary",
                    "adversarial_misuse",
                    "unknown_abstention",
                    "cross_domain_bridge"
                ],
                "acceptance": {
                    "source_provenance_closed": True,
                    "split_groups_isolated": True,
                    "tpu_receipt_required": True,
                    "sealed_gate_required": True,
                    "adapter_independent": True
                }
            }
            path = OUTPUT / f"{shard_id}.json"
            path.write_text(json.dumps(shard, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            index_rows.append({
                "shard_id": shard_id,
                "source_id": source_id,
                "domain_hint": domain_hint,
                "entry_count": len(entries),
                "sha256": file_hash(path),
                "path": path.name,
                "status": "planned"
            })
    expected = {record["discovery_id"] for record in read_discoveries()}
    if seen != expected:
        raise RuntimeError(f"sharding coverage mismatch: missing={len(expected - seen)} extra={len(seen - expected)}")
    counts = collections.Counter(row["source_id"] for row in index_rows)
    index = {
        "schema_version": 1,
        "discovery_ledger_sha256": file_hash(DISCOVERY),
        "shard_size": args.size,
        "shard_count": len(index_rows),
        "entry_count": len(seen),
        "source_shard_counts": dict(sorted(counts.items())),
        "shards": index_rows,
    }
    (OUTPUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: index[key] for key in ("shard_size", "shard_count", "entry_count", "source_shard_counts")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

