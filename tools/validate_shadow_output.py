#!/usr/bin/env python3
"""Independently validate serialized 48D-to-4D shadow output artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "trainer"))

from shadow_projection import validate_serialized_shadow  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    names = (
        "coordinates.json",
        "shadow-projection.json",
        "shadow-coordinates.json",
        "shadow-observers.json",
        "shadow-metrics.json",
        "training-receipt.json",
    )
    missing = [name for name in names if not (args.output / name).is_file()]
    errors = [f"missing artifact {name}" for name in missing]
    artifacts: dict[str, object] = {}
    if not missing:
        try:
            artifacts = {
                name: json.loads((args.output / name).read_text(encoding="utf-8"))
                for name in names
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
            receipt = artifacts["training-receipt.json"]
            projection = receipt.get("shadow_projection", {})
            linked = {
                "projection_artifact_sha256": "shadow-projection.json",
                "coordinate_artifact_sha256": "shadow-coordinates.json",
                "observer_artifact_sha256": "shadow-observers.json",
                "metrics_artifact_sha256": "shadow-metrics.json",
            }
            for field, name in linked.items():
                observed = sha256(args.output / name)
                if projection.get(field) != observed:
                    errors.append(f"receipt {field} does not bind {name}")
                if receipt.get("output_hashes", {}).get(name) != observed:
                    errors.append(f"output hash does not bind {name}")
        except (OSError, json.JSONDecodeError, TypeError, ValueError, KeyError) as error:
            errors.append(str(error))
    if not args.quiet:
        metrics = artifacts.get("shadow-metrics.json", {})
        print(
            json.dumps(
                {
                    "projection_id": metrics.get("projection_id"),
                    "source_dimensions": metrics.get("source_dimensions"),
                    "target_dimensions": metrics.get("target_dimensions"),
                    "observer_only": metrics.get("observer_only"),
                    "non_expansive": metrics.get("non_expansive"),
                    "deterministic_replay": metrics.get("deterministic_replay"),
                    "valid": not errors,
                    "errors": errors,
                },
                indent=2,
            )
        )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
