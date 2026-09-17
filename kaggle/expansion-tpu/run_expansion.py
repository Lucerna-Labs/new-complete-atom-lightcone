#!/usr/bin/env python3
"""Run every pre-registered expansion world in one Kaggle TPU allocation."""

from __future__ import annotations

import json
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path


def exactly_one(pattern: str) -> Path:
    matches = sorted(Path("/kaggle/input").rglob(pattern))
    if len(matches) != 1:
        raise RuntimeError(f"expected one {pattern}, found {len(matches)}")
    return matches[0]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    archive = exactly_one("world-bundles.zip")
    trainer = exactly_one("train_jax.py")
    shadow_projection = exactly_one("shadow_projection.py")
    semantic_geometry = exactly_one("semantic_geometry.py")
    expansion_manifest = json.loads(exactly_one("expansion-manifest.json").read_text(encoding="utf-8"))
    if sha256(trainer) != expansion_manifest["trainer_sha256"]:
        raise RuntimeError("trainer hash differs from expansion manifest")
    if sha256(shadow_projection) != expansion_manifest["shadow_projection_sha256"]:
        raise RuntimeError("shadow projection module hash differs from expansion manifest")
    if sha256(semantic_geometry) != expansion_manifest["semantic_geometry_sha256"]:
        raise RuntimeError("semantic geometry module hash differs from expansion manifest")
    input_root = Path("/kaggle/working/expansion-input")
    output_root = Path("/kaggle/working/lightcone-output")
    input_root.mkdir(parents=True, exist_ok=True)
    output_root.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(input_root)

    results = []
    for world in expansion_manifest["worlds"]:
        world_id = world["world_id"]
        bundle_root = input_root / world_id
        output = output_root / world_id
        command = [
            sys.executable,
            str(trainer),
            "--input",
            str(bundle_root),
            "--config",
            str(bundle_root / "training-config.json"),
            "--output",
            str(output),
            "--require-tpu",
        ]
        completed = subprocess.run(command, check=False)
        receipt_path = output / "training-receipt.json"
        if receipt_path.is_file():
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            results.append({
                "world_id": world_id,
                "process_return_code": completed.returncode,
                "status": receipt["status"],
                "run_id": receipt["run_id"],
                "failed_gates": receipt.get("failure", {}).get("failed_gates", []) if receipt.get("failure") else [],
            })
        else:
            results.append({
                "world_id": world_id,
                "process_return_code": completed.returncode,
                "status": "error_without_receipt",
                "run_id": None,
                "failed_gates": [],
            })
    summary = {
        "schema_version": 1,
        "kernel_ref": expansion_manifest["kernel_ref"],
        "kernel_version": expansion_manifest["kernel_version"],
        "source_revision": expansion_manifest["source_revision"],
        "trainer_sha256": expansion_manifest["trainer_sha256"],
        "shadow_projection_sha256": expansion_manifest["shadow_projection_sha256"],
        "semantic_geometry_sha256": expansion_manifest["semantic_geometry_sha256"],
        "world_count": len(results),
        "passed_count": sum(result["status"] == "passed" for result in results),
        "failed_count": sum(result["status"] != "passed" for result in results),
        "results": results,
    }
    (output_root / "expansion-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
