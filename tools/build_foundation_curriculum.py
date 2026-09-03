#!/usr/bin/env python3
"""Author the first sourced, typed foundation-lane curriculum deterministically.

This tranche trains lane anatomy and cross-lane boundaries. It is deliberately
not labeled exhaustive; the coverage ledger remains open until deeper subject
curricula and sealed tests are complete.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from registry_lib import LANE_CATALOG, ROOT, load_json


OUTPUT = ROOT / "curricula" / "foundation" / "lane-foundations.jsonl"
WORLD_ID = "foundation-lanes-v0"


LANE_CONTEXT: dict[str, dict[str, Any]] = {
    "reasoning.deductive": {"domain": "formal-mathematics", "subject": "formal-mathematics.mathematical-logic", "sources": ["open-logic-project", "sep-argument"]},
    "reasoning.inductive": {"domain": "probability-statistics", "subject": "probability-statistics.probability-foundations", "sources": ["sep-inductive-logic", "sep-argument"]},
    "reasoning.abductive": {"domain": "research-scientific-method", "subject": "research-scientific-method.hypotheses", "sources": ["sep-abduction", "sep-scientific-discovery"]},
    "reasoning.analogical": {"domain": "philosophy", "subject": "philosophy.logic", "sources": ["sep-analogy", "sep-argument"]},
    "reasoning.causal": {"domain": "probability-statistics", "subject": "probability-statistics.causal-inference", "sources": ["sep-causal-models"]},
    "reasoning.counterfactual": {"domain": "philosophy", "subject": "philosophy.logic", "sources": ["sep-counterfactuals", "sep-causal-models"]},
    "reasoning.probabilistic": {"domain": "probability-statistics", "subject": "probability-statistics.probability-foundations", "sources": ["sep-probability", "sep-inductive-logic"]},
    "thinking.bottom_up": {"domain": "first-principles", "subject": "first-principles.composition", "sources": ["open-logic-project", "openstax-psychology-2e"]},
    "thinking.lateral": {"domain": "first-principles", "subject": "first-principles.composition", "sources": ["de-bono-lateral-thinking", "sep-scientific-discovery"]},
    "creativity.generation_selection": {"domain": "creative-writing", "subject": "creative-writing.story-structure", "sources": ["campbell-1960-bvsr", "boden-creative-mind"]},
    "creativity.conceptual_blending": {"domain": "creative-writing", "subject": "creative-writing.story-structure", "sources": ["boden-creative-mind"]},
    "creativity.constraint_based": {"domain": "creative-writing", "subject": "creative-writing.constraint-preservation", "sources": ["boden-creative-mind"]},
    "creativity.novelty_value": {"domain": "creative-writing", "subject": "creative-writing.story-structure", "sources": ["campbell-1960-bvsr", "boden-creative-mind"]},
    "creativity.problem_framing": {"domain": "first-principles", "subject": "first-principles.decomposition", "sources": ["sep-scientific-discovery", "boden-creative-mind"]},
    "creativity.tension_transformation": {"domain": "creative-writing", "subject": "creative-writing.tension", "sources": ["boden-creative-mind"]},
    "creativity.memory_recombination": {"domain": "psychology-cognitive-science", "subject": "psychology-cognitive-science.learning", "sources": ["openstax-psychology-2e", "boden-creative-mind"]},
    "philosophy.analysis": {"domain": "philosophy", "subject": "philosophy.epistemology", "sources": ["sep-argument", "open-logic-project"]},
    "rhetoric.analysis": {"domain": "rhetoric-argumentation", "subject": "rhetoric-argumentation.rhetorical-situation", "sources": ["sep-aristotle-rhetoric", "sep-argument"]},
    "geometry.structural": {"domain": "geometry", "subject": "geometry.transformations", "sources": ["mathlib4", "openstax-precalculus-2e"]},
    "psychology.evidence": {"domain": "psychology-cognitive-science", "subject": "psychology-cognitive-science.replication", "sources": ["openstax-psychology-2e"]},
    "neuroscience.evidence": {"domain": "neuroscience-neurology", "subject": "neuroscience-neurology.clinical-boundaries", "sources": ["ninds-brain-basics", "ncbi-neuroscience-2e"]}
}


STAGE_EXPLANATIONS = {
    "premise_set": "the premises are enumerated with their scope and no hidden premise is silently added",
    "formalization": "natural-language claims are mapped to a declared formal representation",
    "validity_check": "the proposed inference form is checked independently of whether its premises are true",
    "derivation": "each conclusion step follows from the formal premises and admitted rules",
    "warrant": "the conclusion is released only with the derivation and premise conditions attached",
    "observations": "the observed cases and collection process remain explicit",
    "sample_assessment": "sample selection, size, representativeness, and measurement quality are evaluated",
    "pattern": "a candidate regularity is separated from random variation and artifact",
    "generalization_strength": "support beyond observed cases is calibrated rather than treated as necessity",
    "provisional_warrant": "the conclusion remains defeasible and carries uncertainty and counterevidence",
    "observation": "the surprising or unexplained observation is stated without baking in its explanation",
    "candidate_explanations": "multiple live explanations are generated before selection",
    "rival_comparison": "candidate explanations are compared on fit, scope, assumptions, and alternatives",
    "best_explanation": "the best currently available explanation is selected without being promoted to deductive certainty",
    "source_structure": "the source case is represented by roles and relations rather than surface words",
    "mapping": "corresponding roles and relations between structures are made explicit",
    "relevant_similarity": "similarities that support the projected relation are separated from irrelevant resemblance",
    "target_projection": "only mapped structure is projected to the target",
    "qualified_warrant": "the analogical conclusion carries the mapping limits and possible disanalogies",
    "covariation": "the candidate cause and effect are checked for a systematic association",
    "temporal_order": "the cause is required to precede or lawfully co-determine the effect",
    "alternative_control": "confounders, common causes, selection effects, and reverse direction are examined",
    "mechanism": "a process capable of transmitting the effect is represented",
    "causal_warrant": "causal attribution is scoped to the intervention, population, and assumptions supported",
    "actual_case": "the observed world and its evidence are retained separately from simulations",
    "intervention": "the counterfactual change is declared rather than smuggled in as observation",
    "similarity_control": "non-target conditions are held fixed according to an explicit comparison rule",
    "difference_making": "the outcome difference attributable to the declared change is computed or traced",
    "counterfactual_warrant": "the conclusion is labeled simulated and inherits the model assumptions",
    "possibility_space": "the outcomes and their boundaries are declared before probability is assigned",
    "assignment": "probability mass is assigned under a declared interpretation and information state",
    "coherence": "non-negativity, normalization, and compatible conditioning constraints are checked",
    "update": "new evidence changes assignments through a declared update rule",
    "calibrated_warrant": "probabilistic conclusions retain their numerical uncertainty and calibration evidence",
    "primitive_extraction": "candidate primitives are tested for irreducibility and load-bearing behavior",
    "local_relations": "relations are established locally before a global story is inferred",
    "composition": "validated primitives and local relations are assembled in an explicit order",
    "abstraction": "higher-level structure retains a trace back to the observations and primitives that support it",
    "frame_inventory": "the current frame and plausible alternate frames are named",
    "perspective_shift": "a deliberate change of viewpoint is performed without changing the task's hard requirements",
    "remote_association": "a distant candidate is connected by a structural bridge rather than word proximity",
    "constraint_check": "evidence, safety, permission, and hard task constraints are re-applied",
    "candidate_comparison": "conventional and lateral candidates are compared on usefulness and validity",
    "generation": "more than one candidate is produced before selection",
    "trace": "the operations and source material that produced each candidate remain visible",
    "selection": "candidates are selected by declared value and constraint criteria",
    "spaces": "each contributing conceptual space is represented separately",
    "blend": "mapped structure is combined into a candidate with emergent properties labeled",
    "provenance": "every contribution and transformation remains traceable",
    "hard_constraints": "requirements that cannot be traded away are separated from preferences",
    "soft_preferences": "desirable but negotiable qualities are represented separately",
    "constraint_filter": "any candidate violating a hard constraint is rejected regardless of novelty",
    "novelty": "distance from known candidates is measured without assuming difference is value",
    "value": "usefulness and fitness to the declared purpose are evaluated",
    "pareto_comparison": "non-dominated novelty-value tradeoffs remain visible instead of collapsing prematurely",
    "original_requirements": "the initial problem and its obligations remain the reference boundary",
    "frames": "multiple representations of the problem are generated",
    "comparison": "frames are compared for retained requirements, insight, and tractability",
    "left": "one side of the tension is represented without caricature",
    "right": "the other side of the tension is represented without erasure",
    "tension": "the incompatibility or tradeoff between the sides is stated",
    "bridge": "a candidate transformation addresses both sides through an explicit mechanism",
    "memory_sources": "memory contributes named candidate material with provenance",
    "recombination": "memory elements are recombined without being treated as evidence for truth",
    "novel_candidate": "the recombination produces a distinguishable candidate",
    "verification": "the candidate is rechecked against evidence, constraints, and intended use",
    "concepts": "key terms are clarified and competing meanings remain distinct",
    "argument": "premises, inferential links, and conclusion are reconstructed charitably",
    "assumptions": "unstated commitments and background conditions are surfaced",
    "objections": "strong objections and counterpositions are tested",
    "qualified_conclusion": "the conclusion states what follows, what remains disputed, and why",
    "rhetorical_situation": "speaker, audience, purpose, exigence, genre, medium, and context are identified",
    "claims_evidence": "claims, evidence, warrants, and omissions are separated",
    "appeals": "credibility, emotion, and argument are analyzed as persuasive means rather than truth guarantees",
    "framing_style": "word choice, arrangement, figures, emphasis, and framing are traced",
    "effects_limitations": "plausible audience effects are distinguished from unknowable intent and measured impact",
    "objects": "the relevant geometric objects and dimensions are explicitly typed",
    "relations": "incidence, distance, angle, adjacency, containment, and orientation are kept distinct",
    "transformation": "a declared transformation maps objects and relations between representations",
    "invariants": "properties preserved by the transformation are identified",
    "boundary": "degenerate cases, dimensional limits, and projection loss are tested",
    "construct": "the psychological construct is defined without reifying a measurement label",
    "operationalization": "the procedure connecting the construct to observations is specified",
    "evidence": "study design, measurement quality, effect uncertainty, and replication are retained",
    "variation": "population, context, developmental, and individual variation remain visible",
    "limitations": "the evidence boundary blocks diagnosis and unjustified person-level inference",
    "structure": "neural structures are identified at the appropriate anatomical scale",
    "function": "functional claims are tied to tasks and evidence rather than inferred from location alone",
    "clinical_boundary": "clinical claims carry date, population, uncertainty, and non-diagnostic scope"
}


def phrase(identifier: str) -> str:
    return identifier.replace("_", " ").replace("-", " ")


def record_base(lane_id: str, context: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "world_id": WORLD_ID,
        "domain_id": context["domain"],
        "subject_id": context["subject"],
        "lanes": [lane_id],
        "scope": "foundation lane anatomy; deeper domain curriculum remains required",
        "limitations": ["This tranche establishes lane structure and controls, not exhaustive subject coverage."],
        "as_of": "2026-09-03",
        "version_boundary": "foundation-v0",
        "tags": ["foundation", "lane-anatomy"]
    }


def build() -> list[dict[str, Any]]:
    lanes = load_json(LANE_CATALOG)["lanes"]
    records: list[dict[str, Any]] = []
    root_ids: dict[str, str] = {}
    for lane in lanes:
        lane_id = lane["id"]
        context = LANE_CONTEXT[lane_id]
        base = record_base(lane_id, context)
        root_id = f"{lane_id}.root"
        root_ids[lane_id] = root_id
        records.append({
            **base,
            "record_id": root_id,
            "record_kind": "concept",
            "epistemic_class": "interpretive" if lane["kind"] == "analysis" else "established",
            "label": lane["label"],
            "statement": lane["definition"],
            "aliases": [lane["label"].lower(), phrase(lane_id)],
            "coverage_axes": ["definitions_scope", "primitives_invariants"],
            "split_group": f"{lane_id}.definition",
            "split": "train",
            "source_ids": context["sources"],
            "tags": ["foundation", "lane-anatomy", "stage-index-0", f"lane-length-{len(lane['required_stages'])}"]
        })

        stage_ids: list[str] = []
        for stage_index, stage in enumerate(lane["required_stages"]):
            stage_id = f"{lane_id}.stage.{stage}"
            stage_ids.append(stage_id)
            records.append({
                **base,
                "record_id": stage_id,
                "record_kind": "concept",
                "epistemic_class": "interpretive" if lane["kind"] in {"analysis", "creativity"} else "established",
                "label": f"{lane['label']}: {phrase(stage)}",
                "statement": f"In {lane['label'].lower()}, {STAGE_EXPLANATIONS[stage]}.",
                "aliases": [phrase(stage), f"{lane['label'].lower()} {phrase(stage)}"],
                "coverage_axes": ["primitives_invariants", "mechanisms_causal_laws", "assumptions_prerequisites"],
                "split_group": f"{lane_id}.stage.{stage}",
                "split": "train",
                "source_ids": context["sources"],
                "tags": ["foundation", "lane-anatomy", f"stage-index-{stage_index + 1}", f"lane-length-{len(lane['required_stages'])}"]
            })
        for stage_index, stage_id in enumerate(stage_ids):
            records.append({
                **base,
                "record_id": f"{lane_id}.membership.{stage_index:02d}",
                "record_kind": "relation",
                "epistemic_class": "interpretive" if lane["kind"] in {"analysis", "creativity"} else "established",
                "label": f"{lane['label']} stage membership {stage_index + 1}",
                "statement": f"The {phrase(stage_id.rsplit('.', 1)[-1])} stage is part of the declared {lane['label'].lower()} lane.",
                "aliases": [],
                "relation": {
                    "source_node": stage_id,
                    "target_node": root_id,
                    "kind": "part_of",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the lane contract is active"],
                    "exceptions": []
                },
                "coverage_axes": ["primitives_invariants", "within_domain_composition"],
                "split_group": f"{lane_id}.membership.{stage_index:02d}",
                "split": "train",
                "source_ids": context["sources"]
            })
        predecessors = [root_id, *stage_ids[:-1]]
        for edge_index, (left, right) in enumerate(zip(predecessors, stage_ids, strict=True)):
            if edge_index == len(stage_ids) - 1:
                edge_split = "sealed_test"
            elif edge_index == len(stage_ids) - 2:
                edge_split = "validation"
            else:
                edge_split = "train"
            edge_id = f"{lane_id}.edge.{edge_index:02d}"
            records.append({
                **base,
                "record_id": edge_id,
                "record_kind": "relation",
                "epistemic_class": "interpretive" if lane["kind"] in {"analysis", "creativity"} else "established",
                "label": f"{lane['label']} stage transition {edge_index + 1}",
                "statement": f"Within {lane['label'].lower()}, {phrase(left.rsplit('.', 1)[-1])} is a prerequisite for {phrase(right.rsplit('.', 1)[-1])}.",
                "aliases": [],
                "relation": {
                    "source_node": left,
                    "target_node": right,
                    "kind": "prerequisite",
                    "polarity": 1,
                    "direction": "forward",
                    "conditions": ["the lane is invoked for a claim-bearing task"],
                    "exceptions": []
                },
                "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition"],
                "split_group": f"{lane_id}.transition.{edge_index:02d}",
                "split": edge_split,
                "source_ids": context["sources"]
            })

        for control_index, control in enumerate(lane["required_controls"]):
            if control_index == 0:
                control_split = "train"
            elif control_index == len(lane["required_controls"]) - 1:
                control_split = "sealed_test"
            else:
                control_split = "validation"
            records.append({
                **base,
                "record_id": f"{lane_id}.control.{control}",
                "record_kind": "synthetic_control",
                "epistemic_class": "synthetic_control",
                "label": f"{lane['label']} control: {phrase(control)}",
                "statement": f"Control case for {lane['label'].lower()}: {phrase(control)} must be detected and must block or qualify unsupported output.",
                "aliases": [phrase(control)],
                "coverage_axes": ["errors_adversarial_misuse", "unknown_abstention"],
                "split_group": f"{lane_id}.control.{control}",
                "split": control_split,
                "source_ids": [],
                "synthetic": True,
                "tags": ["foundation", "negative-control", lane["kind"]]
            })

    bridges = [
        ("thinking.bottom_up", "reasoning.deductive", "enables", "Bottom-up primitive extraction enables a deductive lane to declare rather than assume its premises."),
        ("geometry.structural", "reasoning.analogical", "enables", "Structural geometry enables analogy to match relations and invariants instead of surface vocabulary."),
        ("reasoning.abductive", "reasoning.causal", "qualifies", "Abduction proposes explanations; causal controls qualify which explanation may receive causal warrant."),
        ("reasoning.probabilistic", "reasoning.inductive", "supports", "Probabilistic calibration supports the strength assigned to an inductive generalization."),
        ("reasoning.counterfactual", "reasoning.causal", "clarifies", "A controlled counterfactual clarifies whether a candidate cause makes a difference under declared assumptions."),
        ("thinking.lateral", "creativity.problem_framing", "enables", "Lateral perspective shifts enable alternate problem frames while the original requirements remain fixed."),
        ("creativity.constraint_based", "rhetoric.analysis", "qualifies", "Constraint checks qualify persuasive rewrites so rhetorical force cannot trade away factual or task requirements."),
        ("philosophy.analysis", "rhetoric.analysis", "clarifies", "Philosophical argument reconstruction clarifies the distinction between inferential support and persuasive effect."),
        ("psychology.evidence", "rhetoric.analysis", "qualifies", "Psychological evidence qualifies claims about audience effects and blocks unsupported mind-reading."),
        ("neuroscience.evidence", "psychology.evidence", "qualifies", "Neuroscience can constrain psychological mechanism claims without reducing constructs to brain-location labels."),
        ("geometry.structural", "thinking.bottom_up", "supports", "Objects, relations, transformations, and invariants support bottom-up composition across domains.")
    ]
    for index, (left, right, relation, statement) in enumerate(bridges):
        left_context = LANE_CONTEXT[left]
        sources = sorted(set(left_context["sources"] + LANE_CONTEXT[right]["sources"]))
        records.append({
            **record_base(left, left_context),
            "record_id": f"bridge.foundation.{index:02d}",
            "lanes": [left, right],
            "record_kind": "relation",
            "epistemic_class": "interpretive" if "rhetoric" in right or "philosophy" in left else "established",
            "label": f"Foundation bridge {left} to {right}",
            "statement": statement,
            "aliases": [],
            "relation": {
                "source_node": root_ids[left],
                "target_node": root_ids[right],
                "kind": relation,
                "polarity": 1,
                "direction": "forward",
                "conditions": ["both lanes are admitted by the task geometry"],
                "exceptions": ["proximity alone does not authorize cross-lane transfer"]
            },
            "coverage_axes": ["cross_domain_composition", "mechanisms_causal_laws"],
            "split_group": f"bridge.foundation.{index:02d}",
            "split": "cross_domain_holdout" if index % 3 == 2 else "train",
            "source_ids": sources,
            "tags": ["foundation", "cross-lane-bridge"]
        })
    return sorted(records, key=lambda record: record["record_id"])


def main() -> int:
    records = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records),
        encoding="utf-8"
    )
    counts: dict[str, int] = {}
    for record in records:
        counts[record["split"]] = counts.get(record["split"], 0) + 1
    print(f"wrote {OUTPUT} with {len(records)} records: {dict(sorted(counts.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
