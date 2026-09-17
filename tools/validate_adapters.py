#!/usr/bin/env python3
"""Validate model-neutral adapter profiles and capability honesty."""

from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FAMILIES = {"llama.cpp", "ollama", "vllm", "mlx", "transformers"}
CAPABILITIES = {"raw_logits", "custom_sampler", "grammar", "tools", "streaming", "multimodal", "deterministic", "seed_control", "embeddings"}
FIELDS = {"schema_version", "adapter_id", "runtime_family", "transport", "prompt_format", "boundary_mode", "model_match", "capabilities", "context_limit", "output_limit", "conformance_status", "conformance_receipt"}
TARGET_FIELDS = {
    "schema_version", "target_id", "model_id", "publisher", "model_revision",
    "license", "architecture", "parameter_count", "native_context_limit",
    "modalities", "thinking_controls", "declared_runtime_routes", "source",
    "conformance_status", "conformance_receipts", "limitations"
}
ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def main() -> int:
    errors: list[str] = []
    profiles = []
    for path in sorted((ROOT / "adapters" / "profiles").glob("*.json")):
        try:
            profile = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            errors.append(f"{path}: {error}")
            continue
        profiles.append(profile)
        if set(profile) != FIELDS:
            errors.append(f"{path.name}: profile fields differ")
        if profile.get("schema_version") != 1 or not ID.fullmatch(str(profile.get("adapter_id", ""))):
            errors.append(f"{path.name}: invalid identity")
        capabilities = profile.get("capabilities", {})
        if set(capabilities) != CAPABILITIES or not all(isinstance(value, bool) for value in capabilities.values()):
            errors.append(f"{path.name}: capabilities are incomplete or non-boolean")
        native = profile.get("boundary_mode") == "native_post_logits"
        if native != bool(capabilities.get("raw_logits") and capabilities.get("custom_sampler")):
            errors.append(f"{path.name}: boundary mode contradicts logit capabilities")
        if profile.get("output_limit", 0) <= 0 or profile.get("output_limit", 0) >= profile.get("context_limit", 0):
            errors.append(f"{path.name}: invalid context/output limits")
        if profile.get("model_match") != {}:
            errors.append(f"{path.name}: baseline profile is unexpectedly locked to a model")
        status = profile.get("conformance_status")
        receipt = profile.get("conformance_receipt")
        if (status == "passed") != isinstance(receipt, str):
            errors.append(f"{path.name}: conformance status/receipt mismatch")
    ids = [profile.get("adapter_id") for profile in profiles]
    duplicate_ids = [value for value, count in collections.Counter(ids).items() if count > 1]
    if duplicate_ids:
        errors.append(f"duplicate adapter IDs: {duplicate_ids}")
    families = {profile.get("runtime_family") for profile in profiles}
    if not REQUIRED_FAMILIES <= families:
        errors.append(f"missing adapter families: {sorted(REQUIRED_FAMILIES - families)}")
    profile_ids = set(ids)
    profiles_by_id = {profile["adapter_id"]: profile for profile in profiles}
    targets = []
    for path in sorted((ROOT / "adapters" / "targets").glob("*.json")):
        try:
            target = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            errors.append(f"{path}: {error}")
            continue
        targets.append(target)
        if set(target) != TARGET_FIELDS:
            errors.append(f"{path.name}: target fields differ")
        if target.get("schema_version") != 1 or not ID.fullmatch(str(target.get("target_id", ""))):
            errors.append(f"{path.name}: invalid target identity")
        if not target.get("model_id") or target.get("parameter_count", 0) <= 0:
            errors.append(f"{path.name}: missing model identity or parameter count")
        if target.get("native_context_limit", 0) < 256:
            errors.append(f"{path.name}: invalid native context limit")
        unknown_routes = set(target.get("declared_runtime_routes", [])) - profile_ids
        if unknown_routes:
            errors.append(f"{path.name}: unknown runtime routes {sorted(unknown_routes)}")
        receipts = target.get("conformance_receipts")
        if target.get("conformance_status") == "passed" and not receipts:
            errors.append(f"{path.name}: passed target lacks conformance receipts")
        if target.get("conformance_status") != "passed" and receipts:
            errors.append(f"{path.name}: unpassed target unexpectedly has conformance receipts")
        for relative in receipts or []:
            receipt_path = ROOT / relative
            if not receipt_path.is_file():
                errors.append(f"{path.name}: missing target conformance receipt {relative}")
                continue
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            failed_gates = sorted(
                name for name, gate in receipt.get("gates", {}).items() if gate.get("passed") is not True
            )
            if receipt.get("status") != "passed" or failed_gates:
                errors.append(f"{path.name}: receipt {relative} is not passed: {failed_gates}")
            if receipt.get("target_id") != target.get("target_id"):
                errors.append(f"{path.name}: receipt target identity differs")
            adapter_id = receipt.get("adapter_id")
            if adapter_id not in target.get("declared_runtime_routes", []):
                errors.append(f"{path.name}: receipt adapter is not a declared target route")
            profile = profiles_by_id.get(adapter_id)
            if profile is None or profile.get("conformance_status") != "passed" or profile.get("conformance_receipt") != relative:
                errors.append(f"{path.name}: receipt adapter profile is not bound as passed")
            elif receipt.get("profile_sha256") != canonical_hash(
                {**profile, "conformance_status": "declared", "conformance_receipt": None}
            ):
                errors.append(f"{path.name}: receipt profile contract hash differs")
            if receipt.get("target_sha256") != canonical_hash(
                {**target, "conformance_status": "declared", "conformance_receipts": []}
            ):
                errors.append(f"{path.name}: receipt target contract hash differs")
            if receipt.get("model", {}).get("revision") != target.get("model_revision"):
                errors.append(f"{path.name}: receipt model revision differs")
    print(f"adapter profiles: {len(profiles)}")
    print(f"runtime families: {sorted(families)}")
    print(f"model-locked profiles: {sum(profile.get('model_match') != {} for profile in profiles)}")
    print(f"conformance passed: {sum(profile.get('conformance_status') == 'passed' for profile in profiles)}")
    print(f"model targets: {len(targets)}")
    print(f"target conformance passed: {sum(target.get('conformance_status') == 'passed' for target in targets)}")
    print(f"valid: {not errors}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
