#!/usr/bin/env python3
"""Author the first deep geometry world from formal/open references."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from registry_lib import ROOT
from curriculum_split import RelationSplitter


OUTPUT = ROOT / "curricula" / "geometry" / "geometry-foundations.jsonl"
WORLD = "geometry-foundation-v0"
LANES = ["geometry.structural", "reasoning.deductive", "thinking.bottom_up"]
SOURCES = ["mathlib4", "openstax-precalculus-2e"]


CONCEPTS = [
    ("root", "Structural geometry foundation", "Geometry represents typed objects, relations, transformations, invariants, and boundaries without confusing a representation with the represented structure.", "geometry.transformations", ["structural geometry", "geometric reasoning"]),
    ("point", "Point", "A point represents a position without assigning it length, area, or volume.", "geometry.euclidean", ["position"]),
    ("vector", "Vector", "A vector represents displacement with magnitude and direction independently of a chosen origin.", "geometry.analytic", ["displacement"]),
    ("affine-point", "Affine point", "An affine point can be translated by a vector, while subtracting two affine points yields a vector.", "geometry.affine", ["affine space"]),
    ("line", "Line", "A line is a one-dimensional affine set determined by a point and a nonzero direction.", "geometry.euclidean", ["straight line"]),
    ("segment", "Line segment", "A line segment is the bounded set between two endpoints on a line.", "geometry.euclidean", ["segment"]),
    ("ray", "Ray", "A ray has one endpoint and extends indefinitely in one direction.", "geometry.euclidean", []),
    ("plane", "Plane", "A plane is a two-dimensional affine set determined by a point and two independent directions.", "geometry.euclidean", []),
    ("dimension", "Dimension", "Dimension counts independent coordinates or directions required by the declared geometric structure.", "geometry.transformations", ["spatial dimension"]),
    ("incidence", "Incidence", "Incidence records whether a point lies on an object or whether geometric objects meet.", "geometry.projective", ["lies on", "intersection"]),
    ("betweenness", "Betweenness", "Betweenness is an ordered relation among collinear points and is not determined by incidence alone.", "geometry.euclidean", []),
    ("metric", "Metric", "A metric assigns nonnegative distances, separates distinct points, is symmetric, and satisfies the triangle inequality.", "geometry.analytic", ["distance function"]),
    ("euclidean-distance", "Euclidean distance", "Euclidean distance is the norm of the difference between two points in Euclidean coordinates.", "geometry.analytic", ["distance formula"]),
    ("angle", "Angle", "An angle measures the relative direction of two rays or nonzero vectors under a declared metric or inner product.", "geometry.euclidean", []),
    ("orientation", "Orientation", "Orientation distinguishes consistent handedness or ordering that some transformations preserve and reflections reverse.", "geometry.transformations", ["handedness"]),
    ("collinearity", "Collinearity", "Points are collinear when they lie on one line.", "geometry.affine", []),
    ("parallelism", "Parallelism", "Distinct affine lines are parallel when their direction subspaces coincide and they do not meet.", "geometry.affine", ["parallel lines"]),
    ("perpendicularity", "Perpendicularity", "Two nonzero directions are perpendicular when their inner product is zero.", "geometry.euclidean", ["orthogonal"]),
    ("triangle", "Triangle", "A nondegenerate triangle consists of three non-collinear vertices and the segments joining them.", "geometry.euclidean", []),
    ("triangle-inequality", "Triangle inequality", "For any metric, the direct distance between two points does not exceed a path through a third point.", "geometry.analytic", []),
    ("pythagorean", "Pythagorean relation", "In a Euclidean right triangle, the squared hypotenuse length equals the sum of the squared leg lengths.", "geometry.euclidean", ["Pythagorean theorem"]),
    ("congruence", "Congruence", "Congruent figures are related by an isometry and therefore agree in metric shape and size.", "geometry.euclidean", []),
    ("similarity", "Similarity", "Similar figures differ by an isometry followed by a uniform scaling and preserve angles and length ratios.", "geometry.transformations", []),
    ("transformation", "Geometric transformation", "A geometric transformation maps objects while making its domain, codomain, and preserved structure explicit.", "geometry.transformations", ["mapping"]),
    ("isometry", "Isometry", "An isometry preserves all distances in its domain.", "geometry.transformations", ["distance-preserving transformation"]),
    ("translation", "Translation", "A translation adds one fixed vector to every point and preserves displacement, distance, parallelism, and orientation.", "geometry.transformations", []),
    ("rotation", "Rotation", "A rotation turns points about a fixed center or axis while preserving distance and orientation.", "geometry.transformations", []),
    ("reflection", "Reflection", "A reflection across a suitable subspace is an involutive isometry that reverses orientation in the reflected direction.", "geometry.transformations", []),
    ("uniform-scaling", "Uniform scaling", "Uniform scaling multiplies all lengths by one factor and preserves angles but not absolute distance unless the factor has magnitude one.", "geometry.transformations", ["dilation"]),
    ("affine-transformation", "Affine transformation", "An affine transformation combines a linear map with translation and preserves affine combinations and collinearity.", "geometry.affine", []),
    ("projective-transformation", "Projective transformation", "A projective transformation preserves incidence and cross-ratio where defined, but need not preserve Euclidean distance or parallelism.", "geometry.projective", ["homography"]),
    ("projection", "Projection", "A projection maps higher-dimensional geometry to a lower-dimensional representation and can discard metric or depth information.", "geometry.projective", ["perspective projection", "orthographic projection"]),
    ("coordinate-system", "Coordinate system", "A coordinate system represents geometric objects numerically; changing coordinates need not change the represented object.", "geometry.analytic", ["reference frame"]),
    ("basis-change", "Change of basis", "A change of basis alters vector coordinates while preserving the underlying vector and linear relationships when transformed consistently.", "geometry.analytic", []),
    ("invariant", "Invariant", "An invariant is a property unchanged by every transformation in a declared class.", "geometry.transformations", ["preserved property"]),
    ("convexity", "Convexity", "A set is convex when the segment between any two of its points remains in the set.", "geometry.convex", []),
    ("topology", "Topology", "A topology specifies open sets and continuity without requiring a metric, angle, or length.", "geometry.topology", ["topological space"]),
    ("continuity", "Continuity", "A continuous map preserves neighborhood structure; it need not preserve distance, angle, or shape.", "geometry.topology", []),
    ("homeomorphism", "Homeomorphism", "A homeomorphism is a continuous bijection with continuous inverse and preserves topological properties.", "geometry.topology", []),
    ("manifold", "Manifold", "A manifold is locally modeled on Euclidean space while its global geometry or topology may differ.", "geometry.differential", []),
    ("tangent-space", "Tangent space", "A tangent space linearly approximates a smooth manifold at one point.", "geometry.differential", []),
    ("curvature", "Curvature", "Curvature measures how geometric structure departs from a locally flat reference under a declared geometry.", "geometry.differential", []),
    ("graph-geometry", "Graph geometry", "A graph induces discrete paths and distances from vertices and edges without implying Euclidean embedding.", "geometry.discrete", ["graph distance"]),
    ("mesh", "Geometric mesh", "A mesh approximates a geometric domain with connected discrete elements and carries approximation error.", "geometry.meshes-cad", ["triangular mesh"]),
    ("degeneracy", "Geometric degeneracy", "A degenerate configuration loses an assumed dimension or independence, such as three collinear triangle vertices.", "geometry.computational", ["degenerate case"]),
    ("numerical-robustness", "Geometric numerical robustness", "Computational geometry must distinguish exact predicates from floating-point approximations near degenerate boundaries.", "geometry.computational", ["robust predicate"])
]


RELATIONS = [
    ("vector-between-points", "affine-point", "vector", "clarifies", "Subtracting affine points produces the displacement vector between them.", ["both points inhabit the same affine space"], []),
    ("line-from-point-direction", "affine-point", "line", "enables", "A point and a nonzero direction determine an affine line.", ["direction is nonzero"], []),
    ("segment-part-line", "segment", "line", "part_of", "Every line segment lies on its supporting line.", [], []),
    ("ray-part-line", "ray", "line", "part_of", "Every ray lies on its supporting line.", [], []),
    ("line-incidence", "incidence", "line", "clarifies", "Point-line incidence specifies which points lie on a line.", [], []),
    ("betweenness-needs-collinearity", "collinearity", "betweenness", "prerequisite", "Betweenness applies only after collinearity is established.", [], []),
    ("metric-measures-distance", "metric", "euclidean-distance", "grounds", "Euclidean distance is a metric induced by the Euclidean norm.", ["Euclidean coordinate space"], []),
    ("metric-triangle-inequality", "metric", "triangle-inequality", "grounds", "The triangle inequality is a defining metric constraint.", [], []),
    ("inner-product-angle", "perpendicularity", "angle", "clarifies", "A zero inner product corresponds to a right angle for nonzero Euclidean directions.", ["nonzero vectors in an inner-product space"], []),
    ("triangle-nondegenerate", "collinearity", "triangle", "prevents", "Collinearity prevents three vertices from defining a nondegenerate triangle.", [], []),
    ("right-triangle-pythagorean", "perpendicularity", "pythagorean", "enables", "A right-angle condition enables the Pythagorean relation.", ["Euclidean triangle"], []),
    ("isometry-congruence", "isometry", "congruence", "grounds", "An isometry maps a figure to a congruent figure.", [], []),
    ("similarity-from-scaling", "uniform-scaling", "similarity", "enables", "Uniform scaling composed with an isometry produces a similarity transformation.", ["nonzero scale factor"], []),
    ("transformation-isometry", "isometry", "transformation", "part_of", "Isometries form a structure-preserving class of geometric transformations.", [], []),
    ("translation-isometry", "translation", "isometry", "part_of", "Every Euclidean translation is an isometry.", [], []),
    ("rotation-isometry", "rotation", "isometry", "part_of", "Every Euclidean rotation is an isometry.", [], []),
    ("reflection-isometry", "reflection", "isometry", "part_of", "Every Euclidean reflection across an admissible subspace is an isometry.", [], []),
    ("reflection-involution", "reflection", "invariant", "supports", "Applying the same reflection twice returns each point to itself.", [], []),
    ("translation-orientation", "translation", "orientation", "supports", "Translations preserve orientation.", [], []),
    ("rotation-orientation", "rotation", "orientation", "supports", "Proper rotations preserve orientation.", [], []),
    ("reflection-reverses-orientation", "reflection", "orientation", "inhibits", "A reflection reverses orientation along the reflected dimension.", [], []),
    ("scaling-not-isometry", "uniform-scaling", "isometry", "contradicts", "A uniform scaling with factor magnitude other than one is not an isometry.", ["scale magnitude differs from one"], []),
    ("affine-preserves-collinearity", "affine-transformation", "collinearity", "supports", "Affine transformations preserve collinearity.", [], ["a singular map may collapse distinct points"]),
    ("affine-preserves-parallelism", "affine-transformation", "parallelism", "supports", "Invertible affine transformations preserve parallel lines.", ["transformation is invertible"], []),
    ("projective-preserves-incidence", "projective-transformation", "incidence", "supports", "Projective transformations preserve incidence relations.", ["objects and images are defined"], []),
    ("projective-not-parallel", "projective-transformation", "parallelism", "contradicts", "General projective transformations need not preserve Euclidean parallelism.", [], []),
    ("projection-information-loss", "projection", "euclidean-distance", "inhibits", "Projection can destroy Euclidean distance information.", [], ["special restricted configurations may retain selected distances"]),
    ("projection-dimension", "projection", "dimension", "transforms_to", "Projection can map a higher-dimensional object into a lower-dimensional representation.", [], []),
    ("coordinates-represent-points", "coordinate-system", "affine-point", "clarifies", "Coordinates encode a point relative to a chosen frame.", [], []),
    ("basis-preserves-vector", "basis-change", "vector", "supports", "A consistent basis change preserves the underlying vector while changing its coordinate tuple.", [], []),
    ("transformation-invariants", "transformation", "invariant", "enables", "A transformation class determines which properties qualify as invariants.", [], []),
    ("convexity-segments", "segment", "convexity", "grounds", "Convexity is defined by containment of every segment joining points of the set.", [], []),
    ("topology-no-metric", "topology", "metric", "qualifies", "A metric induces a topology, but a topology does not by itself supply distances.", [], []),
    ("continuity-topology", "topology", "continuity", "grounds", "Continuity is defined from inverse images of open sets in topology.", [], []),
    ("homeomorphism-continuity", "homeomorphism", "continuity", "part_of", "A homeomorphism is continuous in both directions.", [], []),
    ("homeomorphism-not-isometry", "homeomorphism", "isometry", "qualifies", "A homeomorphism need not preserve metric distance and therefore need not be an isometry.", [], []),
    ("manifold-local-euclidean", "manifold", "dimension", "grounds", "A manifold's dimension is the dimension of its local Euclidean charts.", ["manifold dimension is constant on the considered component"], []),
    ("tangent-local-manifold", "tangent-space", "manifold", "part_of", "The tangent space belongs to a manifold at a specified point.", [], []),
    ("curvature-needs-geometry", "manifold", "curvature", "prerequisite", "Curvature requires additional geometric structure beyond a bare topological manifold.", [], []),
    ("graph-distance-metric", "graph-geometry", "metric", "enables", "Shortest-path length defines a metric on connected graph vertices under nonnegative edge lengths.", ["graph is connected and edge lengths are nonnegative"], []),
    ("graph-not-euclidean", "graph-geometry", "euclidean-distance", "qualifies", "Graph distance does not imply a distance-preserving Euclidean embedding.", [], []),
    ("mesh-approximates", "mesh", "manifold", "measures", "A mesh can approximate a manifold while introducing discretization error.", [], []),
    ("degeneracy-loses-dimension", "degeneracy", "dimension", "inhibits", "Degeneracy reduces the effective dimension assumed by a construction.", [], []),
    ("robustness-detects-degeneracy", "numerical-robustness", "degeneracy", "clarifies", "Robust predicates classify near-boundary degeneracies without treating floating-point noise as geometry.", [], []),
    ("geometry-bottom-up", "point", "transformation", "enables", "Geometric reasoning composes typed objects and relations before applying transformations.", [], []),
    ("geometry-invariant-warrant", "invariant", "congruence", "qualifies", "Congruence requires the invariants of isometry, not merely visual resemblance.", [], [])
]


EXAMPLES = [
    ("example-coordinate-translation", "Coordinate translation example", "Translating every point by the same vector changes coordinates but preserves every pairwise displacement and distance.", "geometry.transformations", ["translation example"]),
    ("example-reflection-twice", "Reflection involution example", "Reflecting a point across the same line twice returns the original point.", "geometry.transformations", ["reflection twice"]),
    ("example-projection-ambiguity", "Projection ambiguity example", "Distinct three-dimensional points can share one two-dimensional projected location, demonstrating depth information loss.", "geometry.projective", ["depth ambiguity"]),
    ("example-coordinate-invariance", "Coordinate invariance example", "Rotating a coordinate frame changes component values while a consistently transformed geometric relation remains the same.", "geometry.analytic", ["frame change"]),
    ("example-graph-path", "Graph distance example", "In an unweighted graph, the distance between connected vertices is the minimum number of traversed edges.", "geometry.discrete", ["shortest path"]),
    ("example-degenerate-triangle", "Degenerate triangle example", "Three collinear points have zero triangle area and do not form a nondegenerate triangle.", "geometry.computational", ["zero area triangle"])
]


CONTROLS = [
    ("control-diagram-proof", "Diagram is not proof", "A visually convincing diagram must not substitute for a derivation that covers all permitted configurations."),
    ("control-projection-distance", "Projection does not generally preserve distance", "A projected image must not be used to infer original Euclidean distances without additional constraints."),
    ("control-coordinate-object", "Coordinates are not the object", "Changing a coordinate representation must not be reported as changing the underlying geometric object."),
    ("control-topology-metric", "Topology is not metric geometry", "Continuity or homeomorphism must not be reported as distance or angle preservation."),
    ("control-similarity-congruence", "Similarity is not congruence", "Equal angles and proportional sides must not be reported as equal absolute size."),
    ("control-degenerate-assumption", "Degenerate boundary", "A theorem requiring non-collinearity must abstain or qualify when the input points are collinear."),
    ("control-dimension-collapse", "Dimension collapse", "A singular transformation must not be treated as invertible after it collapses independent directions."),
    ("control-graph-embedding", "Graph distance is not automatically Euclidean", "A graph metric must not be treated as a distance-preserving Euclidean layout without an embedding proof."),
    ("control-floating-predicate", "Near-degenerate numerical predicate", "A floating-point sign near zero must not be treated as an exact orientation proof without an error bound or exact predicate.")
]


def base(record_id: str, subject: str, split: str, sources: list[str], epistemic: str, kind: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "record_id": f"geometry.v0.{record_id}",
        "world_id": WORLD,
        "domain_id": "geometry",
        "subject_id": subject,
        "lanes": LANES,
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws", "representations_transformations"],
        "source_ids": sources,
        "scope": "geometry foundation tranche",
        "limitations": ["Advanced proofs and every geometry subfield remain open in the exhaustive ledger."],
        "as_of": "2026-09-03",
        "version_boundary": "geometry-foundation-v0",
        "split_group": f"geometry.v0.{record_id}",
        "split": split,
        "tags": ["geometry", "foundation"]
    }


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, (identifier, label, statement, subject, aliases) in enumerate(CONCEPTS):
        split = "train" if index % 11 else "validation"
        records.append({
            **base(identifier, subject, split, SOURCES, "formal", "concept"),
            "label": label,
            "statement": statement,
            "aliases": aliases
        })
        if identifier != "root":
            records.append({
                **base(f"membership-{identifier}", subject, "train", SOURCES, "formal", "relation"),
                "label": f"{label} geometry membership",
                "statement": f"{label} is part of the structural geometry foundation and retains its own declared invariants.",
                "aliases": [],
                "relation": {
                    "source_node": f"geometry.v0.{identifier}",
                    "target_node": "geometry.v0.root",
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the relevant geometric structure is declared"],
                    "exceptions": []
                },
                "coverage_axes": ["primitives_invariants", "within_domain_composition"]
            })
    splitter = RelationSplitter([kind for _identifier, _source, _target, kind, _statement, _conditions, _exceptions in RELATIONS])
    for index, (identifier, source, target, kind, statement, conditions, exceptions) in enumerate(RELATIONS):
        split = splitter.split(kind, cross_requested=index % 17 == 0)
        if identifier == "geometry-bottom-up":
            split = "cross_domain_holdout"
        records.append({
            **base(identifier, "geometry.transformations", split, SOURCES, "formal", "relation"),
            "label": identifier.replace("-", " "),
            "statement": statement,
            "aliases": [],
            "relation": {
                "source_node": f"geometry.v0.{source}",
                "target_node": f"geometry.v0.{target}",
                "kind": kind,
                "polarity": -1 if kind in {"inhibits", "prevents", "contradicts"} else 1,
                "direction": "forward",
                "conditions": conditions,
                "exceptions": exceptions
            },
            "coverage_axes": ["mechanisms_causal_laws", "representations_transformations", "within_domain_composition"]
        })
    for index, (identifier, label, statement, subject, aliases) in enumerate(EXAMPLES):
        records.append({
            **base(identifier, subject, "validation" if index % 2 == 0 else "sealed_test", SOURCES, "formal", "worked_example"),
            "label": label,
            "statement": statement,
            "aliases": aliases,
            "coverage_axes": ["deductions_predictions_execution", "within_domain_composition"]
        })
    for index, (identifier, label, statement) in enumerate(CONTROLS):
        control_split = "train" if index == 0 else "sealed_test" if index == len(CONTROLS) - 1 or index % 2 else "validation"
        record = {
            **base(identifier, "geometry.computational", control_split, [], "synthetic_control", "synthetic_control"),
            "label": label,
            "statement": statement,
            "aliases": [label.lower()],
            "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
            "synthetic": True,
            "tags": ["geometry", "negative-control"]
        }
        records.append(record)
    return sorted(records, key=lambda record: record["record_id"])


def main() -> int:
    records = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records), encoding="utf-8")
    counts: dict[str, int] = {}
    for record in records:
        counts[record["split"]] = counts.get(record["split"], 0) + 1
    print(f"wrote {OUTPUT} with {len(records)} records: {dict(sorted(counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
