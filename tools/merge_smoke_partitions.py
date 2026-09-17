#!/usr/bin/env python3
"""Merge disjoint local-smoke partition summaries with catalog closure checks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from world_catalog import TAXONOMY_WORLD_CONFIGS, WORLD_CONFIGS


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_root", type=Path)
    parser.add_argument("--partition-count", type=int, required=True)
    parser.add_argument("--catalog", choices=["taxonomy", "all"], default="taxonomy")
    args = parser.parse_args()
    summaries = [
        json.loads(
            (args.output_root / f"summary-part-{index}-of-{args.partition_count}.json").read_text(
                encoding="utf-8"
            )
        )
        for index in range(args.partition_count)
    ]
    results = [row for summary in summaries for row in summary["results"]]
    ids = [row["world_id"] for row in results]
    selected_catalog = WORLD_CONFIGS if args.catalog == "all" else TAXONOMY_WORLD_CONFIGS
    expected = {world_id for world_id, _config in selected_catalog}
    if len(ids) != len(set(ids)) or set(ids) != expected:
        raise RuntimeError(
            f"partition closure mismatch: rows={len(ids)} unique={len(set(ids))} "
            f"missing={len(expected - set(ids))} extra={len(set(ids) - expected)}"
        )
    merged = {
        "schema_version": 1,
        "diagnostic_only": True,
        "accelerator_accepted": False,
        "partition_count": args.partition_count,
        "world_count": len(results),
        "non_tpu_pass_count": sum(row["status"] == "non_tpu_gates_passed" for row in results),
        "non_tpu_failure_count": sum(row["status"] != "non_tpu_gates_passed" for row in results),
        "shadow_pass_count": sum(not row.get("failed_shadow_gates", ["missing"]) for row in results),
        "shadow_failure_count": sum(bool(row.get("failed_shadow_gates", ["missing"])) for row in results),
        "results": sorted(results, key=lambda row: row["world_id"]),
    }
    (args.output_root / "summary.json").write_text(
        json.dumps(merged, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: value for key, value in merged.items() if key != "results"}, indent=2))
    return 0 if merged["non_tpu_failure_count"] == 0 and merged["shadow_failure_count"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
