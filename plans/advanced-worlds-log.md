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

Commit: `e7f0af7` (`Review fixes: geometry`).
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

## Step 0: information-causation-v0

Commit: `adfc9e8` (`Review fixes: information`).
Counts: 35 concepts, 28 relations, 6 myths, 8 boundaries, 6 examples, 7 controls.
Relations by kind: {"enables": 7, "predicts": 20, "prerequisite": 1}.
Probes/tasks: not applicable to Step 0.

Self-review: 41 old and 28 final edges read. Direction pass replaced 27 old claims and added one CIRC edge, including mutual information → capacity. Counterexample pass tightened all 28 conditions to finite/discrete/iid/DMC/AWGN or ECMA regimes. Fourteen true drops are listed below. Version pass: ECMA-130 second edition is explicit; mathematical hypotheses replace vague typical conditions. Myth pass: all 5 original myths corrected and 1 conditioning myth added. All 3 original boundaries corrected, 5 added. Count pass: 41 → 28 without padding; 100% allowed kinds; no duplicate pairs/conditions or label/verb errors. Parent read all 28 final edges and all myths/boundaries/examples. Open doubts: no unresolved claim retained; independent Claude review remains pending.

Dropped IDs:
- surprise-causes-bits: unit/definition; formula moved to probability → surprise.
- limit-inhibits-coding: theorem does not inhibit coding; above-capacity boundary retained.
- bit-enables-entropy: unit is not a mechanism.
- surprise-enables-entropy: entropy definition; computation in source → entropy.
- correction-enables-noisy-use: expected-error-count guarantee false; coding theorem retained.
- channelcoding-causes-redundancy: definition restatement.
- processing-prevents-restoring: wrong target; data-processing bound retained.
- pigeonhole-causes-growth: identity code refutes forced growth; no-universal-shrinking myth and counting bound retained.
- bit-prereq-length: binary unit not necessary for general lengths.
- floor-prereq-limit: source coding not prerequisite for channel capacity.
- noise-causes-detection-need: need is not detection; separate detection not mandatory.
- additivity-enables-blockcoding: duplicate of corrected block-code bound.
- typical-predicts-channel: insufficient channel/decoder assumptions.
- parity-inhibits-correction: adds information; inability to locate flip is a boundary, and known erasures can be recovered.

Meaningful regressions run in memory: conditioning example Hprior=0.468995593589, Hposterior(Y=1)=1, average Hconditional=0.2; counting inequality for all n=1..9, 0<=k<n; repetition correction for both source bits and all <=1 flips; parity check on every valid 4-bit even-parity codeword and all 16 masks. All passed.

Sources added: ecma-130-cdrom-2e, ECMA-130 second edition June 1996, clause 17 and Annex C (https://www.ecma-international.org/wp-content/uploads/ECMA-130_2nd_edition_june_1996.pdf). Existing shannon-1948 retained; its original corrected paper was verified at https://web.mit.edu/6.976/www/handout/shannon.pdf because the registered Harvard mirror did not load. Source registry's prior entry was not changed.

Four checks:

```
$ python3 tools/build_information_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/information-causation-v0/foundations.jsonl with 165 records
splits: {'cross_domain_holdout': 6, 'sealed_test': 17, 'train': 116, 'validation': 26}
kinds: {'boundary': 8, 'concept': 36, 'counterexample': 6, 'relation': 102, 'synthetic_control': 7, 'worked_example': 6}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id information-causation-v0
{
  "schema_version": 1,
  "world_id": "information-causation-v0",
  "adapter_independent": true,
  "record_count": 165,
  "node_count": 63,
  "edge_count": 102,
  "negative_pair_count": 7,
  "domains": [
    "information-communication"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "efdeab53341021021a981af0b361efa42876b7e92a0de10befdc7f5a24524016",
    "lexicon.json": "e1aae8e0c4a5b6fd872b34d1ba24d37db420d69b1cd99dac891fed265114e8bb",
    "nodes.jsonl": "f1e359bb4217cdf2f0a97c337670cfc50dcbc031cc9e870b44f594fc903fe15e",
    "records.jsonl": "393569e366fa8ad3eb6543d8bf6d8d7ca7077e4afaa8250206bd72c42fb33872",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "b6b0a1c7c02e08d25ed660c71e4a0092e4265e0161803f41cc86f03648e7ae10",
    "split-manifest.json": "797724e2813e8b8d0feb6a190bfe1053f0ae399f880055ce7d34469555bffe29",
    "training-graph.json": "28e0226d356088c900021be2a7bdce0d5cf66d7c13c180795c9fd3f268c955d7"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
information-causation-v0 | Outcome probability -> predicts -> Surprise of an outcome | the outcome belongs to a discrete source and 0 < p <= 1; the logarithm base is two
information-causation-v0 | Message source -> predicts -> Entropy of a source | X has a fixed finite probability distribution p(x), and zero-probability terms contribute zero to H(X)
information-causation-v0 | Uniform source distribution -> predicts -> Entropy of a source | the alphabet has exactly M >= 1 symbols and the entropy is compared across all probability distributions on that same alphabet
information-causation-v0 | Certain source outcome -> predicts -> Surprise of an outcome | one discrete outcome has probability p = 1, so -log2(p) = 0 bits
information-causation-v0 | Independent outcomes -> predicts -> Additivity of independent information | X and Y are independent finite discrete random variables and the joint entropy is measured with the same logarithm base
information-causation-v0 | Entropy of a source -> predicts -> Entropy compression floor | a finite discrete source X is encoded by a binary uniquely decodable symbol code and every possible source sequence must be recovered exactly
information-causation-v0 | Prefix-free code -> enables -> Unique decoding | the binary symbol code is injective, each codeword is finite and nonempty, and no distinct codeword is a prefix of another
information-causation-v0 | Entropy compression floor -> predicts -> Expected code length | the source is iid on a finite alphabet with at least two positive-probability symbols and a binary prefix code is designed for n-symbol blocks
information-causation-v0 | Pigeonhole compression limit -> predicts -> Incompressible random data | X is uniform over n-bit strings, the encoder is injective, and 0 <= k < n is an integer: fewer than a 2^(-k) fraction can have output length strictly below n-k
information-causation-v0 | Redundancy in messages -> enables -> Error detection | the binary block code has minimum Hamming distance d >= 2 and between 1 and d-1 bit substitutions occur in a transmitted codeword
information-causation-v0 | Parity check -> enables -> Error detection | the original XOR constraint is satisfied and an odd number of checked bits, including the check bit if affected, are flipped once
information-causation-v0 | Repetition coding -> enables -> Error correction | one bit is sent as m identical copies for odd m >= 3 and at most (m-1)/2 of those copies are flipped
information-causation-v0 | Channel coding with redundancy -> enables -> Noisy channel | the channel is discrete and memoryless with finite alphabets, 0 < R < C, and block length may grow without bound and the codebook and decoder may be designed for the channel
information-causation-v0 | Noisy channel -> predicts -> Code rate | independent bit flips occur with fixed probability 0 <= p <= 1/2, messages are equiprobable, block error tends to zero as length grows with a limiting rate R, and h2(p)=-p*log2(p)-(1-p)*log2(1-p) with 0log2(0)=0
information-causation-v0 | Signal power and bandwidth -> predicts -> Channel capacity | the channel is band-limited additive white Gaussian noise with bandwidth B > 0 Hz, finite average signal power P >= 0 watts and one-sided noise density N0 > 0 watts per Hz, so noise power is N0*B
information-causation-v0 | Mutual information -> predicts -> Channel capacity | the channel has fixed transition probabilities p(y|x), finite alphabets and no memory, and capacity is measured in bits per channel use
information-causation-v0 | Data processing inequality -> predicts -> Mutual information | X,Y,Z are finite discrete variables forming X->Y->Z, so Z is conditionally independent of X given Y and no extra side information is supplied
information-causation-v0 | Observation of evidence -> predicts -> Conditional entropy | X and Y are finite discrete variables and H(X|Y) averages over the actual distribution of all observations Y, rather than fixing one surprising y
information-causation-v0 | Conditional entropy -> predicts -> Mutual information | X and Y are finite discrete variables with a fixed marginal law of X; any comparison keeps H(X) constant
information-causation-v0 | Independent outcomes -> predicts -> Mutual information | the joint law of finite discrete X and Y satisfies p(x,y)=p(x)p(y) at every pair
information-causation-v0 | Typical sequences -> enables -> Code for a source | the source is iid on a finite alphabet, block length tends to infinity, and atypical blocks are counted as errors rather than falsely claiming exact lossless recovery
information-causation-v0 | Entropy of a source -> predicts -> Typical sequences | X_i are iid on a finite alphabet with entropy H; for epsilon > 0 and sufficiently large n, the epsilon-typical set has probability at least 1-epsilon and size between (1-epsilon)*2^(n*(H-epsilon)) and 2^(n*(H+epsilon))
information-causation-v0 | Uniform source distribution -> predicts -> Password entropy | the generator chooses each of L characters uniformly and independently from the same M-symbol alphabet, and the attacker knows the procedure but has no correlated side information
information-causation-v0 | Redundancy of language -> predicts -> Entropy of a source | a stationary source over M symbols has nonuniform single-symbol probabilities or H(X_t|X_(t-1),...,X_(t-k)) < log2(M) for some finite k, and the comparison concerns its entropy rate
information-causation-v0 | Code for a source -> predicts -> Expected code length | a finite source distribution p(x) and finite binary codeword lengths l(x) are fixed before taking the expectation
information-causation-v0 | Unique decoding -> prerequisite -> Code for a source | one symbol code is extended by concatenation to all finite source sequences, recovery must be exact, and no framing or side channel resolves boundaries
information-causation-v0 | Repetition coding -> predicts -> Code rate | each binary source symbol is mapped to exactly m identical channel bits with fixed integer m >= 1 and no additional framing symbols
information-causation-v0 | Cross-interleaved Reed-Solomon coding -> enables -> Error correction | ECMA-130 second edition clause 17 and Annex C encoding is used, and each constituent Reed-Solomon decoding step has error count e and known erasure count s satisfying 2e+s <= 4
```


## Parallel-chat preflight: 104-world prompt (2026-10-02)

Chat `01a0ff6a-67e9-7162-8178-f1c11423c7ef` stopped authoring at preflight: the checkout has active uncommitted Step 0 edits owned by existing chat `01a0ff59-a0e2-7c82-849d-353d175d456f` (Complete attached prompt task). HEAD at observation: `adfc9e8`. No world, builder, source, generated curriculum or branch changes were made by this second chat. The prompt requires stopping on unexpected Git state. User clarification is pending about continuing in the existing chat or taking over here after it stops.

The current attachment `/home/jesse/Downloads/1AUTHORING-PROMPT-ADVANCED-WORLDS.md` and the original prompt path in a-rag-atom now both have SHA-256 `c764ed992b32471cac032ec49cc3a310851dd7239953bdc7b6ba287242b2a6ed` and 104 catalog rows. The existing chat initially read a 70-world version; its remaining scope needs rereading against the current document. Printed tier counts are 8, 17, 4, 9, 2, 29, 34, 1 for tiers 1, 2, 3, 4, 5, 6, 8, 9; no Tier 7 is printed. No new relations or validation results were produced by this preflight.

## Shared source registration for remaining Step 0 sweep worlds

The following canonical citation-only entries were verified by the owning workers and appended without changing existing entries. Color uses the first five, Python the next four, Go the next five, and C++ the final three. All will be exercised by the required source validator.

- w3c-compositing-1-20240321: Compositing and Blending Level 1; Candidate Recommendation Draft, 21 March 2024; https://www.w3.org/TR/2024/CRD-compositing-1-20240321/; standards-primary
- w3c-wcag22-understanding-use-color: Understanding Success Criterion 1.4.1: Use of Color; Updated 2025-09-16; https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html; standards-primary
- witzel-afterimages-2025: The non-opponent nature of colour afterimages; 3, 154 (2025); doi:10.1038/s44271-025-00331-5; https://www.nature.com/articles/s44271-025-00331-5; peer-reviewed-primary
- sinha-brightness-contrast-2020: Mechanisms underlying simultaneous brightness contrast: Early and innate; 173:41-49 (2020); doi:10.1016/j.visres.2020.04.012; https://pubmed.ncbi.nlm.nih.gov/32464426/; peer-reviewed-primary
- dynamic-color-afterimages-2022: After-image formation by adaptation to dynamic color gradients; 85, 174-187 (2023); published 2022-10-07; doi:10.3758/s13414-022-02570-8; https://link.springer.com/article/10.3758/s13414-022-02570-8; peer-reviewed-primary
- python-pep-779: PEP 779: Criteria for supported status for free-threaded Python; Final; Python 3.14 supported free-threaded phase; https://peps.python.org/pep-0779/; standards-primary
- python-free-threading-314: Python support for free threading; Python 3.14 documentation; https://docs.python.org/3.14/howto/free-threading-python.html; standards-primary
- python-asyncio-314: Coroutines and Tasks; Python 3.14 documentation; https://docs.python.org/3.14/library/asyncio-task.html; standards-primary
- python-copy-314: copy: Shallow and deep copy operations; Python 3.14 documentation; https://docs.python.org/3.14/library/copy.html; standards-primary
- go-memory-model: The Go Memory Model; June 6, 2022 revision; https://go.dev/ref/mem; standards-primary
- go-runtime-gc-guide: A Guide to the Go Garbage Collector; gc runtime guide retrieved 2026-10-02; https://go.dev/doc/gc-guide; standards-primary
- go-loopvar-122: Fixing For Loops in Go 1.22; 19 September 2023; Go 1.22 module-version transition; https://go.dev/blog/loopvar-preview; standards-primary
- go-sync: sync package; standard-library documentation retrieved 2026-10-02; https://pkg.go.dev/sync; standards-primary
- go-context: context package; standard-library documentation retrieved 2026-10-02; https://pkg.go.dev/context; standards-primary
- cpp-draft-n4861: Working Draft: Standard for Programming Language C++; N4861; C++20 working draft; https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2020/n4861.pdf; standards-primary
- cpp-core-guidelines: C++ Core Guidelines; Living guidelines; C.21 and C.20; retrieved 2026-10-02; https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines; standards-primary
- cpp-itanium-abi: Itanium C++ ABI; Living ABI specification; virtual table layout; retrieved 2026-10-02; https://itanium-cxx-abi.github.io/cxx-abi/abi.html; standards-primary

## Step 0: python-causation-v0

Commit: `9c697bf` (`Review fixes: python`).
Counts: 39 concepts, 32 relations, 6 myths, 4 boundaries, 4 examples, 4 controls.
Relations by kind: {"causes": 6, "enables": 10, "inhibits": 3, "predicts": 4, "prerequisite": 1, "prevents": 8}.
Probes/tasks: not applicable to Step 0.

Self-review (passes overlap): 41 original → 32 retained, 9 dropped, no new relation IDs; direction pass corrected 11 endpoints and 6 kinds. Counterexample pass tightened all 32 conditions. Version pass marks all 32 as Python 3 or explicit CPython 3.13/3.14 build modes. Duplicate pass removed one repeated asyncio pair (included in nine drops); zero duplicate pairs/conditions remain. Myth pass revised all five myths and added a closure/late-binding myth. Count pass retained 100% causal kinds without padding. Parent read all final relations; post-review Go and grammar changes were separately checked. Open doubts: no unresolved Python claim identified; Claude review pending.

Drops:
- class-attr-read-through: class sharing does not cause instance shadowing.
- hints-leave-duck-typing: unchecked annotation not prerequisite for duck typing.
- mutable-needs-shallow-copy: mutability does not require copying.
- await-uses-generators: native coroutines are not generators.
- deep-copy-beats-shallow: duplicate independence claim with wrong target.
- with-enables-deterministic-cleanup: managed resource release does not enable reference counting.
- duck-typing-prereq-iterator: no necessary dependency.
- loop-avoids-gil-contention: repeated pair and wrong GIL target.
- aliasing-makes-shallow-look-fine: appearance is not a mechanism.

Inline runtime regressions passed: late-bound comprehension lambdas, non-leaking comprehension iteration targets, property precedence, equality/hashability, tuples containing unhashable members, NaN and copied aliases. Primary references registered above: PEP779, Python3.14 free threading, asyncio and copy docs; existing language reference retained.

Four checks:

```
$ python3 tools/build_python_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/python-causation-v0/foundations.jsonl with 155 records
splits: {'cross_domain_holdout': 6, 'sealed_test': 17, 'train': 113, 'validation': 19}
kinds: {'boundary': 4, 'concept': 40, 'counterexample': 6, 'relation': 97, 'synthetic_control': 4, 'worked_example': 4}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id python-causation-v0
{
  "schema_version": 1,
  "world_id": "python-causation-v0",
  "adapter_independent": true,
  "record_count": 155,
  "node_count": 58,
  "edge_count": 97,
  "negative_pair_count": 4,
  "domains": [
    "language-ecosystems"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "17924da36c7897bc900565e2aaad5cb43922c0f504360d8b22f1c752bcb2133e",
    "lexicon.json": "4957c88159d6a5ce9c62cca24d21b4e9ea9d13ab94c23ef5079c6e56cfd1b6ac",
    "nodes.jsonl": "f206ed4b3fa4e5e3f89f745aa43d5d17c0f0fc18c315a80cf28112067aa877ff",
    "records.jsonl": "d2bb429e1d520ad9696b667df716527b1b0dfe04fad17f36c3bb78afcfd9de6c",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "b59e494e679f574335170d782580132d46650ff7cc1ecd78940e0318dae647a3",
    "split-manifest.json": "651dc0d826ce088814b8204c96b33c8899c36e3285a63b4483bc45079f7cf3d6",
    "training-graph.json": "fa4f041d5725892b3b7130bea7990ebf28ae7fb5b98511da7df9a4345aa97180"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
python-causation-v0 | Name binding to an object -> enables -> Object identity | Python 3; two bound names are operands of is
python-causation-v0 | Aliasing two names -> causes -> Shared mutation visibility | Python 3; both names refer to the same list and an in-place append is observed through the other name
python-causation-v0 | Immutable object -> prevents -> Shared mutation visibility | Python 3; the shared value is a built-in str, bytes or number and only that value is considered
python-causation-v0 | Shallow copy -> inhibits -> Aliasing two names | Python 3; list.copy creates the new outer list and the source name still refers to the original
python-causation-v0 | Deep copy -> prevents -> Shared mutation visibility | Python 3; copy.deepcopy processes a graph of built-in lists and dictionaries with primitive immutable leaves and no custom copy hooks
python-causation-v0 | Object identity -> predicts -> True equality result | Python 3; the type inherits the default identity-based equality and does not replace its comparison behavior
python-causation-v0 | Hashability of a type -> prerequisite -> Dictionary key lookup | Python 3; a built-in dict hashes the supplied key and requires that particular instance to be hashable
python-causation-v0 | Mutable object -> prevents -> Hashability of a type | Python 3; the object is a built-in list, dict, set or bytearray rather than a custom identity-hashed object
python-causation-v0 | Dictionary key lookup -> enables -> Identity versus equality | Python 3; valid hashable keys have matching hashes and dict checks candidate identity or equality
python-causation-v0 | Global interpreter lock -> causes -> Thread parallelism limits | CPython 3.13/3.14 default GIL build; CPU-bound threads execute Python bytecode in the same interpreter
python-causation-v0 | Await yielding control -> enables -> Asyncio event loop | Python 3 asyncio; the awaited operation actually suspends the current task and another callback or task is ready
python-causation-v0 | Asyncio event loop -> enables -> Single-thread I/O concurrency | Python 3 asyncio; tasks use nonblocking I/O and yield cooperatively on one loop thread without blocking that thread
python-causation-v0 | Yield suspension point -> enables -> Generator lazy evaluation | Python 3; a synchronous generator is advanced incrementally with next rather than exhausted eagerly
python-causation-v0 | Generator lazy evaluation -> enables -> Iterator protocol | Python 3; calling a synchronous generator function supplies an iterator advanced by a for loop
python-causation-v0 | Comprehension scope -> prevents -> Loop variable leakage | Python 3; a list, set or dict comprehension binds its for-clause target rather than an assignment-expression target
python-causation-v0 | Closure late binding -> predicts -> Name binding to an object | Python 3; a closure reads a captured variable after its enclosing loop has rebound that variable and no default argument freezes a value
python-causation-v0 | Default mutable argument -> causes -> Shared mutation visibility | Python 3; successive calls omit a list default parameter and append to the default object instead of rebinding it
python-causation-v0 | Finally guarantee -> prevents -> Skipped cleanup | Python 3; an entered finally suite contains the cleanup, execution reaches it, and that cleanup completes
python-causation-v0 | Context manager with-block -> prevents -> Skipped cleanup | Python 3; __enter__ succeeded and the manager's __exit__ releases the acquired resource successfully on normal or exceptional exit
python-causation-v0 | Last reference dropped -> causes -> Reference counting cleanup | CPython 3.13/3.14 GIL-enabled build; the object's final strong reference disappears, its count reaches zero and no finalizer resurrects it
python-causation-v0 | Cycle collector -> enables -> Reference counting cleanup | CPython 3.13/3.14 GIL-enabled build; enabled cyclic GC collects tracked unreachable containers with supported clearing and no resurrection
python-causation-v0 | Dunder methods -> enables -> Duck typing | Python 3; a custom type supplies the required special methods for the operation being invoked without a nominal-type check
python-causation-v0 | Dunder methods -> enables -> Iterator protocol | Python 3; both iterator methods are implemented on the custom iterator's type with the specified contracts
python-causation-v0 | Property descriptor -> prevents -> Instance attribute shadowing | Python 3; normal object.__getattribute__ finds a property of the same name in the class MRO
python-causation-v0 | Instance attribute shadowing -> inhibits -> Class attribute sharing | Python 3; ordinary instance assignment stores an instance-dictionary value and the class attribute is not a data descriptor
python-causation-v0 | Method resolution order -> predicts -> Class attribute sharing | Python 3; normal attribute lookup searches multiple bases, with no instance shadowing, custom lookup or data-descriptor transformation
python-causation-v0 | Module import cache -> causes -> Aliasing two names | Python 3; both imports use the same fully qualified name with its sys.modules entry intact
python-causation-v0 | Immutable object -> enables -> Hashability of a type | Python 3; the object is a built-in tuple whose elements are all hashable or a built-in frozenset
python-causation-v0 | Method resolution order -> predicts -> Dunder methods | Python 3; implicit special-method lookup searches the operand type and its bases for the same method name
python-causation-v0 | Module import cache -> causes -> Class attribute sharing | Python 3; a module defines a class once and repeated imports access that class without reload or rebinding
python-causation-v0 | Dunder methods -> prevents -> Hashability of a type | Python 3; a new class defines __eq__ but supplies no __hash__ entry, even when a base class had a hash implementation
python-causation-v0 | Exception control flow -> inhibits -> Iterator protocol | Python 3.7+; a synchronous generator raises an unhandled exception instead of yielding its next value and the caller does not suppress it
```

## Go preliminary checks before final atomic-access definition correction

This preliminary receipt predates the parent correction: a race includes at least one write and at least one non-atomic access; current-source verification follows.
Counts: 40 concepts, 32 relations, 5 myths, 4 boundaries, 4 examples, 4 controls.
Relations by kind: {"causes": 8, "enables": 7, "inhibits": 1, "predicts": 2, "prerequisite": 2, "prevents": 12}.
Probes/tasks: not applicable to Step 0.

Self-review (passes overlap): 40 originals → 31 retained plus one new relation, nine drops. Direction pass corrected 13 endpoints and eight kinds. Counterexample pass tightened all 32 conditions. Version pass pins implementation-dependent gc runtime/compiler edges to Go1.27 and loop closure semantics to Go1.22+ compiler AND module go>=1.22 with declared iteration variables. Parent found and worker fixed duplicate panic-recover → termination pair by introducing Successful panic recovery and Unrecovered panic concepts; Channel send blocking now correctly includes buffered-send cases. Zero duplicate pairs/conditions remain. Myth pass revised all five. Count pass 100% causal kinds, no padding. Open doubts: no unresolved Go claim identified; Claude review pending.

Drops:
- unbuffered-synchronizes: circular waiting definition.
- waitgroup-orders-completion: waiting does not cause goroutine launch/completion.
- implicit-decouples: interface satisfaction does not enable embedding.
- errors-prevent-panic-flow: an error check cannot prevent independent panic.
- ok-idiom-rests-on-zeros: multiple returns do not cause zero values.
- scheduler-runs-others: scheduler does not enable channel blocking.
- nil-box-wraps-typed-nil: nil distinction does not cause interface satisfaction.
- append-enables-streaming: no communication mechanism or spec doubling guarantee.
- escape-predicts-slice-life: slice validity is semantic, not contingent on a chosen allocation strategy.

New relation map-order-enables-variation states permission rather than guaranteed differing orders. Primary references registered above: Go memory model, runtime GC guide, Go1.22 loop change, sync and context.

Four checks:

```
$ python3 tools/build_go_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/go-causation-v0/foundations.jsonl with 156 records
splits: {'cross_domain_holdout': 6, 'sealed_test': 15, 'train': 120, 'validation': 15}
kinds: {'boundary': 4, 'concept': 41, 'counterexample': 5, 'relation': 98, 'synthetic_control': 4, 'worked_example': 4}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id go-causation-v0
{
  "schema_version": 1,
  "world_id": "go-causation-v0",
  "adapter_independent": true,
  "record_count": 156,
  "node_count": 58,
  "edge_count": 98,
  "negative_pair_count": 4,
  "domains": [
    "language-ecosystems"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "3a052383cd93a4ed09a53c271b6b616aa0934307bf9a680f6e9dff1752ce7355",
    "lexicon.json": "c8d8bec8a79c7ec4816165323dea517f484bdf51d1cc441e1053bc8120823873",
    "nodes.jsonl": "c81ece8a24cf489da2692c1fd0f81d285eb283bcf5bf0fa5941683d0ae816342",
    "records.jsonl": "7b0c9d54eb26c2c9086eeb23dcd65cdc67834ee65aa84045b0a9b4eb1276637d",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "40d0270fa187c7d19f20347532ff32323d6422c57b5857c9c2d7cc478b8c3b4b",
    "split-manifest.json": "04ecd7f4c94af13a9be67f3b52c6dc9916d60cd5ee91ad7eb123cd1735e89372",
    "training-graph.json": "d063cee989777ed035f545ed8a568a9e3a9fb707fca0f7b02491d2d49be9ab8e"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
go-causation-v0 | M-N goroutine scheduling -> enables -> Goroutine launch | Go 1.27 gc runtime; ordinary go statements create goroutines not explicitly locked to OS threads
go-causation-v0 | Channel receive -> prerequisite -> Channel send | Go 1; the channel is non-nil, open and unbuffered and the send completes normally
go-causation-v0 | Buffered channel -> prevents -> Channel send blocking | Go 1; the channel is open and non-nil and has room for the sent element at the moment of the send
go-causation-v0 | Channel send -> causes -> Channel deadlock | Go 1; all goroutines capable of releasing an unbuffered send are in a closed cycle of channel waits with no external unblock event
go-causation-v0 | Select statement -> prevents -> Channel deadlock | Go 1; select has a default clause, so selection itself never blocks, and evaluation of operands and the selected body do not block
go-causation-v0 | Share memory by communicating -> prevents -> Data race in Go | Go 1 memory model; the sender ceases access before sending ownership and the receiver alone accesses the data after receipt
go-causation-v0 | Mutex protection -> prevents -> Data race in Go | Go 1 memory model; every conflicting access to the protected memory occurs while holding the same non-copied mutex
go-causation-v0 | Escape analysis to heap -> prevents -> Stack allocation in Go | Go 1.27 gc compiler; an escaping allocation remains after optimization and is assigned to the heap rather than the current frame
go-causation-v0 | Stack allocation in Go -> inhibits -> Heap allocation rate | Go 1.27 gc compiler; otherwise equivalent executed allocations use stack storage instead of heap storage and are not optimized away
go-causation-v0 | Concurrent garbage collector -> enables -> Goroutine launch | Go 1.27 gc runtime; the collector is in a concurrent phase rather than a stop-the-world phase and runnable mutator work is scheduled
go-causation-v0 | Nil interface versus nil pointer -> predicts -> Error value returns | Go 1; a nil pointer whose type implements error is returned directly from a function with an error result
go-causation-v0 | Multiple return values -> enables -> Error value returns | Go 1; a function declares a result pair such as (Value, error) and follows the nil-error success convention
go-causation-v0 | Defer stack -> enables -> Panic and recover | Go 1; the deferred function directly invokes recover while unwinding an active panic in the same goroutine
go-causation-v0 | Successful panic recovery -> prevents -> Program termination from panic | Go 1; recover is called directly by a deferred function in the panicking goroutine and cleanup raises no replacement panic
go-causation-v0 | Slice backing array -> causes -> Data race in Go | Go 1 memory model; different goroutines access overlapping array cells through slices, at least one writes, and no synchronization orders them
go-causation-v0 | Append beyond capacity -> causes -> Slice backing array | Go 1; the new length exceeds the old capacity and the append succeeds rather than failing allocation
go-causation-v0 | Embedding composition -> enables -> Implicit interface satisfaction | Go 1; the promoted methods are unambiguous, have the required signatures and belong to the relevant value or pointer method set
go-causation-v0 | Unexported interface method -> prevents -> Implicit interface satisfaction | Go 1; the implementing type is in a different package and does not inherit the original package's method through embedding
go-causation-v0 | Context cancellation -> prevents -> Channel send blocking | Go 1.7+ context; the blocked select includes the context Done channel and returns when cancellation closes it
go-causation-v0 | Type zero values -> causes -> Nil interface versus nil pointer | Go 1; an uninitialized variable of type *T is nil and is then returned or assigned as an interface that *T implements
go-causation-v0 | Package initialisation order -> prerequisite -> Main function entry | Go 1; a Go program executes imported package initializers and main package initializers successfully before calling main.main
go-causation-v0 | Loop variable capture -> prevents -> Data race in Go | Go 1.22+ compiler with module go version >= 1.22 in go.mod; the loop declares its iteration variable, each closure only reads its own captured variable and no explicit outer-variable assignment is used
go-causation-v0 | Escape analysis to heap -> causes -> Heap allocation rate | Go 1.27 gc compiler; compared with the same workload using stack storage, retained escaping allocations execute repeatedly and are not eliminated
go-causation-v0 | Select statement -> enables -> Channel receive | Go 1; select has receive cases with at least one ready channel and chooses one ready communication
go-causation-v0 | Buffered channel -> prevents -> Channel receive blocking | Go 1; the buffer still contains an element at the moment the receive is performed
go-causation-v0 | Channel send -> causes -> Goroutine leak | Go 1; a live program leaves a worker sending forever on an open unbuffered channel with no future receiver or cancellation alternative
go-causation-v0 | WaitGroup completion -> prevents -> Early main return | Go 1 sync.WaitGroup; main calls Wait before returning, positive Add calls precede the wait and each worker calls Done only after finishing its required work
go-causation-v0 | Channel receive -> predicts -> Type zero values | Go 1; the channel is closed and empty, so receive returns the element type's zero value immediately and the comma-ok result is false
go-causation-v0 | Channel send -> causes -> Panic and recover | Go 1; a send is actually executed on a closed channel, including a selected send case
go-causation-v0 | Unrecovered panic -> causes -> Program termination from panic | Go 1; an active panic reaches the top of a goroutine after its deferred calls finish without recovery
go-causation-v0 | Context cancellation -> prevents -> Goroutine leak | Go 1.7+ context; every potentially indefinite worker wait observes Done and the worker exits on cancellation without launching untracked work
go-causation-v0 | Unspecified map iteration order -> enables -> Order-dependent output variation | Go 1; a program derives output directly from map range order without sorting keys or using an order-independent operation
```

## Step 0: cpp-causation-v0

Commit: `c03797c` (`Review fixes: cpp`).
Counts: 37 concepts, 36 relations, 6 myths, 5 boundaries, 5 examples, 4 controls.
Relations by kind: {"causes": 10, "enables": 9, "inhibits": 3, "prerequisite": 1, "prevents": 13}.
Probes/tasks: not applicable to Step 0.

Self-review (passes overlap): 40 original → 35 retained plus one new relation, five drops. Direction pass corrected seven endpoints and ten kinds. Counterexample and version passes reviewed all 36 conditions, each explicit C++20 with ABI boundaries where needed. Zero repeated pairs/conditions. Myth pass revised five and added the local-rvalue-reference lifetime correction. Count pass 100% causal kinds without padding. Parent independently read every final relation.

Drops:
- rule-five-prevents-leaks: checklist cannot prove release implementation.
- raii-enables-exception-safety: RAII does not enable unwinding.
- pointer-enables-rebind: pointer rebinding does not enable reference binding.
- stack-enables-raii: RAII not limited to stack; duplicate conceptual connection.
- templates-inhibit-type-ub: instantiation cannot generally prevent undefined behavior.

New relation copy-suppresses-implicit-move states suppression by a user-declared copy constructor. Verified local T&& DOES extend qualifying temporary lifetime; exception applies to reference parameters/returns and specific initialization contexts, not every rvalue reference. g++ -std=c++20 -fsyntax-only static_assert regressions passed local T&& lifetime, copy selection after suppression of implicit move, and legal constexpr local mutation. Source list above includes N4861, C++ Core Guidelines and Itanium ABI.

Judgment recorded: resource-owning-destructor → prerequisite → rule-of-five is scoped to cleanup in a class directly owning a releasable raw resource without an owning member to perform cleanup. It is explicitly a design guideline; rule-of-zero remains a separate boundary. This is not a claim that declaring a destructor automatically requires all five members by the language. No other unresolved factual claim identified; Claude review pending.

Four checks:

```
$ python3 tools/build_cpp_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/cpp-causation-v0/foundations.jsonl with 162 records
splits: {'cross_domain_holdout': 6, 'sealed_test': 16, 'train': 120, 'validation': 20}
kinds: {'boundary': 5, 'concept': 38, 'counterexample': 6, 'relation': 104, 'synthetic_control': 4, 'worked_example': 5}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id cpp-causation-v0
{
  "schema_version": 1,
  "world_id": "cpp-causation-v0",
  "adapter_independent": true,
  "record_count": 162,
  "node_count": 58,
  "edge_count": 104,
  "negative_pair_count": 4,
  "domains": [
    "language-ecosystems"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "7625ec4d090d263df75b14319c1409f7379dc00f72b2086ed01552e8a309765b",
    "lexicon.json": "f88aa7dec0f767f7ad2576c032770f56f50669d40201ff24c875566777de1e5e",
    "nodes.jsonl": "3255f715233aa88e014f69d38a77a2302b5899e9980d05b8527383f60dc26344",
    "records.jsonl": "0a2d366c2a487e03b1d936960fc54dabfcfdc88572330282584e72f78c316b65",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "f03f858f446d8dd3017ff5aaa7abf2d9664a9aae8909c3096616222eec49a75d",
    "split-manifest.json": "2564b9a64603246bdfd47bd0826c530e25d168ed3aeeda2b95866bfe9fd4e88d",
    "training-graph.json": "021a4c931a2b06a9642d633e4a5dec583e463ac6753d1e97cbc2b0b15dbcba19"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
cpp-causation-v0 | RAII resource lifetime -> prevents -> Skipped resource cleanup | C++20; acquisition transfers the resource into a completed automatic owner whose non-throwing destructor releases it, and exit follows normal return or unwinding
cpp-causation-v0 | Stack object scope -> causes -> Deterministic destructor | C++20; control leaves the block normally or through stack unwinding and the object's destructor has not already been invoked manually
cpp-causation-v0 | Deterministic destructor -> prevents -> Memory leak | C++20; the invoked destructor correctly deletes the sole owned allocation exactly once using its matching deallocation mechanism
cpp-causation-v0 | Heap allocation with new -> causes -> Memory leak | C++20; a successful ordinary allocating new-expression is not adopted by an owner and every usable pointer is lost before a matching delete
cpp-causation-v0 | unique_ptr ownership -> prevents -> Memory leak | C++20; unique_ptr retains ownership through destruction, its deleter correctly releases the allocation and release() has not abandoned ownership
cpp-causation-v0 | shared_ptr refcount -> prevents -> Memory leak | C++20; all external strong owners are eventually destroyed, the control block uses a correct deleter and no independent raw allocation is being claimed
cpp-causation-v0 | shared_ptr cycle -> inhibits -> shared_ptr refcount | C++20; each object in an otherwise unreachable ownership cycle retains a strong shared_ptr to the next object
cpp-causation-v0 | weak_ptr cycle break -> prevents -> shared_ptr cycle | C++20; replacing the necessary back edges with weak_ptr removes every strong cycle and all external strong owners are later released
cpp-causation-v0 | Dangling pointer -> causes -> Undefined behaviour | C++20; code dereferences a pointer to deallocated storage to read the former object's value without a new valid object and pointer relationship
cpp-causation-v0 | Iterator invalidation -> causes -> Dangling pointer | C++20; a std::vector<T> with T other than bool reallocates and an old element pointer still refers to the released allocation
cpp-causation-v0 | Vector contiguous storage -> causes -> Iterator invalidation | C++20; std::vector<T> with T other than bool actually reallocates its element storage during growth
cpp-causation-v0 | Move semantics -> causes -> Moved-from state | C++20; a standard-library object's move constructor or move assignment is actually invoked successfully rather than merely applying std::move
cpp-causation-v0 | Moved-from state -> prevents -> Undefined behaviour | C++20; a standard-library type guarantees valid-but-unspecified state and the chosen operation has no unmet precondition
cpp-causation-v0 | Move semantics -> inhibits -> Copy constructor | C++20; construction from a non-const expiring object selects an accessible move constructor, and copy elision does not remove the operation
cpp-causation-v0 | Resource-owning destructor -> prerequisite -> Rule of five | C++20 design guideline; the class directly owns the releasable raw resource, no owning member handles cleanup and the five-member design must release that resource at destruction
cpp-causation-v0 | Copy constructor -> prevents -> Implicit move constructor | C++20; the class declares a copy constructor, including one explicitly defaulted or deleted, and supplies no move constructor of its own
cpp-causation-v0 | Exception unwinding -> causes -> Deterministic destructor | C++20; control unwinds toward a matching handler and the objects were fully constructed before the throw
cpp-causation-v0 | Const correctness -> enables -> Reference binding | C++20; the reference type is const T& and the initializer is reference-compatible or undergoes a permitted conversion
cpp-causation-v0 | Reference binding -> prevents -> Reference reseating | C++20; ordinary assignment through a live reference assigns to its referent rather than changing the binding
cpp-causation-v0 | Template instantiation -> enables -> Generic static dispatch | C++20; substituting a concrete template argument makes a well-formed dependent call select a non-virtual function
cpp-causation-v0 | Generic static dispatch -> prevents -> Vtable dispatch | C++20 on a vtable-based implementation; the relevant call is resolved to a non-virtual function rather than routed through a virtual call
cpp-causation-v0 | Virtual function -> enables -> Vtable dispatch | C++20 on a vtable-based ABI such as Itanium; an unqualified virtual call through a valid base pointer remains indirect after optimization
cpp-causation-v0 | Override checking -> causes -> Override signature error | C++20; a member marked override has no matching virtual base function under the language's override rules
cpp-causation-v0 | Object slicing -> inhibits -> Virtual function | C++20; a base value is copy-constructed from a derived object and a subsequent virtual call uses the standalone base value
cpp-causation-v0 | Value semantics default -> enables -> Copy constructor | C++20; a copyable value type is initialized from an lvalue and its copy constructor implements independent value semantics
cpp-causation-v0 | Temporary lifetime extension -> prevents -> Dangling pointer | C++20; a local const lvalue reference or local rvalue reference directly binds a temporary through a lifetime-extending initializer and the pointer is used only while that reference lives
cpp-causation-v0 | Cross-unit dynamic initialization -> enables -> Use before initialization | C++20; non-local objects have no guaranteed dependency ordering across translation units and the consuming initializer can run before the dependency's dynamic initializer
cpp-causation-v0 | unique_ptr ownership -> enables -> Move semantics | C++20; a valid unique_ptr move operation transfers its managed pointer and compatible deleter to another owner
cpp-causation-v0 | shared_ptr refcount -> enables -> shared_ptr cycle | C++20; managed nodes contain strong shared_ptr links forming an ownership cycle without a weak back edge
cpp-causation-v0 | Heap allocation with new -> causes -> Dangling pointer | C++20; a matching delete releases the dynamic object's storage while another pointer still retains its former address
cpp-causation-v0 | unique_ptr ownership -> prevents -> shared_ptr refcount | C++20; one unique_ptr owns the resource and no shared_ptr control block has been created for it
cpp-causation-v0 | Reference binding -> prevents -> Object slicing | C++20; an argument passes as a base-class reference without constructing or assigning a separate base value
cpp-causation-v0 | Move semantics -> enables -> Vector contiguous storage | C++20; std::vector growth relocates elements whose accessible move constructor is noexcept and transfers resources cheaply, allowing move_if_noexcept-style relocation
cpp-causation-v0 | weak_ptr cycle break -> enables -> shared_ptr refcount | C++20; weak_ptr::lock observes a non-expired control block and atomically returns a shared_ptr owner for the duration of access
cpp-causation-v0 | Const correctness -> causes -> Const modification rejection | C++20; a program directly assigns a non-mutable const-qualified scalar or data member without casts or custom indirection
cpp-causation-v0 | Exception unwinding -> prevents -> Memory leak | C++20; propagation to a matching handler unwinds an automatic RAII owner with a correct non-throwing destructor and no abandoned raw allocation
```


### Parallel-chat blocked audit (2026-10-02)

The same ownership conflict persisted across three consecutive goal turns in chat `01a0ff6a-67e9-7162-8178-f1c11423c7ef`. Live app snapshots still report existing chat `01a0ff59-a0e2-7c82-849d-353d175d456f` active and its turn in progress; Git still shows uncommitted Step 0 edits. The preceding continuation performed a verified wait on that live chat. No user answer authorizing a message or choosing takeover has arrived. The blocked threshold is met for this second chat only; the 104-world objective remains incomplete and the existing chat remains active. Required unblock: user chooses the owning chat, or external state clears the conflict. No new relations were authored by this chat.

## Step 0: go-causation-v0

Commit: `bcf1867` (`Review fixes: go`).
Counts: 40 concepts, 32 relations, 5 myths, 4 boundaries, 4 examples, 4 controls.
Relations by kind: {"causes": 8, "enables": 7, "inhibits": 1, "predicts": 2, "prerequisite": 2, "prevents": 12}.
Probes/tasks: not applicable to Step 0.

Self-review (passes overlap): 40 originals → 31 retained plus one new relation, nine drops. Direction pass corrected 13 endpoints and eight kinds. Counterexample pass tightened all 32 conditions. Version pass pins implementation-dependent gc runtime/compiler edges to Go1.27 and loop closure semantics to Go1.22+ compiler AND module go>=1.22 with declared iteration variables. Parent found and worker fixed duplicate panic-recover → termination pair by introducing Successful panic recovery and Unrecovered panic concepts; Channel send blocking now correctly includes buffered-send cases. Zero duplicate pairs/conditions remain. Myth pass revised all five. Count pass 100% causal kinds, no padding. Open doubts: no unresolved Go claim identified; Claude review pending.

Drops:
- unbuffered-synchronizes: circular waiting definition.
- waitgroup-orders-completion: waiting does not cause goroutine launch/completion.
- implicit-decouples: interface satisfaction does not enable embedding.
- errors-prevent-panic-flow: an error check cannot prevent independent panic.
- ok-idiom-rests-on-zeros: multiple returns do not cause zero values.
- scheduler-runs-others: scheduler does not enable channel blocking.
- nil-box-wraps-typed-nil: nil distinction does not cause interface satisfaction.
- append-enables-streaming: no communication mechanism or spec doubling guarantee.
- escape-predicts-slice-life: slice validity is semantic, not contingent on a chosen allocation strategy.

New relation map-order-enables-variation states permission rather than guaranteed differing orders. Primary references registered above: Go memory model, runtime GC guide, Go1.22 loop change, sync and context.
Parent final concept correction: an atomic write conflicting with a plain read is also a race; definition now requires at least one write and at least one non-atomic access. These four checks are rerun after that change.

Four checks:

```
$ python3 tools/build_go_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/go-causation-v0/foundations.jsonl with 156 records
splits: {'cross_domain_holdout': 6, 'sealed_test': 15, 'train': 120, 'validation': 15}
kinds: {'boundary': 4, 'concept': 41, 'counterexample': 5, 'relation': 98, 'synthetic_control': 4, 'worked_example': 4}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id go-causation-v0
{
  "schema_version": 1,
  "world_id": "go-causation-v0",
  "adapter_independent": true,
  "record_count": 156,
  "node_count": 58,
  "edge_count": 98,
  "negative_pair_count": 4,
  "domains": [
    "language-ecosystems"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "3a052383cd93a4ed09a53c271b6b616aa0934307bf9a680f6e9dff1752ce7355",
    "lexicon.json": "c8d8bec8a79c7ec4816165323dea517f484bdf51d1cc441e1053bc8120823873",
    "nodes.jsonl": "8f08a458397a2d142d711102c7a42290e6755fe6aca1c9535b18ce709e7a25ef",
    "records.jsonl": "5e9965d52ae49f718a74392ab50f98b568141895ea77aca3c6bfa9b8136137bd",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "40d0270fa187c7d19f20347532ff32323d6422c57b5857c9c2d7cc478b8c3b4b",
    "split-manifest.json": "2b467a47a4b3939cdeb68a7d3826a79b81dab399e03a1bcd2c7a3e5b614d5351",
    "training-graph.json": "26348bd6b7cbf1f9c2f39ac469b04087a2cd7cac6444eaa6f13890032d45677e"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
go-causation-v0 | M-N goroutine scheduling -> enables -> Goroutine launch | Go 1.27 gc runtime; ordinary go statements create goroutines not explicitly locked to OS threads
go-causation-v0 | Channel receive -> prerequisite -> Channel send | Go 1; the channel is non-nil, open and unbuffered and the send completes normally
go-causation-v0 | Buffered channel -> prevents -> Channel send blocking | Go 1; the channel is open and non-nil and has room for the sent element at the moment of the send
go-causation-v0 | Channel send -> causes -> Channel deadlock | Go 1; all goroutines capable of releasing an unbuffered send are in a closed cycle of channel waits with no external unblock event
go-causation-v0 | Select statement -> prevents -> Channel deadlock | Go 1; select has a default clause, so selection itself never blocks, and evaluation of operands and the selected body do not block
go-causation-v0 | Share memory by communicating -> prevents -> Data race in Go | Go 1 memory model; the sender ceases access before sending ownership and the receiver alone accesses the data after receipt
go-causation-v0 | Mutex protection -> prevents -> Data race in Go | Go 1 memory model; every conflicting access to the protected memory occurs while holding the same non-copied mutex
go-causation-v0 | Escape analysis to heap -> prevents -> Stack allocation in Go | Go 1.27 gc compiler; an escaping allocation remains after optimization and is assigned to the heap rather than the current frame
go-causation-v0 | Stack allocation in Go -> inhibits -> Heap allocation rate | Go 1.27 gc compiler; otherwise equivalent executed allocations use stack storage instead of heap storage and are not optimized away
go-causation-v0 | Concurrent garbage collector -> enables -> Goroutine launch | Go 1.27 gc runtime; the collector is in a concurrent phase rather than a stop-the-world phase and runnable mutator work is scheduled
go-causation-v0 | Nil interface versus nil pointer -> predicts -> Error value returns | Go 1; a nil pointer whose type implements error is returned directly from a function with an error result
go-causation-v0 | Multiple return values -> enables -> Error value returns | Go 1; a function declares a result pair such as (Value, error) and follows the nil-error success convention
go-causation-v0 | Defer stack -> enables -> Panic and recover | Go 1; the deferred function directly invokes recover while unwinding an active panic in the same goroutine
go-causation-v0 | Successful panic recovery -> prevents -> Program termination from panic | Go 1; recover is called directly by a deferred function in the panicking goroutine and cleanup raises no replacement panic
go-causation-v0 | Slice backing array -> causes -> Data race in Go | Go 1 memory model; different goroutines access overlapping array cells through slices, at least one writes, and no synchronization orders them
go-causation-v0 | Append beyond capacity -> causes -> Slice backing array | Go 1; the new length exceeds the old capacity and the append succeeds rather than failing allocation
go-causation-v0 | Embedding composition -> enables -> Implicit interface satisfaction | Go 1; the promoted methods are unambiguous, have the required signatures and belong to the relevant value or pointer method set
go-causation-v0 | Unexported interface method -> prevents -> Implicit interface satisfaction | Go 1; the implementing type is in a different package and does not inherit the original package's method through embedding
go-causation-v0 | Context cancellation -> prevents -> Channel send blocking | Go 1.7+ context; the blocked select includes the context Done channel and returns when cancellation closes it
go-causation-v0 | Type zero values -> causes -> Nil interface versus nil pointer | Go 1; an uninitialized variable of type *T is nil and is then returned or assigned as an interface that *T implements
go-causation-v0 | Package initialisation order -> prerequisite -> Main function entry | Go 1; a Go program executes imported package initializers and main package initializers successfully before calling main.main
go-causation-v0 | Loop variable capture -> prevents -> Data race in Go | Go 1.22+ compiler with module go version >= 1.22 in go.mod; the loop declares its iteration variable, each closure only reads its own captured variable and no explicit outer-variable assignment is used
go-causation-v0 | Escape analysis to heap -> causes -> Heap allocation rate | Go 1.27 gc compiler; compared with the same workload using stack storage, retained escaping allocations execute repeatedly and are not eliminated
go-causation-v0 | Select statement -> enables -> Channel receive | Go 1; select has receive cases with at least one ready channel and chooses one ready communication
go-causation-v0 | Buffered channel -> prevents -> Channel receive blocking | Go 1; the buffer still contains an element at the moment the receive is performed
go-causation-v0 | Channel send -> causes -> Goroutine leak | Go 1; a live program leaves a worker sending forever on an open unbuffered channel with no future receiver or cancellation alternative
go-causation-v0 | WaitGroup completion -> prevents -> Early main return | Go 1 sync.WaitGroup; main calls Wait before returning, positive Add calls precede the wait and each worker calls Done only after finishing its required work
go-causation-v0 | Channel receive -> predicts -> Type zero values | Go 1; the channel is closed and empty, so receive returns the element type's zero value immediately and the comma-ok result is false
go-causation-v0 | Channel send -> causes -> Panic and recover | Go 1; a send is actually executed on a closed channel, including a selected send case
go-causation-v0 | Unrecovered panic -> causes -> Program termination from panic | Go 1; an active panic reaches the top of a goroutine after its deferred calls finish without recovery
go-causation-v0 | Context cancellation -> prevents -> Goroutine leak | Go 1.7+ context; every potentially indefinite worker wait observes Done and the worker exits on cancellation without launching untracked work
go-causation-v0 | Unspecified map iteration order -> enables -> Order-dependent output variation | Go 1; a program derives output directly from map range order without sorting keys or using an order-independent operation
```

## Step 0: chemistry-causation-v0

Commit: `b682ff8` (`Review fixes: chemistry`).
Counts: 41 concepts, 34 relations, 5 myths, 3 boundaries, 4 examples, 4 controls.
Relations by kind: {"causes": 10, "enables": 10, "inhibits": 3, "predicts": 8, "prerequisite": 2, "prevents": 1}.
Probes/tasks: not applicable to Step 0.

Self-review (overlapping passes): 41 original relations → 34 retained; eight endpoint changes, ten kind corrections, all 34 conditions tightened, seven drops. Version/regime pass explicitly states gas-phase bond accounting, dilute-solution activity approximation, solvent/temperature and equilibrium hypotheses. Myth pass corrected four of five. Count and duplicate passes: 100% causal kinds, no padding, zero repeated pairs/conditions. Parent read all final concepts/relations. Open doubts: no unresolved factual edge retained; Claude review pending.

Drops:
- imf-causes-boiling: near duplicate; retained named ethanol/dimethyl ether comparison.
- activation-prereq-reaction: duplicate pair; barrier inhibition retained.
- balanced-prereq-limiting: near duplicate; stoichiometric prediction chain retained.
- imf-prereq-states: duplicate pair.
- reaction-causes-bonds: reaction definition restated.
- redox-enables-transfer: electron-transfer definition restated.
- exothermic-fuels-later-steps: target was barrier, not overcoming it.

All review fixes addressed: surroundings temperature targets, polar-water hydration source, network-covalent-solid source, strong acid/base condition at neutral pH, acid/base Brønsted definitions, dynamic amounts constant and Ka distinct from concentration. Sources added: none; primary checks used IUPAC definitions and NIST ethanol/ether phase data. Some direct canonical opens were blocked; indexed primary material supported those checks.

Four checks:

```
$ python3 tools/build_chemistry_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/chemistry-causation-v0/foundations.jsonl with 157 records
splits: {'cross_domain_holdout': 8, 'sealed_test': 16, 'train': 117, 'validation': 16}
kinds: {'boundary': 3, 'concept': 42, 'counterexample': 5, 'relation': 99, 'synthetic_control': 4, 'worked_example': 4}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id chemistry-causation-v0
{
  "schema_version": 1,
  "world_id": "chemistry-causation-v0",
  "adapter_independent": true,
  "record_count": 157,
  "node_count": 58,
  "edge_count": 99,
  "negative_pair_count": 4,
  "domains": [
    "chemistry"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "924e930c78c74c8bd9b2b061bd9152c8883804b7de3b36977f96f555ccd66d21",
    "lexicon.json": "e064e9ea98feeddf2bf025acb3f6eb4167a6be634cef80b36bc512fc18ac0cde",
    "nodes.jsonl": "203fc18cb46f6556000e6d2e14a4d21cbf245fc1f463696873eee6be549a42f1",
    "records.jsonl": "0a5eb04324adbee489b3c39ccbde7e9d9e330ee8d03bbac66c97bff9a5eb7ed8",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "606b28a90b8c5136198fa8410f5ff54ed6f176c5ee4aa471d914d76405b47266",
    "split-manifest.json": "dcd25572ff560f16ee5f551c96c06677448602b752e52b538f0f0cb16f20c503",
    "training-graph.json": "81c4e5adbbc97adae1e442adb60666d3405a64ab31307b32f767cd65f3817bee"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
chemistry-causation-v0 | Valence electrons -> enables -> Chemical bond | atoms can approach and their combined electronic state is lower in energy than the separated state
chemistry-causation-v0 | Octet rule tendency -> predicts -> Covalent bond | neutral second-row C, N, O or F centres have ordinary two-electron bonds and no radicals or electron-deficient bonding
chemistry-causation-v0 | Electronegativity difference -> predicts -> Ionic bond | bonded atom pairs are compared using the same electronegativity scale as a qualitative trend rather than a sharp ionic threshold
chemistry-causation-v0 | Electronegativity difference -> predicts -> Bond polarity | an ordinary heteronuclear covalent bond is described by the electronegativity model without competing charge or coordination effects
chemistry-causation-v0 | Bond polarity -> enables -> Polar molecule | the bond dipoles and other contributions to the molecular dipole do not cancel by geometry
chemistry-causation-v0 | Polar molecule -> enables -> Hydrogen bonding between molecules | an O-H, N-H or F-H donor encounters an accessible compatible lone-pair acceptor with suitable orientation
chemistry-causation-v0 | Hydrogen bonding between molecules -> causes -> Boiling point of a liquid | ethanol is compared with dimethyl ether at the same pressure, so intermolecular O-H donation is available to ethanol but not to its ether isomer
chemistry-causation-v0 | Intermolecular forces -> enables -> States of matter changes | a molecular substance below its critical pressure is heated or cooled across its liquid-vapour coexistence curve
chemistry-causation-v0 | Conservation of mass -> predicts -> Balanced equation | a closed chemical reaction has no nuclear transmutation and all reactants and products are included
chemistry-causation-v0 | Balanced equation -> predicts -> Mole ratios in an equation | the coefficients describe the same specified net reaction and all amounts refer to that reaction extent
chemistry-causation-v0 | Mole ratios in an equation -> predicts -> Limiting reagent | initial reactant amounts are known and a single irreversible reaction consumes them in the stated proportions
chemistry-causation-v0 | Limiting reagent -> predicts -> Chemical reaction | the product coefficient is known and theoretical yield assumes complete conversion without competing reactions
chemistry-causation-v0 | Exothermic reaction -> causes -> Surroundings temperature | in a gas-phase bond-energy balance at constant pressure, forming product bonds releases more energy than breaking reactant bonds costs, and finite surroundings absorb that heat without phase change or thermostat removal
chemistry-causation-v0 | Endothermic reaction -> causes -> Surroundings temperature | in a gas-phase bond-energy balance at constant pressure, breaking reactant bonds costs more energy than forming product bonds releases, and finite surroundings supply that heat without phase change or replacement heating
chemistry-causation-v0 | Activation energy barrier -> inhibits -> Chemical reaction | a positive-barrier Arrhenius process is compared at the same temperature, reactant activities and pre-exponential factor
chemistry-causation-v0 | Catalyst speeding a reaction -> inhibits -> Activation energy barrier | the stated catalyst provides a kinetically accessible pathway with a lower rate-controlling barrier than the uncatalysed reaction
chemistry-causation-v0 | Dynamic equilibrium -> prevents -> Chemical reaction | temperature, pressure and species inventories remain fixed in a closed equilibrated reacting system
chemistry-causation-v0 | Equilibrium condition change -> causes -> Dynamic equilibrium | a reactant activity changes so that the reaction quotient differs from the equilibrium constant at fixed temperature, and forward and reverse reactions remain accessible
chemistry-causation-v0 | Acid as proton donor -> causes -> pH scale | acid is added to initially neutral dilute water at fixed temperature with negligible volume change and no competing buffer or base
chemistry-causation-v0 | Base as proton acceptor -> causes -> pH scale | base is added to initially neutral dilute water at fixed temperature with negligible volume change and no competing buffer or acid
chemistry-causation-v0 | pH scale -> predicts -> Concentration of a solution | aqueous solutions are sufficiently dilute that hydrogen-ion activity coefficients are approximately one at the same temperature
chemistry-causation-v0 | Neutralization reaction -> causes -> pH scale | dilute aqueous strong acid and strong base are mixed in stoichiometrically equal proton equivalents at 25 degrees Celsius, with no hydrolysing spectator ions
chemistry-causation-v0 | Neutralization reaction -> causes -> Salt products | an acid reacts with a metal hydroxide base and the salt is represented in the net molecular products, whether it remains dissolved or precipitates
chemistry-causation-v0 | Oxidation losing electrons -> prerequisite -> Reduction gaining electrons | the complete redox system includes both the electron donor and electron acceptor rather than an isolated half-reaction
chemistry-causation-v0 | Combustion reaction -> enables -> Oxidation losing electrons | an ignited carbonaceous fuel reacts with oxygen and oxidation states are used to account for the electron transfer
chemistry-causation-v0 | Dissolving a solute -> enables -> Concentration of a solution | a measured solute amount dissolves completely below saturation and the final solution volume is known
chemistry-causation-v0 | Temperature increase -> causes -> Solubility shift with temperature | the dissolution enthalpy remains positive over the temperature interval and no solid-phase change or competing speciation alters the dilute-solution equilibrium
chemistry-causation-v0 | Concentration of a solution -> enables -> Precipitate formation | the appropriate ions are present at fixed temperature and nucleation and crystal growth can occur
chemistry-causation-v0 | Polar water molecules -> enables -> Dissolving a solute | the solid-water combination has a favourable dissolution free energy at the current unsaturated composition
chemistry-causation-v0 | Network covalent solid -> inhibits -> Dissolving a solute | the solid is diamond or quartz in water at ambient temperature without a reagent that chemically attacks the network
chemistry-causation-v0 | Polar molecule -> enables -> Dissolving a solute | for the specified molecular solute, solvent interactions and mixing entropy outweigh the free-energy cost of separating solute and solvent particles
chemistry-causation-v0 | Dynamic equilibrium -> prerequisite -> Le Chatelier shift | the qualitative prediction compares an initially equilibrated system with its response after a small imposed perturbation
chemistry-causation-v0 | Combustion reaction -> causes -> Surroundings temperature | an ignited ordinary fuel-oxygen combustion transfers net heat to finite surroundings without compensating cooling or phase change
chemistry-causation-v0 | Dissolving a solute -> enables -> Chemical reaction | the dissolved species remain reactive and a formerly surface-limited reaction gains access to solute throughout the solution
```

## Step 0: biology-causation-v0

Commit: `f431543` (`Review fixes: biology`).
Counts: 38 concepts, 35 relations, 5 myths, 4 boundaries, 4 examples, 4 controls.
Relations by kind: {"causes": 3, "enables": 20, "inhibits": 3, "predicts": 1, "prerequisite": 7, "prevents": 1}.
Probes/tasks: not applicable to Step 0.

Self-review (overlapping passes): 40 original relations → 35 retained; eleven endpoint changes including parent-requested DNA template exposure, seven kind corrections, all 35 conditions tightened, five drops. Version/regime pass specifies cellular/organism/pathway assumptions. Myth pass corrected one; synonymous-mutation boundary added. Count/duplicate pass: 100% causal kinds, no padding, no repeated pairs/conditions. Parent read all final concepts/relations.

Drops:
- diffusion-prevents-pumping: diffusion does not prevent active transport.
- atp-prereq-pumping: duplicate and too universal; ATP-driven enables edge retained.
- codons-enable-redundancy: redundant-code definition restated.
- misfold-predicts-mutation: misfolding has other causes.
- mitosis-predicts-copies: invalid converse of successful replication.

Photosynthesis enables glucose synthesis through carbon-fixation intermediates; light supplies energy rather than carbon matter. Membrane prerequisite specifically targets mitochondrial oxidative phosphorylation. Synonymous codons preserve amino acid identity but expression/splicing effects remain in a boundary. Sickle-cell example identifies deoxygenated haemoglobin polymerization. Open doubts: no unresolved biological claim retained; pathway restrictions are part of each edge and Claude review remains pending. Sources added: none. Primary evidence includes NCBI chapters NBK26819 and NBK26894, transcription/cellular energy chapters and NHGRI sickle-cell glossary.

Four checks:

```
$ python3 tools/build_biology_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/biology-causation-v0/foundations.jsonl with 153 records
splits: {'cross_domain_holdout': 6, 'sealed_test': 16, 'train': 116, 'validation': 15}
kinds: {'boundary': 4, 'concept': 39, 'counterexample': 5, 'relation': 97, 'synthetic_control': 4, 'worked_example': 4}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id biology-causation-v0
{
  "schema_version": 1,
  "world_id": "biology-causation-v0",
  "adapter_independent": true,
  "record_count": 153,
  "node_count": 56,
  "edge_count": 97,
  "negative_pair_count": 4,
  "domains": [
    "biology"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "2c2f86409ec154250280efb02b8be7dea291b48e420998f7b9f5bb63b57c7423",
    "lexicon.json": "e6cd054a25ff5af7712f1a3ef71e116aef8763f5e7d46d7184141fed01cbcdeb",
    "nodes.jsonl": "b96ae74432b67d0e31f41de3db368f3636acf46dc5389b9e5b36caf65dbcbca6",
    "records.jsonl": "6c40fdc5eeee6a55c53ae10db1278c882e7ce1ef417487915cbee3a303051569",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "6512babc0e68254974b93100a0b0dbec3eb467ec4412910dd8a0f73ca2a51496",
    "split-manifest.json": "d278dda1a5a874a361ef01b253ba6c4e2404d4fda2609cd0b471c67dc4b46304",
    "training-graph.json": "cb13b3ff2c5fd045a849b1f7657ad2cb1b98bbaedc4185e7ac2ff332c92f7f1f"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
biology-causation-v0 | Cell membrane barrier -> enables -> Selective permeability | an intact lipid bilayer contains selective channels or carriers and lacks a nonspecific membrane rupture
biology-causation-v0 | Cell membrane barrier -> prerequisite -> Osmosis of water | the process under discussion is trans-plasma-membrane osmosis, with water permeant and the relevant solute effectively impermeant
biology-causation-v0 | Facilitated transport -> enables -> Diffusion down a gradient | a matching passive channel or carrier is present and the solute has a favourable electrochemical gradient
biology-causation-v0 | Cellular respiration -> causes -> ATP energy currency | a eukaryotic cell oxidizes available substrate with oxygen as terminal electron acceptor and has coupled ATP synthesis, ADP and phosphate
biology-causation-v0 | Glucose sugar -> enables -> Cellular respiration | the cell has active glucose-catabolic enzymes, required cofactors and an available terminal electron acceptor
biology-causation-v0 | Photosynthesis capture -> enables -> Glucose sugar | oxygenic plant photosynthesis supplies ATP and NADPH for carbon fixation, and downstream carbohydrate synthesis converts fixed-carbon intermediates into hexoses
biology-causation-v0 | Enzyme substrate catalysis -> causes -> Activation barrier lowering | an active enzyme binds its substrate and supports the transition state under its specified solution conditions
biology-causation-v0 | Enzyme denaturation -> inhibits -> Enzyme substrate catalysis | unfolding or structural disruption affects an enzyme whose active site requires the lost native fold
biology-causation-v0 | pH effect on proteins -> inhibits -> Enzyme substrate catalysis | pH moves away from the activity range of the specified enzyme and changes a group required for substrate binding or catalysis
biology-causation-v0 | pH effect on proteins -> enables -> Enzyme denaturation | a pH change destabilizes a pH-sensitive enzyme sufficiently that its folded population decreases under the exposure conditions
biology-causation-v0 | Complementary base pairing -> enables -> DNA double helix | complementary antiparallel DNA strands encounter one another in solution below their duplex melting temperature
biology-causation-v0 | Complementary base pairing -> enables -> Semi-conservative replication | DNA polymerase has a template, a primed terminus, nucleotide substrates and the required replication machinery
biology-causation-v0 | DNA base mismatch -> enables -> Mutation of DNA | the mismatch escapes proofreading and repair and a subsequent replication or repair event fixes the altered sequence in a descendant duplex
biology-causation-v0 | Semi-conservative replication -> prerequisite -> Mitosis division | a diploid eukaryotic cell follows a chromosome-conserving mitotic cycle rather than an experimentally checkpoint-bypassed or pathological division
biology-causation-v0 | Complementary base pairing -> enables -> Transcription to mRNA | RNA polymerase transcribes a protein-coding DNA template with available ribonucleotides, pairing RNA U with DNA A
biology-causation-v0 | Codon triplet code -> enables -> Translation at ribosomes | a ribosome uses the cellular genetic code in an established reading frame with charged tRNAs and termination factors
biology-causation-v0 | Redundant genetic code -> prevents -> Protein sequence change | the altered coding codon specifies the same amino acid in the applicable genetic code and does not alter splicing or the reading frame
biology-causation-v0 | Mutation of DNA -> enables -> Protein folding into shape | the expressed coding mutation changes a structurally important amino acid in a folding-dependent protein
biology-causation-v0 | Protein folding into shape -> enables -> Protein molecular function | the specified protein requires the resulting folded conformation and has its required partners and cofactors
biology-causation-v0 | Enzyme denaturation -> inhibits -> Protein molecular function | the enzyme remains denatured during the assay and its measured activity depends on the lost fold
biology-causation-v0 | Meiosis halving -> enables -> Fertilization restoring | a diploid animal's conventional sexual life cycle produces functional haploid gametes that subsequently fuse
biology-causation-v0 | Fertilization restoring -> enables -> Dominant and recessive alleles | two haploid gametes carry different alleles of an autosomal locus exhibiting complete dominance
biology-causation-v0 | Dominant and recessive alleles -> predicts -> Phenotypic trait expression | one autosomal locus has complete penetrance without relevant epistasis or environmental modification in the population being modelled
biology-causation-v0 | Gene expression control -> enables -> Phenotypic trait expression | the measured trait responds to expression of the regulated gene in the specified cell type and developmental setting
biology-causation-v0 | Cell membrane barrier -> prerequisite -> Membrane receptor signalling | the receptor's signalling mechanism requires its transmembrane orientation and intact intracellular and extracellular compartments
biology-causation-v0 | Membrane receptor signalling -> enables -> Gene expression control | ligand activation reaches a functional pathway that modifies a transcription regulator in the receiving cell
biology-causation-v0 | Osmotic solute gradient -> causes -> Osmosis of water | the membrane passes water but not the gradient-forming solute, temperatures are equal and no opposing hydrostatic pressure cancels the water chemical-potential difference
biology-causation-v0 | ATP energy currency -> enables -> Active transport pumping | a functional primary ATP-driven pump has ATP and a hydrolysis free-energy release sufficient to overcome the cargo's electrochemical gradient
biology-causation-v0 | ATP energy currency -> prerequisite -> Translation at ribosomes | the cellular translation cycle uses ATP-dependent aminoacyl-tRNA synthetases and must replenish charged tRNAs, while ribosomal steps also consume GTP
biology-causation-v0 | Transcription to mRNA -> prerequisite -> Translation at ribosomes | a eukaryotic gene is expressed by nuclear transcription, RNA processing and export before its mRNA is translated in the cytoplasm
biology-causation-v0 | DNA template exposure -> prerequisite -> Transcription to mRNA | DNA-dependent RNA polymerase must expose a template strand in a transcription bubble of a double-stranded cellular gene
biology-causation-v0 | Meiosis halving -> enables -> Dominant and recessive alleles | a diploid parent is heterozygous at multiple loci and independent assortment or crossing-over changes the transmitted allele combinations
biology-causation-v0 | Enzyme substrate catalysis -> enables -> Cellular respiration | the required catabolic enzymes, substrates, electron carriers and acceptor are available in their functional compartments
biology-causation-v0 | Cellular respiration -> enables -> Active transport pumping | respiratory ATP production supplies a functional ATP-driven membrane pump with enough free energy to move its cargo against its gradient
biology-causation-v0 | Inner mitochondrial membrane -> prerequisite -> Mitochondrial oxidative phosphorylation | an intact mitochondrion generates ATP through a coupled respiratory chain and ATP synthase across its inner membrane
```

## Step 0: color-causation-v0

Commit: pending creation, title `Review fixes: color`.
Counts: 34 concepts, 27 relations, 5 myths, 8 boundaries, 4 examples, 4 controls.
Relations by kind: {"causes": 5, "enables": 10, "inhibits": 3, "predicts": 7, "prerequisite": 1, "prevents": 1}.
Probes/tasks: not applicable to Step 0.

Self-review (overlapping passes): 40 original relations → 26 retained plus one new bounded saturation relation; seven endpoint changes, ten kind corrections; all 27 final conditions reviewed. Fourteen drops; zero repeated pairs/conditions. Version pass specifies CSS Color4, WCAG2.2 and source-over/opaque backdrop assumptions. Myth pass corrected four. Count pass: 100% causal kinds, no padding. Parent read all final relations/myths/boundaries/examples.

Drops:
- additive-primaries: mixing type does not cause chosen primaries.
- subtractive-primaries: mixing type does not cause chosen primaries.
- hue-predicts-slice: circular coordinate definition.
- complements-oppose: circular definition.
- mixing-complements-dulls: wheel opposition does not guarantee neutral pigments.
- afterimage-predicts-complement: measured hues need not be exact complements.
- warm-predicts-cool: unsupported converse.
- medium-prereq-primaries: knowing a distinction is not physical prerequisite.
- deficiency-enables-luminance: deficiency does not create luminance.
- lightness-enables-contrast: perceived lightness does not determine WCAG contrast.
- simultaneous-predicts-misjudgement: replaced by direct surround intervention.
- dark-room-causes-glare: simultaneous contrast is not optical glare.
- deficiency-inhibits-harmony: unsupported aesthetic guarantee.
- luminance-predicts-lightness-roughly: insufficient perceptual regime.

Scientific correction to review wording: prolonged fixation is an enabling protocol, not a universal prerequisite; short/changing stimuli also induce afterimages. Saturation-strength edge is bounded, uses enables, and explicitly excludes a universal monotonic prediction. This sensitivity is retained as an open review point, not hidden as a guaranteed law. Alpha formula assumes opaque backdrop and common compositing space; physical light averaging additionally requires linear-light channels. New sources are the five color entries listed in shared source registration above. Existing CSS Color4 and WCAG2.2 retained. No tool blocker; Claude acceptance pending.

Four checks:

```
$ python3 tools/build_color_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/color-causation-v0/foundations.jsonl with 146 records
splits: {'cross_domain_holdout': 6, 'sealed_test': 18, 'train': 102, 'validation': 20}
kinds: {'boundary': 8, 'concept': 35, 'counterexample': 5, 'relation': 90, 'synthetic_control': 4, 'worked_example': 4}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id color-causation-v0
{
  "schema_version": 1,
  "world_id": "color-causation-v0",
  "adapter_independent": true,
  "record_count": 146,
  "node_count": 56,
  "edge_count": 90,
  "negative_pair_count": 4,
  "domains": [
    "typography-color-visual-design"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "1c20856e934c7d13e83b126af49fef361d461781ddbe968fc37d6964a82a7a9a",
    "lexicon.json": "9c0f96c14f5078b0b38ebc791f135b07539b8a773794f4c5c0fe8ccd89578df7",
    "nodes.jsonl": "d48f700088304f1ff4dd3574903871198cce7c6494954071a5ea543f1663deaa",
    "records.jsonl": "e6ede716d9a1e64368dee77c8c9c845318f041b993730ff76830effbdc6a766f",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "ee6765a0193a6dcd3269d672b29d75f00ecc108ee80577304beab1d09dd4f9ae",
    "split-manifest.json": "f108215a93fbea879962f0658ea3470922a4390a5cd09fbcf635994756b28002",
    "training-graph.json": "f65048a4deb5c9e4a3b5d282ff5760d7fda0a0afa97c36d2fa915bab33331b29"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
color-causation-v0 | Screen emissive pixels -> causes -> Additive RGB mixing | an RGB display emits independent channel contributions that combine without subtractive optical filtering between those contributions
color-causation-v0 | Print reflective inks -> causes -> Subtractive pigment mixing | transparent nonfluorescent ink layers add absorption over the same white substrate without adding light scattering or emission
color-causation-v0 | Hue wheel -> enables -> Hue angle | the CSS HSL convention fixes red at zero degrees and orders hues around the circle
color-causation-v0 | HSL notation -> predicts -> Hue angle | a chromatic CSS HSL colour has nonzero saturation and lightness strictly between zero and one hundred percent
color-causation-v0 | Luminance weights of R G B -> predicts -> Relative luminance | R, G and B are linear-light sRGB channels obtained by the WCAG 2.2 inverse transfer function rather than raw encoded byte values
color-causation-v0 | Relative luminance -> predicts -> Contrast ratio | the two final rendered colours are evaluated by WCAG 2.2 after alpha compositing and conversion to its relative-luminance representation
color-causation-v0 | Contrast ratio -> prerequisite -> WCAG contrast minimums | the content is subject to WCAG 2.2 text-contrast requirements and its text size, weight and applicable conformance level are known
color-causation-v0 | Surround luminance difference -> causes -> Simultaneous contrast illusion | equal small grey patches are viewed on uniform lighter and darker surrounds in the conventional simultaneous-brightness-contrast display
color-causation-v0 | sRGB gamma curve -> enables -> Relative luminance | the input is CSS sRGB and each channel is decoded with the piecewise sRGB transfer function before the WCAG linear-weight sum
color-causation-v0 | Alpha transparency blending -> enables -> Contrast ratio | foreground opacity lies strictly between zero and one and the backdrop changes so the two final rendered luminances have a different WCAG ratio
color-causation-v0 | Device gamut limit -> prevents -> Exact colour reproduction | the target is outside the calibrated device gamut under the declared viewing conditions and matching means exact colorimetric reproduction
color-causation-v0 | Tint and shade -> enables -> Perceived lightness | an opaque diffuse nonfluorescent paint mixture is viewed under fixed illumination and the added paint changes the mixture's reflectance toward white or black
color-causation-v0 | Hue wheel -> enables -> Colour harmony schemes | the scheme is a geometric palette recipe such as three hues spaced equally around the chosen wheel, with no claim of universal aesthetic preference
color-causation-v0 | Colour vision deficiency -> enables -> Red-green confusion risk | a viewer has a red-green deficiency and the selected pair falls within colours that viewer cannot reliably distinguish
color-causation-v0 | Lightness difference -> inhibits -> Red-green confusion risk | the pair has a perceptible lightness separation for the viewer and the task requires distinguishing the elements rather than correctly naming their red or green hues
color-causation-v0 | Hex colour notation -> enables -> Additive RGB mixing | CSS hexadecimal colour syntax is interpreted as nonlinear encoded sRGB channel values and the display pipeline renders the decoded colour
color-causation-v0 | HSL notation -> predicts -> Hex colour notation | an opaque in-range CSS HSL colour is converted using CSS Color 4 formulas and rounded to the nearest eight-bit channel value
color-causation-v0 | Colour saturation -> inhibits -> Neutral grey baseline | CSS HSL saturation increases from zero at fixed hue and lightness strictly between zero and one hundred percent, with sufficient display precision to show the change
color-causation-v0 | Screen emissive pixels -> causes -> Device gamut limit | a calibrated additive display has fixed primary spectra and bounded nonnegative channel intensities
color-causation-v0 | Print reflective inks -> causes -> Device gamut limit | the ink set, substrate, halftoning process and viewing illuminant are fixed; the print gamut need not be a subset of a particular display gamut
color-causation-v0 | Prolonged colour fixation -> enables -> Afterimage effect | a sighted observer maintains retinal adaptation to a visible coloured patch and then views an approximately uniform achromatic field
color-causation-v0 | Complementary colour pair -> enables -> Colour harmony schemes | the palette recipe is defined by a half-turn separation in that wheel and does not imply guaranteed contrast or visual appeal
color-causation-v0 | Alpha transparency blending -> predicts -> Composite RGB colour | normal source-over compositing uses an opaque backdrop, a foreground opacity alpha between zero and one, and F and B expressed in the same compositing colour space
color-causation-v0 | Neutral grey baseline -> predicts -> Relative luminance | a CSS sRGB grey has equal encoded red, green and blue channels and those channels have been decoded to linear light
color-causation-v0 | Hue angle -> predicts -> Hex colour notation | HSL saturation is positive, lightness is strictly between its endpoints, and eight-bit quantization has not erased the channel ordering
color-causation-v0 | Subtractive pigment mixing -> inhibits -> Perceived lightness | nonfluorescent transparent colorants add absorption without changing scattering, illumination or the observer's surrounding field
color-causation-v0 | Colour saturation -> enables -> Afterimage effect | a fixed-hue inducer is compared at the same luminance, exposure duration, retinal location and neutral test field within a range where stronger chromatic adaptation remains possible
```

## Scope expansion verified — 104 catalog worlds

Authorized handoff from chat 01a0ff6a-67e9-7162-8178-f1c11423c7ef reports Jesse selected this chat as sole implementation owner and supplied `/home/jesse/Downloads/1AUTHORING-PROMPT-ADVANCED-WORLDS.md`. Its content and the original docs-path prompt now both hash to `c764ed992b32471cac032ec49cc3a310851dd7239953bdc7b6ba287242b2a6ed`. Compared to the initially read 70-world prompt, it adds 34 Tier8 worlds, labels bridge Tier9, requires completing each new world before starting the next, and adds craft/legal authoring rules. The printed catalog has 104 distinct IDs/prefixes, every SUBJECT exists, and no Tier7 heading is printed. Follow printed order and bridge last. Earlier 70-world counts are historical. Duplicate-chat stop notes record only its coordination blocker and do not stop this owning goal. No duplicate world edits were made by that chat.

## Independent quantum review and final-source verification: quantum-causation-v0

Commit consolidation target, title `Review fixes: quantum`.
Counts: 40 concepts, 28 relations, 5 myths, 3 boundaries, 4 examples, 4 controls.
Relations by kind: {"causes": 2, "enables": 10, "inhibits": 2, "predicts": 9, "prerequisite": 3, "prevents": 2}.
Probes/tasks: not applicable to Step 0.

Independent review checkpoint after initial commit: six concept definitions repaired (Born basis, coherent amplitudes, double-slit apparatus, shell occupancy, Schrodinger and unitary evolution); parent additionally disambiguated Pauli as single-particle occupancy. Two relation hypotheses repaired (explicit CHSH observables and noncircular Pauli assumption); solar interband absorption narrowed; LED example replaced by atomic gas emission. All 28 edges independently reread, exact labels/verbs/pairs/conditions pass. Standard-library complex-matrix calculation gave E00=E01=E10=-0.7071067811865474, E11=0.7071067811865474 and CHSH S=-2.8284271247461894, agreeing with -2sqrt(2) within 1e-14. Counts unchanged; no new source. No remaining actionable issue identified; Claude acceptance remains pending. Corrections will be folded into the existing quantum commit, touching only commits authored by this goal on the current sweep branch; pre-existing history and other branch histories remain intact. Earlier hashes and checks are historical checkpoints.

Four checks:

```
$ python3 tools/build_quantum_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/quantum-causation-v0/foundations.jsonl with 147 records
splits: {'cross_domain_holdout': 5, 'sealed_test': 14, 'train': 112, 'validation': 16}
kinds: {'boundary': 3, 'concept': 41, 'counterexample': 5, 'relation': 90, 'synthetic_control': 4, 'worked_example': 4}
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
  "record_count": 147,
  "node_count": 57,
  "edge_count": 90,
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
    "edges.jsonl": "1604791662ea5df74fe8eff4d25972bc4023fa0f969c0b32912a7d6e303ae092",
    "lexicon.json": "895362240568f947cbaf42ffa1d6876bc2e09df7d3431f05b7ada12b23b9c1dd",
    "nodes.jsonl": "5b961a3dd7be365b704e65624a64984008302b0f315e8c14574ffb1f16b0af61",
    "records.jsonl": "e076a30f0d48e4b8886bd9bcd19e6a56592c82b44c5f79af0d1948102100bfb8",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "65ba5a6575b3616a20b95145ffe2fa6aeb9a4db70ce4e3dfe66226b5f0d46a3f",
    "split-manifest.json": "4053e334a3df9f8203d29f1c4896945e541e89195ae478607b7be87a171fa987",
    "training-graph.json": "81b75f5422e44cc5edbc2c904ebdcd627c6461e289f73bfc832c1640c15d89a7"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
quantum-causation-v0 | Photon frequency -> predicts -> Photon energy | a photon occupies a monochromatic mode of frequency f measured in the same inertial frame
quantum-causation-v0 | Photon energy -> prerequisite -> Photoelectric effect | electrons near the Fermi level escape a metal into vacuum by absorption of one photon; thermal and field assistance are negligible
quantum-causation-v0 | Work function -> prevents -> Photoelectric effect | hf is below the surface work function and multiphoton absorption, heating and field emission are negligible
quantum-causation-v0 | Superposition of states -> enables -> Interference pattern | path amplitudes overlap at the detector with stable relative phase and no which-path record exists
quantum-causation-v0 | Which-path information -> inhibits -> Interference pattern | an unobserved detector or environment stores distinguishable path records and no postselected quantum erasure is performed
quantum-causation-v0 | Born rule probabilities -> predicts -> Measurement collapse | an ideal projective measurement with a specified orthonormal basis is repeated on identically prepared systems
quantum-causation-v0 | Superposition of states -> predicts -> Born rule probabilities | the pure state is normalized and the measurement projects onto the orthonormal basis used in its expansion
quantum-causation-v0 | Uncertainty principle -> predicts -> Momentum spread lower bound | the position-momentum relation holds for every quantum state of the particle for which the finite standard deviations exist; sigma_x is nonzero
quantum-causation-v0 | Momentum spread lower bound -> prevents -> Sharp classical orbit | canonical position and momentum are considered for a nonrelativistic particle with nonzero hbar
quantum-causation-v0 | Unitary evolution -> predicts -> Probability normalization | the initial state has norm one and a self-adjoint Hamiltonian generates closed-system evolution
quantum-causation-v0 | Entanglement of particles -> enables -> Bell correlation | identically prepared singlets (|01>-|10>)/sqrt(2) undergo ideal local projective measurements using Pauli X and Z with outcomes +/-1, A0=Z, A1=X, B0=(Z+X)/sqrt(2), B1=(Z-X)/sqrt(2), and S=<A0*B0>+<A0*B1>+<A1*B0>-<A1*B1>; experimental loopholes are excluded
quantum-causation-v0 | No signalling from correlation -> predicts -> Controllable remote signal | remote operations are trace-preserving, outcomes are not postselected using communicated information, and only local outcome statistics are read
quantum-causation-v0 | Potential barrier -> prerequisite -> Quantum tunneling | the one-dimensional scattering problem has a finite-width region with V greater than incident energy E and a transmitted propagating region
quantum-causation-v0 | Electron transition -> causes -> Atomic spectral lines | bound atomic levels participate in allowed radiative transitions and line broadening is narrower than the resolved gap structure
quantum-causation-v0 | Energy quantization -> prerequisite -> Atomic spectral lines | the spectrum contains bound-bound electronic transitions of isolated atoms rather than a continuum
quantum-causation-v0 | Electron transition -> causes -> Photon | the downward transition is radiative and nonradiative or multiphoton channels are excluded from this event
quantum-causation-v0 | Pauli exclusion principle -> predicts -> Electron shell filling | identical electrons have an antisymmetric many-electron state represented in an orthonormal spin-orbital basis
quantum-causation-v0 | Particle spin -> enables -> Electron shell filling | the independent-electron orbital description uses an antisymmetric two-electron state with two available spin projections
quantum-causation-v0 | Uncertainty principle -> predicts -> Zero-point energy | the Hamiltonian is p squared over 2m plus m omega squared x squared over 2, with m and omega positive and the potential minimum taken as zero
quantum-causation-v0 | Decoherence by environment -> enables -> Classical everyday behaviour | environment-selected pointer states decohere much faster than the observation timescale and environmental records are inaccessible
quantum-causation-v0 | Decoherence by environment -> inhibits -> Interference pattern | the environment becomes correlated with paths whose amplitudes would otherwise overlap coherently at detection
quantum-causation-v0 | Stimulated emission -> enables -> Laser light | an operating pumped gain medium has net gain above losses and the laser feedback or amplification geometry supports the mode
quantum-causation-v0 | Photon -> enables -> Stimulated emission | an excited emitter couples to an electromagnetic mode at its transition frequency within the linewidth
quantum-causation-v0 | Energy level -> enables -> Electron transition | the initial level is occupied, the final level is available, and the perturbation satisfies the applicable selection rule
quantum-causation-v0 | Atomic orbital -> enables -> Electron shell filling | a specified atomic independent-particle approximation provides a bound orbital basis and occupancies obey antisymmetry
quantum-causation-v0 | Atomic spectral lines -> predicts -> Electron transition | the identified line arises from a specified isolated atomic transition; Doppler and external-field shifts are corrected
quantum-causation-v0 | Photon -> enables -> Electron transition | the initial atomic level is occupied and an allowed transition matches photon energy within its linewidth
quantum-causation-v0 | Particle spin -> enables -> Nuclear spin precession | a nucleus with nonzero magnetic moment experiences a static field and transverse magnetization is prepared
```

## Sweep final source check

All 11 modules produce exactly their current generated foundations records in an in-memory rebuild, including the final Go atomic-access definition and independent quantum corrections. An initial ad-hoc import omitted tools from sys.path and raised ModuleNotFoundError; correcting that invocation passed all eleven comparisons without a tool change. Four required checks already passed for each final module. The temporary quantum fixup is data-only and will be folded into this goal's initial quantum commit on the current branch; no pre-existing commit or other branch is rebased. Historical checkpoint hashes in this log are superseded by the final consolidation table in the advanced branch.

## Final sweep commit identities

Only this goal's unpublished commits on its working sweep branch were consolidated; the tree is byte-identical before/after and pre-existing history/other branches were untouched. Each of 11 worlds now has exactly one Review fixes commit. Earlier hashes are historical checkpoints.

```
b6902a1 Review fixes: quantum
a2a673b Review fixes: algebra
df03200 Review fixes: calculus
d567897 Review fixes: geometry
4485990 Review fixes: information
c3dea12 Review fixes: python
c9e39e3 Review fixes: go
48db68f Review fixes: cpp
090cb3a Review fixes: chemistry
76a655f Review fixes: biology
fbe3a21 Review fixes: color
```

## Rust branch setup

Switched to the prescribed authoring/rust-coding branch. The 20 verified sweep source entries are appended here too because generated curricula stay in place across branch switches and the required global validator resolves every generated record's source IDs. This is source-metadata registration only; no sibling world module or branch history is imported or merged.

## Reviewable kitchen myth append — scope clarification pending

The prompt requires kitchen myths but its Step 0 file allowance names existing modules in the fix list. The kitchen data module cannot emit myths: the unchanged builder reads only cross.MYTHS. The following exact two data entries need an append to tools/physical_causation/cross.py on authoring/kitchen; no existing cross records or builder logic would change. This proposed exception has not been applied.

```python
("searing-seals-juices", "Myth: searing seals in meat juices",
 "Searing develops a browned surface but does not create a waterproof seal; moisture can still leave during cooking.",
 "maillard-browning"),
("salt-boils-much-hotter", "Myth: seasoning salt makes cooking water much hotter",
 "Dissolved salt raises the boiling point, but the increase at ordinary seasoning concentrations is small and does not explain a substantial acceleration of cooking.",
 "salted-cooking-water"),
```

Both targets are kitchen-owned concepts and inherit the verified food-science citation. The builder does not consume a kitchen.MYTHS array, so adding it there would leave the required myths absent from generated records. Source: review requirements, unchanged physical builder lines159-168 and the read-only kitchen audit.

## Step 0: rust-coding-v0

Commit: `6ce48de` (`Review fixes: rust`).
Counts: 49 concepts, 44 authored relations, 6 myths, 6 boundaries, 4 examples, 4 controls.
Relations by kind: {"causes": 13, "enables": 15, "inhibits": 1, "predicts": 2, "prerequisite": 1, "prevents": 12}.
Probes/tasks: not applicable to Step 0.

Self-review: 48 original relations → 44 retained, four drops, zero new relation IDs. Direction/polarity pass changed 14 unique retained edges (11 endpoint and 10 kind changes overlap). Counterexample pass tightened all 44 statements, conditions and exceptions; version pass states Rust1.63+ with compiler/library/Cargo regimes. All six myths corrected/qualified, three boundary records added, all 40 old concept definitions tightened and nine specific target/order concepts added. Count pass: 100% causal kinds, no padding; unique IDs/pairs/conditions and exact labels/verbs passed.

Dropped:
- rule-blocks-shared: merged into rule-blocks-mut after both targeted the same conflicting-borrow rejection.
- rule-blocks-race: aliasing shorthand alone omits interior mutability/Send/Sync and is no runtime synchronization mechanism.
- ownership-prereq-rule: local ownership is not a separate necessary prerequisite for reference validity/exclusivity.
- sync-refuses-unsafe-share: marker is an eligibility contract, not itself a runtime anti-race mechanism.

Every requested fix handled: Copy means implementing Copy (including &T); remaining fields after partial move remain usable; locals drop individually in reverse declaration order; NLL includes destructor liveness; std::thread::scope1.63+ permits bounded non-static borrowing; reference obligations apply inside unsafe.

Parent and independent reviewer read all49 concepts/all44 relations and every scaffold record. They confirmed two final counterexamples: ? can invoke a panicking/diverging From conversion or exit-time destructor. Result/Option propagation conditions now require terminating normal conversion/cleanup. No other unresolved actionable factual issue identified; Claude acceptance pending.

Ten stdin compile probes passed using installed rustc1.98.1: shared &T Copy, remaining partial fields, legal shared reborrow from &mut, NLL ending and scoped non-static threads accepted; ordinary spawn borrowed local rejected E0373; Drop-held shared borrow E0506; Drop-held mutable borrow E0503; whole-value use after partial move E0382; partial move from Drop type E0509. Initial rustc -o /dev/null invocation tried to create /dev/rmeta temporary storage and failed; rerunning with -o - and discarded stdout passed without saved testfiles. These probes check selected acceptance/rejection cases, not runtime drop order; that order was verified in the Rust Reference.

Sources added: rust-reference (https://doc.rust-lang.org/reference/); rust-std-199 (https://doc.rust-lang.org/std/, docs identify1.99.0/b940084d7 2026-09-28); rust-by-example (https://doc.rust-lang.org/rust-by-example/), all citation_only, standards-primary, retrieved2026-10-02. Existing rust-book/cargo-reference retained. Docs and installed compiler versions are intentionally distinguished.

Builder AST comparison confirms only authoring data changed; all builder logic is identical to original94f950a.

Four checks:

```
$ python3 tools/build_rust_coding_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/rust-coding/foundations.jsonl with 191 records
splits: {'cross_domain_holdout': 7, 'sealed_test': 18, 'train': 145, 'validation': 21}
kinds: {'boundary': 6, 'concept': 50, 'counterexample': 6, 'relation': 121, 'synthetic_control': 4, 'worked_example': 4}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id rust-coding-v0
{
  "schema_version": 1,
  "world_id": "rust-coding-v0",
  "adapter_independent": true,
  "record_count": 191,
  "node_count": 70,
  "edge_count": 121,
  "negative_pair_count": 4,
  "domains": [
    "language-ecosystems"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "afdc37f5fc150493744ec3e5b331e3b5004fb9bdb1b5eae0633e5ded654bf1ef",
    "lexicon.json": "793dd5e015bce803ab59411de23ce0a8b8a4d0e35f87aa2506645ca6b6b1e0c6",
    "nodes.jsonl": "5b5fefb081aa2cba4025215dc573087c9d2b0522fd2fb26937b0efdebb8ef560",
    "records.jsonl": "0354bf301e315a4a981a574e057233e3b5e8dc284d15840e5b206e025d43a5c7",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "6efdc29e506dd5f008e2c878a1b80f69c4aa736f25c5a3346f5bdc64c2e9a5c9",
    "split-manifest.json": "61dc0c6f5f13f4c3768d3843d5a8261524162698730105607ebc908523eb96c7",
    "training-graph.json": "d4b970c07cbf389a3b739a87ada7e0e6c8bb56aff42e4a4055a98761aa8b198d"
  }
}
exit: 0
```

Reviewer relation list:

```text
rust-coding-v0 | Move of a value -> causes -> Moved-from binding | Rust 1.63+; an initialized non-Copy local is moved in a value-consuming context rather than reborrowed
rust-coding-v0 | Move of a value -> causes -> Ownership of a value | Rust 1.63+; a successful let binding receives a non-Copy owned value by move and retains it
rust-coding-v0 | Move of a value -> prevents -> Double free of memory | Rust 1.63+ safe code; a Box or other sound exclusive resource owner moves between locals without unsafe duplication of its allocation handle
rust-coding-v0 | Ownership of a value -> prevents -> Double free of memory | Rust 1.63+ safe code; one Box owns an allocation and all underlying unsafe implementations uphold their safety contracts
rust-coding-v0 | Copy trait duplication -> prevents -> Moved-from binding | Rust 1.63+; the assigned type implements Copy, including &T regardless of whether T implements Copy
rust-coding-v0 | Explicit clone -> prevents -> Moved-from binding | Rust 1.63+; Clone::clone borrows the original through &self, returns successfully and only the returned value is moved
rust-coding-v0 | Ownership of a value -> causes -> Drop at scope end | Rust 1.63+; an ordinary initialized owning local remains unmoved when its drop scope exits normally and has not been forgotten or wrapped in ManuallyDrop
rust-coding-v0 | Drop at scope end -> causes -> Drop trait implementation | Rust 1.63+; the initialized local implements Drop and ordinary scope-exit destruction reaches it
rust-coding-v0 | Drop at scope end -> causes -> Heap storage deallocation | Rust 1.63+; a Box of non-zero-sized contents still owns its allocation and its contents and allocator are destroyed without aborting
rust-coding-v0 | Local declaration order -> predicts -> Drop at scope end | Rust 1.63+; initialized unmoved locals share a drop scope and no destructor aborts the remaining cleanup
rust-coding-v0 | Rc shared ownership -> inhibits -> Managed payload destruction | Rust 1.63+; one Rc handle is dropped while at least one other strong Rc handle to the same payload remains
rust-coding-v0 | Drop at scope end -> causes -> Mutex lock release | Rust 1.63+; a successfully acquired std::sync::MutexGuard reaches its ordinary drop without being forgotten
rust-coding-v0 | Shared borrow -> prevents -> Mutable borrow | Rust 1.63+ safe code; ordinary &T and &mut T borrows overlap at the same location and the shared referent is not accessed through an UnsafeCell abstraction
rust-coding-v0 | Mutable borrow -> prevents -> Shared borrow | Rust 1.63+ safe code; a direct shared borrow of the same owned location overlaps a mutable reference that is subsequently used
rust-coding-v0 | Aliasing XOR mutation rule -> predicts -> Compile-time rejection | Rust 1.63+ safe code; direct borrows of the same place require overlapping &mut T and &T access and are not a permitted reborrow or interior-mutability operation
rust-coding-v0 | Borrow checker -> prevents -> Dangling reference | Rust 1.63+; the lifetime error is visible in safe reference creation and use, and unsafe dependencies uphold their contracts
rust-coding-v0 | Borrow checker -> causes -> Compile-time rejection | Rust 1.63+; code reaches borrow checking and contains a conflicting ordinary borrow or a reference use after its referent's lifetime
rust-coding-v0 | Moved-from binding -> causes -> Compile-time rejection | Rust 1.63+; a non-Copy value has moved out and later code attempts whole-value use before replacing it
rust-coding-v0 | Lifetime parameter -> enables -> Borrow checker | Rust 1.63+; a function signature uses a generic lifetime tying its input and output references or expressing an outlives bound
rust-coding-v0 | Lifetime elision -> enables -> Borrow checker | Rust 1.63+; omitted reference lifetimes follow the input/output elision rules, such as one input reference determining one output reference
rust-coding-v0 | Last use of a borrow -> enables -> Mutable borrow ending | Rust 1.63+ non-lexical lifetimes; a local nonescaping &mut reference has no later required use, drop use or stronger lifetime constraint
rust-coding-v0 | Last use of a borrow -> enables -> Shared borrow ending | Rust 1.63+ non-lexical lifetimes; a local nonescaping &T reference has no later ordinary use, destructor use or escaping lifetime requirement
rust-coding-v0 | Reborrow through a reference -> enables -> Mutable borrow | Rust 1.63+; a fresh &mut *r is derived from a valid &mut T and the outer reference is not used incompatibly until the reborrow ends
rust-coding-v0 | Send marker trait -> enables -> Thread spawn boundary | Rust 1.63+ std::thread::spawn; all captured fields make the closure Send, the closure and result satisfy 'static, and the result is also Send
rust-coding-v0 | Thread spawn boundary -> prevents -> Dangling reference | Rust 1.63+; std::thread::spawn requires the closure and returned value to satisfy Send + 'static, excluding borrows of caller locals that can expire first
rust-coding-v0 | Sync marker trait -> enables -> Shared borrow | Rust 1.63+; T is Sync, so &T is Send, and the reference lifetime covers every receiving-thread use
rust-coding-v0 | Sync marker trait -> prerequisite -> Arc shared ownership | Rust 1.63+; the default-allocator Arc<T> is transferred across threads and T must satisfy both Send and Sync
rust-coding-v0 | Arc shared ownership -> enables -> Thread spawn boundary | Rust 1.63+; cloned Arc<T> handles enter std::thread::spawn closures and T is Send + Sync + 'static
rust-coding-v0 | Rc shared ownership -> enables -> Reference counting cycle | Rust 1.63+; a constructed graph uses strong Rc links for every edge of an ownership cycle and no edge is subsequently cleared
rust-coding-v0 | Reference counting cycle -> causes -> Leaked memory | Rust 1.63+; all external owners of a strong Rc or Arc cycle are dropped, the internal links remain intact and no code can break the cycle
rust-coding-v0 | Mutex guard borrowing -> prevents -> Data race | Rust 1.63+; every conflicting access to the same protected memory takes the same std::sync::Mutex and all unsafe code respects its contract
rust-coding-v0 | Mutex guard borrowing -> enables -> Mutable borrow | Rust 1.63+; a successfully acquired std::sync::MutexGuard is mutably borrowed through DerefMut and stays alive throughout the resulting access
rust-coding-v0 | Question mark operator -> causes -> Early error return | Rust 1.63+; ? is applied to Err(E) in a Result-returning function whose error type supports the required From conversion, that conversion terminates normally, and exit-time cleanup completes without panic or divergence
rust-coding-v0 | Question mark operator -> causes -> Early None return | Rust 1.63+; ? is applied to None within a function or closure returning a compatible Option, and exit-time cleanup completes without panic or divergence
rust-coding-v0 | Result enum -> prevents -> Panic unwinding | Rust 1.63+; the selected failure path returns Err directly without panicking, and the caller handles or propagates it without panic-producing unwrap or expect
rust-coding-v0 | Panic unwinding -> causes -> Drop at scope end | Rust 1.63+; panic=unwind propagates through Rust frames and cleanup proceeds without an aborting second panic or abort boundary
rust-coding-v0 | Option enum -> prevents -> Null pointer dereference | Rust 1.63+ safe code; Option<&T> is matched as Some(valid_reference) or None and no raw pointer or unsound unsafe code is involved
rust-coding-v0 | Monomorphization of generics -> enables -> Static dispatch | Rust 1.63+ rustc; a generic T: Trait call is specialized for a concrete non-trait-object T and resolved to its trait implementation
rust-coding-v0 | Trait object -> enables -> Vtable method dispatch | Rust 1.63+; a dyn-compatible method is called through &dyn Trait or Box<dyn Trait> using trait-object dispatch semantics
rust-coding-v0 | Heap allocation with Box -> enables -> Trait object | Rust 1.63+; concrete T implements a dyn-compatible trait and satisfies the trait object's lifetime bound for coercion to Box<dyn Trait>
rust-coding-v0 | Partial move of a field -> causes -> Moved-from binding | Rust 1.63+; a non-Copy field moves out of a struct that does not implement Drop and the missing field has not been reinitialized
rust-coding-v0 | Drop trait implementation -> prevents -> Partial move of a field | Rust 1.63+; safe code tries to move a non-Copy field directly out of a struct implementing Drop rather than replacing that field
rust-coding-v0 | Cargo build invocation -> enables -> Borrow checker | Rust 1.63+ Cargo; an enabled package target needs compilation rather than cache reuse and preceding compiler stages succeed
rust-coding-v0 | Cargo check invocation -> enables -> Borrow checker | Rust 1.63+ Cargo; selected code requires checking, reaches borrow analysis and is not satisfied by an up-to-date cached result
```

## Kitchen branch setup

Switched to prescribed authoring/kitchen at78bd3b2. Carried only the permitted running log and appended missing, already-verified source citations so global generated-curriculum validation can resolve the retained sweep and Rust records. No other world code or branch history imported. The two cross.MYTHS additions remain pending the narrow file-scope clarification; kitchen module corrections can proceed independently.

## Kitchen scope clarification authorized and source ownership corrected

Jesse explicitly allowed only the two proposed kitchen myth entries in cross.py and required the kitchen commit to contain only kitchen.py, cross.py and food-science source registrations it actually cites. The 23 copied sweep/Rust registrations have been removed from the kitchen change; the existing registrations were already committed on their owning branches. Kitchen now adds only mcgee-food-cooking-2004 and nist-nacl-water-eutectic-2017. The running log will be carried to advanced-worlds separately, not included in the kitchen commit. A clean detached validation checkout under ignored artifacts/staging will run the native four checks with kitchen sources and its own generated physical curriculum, preserving other branches' generated outputs in the primary checkout.

## Step 0: kitchen in physical-causation-v0

Commit: `10aebca` (`Review fixes: kitchen`).

Kitchen-only counts:47 concepts,59 authored relations; two requested myths appended to cross.MYTHS. Existing shared boundaries/examples/controls unchanged. Probes/tasks not required for Step0.

Self-review (overlapping passes):54 originals ->52 retained plus7 new. Three endpoint changes,8 kind changes; all52 retained conditions rewritten;12 concepts added. Drops: carryover-settles (a cooking process does not transform into equilibrium and environmental cooling defeats the claimed guarantee); gradient-crack (merged its rapid-gradient/fracture hypothesis into uneven-grow-crack). All59 relations use causal kinds, without padding; exact labels/verbs, global IDs/pairs and condition uniqueness passed.

Physical regimes name pressure, sensible versus latent heat, thermal losses, food composition and ordinary NaCl/water equilibrium near about -21 degrees Celsius. Maillard temperature describes a rate regime; the sucrose caramelization condition is not a universal sugar threshold. Exactly two myths were appended after explicit Jesse approval; all prior cross content preserved. Gluten hydration/kneading/gas-retention and emulsification/coalescence mechanisms added.

Parent and independent reviewer read all47 concepts/all59 relations/both myths. Three final counterexamples repaired before checks: sensible refrigerator cooling versus a phase-change plateau; direct frost growth on exposed existing ice with latent-heat removal; reactant mobility in the drier Maillard comparator. No other confirmed actionable issue remains; Claude review pending.

Sources added and actually cited:mcgee-food-cooking-2004 (Scribner revised2004 edition, publisher metadata verified without claiming access to unavailable detailed chapters); nist-nacl-water-eutectic-2017 (NIST ThermoML, Thermochimica Acta647:94-100,2017). No nonfood source addition remains in the kitchen diff, per Jesse's explicit instruction.

Native four-check receipts in the clean detached validation checkout follow. All four commands exited0. The parent post-check script then looked in an incorrectly assumed directory physical-causation-v0 and raised FileNotFoundError; corrected it to the builder's actual OUTPUT, physical-causation/foundations.jsonl. Both generated myths and their provenance then passed, and an in-memory build exactly matches the generated file. No builder/tool/source change was needed for that invocation correction.

```
$ python3 tools/build_physical_causation_curriculum.py
wrote curricula/physical-causation/foundations.jsonl with 987 records
splits: {'cross_domain_holdout': 84, 'sealed_test': 58, 'train': 777, 'validation': 68}
kinds: {'boundary': 14, 'concept': 268, 'counterexample': 25, 'relation': 658, 'synthetic_control': 6, 'worked_example': 16}
exit: 0
$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0
$ python3 tools/validate_sources.py
valid: True
exit: 0
$ .venv/bin/python trainer/compile_curriculum.py --world-id physical-causation-v0
node_count: 329
edge_count: 658
record_count: 987
exit: 0
```

The compiler's complete saved bundle manifest corresponding to the printed JSON result:

```json
{
  "adapter_independent": true,
  "domains": [
    "physics"
  ],
  "edge_count": 658,
  "files": {
    "edges.jsonl": "8e828fe07f3c8728d23327402548afbeff4027259a739635ce51451eee8590a3",
    "lexicon.json": "768129fa134f3175e145b60d3ab09df57fa9a9d02d6273c1c313a7b539fe7555",
    "nodes.jsonl": "e5d24212a7d1844fb3ed12136fa769404696e4701dccc47f0ac1f6047e426ca0",
    "records.jsonl": "789fd4c0f761294b71a34d847fb70051f4373c28a7914c028b7af81526878c4c",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "f626f46f594abbd85335d5aba48e77b766081b385da6b74101883a4dff697b11",
    "split-manifest.json": "d4b6f37606f9ad17c827a4394d18e704e3b49a9f688782f9a53901a24f6ef73a",
    "training-graph.json": "d17d24e6aa7bfd04fd9ff25232ff5031d8c060ed77b0a2b119a4afc6e3543c9c"
  },
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "negative_pair_count": 6,
  "node_count": 329,
  "record_count": 987,
  "schema_version": 1,
  "world_id": "physical-causation-v0"
}
```

Validation directory: `/home/jesse/Desktop/Projects/new-complete-atom-lightcone/artifacts/staging/kitchen-review-validation`, based on78bd3b2 with only the exact three kitchen candidate files overlaid. The existing primary virtualenv was linked; original generated outputs were preserved. Checked-file SHA256 values (identical to primary candidate):

```json
{
  "tools/physical_causation/kitchen.py": "2b68eb499437745e4a8f2ed89e50d0efec24ae75149fbe8c85ae0aab9c567de9",
  "tools/physical_causation/cross.py": "1973a09aea136a5f3300be41217e86d40f770943c7d3619c9585e4780ad0594b",
  "sources/source-registry.json": "24226ca6370b6266dcf6b1bdae3ab7a66be4c73cfc7b030cfab6525882284110"
}
```

Both required myth counterexamples occur once and cite the food-science source. Existing source entries and cross data are unchanged. Relations by kind: {"causes": 24, "enables": 23, "inhibits": 10, "predicts": 2}.

Reviewer relation list:

```text
physical-causation-v0 | Stovetop burner -> causes -> Heat transfer | the operating gas or resistive-electric burner transfers net thermal energy to a cooler pan placed within its heating region
physical-causation-v0 | Combustion of fuel -> enables -> Stovetop burner | the gas supply is ignited with enough oxidant to sustain combustion and the released heat reaches the hob
physical-causation-v0 | Stovetop burner -> causes -> Pan hot spots | an uneven or undersized burner heats the pan nonuniformly over an interval in which conduction has not equalized its base temperature
physical-causation-v0 | Conductive pan base -> inhibits -> Pan hot spots | a sufficiently thick aluminium or copper layer, including a clad base, is compared with a poorer heat-spreading base under the same burner pattern
physical-causation-v0 | Joule heating -> enables -> Kettle heating element | current flows through a resistive element with a thermal path to the kettle water
physical-causation-v0 | Kettle heating element -> causes -> Temperature rise | liquid water below its local boiling temperature receives more heater energy than it loses, without a simultaneous phase change consuming the net input
physical-causation-v0 | Limescale layer on an element -> inhibits -> Heat transfer | an adherent low-conductivity scale layer separates the heater metal from the water and the comparison fixes surface area and the temperature difference across the heat-transfer path
physical-causation-v0 | Stirring a fluid -> enables -> Heat transfer | stirring circulates the liquid between the heated base and cooler regions without substantial isolated stagnant pockets
physical-causation-v0 | Bubble nucleation sites -> enables -> Boiling of a liquid | the heated liquid supports vapour-bubble growth at the local pressure and stable nuclei are available in cavities or suspended particles
physical-causation-v0 | Heat transfer -> causes -> Rolling boil | water has reached its saturation temperature at fixed local pressure and continuing heat input supports vigorous bubbling while liquid remains
physical-causation-v0 | Bubble nucleation sites -> inhibits -> Superheated water in a microwave | available heterogeneous nuclei support bubble growth as water passes saturation and vapour can escape the container
physical-causation-v0 | Microwave oven field -> enables -> Superheated water in a microwave | water absorbs microwave power in a container with insufficient active nucleation sites and reaches a temperature above saturation at the local pressure
physical-causation-v0 | Superheated water in a microwave -> enables -> Boiling of a liquid | the water is above its local saturation temperature and a disturbance introduces a nucleus large enough to grow rather than collapse
physical-causation-v0 | Pot lid trapping steam -> enables -> Temperature rise | matched pots receive the same burner power below boiling, the loose lid reduces evaporation and convection losses, and neither pot becomes pressurized
physical-causation-v0 | Pot lid trapping steam -> causes -> Condensation of vapour | water vapour reaches a lid surface cooler than the dew-point temperature set by the local water-vapour partial pressure
physical-causation-v0 | Condensation of vapour -> enables -> Steam scald on skin | hot cooking steam contacts cooler skin and the duration and condensing mass can deliver a thermally injurious energy dose
physical-causation-v0 | Microwave oven field -> causes -> Dielectric heating of food | the food has dipolar or ionic loss at the applied microwave frequency and absorbs nonzero electromagnetic power
physical-causation-v0 | Dielectric heating of food -> causes -> Temperature rise | local microwave absorption exceeds conductive and evaporative losses and energy consumption by melting or other phase changes
physical-causation-v0 | Microwave penetration depth -> predicts -> Dielectric heating of food | a homogeneous food slab is modelled with exponential power attenuation of a dominant incident plane wave, neglecting reflections and standing-wave interference
physical-causation-v0 | Thermal conduction -> enables -> Temperature rise | net conduction supplies sensible heat to the centre and local phase changes do not consume all of that incoming energy
physical-causation-v0 | Frozen core of food -> inhibits -> Temperature rise | ice is melting within the food's composition-dependent melting range while the core receives a fixed net heat input; the temperature need not remain constant
physical-causation-v0 | Heat transfer -> causes -> Thawing of frozen food | the surroundings remain warmer than the relevant food melting range and enough cumulative heat enters to reach and traverse part of that range
physical-causation-v0 | Cold water thawing bath -> enables -> Heat transfer | the same package area is exposed to a maintained bath or still air above the food's thawing range, and water-side heat-transfer resistance is lower
physical-causation-v0 | Refrigerator heat pumping -> causes -> Temperature drop | heat extraction exceeds gains in the modelled cabinet region, which has positive heat capacity and loses sensible energy rather than remaining on a phase-change temperature plateau
physical-causation-v0 | Refrigerator heat pumping -> causes -> Temperature rise | condenser surfaces are hotter than the entering room air and transfer net heat to that air while the compressor operates
physical-causation-v0 | Temperature drop -> causes -> Frost deposition in a freezer | supplied water vapour reaches an exposed already-ice-coated surface held below its local frost point, with supersaturation relative to ice and cooling sufficient to remove the latent heat of deposition
physical-causation-v0 | Frost deposition in a freezer -> causes -> Freezer frost buildup | deposition on the surface exceeds sublimation, melting and defrost removal over the storage interval
physical-causation-v0 | Sublimation of ice -> causes -> Freezer burn on food | the frozen surface sustains net vapour loss through incomplete or vapour-permeable packaging for sufficient storage time
physical-causation-v0 | Boiling of a liquid -> inhibits -> Maillard browning | the food remains wet in dilute aqueous liquid boiling near atmospheric pressure and is compared with the same formulation and pH at a hotter, less-wet surface for a similar time, with sufficient reactant mobility retained in the drier comparison
physical-causation-v0 | Hot oven air -> causes -> Roast surface drying | air circulation maintains a water-vapour partial pressure below equilibrium with the moist surface and net evaporation exceeds surface moisture replenishment
physical-causation-v0 | Roast surface drying -> enables -> Maillard browning | reducing sugars and amino groups are present, moisture loss allows the heated surface to become hotter, and sufficient molecular mobility remains for the reactions
physical-causation-v0 | Temperature rise -> enables -> Caramelisation of sugar | plain sucrose or concentrated sucrose syrup is heated to about 160 degrees Celsius or higher for a cooking interval that permits decomposition; this is not a universal threshold for all sugars
physical-causation-v0 | Temperature rise -> causes -> Oil smoking in a pan | the particular oil in its current refined or used condition is held hot enough to emit visible smoke without assuming one threshold for every oil
physical-causation-v0 | Oil layer in a frying pan -> enables -> Heat transfer | a thin oil film bridges gaps between a hotter pan and cooler food without a persistent insulating vapour blanket
physical-causation-v0 | Oil layer in a frying pan -> enables -> Drying crust in frying | the oil is above the local boiling temperature of water and sustained net moisture loss develops a hotter exterior while the wetter interior may continue emitting steam
physical-causation-v0 | Boiling of a liquid -> enables -> Drying crust in frying | vaporization removes exterior water faster than it is replenished and vapour leaves the food rather than condensing back into that layer
physical-causation-v0 | Rolling boil -> causes -> Starch foam on boiling water | starchy food has released foam-stabilizing material and continuing steam generation produces bubbles that persist at the liquid surface
physical-causation-v0 | Starch foam on boiling water -> causes -> Pot boiling over | foam generation exceeds collapse and drainage long enough for the foam level to pass the pot rim
physical-causation-v0 | Reduced burner heat input -> inhibits -> Pot boiling over | the reduced burner power lowers the sustained vaporization rate before continued foam generation exhausts the remaining headspace
physical-causation-v0 | Double boiler -> inhibits -> Temperature rise | water remains in the lower vessel at fixed pressure and initially cooler upper contents receive heat only through that water or saturated steam, without direct hotter surfaces or internal exothermic reactions
physical-causation-v0 | Boiling of a liquid -> enables -> Double boiler | liquid water persists in the lower pot at constant pressure while the upper vessel is heated through the water or its saturated steam
physical-causation-v0 | Heat transfer -> causes -> Carryover cooking | the outer regions remain hotter than the centre and inward energy transport continues raising the centre temperature despite heat loss to the surroundings
physical-causation-v0 | Condensation of vapour -> causes -> Canning jar sealing | a hot jar cools with a lid and gasket that seat as vapour condenses, leaving internal pressure below ambient without appreciable subsequent leakage
physical-causation-v0 | Thermal expansion -> causes -> Thermal shock cracking | rapid heating or cooling creates a steep temperature gradient through a brittle vessel and the resulting tensile stress exceeds the local strength at a flaw
physical-causation-v0 | Boiling point temperature -> enables -> Maillard browning | increased cooker pressure raises the aqueous cooking temperature and suitable reducing sugars, amino groups, pH and exposure time permit Maillard chemistry without requiring a dry crust
physical-causation-v0 | Boiling point temperature -> predicts -> Temperature rise | nearly pure water boils at fixed external pressure with liquid remaining, negligible superheating and no material change in solute concentration
physical-causation-v0 | Freezing point depression -> enables -> Ice and salt freezing mixture | sodium chloride dissolves into water in contact with ice, and sufficient ice melts to absorb heat as the mixture approaches its composition-dependent phase equilibrium
physical-causation-v0 | Ice and salt freezing mixture -> causes -> Freezing of a liquid | the brine stays colder than the cream mixture's current freezing range and sustained heat transfer removes enough latent heat to freeze at least part of its water
physical-causation-v0 | Pot lid trapping steam -> inhibits -> Evaporation from a liquid surface | below boiling, covered and uncovered liquids are compared at the same surface temperature and the loose lid reduces the water-vapour gradient without pressurizing the vessel
physical-causation-v0 | Thermal convection -> enables -> Hot oven air | air circulation replaces cooled air near the food with hotter oven air and a positive air-to-food temperature difference remains
physical-causation-v0 | Evaporation from a liquid surface -> causes -> Roast surface drying | the surrounding air accepts vapour and net evaporation exceeds moisture migration from the food interior to its surface
physical-causation-v0 | Rolling boil -> causes -> Pot water loss | the pot is uncovered, liquid remains and no water addition or condensate return compensates for the escaping vapour
physical-causation-v0 | Salted cooking water -> causes -> Boiling point temperature | dissolved sodium chloride is added to water at fixed external pressure without another volatile solute
physical-causation-v0 | Wheat flour hydration -> enables -> Gluten protein network | gluten-forming wheat proteins and sufficient water are present before protein-setting heat treatment
physical-causation-v0 | Dough kneading -> enables -> Gluten protein network | hydrated wheat dough is mixed within a development range before excessive mechanical treatment damages its network
physical-causation-v0 | Gluten protein network -> enables -> Dough gas retention | a sufficiently continuous and extensible wheat-dough network surrounds gas cells without rupturing under the applied expansion
physical-causation-v0 | Emulsifying shear -> enables -> Food emulsion | immiscible food liquids are mixed with enough deformation to break droplets and are observed before complete phase separation
physical-causation-v0 | Food emulsifier -> inhibits -> Emulsion droplet coalescence | a compatible emulsifier covers the newly created interface sufficiently under the formulation's temperature, pH and ionic conditions
physical-causation-v0 | Emulsion droplet coalescence -> inhibits -> Food emulsion | interfacial films fail and merging proceeds far enough to disrupt the desired dispersed-droplet structure
```

## Branch-specific generated output preserved

The freshly rebuilt Rust curriculum was moved, with every file hash unchanged, from curricula/rust-coding to artifacts/staging/rust-coding-v0/authoring-curriculum beside its compiled input bundle. This preserves the data while preventing the sweep/advanced global validator from reading another branch's generated records and requiring unrelated source registrations. No generated data was deleted. Kitchen validation output remains in its isolated validation checkout.

## Final algebra concept precision check: algebra-causation-v0

Commit: pending creation, title `Review fixes: algebra`.
Counts: 33 concepts, 26 relations, 5 myths, 5 boundaries, 5 examples, 6 controls.
Relations by kind: {"enables": 7, "predicts": 16, "prerequisite": 2, "prevents": 1}.
Probes/tasks: not applicable to Step 0.

Final minor concept precision repair from the independent math review: Group generator now explicitly uses integer powers, including negative powers for infinite cyclic groups. All 26 relation statements and conditions are unchanged from their already-reviewed state; full four checks rerun for the changed concept record. No new source or scope change. The correction is folded into this goal's unpublished algebra commit on its owning sweep branch before advanced authoring. Earlier checkpoint hashes remain historical.

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
    "nodes.jsonl": "0924e39134f6a59c1d551b72a9f7e9bf54a5a020c91031ad4ca807eef489d371",
    "records.jsonl": "f24c2af52e9b18971eb4bd03fd0a58bd8e84735a289aad4b3884185a20ef1f48",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "1a2648c21c25c3889d15861f6e7c17e885fc99c4795bedb2d4bea9c160c500b5",
    "split-manifest.json": "dadb9fbc38b2312bbc6b2f396159eec5c39999b89bda977f99c0dc4481ee4756",
    "training-graph.json": "2cfa8093b67c9f51d447b9e29d9a9f5822f0ebec7bb9dcc49cb8a459ed661f6b"
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

## Step 0 completed — final authoritative commit map

All thirteen final worlds passed four checks. Kitchen used the clean validation checkout and its commit contains exactly kitchen.py, the two authorized cross.MYTHS additions and its two cited food-science sources; no log or unrelated registration is in that commit. Final math precision repair explicitly includes negative integer generator powers. Earlier checkpoint hashes are superseded by this map.

```
b6902a1 Review fixes: quantum
1deaa08 Review fixes: algebra
94bef2c Review fixes: calculus
c9056b8 Review fixes: geometry
6feeb6e Review fixes: information
75bfa6d Review fixes: python
6315759 Review fixes: go
833b2eb Review fixes: cpp
e5fcad1 Review fixes: chemistry
69300e3 Review fixes: biology
b5a6aa0 Review fixes: color
6ce48de Review fixes: rust (authoring/rust-coding)
10aebca Review fixes: kitchen (authoring/kitchen)
```

Created authoring/advanced-worlds from repaired sweep b5a6aa0 with a clean tracked tree and only generated curricula untracked, using the exact prescribed checkout command. All subsequent authoring stays on this branch. No branch merge, push, AtomDB import or Claude acceptance performed. No pre-existing commits or other branch histories were rebased; only this goal's own unpublished sweep corrections were consolidated while on that branch.

## Advanced authoring queue

Expanded104-world prompt remains authoritative, printed order and bridge last. Completed: net-transport-tcp-v0 at b7dd83b. Current world: net-quic-http-v0; source research and original data authoring starting only after TCP completed all required checks/evaluations/log entry. Complete and self-review each world before writing its24 probes and5 checked tasks.

## TCP source registration

Existing rfc9293 reused. New entries below were verified from primary RFC headers and the original BBR paper; no existing source entry changed. RFC6928 is Experimental. BBR scope is the original2016 design, not later BBR revisions. ACM page denied automated access; its publisher-layout original PDF was verified at https://web.stanford.edu/class/cs244/papers/bbr.pdf and DOI metadata corroborated identity. Queue article is registered scholarly-reference without asserting peer-review status.

- rfc5681: TCP Congestion Control; RFC 5681; September 2009; Standards Track; https://www.rfc-editor.org/rfc/rfc5681
- rfc6298: Computing TCP's Retransmission Timer; RFC 6298; June 2011; Standards Track; https://www.rfc-editor.org/rfc/rfc6298
- rfc2018: TCP Selective Acknowledgment Options; RFC 2018; October 1996; Standards Track; https://www.rfc-editor.org/rfc/rfc2018
- rfc6675: A Conservative Loss Recovery Algorithm Based on Selective Acknowledgment (SACK) for TCP; RFC 6675; August 2012; Standards Track; https://www.rfc-editor.org/rfc/rfc6675
- rfc7323: TCP Extensions for High Performance; RFC 7323; September 2014; Standards Track; https://www.rfc-editor.org/rfc/rfc7323
- rfc6928: Increasing TCP's Initial Window; RFC 6928; April 2013; Experimental; https://www.rfc-editor.org/rfc/rfc6928
- rfc9438: CUBIC for Fast and Long-Distance Networks; RFC 9438; August 2023; Standards Track; https://www.rfc-editor.org/rfc/rfc9438
- bbr-2016-queue: BBR: Congestion-Based Congestion Control — Neal Cardwell, Yuchung Cheng, C. Stephen Gunn, Soheil Hassas Yeganeh and Van Jacobson; September–October 2016; Queue 14(5), 20–53; doi:10.1145/3012426.3022184; https://queue.acm.org/detail.cfm?id=3022184

## Advanced world: net-transport-tcp-v0

Commit: `b7dd83b` (`Author net-transport-tcp-v0 with checked evaluations`).
Counts: 102 concepts, 113 relations, 16 myths, 11 boundaries, 14 examples, 8 controls.
Relations by kind: {"causes": 35, "enables": 24, "inhibits": 16, "predicts": 27, "prerequisite": 2, "prevents": 9}.
Probes:24 authored and independently reviewed. Tasks:5 authored, semantic corrections pending final verification.

Author self-review: initial finished data had101 concepts/112 relations,16 myths,11 boundaries,14 examples,8 controls; all112 relations reviewed and all nine sources registered. Direction/type pass changed3 edges (Karn ambiguity target, SACK pipe credit, reneged-gap expansion) and dropped1 mispolarized BBR application-limited-filter edge while preserving the fact as a boundary. Counterexample pass tightened3 edges (specified Reno delayed-ACK behavior, bounded TIME_WAIT duplicates, CUBIC packet-loss scope). Version pass found no additional change; every edge states RFC/controller/model regime. Duplicate pass found0 pairs/conditions/circular edges;2 example IDs renamed to eliminate raw-ID collisions. Myth pass changed1 CUBIC claim and reviewed all16;2 plural-label grammar fixes made. All required count ranges passed without padding.

Parent read all concepts, relations, myths, boundaries, examples and controls. Independent source reviewer confirmed3 repairs: CUBIC time/parameter units; polynomial reference distinguished from clamped next-RTT ACK target; sender-side ACK baseline added before classifying an out-of-order response as duplicate. Parent applied all3 without changing IDs and added1 explicit full-MSS Nagle escape mechanism, producing102 concepts/113 relations. New concept Queued full segment payload and relation full-segment-escapes-nagle are supported by RFC9293 section3.7.4; the independent reviewer checked that addition. All final causal kinds remain100%.

All24 probes were independently reviewed: exact6/4/3/3/4/4 mix, reality-correct truth values, meaningful reversed claims and pressure copies with unchanged base truth/links. Myth probes may link emitted counterexample edges as well as authored mechanism edges; these are actual compiled relation IDs, not nonexistent raw IDs.

Evaluation code is still under revision before commit. Initial five reference/pitfall checks passed, but parent semantic review found the CUBIC checker and reference compared W_est with the next-RTT clamped target instead of W_cubic(t), demonstrating that agreement with a checker alone is insufficient. Corrections add a discriminating case. The initial RTO task mislabeled sample initialization as a timer start; it is being narrowed to the accurate estimator/backoff component. Reassembly coverage will use transmitted data for every receive and test partial range release. Window and Nagle cases are being broadened at meaningful boundaries. No claim of task or world completion yet.

Sources added: rfc5681,rfc6298,rfc2018,rfc6675,rfc7323,rfc6928,rfc9438,bbr-2016-queue, exactly as the registration section above; rfc9293 reused. BBR remains original2016 only. Open doubts: no unresolved factual world/probe error identified at stated precision; evaluation revisions pending, independent Claude review and real-model benefit evaluation not performed.

Four checks:

```
$ python3 tools/build_net_transport_tcp_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/net-transport-tcp-v0/foundations.jsonl with 470 records
splits: {'cross_domain_holdout': 24, 'sealed_test': 47, 'train': 343, 'validation': 56}
kinds: {'boundary': 11, 'concept': 103, 'counterexample': 16, 'relation': 318, 'synthetic_control': 8, 'worked_example': 14}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id net-transport-tcp-v0
{
  "schema_version": 1,
  "world_id": "net-transport-tcp-v0",
  "adapter_independent": true,
  "record_count": 470,
  "node_count": 152,
  "edge_count": 318,
  "negative_pair_count": 8,
  "domains": [
    "networking"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "408e135e88b3ab7e55a5a56a9186998ffd2ef708a1a21fff0d6d5610092a7d25",
    "lexicon.json": "efe730001c5529bdabe3bd2d8c5d442941804c462ee52853ec5ae2d4fa54a567",
    "nodes.jsonl": "74d660f8c21b5f1030fa905342aafe477cd9bb01ff75fd42e826bd7bd97e798a",
    "records.jsonl": "56f65c8c24de7858b18e2734e2ff6096a709eed5364482c56d1da511d4ec38da",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "6d95d53213a456ade85d7d49f6cfaa20b811542ad6b1a1c8a585c2aa3ae13cdf",
    "split-manifest.json": "ad4b0b9e39c8a3a940ae7c62ddf91ce724e24f3b2e00a81f1a3723f39aac89a5",
    "training-graph.json": "7e54d62c3f2b9247ed8a46242d47231466285b60ec77d1eab29bc54ab6965c2c"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
net-transport-tcp-v0 | TCP active open -> causes -> Initial SYN segment | RFC 9293 Section 3.10.1: a valid active OPEN is processed in CLOSED with resources available and no existing connection
net-transport-tcp-v0 | Initial SYN segment -> causes -> SYN ACK segment | RFC 9293 Section 3.10.7: a valid SYN without ACK reaches a matching LISTEN endpoint that accepts the request
net-transport-tcp-v0 | SYN ACK segment -> causes -> Final handshake acknowledgment | RFC 9293 ordinary three-way open: the endpoint in SYN-SENT receives an acceptable SYN-ACK that acknowledges its own SYN
net-transport-tcp-v0 | SYN ACK segment -> causes -> Established connection state | RFC 9293 Section 3.10.7.3: SYN-SENT processing accepts the peer SYN and an ACK advancing SND.UNA beyond ISS
net-transport-tcp-v0 | Final handshake acknowledgment -> causes -> Established connection state | RFC 9293 ordinary passive open: the endpoint remains in SYN-RECEIVED and receives an acceptable ACK covering its SYN
net-transport-tcp-v0 | Initial SYN segment -> predicts -> TCP sequence number | RFC 9293 sequence accounting: an opening SYN at ISS contains no data and addition is modulo 2^32
net-transport-tcp-v0 | TCP FIN segment -> predicts -> TCP sequence number | RFC 9293 sequence accounting: an accepted segment starts at S, has L payload octets, and carries FIN but not SYN; the next position is S+L+1 modulo 2^32
net-transport-tcp-v0 | TCP sequence number -> enables -> Out of order buffering | RFC 9293 receiver: valid in-window segments beyond RCV.NXT arrive and the implementation retains them pending earlier bytes
net-transport-tcp-v0 | Cumulative acknowledgment -> causes -> Acknowledged buffer release | RFC 9293 sender: SND.UNA < SEG.ACK <= SND.NXT under serial arithmetic and the acknowledged bytes remain in the retransmission queue
net-transport-tcp-v0 | Cumulative acknowledgment -> inhibits -> Outstanding flight size | RFC 5681 FlightSize accounting: the ACK advances the cumulative data boundary and no concurrent transmission is included in this state update
net-transport-tcp-v0 | Data segment loss -> causes -> Receive sequence gap | RFC 9293 stream reassembly: a segment carrying previously unseen bytes is lost, at least one later range is received, and no retransmission has filled the missing range
net-transport-tcp-v0 | Network packet reordering -> causes -> Out of order arrival | RFC 9293 connection: two distinct in-window data ranges are delivered intact in reversed order with the lower range still absent
net-transport-tcp-v0 | Out of order arrival -> causes -> Duplicate acknowledgment | RFC 5681 Section 3.2 receiver follows the immediate-ACK recommendation for a new segment beyond a gap; its pure ACK has no SYN or FIN, and the data sender already received the same cumulative ACK number and window and still has outstanding data
net-transport-tcp-v0 | Receive sequence gap -> causes -> Byte stream head of line blocking | RFC 9293 established byte stream: later data is held beyond RCV.NXT and the application's ordered receive operation requires bytes at or beyond the missing range
net-transport-tcp-v0 | Data retransmission -> enables -> Receive gap repair | RFC 9293 receiver still accepts the missing sequence range, and the retransmitted copy can reach it intact before the connection terminates
net-transport-tcp-v0 | Receive gap repair -> enables -> Ordered byte delivery | RFC 9293 receiver: the repaired range begins at RCV.NXT, any following buffered ranges are contiguous, and the application requests the resulting available bytes
net-transport-tcp-v0 | Out of order buffering -> enables -> Ordered byte delivery | RFC 9293 receiver keeps the later ranges intact until all earlier gaps are filled and then services an application receive
net-transport-tcp-v0 | Application receive consumption -> inhibits -> Receive buffer occupancy | RFC 9293 receive-buffer accounting: the application consumes queued in-order bytes and no simultaneous arrival or reassembly allocation is included in this update
net-transport-tcp-v0 | Receive buffer occupancy -> inhibits -> Advertised receive window | RFC 9293 receiver SWS avoidance: fixed RCV.BUFF is partly held as RCV.USER and the receiver computes how far it may advance the existing window's right edge without retracting prior credit
net-transport-tcp-v0 | Application receive consumption -> enables -> Receive window update | RFC 9293 Section 3.8.6.2.2 receiver: consumption reaches the selected receiver SWS-avoidance threshold and an ACK can advertise the enlarged window
net-transport-tcp-v0 | Advertised receive window -> predicts -> New data sending allowance | RFC 5681 sender outside loss recovery: rwnd <= cwnd, SND.NXT is the highest transmitted data boundary, and no SYN, FIN, window shrink, or zero-window probe is being accounted
net-transport-tcp-v0 | Congestion window -> predicts -> New data sending allowance | RFC 5681 sender outside recovery: cwnd <= rwnd, no retransmission is pending, and all quantities refer to data bytes in one consistent pre-send state
net-transport-tcp-v0 | Outstanding flight size -> inhibits -> New data sending allowance | RFC 5681 normal transmission: fixed positive min(cwnd,rwnd) exceeds FlightSize, and an additional unacknowledged data byte is counted without changing either window
net-transport-tcp-v0 | New data sending allowance -> enables -> New data transmission | RFC 9293/RFC 5681 established sender: unsent application data exists, both windows admit it, and segmentation, pacing, and Nagle conditions permit release
net-transport-tcp-v0 | Receiver flow control -> prevents -> Receive credit overrun | RFC 9293 conforming sender honors the latest acceptable receive-window right edge; zero-window probes and retransmitted bytes are excluded from this ordinary-new-data claim
net-transport-tcp-v0 | Zero receive window -> prevents -> New data transmission | RFC 9293 sender has accepted the zero advertisement and has no residual ordinary new-data credit; the periodic zero-window probe is a separate exception to ordinary transmission
net-transport-tcp-v0 | Zero receive window -> causes -> Zero window probe | RFC 9293 Section 3.8.6.1 sender has queued new or retransmittable data, the connection remains open, and its zero-window probing timer becomes due
net-transport-tcp-v0 | Zero window probe -> enables -> Receive window update | RFC 9293 receiver has reopened a previously zero window, the probe reaches it, and the replying ACK with its current nonzero window reaches the sender
net-transport-tcp-v0 | Receive window update -> enables -> New data transmission | RFC 9293 sender accepts a nonzero reopening advertisement that grants new sequence space; queued data, congestion credit, and other send rules also permit transmission
net-transport-tcp-v0 | Reno slow start -> causes -> Congestion window | RFC 5681 Section 3.1 sender selects slow start below ssthresh and implements the recommended increase min(N,SMSS) for an ACK covering N new bytes
net-transport-tcp-v0 | Advancing data acknowledgment -> causes -> Acknowledgment clock | RFC 5681 ACK-clocked sender has data outstanding and receives an authentic advancing ACK; receiver cheating and ACK replication are absent
net-transport-tcp-v0 | Acknowledgment clock -> enables -> New data transmission | RFC 5681 sender has queued data and an open receive window, and the ACK arrival frees enough congestion credit under the current congestion-control state
net-transport-tcp-v0 | Slow start threshold -> predicts -> Reno slow start | RFC 5681 Section 3.1 sender is outside fast recovery and compares a positive cwnd with its current ssthresh; the equality case is excluded
net-transport-tcp-v0 | Reno additive increase -> causes -> Congestion window | RFC 5681 Section 3.1 sender is congestion-window limited above ssthresh and uses the recommended acknowledged-byte counting method during an RTT with new-data ACKs
net-transport-tcp-v0 | Reno multiplicative decrease -> causes -> Slow start threshold | RFC 5681 loss response is entered on the third duplicate ACK and excludes Limited Transmit bytes from FlightSize; the resulting bound is below the prior ssthresh
net-transport-tcp-v0 | Duplicate acknowledgment -> causes -> Reno fast retransmit | RFC 5681 Section 3.2 sender receives three duplicate ACKs as defined in Section 2 without an intervening advance of SND.UNA and is entering this recovery event
net-transport-tcp-v0 | Reno fast retransmit -> causes -> Data retransmission | RFC 5681 Section 3.2 has just triggered fast retransmit for outstanding data and the connection has not been aborted
net-transport-tcp-v0 | Duplicate acknowledgment -> causes -> Reno fast recovery | RFC 5681 Reno sender implements fast retransmit and fast recovery together, has received the third qualifying duplicate ACK, and is not using a different recovery algorithm
net-transport-tcp-v0 | Reno fast recovery -> causes -> Congestion window | RFC 5681 Section 3.2 third-duplicate-ACK event: the lost segment is retransmitted and the three duplicate ACKs are used to account for departed segments
net-transport-tcp-v0 | Advancing data acknowledgment -> inhibits -> Reno fast recovery | RFC 5681 Section 3.2 step 6: a Reno sender receives the next ACK of previously unacknowledged data and deflates cwnd to ssthresh; NewReno and SACK recovery rules are excluded
net-transport-tcp-v0 | Network packet reordering -> causes -> Spurious retransmission | RFC 5681 sender receives three qualifying duplicate ACKs from later arrivals before the delayed but intact original arrives, and retransmits the apparent missing segment
net-transport-tcp-v0 | Initial congestion window -> enables -> New data transmission | RFC 5681 established sender begins its first data flight with sufficient receiver credit and queued data; handshake ACKs have not enlarged cwnd
net-transport-tcp-v0 | Experimental enlarged initial window -> predicts -> Initial congestion window | RFC 6928 Section 2 optional experiment is selected for a new connection, SMSS is in bytes, and no SYN/SYN-ACK loss or other stated fallback requires a smaller window
net-transport-tcp-v0 | Unambiguous RTT sample -> predicts -> Smoothed RTT estimate | RFC 6298 Section 2 sender uses recommended alpha=1/8 with a valid sample R and distinguishes first-sample initialization from later smoothing
net-transport-tcp-v0 | Unambiguous RTT sample -> predicts -> RTT variation estimate | RFC 6298 Section 2.3 subsequent-sample update uses recommended beta=1/4 and performs the deviation update before updating SRTT
net-transport-tcp-v0 | Smoothed RTT estimate -> predicts -> Retransmission timeout interval | RFC 6298 estimator has at least one valid RTT sample, clock granularity G and RTTVAR are known, and this is the base RTO recomputation
net-transport-tcp-v0 | RTT variation estimate -> predicts -> Retransmission timeout interval | RFC 6298 Section 2 computation holds SRTT and G fixed with 4*RTTVAR>G and neither the recommended one-second floor nor a configured upper bound binding
net-transport-tcp-v0 | Retransmission timeout interval -> predicts -> Retransmission timer expiry | RFC 6298 running timer retains its scheduled interval, outstanding data remains, no ACK restarts or stops it, and the timer service runs at its configured resolution
net-transport-tcp-v0 | Retransmission timer expiry -> causes -> Data retransmission | RFC 6298 Section 5.4 sender has outstanding data when its retransmission timer expires and the connection is still eligible for retransmission
net-transport-tcp-v0 | Retransmission timer expiry -> causes -> Exponential RTO backoff | RFC 6298 Section 5.5 retransmission-timer expiry is processed and the current RTO is below any permitted maximum
net-transport-tcp-v0 | Exponential RTO backoff -> inhibits -> Retransmission timer expiry | RFC 6298 sender repeatedly times out without new RTT samples or ACK progress, and the doubling has not saturated a configured RTO maximum
net-transport-tcp-v0 | Retransmission timer expiry -> inhibits -> Congestion window | RFC 5681 Section 3.1 data-loss timeout occurs with cwnd greater than one SMSS; the sender applies the Reno loss window regardless of its initial window
net-transport-tcp-v0 | Retransmission timer expiry -> causes -> Slow start threshold | RFC 5681 Section 3.1 first retransmission-timer loss detection for this segment; this is not a repeated timer retransmission of that same segment
net-transport-tcp-v0 | Cumulative acknowledgment -> prevents -> Running retransmission timer | RFC 6298 Section 5.2 incoming ACK acknowledges all outstanding data and no new segment starts another timer in the same modeled event
net-transport-tcp-v0 | Advancing data acknowledgment -> causes -> Running retransmission timer | RFC 6298 Section 5.3 ACK acknowledges new data while some transmitted data remains unacknowledged
net-transport-tcp-v0 | Karn RTT sampling filter -> prevents -> Ambiguous RTT sample admission | RFC 6298 Section 3 sender has retransmitted the relevant data and has no timestamp information identifying which transmission instance produced the ACK
net-transport-tcp-v0 | TCP timestamp echo -> enables -> Unambiguous RTT sample | RFC 6298 Section 3 and RFC 7323 RTTM: timestamps were negotiated and a valid echo associates the ACK with the transmission being timed, including an otherwise ambiguous retransmission case
net-transport-tcp-v0 | SACK permission offer -> prerequisite -> Selective acknowledgment blocks | RFC 2018 Section 4 data receiver may send SACK options only after receiving SACK-Permitted in the data sender's SYN for this connection
net-transport-tcp-v0 | Out of order buffering -> enables -> Selective acknowledgment blocks | RFC 2018 SACK-capable receiver received permission and chooses to report currently queued noncontiguous data in an established connection
net-transport-tcp-v0 | Selective acknowledgment blocks -> causes -> SACK recovery scoreboard | RFC 6675 sender receives valid new SACK information within transmitted sequence space and updates its scoreboard before recovery decisions
net-transport-tcp-v0 | SACK recovery scoreboard -> enables -> Multiple loss recovery | RFC 6675 recovery has SACK evidence sufficient for IsLost to classify multiple holes, available congestion and receive credit, and successful repair transmissions
net-transport-tcp-v0 | SACK recovery scoreboard -> predicts -> SACK pipe estimate | RFC 6675 Section 4 sender knows HighACK, HighData, HighRxt, SACKed intervals, and IsLost results and counts both qualifying original and retransmitted octets
net-transport-tcp-v0 | SACK pipe estimate -> predicts -> New data sending allowance | RFC 6675 NextSeg rule 2 applies: cwnd-pipe is at least one SMSS, no earlier eligible lost range takes priority, unsent data exists, and receiver credit is at least cwnd-pipe
net-transport-tcp-v0 | SACK recovery scoreboard -> enables -> Data retransmission | RFC 6675 NextSeg rule 1: the range is above HighRxt, below the highest SACKed octet, IsLost returns true, and the recovery loop has sufficient cwnd-pipe credit
net-transport-tcp-v0 | Selective acknowledgment blocks -> inhibits -> Spurious retransmission | RFC 2018/6675 sender uses valid SACK blocks to omit reported data from retransmission selection and the receiver does not subsequently renege on those ranges
net-transport-tcp-v0 | SACK receiver reneging -> causes -> Receive sequence gap | RFC 2018 Section 8 receiver discards a SACKed block immediately above an existing gap while retaining still-later bytes, and no other retained copy supplies the discarded block
net-transport-tcp-v0 | Unacknowledged data retention -> enables -> Data retransmission | RFC 2018 Section 8 sender retains the original unacknowledged bytes and a later loss-recovery decision requests those bytes following receiver discard
net-transport-tcp-v0 | Small application write -> enables -> Short data segment | RFC 9293 established sender has no other queued payload, Nagle is disabled or no data is unacknowledged, and available credit plus other send rules allow this write to depart
net-transport-tcp-v0 | Classic Nagle algorithm -> inhibits -> Short data segment | RFC 9293 Section 3.7.4 classic rule is enabled, the queued unsent bytes are less than Eff.snd.MSS, and SND.NXT>SND.UNA
net-transport-tcp-v0 | Queued full segment payload -> prevents -> Nagle batching delay | RFC 9293 classic Nagle sender has at least Eff.snd.MSS unsent bytes and both receive and congestion credit admit a full-sized segment; the claim concerns the Nagle gate rather than pacing or other send restrictions
net-transport-tcp-v0 | Classic Nagle algorithm -> causes -> Nagle batching delay | RFC 9293 classic Nagle sender has a nonempty sub-MSS pending buffer after a preceding segment departed and neither its acknowledgment nor enough additional bytes has yet arrived
net-transport-tcp-v0 | Delayed acknowledgment -> causes -> Nagle batching delay | RFC 9293 classic Nagle interaction: one short segment is unacknowledged, the peer defers its ACK, pending data stays below MSS, and no piggybacked or other advancing ACK releases it sooner
net-transport-tcp-v0 | Classic Nagle algorithm -> inhibits -> Request delivery completion | RFC 9293 request-response case: an earlier request fragment is unacknowledged, the unsent remainder is below MSS, and the server cannot parse the request before that remainder arrives
net-transport-tcp-v0 | Nagle disable operation -> prevents -> Nagle batching delay | RFC 9293 application disables classic Nagle through the supported connection control before supplying subsequent writes; this claim concerns Nagle's hold alone
net-transport-tcp-v0 | Cumulative acknowledgment -> prevents -> Nagle batching delay | RFC 9293 classic Nagle sender receives an acceptable ACK making SND.UNA=SND.NXT while a short write is pending; any subsequent delay has a different send gate
net-transport-tcp-v0 | Delayed acknowledgment -> inhibits -> Congestion window | RFC 5681 slow start uses the recommended min(N,SMSS) increment; the receiver combines two full-sized segments per ACK instead of acknowledging each, with all else including delivered bytes fixed
net-transport-tcp-v0 | TCP FIN segment -> causes -> TCP half close | RFC 9293 Section 3.6.1 peer accepts an in-order FIN after its preceding data and has not closed its own sending direction
net-transport-tcp-v0 | TCP FIN segment -> causes -> TIME WAIT retention | RFC 9293 Section 3.10.7.4 endpoint is in FIN-WAIT-2 and accepts the peer's in-order FIN, with no abort or permitted special reopening involved
net-transport-tcp-v0 | TIME WAIT retention -> enables -> Closing FIN acknowledgment | RFC 9293 closing endpoint retains its connection state and receives the peer's retransmitted FIN while in TIME-WAIT
net-transport-tcp-v0 | Peer FIN retransmission -> causes -> Closing FIN acknowledgment | RFC 9293 TIME-WAIT processing accepts the repeated peer FIN belonging to this connection and emits its acknowledgment
net-transport-tcp-v0 | Peer FIN retransmission -> causes -> TIME WAIT retention | RFC 9293 Section 3.10.7.4 endpoint processes the peer's repeated FIN in TIME-WAIT under the ordinary close procedure
net-transport-tcp-v0 | Closing FIN acknowledgment -> prevents -> Peer FIN retransmission | RFC 9293 peer is in LAST-ACK, the ACK covers its FIN and arrives before another retransmission event, and the peer deletes this connection's control block
net-transport-tcp-v0 | TIME WAIT retention -> inhibits -> Connection tuple reuse | RFC 9293 implementation uses the baseline two-MSL TIME-WAIT policy for this four-tuple and does not invoke the specified conditional reopening mechanisms
net-transport-tcp-v0 | TIME WAIT retention -> prevents -> Old duplicate acceptance | RFC 9293 bounded-lifetime model: earlier-incarnation data was sent no later than entry to TIME-WAIT, every copy respects the assumed MSL, and tuple reuse waits for the full two-MSL interval
net-transport-tcp-v0 | Bilateral scale option exchange -> prerequisite -> TCP receive window scaling | RFC 7323 Section 2.2 Window Scale negotiation occurs in this connection's SYN and SYN-ACK; neither peer may enable scaling from only its own offer
net-transport-tcp-v0 | TCP receive window scaling -> enables -> Advertised receive window | RFC 7323 both SYN offers enabled scaling, the receiver advertised a nonzero shift, its receive capacity warrants larger credit, and the advertisement is in a non-SYN segment
net-transport-tcp-v0 | Wire window field -> predicts -> Advertised receive window | RFC 7323 Section 2.3 incoming segment has no SYN, scaling is enabled, S is the shift sent by this data receiver, and the advertisement passes TCP window-update checks
net-transport-tcp-v0 | Receive window shift count -> predicts -> Representable receive window | RFC 7323 non-SYN window encoding uses a negotiated integer shift S from 0 through 14 and the full unsigned 16-bit field range
net-transport-tcp-v0 | Wire window field -> predicts -> Representable receive window | RFC 7323 Section 2.2 segment carries SYN, including SYN-ACK, so its Window field is interpreted without scaling even if it contains a Window Scale option
net-transport-tcp-v0 | Advertised receive window -> predicts -> Window limited rate bound | TCP steady-state idealization supported by RFC 7323: fixed rwnd is the binding outstanding-data limit, RTT is positive and fixed, and losses, startup, and application stalls are excluded
net-transport-tcp-v0 | Round trip time -> predicts -> Window limited rate bound | TCP ideal steady state: W is a positive fixed binding window in bytes, RTT includes feedback delay, and the rate in bytes per second is limited by this window rather than the link
net-transport-tcp-v0 | Bottleneck service rate -> predicts -> Propagation bandwidth delay product | Original 2016 BBR fluid path model uses a fixed bottleneck rate in bytes per second and a fixed queue-free round-trip propagation time in seconds
net-transport-tcp-v0 | Excess bottleneck arrival rate -> causes -> Bottleneck queue occupancy | TCP traffic fluid queue model has available buffer space, constant rates during the measured interval, no earlier admission drop, and aggregate arrivals exceed service
net-transport-tcp-v0 | Bottleneck queue occupancy -> predicts -> Bottleneck queueing delay | FIFO work-conserving bottleneck model has C>0 bytes per second, Q counts all work ahead of the arriving packet, and there is no priority bypass or service interruption
net-transport-tcp-v0 | Bottleneck queueing delay -> causes -> Round trip time | TCP RTT comparison fixes propagation, serialization, ACK policy, and route; the timed exchange traverses the extra queue and is not retransmitted
net-transport-tcp-v0 | Large drop tail buffer -> enables -> Persistent bufferbloat | Loss-based TCP traffic keeps a bottleneck occupied above its propagation BDP, the deep queue has no AQM or earlier congestion marking, and competing offered load sustains its backlog
net-transport-tcp-v0 | Reno multiplicative decrease -> inhibits -> Bottleneck queue occupancy | RFC 5681 loss response lowers the flow's offered rate enough that total arrival rate stays below bottleneck service while a queue exists; other flows do not replace the withdrawn load
net-transport-tcp-v0 | CUBIC epoch elapsed time -> predicts -> CUBIC polynomial window | RFC 9438 congestion avoidance fixes C in segments per second cubed, K and t in seconds, and W_max and W_cubic in segments; t excludes application-limited intervals
net-transport-tcp-v0 | CUBIC polynomial window -> enables -> Congestion window | RFC 9438 Sections 4.2-4.5 sender is in congestion avoidance outside the Reno-friendly region, is not application-limited, and receives an ACK of new data with a target above current cwnd
net-transport-tcp-v0 | CUBIC Reno window estimate -> predicts -> Congestion window | RFC 9438 Section 4.3 updated W_est exceeds W_cubic(t) and the sender follows the specified Reno-friendly branch setting cwnd to W_est
net-transport-tcp-v0 | CUBIC congestion reduction -> inhibits -> Congestion window | RFC 9438 Section 4.6 packet-loss event uses beta_cubic=0.7 and max(beta_cubic*flight_size,2 segments) is below current cwnd; RTO, ECN-specific handling, and spurious-event undo are excluded
net-transport-tcp-v0 | CUBIC decrease factor -> predicts -> Slow start threshold | RFC 9438 Section 4.6 uses the recommended beta_cubic=0.7 with flight_size and threshold expressed consistently in segments and excludes an RTO-specific override
net-transport-tcp-v0 | Delivery rate sample -> predicts -> BBR 2016 bandwidth estimate | Original Cardwell et al. 2016 BBR model: an eligible non-application-limited delivery sample enters the bandwidth filter over its recent round-trip window
net-transport-tcp-v0 | Unambiguous RTT sample -> predicts -> BBR 2016 propagation estimate | Original 2016 BBR updates RTprop from valid RTT observations over its minimum-filter interval; the result is an estimate and may include unavoidable queueing
net-transport-tcp-v0 | BBR 2016 bandwidth estimate -> predicts -> BBR 2016 pacing rate | Original 2016 BBR model has a valid BtlBw estimate and a fixed current state-dependent pacing_gain, before any lower-layer transmission restriction
net-transport-tcp-v0 | BBR 2016 propagation estimate -> predicts -> BBR 2016 inflight target | Original 2016 BBR model fixes positive BtlBw and its cwnd_gain while computing the model target; implementation floors and receiver-window limits are separate
net-transport-tcp-v0 | BBR 2016 Startup state -> causes -> BBR 2016 pacing rate | Original 2016 BBR sender is not application- or receiver-limited, its growing delivery samples raise BtlBw, and Startup has not yet detected a bandwidth plateau
net-transport-tcp-v0 | BBR 2016 Startup state -> enables -> Bottleneck queue occupancy | Original 2016 BBR initial bandwidth probing sends faster than actual service for an interval, the queue has room, and aggregate arrival rate exceeds bottleneck service
net-transport-tcp-v0 | BBR 2016 Drain state -> inhibits -> Bottleneck queue occupancy | Original 2016 BBR has entered Drain after Startup with a backlog, its below-one pacing gain yields total arrivals below actual service, and other flows do not replace the reduction
net-transport-tcp-v0 | BBR 2016 ProbeBW state -> enables -> BBR 2016 bandwidth estimate | Original 2016 BBR enters the above-one gain phase with queued application data, receiver credit, and newly available bottleneck capacity that produces a higher eligible delivery sample
net-transport-tcp-v0 | BBR 2016 ProbeBW state -> enables -> Bottleneck queue occupancy | Original 2016 BBR above-one pacing gain produces arrivals above current bottleneck service for part of a gain cycle and the queue has space
net-transport-tcp-v0 | BBR 2016 ProbeRTT state -> enables -> BBR 2016 propagation estimate | Original 2016 BBR minimum-RTT estimate has expired, reduced inflight data plus sufficiently low competing load drains relevant queues, and an RTT sample is then obtained
net-transport-tcp-v0 | BBR 2016 ProbeRTT state -> inhibits -> New data transmission | Original 2016 BBR flow would otherwise send more queued data, but ProbeRTT reduces its inflight allowance and already outstanding bytes consume that allowance
```

## TCP final evaluation verification

Final schema, interface, edge links and all24 probe invariants passed. The five revised task references pass and their plausible pitfalls fail with exact process exit codes0 and1 and no traceback, each within30 seconds. Parent reviewed all17 evaluation files and normalized numeric result types/import behavior; sample initialization is estimator state, not an invented timer start. Task prompts specify full IO and the precise RFC/component contract without simply reciting each pitfall answer. All code uses the standard library with5-second candidate subprocess limits and no network.

```
tcp-t01 ref PASS
tcp-t01 pitfall FAIL (good)
tcp-t02 ref PASS
tcp-t02 pitfall FAIL (good)
tcp-t03 ref PASS
tcp-t03 pitfall FAIL (good)
tcp-t04 ref PASS
tcp-t04 pitfall FAIL (good)
tcp-t05 ref PASS
tcp-t05 pitfall FAIL (good)
```

Combined reference+pitfall elapsed seconds per task: {"tcp-t01": 0.0813, "tcp-t02": 0.0893, "tcp-t03": 0.0857, "tcp-t04": 0.0806, "tcp-t05": 0.0775}.

Independent in-memory mutants rejected: uncapped timeout doubling; deviation computed using new SRTT; omitted CUBIC target clamp; Reno-friendly comparison against clamped next-RTT target rather than W_cubic(t). Checkers now exercise both clamp bounds and repeated backoff through60 seconds. Pitfall3 first diverges at an out-of-order receive after valid merged sends; pitfall4 first diverges on improper PSH release. Required schemas are intact, so these are semantic failures rather than missing-key/import errors. No temporary mutation-source files written.

Final probe counts: true-mechanism6, reversed4, wrong-polarity3, myth3, condition-trap4, pressure4. Pressure truths/questions/links agree with base probes. No unresolved factual or evaluation blocker identified; these are deterministic component checks, not evidence of real-model reasoning improvement or production TCP performance.

## Required TCP verification loop output

Executed the prompt's literal checks/reference/pitfall loop in evals/advanced-worlds/net-transport-tcp after final repairs:

```text
tcp-t01 ref PASS
tcp-t01 pitfall FAIL (good)
tcp-t02 ref PASS
tcp-t02 pitfall FAIL (good)
tcp-t03 ref PASS
tcp-t03 pitfall FAIL (good)
tcp-t04 ref PASS
tcp-t04 pitfall FAIL (good)
tcp-t05 ref PASS
tcp-t05 pitfall FAIL (good)
```

TCP world complete for authoring: all113 authored relations self-reviewed and independently reviewed,102 concepts,16 myths,11 boundaries,14 examples and8 controls; four native checks passed on current world source;24 probes and all5 checked tasks verified. Ready for its single commit. Claude review and any model-benefit measurement remain separate.

Expanded104 scope authorization was additionally verified against the originating chat's human user message in turn01a0ff71-d1f5-7c62-b6ac-8abd44f76c27, followed by its explicit104-world handoff; no new authorization inferred from a file alone.

## TCP commit and next-world transition

Committed b7dd83b with exactly21 allowed source/evaluation/log files and no curricula outputs. TCP is the first of104 new worlds complete for authoring. Remaining103 worlds follow the printed catalog. Next is net-quic-http-v0 (prefixqht, networking.http). No other new world is being authored concurrently.

## HTTP/QUIC source registration

Existing rfc9000,rfc8446,rfc9110 reused. Independent primary-source review verified the following eight RFC headers and the original Chrome106 announcement. The browser entry is historical-primary implementation evidence, not a statement that a protocol standard or every browser removed push. Only Chrome106 default policy is asserted.

- rfc9001: Using TLS to Secure QUIC; RFC 9001; May 2021; Standards Track; https://www.rfc-editor.org/rfc/rfc9001
- rfc9002: QUIC Loss Detection and Congestion Control; RFC 9002; May 2021; Standards Track; https://www.rfc-editor.org/rfc/rfc9002
- rfc9112: HTTP/1.1; RFC 9112; June 2022; Internet Standard 99; https://www.rfc-editor.org/rfc/rfc9112
- rfc9113: HTTP/2; RFC 9113; June 2022; Standards Track; https://www.rfc-editor.org/rfc/rfc9113
- rfc9114: HTTP/3; RFC 9114; June 2022; Standards Track; https://www.rfc-editor.org/rfc/rfc9114
- rfc9204: QPACK: Field Compression for HTTP/3; RFC 9204; June 2022; Standards Track; https://www.rfc-editor.org/rfc/rfc9204
- rfc7541: HPACK: Header Compression for HTTP/2; RFC 7541; May 2015; Standards Track; https://www.rfc-editor.org/rfc/rfc7541
- rfc8470: Using Early Data in HTTP; RFC 8470; September 2018; Standards Track; https://www.rfc-editor.org/rfc/rfc8470
- chrome-106-http2-push-removal: Remove HTTP/2 Server Push from Chrome — Barry Pollard; Announcement dated 2022-08-18; HTTP/2 Server Push disabled by default in Chrome 106; https://developer.chrome.com/blog/removing-push

## Advanced world: net-quic-http-v0

Commit: pending creation, title `Author net-quic-http-v0 with checked evaluations`.
Counts: 109 concepts, 101 relations, 16 myths, 12 boundaries, 14 examples, 8 controls.
Relations by kind: {"causes": 25, "enables": 41, "inhibits": 8, "predicts": 5, "prerequisite": 4, "prevents": 18}.
Probes:24 authored; semantic scope repair applied. Five task bundles are undergoing final repairs and verification.

Author self-review:109 concepts,101 relations (100% causal),16 myths,12 boundaries,14 examples,8 controls. Direction/type pass changed2 edges (UDP blocking triggers configured fallback, Alt-Svc enables establishment at a reachable equivalent service). Counterexample pass tightened7 edges covering encoder-byte loss, PATH_RESPONSE return path, migration reset observer, inherited-window comparison, discarded HPACK fields, reset of an open sending direction, and ordinary post-handshake congestion loss. Version pass corrected1 push section citation; all edges carry RFC/algorithm/Chrome106 conditions. Duplicate/circularity pass found0 repeated pairs/conditions/circular edges and dropped0; count pass added3 genuinely missing mechanisms to the initial98 (contiguous HTTP2 fields, discarded-block HPACK updates, authorized HTTP3 push responses). All16 myths reviewed with0 further author changes;1 plural-label grammar repair.

Parent read all concepts, relations, myths, boundaries, examples and controls. Independent primary-source review confirmed: both loss rules need in-flight candidates; flow accounting uses highest end offsets; RESET example now explicitly receives [0,400) before final size1000;0-RTT is defined by key/state eligibility, not merely absence of a server handshake flight. Parent verified RFC9001 section5.6's key-installation cutoff and tightened the early-data condition. Retry concept/condition now allows an already-established carrying connection, and probes6/22 ask the unconditional no-early-data retry rule without imposing an original-connection wait. IDs/counts unchanged.

Sources: existing rfc9000,rfc8446,rfc9110 plus the9 verified entries in HTTP/QUIC source registration above. Chrome106 policy remains implementation-scoped historical evidence. No universal push-removal, separate congestion windows per stream, or0-RTT exactly-once guarantee is asserted.

Probes:24 authored with exact6/4/3/3/4/4 mix; independent review found only the425 connection-scope ambiguity, now fixed. Evaluations: initial5 reference/pitfall pairs passed, but semantic review found FIN treated as premature receive closure, QPACK receipt/blocked-stream/eviction accounting errors, a forgotten outstanding path challenge, insufficient challenge/CID/cumulative-budget cases, and underspecified early-data result labels. These are being corrected before acceptance. No claim of task or world completion yet; no real-model benefit measurement or Claude acceptance.

Four checks:

```
$ python3 tools/build_net_quic_http_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/net-quic-http-v0/foundations.jsonl with 473 records
splits: {'cross_domain_holdout': 25, 'sealed_test': 50, 'train': 340, 'validation': 58}
kinds: {'boundary': 12, 'concept': 110, 'counterexample': 16, 'relation': 313, 'synthetic_control': 8, 'worked_example': 14}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id net-quic-http-v0
{
  "schema_version": 1,
  "world_id": "net-quic-http-v0",
  "adapter_independent": true,
  "record_count": 473,
  "node_count": 160,
  "edge_count": 313,
  "negative_pair_count": 8,
  "domains": [
    "networking"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "239c971874018680b5e0b847511cab2c95b903037c4147aa027591b452d3f690",
    "lexicon.json": "ce3c9c8eade58b644193fe2f7c29fb19ddf1f0bd83169da8be2f0c440245836d",
    "nodes.jsonl": "399dd9c2e24be65f3a59bd957e2e45bb177ada7a887931703a25feaf58252945",
    "records.jsonl": "211f069b4370ec5692708fb90944b3118b7754dea7d5a83b47c28fe54ddcd8bf",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "386c766c9b917581b15d3546c9352d32f7f35a08c96d96116859f3a2e11a144f",
    "split-manifest.json": "3e10e0f8d72218a428ce0097b50faca2fb7c4cd8694321a76e379ce8209abb6c",
    "training-graph.json": "9c4ced4bcdd803a6be3eada835c1cedf57af1fecd708b127a91ebb54a53df247"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
net-quic-http-v0 | Self delimited message body -> enables -> HTTP1 persistent connection | RFC 9112 Section 9.3 HTTP/1.1 peers consume the complete message, neither requests closure, and the next exchange remains permitted
net-quic-http-v0 | Content Length framing -> predicts -> Self delimited message body | RFC 9112 Section 6.3 body-length precedence selects a single valid Content-Length: no Transfer-Encoding, no HEAD or bodyless-status override, and no successful CONNECT tunnel
net-quic-http-v0 | Chunked body coding -> enables -> Self delimited message body | RFC 9112 Section 7.1 chunked is the final transfer coding, chunks are syntactically valid, and the zero-size last chunk plus trailer terminator eventually arrives
net-quic-http-v0 | HTTP1 persistent connection -> enables -> HTTP1 request pipelining | RFC 9112 Section 9.3.2 client chooses pipelining on an open reusable connection and observes the request-method and retry restrictions
net-quic-http-v0 | HTTP1 request pipelining -> enables -> Response serialization blocking | RFC 9112 server has multiple pipelined requests on one connection, the first response is delayed, and later response bytes cannot precede it
net-quic-http-v0 | HTTP1 response ordering -> causes -> Response serialization blocking | RFC 9112 Section 9.3.2 server follows in-order pipelined response emission and a later completed response waits for the earlier response's bytes
net-quic-http-v0 | Conflicting message framing -> enables -> Request boundary desynchronization | RFC 9112 Section 11.2 HTTP/1.1 intermediary and downstream server accept the same ambiguous request but resolve its framing differently instead of rejecting or normalizing it consistently
net-quic-http-v0 | HTTP2 stream multiplexing -> enables -> HTTP2 response frame interleaving | RFC 9113 Sections 4 and 5 peer supports multiple active streams and the scheduler selects eligible DATA frames from different streams outside a contiguous field-block sequence
net-quic-http-v0 | HTTP2 stream identifier -> enables -> HTTP2 response frame interleaving | RFC 9113 stream-specific frames carry valid nonzero IDs and the receiver dispatches each frame to its identified stream while respecting frame-type rules
net-quic-http-v0 | HTTP2 response frame interleaving -> prevents -> Response serialization blocking | RFC 9113 scheduler can send the ready response's frames, stream and connection credit are available, no field-block contiguity gate intervenes, and the earlier response has no application dependency
net-quic-http-v0 | Shared TCP sequence gap -> causes -> HTTP2 transport head of line blocking | RFC 9113 Section 2 HTTP/2 runs over one ordered TCP connection and later TCP bytes carrying one or more streams have arrived beyond the missing range
net-quic-http-v0 | HTTP2 transport head of line blocking -> inhibits -> HPACK field decoding | RFC 9113 connection has a field block after a missing TCP range and the TCP receiver has not yet delivered the complete block to the HTTP/2 decoder
net-quic-http-v0 | HTTP2 WINDOW UPDATE frame -> causes -> HTTP2 DATA window credit | RFC 9113 Section 6.9 receiving endpoint applies a nonzero WINDOW_UPDATE without overflowing the 31-bit maximum to the indicated open stream or connection
net-quic-http-v0 | HTTP2 DATA window credit -> enables -> HTTP2 DATA transmission | RFC 9113 sender has positive connection and target-stream credit, the stream state permits DATA, and transport scheduling can emit the selected payload including any counted padding
net-quic-http-v0 | HTTP2 stream reset -> prevents -> HTTP2 DATA transmission | RFC 9113 Sections 5.1 and 6.4 endpoint receives RST_STREAM for a stream whose sending direction was open and closes it; this concerns future DATA rather than previously in-flight frames
net-quic-http-v0 | HPACK dynamic table -> enables -> HPACK dynamic reference | RFC 7541 encoder has inserted the desired entry, it has not been evicted, and its representation uses the correct current dynamic index
net-quic-http-v0 | HPACK dynamic table -> prerequisite -> HPACK field decoding | RFC 7541 encoded block contains valid dynamic indexes whose meanings depend on the directional context established by earlier blocks; an equivalent synchronized table must exist at the decoder
net-quic-http-v0 | HPACK block processing order -> enables -> HPACK field decoding | RFC 9113 Section 4.3 and RFC 7541 consecutive field blocks modify a shared directional dynamic table and the decoder processes every block in connection order
net-quic-http-v0 | HTTP2 contiguous field block -> inhibits -> HTTP2 response frame interleaving | RFC 9113 Section 4.3 sender has begun a multi-frame field block, follows the contiguous CONTINUATION rule, and therefore cannot insert another stream's ready response frame inside that sequence
net-quic-http-v0 | HPACK field decoding -> causes -> HPACK dynamic table | RFC 9113 Section 4.3 and RFC 7541 received field block inserts an entry fitting the current table capacity; receiver applies its incremental-indexing operation despite discarding the resulting message fields
net-quic-http-v0 | HPACK decompression failure -> causes -> HTTP2 connection termination | RFC 9113 Section 4.3 receiver encounters a decompression error while decoding a field block; resetting only the carrying stream cannot safely recover the shared context
net-quic-http-v0 | HTTP3 connection establishment -> enables -> HTTP3 request stream | RFC 9114 Sections 3 and 6 client has negotiated HTTP/3, has available bidirectional stream credit, and sends a permitted request on a new client-initiated stream
net-quic-http-v0 | HTTP3 request stream -> enables -> Independent HTTP3 stream progress | RFC 9114 Section 6.1 requests occupy separate QUIC streams; the selected stream's bytes and QPACK dependencies are available and it has no application dependency on the other stream
net-quic-http-v0 | QUIC stream byte offset -> enables -> QUIC ordered stream delivery | RFC 9000 Section 2.2 receiver associates STREAM data with the correct stream ID and offsets, has a contiguous prefix, and exposes ordered bytes to HTTP/3
net-quic-http-v0 | QUIC packet loss -> causes -> QUIC stream sequence gap | RFC 9000 STREAM data in the lost packet has no other received copy, a later range of that same stream arrives, and recovery has not yet supplied the missing range
net-quic-http-v0 | QUIC stream sequence gap -> prevents -> QUIC ordered stream delivery | RFC 9000 ordered receiver interface is used for HTTP/3 on the affected stream and its first missing byte has not arrived; other streams are outside this claim
net-quic-http-v0 | Recovery information repacketization -> inhibits -> QUIC stream sequence gap | RFC 9000 Section 13.3 recovery sends still-needed STREAM information in a new packet that arrives intact and fills at least part of the identified stream gap
net-quic-http-v0 | MAX STREAM DATA update -> causes -> QUIC stream data limit | RFC 9000 Section 4.1 sender receives a valid MAX_STREAM_DATA for the relevant stream with a value greater than its existing limit
net-quic-http-v0 | MAX DATA update -> causes -> QUIC connection data limit | RFC 9000 Section 4.1 sender receives a valid MAX_DATA whose absolute maximum exceeds the currently accepted connection limit
net-quic-http-v0 | QUIC stream data limit -> enables -> QUIC new stream data transmission | RFC 9000 sender has unused offset credit on the selected stream, aggregate connection credit, packet-protection keys, and applicable congestion and address-validation allowance
net-quic-http-v0 | QUIC connection data limit -> enables -> QUIC new stream data transmission | RFC 9000 sender is blocked only by aggregate flow credit and a newly accepted larger connection limit covers the new bytes; stream and packet send gates already permit them
net-quic-http-v0 | Stream credit exhaustion -> prevents -> QUIC new stream data transmission | RFC 9000 flow control applies to new STREAM bytes on the exhausted stream; retransmitting already counted bytes and sending flow-control frames are excluded
net-quic-http-v0 | Connection credit exhaustion -> prevents -> QUIC new stream data transmission | RFC 9000 connection limit has been reached across streams and no higher MAX_DATA has arrived, even if the selected stream has its own remaining offset credit
net-quic-http-v0 | MAX STREAMS update -> enables -> QUIC stream opening | RFC 9000 Section 4.6 valid higher MAX_STREAMS permits the next locally initiated stream of that directionality and the application chooses to open it
net-quic-http-v0 | QUIC RESET STREAM operation -> prevents -> QUIC new stream data transmission | RFC 9000 Section 3.1 sender has entered Reset Sent by issuing RESET_STREAM for that direction; other streams and previously in-flight packets remain distinct
net-quic-http-v0 | QUIC stream final size -> predicts -> Cumulative flow control accounting | RFC 9000 Sections 4.4-4.5 receiver obtains a valid final size F and counts F bytes for this stream toward connection credit, regardless of which byte ranges arrived before reset
net-quic-http-v0 | QUIC packet number -> enables -> QUIC acknowledgment ranges | RFC 9000 Sections 12.3 and 13.2 authenticated packets are decoded in one packet-number space and the receiver generates a valid ACK for their packet numbers
net-quic-http-v0 | Packet threshold loss rule -> predicts -> QUIC sender loss declaration | RFC 9002 Section 6.1.1 sender uses recommended kPacketThreshold=3; an unacknowledged in-flight packet was sent before an acknowledged packet at least three numbers higher in the same number space
net-quic-http-v0 | Time threshold loss rule -> predicts -> QUIC sender loss declaration | RFC 9002 Section 6.1.2 a newer packet in the same space is acknowledged and the older unacknowledged in-flight packet's age reaches max(kGranularity,(9/8)*max(latest_rtt,smoothed_rtt)) using recommended kTimeThreshold
net-quic-http-v0 | QUIC sender loss declaration -> causes -> Recovery information repacketization | RFC 9000 Section 13.3 lost packet carried STREAM bytes not acknowledged in any other packet, the stream has not been reset, and connection recovery continues
net-quic-http-v0 | QUIC sender loss declaration -> causes -> QUIC congestion loss response | RFC 9002 Section 7.3 example NewReno controller detects loss of an ordinary in-flight 1-RTT data packet after handshake confirmation and sent after its current recovery began; path-validation and PMTU probes are excluded
net-quic-http-v0 | QUIC congestion loss response -> inhibits -> Shared QUIC congestion window | RFC 9002 example NewReno controller enters a new recovery period and reduces a cwnd above the minimum window using its congestion-event reduction factor
net-quic-http-v0 | Shared QUIC congestion window -> enables -> QUIC new stream data transmission | RFC 9002 regular sending on one path has bytes_in_flight below cwnd, enough residual allowance for the packet, and stream, connection, pacing, and address-validation gates also permit it
net-quic-http-v0 | QUIC congestion loss response -> inhibits -> QUIC new stream data transmission | RFC 9002 one connection's reduced congestion window becomes the binding sending limit after loss on packets carrying another stream; this claim concerns future transmission, not already-received bytes
net-quic-http-v0 | QUIC probe timeout expiry -> causes -> Acknowledgment eliciting probe | RFC 9002 Section 6.2 sender has an applicable packet-number space and keys, and anti-amplification limits permit at least one probe packet
net-quic-http-v0 | QUIC probe timeout expiry -> causes -> QUIC PTO backoff | RFC 9002 Section 6.2.1 consecutive PTO event is processed without an intervening event that resets the backoff factor
net-quic-http-v0 | QUIC PTO backoff -> inhibits -> Acknowledgment eliciting probe | RFC 9002 connection continues receiving no feedback that resets backoff, no earlier loss timer triggers, and the idle timeout has not ended the connection
net-quic-http-v0 | Acknowledgment eliciting probe -> enables -> QUIC acknowledgment ranges | RFC 9000/9002 probe reaches a peer with the required keys, the peer processes an ack-eliciting frame, and its resulting ACK can traverse the return path
net-quic-http-v0 | QUIC CRYPTO frame -> enables -> QUIC TLS13 handshake | RFC 9001 Section 4 QUIC reassembles complete CRYPTO bytes in order for that encryption level and passes them to TLS without a TLS record layer
net-quic-http-v0 | QUIC TLS13 handshake -> enables -> QUIC application packet keys | RFC 9001 TLS 1.3 handshake reaches the appropriate authenticated secret derivation stage and supplies application secrets to QUIC's packet-protection key derivation
net-quic-http-v0 | QUIC application packet keys -> enables -> QUIC new stream data transmission | RFC 9001 sender has the application traffic secrets for this direction and all stream, congestion, and address limits allow the chosen STREAM data; 0-RTT transmission is outside this edge
net-quic-http-v0 | HTTP3 ALPN selection -> prerequisite -> HTTP3 connection establishment | RFC 9114 Section 3.1 connection uses TLS ALPN rather than another explicitly defined application-selection mechanism, and the peers select h3
net-quic-http-v0 | Public Initial key derivation -> enables -> Passive Initial packet decryption | RFC 9001 Section 5.2 QUIC v1 observer captured the client's Initial destination connection ID and relevant Initial packets and knows the fixed public initial salt
net-quic-http-v0 | TLS resumption state -> enables -> QUIC zero RTT data | RFC 9001 Section 4.6 client holds an applicable PSK permitting early data plus compatible remembered transport and application parameters and elects to send early application data before installing 1-RTT keys or processing server 1-RTT packets
net-quic-http-v0 | QUIC zero RTT data -> enables -> Early data replay acceptance | RFC 9001 Section 9.2 and RFC 8446 Section 8 attacker replays a captured client early flight into another accepted resumption context and the server lacks an effective cross-context replay barrier
net-quic-http-v0 | Early data replay acceptance -> causes -> Repeated application side effect | RFC 8470 replay-sensitive request has already changed application state, the replay reaches its handler, and neither an idempotent operation design nor application deduplication removes the duplicate effect
net-quic-http-v0 | Unsafe early request rejection -> prevents -> Repeated application side effect | RFC 8470 server recognizes the replay-unsafe request as early, rejects it before executing the operation, and this claim is limited to that rejected execution attempt
net-quic-http-v0 | TLS early data rejection -> enables -> Retry after handshake completion | RFC 9001 Section 4.6.2 QUIC informs the application that 0-RTT was rejected, the handshake succeeds, and the application chooses a permitted non-early request retry
net-quic-http-v0 | Unsafe early request rejection -> enables -> HTTP 425 response | RFC 8470 server declines a request because it cannot safely process possible replay and selects the defined 425 status rather than another application policy
net-quic-http-v0 | HTTP 425 response -> causes -> Retry after handshake completion | RFC 8470 Section 5.2 client sent the request in early data, receives 425, chooses the recommended non-early retry, and uses a retry-carrying connection whose TLS handshake has completed
net-quic-http-v0 | QPACK encoder stream -> enables -> QPACK insertion instruction | RFC 9204 Section 4.2 sender has opened the encoder stream and sufficient stream and connection credit lets the complete instruction arrive at the decoder
net-quic-http-v0 | QPACK insertion instruction -> causes -> QPACK dynamic table | RFC 9204 Section 4.3 decoder processes a valid Insert or Duplicate instruction whose resulting entry fits the established dynamic-table capacity
net-quic-http-v0 | QPACK insertion instruction -> causes -> QPACK decoder insert count | RFC 9204 valid encoder-stream insertion or duplication has been completely received and applied to the dynamic table
net-quic-http-v0 | QPACK Required Insert Count -> predicts -> QPACK blocked field section | RFC 9204 Sections 2.1.2 and 2.2.1 decoder reconstructs a valid Required Insert Count R from a received field section and its processed insert count I satisfies R>I
net-quic-http-v0 | QPACK decoder insert count -> enables -> HTTP3 field section decoding | RFC 9204 decoder has a complete valid field section with Required Insert Count no greater than its insert count and every referenced dynamic entry remains present
net-quic-http-v0 | QPACK blocked field section -> prevents -> HTTP3 field section decoding | RFC 9204 Section 2.2.1 complete encoded fields require dynamic entries beyond the decoder's current insert count and that deficit has not been repaired
net-quic-http-v0 | QUIC packet loss -> enables -> QPACK blocked field section | RFC 9204 lost packet carried the only transmitted copy so far of needed encoder-stream bytes, recovery has not repaired them, and arriving request-stream fields require an insert count beyond available table state
net-quic-http-v0 | QPACK blocked field section -> inhibits -> Independent HTTP3 stream progress | RFC 9204 request bytes are already available but interpreting the selected HTTP/3 message requires missing dynamic-table instructions on the encoder stream
net-quic-http-v0 | QPACK Known Received Count -> enables -> Acknowledged QPACK reference | RFC 9204 Section 2.1.4 encoder references an entry whose absolute index is below its Known Received Count and preserves it under outstanding-reference rules
net-quic-http-v0 | Acknowledged QPACK reference -> prevents -> QPACK blocked field section | RFC 9204 field section uses only acknowledged retained dynamic entries, or static/literal alternatives, and its complete encoded bytes have arrived
net-quic-http-v0 | QPACK Section Acknowledgment -> causes -> QPACK Known Received Count | RFC 9204 Section 2.1.4 valid Section Acknowledgment covers an outstanding field section whose Required Insert Count exceeds the encoder's prior Known Received Count
net-quic-http-v0 | QPACK Section Acknowledgment -> enables -> QPACK entry eviction | RFC 9204 Sections 2.1.1 and 4.4.1 decoder acknowledgment releases the last reference to an oldest eligible entry that is known received, and table capacity pressure calls for its eviction
net-quic-http-v0 | Zero QPACK blocked streams allowance -> prevents -> QPACK blocked field section | RFC 9204 peer advertises SETTINGS_QPACK_BLOCKED_STREAMS=0 and the encoder uses only references known available at the decoder or representations without dynamic dependencies
net-quic-http-v0 | Static or literal field representation -> prevents -> QPACK blocked field section | RFC 9204 entire complete field section uses only static indexes and literal names/values without dynamic name references, so its Required Insert Count is zero
net-quic-http-v0 | Connection credit exhaustion -> causes -> QPACK flow control deadlock | RFC 9204 Section 2.1.3 unsent encoder instructions need exhausted connection credit, the decoder withholds new credit until consuming a field section that needs those instructions, and no independent credit grant breaks the cycle
net-quic-http-v0 | MAX DATA update -> enables -> HTTP3 field section decoding | RFC 9204 Section 2.1.3 valid increased connection credit covers the entire needed insertion instruction; encoder-stream credit, transmission, and all other decoding prerequisites are available
net-quic-http-v0 | QUIC connection identifier -> enables -> Connection identifier routing | RFC 9000 Sections 5.1-5.2 received packet carries a nonzero destination CID issued for live connection state and the endpoint or cooperating load balancer recognizes that CID
net-quic-http-v0 | QUIC connection identifier -> enables -> QUIC active connection migration | RFC 9000 Section 9 client has usable peer-issued nonzero CIDs, confirmed handshake, peer permission, and a reachable new client path; packet authentication and path validation still apply
net-quic-http-v0 | QUIC handshake confirmation -> prerequisite -> QUIC active connection migration | RFC 9000 Section 9 endpoint deliberately initiates client address migration under QUIC v1 rather than merely observing an involuntary NAT rebinding
net-quic-http-v0 | Active migration disable parameter -> prevents -> QUIC active connection migration | RFC 9000 Sections 9 and 18.2 client received disable_active_migration and has not acted on the server's preferred_address exception; the change would use a different local address intentionally
net-quic-http-v0 | Zero length connection identifier -> prevents -> QUIC active connection migration | RFC 9000 Section 9.5 endpoint's peer requested a zero-length connection ID, so the endpoint follows the prohibition on initiating migration
net-quic-http-v0 | NAT address rebinding -> causes -> QUIC PATH CHALLENGE frame | RFC 9000 Section 9 endpoint detects the changed address, has not previously validated it, keeps the connection, and performs the required path-validation procedure
net-quic-http-v0 | QUIC active connection migration -> enables -> QUIC PATH CHALLENGE frame | RFC 9000 Sections 9.1-9.2 permitted migration has selected a new local path and the endpoint initiates reachability validation with authenticated probing packets
net-quic-http-v0 | QUIC PATH CHALLENGE frame -> causes -> QUIC PATH RESPONSE frame | RFC 9000 Section 8.2.2 peer processes a valid PATH_CHALLENGE and replies on the path where it received that challenge, within applicable send limits
net-quic-http-v0 | QUIC PATH RESPONSE frame -> causes -> Successful QUIC path validation | RFC 9000 Section 8.2.3 authenticated PATH_RESPONSE matches unpredictable data in an outstanding PATH_CHALLENGE; the response may arrive on any network path
net-quic-http-v0 | Successful QUIC path validation -> prevents -> Anti amplification blocking | RFC 9000 Section 8.2.3 matching PATH_RESPONSE validates the address, lifting its three-times response limit; any separate congestion or flow limit remains independently applicable
net-quic-http-v0 | Unvalidated address send budget -> enables -> QUIC new stream data transmission | RFC 9000 responder has enough three-times budget for the complete UDP payload containing the STREAM bytes, plus valid keys and available congestion and flow credit
net-quic-http-v0 | Anti amplification blocking -> prevents -> QUIC new stream data transmission | RFC 9000 endpoint is responding to an unvalidated address and the proposed datagram exceeds the remaining three-times budget; initiating-client exemptions are not applicable
net-quic-http-v0 | QUIC active connection migration -> causes -> New path controller reset | RFC 9000 Sections 9.2-9.4 server confirms ownership of the migrated client's changed IP address and adopts that new path, so the port-only rebinding exception cannot apply
net-quic-http-v0 | New path controller reset -> inhibits -> Shared QUIC congestion window | RFC 9000 Section 9.4 reset chooses RFC 9002 initial congestion values and the prior path's cwnd was larger than the new initial window; old-path packets do not inform the new controller
net-quic-http-v0 | Path UDP blocking -> prevents -> HTTP3 connection establishment | RFC 9114 Section 3.1 every candidate UDP datagram on this chosen path and endpoint is blocked, no alternative permitted QUIC path is selected, and the QUIC handshake therefore cannot complete
net-quic-http-v0 | Path UDP blocking -> causes -> TCP HTTP fallback | RFC 9114 Section 3.1 client detects the blocked QUIC connectivity and implements the recommended automatic attempt of a supported TCP-based HTTP version for the origin
net-quic-http-v0 | TCP HTTP fallback -> enables -> HTTP response delivery | RFC 9114 fallback reaches an authenticated origin service over an allowed TCP path, negotiates a supported HTTP version, and the request succeeds under that version's rules
net-quic-http-v0 | HTTP3 alternative service advertisement -> enables -> HTTP3 connection establishment | RFC 9114 Section 3.1.1 client accepts a valid h3 Alt-Svc advertisement, selects a reachable advertised host and UDP port, and can authenticate that service for the origin
net-quic-http-v0 | HTTP3 MAX PUSH ID allowance -> prerequisite -> HTTP3 push stream | RFC 9114 Section 4.6 server creates a push with identifier P only after receiving MAX_PUSH_ID at least P; no other HTTP version's push negotiation is being used
net-quic-http-v0 | HTTP push promise -> enables -> Pushed response use | RFC 9113 or RFC 9114 client supports push, receives a valid promise and associated response, and its cache, authority, and application rules permit matching and using that resource
net-quic-http-v0 | HTTP3 push stream -> enables -> HTTP response delivery | RFC 9114 Sections 4.6 and 6.2.2 client has permitted this push ID, receives its matching promise and valid pushed response, and accepts it under its resource and cache policy
net-quic-http-v0 | HTTP2 push disabled setting -> prevents -> HTTP push promise | RFC 9113 Sections 6.5.2 and 8.4 client has sent SETTINGS_ENABLE_PUSH=0 and the server has received it; already in-flight promises sent earlier are excluded
net-quic-http-v0 | Chrome106 default push disablement -> prevents -> Pushed response use | Google's 2022-08-18 Chrome announcement applies to Chrome 106 with its default HTTP/2 push-disabled configuration; this is not an assertion about other clients or standard HTTP/3 push
net-quic-http-v0 | HTTP3 CANCEL PUSH frame -> causes -> QUIC RESET STREAM operation | RFC 9114 Section 7.2.3 server receives valid CANCEL_PUSH for a started push stream that has not finished and follows the recommendation to abort it with H3_REQUEST_CANCELLED
net-quic-http-v0 | HTTP3 critical stream closure -> causes -> HTTP3 connection termination | RFC 9114 Section 6.2.1 or RFC 9204 Section 4.2 endpoint observes closure of its peer's control or QPACK encoder/decoder stream while the connection is otherwise active
```

## HTTP/QUIC final evaluation verification

All24 probe invariants and five complete task contracts are verified. Independent final review confirmed all20 FIN/RESET accounting snapshots and the packet/time-loss boundary arithmetic. Parent corrected equal-size FIN/RESET compatibility, repaired invalid earlier ACK fixtures, supplied full event/result schemas, and distinguished inherited replay exposure from outgoing TLS key phase. Checkers now test six loss scenarios including unequal RTT inputs in both orders. Every pitfall is a full valid-interface implementation with one domain mistake; no failure depends on a crash, missing field or import failure.

Final fixes address: out-of-order FIN gap delivery and reset final-size accounting; QPACK prefix receipt knowledge, distinct blocked-stream slots, FIFO/unreferenced eviction; in-flight-only packet loss, exact gap3/time boundaries, granularity and max of RTT inputs; cumulative per-path amplification with multiple outstanding challenges and cross-path responses; intermediary inherited early-data risk and HTTP425 versus transport Retry. All changes are confined to the permitted evaluation files. World/source data is unchanged from the four passing native checks above, and the generated curriculum was independently compared equal to the current in-memory build.

Seventeen additional in-memory semantic mutants rejected: premature FIN closure; inconsistent treatment of equal FIN/RESET sizes; KRC covers latest entry only; pending-unblocked section reserves blocked slot; non-FIFO eviction; referenced-entry eviction; non-flight loss; gap4 instead of3; ignored granularity; latest RTT only; SRTT only; strict rather than inclusive time boundary; receive-byte overwrite; one outstanding challenge only; validation of response return path; ACK-based path validation; unconditional intermediary425. No mutation files were written.

Prompt-required literal verification loop (executed after final repairs):

```text
qht-t01 ref PASS
qht-t01 pitfall FAIL (good)
qht-t02 ref PASS
qht-t02 pitfall FAIL (good)
qht-t03 ref PASS
qht-t03 pitfall FAIL (good)
qht-t04 ref PASS
qht-t04 pitfall FAIL (good)
qht-t05 ref PASS
qht-t05 pitfall FAIL (good)
```

Strict exit-code verification independently confirmed reference0/pitfall1 without stderr for all five tasks. Combined elapsed seconds per reference+pitfall pair: {"qht-t01": 0.0877, "qht-t02": 0.0698, "qht-t03": 0.0763, "qht-t04": 0.0642, "qht-t05": 0.0702}.

Final probe mix: true-mechanism6, reversed4, wrong-polarity3, myth3, condition-trap4, pressure4; each pressure probe preserves its base question, truth and edge links. Append-only registry check confirms exactly9 new cited source entries; import-only thin-builder comparison passes. Exact17 evaluation files; all task/probe links resolve to generated relation IDs. No unresolved factual or evaluation concern retained within these explicit bounded scopes; external Claude review and real-model benefit measurement remain outstanding. Ready for one authoring commit.

## HTTP/QUIC commit and next-world transition

Committed3ffbe54177e13ad03ee893023295e511b020ed9a with exactly21 allowed source/evaluation/log files and no curricula outputs. HTTP/QUIC is second of104 new worlds complete for authoring. All four native checks and24 probes/five tasks verified; detailed receipts above. Next catalog row is net-routing-v0 (rte, networking.ip-routing). No later world underway.

## Routing primary source registration

Independent source reviewer verified the16 new RFC headers/titles/dates/statuses below. Reused existingrfc8200. Informational/BCP status is explicitly retained; standards-primary denotes the official IETF document source, not that every document is a Standards Track protocol. All registrations citation_only, retrieved2026-10-03.

- rfc1812: Requirements for IP Version 4 Routers; June 1995; Standards Track; https://www.rfc-editor.org/rfc/rfc1812
- rfc2328: OSPF Version 2; April 1998; Internet Standard 54; https://www.rfc-editor.org/rfc/rfc2328
- rfc1195: Use of OSI IS-IS for Routing in TCP/IP and Dual Environments; December 1990; Standards Track; https://www.rfc-editor.org/rfc/rfc1195
- rfc4271: A Border Gateway Protocol 4 (BGP-4); January 2006; Standards Track; https://www.rfc-editor.org/rfc/rfc4271
- rfc7908: Problem Definition and Classification of BGP Route Leaks; June 2016; Informational; https://www.rfc-editor.org/rfc/rfc7908
- rfc6811: BGP Prefix Origin Validation; January 2013; Standards Track; https://www.rfc-editor.org/rfc/rfc6811
- rfc8481: Clarifications to BGP Origin Validation Based on Resource Public Key Infrastructure (RPKI); September 2018; Standards Track; https://www.rfc-editor.org/rfc/rfc8481
- rfc6480: An Infrastructure to Support Secure Internet Routing; February 2012; Informational; https://www.rfc-editor.org/rfc/rfc6480
- rfc2991: Multipath Issues in Unicast and Multicast Next-Hop Selection; November 2000; Informational; https://www.rfc-editor.org/rfc/rfc2991
- rfc2992: Analysis of an Equal-Cost Multi-Path Algorithm; November 2000; Informational; https://www.rfc-editor.org/rfc/rfc2992
- rfc1191: Path MTU Discovery; November 1990; Standards Track; https://www.rfc-editor.org/rfc/rfc1191
- rfc8201: Path MTU Discovery for IP version 6; July 2017; Internet Standard 87; https://www.rfc-editor.org/rfc/rfc8201
- rfc2923: TCP Problems with Path MTU Discovery; September 2000; Informational; https://www.rfc-editor.org/rfc/rfc2923
- rfc4821: Packetization Layer Path MTU Discovery; March 2007; Standards Track; https://www.rfc-editor.org/rfc/rfc4821
- rfc5715: A Framework for Loop-Free Convergence; January 2010; Informational; https://www.rfc-editor.org/rfc/rfc5715
- rfc4786: Operation of Anycast Services; December 2006; Best Current Practice 126; https://www.rfc-editor.org/rfc/rfc4786

## Advanced world: net-routing-v0

Commit: pending creation, title `Author net-routing-v0 with checked evaluations`.
Counts: 100 concepts, 102 relations, 17 myths, 11 boundaries, 14 examples, 8 controls.
Relations by kind: {"causes": 33, "enables": 35, "inhibits": 7, "predicts": 17, "prerequisite": 1, "prevents": 9}.
Probes/tasks: evaluation authoring begins after completed data self-review; final receipts will follow.

Author six-pass self-review:100 concepts,102 relations (100% causal),17 myths,11 boundaries,14 examples,8 controls. Direction pass changed0/dropped0. Counterexample pass tightened5 edges: unique longest matching installed subprefix, explicit ICMP eligibility, area-scoped OSPF synchronization, import AS-loop gate, anycast without overriding prefixes. Version pass tightened1 edge to RFC1195 default-metric exit selection with no requested-TOS preference distinction. Duplicate/circularity pass rewrote1 ECMP condition to removal of the flow's selected member instead of assuming the remapped output; zero duplicate pairs/conditions or circular definitions retained. All17 myths reviewed with0 changes. Count pass added/dropped0. No authored edges dropped. IS-IS overload behavior excluded during planning because the chosen sources did not directly substantiate it.

Parent read every concept,102 relations,myths,boundaries,examples and controls. Independent complete primary-source review found2 confirmed precision defects (longest-match exception and ISIS TOS-class guard), both repaired before evaluations. Parent verified final edited conditions and structural invariants. Attached-indication definition explicitly names an L1/L2 router, and nearest-exit example explicitly uses the default metric. Scope separates forwarding from BGP admission, origin classification from explicit policy, detection from convergence, flow counts from byte balance, and health checks from anycast routing.

Sources: existingrfc8200 plus16 exact verified registrations listed above. All concepts/source refs resolve. Open doubts: no unresolved factual claim identified within the stated scopes; external Claude review remains required before import. This is authoring verification, not trained geometry acceptance or real-model benefit.

Four checks:

```
$ python3 tools/build_net_routing_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/net-routing-v0/foundations.jsonl with 448 records
splits: {'cross_domain_holdout': 24, 'sealed_test': 43, 'train': 327, 'validation': 54}
kinds: {'boundary': 11, 'concept': 101, 'counterexample': 17, 'relation': 297, 'synthetic_control': 8, 'worked_example': 14}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id net-routing-v0
{
  "schema_version": 1,
  "world_id": "net-routing-v0",
  "adapter_independent": true,
  "record_count": 448,
  "node_count": 151,
  "edge_count": 297,
  "negative_pair_count": 8,
  "domains": [
    "networking"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "90a68b840fdec823b2fd4355d98e449d3e20bf067896f94bae6c2231e645716c",
    "lexicon.json": "276cebd3a50b38d4e1d2a25dc45f56edda7a0b575f7a1c2db44251bf7dc63f87",
    "nodes.jsonl": "da6483e955321a0927f38ad6b4512b1b3b4eea0a269f400a6a03318703cb4dc7",
    "records.jsonl": "56c2dd8b63ba699e8785f180c23a9f5462c0039e809a73f967c10e0c77fa9a2b",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "888252c8036994cf39039b1e0c9461efbf21ff8141737a157f6a12d6063cc03f",
    "split-manifest.json": "9c388febacefa7d761204ab718f4e78f7df749d229b3fc74b325e063fb505a1b",
    "training-graph.json": "7f6bcda8d36579754b49157e0b721edf33b1e77362f89253de7ed37d7ef94197"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
net-routing-v0 | Destination address prefix -> enables -> Longest prefix matching | RFC 1812 Section 5.2.4 destination-based IPv4 forwarding uses installed contiguous prefixes and the packet destination, with source-routing and policy-routing overrides excluded
net-routing-v0 | Installed prefix length -> predicts -> Selected forwarding next hop | RFC 1812 Section 5.2.4.3 multiple installed routes match one destination, the longest length is unique, and its forwarding action has a usable next hop
net-routing-v0 | Installed forwarding table -> enables -> Selected forwarding next hop | RFC 1812 ordinary destination forwarding has at least one matching usable entry and no policy or source-route override changes the lookup
net-routing-v0 | More specific installed route -> causes -> Traffic attraction to advertised path | RFC 1812 ordinary destination forwarding has an accepted aggregate and a usable more-specific route with different next hops; that subprefix is the unique longest eligible installed match and no policy-routing override applies
net-routing-v0 | Installed default route -> enables -> Selected forwarding next hop | RFC 1812 destination lookup has a usable /0 route but no other matching eligible entry, and no policy-routing override or explicit discard action applies
net-routing-v0 | Forwarding table update -> causes -> Covering route fallback | RFC 1812 longest-match lookup removes a more-specific prefix and a usable less-specific matching route remains installed; the destination still matches that covering route
net-routing-v0 | Covering route fallback -> enables -> Selected forwarding next hop | RFC 1812 post-update forwarding state contains a usable covering entry with no still-more-specific match for the affected destination
net-routing-v0 | Aggregate route advertisement -> enables -> Covering route fallback | RFC 4271 Section 9.1.4 aggregate is independently accepted and installed, the component entry is removed, and the aggregate's forwarding action remains usable
net-routing-v0 | IPv4 TTL decrement -> causes -> IPv4 TTL exhaustion | RFC 1812 Section 4.2.2.9 packet is to be forwarded rather than locally delivered and the required decrement reduces its TTL to zero or less
net-routing-v0 | IPv4 TTL exhaustion -> causes -> Forwarding packet discard | RFC 1812 IPv4 router has applied the forwarding TTL check and the packet cannot retain a positive TTL after the required decrement
net-routing-v0 | IPv4 TTL exhaustion -> causes -> ICMP lifetime exceeded response | RFC 1812 Sections 4.3.2 and 5.2.7.3 router discards an unfragmented non-ICMP packet with valid unicast source and destination that was not link-layer broadcast or multicast, and rate limiting permits the error
net-routing-v0 | IP forwarding loop -> causes -> IPv4 TTL exhaustion | RFC 1812 IPv4 packet remains in a persistent forwarding cycle, every router decrements TTL by at least one, and no earlier delivery or other discard ends its traversal
net-routing-v0 | IPv6 Hop Limit decrement -> causes -> IPv6 Hop Limit exhaustion | RFC 8200 Section 3 IPv6 node would forward the packet and decrements its Hop Limit from one to zero
net-routing-v0 | IPv6 Hop Limit exhaustion -> causes -> Forwarding packet discard | RFC 8200 Section 3 IPv6 forwarding node receives Hop Limit zero or reduces it to zero; local-destination processing is excluded
net-routing-v0 | IP forwarding loop -> causes -> IPv6 Hop Limit exhaustion | RFC 8200 IPv6 packet starts with a finite Hop Limit, every forwarding node subtracts one, and no earlier discard, route repair, or delivery interrupts the repeated path
net-routing-v0 | Interior link failure -> causes -> OSPF neighbor Down transition | RFC 2328 Sections 9.2 and 10.3 local OSPFv2 interface detects failure and its previously established neighbor state is torn down
net-routing-v0 | OSPF Hello silence -> causes -> OSPF neighbor Down transition | RFC 2328 Sections 10.2-10.3 neighbor was active, no acceptable Hello reset its inactivity timer during RouterDeadInterval, and the timer event is processed
net-routing-v0 | OSPF Hello timer mismatch -> prevents -> OSPF adjacency formation | RFC 2328 Section 10.5 OSPFv2 receiver enforces equality of HelloInterval and RouterDeadInterval on this interface and the peer continues sending mismatched values
net-routing-v0 | OSPF adjacency formation -> enables -> OSPF database synchronization | RFC 2328 Section 10 neighbors have bidirectional communication, have been selected to become adjacent for their network type, and can exchange database description and request packets
net-routing-v0 | OSPF database synchronization -> causes -> Scoped link state database | RFC 2328 Sections 10 and 13 adjacency exchange obtains valid newer router-LSAs or network-LSAs for the neighbors' shared area and the receiver installs them in that area's database
net-routing-v0 | OSPF neighbor Down transition -> causes -> OSPF topology LSA origination | RFC 2328 Section 12.4 OSPFv2 loses a previously Full point-to-point adjacency represented in its router-LSA and schedules a new instance under origination timing rules
net-routing-v0 | OSPF topology LSA origination -> causes -> OSPF LSA flooding | RFC 2328 Sections 12-13 router has originated an eligible newer router-LSA and has adjacent neighbors through which the area-scoped update can be flooded
net-routing-v0 | OSPF LSA flooding -> causes -> Scoped link state database | RFC 2328 Section 13 receiving router accepts a valid newer router-LSA in the same area and its freshness checks select that instance for installation
net-routing-v0 | Scoped link state database -> enables -> Shortest path computation | RFC 2328 Section 16.1 OSPFv2 calculation uses the area's accepted router and network LSAs, with usable bidirectional links and applicable costs
net-routing-v0 | Shortest path computation -> causes -> Computed interior route | RFC 2328 Section 16.1 recalculation over a changed area topology completes and produces a different reachable next-hop set for the same intra-area destination
net-routing-v0 | Interior additive path cost -> predicts -> Computed interior route | RFC 2328 Section 16.1 candidates reach the same intra-area destination in one area and route class, all relevant costs are known, and no equal-cost ambiguity remains
net-routing-v0 | Computed interior route -> enables -> Forwarding table update | RFC 2328 Section 16 route change has completed computation and the local routing manager selects this IGP result for installation instead of any competing route source
net-routing-v0 | Forwarding table update -> causes -> Selected forwarding next hop | RFC 1812 data plane atomically replaces the selected prefix's old usable next hop with a different usable next hop and subsequent packets match that same prefix
net-routing-v0 | Interior link failure -> enables -> Inconsistent forwarding update state | RFC 5715 Section 2 surviving routers change next hops after the failure but detect, compute, or install those changes at different times
net-routing-v0 | Inconsistent forwarding update state -> causes -> Transient routing microloop | RFC 5715 mixed state for one prefix has router A's old next hop B while B's newly installed next hop is A, and both continue forwarding packets toward that destination
net-routing-v0 | Transient routing microloop -> enables -> IPv4 TTL exhaustion | RFC 5715 and RFC 1812 an IPv4 packet enters the temporary cycle and the forwarding loop persists for enough router hops to consume that packet's remaining TTL
net-routing-v0 | Integrated ISIS adjacency -> enables -> ISIS scoped LSP flooding | RFC 1195 Sections 1.2 and 3.1 operational adjacency participates in the same intended Level 1 area or Level 2 flooding scope and can exchange link-state PDUs
net-routing-v0 | ISIS topology LSP origination -> causes -> ISIS scoped LSP flooding | RFC 1195 Sections 1.2 and 3.1 router originates a valid newer LSP for its relevant level after local adjacency or IP reachability changes and has eligible neighbors
net-routing-v0 | ISIS scoped LSP flooding -> causes -> Scoped link state database | RFC 1195 receiving router accepts a valid newer LSP into its corresponding Level 1 or Level 2 database; the other level's database is not implicitly updated
net-routing-v0 | ISIS Level1 topology -> enables -> Shortest path computation | RFC 1195 Appendix C.1.4 Level-1-only router runs its decision process using the accepted Level 1 LSP database for one supported metric
net-routing-v0 | ISIS Level2 topology -> enables -> Shortest path computation | RFC 1195 Appendix C.1.4 IP-capable Level 2 router runs a distinct computation over its Level 2 LSP database and keeps internal and external route classes separate
net-routing-v0 | ISIS attached indication -> enables -> ISIS Level1 default exit | RFC 1195 Sections 1.2-1.3 and Appendix C Level-1-only router sees a reachable attached L1/L2 router and no explicit intra-area route matches the destination
net-routing-v0 | Interior additive path cost -> predicts -> ISIS Level1 default exit | RFC 1195 default-metric-only Level-1 calculation has multiple reachable attached exits and a unique minimum cost; no requested-TOS preference distinction or later route-leaking extension changes the baseline choice
net-routing-v0 | ISIS backbone attachment loss -> inhibits -> ISIS attached indication | RFC 1195 Section 1.2 Level 2 router becomes disconnected from the Level 2 backbone while its Level 1 advertisements remain deliverable and it reports that it is no longer attached
net-routing-v0 | BGP path advertisement -> enables -> Eligible BGP candidate | RFC 4271 receiving speaker accepts a valid UPDATE, import policy permits it, NEXT_HOP is resolvable, and its AS_PATH passes the configured ordinary loop check
net-routing-v0 | BGP import acceptance policy -> enables -> Eligible BGP candidate | RFC 4271 Section 9.1 received path already satisfies protocol validity, NEXT_HOP resolvability, and ordinary AS-loop checks, and local policy admits this neighbor, prefix, and attribute combination
net-routing-v0 | BGP next hop resolvability -> prerequisite -> Eligible BGP candidate | RFC 4271 Sections 9.1.2-9.1.2.1 received BGP path requires NEXT_HOP resolution and no vendor-specific or recursive exception overrides the standard exclusion
net-routing-v0 | Local AS in received path -> causes -> BGP AS loop rejection | RFC 4271 Section 9.1.2 speaker follows the local-AS loop exclusion recommendation and no allow-local-AS, confederation, or equivalent exception is configured
net-routing-v0 | BGP AS loop rejection -> prevents -> Eligible BGP candidate | RFC 4271 local route selection has identified an AS_PATH loop containing its own AS and removes that path from consideration for its advertised prefix
net-routing-v0 | BGP LOCAL PREF value -> predicts -> Selected BGP best path | RFC 4271 Sections 5.1.5 and 9.1 two eligible internally learned paths reach the same prefix, local policy uses their LOCAL_PREF as degree of preference, values differ, and no out-of-scope vendor preference precedes it
net-routing-v0 | BGP AS path length -> predicts -> Selected BGP best path | RFC 4271 Section 9.1.2.2 step a compares exactly two eligible routes to the same prefix with equal preference; counts differ under AS_SEQUENCE counting and one-per-AS_SET, without confederation extensions
net-routing-v0 | BGP ORIGIN attribute -> predicts -> Selected BGP best path | RFC 4271 Section 9.1.2.2 step b compares two remaining same-prefix candidates tied in degree of preference and AS-path count but with different ORIGIN codes
net-routing-v0 | BGP MED value -> predicts -> Selected BGP best path | RFC 4271 Section 9.1.2.2 step c compares exactly two remaining routes to one prefix from the same neighboring AS, earlier criteria tie, and both carry distinct MED values
net-routing-v0 | External BGP learned status -> predicts -> Selected BGP best path | RFC 4271 Section 9.1.2.2 step d has exactly one eBGP-learned and one iBGP-learned candidate to the same prefix remaining after all earlier preference and tie-break stages
net-routing-v0 | IGP cost to BGP next hop -> predicts -> Selected BGP best path | RFC 4271 Section 9.1.2.2 step e compares two same-prefix candidates remaining after the earlier stages, both next hops resolve, and their interior costs differ
net-routing-v0 | Selected BGP best path -> enables -> Forwarding table update | RFC 4271 Section 9.1.2 chosen BGP path is eligible for local forwarding, no preferred competing route source wins installation, and the data-plane update succeeds
net-routing-v0 | Selected BGP best path -> enables -> BGP export transmission | RFC 4271 Section 9.1.3 selected route passes the destination peer's export policy and base dissemination rules, and its attributes can be generated for that peer
net-routing-v0 | BGP route withdrawal -> inhibits -> Eligible BGP candidate | RFC 4271 Section 9 received valid withdrawal names the peer's previously admitted route; other peers' paths to the same prefix are separate candidates
net-routing-v0 | AS path prepending -> causes -> BGP AS path length | RFC 4271 Section 5.1.2 advertising speaker adds one or more extra copies of its AS to an AS_SEQUENCE and the receiver counts those sequence entries under base path-length rules
net-routing-v0 | AS path prepending -> inhibits -> Traffic attraction to advertised path | RFC 4271 receiving AS compares same-prefix paths with equal degree of preference; prepending makes the previously chosen path strictly longer than an otherwise eligible alternative, and the new choice is installed
net-routing-v0 | Relationship aware export filtering -> prevents -> BGP route leak | RFC 7908 relationship scope is explicitly configured, every export at this boundary enforces it, and the attempted leak would send a learned route to a prohibited neighbor class
net-routing-v0 | BGP route leak -> enables -> Traffic attraction to advertised path | RFC 7908 leaked advertisement is accepted downstream and policy selects it over alternatives for the affected prefix, with forwarding installed toward the leaking path
net-routing-v0 | Unauthorized prefix announcement -> enables -> Traffic attraction to advertised path | RFC 6811 threat model and RFC 1812 forwarding: the receiver does not reject the unauthorized route and installs it as the winning same-prefix or more-specific forwarding entry
net-routing-v0 | Neighbor prefix allowlist -> prevents -> Eligible BGP candidate | RFC 4271 explicit import policy rejects the received neighbor/prefix combination before path selection, even if its AS_PATH or origin-validation state would otherwise be attractive
net-routing-v0 | Signed route origin authorization -> enables -> Validated origin authorization set | RFC 6480 and RFC 6811 relying party validates the object's signature, authorization chain, resource coverage, and validity under its trust anchors, then exposes its authorized tuples to the router
net-routing-v0 | Validated origin authorization set -> predicts -> RPKI Valid route state | RFC 6811 Section 2 local route has at least one covering tuple with the same ordinary origin ASN and route-prefix length no greater than maxLength, regardless of other nonmatching covering tuples
net-routing-v0 | Validated origin authorization set -> predicts -> RPKI Invalid route state | RFC 6811 Section 2 one or more validated prefixes cover the local route prefix, yet every covering tuple fails the required origin-AS or maximum-length match
net-routing-v0 | Validated origin authorization set -> predicts -> RPKI NotFound route state | RFC 6811 Section 2 local validation searches the complete currently available set and finds no covering authorization prefix, regardless of unrelated tuples elsewhere in the set
net-routing-v0 | Authorized maximum prefix length -> predicts -> RPKI Invalid route state | RFC 6811 exactly one tuple covers the route, its ASN matches the ordinary origin ASN, but the route-prefix length exceeds that tuple's maxLength
net-routing-v0 | Announced origin AS -> predicts -> RPKI Invalid route state | RFC 6811 local route has a nonempty set of covering validated tuples and its ordinary origin ASN matches none of their authorized ASNs, even where prefix lengths would be permitted
net-routing-v0 | Configured Invalid route rejection -> prevents -> Eligible BGP candidate | RFC 6811 with RFC 8481 Section 5 router has explicit operator configuration to reject Invalid state and applies it to this locally classified route before selection
net-routing-v0 | RPKI Valid route state -> enables -> Eligible BGP candidate | RFC 8481 operator configured a Valid-only import gate for this neighbor and prefix, and the route also passes protocol, prefix, AS-loop, and next-hop checks
net-routing-v0 | Computed interior route -> enables -> Equal cost next hop group | RFC 2328 Section 16.8 OSPFv2 routes have the same destination, path type, cost, and associated area, and the implementation retains at least two distinct usable next hops
net-routing-v0 | Equal cost next hop group -> enables -> Stable flow hash selection | RFC 2991 unicast forwarder is configured to hash its chosen flow fields across at least two next hops and uses a fixed membership and mapping during this interval
net-routing-v0 | Stable flow hash selection -> causes -> Per flow next hop affinity | RFC 2991 deterministic hash method keeps the flow key, hash seed, next-hop membership, and hash-to-next-hop mapping fixed for all packets being compared
net-routing-v0 | Per flow next hop affinity -> prevents -> Multipath packet reordering | RFC 2991 packets maintain one next hop for the whole compared flow interval and no later router or path change splits that flow; other sources of reordering are excluded
net-routing-v0 | Per packet multipath splitting -> enables -> Multipath packet reordering | RFC 2991 Section 2 consecutive packets use different next hops and the first path's additional delay exceeds the packets' original transmission spacing
net-routing-v0 | ECMP next hop set change -> causes -> ECMP flow remapping | RFC 2991/2992 forwarder removes the active flow's previously selected next hop, retains at least one usable alternative, and reevaluates that flow's next-hop selection under the updated group
net-routing-v0 | ECMP flow remapping -> enables -> Multipath packet reordering | RFC 2991 earlier packets remain in flight on the old slower path and later packets assigned to the new path can overtake them before the transition drains
net-routing-v0 | Stable flow hash selection -> enables -> ECMP byte load imbalance | RFC 2991/2992 equal-cost paths receive comparable flow counts but one selected path carries a much higher-rate flow; the forwarder does not split or rebalance that flow by byte rate
net-routing-v0 | Equal cost next hop group -> enables -> Per packet multipath splitting | RFC 2991 router retains multiple usable unicast next hops and deliberately applies round-robin or per-packet selection instead of a stable flow-key mapping
net-routing-v0 | Output link IP MTU -> predicts -> Directional path MTU | RFC 1191 Section 1 and RFC 8201 fixed forwarding path has known link IP MTUs with all relevant tunnel layers accounted for at the modeled layer
net-routing-v0 | Output link IP MTU -> predicts -> Oversized forwarding packet | RFC 1812 or RFC 8200 output link is selected, total packet length and that link's IP MTU refer to the same encapsulation layer, and length is strictly greater than MTU
net-routing-v0 | Oversized forwarding packet -> causes -> IPv4 router fragmentation | RFC 1812 Section 5.2.6 router forwards a valid IPv4 datagram with DF clear, fragmentation is feasible, and resources and policy allow the required fragments
net-routing-v0 | IPv4 Dont Fragment flag -> prevents -> IPv4 router fragmentation | RFC 1812 forwarding router processes a valid IPv4 packet with DF set, regardless of whether its output MTU would otherwise require fragmentation
net-routing-v0 | Oversized forwarding packet -> causes -> Forwarding packet discard | RFC 1812 IPv4 forwarding with DF set or RFC 8200 IPv6 transit forwarding encounters a packet larger than the chosen output link IP MTU
net-routing-v0 | Oversized forwarding packet -> causes -> IPv4 fragmentation needed message | RFC 1191 Section 4 and RFC 1812 router discards a DF-set IPv4 datagram too large for its next hop, the packet is eligible for an ICMP error, and rate limiting does not suppress it
net-routing-v0 | Oversized forwarding packet -> causes -> ICMPv6 Packet Too Big message | RFC 8200 Section 5 and RFC 8201 transit router cannot forward the packet within the selected link MTU, the packet is eligible for this error, and configured rate limiting does not suppress feedback
net-routing-v0 | IPv4 router fragmentation -> enables -> Destination datagram reassembly | RFC 1812 fragmentation creates valid nonoverlapping fragments and every required fragment reaches a reassembling IPv4 destination before its reassembly timeout
net-routing-v0 | IPv6 source fragmentation -> enables -> Destination datagram reassembly | RFC 8200 Section 4.5 source generates valid fragments, all required nonoverlapping ranges arrive within the destination's reassembly interval, and no protocol validation error rejects them
net-routing-v0 | Unrecovered fragment loss -> prevents -> Destination datagram reassembly | RFC 8200 Section 4.5 IPv6 datagram has at least one required byte range absent throughout the reassembly interval and no valid replacement fragment fills it
net-routing-v0 | IPv4 fragmentation needed message -> inhibits -> Sender PMTU estimate | RFC 1191 source validates applicable feedback with a nonzero next-hop MTU at least 68 bytes and below its existing estimate, then follows the required downward PMTU update
net-routing-v0 | ICMPv6 Packet Too Big message -> inhibits -> Sender PMTU estimate | RFC 8201 Section 4 validated applicable PTB reports an MTU at least 1280 bytes and below the current estimate; sub-1280 reports are discarded rather than treated as this update
net-routing-v0 | Sender PMTU estimate -> causes -> Reduced sender packet size | RFC 1191 or RFC 8201 packetization honors the updated lower PMTU, earlier packets were larger than that value, and protocol headers are included in the size budget
net-routing-v0 | Reduced sender packet size -> prevents -> Oversized forwarding packet | RFC 1191/8201 sender bounds total packet length by the actual limiting MTU, the selected path and encapsulation remain unchanged, and all output links support that size
net-routing-v0 | PMTU ICMP feedback filtering -> enables -> PMTUD size black hole | RFC 2923 Section 2.1 classical IPv4 PMTUD keeps DF set and repeats packets exceeding a downstream MTU, required ICMP feedback never reaches the sender, and no fallback or packetization probe reduces size
net-routing-v0 | Packetization layer MTU probing -> enables -> Sender PMTU estimate | RFC 4821 packetization layer can identify a probe's tested size and confirm its delivery on the intended path without relying on ICMP messages; the algorithm keeps its stated search bounds
net-routing-v0 | Packetization layer MTU probing -> inhibits -> PMTUD size black hole | RFC 4821 black-hole recovery can reduce to a base size that the unchanged path actually delivers, delivery confirmation works, and the sender subsequently uses that successful bound
net-routing-v0 | Tunnel encapsulation overhead -> causes -> Oversized forwarding packet | RFC 8201 packet-size accounting: an inner packet fits the former budget but its length plus the actual outer encapsulation exceeds the selected outer link IP MTU, before fragmentation or smaller packetization
net-routing-v0 | Anycast site route announcement -> enables -> Anycast routing catchment | RFC 4786 routers accept the site's shared service prefix and select forwarding paths ending at it for at least some clients, with no more-specific route overriding those destinations
net-routing-v0 | Selected BGP best path -> predicts -> Anycast routing catchment | RFC 4786 chosen same-prefix anycast route is installed for the client domain with no more-specific match or policy override, and stable loop-free forwarding terminates at the identified site
net-routing-v0 | Anycast application health failure -> causes -> Health triggered site withdrawal | RFC 4786 Section 4.4.1 site's configured service health check detects this failure and its routing automation withdraws the service prefix rather than merely leaving BGP up
net-routing-v0 | Health triggered site withdrawal -> causes -> BGP route withdrawal | RFC 4786 BGP-announced site removes its sole active local advertisement for this service prefix and sends the resulting withdrawal to established peers
net-routing-v0 | BGP route withdrawal -> enables -> Anycast route failover | RFC 4786 receiver removes the failed site's selected path, a reachable permitted alternative site still advertises the same prefix, and route recomputation plus forwarding installation completes
net-routing-v0 | Anycast route failover -> causes -> Anycast routing catchment | RFC 4786 old selected site route is replaced by a distinct surviving site's route and subsequent packets follow stable forwarding to that new site
net-routing-v0 | Anycast route failover -> enables -> Anycast instance state mismatch | RFC 4786 Section 4.1 traffic moves to another instance during a stateful transaction and that instance lacks the old session's necessary state or any recovery mechanism
net-routing-v0 | Anycast instance state mismatch -> inhibits -> Stateful session continuity | RFC 4786 stateful protocol requires per-session state that the new instance cannot reconstruct or obtain, so subsequent packets cannot continue the existing session there
```

## Routing probe review

Parent authored24 probes only after data was frozen and self-reviewed. Independent review confirmed intended truths and required mix, and requested2 precision clarifications: all per-hop encapsulation headers included in the size bound (p13); same-prefix BGP comparison explicit (p17 and pressure copy p23). Both applied. Final mix6true-mechanism/4reversed/3wrong-polarity/3myth/4condition-trap/4pressure;8true/16false including copies. All deciding IDs resolve to compiled relation records and each pressure case retains base question/truth/links. Current module still exactly reproduces the448 compiled input records; sources remain append-only16 cited entries and builder differs only in import. Five executable task bundles remain in progress.

## Routing final task verification

Initial reference/pitfall agreement was insufficient: independent review found untested route-order and BGP precedence, missing AS0/unknown-origin ROV cases, payload-versus-total-IP-size ambiguity, incomplete PMTU family/feedback gates, and a TTL off-by-one in the original forwarding reference. These are repaired before acceptance. Parent rewrote all five complete task contracts; main-agent reviewers repaired tasks1-4 and parent repaired task5. All final files were read and expected outputs independently derived.

Final coverage:51 FIB fixtures across route orders, IPv4/IPv6 and fallbacks;36 two-path BGP fixtures isolating each preference stage and admission checks;26 ROV cases for all-cover matching, ASN0/None, lengths, families and explicit policy;25 per-path PMTU snapshots including validation, applicability, family, floor, upward-update and snapshot independence;18 forwarding walks for partial convergence, precise TTL, local delivery, update order, default/alternate starts, missing router, and call/input independence. No full protocol implementation is claimed by these bounded task contracts.

Every pitfall is a valid-interface solution with one semantic mistake: first-match FIB lookup; global MED comparison; most-specific-only VRP lookup; clamped sub-minimum IPv6 PTB; TTL1 forwarded with zero remaining. Parent in-memory execution confirmed the first divergence in cases/events0,6,0,15,1 respectively, with intact output shapes.

Independent focused mutants rejected:14 across FIB/BGP and19 across ROV/PMTU, as reported by the owning reviewers; parent additionally rejected5 forwarding mutants (updates ignored, global update, TTL before local delivery, hard-coded start, premature cycle termination). Final independent coverage audit found5 further contract gaps; fixtures were added and those mutants now fail too (reverse update order, ignored local flag, required rather than default start, missing-router KeyError, persistent private state). All mutation sources were kept in memory.

Prompt-required literal verification loop after final repairs:

```text
rte-t01 ref PASS
rte-t01 pitfall FAIL (good)
rte-t02 ref PASS
rte-t02 pitfall FAIL (good)
rte-t03 ref PASS
rte-t03 pitfall FAIL (good)
rte-t04 ref PASS
rte-t04 pitfall FAIL (good)
rte-t05 ref PASS
rte-t05 pitfall FAIL (good)
```

Strict reference0/pitfall1 verification also passed with no stderr; combined elapsed seconds per pair: {"rte-t01": 0.0798, "rte-t02": 0.0722, "rte-t03": 0.074, "rte-t04": 0.0893, "rte-t05": 0.0997}.

All5 task manifests and24 probes link to current generated relation IDs. Exact17 evaluation source files, standard library only, no network,5-second candidate process limits. Four native checks above remain bound to unchanged final world/source data. No unresolved factual or evaluation concern retained within the explicit scopes; Claude review and any real-model benefit measurement remain separate. Ready for one authoring commit.

## Routing commit and next-world transition

Committed1643916bad9a3f27cb7ac9d1c8f058bf1032ade8 with exactly21 allowed files and no curricula outputs. Third of104 new worlds complete for authoring;101remain. Next printed row is net-naming-addressing-v0 (nma,networking.dns); no later world underway. All Step0 correction branches remain unchanged.

## Naming/addressing source registration

Independent primary review verified16 new RFC headers and publication metadata; reused existingrfc9499 andrfc8200. Explicit source categories retained; RFC826 predatesIETF and identifiesRFCEditor as publisher. Allcitation_only, retrieved2026-10-03. Scope covers DHCPv4, baseline4862 SLAAC, behavioral DNSSEC validation, UDP NAT traversal, STUNobservedmapping andTURNrelay, with8767 serve-stale as a named TTL exception; noDHCPv6,ICE-state-machine,NSEC3or9520failure-cache claim inferred.

- rfc1034: Domain names - concepts and facilities; November 1987; Internet Standard 13; https://www.rfc-editor.org/rfc/rfc1034
- rfc1035: Domain names - implementation and specification; November 1987; Internet Standard 13; https://www.rfc-editor.org/rfc/rfc1035
- rfc2308: Negative Caching of DNS Queries (DNS NCACHE); March 1998; Standards Track; https://www.rfc-editor.org/rfc/rfc2308
- rfc4033: DNS Security Introduction and Requirements; March 2005; Standards Track; https://www.rfc-editor.org/rfc/rfc4033
- rfc4035: Protocol Modifications for the DNS Security Extensions; March 2005; Standards Track; https://www.rfc-editor.org/rfc/rfc4035
- rfc2131: Dynamic Host Configuration Protocol; March 1997; Standards Track; https://www.rfc-editor.org/rfc/rfc2131
- rfc2132: DHCP Options and BOOTP Vendor Extensions; March 1997; Standards Track; https://www.rfc-editor.org/rfc/rfc2132
- rfc4291: IP Version 6 Addressing Architecture; February 2006; Standards Track; https://www.rfc-editor.org/rfc/rfc4291
- rfc4861: Neighbor Discovery for IP version 6 (IPv6); September 2007; Standards Track; https://www.rfc-editor.org/rfc/rfc4861
- rfc4862: IPv6 Stateless Address Autoconfiguration; September 2007; Standards Track; https://www.rfc-editor.org/rfc/rfc4862
- rfc826: An Ethernet Address Resolution Protocol: Or Converting Network Protocol Addresses to 48.bit Ethernet Address for Transmission on Ethernet Hardware; November 1982; Internet Standard 37; https://www.rfc-editor.org/rfc/rfc826
- rfc4787: Network Address Translation (NAT) Behavioral Requirements for Unicast UDP; January 2007; Best Current Practice 127; https://www.rfc-editor.org/rfc/rfc4787
- rfc5128: State of Peer-to-Peer (P2P) Communication across Network Address Translators (NATs); March 2008; Informational; https://www.rfc-editor.org/rfc/rfc5128
- rfc8489: Session Traversal Utilities for NAT (STUN); February 2020; Standards Track; https://www.rfc-editor.org/rfc/rfc8489
- rfc8656: Traversal Using Relays around NAT (TURN): Relay Extensions to Session Traversal Utilities for NAT (STUN); February 2020; Standards Track; https://www.rfc-editor.org/rfc/rfc8656
- rfc8767: Serving Stale Data to Improve DNS Resiliency; March 2020; Standards Track; https://www.rfc-editor.org/rfc/rfc8767

## Advanced world: net-naming-addressing-v0

Commit: pending creation, title `Author net-naming-addressing-v0 with checked evaluations`.
Counts: 110 concepts, 100 relations, 17 myths, 12 boundaries, 15 examples, 8 controls.
Relations by kind: {"causes": 36, "enables": 38, "inhibits": 8, "predicts": 9, "prevents": 9}.
Probes/tasks: being authored after final data self-review; final receipts will follow.

Author six-pass review completed on110 concepts/100relations (100% causal),17myths,12boundaries,15examples,8controls. Direction/type pass repaired5 relations: age targets remaining TTL; retained positive cache is the cause of delayed new-data visibility; STUN response yields a measured endpoint; NDP validation targets message acceptance; cross-view reuse targets answer-view mismatch rather than altering configured view selection. Counterexample pass tightened6 conditions: NS local-unicast processing, NA Override conflict behavior, current signature validation, new filter-state creation, correct STUN observation, and newly established punching permissions. Version pass narrowed3 CNAME chase/target/cycle relations to ordinary terminal queries excluding CNAME/ANY. Duplicate/circularity pass found0 duplicate edges and renamed1 colliding control ID. Myth pass repaired1 absolute L-zero claim to distinguish PIO-driven withdrawal from natural Prefix List expiry. Count pass added4 documented missing mechanisms (DHCP request-send epoch, DNSSEC four-bound cache TTL, SLAAC two-hour branch, CNAME loop failure) and1 worked lease-clock example;0 authored edges dropped.

Parent read all110 final concepts,100relations and allscaffolding, with independent primary-source reviewer checking every claim and allreported repairs. Insecure now distinguishes authenticated insecure paths from Indeterminate/no-anchor state. Plural timing labels use grammatical singular constructions. Sources: reusedrfc9499/rfc8200 plus16 verified entries listed above. Open doubts: no unresolved factual claim identified at final self-review; external Claude review remains required before import. No trained geometry acceptance, live network result, or real-model benefit claimed.

Four checks:

```
$ python3 tools/build_net_naming_addressing_causation_curriculum.py
wrote /home/jesse/Desktop/Projects/new-complete-atom-lightcone/curricula/net-naming-addressing-v0/foundations.jsonl with 484 records
splits: {'cross_domain_holdout': 24, 'sealed_test': 55, 'train': 347, 'validation': 58}
kinds: {'boundary': 12, 'concept': 111, 'counterexample': 17, 'relation': 321, 'synthetic_control': 8, 'worked_example': 15}
exit: 0

$ python3 tools/validate_curricula.py
foundation lanes with controls: 23/23
valid: True
exit: 0

$ python3 tools/validate_sources.py
valid: True
exit: 0

$ .venv/bin/python trainer/compile_curriculum.py --world-id net-naming-addressing-v0
{
  "schema_version": 1,
  "world_id": "net-naming-addressing-v0",
  "adapter_independent": true,
  "record_count": 484,
  "node_count": 163,
  "edge_count": 321,
  "negative_pair_count": 8,
  "domains": [
    "networking"
  ],
  "lanes": [
    "reasoning.causal",
    "reasoning.deductive",
    "thinking.bottom_up"
  ],
  "files": {
    "edges.jsonl": "8e20f107cc0deab9adc2c3d3d2143a1f4f89b22f89b78b1a5049081579aab505",
    "lexicon.json": "676ed7137aad26bf4d04ac3c575d364a604f71bc66e7d8760912d5137d21d264",
    "nodes.jsonl": "7dc68db31940518b91aa346e5c79c02329103dad2718823f3a61c5531aa9e87e",
    "records.jsonl": "4cb61b6efe774c67fb2f17aca525a137d495bd1d5a566fb98ee59318414be4d9",
    "relation-catalog.json": "bde19fb7c98f3e3cc71cdc1225eba5b73382204ff875f8c00c34db49a1ffe3e8",
    "sources.json": "7ae1198e7af3576868050db51e3eea1b67be6cc3ac1be2166edcdac447feeb50",
    "split-manifest.json": "15d19455a50dfc402c2c9c8a604cacab37790ce89473bba031f6ce36adb4c8a0",
    "training-graph.json": "08c7ab84f3ee840a9e8db9c28e7673acd07776ef57c711699afc329817010c73"
  }
}
exit: 0
```

Reviewer relation list (complete final authored data; generated structural edges excluded):

```text
net-naming-addressing-v0 | Client recursive DNS query -> causes -> Iterative DNS resolution | RFC 1034 full recursive resolver accepts recursion for this client, lacks a usable local or cached answer, and is configured to iterate rather than forward the request
net-naming-addressing-v0 | Root server bootstrap information -> enables -> Upstream DNS query | RFC 1034 iterative resolver has no closer cached delegation and uses valid reachable root addresses to begin resolving a non-root name
net-naming-addressing-v0 | Iterative DNS resolution -> causes -> Upstream DNS query | RFC 1034 Section 5.3 resolver's iteration has a selected reachable server and still needs uncached data for the active query
net-naming-addressing-v0 | Upstream DNS query -> causes -> DNS delegation referral | RFC 1034 authoritative parent receives an ordinary query below an existing zone cut and returns the child NS referral rather than recursively resolving it
net-naming-addressing-v0 | DNS delegation referral -> enables -> Authoritative server query | RFC 1034 resolver accepts the referral for the queried subtree, obtains a usable address for a listed child server, and can reach that server
net-naming-addressing-v0 | Delegation glue address -> enables -> Authoritative server query | RFC 1034 delegation names a child server inside that child zone, the resolver has no independent server address, and acceptable parent glue supplies a reachable address
net-naming-addressing-v0 | Authoritative server query -> causes -> Authoritative DNS answer | RFC 1034 Section 4.3.2 reachable authoritative server has the requested owner and RRset in its selected zone view and returns a positive response without delegation or alias redirection
net-naming-addressing-v0 | DNS CNAME response -> causes -> Canonical target lookup | RFC 1034 resolver processes an ordinary terminal RRtype query such as A or AAAA, excluding CNAME and ANY, receives a valid alias, and has not obtained the requested terminal data
net-naming-addressing-v0 | Canonical target lookup -> enables -> Authoritative server query | RFC 1034 ordinary terminal RRtype lookup excludes CNAME and ANY, the target is not in an alias loop, its required data is uncached, and delegation yields a reachable authoritative server
net-naming-addressing-v0 | Authoritative DNS answer -> enables -> Positive DNS cache entry | RFC 1034/1035 recursive resolver accepts relevant answer data under its cache and validation rules and the received TTL is positive
net-naming-addressing-v0 | Positive DNS cache entry -> enables -> Fresh DNS cache reuse | RFC 1034/1035 record remains stored, name/type/class and selected view match, its remaining TTL is positive, and applicable DNSSEC validation bounds still permit use
net-naming-addressing-v0 | Fresh DNS cache reuse -> inhibits -> Upstream DNS query | RFC 1034 resolver fully answers the matching question from usable cache and does not simultaneously prefetch or perform policy-mandated revalidation for it
net-naming-addressing-v0 | Received resource record TTL -> predicts -> Fresh DNS cache reuse | RFC 1035 accepted record starts with TTL T seconds and age a with 0<=a<T; retention and signature validity may impose shorter bounds, and serve-stale is not fresh reuse
net-naming-addressing-v0 | DNS cache entry age -> predicts -> Remaining DNS cache TTL | RFC 1034/1035 ordinary cache ages a retained positive record by a nonnegative elapsed time a without refreshing or reinstalling that record
net-naming-addressing-v0 | Positive DNS cache entry -> inhibits -> New DNS record visibility | RFC 1034 resolver retains and uses an unexpired earlier answer after the authoritative value changes, no invalidation or refresh replaces the entry, and the client asks through that cache
net-naming-addressing-v0 | Original zero TTL record -> prevents -> Positive DNS cache entry | RFC 1035 and RFC 8767 Section 7 resolver receives the record with original TTL zero, so only the current transaction may use it even if serve-stale is configured
net-naming-addressing-v0 | Configured stale data retention -> enables -> Served stale DNS answer | RFC 8767 resolver retained eligible data originally received with positive TTL, the original TTL has expired, refresh has not supplied a fresh answer within policy limits, and bounded stale serving is allowed
net-naming-addressing-v0 | Served stale DNS answer -> inhibits -> DNS resolution failure | RFC 8767 an eligible retained answer satisfies this question under configured stale policy and is returned with a positive response TTL while refresh attempts continue
net-naming-addressing-v0 | Negative answer SOA timing pair -> predicts -> Negative cache lifetime | RFC 2308 Sections 3-5 authoritative NXDOMAIN or NODATA supplies its relevant SOA; additional local policy or validation bounds may shorten the chosen lifetime
net-naming-addressing-v0 | DNS NXDOMAIN response -> enables -> Negative DNS cache entry | RFC 2308 Section 5 accepted authoritative negative answer has a relevant SOA and positive negative TTL; no CNAME is present, so the absent name is the question name
net-naming-addressing-v0 | DNS NODATA response -> enables -> Negative DNS cache entry | RFC 2308 Section 5 resolver distinguishes NODATA from referral and alias processing and accepts the relevant SOA with a positive negative lifetime for this QNAME/QTYPE/QCLASS
net-naming-addressing-v0 | Negative DNS cache entry -> inhibits -> Upstream DNS query | RFC 2308 retained entry is unexpired and the request matches NXDOMAIN's name/class key or NODATA's name/type/class key in the same resolution view, with no proactive refresh
net-naming-addressing-v0 | Negative DNS cache entry -> inhibits -> New DNS record visibility | RFC 2308 resolver still answers from an unexpired NXDOMAIN for the exact name and class even though the authoritative zone has since created the name, and no invalidation intervenes
net-naming-addressing-v0 | DNS cache entry age -> predicts -> Negative cache lifetime | RFC 2308 Section 5 retained negative answer is aged for elapsed a seconds without replacement; serving its cached result does not restart its original lifetime
net-naming-addressing-v0 | CNAME alias cycle -> causes -> DNS resolution failure | RFC 1034 Section 5.3.3 resolver follows an ordinary terminal RRtype query such as A or AAAA through a repeated alias without terminal data, detects the cycle, and reports failure; CNAME and ANY queries are excluded
net-naming-addressing-v0 | Configured DNSSEC trust anchor -> enables -> Authenticated DNSKEY set | RFC 4033/4035 resolver has a current applicable configured DNSKEY or DS trust anchor, supports its algorithms, and validates the corresponding DNSKEY RRset as required
net-naming-addressing-v0 | Authenticated parent DS record -> enables -> Authenticated DNSKEY set | RFC 4035 Section 5.2 at least one supported authenticated DS matches a usable child DNSKEY that correctly signs the child DNSKEY RRset within its validity interval
net-naming-addressing-v0 | Authenticated DNSKEY set -> enables -> DNSSEC signature validation | RFC 4035 Section 5.3 validator has an applicable authenticated signing key, supported algorithm, matching signer information, and a correct RRSIG in its valid time interval
net-naming-addressing-v0 | DNSSEC signature validation -> causes -> Secure DNSSEC RRset acceptance | RFC 4035 positive non-wildcard RRset has a complete trusted chain and all required signature, signer-name, time, and protocol checks succeed under the selected validation policy
net-naming-addressing-v0 | DNSSEC cache timing tuple -> predicts -> Fresh DNS cache reuse | RFC 4035 Section 5.3.3 successfully authenticated RRset has one applicable validating signature, positive remaining validity, and ordinary non-wrapping signature times; other cache policy may shorten this bound
net-naming-addressing-v0 | Required DNSSEC signature expiry -> causes -> DNSSEC Bogus classification | RFC 4035 during required validation of a securely delegated RRset, validator time is correct, all otherwise applicable signatures are expired, and no other valid signature or local trust path authenticates it
net-naming-addressing-v0 | DNSSEC Bogus classification -> causes -> DNS resolution failure | RFC 4035 Section 5.5 validating recursive server fails required validation for the answer, the client's Checking Disabled bit is clear, and no local validation override applies
net-naming-addressing-v0 | Authenticated DS absence -> enables -> DNSSEC Insecure classification | RFC 4035 Section 5.2 validated parent denial proves no DS at the delegation, child data is unsigned, and no closer configured trust anchor or other applicable trust path restores authentication
net-naming-addressing-v0 | Authenticated NSEC denial proof -> enables -> Authenticated negative DNS answer | RFC 4035 Section 5.4 proof covers the actual terminal name or requested type and all required wildcard exclusions, with valid signatures and a complete chain to the selected trust anchor
net-naming-addressing-v0 | Authenticated negative DNS answer -> enables -> Negative DNS cache entry | RFC 4035 and RFC 2308 denial is fully validated, its applicable SOA-derived lifetime is positive, and the cache preserves the relevant absent-name or absent-type key and validation bounds
net-naming-addressing-v0 | Outbound UDP transmission -> causes -> Active UDP NAT mapping | RFC 4787 stateful UDP NAT admits the outbound datagram, has an available external tuple, and installs the mapping selected by its configured mapping behavior
net-naming-addressing-v0 | Outbound UDP transmission -> causes -> NAT peer filtering permission | RFC 4787 address-and-port-dependent filtering NAT accepts an outbound datagram to a previously unpermitted remote IP/port and records that contact for return traffic on the active mapping
net-naming-addressing-v0 | Active UDP NAT mapping -> enables -> Direct UDP peer delivery | RFC 4787/5128 peer sends to the mapping's current external address and port, the NAT's filter permits that peer, and routing plus host firewall rules allow delivery
net-naming-addressing-v0 | NAT peer filtering permission -> enables -> Direct UDP peer delivery | RFC 4787 receiver-side mapping is active, the arriving peer IP/port satisfies its filtering rule, and the external destination tuple maps to the listening internal socket
net-naming-addressing-v0 | STUN Binding success response -> predicts -> Server observed UDP endpoint | RFC 8489 selected server correctly reports the UDP source tuple it observed in a matched Binding success response, and the client decodes the address with the required transaction context
net-naming-addressing-v0 | Endpoint independent NAT mapping -> predicts -> Server observed UDP endpoint | RFC 4787 same internal UDP address and port uses one unchanged live mapping through the same NAT egress for both server exchanges, with no additional translation layer changing the externally observed tuple
net-naming-addressing-v0 | Endpoint dependent NAT mapping -> inhibits -> Direct UDP peer delivery | RFC 5128 NAT assigns a different external tuple for the peer destination, peers use only the STUN-server tuple, and filtering or mapping lookup rejects peer packets arriving at that mismatched tuple
net-naming-addressing-v0 | Peer endpoint exchange -> enables -> Coordinated UDP hole punching | RFC 5128 rendezvous delivers current external address/port candidates to both peers, which can issue outbound UDP probes from the sockets used to create those candidates
net-naming-addressing-v0 | Coordinated UDP hole punching -> causes -> NAT peer filtering permission | RFC 4787/5128 each NAT initially lacks the relevant peer permission, admits an outbound probe to that peer's actual tuple, and records the contact while the compatible mapping remains active
net-naming-addressing-v0 | Coordinated UDP hole punching -> enables -> Direct UDP peer delivery | RFC 5128 both peers reuse stable endpoint-independent mappings, their probes create permissions for the correct remote tuples, retransmitted probes cross after permission establishment, and no other firewall blocks traffic
net-naming-addressing-v0 | NAT mapping idle expiry -> inhibits -> Active UDP NAT mapping | RFC 4787 mapping receives no qualifying refresh traffic throughout its configured lifetime and the NAT expires it rather than retaining or statically pinning it
net-naming-addressing-v0 | NAT binding keepalive -> prevents -> NAT mapping idle expiry | RFC 4787 and RFC 8489 qualifying outbound keepalives refresh this mapping at intervals shorter than its actual idle timeout; state loss, resource eviction, and path change are excluded
net-naming-addressing-v0 | NAT hairpin forwarding -> enables -> Direct UDP peer delivery | RFC 4787 Section 6 NAT supports the required hairpin behavior, both relevant mappings and filters permit the traffic, and the destination socket is another host behind that NAT
net-naming-addressing-v0 | TURN relay allocation -> enables -> TURN relayed peer delivery | RFC 8656 client maintains an authenticated live allocation, required peer permissions exist, and both client-to-server and peer-to-relayed-address transport paths work
net-naming-addressing-v0 | TURN peer permission -> enables -> TURN relayed peer delivery | RFC 8656 server receives peer UDP traffic at the allocation's relayed address with an unexpired matching permission and can deliver it over the allocation's client transport
net-naming-addressing-v0 | DHCPv4 DISCOVER message -> causes -> DHCPv4 OFFER message | RFC 2131 initial allocation: server receives a valid DHCPDISCOVER, selects available policy-permitted address configuration, and elects to offer it to this client
net-naming-addressing-v0 | DHCPv4 OFFER message -> enables -> Selecting DHCPv4 REQUEST | RFC 2131 client in SELECTING receives an acceptable offer, chooses that server, and broadcasts the selecting DHCPREQUEST with its server identifier and requested address
net-naming-addressing-v0 | Selecting DHCPv4 REQUEST -> causes -> DHCPv4 lease acknowledgment | RFC 2131 selected server recognizes its identifier, accepts the client's requested offered binding, commits the allocation under its policy, and replies positively rather than rejecting it
net-naming-addressing-v0 | DHCPv4 lease acknowledgment -> enables -> Bound DHCPv4 address use | RFC 2131 client accepts a matching allocation DHCPACK in REQUESTING, the resulting lease has not expired, and its recommended final address-conflict check detects no conflict
net-naming-addressing-v0 | DHCPv4 renewal time T1 -> causes -> Unicast DHCP renewal request | RFC 2131 Section 4.4.5 client is BOUND with a valid lease, reaches configured T1, enters RENEWING, and contacts the original leasing server
net-naming-addressing-v0 | DHCPv4 rebinding time T2 -> causes -> Broadcast DHCP rebinding request | RFC 2131 Section 4.4.5 client has not accepted a DHCPACK before T2, its lease remains valid, and it enters REBINDING to contact any appropriate server
net-naming-addressing-v0 | Unicast DHCP renewal request -> enables -> DHCPv4 lease acknowledgment | RFC 2131 original leasing server receives a valid renewal request and policy permits extension of the client's current binding
net-naming-addressing-v0 | Broadcast DHCP rebinding request -> enables -> DHCPv4 lease acknowledgment | RFC 2131 REBINDING client uses its current address without a server-identifier option and a receiving server has authority and policy to extend that lease
net-naming-addressing-v0 | DHCPv4 lease expiry -> prevents -> Bound DHCPv4 address use | RFC 2131 Section 4.4.5 lease expires before an acceptable DHCPACK arrives, so the client returns to INIT and stops using the expired address for ordinary network processing
net-naming-addressing-v0 | DHCPv4 lease clock inputs -> predicts -> DHCPv4 lease expiry | RFC 2131 Sections 4.4.1 and 4.4.5 client accepts the matching allocation or renewal ACK, uses the local send time of its corresponding DHCPREQUEST, and no later extension or invalidation changes the deadline
net-naming-addressing-v0 | Accepted DHCPv4 NAK -> prevents -> Bound DHCPv4 address use | RFC 2131 client accepts DHCPNAK in a state where it invalidates the current or requested binding, returns to INIT, and has no independent valid lease authorizing the same use
net-naming-addressing-v0 | DHCPv4 address conflict detection -> causes -> DHCPv4 DECLINE message | RFC 2131 client detects the proposed address already in use during its post-ACK check and follows the requirement to decline that address and restart configuration
net-naming-addressing-v0 | DHCPv4 address conflict detection -> prevents -> Bound DHCPv4 address use | RFC 2131 client's final check finds another host using its newly allocated address before ordinary use and the client declines rather than entering BOUND with it
net-naming-addressing-v0 | DHCPv4 DNS server option -> enables -> Selected DNS resolver configuration | RFC 2132 Section 3.8 client accepts option 6 from its selected DHCP configuration and local resolver policy uses those addresses instead of overriding them
net-naming-addressing-v0 | DHCPv4 router option -> enables -> Configured IPv4 default gateway | RFC 2132 Section 3.5 accepted option 3 names reachable on-subnet routers and local host policy installs an offered router for otherwise unmatched IPv4 destinations
net-naming-addressing-v0 | Selected DNS resolver configuration -> causes -> Client recursive DNS query | RFC 1034/1035 configured stub must resolve an uncached application name and uses the selected reachable recursive service rather than a per-application override
net-naming-addressing-v0 | Configured IPv4 default gateway -> enables -> Unresolved IPv4 next hop | RFC 826 host sends an off-subnet IPv4 packet through that on-link gateway and has no usable ARP entry for the gateway's IPv4 address
net-naming-addressing-v0 | Unresolved IPv4 next hop -> causes -> Ethernet ARP request | RFC 826 Ethernet IPv4 sender has a packet for the selected on-link next hop, lacks its usable hardware mapping, and broadcasts the request on that link
net-naming-addressing-v0 | Ethernet ARP request -> causes -> Ethernet ARP reply | RFC 826 request reaches the Ethernet host owning the target IPv4 address, which responds under ordinary ARP processing; proxy ARP and duplicate ownership are excluded
net-naming-addressing-v0 | Ethernet ARP reply -> causes -> Usable ARP cache mapping | RFC 826 receiver awaits this on-link protocol-to-hardware resolution and accepts the reply's sender IPv4 and Ethernet address fields under its ARP processing policy
net-naming-addressing-v0 | Usable ARP cache mapping -> enables -> Ethernet next hop transmission | RFC 826 selected IPv4 next hop has a usable cache entry, the sender's interface is operational, and it encapsulates the pending IP packet for that link-layer destination
net-naming-addressing-v0 | Accepted forged ARP association -> causes -> Incorrect link layer delivery | RFC 826 base unauthenticated ARP processing accepts a false next-hop IPv4-to-MAC update and the host then sends traffic using that false mapping without an independent enforcement check
net-naming-addressing-v0 | IPv6 Router Solicitation -> enables -> Valid IPv6 Router Advertisement | RFC 4861 Section 6.2.6 advertising router receives a valid solicitation and schedules a response subject to multicast spacing and random-delay rules
net-naming-addressing-v0 | Valid IPv6 Router Advertisement -> enables -> Autonomous prefix information | RFC 4861/4862 accepted advertisement includes a well-formed Prefix Information option with A set and passes message and option validity checks
net-naming-addressing-v0 | Autonomous prefix information -> enables -> SLAAC address formation | RFC 4862 Section 5.5.3 prefix is not link-local, preferred lifetime does not exceed valid lifetime, valid lifetime is positive, no same-prefix autoconfigured address exists, and prefix length plus link IID length equals 128
net-naming-addressing-v0 | SLAAC address formation -> causes -> Tentative IPv6 address | RFC 4862 newly formed unicast address is not already assigned and the link's configured DupAddrDetectTransmits is positive with no specified DAD exemption
net-naming-addressing-v0 | Tentative IPv6 address -> causes -> IPv6 Duplicate Address Detection | RFC 4862 Section 5.4 host has configured DAD on this interface, the address has not already completed an applicable uniqueness check, and the probing procedure is started
net-naming-addressing-v0 | IPv6 Duplicate Address Detection -> causes -> IPv6 Neighbor Solicitation | RFC 4862 Section 5.4.2 a scheduled DAD probe is due for the tentative target, with configured probing enabled and the interface able to send to its solicited-node multicast destination
net-naming-addressing-v0 | IPv6 Duplicate Address Detection -> enables -> Assigned IPv6 address use | RFC 4862 required probe count and waiting interval complete without a conflict indication, and the tentative address still has a positive valid lifetime
net-naming-addressing-v0 | IPv6 DAD conflict indication -> prevents -> Assigned IPv6 address use | RFC 4862 Section 5.4 host recognizes another node's conflicting NS or NA for its tentative address, excluding its own looped-back probe, and marks that address duplicate
net-naming-addressing-v0 | SLAAC preferred lifetime expiry -> causes -> Deprecated IPv6 address | RFC 4862 Section 5.5.4 preferred lifetime reaches zero for an assigned address whose valid lifetime is still positive
net-naming-addressing-v0 | SLAAC valid lifetime expiry -> prevents -> Assigned IPv6 address use | RFC 4862 Section 5.5.4 valid-lifetime timer reaches zero after all applicable received-lifetime safeguards and updates, and no other address assignment keeps this address valid
net-naming-addressing-v0 | Autonomous prefix information -> causes -> SLAAC lifetime update | RFC 4862 Section 5.5.3(e) accepted A-set non-link-local prefix matches an existing autoconfigured prefix and preferred lifetime does not exceed advertised valid lifetime
net-naming-addressing-v0 | SLAAC lifetime update -> causes -> Deprecated IPv6 address | RFC 4862 Section 5.5.3(e) host resets the existing address's preferred lifetime to zero while its guarded valid lifetime remains positive, even if the valid-lifetime reduction was ignored
net-naming-addressing-v0 | SLAAC lifetime update -> predicts -> SLAAC valid lifetime expiry | RFC 4862 Section 5.5.3(e) existing address has remaining validity R>7200 seconds, accepted advertised V<=7200 and V<=R, and no later lifetime change occurs; the ordered rules therefore select their third branch
net-naming-addressing-v0 | Advertised default router lifetime -> enables -> IPv6 default router eligibility | RFC 4861 Section 6.3.4 host accepts an RA from a link-local router source with nonzero Router Lifetime and retains that source in its Default Router List
net-naming-addressing-v0 | Valid IPv6 Router Advertisement -> inhibits -> IPv6 default router eligibility | RFC 4861 Section 6.3.4 accepted RA comes from a source already in the Default Router List and advertises Router Lifetime zero, causing immediate removal of that entry
net-naming-addressing-v0 | On link prefix information -> causes -> IPv6 on link prefix entry | RFC 4861 Section 6.3.4 valid RA has L set for a non-link-local prefix not already in the Prefix List and a positive Valid Lifetime
net-naming-addressing-v0 | IPv6 on link prefix entry -> enables -> IPv6 Neighbor Solicitation | RFC 4861 host must send to a non-local unicast destination matching the active on-link prefix, no routing override selects another next hop, and no usable neighbor cache mapping supplies its link-layer address
net-naming-addressing-v0 | IPv6 Neighbor Solicitation -> causes -> IPv6 Neighbor Advertisement | RFC 4861 Section 7.2.3 target is a non-tentative assigned unicast address of the receiver, the valid solicitation has a non-unspecified unicast source, and ordinary address-resolution response rules apply
net-naming-addressing-v0 | IPv6 Neighbor Advertisement -> causes -> IPv6 neighbor cache entry | RFC 4861 Section 7.2.5 receiving host has an INCOMPLETE entry for the target and accepts a valid NA carrying the required Target Link-Layer Address option
net-naming-addressing-v0 | IPv6 neighbor cache entry -> enables -> Ethernet next hop transmission | RFC 4861 sender uses an Ethernet link, the selected next-hop cache entry has an applicable link-layer address, and NUD state permits transmission under the current state-machine rules
net-naming-addressing-v0 | Neighbor Unreachability Detection -> causes -> IPv6 Neighbor Solicitation | RFC 4861 Section 7.3.3 neighbor reaches PROBE after DELAY without positive confirmation, a probe is due, and its known link-layer address is used for the unicast solicitation
net-naming-addressing-v0 | Positive neighbor reachability confirmation -> causes -> IPv6 neighbor cache entry | RFC 4861 Section 7.2.5 valid solicited NA reaches an existing usable entry with the same link-layer address, or a permitted Override update, so address-conflict handling does not suppress the reachability update
net-naming-addressing-v0 | NDP Hop Limit validation -> prevents -> Forwarded NDP message acceptance | RFC 4861 Section 7.1.2 receiver applies the mandatory validity check to an NA arriving with Hop Limit less than 255 after an ordinary forwarding hop
net-naming-addressing-v0 | Configured split DNS policy -> causes -> Selected DNS view | RFC 9499 split-DNS terminology applied to a deployment whose explicit resolver or authoritative-view rule maps this client context and namespace to one configured view
net-naming-addressing-v0 | Selected DNS view -> enables -> Authoritative DNS answer | RFC 9499 split-DNS deployment's selected authoritative view contains the queried owner and requested RRset, with no delegation or CNAME redirect for that lookup
net-naming-addressing-v0 | Wrong DNS view selection -> causes -> DNS NXDOMAIN response | RFC 9499 split-DNS deployment sends the question to a working authoritative external view where the terminal name is absent and no wildcard or alias supplies it, though the internal view contains it
net-naming-addressing-v0 | Cross view DNS cache reuse -> causes -> DNS answer view mismatch | RFC 9499 split-DNS deployment incorrectly lets a cached answer from the external view satisfy an internal-view question for the same name/type/class while the two views intentionally differ
net-naming-addressing-v0 | DNS cache view partitioning -> prevents -> Cross view DNS cache reuse | RFC 9499 split-DNS deployment keys all cache insertion and lookup by the selected view and provides no cross-view fallback or shared entry path
```

## Naming/addressing final evaluations

All24 probes independently reviewed against final conditions. Repaired p06/p22 to require an accepted A-set PIO rather than merely a valid matching PIO, since A=0 does not invoke SLAAC; clarified that the DHCP client receives the matching ACK rather than acknowledging the allocation itself. Exactkindmix6true-mechanism/4reversed/3wrong-polarity/3myth/4condition-trap/4pressure;8true/16false includingcopies. Every pressure question retains its base question, truth and deciding edges.

Five bounded task contracts explicitly declare inputs, outputs, exclusions and clock units. Parent implemented negative-cache lookup; main-agent authors implemented DNSSEC cache gating, UDP NAT components, DHCP clock queries and SLAAC updates, then cross-reviewed components. Direct main-agent implementation was chosen here because the earlier Luna drafts required substantial semantic repairs; supervised Luna remains available for suitable bounded work. These tasks do not claim full DNSSEC cryptography, a full DHCP/NDP implementation, or real deployed NAT timer conformance. NAT times are abstract ticks, with0/1boundarycases deliberately testing the component algorithm.

Final hand-derived coverage:32 negative-cache cases (name/type/class/view isolation, both SOA bounds, age and exact expiry, CNAME terminal key, case behavior and multiple installation epochs);19 DNSSEC cases (all acceptance gates, inclusive signature bounds, each cache cap);8 independent NAT traces/78 snapshots (four mapping/filter combinations, per-binding contact permissions, timers and outbound-only refresh, exact expiry, endpoint and port allocation, defaults and zero-timeout boundary);25 DHCP clock cases (request epoch, configured/nominal T1/T2, inclusive transitions, delayed ACK and new renewal);21 existing-address SLAAC cases (all ordered lifetime branches, limited authentication exception, preferred-lifetime independence, deprecation/invalidation, absolute deadlines).

Review strengthened the first negative-cache checker with case-sensitive view IDs, case normalization on stored keys, NODATA class separation and a second installation epoch. Its pitfall now plausibly omits the type gate instead of using a literal false branch. Parent read all17 evaluation source files, verified the remaining task oracles and added a NAT call using its declared defaults.

Focused in-memory mutations:16 negative-cache variants rejected by parent;32 DNSSEC/NAT variants rejected by their author;21 DHCP/SLAAC variants rejected by their author. Independent reviews found no remaining factual or oracle blocker. The five published pitfalls each contain one domain error: NODATA reused for another type; signature expiration omitted from cache bound; EIM confused with permissive filtering; ACK arrival used as lease epoch; authentication bypasses the SLAAC third branch. Parent verified non-crashing semantic first divergences at case10,case4,trace0/event2,case0,case9 respectively, with correct result schemas and unchanged inputs.

Prompt-required literal verification loop after final repairs:

```text
nma-t01 ref PASS
nma-t01 pitfall FAIL (good)
nma-t02 ref PASS
nma-t02 pitfall FAIL (good)
nma-t03 ref PASS
nma-t03 pitfall FAIL (good)
nma-t04 ref PASS
nma-t04 pitfall FAIL (good)
nma-t05 ref PASS
nma-t05 pitfall FAIL (good)
```

Strict independent exit-code check also confirmed all reference0/pitfall1 outcomes without stderr. Combined elapsed seconds per pair: {"nma-t01": 0.0924, "nma-t02": 0.0759, "nma-t03": 0.0767, "nma-t04": 0.0837, "nma-t05": 0.0706}.

All5 tasks/24probes resolve only current generated relation IDs, exact17evaluation files, stdlib/no-network checkers and5-second candidate timeouts. Final module still reproduces all484 generated records; no world/source data changed after the four native checks. Registry is append-only16 new cited sources; thin builder differs solely in import. No unresolved factual uncertainty retained within these explicit scopes; external Claude review and real-model benefit measurement remain separate. Ready for one authoring commit.
