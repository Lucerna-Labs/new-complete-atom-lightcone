# Architecture

## Boundary law

The full system is layered so that no model or reasoning engine is confused
with the Lightcone itself:

```text
sourced observations and formal laws
    -> curriculum compiler
    -> world trainer
    -> immutable causal world pack
    -> passive Lightcone admission
    -> admitted nodes and edges plus receipt
    -> optional reasoning, formal, or creativity lane
    -> replaceable local-model adapter
    -> candidate output
    -> host-owned validation and release policy
```

The Lightcone performs seed resolution and bounded causal reachability. It may
use trained coordinates to find geometric seeds, but it cannot turn proximity
into truth. Exact graph edges, evidence, scope, and epistemic status remain in
the returned neighborhood.

## Components

### Coverage registry

The registry is the authoritative statement of what is known to require
training. Every item has an owner, parent, epistemic class, coverage axes,
dependencies, cross-domain obligations, status, and evidence location. New
items can be added without changing the runtime schema.

### Evidence store

Source records identify authorship, stable locator, version or retrieval date,
rights lane, trust role, and permitted use. Curriculum records cite source IDs
and distinguish source-grounded observations from hypotheses, interpretations,
formal theorems, executable results, and creative prompts.

### World trainer

Training has two simultaneous outputs:

1. an exact causal graph whose edges retain relation type, direction, scope,
   polarity, provenance, and split assignment;
2. learned geometric coordinates optimized for seed locality, causal
   neighborhood continuity, relation discrimination, and exclusion of
   adversarial negatives.

Coordinates accelerate admission. They never replace the exact graph or its
evidence.

### Passive Lightcone runtime

The runtime verifies every manifest hash before loading. Admission is
deterministic for a fixed pack, policy, and query representation. Its receipt
records the pack identity, policy, seed nodes, traversed edges, admitted nodes,
excluded candidates, truncation, and hashes. It returns no answer or verdict.

### Reasoning and creative lanes

Reasoning lanes consume only admitted material. Each lane has its own typed
intermediate steps, failure controls, and output contract. Creativity is a
proposal generator: novelty cannot override hard constraints, evidence,
causality, safety, or permission.

### Model adapters

Adapters translate a canonical turn into a model's prompt/API and translate the
response back. They declare capabilities rather than pretending equivalence:
raw-logit access, grammar constraints, tool calls, multimodality, context
length, streaming, and deterministic decoding are independently probed.

## Geometry as a foundation

Geometry is both a subject world and a structural service. The subject world
covers spatial, analytic, affine, projective, discrete, computational,
differential, algebraic, topological, and transformational geometry. The
structural service supplies invariants used across physics, engineering,
graphics, typography, architecture, robotics, interfaces, networks, and
reasoning about transformations.

Graph distance, learned coordinate distance, logical entailment, causal
direction, and evidential strength are separate quantities. The system must
never collapse them into one similarity score.

## Scaling and partitioning

Worlds may be separated by domain, epistemic regime, update cadence, safety
boundary, or computational toolchain. Cross-world bridge edges are trained and
tested explicitly. Partitioning is an implementation tool, not permission to
leave a requested domain uncovered.

