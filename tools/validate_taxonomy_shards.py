#!/usr/bin/env python3
"""Prove that taxonomy work shards cover every discovery exactly once."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from registry_lib import ROOT


DISCOVERY = ROOT / "ontology" / "discovery-ledger.jsonl"
SHARDS = ROOT / "plans" / "taxonomy-training-shards"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    index = json.loads((SHARDS / "index.json").read_text(encoding="utf-8"))
    if index.get("discovery_ledger_sha256") != file_hash(DISCOVERY):
        errors.append("shard index is stale relative to discovery ledger")
    expected = {
        json.loads(line)["discovery_id"]
        for line in DISCOVERY.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    observed: set[str] = set()
    duplicate = set()
    for row in index.get("shards", []):
        path = SHARDS / row["path"]
        if not path.is_file() or file_hash(path) != row["sha256"]:
            errors.append(f"missing or changed shard {row.get('shard_id')}")
            continue
        shard = json.loads(path.read_text(encoding="utf-8"))
        if shard.get("status") not in {"planned", "authored"} or shard.get("entry_count") != len(shard.get("entries", [])):
            errors.append(f"invalid shard metadata {row.get('shard_id')}")
        if row.get("status") != shard.get("status"):
            errors.append(f"shard/index status mismatch {row.get('shard_id')}")
        if shard.get("status") == "authored":
            curriculum = ROOT / str(shard.get("curriculum_path", ""))
            if (
                not curriculum.is_file()
                or file_hash(curriculum) != shard.get("curriculum_sha256")
                or row.get("curriculum_sha256") != shard.get("curriculum_sha256")
            ):
                errors.append(f"missing or changed authored curriculum {row.get('shard_id')}")
            if (
                shard.get("mapped_entry_count") != shard.get("entry_count")
                or row.get("mapped_entry_count") != row.get("entry_count")
                or not shard.get("world_id")
            ):
                errors.append(f"authored shard is not mapped or world-bound {row.get('shard_id')}")
        for entry in shard.get("entries", []):
            discovery_id = entry["discovery_id"]
            if discovery_id in observed:
                duplicate.add(discovery_id)
            observed.add(discovery_id)
    if duplicate:
        errors.append(f"duplicate discoveries across shards: {len(duplicate)}")
    if observed != expected:
        errors.append(f"shard closure mismatch: missing={len(expected - observed)} extra={len(observed - expected)}")
    if index.get("entry_count") != len(observed) or index.get("shard_count") != len(index.get("shards", [])):
        errors.append("shard index counts differ")
    print(f"shards: {len(index.get('shards', []))}")
    print(f"covered discoveries: {len(observed)}")
    print(f"duplicates: {len(duplicate)}")
    print(f"valid: {not errors}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
