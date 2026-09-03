#!/usr/bin/env python3
"""Author deep creativity, bottom-up, and lateral-thinking curricula."""

from __future__ import annotations

import json
from typing import Any

from registry_lib import ROOT
from curriculum_split import RelationSplitter


OUTPUT = ROOT / "curricula" / "creativity-thinking" / "foundations.jsonl"
WORLD = "creativity-thinking-v0"
SOURCES = ["campbell-1960-bvsr", "boden-creative-mind", "de-bono-lateral-thinking", "sep-scientific-discovery", "openstax-psychology-2e"]


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
    ("lateral", "novelty-only", "A lateral candidate must not bypass comparison with a conventional candidate on validity and value.")
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
        "scope": "creativity, bottom-up, and lateral-thinking foundation",
        "limitations": ["Creative outputs remain proposals; domain truth and operational permission require independent lanes."],
        "as_of": "2026-09-03",
        "version_boundary": "creativity-thinking-v0",
        "split_group": record_id,
        "split": split,
        "tags": ["creativity", "bottom-up", "lateral"]
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
