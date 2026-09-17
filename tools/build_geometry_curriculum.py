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
SOURCES = ["mathlib4", "msc2020"]


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
    ("full-coordinate-space", "Full coordinate space", "A full coordinate space retains every registered geometric axis used by a world before any observer projection is applied.", "geometry.shadow-projection", ["source geometry"]),
    ("all-spatial-shadow", "All-spatial shadow", "An all-spatial shadow is a lower-dimensional observer representation whose axes are spatial and whose projection has no time coordinate or causal authority.", "geometry.shadow-projection", ["4D shadow"]),
    ("orthonormal-projection", "Orthonormal projection", "A matrix with orthonormal rows maps a Euclidean coordinate vector into a lower-dimensional subspace without increasing pairwise Euclidean distance.", "geometry.shadow-projection", ["non-expansive projection"]),
    ("projection-collision", "Projection collision", "A projection collision occurs when distinct full-space points map into the same declared shadow cell and therefore become indistinguishable to that observer.", "geometry.shadow-projection", ["shadow conflation"]),
    ("false-proximity", "Shadow false proximity", "False proximity occurs when points outside a full-space reach radius map within that radius in a lower-dimensional shadow.", "geometry.shadow-projection", ["near shadow"]),
    ("invisible-edge", "Invisible projected edge", "An exact graph edge becomes invisible to a shadow when its distinct endpoints collapse into the same observer cell; the underlying edge remains authoritative.", "geometry.shadow-projection", []),
    ("projection-composition", "Projection composition", "A registered projection composes when sequential dimension reductions equal the corresponding direct transformation for every input point.", "geometry.shadow-projection", ["commuting projection"]),
    ("observer-basis", "Observer projection basis", "An observer basis declares the source dimensions, kept directions, axis names, metric, fitting scope, version, and hash needed to reproduce a shadow.", "geometry.shadow-projection", []),
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
    ("numerical-robustness", "Geometric numerical robustness", "Computational geometry must distinguish exact predicates from floating-point approximations near degenerate boundaries.", "geometry.computational", ["robust predicate"]),
    ("circle", "Circle", "A Euclidean circle is the set of points at one fixed positive distance from a center.", "geometry.euclidean", []),
    ("polygon", "Polygon", "A polygon is a cyclic sequence of vertices joined by segments, with simplicity, orientation, holes, and degeneracy declared separately.", "geometry.euclidean", []),
    ("polyhedron", "Polyhedron", "A polyhedron is a three-dimensional region or surface assembled from planar polygonal faces under incidence and manifold conditions.", "geometry.euclidean", []),
    ("area", "Area measure", "Area assigns a nonnegative two-dimensional measure that is additive on suitable disjoint regions and transforms predictably under scaling.", "geometry.euclidean", []),
    ("volume", "Volume measure", "Volume assigns a nonnegative three-dimensional measure that is additive on suitable regions and scales cubically under uniform dilation.", "geometry.euclidean", []),
    ("coordinate-equation", "Coordinate equation", "A coordinate equation represents a geometric locus relative to a frame and must transform consistently when the frame changes.", "geometry.analytic", []),
    ("dot-product", "Dot product", "A Euclidean dot product is a symmetric bilinear form that determines squared norm, angle, and perpendicularity.", "geometry.analytic", ["inner product"]),
    ("cross-product", "Three-dimensional cross product", "The three-dimensional cross product produces an oriented vector perpendicular to two input vectors with magnitude equal to their parallelogram area.", "geometry.analytic", []),
    ("transformation-matrix", "Transformation matrix", "A matrix represents a linear transformation in chosen bases; composition corresponds to ordered matrix multiplication.", "geometry.analytic", []),
    ("barycentric", "Barycentric coordinates", "Barycentric coordinates express a point as an affine combination of reference vertices and expose containment through coefficient constraints.", "geometry.affine", []),
    ("affine-combination", "Affine combination", "An affine combination weights points with coefficients summing to one and is invariant under translation of the coordinate origin.", "geometry.affine", []),
    ("affine-independence", "Affine independence", "Points are affinely independent when none is an affine combination of the others, establishing the dimension of their simplex.", "geometry.affine", []),
    ("homogeneous-coordinate", "Homogeneous coordinates", "Homogeneous coordinates represent a projective point by any nonzero scalar multiple of one coordinate vector.", "geometry.projective", []),
    ("point-at-infinity", "Point at infinity", "Projective completion represents each affine direction by a point at infinity so parallel affine lines can meet projectively.", "geometry.projective", []),
    ("cross-ratio", "Cross-ratio", "The cross-ratio of four collinear projective points is invariant under projective transformations where it is defined.", "geometry.projective", []),
    ("dual-projective", "Projective duality", "Projective duality exchanges point and hyperplane incidence statements under a dimension-appropriate correspondence.", "geometry.projective", []),
    ("lattice", "Geometric lattice", "A geometric lattice is a discrete additive set generated by independent basis vectors and inherits a fundamental cell and periodicity.", "geometry.discrete", []),
    ("planar-graph", "Planar graph embedding", "A planar embedding represents a graph in the plane without edge crossings except at shared endpoints and includes a cyclic order around vertices.", "geometry.discrete", []),
    ("polytope", "Polytope", "A convex polytope is equivalently the convex hull of finitely many points or a bounded intersection of finitely many half-spaces.", "geometry.discrete", []),
    ("discrete-curvature", "Discrete curvature", "Discrete curvature assigns curvature-like quantities to mesh vertices, edges, or cells so integrated geometric relations survive discretization approximately or exactly.", "geometry.discrete", []),
    ("convex-combination", "Convex combination", "A convex combination is an affine combination with nonnegative coefficients and therefore remains inside every convex set containing its inputs.", "geometry.convex", []),
    ("convex-hull", "Convex hull", "The convex hull is the smallest convex set containing a given set, equivalently all of its finite convex combinations.", "geometry.convex", []),
    ("supporting-hyperplane", "Supporting hyperplane", "A supporting hyperplane touches a convex set while the entire set remains in one closed half-space.", "geometry.convex", []),
    ("separation", "Convex separation", "Under appropriate closure and disjointness conditions, a hyperplane can separate convex sets and provide a certificate of nonintersection.", "geometry.convex", []),
    ("chart", "Manifold chart", "A chart maps a neighborhood of a manifold homeomorphically to an open subset of Euclidean space and supplies local coordinates.", "geometry.differential", []),
    ("atlas", "Manifold atlas", "An atlas covers a manifold with compatible charts whose transition maps determine the declared differentiability class.", "geometry.differential", []),
    ("smooth-map", "Smooth map", "A map between smooth manifolds is smooth when its coordinate representations are differentiable in overlapping charts.", "geometry.differential", []),
    ("differential", "Differential of a map", "The differential is the linear map between tangent spaces induced by a smooth map at a point.", "geometry.differential", []),
    ("vector-field", "Vector field", "A vector field assigns a tangent vector to each point with declared smoothness and can generate local flows.", "geometry.differential", []),
    ("riemannian-metric", "Riemannian metric", "A Riemannian metric assigns a smoothly varying positive-definite inner product to each tangent space.", "geometry.riemannian", []),
    ("geodesic", "Geodesic", "A geodesic locally follows zero covariant acceleration and, over sufficiently small intervals, extremizes distance under a Riemannian metric.", "geometry.riemannian", []),
    ("connection", "Affine connection", "A connection defines covariant differentiation and parallel transport, making comparison of tangent vectors at different points meaningful along a path.", "geometry.riemannian", []),
    ("exponential-map", "Riemannian exponential map", "The exponential map sends a tangent vector to the point reached at unit parameter along the geodesic with that initial velocity where defined.", "geometry.riemannian", []),
    ("sectional-curvature", "Sectional curvature", "Sectional curvature assigns Gaussian-like curvature to each two-dimensional tangent plane in a Riemannian manifold.", "geometry.riemannian", []),
    ("ricci-curvature", "Ricci curvature", "Ricci curvature contracts the Riemann curvature tensor and measures averaged sectional curvature around a tangent direction.", "geometry.riemannian", []),
    ("scalar-curvature", "Scalar curvature", "Scalar curvature is the trace of Ricci curvature and summarizes local volume distortion to leading order.", "geometry.riemannian", []),
    ("polynomial-locus", "Polynomial locus", "An algebraic locus is the set of points satisfying a family of polynomial equations over a declared field.", "geometry.algebraic", []),
    ("ideal", "Polynomial ideal", "A polynomial ideal is closed under addition and multiplication by arbitrary ring elements and encodes consequences of algebraic equations.", "geometry.algebraic", []),
    ("affine-variety", "Affine algebraic variety", "An affine algebraic variety or algebraic set is a polynomial zero locus in affine space, with terminology depending on field and irreducibility conventions.", "geometry.algebraic", []),
    ("projective-variety", "Projective variety", "A projective variety is defined by homogeneous polynomial equations on projective space so the zero condition is independent of representative scale.", "geometry.algebraic", []),
    ("algebraic-singularity", "Algebraic singularity", "A singular point is one where the local algebraic or differential structure fails the regularity rank expected for a smooth variety.", "geometry.algebraic", []),
    ("connectedness", "Topological connectedness", "A space is connected when it cannot be partitioned into two disjoint nonempty open subsets.", "geometry.topology", []),
    ("compactness", "Topological compactness", "A space is compact when every open cover has a finite subcover, with metric-space sequence characterizations requiring additional structure.", "geometry.topology", []),
    ("homotopy", "Homotopy", "A homotopy continuously deforms one map into another through a parameterized family of maps.", "geometry.topology", []),
    ("fundamental-group", "Fundamental group", "The fundamental group records based loops up to homotopy under concatenation and detects selected one-dimensional holes.", "geometry.topology", []),
    ("homology", "Homology", "Homology assigns algebraic groups to a space to record cycles modulo boundaries in each dimension.", "geometry.topology", []),
    ("self-similarity", "Fractal self-similarity", "Self-similarity relates a whole set to scaled or transformed copies of its parts, exactly or statistically under a declared construction.", "geometry.fractal", []),
    ("iterated-function-system", "Iterated function system", "An iterated function system uses a finite family of contractions whose invariant set can generate a self-similar fractal.", "geometry.fractal", []),
    ("fractal-dimension", "Fractal dimension", "A fractal dimension measures scaling complexity and must name the definition, since Hausdorff, box-counting, and other dimensions can differ.", "geometry.fractal", []),
    ("scale-invariance", "Scale invariance", "Scale invariance means selected statistical or exact structure remains similar across a range of magnifications, not necessarily every scale.", "geometry.fractal", []),
    ("symmetry", "Geometric symmetry", "A symmetry is a structure-preserving automorphism of an object under a declared transformation class.", "geometry.transformations", []),
    ("group-action", "Transformation group action", "A group action maps group elements to transformations so identity acts trivially and composition agrees with group multiplication.", "geometry.transformations", []),
    ("orbit", "Transformation orbit", "An orbit is the set of points or configurations reachable from one input under a group action.", "geometry.transformations", []),
    ("stabilizer", "Transformation stabilizer", "A stabilizer is the subgroup of transformations that leave a chosen point or object unchanged.", "geometry.transformations", []),
    ("spatial-frame", "Spatial reference frame", "A spatial frame specifies origin, axes, handedness, scale, and orientation for describing positions and directions.", "geometry.spatial-reasoning", []),
    ("containment", "Spatial containment", "Containment distinguishes interior, boundary, and exterior relations under the topology and geometry of the represented objects.", "geometry.spatial-reasoning", []),
    ("adjacency", "Spatial adjacency", "Adjacency records which regions or objects share a declared boundary or neighborhood relation without requiring metric closeness alone.", "geometry.spatial-reasoning", []),
    ("occlusion", "Occlusion", "Occlusion occurs when one object blocks a viewing ray to another under a viewpoint and projection model.", "geometry.spatial-reasoning", []),
    ("mental-rotation", "Mental rotation structure", "A mental-rotation task compares objects under candidate rotations while preserving shape, chirality, and incidence rather than relying on pixel similarity.", "geometry.spatial-reasoning", []),
    ("perspective-cue", "Perspective cue", "Perspective cues such as convergence, relative size, overlap, and shading constrain but do not uniquely determine three-dimensional structure.", "geometry.spatial-reasoning", []),
    ("geometric-product", "Geometric product", "The geometric product combines inner and exterior products, encoding metric and oriented subspace relations in a Clifford algebra.", "geometry.geometric-algebra", []),
    ("blade", "Blade", "A blade represents an oriented subspace element formed as an exterior product of independent vectors.", "geometry.geometric-algebra", []),
    ("wedge-product", "Exterior product", "The wedge product is alternating and encodes oriented area, volume, and higher-dimensional subspace elements.", "geometry.geometric-algebra", []),
    ("multivector", "Multivector", "A multivector is a sum of scalar, vector, bivector, and higher-grade components in a geometric algebra.", "geometry.geometric-algebra", []),
    ("rotor", "Rotor", "A normalized even multivector can encode a rotation through a sandwich action while avoiding coordinate singularities of some angle parameterizations.", "geometry.geometric-algebra", []),
    ("mesh-topology", "Mesh topology", "Mesh topology records vertices, edges, faces, cells, adjacency, boundary, and incidence independently of vertex coordinates.", "geometry.meshes-cad", []),
    ("mesh-geometry", "Mesh geometry", "Mesh geometry assigns positions, normals, metrics, and attributes to topological mesh elements.", "geometry.meshes-cad", []),
    ("manifold-mesh", "Manifold mesh", "A manifold surface mesh has neighborhoods locally equivalent to a disk or half-disk, subject to orientation and boundary conventions.", "geometry.meshes-cad", []),
    ("boundary-representation", "Boundary representation", "A CAD boundary representation encodes a solid through oriented faces, edges, vertices, geometry, topology, and consistency relations.", "geometry.meshes-cad", ["B-rep"]),
    ("constructive-solid", "Constructive solid geometry", "Constructive solid geometry builds solids from primitive regions using regularized Boolean operations and transformations.", "geometry.meshes-cad", ["CSG"]),
    ("parametric-surface", "Parametric surface", "A parametric surface maps a two-dimensional parameter domain into space with derivatives, seams, singularities, and trimming boundaries.", "geometry.meshes-cad", []),
    ("cad-tolerance", "CAD geometric tolerance", "A geometric tolerance declares acceptable deviation and topology decisions for representations that cannot rely on exact real arithmetic.", "geometry.meshes-cad", []),
    ("orientation-predicate", "Orientation predicate", "An orientation predicate uses a determinant sign to classify left, right, coplanar, or degenerate configurations under exact or certified arithmetic.", "geometry.computational", []),
    ("segment-intersection", "Segment intersection", "Segment intersection combines orientation and bounding predicates while handling endpoint, collinear, and overlapping cases explicitly.", "geometry.computational", []),
    ("voronoi", "Voronoi diagram", "A Voronoi diagram partitions space into cells whose points are closest to each generating site under a declared metric.", "geometry.computational", []),
    ("delaunay", "Delaunay triangulation", "A Delaunay triangulation is dual to a Voronoi diagram under general-position conditions and satisfies an empty-circumcircle property.", "geometry.computational", []),
    ("spatial-index", "Spatial index", "A spatial index organizes bounding regions or partitions to prune geometric queries without changing exact final predicates.", "geometry.computational", [])
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
    ("geometry-invariant-warrant", "invariant", "congruence", "qualifies", "Congruence requires the invariants of isometry, not merely visual resemblance.", [], []),
    ("circle-metric", "metric", "circle", "grounds", "A metric and center ground the equal-distance definition of a circle.", ["positive radius"], []),
    ("polygon-segment", "segment", "polygon", "part_of", "Segments form the boundary edges of a polygon.", [], []),
    ("polyhedron-polygon", "polygon", "polyhedron", "part_of", "Polygonal faces form the boundary of a polyhedron.", [], []),
    ("scaling-area", "uniform-scaling", "area", "transforms_to", "Uniform scaling by a factor transforms area by the square of its magnitude.", [], []),
    ("scaling-volume", "uniform-scaling", "volume", "transforms_to", "Uniform scaling by a factor transforms volume by the cube of its magnitude.", [], []),
    ("coordinate-equation-frame", "coordinate-system", "coordinate-equation", "enables", "A coordinate frame enables equation representations of loci.", [], []),
    ("dot-angle", "dot-product", "angle", "grounds", "The normalized dot product grounds Euclidean angle for nonzero vectors.", ["nonzero vectors"], []),
    ("dot-perpendicular", "dot-product", "perpendicularity", "grounds", "A zero Euclidean dot product grounds perpendicularity.", ["nonzero directions"], []),
    ("cross-area", "cross-product", "area", "measures", "Cross-product magnitude measures parallelogram area in three dimensions.", [], []),
    ("matrix-transformation", "transformation-matrix", "transformation", "implements", "A matrix implements a linear transformation in selected bases.", [], []),
    ("affine-combination-preservation", "affine-combination", "affine-transformation", "qualifies", "Preservation of affine combinations qualifies an affine transformation.", [], []),
    ("barycentric-affine", "barycentric", "affine-combination", "implements", "Barycentric coordinates implement affine combinations relative to reference vertices.", [], []),
    ("independence-dimension", "affine-independence", "dimension", "grounds", "The size of an affinely independent simplex grounds its affine dimension.", [], []),
    ("homogeneous-projective", "homogeneous-coordinate", "projective-transformation", "enables", "Homogeneous coordinates enable matrix representation of projective transformations.", [], []),
    ("infinity-parallel", "point-at-infinity", "parallelism", "clarifies", "Projective points at infinity clarify common affine directions of parallel lines.", [], []),
    ("crossratio-invariant", "cross-ratio", "invariant", "part_of", "Cross-ratio is a projective invariant where defined.", [], []),
    ("duality-incidence", "dual-projective", "incidence", "transforms_to", "Projective duality transforms point-hyperplane incidence statements into dual statements.", [], []),
    ("lattice-basis", "basis-change", "lattice", "qualifies", "Integral unimodular basis changes preserve a lattice while changing its generators.", [], []),
    ("planar-incidence", "planar-graph", "incidence", "qualifies", "A planar embedding qualifies graph incidence with cyclic and face structure.", [], []),
    ("polytope-convex", "polytope", "convexity", "part_of", "A convex polytope is a finite convex object.", [], []),
    ("discrete-mesh", "discrete-curvature", "mesh", "qualifies", "Discrete curvature qualifies a mesh approximation of smooth curvature.", [], []),
    ("convexcomb-convex", "convex-combination", "convexity", "grounds", "Closure under convex combinations grounds convexity.", [], []),
    ("hull-combination", "convex-combination", "convex-hull", "grounds", "Finite convex combinations ground the convex hull.", [], []),
    ("support-convex", "supporting-hyperplane", "convexity", "qualifies", "A supporting hyperplane qualifies a convex boundary direction.", [], []),
    ("separation-disjoint", "separation", "convexity", "supports", "A separation certificate supports nonintersection of suitably conditioned convex sets.", [], []),
    ("chart-manifold", "chart", "manifold", "part_of", "Charts provide local coordinate neighborhoods of a manifold.", [], []),
    ("atlas-chart", "chart", "atlas", "part_of", "Compatible charts compose an atlas.", [], []),
    ("atlas-manifold", "atlas", "manifold", "qualifies", "Atlas transition regularity qualifies the smooth structure on a manifold.", [], []),
    ("smooth-chart", "chart", "smooth-map", "qualifies", "Coordinate representations in charts qualify smoothness of a map.", [], []),
    ("differential-tangent", "differential", "tangent-space", "transforms_to", "The differential maps tangent vectors between tangent spaces.", [], []),
    ("field-tangent", "vector-field", "tangent-space", "part_of", "A vector field selects an element of each tangent space.", [], []),
    ("metric-tangent", "riemannian-metric", "tangent-space", "qualifies", "A Riemannian metric equips each tangent space with an inner product.", [], []),
    ("metric-geodesic", "riemannian-metric", "geodesic", "grounds", "A Riemannian metric and its connection ground the geodesic equation.", [], []),
    ("connection-geodesic", "connection", "geodesic", "grounds", "Zero covariant acceleration under a connection grounds geodesic motion.", [], []),
    ("exp-geodesic", "exponential-map", "geodesic", "implements", "The exponential map implements geodesic evolution from tangent initial data.", [], []),
    ("sectional-curvature-kind", "sectional-curvature", "curvature", "part_of", "Sectional curvature is one Riemannian curvature measure.", [], []),
    ("ricci-sectional", "sectional-curvature", "ricci-curvature", "transforms_to", "Ricci curvature aggregates sectional curvature around a direction.", [], []),
    ("scalar-ricci", "ricci-curvature", "scalar-curvature", "transforms_to", "Tracing Ricci curvature produces scalar curvature.", [], []),
    ("polynomial-ideal", "ideal", "polynomial-locus", "grounds", "A polynomial ideal grounds a shared algebraic zero locus.", [], []),
    ("affine-locus", "polynomial-locus", "affine-variety", "grounds", "Polynomial zero loci in affine space ground affine algebraic sets.", [], []),
    ("homogeneous-projective-variety", "homogeneous-coordinate", "projective-variety", "prerequisite", "Homogeneous coordinates and equations are prerequisite to a well-defined projective variety.", [], []),
    ("singularity-variety", "algebraic-singularity", "affine-variety", "qualifies", "Singular points qualify failure of expected smooth local variety structure.", [], []),
    ("connected-topology", "topology", "connectedness", "grounds", "Open-set separation grounds connectedness.", [], []),
    ("compact-topology", "topology", "compactness", "grounds", "Open covers ground the topological definition of compactness.", [], []),
    ("homotopy-continuity", "continuity", "homotopy", "prerequisite", "A homotopy is a continuous parameterized deformation.", [], []),
    ("fundamental-homotopy", "homotopy", "fundamental-group", "grounds", "Loop homotopy classes ground the fundamental group.", [], []),
    ("homology-topology", "homology", "topology", "implements", "Homology implements algebraic invariants of topological cycle structure.", [], []),
    ("selfsimilar-fractal", "self-similarity", "fractal-dimension", "qualifies", "Self-similar scaling can qualify a fractal-dimension relation under separation assumptions.", [], []),
    ("ifs-fractal", "iterated-function-system", "self-similarity", "causes", "Contractive iterated functions cause an invariant self-similar attractor.", [], []),
    ("dimension-scale", "scale-invariance", "fractal-dimension", "grounds", "Scaling behavior grounds box-counting and related dimension estimates.", [], []),
    ("symmetry-invariant", "symmetry", "invariant", "grounds", "A symmetry group grounds the properties treated as invariant.", [], []),
    ("action-transformation", "group-action", "transformation", "implements", "A group action implements compatible transformations of a space.", [], []),
    ("orbit-action", "group-action", "orbit", "causes", "Applying all group elements causes the orbit of a point.", [], []),
    ("stabilizer-action", "stabilizer", "group-action", "part_of", "The stabilizer is a subgroup within a group action.", [], []),
    ("frame-coordinate", "spatial-frame", "coordinate-system", "implements", "A spatial frame implements a coordinate reference for positions and directions.", [], []),
    ("containment-topology", "topology", "containment", "qualifies", "Topology qualifies interior and boundary used in containment.", [], []),
    ("adjacency-incidence", "adjacency", "incidence", "analogous_to", "Adjacency and incidence are related discrete spatial relations with different boundary requirements.", [], []),
    ("occlusion-projection", "projection", "occlusion", "enables", "A viewpoint projection enables depth ordering and occlusion.", [], []),
    ("mental-rotation-implements", "rotation", "mental-rotation", "implements", "Candidate rotations implement structural comparison in a mental-rotation task.", [], []),
    ("perspective-projection", "perspective-cue", "projection", "supports", "Perspective cues support hypotheses about a projection and scene.", [], []),
    ("product-wedge", "wedge-product", "geometric-product", "part_of", "The exterior product forms the antisymmetric part of the geometric product.", [], []),
    ("wedge-blade", "wedge-product", "blade", "causes", "The exterior product of independent vectors causes a blade representing their oriented span.", [], []),
    ("blade-multivector", "blade", "multivector", "part_of", "Blades are homogeneous components of multivectors.", [], []),
    ("rotor-rotation", "rotor", "rotation", "implements", "Rotor sandwich action implements rotations in geometric algebra.", [], []),
    ("mesh-topology-geometry", "mesh-topology", "mesh-geometry", "qualifies", "Topology qualifies which geometric attributes and elements are adjacent.", [], []),
    ("mesh-manifold", "manifold-mesh", "mesh-topology", "qualifies", "Local disk or half-disk neighborhoods qualify manifold mesh topology.", [], []),
    ("brep-solid", "boundary-representation", "polyhedron", "analogous_to", "A boundary representation generalizes polyhedral boundary topology to curved CAD geometry.", [], []),
    ("csg-solid", "constructive-solid", "containment", "transforms_to", "Regularized Boolean operations transform contained solid regions.", [], []),
    ("parametric-manifold", "parametric-surface", "manifold", "supports", "A regular parametric surface supports a local two-dimensional manifold representation.", [], []),
    ("tolerance-robust", "cad-tolerance", "numerical-robustness", "qualifies", "CAD tolerance qualifies numerical topology decisions near coincident geometry.", [], []),
    ("orientation-degeneracy", "orientation-predicate", "degeneracy", "clarifies", "An exact zero orientation determinant clarifies an affine degeneracy.", [], []),
    ("segment-orientation", "orientation-predicate", "segment-intersection", "prerequisite", "Orientation predicates are prerequisite to robust segment-intersection classification.", [], []),
    ("voronoi-metric", "metric", "voronoi", "grounds", "A declared distance metric grounds nearest-site Voronoi cells.", [], []),
    ("delaunay-voronoi", "voronoi", "delaunay", "transforms_to", "Voronoi adjacency transforms to Delaunay edges under general-position conventions.", [], []),
    ("index-predicate", "spatial-index", "numerical-robustness", "supports", "A spatial index supports pruning while exact or certified predicates decide final geometry.", [], []),
    ("full-shadow", "full-coordinate-space", "all-spatial-shadow", "transforms_to", "A registered observer transformation maps full coordinates into an all-spatial shadow without replacing the source geometry.", [], []),
    ("orthonormal-shadow", "orthonormal-projection", "all-spatial-shadow", "implements", "An orthonormal row basis implements a non-expansive Euclidean shadow.", [], []),
    ("basis-projection", "observer-basis", "orthonormal-projection", "qualifies", "The registered basis and metric qualify which non-expansion claim can be made.", [], []),
    ("shadow-collision", "all-spatial-shadow", "projection-collision", "causes", "Dropping geometric information can cause distinct full-space points to share one observer cell.", [], []),
    ("shadow-proximity", "all-spatial-shadow", "false-proximity", "causes", "Distance contraction can cause full-far points to appear near in a shadow.", [], []),
    ("collision-edge", "projection-collision", "invisible-edge", "enables", "A collision enables an exact edge to appear as a degenerate self-loop to the observer.", [], []),
    ("composition-shadow", "projection-composition", "all-spatial-shadow", "qualifies", "Composition tests qualify whether chained 3D and 2D observer views reproduce their direct transformations.", [], [])
]


EXAMPLES = [
    ("example-coordinate-translation", "Coordinate translation example", "Translating every point by the same vector changes coordinates but preserves every pairwise displacement and distance.", "geometry.transformations", ["translation example"]),
    ("example-reflection-twice", "Reflection involution example", "Reflecting a point across the same line twice returns the original point.", "geometry.transformations", ["reflection twice"]),
    ("example-projection-ambiguity", "Projection ambiguity example", "Distinct three-dimensional points can share one two-dimensional projected location, demonstrating depth information loss.", "geometry.projective", ["depth ambiguity"]),
    ("example-coordinate-invariance", "Coordinate invariance example", "Rotating a coordinate frame changes component values while a consistently transformed geometric relation remains the same.", "geometry.analytic", ["frame change"]),
    ("example-graph-path", "Graph distance example", "In an unweighted graph, the distance between connected vertices is the minimum number of traversed edges.", "geometry.discrete", ["shortest path"]),
    ("example-degenerate-triangle", "Degenerate triangle example", "Three collinear points have zero triangle area and do not form a nondegenerate triangle.", "geometry.computational", ["zero area triangle"]),
    ("example-barycentric", "Barycentric containment example", "A point with three nonnegative triangle barycentric coordinates summing to one lies in the closed triangle, while a negative coefficient places it outside across the opposite edge.", "geometry.affine", []),
    ("example-projective-parallel", "Projective parallel-lines example", "Two affine parallel rails meet at a projective point at infinity under perspective representation without becoming physically intersecting rails.", "geometry.projective", []),
    ("example-convex-separation", "Convex separation example", "Two disjoint compact convex polygons admit a separating line whose signed half-space inequalities certify nonintersection.", "geometry.convex", []),
    ("example-sphere-geodesic", "Sphere geodesic example", "Great-circle arcs are geodesics on a round sphere, while the shorter arc is distance minimizing only until the relevant cut point.", "geometry.riemannian", []),
    ("example-singular-locus", "Algebraic singularity example", "At a crossing polynomial curve, the gradient vanishes and the local locus does not have one regular tangent direction.", "geometry.algebraic", []),
    ("example-loop-hole", "Fundamental-loop example", "A loop around a puncture cannot contract without crossing the missing point, while the same loop contracts after the puncture is filled.", "geometry.topology", []),
    ("example-fractal-scale", "Fractal scale example", "A self-similar set made from multiple scaled copies yields a dimension relation only after the contraction and overlap conditions are declared.", "geometry.fractal", []),
    ("example-mental-rotation", "Structural mental rotation example", "A candidate rotation preserves edge incidence and handedness, whereas a mirror image matches many projected distances but reverses orientation.", "geometry.spatial-reasoning", []),
    ("example-rotor", "Geometric-algebra rotor example", "A normalized rotor and its reverse sandwich a vector to rotate it while preserving its squared norm.", "geometry.geometric-algebra", []),
    ("example-voronoi-delaunay", "Voronoi-Delaunay dual example", "Two sites share a Delaunay edge exactly when their Voronoi cells share an edge under the stated nondegeneracy convention.", "geometry.computational", []),
    ("example-brep-tolerance", "B-rep tolerance example", "Two nearly coincident CAD edges are merged only under a declared tolerance and topology check; raw floating equality does not decide solid validity.", "geometry.meshes-cad", []),
    ("example-exact-midpoint", "Exact rational midpoint", "The midpoint of (-3, 4) and (8, -1) is (5/2, 3/2); the formal engine retains the rational coordinates instead of rounding them.", "geometry.analytic", ["rational midpoint"]),
    ("example-exact-point-on-segment", "Exact point-on-segment predicate", "The point (3, 3) lies on the closed segment from (0, 0) to (6, 6) because its orientation determinant is zero and both coordinates lie within the endpoint bounds.", "geometry.computational", ["point on segment"]),
    ("example-exact-segment-intersection", "Exact segment intersection", "The diagonals from (0, 0) to (6, 6) and from (0, 6) to (6, 0) intersect because each pair of endpoint orientations has opposite signs; collinear endpoint contact is handled as a separate boundary case.", "geometry.computational", ["segment intersection"]),
    ("example-exact-polygon-area", "Exact polygon area", "The shoelace sum for the rectangle (0,0), (5,0), (5,3), (0,3) has absolute twice-area 30, agreeing with an independent triangle-fan decomposition.", "geometry.computational", ["shoelace area"]),
    ("example-exact-line-intersection", "Exact rational line intersection", "The infinite lines through (0,0)-(3,3) and (0,2)-(4,0) meet at (4/3, 4/3); parallel or coincident lines have no unique intersection and fail closed.", "geometry.analytic", ["line intersection"]),
    ("example-shadow-non-expansion", "Shadow non-expansion certificate", "For an orthonormal four-row basis P, the operator norm is one and every pair satisfies ||P(a-b)||2 <= ||a-b||2; the certificate is checked across all world-node pairs.", "geometry.shadow-projection", ["projection certificate"]),
    ("example-shadow-composition", "Shadow composition example", "Deleting w from a 4D shadow equals applying the x-y-z rows of the registered 48D-to-4D basis directly; retaining x-y likewise agrees through either 3D intermediate view.", "geometry.shadow-projection", ["48D to 4D to 3D"]),
    ("example-shadow-collision", "Shadow collision example", "Two full-space points that differ only in discarded directions can occupy one quantized 4D observer cell while their distinct node identities and exact connecting edge remain present.", "geometry.shadow-projection", ["invisible edge"])
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
    ("control-floating-predicate", "Near-degenerate numerical predicate", "A floating-point sign near zero must not be treated as an exact orientation proof without an error bound or exact predicate."),
    ("control-geodesic-shortest", "Geodesic is not globally shortest", "A geodesic must not be described as globally distance minimizing beyond its valid interval."),
    ("control-chart-global", "One chart is not whole manifold", "Local Euclidean coordinates must not be assumed to cover a manifold globally without a chart-domain proof."),
    ("control-topology-shape", "Homeomorphism preserves every shape", "A homeomorphism must not be reported as preserving angles, curvature, straightness, or metric shape."),
    ("control-fractal-dimension", "One fractal dimension", "A dimension value must not be reported without naming the dimension definition and verifying its assumptions."),
    ("control-perspective-depth", "Perspective cue proves depth", "A single perspective cue must not be treated as a unique reconstruction of three-dimensional depth."),
    ("control-wedge-cross", "Exterior product equals three-dimensional cross product", "The exterior product must not be collapsed into the three-dimensional cross product outside the required duality and dimension conventions."),
    ("control-cad-tolerance", "Tolerance equals exact coincidence", "A CAD tolerance decision must not be stored as a proof that represented mathematical objects are exactly identical."),
    ("control-spatial-index", "Bounding-box hit proves intersection", "A spatial-index candidate overlap must not be treated as exact geometric intersection without a final predicate."),
    ("control-shadow-authority", "Shadow treated as authority", "A four-dimensional shadow must not replace exact graph reachability, full coordinates, provenance, or epistemic status."),
    ("control-shadow-time", "Fourth shadow axis treated as time", "The all-spatial w axis must not be interpreted as time or causal order."),
    ("control-shadow-nonexpansion", "Arbitrary projection assumed non-expansive", "A learned or nonlinear projection must not inherit a non-expansion guarantee without a compatible metric and certificate."),
    ("control-shadow-collision", "Projection collision erased", "Collisions, invisible edges, and false proximity must remain measured instead of being hidden as successful compression.")
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
        split = ["train", "validation", "sealed_test"][index % 3]
        records.append({
            **base(identifier, subject, split, SOURCES, "formal", "worked_example"),
            "label": label,
            "statement": statement,
            "aliases": aliases,
            "coverage_axes": ["deductions_predictions_execution", "applications_toolchains", "within_domain_composition"]
        })
        records.append({
            **base(f"membership-{identifier}", subject, split, SOURCES, "formal", "relation"),
            "label": f"{label} geometry membership",
            "statement": f"{label} is a checked application of the structural geometry foundation.",
            "aliases": [],
            "relation": {
                "source_node": f"geometry.v0.{identifier}",
                "target_node": "geometry.v0.root",
                "kind": "part_of",
                "polarity": 1,
                "direction": "forward",
                "conditions": ["the example's exact arithmetic and geometric assumptions hold"],
                "exceptions": []
            },
            "coverage_axes": ["applications_toolchains", "within_domain_composition"]
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
