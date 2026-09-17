#!/usr/bin/env python3
"""Author an explicit first-principles decomposition and recomposition world."""

from __future__ import annotations

import json
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "first-principles" / "foundations.jsonl"
WORLD = "first-principles-v0"
DOMAIN = "first-principles"
LANES = ["thinking.bottom_up", "reasoning.deductive", "reasoning.causal", "philosophy.analysis"]
SOURCES = ["open-logic-project", "sep-argument", "sep-causal-models", "sep-scientific-discovery", "national-academies-reproducibility"]


CONCEPTS = [
    ("root", "First-principles analysis", "First-principles analysis decomposes a problem into independently defensible primitives, exposes assumptions and constraints, identifies invariants, recomposes mechanisms bottom up, and attacks the result at its boundaries.", "first-principles.decomposition"),
    ("problem-boundary", "Problem boundary", "A problem boundary declares the system, actors, objective, inputs, outputs, environment, authority, time, scale, and excluded concerns.", "first-principles.decomposition"),
    ("observation", "Primitive observation", "A primitive observation is a minimally interpreted recorded fact with provenance, units, conditions, uncertainty, and no hidden explanation.", "first-principles.decomposition"),
    ("definition", "Primitive definition", "A primitive definition fixes the operative meaning of a term and distinguishes neighboring concepts without claiming empirical truth by itself.", "first-principles.decomposition"),
    ("operation", "Primitive operation", "A primitive operation maps typed inputs to outputs under explicit preconditions, side effects, errors, and invariants.", "first-principles.decomposition"),
    ("relation", "Primitive relation", "A primitive relation connects entities through a typed direction, polarity, cardinality, conditions, and possible exceptions.", "first-principles.decomposition"),
    ("irreducibility", "Operational irreducibility", "A proposed primitive is irreducible only relative to the task when further decomposition would not change reasoning, testing, or control decisions.", "first-principles.decomposition"),
    ("explicit-assumption", "Explicit assumption", "An explicit assumption is a proposition accepted for the current derivation with scope, rationale, owner, and failure consequence.", "first-principles.assumptions"),
    ("hidden-assumption", "Hidden assumption", "A hidden assumption is an unstated commitment required for a claim, mechanism, measurement, or plan to work.", "first-principles.assumptions"),
    ("background-condition", "Background condition", "A background condition is held fixed or treated as stable while the focal relation is analyzed.", "first-principles.assumptions"),
    ("model-assumption", "Model assumption", "A model assumption simplifies structure, dynamics, distribution, boundary, or measurement and must be tied to adequacy evidence.", "first-principles.assumptions"),
    ("dependency-question", "Assumption dependency question", "Removing or reversing an assumption tests which downstream claims, constraints, and decisions actually depend on it.", "first-principles.assumptions"),
    ("invariant", "Invariant", "An invariant is a property that must remain true across every permitted state or transformation in a declared class.", "first-principles.invariants"),
    ("conservation", "Conservation invariant", "A conservation invariant balances an extensive quantity across storage, transfer, production, and loss under a system boundary.", "first-principles.invariants"),
    ("identity-invariant", "Identity invariant", "An identity invariant preserves which entity, request, artifact, or state transition is being tracked through transformations.", "first-principles.invariants"),
    ("order-invariant", "Order invariant", "An order invariant preserves a partial or total ordering required by causality, lifecycle, priority, or consistency.", "first-principles.invariants"),
    ("safety-invariant", "Safety invariant", "A safety invariant defines a forbidden-state boundary that every reachable transition must preserve.", "first-principles.invariants"),
    ("representation-invariant", "Representation invariant", "A representation invariant connects encoded state to valid abstract state and must hold after every mutating operation.", "first-principles.invariants"),
    ("hard-constraint", "Hard constraint", "A hard constraint eliminates any candidate that violates law, safety, physics, interface, authority, or required outcome.", "first-principles.constraints"),
    ("soft-constraint", "Soft constraint", "A soft constraint contributes a preference or cost and can be traded only under declared priorities.", "first-principles.constraints"),
    ("resource-constraint", "Resource constraint", "A resource constraint bounds time, compute, memory, energy, money, people, bandwidth, material, or attention.", "first-principles.constraints"),
    ("interface-constraint", "Interface constraint", "An interface constraint fixes types, units, protocol, timing, identity, compatibility, and failure semantics across a boundary.", "first-principles.constraints"),
    ("derived-constraint", "Derived constraint", "A derived constraint follows from primitives, invariants, and other constraints through an auditable derivation.", "first-principles.constraints"),
    ("constraint-conflict", "Constraint conflict", "A constraint conflict occurs when no candidate can satisfy all current hard obligations and therefore requires authority to change scope or priority.", "first-principles.constraints"),
    ("composition-order", "Composition order", "Composition order specifies which primitives must exist or run before others and distinguishes dependencies from mere presentation sequence.", "first-principles.composition"),
    ("state-transition", "State transition", "A state transition maps a valid prior state and event to a next state and effects while preserving invariants.", "first-principles.composition"),
    ("mechanism-chain", "Mechanism chain", "A mechanism chain connects entities and activities so each intermediate state transmits the proposed effect.", "first-principles.composition"),
    ("emergent-property", "Emergent property", "An emergent property arises from component interactions and organization and must be demonstrated rather than assigned from component labels.", "first-principles.composition"),
    ("cross-scale", "Cross-scale composition", "Cross-scale composition maps lower-level states and statistics to higher-level variables while retaining aggregation and information-loss limits.", "first-principles.composition"),
    ("evidence-chain", "Evidence chain", "An evidence chain links source observation through transformations, inference, artifact, execution, and conclusion with identity and uncertainty intact.", "first-principles.composition"),
    ("counterexample", "Counterexample test", "A counterexample supplies an admissible case that defeats a universal claim or alleged invariant.", "first-principles.falsification"),
    ("boundary-case", "Boundary case", "A boundary case lies at zero, empty, maximum, degenerate, singular, transition, or regime limits where hidden assumptions often fail.", "first-principles.falsification"),
    ("negative-control", "Negative control", "A negative control should lack the focal cause or relation and tests whether a method produces unsupported positives.", "first-principles.falsification"),
    ("adversarial-case", "Adversarial case", "An adversarial case is intentionally selected to exploit ambiguity, approximation, interface, distribution, or control weaknesses within an authorized test scope.", "first-principles.falsification"),
    ("falsifier", "Potential falsifier", "A potential falsifier states an observable result that would contradict or materially weaken the current claim under its auxiliaries.", "first-principles.falsification"),
    ("scope-failure", "Scope failure", "A scope failure occurs when a model or mechanism is applied outside the systems, scale, precision, conditions, or purposes for which it was supported.", "first-principles.falsification"),
]


RELATIONS = [
    ("boundary-observation", "fp.problem-boundary", "fp.observation", "qualifies", "The problem boundary qualifies which observations are relevant and comparable."),
    ("definition-operation", "fp.definition", "fp.operation", "prerequisite", "Defined types and terms are prerequisites to specifying an operation."),
    ("operation-relation", "fp.operation", "fp.relation", "causes", "Observed operation behavior can cause or instantiate typed relations."),
    ("irreducible-operation", "fp.irreducibility", "fp.operation", "qualifies", "Task-relative irreducibility qualifies whether an operation is treated as primitive."),
    ("hidden-explicit", "fp.hidden-assumption", "fp.explicit-assumption", "transforms_to", "Assumption discovery transforms a hidden commitment into an explicit reviewable assumption."),
    ("background-model", "fp.background-condition", "fp.model-assumption", "qualifies", "Held-fixed background conditions qualify a model assumption."),
    ("dependency-assumption", "fp.dependency-question", "fp.explicit-assumption", "measures", "Counterfactual removal measures downstream dependence on an assumption."),
    ("invariant-operation", "fp.invariant", "fp.operation", "qualifies", "Invariants qualify every permitted operation and transition."),
    ("conservation-boundary", "fp.problem-boundary", "fp.conservation", "prerequisite", "A declared system boundary is prerequisite to a conservation balance."),
    ("identity-evidence", "fp.identity-invariant", "fp.evidence-chain", "supports", "Identity preservation supports an auditable evidence chain."),
    ("order-mechanism", "fp.order-invariant", "fp.mechanism-chain", "qualifies", "Causal order qualifies mechanism-chain validity."),
    ("safety-transition", "fp.safety-invariant", "fp.state-transition", "qualifies", "A safety invariant qualifies every reachable state transition."),
    ("representation-state", "fp.representation-invariant", "fp.state-transition", "qualifies", "Representation validity qualifies mutation of encoded state."),
    ("hard-candidate", "fp.hard-constraint", "fp.constraint-conflict", "enables", "Mutually incompatible hard constraints enable a detected constraint conflict."),
    ("soft-hard", "fp.soft-constraint", "fp.hard-constraint", "qualifies", "Separating preferences qualifies which obligations cannot be traded."),
    ("resource-order", "fp.resource-constraint", "fp.composition-order", "qualifies", "Resource limits qualify feasible composition order and concurrency."),
    ("interface-composition", "fp.interface-constraint", "fp.composition-order", "qualifies", "Interface contracts qualify how primitives compose."),
    ("derive-primitive", "fp.invariant", "fp.derived-constraint", "supports", "Invariants support derivation of downstream constraints."),
    ("order-transition", "fp.composition-order", "fp.state-transition", "qualifies", "Dependency order qualifies admissible state transitions."),
    ("transition-mechanism", "fp.state-transition", "fp.mechanism-chain", "part_of", "State transitions compose a mechanism chain."),
    ("mechanism-emergence", "fp.mechanism-chain", "fp.emergent-property", "supports", "An interaction mechanism supports an emergent-property claim."),
    ("cross-emergence", "fp.cross-scale", "fp.emergent-property", "qualifies", "Aggregation across scales qualifies interpretation of an emergent property."),
    ("evidence-composition", "fp.evidence-chain", "fp.mechanism-chain", "supports", "A preserved evidence chain supports the proposed mechanism composition."),
    ("counter-invariant", "fp.counterexample", "fp.invariant", "contradicts", "One admissible counterexample contradicts an alleged universal invariant."),
    ("boundary-assumption", "fp.boundary-case", "fp.hidden-assumption", "clarifies", "Boundary cases clarify assumptions hidden in ordinary inputs."),
    ("negative-relation", "fp.negative-control", "fp.relation", "undercuts", "A positive result on a negative control undercuts specificity of the claimed relation."),
    ("adversarial-interface", "fp.adversarial-case", "fp.interface-constraint", "qualifies", "Adversarial cases qualify whether an interface rejects ambiguous or malicious inputs."),
    ("falsifier-assumption", "fp.falsifier", "fp.explicit-assumption", "qualifies", "Falsifiers qualify which assumption or claim would be weakened by an outcome."),
    ("scope-model", "fp.scope-failure", "fp.model-assumption", "undercuts", "A scope failure undercuts applying the model assumption to the current case."),
    ("bridge-decompose-compose", "fp.irreducibility", "fp.composition-order", "prerequisite", "Validated primitives are prerequisites to bottom-up recomposition."),
    ("bridge-assume-falsify", "fp.dependency-question", "fp.falsifier", "supports", "Assumption-dependency questions support targeted falsifiers."),
    ("bridge-constraint-boundary", "fp.derived-constraint", "fp.boundary-case", "qualifies", "Boundary tests qualify whether a derived constraint holds at regime limits."),
]


CONTROLS = [
    ("label-primitive", "Label treated as primitive", "A familiar name must not be treated as irreducible without testing its internal dependencies."),
    ("assumption-fact", "Assumption emitted as fact", "An assumed premise must not be presented as observed or proved."),
    ("hidden-default", "Hidden default", "A default unit, timezone, frame, population, version, or permission must not enter silently."),
    ("invariant-example", "Example treated as invariant", "A property observed in selected examples must not be generalized to every permitted state without proof."),
    ("soft-hard", "Preference treated as hard constraint", "A soft preference must not block all solutions unless authority promotes it to an obligation."),
    ("conflict-ignore", "Constraint conflict ignored", "An impossible hard-constraint set must not be resolved by silently dropping one obligation."),
    ("composition-gap", "Composition gap", "Locally valid components must not establish end-to-end behavior when interface and intermediate-state relations are missing."),
    ("emergence-name", "Emergence by naming", "Calling a property emergent must not replace a mechanism or evidence linking organization to the property."),
    ("scale-collapse", "Scale collapse", "A microscopic relation must not be copied directly to a macroscopic variable without aggregation and regime evidence."),
    ("no-negative", "No negative control", "A method without negative controls must not claim specificity against unsupported positives."),
    ("boundary-skip", "Boundary cases skipped", "Passing ordinary examples must not establish behavior at zero, empty, maximum, singular, or transition cases."),
    ("falsifier-immunized", "Claim immunized from falsification", "A claim that reinterprets every possible outcome as confirmation must not receive empirical warrant."),
]


WORKED_EXAMPLES = [
    ("queue", "Bounded queue decomposition", "A queue is decomposed into item identity, capacity, enqueue, dequeue, ordering, backpressure, close, cancellation, and overflow behavior before an orchestrator is chosen.", "first-principles.decomposition"),
    ("timeout", "Timeout assumption audit", "A timeout is separated from remote failure; the audit exposes the hidden assumption that no side effect occurred and adds idempotency plus reconciliation.", "first-principles.assumptions"),
    ("balance", "Conservation balance", "A storage process records initial amount plus inflows minus outflows plus production minus loss equals final amount under one boundary and interval.", "first-principles.invariants"),
    ("hard-soft", "Constraint classification", "Safety, legal authority, output schema, and data preservation remain hard; color preference and implementation style remain ranked soft preferences.", "first-principles.constraints"),
    ("pipeline", "Bottom-up pipeline", "Validated parse, type, execute, persist, and report primitives are composed through typed state transitions with receipts at each interface.", "first-principles.composition"),
    ("counterexample", "Universal-claim counterexample", "A claim that every retry is safe is defeated by one non-idempotent charged operation, so the corrected rule requires operation identity and reconciliation.", "first-principles.falsification"),
]


def split_for(index: int) -> str:
    if index and index % 17 == 0:
        return "cross_domain_holdout"
    if index and index % 13 == 0:
        return "sealed_test"
    if index and index % 11 == 0:
        return "validation"
    return "train"


def base(identifier: str, subject: str, split: str, kind: str, epistemic: str, sources: list[str]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "record_id": identifier,
        "world_id": WORLD,
        "domain_id": DOMAIN,
        "subject_id": subject,
        "lanes": LANES,
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"],
        "source_ids": sources,
        "scope": "first-principles decomposition, derivation, recomposition, and falsification",
        "limitations": ["Irreducibility is task-relative; deeper domain primitives remain owned by their specialist worlds."],
        "as_of": "2026-09-03",
        "version_boundary": "first-principles-v0",
        "split_group": identifier,
        "split": split,
        "tags": ["foundation", "first-principles"],
    }


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, (identifier, label, statement, subject) in enumerate(CONCEPTS):
        node_id = f"fp.{identifier}"
        records.append(
            {
                **base(node_id, subject, "train" if identifier == "root" else split_for(index), "concept", "established", SOURCES),
                "label": label,
                "statement": statement,
                "aliases": [label.lower()],
            }
        )
        if identifier != "root":
            relation_id = f"fp.membership.{identifier}"
            records.append(
                {
                    **base(relation_id, subject, split_for(index + 3), "relation", "established", SOURCES),
                    "label": f"{label} first-principles membership",
                    "statement": f"{label} is a distinct component of first-principles analysis with its own proof and failure conditions.",
                    "aliases": [],
                    "relation": {
                        "source_node": node_id,
                        "target_node": "fp.root",
                        "kind": "part_of",
                        "polarity": 1,
                        "direction": "forward",
                        "conditions": ["the problem and task boundary are declared"],
                        "exceptions": [],
                    },
                    "coverage_axes": ["primitives_invariants", "within_domain_composition"],
                }
            )

    splitter = RelationSplitter(
        [kind for _identifier, _source, _target, kind, _statement in RELATIONS],
        cross_plan=[
            identifier.startswith("bridge-")
            for identifier, _source, _target, _kind, _statement in RELATIONS
        ],
    )
    for identifier, source, target, kind, statement in RELATIONS:
        records.append(
            {
                **base(
                    f"fp.relation.{identifier}", "first-principles.composition",
                    splitter.split(kind),
                    "relation",
                    "established",
                    SOURCES,
                ),
                "label": identifier.replace("-", " "),
                "statement": statement,
                "aliases": [],
                "relation": {
                    "source_node": source,
                    "target_node": target,
                    "kind": kind,
                    "polarity": -1 if kind in {"inhibits", "prevents", "contradicts", "undercuts"} else 1,
                    "direction": "forward",
                    "conditions": ["the declared task, evidence, and hard constraints remain fixed"],
                    "exceptions": [],
                },
                "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"],
            }
        )

    splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, label, statement) in enumerate(CONTROLS):
        record_id = f"fp.control.{identifier}"
        records.append(
            {
                **base(record_id, "first-principles.falsification", splits[index % 4], "synthetic_control", "synthetic_control", []),
                "label": label,
                "statement": statement,
                "aliases": [label.lower()],
                "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
                "synthetic": True,
                "tags": ["negative-control", "first-principles"],
            }
        )

    for index, (identifier, label, statement, subject) in enumerate(WORKED_EXAMPLES):
        split = splits[index % 4]
        node_id = f"fp.example.{identifier}"
        records.append(
            {
                **base(node_id, subject, split, "worked_example", "established", SOURCES),
                "label": label,
                "statement": statement,
                "aliases": [],
                "coverage_axes": ["applications_toolchains", "deductions_predictions_execution", "within_domain_composition"],
                "tags": ["worked-example", "first-principles"],
            }
        )
        records.append(
            {
                **base(f"fp.example-membership.{identifier}", subject, split, "relation", "established", SOURCES),
                "label": f"{label} membership",
                "statement": f"The {label.lower()} operationalizes one bounded first-principles analysis.",
                "aliases": [],
                "relation": {
                    "source_node": node_id,
                    "target_node": "fp.root",
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the example remains bounded"],
                    "exceptions": [],
                },
                "coverage_axes": ["applications_toolchains", "within_domain_composition"],
            }
        )

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
