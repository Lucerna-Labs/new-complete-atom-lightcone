"""Canonical ordered mapping from world identities to training configurations."""

from __future__ import annotations

import json
from pathlib import Path

FOUNDATION_WORLD_CONFIGS = [
    ("foundation-lanes-v0", "foundation-v0.json"),
    ("geometry-foundation-v0", "geometry-foundation-v0.json"),
    ("philosophy-rhetoric-v0", "philosophy-rhetoric-v0.json"),
    ("psychology-neuroscience-v0", "psychology-neuroscience-v0.json"),
    ("rust-orchestrator-apps-v0", "rust-orchestrator-apps-v0.json"),
    ("scientific-reasoning-v0", "scientific-reasoning-v0.json"),
    ("creativity-thinking-v0", "creativity-thinking-v0.json"),
    ("typography-color-v0", "typography-color-v0.json"),
    ("literature-writing-v0", "literature-writing-v0.json"),
    ("network-security-browser-v0", "network-security-browser-v0.json"),
    ("software-app-development-v0", "software-app-development-v0.json"),
    ("languages-compilers-v0", "languages-compilers-v0.json"),
    ("operating-systems-v0", "operating-systems-v0.json"),
    ("ai-development-v0", "ai-development-v0.json"),
    ("math-probability-information-v0", "math-probability-information-v0.json"),
    ("sciences-v0", "sciences-v0.json"),
    ("engineering-v0", "engineering-v0.json"),
    ("first-principles-v0", "first-principles-v0.json"),
    ("computer-data-systems-v0", "computer-data-systems-v0.json"),
    ("human-communication-learning-v0", "human-communication-learning-v0.json"),
    ("health-agriculture-v0", "health-agriculture-v0.json"),
    ("society-culture-arts-v0", "society-culture-arts-v0.json"),
]


ROOT = Path(__file__).resolve().parents[1]
SHARD_INDEX = ROOT / "plans" / "taxonomy-training-shards" / "index.json"


def taxonomy_world_configs() -> list[tuple[str, str]]:
    if not SHARD_INDEX.is_file():
        return []
    index = json.loads(SHARD_INDEX.read_text(encoding="utf-8"))
    return [
        (row["world_id"], f"taxonomy/{row['world_id']}.json")
        for row in index.get("shards", [])
        if row.get("status") == "authored" and row.get("world_id")
    ]


TAXONOMY_WORLD_CONFIGS = taxonomy_world_configs()
COVERAGE_WORLD_CONFIGS = [("coverage-closure-v0", "coverage-closure-v0.json")]
WORLD_CONFIGS = [
    *FOUNDATION_WORLD_CONFIGS,
    *TAXONOMY_WORLD_CONFIGS,
    *COVERAGE_WORLD_CONFIGS,
]
GENERATED_WORLD_CONFIGS = [
    pair for pair in WORLD_CONFIGS if pair[0] != "foundation-lanes-v0"
]
GENERATED_WORLD_IDS = [world_id for world_id, _config in GENERATED_WORLD_CONFIGS]
