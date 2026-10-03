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

Commit: pending creation, title `Review fixes: chemistry`.
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

Commit: pending creation, title `Review fixes: biology`.
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
