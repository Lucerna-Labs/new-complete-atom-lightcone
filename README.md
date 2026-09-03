# New Complete Lightcone

This is a from-scratch, model-adaptable Lightcone and causal-world training
system. It is being built for exhaustive, auditable coverage rather than a
small seed pack or a single model.

**Current status:** foundation tranche in progress. The repository is not yet
exhaustive and no domain is complete until the coverage ledger and sealed gates
prove it.

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
- bottom-up and lateral thinking;
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
- `kaggle/` — Kaggle TPU job packaging.
- `adapters/` — declarative local-model adapter profiles and conformance data.
- `artifacts/` — generated world packs; never accepted without receipts.
- `receipts/` — immutable training and validation evidence.
- `docs/` — architecture, coverage, sourcing, training, and validation laws.

## Initial local verification

```bash
cargo test --workspace
python3 tools/validate_registry.py
python3 tools/validate_curricula.py
```

Kaggle jobs are submitted only after the local compiler and leakage checks pass.

