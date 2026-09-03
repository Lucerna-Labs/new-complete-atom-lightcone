"""Shared deterministic registry helpers for the new Lightcone project."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology"

DOMAIN_CATALOG = ONTOLOGY / "domain-catalog.json"
LANE_CATALOG = ONTOLOGY / "lane-catalog.json"
COVERAGE_AXES = ONTOLOGY / "coverage-axes.json"
COVERAGE_LEDGER = ONTOLOGY / "coverage-ledger.json"


STATUS_ORDER = (
    "discovered",
    "scoped",
    "sourced",
    "authored",
    "compiled",
    "trained",
    "locally_validated",
    "accelerator_validated",
    "sealed",
)

COVERAGE_ORDER = ("missing", "planned", "authored", "tested", "sealed")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def catalog_hashes() -> dict[str, str]:
    return {
        "domain_catalog": file_hash(DOMAIN_CATALOG),
        "lane_catalog": file_hash(LANE_CATALOG),
        "coverage_axes": file_hash(COVERAGE_AXES),
    }


def expected_items() -> list[dict[str, Any]]:
    domains = load_json(DOMAIN_CATALOG)
    lanes = load_json(LANE_CATALOG)
    axes = [axis["id"] for axis in load_json(COVERAGE_AXES)["axes"]]
    blank = {axis: "missing" for axis in axes}
    items: list[dict[str, Any]] = []

    for lane in lanes["lanes"]:
        items.append(
            {
                "id": lane["id"],
                "kind": "lane",
                "parent": None,
                "mandatory": True,
                "status": "scoped",
                "coverage": dict(blank),
                "evidence": [],
                "notes": ["Lane contract registered; sourcing and curriculum remain open."],
            }
        )

    for domain in domains["domains"]:
        items.append(
            {
                "id": domain["id"],
                "kind": "domain",
                "parent": None,
                "mandatory": bool(domain["mandatory"]),
                "status": "scoped",
                "coverage": dict(blank),
                "evidence": [],
                "notes": ["Domain and initial subfield boundary registered; open discovery remains active."],
            }
        )
        for subfield in domain["subfields"]:
            items.append(
                {
                    "id": subfield["id"],
                    "kind": "subfield",
                    "parent": domain["id"],
                    "mandatory": bool(domain["mandatory"]),
                    "status": "discovered",
                    "coverage": dict(blank),
                    "evidence": [],
                    "notes": [],
                }
            )

    return sorted(items, key=lambda item: (item["kind"], item["id"]))

