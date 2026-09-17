#!/usr/bin/env python3
"""Author the intentionally small custom Rust-orchestrator world."""

from __future__ import annotations

import json
from typing import Any

from registry_lib import ROOT
from curriculum_split import RelationSplitter


OUTPUT = ROOT / "curricula" / "custom-rust-orchestrators" / "foundations.jsonl"
WORLD = "rust-orchestrator-apps-v0"
DOMAIN = "custom-rust-orchestrated-apps"
LANES = ["thinking.bottom_up", "creativity.constraint_based", "reasoning.causal", "reasoning.counterfactual"]
SOURCES = ["rust-book", "cargo-reference", "tokio-documentation"]


CONCEPTS = [
    ("root", "First-principles Rust orchestration", "A Rust orchestrator decomposes requirements into typed state, messages, capabilities, workers, and explicit failure behavior before assembling an application.", "custom-rust-orchestrated-apps.requirement-decomposition"),
    ("requirement", "Requirement", "A requirement states an observable obligation, constraint, exclusion, or quality target without prematurely choosing implementation structure.", "custom-rust-orchestrated-apps.requirement-decomposition"),
    ("invariant", "Application invariant", "An invariant is a condition that must remain true across every permitted state transition.", "custom-rust-orchestrated-apps.requirement-decomposition"),
    ("owner", "Single state owner", "Mutable orchestration state has an explicit owner so concurrent components cannot silently create competing truth.", "custom-rust-orchestrated-apps.state-machines"),
    ("command", "Typed command", "A command requests an operation and carries the data and identity required to decide it.", "custom-rust-orchestrated-apps.typed-bus"),
    ("event", "Typed event", "An event records an accepted state transition or observed outcome in a form downstream components can interpret without string guessing.", "custom-rust-orchestrated-apps.typed-bus"),
    ("state-machine", "State machine", "A state machine declares valid states, transitions, guards, and terminal conditions.", "custom-rust-orchestrated-apps.state-machines"),
    ("reducer", "Deterministic reducer", "A reducer applies one event to one prior state to produce one next state without hidden side effects.", "custom-rust-orchestrated-apps.state-machines"),
    ("bus", "Typed event bus", "A typed bus transports declared messages while preserving message identity and delivery errors.", "custom-rust-orchestrated-apps.typed-bus"),
    ("bounded-queue", "Bounded queue", "A bounded queue limits admitted work and makes overload behavior explicit.", "custom-rust-orchestrated-apps.typed-bus"),
    ("backpressure", "Backpressure", "Backpressure slows or rejects producers when downstream capacity is exhausted rather than hiding unbounded growth.", "custom-rust-orchestrated-apps.typed-bus"),
    ("worker", "Worker", "A worker owns execution of a narrow task contract and reports outcomes through typed events.", "custom-rust-orchestrated-apps.loose-coupling"),
    ("orchestrator", "Orchestrator", "An orchestrator coordinates state and work ownership without absorbing every component's domain logic.", "custom-rust-orchestrated-apps.loose-coupling"),
    ("capability", "Capability boundary", "A capability grants a narrow operation on an explicit resource and does not imply adjacent authority.", "custom-rust-orchestrated-apps.capability-boundaries"),
    ("idempotency", "Idempotency key", "An idempotency key lets repeated delivery identify an already accepted logical operation.", "custom-rust-orchestrated-apps.failure-recovery"),
    ("correlation", "Correlation identifier", "A correlation identifier links commands, events, logs, and results belonging to one logical operation.", "custom-rust-orchestrated-apps.typed-bus"),
    ("cancellation", "Cancellation", "Cancellation is an explicit state transition whose safety depends on what work can be interrupted and what cleanup is guaranteed.", "custom-rust-orchestrated-apps.failure-recovery"),
    ("timeout", "Timeout", "A timeout bounds waiting and produces an explicit outcome; it does not prove the remote operation stopped.", "custom-rust-orchestrated-apps.failure-recovery"),
    ("retry", "Retry policy", "A retry policy declares eligible failures, attempt limits, delay, jitter, and idempotency requirements.", "custom-rust-orchestrated-apps.failure-recovery"),
    ("supervision", "Supervision", "Supervision observes worker termination and applies a declared restart, isolate, escalate, or stop policy.", "custom-rust-orchestrated-apps.failure-recovery"),
    ("failure-isolation", "Failure isolation", "Failure isolation prevents one component fault from corrupting unrelated state or authority.", "custom-rust-orchestrated-apps.failure-recovery"),
    ("side-effect-boundary", "Side-effect boundary", "External writes and irreversible effects occur behind explicit interfaces that can be reviewed, tested, and substituted.", "custom-rust-orchestrated-apps.capability-boundaries"),
    ("provenance", "Operation provenance", "Provenance records who or what requested an operation, which capability authorized it, and which result followed.", "custom-rust-orchestrated-apps.capability-boundaries"),
    ("observability", "Observability", "Logs, metrics, and traces expose state transitions, queue pressure, latency, failures, and causal identifiers without exposing secrets.", "custom-rust-orchestrated-apps.failure-recovery"),
    ("compiler", "Rust compiler boundary", "The Rust compiler validates types, ownership, lifetimes, and declared trait contracts but cannot prove application requirements or runtime environment behavior.", "custom-rust-orchestrated-apps.compiler-feedback"),
    ("unit-test", "Unit test", "A unit test isolates a component law with controlled inputs and expected outcomes.", "custom-rust-orchestrated-apps.compiler-feedback"),
    ("integration-test", "Integration test", "An integration test verifies operational boundaries among real components and transports.", "custom-rust-orchestrated-apps.end-to-end"),
    ("end-to-end", "End-to-end proof", "An end-to-end proof exercises the user-visible path through the real orchestrator, workers, boundaries, and result surface.", "custom-rust-orchestrated-apps.end-to-end")
]


RELATIONS = [
    ("requirements-invariants", "requirement", "invariant", "enables", "Requirements enable explicit application invariants to be derived."),
    ("invariants-state", "invariant", "state-machine", "qualifies", "Invariants qualify which state transitions are valid."),
    ("owner-state", "owner", "state-machine", "grounds", "An explicit owner grounds authoritative state transitions."),
    ("command-orchestrator", "command", "orchestrator", "enables", "Typed commands provide requests the orchestrator can decide."),
    ("orchestrator-event", "orchestrator", "event", "causes", "An accepted orchestrator decision emits a typed event."),
    ("event-reducer", "event", "reducer", "enables", "Typed events provide deterministic reducer inputs."),
    ("reducer-state", "reducer", "state-machine", "implements", "The reducer implements declared state transitions."),
    ("bus-command", "bus", "command", "part_of", "Commands are one typed payload carried by the bus."),
    ("bus-event", "bus", "event", "part_of", "Events are one typed payload carried by the bus."),
    ("bounded-backpressure", "bounded-queue", "backpressure", "enables", "A bounded queue enables backpressure when capacity is reached."),
    ("worker-event", "worker", "event", "causes", "A worker reports completion or failure through typed events."),
    ("orchestrator-worker", "orchestrator", "worker", "enables", "The orchestrator assigns accepted work to narrow workers."),
    ("capability-side-effect", "capability", "side-effect-boundary", "qualifies", "Capabilities qualify which external side effects a worker may perform."),
    ("idempotency-retry", "idempotency", "retry", "prerequisite", "Safe retries of effectful operations generally require idempotency or deduplication."),
    ("correlation-provenance", "correlation", "provenance", "supports", "Correlation identifiers support an operation's provenance chain."),
    ("timeout-cancellation", "timeout", "cancellation", "qualifies", "A timeout may request cancellation but does not prove the operation stopped."),
    ("supervision-worker", "supervision", "worker", "qualifies", "Supervision qualifies how worker failure affects restart and escalation."),
    ("isolation-supervision", "failure-isolation", "supervision", "supports", "Failure isolation supports bounded supervision decisions."),
    ("observability-supervision", "observability", "supervision", "supports", "Observability supplies evidence for supervision and diagnosis."),
    ("compiler-unit", "compiler", "unit-test", "qualifies", "Successful compilation is prerequisite evidence but does not replace behavior tests."),
    ("unit-integration", "unit-test", "integration-test", "supports", "Unit tests support but do not substitute for integration tests."),
    ("integration-e2e", "integration-test", "end-to-end", "supports", "Integration tests support but do not substitute for a user-visible end-to-end proof."),
    ("bottom-up-build", "requirement", "end-to-end", "enables", "A first-principles build composes the path from requirements through verified boundaries to an end-to-end result.")
]


CONTROLS = [
    ("unbounded-channel", "Unbounded-channel control", "An unbounded channel must not be described as backpressure because producers can continue allocating without waiting for capacity."),
    ("timeout-stopped", "Timeout-is-not-stop control", "A timeout must not be reported as proof that an external operation terminated."),
    ("retry-nonidempotent", "Non-idempotent retry control", "An effectful operation without deduplication must not be retried automatically as though repetition were harmless."),
    ("compiler-complete", "Compiler-is-not-completion control", "A clean compile must not be reported as proof that requirements, integration, or user behavior are correct."),
    ("stringly-typed", "Stringly typed bus control", "Ad-hoc message strings must not be treated as equivalent to a typed message contract."),
    ("orchestrator-monolith", "Orchestrator monolith control", "Coordination does not authorize the orchestrator to absorb every worker's domain logic and storage."),
    ("cancellation-unsafe", "Cancellation-safety control", "Dropping an arbitrary future must not be assumed safe without checking its partial-effect behavior."),
    ("capability-expansion", "Capability expansion control", "Permission for one operation must not silently authorize neighboring resources or actions."),
    ("duplicate-delivery", "Duplicate-delivery control", "At-least-once delivery must not be treated as exactly-once execution without an idempotency mechanism."),
    ("logs-secrets", "Secret-observability control", "Observability must not expose credentials, private payloads, or secret material."),
    ("fake-boundary", "Mock-only boundary control", "A mocked integration must not be reported as an operational host-boundary proof.")
]


EXAMPLES = [
    ("bounded-worker", "Bounded worker pipeline", "A typed command enters a bounded channel, one state owner validates the transition, a worker returns a correlated event, and overload is rejected before unbounded allocation.", "custom-rust-orchestrated-apps.typed-bus", "train"),
    ("idempotent-retry", "Idempotent retry and reconciliation", "A timed-out effect retains its operation identity; a bounded retry is allowed only after the worker can deduplicate it, and reconciliation determines whether the original attempt committed.", "custom-rust-orchestrated-apps.failure-recovery", "validation"),
    ("cancellation-ownership", "Cancellation-safe ownership", "An orchestrator cancels a child task only after the resource owner defines how partially completed I/O, locks, buffers, and completion events are reconciled.", "custom-rust-orchestrated-apps.state-machines", "sealed_test"),
    ("host-boundary", "End-to-end host boundary", "A Rust coordinator passes a typed request through the real process boundary, verifies the returned identity and receipt, and distinguishes that proof from an in-memory mock.", "custom-rust-orchestrated-apps.end-to-end", "cross_domain_holdout"),
]


def base(identifier: str, subject: str, split: str, kind: str, epistemic: str, sources: list[str]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "record_id": f"rust-orchestrator.v0.{identifier}",
        "world_id": WORLD,
        "domain_id": DOMAIN,
        "subject_id": subject,
        "lanes": LANES,
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws", "applications_toolchains"],
        "source_ids": sources,
        "scope": "small custom Rust-orchestrator application-building world",
        "limitations": ["This custom lane is intentionally smaller than general software-engineering and language worlds."],
        "as_of": "2026-09-03",
        "version_boundary": "Rust 2024 edition; Tokio 1.x documentation baseline",
        "split_group": f"rust-orchestrator.v0.{identifier}",
        "split": split,
        "tags": ["rust", "orchestration", "first-principles"]
    }


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, (identifier, label, statement, subject) in enumerate(CONCEPTS):
        records.append({
            **base(identifier, subject, "validation" if index and index % 13 == 0 else "train", "concept", "established", SOURCES),
            "label": label,
            "statement": statement,
            "aliases": [label.lower()]
        })
        if identifier != "root":
            records.append({
                **base(f"membership-{identifier}", subject, "train", "relation", "established", SOURCES),
                "label": f"{label} orchestrator-world membership",
                "statement": f"{label} is a distinct component of the first-principles Rust orchestrator world.",
                "aliases": [],
                "relation": {"source_node": f"rust-orchestrator.v0.{identifier}", "target_node": "rust-orchestrator.v0.root", "kind": "part_of", "polarity": 1, "direction": "forward", "conditions": [], "exceptions": []},
                "coverage_axes": ["primitives_invariants", "within_domain_composition"]
            })
    splitter = RelationSplitter([kind for _identifier, _source, _target, kind, _statement in RELATIONS])
    for index, (identifier, source, target, kind, statement) in enumerate(RELATIONS):
        split = splitter.split(kind, cross_requested=index % 17 == 0)
        records.append({
            **base(identifier, "custom-rust-orchestrated-apps.end-to-end", split, "relation", "established", SOURCES),
            "label": identifier.replace("-", " "),
            "statement": statement,
            "aliases": [],
            "relation": {
                "source_node": f"rust-orchestrator.v0.{source}",
                "target_node": f"rust-orchestrator.v0.{target}",
                "kind": kind,
                "polarity": 1,
                "direction": "forward",
                "conditions": ["the component contracts and ownership are explicit"],
                "exceptions": []
            },
            "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "applications_toolchains"]
        })
    for identifier, label, statement, subject, split in EXAMPLES:
        node_id = f"example-{identifier}"
        records.append({
            **base(node_id, subject, split, "worked_example", "established", SOURCES),
            "label": label,
            "statement": statement,
            "aliases": [],
            "coverage_axes": ["deductions_predictions_execution", "applications_toolchains", "within_domain_composition"]
        })
        records.append({
            **base(f"example-membership-{identifier}", subject, split, "relation", "established", SOURCES),
            "label": f"{label} membership",
            "statement": f"The {label.lower()} exercises a bounded Rust-orchestrator mechanism.",
            "aliases": [],
            "relation": {"source_node": f"rust-orchestrator.v0.{node_id}", "target_node": "rust-orchestrator.v0.root", "kind": "part_of", "polarity": 1, "direction": "forward", "conditions": ["the typed lifecycle and authority boundary remain fixed"], "exceptions": []},
            "coverage_axes": ["applications_toolchains", "within_domain_composition"]
        })
    for index, (identifier, label, statement) in enumerate(CONTROLS):
        control_split = "train" if index == 0 else "sealed_test" if index == len(CONTROLS) - 1 or index % 2 else "validation"
        records.append({
            **base(identifier, "custom-rust-orchestrated-apps.failure-recovery", control_split, "synthetic_control", "synthetic_control", []),
            "label": label,
            "statement": statement,
            "aliases": [label.lower()],
            "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
            "synthetic": True,
            "tags": ["rust", "negative-control"]
        })
    return sorted(records, key=lambda record: record["record_id"])


def main() -> int:
    records = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records), encoding="utf-8")
    counts: dict[str, int] = {}
    for record in records:
        counts[record["split"]] = counts.get(record["split"], 0) + 1
    print(f"wrote {OUTPUT} with {len(records)} records: {dict(sorted(counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
