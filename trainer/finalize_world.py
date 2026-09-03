#!/usr/bin/env python3
"""Accept a passed TPU result and assemble an immutable verified world pack."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from common import file_hash, write_json


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_training(output: Path) -> dict[str, Any]:
    receipt_path = output / "training-receipt.json"
    subprocess.run(
        [
            "python3",
            str(ROOT / "tools" / "validate_training_receipt.py"),
            str(receipt_path),
            "--output-root",
            str(output),
            "--require-passed",
        ],
        cwd=ROOT,
        check=True,
    )
    return load_json(receipt_path)


def finalize(input_root: Path, training_output: Path, destination: Path, version: str) -> Path:
    bundle = load_json(input_root / "bundle-manifest.json")
    graph = load_json(input_root / "training-graph.json")
    receipt = validate_training(training_output)
    if bundle["world_id"] != graph["world_id"] or not receipt["run_id"].startswith(graph["world_id"] + "-"):
        raise RuntimeError("world identity differs across input and training output")
    coordinates = load_json(training_output / "coordinates.json")
    if len(coordinates["vectors"]) != bundle["node_count"]:
        raise RuntimeError("coordinate count differs from compiled node count")

    if destination.exists():
        raise RuntimeError(f"destination already exists: {destination}")
    destination.mkdir(parents=True)
    (destination / "receipts").mkdir()
    (destination / "training").mkdir()

    for name in ("nodes.jsonl", "edges.jsonl", "sources.json", "lexicon.json"):
        shutil.copy2(input_root / name, destination / name)
    shutil.copy2(training_output / "coordinates.json", destination / "coordinates.json")
    shutil.copy2(training_output / "training-receipt.json", destination / "receipts" / "training-receipt.json")
    for name in (
        "metrics.json",
        "training-curve.json",
        "relation-coordinates.json",
        "trained-node-coordinates.npy",
        "trained-relation-coordinates.npy",
    ):
        shutil.copy2(training_output / name, destination / "training" / name)

    validation = {
        "schema_version": 1,
        "world_id": graph["world_id"],
        "world_version": version,
        "training_run_id": receipt["run_id"],
        "status": "passed",
        "checks": {
            "input_bundle_hashes": True,
            "split_manifest_bound": receipt["split_manifest_hash"] == graph["split_manifest_hash"],
            "kaggle_tpu": receipt["accelerator"]["platform"] == "kaggle" and receipt["accelerator"]["kind"] == "tpu",
            "all_pre_registered_gates": all(gate["passed"] for gate in receipt["gates"].values()),
            "coordinate_count": len(coordinates["vectors"]) == bundle["node_count"],
            "adapter_independent": bool(graph["adapter_independent"]),
        },
        "limitations": [
            "Foundation lane anatomy only; the exhaustive subject ledger remains open.",
            "Adapter conformance is evaluated separately from world training.",
        ],
    }
    if not all(validation["checks"].values()):
        raise RuntimeError(f"accelerator validation failed: {validation['checks']}")
    validation_path = destination / "receipts" / "accelerator-validation.json"
    write_json(validation_path, validation)

    files = {
        str(path.relative_to(destination)): file_hash(path)
        for path in sorted(destination.rglob("*"))
        if path.is_file()
    }
    manifest = {
        "schema_version": 1,
        "world_id": graph["world_id"],
        "version": version,
        "created_at": receipt["finished_at"],
        "adapter_independent": True,
        "ontology_hash": graph["ontology_hash"],
        "domains": graph["domains"],
        "lanes": graph["lanes"],
        "node_count": bundle["node_count"],
        "edge_count": bundle["edge_count"],
        "coordinate_dimensions": coordinates["dimensions"],
        "files": files,
        "training_receipt": "receipts/training-receipt.json",
        "validation_receipts": ["receipts/accelerator-validation.json"],
        "limitations": validation["limitations"],
    }
    write_json(destination / "manifest.json", manifest)
    return destination / "manifest.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--training-output", type=Path, required=True)
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--version", default="0.1.0")
    args = parser.parse_args()
    manifest = finalize(args.input, args.training_output, args.destination, args.version)
    print(json.dumps({"world_pack": str(args.destination), "manifest_hash": file_hash(manifest)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

