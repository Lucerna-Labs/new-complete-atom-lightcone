from __future__ import annotations

import runpy
import tempfile
import unittest
import zipfile
from pathlib import Path


RUNNER = runpy.run_path(
    str(Path(__file__).resolve().parent / "catalog-tpu" / "run_catalog.py")
)


class CatalogRunnerBoundaryTests(unittest.TestCase):
    def test_safe_extract_rejects_parent_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            archive_path = root / "input.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("../escape.json", "{}")
            destination = root / "destination"
            destination.mkdir()
            with zipfile.ZipFile(archive_path) as archive:
                with self.assertRaisesRegex(RuntimeError, "escapes destination"):
                    RUNNER["safe_extract"](archive, destination)

    def test_nonempty_working_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "stale.txt").write_text("stale", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "not empty"):
                RUNNER["require_empty_directory"](root)


if __name__ == "__main__":
    unittest.main()
