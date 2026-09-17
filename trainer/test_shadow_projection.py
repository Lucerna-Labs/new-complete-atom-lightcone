from __future__ import annotations

import unittest

import numpy as np

from shadow_projection import (
    build_shadow_artifacts,
    fit_train_pca,
    project,
    random_orthonormal_basis,
    validate_serialized_shadow,
    validate_shadow_training_config,
)


class ShadowProjectionTests(unittest.TestCase):
    def test_fit_uses_training_nodes_only(self) -> None:
        coordinates = np.asarray(
            [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 10.0, 10.0],
            ]
        )
        train = np.arange(5)
        first = fit_train_pca(coordinates, train, 4)
        changed = coordinates.copy()
        changed[5] = [999.0, -999.0, 500.0, -500.0, 1000.0, -1000.0]
        second = fit_train_pca(changed, train, 4)
        np.testing.assert_array_equal(first[0], second[0])
        np.testing.assert_array_equal(first[1], second[1])

    def test_orthonormal_projection_is_non_expansive(self) -> None:
        rng = np.random.default_rng(7)
        source = rng.normal(size=(30, 12))
        basis = random_orthonormal_basis(12, 4, 91)
        shadow = project(source, np.zeros(12), basis)
        for left in range(len(source)):
            for right in range(left + 1, len(source)):
                full_distance = np.linalg.norm(source[left] - source[right])
                shadow_distance = np.linalg.norm(shadow[left] - shadow[right])
                self.assertLessEqual(shadow_distance, full_distance + 1e-10)

    def test_artifacts_report_composition_collisions_and_false_proximity(self) -> None:
        coordinates = np.asarray(
            [
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 10.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 10.0],
                [0.5, 0.5, 0.0, 0.0, 0.0, 0.0],
            ],
            dtype=np.float64,
        )
        splits = ["train"] * 5 + ["validation", "sealed_test", "cross_domain_holdout"]
        nodes = [
            {"node_id": f"node-{index}", "split": split}
            for index, split in enumerate(splits)
        ]
        edges = [
            {
                "source_node": "node-0",
                "target_node": "node-5",
                "split": "validation",
                "relation": "supports",
            }
        ]
        config = {
            "seed": 11,
            "shadow_dimensions": 4,
            "shadow_metric": "euclidean_l2",
            "shadow_fit_split": "train",
            "shadow_tolerance": 1e-8,
            "shadow_cell_width": 0.1,
            "shadow_reach_radius": 0.5,
            "shadow_knn_k": 1,
            "shadow_random_seed_offset": 101,
            "shadow_axis_shuffle_seed_offset": 211,
        }
        artifacts = build_shadow_artifacts(
            world_id="fixture-world",
            coordinates=coordinates,
            nodes=nodes,
            edges=edges,
            config=config,
        )
        metrics = artifacts["metrics"]
        self.assertTrue(metrics["observer_only"])
        self.assertFalse(metrics["used_for_admission"])
        self.assertTrue(metrics["all_spatial"])
        self.assertFalse(metrics["has_time_axis"])
        self.assertTrue(metrics["non_expansive"])
        self.assertTrue(metrics["composition_3d_exact"])
        self.assertTrue(metrics["composition_2d_exact"])
        self.assertGreater(metrics["collided_placements"], 0)
        self.assertGreater(metrics["false_proximity_pairs"], 0)
        self.assertEqual(metrics["invisible_edges_by_split"]["validation"], 1)
        self.assertEqual(len(artifacts["observers"]["three_dimensional"]), 4)
        self.assertEqual(len(artifacts["observers"]["two_dimensional"]), 6)
        full = {
            "schema_version": 1,
            "dimensions": 6,
            "vectors": [
                {
                    "node_id": node["node_id"],
                    "values": [round(float(value), 9) for value in coordinates[index]],
                }
                for index, node in enumerate(nodes)
            ],
        }
        self.assertEqual(
            validate_serialized_shadow(
                full_coordinates=full,
                projection_artifact=artifacts["projection"],
                shadow_coordinates=artifacts["coordinates"],
                observer_artifact=artifacts["observers"],
                metrics_artifact=artifacts["metrics"],
            ),
            [],
        )
        artifacts["coordinates"]["vectors"][0]["values"][0] = 99.0
        self.assertTrue(
            validate_serialized_shadow(
                full_coordinates=full,
                projection_artifact=artifacts["projection"],
                shadow_coordinates=artifacts["coordinates"],
                observer_artifact=artifacts["observers"],
                metrics_artifact=artifacts["metrics"],
            )
        )

    def test_placebo_basis_is_seed_deterministic(self) -> None:
        first = random_orthonormal_basis(48, 4, 12345)
        second = random_orthonormal_basis(48, 4, 12345)
        different = random_orthonormal_basis(48, 4, 12346)
        np.testing.assert_array_equal(first, second)
        self.assertFalse(np.array_equal(first, different))

    def test_shadow_config_rejects_missing_registered_gates(self) -> None:
        with self.assertRaisesRegex(ValueError, "registered specification"):
            validate_shadow_training_config(
                {
                    "protocol_id": "fixture-v3",
                    "shadow_dimensions": 4,
                    "shadow_metric": "euclidean_l2",
                    "shadow_fit_split": "train",
                    "shadow_tolerance": 0.00001,
                    "shadow_cell_width": 0.25,
                    "shadow_reach_radius": 1.25,
                    "shadow_knn_k": 5,
                    "shadow_random_seed_offset": 11,
                    "shadow_axis_shuffle_seed_offset": 13,
                    "gates": {},
                }
            )


if __name__ == "__main__":
    unittest.main()
