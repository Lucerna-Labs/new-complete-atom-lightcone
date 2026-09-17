#!/usr/bin/env python3
"""Record hash-bound CPU diagnostics without promoting them to TPU evidence."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
from pathlib import Path

from registry_lib import ROOT
from world_catalog import WORLD_CONFIGS


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--receipt-id")
    args = parser.parse_args()
    paths = (
        {"catalog": args.summary}
        if args.summary
        else {
            "curated": ROOT / "artifacts" / "smoke" / "protocol-v3-jax" / "summary.json",
            "taxonomy": ROOT / "artifacts" / "smoke" / "taxonomy-v3-jax" / "summary.json",
        }
    )
    summaries = {
        name: json.loads(path.read_text(encoding="utf-8")) for name, path in paths.items()
    }
    results = [
        row for summary in summaries.values() for row in summary["results"]
    ]
    expected = len(WORLD_CONFIGS) if args.summary else 177
    if len(results) != expected or len({row["world_id"] for row in results}) != expected:
        raise RuntimeError(f"local diagnostic summaries do not close over {expected} unique worlds")
    failures = [
        row
        for row in results
        if row["status"] != "non_tpu_gates_passed"
        or row.get("failed_non_tpu_gates")
        or row.get("failed_shadow_gates")
        or row.get("shadow_serialized_valid") is not True
    ]
    if failures:
        raise RuntimeError(f"local diagnostic failures remain: {len(failures)}")
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    dirty = bool(
        subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            cwd=ROOT,
            text=True,
        ).strip()
    )
    receipt = {
        "schema_version": 1,
        "receipt_id": args.receipt_id or "protocol-v3-cpu-diagnostic-20260911",
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "diagnostic_only": True,
        "accelerator_accepted": False,
        "framework": {"name": "jax", "version": "0.11.1", "backend": "cpu"},
        "source_revision": revision,
        "source_dirty": dirty,
        "configured_training_steps": sum(
            int(json.loads((ROOT / "trainer" / "configs" / config_name).read_text(encoding="utf-8"))["steps"])
            for _world_id, config_name in (WORLD_CONFIGS if args.summary else WORLD_CONFIGS[:-1])
        ),
        "world_count": len(results),
        "non_tpu_pass_count": len(results),
        "non_tpu_failure_count": 0,
        "shadow_pass_count": len(results),
        "shadow_failure_count": 0,
        "summary_hashes": {name: sha256(path) for name, path in paths.items()},
        "runs": [
            {
                "world_id": row["world_id"],
                "run_id": row["run_id"],
                "shadow_projection_id": row["shadow_projection_id"],
            }
            for row in sorted(results, key=lambda item: item["world_id"])
        ],
        "limitations": [
            "CPU diagnostics are not Kaggle TPU evidence and cannot advance accelerator status.",
            "The source tree was dirty when these local diagnostics ran; a clean revision must reproduce them before accelerator acceptance.",
            "Adapter conformance remains separate from world-training diagnostics."
        ],
    }
    output = args.output or ROOT / "receipts" / "local-diagnostics" / "protocol-v3-cpu-20260911.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in receipt.items() if key != "runs"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
