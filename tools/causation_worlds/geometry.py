"""Geometry causation: parallels, similarity, right triangles, circles, rigidity."""

WORLD = "geometry-causation-v0"
PREFIX = "geo"
DOMAIN = "geometry"
SUBJECT = "geometry.euclidean"
SOURCES = ["mathlib4", "nist-dlmf"]
SCOPE = "Everyday Euclidean geometry: parallel lines, triangle angle sums, similarity and scale, right triangles, circles, rigidity of structures"
ROOT_LABEL = "Geometry causation world"
ROOT_STATEMENT = 'Root of the geometry causation world: how Euclidean hypotheses predict lengths, angles and measures, and how ideal braces constrain planar frame motion.'

CONCEPTS = [
    ('straight-line-segment', 'Straight line segment', 'The set {(1-t)A+tB: 0 <= t <= 1} joining two points in Euclidean space.', []),
    ('parallel-lines', 'Parallel lines', 'Distinct coplanar straight lines with no intersection; in Euclidean geometry their perpendicular separation is constant.', []),
    ('parallel-postulate', 'Parallel postulate', 'Through a point off a line exactly one parallel to it exists in the flat plane.', []),
    ('transversal', 'Transversal of parallels', 'A straight line meeting two distinct parallel lines in two distinct points.', []),
    ('corresponding-angles', 'Corresponding angles', 'Matching corner angles where a transversal crosses two lines.', []),
    ('alternate-angles', 'Alternate interior angles', 'The inside angles on opposite sides of a transversal between two lines.', []),
    ('angle-sum-triangle', 'Triangle angle sum', 'The three inside angles of a flat-plane triangle always add to 180 degrees.', []),
    ('exterior-angle', 'Exterior angle of a triangle', "The angle a triangle's side makes when extended past a corner.", []),
    ('triangle-inequality', 'Triangle inequality', 'For positive side lengths of a nondegenerate Euclidean triangle, each is strictly smaller than the sum of the other two.', []),
    ('triangle-existence', 'Triangle existence from three sides', 'The existence of a nondegenerate Euclidean triangle realizing three specified positive side lengths.', []),
    ('side-angle-link', 'Side and angle ranking', 'Longer sides of a triangle always sit opposite larger angles.', []),
    ('similar-triangles', 'Similar triangles', 'Triangles with equal matching angles and proportional sides.', []),
    ('aa-criterion', 'Angle-angle similarity', 'Two matching angles are enough to prove two triangles similar.', []),
    ('scale-factor', 'Uniform scaling', 'A Euclidean dilation x -> c + k(x-c) with fixed centre c and positive scale factor k.', []),
    ('area-scale-square', 'Squared area scale', 'The ratio k^2 of areas before and after a uniform length dilation with factor k > 0.', []),
    ('volume-scale-cube', 'Cubed volume scale', 'The ratio k^3 of volumes before and after a uniform length dilation with factor k > 0.', []),
    ('right-triangle', 'Right triangle', 'A triangle holding a 90 degree corner.', []),
    ('hypotenuse', 'Hypotenuse', 'The side of a right triangle opposite the right angle, always its longest.', []),
    ('pythagorean-relation', 'Pythagorean relation', 'In a right triangle the squared hypotenuse equals the sum of squared legs.', []),
    ('converse-pythagorean', 'Converse Pythagorean test', 'If the squared longest side equals the sum of squared others, the corner is right.', []),
    ('diameter', 'Diameter of a circle', 'A segment through a circle centre with endpoints on the circle, of length twice the radius.', []),
    ('pi-constant', 'Pi constant', "The ratio of every circle's circumference to its diameter, an irrational number near 3.1416.", []),
    ('circle-circumference', 'Circle circumference', 'The length of the boundary of a Euclidean disk.', []),
    ('circle-area', 'Circle area', 'The two-dimensional Euclidean area of a disk.', []),
    ('central-angle', 'Central angle', 'The angle at the circle centre subtending a selected arc, allowing the reflex angle when the selected arc exceeds a semicircle.', []),
    ('inscribed-angle', 'Inscribed angle', 'An angle with vertex on a circle and sides along two distinct chords through that vertex.', []),
    ('thales-triangle', 'Triangle in a semicircle', 'A triangle whose one side is a circle diameter and whose third distinct vertex lies on the circle.', []),
    ('congruence-sas', 'Side-angle-side congruence', 'Two triangles matching in two sides and the angle between them are copies of each other.', []),
    ('triangle-rigidity', 'Triangle rigidity', 'Preservation of a noncollinear triangle shape when all three side lengths are fixed, up to rigid motions and reflection.', []),
    ('quadrilateral-wobble', 'Quadrilateral shear', 'A continuous change of a planar hinged quadrilateral shape while its four side lengths stay fixed.', []),
    ('diagonal-brace', 'Diagonal brace', 'A length-fixed member attached between opposite corners of a hinged quadrilateral frame.', []),
    ('angle-sum-quadrilateral', 'Quadrilateral angle sum', 'The sum of interior angles of a simple Euclidean quadrilateral, including a reflex angle if present.', []),
    ('polygon-interior-sum', 'Polygon interior angle sum', 'The sum of interior angles of a simple Euclidean polygon, counting any reflex interior angles.', []),
    ('perpendicular-foot', 'Perpendicular distance', 'The Euclidean distance from a point to its orthogonal projection on a line.', []),
    ('area-additivity', 'Area additivity', "A shape's area equals the sum of the areas of its non-overlapping parts.", []),
    ('regular-tessellation', 'Regular tessellation', 'An edge-to-edge tiling of the Euclidean plane by congruent copies of a single regular polygon.', []),
    ('congruence-sss', 'Side-side-side congruence', 'The theorem that equal corresponding side lengths make two nondegenerate Euclidean triangles congruent.', []),
    ('radius', 'Circle radius', 'The positive distance from the centre of a nondegenerate circle to any of its points.', []),
    ('tessellation-area', 'Tessellation area calculation', 'The computation of the area of a specified finite union of tiles.', []),
    ('angle-distortion', 'Angle distortion', 'A change in the angle between corresponding line segments under a transformation.', []),
]

RELATIONS = [
    ('transversal-predicts-corresponding', 'transversal', 'corresponding-angles', 'predicts', 'A transversal of parallels predicts equal corresponding angles.', 'two distinct lines are parallel in a Euclidean plane and a third line intersects each of them', ''),
    ('transversal-predicts-alternate', 'transversal', 'alternate-angles', 'predicts', 'A transversal of parallels predicts equal alternate interior angles.', 'a line crosses two distinct coplanar parallel lines at separate points in Euclidean geometry', ''),
    ('aa-predicts-similar', 'aa-criterion', 'similar-triangles', 'predicts', 'Angle-angle similarity predicts similar triangles without requiring side measurements.', 'two nondegenerate Euclidean triangles have two equal pairs of corresponding interior angles', ''),
    ('similar-predicts-scaling', 'similar-triangles', 'scale-factor', 'predicts', 'A pair of similar triangles predicts a uniform scaling factor relating all corresponding side lengths.', 'matching vertices of two nondegenerate Euclidean triangles are fixed, and scaling may be followed by an isometry', ''),
    ('scale-predicts-area', 'scale-factor', 'area-scale-square', 'predicts', 'Uniform scaling predicts squared area scale k^2.', 'a planar measurable figure of finite positive area is dilated by one positive length factor k in every direction', ''),
    ('scale-predicts-volume', 'scale-factor', 'volume-scale-cube', 'predicts', 'Uniform scaling predicts cubed volume scale k^3.', 'a measurable solid of finite positive volume in Euclidean three-space is dilated by one factor k > 0 along every spatial axis', ''),
    ('right-prereq-pythagoras', 'right-triangle', 'pythagorean-relation', 'prerequisite', 'A right triangle is a prerequisite for the Pythagorean relation c^2 = a^2+b^2 between its side lengths.', 'a,b,c are the positive side lengths of a nondegenerate Euclidean triangle and c is its longest side', ''),
    ('pythagoras-predicts-hypotenuse', 'pythagorean-relation', 'hypotenuse', 'predicts', 'The Pythagorean relation predicts the hypotenuse length as sqrt(a^2+b^2).', 'a and b are the known positive perpendicular leg lengths of a Euclidean right triangle', ''),
    ('converse-predicts-right', 'converse-pythagorean', 'right-triangle', 'predicts', 'The converse Pythagorean test predicts a right triangle from c^2 = a^2+b^2.', 'a,b,c are sides of a nondegenerate Euclidean triangle, c is longest, and c^2 = a^2+b^2', ''),
    ('diameter-predicts-thales', 'diameter', 'thales-triangle', 'predicts', 'A diameter of a circle predicts a right angle at the third vertex of a triangle in a semicircle.', 'the circle has positive radius and the third vertex is on the circle but differs from both diameter endpoints', ''),
    ('central-predicts-inscribed', 'central-angle', 'inscribed-angle', 'predicts', 'A central angle predicts an inscribed angle equal to half its measure when both subtend the same arc.', 'A and B are distinct points of a Euclidean circle, the inscribed vertex lies on the complementary open arc, and the central angle measures the selected arc AB, including a reflex angle when needed', ''),
    ('anglesum-predicts-exterior', 'angle-sum-triangle', 'exterior-angle', 'predicts', 'The triangle angle sum predicts an exterior angle of a triangle equal to the sum of its two remote interior angles.', 'the triangle is nondegenerate and Euclidean, and the exterior angle is supplementary to the interior angle at the extended side', ''),
    ('anglesum-predicts-quadsum', 'angle-sum-triangle', 'angle-sum-quadrilateral', 'predicts', 'The triangle angle sum predicts a quadrilateral angle sum of 360 degrees.', 'a simple nondegenerate Euclidean quadrilateral is divided along an internal diagonal into two nonoverlapping triangles', ''),
    ('anglesum-predicts-polygonsum', 'angle-sum-triangle', 'polygon-interior-sum', 'predicts', 'The triangle angle sum predicts a polygon interior angle sum of (n-2) times 180 degrees.', 'a simple Euclidean polygon with n >= 3 vertices is triangulated into n-2 nonoverlapping triangles; any reflex interior angles are counted', ''),
    ('diameter-predicts-circumference', 'diameter', 'circle-circumference', 'predicts', 'The diameter of a circle predicts its circle circumference as pi times the diameter length.', 'the circle is Euclidean with positive diameter d, so its rectifiable boundary has length pi*d', ''),
    ('radius-predicts-circlearea', 'radius', 'circle-area', 'predicts', 'The circle radius predicts the circle area as pi*r^2.', 'r > 0 is the radius of a disk in the Euclidean plane and area uses the usual two-dimensional measure', ''),
    ('sss-predicts-rigidity', 'congruence-sss', 'triangle-rigidity', 'predicts', 'Side-side-side congruence predicts triangle rigidity when the three side lengths are fixed.', 'three positive lengths satisfy all strict triangle inequalities and the triangle remains in Euclidean space', ''),
    ('brace-causes-rigidity', 'diagonal-brace', 'triangle-rigidity', 'causes', 'A diagonal brace causes triangle rigidity in each half of an ideal planar four-sided frame.', 'the four side members and attached diagonal have fixed lengths, the two triangles are noncollinear, and joints remain connected with motion restricted to the plane', ''),
    ('brace-prevents-wobble', 'diagonal-brace', 'quadrilateral-wobble', 'prevents', 'A diagonal brace prevents quadrilateral shear by fixing the shapes of the two triangles.', 'a nondegenerate planar hinged frame has rigid side bars and a securely attached diagonal that resists tension and compression without deformation', ''),
    ('inequality-predicts-existence', 'triangle-inequality', 'triangle-existence', 'predicts', 'The triangle inequality predicts triangle existence from three sides when all three strict inequalities hold.', 'the three proposed lengths are positive real numbers and each length is strictly less than the sum of the other two', ''),
    ('ranking-predicts-hypotenuse', 'side-angle-link', 'hypotenuse', 'predicts', 'Side and angle ranking predicts the hypotenuse as the unique longest side of a right triangle.', 'the Euclidean triangle is nondegenerate with one interior angle of 90 degrees and two strictly smaller positive angles', ''),
    ('pythagoras-predicts-perpendicular', 'pythagorean-relation', 'perpendicular-foot', 'predicts', 'The Pythagorean relation predicts perpendicular distance as the minimum distance from a point to a line.', 'P lies off a Euclidean line, H is its perpendicular foot, and any other point Q on the line gives PQ^2 = PH^2+HQ^2', ''),
    ('areaadd-enables-circle', 'area-additivity', 'circle-area', 'enables', 'Area additivity enables a sector-rearrangement derivation of circle area in the limit of infinitely fine sectors.', 'a disk of radius r > 0 is partitioned into equal sectors without overlapping interiors, and a justified area limit of their rearrangements is the rectangle with sides pi*r and r', ''),
    ('parallels-prereq-corresponding', 'parallel-lines', 'corresponding-angles', 'prerequisite', 'A pair of parallel lines is a prerequisite for equal corresponding angles at a transversal in the Euclidean plane.', 'two distinct coplanar lines meet a transversal at distinct points, and one matching pair of corresponding angles is equal', ''),
    ('alternate-predicts-parallels', 'alternate-angles', 'parallel-lines', 'predicts', 'Equality of alternate interior angles predicts parallel lines.', 'two distinct coplanar Euclidean lines meet the same transversal at separate points and an alternate interior angle pair is equal', ''),
    ('polysum-predicts-tessellation', 'polygon-interior-sum', 'regular-tessellation', 'predicts', 'The polygon interior angle sum predicts that a regular tessellation by a single polygon type can use only triangles, squares or hexagons.', 'congruent regular n-gons tile the Euclidean plane edge to edge with q >= 3 corners at each vertex, so q*(n-2)*180/n = 360 with integer n >= 3', ''),
    ('pythagoras-predicts-diagonal', 'pythagorean-relation', 'straight-line-segment', 'predicts', 'The Pythagorean relation predicts a straight line segment length as sqrt(dx^2+dy^2).', 'the endpoints have coordinate differences dx and dy in an orthonormal Cartesian coordinate system in the Euclidean plane', ''),
    ('postulate-predicts-anglesum', 'parallel-postulate', 'angle-sum-triangle', 'predicts', 'The parallel postulate predicts a triangle angle sum of 180 degrees.', 'the remaining axioms of neutral plane geometry hold, and the triangle is nondegenerate', ''),
    ('scale-prevents-anglechange', 'scale-factor', 'angle-distortion', 'prevents', 'Uniform scaling prevents angle distortion between corresponding nonzero line segments.', 'the transformation is one dilation x -> c+k(x-c) with the same k > 0 in every direction in Euclidean space', ''),
    ('pythagoras-enables-converse', 'pythagorean-relation', 'converse-pythagorean', 'enables', 'The Pythagorean relation enables a proof of the converse Pythagorean test by a constructed right triangle and side-side-side congruence.', 'a nondegenerate triangle has lengths a,b,c satisfying a^2+b^2=c^2, and a right triangle with legs a,b is constructed and compared by SSS', ''),
    ('areaadd-enables-tessellation', 'area-additivity', 'tessellation-area', 'enables', 'Area additivity enables tessellation area calculation by summing tile areas.', 'the patch is exactly a finite union of congruent tiles with pairwise disjoint interiors; shared boundaries have zero area', ''),
]

MYTHS = [
    ('pythagoras-all-triangles', 'The Pythagorean rule holds for every triangle', 'The relation holds only for right triangles; in other triangles the squares of two sides need not match the third.', 'pythagorean-relation'),
    ('pi-equals-22-7', 'Pi is exactly 22 over 7', 'Pi is irrational and therefore is not equal to any ratio of integers, including 22/7.', 'pi-constant'),
    ('triangle-180-always', "Every triangle's angles sum to 180 degrees", 'Nondegenerate geodesic triangles on a sphere have angle sum greater than 180 degrees, while those in the hyperbolic plane have sum less than 180 degrees; the Euclidean sum is 180 degrees.', 'angle-sum-triangle'),
    ('area-doubles-with-sides', 'Doubling every side doubles the area', 'Doubling every length multiplies area by four and volume by eight.', 'area-scale-square'),
    ('circles-grow-pi', 'Bigger circles have bigger pi', 'The ratio stays the same for every circle regardless of size.', 'pi-constant'),
]

BOUNDARIES = [
    ('non-euclidean-bounds', 'Geometry depends on the metric', 'Euclidean angle-sum and parallel theorems apply to a flat Euclidean metric; spherical and hyperbolic geodesic triangles have different angle sums.', 'angle-sum-triangle'),
    ('similarity-limits', 'Similarity fixes shape, not size', 'A uniform positive dilation preserves angles and multiplies lengths by k, areas by k^2 and volumes by k^3; a zero factor collapses the figure.', 'scale-factor'),
    ('compass-limits', 'Classical tools cannot square the circle', 'Starting from a given nonzero unit segment, finitely many unmarked straightedge and compass steps cannot construct a square equal in area to the unit disk because pi is transcendental.', 'circle-area'),
    ('at-most-one-right-angle', 'A Euclidean triangle has at most one right angle', 'A nondegenerate Euclidean triangle has three positive interior angles summing to 180 degrees, so at most one can equal 90 degrees.', 'angle-sum-triangle'),
    ('unique-parallel', 'Parallel existence alone is not the parallel postulate', 'The Euclidean parallel postulate asserts uniqueness of the parallel through an external point; neutral geometry already admits a parallel, while hyperbolic geometry admits more than one.', 'parallel-postulate'),
    ('brace-idealization', 'A planar brace does not guarantee physical strength', 'The rigidity conclusion assumes undeformed members, secure joints and planar motion; buckling, loosened joints or out-of-plane folding are outside that ideal model.', 'diagonal-brace'),
    ('strict-side-inequality', 'Equality produces a degenerate triangle', 'Lengths 1, 2 and 3 do not form a nondegenerate triangle because one length equals the sum of the other two.', 'triangle-existence'),
]

EXAMPLES = [
    ('ladder-wall', 'A ladder against a wall', 'A 5-metre straight ladder against a vertical wall reaches 4 metres up when its foot is 3 metres from the wall on level ground, since 3^2+4^2=5^2.', ['right-triangle', 'pythagorean-relation', 'hypotenuse']),
    ('shadow-height', 'Measuring a tree from its shadow', 'On level ground with parallel sunlight rays, a vertical 2-metre stick casting a 3-metre shadow and a vertical tree casting a 12-metre shadow form similar triangles, giving tree height 8 metres.', ['similar-triangles', 'scale-factor', 'aa-criterion']),
    ('shelf-brace', 'Bracing a wobbly shelf', 'An ideal rectangular frame of rigid side bars and hinged corners can shear; attaching a rigid diagonal fixes all three sides of each triangle and blocks in-plane shear.', ['diagonal-brace', 'quadrilateral-wobble', 'triangle-rigidity']),
    ('fence-around-pond', 'Fencing around a circular pond', 'A Euclidean circular pond of diameter 10 metres needs 10*pi metres of fence along its boundary, assuming no gate allowance.', ['circle-circumference', 'pi-constant', 'diameter']),
    ('collinear-sides', 'Three lengths that do not close', 'Lengths 1, 2 and 3 satisfy non-strict triangle inequalities but only give a straight, degenerate configuration, so strict inequalities are required.', ['triangle-inequality', 'triangle-existence']),
    ('thales-endpoint', 'The excluded endpoint in Thales theorem', 'For diameter endpoints A and B, a third point C on the circle gives angle ACB=90 degrees only when C differs from A and B; choosing C=A does not produce a triangle.', ['diameter', 'thales-triangle', 'inscribed-angle']),
]

CONTROLS = [
    ('pythagoras-obtuse', 'The Pythagorean relation holds for obtuse triangles', 'The Pythagorean relation must not be treated as holding for triangles without a right angle.'),
    ('pi-shrinks-circle', 'A smaller circle has a smaller pi', 'Pi must not be treated as varying from circle to circle.'),
    ('brace-proves-postulate', 'A diagonal brace proves the parallel postulate', 'A diagonal brace must not be treated as establishing the axioms of the plane.'),
    ('scaling-changes-angles', 'Scaling a figure changes its angles', 'Uniform scaling must not be treated as altering any angle of a figure.'),
    ('sss-not-sas', 'Hinges keep an included angle fixed', 'A freely hinged three-bar frame must not be treated as having an independently fixed included angle; its fixed side lengths supply the SSS argument.'),
    ('triangle-equality', 'Equality is enough for a triangle', 'Three positive lengths with one equal to the sum of the other two must not be treated as forming a nondegenerate triangle.'),
    ('thales-endpoint-control', 'A diameter endpoint is a third vertex', 'A diameter endpoint reused as the third vertex must not be treated as a valid right triangle in Thales theorem.'),
]
