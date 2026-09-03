#!/usr/bin/env python3
"""Validate an accelerator receipt and its output hashes without trusting prose."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


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
        "hyperparameters", "metrics", "gates", "output_hashes", "started_at", "finished_at"
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
    if output_root is not None:
        for relative, expected in receipt.get("output_hashes", {}).items():
            path = output_root / relative
            if not path.is_file():
                errors.append(f"missing output {relative}")
                continue
            observed = file_hash(path)
            if observed != expected:
                errors.append(f"output hash mismatch for {relative}: {observed} != {expected}")
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

