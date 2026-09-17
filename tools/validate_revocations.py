#!/usr/bin/env python3
"""Validate immutable revocations and chained replacement supersessions."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from registry_lib import ROOT, file_hash


BASE_FIELDS = {
    "schema_version", "revocation_id", "world_id", "world_version",
    "manifest_sha256", "revoked_at", "reason_class", "affected_source_ids",
    "source_evidence", "decision", "artifact_retained_for_audit",
    "replacement_curriculum", "replacement_curriculum_sha256",
    "replacement_status", "notes",
}
SUPERSESSION_FIELDS = {
    "schema_version", "supersession_id", "supersedes_revocation",
    "superseded_receipt_sha256", "world_id", "world_version", "created_at",
    "reason_class", "affected_source_ids", "decision", "replacement_curriculum",
    "replacement_curriculum_sha256", "replacement_status",
    "excluded_source_overlap", "notes",
}


def curriculum_source_ids(path: Path) -> set[str]:
    used: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            used.update(json.loads(line)["source_ids"])
    return used


def validate(root: Path = ROOT) -> tuple[int, int, list[str]]:
    errors: list[str] = []
    exclusions = json.loads((root / "sources" / "exclusions.json").read_text(encoding="utf-8"))
    excluded_ids = {row["source_id"] for row in exclusions["exclusions"]}
    paths = sorted((root / "receipts" / "revocations").glob("*.json"))
    bases: dict[str, tuple[Path, dict[str, Any]]] = {}
    supersessions: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in paths:
        receipt = json.loads(path.read_text(encoding="utf-8"))
        if "revocation_id" in receipt:
            identifier = str(receipt["revocation_id"])
            if identifier in bases:
                errors.append(f"{path.name}: duplicate revocation_id {identifier}")
            bases[identifier] = (path, receipt)
        elif "supersession_id" in receipt:
            identifier = str(receipt["supersession_id"])
            if identifier in supersessions:
                errors.append(f"{path.name}: duplicate supersession_id {identifier}")
            supersessions[identifier] = (path, receipt)
        else:
            errors.append(f"{path.name}: unknown revocation receipt kind")

    referenced_receipts = {
        str(receipt.get("supersedes_revocation", ""))
        for _path, receipt in supersessions.values()
    }

    def root_revocation(identifier: str, trail: set[str] | None = None) -> str | None:
        if identifier in bases:
            return identifier
        if identifier not in supersessions:
            return None
        trail = set() if trail is None else set(trail)
        if identifier in trail:
            return None
        trail.add(identifier)
        return root_revocation(
            str(supersessions[identifier][1].get("supersedes_revocation", "")),
            trail,
        )

    valid_terminal_supersessions: dict[str, list[dict[str, Any]]] = {}
    for identifier, (path, receipt) in supersessions.items():
        local: list[str] = []
        if set(receipt) != SUPERSESSION_FIELDS:
            local.append("receipt fields differ from supersession contract")
        if receipt.get("schema_version") != 1:
            local.append("schema_version must be 1")
        superseded = str(receipt.get("supersedes_revocation", ""))
        predecessor = bases.get(superseded) or supersessions.get(superseded)
        root_id = root_revocation(superseded)
        if predecessor is None or root_id is None:
            local.append("superseded revocation or supersession does not exist, or chain is cyclic")
        else:
            predecessor_path, predecessor_receipt = predecessor
            if receipt.get("superseded_receipt_sha256") != file_hash(predecessor_path):
                local.append("superseded receipt hash differs")
            if receipt.get("world_id") != predecessor_receipt.get("world_id") or receipt.get(
                "world_version"
            ) != predecessor_receipt.get("world_version"):
                local.append("world identity differs from superseded revocation")
            if set(receipt.get("affected_source_ids", [])) != set(
                predecessor_receipt.get("affected_source_ids", [])
            ):
                local.append("affected source set differs from superseded revocation")
        replacement = root / str(receipt.get("replacement_curriculum", ""))
        if not replacement.is_file():
            local.append("replacement curriculum is missing")
        is_terminal = identifier not in referenced_receipts
        if replacement.is_file() and is_terminal:
            if file_hash(replacement) != receipt.get("replacement_curriculum_sha256"):
                local.append("replacement curriculum hash differs")
            overlap = sorted(curriculum_source_ids(replacement) & excluded_ids)
            if overlap != receipt.get("excluded_source_overlap"):
                local.append("excluded-source overlap declaration differs from curriculum")
            if overlap:
                local.append("replacement curriculum uses an excluded source")
        if receipt.get("decision") != "replacement_evidence_rebound":
            local.append("decision is not replacement_evidence_rebound")
        if not set(receipt.get("affected_source_ids", [])) <= excluded_ids:
            local.append("affected sources are not all excluded")
        if local:
            errors.extend(f"{path.name}: {error}" for error in local)
        elif is_terminal and root_id is not None:
            valid_terminal_supersessions.setdefault(root_id, []).append(receipt)

    for revocation_id, (path, receipt) in bases.items():
        if set(receipt) != BASE_FIELDS:
            errors.append(f"{path.name}: receipt fields differ from contract")
            continue
        if receipt["schema_version"] != 1:
            errors.append(f"{path.name}: schema_version must be 1")
        pack = root / "artifacts" / "worlds" / receipt["world_id"] / receipt["world_version"]
        manifest = pack / "manifest.json"
        sources = pack / "sources.json"
        if not manifest.is_file() or not sources.is_file():
            errors.append(f"{path.name}: retained artifact is missing")
            continue
        if file_hash(manifest) != receipt["manifest_sha256"]:
            errors.append(f"{path.name}: retained manifest hash differs")
        packed_ids = {
            row["source_id"]
            for row in json.loads(sources.read_text(encoding="utf-8"))["sources"]
        }
        affected = set(receipt["affected_source_ids"])
        if not affected or not affected <= packed_ids:
            errors.append(f"{path.name}: affected sources are not present in retained pack")
        if not affected <= excluded_ids:
            errors.append(f"{path.name}: affected sources are not in the exclusion registry")
        replacement = root / receipt["replacement_curriculum"]
        if not replacement.is_file():
            errors.append(f"{path.name}: replacement curriculum is missing")
        elif file_hash(replacement) != receipt["replacement_curriculum_sha256"]:
            candidates = [
                candidate
                for candidate in valid_terminal_supersessions.get(revocation_id, [])
                if candidate["replacement_curriculum"] == receipt["replacement_curriculum"]
                and candidate["replacement_curriculum_sha256"] == file_hash(replacement)
            ]
            if not candidates:
                errors.append(
                    f"{path.name}: replacement curriculum changed without a valid supersession"
                )
        if receipt["decision"] != "excluded_from_active_world_acceptance":
            errors.append(f"{path.name}: decision is not an active-acceptance exclusion")
        if receipt["artifact_retained_for_audit"] is not True:
            errors.append(f"{path.name}: retained-audit declaration is false")
    return len(bases), len(supersessions), errors


def main() -> int:
    base_count, supersession_count, errors = validate()
    print(f"revocation receipts: {base_count}")
    print(f"replacement supersessions: {supersession_count}")
    print(f"valid: {not errors}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
