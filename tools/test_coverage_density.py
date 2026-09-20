from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from audit_coverage_density import build_report
from build_depth_completion_curriculum import Builder, OUTPUT, WORLD_ID

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "trainer"))

from compile_curriculum import collect_all, compile_bundle  # noqa: E402


class CoverageDepthRegressionTests(unittest.TestCase):
    def test_depth_floor_and_committed_output_are_deterministic(self) -> None:
        report = build_report(4)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["mandatory_pairs"], 8960)
        self.assertEqual(report["credited_pairs"], 8960)
        self.assertEqual(report["pairs_below_min"], 0)

        builder = Builder()
        generated = builder.run(4, write=False)
        rendered = "".join(
            json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
            for record in builder.output
        )
        self.assertTrue(generated)
        self.assertEqual(rendered, OUTPUT.read_text(encoding="utf-8"))

    def test_depth_relations_compile_without_cross_world_endpoints(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            bundle = compile_bundle(WORLD_ID, Path(raw), collect_all())
        self.assertGreater(bundle["node_count"], 0)
        self.assertGreater(bundle["edge_count"], 0)


if __name__ == "__main__":
    unittest.main()
