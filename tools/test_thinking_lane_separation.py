from __future__ import annotations

import json
import unittest
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ThinkingLaneSeparationTests(unittest.TestCase):
    def test_thinking_stage_and_control_contracts_are_distinct(self) -> None:
        lanes = {
            item["id"]: item
            for item in json.loads(
                (ROOT / "ontology" / "lane-catalog.json").read_text(encoding="utf-8")
            )["lanes"]
        }
        identifiers = (
            "thinking.bottom_up",
            "thinking.vertical",
            "thinking.nonlinear",
            "thinking.lateral",
        )
        for lane in identifiers:
            self.assertEqual(lanes[lane]["kind"], "thinking")
        for left, right in combinations(identifiers, 2):
            self.assertNotEqual(
                set(lanes[left]["required_stages"]),
                set(lanes[right]["required_stages"]),
            )
            self.assertNotEqual(
                set(lanes[left]["required_controls"]),
                set(lanes[right]["required_controls"]),
            )

    def test_new_deep_roots_do_not_collapse_lane_identity(self) -> None:
        records = {
            item["record_id"]: item
            for item in (
                json.loads(line)
                for line in (
                    ROOT / "curricula" / "creativity-thinking" / "foundations.jsonl"
                ).read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
        }
        vertical = records["vertical.root"]["lanes"]
        nonlinear = records["nonlinear.root"]["lanes"]
        self.assertIn("thinking.vertical", vertical)
        self.assertNotIn("thinking.nonlinear", vertical)
        self.assertNotIn("thinking.lateral", vertical)
        self.assertIn("thinking.nonlinear", nonlinear)
        self.assertNotIn("thinking.vertical", nonlinear)
        self.assertNotIn("thinking.lateral", nonlinear)


if __name__ == "__main__":
    unittest.main()
