"""Geometry causation: parallels, similarity, right triangles, circles, rigidity."""

WORLD = "geometry-causation-v0"
PREFIX = "geo"
DOMAIN = "geometry"
SUBJECT = "geometry.euclidean"
SOURCES = ["mathlib4", "nist-dlmf"]
SCOPE = "Everyday Euclidean geometry: parallel lines, triangle angle sums, similarity and scale, right triangles, circles, rigidity of structures"
ROOT_LABEL = "Geometry causation world"
ROOT_STATEMENT = "Root of the geometry causation world: how flat-plane axioms cause the angle, length, area and rigidity behaviour of everyday shapes."

CONCEPTS = [
    ("straight-line-segment", "Straight line segment", "The shortest path between two points.", []),
    ("parallel-lines", "Parallel lines", "Lines in one flat plane that never meet, however far extended.", []),
    ("parallel-postulate", "Parallel postulate", "Through a point off a line exactly one parallel to it exists in the flat plane.", []),
    ("transversal", "Transversal of parallels", "A line that crosses two or more other lines.", []),
    ("corresponding-angles", "Corresponding angles", "Matching corner angles where a transversal crosses two lines.", []),
    ("alternate-angles", "Alternate interior angles", "The inside angles on opposite sides of a transversal between two lines.", []),
    ("angle-sum-triangle", "Triangle angle sum", "The three inside angles of a flat-plane triangle always add to 180 degrees.", []),
    ("exterior-angle", "Exterior angle of a triangle", "The angle a triangle's side makes when extended past a corner.", []),
    ("triangle-inequality", "Triangle inequality", "Each side of a triangle stays shorter than the sum of the other two.", []),
    ("triangle-existence", "Triangle existence from three sides", "Whether three given lengths can close into a triangle at all.", []),
    ("side-angle-link", "Side and angle ranking", "Longer sides of a triangle always sit opposite larger angles.", []),
    ("similar-triangles", "Similar triangles", "Triangles with equal matching angles and proportional sides.", []),
    ("aa-criterion", "Angle-angle similarity", "Two matching angles are enough to prove two triangles similar.", []),
    ("scale-factor", "Scale factor", "One number multiplying every length of a shape to make a similar copy.", []),
    ("area-scale-square", "Squared area scale", "Lengths scaled by k give areas scaled by k squared.", []),
    ("volume-scale-cube", "Cubed volume scale", "Lengths scaled by k give volumes scaled by k cubed.", []),
    ("right-triangle", "Right triangle", "A triangle holding a 90 degree corner.", []),
    ("hypotenuse", "Hypotenuse", "The side of a right triangle opposite the right angle, always its longest.", []),
    ("pythagorean-relation", "Pythagorean relation", "In a right triangle the squared hypotenuse equals the sum of squared legs.", []),
    ("converse-pythagorean", "Converse Pythagorean test", "If the squared longest side equals the sum of squared others, the corner is right.", []),
    ("diameter", "Diameter of a circle", "A straight segment across a circle through its centre.", []),
    ("pi-constant", "Pi constant", "The ratio of every circle's circumference to its diameter, an irrational number near 3.1416.", []),
    ("circle-circumference", "Circle circumference", "The distance once around a circle, pi times its diameter.", []),
    ("circle-area", "Circle area", "The space inside a circle, pi times the squared radius.", []),
    ("central-angle", "Central angle", "An angle whose vertex sits at the circle's centre.", []),
    ("inscribed-angle", "Inscribed angle", "An angle whose vertex sits on the circle itself.", []),
    ("thales-triangle", "Triangle in a semicircle", "Any triangle whose base is a diameter and third corner sits on the circle is right-angled.", []),
    ("congruence-sas", "Side-angle-side congruence", "Two triangles matching in two sides and the angle between them are copies of each other.", []),
    ("triangle-rigidity", "Triangle rigidity", "A triangle fixed by its side lengths cannot change shape without changing a side.", []),
    ("quadrilateral-wobble", "Wobbly quadrilateral", "A four-sided frame with hinged corners can shear without any side changing length.", []),
    ("diagonal-brace", "Diagonal brace", "A strut joining opposite corners of a frame, dividing it into triangles.", []),
    ("angle-sum-quadrilateral", "Quadrilateral angle sum", "The inside angles of any flat four-sided figure add to 360 degrees.", []),
    ("polygon-interior-sum", "Polygon interior angle sum", "Inside angles of an n-sided flat polygon total n minus 2 times 180 degrees.", []),
    ("perpendicular-foot", "Perpendicular distance", "The shortest drop from a point to a line, meeting it at a right angle.", []),
    ("area-additivity", "Area additivity", "A shape's area equals the sum of the areas of its non-overlapping parts.", []),
    ("regular-tessellation", "Regular tessellation", "A repeating tiling by one kind of regular polygon meeting edge to edge.", []),
]

RELATIONS = [
    ("postulate-prereq-parallels", "parallel-postulate", "parallel-lines", "prerequisite", "The parallel postulate is a prerequisite for parallel lines staying everywhere equidistant and never meeting.", "the geometry stays on a flat plane", ""),
    ("transversal-causes-corresponding", "transversal", "corresponding-angles", "causes", "A transversal of parallels causes corresponding angles to come out equal.", "the two lines crossed are parallel", ""),
    ("transversal-causes-alternate", "transversal", "alternate-angles", "causes", "A transversal of parallels causes alternate interior angles to come out equal.", "the crossing line cuts two parallel lines", ""),
    ("corresponding-enables-aa", "corresponding-angles", "aa-criterion", "enables", "Equality of corresponding angles enables the angle-angle similarity test when two matching angles agree.", "two pairs of matching angles are known equal", ""),
    ("aa-enables-similar", "aa-criterion", "similar-triangles", "enables", "The angle-angle similarity criterion enables similar triangles to be proved without measuring any side.", "two angles of one triangle match two of the other", ""),
    ("similar-enables-scale", "similar-triangles", "scale-factor", "enables", "Pairing similar triangles enables a single scale factor to link every pair of matching sides.", "matching vertices are paired in order", ""),
    ("scale-causes-area", "scale-factor", "area-scale-square", "causes", "A scale factor causes squared area scale between similar figures.", "every length is multiplied by the same factor", ""),
    ("scale-causes-volume", "scale-factor", "volume-scale-cube", "causes", "A scale factor causes cubed volume scale between similar solids.", "all three dimensions grow by the same factor", ""),
    ("right-prereq-pythagoras", "right-triangle", "pythagorean-relation", "prerequisite", "A right triangle is a prerequisite for the Pythagorean relation to hold.", "the triangle lies in a flat plane", ""),
    ("pythagoras-predicts-hypotenuse", "pythagorean-relation", "hypotenuse", "predicts", "The Pythagorean relation predicts the hypotenuse from the two legs.", "the two shorter sides are known", ""),
    ("converse-predicts-right", "converse-pythagorean", "right-triangle", "predicts", "The converse Pythagorean test predicts a right triangle from the three sides alone.", "the longest side squared equals the other two squares summed", ""),
    ("diameter-causes-thales", "diameter", "thales-triangle", "causes", "A diameter of a circle causes the triangle in a semicircle to be right-angled.", "the third corner sits anywhere on the circle", ""),
    ("central-causes-inscribed", "central-angle", "inscribed-angle", "causes", "A central angle causes the inscribed angle on the same arc to be exactly half as large.", "both angles cut off the same arc", ""),
    ("anglesum-causes-exterior", "angle-sum-triangle", "exterior-angle", "causes", "The triangle angle sum causes the exterior angle of a triangle to equal the two remote interior angles.", "one side is extended past its corner", ""),
    ("anglesum-causes-quadsum", "angle-sum-triangle", "angle-sum-quadrilateral", "causes", "The triangle angle sum causes the quadrilateral angle sum of 360 degrees once a diagonal splits the shape.", "one diagonal divides the quadrilateral", ""),
    ("anglesum-causes-polygonsum", "angle-sum-triangle", "polygon-interior-sum", "causes", "The triangle angle sum causes the polygon interior angle sum by fan-splitting into triangles.", "the polygon has n sides and no dents", ""),
    ("pi-enables-circumference", "pi-constant", "circle-circumference", "enables", "The pi constant enables the circle circumference to be found from the diameter.", "the circle lies in a flat plane", ""),
    ("pi-enables-circlearea", "pi-constant", "circle-area", "enables", "The pi constant enables the circle area to be found from the radius.", "the radius is known", ""),
    ("sas-enables-rigidity", "congruence-sas", "triangle-rigidity", "enables", "Side-angle-side congruence enables triangle rigidity by fixing two sides and the angle joining them.", "two sides and the angle between them are fixed", ""),
    ("rigidity-inhibits-wobble", "triangle-rigidity", "quadrilateral-wobble", "inhibits", "Triangle rigidity inhibits wobbly quadrilateral shear once the frame is divided into triangles.", "a brace divides the frame into triangles", ""),
    ("brace-causes-rigidity", "diagonal-brace", "triangle-rigidity", "causes", "A diagonal brace causes triangle rigidity inside a four-sided frame.", "the brace runs between opposite corners", ""),
    ("brace-inhibits-wobble", "diagonal-brace", "quadrilateral-wobble", "inhibits", "A diagonal brace inhibits wobbly quadrilateral shear by converting it into two triangles.", "the corner joints hinge freely", ""),
    ("inequality-enables-existence", "triangle-inequality", "triangle-existence", "enables", "The triangle inequality enables triangle existence from three sides to be decided by length checks alone.", "no single length exceeds the sum of the other two", ""),
    ("ranking-predicts-hypotenuse", "side-angle-link", "hypotenuse", "predicts", "Side and angle ranking predicts the hypotenuse as the longest side of a right triangle.", "the right angle is the largest angle", ""),
    ("segment-enables-perpendicular", "straight-line-segment", "perpendicular-foot", "enables", "A straight line segment enables the perpendicular distance as the shortest drop from a point to a line.", "the foot meets the line at a right angle", ""),
    ("areaadd-enables-circle", "area-additivity", "circle-area", "enables", "Area additivity enables the circle area formula by rearranging fine sectors into a near-rectangle.", "the circle is cut into very fine sectors", ""),
    ("anglesum-prereq-aa", "angle-sum-triangle", "aa-criterion", "prerequisite", "The triangle angle sum is a prerequisite for the angle-angle similarity test, since the third angle follows from the other two.", "two of the three angles are known", ""),
    ("parallels-prereq-corresponding", "parallel-lines", "corresponding-angles", "prerequisite", "A pair of parallel lines is a prerequisite for equal corresponding angles at a transversal.", "a third line crosses both parallels", ""),
    ("alternate-enables-parallels", "alternate-angles", "parallel-lines", "enables", "A pair of equal alternate interior angles enables proving parallel lines from one transversal.", "one transversal gives equal alternate interior angles", ""),
    ("polysum-enables-tessellation", "polygon-interior-sum", "regular-tessellation", "enables", "The polygon interior angle sum enables the regular tessellation test by checking whole numbers of corners around a point.", "copies meet edge to edge around one point", ""),
    ("pythagoras-predicts-diagonal", "pythagorean-relation", "straight-line-segment", "predicts", "The Pythagorean relation predicts any straight line segment's length across a square grid.", "the segment's legs run along the grid axes", ""),
    ("anglesum-prevents-three-rights", "angle-sum-triangle", "right-triangle", "prevents", "The triangle angle sum prevents a right triangle from carrying two more right angles.", "the triangle is drawn on a flat sheet", ""),
    ("postulate-enables-anglesum", "parallel-postulate", "angle-sum-triangle", "enables", "The parallel postulate enables the triangle angle sum of 180 degrees.", "the geometry is Euclidean", ""),
    ("scale-inhibits-anglechange", "scale-factor", "angle-sum-triangle", "inhibits", "A uniform scale factor inhibits any change to the triangle angle sum under scaling.", "the scaling is uniform in every direction", ""),
    ("inscribed-enables-thales", "inscribed-angle", "thales-triangle", "enables", "An inscribed angle standing on a half-circle arc enables the triangle in a semicircle proof.", "the arc it stands on is a half circle", ""),
    ("central-enables-pi", "central-angle", "pi-constant", "enables", "A central angle of a full turn enables the pi constant to be defined as circumference over diameter.", "the full turn is taken as 360 degrees", ""),
    ("segment-enables-inequality", "straight-line-segment", "triangle-inequality", "enables", "A straight line segment enables the triangle inequality, since the direct path can never be longer than a detour.", "the detour passes through a third point", ""),
    ("pythagoras-enables-converse", "pythagorean-relation", "converse-pythagorean", "enables", "The Pythagorean relation enables the converse Pythagorean test once both directions are proved.", "the equivalence is checked both ways", ""),
    ("rectarea-prereq-additivity", "area-additivity", "regular-tessellation", "enables", "Area additivity enables regular tessellation area checks by summing identical tiles.", "tiles do not overlap and leave no gaps", ""),
    ("hypotenuse-prereq-thales", "hypotenuse", "thales-triangle", "prerequisite", "A hypotenuse spanning the diameter is a prerequisite for the triangle in a semicircle being right-angled.", "both ends of the hypotenuse sit on the circle", ""),
]

MYTHS = [
    ("pythagoras-all-triangles", "The Pythagorean rule holds for every triangle",
     "The relation holds only for right triangles; in other triangles the squares of two sides need not match the third.", "pythagorean-relation"),
    ("pi-equals-22-7", "Pi is exactly 22 over 7",
     "Pi is irrational, close to but never equal to any simple fraction.", "pi-constant"),
    ("triangle-180-always", "Every triangle's angles sum to 180 degrees",
     "Only flat-plane triangles sum to 180 degrees; on a sphere they sum to more, on a saddle to less.", "angle-sum-triangle"),
    ("area-doubles-with-sides", "Doubling every side doubles the area",
     "Doubling every length multiplies area by four and volume by eight.", "area-scale-square"),
    ("circles-grow-pi", "Bigger circles have bigger pi",
     "The ratio stays the same for every circle regardless of size.", "pi-constant"),
]

BOUNDARIES = [
    ("non-euclidean-bounds", "Curved surfaces change angle sums",
     "On curved surfaces the parallel postulate fails and triangle angle sums leave 180 degrees.", "angle-sum-triangle"),
    ("similarity-limits", "Similarity fixes shape, not size",
     "Scale factors preserve angles while changing lengths, areas and volumes by their powers.", "scale-factor"),
    ("compass-limits", "Classical tools cannot square the circle",
     "With compass and straightedge alone, a square equal in area to a circle cannot be constructed.", "circle-area"),
]

EXAMPLES = [
    ("ladder-wall", "A ladder against a wall",
     "Ladder, wall and ground form a right triangle whose three lengths must satisfy the Pythagorean relation.",
     ["right-triangle", "pythagorean-relation", "hypotenuse"]),
    ("shadow-height", "Measuring a tree from its shadow",
     "Tree and shadow form triangles similar to a stick and its shadow, so the height follows from one scale factor.",
     ["similar-triangles", "scale-factor", "aa-criterion"]),
    ("shelf-brace", "Bracing a wobbly shelf",
     "A diagonal brace turns a wobbly four-sided shelf into two rigid triangles that cannot shear.",
     ["diagonal-brace", "quadrilateral-wobble", "triangle-rigidity"]),
    ("fence-around-pond", "Fencing around a circular pond",
     "The fence length for a round pond follows the circumference from the diameter through pi.",
     ["circle-circumference", "pi-constant", "diameter"]),
]

CONTROLS = [
    ("pythagoras-obtuse", "The Pythagorean relation holds for obtuse triangles",
     "The Pythagorean relation must not be treated as holding for triangles without a right angle."),
    ("pi-shrinks-circle", "A smaller circle has a smaller pi",
     "Pi must not be treated as varying from circle to circle."),
    ("brace-proves-postulate", "A diagonal brace proves the parallel postulate",
     "A diagonal brace must not be treated as establishing the axioms of the plane."),
    ("scaling-changes-angles", "Scaling a figure changes its angles",
     "Uniform scaling must not be treated as altering any angle of a figure."),
]
