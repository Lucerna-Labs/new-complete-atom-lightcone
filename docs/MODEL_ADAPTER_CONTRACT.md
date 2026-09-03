# Local-model adapter contract

## Goal

The Lightcone must support most local LLMs without placing model-specific data
inside trained worlds. An adapter is a replaceable boundary implementation,
not a fork of the worlds or geometry.

## Canonical turn

Every adapter accepts:

- ordered system, user, assistant, and tool messages;
- an admitted causal neighborhood with provenance and limitations;
- optional typed reasoning or formal results;
- generation limits and deterministic-decoding request;
- optional tool schema;
- a boundary policy identifier.

It returns visible text, hidden-reasoning presence metadata without exposing
private reasoning, tool calls, token counts, stop reason, model identity,
runtime identity, and capability receipts.

## Declared capabilities

Adapters independently declare and probe:

- tokenizer identity and revision;
- chat-template identity;
- context and output limits;
- raw-logit access;
- custom sampler support;
- grammar or constrained-decoding support;
- tool-call syntax;
- streaming behavior;
- multimodal inputs;
- deterministic decoding;
- seed control;
- embedding support.

Unsupported capabilities remain false. A host-enforced input/output boundary
is required when raw logits or custom samplers are unavailable.

## Conformance

An adapter is supported only after passing identity, passthrough, grounding,
unknown, injection, truncation, tool-call, malformed-output, and restart tests.
Model accuracy and boundary correctness are scored separately.

