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

Commit: pending creation, title `Review fixes: quantum`.
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
