#!/usr/bin/env python3
"""Package every rights-clean authored world for a hash-bound Kaggle TPU run."""

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
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "trainer"))

from world_catalog import WORLD_CONFIGS  # noqa: E402
from compile_curriculum import collect_all, compile_bundle  # noqa: E402

DATASET = ROOT / "kaggle" / "catalog-dataset"
TRAINER = ROOT / "trainer" / "train_jax.py"
SHADOW_TRAINER = ROOT / "trainer" / "shadow_projection.py"
SEMANTIC_TRAINER = ROOT / "trainer" / "semantic_geometry.py"
KERNEL_REF = "jessealicea/new-lightcone-catalog-tpu-v0"
ARCHIVE_FILENAME = "world-bundles.lcz"


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
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="run every packaging prerequisite without creating upload files",
    )
    args = parser.parse_args()
    if args.kernel_version < 1:
        parser.error("kernel version must be positive")

    for validator in (
        "tools/validate_registry.py",
        "tools/validate_sources.py",
        "tools/validate_curricula.py",
        "tools/validate_adapters.py",
        "tools/validate_taxonomy_shards.py",
        "tools/validate_revocations.py",
        "tools/sync_authored_coverage.py",
    ):
        subprocess.run([sys.executable, str(ROOT / validator)], cwd=ROOT, check=True)
    for test_root in ("trainer", "tools", "kaggle"):
        subprocess.run(
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                test_root,
                "-p",
                "test_*.py",
            ],
            cwd=ROOT,
            check=True,
        )
    curriculum_records = collect_all()
    for world_id, _config_name in WORLD_CONFIGS:
        compile_bundle(
            world_id,
            ROOT / "artifacts" / "staging" / world_id / "input",
            curriculum_records,
        )
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate_training_protocols.py")],
        cwd=ROOT,
        check=True,
    )
    if args.validate_only:
        print(
            json.dumps(
                {
                    "valid": True,
                    "world_count": len(WORLD_CONFIGS),
                    "packaged": False,
                    "reason": "validate_only",
                },
                indent=2,
            )
        )
        return 0

    revision = git("rev-parse", "HEAD")
    if git("status", "--porcelain", "--untracked-files=normal"):
        raise RuntimeError("refusing to package a dirty source tree")

    package_root = ROOT / "artifacts" / "staging" / "catalog-package"
    if package_root.exists():
        shutil.rmtree(package_root)
    package_root.mkdir(parents=True)
    worlds = []
    for world_id, config_name in WORLD_CONFIGS:
        source = ROOT / "artifacts" / "staging" / world_id / "input"
        destination = package_root / world_id
        shutil.copytree(source, destination)
        config = ROOT / "trainer" / "configs" / config_name
        shutil.copy2(config, destination / "training-config.json")
        run_context = {
            "schema_version": 1,
            "source_revision": revision,
            "source_dirty": False,
            "kernel_ref": KERNEL_REF,
            "kernel_version": args.kernel_version,
        }
        (destination / "run-context.json").write_text(
            json.dumps(run_context, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        bundle_path = destination / "bundle-manifest.json"
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        bundle["files"]["training-config.json"] = sha256(destination / "training-config.json")
        bundle["files"]["run-context.json"] = sha256(destination / "run-context.json")
        bundle_path.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        worlds.append(
            {
                "world_id": world_id,
                "bundle_manifest_sha256": sha256(bundle_path),
                "training_config_sha256": sha256(destination / "training-config.json"),
            }
        )

    # Kaggle automatically expands files with a .zip suffix when it creates a
    # dataset version.  Keep the deterministic ZIP payload under a project
    # extension so the TPU runner can verify the archive bytes before safely
    # extracting them itself.
    (DATASET / "world-bundles.zip").unlink(missing_ok=True)
    archive = DATASET / ARCHIVE_FILENAME
    deterministic_zip(package_root, archive)
    shutil.copy2(TRAINER, DATASET / "train_jax.py")
    shutil.copy2(SHADOW_TRAINER, DATASET / "shadow_projection.py")
    shutil.copy2(SEMANTIC_TRAINER, DATASET / "semantic_geometry.py")
    manifest = {
        "schema_version": 1,
        "dataset_ref": "jessealicea/new-lightcone-catalog-input-v0",
        "kernel_ref": KERNEL_REF,
        "kernel_version": args.kernel_version,
        "source_revision": revision,
        "source_dirty": False,
        "archive_filename": ARCHIVE_FILENAME,
        "archive_sha256": sha256(archive),
        "trainer_sha256": sha256(DATASET / "train_jax.py"),
        "shadow_projection_sha256": sha256(DATASET / "shadow_projection.py"),
        "semantic_geometry_sha256": sha256(DATASET / "semantic_geometry.py"),
        "worlds": worlds,
    }
    (DATASET / "catalog-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
