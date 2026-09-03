#!/usr/bin/env python3
"""Package seven committed world bundles for one Kaggle TPU expansion run."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "kaggle" / "expansion-dataset"
TRAINER = ROOT / "trainer" / "train_jax.py"
KERNEL_REF = "jessealicea/new-lightcone-expansion-tpu-v0"
WORLDS = [
    "geometry-foundation-v0",
    "philosophy-rhetoric-v0",
    "psychology-neuroscience-v0",
    "rust-orchestrator-apps-v0",
    "scientific-reasoning-v0",
    "creativity-thinking-v0",
    "typography-color-v0",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*arguments: str) -> str:
    return subprocess.check_output(["git", *arguments], cwd=ROOT, text=True).strip()


def deterministic_zip(source_root: Path, output: Path) -> None:
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(source_root.rglob("*")):
            if not path.is_file():
                continue
            info = zipfile.ZipInfo(str(path.relative_to(source_root)))
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kernel-version", type=int, required=True)
    args = parser.parse_args()
    if args.kernel_version < 1:
        parser.error("kernel version must be positive")
    for validator in (
        "tools/validate_registry.py",
        "tools/validate_sources.py",
        "tools/validate_curricula.py",
        "tools/validate_adapters.py",
    ):
        subprocess.run([sys.executable, str(ROOT / validator)], cwd=ROOT, check=True)
    for world in WORLDS:
        subprocess.run(
            [sys.executable, str(ROOT / "trainer" / "compile_curriculum.py"), "--world-id", world],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
        )
    revision = git("rev-parse", "HEAD")
    if git("status", "--porcelain", "--untracked-files=normal"):
        raise RuntimeError("refusing to package a dirty source tree")

    package_root = ROOT / "artifacts" / "staging" / "expansion-package"
    if package_root.exists():
        shutil.rmtree(package_root)
    package_root.mkdir(parents=True)
    world_rows = []
    for world in WORLDS:
        source = ROOT / "artifacts" / "staging" / world / "input"
        destination = package_root / world
        shutil.copytree(source, destination)
        config = ROOT / "trainer" / "configs" / f"{world}.json"
        shutil.copy2(config, destination / "training-config.json")
        run_context = {
            "schema_version": 1,
            "source_revision": revision,
            "source_dirty": False,
            "kernel_ref": KERNEL_REF,
            "kernel_version": args.kernel_version,
        }
        (destination / "run-context.json").write_text(
            json.dumps(run_context, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        bundle_path = destination / "bundle-manifest.json"
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        bundle["files"]["training-config.json"] = sha256(destination / "training-config.json")
        bundle["files"]["run-context.json"] = sha256(destination / "run-context.json")
        bundle_path.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        world_rows.append({
            "world_id": world,
            "bundle_manifest_sha256": sha256(bundle_path),
            "training_config_sha256": sha256(destination / "training-config.json"),
        })

    archive = DATASET / "world-bundles.zip"
    deterministic_zip(package_root, archive)
    shutil.copy2(TRAINER, DATASET / "train_jax.py")
    expansion = {
        "schema_version": 1,
        "dataset_ref": "jessealicea/new-lightcone-expansion-input-v0",
        "kernel_ref": KERNEL_REF,
        "kernel_version": args.kernel_version,
        "source_revision": revision,
        "source_dirty": False,
        "archive_sha256": sha256(archive),
        "trainer_sha256": sha256(DATASET / "train_jax.py"),
        "worlds": world_rows,
    }
    (DATASET / "expansion-manifest.json").write_text(
        json.dumps(expansion, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(expansion, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

