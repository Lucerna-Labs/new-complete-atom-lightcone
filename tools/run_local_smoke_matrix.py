#!/usr/bin/env python3
"""Compile and CPU-smoke every world without claiming accelerator acceptance."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from registry_lib import ROOT
from world_catalog import FOUNDATION_WORLD_CONFIGS, TAXONOMY_WORLD_CONFIGS, WORLD_CONFIGS


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--world", action="append", default=[])
    parser.add_argument("--require-non-tpu-pass", action="store_true")
    parser.add_argument("--curated-only", action="store_true")
    parser.add_argument("--taxonomy-only", action="store_true")
    parser.add_argument(
        "--reuse-compiled",
        action="store_true",
        help="reuse bundles already produced by a successful package preflight",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT / "artifacts" / "smoke" / "matrix",
    )
    parser.add_argument("--partition-count", type=int, default=1)
    parser.add_argument("--partition-index", type=int, default=0)
    args = parser.parse_args()
    if args.curated_only and args.taxonomy_only:
        parser.error("--curated-only and --taxonomy-only are mutually exclusive")
    if args.partition_count < 1 or not 0 <= args.partition_index < args.partition_count:
        parser.error("partition index must be within 0..partition-count-1")
    selected = set(args.world)
    unknown = selected - {world for world, _config in WORLD_CONFIGS}
    if unknown:
        parser.error(f"unknown worlds: {sorted(unknown)}")

    catalog = (
        FOUNDATION_WORLD_CONFIGS
        if args.curated_only
        else TAXONOMY_WORLD_CONFIGS
        if args.taxonomy_only
        else WORLD_CONFIGS
    )
    catalog = [
        pair
        for position, pair in enumerate(catalog)
        if position % args.partition_count == args.partition_index
    ]
    results = []
    for position, (world_id, config_name) in enumerate(catalog, start=1):
        if selected and world_id not in selected:
            continue
        compiled_graph = ROOT / "artifacts" / "staging" / world_id / "input" / "training-graph.json"
        if not args.reuse_compiled or not compiled_graph.is_file():
            subprocess.run(
                [sys.executable, str(ROOT / "trainer" / "compile_curriculum.py"), "--world-id", world_id],
                cwd=ROOT,
                check=True,
                stdout=subprocess.DEVNULL,
            )
        output = args.output_root / world_id
        if output.exists():
            shutil.rmtree(output)
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "trainer" / "train_jax.py"),
                "--input",
                str(ROOT / "artifacts" / "staging" / world_id / "input"),
                "--config",
                str(ROOT / "trainer" / "configs" / config_name),
                "--output",
                str(output),
            ],
            cwd=ROOT,
            check=False,
            stdout=subprocess.DEVNULL,
        )
        receipt_path = output / "training-receipt.json"
        if not receipt_path.is_file():
            results.append(
                {
                    "world_id": world_id,
                    "status": "error_without_receipt",
                    "process_return_code": completed.returncode,
                    "failed_non_tpu_gates": ["missing_receipt"],
                }
            )
            continue
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        shadow_validation = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "validate_shadow_output.py"),
                str(output),
                "--quiet",
            ],
            cwd=ROOT,
            check=False,
        )
        failed = [
            name
            for name, gate in receipt["gates"].items()
            if gate["passed"] is not True and name != "tpu_backend"
        ]
        if shadow_validation.returncode != 0:
            failed.append("shadow_artifact_validation")
        shadow_failed = sorted(
            name
            for name, gate in receipt["gates"].items()
            if name.startswith("shadow_") and gate["passed"] is not True
        )
        results.append(
            {
                "world_id": world_id,
                "status": "non_tpu_gates_passed" if not failed else "non_tpu_gates_failed",
                "process_return_code": completed.returncode,
                "failed_non_tpu_gates": sorted(failed),
                "failed_shadow_gates": shadow_failed,
                "shadow_projection_id": receipt["shadow_projection"]["projection_id"],
                "shadow_serialized_valid": shadow_validation.returncode == 0,
                "run_id": receipt["run_id"],
            }
        )
        print(
            f"completed {position}/{len(catalog)} {world_id}: "
            f"{results[-1]['status']}",
            flush=True,
        )

    summary = {
        "schema_version": 1,
        "diagnostic_only": True,
        "accelerator_accepted": False,
        "world_count": len(results),
        "non_tpu_pass_count": sum(row["status"] == "non_tpu_gates_passed" for row in results),
        "non_tpu_failure_count": sum(row["status"] != "non_tpu_gates_passed" for row in results),
        "shadow_pass_count": sum(not row.get("failed_shadow_gates", ["missing"]) for row in results),
        "shadow_failure_count": sum(bool(row.get("failed_shadow_gates", ["missing"])) for row in results),
        "results": results,
    }
    summary_name = (
        "summary.json"
        if args.partition_count == 1
        else f"summary-part-{args.partition_index}-of-{args.partition_count}.json"
    )
    output_path = args.output_root / summary_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    failed = summary["non_tpu_failure_count"] > 0
    return 2 if args.require_non_tpu_pass and failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
