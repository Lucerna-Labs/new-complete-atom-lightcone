#!/usr/bin/env python3
"""Validate that every configured training gate has actual examples."""

from __future__ import annotations

import json
import sys

from registry_lib import ROOT
from world_catalog import WORLD_CONFIGS


sys.path.insert(0, str(ROOT / "trainer"))

from shadow_projection import validate_shadow_training_config  # noqa: E402
from semantic_geometry import validate_protocol_v3_config  # noqa: E402
from train_jax import validate_protocol_samples  # noqa: E402


def main() -> int:
    summaries: list[dict[str, object]] = []
    for world_id, config_name in WORLD_CONFIGS:
        graph_path = ROOT / "artifacts" / "staging" / world_id / "input" / "training-graph.json"
        config_path = ROOT / "trainer" / "configs" / config_name
        if not graph_path.is_file():
            raise RuntimeError(
                f"missing compiled graph for {world_id}; run compile_curriculum.py first"
            )
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if graph["world_id"] != world_id or config["world_id"] != world_id:
            raise RuntimeError(f"world identity mismatch for {world_id}")
        validate_shadow_training_config(config)
        validate_protocol_v3_config(config)
        summaries.append(
            {
                "world_id": world_id,
                "sample_counts": validate_protocol_samples(graph, config),
            }
        )
    print(f"training protocols: {len(summaries)}")
    print("empty required sample sets: 0")
    print("valid: True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
