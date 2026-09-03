# Training and validation protocol

## Before training

1. Register the domain, lane, subfield, and all required coverage axes.
2. Register authoritative sources and rights constraints.
3. Author typed causal records with provenance and explicit epistemic status.
4. Create positive, negative, adversarial, contradiction, and unknown records.
5. Freeze train, validation, sealed-test, and cross-domain holdout groups by
   mechanism—not by random paraphrase row.
6. Run schema, graph, provenance, rights, duplicate, and leakage validators.

## Accelerator training

The canonical accelerator path is Kaggle TPU with JAX. Every run must record:

- Kaggle kernel and version identity;
- TPU device/topology evidence from the running process;
- exact input dataset version and hashes;
- source revision and dirty-state declaration;
- hyperparameters, seed, dtype, batch size, and step count;
- training/validation curves and stopped-step reason;
- wall time and accelerator utilization evidence;
- output file hashes.

A CPU or GPU smoke test may find bugs but cannot satisfy a TPU training gate.

## Objective families

Training optimizes distinct objectives and reports them separately:

- seed retrieval and alias robustness;
- causal-edge direction and relation classification;
- local-neighborhood continuity;
- out-of-cone and hard-negative separation;
- multi-step reachability;
- counterfactual and contradiction discrimination;
- cross-world bridge recovery;
- geometric transformation and invariant preservation.

No aggregate score may hide a failed required family.

## Sealed evaluation

Sealed tests contain unseen mechanisms, not just unseen wording. Evaluation
must report per-domain, per-lane, per-relation, per-hop, and per-coverage-axis
metrics. Reachability and final decisiveness are separate measurements.

Required failure labels include source error, curriculum error, leakage,
geometry failure, routing failure, relation failure, adapter failure, resource
failure, and mechanism failure. Corrections append a new receipt; they do not
rewrite the failed run.

## Artifact acceptance

A world pack is accepted only when:

- all declared files match its manifest hashes;
- graph references and evidence references are closed;
- no test split appears in training-derived files;
- required gates pass without post-hoc threshold changes;
- the pack reloads and produces deterministic admission receipts;
- the training and validation receipts are present and hash-bound.

