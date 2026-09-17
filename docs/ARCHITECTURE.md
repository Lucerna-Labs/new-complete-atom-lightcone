# Architecture

## Boundary law

The full system is layered so that no model or reasoning engine is confused
with the Lightcone itself:

```text
sourced observations and formal laws
    -> curriculum compiler
    -> world trainer
    -> immutable causal world pack
    -> full geometry plus passive 4D all-spatial shadow
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

Protocol-v3 worlds retain the raw JAX optimization geometry separately from the
final 48D geometry. A train-only semantic backbone supplies four dominant
spatial coordinates for auditable projection; a scaled 44D optimization
residual retains additional learned structure. Held-out evidence-to-node and
relation-family metrics use train-fitted text statistics and the registered
typed-relation semantics. These learned views remain subordinate to exact graph
reachability.

Each accepted world also carries an observer-only four-dimensional shadow of
its full coordinates. The projection is fitted on training nodes only, has an
orthonormal non-expansion certificate, and emits composed 3D/2D views. Shadow
collisions and false proximity are measured explicitly. Admission never uses
the shadow; see `SHADOW_GEOMETRY.md`.

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

Thinking modes are also separate contracts. Bottom-up thinking composes from
primitives; vertical/linear thinking deepens one selected dependency path;
nonlinear thinking externalizes branching, recursive, feedback-linked, and
holistic cues before verification; lateral thinking deliberately changes the
frame. Bridges can hand candidates between these lanes, but do not merge their
stages, controls, evidence classes, or scores.

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
