#!/usr/bin/env python3
"""Replay protocol-v3 post-training gates over retained v2 CPU coordinates.

This is a diagnostic for the corrected evaluation and semantic-shadow layers.
It is never accelerator evidence and cannot advance the coverage ledger.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

from registry_lib import ROOT
from world_catalog import WORLD_CONFIGS


sys.path.insert(0, str(ROOT / "trainer"))

from semantic_geometry import (  # noqa: E402
    build_evidence_index,
    build_semantic_overlay,
    evaluate_evidence_edges,
    validate_protocol_v3_config,
)
from shadow_projection import build_shadow_artifacts, validate_shadow_training_config  # noqa: E402
from train_jax import (  # noqa: E402
    arrays_for_edges,
    arrays_for_pairs,
    compare,
    evaluate_edges,
    evaluate_membership,
    evaluate_pairs,
    metric_at,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    relation_catalog = load_json(ROOT / "ontology" / "relation-catalog.json")
    results: list[dict[str, Any]] = []
    output_root = ROOT / "artifacts" / "smoke" / "protocol-v3-replay"
    output_root.mkdir(parents=True, exist_ok=True)
    for world_id, config_name in WORLD_CONFIGS:
        graph = load_json(
            ROOT / "artifacts" / "staging" / world_id / "input" / "training-graph.json"
        )
        config = load_json(ROOT / "trainer" / "configs" / config_name)
        validate_shadow_training_config(config)
        validate_protocol_v3_config(config)
        retained = ROOT / "artifacts" / "smoke" / "matrix" / world_id
        optimization_node = np.load(
            retained / "trained-node-coordinates.npy", allow_pickle=False
        )
        relation = np.load(
            retained / "trained-relation-coordinates.npy", allow_pickle=False
        )
        old_metrics = load_json(retained / "metrics.json")
        nodes = sorted(graph["nodes"], key=lambda node: node["node_id"])
        node_index = {node["node_id"]: index for index, node in enumerate(nodes)}
        relations = sorted(graph["relation_vocab"])
        relation_index = {relation_id: index for index, relation_id in enumerate(relations)}
        relational_edges = [
            edge for edge in graph["edges"] if edge["relation"] != "part_of"
        ]
        edges_by_split = {
            split: [edge for edge in relational_edges if edge["split"] == split]
            for split in ("train", "validation", "sealed_test", "cross_domain_holdout")
        }
        translation = {
            split: evaluate_edges(
                optimization_node,
                relation,
                arrays_for_edges(edges, node_index, relation_index),
            )
            for split, edges in edges_by_split.items()
        }
        evidence, evidence_artifact = build_evidence_index(
            nodes, relational_edges, relation_catalog, config
        )
        evaluated = {
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
        edges: dict[str, dict[str, Any]] = {}
        for split in ("train", "validation", "sealed_test", "cross_domain_holdout"):
            if split == "train" and config["train_edge_evaluation_method"] == "jax_translation":
                edges[split] = translation[split]
                continue
            edges[split] = {
                **evaluated[split],
                "direction_accuracy": translation[split]["direction_accuracy"],
                "translation_geometry": translation[split],
            }
        node, overlay = build_semantic_overlay(optimization_node, nodes, config)
        membership = {}
        negative_pairs = {}
        for split in ("train", "validation", "sealed_test", "cross_domain_holdout"):
            selected_memberships = [
                edge
                for edge in graph["edges"]
                if edge["split"] == split and edge["relation"] == "part_of"
            ]
            membership[split] = evaluate_membership(
                node,
                {
                    "left": np.asarray(
                        [node_index[edge["source_node"]] for edge in selected_memberships],
                        dtype=np.int32,
                    ),
                    "right": np.asarray(
                        [node_index[edge["target_node"]] for edge in selected_memberships],
                        dtype=np.int32,
                    ),
                },
                float(config["membership_radius"]),
            )
            selected_pairs = [
                pair for pair in graph["negative_pairs"] if pair["split"] == split
            ]
            negative_pairs[split] = evaluate_pairs(
                node,
                arrays_for_pairs(selected_pairs, node_index),
                float(config["negative_margin"]) - 1e-5,
            )
        shadow = build_shadow_artifacts(
            world_id=world_id,
            coordinates=node,
            nodes=nodes,
            edges=graph["edges"],
            config=config,
        )["metrics"]
        metrics = {
            "accelerator": {
                "is_tpu": False,
                "backend": "retained-cpu-coordinate-replay",
                "training_device": "historical-cpu",
                "device_count": 1,
            },
            "loss": old_metrics["loss"],
            "edges": edges,
            "membership": membership,
            "negative_pairs": negative_pairs,
            "coordinates": {
                "finite": bool(
                    np.isfinite(node).all()
                    and np.isfinite(optimization_node).all()
                    and np.isfinite(relation).all()
                ),
                "dimensions": int(node.shape[1]),
                "max_absolute_value": float(
                    max(np.max(np.abs(node)), np.max(np.abs(relation)))
                ),
            },
            "evidence_retrieval": evidence_artifact,
            "semantic_overlay": overlay,
            "shadow": shadow,
        }
        gates = {
            name: {
                **gate,
                "observed": metric_at(metrics, gate["metric"]),
            }
            for name, gate in config["gates"].items()
        }
        for gate in gates.values():
            gate["passed"] = compare(
                gate["observed"], gate["operator"], gate["threshold"]
            )
        failed_non_tpu = sorted(
            name for name, gate in gates.items() if name != "tpu_backend" and not gate["passed"]
        )
        detail = {
            "schema_version": 1,
            "diagnostic_only": True,
            "world_id": world_id,
            "protocol_id": config["protocol_id"],
            "coordinate_source": "retained protocol-v2 CPU optimization coordinates",
            "accelerator_accepted": False,
            "metrics": metrics,
            "gates": gates,
            "failed_non_tpu_gates": failed_non_tpu,
        }
        (output_root / f"{world_id}.json").write_text(
            json.dumps(detail, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        results.append(
            {
                "world_id": world_id,
                "protocol_id": config["protocol_id"],
                "failed_non_tpu_gates": failed_non_tpu,
                "non_tpu_passed": not failed_non_tpu,
            }
        )
    summary = {
        "schema_version": 1,
        "diagnostic_only": True,
        "coordinate_source": "retained protocol-v2 CPU optimization coordinates",
        "accelerator_accepted": False,
        "world_count": len(results),
        "non_tpu_pass_count": sum(result["non_tpu_passed"] for result in results),
        "non_tpu_failure_count": sum(not result["non_tpu_passed"] for result in results),
        "results": results,
    }
    (output_root / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 0 if summary["non_tpu_failure_count"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
