"""Abstract algebra causation: groups, subgroups, homomorphisms, rings, fields, vector spaces."""

WORLD = "algebra-causation-v0"
PREFIX = "alg"
DOMAIN = "formal-mathematics"
SUBJECT = "formal-mathematics.abstract-algebra"
SOURCES = ["mathlib4"]
SCOPE = "High-level algebra: group axioms and their consequences, subgroups and Lagrange counting, homomorphisms and kernels, rings, fields, vector spaces, symmetry groups"
ROOT_LABEL = "Algebra causation world"
ROOT_STATEMENT = "Root of the algebra causation world: how a few axioms about operations cause the structure of groups, rings, fields and vector spaces."

CONCEPTS = [
    ("group-axioms", "Group axioms", "Closure, associativity, an identity and inverses for one operation on a set.", []),
    ("identity-element", "Identity element", "The member that leaves every other unchanged under the operation.", []),
    ("inverse-element", "Inverse element", "The partner that returns any member to the identity.", []),
    ("associativity", "Associativity of the operation", "Grouping does not change a product of three or more elements.", []),
    ("abelian-group", "Abelian group", "A group whose operation also commutes for every pair.", []),
    ("commutativity", "Commutativity", "Swapping the order of two elements leaves the result the same.", []),
    ("subgroup", "Subgroup", "A subset that is itself a group under the same operation.", []),
    ("cyclic-group", "Cyclic group", "A group made of the powers of one element.", []),
    ("generator", "Group generator", "An element whose repeated operation reaches every member.", []),
    ("element-order", "Order of an element", "How many repetitions return an element to the identity.", []),
    ("lagrange-theorem", "Lagrange theorem on subgroups", "A finite group's order is a multiple of each subgroup's order.", []),
    ("coset", "Cosets of a subgroup", "The translated copies of a subgroup that tile the group.", []),
    ("normal-subgroup", "Normal subgroup", "A subgroup unchanged by conjugation, so its cosets carry an operation.", []),
    ("quotient-group", "Quotient group", "The group whose elements are the cosets of a normal subgroup.", []),
    ("group-homomorphism", "Group homomorphism", "A map between groups that respects the operation.", []),
    ("kernel", "Kernel of a homomorphism", "The members a homomorphism sends to the target's identity.", []),
    ("isomorphism", "Group isomorphism", "A bijective homomorphism, so both groups are the same structure renamed.", []),
    ("ring-axioms", "Ring axioms", "A set with addition and multiplication tied by distributivity.", []),
    ("field-axioms", "Field axioms", "A commutative ring where every nonzero element divides.", []),
    ("multiplicative-inverse", "Multiplicative inverse", "The partner multiplying any nonzero element to one.", []),
    ("zero-divisor", "Zero divisor", "A nonzero element that multiplies with another nonzero to give zero.", []),
    ("integral-domain", "Integral domain", "A commutative ring with no zero divisors, so cancellation holds.", []),
    ("polynomial-ring", "Polynomial ring", "Expressions in an unknown with coefficients from a ring, added and multiplied formally.", []),
    ("vector-space", "Vector space", "Vectors scaled by a field's elements and added together.", []),
    ("linear-map", "Linear map", "A function between vector spaces preserving addition and scaling.", []),
    ("basis", "Basis of a vector space", "An independent spanning set giving every vector unique coordinates.", []),
    ("dimension", "Dimension of a space", "The number of vectors in any basis.", []),
    ("symmetric-group", "Symmetric group", "All rearrangements of a finite set under composition.", []),
    ("permutation", "Permutation of elements", "One rearrangement of a set's members.", []),
    ("group-action", "Group action on a set", "A group moving a set's elements around consistently.", []),
    ("dihedral-symmetry", "Dihedral symmetry of a square", "The eight flips and rotations preserving a square.", []),
    ("modular-arithmetic", "Modular arithmetic", "Arithmetic that wraps around a fixed modulus like a clock.", []),
    ("fermat-little", "Fermat little theorem", "For prime p, any a not divisible by p gives a to the p minus a divisible by p.", []),
]

RELATIONS = [
    ("axioms-enable-identity", "group-axioms", "identity-element", "enables", "Satisfying the group axioms enables an identity element to work for every member.", "the set with its operation forms a group", ""),
    ("axioms-enable-inverse", "group-axioms", "inverse-element", "enables", "Satisfying the group axioms enables an inverse element for every member.", "every element can be undone", ""),
    ("associativity-enables-axioms", "associativity", "group-axioms", "enables", "Associativity of the operation enables the group axioms to allow free regrouping of products.", "products of three or more elements are formed", ""),
    ("commutativity-causes-abelian", "commutativity", "abelian-group", "causes", "Commutativity causes the abelian group structure.", "every pair of elements swaps in the product", ""),
    ("generator-causes-cyclic", "generator", "cyclic-group", "causes", "A single group generator causes a cyclic group of its powers.", "one element reaches every other by repetition", ""),
    ("cyclic-enables-order", "cyclic-group", "element-order", "enables", "A finite cyclic group enables the order of an element to divide the group size.", "the cyclic group has finite size n", ""),
    ("lagrange-predicts-subgroups", "lagrange-theorem", "subgroup", "predicts", "The Lagrange theorem on subgroups predicts each subgroup size dividing the group size.", "the ambient group is finite", ""),
    ("cosets-enable-lagrange", "coset", "lagrange-theorem", "enables", "Tiling by equal cosets of a subgroup enables the Lagrange theorem on subgroups to count.", "the cosets tile the group exactly", ""),
    ("normal-enables-quotient", "normal-subgroup", "quotient-group", "enables", "A normal subgroup enables a quotient group on its cosets.", "left and right cosets coincide", ""),
    ("homomorphism-transports-axioms", "group-homomorphism", "group-axioms", "enables", "A group homomorphism enables the group axioms to carry across to the image.", "the map respects the operation", ""),
    ("kernel-predicts-injective", "kernel", "group-homomorphism", "predicts", "A trivial kernel of a homomorphism predicts that the group homomorphism is injective.", "the kernel contains only the identity", ""),
    ("kernel-causes-normal", "kernel", "normal-subgroup", "causes", "The kernel of a homomorphism causes a normal subgroup to appear automatically.", "the homomorphism is fixed", ""),
    ("isomorphism-predicts-sameness", "isomorphism", "group-axioms", "predicts", "A group isomorphism predicts the same group axioms consequences on both sides.", "the two groups are compared element to element", ""),
    ("ring-enables-additive-group", "ring-axioms", "group-axioms", "enables", "Satisfying ring axioms enables the group axioms for addition inside the ring.", "both operations are present", ""),
    ("field-enables-inverse", "field-axioms", "multiplicative-inverse", "enables", "Satisfying field axioms enables a multiplicative inverse for every nonzero element.", "the element is not zero", ""),
    ("zero-divisor-prevents-field", "zero-divisor", "field-axioms", "prevents", "A nonzero zero divisor prevents field axioms from holding.", "two nonzero elements multiply to zero", ""),
    ("domain-prevents-zerodivisor", "integral-domain", "zero-divisor", "prevents", "An integral domain prevents a nonzero zero divisor from existing.", "the ring is commutative with identity", ""),
    ("field-causes-domain", "field-axioms", "integral-domain", "causes", "Satisfying field axioms causes an integral domain because inverses block zero divisors.", "every nonzero element is invertible", ""),
    ("coefficients-enable-polyring", "ring-axioms", "polynomial-ring", "enables", "Having ring axioms on the coefficients enables the polynomial ring to form.", "coefficients come from one ring", ""),
    ("basis-enables-coordinates", "basis", "vector-space", "enables", "A basis of a vector space enables every vector space member to get unique coordinates.", "the spanning set is linearly independent", ""),
    ("basis-predicts-dimension", "basis", "dimension", "predicts", "The size of a basis of a vector space predicts the dimension of a space.", "any two bases are compared", ""),
    ("linearmap-preserves-structure", "linear-map", "vector-space", "enables", "A linear map enables the vector space structure to survive the mapping.", "addition and scaling are respected", ""),
    ("permutations-cause-symmetric", "permutation", "symmetric-group", "causes", "The family of every permutation of elements causes the symmetric group under composition.", "all rearrangements are included", ""),
    ("action-enables-embedding", "group-action", "symmetric-group", "enables", "A group action on a set enables an embedding into a symmetric group.", "the set is finite", ""),
    ("square-moves-cause-dihedral", "dihedral-symmetry", "group-action", "causes", "The dihedral symmetry of a square causes a group action on a set of four corners.", "only square-preserving moves are allowed", ""),
    ("modular-causes-cyclic", "modular-arithmetic", "cyclic-group", "causes", "Clock-face modular arithmetic causes a cyclic group of residues.", "addition wraps at the modulus", ""),
    ("lagrange-enables-fermat", "lagrange-theorem", "fermat-little", "enables", "The Lagrange theorem on subgroups enables Fermat little theorem for prime moduli.", "the modulus is prime", ""),
    ("modular-causes-abelian", "modular-arithmetic", "abelian-group", "causes", "Modular arithmetic causes an abelian group under addition of residues.", "addition is taken mod n", ""),
    ("homomorphism-enables-quotient", "group-homomorphism", "quotient-group", "enables", "Every group homomorphism enables a quotient group by its kernel.", "the kernel is taken as the subgroup", ""),
    ("inverse-enables-identity", "inverse-element", "identity-element", "enables", "An inverse element enables a product to return to the identity element.", "the element is multiplied by its inverse", ""),
    ("subgroup-shares-identity", "subgroup", "identity-element", "prerequisite", "Sharing the identity element is a prerequisite for a subgroup to qualify.", "the subset is tested for membership", ""),
    ("vectorspace-enables-linearmap", "vector-space", "linear-map", "enables", "A vector space enables a linear map to be defined between such spaces.", "both domain and target are vector spaces", ""),
    ("dimension-predicts-isomorphism", "dimension", "vector-space", "predicts", "The dimension of a space predicts the vector space up to isomorphism.", "the field is fixed and the space is finite-dimensional", ""),
    ("cycles-cause-order", "permutation", "element-order", "causes", "Repeating a permutation of elements causes the order of an element to appear as its cycle lengths.", "the permutation decomposes into cycles", ""),
    ("generator-causes-subgroup", "generator", "subgroup", "causes", "One group generator causes a subgroup made of its powers.", "only the generated powers are kept", ""),
    ("field-enables-vectorspace", "field-axioms", "vector-space", "enables", "A set of field axioms enables a vector space of tuples over the field.", "scalars come from the field", ""),
    ("lagrange-predicts-order", "lagrange-theorem", "element-order", "predicts", "The Lagrange theorem on subgroups predicts the order of an element dividing the group size.", "the element sits in a finite group", ""),
    ("cosets-prereq-quotient", "coset", "quotient-group", "prerequisite", "The family of cosets of a subgroup is a prerequisite for a quotient group to be built.", "the cosets carry an operation", ""),
    ("abelian-causes-normal", "abelian-group", "normal-subgroup", "causes", "An abelian group causes every subgroup to be a normal subgroup.", "the ambient group operation commutes", ""),
    ("ring-prevents-guaranteed-inverse", "ring-axioms", "multiplicative-inverse", "prevents", "Relying on bare ring axioms prevents a guaranteed multiplicative inverse for every nonzero element.", "no division is assumed beyond the axioms", ""),
    ("homomorphism-prereq-kernel", "group-homomorphism", "kernel", "prerequisite", "A group homomorphism is a prerequisite for a kernel of a homomorphism to exist.", "the map is fixed between groups", ""),
]

MYTHS = [
    ("algebra-is-equations", "Abstract algebra is just solving equations",
     "The subject studies structure itself, treating groups, rings and fields as objects.", "group-axioms"),
    ("every-nonzero-divides", "Every nonzero element can divide in any ring",
     "Only fields guarantee inverses; general rings may host zero divisors.", "zero-divisor"),
    ("any-subset-subgroup", "Any subset makes a subgroup",
     "A subgroup must itself satisfy closure, identity and inverses.", "subgroup"),
    ("all-groups-commute", "All groups commute",
     "Most natural groups, such as permutations of elements, do not commute.", "commutativity"),
    ("lagrange-converse-holds", "Lagrange's converse always holds",
     "A divisor of the group order need not host a subgroup of that size in every finite group.", "lagrange-theorem"),
]

BOUNDARIES = [
    ("finite-groups-only", "Lagrange speaks to finite groups",
     "The dividing argument is stated for finite groups; infinite groups need other tools.", "lagrange-theorem"),
    ("isomorphism-ignores-labels", "Isomorphism ignores labels only",
     "Isomorphic groups match in structure while element names may differ freely.", "isomorphism"),
    ("vector-needs-field", "Vector spaces assume a field",
     "Over rings instead of fields, the same construction is a module and behaves differently.", "vector-space"),
]

EXAMPLES = [
    ("clock-arithmetic", "Clock arithmetic",
     "Hours wrap by modular arithmetic into a small cyclic group.",
     ["modular-arithmetic", "cyclic-group", "abelian-group"]),
    ("rubik-cube", "A Rubik cube as a group",
     "Every legal twist is a permutation of elements inside a huge generated subgroup.",
     ["permutation", "generator", "subgroup"]),
    ("card-checksum", "Card checksums from modular math",
     "The check digit comes from modular arithmetic weighting of the digits.",
     ["modular-arithmetic", "fermat-little"]),
    ("wallpaper-symmetry", "Wallpaper patterns act on the plane",
     "Repeating decorations realise a group action on a set of points.",
     ["group-action", "dihedral-symmetry"]),
]

CONTROLS = [
    ("zero-invertible", "Zero has a multiplicative inverse",
     "Zero must not be treated as invertible in a field."),
    ("redundant-basis", "A basis may contain dependent vectors",
     "A basis of a vector space must not be treated as containing dependent vectors."),
    ("kernel-any-subset", "A kernel can be any subset",
     "The kernel of a homomorphism must not be treated as an arbitrary subset."),
    ("isomorphism-resizes", "Isomorphic groups can differ in size",
     "A group isomorphism must not be treated as relating groups of different sizes."),
]
