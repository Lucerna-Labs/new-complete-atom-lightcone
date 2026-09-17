"""Deterministic, observer-only projection of full world geometry into 4-space."""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from typing import Any

import numpy as np


AXES_4D = ("x", "y", "z", "w")
EVALUATION_SPLITS = ("train", "validation", "sealed_test", "cross_domain_holdout")
SHADOW_GATE_SPECS: dict[str, tuple[str, str, Any]] = {
    "shadow_observer_only": ("shadow.observer_only", "eq", True),
    "shadow_not_used_for_admission": ("shadow.used_for_admission", "eq", False),
    "shadow_all_spatial": ("shadow.all_spatial", "eq", True),
    "shadow_has_no_time_axis": ("shadow.has_time_axis", "eq", False),
    "shadow_four_dimensions": ("shadow.target_dimensions", "eq", 4),
    "shadow_non_expansive": ("shadow.non_expansive", "eq", True),
    "shadow_deterministic_replay": ("shadow.deterministic_replay", "eq", True),
    "shadow_composes_to_3d": ("shadow.composition_3d_exact", "eq", True),
    "shadow_composes_to_2d": ("shadow.composition_2d_exact", "eq", True),
    "shadow_validation_neighbor_recall": (
        "shadow.evaluation.validation.neighbor_recall_at_k",
        "gte",
        0.1,
    ),
    "shadow_sealed_neighbor_recall": (
        "shadow.evaluation.sealed_test.neighbor_recall_at_k",
        "gte",
        0.1,
    ),
    "shadow_validation_beats_random": (
        "shadow.evaluation.validation.beats_random_basis",
        "eq",
        True,
    ),
    "shadow_validation_beats_axis_shuffle": (
        "shadow.evaluation.validation.beats_axis_shuffle",
        "eq",
        True,
    ),
    "shadow_sealed_beats_random": (
        "shadow.evaluation.sealed_test.beats_random_basis",
        "eq",
        True,
    ),
    "shadow_sealed_beats_axis_shuffle": (
        "shadow.evaluation.sealed_test.beats_axis_shuffle",
        "eq",
        True,
    ),
    "shadow_cross_domain_beats_random": (
        "shadow.edge_evaluation.cross_domain_holdout.beats_random_basis",
        "eq",
        True,
    ),
    "shadow_cross_domain_beats_axis_shuffle": (
        "shadow.edge_evaluation.cross_domain_holdout.beats_axis_shuffle",
        "eq",
        True,
    ),
}


def validate_shadow_training_config(config: dict[str, Any]) -> None:
    expected = {
        "shadow_dimensions": 4,
        "shadow_metric": "euclidean_l2",
        "shadow_fit_split": "train",
    }
    errors = [
        f"{key}={config.get(key)!r}, expected {value!r}"
        for key, value in expected.items()
        if config.get(key) != value
    ]
    for key in (
        "shadow_tolerance",
        "shadow_cell_width",
        "shadow_reach_radius",
        "shadow_knn_k",
        "shadow_random_seed_offset",
        "shadow_axis_shuffle_seed_offset",
    ):
        value = config.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            errors.append(f"{key} must be positive")
    protocol_id = config.get("protocol_id")
    if not isinstance(protocol_id, str) or not protocol_id.endswith("-v3"):
        errors.append("shadow training protocol_id must end in -v3")
    gates = config.get("gates", {})
    for gate_name, (metric, operator, threshold) in SHADOW_GATE_SPECS.items():
        gate = gates.get(gate_name)
        if gate != {"metric": metric, "operator": operator, "threshold": threshold}:
            errors.append(f"shadow gate {gate_name} differs from its registered specification")
    if errors:
        raise ValueError("invalid shadow training configuration: " + "; ".join(errors))


def canonical_hash(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _rounded(values: np.ndarray, digits: int = 12) -> list[Any]:
    if values.ndim == 1:
        return [round(float(value), digits) for value in values]
    return [_rounded(row, digits) for row in values]


def _canonicalize_row_signs(basis: np.ndarray) -> np.ndarray:
    result = np.array(basis, dtype=np.float64, copy=True)
    for row in result:
        pivot = int(np.argmax(np.abs(row)))
        if row[pivot] < 0:
            row *= -1.0
    return result


def fit_train_pca(
    coordinates: np.ndarray,
    train_indices: np.ndarray,
    target_dimensions: int,
) -> tuple[np.ndarray, np.ndarray, list[float], int]:
    """Fit an orthonormal PCA observer using training nodes only."""
    source = np.asarray(coordinates, dtype=np.float64)
    indices = np.asarray(train_indices, dtype=np.int64)
    if source.ndim != 2 or source.shape[0] < 2:
        raise ValueError("shadow projection requires at least two coordinate vectors")
    if not 1 <= target_dimensions <= source.shape[1]:
        raise ValueError("shadow target dimensions must fit within source dimensions")
    if indices.ndim != 1 or len(indices) < 2:
        raise ValueError("shadow projection requires at least two training nodes")
    if np.any(indices < 0) or np.any(indices >= source.shape[0]):
        raise ValueError("shadow training index is out of bounds")

    train = source[indices]
    center = np.mean(train, axis=0, dtype=np.float64)
    centered = train - center
    _left, singular_values, right = np.linalg.svd(centered, full_matrices=True)
    basis = _canonicalize_row_signs(right[:target_dimensions])
    squared = np.square(singular_values, dtype=np.float64)
    total = float(np.sum(squared))
    explained = [
        float(squared[index] / total) if index < len(squared) and total > 0 else 0.0
        for index in range(target_dimensions)
    ]
    tolerance = max(centered.shape) * np.finfo(np.float64).eps * (
        float(singular_values[0]) if len(singular_values) else 0.0
    )
    rank = int(np.sum(singular_values > tolerance))
    return center, basis, explained, rank


def random_orthonormal_basis(
    source_dimensions: int,
    target_dimensions: int,
    seed: int,
) -> np.ndarray:
    if not 1 <= target_dimensions <= source_dimensions:
        raise ValueError("random shadow basis dimensions are invalid")
    rng = np.random.default_rng(seed)
    raw = rng.standard_normal((source_dimensions, target_dimensions))
    orthonormal, _upper = np.linalg.qr(raw, mode="reduced")
    return _canonicalize_row_signs(orthonormal.T)


def project(
    coordinates: np.ndarray,
    center: np.ndarray,
    basis: np.ndarray,
) -> np.ndarray:
    source = np.asarray(coordinates, dtype=np.float64)
    return (source - np.asarray(center, dtype=np.float64)) @ np.asarray(
        basis, dtype=np.float64
    ).T


def _pairwise_distances(values: np.ndarray) -> np.ndarray:
    source = np.asarray(values, dtype=np.float64)
    squared_norm = np.sum(np.square(source), axis=1)
    squared = squared_norm[:, None] + squared_norm[None, :] - 2.0 * (source @ source.T)
    return np.sqrt(np.maximum(squared, 0.0))


def _quantized_cells(values: np.ndarray, width: float) -> np.ndarray:
    if not math.isfinite(width) or width <= 0:
        raise ValueError("shadow cell width must be positive and finite")
    return np.floor(np.asarray(values, dtype=np.float64) / width + 0.5).astype(np.int64)


def _neighbor_metrics(
    full_distances: np.ndarray,
    projected_distances: np.ndarray,
    query_indices: list[int],
    neighbors: int,
) -> dict[str, Any]:
    if not query_indices:
        return {
            "query_count": 0,
            "neighbor_count": neighbors,
            "neighbor_recall_at_k": 0.0,
            "distance_correlation": 0.0,
        }
    node_count = full_distances.shape[0]
    k = min(neighbors, node_count - 1)
    stable = np.arange(node_count)
    recalls: list[float] = []
    full_values: list[float] = []
    projected_values: list[float] = []
    for query in query_indices:
        full_order = np.lexsort((stable, full_distances[query]))
        projected_order = np.lexsort((stable, projected_distances[query]))
        full_neighbors = [int(index) for index in full_order if int(index) != query][:k]
        projected_neighbors = [
            int(index) for index in projected_order if int(index) != query
        ][:k]
        recalls.append(
            len(set(full_neighbors) & set(projected_neighbors)) / max(k, 1)
        )
        for target in range(node_count):
            if target == query:
                continue
            full_values.append(float(full_distances[query, target]))
            projected_values.append(float(projected_distances[query, target]))
    full_array = np.asarray(full_values, dtype=np.float64)
    projected_array = np.asarray(projected_values, dtype=np.float64)
    if np.std(full_array) <= 1e-15 or np.std(projected_array) <= 1e-15:
        correlation = 0.0
    else:
        correlation = float(np.corrcoef(full_array, projected_array)[0, 1])
    return {
        "query_count": len(query_indices),
        "neighbor_count": k,
        "neighbor_recall_at_k": float(np.mean(recalls)),
        "distance_correlation": correlation,
    }


def _edge_distance_metrics(
    *,
    edges: list[dict[str, Any]],
    split: str,
    node_index: dict[str, int],
    full_distances: np.ndarray,
    projected_distances: np.ndarray,
    random_distances: np.ndarray,
    shuffled_distances: np.ndarray,
) -> dict[str, Any]:
    selected = [
        edge
        for edge in edges
        if edge["split"] == split and edge["relation"] != "part_of"
    ]
    pairs = [
        (node_index[edge["source_node"]], node_index[edge["target_node"]])
        for edge in selected
    ]
    usable = [pair for pair in pairs if full_distances[pair] > 1e-12]
    if not usable:
        return {
            "edge_count": len(selected),
            "usable_edge_count": 0,
            "normalized_distance_stress": 1.0,
            "random_basis_normalized_distance_stress": 1.0,
            "axis_shuffle_normalized_distance_stress": 1.0,
            "stress_margin_vs_random": 0.0,
            "stress_margin_vs_axis_shuffle": 0.0,
            "beats_random_basis": False,
            "beats_axis_shuffle": False,
        }
    full = np.asarray([full_distances[pair] for pair in usable], dtype=np.float64)

    def stress(distances: np.ndarray) -> float:
        projected = np.asarray([distances[pair] for pair in usable], dtype=np.float64)
        return float(np.sqrt(np.mean(np.square(projected - full))) / np.mean(full))

    primary_stress = stress(projected_distances)
    random_stress = stress(random_distances)
    shuffled_stress = stress(shuffled_distances)
    return {
        "edge_count": len(selected),
        "usable_edge_count": len(usable),
        "normalized_distance_stress": primary_stress,
        "random_basis_normalized_distance_stress": random_stress,
        "axis_shuffle_normalized_distance_stress": shuffled_stress,
        "stress_margin_vs_random": random_stress - primary_stress,
        "stress_margin_vs_axis_shuffle": shuffled_stress - primary_stress,
        "beats_random_basis": primary_stress + 1e-12 < random_stress,
        "beats_axis_shuffle": primary_stress + 1e-12 < shuffled_stress,
    }


def _vectors(node_ids: list[str], values: np.ndarray, digits: int = 9) -> list[dict[str, Any]]:
    return [
        {
            "node_id": node_id,
            "values": [round(float(value), digits) for value in values[index]],
        }
        for index, node_id in enumerate(node_ids)
    ]


def _build_shadow_artifacts_once(
    *,
    world_id: str,
    coordinates: np.ndarray,
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    config: dict[str, Any],
) -> dict[str, Any]:
    source = np.asarray(coordinates, dtype=np.float64)
    node_ids = [str(node["node_id"]) for node in nodes]
    if source.shape[0] != len(node_ids):
        raise ValueError("shadow source coordinates do not align with graph nodes")
    target_dimensions = int(config["shadow_dimensions"])
    if target_dimensions != 4:
        raise ValueError("the registered Lightcone shadow must have exactly four axes")
    if config.get("shadow_metric") != "euclidean_l2":
        raise ValueError("shadow metric must be euclidean_l2")
    if config.get("shadow_fit_split") != "train":
        raise ValueError("shadow projection must be fitted on the train split only")
    tolerance = float(config["shadow_tolerance"])
    cell_width = float(config["shadow_cell_width"])
    reach_radius = float(config["shadow_reach_radius"])
    neighbor_count = int(config["shadow_knn_k"])
    if tolerance <= 0 or reach_radius <= 0 or neighbor_count <= 0:
        raise ValueError("shadow tolerances, radius, and neighbor count must be positive")

    train_indices = np.asarray(
        [index for index, node in enumerate(nodes) if node["split"] == "train"],
        dtype=np.int64,
    )
    center, basis, explained, train_rank = fit_train_pca(
        source, train_indices, target_dimensions
    )
    shadow = project(source, center, basis)

    random_seed = int(config["seed"]) + int(config["shadow_random_seed_offset"])
    shuffle_seed = int(config["seed"]) + int(config["shadow_axis_shuffle_seed_offset"])
    random_basis = random_orthonormal_basis(
        source.shape[1], target_dimensions, random_seed
    )
    random_shadow = project(source, center, random_basis)
    shuffle_rng = np.random.default_rng(shuffle_seed)
    axis_permutation = shuffle_rng.permutation(source.shape[1])
    shuffled_shadow = (source[:, axis_permutation] - center[axis_permutation]) @ basis.T

    arrays = (source, shadow, random_shadow, shuffled_shadow, basis, random_basis)
    if any(not np.isfinite(array).all() for array in arrays):
        raise ValueError("shadow projection produced a non-finite value")

    full_distances = _pairwise_distances(source)
    shadow_distances = _pairwise_distances(shadow)
    random_distances = _pairwise_distances(random_shadow)
    shuffled_distances = _pairwise_distances(shuffled_shadow)
    upper = np.triu_indices(len(nodes), 1)
    expansions = shadow_distances[upper] - full_distances[upper]
    maximum_expansion = float(max(0.0, np.max(expansions, initial=0.0)))
    expansion_violations = int(np.sum(expansions > tolerance))
    orthonormal_error = float(
        np.max(np.abs(basis @ basis.T - np.eye(target_dimensions)))
    )
    spectral_norm = float(np.linalg.svd(basis, compute_uv=False)[0])
    non_expansive = (
        expansion_violations == 0
        and maximum_expansion <= tolerance
        and spectral_norm <= 1.0 + tolerance
        and orthonormal_error <= tolerance
    )

    cells = _quantized_cells(shadow, cell_width)
    cell_counts = Counter(tuple(int(value) for value in row) for row in cells)
    collided_placements = sum(count for count in cell_counts.values() if count > 1)
    node_index = {node_id: index for index, node_id in enumerate(node_ids)}
    invisible_by_split = Counter()
    for edge in edges:
        source_index = node_index[edge["source_node"]]
        target_index = node_index[edge["target_node"]]
        if (
            np.array_equal(cells[source_index], cells[target_index])
            and full_distances[source_index, target_index] > tolerance
        ):
            invisible_by_split[str(edge["split"])] += 1

    full_far = full_distances[upper] > reach_radius + tolerance
    shadow_near = shadow_distances[upper] <= reach_radius + tolerance
    false_proximity = int(np.sum(full_far & shadow_near))
    full_far_count = int(np.sum(full_far))

    split_metrics: dict[str, dict[str, Any]] = {}
    for split in EVALUATION_SPLITS:
        query_indices = [
            index for index, node in enumerate(nodes) if node["split"] == split
        ]
        primary = _neighbor_metrics(
            full_distances, shadow_distances, query_indices, neighbor_count
        )
        random = _neighbor_metrics(
            full_distances, random_distances, query_indices, neighbor_count
        )
        shuffled = _neighbor_metrics(
            full_distances, shuffled_distances, query_indices, neighbor_count
        )
        primary_recall = float(primary["neighbor_recall_at_k"])
        random_recall = float(random["neighbor_recall_at_k"])
        shuffled_recall = float(shuffled["neighbor_recall_at_k"])
        split_metrics[split] = {
            **primary,
            "random_basis_neighbor_recall_at_k": random_recall,
            "axis_shuffle_neighbor_recall_at_k": shuffled_recall,
            "recall_margin_vs_random": primary_recall - random_recall,
            "recall_margin_vs_axis_shuffle": primary_recall - shuffled_recall,
            "beats_random_basis": primary_recall > random_recall + 1e-12,
            "beats_axis_shuffle": primary_recall > shuffled_recall + 1e-12,
        }
    edge_metrics = {
        split: _edge_distance_metrics(
            edges=edges,
            split=split,
            node_index=node_index,
            full_distances=full_distances,
            projected_distances=shadow_distances,
            random_distances=random_distances,
            shuffled_distances=shuffled_distances,
        )
        for split in EVALUATION_SPLITS
    }

    maximum_3d_error = 0.0
    views_3d: list[dict[str, Any]] = []
    for dropped_index, dropped_axis in enumerate(AXES_4D):
        kept = [axis for axis in AXES_4D if axis != dropped_axis]
        chained = np.delete(shadow, dropped_index, axis=1)
        direct = project(source, center, np.delete(basis, dropped_index, axis=0))
        maximum_3d_error = max(
            maximum_3d_error,
            float(np.max(np.abs(chained - direct), initial=0.0)),
        )
        views_3d.append(
            {
                "observer_id": f"drop-{dropped_axis}",
                "dropped_axes": [dropped_axis],
                "kept_axes": kept,
                "dimensions": 3,
                "vectors": _vectors(node_ids, chained),
            }
        )

    maximum_2d_error = 0.0
    views_2d: list[dict[str, Any]] = []
    for left in range(4):
        for right in range(left + 1, 4):
            kept_indices = [left, right]
            kept_axes = [AXES_4D[index] for index in kept_indices]
            dropped_axes = [axis for axis in AXES_4D if axis not in kept_axes]
            chained = shadow[:, kept_indices]
            direct = project(source, center, basis[kept_indices])
            maximum_2d_error = max(
                maximum_2d_error,
                float(np.max(np.abs(chained - direct), initial=0.0)),
            )
            views_2d.append(
                {
                    "observer_id": f"keep-{'-'.join(kept_axes)}",
                    "dropped_axes": dropped_axes,
                    "kept_axes": kept_axes,
                    "dimensions": 2,
                    "vectors": _vectors(node_ids, chained),
                }
            )

    source_coordinate_payload = {
        "dimensions": int(source.shape[1]),
        "vectors": _vectors(node_ids, source),
    }
    basis_payload = {"center": _rounded(center), "basis": _rounded(basis)}
    projection_id = f"{world_id}-all-spatial-shadow4-v1"
    projection_artifact = {
        "schema_version": 1,
        "projection_id": projection_id,
        "world_id": world_id,
        "observer_only": True,
        "used_for_admission": False,
        "all_spatial": True,
        "has_time_axis": False,
        "source_dimensions": int(source.shape[1]),
        "target_dimensions": target_dimensions,
        "axis_names": list(AXES_4D),
        "metric": "euclidean_l2",
        "method": "train_split_centered_pca_with_orthonormal_rows",
        "fit_split": "train",
        "fit_node_count": int(len(train_indices)),
        "fit_node_ids_sha256": canonical_hash(
            [node_ids[int(index)] for index in train_indices]
        ),
        "source_coordinates_sha256": canonical_hash(source_coordinate_payload),
        "basis_sha256": canonical_hash(basis_payload),
        "center": basis_payload["center"],
        "basis": basis_payload["basis"],
        "train_rank": train_rank,
        "explained_variance_ratio": [round(value, 12) for value in explained],
        "cell_quantization": {
            "method": "nearest_integer_cell",
            "cell_width": cell_width,
        },
        "reach_radius": reach_radius,
        "random_basis_placebo_seed": random_seed,
        "axis_shuffle_placebo_seed": shuffle_seed,
        "axis_shuffle_permutation": [int(value) for value in axis_permutation],
        "certificate": {
            "non_expansive": non_expansive,
            "orthonormal_max_error": orthonormal_error,
            "spectral_norm": spectral_norm,
            "maximum_distance_expansion": maximum_expansion,
            "distance_expansion_violations": expansion_violations,
            "tolerance": tolerance,
        },
    }
    shadow_coordinates = {
        "schema_version": 1,
        "projection_id": projection_id,
        "dimensions": 4,
        "axis_names": list(AXES_4D),
        "vectors": _vectors(node_ids, shadow),
    }
    observer_artifact = {
        "schema_version": 1,
        "projection_id": projection_id,
        "observer_only": True,
        "composition": {
            "three_dimensional_max_error": maximum_3d_error,
            "two_dimensional_max_error": maximum_2d_error,
            "tolerance": tolerance,
            "three_dimensional_exact": maximum_3d_error <= tolerance,
            "two_dimensional_exact": maximum_2d_error <= tolerance,
        },
        "three_dimensional": views_3d,
        "two_dimensional": views_2d,
    }
    metrics = {
        "schema_version": 1,
        "projection_id": projection_id,
        "observer_only": True,
        "used_for_admission": False,
        "all_spatial": True,
        "has_time_axis": False,
        "source_dimensions": int(source.shape[1]),
        "target_dimensions": 4,
        "finite": True,
        "fit_node_count": int(len(train_indices)),
        "non_expansive": non_expansive,
        "orthonormal_max_error": orthonormal_error,
        "spectral_norm": spectral_norm,
        "maximum_distance_expansion": maximum_expansion,
        "distance_expansion_violations": expansion_violations,
        "composition_3d_max_error": maximum_3d_error,
        "composition_2d_max_error": maximum_2d_error,
        "composition_3d_exact": maximum_3d_error <= tolerance,
        "composition_2d_exact": maximum_2d_error <= tolerance,
        "collision_classes": len(cell_counts),
        "collided_placements": collided_placements,
        "invisible_edges": int(sum(invisible_by_split.values())),
        "invisible_edges_by_split": {
            split: int(invisible_by_split[split]) for split in EVALUATION_SPLITS
        },
        "false_proximity_pairs": false_proximity,
        "full_far_pair_count": full_far_count,
        "false_proximity_rate": false_proximity / max(full_far_count, 1),
        "evaluation": split_metrics,
        "edge_evaluation": edge_metrics,
    }
    return {
        "projection": projection_artifact,
        "coordinates": shadow_coordinates,
        "observers": observer_artifact,
        "metrics": metrics,
        "shadow_array": shadow.astype(np.float32),
        "basis_array": basis.astype(np.float64),
        "random_basis_array": random_basis.astype(np.float64),
        "axis_permutation_array": axis_permutation.astype(np.int32),
    }


def build_shadow_artifacts(
    *,
    world_id: str,
    coordinates: np.ndarray,
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    config: dict[str, Any],
) -> dict[str, Any]:
    arguments = {
        "world_id": world_id,
        "coordinates": coordinates,
        "nodes": nodes,
        "edges": edges,
        "config": config,
    }
    first = _build_shadow_artifacts_once(**arguments)
    second = _build_shadow_artifacts_once(**arguments)
    json_keys = ("projection", "coordinates", "observers", "metrics")
    array_keys = (
        "shadow_array",
        "basis_array",
        "random_basis_array",
        "axis_permutation_array",
    )
    deterministic = all(first[key] == second[key] for key in json_keys) and all(
        np.array_equal(first[key], second[key]) for key in array_keys
    )
    replay_sha256 = canonical_hash({key: first[key] for key in json_keys})
    first["projection"]["deterministic_replay"] = deterministic
    first["projection"]["deterministic_replay_sha256"] = replay_sha256
    first["metrics"]["deterministic_replay"] = deterministic
    first["metrics"]["deterministic_replay_sha256"] = replay_sha256
    return first


def validate_serialized_shadow(
    *,
    full_coordinates: dict[str, Any],
    projection_artifact: dict[str, Any],
    shadow_coordinates: dict[str, Any],
    observer_artifact: dict[str, Any],
    metrics_artifact: dict[str, Any],
) -> list[str]:
    """Recompute projection and composition laws from serialized artifacts."""
    errors: list[str] = []
    projection_id = projection_artifact.get("projection_id")
    expected_axes = list(AXES_4D)
    source_dimensions = full_coordinates.get("dimensions")
    tolerance = float(
        projection_artifact.get("certificate", {}).get("tolerance", 0.0)
    )
    if (
        projection_artifact.get("schema_version") != 1
        or projection_artifact.get("observer_only") is not True
        or projection_artifact.get("used_for_admission") is not False
        or projection_artifact.get("all_spatial") is not True
        or projection_artifact.get("has_time_axis") is not False
        or projection_artifact.get("source_dimensions") != source_dimensions
        or projection_artifact.get("target_dimensions") != 4
        or projection_artifact.get("axis_names") != expected_axes
        or projection_artifact.get("metric") != "euclidean_l2"
        or projection_artifact.get("fit_split") != "train"
        or projection_artifact.get("deterministic_replay") is not True
        or not isinstance(projection_artifact.get("deterministic_replay_sha256"), str)
        or not math.isfinite(tolerance)
        or tolerance <= 0
    ):
        errors.append("projection metadata violates the 4D all-spatial observer contract")
    if (
        shadow_coordinates.get("schema_version") != 1
        or shadow_coordinates.get("projection_id") != projection_id
        or shadow_coordinates.get("dimensions") != 4
        or shadow_coordinates.get("axis_names") != expected_axes
    ):
        errors.append("shadow coordinate metadata differs from projection")
    if (
        observer_artifact.get("schema_version") != 1
        or observer_artifact.get("projection_id") != projection_id
        or observer_artifact.get("observer_only") is not True
    ):
        errors.append("observer metadata differs from projection")
    if errors:
        return errors

    center = np.asarray(projection_artifact.get("center", []), dtype=np.float64)
    basis = np.asarray(projection_artifact.get("basis", []), dtype=np.float64)
    if center.shape != (source_dimensions,) or basis.shape != (4, source_dimensions):
        return ["projection center or basis has the wrong shape"]
    if not np.isfinite(center).all() or not np.isfinite(basis).all():
        return ["projection center or basis is non-finite"]
    if canonical_hash({"center": _rounded(center), "basis": _rounded(basis)}) != projection_artifact.get(
        "basis_sha256"
    ):
        errors.append("projection basis hash does not match its serialized values")
    replay_projection = dict(projection_artifact)
    replay_projection.pop("deterministic_replay", None)
    replay_projection.pop("deterministic_replay_sha256", None)
    replay_metrics = dict(metrics_artifact)
    replay_metrics.pop("deterministic_replay", None)
    replay_metrics.pop("deterministic_replay_sha256", None)
    replay_sha256 = canonical_hash(
        {
            "projection": replay_projection,
            "coordinates": shadow_coordinates,
            "observers": observer_artifact,
            "metrics": replay_metrics,
        }
    )
    if replay_sha256 != projection_artifact.get("deterministic_replay_sha256"):
        errors.append("deterministic replay hash does not bind the serialized shadow")

    full_vectors = full_coordinates.get("vectors", [])
    shadow_vectors = shadow_coordinates.get("vectors", [])
    if canonical_hash(
        {"dimensions": source_dimensions, "vectors": full_vectors}
    ) != projection_artifact.get("source_coordinates_sha256"):
        errors.append("full-coordinate canonical hash differs from projection source hash")
    full_ids = [row.get("node_id") for row in full_vectors]
    shadow_ids = [row.get("node_id") for row in shadow_vectors]
    if (
        len(full_ids) != len(set(full_ids))
        or len(shadow_ids) != len(set(shadow_ids))
        or full_ids != shadow_ids
    ):
        return [*errors, "full and shadow vectors do not cover identical ordered nodes"]
    full = np.asarray([row.get("values", []) for row in full_vectors], dtype=np.float64)
    observed_shadow = np.asarray(
        [row.get("values", []) for row in shadow_vectors], dtype=np.float64
    )
    if full.shape != (len(full_ids), source_dimensions) or observed_shadow.shape != (
        len(full_ids),
        4,
    ):
        return [*errors, "full or shadow coordinate matrix has the wrong shape"]
    recomputed = project(full, center, basis)
    projection_error = float(
        np.max(np.abs(recomputed - observed_shadow), initial=0.0)
    )
    serialized_tolerance = max(tolerance * 4.0, 0.00002)
    if projection_error > serialized_tolerance:
        errors.append(
            f"serialized shadow differs from projection by {projection_error}"
        )
    orthonormal_error = float(np.max(np.abs(basis @ basis.T - np.eye(4))))
    if orthonormal_error > serialized_tolerance:
        errors.append("serialized projection rows are not orthonormal")
    full_distances = _pairwise_distances(full)
    shadow_distances = _pairwise_distances(observed_shadow)
    upper = np.triu_indices(len(full_ids), 1)
    expansion = shadow_distances[upper] - full_distances[upper]
    expansion_violations = int(np.sum(expansion > serialized_tolerance))
    if expansion_violations:
        errors.append(
            f"serialized shadow has {expansion_violations} distance-expansion violations"
        )
    certificate = projection_artifact.get("certificate", {})
    if (
        certificate.get("non_expansive") is not True
        or certificate.get("distance_expansion_violations") != 0
    ):
        errors.append("projection does not carry a clean non-expansion certificate")

    three_views = observer_artifact.get("three_dimensional", [])
    two_views = observer_artifact.get("two_dimensional", [])
    if len(three_views) != 4 or len(two_views) != 6:
        errors.append("observer artifact does not contain four 3D and six 2D views")
    for view in [*three_views, *two_views]:
        kept_axes = view.get("kept_axes", [])
        kept_indices = [expected_axes.index(axis) for axis in kept_axes if axis in expected_axes]
        view_values = np.asarray(
            [row.get("values", []) for row in view.get("vectors", [])],
            dtype=np.float64,
        )
        expected = observed_shadow[:, kept_indices]
        if (
            len(kept_indices) != view.get("dimensions")
            or view_values.shape != expected.shape
            or [row.get("node_id") for row in view.get("vectors", [])] != full_ids
            or float(np.max(np.abs(view_values - expected), initial=0.0))
            > serialized_tolerance
        ):
            errors.append(f"observer view {view.get('observer_id')} does not compose")
    composition = observer_artifact.get("composition", {})
    if (
        composition.get("three_dimensional_exact") is not True
        or composition.get("two_dimensional_exact") is not True
    ):
        errors.append("observer artifact does not certify 3D and 2D composition")
    if (
        metrics_artifact.get("projection_id") != projection_id
        or metrics_artifact.get("observer_only") is not True
        or metrics_artifact.get("used_for_admission") is not False
        or metrics_artifact.get("non_expansive") is not True
        or metrics_artifact.get("composition_3d_exact") is not True
        or metrics_artifact.get("composition_2d_exact") is not True
        or metrics_artifact.get("deterministic_replay") is not True
        or metrics_artifact.get("deterministic_replay_sha256")
        != projection_artifact.get("deterministic_replay_sha256")
    ):
        errors.append("shadow metrics do not preserve the projection contract")
    return errors
