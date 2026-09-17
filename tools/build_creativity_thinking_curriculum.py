#!/usr/bin/env python3
"""Author deep creativity and distinct bottom-up, vertical, nonlinear, and lateral-thinking curricula."""

from __future__ import annotations

import json
from typing import Any

from registry_lib import ROOT
from curriculum_split import RelationSplitter


OUTPUT = ROOT / "curricula" / "creativity-thinking" / "foundations.jsonl"
WORLD = "creativity-thinking-v0"
SOURCES = [
    "campbell-1960-bvsr", "boden-creative-mind", "de-bono-lateral-thinking",
    "de-bono-lateral-vertical-1969", "vance-linear-nonlinear-2007",
    "sep-scientific-discovery", "noba-psychology"
]


GROUPS = {
    "creative": {
        "root": "creative.root",
        "domain": "creative-writing",
        "subject": "creative-writing.story-structure",
        "lanes": [
            "creativity.generation_selection", "creativity.conceptual_blending",
            "creativity.constraint_based", "creativity.novelty_value",
            "creativity.problem_framing", "creativity.tension_transformation",
            "creativity.memory_recombination"
        ],
        "concepts": [
            ("root", "Creative proposal system", "A creative proposal system generates multiple traceable candidates, preserves hard constraints, compares novelty with value, and grants no factual authority to invention."),
            ("generation", "Candidate generation", "Candidate generation deliberately produces multiple alternatives before selection."),
            ("variation", "Structured variation", "Structured variation changes declared attributes, relations, frames, or combinations while retaining a trace of each operation."),
            ("selection", "Candidate selection", "Candidate selection applies declared constraints and value criteria after generation rather than steering every candidate toward one early answer."),
            ("conceptual-space", "Conceptual space", "A conceptual space organizes concepts and transformations under a shared set of dimensions, relations, or practices."),
            ("structural-mapping", "Structural mapping", "Structural mapping aligns roles and relations between conceptual spaces before blending their content."),
            ("blend", "Conceptual blend", "A conceptual blend combines mapped structure from multiple spaces and records every contributor."),
            ("emergence", "Emergent blend structure", "Emergent blend structure is a new relation or property produced by the combination and remains a proposal until separately tested."),
            ("hard-constraint", "Hard constraint", "A hard constraint is an obligation no amount of novelty or soft value can trade away."),
            ("soft-preference", "Soft preference", "A soft preference contributes value but may be traded against other preferences after hard constraints pass."),
            ("constraint-filter", "Constraint filter", "A constraint filter rejects candidates that violate any hard constraint before ranking."),
            ("novelty", "Novelty", "Novelty measures relevant difference from known candidates and is not equivalent to usefulness or truth."),
            ("value", "Creative value", "Creative value measures fitness to a declared purpose, audience, or need under its constraints."),
            ("pareto-front", "Novelty-value frontier", "A novelty-value frontier preserves candidates that are not dominated on both novelty and value."),
            ("problem", "Original problem", "The original problem records requirements, stakeholders, context, exclusions, and success conditions before reframing."),
            ("frame", "Problem frame", "A problem frame selects a representation, boundary, and perspective from which solutions are generated."),
            ("reframe", "Reframing", "Reframing changes representation or boundary while preserving a traceable link to original requirements."),
            ("tension", "Creative tension", "A creative tension states two valuable but apparently incompatible requirements without deleting either side."),
            ("bridge", "Tension bridge", "A tension bridge proposes a mechanism that addresses both sides of a declared tension."),
            ("memory-source", "Memory source", "A memory source contributes candidate material with provenance but does not become evidence for a new claim merely through recall."),
            ("recombination", "Memory recombination", "Memory recombination assembles elements from prior cases into a new candidate while retaining source identity."),
            ("provenance", "Creative provenance", "Creative provenance records source concepts, spaces, frames, transformations, and selection criteria."),
            ("proposal-status", "Proposal status", "A creative candidate remains explicitly proposed, fictional, hypothetical, or design-oriented until the appropriate evidence lane validates it.")
        ]
    },
    "bottom": {
        "root": "bottom.root",
        "domain": "first-principles",
        "subject": "first-principles.composition",
        "lanes": ["thinking.bottom_up", "reasoning.inductive", "reasoning.causal", "geometry.structural"],
        "concepts": [
            ("root", "Bottom-up construction", "Bottom-up construction begins with observations and irreducible primitives, establishes local relations, composes them explicitly, and retains a trace into higher abstractions."),
            ("observation", "Observation inventory", "An observation inventory records what is actually given before a global explanation is imposed."),
            ("primitive", "Primitive candidate", "A primitive candidate is tested for irreducibility, load-bearing behavior, and composability."),
            ("local-relation", "Local relation", "A local relation connects explicitly observed or derived elements under stated conditions."),
            ("mechanism", "Local mechanism", "A local mechanism explains how a relation transmits change without requiring a global narrative."),
            ("composition-order", "Composition order", "Composition order states which validated pieces must exist before later structure can be assembled."),
            ("intermediate", "Intermediate structure", "An intermediate structure is an inspectable composition that can be tested before higher abstraction."),
            ("abstraction", "Traceable abstraction", "A traceable abstraction compresses recurring structure while retaining links to its supporting cases and exceptions."),
            ("emergence", "Emergent behavior", "Emergent behavior is a higher-level pattern produced by interacting lower-level components and must be measured rather than assumed."),
            ("feedback", "Bottom-up feedback", "Observed failure or mismatch propagates back to the specific primitive, relation, or composition that produced it."),
            ("boundary", "Construction boundary", "A construction boundary states where the available primitives and relations no longer support extrapolation.")
        ]
    },
    "vertical": {
        "root": "vertical.root",
        "domain": "first-principles",
        "subject": "first-principles.composition",
        "lanes": ["thinking.vertical", "reasoning.deductive", "thinking.bottom_up"],
        "concepts": [
            ("root", "Vertical and linear refinement", "Vertical and linear refinement selects a working frame, advances through relevant dependency-ordered steps, validates each step, and checks whether the path converged or must reopen."),
            ("selected-frame", "Selected working frame", "A selected working frame states which representation, assumptions, requirements, and success conditions currently organize the investigation."),
            ("relevance", "Frame-relative relevance", "Frame-relative relevance prioritizes information that bears on the selected path while retaining anomalies and counterevidence for possible reopening."),
            ("dependency", "Dependency chain", "A dependency chain orders steps so no result is used before its prerequisites have been established."),
            ("step", "Sequential step", "A sequential step performs one declared operation and exposes its inputs and output."),
            ("validation", "Local step validation", "Local step validation checks a result before it is admitted as an input to the next operation."),
            ("deepening", "Path deepening", "Path deepening refines the most defensible current approach without pretending it is the only possible frame."),
            ("convergence", "Convergence check", "A convergence check compares the current result with declared success, uncertainty, and stop conditions."),
            ("dead-end", "Dead-end detection", "Dead-end detection identifies when further work inside the current frame cannot satisfy the requirements."),
            ("reopen", "Frame reopening", "Frame reopening returns an invalid, exhausted, or contradicted path to assumption review and alternate-frame generation."),
            ("trace", "Sequential dependency trace", "A sequential dependency trace preserves every validated step and the reason it was selected."),
            ("handoff", "Vertical release boundary", "A vertical result is released only with its frame, dependency trace, checks, and remaining alternatives attached.")
        ]
    },
    "nonlinear": {
        "root": "nonlinear.root",
        "domain": "first-principles",
        "subject": "first-principles.composition",
        "lanes": ["thinking.nonlinear", "reasoning.abductive", "reasoning.analogical", "reasoning.causal"],
        "concepts": [
            ("root", "Nonlinear thinking network", "A nonlinear thinking network integrates branching, recursive, feedback-linked, intuitive, and holistic cues, then externalizes and verifies its candidate structure before claim release."),
            ("cue-field", "Cue field", "A cue field retains observations, internal cues, associations, constraints, tensions, and unknowns without granting every cue equal evidential weight."),
            ("source-boundary", "Internal-external cue boundary", "The internal-external cue boundary distinguishes intuition and memory from externally checkable observations and sources."),
            ("branch", "Branching exploration", "Branching exploration permits multiple linked paths to develop concurrently without collapsing them into one premature chain."),
            ("association", "Association edge", "An association edge names why two cues are connected and how that connection could be checked."),
            ("feedback", "Bounded feedback loop", "A bounded feedback loop allows downstream implications to revise earlier structure under an explicit termination rule."),
            ("recursion", "Recursive decomposition", "Recursive decomposition revisits a candidate component at a finer scale while preserving its parent relation and stopping condition."),
            ("holistic-pattern", "Holistic candidate pattern", "A holistic candidate pattern compresses distributed cues without erasing disagreements, missing links, or source classes."),
            ("candidate", "Nonlinear candidate structure", "A nonlinear candidate structure is a proposed graph of relevant cues, relations, loops, and boundaries rather than an unexplained intuition."),
            ("externalization", "Connection externalization", "Connection externalization converts implicit jumps into inspectable nodes, edges, assumptions, and alternatives."),
            ("verification", "Nonlinear verification", "Nonlinear verification tests the externalized candidate with the appropriate logical, causal, probabilistic, empirical, or formal lane."),
            ("stop", "Feedback stop condition", "A feedback stop condition prevents endless recursion, circular self-support, and unbounded associative drift.")
        ]
    },
    "lateral": {
        "root": "lateral.root",
        "domain": "first-principles",
        "subject": "first-principles.composition",
        "lanes": ["thinking.lateral", "reasoning.analogical", "creativity.problem_framing", "creativity.constraint_based"],
        "concepts": [
            ("root", "Lateral exploration", "Lateral exploration deliberately changes frames, perspectives, assumptions, and remote structural associations while reapplying evidence, safety, permission, and task constraints."),
            ("current-frame", "Current frame", "The current frame makes the existing problem boundary and default assumptions explicit."),
            ("alternate-frame", "Alternate frame", "An alternate frame represents the same underlying requirements through a different boundary or perspective."),
            ("assumption-challenge", "Assumption challenge", "An assumption challenge asks whether a default commitment is necessary, contingent, or merely habitual."),
            ("perspective", "Perspective shift", "A perspective shift reconstructs the problem from another stakeholder, scale, time, or system boundary."),
            ("remote-domain", "Remote domain", "A remote domain supplies potentially useful relational structure rather than just surprising vocabulary."),
            ("remote-association", "Remote association", "A remote association connects distant concepts through an explicit structural bridge."),
            ("provocation", "Provocative candidate", "A provocative candidate temporarily disrupts the default frame to reveal alternatives and does not receive truth or permission authority."),
            ("reversal", "Constraint reversal probe", "A reversal probe asks what changes if a default direction or role is inverted, then restores hard constraints before acceptance."),
            ("constraint-return", "Constraint return", "Constraint return reapplies original requirements, evidence, safety, and permissions after exploration."),
            ("comparison", "Lateral candidate comparison", "Lateral candidates are compared with conventional candidates for validity, usefulness, cost, novelty, and failure modes."),
            ("integration", "Lateral integration", "A lateral candidate enters normal planning only after its bridge and constraints survive evaluation.")
        ]
    }
}


RELATIONS = [
    ("creative", "generation-selection", "creative.generation", "creative.selection", "prerequisite", "Generation precedes selection so exploration is not collapsed to the first candidate."),
    ("creative", "variation-generation", "creative.variation", "creative.generation", "enables", "Structured variation enables multiple candidate generation."),
    ("creative", "space-mapping", "creative.conceptual-space", "creative.structural-mapping", "prerequisite", "Contributing spaces are declared before structural mapping."),
    ("creative", "mapping-blend", "creative.structural-mapping", "creative.blend", "enables", "Structural mapping enables a traceable conceptual blend."),
    ("creative", "blend-emergence", "creative.blend", "creative.emergence", "enables", "A blend can enable emergent candidate structure."),
    ("creative", "hard-filter", "creative.hard-constraint", "creative.constraint-filter", "prerequisite", "Hard constraints must be declared before candidates are filtered."),
    ("creative", "filter-selection", "creative.constraint-filter", "creative.selection", "prerequisite", "Constraint filtering precedes value-based selection."),
    ("creative", "preference-value", "creative.soft-preference", "creative.value", "supports", "Satisfied soft preferences support creative value after hard constraints pass."),
    ("creative", "novelty-front", "creative.novelty", "creative.pareto-front", "enables", "Novelty is one independent objective on the selection frontier."),
    ("creative", "value-front", "creative.value", "creative.pareto-front", "enables", "Value is one independent objective on the selection frontier."),
    ("creative", "problem-frame", "creative.problem", "creative.frame", "prerequisite", "The original problem precedes alternate framing."),
    ("creative", "frame-reframe", "creative.frame", "creative.reframe", "enables", "A declared frame enables a traceable reframe."),
    ("creative", "tension-bridge", "creative.tension", "creative.bridge", "enables", "A declared tension enables evaluation of a bridge that addresses both sides."),
    ("creative", "memory-recombine", "creative.memory-source", "creative.recombination", "enables", "Named memory sources enable traceable recombination."),
    ("creative", "recombine-provenance", "creative.recombination", "creative.provenance", "requires", "Recombination requires provenance for every source contribution."),
    ("creative", "provenance-status", "creative.provenance", "creative.proposal-status", "qualifies", "Provenance and transformation history qualify a candidate's proposal status."),
    ("bottom", "observation-primitive", "bottom.observation", "bottom.primitive", "enables", "Observations enable candidate primitives to be extracted and tested."),
    ("bottom", "primitive-local", "bottom.primitive", "bottom.local-relation", "enables", "Validated primitives enable local relations to be stated."),
    ("bottom", "local-mechanism", "bottom.local-relation", "bottom.mechanism", "enables", "Local relations enable mechanisms to be tested."),
    ("bottom", "order-intermediate", "bottom.composition-order", "bottom.intermediate", "enables", "Declared composition order enables an inspectable intermediate structure."),
    ("bottom", "intermediate-abstraction", "bottom.intermediate", "bottom.abstraction", "enables", "Repeated validated intermediate structure enables a traceable abstraction."),
    ("bottom", "composition-emergence", "bottom.intermediate", "bottom.emergence", "causes", "Interacting intermediate structures can cause measured emergent behavior."),
    ("bottom", "feedback-local", "bottom.feedback", "bottom.local-relation", "qualifies", "Failure feedback qualifies which local relation or mechanism must be revised."),
    ("bottom", "boundary-abstraction", "bottom.boundary", "bottom.abstraction", "qualifies", "The construction boundary limits abstraction and extrapolation."),
    ("vertical", "frame-relevance", "vertical.selected-frame", "vertical.relevance", "qualifies", "The selected frame qualifies which information is immediately relevant without deleting counterevidence."),
    ("vertical", "relevance-dependency", "vertical.relevance", "vertical.dependency", "enables", "Relevant evidence enables a dependency-ordered path to be constructed."),
    ("vertical", "dependency-step", "vertical.dependency", "vertical.step", "prerequisite", "Declared dependencies precede each sequential step."),
    ("vertical", "step-validation", "vertical.step", "vertical.validation", "prerequisite", "Each sequential operation precedes its local validation."),
    ("vertical", "validation-deepening", "vertical.validation", "vertical.deepening", "enables", "A validated step enables defensible path deepening."),
    ("vertical", "deepening-convergence", "vertical.deepening", "vertical.convergence", "enables", "Path deepening enables a convergence check against declared success conditions."),
    ("vertical", "dead-end-reopen", "vertical.dead-end", "vertical.reopen", "enables", "A demonstrated dead end enables the working frame to be reopened."),
    ("vertical", "trace-handoff", "vertical.trace", "vertical.handoff", "prerequisite", "A complete dependency trace is prerequisite to releasing a vertical result."),
    ("nonlinear", "cue-source-boundary", "nonlinear.cue-field", "nonlinear.source-boundary", "prerequisite", "Cue inventory precedes classification of internal and external evidence sources."),
    ("nonlinear", "cue-branch", "nonlinear.cue-field", "nonlinear.branch", "enables", "The cue field enables several candidate paths to remain live."),
    ("nonlinear", "branch-association", "nonlinear.branch", "nonlinear.association", "enables", "Branching paths enable explicit association edges to be proposed."),
    ("nonlinear", "association-feedback", "nonlinear.association", "nonlinear.feedback", "enables", "Declared association edges enable bounded feedback across the candidate network."),
    ("nonlinear", "feedback-recursion", "nonlinear.feedback", "nonlinear.recursion", "enables", "Feedback can enable recursive decomposition when the stopping rule remains explicit."),
    ("nonlinear", "pattern-candidate", "nonlinear.holistic-pattern", "nonlinear.candidate", "enables", "A retained holistic pattern enables a candidate network structure to be stated."),
    ("nonlinear", "candidate-externalization", "nonlinear.candidate", "nonlinear.externalization", "prerequisite", "The nonlinear candidate must be externalized before it can receive evidential weight."),
    ("nonlinear", "externalization-verification", "nonlinear.externalization", "nonlinear.verification", "prerequisite", "Externalized connections precede independent verification."),
    ("nonlinear", "stop-feedback", "nonlinear.stop", "nonlinear.feedback", "qualifies", "The stop condition qualifies every feedback iteration and blocks unbounded cycling."),
    ("lateral", "current-alternate", "lateral.current-frame", "lateral.alternate-frame", "enables", "Making the current frame explicit enables controlled alternatives."),
    ("lateral", "challenge-alternate", "lateral.assumption-challenge", "lateral.alternate-frame", "enables", "Challenging contingent assumptions enables alternate frames."),
    ("lateral", "perspective-alternate", "lateral.perspective", "lateral.alternate-frame", "enables", "A perspective shift enables a differently bounded representation."),
    ("lateral", "remote-association", "lateral.remote-domain", "lateral.remote-association", "enables", "A remote domain enables association only through mapped relational structure."),
    ("lateral", "provocation-frame", "lateral.provocation", "lateral.alternate-frame", "enables", "A provocative candidate can expose an alternate frame without becoming an accepted claim."),
    ("lateral", "reversal-return", "lateral.reversal", "lateral.constraint-return", "requires", "A reversal probe requires restoration of hard constraints before evaluation."),
    ("lateral", "association-return", "lateral.remote-association", "lateral.constraint-return", "requires", "A remote association requires evidence and constraint reapplication."),
    ("lateral", "return-comparison", "lateral.constraint-return", "lateral.comparison", "prerequisite", "Only constraint-surviving candidates enter comparison."),
    ("lateral", "comparison-integration", "lateral.comparison", "lateral.integration", "enables", "Comparative evaluation enables a lateral proposal to enter planning."),
    ("bridge", "bottom-creative", "bottom.intermediate", "creative.generation", "supports", "Bottom-up intermediate structures provide grounded material for creative generation."),
    ("bridge", "lateral-frame-creative", "lateral.alternate-frame", "creative.reframe", "supports", "Lateral alternate frames support creative reframing."),
    ("bridge", "creative-lateral-return", "creative.proposal-status", "lateral.constraint-return", "requires", "A creative proposal requires lateral constraint return before operational use."),
    ("bridge", "lateral-vertical", "lateral.alternate-frame", "vertical.selected-frame", "enables", "Lateral exploration supplies alternate frames from which vertical refinement explicitly selects one."),
    ("bridge", "nonlinear-vertical", "nonlinear.externalization", "vertical.selected-frame", "enables", "Externalized nonlinear structure enables a checkable frame to enter vertical refinement."),
    ("bridge", "vertical-lateral-reopen", "vertical.reopen", "lateral.current-frame", "enables", "Vertical dead-end detection enables renewed lateral examination of the current frame."),
    ("bridge", "bottom-nonlinear", "bottom.local-relation", "nonlinear.association", "supports", "Bottom-up local relations support evidence-weighted edges in nonlinear exploration."),
    ("bridge", "geometry-mapping", "bottom.local-relation", "creative.structural-mapping", "supports", "Explicit local relations support structural mapping across conceptual spaces.")
]


CONTROLS = [
    ("creative", "novelty-trap", "Novel but useless or harmful output must not win merely because it differs from memory."),
    ("creative", "constraint-poisoning", "A prompt that asks creativity to ignore a hard constraint must be rejected."),
    ("creative", "single-candidate", "Producing one predetermined answer must not be reported as generation-and-selection."),
    ("creative", "source-erasure", "A blend that loses contributing source identities must not pass provenance."),
    ("creative", "memory-truth", "Recalled material must not become factual evidence through recombination."),
    ("creative", "frame-goal-loss", "A reframe that drops an original hard requirement must not pass."),
    ("creative", "tension-side-delete", "Deleting one side of a tension must not be reported as transforming it."),
    ("bottom", "premature-abstraction", "A global abstraction without tested primitives and local relations must not receive bottom-up warrant."),
    ("bottom", "top-down-overwrite", "A preferred theory must not overwrite observations that conflict with it."),
    ("bottom", "missing-mechanism", "A correlation between levels must not be reported as an emergent mechanism without an interaction path."),
    ("bottom", "unbounded-extrapolation", "A local mechanism must not be extrapolated past its measured boundary without evidence."),
    ("lateral", "random-word", "A surprising word association without relational mapping must not count as lateral reasoning."),
    ("lateral", "unsafe-reframe", "A reframe must not evade safety, permission, or user exclusions."),
    ("lateral", "false-analogy", "Surface resemblance without aligned causal or relational structure must not justify transfer."),
    ("lateral", "provocation-fact", "A provocative exploration must not be stored or released as observed fact."),
    ("lateral", "novelty-only", "A lateral candidate must not bypass comparison with a conventional candidate on validity and value."),
    ("vertical", "tunnel-vision", "A selected frame must not erase anomalies, counterevidence, or the option to reopen."),
    ("vertical", "premature-convergence", "A plausible intermediate result must not be reported as convergence before success and stop conditions pass."),
    ("vertical", "invalid-step", "A failed local step must not become a premise for later sequential work."),
    ("vertical", "assumption-lock-in", "Repeated work inside one frame must not convert an untested assumption into a fact."),
    ("nonlinear", "intuition-fact", "An intuitive or holistic impression must not be released as observed or established fact."),
    ("nonlinear", "opaque-jump", "An association whose connecting relation cannot be externalized must remain an unsupported candidate."),
    ("nonlinear", "runaway-feedback", "Feedback without a stop rule must not be treated as deeper understanding."),
    ("nonlinear", "post-hoc-coherence", "A neat network assembled after seeing an outcome must not be mistaken for independent prediction or causal evidence.")
]


EXAMPLES = [
    ("creative", "candidate-portfolio", "Creative candidate portfolio", "A design brief produces a conventional option, a constraint-driven option, a structural blend, and a lateral reframe; hard constraints eliminate two before novelty and value rank the survivors.", "train"),
    ("bottom", "service-reconstruction", "Bottom-up service reconstruction", "Observed requests, state transitions, queue capacity, persistence acknowledgements, and failure receipts are composed into a service model without assuming an undocumented global coordinator.", "validation"),
    ("lateral", "cooling-reframe", "Lateral cooling reframe", "A cooling-capacity problem is reframed through thermal storage, workload timing, heat reuse, and demand reduction, then every candidate is returned to safety, cost, and temperature constraints.", "sealed_test"),
    ("creative", "tension-bridge", "Creative tension bridge", "A need for rapid recovery and a need for complete audit are transformed into an append-only event log plus rebuildable materialized state, with the tradeoffs kept explicit.", "cross_domain_holdout"),
    ("vertical", "compiler-chain", "Vertical compiler investigation", "A compiler failure is followed through parsing, typing, ownership, code generation, and linkage in dependency order; every local result is validated before the path deepens.", "validation"),
    ("nonlinear", "distributed-outage", "Nonlinear outage map", "Timing, load, retry, cache, ownership, and observation cues are linked into a bounded feedback graph, then externalized as hypotheses for independent causal and empirical checks.", "sealed_test"),
]


def base(record_id: str, group: str, split: str, kind: str, epistemic: str, sources: list[str]) -> dict[str, Any]:
    spec = GROUPS[group] if group in GROUPS else GROUPS["creative"]
    return {
        "schema_version": 1,
        "record_id": record_id,
        "world_id": WORLD,
        "domain_id": spec["domain"],
        "subject_id": spec["subject"],
        "lanes": spec["lanes"],
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws", "within_domain_composition"],
        "source_ids": sources,
        "scope": "creativity plus distinct bottom-up, vertical, nonlinear, and lateral-thinking foundations",
        "limitations": ["Creative outputs remain proposals; domain truth and operational permission require independent lanes."],
        "as_of": "2026-09-03",
        "version_boundary": "creativity-thinking-v0",
        "split_group": record_id,
        "split": split,
        "tags": ["creativity", "bottom-up", "vertical", "nonlinear", "lateral"]
    }


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for group, spec in GROUPS.items():
        for index, (identifier, label, statement) in enumerate(spec["concepts"]):
            node_id = f"{group}.{identifier}"
            records.append({
                **base(node_id, group, "validation" if index and index % 13 == 0 else "train", "concept", "creative" if group == "creative" else "interpretive", SOURCES),
                "label": label,
                "statement": statement,
                "aliases": [label.lower()]
            })
            if node_id != spec["root"]:
                membership = f"{group}.membership.{identifier}"
                records.append({
                    **base(membership, group, "train", "relation", "interpretive", SOURCES),
                    "label": f"{label} lane membership",
                    "statement": f"{label} is a distinct component of the {group} thinking world.",
                    "aliases": [],
                    "relation": {"source_node": node_id, "target_node": spec["root"], "kind": "part_of", "polarity": 1, "direction": "forward", "conditions": [], "exceptions": []},
                    "coverage_axes": ["primitives_invariants", "within_domain_composition"]
                })
    normalized_kinds = ["prerequisite" if kind == "requires" else kind for _group, _identifier, _source, _target, kind, _statement in RELATIONS]
    splitter = RelationSplitter(normalized_kinds)
    for index, (group, identifier, source, target, kind, statement) in enumerate(RELATIONS):
        normalized_kind = "prerequisite" if kind == "requires" else kind
        owner = group if group in GROUPS else "creative"
        split = splitter.split(normalized_kind, cross_requested=group == "bridge" or index % 17 == 0)
        lanes = sorted(set(lane for spec in GROUPS.values() for lane in spec["lanes"])) if group == "bridge" else GROUPS[owner]["lanes"]
        record = base(f"relation.{identifier}", owner, split, "relation", "interpretive", SOURCES)
        record["lanes"] = lanes
        record.update({
            "label": identifier.replace("-", " "),
            "statement": statement,
            "aliases": [],
            "relation": {
                "source_node": source,
                "target_node": target,
                "kind": normalized_kind,
                "polarity": 1,
                "direction": "forward",
                "conditions": ["hard constraints and proposal status remain explicit"],
                "exceptions": []
            },
            "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"]
        })
        records.append(record)
    for group, identifier, label, statement, split in EXAMPLES:
        node_id = f"example.{group}.{identifier}"
        epistemic = "creative" if group == "creative" else "interpretive"
        records.append({
            **base(node_id, group, split, "worked_example", epistemic, SOURCES),
            "label": label,
            "statement": statement,
            "aliases": [],
            "coverage_axes": ["deductions_predictions_execution", "applications_toolchains", "uncertainty_competing_hypotheses"]
        })
        records.append({
            **base(f"example-membership.{group}.{identifier}", group, split, "relation", epistemic, SOURCES),
            "label": f"{label} membership",
            "statement": f"The {label.lower()} exercises a bounded {group} mechanism.",
            "aliases": [],
            "relation": {"source_node": node_id, "target_node": GROUPS[group]["root"], "kind": "part_of", "polarity": 1, "direction": "forward", "conditions": ["proposal status and hard constraints remain explicit"], "exceptions": []},
            "coverage_axes": ["applications_toolchains", "within_domain_composition"]
        })
    for index, (group, identifier, statement) in enumerate(CONTROLS):
        control_split = "train" if index == 0 else "sealed_test" if index == len(CONTROLS) - 1 or index % 2 else "validation"
        records.append({
            **base(f"control.{group}.{identifier}", group, control_split, "synthetic_control", "synthetic_control", []),
            "label": identifier.replace("-", " "),
            "statement": statement,
            "aliases": [identifier.replace("-", " ")],
            "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
            "synthetic": True,
            "tags": ["negative-control", group]
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
