from __future__ import annotations

import unittest
import tempfile
from pathlib import Path

import numpy as np

from train_jax import (
    evaluate_edges,
    pairwise_squared_distances,
    require_fresh_output,
    validate_protocol_samples,
)


def graph(*, include_cross_edge: bool) -> dict[str, object]:
    edges = [
        {"split": "train", "relation": "supports"},
        {"split": "train", "relation": "part_of"},
    ]
    if include_cross_edge:
        edges.append({"split": "cross_domain_holdout", "relation": "supports"})
    nodes = [{"split": "train"}]
    if include_cross_edge:
        nodes.append({"split": "cross_domain_holdout"})
    return {
        "edges": edges,
        "negative_pairs": [{"split": "train"}],
        "nodes": nodes,
    }


CONFIG = {
    "gates": {
        "cross_domain_edge_discrimination": {
            "metric": "edges.cross_domain_holdout.edge_discrimination_accuracy",
            "operator": "gte",
            "threshold": 0.5,
        }
    }
}


class ProtocolSampleTests(unittest.TestCase):
    def test_pairwise_distance_algebra_matches_broadcast_reference(self) -> None:
        query = np.asarray(
            [[0.0, 1.0, -2.0], [4.0, -3.0, 2.0]], dtype=np.float32
        )
        nodes = np.asarray(
            [[1.0, 0.0, 2.0], [-2.0, 3.0, 1.0], [4.0, -3.0, 2.0]],
            dtype=np.float32,
        )
        expected = np.sum(
            (query[:, None, :] - nodes[None, :, :]) ** 2, axis=2
        )
        observed = pairwise_squared_distances(np, query, nodes)
        np.testing.assert_allclose(observed, expected, rtol=1e-6, atol=1e-6)

    def test_empty_gated_split_is_rejected(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "edges.cross_domain_holdout"):
            validate_protocol_samples(graph(include_cross_edge=False), CONFIG)

    def test_populated_gated_split_is_accepted(self) -> None:
        counts = validate_protocol_samples(graph(include_cross_edge=True), CONFIG)
        self.assertEqual(counts["edges"]["cross_domain_holdout"], 1)

    def test_heldout_relation_requires_training_support(self) -> None:
        fixture = graph(include_cross_edge=True)
        fixture["edges"][-1]["relation"] = "clarifies"
        with self.assertRaisesRegex(RuntimeError, "relation.clarifies.training_support"):
            validate_protocol_samples(fixture, CONFIG)

    def test_empty_shadow_evaluation_split_is_rejected(self) -> None:
        config = {
            "gates": {
                "shadow_sealed": {
                    "metric": "shadow.evaluation.sealed_test.neighbor_recall_at_k",
                    "operator": "gte",
                    "threshold": 0.1,
                }
            }
        }
        with self.assertRaisesRegex(RuntimeError, "nodes.sealed_test"):
            validate_protocol_samples(graph(include_cross_edge=True), config)

    def test_nonempty_output_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            output = Path(raw)
            (output / "stale.json").write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "stale artifact"):
                require_fresh_output(output)

    def test_missing_output_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            require_fresh_output(Path(raw) / "new-output")

    def test_edge_discrimination_is_exact_pairwise_win_rate(self) -> None:
        nodes = np.asarray([[0.0], [1.0], [2.0]], dtype=np.float32)
        relations = np.asarray([[1.4]], dtype=np.float32)
        arrays = {
            "source": np.asarray([0], dtype=np.int32),
            "target": np.asarray([2], dtype=np.int32),
            "relation": np.asarray([0], dtype=np.int32),
            "polarity": np.asarray([1.0], dtype=np.float32),
            "forward": np.asarray([True], dtype=np.bool_),
        }
        metrics = evaluate_edges(nodes, relations, arrays)
        self.assertEqual(metrics["edge_discrimination_accuracy"], 0.5)
        self.assertEqual(
            metrics["edge_discrimination_method"],
            "all_non_target_pairwise_win_rate_v1",
        )



if __name__ == "__main__":
    unittest.main()
