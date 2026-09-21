#!/usr/bin/env python3
"""Materialize pre-registered per-world TPU protocols from one reviewed template."""

from __future__ import annotations

import copy
import json

from registry_lib import ROOT
from world_catalog import GENERATED_WORLD_CONFIGS


def main() -> int:
    root = ROOT / "trainer" / "configs"
    template = json.loads((root / "world-v0-template.json").read_text(encoding="utf-8"))
    for offset, (world_id, config_name) in enumerate(GENERATED_WORLD_CONFIGS, start=1):
        config = copy.deepcopy(template)
        config["world_id"] = world_id
        config["protocol_id"] = f"{world_id}-kaggle-tpu-v3"
        config["seed"] = template["seed"] + offset
        if world_id.startswith("taxonomy-") or world_id == "coverage-closure-v0":
            config["steps"] = 1200
            config["train_edge_evaluation_method"] = "train_fitted_evidence"
        if world_id == "coverage-closure-v0":
            config["evidence_exact_label_weight"] = 2.0
            config["semantic_overlay_residual_scale"] = 0.005
        path = root / config_name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {len(GENERATED_WORLD_CONFIGS)} pre-registered world-training configs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
