#!/usr/bin/env python3
"""Materialize pre-registered per-world TPU protocols from one reviewed template."""

from __future__ import annotations

import copy
import json

from registry_lib import ROOT


WORLDS = [
    "geometry-foundation-v0",
    "philosophy-rhetoric-v0",
    "psychology-neuroscience-v0",
    "rust-orchestrator-apps-v0",
    "scientific-reasoning-v0",
    "creativity-thinking-v0",
    "typography-color-v0",
]


def main() -> int:
    root = ROOT / "trainer" / "configs"
    template = json.loads((root / "world-v0-template.json").read_text(encoding="utf-8"))
    for offset, world_id in enumerate(WORLDS, start=1):
        config = copy.deepcopy(template)
        config["world_id"] = world_id
        config["protocol_id"] = f"{world_id}-kaggle-tpu-v0"
        config["seed"] = template["seed"] + offset
        path = root / f"{world_id}.json"
        path.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {len(WORLDS)} pre-registered world-training configs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

