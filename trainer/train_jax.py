#!/usr/bin/env python3
"""Train model-independent causal-world coordinates with JAX on Kaggle TPU.

The exact graph remains authoritative. This trainer learns geometric
coordinates for seed locality and typed-edge recovery; it does not create facts
or verdicts. A run configured with --require-tpu fails unless JAX places the
training state on a real TPU device.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
import re
import time
from pathlib import Path
from typing import Any

import numpy as np


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def find_bundle(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit
    candidates = sorted(Path("/kaggle/input").rglob("training-graph.json"))
    if len(candidates) != 1:
        raise RuntimeError(f"expected exactly one training-graph.json under /kaggle/input, found {len(candidates)}")
    return candidates[0].parent


def verify_bundle(root: Path) -> dict[str, Any]:
    manifest_path = root / "bundle-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    mismatches = []
    for relative, expected in manifest["files"].items():
        observed = file_hash(root / relative)
        if observed != expected:
            mismatches.append({"file": relative, "expected": expected, "observed": observed})
    if mismatches:
        raise RuntimeError(f"input bundle hash mismatch: {mismatches}")
    return manifest


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9+#]+", text.lower())
    features = list(words)
    features.extend(f"word2:{left}_{right}" for left, right in zip(words, words[1:]))
    compact = "_".join(words)
    features.extend(f"char3:{compact[index:index + 3]}" for index in range(max(0, len(compact) - 2)))
    return features


def feature_matrix(nodes: list[dict[str, Any]], dimensions: int) -> np.ndarray:
    if dimensions < 32:
        raise ValueError("feature_dimensions must be at least 32")
    matrix = np.zeros((len(nodes), dimensions), dtype=np.float32)
    for row_index, node in enumerate(nodes):
        tags = node.get("tags", [])
        stage_index = next(
            (int(tag.rsplit("-", 1)[1]) for tag in tags if tag.startswith("stage-index-") and tag.rsplit("-", 1)[1].isdigit()),
            None,
        )
        lane_length = next(
            (int(tag.rsplit("-", 1)[1]) for tag in tags if tag.startswith("lane-length-") and tag.rsplit("-", 1)[1].isdigit()),
            None,
        )
        matrix[row_index, 0] = 1.0
        matrix[row_index, 1] = float(stage_index or 0) / 8.0
        matrix[row_index, 2] = 1.0 if stage_index is not None and stage_index > 0 else 0.0
        matrix[row_index, 3] = 1.0 if stage_index == 0 else 0.0
        matrix[row_index, 4] = 1.0 if "negative-control" in tags else 0.0
        matrix[row_index, 5] = 1.0 if node["epistemic_class"] == "synthetic_control" else 0.0
        matrix[row_index, 6] = min(4.0, float(len(node["lanes"]))) / 4.0
        matrix[row_index, 7] = min(16.0, float(lane_length or 0)) / 16.0
        structured = [
            f"domain:{node['domain_id']}",
            f"subject:{node['subject_id']}",
            f"epistemic:{node['epistemic_class']}",
            *(f"lane:{lane}" for lane in node["lanes"]),
            *(f"tag:{tag}" for tag in node.get("tags", [])),
        ]
        for feature in [*tokenize(node["text"]), *structured]:
            digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=16).digest()
            index = 8 + int.from_bytes(digest[:8], "little") % (dimensions - 8)
            sign = 1.0 if digest[8] & 1 else -1.0
            matrix[row_index, index] += sign
    lexical_norms = np.linalg.norm(matrix[:, 8:], axis=1, keepdims=True)
    matrix[:, 8:] /= np.maximum(lexical_norms, 1e-8)
    return matrix


def structural_matrix(nodes: list[dict[str, Any]], dimensions: int) -> np.ndarray:
    if dimensions < 24:
        raise ValueError("structural_dimensions must be at least 24")
    matrix = np.zeros((len(nodes), dimensions), dtype=np.float32)
    for row_index, node in enumerate(nodes):
        tags = node.get("tags", [])
        stage_index = next(
            (int(tag.rsplit("-", 1)[1]) for tag in tags if tag.startswith("stage-index-") and tag.rsplit("-", 1)[1].isdigit()),
            None,
        )
        lane_length = next(
            (int(tag.rsplit("-", 1)[1]) for tag in tags if tag.startswith("lane-length-") and tag.rsplit("-", 1)[1].isdigit()),
            None,
        )
        matrix[row_index, 0] = float(stage_index or 0) / 8.0
        matrix[row_index, 1] = 1.0 if "negative-control" in tags else 0.0
        matrix[row_index, 2] = 1.0 if node["epistemic_class"] == "synthetic_control" else 0.0
        matrix[row_index, 3] = 0.25 if stage_index == 0 else 0.0
        matrix[row_index, 4] = 0.25 if stage_index is not None and stage_index > 0 else 0.0
        matrix[row_index, 5] = min(16.0, float(lane_length or 0)) / 16.0
        matrix[row_index, 6] = min(4.0, float(len(node["lanes"]))) / 4.0
        matrix[row_index, 7] = 1.0
        for lane in node["lanes"]:
            digest = hashlib.blake2b(f"lane:{lane}".encode("utf-8"), digest_size=16).digest()
            for offset in range(12):
                matrix[row_index, 8 + offset] += 1.0 if digest[offset] & 1 else -1.0
        if node["lanes"]:
            matrix[row_index, 8:20] /= math.sqrt(12.0) * len(node["lanes"])
        domain_digest = hashlib.blake2b(f"domain:{node['domain_id']}".encode("utf-8"), digest_size=8).digest()
        for offset in range(4):
            matrix[row_index, 20 + offset] = 0.5 if domain_digest[offset] & 1 else -0.5
    return matrix


def arrays_for_edges(edges: list[dict[str, Any]], node_index: dict[str, int], relation_index: dict[str, int]) -> dict[str, np.ndarray]:
    return {
        "source": np.asarray([node_index[edge["source_node"]] for edge in edges], dtype=np.int32),
        "target": np.asarray([node_index[edge["target_node"]] for edge in edges], dtype=np.int32),
        "relation": np.asarray([relation_index[edge["relation"]] for edge in edges], dtype=np.int32),
        "polarity": np.asarray([edge["polarity"] if edge["polarity"] != 0 else 1 for edge in edges], dtype=np.float32),
        "forward": np.asarray([edge["direction"] == "forward" for edge in edges], dtype=np.bool_),
    }


def arrays_for_pairs(pairs: list[dict[str, Any]], node_index: dict[str, int]) -> dict[str, np.ndarray]:
    return {
        "left": np.asarray([node_index[pair["left_node"]] for pair in pairs], dtype=np.int32),
        "right": np.asarray([node_index[pair["right_node"]] for pair in pairs], dtype=np.int32),
    }


def evaluate_edges(node: np.ndarray, relation: np.ndarray, arrays: dict[str, np.ndarray]) -> dict[str, Any]:
    count = len(arrays["source"])
    if count == 0:
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
    ranks: list[int] = []
    direction: list[bool] = []
    discriminated: list[bool] = []
    relation_correct: list[bool] = []
    for source, target, relation_id, polarity, is_forward in zip(
        arrays["source"], arrays["target"], arrays["relation"], arrays["polarity"], arrays["forward"], strict=True
    ):
        rel = relation[int(relation_id)] * float(polarity)
        query = node[int(source)] + rel
        distances = np.sum((node - query) ** 2, axis=1)
        target_distance = float(distances[int(target)])
        ranks.append(1 + int(np.sum(distances < target_distance - 1e-9)))
        negative_target = (
            int(target) + int(source) * 17 + int(relation_id) * 13 + 7
        ) % len(node)
        if negative_target == int(target):
            negative_target = (negative_target + 1) % len(node)
        discriminated.append(target_distance < float(distances[negative_target]))
        relation_distances = np.sum(
            (
                node[int(source)][None, :]
                + relation * float(polarity)
                - node[int(target)][None, :]
            )
            ** 2,
            axis=1,
        )
        relation_correct.append(
            int(np.argmin(relation_distances)) == int(relation_id)
        )
        if bool(is_forward):
            forward_distance = float(np.sum((node[int(source)] + rel - node[int(target)]) ** 2))
            reverse_distance = float(np.sum((node[int(target)] + rel - node[int(source)]) ** 2))
            direction.append(forward_distance < reverse_distance)
    return {
        "count": count,
        "hits_at_1": sum(rank <= 1 for rank in ranks) / count,
        "hits_at_5": sum(rank <= 5 for rank in ranks) / count,
        "hits_at_10": sum(rank <= 10 for rank in ranks) / count,
        "mrr": float(np.mean([1.0 / rank for rank in ranks])),
        "mean_rank": float(np.mean(ranks)),
        "direction_accuracy": sum(direction) / len(direction) if direction else 1.0,
        "edge_discrimination_accuracy": sum(discriminated) / len(discriminated),
        "relation_accuracy": sum(relation_correct) / len(relation_correct),
    }


def evaluate_pairs(node: np.ndarray, arrays: dict[str, np.ndarray], threshold: float) -> dict[str, Any]:
    count = len(arrays["left"])
    if count == 0:
        return {"count": 0, "separation_accuracy": 1.0, "mean_distance": None, "threshold": threshold}
    distances = np.linalg.norm(node[arrays["left"]] - node[arrays["right"]], axis=1)
    return {
        "count": count,
        "separation_accuracy": float(np.mean(distances >= threshold)),
        "mean_distance": float(np.mean(distances)),
        "minimum_distance": float(np.min(distances)),
        "threshold": threshold,
    }


def evaluate_membership(node: np.ndarray, arrays: dict[str, np.ndarray], radius: float) -> dict[str, Any]:
    count = len(arrays["left"])
    if count == 0:
        return {"count": 0, "within_radius_accuracy": 1.0, "mean_distance": None, "radius": radius}
    distances = np.linalg.norm(node[arrays["left"]] - node[arrays["right"]], axis=1)
    return {
        "count": count,
        "within_radius_accuracy": float(np.mean(distances <= radius)),
        "mean_distance": float(np.mean(distances)),
        "maximum_distance": float(np.max(distances)),
        "radius": radius,
    }


def metric_at(metrics: dict[str, Any], dotted: str) -> Any:
    value: Any = metrics
    for part in dotted.split("."):
        value = value[part]
    return value


def compare(observed: Any, operator: str, threshold: Any) -> bool:
    if operator == "eq":
        return observed == threshold
    if not isinstance(observed, (int, float)) or isinstance(observed, bool) or not math.isfinite(float(observed)):
        return False
    if operator == "gte":
        return float(observed) >= float(threshold)
    if operator == "lte":
        return float(observed) <= float(threshold)
    raise ValueError(f"unknown gate operator {operator}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("/kaggle/working/lightcone-output"))
    parser.add_argument("--config", type=Path)
    parser.add_argument("--require-tpu", action="store_true")
    args = parser.parse_args()
    started = dt.datetime.now(dt.timezone.utc)
    wall_start = time.monotonic()

    bundle_root = find_bundle(args.input)
    bundle_manifest = verify_bundle(bundle_root)
    graph = json.loads((bundle_root / "training-graph.json").read_text(encoding="utf-8"))
    config_path = args.config or bundle_root / "training-config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    run_context_path = bundle_root / "run-context.json"
    run_context = json.loads(run_context_path.read_text(encoding="utf-8")) if run_context_path.exists() else {
        "source_revision": f"bundle:{file_hash(bundle_root / 'bundle-manifest.json')}",
        "source_dirty": True,
        "kernel_ref": None,
        "kernel_version": None,
    }
    if graph["world_id"] != config["world_id"] or graph["world_id"] != bundle_manifest["world_id"]:
        raise RuntimeError("world identity differs between graph, config, and bundle")

    import jax
    import jax.numpy as jnp

    jax.config.update("jax_enable_x64", False)
    devices = jax.devices()
    tpu_devices = [device for device in devices if device.platform == "tpu"]
    require_tpu = args.require_tpu or Path("/kaggle").exists()
    if require_tpu and not tpu_devices:
        raise RuntimeError(f"TPU required but JAX devices are: {[str(device) for device in devices]}")
    training_device = tpu_devices[0] if tpu_devices else devices[0]

    nodes = sorted(graph["nodes"], key=lambda node: node["node_id"])
    node_ids = [node["node_id"] for node in nodes]
    node_index = {node_id: index for index, node_id in enumerate(node_ids)}
    relations = sorted(graph["relation_vocab"])
    relation_index = {relation: index for index, relation in enumerate(relations)}
    relation_prior_np = np.zeros((len(relations), int(config["coordinate_dimensions"])), dtype=np.float32)
    if "prerequisite" in relation_index:
        relation_prior_np[relation_index["prerequisite"], 0] = float(config["structural_scale"]) / 8.0
    edges_by_split = {
        split: [edge for edge in graph["edges"] if edge["split"] == split and edge["relation"] != "part_of"]
        for split in ("train", "validation", "sealed_test", "cross_domain_holdout")
    }
    memberships_by_split = {
        split: [edge for edge in graph["edges"] if edge["split"] == split and edge["relation"] == "part_of"]
        for split in ("train", "validation", "sealed_test", "cross_domain_holdout")
    }
    pairs_by_split = {
        split: [pair for pair in graph["negative_pairs"] if pair["split"] == split]
        for split in ("train", "validation", "sealed_test", "cross_domain_holdout")
    }
    edge_arrays_np = {split: arrays_for_edges(edges, node_index, relation_index) for split, edges in edges_by_split.items()}
    membership_arrays_np = {
        split: {
            "left": np.asarray([node_index[edge["source_node"]] for edge in edges], dtype=np.int32),
            "right": np.asarray([node_index[edge["target_node"]] for edge in edges], dtype=np.int32),
        }
        for split, edges in memberships_by_split.items()
    }
    pair_arrays_np = {split: arrays_for_pairs(pairs, node_index) for split, pairs in pairs_by_split.items()}
    train_edges_np = edge_arrays_np["train"]
    train_memberships_np = membership_arrays_np["train"]
    train_pairs_np = pair_arrays_np["train"]
    if len(train_edges_np["source"]) == 0 or len(train_memberships_np["left"]) == 0 or len(train_pairs_np["left"]) == 0:
        raise RuntimeError("training split must contain relational edges, membership edges, and negative control pairs")

    features = feature_matrix(nodes, int(config["feature_dimensions"]))
    structural = structural_matrix(nodes, int(config["structural_dimensions"]))
    rng = np.random.default_rng(int(config["seed"]))
    learned_dimensions = int(config["coordinate_dimensions"]) - int(config["structural_dimensions"])
    if learned_dimensions < 8:
        raise RuntimeError("coordinate_dimensions must leave at least 8 learned dimensions after structural coordinates")
    projection = rng.normal(
        0.0,
        1.0 / math.sqrt(features.shape[1] - 8),
        size=(features.shape[1] - 8, learned_dimensions),
    ).astype(np.float32)

    with jax.default_device(training_device):
        train_edges = {name: jnp.asarray(value) for name, value in train_edges_np.items()}
        train_pairs = {name: jnp.asarray(value) for name, value in train_pairs_np.items()}
        train_memberships = {name: jnp.asarray(value) for name, value in train_memberships_np.items()}
        feature_values = jnp.asarray(features)
        structural_values = jnp.asarray(structural)
        anchor_projection = jnp.asarray(projection)
        relation_prior = jnp.asarray(relation_prior_np)
        key = jax.random.PRNGKey(int(config["seed"]))
        params = {
            "projection": anchor_projection,
            "relation": relation_prior
            + jax.random.normal(
                key,
                (len(relations), int(config["coordinate_dimensions"])),
                dtype=jnp.float32,
            )
            * 0.02,
        }
        def normalized(values: Any) -> Any:
            return values / jnp.maximum(jnp.linalg.norm(values, axis=1, keepdims=True), 1e-8)

        def node_coordinates(current: dict[str, Any]) -> Any:
            fixed = structural_values * float(config["structural_scale"])
            learned = normalized(feature_values[:, 8:] @ current["projection"])
            return jnp.concatenate([fixed, learned * float(config["learned_scale"])], axis=1)

        def loss_fn(current: dict[str, Any]) -> Any:
            node = node_coordinates(current)
            relation = current["relation"]
            rel = relation[train_edges["relation"]] * train_edges["polarity"][:, None]
            query = node[train_edges["source"]] + rel
            distances = jnp.sum((query[:, None, :] - node[None, :, :]) ** 2, axis=2)
            logits = -distances / float(config["softmax_temperature"])
            edge_loss = -jnp.mean(jax.nn.log_softmax(logits, axis=1)[jnp.arange(logits.shape[0]), train_edges["target"]])
            observed_delta = (
                node[train_edges["target"]] - node[train_edges["source"]]
            ) * train_edges["polarity"][:, None]
            relation_distances = jnp.sum(
                (observed_delta[:, None, :] - relation[None, :, :]) ** 2,
                axis=2,
            )
            relation_logits = -relation_distances / float(config["softmax_temperature"])
            relation_classification_loss = -jnp.mean(
                jax.nn.log_softmax(relation_logits, axis=1)[
                    jnp.arange(relation_logits.shape[0]), train_edges["relation"]
                ]
            )
            pair_distance = jnp.linalg.norm(node[train_pairs["left"]] - node[train_pairs["right"]], axis=1)
            pair_loss = jnp.mean(jnp.square(jax.nn.relu(float(config["negative_margin"]) - pair_distance)))
            membership_distance = jnp.linalg.norm(
                node[train_memberships["left"]] - node[train_memberships["right"]], axis=1
            )
            membership_loss = jnp.mean(
                jnp.square(jax.nn.relu(membership_distance - float(config["membership_radius"])))
            )
            anchor_loss = jnp.mean(jnp.square(current["projection"] - anchor_projection))
            relation_loss = jnp.mean(jnp.square(relation - relation_prior))
            return (
                edge_loss
                + float(config.get("relation_classification_weight", 0.0))
                * relation_classification_loss
                + float(config["negative_weight"]) * pair_loss
                + float(config["membership_weight"]) * membership_loss
                + float(config["anchor_weight"]) * anchor_loss
                + float(config["relation_regularization"]) * relation_loss
            )

        value_and_grad = jax.jit(jax.value_and_grad(loss_fn))
        zeros = jax.tree_util.tree_map(jnp.zeros_like, params)
        first_moment = zeros
        second_moment = zeros

        @jax.jit
        def update(current: dict[str, Any], first: dict[str, Any], second: dict[str, Any], step_index: Any) -> tuple[Any, Any, Any, Any]:
            loss_value, gradients = value_and_grad(current)
            first = jax.tree_util.tree_map(lambda old, grad: 0.9 * old + 0.1 * grad, first, gradients)
            second = jax.tree_util.tree_map(lambda old, grad: 0.999 * old + 0.001 * jnp.square(grad), second, gradients)
            bias_one = 1.0 - jnp.power(0.9, step_index)
            bias_two = 1.0 - jnp.power(0.999, step_index)
            learning_rate = float(config["learning_rate"])
            current = jax.tree_util.tree_map(
                lambda value, moment, variance: value - learning_rate * (moment / bias_one) / (jnp.sqrt(variance / bias_two) + 1e-8),
                current,
                first,
                second,
            )
            return current, first, second, loss_value

        initial_loss = float(jax.device_get(loss_fn(params)))
        curve = [{"step": 0, "loss": initial_loss}]
        report_every = max(1, int(config["steps"]) // 32)
        for step_index in range(1, int(config["steps"]) + 1):
            params, first_moment, second_moment, loss_value = update(
                params, first_moment, second_moment, jnp.asarray(step_index, dtype=jnp.float32)
            )
            if step_index % report_every == 0 or step_index == int(config["steps"]):
                curve.append({"step": step_index, "loss": float(jax.device_get(loss_value))})
        final_loss = float(jax.device_get(loss_fn(params)))
        node = np.array(
            jax.device_get(node_coordinates(params)),
            dtype=np.float32,
            copy=True,
        )
        relation = np.array(jax.device_get(params["relation"]), dtype=np.float32, copy=True)

    separation_threshold = float(config["negative_margin"]) - 1e-5
    metrics: dict[str, Any] = {
        "accelerator": {
            "is_tpu": bool(tpu_devices),
            "backend": jax.default_backend(),
            "training_device": str(training_device),
            "device_count": len(devices),
        },
        "loss": {
            "initial": initial_loss,
            "final": final_loss,
            "decrease_fraction": (initial_loss - final_loss) / max(abs(initial_loss), 1e-12),
        },
        "edges": {split: evaluate_edges(node, relation, arrays) for split, arrays in edge_arrays_np.items()},
        "membership": {
            split: evaluate_membership(node, arrays, float(config["membership_radius"]))
            for split, arrays in membership_arrays_np.items()
        },
        "negative_pairs": {split: evaluate_pairs(node, arrays, separation_threshold) for split, arrays in pair_arrays_np.items()},
        "coordinates": {
            "finite": bool(np.isfinite(node).all() and np.isfinite(relation).all()),
            "dimensions": int(node.shape[1]),
            "minimum_norm": float(np.min(np.linalg.norm(node, axis=1))),
            "maximum_norm": float(np.max(np.linalg.norm(node, axis=1))),
            "max_absolute_value": float(max(np.max(np.abs(node)), np.max(np.abs(relation)))),
        },
    }
    gate_results: dict[str, Any] = {}
    for gate_name, gate in config["gates"].items():
        observed = metric_at(metrics, gate["metric"])
        gate_results[gate_name] = {
            "metric": gate["metric"],
            "operator": gate["operator"],
            "threshold": gate["threshold"],
            "observed": observed,
            "passed": compare(observed, gate["operator"], gate["threshold"]),
        }
    passed = all(gate["passed"] for gate in gate_results.values())

    args.output.mkdir(parents=True, exist_ok=True)
    coordinates = {
        "schema_version": 1,
        "dimensions": int(node.shape[1]),
        "vectors": [
            {"node_id": node_id, "values": [round(float(value), 9) for value in node[index]]}
            for index, node_id in enumerate(node_ids)
        ],
    }
    write_json(args.output / "coordinates.json", coordinates)
    write_json(args.output / "metrics.json", metrics)
    write_json(args.output / "training-curve.json", curve)
    write_json(
        args.output / "relation-coordinates.json",
        {
            "schema_version": 1,
            "dimensions": int(relation.shape[1]),
            "vectors": [
                {"relation": relation_id, "values": [round(float(value), 9) for value in relation[index]]}
                for index, relation_id in enumerate(relations)
            ],
        },
    )
    np.save(args.output / "trained-node-coordinates.npy", node, allow_pickle=False)
    np.save(args.output / "trained-relation-coordinates.npy", relation, allow_pickle=False)
    output_hashes = {
        path.name: file_hash(path)
        for path in sorted(args.output.iterdir())
        if path.is_file() and path.name != "training-receipt.json"
    }
    finished = dt.datetime.now(dt.timezone.utc)
    receipt = {
        "schema_version": 1,
        "run_id": f"{graph['world_id']}-{started.strftime('%Y%m%dT%H%M%SZ')}",
        "status": "passed" if passed else "failed",
        "source_revision": run_context["source_revision"],
        "source_dirty": bool(run_context["source_dirty"]),
        "input_hashes": bundle_manifest["files"],
        "split_manifest_hash": graph["split_manifest_hash"],
        "accelerator": {
            "platform": "kaggle" if Path("/kaggle").exists() else "local",
            "kind": "tpu" if tpu_devices else str(training_device.platform),
            "device_count": len(devices),
            "devices": [str(device) for device in devices],
            "kernel_ref": run_context.get("kernel_ref"),
            "kernel_version": run_context.get("kernel_version"),
        },
        "framework": {"name": "jax", "version": jax.__version__},
        "seed": int(config["seed"]),
        "hyperparameters": {key: value for key, value in config.items() if key not in {"gates", "schema_version", "protocol_id", "world_id"}},
        "protocol_id": config["protocol_id"],
        "metrics": metrics,
        "gates": gate_results,
        "output_hashes": output_hashes,
        "started_at": started.isoformat(),
        "finished_at": finished.isoformat(),
        "elapsed_seconds": time.monotonic() - wall_start,
        "failure": None if passed else {"class": "pre_registered_gate_failure", "failed_gates": [name for name, gate in gate_results.items() if not gate["passed"]]},
    }
    write_json(args.output / "training-receipt.json", receipt)
    print(json.dumps({
        "status": receipt["status"],
        "run_id": receipt["run_id"],
        "backend": metrics["accelerator"],
        "failed_gates": receipt["failure"]["failed_gates"] if receipt["failure"] else [],
        "output": str(args.output),
    }, indent=2))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
