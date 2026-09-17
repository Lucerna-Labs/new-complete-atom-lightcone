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

## Protocol v3 evidence and shadow correction

Protocol v2 retained relation statements in the curriculum but discarded their
text from the training graph, then asked one global translation vector to infer
every held-out typed relation. It also allowed the observer PCA to compete with
placebos over coordinates whose useful variance was not explicitly organized
for a four-dimensional observer. Those failures remain preserved as evidence.

Protocol v3 keeps all thresholds unchanged and corrects the owning layers:

- the compiler carries source-bound relation evidence text into the graph;
- train-only hashed TF-IDF statistics align unseen evidence statements with
  graph nodes, while a registered relation-semantics catalog and train-only
  centroids score relation families;
- curated causal worlds retain the JAX translation objective for training-edge
  recovery; authoritative taxonomy worlds use evidence-to-descriptor recovery;
- a train-only semantic PCA backbone occupies four dominant spatial
  coordinates, while the remaining 44 coordinates retain a scaled JAX-trained
  residual;
- the observer projection is still independently fit on training nodes, remains
  orthonormal and non-expansive, and is still excluded from admission.

Optimization coordinates, final coordinates, the semantic-overlay receipt, and
the evidence-index receipt are serialized separately so no evaluation path is
hidden.

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
