#!/usr/bin/env python3
"""Validate model-neutral adapter profiles and capability honesty."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FAMILIES = {"llama.cpp", "ollama", "vllm", "mlx", "transformers"}
CAPABILITIES = {"raw_logits", "custom_sampler", "grammar", "tools", "streaming", "multimodal", "deterministic", "seed_control", "embeddings"}
FIELDS = {"schema_version", "adapter_id", "runtime_family", "transport", "prompt_format", "boundary_mode", "model_match", "capabilities", "context_limit", "output_limit", "conformance_status", "conformance_receipt"}
ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


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
    print(f"adapter profiles: {len(profiles)}")
    print(f"runtime families: {sorted(families)}")
    print(f"model-locked profiles: {sum(profile.get('model_match') != {} for profile in profiles)}")
    print(f"conformance passed: {sum(profile.get('conformance_status') == 'passed' for profile in profiles)}")
    print(f"valid: {not errors}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

