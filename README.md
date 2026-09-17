# New Complete Lightcone

This is a from-scratch, model-adaptable Lightcone and causal-world training
system. It is being built for exhaustive, auditable coverage rather than a
small seed pack or a single model.

**Current status:** 22 curated world tranches, 155 authoritative-taxonomy
worlds, and one source-bound coverage-audit world are independently split and
authored. All 640 catalog items and all 9,600 required axes are locally tested,
but the repository is not yet sealed and no active world is
accelerator-accepted. The current curriculum inventory contains 236,240
records: 102,516 concepts, 131,028 typed relations, 1,355 synthetic controls,
1,093 worked examples, and 248 explicit boundary records.

## Non-negotiable definition

The Lightcone is passive causal geometry. It selects an already trained causal
neighborhood and returns a reproducible receipt. Facts, hypotheses, warrants,
formal execution, creative proposals, and model-output decisions retain their
own owners and epistemic classes.

Worlds are independent of language models. Qwen-class models are important
validation targets, but the runtime must adapt to most local LLMs through
replaceable adapters rather than embedding one tokenizer, prompt template, or
inference engine into world artifacts.

The coverage catalog is deliberately open-ended. It begins with mathematics,
geometry, sciences, engineering, computing, software and compiler ecosystems,
AI development, operating systems, networking, browsers, security, psychology,
neuroscience, philosophy, rhetoric, literature, writing, design, typography,
and the arts, and it expands whenever a defensible Lightcone-suitable field or
cross-domain relationship is discovered.

## Foundational lanes

- deductive, inductive, abductive, analogical, causal, counterfactual, and
  probabilistic reasoning;
- bottom-up, vertical/linear, nonlinear, and lateral thinking as four distinct lanes;
- creativity as constrained generation and selection;
- philosophy and rhetorical analysis;
- geometry as a cross-domain structural foundation;
- psychology and neuroscience as separate evidence-sensitive worlds.

These are foundations, not a closed list.

## Repository map

- `crates/lightcone-core/` — passive, hash-verifying causal-cone runtime.
- `crates/lightcone-cli/` — inspection, verification, and admission commands.
- `schemas/` — canonical machine-readable contracts.
- `ontology/` — open-ended domain, lane, and coverage registry.
- `curricula/` — sourced training records and sealed evaluation fixtures.
- `trainer/` — deterministic curriculum compiler and accelerator trainer.
- `docs/SHADOW_GEOMETRY.md` — the 48D-to-4D observer contract, distortion
  accounting, composition laws, and runtime boundary.
- `kaggle/` — Kaggle TPU job packaging.
- `adapters/` — declarative local-model adapter profiles and conformance data.
- `artifacts/` — generated world packs; never accepted without receipts.
- `receipts/` — immutable training and validation evidence.
- `plans/taxonomy-training-shards/` — bounded work manifests covering every
  imported authoritative taxonomy discovery exactly once.
- `docs/` — architecture, coverage, sourcing, training, and validation laws.

## Initial local verification

```bash
cargo test --workspace
python3 tools/validate_sources.py
python3 tools/validate_registry.py
python3 tools/validate_curricula.py
python3 tools/validate_adapters.py
python3 tools/validate_taxonomy_shards.py
python3 tools/validate_revocations.py
python3 tools/sync_authored_coverage.py

# after compiling all configured worlds
python3 tools/validate_training_protocols.py

# after a training run
python3 tools/validate_shadow_output.py <training-output>

# exercise every catalog-package prerequisite without creating upload files
python3 kaggle/package_catalog_job.py --kernel-version 1 --validate-only
```

The complete CPU diagnostic is `python3 tools/run_local_smoke_matrix.py`. It is
not accelerator evidence and never advances coverage status. The retained
protocol-v2 baseline records 3 of 22 curated worlds passing every non-TPU gate
and 19 explicit held-out failures. Protocol v3 corrects the discarded-evidence
and accidental-shadow boundaries without weakening thresholds. The current
178-world source matrix passes every non-TPU and serialized-shadow gate,
including the separate vertical and nonlinear lanes and the coverage audit.
TPU identity remains intentionally unclaimed.
Kaggle jobs are packaged only from a clean Git revision
after the compiler, rights, leakage, split-population, revocation, and hash
checks pass.

The hash-bound aggregate CPU evidence is retained at
`receipts/local-diagnostics/protocol-v3-cpu-20260911.json`; it explicitly records
the dirty source state and cannot be mistaken for accelerator acceptance.
The later vertical/nonlinear lane extension and both affected-world reruns are
separately bound by
`receipts/local-diagnostics/thinking-lanes-vertical-nonlinear-20260911.json`.
The complete current matrix is bound by
`receipts/local-diagnostics/protocol-v3-current-cpu-20260917.json`, and the
exact Qwen3.8-27B llama.cpp route is bound by
`receipts/adapters/qwen3.8-27b-llama-cpp-openai.json`.

Every protocol-v3 training run derives a hash-bound four-dimensional
all-spatial shadow from the full 48D coordinates using a train-only fitted
orthonormal projection. The shadow is observable through
`lightcone-cli shadow`, but is never used for admission and never replaces the
exact graph. Its collisions, invisible edges, false proximity, 3D/2D
composition, and random/axis-shuffle placebos are required receipt evidence.
The retained protocol-v2 diagnostics preserve their twelve shadow-placebo
failures. All 178 current-source protocol-v3 worlds pass their shadow and
serialized-artifact checks. These diagnostics are not TPU acceptance.

## Authored world tranches

The repository currently contains independently split curricula for the lane
foundation; geometry; philosophy and rhetoric; psychology and neuroscience;
scientific reasoning; constrained creativity plus bottom-up, vertical,
nonlinear, and lateral thinking; custom Rust
orchestrators; typography, color, and visual design; literature and writing;
networking, defensive security, and browsers; software, frontend, Android, and
Apple development; programming languages and compilers; operating systems; AI
development; mathematics, probability, and information theory; natural
sciences; engineering; first-principles analysis; computer and distributed
data systems; HCI, linguistics, communication, and learning; health and
agriculture; and society, culture, law, economics, history, and the arts.

All 640 current catalog items have source-bound evidence and local tests, but
the catalog remains open-ended. The imported MSC 2020 and MeSH 2026 inventories contain 37,713
mapped entries in 155 bounded worlds. The generated curricula preserve 30,960
MeSH scope notes, MSC classification statements, preferred labels, aliases,
version boundaries, and published hierarchy relations. A taxonomy statement is
not promoted into a causal claim. An authored curriculum is not a trained or
accepted world: only a hash-bound real-TPU receipt that passes every
pre-registered gate can advance it to accelerator-validated status.

The historical `foundation-lanes-v0/0.1.0` artifact is retained only for
audit. Its acceptance was revoked after a source-rights review found current
OpenStax textbook notices that prohibit LLM training without permission. The
23 foundation lanes have been rolled back from the revoked artifact and now reference a
rights-clean replacement curriculum awaiting a fresh TPU run.

The exact formal-execution sidecar currently exposes 30 bounded primitives,
including arithmetic, algebra, calculus, probability, word-problem, and exact
2D geometry operations. Every result is dual-evaluated and fails closed on
disagreement; it is deliberately separate from passive Lightcone admission.
See `docs/FORMAL_EXECUTION.md`.
