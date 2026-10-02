#!/usr/bin/env python3
"""Author formal mathematics, probability/statistics, and information theory."""

from __future__ import annotations

import json
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "math-probability-information" / "foundations.jsonl"
WORLD = "math-probability-information-v0"
MATH_LANES = ["reasoning.deductive", "thinking.bottom_up", "geometry.structural"]
PROB_LANES = ["reasoning.probabilistic", "reasoning.inductive", "reasoning.causal", "thinking.bottom_up"]
INFO_LANES = ["reasoning.probabilistic", "reasoning.deductive", "geometry.structural", "thinking.bottom_up"]
MATH_SOURCES = [
    "mathlib4", "open-logic-project", "hefferon-linear-algebra", "msc2020", "nist-dlmf",
    "lean4-theorem-proving",
]
PROB_SOURCES = ["nist-stat-handbook", "sep-probability", "msc2020"]
INFO_SOURCES = ["shannon-1948", "msc2020"]


MATH = [
    ("root", "Formal mathematical system", "Formal mathematics declares objects, operations, relations, axioms, definitions, inference rules, representations, domains, and proof obligations so conclusions follow from explicit premises rather than numerical resemblance.", "formal-mathematics.formal-proof"),
    ("natural", "Natural number", "Natural numbers form a discrete counting structure containing zero under the chosen convention and closed under successor, addition, and multiplication.", "formal-mathematics.arithmetic"),
    ("integer", "Integer", "Integers extend natural numbers with additive inverses and are closed under addition, subtraction, and multiplication.", "formal-mathematics.arithmetic"),
    ("rational", "Rational number", "A rational number is an equivalence class of integer fractions with nonzero denominator and supports exact field arithmetic.", "formal-mathematics.arithmetic"),
    ("real", "Real number", "Real numbers form a complete ordered field, adding limits needed to fill gaps in the rationals.", "formal-mathematics.arithmetic"),
    ("addition", "Addition", "Addition combines two numbers under a typed binary operation with identity zero and domain-specific closure.", "formal-mathematics.arithmetic"),
    ("subtraction", "Subtraction", "Subtraction adds the additive inverse and is not closed on natural numbers without an order condition.", "formal-mathematics.arithmetic"),
    ("multiplication", "Multiplication", "Multiplication is a binary operation with identity one and distributes over addition in rings and fields.", "formal-mathematics.arithmetic"),
    ("division", "Division", "Division by a nonzero number multiplies by its inverse in a field; division by zero is undefined.", "formal-mathematics.arithmetic"),
    ("fraction", "Fraction representation", "A fraction represents a rational value and equivalent numerator-denominator pairs denote the same value after nonzero common scaling.", "formal-mathematics.arithmetic"),
    ("decimal", "Decimal representation", "A positional decimal represents a rational exactly when terminating or repeating, while finite machine decimals may approximate real values.", "formal-mathematics.arithmetic"),
    ("percent", "Percent", "A percent represents a ratio per one hundred and requires a declared base quantity when converted to an amount or change.", "formal-mathematics.arithmetic"),
    ("unit", "Measurement unit", "A unit supplies the dimension and scale of a quantity; arithmetic on measured values must preserve dimensional compatibility.", "formal-mathematics.arithmetic"),
    ("order-operations", "Order of operations", "Expression grammar and precedence determine grouping, while parentheses explicitly override default grouping.", "formal-mathematics.arithmetic"),
    ("divisibility", "Divisibility", "An integer a divides b when an integer multiplier k satisfies b equals a times k.", "formal-mathematics.number-theory"),
    ("prime", "Prime number", "A prime is an integer greater than one whose positive divisors are only one and itself.", "formal-mathematics.number-theory"),
    ("gcd", "Greatest common divisor", "The greatest common divisor is the largest positive integer dividing each member of a nonzero integer pair or finite set.", "formal-mathematics.number-theory"),
    ("euclidean-algorithm", "Euclidean algorithm", "The Euclidean algorithm repeatedly replaces a pair by divisor and remainder until the last nonzero remainder gives their gcd.", "formal-mathematics.number-theory"),
    ("modular", "Modular congruence", "Integers are congruent modulo n when their difference is divisible by nonzero modulus n.", "formal-mathematics.number-theory"),
    ("fundamental-arithmetic", "Fundamental theorem of arithmetic", "Every integer greater than one factors into primes uniquely up to order.", "formal-mathematics.number-theory"),
    ("diophantine", "Diophantine equation", "A Diophantine equation seeks integer solutions to a polynomial relation and may have none, finitely many, or infinitely many solutions.", "formal-mathematics.number-theory"),
    ("variable", "Algebraic variable", "A variable is a symbol bound to an unknown, parameter, coordinate, or quantified value within a declared domain.", "formal-mathematics.elementary-algebra"),
    ("expression", "Algebraic expression", "An expression denotes a value from constants, variables, and operations under syntax and domain rules.", "formal-mathematics.elementary-algebra"),
    ("equation", "Equation", "An equation asserts equality of two expressions for all or selected variable assignments according to its quantification.", "formal-mathematics.elementary-algebra"),
    ("equivalent-equation", "Equivalent equation", "Two equations are equivalent over a domain when they have exactly the same solution set there.", "formal-mathematics.elementary-algebra"),
    ("linear-equation", "Linear equation", "A one-variable linear equation has the form ax plus b equals c with coefficients in a declared field and a nonzero for a unique solution.", "formal-mathematics.elementary-algebra"),
    ("inequality", "Inequality", "An inequality compares ordered expressions, and multiplying by a negative quantity reverses its order relation.", "formal-mathematics.elementary-algebra"),
    ("polynomial", "Polynomial", "A polynomial is a finite sum of coefficient-weighted nonnegative integer powers of variables over a coefficient ring.", "formal-mathematics.elementary-algebra"),
    ("factorization", "Polynomial factorization", "Factorization expresses a polynomial as a product and converts zero-finding into factor zero conditions over the chosen domain.", "formal-mathematics.elementary-algebra"),
    ("exponent", "Exponent law", "Exponent laws combine powers only under their stated base, exponent, sign, and domain conditions.", "formal-mathematics.elementary-algebra"),
    ("radical", "Radical", "A radical denotes a selected root and requires domain and branch conventions; squaring an equation can introduce extraneous solutions.", "formal-mathematics.elementary-algebra"),
    ("rational-expression", "Rational expression", "A rational expression is a quotient of polynomials whose domain excludes denominator zeros even if algebraic cancellation simplifies its formula.", "formal-mathematics.elementary-algebra"),
    ("function", "Function", "A function assigns exactly one codomain value to each element of its declared domain.", "formal-mathematics.elementary-algebra"),
    ("system-equations", "System of equations", "A system requires one assignment to satisfy every equation simultaneously and can be inconsistent, dependent, or uniquely determined.", "formal-mathematics.elementary-algebra"),
    ("word-quantity", "Word-problem quantity", "A word-problem quantity has meaning, value, unit, role, and relationships that must be identified before symbols are manipulated.", "formal-mathematics.algebra-word-problems"),
    ("word-unknown", "Word-problem unknown", "An unknown is the requested quantity represented by a variable with a declared unit and feasible domain.", "formal-mathematics.algebra-word-problems"),
    ("word-constraint", "Word-problem constraint", "A constraint translates a stated relation among quantities into an equation, inequality, or discrete condition without adding unstated assumptions.", "formal-mathematics.algebra-word-problems"),
    ("word-model", "Word-problem model", "A mathematical model selects variables and relations that preserve the problem's quantities, units, conditions, and requested output.", "formal-mathematics.algebra-word-problems"),
    ("word-solution-check", "Word-problem solution check", "A candidate is checked in the original wording for equations, units, bounds, integrality, and whether it answers the requested quantity.", "formal-mathematics.algebra-word-problems"),
    ("rate", "Rate relation", "A rate relates change in one quantity to change in another, so distance equals rate times time only under compatible units and the modeled constancy or averaging conditions.", "formal-mathematics.algebra-word-problems"),
    ("mixture", "Mixture relation", "A mixture balance conserves the amount of each tracked component across combined quantities under declared losses or reactions.", "formal-mathematics.algebra-word-problems"),
    ("work-rate", "Combined-work relation", "Combined independent work rates add when each rate is measured as completed task fraction per compatible time unit.", "formal-mathematics.algebra-word-problems"),
    ("percent-change", "Percent change", "Percent change divides signed change by the original nonzero base, so equal percentage increase and decrease do not cancel in amount.", "formal-mathematics.algebra-word-problems"),
    ("vector-space", "Vector space", "A vector space is an abelian additive group with scalar multiplication satisfying distributive, associative, and identity axioms over a field.", "formal-mathematics.linear-algebra"),
    ("lin-vector", "Vector", "A vector is an element of a vector space and need not be an ordered coordinate tuple until a basis is chosen.", "formal-mathematics.linear-algebra"),
    ("span", "Linear span", "The span of vectors is the set of all finite linear combinations and is the smallest subspace containing them.", "formal-mathematics.linear-algebra"),
    ("linear-independence", "Linear independence", "Vectors are linearly independent when only the zero coefficient combination equals the zero vector.", "formal-mathematics.linear-algebra"),
    ("basis", "Basis", "A basis is a linearly independent spanning set that gives each vector unique coordinates.", "formal-mathematics.linear-algebra"),
    ("lin-dimension", "Vector-space dimension", "Dimension is the cardinality of a basis, invariant across bases when the theorem's assumptions hold.", "formal-mathematics.linear-algebra"),
    ("linear-map", "Linear map", "A linear map preserves vector addition and scalar multiplication.", "formal-mathematics.linear-algebra"),
    ("matrix", "Matrix representation", "A matrix represents a linear map relative to chosen ordered bases and changes under basis changes while the map can remain fixed.", "formal-mathematics.linear-algebra"),
    ("kernel", "Linear-map kernel", "The kernel is the subspace mapped to zero and measures failure of injectivity.", "formal-mathematics.linear-algebra"),
    ("image", "Linear-map image", "The image is the subspace of reachable outputs and its dimension is the rank.", "formal-mathematics.linear-algebra"),
    ("rank-nullity", "Rank-nullity theorem", "For a linear map from a finite-dimensional space, domain dimension equals kernel dimension plus image dimension.", "formal-mathematics.linear-algebra"),
    ("determinant", "Determinant", "The determinant is an alternating multilinear volume scale that detects invertibility for square matrices.", "formal-mathematics.linear-algebra"),
    ("eigenvalue", "Eigenvalue and eigenvector", "A nonzero vector is an eigenvector when a linear operator scales it by an eigenvalue.", "formal-mathematics.linear-algebra"),
    ("inner-product", "Inner product", "An inner product supplies conjugate symmetry, linearity under convention, and positive definiteness, inducing norms and orthogonality.", "formal-mathematics.linear-algebra"),
    ("binary-operation", "Binary operation", "A binary operation maps an ordered pair of elements of a set to an element of that set.", "formal-mathematics.abstract-algebra"),
    ("semigroup", "Semigroup", "A semigroup is a set with an associative closed binary operation.", "formal-mathematics.abstract-algebra"),
    ("monoid", "Monoid", "A monoid is a semigroup with a two-sided identity element.", "formal-mathematics.abstract-algebra"),
    ("group", "Group", "A group is a monoid in which every element has a two-sided inverse.", "formal-mathematics.abstract-algebra"),
    ("subgroup", "Subgroup", "A subgroup is a subset closed under the inherited group operation and inverses and containing the identity.", "formal-mathematics.abstract-algebra"),
    ("homomorphism", "Algebraic homomorphism", "A homomorphism preserves the operations of the algebraic structures it connects.", "formal-mathematics.abstract-algebra"),
    ("quotient-group", "Quotient group", "A quotient group identifies elements by cosets of a normal subgroup so the induced operation is well defined.", "formal-mathematics.abstract-algebra"),
    ("ring", "Ring", "A ring has an abelian additive group and associative multiplication distributing over addition, with identity convention declared.", "formal-mathematics.abstract-algebra"),
    ("ideal", "Ring ideal", "An ideal is an additive subgroup absorbing multiplication by ring elements and supports quotient-ring construction.", "formal-mathematics.abstract-algebra"),
    ("field", "Field", "A field is a commutative ring in which every nonzero element has a multiplicative inverse.", "formal-mathematics.abstract-algebra"),
    ("limit", "Function limit", "A function limit L at a point means outputs approach L whenever domain inputs approach the point under quantified neighborhood conditions.", "formal-mathematics.calculus"),
    ("continuity", "Continuity", "A function is continuous at a point when its value is defined and equals its limit there.", "formal-mathematics.calculus"),
    ("derivative", "Derivative", "The derivative is the limit of a difference quotient and gives the best local linear rate where it exists.", "formal-mathematics.calculus"),
    ("product-rule", "Product rule", "The derivative of a product equals the first derivative times the second plus the first times the second derivative where both are differentiable.", "formal-mathematics.calculus"),
    ("chain-rule", "Chain rule", "The derivative of a composition is the outer derivative evaluated at the inner value multiplied by the inner derivative under differentiability assumptions.", "formal-mathematics.calculus"),
    ("integral", "Definite integral", "A definite integral is a signed accumulation defined as a limit of sums or by a more general integration theory under integrability conditions.", "formal-mathematics.calculus"),
    ("ftc", "Fundamental theorem of calculus", "Under its hypotheses, differentiation and integration connect through accumulation functions and antiderivative endpoint differences.", "formal-mathematics.calculus"),
    ("substitution", "Integration by substitution", "Substitution transforms an integral through a differentiable change of variable with bounds, orientation, multiplicity, and domain handled consistently.", "formal-mathematics.calculus"),
    ("sequence-series", "Infinite series", "An infinite series converges when the sequence of finite partial sums converges.", "formal-mathematics.calculus"),
    ("taylor", "Taylor expansion", "A Taylor polynomial uses derivatives at one point, while equality to an infinite series requires a remainder tending to zero.", "formal-mathematics.calculus"),
    ("partial-derivative", "Partial derivative", "A partial derivative varies one coordinate while holding the others fixed in a chosen chart.", "formal-mathematics.calculus"),
    ("gradient", "Gradient", "The gradient represents the derivative of a scalar field through an inner product and points in steepest local increase under the corresponding norm.", "formal-mathematics.calculus"),
    ("jacobian", "Jacobian", "A Jacobian matrix represents the derivative of a multivariable map in selected coordinate bases.", "formal-mathematics.calculus"),
    ("multiple-integral", "Multiple integral", "A multiple integral accumulates over a multidimensional region with measure and coordinate-change Jacobians declared.", "formal-mathematics.calculus"),
    ("real-sequence", "Real sequence", "A real sequence is a function from natural indices to real values.", "formal-mathematics.real-analysis"),
    ("convergence", "Sequence convergence", "A sequence converges to L when every positive tolerance eventually bounds all later terms within that tolerance of L.", "formal-mathematics.real-analysis"),
    ("cauchy", "Cauchy sequence", "A Cauchy sequence has arbitrarily close sufficiently late terms without naming a limit in the ambient space.", "formal-mathematics.real-analysis"),
    ("completeness", "Completeness", "A metric space is complete when every Cauchy sequence converges to a point in the space.", "formal-mathematics.real-analysis"),
    ("compact", "Compactness", "Compactness can be characterized by finite subcovers and, in metric spaces, by sequential compactness under standard equivalence theorems.", "formal-mathematics.real-analysis"),
    ("uniform-continuity", "Uniform continuity", "Uniform continuity uses one input tolerance for every point in the domain, unlike pointwise continuity.", "formal-mathematics.real-analysis"),
    ("uniform-convergence", "Uniform convergence", "Uniform convergence controls the maximum pointwise error with one stage bound across the whole domain.", "formal-mathematics.real-analysis"),
    ("measure", "Measure", "A measure assigns nonnegative extended size to measurable sets with countable additivity.", "formal-mathematics.real-analysis"),
    ("lebesgue-integral", "Lebesgue integral", "The Lebesgue integral accumulates a measurable function through value-based simple approximations and positive-negative decomposition.", "formal-mathematics.real-analysis"),
    ("complex-number", "Complex number", "A complex number has real and imaginary components and forms an algebraically closed field after adjoining a square root of negative one.", "formal-mathematics.complex-analysis"),
    ("modulus-argument", "Complex modulus and argument", "A nonzero complex number has magnitude and direction, with argument defined modulo full turns and branches chosen explicitly.", "formal-mathematics.complex-analysis"),
    ("holomorphic", "Holomorphic function", "A complex function is holomorphic when it is complex differentiable on an open neighborhood, a stronger condition than real differentiability.", "formal-mathematics.complex-analysis"),
    ("cauchy-riemann", "Cauchy-Riemann equations", "Under appropriate real differentiability conditions, Cauchy-Riemann equations characterize complex differentiability.", "formal-mathematics.complex-analysis"),
    ("contour-integral", "Contour integral", "A contour integral integrates a complex function along an oriented parameterized curve.", "formal-mathematics.complex-analysis"),
    ("residue", "Residue", "A residue is the coefficient of the inverse first power in a Laurent expansion and determines contour contributions around isolated singularities.", "formal-mathematics.complex-analysis"),
    ("normed-space", "Normed vector space", "A normed vector space has a vector norm satisfying positivity, homogeneity, and the triangle inequality.", "formal-mathematics.functional-analysis"),
    ("banach", "Banach space", "A Banach space is a complete normed vector space.", "formal-mathematics.functional-analysis"),
    ("hilbert", "Hilbert space", "A Hilbert space is a complete inner-product space under the induced norm.", "formal-mathematics.functional-analysis"),
    ("bounded-operator", "Bounded linear operator", "A linear operator between normed spaces is bounded exactly when it is continuous.", "formal-mathematics.functional-analysis"),
    ("dual-space", "Continuous dual space", "The continuous dual consists of bounded linear functionals on a topological vector space.", "formal-mathematics.functional-analysis"),
    ("spectrum", "Operator spectrum", "The spectrum contains scalars for which an operator minus that scalar identity lacks a bounded inverse under the chosen space.", "formal-mathematics.functional-analysis"),
    ("ode", "Ordinary differential equation", "An ODE relates an unknown function of one independent variable to its derivatives.", "formal-mathematics.differential-equations"),
    ("initial-value", "Initial-value problem", "An initial-value problem pairs a differential equation with state values at an initial point.", "formal-mathematics.differential-equations"),
    ("existence-uniqueness", "ODE existence and uniqueness", "Existence and uniqueness follow only under theorem-specific continuity, Lipschitz, domain, and interval conditions.", "formal-mathematics.differential-equations"),
    ("equilibrium", "Dynamical equilibrium", "An equilibrium is a state where the differential evolution vanishes.", "formal-mathematics.differential-equations"),
    ("stability", "Dynamical stability", "Stability describes whether trajectories starting near an invariant state remain near or converge under quantified perturbations.", "formal-mathematics.differential-equations"),
    ("linear-ode", "Linear differential equation", "A linear differential equation applies a linear differential operator to the unknown function and supports superposition for homogeneous solutions.", "formal-mathematics.differential-equations"),
    ("pde", "Partial differential equation", "A PDE relates a multivariable field to partial derivatives and requires domain, boundary, initial, and regularity conditions.", "formal-mathematics.differential-equations"),
    ("boundary-value", "Boundary-value problem", "A boundary-value problem constrains a differential equation on the boundary of its domain and may differ sharply from initial-value well-posedness.", "formal-mathematics.differential-equations"),
    ("math-induction", "Mathematical induction", "Induction proves a property for all natural indices by establishing a base and a step from each index to its successor.", "formal-mathematics.discrete-mathematics"),
    ("recurrence", "Recurrence relation", "A recurrence defines sequence values from earlier indexed values plus sufficient initial conditions.", "formal-mathematics.discrete-mathematics"),
    ("loop-invariant", "Loop invariant", "A loop invariant holds before and after every iteration and helps prove initialization, preservation, and postcondition at termination.", "formal-mathematics.discrete-mathematics"),
    ("finite-state", "Finite-state system", "A finite-state system has a finite set of states and a transition relation or function over events.", "formal-mathematics.discrete-mathematics"),
    ("boolean-algebra", "Boolean algebra", "A Boolean algebra models conjunction, disjunction, complement, zero, and one under distributive lattice laws.", "formal-mathematics.discrete-mathematics"),
    ("sum-rule", "Combinatorial sum rule", "Counts of disjoint alternative cases add when every object belongs to exactly one case.", "formal-mathematics.combinatorics"),
    ("combinatorial-product-rule", "Combinatorial product rule", "Counts of sequential independent choices multiply when each complete object corresponds uniquely to one choice tuple.", "formal-mathematics.combinatorics"),
    ("permutation", "Permutation", "A permutation is a bijective ordering or self-map of a finite set.", "formal-mathematics.combinatorics"),
    ("combination", "Combination", "A combination selects an unordered subset of fixed size from a finite set.", "formal-mathematics.combinatorics"),
    ("pigeonhole", "Pigeonhole principle", "Placing more objects than containers forces at least one container to receive multiple objects.", "formal-mathematics.combinatorics"),
    ("inclusion-exclusion", "Inclusion-exclusion", "Inclusion-exclusion alternates intersection counts to correct repeated counting of a union.", "formal-mathematics.combinatorics"),
    ("graph", "Graph", "A graph consists of vertices and edges with directedness, multiplicity, loops, labels, and weights declared by the graph class.", "formal-mathematics.graph-theory"),
    ("graph-path", "Graph path", "A path is a sequence of incident vertices and edges satisfying direction and repetition conventions.", "formal-mathematics.graph-theory"),
    ("graph-cycle", "Graph cycle", "A cycle is a closed path with repetition restrictions determined by graph conventions.", "formal-mathematics.graph-theory"),
    ("connected", "Graph connectedness", "An undirected graph is connected when every pair of vertices has a path between them.", "formal-mathematics.graph-theory"),
    ("tree", "Tree", "A tree is a connected acyclic undirected graph and has a unique simple path between each vertex pair.", "formal-mathematics.graph-theory"),
    ("shortest-path", "Shortest path", "A shortest path minimizes total nonnegative edge length or edge count among valid source-target paths.", "formal-mathematics.graph-theory"),
    ("network-flow", "Network flow", "A network flow assigns edge values satisfying capacity and conservation constraints except at source and sink.", "formal-mathematics.graph-theory"),
    ("matching", "Graph matching", "A matching is a set of edges sharing no endpoints under the graph's incidence relation.", "formal-mathematics.graph-theory"),
    ("coloring", "Graph coloring", "A proper vertex coloring assigns colors so adjacent vertices differ and seeks feasibility or minimum color count.", "formal-mathematics.graph-theory"),
    ("set", "Set (mathematics)", "A set is determined extensionally by which objects are its members.", "formal-mathematics.set-theory"),
    ("subset", "Subset", "A is a subset of B when every member of A is a member of B.", "formal-mathematics.set-theory"),
    ("union", "Set union", "A union contains exactly the objects belonging to at least one input set.", "formal-mathematics.set-theory"),
    ("intersection", "Set intersection", "An intersection contains exactly the objects belonging to every input set.", "formal-mathematics.set-theory"),
    ("cartesian-product", "Cartesian product", "A Cartesian product contains ordered tuples whose components come from the corresponding factor sets.", "formal-mathematics.set-theory"),
    ("power-set", "Power set", "The power set of a set contains all of its subsets.", "formal-mathematics.set-theory"),
    ("cardinality", "Cardinality", "Cardinality compares set size through bijections and extends beyond finite counting.", "formal-mathematics.set-theory"),
    ("proposition", "Proposition", "A proposition is a declarative object assigned a truth value within a logical semantics.", "formal-mathematics.mathematical-logic"),
    ("predicate", "Predicate", "A predicate becomes a proposition when its free variables receive values or quantification.", "formal-mathematics.mathematical-logic"),
    ("quantifier", "Quantifier", "Universal and existential quantifiers range over a declared domain and bind variables with scope.", "formal-mathematics.mathematical-logic"),
    ("logical-entailment", "Logical entailment", "Premises entail a conclusion when every model satisfying the premises also satisfies the conclusion.", "formal-mathematics.mathematical-logic"),
    ("satisfiable", "Satisfiability", "A formula or theory is satisfiable when at least one model makes all of it true.", "formal-mathematics.mathematical-logic"),
    ("proof", "Formal proof", "A formal proof is a finite derivation from axioms and hypotheses using permitted inference rules.", "formal-mathematics.mathematical-logic"),
    ("soundness", "Logical soundness", "A proof system is sound when every derivable conclusion is semantically entailed by its premises.", "formal-mathematics.mathematical-logic"),
    ("completeness-logic", "Logical completeness", "A proof system is complete for a semantics when every semantically entailed formula is derivable.", "formal-mathematics.mathematical-logic"),
    ("category", "Category", "A category has objects and morphisms with associative composition and identity morphisms.", "formal-mathematics.category-theory"),
    ("morphism", "Morphism", "A morphism is a typed arrow between category objects and composes only when codomain and domain match.", "formal-mathematics.category-theory"),
    ("functor", "Functor", "A functor maps objects and morphisms between categories while preserving identities and composition.", "formal-mathematics.category-theory"),
    ("natural-transformation", "Natural transformation", "A natural transformation maps one functor to another through component morphisms commuting with every source morphism.", "formal-mathematics.category-theory"),
    ("product-category", "Categorical product", "A categorical product is characterized up to unique isomorphism by projection morphisms and a universal mapping property.", "formal-mathematics.category-theory"),
    ("adjunction", "Adjunction", "An adjunction relates two functors through a natural bijection of hom-sets or equivalent unit-counit data.", "formal-mathematics.category-theory"),
    ("objective", "Optimization objective", "An objective maps candidate decisions to a value or ordered vector to minimize or maximize.", "formal-mathematics.optimization"),
    ("feasible-set", "Feasible set", "The feasible set contains candidates satisfying every constraint and domain condition.", "formal-mathematics.optimization"),
    ("local-optimum", "Local optimum", "A local optimum is no worse than nearby feasible candidates under a declared topology or neighborhood.", "formal-mathematics.optimization"),
    ("global-optimum", "Global optimum", "A global optimum is no worse than every feasible candidate.", "formal-mathematics.optimization"),
    ("convex-optimization", "Convex optimization", "A convex optimization problem has a convex feasible set and convex minimization objective, making every local minimum global under standard conditions.", "formal-mathematics.optimization"),
    ("lagrangian", "Lagrangian", "A Lagrangian combines an objective and constraint functions with multipliers to analyze constrained optima and dual bounds.", "formal-mathematics.optimization"),
    ("duality", "Optimization duality", "A dual problem supplies bounds on a primal objective, with equality requiring theorem-specific regularity conditions.", "formal-mathematics.optimization"),
    ("linear-program", "Linear program", "A linear program optimizes a linear objective over linear equality and inequality constraints.", "formal-mathematics.optimization"),
    ("integer-program", "Integer program", "An integer program restricts selected decision variables to discrete values, changing convexity and algorithmic complexity.", "formal-mathematics.optimization"),
    ("floating-error", "Floating-point error", "Floating-point arithmetic rounds to a finite representable set and its operations need not satisfy real-number associativity or distributivity exactly.", "formal-mathematics.numerical-methods"),
    ("conditioning", "Problem conditioning", "Conditioning measures sensitivity of the exact mathematical solution to small input perturbations independently of an algorithm.", "formal-mathematics.numerical-methods"),
    ("numerical-stability", "Numerical stability", "A stable algorithm controls amplification of rounding and truncation error relative to the problem's conditioning.", "formal-mathematics.numerical-methods"),
    ("method-convergence", "Numerical method convergence", "A numerical method converges when its approximations approach the exact solution as discretization or iteration is refined under stated assumptions.", "formal-mathematics.numerical-methods"),
    ("root-finding", "Root finding", "Root finding approximates x with f of x equal to zero using bracketing, derivatives, interpolation, or fixed-point structure under method-specific conditions.", "formal-mathematics.numerical-methods"),
    ("interpolation", "Interpolation", "Interpolation constructs a function matching given data at selected nodes and carries approximation and conditioning error between them.", "formal-mathematics.numerical-methods"),
    ("quadrature", "Numerical quadrature", "Quadrature approximates an integral by weighted function samples with error depending on smoothness, nodes, and interval structure.", "formal-mathematics.numerical-methods"),
    ("theorem", "Formal theorem", "A theorem is a proposition paired with a proof term checked against a declared formal environment.", "formal-mathematics.formal-proof"),
    ("definition", "Formal definition", "A formal definition introduces a symbol by an accepted expression or inductive specification without adding an unproved theorem.", "formal-mathematics.formal-proof"),
    ("axiom", "Formal axiom", "An axiom adds an assumed proposition to the environment and therefore expands what can be derived without an internal proof.", "formal-mathematics.formal-proof"),
    ("proof-term", "Proof term", "A proof term inhabits a proposition-as-type and can be checked by a small trusted kernel.", "formal-mathematics.formal-proof"),
    ("kernel-checker", "Proof kernel", "A proof kernel checks typing, definitional equality, and trusted declarations rather than trusting tactics or generated prose.", "formal-mathematics.formal-proof"),
    ("tactic", "Proof tactic", "A tactic constructs proof terms by transforming goals and may fail or be buggy without compromising soundness when the kernel checks its output.", "formal-mathematics.formal-proof"),
    ("rewrite", "Equality rewriting", "Rewriting replaces equals by equals in a context under type and direction constraints.", "formal-mathematics.formal-proof"),
]


PROBABILITY = [
    ("root", "Probability and statistical inference", "Probability formalizes uncertain events under a declared sample space and measure, while statistics uses sampled evidence and assumptions to estimate, test, predict, calibrate, and make decisions about a population or process.", "probability-statistics.probability-foundations"),
    ("sample-space", "Sample space", "A sample space is the set of possible elementary outcomes under the modeled experiment.", "probability-statistics.probability-foundations"),
    ("event", "Event", "An event is a measurable subset of the sample space.", "probability-statistics.probability-foundations"),
    ("probability-measure", "Probability measure", "A probability measure assigns nonnegative mass one to the full sample space and is countably additive over disjoint events.", "probability-statistics.probability-foundations"),
    ("conditional", "Conditional probability", "Conditional probability rescales joint probability within a conditioning event of positive probability or uses a regular conditional construction in more general settings.", "probability-statistics.probability-foundations"),
    ("independence", "Event independence", "Events are independent when their joint probability factors into marginal probabilities; lack of correlation alone is generally weaker.", "probability-statistics.probability-foundations"),
    ("bayes-rule", "Bayes rule", "Bayes rule reverses conditioning by combining likelihood and prior probability and normalizing by evidence probability.", "probability-statistics.probability-foundations"),
    ("total-probability", "Law of total probability", "A measurable partition decomposes an event probability into conditioned contributions weighted by partition probabilities.", "probability-statistics.probability-foundations"),
    ("random-variable", "Random variable", "A random variable is a measurable function from outcomes to a value space.", "probability-statistics.random-variables"),
    ("distribution", "Probability distribution", "A distribution is the pushforward probability assigned to values or sets of values of a random variable.", "probability-statistics.random-variables"),
    ("pmf", "Probability mass function", "A PMF assigns probability to each value of a discrete random variable and sums to one.", "probability-statistics.random-variables"),
    ("density", "Probability density", "A density integrates to probabilities relative to a base measure and its point values are not probabilities for a continuous variable.", "probability-statistics.random-variables"),
    ("cdf", "Cumulative distribution function", "A CDF gives probability that a random variable is at most a threshold and uniquely determines its distribution.", "probability-statistics.random-variables"),
    ("expectation", "Expectation", "Expectation is the probability-weighted integral of a random variable when its positive and negative parts satisfy the needed integrability conditions.", "probability-statistics.random-variables"),
    ("variance", "Variance", "Variance is the expected squared deviation from the mean and measures spread in squared units.", "probability-statistics.random-variables"),
    ("covariance", "Covariance", "Covariance measures joint centered linear variation and depends on scale; zero covariance need not imply independence.", "probability-statistics.random-variables"),
    ("prior", "Bayesian prior", "A prior distribution represents modeled uncertainty about parameters before the current data under a declared information state.", "probability-statistics.bayesian-inference"),
    ("likelihood", "Likelihood", "A likelihood is the data probability or density viewed as a function of parameters and is not itself a normalized parameter distribution.", "probability-statistics.bayesian-inference"),
    ("posterior", "Bayesian posterior", "A posterior distribution is proportional to likelihood times prior under the model and conditions on observed data.", "probability-statistics.bayesian-inference"),
    ("posterior-predictive", "Posterior predictive", "A posterior predictive averages future-data distributions over posterior parameter uncertainty.", "probability-statistics.bayesian-inference"),
    ("credible-interval", "Credible interval", "A Bayesian credible interval contains a declared posterior probability for the parameter under the model and prior.", "probability-statistics.bayesian-inference"),
    ("bayes-factor", "Bayes factor", "A Bayes factor compares models through marginal likelihood and can be sensitive to prior mass and model specification.", "probability-statistics.bayesian-inference"),
    ("population", "Statistical population", "A population is the set or generative process about which an inference is intended, bounded by units, place, time, and inclusion rules.", "probability-statistics.frequentist-inference"),
    ("sample", "Statistical sample", "A sample is the observed subset or sequence produced by a sampling design from a population or process.", "probability-statistics.frequentist-inference"),
    ("statistic", "Statistic", "A statistic is a function of observed sample data and does not depend on unknown parameters in its computable definition.", "probability-statistics.frequentist-inference"),
    ("estimator", "Estimator", "An estimator is a statistic used to estimate a population parameter and is evaluated by its sampling distribution.", "probability-statistics.frequentist-inference"),
    ("bias", "Estimator bias", "Bias is the difference between an estimator's expected value and the target parameter under a sampling model.", "probability-statistics.frequentist-inference"),
    ("standard-error", "Standard error", "A standard error estimates the sampling standard deviation of an estimator under declared assumptions.", "probability-statistics.frequentist-inference"),
    ("confidence-interval", "Confidence interval", "A confidence-interval procedure has a long-run coverage rate over repeated samples under its model; one realized interval does not assign that frequentist probability to a fixed parameter.", "probability-statistics.frequentist-inference"),
    ("hypothesis-test", "Hypothesis test", "A hypothesis test defines null and alternative models, a statistic, decision rule, error rates, assumptions, and interpretation before inspecting the test outcome.", "probability-statistics.frequentist-inference"),
    ("p-value", "P value", "A p value is the probability, under the null model, of a statistic at least as incompatible as observed; it is not the probability that the null is true.", "probability-statistics.frequentist-inference"),
    ("power", "Statistical power", "Power is the probability that a test rejects the null under a specified alternative and design.", "probability-statistics.frequentist-inference"),
    ("experimental-unit", "Experimental unit", "An experimental unit is the smallest unit independently assigned to a treatment and determines the replication level.", "probability-statistics.experimental-design"),
    ("randomization", "Random assignment", "Random assignment uses a chance mechanism to allocate treatments and supports causal comparison by balancing confounders in expectation.", "probability-statistics.experimental-design"),
    ("control-group", "Control group", "A control group supplies a comparison condition under the same measurement and follow-up process.", "probability-statistics.experimental-design"),
    ("blinding", "Blinding", "Blinding withholds assignment or hypothesis information from selected participants, caregivers, assessors, or analysts to reduce behavior and measurement bias.", "probability-statistics.experimental-design"),
    ("blocking", "Experimental blocking", "Blocking groups units by prognostic variables before randomization to improve balance and precision.", "probability-statistics.experimental-design"),
    ("factorial", "Factorial design", "A factorial design varies multiple factors across combinations to estimate main effects and interactions under its randomization structure.", "probability-statistics.experimental-design"),
    ("causal-effect", "Causal effect", "A causal effect compares potential outcomes under different interventions for the same target unit or population through an identification strategy.", "probability-statistics.causal-inference"),
    ("potential-outcome", "Potential outcome", "A potential outcome is the result a unit would have under a particular intervention, with only selected outcomes observed.", "probability-statistics.causal-inference"),
    ("confounding", "Confounding", "Confounding occurs when common causes influence both exposure and outcome, mixing causal effect with background differences.", "probability-statistics.causal-inference"),
    ("exchangeability", "Exchangeability", "Conditional exchangeability asserts that treatment groups are comparable in potential outcomes after conditioning on measured covariates.", "probability-statistics.causal-inference"),
    ("positivity", "Causal positivity", "Positivity requires nonzero probability of each compared treatment across covariate strata needed for the target inference.", "probability-statistics.causal-inference"),
    ("consistency", "Causal consistency", "Consistency connects an observed outcome to the potential outcome under the intervention actually received, requiring well-defined treatment versions.", "probability-statistics.causal-inference"),
    ("process", "Stochastic process", "A stochastic process is an indexed family of random variables over time, space, or another parameter set.", "probability-statistics.stochastic-processes"),
    ("markov", "Markov property", "The Markov property makes the conditional distribution of the future depend on the present state rather than the full past under the chosen state representation.", "probability-statistics.stochastic-processes"),
    ("martingale", "Martingale", "A martingale has conditional expected future value equal to the present under its filtration and integrability conditions.", "probability-statistics.stochastic-processes"),
    ("stationarity", "Stationarity", "Stationarity makes selected joint or moment distributions invariant under index shifts, with strict and weak definitions distinguished.", "probability-statistics.stochastic-processes"),
    ("poisson-process", "Poisson process", "A homogeneous Poisson process has independent stationary increments and Poisson event counts with rate proportional to interval length.", "probability-statistics.stochastic-processes"),
    ("time-series", "Time series", "A time series is an ordered sequence of observations whose dependence, trend, seasonality, intervention, and measurement process must be modeled.", "probability-statistics.time-series"),
    ("autocorrelation", "Autocorrelation", "Autocorrelation measures linear association between time-shifted values and can reflect trend or seasonality rather than direct dynamics.", "probability-statistics.time-series"),
    ("forecast", "Forecast", "A forecast is a probability distribution or point-and-interval prediction for future observations under an information cutoff and model.", "probability-statistics.time-series"),
    ("backtest", "Forecast backtest", "A backtest simulates historical forecast origins and prevents future data, revisions, and preprocessing from leaking across each cutoff.", "probability-statistics.time-series"),
    ("concept-drift", "Temporal concept drift", "Concept drift changes the relation between predictors and target over time, while covariate shift changes predictor prevalence.", "probability-statistics.time-series"),
    ("uncertainty-budget", "Uncertainty budget", "An uncertainty budget identifies and combines quantified sources of measurement and model uncertainty under dependency assumptions.", "probability-statistics.uncertainty-quantification"),
    ("aleatoric", "Aleatoric uncertainty", "Aleatoric uncertainty describes modeled outcome variability that remains even with known parameters and state.", "probability-statistics.uncertainty-quantification"),
    ("epistemic", "Epistemic uncertainty", "Epistemic uncertainty reflects limited knowledge of parameters, structure, mechanisms, or distributions and may shrink with relevant evidence.", "probability-statistics.uncertainty-quantification"),
    ("sensitivity", "Sensitivity analysis", "Sensitivity analysis varies assumptions, inputs, models, and missing-data mechanisms to measure how conclusions change.", "probability-statistics.uncertainty-quantification"),
    ("monte-carlo", "Monte Carlo estimation", "Monte Carlo estimates integrals or distributions from simulated draws with sampling error and convergence diagnostics.", "probability-statistics.uncertainty-quantification"),
    ("prob-calibration", "Forecast calibration", "A probabilistic forecast is calibrated when events occur at rates consistent with assigned probabilities under the evaluation grouping.", "probability-statistics.calibration"),
    ("reliability-diagram", "Reliability diagram", "A reliability diagram compares binned predicted probabilities with empirical frequencies and carries binning and sampling uncertainty.", "probability-statistics.calibration"),
    ("proper-score", "Proper scoring rule", "A proper scoring rule makes honest reporting of a forecaster's probability distribution optimal in expectation.", "probability-statistics.calibration"),
    ("sharpness", "Forecast sharpness", "Sharpness measures concentration of predictive distributions and is valuable only subject to calibration.", "probability-statistics.calibration"),
    ("outlier", "Outlier", "An outlier is an observation unusually distant under a declared model or summary and may be error, rare valid data, or new mechanism.", "probability-statistics.robust-statistics"),
    ("breakdown", "Estimator breakdown point", "A breakdown point is the contamination fraction that can drive an estimator arbitrarily far or otherwise destroy its bounded behavior.", "probability-statistics.robust-statistics"),
    ("median", "Median", "A median is a value with at least half the probability or sample mass on each side and is robust to extreme magnitude in a minority of observations.", "probability-statistics.robust-statistics"),
    ("trimmed", "Trimmed estimator", "A trimmed estimator removes selected extreme order statistics before summarizing and trades efficiency for robustness under a contamination model.", "probability-statistics.robust-statistics"),
    ("nonparametric", "Nonparametric method", "A nonparametric method avoids fixing a finite-dimensional distribution family but still relies on smoothness, exchangeability, rank, or other assumptions.", "probability-statistics.nonparametric"),
    ("empirical-cdf", "Empirical distribution function", "The empirical CDF assigns cumulative sample proportion at each threshold and converges to the population CDF under sampling assumptions.", "probability-statistics.nonparametric"),
    ("rank-test", "Rank test", "A rank test bases inference on order information and has null validity under design-specific exchangeability or distribution assumptions.", "probability-statistics.nonparametric"),
    ("bootstrap", "Bootstrap", "The bootstrap approximates a sampling distribution by resampling an empirical or fitted distribution under representativeness and dependence assumptions.", "probability-statistics.nonparametric"),
    ("permutation-test", "Permutation test", "A permutation test compares the observed statistic with relabeled assignments valid under a null exchangeability condition.", "probability-statistics.nonparametric"),
]


INFORMATION = [
    ("root", "Information and communication system", "Information theory quantifies uncertainty, representation, compression, transmission, and inference under a probability model, while communication engineering maps messages through codes, signals, channels, receivers, and error controls.", "information-communication.entropy-information"),
    ("self-information", "Self-information", "The self-information of an outcome is the negative logarithm of its modeled probability, with units determined by logarithm base.", "information-communication.entropy-information"),
    ("entropy", "Shannon entropy", "Entropy is expected self-information for a discrete distribution and quantifies average uncertainty under that model.", "information-communication.entropy-information"),
    ("joint-entropy", "Joint entropy", "Joint entropy measures uncertainty in a pair or tuple of random variables together.", "information-communication.entropy-information"),
    ("conditional-entropy", "Conditional entropy", "Conditional entropy measures remaining average uncertainty in one variable after another is known.", "information-communication.entropy-information"),
    ("mutual-information", "Mutual information", "Mutual information is the expected log ratio between joint and independent models and measures statistical dependence symmetrically.", "information-communication.entropy-information"),
    ("kl-divergence", "Kullback-Leibler divergence", "KL divergence measures expected log likelihood ratio from one distribution to another and is nonnegative but not symmetric or a metric.", "information-communication.entropy-information"),
    ("data-processing", "Data-processing inequality", "Processing variables through a channel cannot increase mutual information about an upstream variable under the Markov condition.", "information-communication.entropy-information"),
    ("source", "Information source", "A source emits symbols according to a modeled stochastic process with alphabet, distribution, memory, and rate.", "information-communication.source-coding"),
    ("codeword", "Source codeword", "A codeword is a finite output-symbol sequence assigned to a source symbol or block.", "information-communication.source-coding"),
    ("prefix-code", "Prefix code", "A prefix code has no codeword that begins another and therefore supports instantaneous left-to-right decoding.", "information-communication.source-coding"),
    ("kraft", "Kraft inequality", "Prefix-code lengths over a fixed code alphabet satisfy Kraft's inequality, and qualifying integer lengths can construct a prefix code.", "information-communication.source-coding"),
    ("lossless-compression", "Lossless source coding", "Lossless compression maps source sequences to uniquely decodable representations from which the original can be recovered exactly.", "information-communication.source-coding"),
    ("typical-set", "Typical set", "For suitable long source blocks, a typical set carries most probability mass and has size exponential in entropy rate.", "information-communication.source-coding"),
    ("source-theorem", "Source coding theorem", "Under theorem assumptions, average lossless code length approaches but cannot beat source entropy rate asymptotically.", "information-communication.source-coding"),
    ("channel", "Communication channel", "A channel is a conditional distribution or physical system mapping input symbols to uncertain output observations.", "information-communication.channel-coding"),
    ("channel-code", "Channel code", "A channel code maps messages to longer transmitted sequences so redundancy enables recovery under a channel model.", "information-communication.channel-coding"),
    ("code-rate", "Code rate", "Code rate is the ratio of source message symbols or information bits to transmitted channel symbols under a declared convention.", "information-communication.channel-coding"),
    ("capacity", "Channel capacity", "Channel capacity is the maximum mutual-information rate over allowable input distributions and constraints for a memoryless channel or its generalized definition.", "information-communication.channel-coding"),
    ("noisy-channel", "Noisy-channel coding theorem", "Rates below capacity can achieve arbitrarily small error with sufficiently long codes under theorem assumptions, while rates above capacity cannot.", "information-communication.channel-coding"),
    ("encoder", "Channel encoder", "An encoder transforms message and optional state into a codeword satisfying rate, power, latency, and structure constraints.", "information-communication.channel-coding"),
    ("decoder", "Channel decoder", "A decoder maps noisy observations and side information to an estimated message with defined error criterion and complexity.", "information-communication.channel-coding"),
    ("hamming-distance", "Hamming distance", "Hamming distance counts positions at which equal-length symbol strings differ and is a metric.", "information-communication.error-correction"),
    ("minimum-distance", "Minimum code distance", "Minimum distance is the smallest distance between distinct codewords and bounds guaranteed detection and correction under the metric.", "information-communication.error-correction"),
    ("parity-check", "Parity-check constraint", "A parity-check matrix maps valid linear codewords to zero syndrome over the code field.", "information-communication.error-correction"),
    ("syndrome", "Error syndrome", "A syndrome is the parity-check result of a received word and identifies an error coset rather than always one unique error.", "information-communication.error-correction"),
    ("erasure", "Erasure channel error", "An erasure identifies a position whose symbol is unknown, providing more location information than an arbitrary substitution error.", "information-communication.error-correction"),
    ("soft-decision", "Soft-decision decoding", "Soft-decision decoding uses graded likelihood information from the detector rather than hard symbol decisions.", "information-communication.error-correction"),
    ("message", "Communication message", "A message is the information-bearing object selected from a declared set before source and channel representation.", "information-communication.communication-systems"),
    ("transmitter", "Transmitter", "A transmitter encodes, modulates, shapes, amplifies, and emits a signal under spectrum, power, hardware, and channel constraints.", "information-communication.communication-systems"),
    ("receiver", "Receiver", "A receiver filters, synchronizes, estimates, detects, decodes, and reconstructs messages from observations under uncertainty.", "information-communication.communication-systems"),
    ("noise", "Communication noise", "Noise is modeled unwanted variation added or coupled into observations, with distribution and dependence affecting optimal detection.", "information-communication.communication-systems"),
    ("snr", "Signal-to-noise ratio", "SNR compares signal power to noise power under a bandwidth, impedance, location, and averaging convention.", "information-communication.communication-systems"),
    ("link-budget", "Link budget", "A link budget combines transmit power, gains, path losses, noise, bandwidth, and margins in compatible logarithmic or linear units.", "information-communication.communication-systems"),
    ("symbol", "Modulation symbol", "A modulation symbol selects one point or waveform from a constellation to represent coded bits during a symbol interval.", "information-communication.modulation"),
    ("constellation", "Signal constellation", "A constellation is the set of permitted modulation points in a signal space with geometry governing noise sensitivity.", "information-communication.modulation"),
    ("modulation", "Modulation", "Modulation maps symbols onto carrier amplitude, phase, frequency, time, or multicarrier degrees of freedom for transmission.", "information-communication.modulation"),
    ("demodulation", "Demodulation", "Demodulation maps received waveforms to symbol likelihoods or estimates using synchronization and channel information.", "information-communication.modulation"),
    ("matched-filter", "Matched filter", "Under an additive white Gaussian noise model, a matched filter maximizes output SNR for detecting a known waveform at a chosen sample.", "information-communication.modulation"),
    ("nyquist", "Nyquist pulse criterion", "A zero-inter-symbol-interference pulse family satisfies sample-domain constraints at symbol decision times under timing alignment.", "information-communication.modulation"),
    ("sample", "Signal sample", "A sample records signal value at a time or spatial position under an acquisition bandwidth and quantization convention.", "information-communication.signal-processing"),
    ("sampling-theorem", "Sampling theorem", "A suitably bandlimited signal can be reconstructed from samples above its Nyquist rate under ideal theorem conditions.", "information-communication.signal-processing"),
    ("aliasing", "Aliasing", "Aliasing makes distinct continuous-frequency components indistinguishable after insufficient or structured sampling.", "information-communication.signal-processing"),
    ("convolution", "Signal convolution", "Convolution combines an input with an impulse response to produce the output of a linear time-invariant system.", "information-communication.signal-processing"),
    ("fourier", "Fourier transform", "A Fourier transform represents a signal through frequency components under transform, normalization, and integrability conventions.", "information-communication.signal-processing"),
    ("filter", "Digital filter", "A digital filter transforms a sampled sequence through difference equations, convolution, or state-space dynamics with stability and phase properties.", "information-communication.signal-processing"),
    ("quantization", "Signal quantization", "Quantization maps a continuous or high-resolution value to a finite set, introducing error correlated with the signal unless model conditions justify a noise approximation.", "information-communication.signal-processing"),
    ("network-source", "Network information source", "A network information problem has multiple sources, channels, terminals, messages, and side information with joint coding constraints.", "information-communication.network-information"),
    ("multiple-access", "Multiple-access channel", "A multiple-access channel combines inputs from multiple transmitters into one receiver observation and has a rate region rather than one capacity number.", "information-communication.network-information"),
    ("broadcast-channel", "Broadcast channel", "A broadcast channel maps one transmitter input to multiple receiver observations with receiver-specific messages and side information.", "information-communication.network-information"),
    ("relay-channel", "Relay channel", "A relay channel includes an intermediate terminal whose observation and transmission can assist end-to-end communication.", "information-communication.network-information"),
    ("network-coding", "Network coding", "Network coding allows intermediate nodes to combine messages algebraically rather than only route copies, improving achievable rates in some networks.", "information-communication.network-information"),
    ("semantic-content", "Semantic content", "Semantic information concerns meaning, truth, relevance, or task value and is not determined by Shannon entropy alone.", "information-communication.semantic-information"),
    ("syntax-semantics", "Syntactic-semantic boundary", "Two messages can have equal code length or entropy and different meaning, truth, or usefulness to an agent.", "information-communication.semantic-information"),
    ("task-information", "Task-relevant information", "Task-relevant information is the portion of representation that improves a declared decision or prediction under a utility and distribution.", "information-communication.semantic-information"),
    ("common-ground", "Communication common ground", "Interpretation depends on shared language, context, codebook, world knowledge, and pragmatic assumptions beyond physical transmission.", "information-communication.semantic-information"),
    ("misinformation", "Misinformation boundary", "A reliably transmitted message can still be false or misleading because channel fidelity does not establish semantic truth.", "information-communication.semantic-information"),
]


RELATIONS = [
    ("math-natural-integer", "math.natural", "math.integer", "part_of", "Natural numbers embed into integers."),
    ("math-integer-rational", "math.integer", "math.rational", "part_of", "Integers embed into rationals through denominator one."),
    ("math-rational-real", "math.rational", "math.real", "part_of", "Rationals embed densely into the real numbers."),
    ("math-add-sub", "math.addition", "math.subtraction", "qualifies", "Subtraction is addition of an additive inverse in a group."),
    ("math-mul-div", "math.multiplication", "math.division", "qualifies", "Division by a nonzero field element is multiplication by its inverse."),
    ("math-fraction-rational", "math.fraction", "math.rational", "implements", "A nonzero-denominator fraction implements a rational representation."),
    ("math-decimal-rational", "math.decimal", "math.rational", "implements", "A terminating or repeating decimal implements a rational representation."),
    ("math-percent-fraction", "math.percent", "math.fraction", "transforms_to", "Dividing a percent value by one hundred transforms it into a ratio."),
    ("math-unit-word", "math.unit", "math.word-quantity", "qualifies", "Units qualify admissible word-problem operations and answers."),
    ("math-divisibility-factor", "math.divisibility", "math.fundamental-arithmetic", "supports", "Divisibility supports prime factorization statements."),
    ("math-prime-factor", "math.prime", "math.fundamental-arithmetic", "part_of", "Prime factors compose the unique factorization of positive integers."),
    ("math-gcd-euclid", "math.euclidean-algorithm", "math.gcd", "implements", "The Euclidean algorithm implements gcd computation."),
    ("math-mod-divide", "math.divisibility", "math.modular", "grounds", "Divisibility of a difference grounds modular congruence."),
    ("math-variable-expression", "math.variable", "math.expression", "part_of", "Variables can form leaves of algebraic expressions."),
    ("math-expression-equation", "math.expression", "math.equation", "part_of", "Two expressions form the sides of an equation."),
    ("math-equivalence-solution", "math.equivalent-equation", "math.equation", "qualifies", "Equivalent transformations preserve the equation solution set."),
    ("math-linear-equation", "math.linear-equation", "math.equation", "part_of", "A linear equation is one equation class."),
    ("math-factor-polynomial", "math.factorization", "math.polynomial", "transforms_to", "Factorization transforms a polynomial into an equal product."),
    ("math-rational-domain", "math.division", "math.rational-expression", "qualifies", "Division qualifies the excluded denominator-zero domain of rational expressions."),
    ("math-system-equation", "math.equation", "math.system-equations", "part_of", "Equations compose a simultaneous system."),
    ("math-quantity-unknown", "math.word-quantity", "math.word-unknown", "qualifies", "The requested quantity qualifies the unknown and its units."),
    ("math-constraint-model", "math.word-constraint", "math.word-model", "part_of", "Translated constraints form part of a word-problem model."),
    ("math-model-equation", "math.word-model", "math.equation", "implements", "A word-problem model implements quantity relations as equations or inequalities."),
    ("math-check-model", "math.word-solution-check", "math.word-model", "supports", "Substitution into the original model supports acceptance of a candidate solution."),
    ("math-rate-model", "math.rate", "math.word-model", "part_of", "Rate relationships form one word-problem mechanism."),
    ("math-mixture-model", "math.mixture", "math.word-model", "part_of", "Component balances form one word-problem mechanism."),
    ("math-work-model", "math.work-rate", "math.rate", "qualifies", "Work rates qualify additive completion per unit time."),
    ("math-percent-model", "math.percent-change", "math.percent", "qualifies", "Original-base selection qualifies percent change."),
    ("math-vector-space", "math.lin-vector", "math.vector-space", "part_of", "Vectors are elements of a vector space."),
    ("math-span-space", "math.span", "math.vector-space", "part_of", "A span is a vector subspace."),
    ("math-independent-basis", "math.linear-independence", "math.basis", "prerequisite", "Linear independence is prerequisite to a basis."),
    ("math-span-basis", "math.span", "math.basis", "prerequisite", "Spanning the space is prerequisite to a basis."),
    ("math-basis-dimension", "math.basis", "math.lin-dimension", "grounds", "Basis cardinality grounds vector-space dimension."),
    ("math-map-matrix", "math.matrix", "math.linear-map", "implements", "A matrix implements a linear map in chosen bases."),
    ("math-kernel-map", "math.kernel", "math.linear-map", "part_of", "The kernel is a subspace attached to a linear map."),
    ("math-image-map", "math.image", "math.linear-map", "part_of", "The image is a subspace attached to a linear map."),
    ("math-rank-nullity", "math.kernel", "math.rank-nullity", "part_of", "Kernel dimension forms the nullity term in rank-nullity."),
    ("math-image-rank", "math.image", "math.rank-nullity", "part_of", "Image dimension forms the rank term in rank-nullity."),
    ("math-det-invert", "math.determinant", "math.linear-map", "qualifies", "A nonzero determinant qualifies invertibility of a square finite-dimensional map."),
    ("math-eigen-map", "math.eigenvalue", "math.linear-map", "qualifies", "Eigenpairs qualify invariant one-dimensional directions."),
    ("math-inner-vector", "math.inner-product", "math.vector-space", "qualifies", "An inner product equips a vector space with metric and angle structure."),
    ("math-operation-semigroup", "math.binary-operation", "math.semigroup", "prerequisite", "A closed binary operation is prerequisite to a semigroup."),
    ("math-semigroup-monoid", "math.semigroup", "math.monoid", "prerequisite", "Associative operation is prerequisite to a monoid."),
    ("math-monoid-group", "math.monoid", "math.group", "prerequisite", "A monoid structure is prerequisite to a group."),
    ("math-group-subgroup", "math.subgroup", "math.group", "part_of", "A subgroup inherits a group operation."),
    ("math-hom-operation", "math.homomorphism", "math.binary-operation", "supports", "A homomorphism preserves the relevant operations."),
    ("math-normal-quotient", "math.subgroup", "math.quotient-group", "qualifies", "Normality of a subgroup qualifies well-defined quotient multiplication."),
    ("math-group-ring", "math.group", "math.ring", "part_of", "The additive structure of a ring is an abelian group."),
    ("math-ideal-ring", "math.ideal", "math.ring", "part_of", "An ideal is an absorbing additive subgroup of a ring."),
    ("math-ring-field", "math.ring", "math.field", "prerequisite", "A commutative ring structure is prerequisite to a field."),
    ("math-limit-continuity", "math.limit", "math.continuity", "grounds", "Equality between function value and limit grounds continuity."),
    ("math-limit-derivative", "math.limit", "math.derivative", "grounds", "A difference-quotient limit grounds the derivative."),
    ("math-product-derivative", "math.product-rule", "math.derivative", "implements", "The product rule implements differentiation of products."),
    ("math-chain-derivative", "math.chain-rule", "math.derivative", "implements", "The chain rule implements differentiation of compositions."),
    ("math-integral-ftc", "math.integral", "math.ftc", "part_of", "The definite integral forms one side of the fundamental calculus relation."),
    ("math-derivative-ftc", "math.derivative", "math.ftc", "part_of", "Differentiation forms the other side of the fundamental calculus relation."),
    ("math-substitution-integral", "math.substitution", "math.integral", "transforms_to", "Substitution transforms an integral through a change of variables."),
    ("math-series-sequence", "math.real-sequence", "math.sequence-series", "prerequisite", "Partial sums form a sequence whose convergence defines a series."),
    ("math-taylor-derivative", "math.derivative", "math.taylor", "prerequisite", "Repeated derivatives are prerequisites to Taylor coefficients."),
    ("math-partial-jacobian", "math.partial-derivative", "math.jacobian", "part_of", "Partial derivatives form Jacobian entries."),
    ("math-gradient-partial", "math.partial-derivative", "math.gradient", "part_of", "Coordinate partial derivatives form a Euclidean gradient."),
    ("math-jacobian-integral", "math.jacobian", "math.multiple-integral", "qualifies", "A change-of-variables Jacobian qualifies transformed volume elements."),
    ("math-sequence-convergence", "math.real-sequence", "math.convergence", "qualifies", "A sequence can be classified by its convergence."),
    ("math-converge-cauchy", "math.convergence", "math.cauchy", "causes", "Every convergent sequence is Cauchy in a metric space."),
    ("math-complete-cauchy", "math.completeness", "math.cauchy", "qualifies", "Completeness qualifies whether every Cauchy sequence has an internal limit."),
    ("math-compact-uniform", "math.compact", "math.uniform-continuity", "supports", "Continuity on a compact metric domain supports uniform continuity."),
    ("math-uniform-pointwise", "math.uniform-convergence", "math.convergence", "qualifies", "Uniform convergence is stronger than pointwise convergence."),
    ("math-measure-integral", "math.measure", "math.lebesgue-integral", "prerequisite", "A measure is prerequisite to Lebesgue integration."),
    ("math-complex-polar", "math.modulus-argument", "math.complex-number", "implements", "Modulus and argument implement a polar representation of nonzero complex numbers."),
    ("math-cr-holomorphic", "math.cauchy-riemann", "math.holomorphic", "qualifies", "Cauchy-Riemann equations with regularity qualify holomorphicity."),
    ("math-holo-contour", "math.holomorphic", "math.contour-integral", "qualifies", "Holomorphicity qualifies deformation and integral theorems on suitable domains."),
    ("math-residue-contour", "math.residue", "math.contour-integral", "supports", "Residues support evaluating contours around isolated singularities."),
    ("math-norm-banach", "math.normed-space", "math.banach", "prerequisite", "A normed space structure is prerequisite to a Banach space."),
    ("math-inner-hilbert", "math.inner-product", "math.hilbert", "prerequisite", "An inner product and completeness are prerequisites to a Hilbert space."),
    ("math-bounded-dual", "math.bounded-operator", "math.dual-space", "part_of", "Continuous linear functionals are bounded operators into the scalar field."),
    ("math-spectrum-operator", "math.bounded-operator", "math.spectrum", "qualifies", "The operator and space qualify its spectrum."),
    ("math-ode-ivp", "math.initial-value", "math.ode", "qualifies", "Initial data qualifies an ODE as an initial-value problem."),
    ("math-existence-ivp", "math.existence-uniqueness", "math.initial-value", "qualifies", "Regularity conditions qualify existence and uniqueness of an IVP."),
    ("math-equilibrium-stability", "math.equilibrium", "math.stability", "prerequisite", "An invariant equilibrium is prerequisite to equilibrium stability analysis."),
    ("math-linear-superposition", "math.linear-ode", "math.ode", "part_of", "Linear ODEs form a structured class supporting homogeneous superposition."),
    ("math-pde-boundary", "math.boundary-value", "math.pde", "qualifies", "Boundary conditions qualify a PDE problem."),
    ("math-induction-recurrence", "math.math-induction", "math.recurrence", "supports", "Induction supports proofs about recursively defined sequences."),
    ("math-invariant-state", "math.loop-invariant", "math.finite-state", "qualifies", "An invariant qualifies every reachable state transition."),
    ("math-boolean-logic", "math.boolean-algebra", "math.proposition", "implements", "Boolean algebra implements truth-functional operations."),
    ("math-sum-count", "math.sum-rule", "math.combination", "supports", "Disjoint case addition supports combinatorial counting."),
    ("math-product-count", "math.combinatorial-product-rule", "math.permutation", "supports", "Sequential choice multiplication supports permutation counts."),
    ("math-pigeon-count", "math.pigeonhole", "math.combination", "supports", "Counting objects and containers supports pigeonhole conclusions."),
    ("math-inclusion-union", "math.inclusion-exclusion", "math.union", "implements", "Inclusion-exclusion implements corrected union counting."),
    ("math-path-graph", "math.graph-path", "math.graph", "part_of", "Paths are sequences within a graph."),
    ("math-cycle-path", "math.graph-cycle", "math.graph-path", "part_of", "Cycles are closed paths."),
    ("math-connected-path", "math.graph-path", "math.connected", "grounds", "Pairwise path existence grounds graph connectedness."),
    ("math-tree-connected", "math.tree", "math.connected", "part_of", "Every tree is connected."),
    ("math-shortest-path", "math.shortest-path", "math.graph-path", "qualifies", "Minimum weight qualifies a shortest path."),
    ("math-flow-graph", "math.network-flow", "math.graph", "qualifies", "Capacities and conservation qualify a graph as a flow network."),
    ("math-matching-graph", "math.matching", "math.graph", "part_of", "A matching is a constrained edge subset of a graph."),
    ("math-color-graph", "math.coloring", "math.graph", "qualifies", "Adjacency constraints qualify proper graph coloring."),
    ("math-subset-set", "math.subset", "math.set", "qualifies", "Membership implication qualifies the subset relation."),
    ("math-union-set", "math.union", "math.set", "implements", "Union implements disjunctive membership."),
    ("math-intersection-set", "math.intersection", "math.set", "implements", "Intersection implements conjunctive membership."),
    ("math-product-set", "math.cartesian-product", "math.set", "implements", "Cartesian products implement ordered tuple construction."),
    ("math-powerset-cardinality", "math.power-set", "math.cardinality", "qualifies", "For a finite n-element set, its power set has cardinality two to the n."),
    ("math-predicate-proposition", "math.predicate", "math.proposition", "transforms_to", "Binding or quantifying free variables transforms a predicate into a proposition."),
    ("math-quantifier-predicate", "math.quantifier", "math.predicate", "qualifies", "Quantifiers qualify variable domain and scope."),
    ("math-model-entail", "math.logical-entailment", "math.satisfiable", "qualifies", "Model satisfaction qualifies semantic entailment."),
    ("math-proof-sound", "math.proof", "math.soundness", "qualifies", "Soundness qualifies derivations as semantically valid."),
    ("math-complete-entail", "math.completeness-logic", "math.logical-entailment", "supports", "Completeness supports deriving every semantic consequence in scope."),
    ("math-morphism-category", "math.morphism", "math.category", "part_of", "Morphisms form the arrows of a category."),
    ("math-functor-category", "math.functor", "math.category", "transforms_to", "A functor maps one category structure to another."),
    ("math-natural-functor", "math.natural-transformation", "math.functor", "qualifies", "Naturality qualifies a transformation between functors."),
    ("math-product-universal", "math.product-category", "math.category", "part_of", "Categorical products are defined by a universal property in a category."),
    ("math-adjunction-functor", "math.adjunction", "math.functor", "qualifies", "An adjunction qualifies a pair of functors through natural correspondence."),
    ("math-objective-feasible", "math.feasible-set", "math.objective", "qualifies", "Feasibility qualifies the candidates compared by an objective."),
    ("math-local-global", "math.local-optimum", "math.global-optimum", "qualifies", "A local optimum need not be global without additional structure."),
    ("math-convex-global", "math.convex-optimization", "math.local-optimum", "supports", "Convexity supports every local minimum being global under standard conditions."),
    ("math-lagrange-dual", "math.lagrangian", "math.duality", "implements", "The Lagrangian implements construction of a dual bound."),
    ("math-linear-convex", "math.linear-program", "math.convex-optimization", "part_of", "Linear programming is a convex optimization class."),
    ("math-integer-convex", "math.integer-program", "math.convex-optimization", "undercuts", "Integrality constraints undercut continuous convex feasibility even with linear objectives."),
    ("math-conditioning-error", "math.conditioning", "math.floating-error", "qualifies", "Problem conditioning qualifies how input and rounding error affect solutions."),
    ("math-stability-error", "math.numerical-stability", "math.floating-error", "inhibits", "A stable algorithm inhibits unnecessary amplification of rounding error."),
    ("math-convergence-method", "math.method-convergence", "math.numerical-stability", "qualifies", "Convergence and stability qualify a numerical approximation under refinement."),
    ("math-root-method", "math.root-finding", "math.method-convergence", "qualifies", "Method assumptions qualify root-finding convergence."),
    ("math-interpolation-quadrature", "math.interpolation", "math.quadrature", "supports", "Polynomial interpolation supports many quadrature constructions."),
    ("math-definition-theorem", "math.definition", "math.theorem", "prerequisite", "Definitions and assumptions are prerequisites to theorem statements."),
    ("math-axiom-proof", "math.axiom", "math.proof", "prerequisite", "Axioms and hypotheses are permitted premises of a formal proof."),
    ("math-proof-term", "math.proof-term", "math.proof", "implements", "A proof term implements a formal derivation."),
    ("math-kernel-term", "math.kernel-checker", "math.proof-term", "measures", "The proof kernel checks whether a term inhabits the claimed proposition."),
    ("math-tactic-term", "math.tactic", "math.proof-term", "causes", "A tactic can construct a candidate proof term."),
    ("math-rewrite-proof", "math.rewrite", "math.proof", "implements", "Equality rewriting implements one proof step."),
    ("prob-space-event", "prob.event", "prob.sample-space", "part_of", "Events are measurable subsets of a sample space."),
    ("prob-measure-event", "prob.probability-measure", "prob.event", "measures", "A probability measure assigns mass to events."),
    ("prob-conditional-joint", "prob.conditional", "prob.probability-measure", "transforms_to", "Conditioning transforms a probability measure within an event."),
    ("prob-independent-joint", "prob.independence", "prob.probability-measure", "qualifies", "Independence qualifies joint probability factorization."),
    ("prob-bayes-conditional", "prob.bayes-rule", "prob.conditional", "implements", "Bayes rule implements reversal of conditional probability."),
    ("prob-total-partition", "prob.total-probability", "prob.probability-measure", "implements", "Total probability implements partition-based decomposition."),
    ("prob-rv-space", "prob.random-variable", "prob.sample-space", "transforms_to", "A random variable maps outcomes to values."),
    ("prob-rv-distribution", "prob.random-variable", "prob.distribution", "causes", "A random variable and measure induce its distribution."),
    ("prob-pmf-distribution", "prob.pmf", "prob.distribution", "implements", "A PMF implements a discrete distribution."),
    ("prob-density-distribution", "prob.density", "prob.distribution", "implements", "A density implements an absolutely continuous distribution relative to a base measure."),
    ("prob-cdf-distribution", "prob.cdf", "prob.distribution", "implements", "A CDF implements a complete one-dimensional distribution representation."),
    ("prob-expect-distribution", "prob.distribution", "prob.expectation", "grounds", "A distribution grounds expectations of integrable functions."),
    ("prob-variance-expect", "prob.expectation", "prob.variance", "prerequisite", "A finite mean and second moment are prerequisites to finite variance."),
    ("prob-cov-independence", "prob.independence", "prob.covariance", "causes", "Independence with finite moments causes zero covariance."),
    ("prob-prior-likelihood", "prob.prior", "prob.posterior", "prerequisite", "A prior forms one prerequisite for a Bayesian posterior."),
    ("prob-like-posterior", "prob.likelihood", "prob.posterior", "prerequisite", "A likelihood forms one prerequisite for a Bayesian posterior."),
    ("prob-post-predictive", "prob.posterior", "prob.posterior-predictive", "grounds", "The posterior grounds averaging future predictions over parameter uncertainty."),
    ("prob-credible-post", "prob.posterior", "prob.credible-interval", "grounds", "Posterior mass grounds a credible interval."),
    ("prob-bayesfactor-like", "prob.likelihood", "prob.bayes-factor", "qualifies", "Marginal likelihoods qualify a Bayes factor."),
    ("prob-sample-pop", "prob.sample", "prob.population", "measures", "A sampling design selects observed units from a target population."),
    ("prob-stat-sample", "prob.statistic", "prob.sample", "transforms_to", "A statistic transforms sample data into a summary."),
    ("prob-estimator-stat", "prob.estimator", "prob.statistic", "part_of", "An estimator is a statistic used for a parameter."),
    ("prob-bias-estimator", "prob.bias", "prob.estimator", "measures", "Bias measures expected estimator offset."),
    ("prob-se-estimator", "prob.standard-error", "prob.estimator", "measures", "Standard error measures sampling spread of an estimator."),
    ("prob-ci-se", "prob.standard-error", "prob.confidence-interval", "supports", "Standard-error estimates support many confidence interval constructions."),
    ("prob-test-p", "prob.hypothesis-test", "prob.p-value", "causes", "A prespecified test statistic and null distribution cause a p value."),
    ("prob-power-test", "prob.power", "prob.hypothesis-test", "qualifies", "Power qualifies test behavior under specified alternatives."),
    ("prob-unit-random", "prob.experimental-unit", "prob.randomization", "qualifies", "Experimental-unit identity qualifies valid random assignment and replication."),
    ("prob-random-control", "prob.randomization", "prob.control-group", "supports", "Random assignment supports comparable treatment and control groups in expectation."),
    ("prob-blind-measure", "prob.blinding", "prob.bias", "inhibits", "Blinding inhibits selected behavior and assessment biases."),
    ("prob-block-random", "prob.blocking", "prob.randomization", "qualifies", "Blocking qualifies the randomization structure."),
    ("prob-factor-interaction", "prob.factorial", "prob.randomization", "supports", "Factorial randomization supports estimation of interactions."),
    ("prob-potential-effect", "prob.potential-outcome", "prob.causal-effect", "grounds", "Contrasts of potential outcomes ground causal effects."),
    ("prob-confound-effect", "prob.confounding", "prob.causal-effect", "undercuts", "Uncontrolled confounding undercuts a causal effect estimate."),
    ("prob-exchange-effect", "prob.exchangeability", "prob.causal-effect", "supports", "Exchangeability supports identification of causal contrasts."),
    ("prob-positive-effect", "prob.positivity", "prob.causal-effect", "prerequisite", "Treatment positivity is prerequisite to identifying comparisons across required strata."),
    ("prob-consistency-effect", "prob.consistency", "prob.causal-effect", "prerequisite", "Consistency is prerequisite to linking observed and potential outcomes."),
    ("prob-process-rv", "prob.random-variable", "prob.process", "part_of", "Indexed random variables compose a stochastic process."),
    ("prob-markov-process", "prob.markov", "prob.process", "qualifies", "The Markov condition qualifies dependence of future on present state."),
    ("prob-martingale-process", "prob.martingale", "prob.process", "qualifies", "A filtration and conditional expectation qualify a martingale process."),
    ("prob-stationary-process", "prob.stationarity", "prob.process", "qualifies", "Stationarity qualifies distribution invariance across index shifts."),
    ("prob-poisson-process", "prob.poisson-process", "prob.process", "part_of", "A Poisson process is one counting-process model."),
    ("prob-time-process", "prob.time-series", "prob.process", "measures", "A time series is observed from a temporally indexed process."),
    ("prob-auto-time", "prob.autocorrelation", "prob.time-series", "measures", "Autocorrelation measures linear time-shift association."),
    ("prob-forecast-process", "prob.process", "prob.forecast", "grounds", "A fitted stochastic process grounds a forecast distribution."),
    ("prob-backtest-forecast", "prob.backtest", "prob.forecast", "measures", "Backtesting measures forecasts at historical information cutoffs."),
    ("prob-drift-forecast", "prob.concept-drift", "prob.forecast", "qualifies", "Concept drift qualifies forecast validity over time."),
    ("prob-uncertainty-components", "prob.aleatoric", "prob.uncertainty-budget", "part_of", "Aleatoric variability forms one uncertainty component."),
    ("prob-epistemic-budget", "prob.epistemic", "prob.uncertainty-budget", "part_of", "Epistemic uncertainty forms one uncertainty component."),
    ("prob-sensitivity-budget", "prob.sensitivity", "prob.uncertainty-budget", "measures", "Sensitivity analysis measures conclusion dependence on assumptions."),
    ("prob-montecarlo-expect", "prob.monte-carlo", "prob.expectation", "measures", "Monte Carlo sample averages estimate expectations."),
    ("prob-calibration-forecast", "prob.prob-calibration", "prob.forecast", "qualifies", "Calibration qualifies probability forecasts."),
    ("prob-diagram-calibration", "prob.reliability-diagram", "prob.prob-calibration", "measures", "A reliability diagram measures empirical calibration by bins."),
    ("prob-score-forecast", "prob.proper-score", "prob.forecast", "measures", "A proper score evaluates probabilistic forecasts."),
    ("prob-sharp-cal", "prob.sharpness", "prob.prob-calibration", "qualifies", "Sharpness is interpreted subject to calibration."),
    ("prob-outlier-model", "prob.outlier", "prob.distribution", "qualifies", "The reference distribution qualifies what counts as an outlier."),
    ("prob-breakdown-estimator", "prob.breakdown", "prob.estimator", "qualifies", "Breakdown point qualifies estimator robustness to contamination."),
    ("prob-median-robust", "prob.median", "prob.breakdown", "supports", "The sample median supports resistance to extreme magnitude below its breakdown fraction."),
    ("prob-trim-robust", "prob.trimmed", "prob.estimator", "transforms_to", "Trimming transforms an estimator by removing extremes."),
    ("prob-ecdf-sample", "prob.sample", "prob.empirical-cdf", "transforms_to", "A sample transforms into its empirical CDF."),
    ("prob-rank-nonparam", "prob.rank-test", "prob.nonparametric", "part_of", "Rank tests form one nonparametric method class."),
    ("prob-bootstrap-sample", "prob.bootstrap", "prob.sample", "transforms_to", "Bootstrap resampling transforms an empirical sample into replicate statistics."),
    ("prob-permute-exchange", "prob.exchangeability", "prob.permutation-test", "prerequisite", "Null exchangeability is prerequisite to permutation-test validity."),
    ("info-prob-self", "prob.probability-measure", "info.self-information", "grounds", "Modeled outcome probability grounds self-information."),
    ("info-self-entropy", "info.self-information", "info.entropy", "transforms_to", "Expectation of self-information produces entropy."),
    ("info-joint-conditional", "info.joint-entropy", "info.conditional-entropy", "qualifies", "Joint and marginal entropies qualify conditional entropy."),
    ("info-mutual-conditional", "info.conditional-entropy", "info.mutual-information", "grounds", "Reduction from marginal to conditional entropy grounds mutual information."),
    ("info-kl-mutual", "info.kl-divergence", "info.mutual-information", "implements", "Mutual information is a KL divergence between joint and product marginals."),
    ("info-processing-mutual", "info.data-processing", "info.mutual-information", "qualifies", "The data-processing inequality qualifies dependence after a Markov channel."),
    ("info-source-codeword", "info.source", "info.codeword", "causes", "A source-coding rule maps source outcomes to codewords."),
    ("info-prefix-codeword", "info.prefix-code", "info.codeword", "qualifies", "Prefix freedom qualifies instantaneous codewords."),
    ("info-kraft-prefix", "info.kraft", "info.prefix-code", "qualifies", "Kraft lengths qualify existence of a prefix code."),
    ("info-lossless-code", "info.lossless-compression", "info.codeword", "implements", "A uniquely decodable code implements lossless compression."),
    ("info-typical-entropy", "info.entropy", "info.typical-set", "grounds", "Entropy rate grounds typical-set exponential size."),
    ("info-theorem-entropy", "info.entropy", "info.source-theorem", "grounds", "Entropy rate grounds the asymptotic lossless coding limit."),
    ("info-channel-code", "info.channel-code", "info.channel", "qualifies", "A channel code qualifies transmitted inputs under the channel model."),
    ("info-rate-code", "info.code-rate", "info.channel-code", "measures", "Code rate measures message information per transmitted symbol."),
    ("info-capacity-mutual", "info.mutual-information", "info.capacity", "grounds", "Optimized mutual-information rate grounds memoryless channel capacity."),
    ("info-capacity-theorem", "info.capacity", "info.noisy-channel", "grounds", "Capacity grounds achievable and impossible asymptotic rate regions."),
    ("info-encoder-code", "info.encoder", "info.channel-code", "implements", "An encoder implements message-to-codeword mapping."),
    ("info-decoder-code", "info.decoder", "info.channel-code", "implements", "A decoder implements observation-to-message estimation."),
    ("info-hamming-distance", "info.hamming-distance", "info.minimum-distance", "measures", "Hamming distance measures codeword separation."),
    ("info-distance-correct", "info.minimum-distance", "info.channel-code", "qualifies", "Minimum distance qualifies guaranteed substitution error correction."),
    ("info-parity-syndrome", "info.parity-check", "info.syndrome", "causes", "Applying parity checks to a received word causes its syndrome."),
    ("info-erasure-distance", "info.erasure", "info.minimum-distance", "qualifies", "Known erasure positions qualify recovery bounds differently from unknown substitutions."),
    ("info-soft-decoder", "info.soft-decision", "info.decoder", "qualifies", "Soft likelihoods qualify decoder evidence."),
    ("info-message-source", "info.message", "info.source", "qualifies", "The message set and probabilities qualify an information source."),
    ("info-transmit-channel", "info.transmitter", "info.channel", "causes", "A transmitter injects a coded signal into the channel."),
    ("info-channel-receiver", "info.channel", "info.receiver", "causes", "The channel causes the receiver observation distribution."),
    ("info-noise-channel", "info.noise", "info.channel", "qualifies", "Noise statistics qualify the channel law."),
    ("info-snr-receiver", "info.snr", "info.receiver", "qualifies", "SNR qualifies detector and decoder performance under a noise model."),
    ("info-budget-snr", "info.link-budget", "info.snr", "supports", "A link budget supports predicted received SNR with margin."),
    ("info-symbol-constellation", "info.symbol", "info.constellation", "part_of", "Symbols correspond to constellation points or waveforms."),
    ("info-mod-symbol", "info.modulation", "info.symbol", "transforms_to", "Modulation transforms coded symbols into waveforms."),
    ("info-demod-symbol", "info.demodulation", "info.symbol", "transforms_to", "Demodulation transforms observations into symbol likelihoods."),
    ("info-matched-receiver", "info.matched-filter", "info.receiver", "part_of", "A matched filter forms one receiver detection component."),
    ("info-nyquist-symbol", "info.nyquist", "info.symbol", "qualifies", "Nyquist pulse conditions qualify interference-free decision samples."),
    ("info-sample-signal", "info.sample", "info.sampling-theorem", "part_of", "Uniform samples form the data used by sampling reconstruction."),
    ("info-alias-sampling", "info.aliasing", "info.sampling-theorem", "undercuts", "Aliasing undercuts unique reconstruction after insufficient sampling."),
    ("info-convolution-filter", "info.convolution", "info.filter", "implements", "Convolution implements an LTI digital filter."),
    ("info-fourier-convolution", "info.fourier", "info.convolution", "transforms_to", "Fourier representation transforms convolution into multiplication under theorem conditions."),
    ("info-quantization-sample", "info.quantization", "info.sample", "transforms_to", "Quantization transforms samples into a finite representation."),
    ("info-mac-network", "info.multiple-access", "info.network-source", "part_of", "A multiple-access channel is one network-information topology."),
    ("info-broadcast-network", "info.broadcast-channel", "info.network-source", "part_of", "A broadcast channel is one network-information topology."),
    ("info-relay-network", "info.relay-channel", "info.network-source", "part_of", "A relay channel is one network-information topology."),
    ("info-coding-network", "info.network-coding", "info.network-source", "qualifies", "Intermediate algebraic combination qualifies achievable network rates."),
    ("info-syntax-semantic", "info.syntax-semantics", "info.semantic-content", "qualifies", "Syntactic information quantities do not uniquely determine semantic content."),
    ("info-task-semantic", "info.task-information", "info.semantic-content", "qualifies", "A task and utility qualify relevant semantic information."),
    ("info-ground-semantic", "info.common-ground", "info.semantic-content", "prerequisite", "Shared codebook and context are prerequisites to intended interpretation."),
    ("info-fidelity-truth", "info.misinformation", "info.channel-code", "qualifies", "Channel fidelity qualifies transmission accuracy but not semantic truth."),
    ("bridge-prob-info", "prob.distribution", "info.entropy", "grounds", "A discrete probability distribution grounds Shannon entropy when the logarithm and support conventions align."),
    ("bridge-graph-network", "math.network-flow", "info.network-coding", "analogous_to", "Graph flow and network coding share topology and capacity constraints while coding permits algebraic combination."),
    ("bridge-linear-codes", "math.vector-space", "info.parity-check", "supports", "Linear algebra supports representation and decoding of linear error-correcting codes."),
    ("bridge-calculus-density", "math.integral", "prob.density", "grounds", "Integration of a density over an event grounds its probability."),
]


CONTROLS = [
    ("math-div-zero", "formal-mathematics", "formal-mathematics.arithmetic", MATH_LANES, "Division by zero", "Division by zero must remain undefined rather than receiving a convenient finite answer."),
    ("math-natural-sub", "formal-mathematics", "formal-mathematics.arithmetic", MATH_LANES, "Natural subtraction closure", "Subtracting a larger natural number must not be claimed closed in the naturals without extending the domain."),
    ("math-decimal-exact", "formal-mathematics", "formal-mathematics.arithmetic", MATH_LANES, "Finite decimal is exact real", "A finite machine decimal must not be treated as the exact real value of a nonterminating representation."),
    ("math-percent-base", "formal-mathematics", "formal-mathematics.algebra-word-problems", MATH_LANES, "Missing percent base", "A percentage amount or change must not be computed without identifying its base quantity."),
    ("math-unit-cancel", "formal-mathematics", "formal-mathematics.algebra-word-problems", MATH_LANES, "Incompatible unit equation", "Quantities with incompatible dimensions must not be added merely because their numerical values are available."),
    ("math-word-keyword", "formal-mathematics", "formal-mathematics.algebra-word-problems", MATH_LANES, "Keyword translation", "A word such as more, per, of, or total must not mechanically choose an operation without the full quantity relation."),
    ("math-extraneous", "formal-mathematics", "formal-mathematics.elementary-algebra", MATH_LANES, "Extraneous algebraic solution", "A candidate introduced by squaring, clearing denominators, or other non-equivalent transformation must not survive without checking the original equation and domain."),
    ("math-cancel-domain", "formal-mathematics", "formal-mathematics.elementary-algebra", MATH_LANES, "Cancellation restores excluded point", "Canceling a polynomial factor must not restore a value excluded by the original denominator."),
    ("math-matrix-map", "formal-mathematics", "formal-mathematics.linear-algebra", MATH_LANES, "Matrix is basis-free map", "A matrix must not be treated as the underlying linear map without its domain and codomain bases."),
    ("math-det-size", "formal-mathematics", "formal-mathematics.linear-algebra", MATH_LANES, "Determinant for nonsquare matrix", "A determinant must not be assigned to a nonsquare matrix under the ordinary definition."),
    ("math-group-commute", "formal-mathematics", "formal-mathematics.abstract-algebra", MATH_LANES, "Every group is commutative", "Group multiplication must not be commuted without an abelian hypothesis or element-specific proof."),
    ("math-limit-value", "formal-mathematics", "formal-mathematics.calculus", MATH_LANES, "Limit equals function value", "A finite limit at a point must not imply the function is defined or continuous there."),
    ("math-differentiable-continuous", "formal-mathematics", "formal-mathematics.calculus", MATH_LANES, "Continuity implies differentiability", "Continuity must not be used as sufficient evidence of differentiability."),
    ("math-taylor-equality", "formal-mathematics", "formal-mathematics.calculus", MATH_LANES, "Taylor series always equals function", "An infinitely differentiable function must not be identified with its Taylor series without a vanishing remainder or analyticity result."),
    ("math-cauchy-converge", "formal-mathematics", "formal-mathematics.real-analysis", MATH_LANES, "Cauchy sequence always converges", "A Cauchy sequence must not be claimed to converge inside an incomplete space."),
    ("math-point-uniform", "formal-mathematics", "formal-mathematics.real-analysis", MATH_LANES, "Pointwise equals uniform", "Pointwise convergence must not be substituted for uniform convergence when exchanging limits, continuity, or integrals."),
    ("math-real-complex", "formal-mathematics", "formal-mathematics.complex-analysis", MATH_LANES, "Real differentiability implies holomorphic", "Real differentiability of component functions must not imply complex differentiability without Cauchy-Riemann and regularity conditions."),
    ("math-norm-complete", "formal-mathematics", "formal-mathematics.functional-analysis", MATH_LANES, "Every normed space is complete", "A normed space must not be treated as Banach without a completeness proof."),
    ("math-ode-unique", "formal-mathematics", "formal-mathematics.differential-equations", MATH_LANES, "ODE solution automatically unique", "A differential equation plus initial value must not be assigned a unique solution without theorem conditions."),
    ("math-local-global", "formal-mathematics", "formal-mathematics.optimization", MATH_LANES, "Local optimum is global", "A local optimum must not be reported as global without convexity or another global certificate."),
    ("math-floating-laws", "formal-mathematics", "formal-mathematics.numerical-methods", MATH_LANES, "Floating arithmetic is real arithmetic", "Floating-point addition and multiplication must not be assumed associative or exact as real operations."),
    ("math-tactic-proof", "formal-mathematics", "formal-mathematics.formal-proof", MATH_LANES, "Tactic success bypasses kernel", "A tactic's success message must not replace checking its proof term in the trusted kernel."),
    ("prob-density-point", "probability-statistics", "probability-statistics.random-variables", PROB_LANES, "Density value is point probability", "A continuous density height must not be treated as probability at that exact point."),
    ("prob-zero-impossible", "probability-statistics", "probability-statistics.probability-foundations", PROB_LANES, "Probability zero means impossible", "An event of probability zero must not always be treated as logically impossible in a continuous model."),
    ("prob-uncorrelated-independent", "probability-statistics", "probability-statistics.random-variables", PROB_LANES, "Zero correlation means independence", "Zero covariance must not be treated as independence without additional distribution structure."),
    ("prob-likelihood-prob", "probability-statistics", "probability-statistics.bayesian-inference", PROB_LANES, "Likelihood is parameter probability", "A likelihood curve must not be normalized or interpreted as a posterior without a prior and evidence normalization."),
    ("prob-credible-confidence", "probability-statistics", "probability-statistics.frequentist-inference", PROB_LANES, "Confidence equals credible interval", "A confidence interval's repeated-sampling coverage must not be reported as posterior probability for the realized fixed parameter."),
    ("prob-p-null", "probability-statistics", "probability-statistics.frequentist-inference", PROB_LANES, "P value is probability null is true", "A p value must not be interpreted as the posterior probability that the null hypothesis is true."),
    ("prob-significant-important", "probability-statistics", "probability-statistics.frequentist-inference", PROB_LANES, "Statistical significance means importance", "Rejecting a null must not establish a practically important effect or acceptable uncertainty."),
    ("prob-sample-size", "probability-statistics", "probability-statistics.frequentist-inference", PROB_LANES, "Large sample removes bias", "A large sample must not be treated as correcting selection, measurement, confounding, or model bias."),
    ("prob-unit-count", "probability-statistics", "probability-statistics.experimental-design", PROB_LANES, "Measurements equal experimental units", "Repeated measurements on one assigned unit must not be counted as independent treatment replication."),
    ("prob-association-cause", "probability-statistics", "probability-statistics.causal-inference", PROB_LANES, "Association is causal effect", "An adjusted association must not be called causal without exchangeability, positivity, consistency, and design evidence."),
    ("prob-markov-true", "probability-statistics", "probability-statistics.stochastic-processes", PROB_LANES, "Observed variable is Markov state", "A measured state must not be assumed Markov when omitted history or latent variables predict the future."),
    ("prob-backtest-leak", "probability-statistics", "probability-statistics.time-series", PROB_LANES, "Future-aware backtest", "A forecast backtest must not use revised, normalized, selected, or labeled data unavailable at each historical cutoff."),
    ("prob-aleatoric-fixed", "probability-statistics", "probability-statistics.uncertainty-quantification", PROB_LANES, "Aleatoric uncertainty is immutable", "A variability component must not be labeled irreducible without conditioning on all relevant observable information and task choices."),
    ("prob-calibration-accuracy", "probability-statistics", "probability-statistics.calibration", PROB_LANES, "Calibration means accuracy", "A calibrated predictor can be uninformative, and an accurate classifier can be poorly calibrated; neither property implies the other."),
    ("prob-outlier-delete", "probability-statistics", "probability-statistics.robust-statistics", PROB_LANES, "Delete every outlier", "An unusual observation must not be deleted before checking measurement, protocol, population, and mechanism."),
    ("prob-bootstrap-any", "probability-statistics", "probability-statistics.nonparametric", PROB_LANES, "Naive bootstrap fits dependence", "IID resampling must not be applied to clustered, temporal, spatial, or network data without a structure-preserving design."),
    ("info-entropy-meaning", "information-communication", "information-communication.semantic-information", INFO_LANES, "Entropy measures meaning", "Shannon entropy must not be presented as semantic truth, relevance, understanding, or value without a separate model."),
    ("info-kl-metric", "information-communication", "information-communication.entropy-information", INFO_LANES, "KL divergence is a distance metric", "KL divergence must not be treated as symmetric or satisfying the triangle inequality."),
    ("info-compress-random", "information-communication", "information-communication.source-coding", INFO_LANES, "Every file can be shortened losslessly", "A one-to-one lossless code cannot shorten every possible input of a fixed maximum length without lengthening or excluding others."),
    ("info-capacity-speed", "information-communication", "information-communication.channel-coding", INFO_LANES, "Capacity is one implementation speed", "Channel capacity must not be treated as the throughput of a finite code, hardware implementation, or latency-constrained link."),
    ("info-syndrome-error", "information-communication", "information-communication.error-correction", INFO_LANES, "Syndrome uniquely identifies error", "A syndrome must not be treated as one unique error pattern without a correctable-set and decoder assumption."),
    ("info-snr-quality", "information-communication", "information-communication.communication-systems", INFO_LANES, "Higher SNR guarantees better system", "SNR alone must not establish decoding quality without bandwidth, interference, synchronization, channel, code, and receiver context."),
    ("info-sampling-any", "information-communication", "information-communication.signal-processing", INFO_LANES, "Sampling theorem applies to arbitrary signal", "Perfect reconstruction must not be claimed for an unbounded, non-bandlimited, noisy, jittered, or finitely observed signal under the ideal theorem alone."),
    ("info-reliable-true", "information-communication", "information-communication.semantic-information", INFO_LANES, "Reliable transmission proves truth", "A message decoded without bit error must not be treated as factually true or nonmanipulative."),
]


WORKED_EXAMPLES = [
    ("math", "linear-equation", "Linear-equation derivation", "From three x plus five equals twenty, subtract five from both sides, divide by nonzero three, obtain x equals five, and substitute five into the original equation.", "formal-mathematics.elementary-algebra", MATH_LANES, MATH_SOURCES, "formal"),
    ("math", "rate-distance", "Rate-distance word problem", "A vehicle travels at a constant sixty kilometers per hour for two and one-half hours; compatible multiplication yields one hundred fifty kilometers and the units reduce correctly.", "formal-mathematics.algebra-word-problems", MATH_LANES, MATH_SOURCES, "formal"),
    ("math", "percent-change", "Percent increase and decrease", "Increasing one hundred by twenty percent gives one hundred twenty; decreasing that result by twenty percent gives ninety-six because the second base differs.", "formal-mathematics.algebra-word-problems", MATH_LANES, MATH_SOURCES, "formal"),
    ("math", "matrix-kernel", "Linear-map kernel example", "For the map sending x comma y to x plus y, the kernel contains all pairs t comma negative t and has dimension one while the image has dimension one.", "formal-mathematics.linear-algebra", MATH_LANES, MATH_SOURCES, "formal"),
    ("math", "chain-rule", "Chain-rule derivation", "For the square of three x plus one, the outer derivative contributes two times the inner value and the inner derivative contributes three, giving six times three x plus one.", "formal-mathematics.calculus", MATH_LANES, MATH_SOURCES, "formal"),
    ("math", "induction-sum", "Induction proof skeleton", "The base verifies the first finite sum, and the step adds the next integer to the assumed n formula and algebraically reaches the n plus one formula.", "formal-mathematics.formal-proof", MATH_LANES, MATH_SOURCES, "formal"),
    ("prob", "bayes-screen", "Bayesian screening example", "A posterior positive-case probability combines prevalence, sensitivity, and false-positive probability rather than equating sensitivity with positive predictive value.", "probability-statistics.bayesian-inference", PROB_LANES, PROB_SOURCES, "established"),
    ("prob", "cluster-unit", "Experimental-unit example", "Ten readings from each of five independently randomized devices provide five treatment units, not fifty independent treatment assignments.", "probability-statistics.experimental-design", PROB_LANES, PROB_SOURCES, "established"),
    ("prob", "calibration", "Forecast calibration example", "Across a predeclared bin of events assigned about seventy percent, roughly seven tenths occur within sampling uncertainty; sharpness is reported separately.", "probability-statistics.calibration", PROB_LANES, PROB_SOURCES, "established"),
    ("prob", "causal-dag", "Confounding example", "A common cause influences both treatment and outcome, so their observed association mixes paths until a justified design blocks the backdoor path.", "probability-statistics.causal-inference", PROB_LANES, PROB_SOURCES, "established"),
    ("info", "prefix-code", "Prefix-code example", "Codewords zero, ten, and eleven have no codeword prefixing another, so concatenated symbols decode left to right without separators.", "information-communication.source-coding", INFO_LANES, INFO_SOURCES, "formal"),
    ("info", "hamming-code", "Minimum-distance example", "A binary code with minimum Hamming distance three detects up to two substitutions and corrects one under nearest-codeword decoding.", "information-communication.error-correction", INFO_LANES, INFO_SOURCES, "formal"),
    ("info", "sampling-alias", "Aliasing example", "Two sinusoids separated by an integer multiple of sampling frequency produce identical sample sequences, demonstrating nonunique reconstruction without a band limit.", "information-communication.signal-processing", INFO_LANES, INFO_SOURCES, "formal"),
    ("info", "channel-truth", "Channel and truth boundary", "An error-correcting decoder recovers a false sentence exactly; transport reliability passes while semantic truth remains unsupported.", "information-communication.semantic-information", INFO_LANES, INFO_SOURCES, "established"),
]


def split_for(index: int, *, root: bool = False) -> str:
    if root:
        return "train"
    if index % 43 == 0:
        return "cross_domain_holdout"
    if index % 37 == 0:
        return "sealed_test"
    if index % 29 == 0:
        return "validation"
    return "train"


def edge_split_for(index: int) -> str:
    if index and index % 41 == 0:
        return "cross_domain_holdout"
    if index and index % 31 == 0:
        return "sealed_test"
    if index and index % 23 == 0:
        return "validation"
    return "train"


def make_base(
    identifier: str,
    domain: str,
    subject: str,
    lanes: list[str],
    sources: list[str],
    split: str,
    kind: str,
    epistemic: str,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "record_id": identifier,
        "world_id": WORLD,
        "domain_id": domain,
        "subject_id": subject,
        "lanes": sorted(set(lanes)),
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"],
        "source_ids": sorted(set(sources)),
        "scope": "formal mathematics, probability-statistics, and information-communication foundation tranche",
        "limitations": [
            "Finite worked examples illustrate exact mechanisms and do not exhaust unbounded mathematical domains.",
            "Statistical conclusions retain sampling, measurement, model, population, and causal-identification assumptions.",
            "Advanced theorems and the full MSC discovery frontier remain open until separately authored, proved, trained, and sealed.",
        ],
        "as_of": "2026-09-03",
        "version_boundary": "math-probability-information-v0",
        "split_group": identifier,
        "split": split,
        "tags": ["foundation", domain],
    }


def owner_for_prefix(prefix: str) -> tuple[str, list[str], list[str], str]:
    if prefix == "math":
        return "formal-mathematics", MATH_LANES, MATH_SOURCES, "formal"
    if prefix == "prob":
        return "probability-statistics", PROB_LANES, PROB_SOURCES, "established"
    return "information-communication", INFO_LANES, INFO_SOURCES, "formal"


def relation_context(identifier: str, source: str, target: str) -> tuple[str, str, list[str], list[str], str]:
    prefixes = {endpoint.split(".", 1)[0] for endpoint in (source, target)}
    if identifier.startswith("bridge-") or len(prefixes) > 1:
        return (
            "information-communication",
            "information-communication.entropy-information",
            sorted(set(MATH_LANES + PROB_LANES + INFO_LANES)),
            sorted(set(MATH_SOURCES + PROB_SOURCES + INFO_SOURCES)),
            "established",
        )
    prefix = next(iter(prefixes))
    domain, lanes, sources, epistemic = owner_for_prefix(prefix)
    subject = {
        "math": "formal-mathematics.formal-proof",
        "prob": "probability-statistics.probability-foundations",
        "info": "information-communication.entropy-information",
    }[prefix]
    return domain, subject, lanes, sources, epistemic


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    groups = [
        ("math", "formal-mathematics", MATH, MATH_LANES, MATH_SOURCES, "formal"),
        ("prob", "probability-statistics", PROBABILITY, PROB_LANES, PROB_SOURCES, "established"),
        ("info", "information-communication", INFORMATION, INFO_LANES, INFO_SOURCES, "formal"),
    ]
    roots = {"math": "math.root", "prob": "prob.root", "info": "info.root"}

    for prefix, domain, entries, lanes, sources, epistemic in groups:
        for index, (identifier, label, statement, subject) in enumerate(entries):
            node_id = f"{prefix}.{identifier}"
            records.append(
                {
                    **make_base(
                        node_id, domain, subject, lanes, sources,
                        split_for(index, root=identifier == "root"), "concept", epistemic,
                    ),
                    "label": label,
                    "statement": statement,
                    "aliases": [label.lower()],
                }
            )
            if identifier == "root":
                continue
            membership_id = f"mpi.membership.{prefix}.{identifier}"
            records.append(
                {
                    **make_base(
                        membership_id, domain, subject, lanes, sources,
                        edge_split_for(index), "relation", epistemic,
                    ),
                    "label": f"{label} world membership",
                    "statement": f"{label} is a distinct component of the {domain} world with explicit domain, assumptions, and proof or evidence conditions.",
                    "aliases": [],
                    "relation": {
                        "source_node": node_id,
                        "target_node": roots[prefix],
                        "kind": "part_of",
                        "polarity": 1,
                        "direction": "forward",
                        "conditions": ["the declared mathematical structure or statistical model applies"],
                        "exceptions": [],
                    },
                    "coverage_axes": ["primitives_invariants", "within_domain_composition"],
                }
            )

    splitter = RelationSplitter(
        [kind for _identifier, _source, _target, kind, _statement in RELATIONS],
        cross_plan=[
            identifier.startswith("bridge-")
            for identifier, _source, _target, _kind, _statement in RELATIONS
        ],
    )
    for identifier, source_node, target_node, kind, statement in RELATIONS:
        domain, subject, lanes, sources, epistemic = relation_context(identifier, source_node, target_node)
        records.append(
            {
                **make_base(
                    f"mpi.relation.{identifier}", domain, subject, lanes, sources,
                    splitter.split(kind),
                    "relation",
                    epistemic,
                ),
                "label": identifier.replace("-", " "),
                "statement": statement,
                "aliases": [],
                "relation": {
                    "source_node": source_node,
                    "target_node": target_node,
                    "kind": kind,
                    "polarity": -1 if kind in {"inhibits", "prevents", "contradicts", "undercuts"} else 1,
                    "direction": "forward",
                    "conditions": ["all declared domains, nonzero conditions, model assumptions, and theorem hypotheses hold"],
                    "exceptions": [],
                },
                "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"],
            }
        )

    control_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, domain, subject, lanes, label, statement) in enumerate(CONTROLS):
        record_id = f"mpi.control.{identifier}"
        records.append(
            {
                **make_base(
                    record_id, domain, subject, lanes, [], control_splits[index % 4],
                    "synthetic_control", "synthetic_control",
                ),
                "label": label,
                "statement": statement,
                "aliases": [label.lower()],
                "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
                "synthetic": True,
                "tags": ["negative-control", domain],
            }
        )

    example_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (prefix, identifier, label, statement, subject, lanes, sources, epistemic) in enumerate(WORKED_EXAMPLES):
        domain, _owner_lanes, _owner_sources, _owner_epistemic = owner_for_prefix(prefix)
        split = example_splits[index % 4]
        node_id = f"mpi.example.{prefix}.{identifier}"
        records.append(
            {
                **make_base(node_id, domain, subject, lanes, sources, split, "worked_example", epistemic),
                "label": label,
                "statement": statement,
                "aliases": [],
                "coverage_axes": ["applications_toolchains", "deductions_predictions_execution", "within_domain_composition"],
                "tags": ["worked-example", domain],
            }
        )
        membership_id = f"mpi.example-membership.{prefix}.{identifier}"
        records.append(
            {
                **make_base(membership_id, domain, subject, lanes, sources, split, "relation", epistemic),
                "label": f"{label} membership",
                "statement": f"The {label.lower()} operationalizes one bounded formal or inferential mechanism.",
                "aliases": [],
                "relation": {
                    "source_node": node_id,
                    "target_node": roots[prefix],
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the example remains illustrative and all stated assumptions hold"],
                    "exceptions": [],
                },
                "coverage_axes": ["applications_toolchains", "within_domain_composition"],
            }
        )

    # Bounded facts exercise exact arithmetic admission, but the laws and exact
    # executor—not this finite table—cover arbitrary integer inputs.
    for left in range(13):
        for right in range(13):
            identifier = f"mpi.table.multiply.{left}.{right}"
            records.append(
                {
                    **make_base(
                        identifier, "formal-mathematics", "formal-mathematics.arithmetic",
                        MATH_LANES, MATH_SOURCES, "train", "worked_example", "formal",
                    ),
                    "label": f"{left} times {right}",
                    "statement": f"Exact integer multiplication gives {left} times {right} equals {left * right}.",
                    "aliases": [f"{left} multiplied by {right}"],
                    "coverage_axes": ["deductions_predictions_execution", "applications_toolchains"],
                    "tags": ["arithmetic-table", "operator-multiply", "formal-mathematics"],
                }
            )
            relation_id = f"mpi.table-membership.multiply.{left}.{right}"
            records.append(
                {
                    **make_base(
                        relation_id, "formal-mathematics", "formal-mathematics.arithmetic",
                        MATH_LANES, MATH_SOURCES, "train", "relation", "formal",
                    ),
                    "label": f"{left} times {right} multiplication membership",
                    "statement": f"The exact fact for {left} times {right} is one bounded worked instance of integer multiplication.",
                    "aliases": [],
                    "relation": {
                        "source_node": identifier,
                        "target_node": "math.multiplication",
                        "kind": "part_of",
                        "polarity": 1,
                        "direction": "forward",
                        "conditions": ["integer arithmetic applies"],
                        "exceptions": [],
                    },
                    "coverage_axes": ["deductions_predictions_execution", "within_domain_composition"],
                    "tags": ["arithmetic-table", "operator-multiply", "formal-mathematics"],
                }
            )
    for divisor in range(1, 13):
        for quotient in range(13):
            dividend = divisor * quotient
            identifier = f"mpi.table.divide.{dividend}.{divisor}"
            records.append(
                {
                    **make_base(
                        identifier, "formal-mathematics", "formal-mathematics.arithmetic",
                        MATH_LANES, MATH_SOURCES, "train", "worked_example", "formal",
                    ),
                    "label": f"{dividend} divided by {divisor}",
                    "statement": f"Exact integer division gives {dividend} divided by nonzero {divisor} equals {quotient}.",
                    "aliases": [f"{dividend} over {divisor}"],
                    "coverage_axes": ["deductions_predictions_execution", "applications_toolchains"],
                    "tags": ["arithmetic-table", "operator-divide", "formal-mathematics"],
                }
            )
            relation_id = f"mpi.table-membership.divide.{dividend}.{divisor}"
            records.append(
                {
                    **make_base(
                        relation_id, "formal-mathematics", "formal-mathematics.arithmetic",
                        MATH_LANES, MATH_SOURCES, "train", "relation", "formal",
                    ),
                    "label": f"{dividend} divided by {divisor} division membership",
                    "statement": f"The exact fact for {dividend} divided by {divisor} is one bounded worked instance of nonzero-divisor integer division.",
                    "aliases": [],
                    "relation": {
                        "source_node": identifier,
                        "target_node": "math.division",
                        "kind": "part_of",
                        "polarity": 1,
                        "direction": "forward",
                        "conditions": ["integer arithmetic and a nonzero divisor apply"],
                        "exceptions": [],
                    },
                    "coverage_axes": ["deductions_predictions_execution", "within_domain_composition"],
                    "tags": ["arithmetic-table", "operator-divide", "formal-mathematics"],
                }
            )

    return sorted(records, key=lambda record: record["record_id"])


def main() -> int:
    records = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )
    counts: dict[str, int] = {}
    kinds: dict[str, int] = {}
    for record in records:
        counts[record["split"]] = counts.get(record["split"], 0) + 1
        kinds[record["record_kind"]] = kinds.get(record["record_kind"], 0) + 1
    print(f"wrote {OUTPUT} with {len(records)} records")
    print(f"splits: {dict(sorted(counts.items()))}")
    print(f"kinds: {dict(sorted(kinds.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
