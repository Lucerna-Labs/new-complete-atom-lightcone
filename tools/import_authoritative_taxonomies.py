#!/usr/bin/env python3
"""Import official taxonomies as unresolved coverage discoveries, not facts."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from registry_lib import ROOT


INPUT_MANIFEST = ROOT / "sources" / "taxonomy-inputs.json"
OUTPUT = ROOT / "ontology" / "discovery-ledger.jsonl"
OUTPUT_MANIFEST = ROOT / "ontology" / "discovery-manifest.json"


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def msc_hint(code: str) -> str:
    prefix = int(code[:2]) if code[:2].isdigit() else -1
    if prefix == 62:
        return "probability-statistics"
    if prefix == 68:
        return "computer-science"
    if prefix in {70, 74, 76, 78, 80, 81, 82, 83, 85, 86}:
        return "physics"
    if prefix in {90, 91}:
        return "economics-decision-operations"
    if prefix == 92:
        return "biology"
    if prefix in {93, 94}:
        return "information-communication"
    return "formal-mathematics"


def msc_parent(code: str, known: set[str]) -> list[str]:
    candidates: list[str] = []
    if len(code) == 5 and code[2] == "-" and not code.endswith("XX"):
        candidates.append(code[:2] + "-XX")
    elif len(code) == 5 and code[2].isalpha():
        if not code.endswith("xx") and not code.endswith("XX"):
            candidates.append(code[:3] + "xx")
        candidates.append(code[:2] + "-XX")
    return [candidate for candidate in candidates if candidate in known][:1]


def import_msc(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="iso-8859-1", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    known = {row["code"] for row in rows}
    output = []
    for row in rows:
        code = row["code"]
        output.append({
            "schema_version": 1,
            "discovery_id": f"msc2020.{slug(code)}",
            "source_id": "msc2020",
            "external_id": code,
            "label": row["text"].strip(),
            "description": row["description"].strip(),
            "parent_external_ids": msc_parent(code, known),
            "domain_hint": msc_hint(code),
            "status": "unmapped",
            "mapped_coverage_ids": [],
            "exclusion_reason": None,
        })
    return output


MESH_HINTS = {
    "A": "biology",
    "B": "biology",
    "C": "medicine-health",
    "D": "chemistry",
    "E": "medicine-health",
    "F": "psychology-cognitive-science",
    "G": "biology",
    "H": "research-scientific-method",
    "I": "social-behavioral-sciences",
    "J": "agriculture-food-ecology",
    "K": "philosophy",
    "L": "computer-science",
    "M": "social-behavioral-sciences",
    "N": "medicine-health",
    "V": "research-scientific-method",
    "Z": "history-geography-culture",
}


def import_mesh(path: Path) -> list[dict[str, Any]]:
    descriptors: list[tuple[str, str, list[str]]] = []
    with gzip.open(path, "rb") as handle:
        for _event, element in ET.iterparse(handle, events=("end",)):
            if element.tag != "DescriptorRecord":
                continue
            ui = element.findtext("DescriptorUI")
            name = element.findtext("DescriptorName/String")
            trees = [item.text for item in element.findall("TreeNumberList/TreeNumber") if item.text]
            if ui and name:
                descriptors.append((ui, name.strip(), sorted(trees)))
            element.clear()
    tree_to_ui = {tree: ui for ui, _name, trees in descriptors for tree in trees}
    output = []
    for ui, name, trees in descriptors:
        parents = set()
        for tree in trees:
            if "." in tree:
                parent_tree = tree.rsplit(".", 1)[0]
                if parent_tree in tree_to_ui and tree_to_ui[parent_tree] != ui:
                    parents.add(tree_to_ui[parent_tree])
        top = trees[0][0] if trees else "H"
        output.append({
            "schema_version": 1,
            "discovery_id": f"mesh2026.{ui.lower()}",
            "source_id": "mesh2026",
            "external_id": ui,
            "label": name,
            "description": "MeSH descriptor used as a coverage-discovery term; it is not itself a factual curriculum statement.",
            "parent_external_ids": sorted(parents),
            "tree_numbers": trees,
            "domain_hint": MESH_HINTS.get(top, "medicine-health"),
            "status": "unmapped",
            "mapped_coverage_ids": [],
            "exclusion_reason": None,
        })
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=ROOT / "artifacts" / "downloads" / "taxonomies")
    args = parser.parse_args()
    manifest = json.loads(INPUT_MANIFEST.read_text(encoding="utf-8"))
    inputs = {item["source_id"]: item for item in manifest["inputs"]}
    paths = {source_id: args.input_dir / item["local_name"] for source_id, item in inputs.items()}
    for source_id, path in paths.items():
        observed = file_hash(path)
        expected = inputs[source_id]["sha256"]
        if observed != expected:
            raise RuntimeError(f"{source_id} input hash mismatch: {observed} != {expected}")
    records = import_msc(paths["msc2020"]) + import_mesh(paths["mesh2026"])
    records.sort(key=lambda record: record["discovery_id"])
    ids = [record["discovery_id"] for record in records]
    if len(ids) != len(set(ids)):
        raise RuntimeError("discovery IDs are not unique")
    OUTPUT.write_text("".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records), encoding="utf-8")
    counts: dict[str, int] = {}
    for record in records:
        counts[record["source_id"]] = counts.get(record["source_id"], 0) + 1
    output_manifest = {
        "schema_version": 1,
        "open_world": True,
        "purpose": "Unresolved authoritative taxonomy entries expand the known coverage frontier; entries are not facts or trained worlds.",
        "inputs": manifest["inputs"],
        "entry_count": len(records),
        "counts": dict(sorted(counts.items())),
        "unresolved_count": len(records),
        "ledger_sha256": file_hash(OUTPUT),
        "acknowledgements": [item["acknowledgement"] for item in manifest["inputs"]],
    }
    OUTPUT_MANIFEST.write_text(json.dumps(output_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output_manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
