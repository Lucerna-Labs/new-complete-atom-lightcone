#!/usr/bin/env python3
"""Run every non-optimizer taxonomy gate without claiming training evidence."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

from registry_lib import ROOT
from world_catalog import TAXONOMY_WORLD_CONFIGS


sys.path.insert(0, str(ROOT / "trainer"))

from semantic_geometry import (  # noqa: E402
    build_evidence_index,
    build_semantic_overlay,
    evaluate_evidence_edges,
)
from shadow_projection import build_shadow_artifacts  # noqa: E402
from train_jax import (  # noqa: E402
    arrays_for_pairs,
    compare,
    evaluate_membership,
    evaluate_pairs,
    feature_matrix,
    metric_at,
    structural_matrix,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def initialization_coordinates(
    nodes: list[dict[str, Any]], config: dict[str, Any]
) -> np.ndarray:
    features = feature_matrix(nodes, int(config["feature_dimensions"]))
    structural = structural_matrix(nodes, int(config["structural_dimensions"]))
    learned_dimensions = int(config["coordinate_dimensions"]) - int(
        config["structural_dimensions"]
    )
    rng = np.random.default_rng(int(config["seed"]))
    projection = rng.normal(
        0.0,
        1.0 / math.sqrt(features.shape[1] - 8),
        size=(features.shape[1] - 8, learned_dimensions),
    )
    learned = features[:, 8:] @ projection
    learned /= np.maximum(np.linalg.norm(learned, axis=1, keepdims=True), 1e-8)
    return np.concatenate(
        [
            structural * float(config["structural_scale"]),
            learned * float(config["learned_scale"]),
        ],
        axis=1,
    ).astype(np.float32)


def main() -> int:
    relation_catalog = load_json(ROOT / "ontology" / "relation-catalog.json")
    results: list[dict[str, Any]] = []
    for position, (world_id, config_name) in enumerate(TAXONOMY_WORLD_CONFIGS, start=1):
        graph = load_json(
            ROOT / "artifacts" / "staging" / world_id / "input" / "training-graph.json"
        )
        config = load_json(ROOT / "trainer" / "configs" / config_name)
        nodes = sorted(graph["nodes"], key=lambda node: node["node_id"])
        node_index = {node["node_id"]: index for index, node in enumerate(nodes)}
        relational_edges = [edge for edge in graph["edges"] if edge["relation"] != "part_of"]
        evidence, evidence_artifact = build_evidence_index(
            nodes, relational_edges, relation_catalog, config
        )
        edges = {
            split: evaluate_evidence_edges(
                nodes=nodes,
                edges=relational_edges,
                edge_indices=[
                    index
                    for index, edge in enumerate(relational_edges)
                    if edge["split"] == split
                ],
                evidence=evidence,
                relation_prior_weight=float(config["relation_prior_weight"]),
            )
            for split in ("train", "validation", "sealed_test", "cross_domain_holdout")
        }
        base = initialization_coordinates(nodes, config)
        coordinates, overlay = build_semantic_overlay(base, nodes, config)
        membership = {}
        negative_pairs = {}
        for split in ("train", "validation", "sealed_test", "cross_domain_holdout"):
            member_edges = [
                edge
                for edge in graph["edges"]
                if edge["split"] == split and edge["relation"] == "part_of"
            ]
            membership[split] = evaluate_membership(
                coordinates,
                {
                    "left": np.asarray(
                        [node_index[edge["source_node"]] for edge in member_edges],
                        dtype=np.int32,
                    ),
                    "right": np.asarray(
                        [node_index[edge["target_node"]] for edge in member_edges],
                        dtype=np.int32,
                    ),
                },
                float(config["membership_radius"]),
            )
            pairs = [pair for pair in graph["negative_pairs"] if pair["split"] == split]
            negative_pairs[split] = evaluate_pairs(
                coordinates,
                arrays_for_pairs(pairs, node_index),
                float(config["negative_margin"]) - 1e-5,
            )
        shadow = build_shadow_artifacts(
            world_id=world_id,
            coordinates=coordinates,
            nodes=nodes,
            edges=graph["edges"],
            config=config,
        )["metrics"]
        metrics = {
            "edges": edges,
            "membership": membership,
            "negative_pairs": negative_pairs,
            "coordinates": {
                "finite": bool(np.isfinite(coordinates).all()),
                "dimensions": int(coordinates.shape[1]),
                "max_absolute_value": float(np.max(np.abs(coordinates))),
            },
            "evidence_retrieval": evidence_artifact,
            "semantic_overlay": overlay,
            "shadow": shadow,
        }
        skipped = {"tpu_backend", "loss_decrease"}
        failed = []
        for gate_name, gate in config["gates"].items():
            if gate_name in skipped:
                continue
            observed = metric_at(metrics, gate["metric"])
            if not compare(observed, gate["operator"], gate["threshold"]):
                failed.append(gate_name)
        results.append(
            {
                "world_id": world_id,
                "static_gates_passed": not failed,
                "failed_static_gates": sorted(failed),
                "node_count": len(nodes),
                "edge_count": len(graph["edges"]),
            }
        )
        if position % 10 == 0:
            print(f"preflighted {position}/{len(TAXONOMY_WORLD_CONFIGS)} worlds", flush=True)
    summary = {
        "schema_version": 1,
        "diagnostic_only": True,
        "optimizer_gates_skipped": ["loss_decrease", "tpu_backend"],
        "accelerator_accepted": False,
        "world_count": len(results),
        "static_pass_count": sum(result["static_gates_passed"] for result in results),
        "static_failure_count": sum(not result["static_gates_passed"] for result in results),
        "results": results,
    }
    output = ROOT / "artifacts" / "smoke" / "taxonomy-preflight" / "summary.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["static_failure_count"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
