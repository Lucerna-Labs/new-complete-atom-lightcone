# Advanced worlds authoring log

Task source: `/home/jesse/Downloads/AUTHORING-PROMPT-ADVANCED-WORLDS.md`, byte-identical to the original prompt in `a-rag-atom/experiments/thermodynamic-context/docs/`.
Review source: `a-rag-atom/experiments/thermodynamic-context/docs/REVIEW-FIXES-2026-10-02.md`.
Date: 2026-10-02 (America/New_York).

## Contract and initial state

Step 0 repairs all 13 reviewed worlds on their owning branches, one commit per world. Then create `authoring/advanced-worlds` from the repaired sweep and author the 70 catalog rows in order, bridge last. All 70 subject IDs exist. Keep the passive Lightcone architecture; no import into AtomDB before Claude review. No merge, rebase, push, deletion of files, catalog/trainer/shared-builder edits, or generated-curriculum commits.

Initial sweep HEAD `5fea894`; Rust branch HEAD `94f950a`; kitchen HEAD `78bd3b2`. The review header transposes the Rust hash as `94bd2fa`; the named branch and reviewed content match the intended Rust world. Only untracked curricula existed at preflight.

Step 0 uses the original worlds' scope and records count reductions rather than padding to the new-world minimum. The 24 probes and five task/reference/pitfall triples are required for each NEW advanced world, not retroactively for Step 0.

Commit hashes are filled at the next log checkpoint so a commit never claims to contain its own hash. Each pending hash is identified by its exact unique commit title.

## Step 0: quantum-causation-v0

Commit: `5eadedc` (`Review fixes: quantum`).
Counts: 40 concepts; 28 authored relations (causes 2, enables 10, prevents 2, inhibits 2, prerequisite 3, predicts 9); 5 myths; 3 boundaries; 4 examples; 4 controls. All authored relations use a causal kind. Probes/tasks: not applicable to Step 0.

Self-review (passes overlap; counts are not additive):
- Direction: 2 reversals, Born amplitudes → probabilities and probabilities → outcome distribution; 5 target/source repairs (frequency, sharp classical orbit, normalization, remote signal, momentum spread).
- Counterexamples: all 28 retained/new edges carry explicit conditions; qualified single-photon emission, Bell-state violation, allowed transitions, orbital approximation, closed-system dynamics, and oscillator ground state. Removed 6 unsupported/interpretation-dependent edges in addition to duplicate/category removals below.
- Version/standard: 28 edges checked; no software versions apply. Physical idealizations are local to each edge.
- Duplicate/circularity/category: 8 removals/ID replacements; no repeated pair, repeated condition, self-loop, missing endpoint label, or missing kind verb remains.
- Myths: 5 reviewed; 1 rewritten to distinguish decoherence from outcome selection. Two boundary claims tightened.
- Count: 26 existing IDs changed, 14 old IDs absent, 2 new IDs; net 40 → 28 relations, intentionally unpadded.

Dropped/replaced old IDs and reasons:
- `planck-causes-photonenergy`: replaced with frequency → energy prediction; constant is not a cause.
- `quantization-causes-levels`: definition restatement.
- `photoelectric-causes-duality`, `duality-prereq-slits`, `interference-predicts-duality`: evidence is not a physical cause/necessary precondition.
- `slits-cause-interference`: experiment-as-source removed; coherent superposition edge states the no-which-path condition.
- `slits-enable-whichpath`: experiment setup is not a general mechanism.
- `schrodinger-enables-unitary`: same closed-system evolution in different words.
- `workfunction-prereq-photoelectric`: duplicate ordered pair with threshold edge.
- `planck-prereq-quantization`: a nonzero constant does not specify a discrete spectrum.
- `superposition-prereq-entanglement`: basis-dependent wording fails for mixed-state entanglement.
- `collapse-interrupts-evolution`, `collapse-enables-record`: conditional state update is not a dynamical interruption or solution to macroscopic outcomes.
- `zeropoint-inhibits-stillness`: target was macroscopic classical behavior, not ground-state energy.

New concepts distinguish photon frequency, probability normalization, exact classical orbits, remote signalling, photovoltaic conversion and nuclear precession. Solar-cell and MRI examples corrected. Work function and spin definitions corrected. Open doubts: no unresolved factual edge retained; macroscopic decoherence explicitly does not solve the measurement-outcome problem. This is self-review, not Claude acceptance.

Sources added (citation metadata only; no source text copied):
- `griffiths-schroeter-qm-3e`: Griffiths and Schroeter, Introduction to Quantum Mechanics, third edition (2018), publisher identity verified at https://www.cambridge.org/highereducation/books/introduction-to-quantum-mechanics/990799CA07A83FC5312402AF6860311E
- `zurek-decoherence-2003`: Zurek, Reviews of Modern Physics 75, 715–775 (2003), https://arxiv.org/abs/quant-ph/0105127v3
OpenStax was consulted during discovery but excluded from registered/copyable material because its current footer restricts AI ingestion. Original factual authoring uses the registered canonical citation lanes.

Four checks (current source):

```
$ python3 tools/build_quantum_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/quantum-causation-v0/foundations.jsonl with 146 records
splits: {'cross_domain_holdout': 5, 'sealed_test': 14, 'train': 112, 'validation': 15}
kinds: {'boundary': 3, 'concept': 41, 'counterexample': 5, 'relation': 89, 'synthetic_control': 4, 'worked_example': 4}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id quantum-causation-v0
{
  "schema_version": 1,
  "world_id": "quantum-causation-v0",
  "adapter_independent": true,
  "record_count": 146,
  "node_count": 57,
  "edge_count": 89,
  "negative_pair_count": 4,
  "domains": [
    "quantum-science"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "cc7acabfedccff6b9b25daf0231281ab77a5cac8e90d28a2646fc369b5b37be9",
    "lexicon.json": "11643f0d4841dbfe8952d0e7efe05ec701f34e6bcd237a646f0839245362dd64",
    "nodes.jsonl": "c79c5600be8fdad4d1666ee5b932cd768c74753ac39a746f43ab25ff8f7209a0",
    "records.jsonl": "a299ed8c6a993da3b0d99dc92760cf17f90a1299f0bde6ad26ebde089db72a2f",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "65ba5a6575b3616a20b95145ffe2fa6aeb9a4db70ce4e3dfe66226b5f0d46a3f",
    "split-manifest.json": "791c63f3b5f3c90b493c7612179b9653a5d8174aadfe3446043b6c962e718455",
    "training-graph.json": "d224c6f3c9a75334be2395f1745d6b7b567e844053b06b2ec0a8b1c4d97d3c9b"
  }
}
exit: 0
```

## Step 0: algebra-causation-v0

Commit: `5300627` (`Review fixes: algebra`).
Counts: 33 concepts, 26 relations, 5 myths, 5 boundaries, 5 examples, 6 controls.
Relations by kind: {"enables": 7, "predicts": 16, "prerequisite": 2, "prevents": 1}.
Probes/tasks: not applicable to Step 0. Sources added: none; existing mathlib4 (and existing NIST DLMF where named) retained.

Self-review: all 26 final edges revised in the direction and counterexample passes (formal implications use predicts; inverse and subgroup prerequisites point from identity to dependent concept). 15 redundant/invalid edges dropped, 14 revised IDs renamed, 12 IDs retained. Version pass: 0 software-version changes; finite groups, field, faithfulness and nonzero hypotheses specified. Myth pass: 5 reviewed, 3 corrected. Count pass: 41 → 26 without padding. Duplicate pass: 0 final duplicate pairs/conditions.

True drops, one reason per ID:
- axioms-enable-identity: identity already an axiom.
- axioms-enable-inverse: inverse already an axiom.
- associativity-enables-axioms: part of definition, not mechanism.
- commutativity-causes-abelian: abelian definition restated.
- generator-causes-cyclic: cyclic definition restated.
- ring-enables-additive-group: ring axiom restated.
- field-enables-inverse: field axiom restated.
- domain-prevents-zerodivisor: domain definition restated.
- basis-predicts-dimension: dimension defined by basis cardinality.
- permutations-cause-symmetric: symmetric group defined by permutations.
- vectorspace-enables-linearmap: definitional typing.
- generator-causes-subgroup: generator already spans whole group.
- cosets-prereq-quotient: quotient elements are defined as cosets.
- homomorphism-prereq-kernel: kernel typing restated.
- ring-prevents-guaranteed-inverse: lack of guarantee moved to boundary.

Specific repairs include faithful action, permutation LCM, unique cyclic subgroup per divisor, Fermat p prime and p not dividing a, field 1 != 0 and a toy modulo-10 checksum with no Fermat dependency. Primary verification: mathlib GroupTheory/Perm/Cycle/Type, SpecificGroups/Cyclic/Basic and GroupAction/Basic. All final edges reviewed for direction, counterexamples, theorem hypotheses and duplicates. Parent checked every final relation; structural audit passed for labels/verbs/endpoints/unique ordered pairs/unique conditions. Open doubts: no unresolved mathematical claim identified; independent Claude review remains pending.

Four checks:

```
$ python3 tools/build_algebra_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/algebra-causation-v0/foundations.jsonl with 143 records
splits: {'cross_domain_holdout': 6, 'sealed_test': 13, 'train': 107, 'validation': 17}
kinds: {'boundary': 5, 'concept': 34, 'counterexample': 5, 'relation': 88, 'synthetic_control': 6, 'worked_example': 5}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id algebra-causation-v0
{
  "schema_version": 1,
  "world_id": "algebra-causation-v0",
  "adapter_independent": true,
  "record_count": 143,
  "node_count": 55,
  "edge_count": 88,
  "negative_pair_count": 6,
  "domains": [
    "formal-mathematics"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "70bbb047eef688440bac97acef774cda7b3a241df3b9d2bc99c30ed48ca07428",
    "lexicon.json": "9e5a2ab8ca8bf6038795932ee5863bb024f692e6990bb69236e9b9e64d8541da",
    "nodes.jsonl": "0f89e1b653974fa3344160fb12d7560c012d4463e15ad75024a908070908eb54",
    "records.jsonl": "02ab24e30ec032db4639c54afbf71f8e10c19171888e188cc8da914669f090f4",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "1a2648c21c25c3889d15861f6e7c17e885fc99c4795bedb2d4bea9c160c500b5",
    "split-manifest.json": "c4fbe260e4fe93abeebe69562920bd97fa89b2823c570441c5676f51798878bb",
    "training-graph.json": "3cf1b91fa3378a0796ebe7df33a1c50b010b56ffd2d4de0557bfe97cb6a7afcc"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
algebra-causation-v0 | Cyclic group -> predicts -> Subgroup | G is a finite cyclic group of order n >= 1 and d is a positive divisor of n
algebra-causation-v0 | Lagrange theorem on subgroups -> predicts -> Subgroup | H is a subgroup of a finite group G; this statement does not assert a subgroup for every divisor
algebra-causation-v0 | Cosets of a subgroup -> enables -> Lagrange theorem on subgroups | G is finite and the distinct left cosets of H partition G, each with |H| elements
algebra-causation-v0 | Normal subgroup -> enables -> Quotient group | H is normal in a group G and multiplication on G/H is induced from G
algebra-causation-v0 | Group homomorphism -> predicts -> Subgroup | phi maps a group G to a group K and preserves their binary operations
algebra-causation-v0 | Kernel of a homomorphism -> predicts -> Group homomorphism | phi:G->K is a group homomorphism and ker(phi) = {e_G}
algebra-causation-v0 | Kernel of a homomorphism -> predicts -> Normal subgroup | phi:G->K preserves group multiplication and ker(phi) is the preimage of e_K
algebra-causation-v0 | Group isomorphism -> predicts -> Order of an element | phi:G->K is a bijective group homomorphism and g belongs to G, including the infinite-order case
algebra-causation-v0 | Zero divisor -> prevents -> Field axioms | a and b are nonzero elements of a unital commutative ring and ab = 0
algebra-causation-v0 | Field axioms -> predicts -> Integral domain | F is a field with 1 != 0, so multiplying ab = 0 by a nonzero a inverse forces b = 0
algebra-causation-v0 | Ring axioms -> enables -> Polynomial ring | R is a unital commutative ring and polynomials in one indeterminate have finite coefficient support
algebra-causation-v0 | Basis of a vector space -> predicts -> Vector space | B is a linearly independent spanning set of a vector space V over a fixed field F
algebra-causation-v0 | Linear map -> predicts -> Vector space | T:V->W is linear over one field F and its image inherits addition and scalar multiplication from W
algebra-causation-v0 | Group action on a set -> enables -> Symmetric group | G acts faithfully on a finite set X: only e_G fixes every point of X
algebra-causation-v0 | Dihedral symmetry of a square -> enables -> Group action on a set | the eight Euclidean isometries preserving a nondegenerate square act by their vertex permutations
algebra-causation-v0 | Modular arithmetic -> predicts -> Cyclic group | n is a positive integer and addition is the induced operation on Z/nZ
algebra-causation-v0 | Lagrange theorem on subgroups -> predicts -> Fermat little theorem | p is prime, a is an integer, p does not divide a, and (Z/pZ)^* has order p-1
algebra-causation-v0 | Modular arithmetic -> predicts -> Abelian group | n >= 1 is an integer and residues modulo n inherit the commutative addition of integers
algebra-causation-v0 | Group homomorphism -> enables -> Quotient group | phi:G->K is a group homomorphism and the quotient uses ker(phi), not an arbitrary subgroup
algebra-causation-v0 | Identity element -> prerequisite -> Inverse element | in a monoid the chosen identity e is used in both equations gh = hg = e
algebra-causation-v0 | Identity element -> prerequisite -> Subgroup | H is a subset of a group G and must contain e_G to qualify as a subgroup of G
algebra-causation-v0 | Dimension of a space -> predicts -> Vector space | V and W are finite-dimensional vector spaces over the same field F and dim_F(V) = dim_F(W)
algebra-causation-v0 | Permutation of elements -> predicts -> Order of an element | the permutation acts on a finite nonempty set; fixed points count as length-one cycles
algebra-causation-v0 | Field axioms -> enables -> Vector space | F is a field, n is a nonnegative integer, and scalars act coordinatewise on F^n
algebra-causation-v0 | Lagrange theorem on subgroups -> predicts -> Order of an element | g belongs to a finite group G and the subgroup generated by g has order ord(g)
algebra-causation-v0 | Abelian group -> predicts -> Normal subgroup | H is any subgroup of an abelian group G, so ghg^(-1) = h for g in G and h in H
```

## Step 0: calculus-causation-v0

Commit: `94c115b` (`Review fixes: calculus`).
Counts: 31 concepts, 28 relations, 6 myths, 6 boundaries, 6 examples, 8 controls.
Relations by kind: {"enables": 3, "predicts": 23, "prerequisite": 2}.
Probes/tasks: not applicable to Step 0. Sources added: none; existing mathlib4 (and existing NIST DLMF where named) retained.

Self-review: all 28 final edges revised in the direction and counterexample passes; four necessary/sufficient arrows corrected for critical points and derivative sign changes. 13 true drops, 18 renamed/retargeted IDs, 10 retained IDs. Version pass: 0 software-version changes; real/complex domains, interior points, integrability, differentiability and continuity made explicit. Myth pass: 5 originals reviewed, 2 corrected, 1 smooth-not-analytic myth added. Count pass: 41 → 28 without padding. Duplicate pass: 0 final duplicate pairs/conditions.

True drops:
- limit-enables-derivative: difference-quotient limit is derivative definition.
- derivative-predicts-instant: same rate concept at both ends.
- integral-causes-area: duplicate; retained integral-predicts-area with nonnegative integrable f.
- remainder-predicts-error: subsumed by corrected Taylor remainder prerequisite.
- linear-enables-differential: definition dependency.
- limit-enables-continuity: continuity definition restated.
- differentiability-enables-tangent: duplicates retained derivative/tangent computation.
- inflection-causes-bend-flip: invalid converse/circular definition.
- antiderivative-prereq-ftc: a closed-form prerequisite is false.
- riemann-prereq-integral: duplicate Riemann/integral pair merged.
- integral-causes-net-change: wrong differential target; integrals do not cause changes.
- derivative-prereq-second: typing definition.
- limit-prereq-riemann: finite Riemann sums need no limit.

Specific repairs include |r| < 1, remainder → 0 for Taylor equality, dy distinct from approximation error, sign changes → extrema, and endpoint checks. Primary verification: mathlib Analysis/Calculus/{Deriv/Basic,MeanValue,Taylor} and MeasureTheory/Integral/IntervalIntegral/FundThmCalculus. All final edges reviewed for direction, counterexamples, theorem hypotheses and duplicates. Parent checked every final relation; structural audit passed for labels/verbs/endpoints/unique ordered pairs/unique conditions. Open doubts: no unresolved mathematical claim identified; independent Claude review remains pending.

Four checks:

```
$ python3 tools/build_calculus_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/calculus-causation-v0/foundations.jsonl with 152 records
splits: {'cross_domain_holdout': 6, 'sealed_test': 17, 'train': 105, 'validation': 24}
kinds: {'boundary': 6, 'concept': 32, 'counterexample': 6, 'relation': 94, 'synthetic_control': 8, 'worked_example': 6}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id calculus-causation-v0
{
  "schema_version": 1,
  "world_id": "calculus-causation-v0",
  "adapter_independent": true,
  "record_count": 152,
  "node_count": 58,
  "edge_count": 94,
  "negative_pair_count": 8,
  "domains": [
    "formal-mathematics"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "651c491162c5422ae2f0e8cbe9f5057dffb186a8541006f5c84cb0e890dbc6e6",
    "lexicon.json": "c7f6f5e6de0834224bec7722348040057dfeea99735ceea40524caf20b033662",
    "nodes.jsonl": "697df7a6d2974635ae654f7ae94de71e99cf67c0b751edc9b9c3d3401cad2db2",
    "records.jsonl": "8165d94d7b50ad30112a9f0b5fb29542e1444ea2827e74976566b6793636cb6d",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "0253ecddd3e7ae67cd5ea828cf377b76242fcf366f01b68bed284730ca807c27",
    "split-manifest.json": "2950e8b0ba69ccab03d479e25d40bfed366ea81b2aa070f632aa5662bf551ba4",
    "training-graph.json": "cfe8b0eda9becdede688a7599888590cf0838bf4a503c596997a398a13d6b775"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
calculus-causation-v0 | Average rate of change -> predicts -> Instantaneous rate of change | f is real-valued and differentiable at a, and [f(a+h)-f(a)]/h is evaluated for nonzero h tending to zero
calculus-causation-v0 | Derivative as a rate -> predicts -> Tangent line slope | f is a real function differentiable at a with a finite derivative and the tangent is the limit of secant lines through (a,f(a))
calculus-causation-v0 | Differentiability -> predicts -> Continuity at a point | f is real-valued on an open interval containing a and has a finite derivative at a
calculus-causation-v0 | Local maximum -> predicts -> Critical point | c lies inside an open real interval on which f is defined and f(c) is a local maximum; endpoints are excluded
calculus-causation-v0 | Local minimum -> predicts -> Critical point | c is an interior point of the real domain and f(c) is a local minimum, rather than a boundary minimum
calculus-causation-v0 | Derivative as a rate -> predicts -> Increasing function | f is continuous on [a,b], differentiable on (a,b), a < b, and f prime(x) > 0 throughout (a,b)
calculus-causation-v0 | Derivative as a rate -> predicts -> Decreasing function | a < b, f is continuous on [a,b] and differentiable on (a,b), with f prime(x) < 0 at every interior point
calculus-causation-v0 | Second derivative concavity -> predicts -> Inflection point | f is twice differentiable near c and f double-prime is strictly positive on one side of c and strictly negative on the other
calculus-causation-v0 | Second derivative concavity -> predicts -> Local maximum | f is twice continuously differentiable near an interior c, f prime(c) = 0, and f double-prime(c) < 0
calculus-causation-v0 | Second derivative concavity -> predicts -> Local minimum | c is interior, f is C^2 near c, f prime(c) = 0, and f double-prime(c) > 0
calculus-causation-v0 | Riemann sum approximation -> predicts -> Integral as accumulation | f is Riemann integrable on a finite interval [a,b], and partition mesh tends to zero with arbitrary tags inside each subinterval
calculus-causation-v0 | Fundamental theorem of calculus -> predicts -> Antiderivative family | f is continuous on an open real interval containing a and x, and C is any real constant
calculus-causation-v0 | Fundamental theorem of calculus -> predicts -> Area under a curve | a < b, f is continuous and nonnegative on [a,b], and F is continuous there with F prime = f on (a,b)
calculus-causation-v0 | Antiderivative family -> predicts -> Integral as accumulation | f is continuous on [a,b] and F prime = f on an open interval containing [a,b], so every antiderivative F+C gives F(b)-F(a)
calculus-causation-v0 | Mean value theorem bound -> predicts -> Average rate of change | a < b and f is continuous on [a,b] and differentiable on (a,b)
calculus-causation-v0 | Chain rule for composition -> predicts -> Derivative as a rate | the real inner function g is differentiable at x and the real outer function f is differentiable at g(x)
calculus-causation-v0 | Chain rule for composition -> enables -> Related rates problems | x=g(t) is differentiable at the time t and y=f(x) is differentiable at x=g(t)
calculus-causation-v0 | Critical point -> enables -> Optimization by derivatives | f is continuous on a compact interval [a,b], has finitely many interior critical points, and all of these and both endpoints are evaluated
calculus-causation-v0 | Geometric series sum -> predicts -> Series convergence | a and r are fixed real or complex numbers and |r| < 1 for the series sum_(n=0)^infinity a*r^n
calculus-causation-v0 | Remainder term shrink -> prerequisite -> Taylor approximation | f has derivatives of every order at centre a, P_n is its Taylor polynomial, and equality f(x) = lim_(n->infinity) P_n(x) is required at fixed x
calculus-causation-v0 | Differentiability -> predicts -> Linear approximation near a point | f is differentiable at an interior point a and the increment h tends to zero within its real domain
calculus-causation-v0 | Continuity at a point -> prerequisite -> Differentiability | f is defined on a real open interval containing a and differentiability means a finite two-sided derivative at a
calculus-causation-v0 | Second derivative concavity -> enables -> Optimization by derivatives | f is C^2 on an open interval, f double-prime > 0 throughout it, and an interior c satisfies f prime(c) = 0
calculus-causation-v0 | Geometric series sum -> predicts -> Taylor approximation | the centre is zero, n is a nonnegative integer, x is real, and |x| < 1
calculus-causation-v0 | Integral as accumulation -> predicts -> Area under a curve | f is Riemann integrable and f(x) >= 0 on the finite interval [a,b] with a < b
calculus-causation-v0 | Small change differential -> predicts -> Finite output change | f is differentiable at a and nonzero dx tends to zero, so the error divided by |dx| tends to zero
calculus-causation-v0 | First derivative sign change -> predicts -> Local maximum | f is continuous at c and differentiable on (c-epsilon,c) and (c,c+epsilon), with f prime > 0 to the left and < 0 to the right for epsilon > 0
calculus-causation-v0 | First derivative sign change -> predicts -> Local minimum | for some epsilon > 0, f is continuous at c, differentiable on both punctured sides of c, with f prime < 0 to the left and > 0 to the right
```

## Step 0: geometry-causation-v0

Commit: pending creation, title `Review fixes: geometry`.
Counts: 40 concepts, 31 relations, 5 myths, 7 boundaries, 6 examples, 7 controls.
Relations by kind: {"causes": 1, "enables": 3, "predicts": 23, "prerequisite": 2, "prevents": 2}.
Probes/tasks: not applicable to Step 0. Sources added: none; existing mathlib4 (and existing NIST DLMF where named) retained.

Self-review: all 31 final edges revised in direction and counterexample passes; changed SSS, diameter/radius, strict triangle inequality and scaling targets. 9 true drops, 22 renamed/retargeted IDs and 9 retained IDs. Version pass: 0 software-version changes; Euclidean, finite, nondegenerate, planar and positive-scale regimes specified. Myth pass: 5 reviewed, 2 corrected. Count pass: 40 → 31 without padding. Duplicate pass: 0 final duplicate pairs/conditions. Parent made 1 additional target repair: areaadd-enables-tessellation now targets Tessellation area calculation, because additivity supports computing an existing tiling's area.

True drops:
- postulate-prereq-parallels: uniqueness axiom restatement; mere parallel existence is not the postulate; moved to boundary.
- corresponding-enables-aa: AA input restated.
- rigidity-inhibits-wobble: redundant with direct brace/shear mechanism.
- anglesum-prereq-aa: proof route is not necessary hypothesis.
- anglesum-prevents-three-rights: wrong right-triangle target; moved to at-most-one-right-angle boundary.
- inscribed-enables-thales: diameter/Thales special case already present.
- central-enables-pi: full-turn angle does not enable pi.
- segment-enables-inequality: collinear equality defeats strict conclusion.
- hypotenuse-prereq-thales: assumes conclusion and duplicates diameter/Thales.

Specific repairs include SSS rigidity, reflex intercepted arcs, excluded Thales endpoints, all strict side inequalities, one-right-angle boundary, scaling → absence of angle distortion, and limit justification for sector area. Primary verification: mathlib Geometry/Euclidean/{Congruence,Triangle,Angle/Sphere}. All final edges reviewed for direction, counterexamples, theorem hypotheses and duplicates. Parent checked every final relation; structural audit passed for labels/verbs/endpoints/unique ordered pairs/unique conditions. Open doubts: no unresolved mathematical claim identified; independent Claude review remains pending.

Four checks:

```
$ python3 tools/build_geometry_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/geometry-causation-v0/foundations.jsonl with 172 records
splits: {'cross_domain_holdout': 6, 'sealed_test': 17, 'train': 127, 'validation': 22}
kinds: {'boundary': 7, 'concept': 41, 'counterexample': 5, 'relation': 106, 'synthetic_control': 7, 'worked_example': 6}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id geometry-causation-v0
{
  "schema_version": 1,
  "world_id": "geometry-causation-v0",
  "adapter_independent": true,
  "record_count": 172,
  "node_count": 66,
  "edge_count": 106,
  "negative_pair_count": 7,
  "domains": [
    "geometry"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "a5308f4525dd4723802e31a348a0066dbddb0a68f595ee78801ecc10e2ec7a1a",
    "lexicon.json": "288e1b56bc22f46a0a6fd05dfdd82290918fa03576be2c7d1e08e0d9c6e78b68",
    "nodes.jsonl": "63676ff252e37ad3fc0d53477de92645da07918ada1a67e6a093a44d65271855",
    "records.jsonl": "ccacaf73bc14ed9bbb64ccc2e37c4583540db5fb59c15273b5214a6aabaf1f81",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "0253ecddd3e7ae67cd5ea828cf377b76242fcf366f01b68bed284730ca807c27",
    "split-manifest.json": "cb45def96113ff70a2223c165ecf65f1cd25c4e91899108db3a8c5697d4aa5dd",
    "training-graph.json": "60a15eefc096a05f35265f1646e20e992e8d1d4ddceafdedc42cf755aea268f3"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
geometry-causation-v0 | Transversal of parallels -> predicts -> Corresponding angles | two distinct lines are parallel in a Euclidean plane and a third line intersects each of them
geometry-causation-v0 | Transversal of parallels -> predicts -> Alternate interior angles | a line crosses two distinct coplanar parallel lines at separate points in Euclidean geometry
geometry-causation-v0 | Angle-angle similarity -> predicts -> Similar triangles | two nondegenerate Euclidean triangles have two equal pairs of corresponding interior angles
geometry-causation-v0 | Similar triangles -> predicts -> Uniform scaling | matching vertices of two nondegenerate Euclidean triangles are fixed, and scaling may be followed by an isometry
geometry-causation-v0 | Uniform scaling -> predicts -> Squared area scale | a planar measurable figure of finite positive area is dilated by one positive length factor k in every direction
geometry-causation-v0 | Uniform scaling -> predicts -> Cubed volume scale | a measurable solid of finite positive volume in Euclidean three-space is dilated by one factor k > 0 along every spatial axis
geometry-causation-v0 | Right triangle -> prerequisite -> Pythagorean relation | a,b,c are the positive side lengths of a nondegenerate Euclidean triangle and c is its longest side
geometry-causation-v0 | Pythagorean relation -> predicts -> Hypotenuse | a and b are the known positive perpendicular leg lengths of a Euclidean right triangle
geometry-causation-v0 | Converse Pythagorean test -> predicts -> Right triangle | a,b,c are sides of a nondegenerate Euclidean triangle, c is longest, and c^2 = a^2+b^2
geometry-causation-v0 | Diameter of a circle -> predicts -> Triangle in a semicircle | the circle has positive radius and the third vertex is on the circle but differs from both diameter endpoints
geometry-causation-v0 | Central angle -> predicts -> Inscribed angle | A and B are distinct points of a Euclidean circle, the inscribed vertex lies on the complementary open arc, and the central angle measures the selected arc AB, including a reflex angle when needed
geometry-causation-v0 | Triangle angle sum -> predicts -> Exterior angle of a triangle | the triangle is nondegenerate and Euclidean, and the exterior angle is supplementary to the interior angle at the extended side
geometry-causation-v0 | Triangle angle sum -> predicts -> Quadrilateral angle sum | a simple nondegenerate Euclidean quadrilateral is divided along an internal diagonal into two nonoverlapping triangles
geometry-causation-v0 | Triangle angle sum -> predicts -> Polygon interior angle sum | a simple Euclidean polygon with n >= 3 vertices is triangulated into n-2 nonoverlapping triangles; any reflex interior angles are counted
geometry-causation-v0 | Diameter of a circle -> predicts -> Circle circumference | the circle is Euclidean with positive diameter d, so its rectifiable boundary has length pi*d
geometry-causation-v0 | Circle radius -> predicts -> Circle area | r > 0 is the radius of a disk in the Euclidean plane and area uses the usual two-dimensional measure
geometry-causation-v0 | Side-side-side congruence -> predicts -> Triangle rigidity | three positive lengths satisfy all strict triangle inequalities and the triangle remains in Euclidean space
geometry-causation-v0 | Diagonal brace -> causes -> Triangle rigidity | the four side members and attached diagonal have fixed lengths, the two triangles are noncollinear, and joints remain connected with motion restricted to the plane
geometry-causation-v0 | Diagonal brace -> prevents -> Quadrilateral shear | a nondegenerate planar hinged frame has rigid side bars and a securely attached diagonal that resists tension and compression without deformation
geometry-causation-v0 | Triangle inequality -> predicts -> Triangle existence from three sides | the three proposed lengths are positive real numbers and each length is strictly less than the sum of the other two
geometry-causation-v0 | Side and angle ranking -> predicts -> Hypotenuse | the Euclidean triangle is nondegenerate with one interior angle of 90 degrees and two strictly smaller positive angles
geometry-causation-v0 | Pythagorean relation -> predicts -> Perpendicular distance | P lies off a Euclidean line, H is its perpendicular foot, and any other point Q on the line gives PQ^2 = PH^2+HQ^2
geometry-causation-v0 | Area additivity -> enables -> Circle area | a disk of radius r > 0 is partitioned into equal sectors without overlapping interiors, and a justified area limit of their rearrangements is the rectangle with sides pi*r and r
geometry-causation-v0 | Parallel lines -> prerequisite -> Corresponding angles | two distinct coplanar lines meet a transversal at distinct points, and one matching pair of corresponding angles is equal
geometry-causation-v0 | Alternate interior angles -> predicts -> Parallel lines | two distinct coplanar Euclidean lines meet the same transversal at separate points and an alternate interior angle pair is equal
geometry-causation-v0 | Polygon interior angle sum -> predicts -> Regular tessellation | congruent regular n-gons tile the Euclidean plane edge to edge with q >= 3 corners at each vertex, so q*(n-2)*180/n = 360 with integer n >= 3
geometry-causation-v0 | Pythagorean relation -> predicts -> Straight line segment | the endpoints have coordinate differences dx and dy in an orthonormal Cartesian coordinate system in the Euclidean plane
geometry-causation-v0 | Parallel postulate -> predicts -> Triangle angle sum | the remaining axioms of neutral plane geometry hold, and the triangle is nondegenerate
geometry-causation-v0 | Uniform scaling -> prevents -> Angle distortion | the transformation is one dilation x -> c+k(x-c) with the same k > 0 in every direction in Euclidean space
geometry-causation-v0 | Pythagorean relation -> enables -> Converse Pythagorean test | a nondegenerate triangle has lengths a,b,c satisfying a^2+b^2=c^2, and a right triangle with legs a,b is constructed and compared by SSS
geometry-causation-v0 | Area additivity -> enables -> Tessellation area calculation | the patch is exactly a finite union of congruent tiles with pairwise disjoint interiors; shared boundaries have zero area
```
