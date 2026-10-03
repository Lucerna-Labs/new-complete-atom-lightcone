"""Abstract algebra causation: groups, subgroups, homomorphisms, rings, fields, vector spaces."""

WORLD = "algebra-causation-v0"
PREFIX = "alg"
DOMAIN = "formal-mathematics"
SUBJECT = "formal-mathematics.abstract-algebra"
SOURCES = ["mathlib4"]
SCOPE = "High-level algebra: group axioms and their consequences, subgroups and Lagrange counting, homomorphisms and kernels, rings, fields, vector spaces, symmetry groups"
ROOT_LABEL = "Algebra causation world"
ROOT_STATEMENT = 'Root of the algebra causation world: how algebraic hypotheses predict structural consequences and enable quotient and coordinate constructions.'

CONCEPTS = [
    ('group-axioms', 'Group axioms', 'Closure, associativity, an identity and inverses for one operation on a set.', []),
    ('identity-element', 'Identity element', 'The member that leaves every other unchanged under the operation.', []),
    ('inverse-element', 'Inverse element', 'For g in a group, an element h with gh = hg = e, where e is the identity.', []),
    ('associativity', 'Associativity of the operation', 'Grouping does not change a product of three or more elements.', []),
    ('abelian-group', 'Abelian group', 'A group whose operation also commutes for every pair.', []),
    ('commutativity', 'Commutativity', 'Swapping the order of two elements leaves the result the same.', []),
    ('subgroup', 'Subgroup', 'A subset that is itself a group under the same operation.', []),
    ('cyclic-group', 'Cyclic group', 'A group made of the powers of one element.', []),
    ('generator', 'Group generator', 'An element whose integer powers, including negative powers when needed, generate every group element.', []),
    ('element-order', 'Order of an element', 'The least positive n with g^n = e, or infinite order if no such n exists.', []),
    ('lagrange-theorem', 'Lagrange theorem on subgroups', "A finite group's order is a multiple of each subgroup's order.", []),
    ('coset', 'Cosets of a subgroup', 'The translated copies of a subgroup that tile the group.', []),
    ('normal-subgroup', 'Normal subgroup', 'A subgroup H of G satisfying gHg^(-1) = H for every g in G.', []),
    ('quotient-group', 'Quotient group', 'The group whose elements are the cosets of a normal subgroup.', []),
    ('group-homomorphism', 'Group homomorphism', 'A map between groups that respects the operation.', []),
    ('kernel', 'Kernel of a homomorphism', "The members a homomorphism sends to the target's identity.", []),
    ('isomorphism', 'Group isomorphism', 'A bijective homomorphism, so both groups are the same structure renamed.', []),
    ('ring-axioms', 'Ring axioms', 'Addition is an abelian group operation; multiplication is associative with identity and distributes over addition.', []),
    ('field-axioms', 'Field axioms', 'A commutative ring in which every nonzero element has a multiplicative inverse and 1 != 0.', []),
    ('multiplicative-inverse', 'Multiplicative inverse', 'For an element a of a unital ring, an element b with ab = ba = 1; it exists exactly when a is a unit.', []),
    ('zero-divisor', 'Zero divisor', 'A nonzero element that multiplies with another nonzero to give zero.', []),
    ('integral-domain', 'Integral domain', 'A commutative ring with identity 1 != 0 and no nonzero zero divisors.', []),
    ('polynomial-ring', 'Polynomial ring', 'Expressions in an unknown with coefficients from a ring, added and multiplied formally.', []),
    ('vector-space', 'Vector space', "Vectors scaled by a field's elements and added together.", []),
    ('linear-map', 'Linear map', 'A function between vector spaces preserving addition and scaling.', []),
    ('basis', 'Basis of a vector space', 'A linearly independent spanning set over the scalar field.', []),
    ('dimension', 'Dimension of a space', 'The number of vectors in any basis.', []),
    ('symmetric-group', 'Symmetric group', 'All rearrangements of a finite set under composition.', []),
    ('permutation', 'Permutation of elements', "One rearrangement of a set's members.", []),
    ('group-action', 'Group action on a set', "A group moving a set's elements around consistently.", []),
    ('dihedral-symmetry', 'Dihedral symmetry of a square', 'The eight flips and rotations preserving a square.', []),
    ('modular-arithmetic', 'Modular arithmetic', 'Arithmetic that wraps around a fixed modulus like a clock.', []),
    ('fermat-little', 'Fermat little theorem', 'If p is prime and p does not divide the integer a, then p divides a^(p-1) - 1.', []),
]

RELATIONS = [
    ('cyclic-predicts-subgroups', 'cyclic-group', 'subgroup', 'predicts', 'A cyclic group predicts exactly one subgroup of each order d dividing its order n.', 'G is a finite cyclic group of order n >= 1 and d is a positive divisor of n', ''),
    ('lagrange-predicts-subgroups', 'lagrange-theorem', 'subgroup', 'predicts', 'The Lagrange theorem on subgroups predicts that the order of a subgroup divides the ambient group order.', 'H is a subgroup of a finite group G; this statement does not assert a subgroup for every divisor', ''),
    ('cosets-enable-lagrange', 'coset', 'lagrange-theorem', 'enables', 'Partitioning by equal-sized cosets of a subgroup enables a counting proof of the Lagrange theorem on subgroups.', 'G is finite and the distinct left cosets of H partition G, each with |H| elements', ''),
    ('normal-enables-quotient', 'normal-subgroup', 'quotient-group', 'enables', 'A normal subgroup enables a quotient group with well-defined multiplication (gH)(kH) = (gk)H.', 'H is normal in a group G and multiplication on G/H is induced from G', ''),
    ('homomorphism-predicts-image-subgroup', 'group-homomorphism', 'subgroup', 'predicts', 'A group homomorphism predicts that its image is a subgroup of its codomain.', 'phi maps a group G to a group K and preserves their binary operations', ''),
    ('kernel-predicts-injective', 'kernel', 'group-homomorphism', 'predicts', 'A trivial kernel of a homomorphism predicts an injective group homomorphism.', 'phi:G->K is a group homomorphism and ker(phi) = {e_G}', ''),
    ('kernel-predicts-normal', 'kernel', 'normal-subgroup', 'predicts', 'The kernel of a homomorphism predicts a normal subgroup of the domain.', 'phi:G->K preserves group multiplication and ker(phi) is the preimage of e_K', ''),
    ('isomorphism-predicts-order', 'isomorphism', 'element-order', 'predicts', 'A group isomorphism predicts preservation of the order of an element.', 'phi:G->K is a bijective group homomorphism and g belongs to G, including the infinite-order case', ''),
    ('zero-divisor-prevents-field', 'zero-divisor', 'field-axioms', 'prevents', 'A zero divisor prevents field axioms from holding for the same ring operations.', 'a and b are nonzero elements of a unital commutative ring and ab = 0', ''),
    ('field-predicts-domain', 'field-axioms', 'integral-domain', 'predicts', 'Satisfying field axioms predicts that the underlying commutative ring is an integral domain.', 'F is a field with 1 != 0, so multiplying ab = 0 by a nonzero a inverse forces b = 0', ''),
    ('coefficients-enable-polyring', 'ring-axioms', 'polynomial-ring', 'enables', 'Satisfying ring axioms enables a polynomial ring construction with coefficientwise addition and convolution multiplication.', 'R is a unital commutative ring and polynomials in one indeterminate have finite coefficient support', ''),
    ('basis-predicts-coordinates', 'basis', 'vector-space', 'predicts', 'A basis of a vector space predicts a unique finite linear-combination representation for every vector space element.', 'B is a linearly independent spanning set of a vector space V over a fixed field F', ''),
    ('linearmap-predicts-image-space', 'linear-map', 'vector-space', 'predicts', 'A linear map predicts that its image is a vector space under the codomain operations.', 'T:V->W is linear over one field F and its image inherits addition and scalar multiplication from W', ''),
    ('action-enables-embedding', 'group-action', 'symmetric-group', 'enables', 'A group action on a set enables an injective homomorphism into its symmetric group when the action is faithful.', 'G acts faithfully on a finite set X: only e_G fixes every point of X', ''),
    ('square-moves-enable-action', 'dihedral-symmetry', 'group-action', 'enables', 'Dihedral symmetry of a square enables a faithful group action on a set of its four vertices.', 'the eight Euclidean isometries preserving a nondegenerate square act by their vertex permutations', ''),
    ('modular-predicts-cyclic', 'modular-arithmetic', 'cyclic-group', 'predicts', 'Modular arithmetic predicts a cyclic group of n residues under addition, generated by the residue of 1.', 'n is a positive integer and addition is the induced operation on Z/nZ', ''),
    ('lagrange-predicts-fermat', 'lagrange-theorem', 'fermat-little', 'predicts', 'The Lagrange theorem on subgroups predicts Fermat little theorem by applying element-order divisibility to the nonzero residues.', 'p is prime, a is an integer, p does not divide a, and (Z/pZ)^* has order p-1', ''),
    ('modular-predicts-abelian', 'modular-arithmetic', 'abelian-group', 'predicts', 'Modular arithmetic predicts an abelian group under addition of residues.', 'n >= 1 is an integer and residues modulo n inherit the commutative addition of integers', ''),
    ('homomorphism-enables-quotient', 'group-homomorphism', 'quotient-group', 'enables', 'A group homomorphism enables a quotient group by its kernel that is isomorphic to its image.', 'phi:G->K is a group homomorphism and the quotient uses ker(phi), not an arbitrary subgroup', ''),
    ('identity-prereq-inverse', 'identity-element', 'inverse-element', 'prerequisite', 'An identity element is a prerequisite for an inverse element relative to the given operation.', 'in a monoid the chosen identity e is used in both equations gh = hg = e', ''),
    ('subgroup-shares-identity', 'identity-element', 'subgroup', 'prerequisite', 'The ambient identity element is a prerequisite for a subgroup under the inherited operation.', 'H is a subset of a group G and must contain e_G to qualify as a subgroup of G', ''),
    ('dimension-predicts-isomorphism', 'dimension', 'vector-space', 'predicts', 'The dimension of a space predicts the isomorphism class of a vector space over a fixed field.', 'V and W are finite-dimensional vector spaces over the same field F and dim_F(V) = dim_F(W)', ''),
    ('cycles-predict-order', 'permutation', 'element-order', 'predicts', 'A permutation of elements predicts an order of an element equal to the least common multiple of its disjoint cycle lengths.', 'the permutation acts on a finite nonempty set; fixed points count as length-one cycles', ''),
    ('field-enables-vectorspace', 'field-axioms', 'vector-space', 'enables', 'Satisfying field axioms enables a vector space of n-tuples with coordinatewise operations.', 'F is a field, n is a nonnegative integer, and scalars act coordinatewise on F^n', ''),
    ('lagrange-predicts-order', 'lagrange-theorem', 'element-order', 'predicts', 'The Lagrange theorem on subgroups predicts that the order of an element divides the group order.', 'g belongs to a finite group G and the subgroup generated by g has order ord(g)', ''),
    ('abelian-predicts-normal', 'abelian-group', 'normal-subgroup', 'predicts', 'An abelian group predicts that each of its subgroups is a normal subgroup.', 'H is any subgroup of an abelian group G, so ghg^(-1) = h for g in G and h in H', ''),
]

MYTHS = [
    ('algebra-is-equations', 'Abstract algebra is just solving equations', 'The subject studies structure itself, treating groups, rings and fields as objects.', 'group-axioms'),
    ('every-nonzero-divides', 'Every nonzero element can divide in any ring', 'Fields guarantee inverses for every nonzero element; a general commutative ring may have nonunits even without zero divisors, as 2 in Z shows.', 'zero-divisor'),
    ('any-subset-subgroup', 'Any subset makes a subgroup', 'A subgroup is nonempty and closed under products and inverses; associativity is inherited from the ambient group.', 'subgroup'),
    ('all-groups-commute', 'All groups commute', 'The permutation group on three or more elements is noncommutative; commutativity is an extra hypothesis.', 'commutativity'),
    ('lagrange-converse-holds', "Lagrange's converse always holds", 'A divisor of the group order need not host a subgroup of that size in every finite group.', 'lagrange-theorem'),
]

BOUNDARIES = [
    ('finite-groups-only', 'Lagrange speaks to finite groups', 'The integer divisibility conclusion assumes finite G; for an infinite group, coset index still exists but this finite counting statement does not apply.', 'lagrange-theorem'),
    ('isomorphism-ignores-labels', 'Isomorphism ignores labels only', 'Isomorphic groups match in structure while element names may differ freely.', 'isomorphism'),
    ('vector-needs-field', 'Vector spaces assume a field', 'Over rings instead of fields, the same construction is a module and behaves differently.', 'vector-space'),
    ('ring-inverses-not-guaranteed', 'Ring axioms do not make every nonzero element a unit', 'Ring axioms alone do not guarantee a multiplicative inverse for every nonzero element; in Z the units are 1 and -1 while 2 is not invertible.', 'multiplicative-inverse'),
    ('unfaithful-action', 'An action can identify distinct group elements', 'An action on a finite set gives a homomorphism into its symmetric group, but a nontrivial action kernel prevents that homomorphism from being an embedding.', 'group-action'),
]

EXAMPLES = [
    ('clock-arithmetic', 'Clock arithmetic', 'Addition modulo 12 forms a cyclic group generated by 1; its unique subgroup of order 3 is {0, 4, 8}.', ['modular-arithmetic', 'cyclic-group', 'subgroup']),
    ('disjoint-cycles', 'Two disjoint cycles', 'In S_5 the permutation (1 2)(3 4 5) has order lcm(2,3) = 6, rather than 2, 3, or their sum.', ['permutation', 'element-order', 'symmetric-group']),
    ('card-checksum', 'A toy weighted modulo-10 checksum', 'For a toy checksum with data digits 3 and 4 and weights 1 and 2, the weighted sum is 11; a check digit 9 makes the total 20, zero modulo 10, without using Fermat little theorem.', ['modular-arithmetic', 'abelian-group']),
    ('square-vertices', 'A square acts on its vertices', 'The eight rigid symmetries of a square give eight distinct permutations of its four vertices, so this action embeds D_4 into S_4.', ['group-action', 'dihedral-symmetry', 'symmetric-group']),
    ('trivial-action', 'A group action that is not an embedding', 'Let C_2 act on a singleton by fixing it; both group elements induce the identity permutation, so the action is not faithful.', ['group-action', 'symmetric-group', 'kernel']),
]

CONTROLS = [
    ('zero-invertible', 'Zero has a multiplicative inverse', 'Zero must not be treated as invertible in a field.'),
    ('redundant-basis', 'A basis may contain dependent vectors', 'A basis of a vector space must not be treated as containing dependent vectors.'),
    ('kernel-any-subset', 'A kernel can be any subset', 'The kernel of a homomorphism must not be treated as an arbitrary subset.'),
    ('isomorphism-resizes', 'Isomorphic groups can differ in size', 'A group isomorphism must not be treated as relating groups of different sizes.'),
    ('cycle-order-sum', 'Permutation order adds cycle lengths', 'Disjoint cycle lengths 2 and 3 must not be treated as giving permutation order 5.'),
    ('action-always-embeds', 'Every action gives an embedding', 'A group action with a nontrivial kernel must not be treated as an injective permutation representation.'),
]
