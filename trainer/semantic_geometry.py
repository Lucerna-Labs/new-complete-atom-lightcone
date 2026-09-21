#!/usr/bin/env python3
"""Train-only semantic geometry and evidence-to-graph evaluation.

The exact graph remains authoritative.  This module learns deterministic text
statistics from training records only.  It never changes graph reachability or
uses validation/sealed labels while fitting its IDF, PCA, or relation centroids.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from typing import Any

import numpy as np


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def tokens(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9+#]+", text.lower())
    return [*words, *(f"w2:{left}_{right}" for left, right in zip(words, words[1:]))]


def normalized_phrase(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9+#]+", text.lower()))


def exact_label_indices(
    text: str,
    lookup: dict[str, np.ndarray],
    lengths: tuple[int, ...],
) -> np.ndarray:
    words = normalized_phrase(text).split()
    matches: set[int] = set()
    for length in lengths:
        if length > len(words):
            continue
        for start in range(len(words) - length + 1):
            phrase = " ".join(words[start : start + length])
            indices = lookup.get(phrase)
            if indices is not None:
                matches.update(int(index) for index in indices)
    return np.asarray(sorted(matches), dtype=np.int64)


def hashed_text_matrix(texts: list[str], dimensions: int) -> np.ndarray:
    if dimensions < 256:
        raise ValueError("evidence feature dimensions must be at least 256")
    matrix = np.zeros((len(texts), dimensions), dtype=np.float64)
    for row_index, text in enumerate(texts):
        for feature in tokens(text):
            digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=16).digest()
            index = int.from_bytes(digest[:8], "little") % dimensions
            matrix[row_index, index] += 1.0 if digest[8] & 1 else -1.0
    return matrix


def _normalize_rows(values: np.ndarray) -> np.ndarray:
    return values / np.maximum(np.linalg.norm(values, axis=1, keepdims=True), 1e-12)


def _canonicalize_row_signs(basis: np.ndarray) -> np.ndarray:
    result = np.array(basis, dtype=np.float64, copy=True)
    for row in result:
        pivot = int(np.argmax(np.abs(row)))
        if row[pivot] < 0:
            row *= -1.0
    return result


def _stage_index(node: dict[str, Any]) -> int:
    for tag in node.get("tags", []):
        if tag.startswith("stage-index-") and tag.rsplit("-", 1)[1].isdigit():
            return int(tag.rsplit("-", 1)[1])
    return 0


def overlay_feature_matrix(nodes: list[dict[str, Any]], dimensions: int) -> np.ndarray:
    if dimensions < 32:
        raise ValueError("semantic overlay feature dimensions must be at least 32")
    matrix = np.zeros((len(nodes), dimensions), dtype=np.float64)
    for row_index, node in enumerate(nodes):
        words = re.findall(r"[a-z0-9+#]+", node["text"].lower())
        compact = "_".join(words)
        features = [
            *words,
            *(f"word2:{left}_{right}" for left, right in zip(words, words[1:])),
            *(f"char3:{compact[index:index + 3]}" for index in range(max(0, len(compact) - 2))),
            f"domain:{node['domain_id']}",
            f"subject:{node['subject_id']}",
            f"epistemic:{node['epistemic_class']}",
            *(f"lane:{lane}" for lane in node["lanes"]),
            *(f"tag:{tag}" for tag in node.get("tags", [])),
        ]
        for feature in features:
            digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=16).digest()
            index = int.from_bytes(digest[:8], "little") % dimensions
            matrix[row_index, index] += 1.0 if digest[8] & 1 else -1.0
    return _normalize_rows(matrix)


def build_semantic_overlay(
    base_coordinates: np.ndarray,
    nodes: list[dict[str, Any]],
    config: dict[str, Any],
) -> tuple[np.ndarray, dict[str, Any]]:
    """Make a train-fitted four-coordinate semantic backbone plus 44D residual."""
    source = np.asarray(base_coordinates, dtype=np.float64)
    if source.ndim != 2 or source.shape[1] != int(config["coordinate_dimensions"]):
        raise ValueError("semantic overlay source coordinate dimensions differ from config")
    if source.shape[1] != 48:
        raise ValueError("protocol-v3 semantic overlay requires 48 source dimensions")
    train_indices = np.asarray(
        [index for index, node in enumerate(nodes) if node["split"] == "train"],
        dtype=np.int64,
    )
    if len(train_indices) < 4:
        raise ValueError("semantic overlay requires at least four training nodes")
    feature_dimensions = int(config["semantic_overlay_feature_dimensions"])
    text_dimensions = int(config["semantic_overlay_text_dimensions"])
    if text_dimensions != 2:
        raise ValueError("protocol-v3 reserves two semantic PCA coordinates")
    features = overlay_feature_matrix(nodes, feature_dimensions)
    center = np.mean(features[train_indices], axis=0, dtype=np.float64)
    centered = features - center
    _left, singular_values, right = np.linalg.svd(
        centered[train_indices], full_matrices=False
    )
    basis = _canonicalize_row_signs(right[:text_dimensions])
    semantic = centered @ basis.T
    scale = np.std(semantic[train_indices], axis=0, keepdims=True)
    semantic = semantic / np.maximum(scale, 1e-6)
    semantic = np.clip(semantic, -2.0, 2.0) * float(
        config["semantic_overlay_text_scale"]
    )
    negative = np.asarray(
        [
            1.0
            if "negative-control" in node.get("tags", [])
            or node["epistemic_class"] == "synthetic_control"
            else 0.0
            for node in nodes
        ],
        dtype=np.float64,
    )[:, None] * float(config["semantic_overlay_negative_scale"])
    stage = np.asarray([_stage_index(node) for node in nodes], dtype=np.float64)[:, None]
    stage *= float(config["semantic_overlay_stage_scale"]) / 8.0
    backbone = np.concatenate([negative, stage, semantic], axis=1)
    backbone -= np.mean(backbone[train_indices], axis=0, dtype=np.float64)
    residual = source[:, 4:] * float(config["semantic_overlay_residual_scale"])
    result = np.concatenate([backbone, residual], axis=1).astype(np.float32)
    squared = np.square(singular_values, dtype=np.float64)
    total = float(np.sum(squared))
    artifact = {
        "schema_version": 1,
        "method": "train_only_text_pca_four_coordinate_backbone_v1",
        "fit_split": "train",
        "fit_node_count": int(len(train_indices)),
        "fit_node_ids_sha256": canonical_hash(
            [nodes[int(index)]["node_id"] for index in train_indices]
        ),
        "feature_dimensions": feature_dimensions,
        "semantic_dimensions": text_dimensions,
        "negative_scale": float(config["semantic_overlay_negative_scale"]),
        "stage_scale": float(config["semantic_overlay_stage_scale"]),
        "semantic_scale": float(config["semantic_overlay_text_scale"]),
        "residual_scale": float(config["semantic_overlay_residual_scale"]),
        "feature_center_sha256": canonical_hash([round(float(value), 12) for value in center]),
        "basis_sha256": canonical_hash(
            [[round(float(value), 12) for value in row] for row in basis]
        ),
        "explained_variance_ratio": [
            float(squared[index] / total) if total > 0 else 0.0
            for index in range(text_dimensions)
        ],
        "finite": bool(np.isfinite(result).all()),
    }
    return result, artifact


def build_evidence_index(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    relation_catalog: dict[str, Any],
    config: dict[str, Any],
) -> tuple[dict[str, np.ndarray], dict[str, Any]]:
    dimensions = int(config["evidence_feature_dimensions"])
    node_raw = hashed_text_matrix([node["text"] for node in nodes], dimensions)
    edge_raw = hashed_text_matrix([edge["text"] for edge in edges], dimensions)
    fit_rows = [
        *[node_raw[index] for index, node in enumerate(nodes) if node["split"] == "train"],
        *[edge_raw[index] for index, edge in enumerate(edges) if edge["split"] == "train"],
    ]
    fit = np.asarray(fit_rows, dtype=np.float64)
    document_frequency = np.sum(np.abs(fit) > 1e-12, axis=0)
    idf = np.log((1.0 + len(fit)) / (1.0 + document_frequency)) + 1.0
    node_vectors = _normalize_rows(node_raw * idf)
    edge_vectors = _normalize_rows(edge_raw * idf)
    label_rows: dict[str, list[int]] = {}
    for index, node in enumerate(nodes):
        phrase = normalized_phrase(str(node.get("label", node["node_id"])))
        if phrase:
            label_rows.setdefault(phrase, []).append(index)
    label_lookup = {
        phrase: np.asarray(indices, dtype=np.int64)
        for phrase, indices in label_rows.items()
    }
    label_lengths = tuple(sorted({len(phrase.split()) for phrase in label_lookup}))
    relations = sorted({edge["relation"] for edge in edges if edge["relation"] != "part_of"})
    train_relations = {
        relation: [
            index
            for index, edge in enumerate(edges)
            if edge["split"] == "train" and edge["relation"] == relation
        ]
        for relation in relations
    }
    empty = sorted(relation for relation, indices in train_relations.items() if not indices)
    if empty:
        raise ValueError(f"relations lack training evidence: {empty}")
    centroids = np.asarray(
        [np.mean(edge_vectors[train_relations[relation]], axis=0) for relation in relations],
        dtype=np.float64,
    )
    centroids = _normalize_rows(centroids)
    catalog = {item["id"]: item for item in relation_catalog["relations"]}
    missing = sorted(set(relations) - set(catalog))
    if missing:
        raise ValueError(f"relation catalog lacks training relations: {missing}")
    priors = _normalize_rows(
        hashed_text_matrix(
            [
                " ".join(
                    [catalog[relation]["definition"], *catalog[relation]["lexical_cues"]]
                )
                for relation in relations
            ],
            dimensions,
        )
        * idf
    )
    arrays = {
        "node_vectors": node_vectors,
        "edge_vectors": edge_vectors,
        "relation_centroids": centroids,
        "relation_priors": priors,
        "idf": idf,
        "relations": np.asarray(relations, dtype=object),
        "label_lookup": label_lookup,
        "label_lengths": label_lengths,
        "exact_label_weight": float(config.get("evidence_exact_label_weight", 0.0)),
    }
    artifact = {
        "schema_version": 1,
        "method": "train_fitted_hashed_tfidf_plus_exact_label_v2",
        "fit_split": "train",
        "feature_dimensions": dimensions,
        "fit_document_count": int(len(fit)),
        "relation_prior_weight": float(config["relation_prior_weight"]),
        "exact_label_weight": float(config.get("evidence_exact_label_weight", 0.0)),
        "label_phrase_sha256": canonical_hash(sorted(label_lookup)),
        "relations": relations,
        "idf_sha256": canonical_hash([round(float(value), 12) for value in idf]),
        "relation_centroids_sha256": canonical_hash(
            [[round(float(value), 12) for value in row] for row in centroids]
        ),
        "relation_priors_sha256": canonical_hash(
            [[round(float(value), 12) for value in row] for row in priors]
        ),
    }
    return arrays, artifact


def evaluate_evidence_edges(
    *,
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    edge_indices: list[int],
    evidence: dict[str, np.ndarray],
    relation_prior_weight: float,
) -> dict[str, Any]:
    if not edge_indices:
        return {
            "count": 0,
            "hits_at_1": 0.0,
            "hits_at_5": 0.0,
            "hits_at_10": 0.0,
            "mrr": 0.0,
            "direction_accuracy": 0.0,
            "edge_discrimination_accuracy": 0.0,
            "relation_accuracy": 0.0,
        }
    node_index = {node["node_id"]: index for index, node in enumerate(nodes)}
    relation_index = {
        str(relation): index for index, relation in enumerate(evidence["relations"])
    }
    exact_label_weight = float(evidence.get("exact_label_weight", 0.0))
    ranks: list[int] = []
    wins: list[float] = []
    directions: list[bool] = []
    relations_correct: list[bool] = []
    for edge_index in edge_indices:
        edge = edges[edge_index]
        vector = evidence["edge_vectors"][edge_index]
        scores = evidence["node_vectors"] @ vector
        if exact_label_weight > 0.0:
            matches = exact_label_indices(
                edge["text"], evidence["label_lookup"], evidence["label_lengths"]
            )
            scores[matches] += exact_label_weight
        target = node_index[edge["target_node"]]
        source = node_index[edge["source_node"]]
        target_score = float(scores[target])
        rank = 1 + int(np.sum(scores > target_score + 1e-12))
        ranks.append(rank)
        won = scores < target_score - 1e-12
        won[target] = False
        wins.append(float(np.sum(won)) / max(len(nodes) - 1, 1))
        directions.append(target_score > float(scores[source]) + 1e-12)
        relation_scores = evidence["relation_centroids"] @ vector
        relation_scores += relation_prior_weight * (evidence["relation_priors"] @ vector)
        relations_correct.append(
            int(np.argmax(relation_scores)) == relation_index[edge["relation"]]
        )
    count = len(edge_indices)
    return {
        "count": count,
        "hits_at_1": sum(rank <= 1 for rank in ranks) / count,
        "hits_at_5": sum(rank <= 5 for rank in ranks) / count,
        "hits_at_10": sum(rank <= 10 for rank in ranks) / count,
        "mrr": float(np.mean([1.0 / rank for rank in ranks])),
        "mean_rank": float(np.mean(ranks)),
        "direction_accuracy": sum(directions) / count,
        "edge_discrimination_accuracy": float(np.mean(wins)),
        "edge_discrimination_method": "all_non_target_pairwise_win_rate_v1",
        "retrieval_method": "train_fitted_hashed_tfidf_plus_exact_label_v2",
        "relation_accuracy": sum(relations_correct) / count,
        "relation_classification_method": "train_centroid_plus_registered_semantic_prior_v1",
    }


def validate_protocol_v3_config(config: dict[str, Any]) -> None:
    expected: dict[str, Any] = {
        "edge_discrimination_method": "all_non_target_pairwise_win_rate_v1",
        "evidence_feature_dimensions": 2048,
        "relation_prior_weight": 2.0,
        "semantic_overlay_feature_dimensions": 1024,
        "semantic_overlay_text_dimensions": 2,
        "semantic_overlay_text_scale": 0.3,
        "semantic_overlay_negative_scale": 1.3,
        "semantic_overlay_stage_scale": 0.8,
        "semantic_overlay_residual_scale": (
            0.005 if config.get("world_id") == "coverage-closure-v0" else 0.03
        ),
    }
    errors = [
        f"{key}={config.get(key)!r}, expected {value!r}"
        for key, value in expected.items()
        if config.get(key) != value
    ]
    expected_label_weight = 2.0 if config.get("world_id") == "coverage-closure-v0" else 0.0
    observed_label_weight = float(config.get("evidence_exact_label_weight", 0.0))
    if observed_label_weight != expected_label_weight:
        errors.append(
            f"evidence_exact_label_weight={observed_label_weight!r}, expected {expected_label_weight!r}"
        )
    train_method = config.get("train_edge_evaluation_method")
    allowed_train_methods = {"jax_translation", "train_fitted_evidence"}
    if train_method not in allowed_train_methods:
        errors.append(
            f"train_edge_evaluation_method={train_method!r}, expected one of {sorted(allowed_train_methods)}"
        )
    evidence_world = str(config.get("world_id", "")).startswith("taxonomy-") or config.get("world_id") == "coverage-closure-v0"
    if evidence_world and train_method != "train_fitted_evidence":
        errors.append("taxonomy and coverage-audit worlds must train and score evidence-to-descriptor recovery")
    if not evidence_world and train_method != "jax_translation":
        errors.append("curated causal worlds must retain JAX translation training evaluation")
    if not str(config.get("protocol_id", "")).endswith("-v3"):
        errors.append("semantic geometry protocol_id must end in -v3")
    if errors:
        raise ValueError("invalid protocol-v3 semantic geometry configuration: " + "; ".join(errors))
