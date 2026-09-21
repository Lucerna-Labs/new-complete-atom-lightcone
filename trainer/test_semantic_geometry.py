from __future__ import annotations

import unittest

import numpy as np

from semantic_geometry import (
    build_evidence_index,
    build_semantic_overlay,
    evaluate_evidence_edges,
    validate_protocol_v3_config,
)


CONFIG = {
    "protocol_id": "fixture-v3",
    "coordinate_dimensions": 48,
    "edge_discrimination_method": "all_non_target_pairwise_win_rate_v1",
    "train_edge_evaluation_method": "jax_translation",
    "world_id": "fixture-world",
    "evidence_feature_dimensions": 2048,
    "relation_prior_weight": 2.0,
    "semantic_overlay_feature_dimensions": 1024,
    "semantic_overlay_text_dimensions": 2,
    "semantic_overlay_text_scale": 0.3,
    "semantic_overlay_negative_scale": 1.3,
    "semantic_overlay_stage_scale": 0.8,
    "semantic_overlay_residual_scale": 0.03,
}


def node(node_id: str, split: str, text: str, *tags: str) -> dict[str, object]:
    return {
        "node_id": node_id,
        "split": split,
        "text": text,
        "domain_id": "fixture",
        "subject_id": "fixture.topic",
        "lanes": ["reasoning.causal"],
        "epistemic_class": "synthetic_control" if "negative-control" in tags else "established",
        "tags": list(tags),
    }


class SemanticGeometryTests(unittest.TestCase):
    def test_exact_authored_target_label_is_retrieved_without_target_id(self) -> None:
        config = {
            **CONFIG,
            "world_id": "coverage-closure-v0",
            "train_edge_evaluation_method": "train_fitted_evidence",
            "evidence_exact_label_weight": 2.0,
        }
        nodes = [
            {**node("source", "train", "orbital source"), "label": "Orbital source anchor"},
            {**node("target", "train", "resonant destination"), "label": "Resonant target anchor"},
            {**node("other", "train", "resonant destination"), "label": "Other target anchor"},
        ]
        edges = [
            {
                "source_node": "source",
                "target_node": "target",
                "relation": "supports",
                "split": "train",
                "text": "Orbital evidence supports Resonant target anchor.",
            }
        ]
        catalog = {
            "relations": [
                {
                    "id": "supports",
                    "definition": "Provides evidence for a target.",
                    "lexical_cues": ["support", "supports"],
                }
            ]
        }
        evidence, artifact = build_evidence_index(nodes, edges, catalog, config)
        metrics = evaluate_evidence_edges(
            nodes=nodes,
            edges=edges,
            edge_indices=[0],
            evidence=evidence,
            relation_prior_weight=2.0,
        )
        self.assertEqual(artifact["exact_label_weight"], 2.0)
        self.assertEqual(metrics["hits_at_1"], 1.0)

    def test_overlay_is_train_only_and_keeps_48_dimensions(self) -> None:
        nodes = [
            node("a", "train", "alpha cause"),
            node("b", "train", "beta outcome"),
            node("c", "train", "gamma evidence"),
            node("d", "train", "delta mechanism"),
            node("held", "sealed_test", "held out representation"),
        ]
        base = np.arange(5 * 48, dtype=np.float32).reshape(5, 48) / 100.0
        first, first_artifact = build_semantic_overlay(base, nodes, CONFIG)
        changed = [dict(item) for item in nodes]
        changed[-1] = {**changed[-1], "text": "completely changed held out words"}
        second, second_artifact = build_semantic_overlay(base, changed, CONFIG)
        self.assertEqual(first.shape, (5, 48))
        self.assertEqual(first_artifact["basis_sha256"], second_artifact["basis_sha256"])
        np.testing.assert_array_equal(first[:4], second[:4])
        self.assertFalse(np.array_equal(first[4], second[4]))

    def test_evidence_index_fits_only_training_documents(self) -> None:
        nodes = [
            node("source", "train", "pressure force"),
            node("target", "train", "motion acceleration"),
            node("other", "sealed_test", "unrelated poetry"),
        ]
        edges = [
            {
                "source_node": "source",
                "target_node": "target",
                "relation": "causes",
                "split": "train",
                "text": "Force causes acceleration and motion",
            },
            {
                "source_node": "source",
                "target_node": "target",
                "relation": "causes",
                "split": "sealed_test",
                "text": "Pressure produces acceleration",
            },
        ]
        catalog = {
            "relations": [
                {
                    "id": "causes",
                    "definition": "Produces an outcome.",
                    "lexical_cues": ["cause", "causes", "produces"],
                }
            ]
        }
        evidence, artifact = build_evidence_index(nodes, edges, catalog, CONFIG)
        changed = [dict(edge) for edge in edges]
        changed[1] = {**changed[1], "text": "sealed words changed"}
        _second, second_artifact = build_evidence_index(nodes, changed, catalog, CONFIG)
        self.assertEqual(artifact["idf_sha256"], second_artifact["idf_sha256"])
        metrics = evaluate_evidence_edges(
            nodes=nodes,
            edges=edges,
            edge_indices=[1],
            evidence=evidence,
            relation_prior_weight=2.0,
        )
        self.assertEqual(metrics["count"], 1)
        self.assertEqual(metrics["relation_accuracy"], 1.0)
        self.assertGreaterEqual(metrics["edge_discrimination_accuracy"], 0.5)

    def test_protocol_values_are_frozen(self) -> None:
        validate_protocol_v3_config(CONFIG)
        changed = {**CONFIG, "semantic_overlay_residual_scale": 0.5}
        with self.assertRaisesRegex(ValueError, "registered|protocol-v3"):
            validate_protocol_v3_config(changed)

    def test_coverage_world_uses_registered_dense_world_controls(self) -> None:
        coverage = {
            **CONFIG,
            "world_id": "coverage-closure-v0",
            "train_edge_evaluation_method": "train_fitted_evidence",
            "evidence_exact_label_weight": 2.0,
            "semantic_overlay_residual_scale": 0.005,
        }
        validate_protocol_v3_config(coverage)
        with self.assertRaisesRegex(ValueError, "registered|protocol-v3"):
            validate_protocol_v3_config(
                {**coverage, "semantic_overlay_residual_scale": 0.03}
            )


if __name__ == "__main__":
    unittest.main()
