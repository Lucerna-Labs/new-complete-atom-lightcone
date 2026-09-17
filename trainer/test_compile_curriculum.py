#!/usr/bin/env python3
"""Regression tests for deterministic curriculum compilation boundaries."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from compile_curriculum import compile_bundle, find_lane_roots  # noqa: E402


class LaneRootTests(unittest.TestCase):
    def test_relation_identifier_ending_in_root_is_never_a_lane_root(self) -> None:
        records = [
            {
                "record_id": "membership.topic.root",
                "record_kind": "relation",
                "lanes": ["reasoning.deductive"],
            },
            {
                "record_id": "topic.root",
                "record_kind": "concept",
                "lanes": ["reasoning.deductive"],
            },
        ]
        self.assertEqual(
            find_lane_roots(records),
            {"reasoning.deductive": "topic.root"},
        )

    def test_first_concept_root_per_lane_is_deterministic(self) -> None:
        records = [
            {"record_id": "a.root", "record_kind": "concept", "lanes": ["lane"]},
            {"record_id": "b.root", "record_kind": "concept", "lanes": ["lane"]},
        ]
        self.assertEqual(find_lane_roots(records), {"lane": "a.root"})


class EvidenceTextTests(unittest.TestCase):
    def test_compiled_graph_retains_relation_evidence_text(self) -> None:
        import tempfile
        import json

        with tempfile.TemporaryDirectory() as raw:
            graph_path = Path(raw) / "training-graph.json"
            compile_bundle("rust-orchestrator-apps-v0", Path(raw))
            graph = json.loads(graph_path.read_text(encoding="utf-8"))
            edge = next(item for item in graph["edges"] if item["relation"] != "part_of")
            self.assertTrue(edge["text"].strip())
            self.assertIn("\n", edge["text"])
            node = graph["nodes"][0]
            self.assertIn("label", node)
            self.assertIn("aliases", node)


if __name__ == "__main__":
    unittest.main()
