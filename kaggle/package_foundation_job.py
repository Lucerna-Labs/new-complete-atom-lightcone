#!/usr/bin/env python3
"""Build the exact private Kaggle dataset and kernel upload directories."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "trainer"))

from shadow_projection import validate_shadow_training_config  # noqa: E402

STAGING = ROOT / "artifacts" / "staging" / "foundation-lanes-v0" / "input"
DATASET = ROOT / "kaggle" / "foundation-dataset"
KERNEL = ROOT / "kaggle" / "foundation-tpu"
CONFIG = ROOT / "trainer" / "configs" / "foundation-v0.json"
TRAINER = ROOT / "trainer" / "train_jax.py"
SHADOW_TRAINER = ROOT / "trainer" / "shadow_projection.py"
SEMANTIC_TRAINER = ROOT / "trainer" / "semantic_geometry.py"
KERNEL_REF = "jessealicea/new-lightcone-foundation-tpu-v0"


def sha256(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*arguments: str) -> str:
    return subprocess.check_output(["git", *arguments], cwd=ROOT, text=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kernel-version", type=int, required=True)
    args = parser.parse_args()
    if args.kernel_version < 1:
        parser.error("--kernel-version must be positive")
    subprocess.run([sys.executable, str(ROOT / "tools" / "validate_registry.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "tools" / "validate_sources.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "tools" / "validate_curricula.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "trainer" / "compile_curriculum.py")], cwd=ROOT, check=True)
    validate_shadow_training_config(json.loads(CONFIG.read_text(encoding="utf-8")))

    revision = git("rev-parse", "HEAD")
    dirty = bool(git("status", "--porcelain", "--untracked-files=normal"))
    if dirty:
        raise RuntimeError("refusing to package a dirty source tree; commit the exact trainer and curriculum first")

    for path in DATASET.iterdir():
        if path.name != "dataset-metadata.json" and path.is_file():
            path.unlink()
    for source in sorted(STAGING.iterdir()):
        if source.is_file():
            shutil.copy2(source, DATASET / source.name)
    shutil.copy2(CONFIG, DATASET / "training-config.json")
    run_context = {
        "schema_version": 1,
        "source_revision": revision,
        "source_dirty": False,
        "kernel_ref": KERNEL_REF,
        "kernel_version": args.kernel_version,
    }
    (DATASET / "run-context.json").write_text(
        json.dumps(run_context, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    bundle_path = DATASET / "bundle-manifest.json"
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    bundle["files"]["training-config.json"] = sha256(DATASET / "training-config.json")
    bundle["files"]["run-context.json"] = sha256(DATASET / "run-context.json")
    bundle_path.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    shutil.copy2(TRAINER, KERNEL / "train.py")
    shutil.copy2(SHADOW_TRAINER, KERNEL / "shadow_projection.py")
    shutil.copy2(SEMANTIC_TRAINER, KERNEL / "semantic_geometry.py")

    print(json.dumps({
        "source_revision": revision,
        "dataset_ref": json.loads((DATASET / "dataset-metadata.json").read_text())["id"],
        "kernel_ref": KERNEL_REF,
        "bundle_hash": sha256(bundle_path),
        "dataset_files": sorted(path.name for path in DATASET.iterdir() if path.is_file()),
        "kernel_files": sorted(path.name for path in KERNEL.iterdir() if path.is_file()),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
