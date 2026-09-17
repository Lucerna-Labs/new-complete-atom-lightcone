#!/usr/bin/env python3
"""Validate an accelerator receipt and its output hashes without trusting prose."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "trainer"))

from shadow_projection import SHADOW_GATE_SPECS, validate_serialized_shadow  # noqa: E402


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def finite_tree(value: Any) -> bool:
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return True
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    if isinstance(value, list):
        return all(finite_tree(item) for item in value)
    if isinstance(value, dict):
        return all(finite_tree(item) for item in value.values())
    return False


def validate(receipt_path: Path, output_root: Path | None, require_passed: bool) -> list[str]:
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    required = {
        "schema_version", "run_id", "protocol_id", "status", "source_revision", "source_dirty",
        "input_hashes", "split_manifest_hash", "accelerator", "framework", "seed",
        "hyperparameters", "metrics", "gates", "output_hashes", "shadow_projection", "started_at", "finished_at"
    }
    missing = required - set(receipt)
    if missing:
        errors.append(f"missing receipt fields: {sorted(missing)}")
    if receipt.get("schema_version") != 1:
        errors.append("unsupported receipt schema")
    if require_passed and receipt.get("status") != "passed":
        errors.append(f"training status is {receipt.get('status')}, not passed")
    if receipt.get("source_dirty") is not False:
        errors.append("training source was dirty")
    accelerator = receipt.get("accelerator", {})
    if accelerator.get("platform") != "kaggle" or accelerator.get("kind") != "tpu":
        errors.append(f"accelerator is not Kaggle TPU: {accelerator}")
    if not accelerator.get("devices") or accelerator.get("device_count", 0) < 1:
        errors.append("accelerator device evidence is empty")
    framework = receipt.get("framework", {})
    if framework.get("name") != "jax" or not framework.get("version"):
        errors.append("JAX framework identity is missing")
    failed = sorted(name for name, gate in receipt.get("gates", {}).items() if gate.get("passed") is not True)
    if require_passed and failed:
        errors.append(f"pre-registered gates failed: {failed}")
    if not finite_tree(receipt.get("metrics")):
        errors.append("metrics contain non-finite or unsupported values")
    shadow = receipt.get("shadow_projection", {})
    expected_shadow = {
        "observer_only": True,
        "used_for_admission": False,
        "all_spatial": True,
        "has_time_axis": False,
        "target_dimensions": 4,
        "metric": "euclidean_l2",
        "fit_split": "train",
    }
    for field, expected in expected_shadow.items():
        if shadow.get(field) != expected:
            errors.append(f"shadow projection {field} is {shadow.get(field)!r}, expected {expected!r}")
    if not isinstance(shadow.get("source_dimensions"), int) or shadow.get("source_dimensions", 0) < 4:
        errors.append("shadow projection source dimensions are invalid")
    if not isinstance(shadow.get("deterministic_replay_sha256"), str) or len(
        shadow.get("deterministic_replay_sha256", "")
    ) != 64:
        errors.append("shadow deterministic replay hash is invalid")
    required_shadow_gates = set(SHADOW_GATE_SPECS)
    missing_shadow_gates = required_shadow_gates - set(receipt.get("gates", {}))
    if missing_shadow_gates:
        errors.append(f"missing shadow gates: {sorted(missing_shadow_gates)}")
    shadow_hash_fields = {
        "projection_artifact_sha256": "shadow-projection.json",
        "coordinate_artifact_sha256": "shadow-coordinates.json",
        "observer_artifact_sha256": "shadow-observers.json",
        "metrics_artifact_sha256": "shadow-metrics.json",
    }
    for field, relative in shadow_hash_fields.items():
        if shadow.get(field) != receipt.get("output_hashes", {}).get(relative):
            errors.append(f"shadow {field} does not bind {relative}")
    if output_root is not None:
        for relative, expected in receipt.get("output_hashes", {}).items():
            path = output_root / relative
            if not path.is_file():
                errors.append(f"missing output {relative}")
                continue
            observed = file_hash(path)
            if observed != expected:
                errors.append(f"output hash mismatch for {relative}: {observed} != {expected}")
        shadow_files = {
            name: output_root / name
            for name in (
                "coordinates.json",
                "shadow-projection.json",
                "shadow-coordinates.json",
                "shadow-observers.json",
                "shadow-metrics.json",
            )
        }
        if all(path.is_file() for path in shadow_files.values()):
            try:
                artifacts = {
                    name: json.loads(path.read_text(encoding="utf-8"))
                    for name, path in shadow_files.items()
                }
                errors.extend(
                    validate_serialized_shadow(
                        full_coordinates=artifacts["coordinates.json"],
                        projection_artifact=artifacts["shadow-projection.json"],
                        shadow_coordinates=artifacts["shadow-coordinates.json"],
                        observer_artifact=artifacts["shadow-observers.json"],
                        metrics_artifact=artifacts["shadow-metrics.json"],
                    )
                )
                if shadow.get("basis_sha256") != artifacts["shadow-projection.json"].get(
                    "basis_sha256"
                ):
                    errors.append("receipt shadow basis hash differs from projection artifact")
                if shadow.get("deterministic_replay_sha256") != artifacts[
                    "shadow-projection.json"
                ].get("deterministic_replay_sha256"):
                    errors.append("receipt replay hash differs from projection artifact")
            except (OSError, json.JSONDecodeError, TypeError, ValueError, KeyError) as error:
                errors.append(f"could not validate serialized shadow artifacts: {error}")
        else:
            missing_shadow_files = sorted(
                name for name, path in shadow_files.items() if not path.is_file()
            )
            errors.append(f"missing shadow output files: {missing_shadow_files}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--require-passed", action="store_true")
    args = parser.parse_args()
    errors = validate(args.receipt, args.output_root, args.require_passed)
    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    print(json.dumps({
        "run_id": receipt.get("run_id"),
        "status": receipt.get("status"),
        "accelerator": receipt.get("accelerator"),
        "gate_count": len(receipt.get("gates", {})),
        "valid": not errors,
        "errors": errors,
    }, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
