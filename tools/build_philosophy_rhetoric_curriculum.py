#!/usr/bin/env python3
"""Author philosophy and rhetorical-analysis foundation worlds from scratch."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "philosophy-rhetoric" / "foundations.jsonl"
WORLD = "philosophy-rhetoric-v0"
PHIL_LANES = ["philosophy.analysis", "reasoning.deductive", "reasoning.abductive", "thinking.bottom_up"]
RHET_LANES = ["rhetoric.analysis", "philosophy.analysis", "reasoning.abductive"]
PHIL_SOURCES = ["sep-argument", "open-logic-project"]
RHET_SOURCES = ["sep-aristotle-rhetoric", "sep-argument"]


PHILOSOPHY = [
    ("root", "Philosophical analysis", "Philosophical analysis clarifies concepts, reconstructs arguments, exposes assumptions, tests objections, and reports qualified conclusions without turning a position into fact.", "philosophy.epistemology"),
    ("claim", "Claim", "A claim is a proposition presented for acceptance and must be separated from the evidence or reasoning offered for it.", "philosophy.logic"),
    ("premise", "Premise", "A premise is a stated or reconstructed proposition from which an argument asks an audience to reason.", "philosophy.logic"),
    ("conclusion", "Conclusion", "A conclusion is the proposition an argument presents as following from its premises.", "philosophy.logic"),
    ("inference", "Inference", "An inference is the transition from premises to a conclusion under a declared standard of support.", "philosophy.logic"),
    ("validity", "Deductive validity", "A deductive argument is valid when no interpretation makes all premises true and its conclusion false.", "philosophy.logic"),
    ("soundness", "Soundness", "A deductive argument is sound when it is valid and all of its premises are true.", "philosophy.logic"),
    ("consistency", "Consistency", "A set of propositions is consistent when they can all be true together under the relevant logic.", "philosophy.logic"),
    ("entailment", "Entailment", "Premises entail a conclusion when every admissible model satisfying the premises also satisfies the conclusion.", "philosophy.logic"),
    ("counterexample", "Counterexample", "A counterexample supplies an admissible case that defeats a universal claim or alleged entailment.", "philosophy.logic"),
    ("inductive-support", "Inductive support", "Inductive support raises confidence beyond observed cases without guaranteeing the conclusion.", "philosophy.epistemology"),
    ("abductive-explanation", "Abductive explanation", "Abductive reasoning compares live explanations and selects a provisional best explanation rather than a necessary conclusion.", "philosophy.science"),
    ("analogy", "Analogical argument", "An analogical argument projects a relation from a source to a target and is only as strong as the relevant structural mapping and disanalogy controls.", "philosophy.logic"),
    ("causal-claim", "Causal claim", "A causal claim requires more than temporal association and must retain assumptions about intervention, confounding, mechanism, and population.", "philosophy.science"),
    ("counterfactual", "Counterfactual", "A counterfactual evaluates a declared alternative relative to a similarity or intervention rule and remains distinct from observation.", "philosophy.metaphysics"),
    ("probability", "Probability interpretation", "A probability claim requires a declared event space, formal calculus, and interpretation such as frequency, propensity, or degree of belief.", "philosophy.science"),
    ("bayesian-update", "Bayesian update", "A Bayesian update combines a prior, likelihood, and evidence under a coherent probability model; it does not manufacture evidence.", "philosophy.science"),
    ("explanation", "Explanation", "An explanation relates an explanandum to an account of why or how it occurs and is evaluated for fit, mechanism, scope, and alternatives.", "philosophy.science"),
    ("hypothesis", "Hypothesis", "A hypothesis is a testable proposed account whose predictions and possible defeaters remain explicit.", "philosophy.science"),
    ("model", "Scientific model", "A model represents selected structure for a purpose and must expose idealizations, omissions, domain, and failure conditions.", "philosophy.science"),
    ("assumption", "Assumption", "An assumption is a commitment required by a claim or inference and must be surfaced when it affects warrant.", "philosophy.epistemology"),
    ("relevance", "Premise relevance", "A premise is relevant when changing or removing it can affect support for the conclusion under the argument's mechanism.", "philosophy.logic"),
    ("burden", "Burden of proof", "A burden of proof identifies who must provide support and what standard applies; failure to meet it is not proof of the opposite.", "philosophy.epistemology"),
    ("ambiguity", "Ambiguity", "Ambiguity occurs when a term, structure, or scope supports multiple readings that can change an argument.", "philosophy.language"),
    ("equivocation", "Equivocation", "Equivocation changes a term's operative meaning across an inference while presenting it as stable.", "philosophy.language"),
    ("fallacy", "Fallacy", "A fallacy is a context-sensitive defect in reasoning; assigning a label does not replace reconstructing the actual inferential failure.", "philosophy.logic"),
    ("straw-man", "Straw-man error", "A straw man weakens or distorts a position and then criticizes the substitute rather than the strongest defensible version.", "philosophy.logic"),
    ("steelmanning", "Steelmanning", "Steelmanning reconstructs the strongest defensible version of a position while preserving disagreement and not adding claims its advocate rejects.", "philosophy.epistemology"),
    ("dialectic", "Dialectic", "Dialectic advances inquiry through an explicit thesis, serious objection, reasoned response, and revision or retained disagreement.", "philosophy.epistemology"),
    ("disagreement", "Epistemic disagreement", "Epistemic disagreement requires separating shared evidence, differing priors, standards, concepts, and values before diagnosing the dispute.", "philosophy.epistemology"),
    ("testimony", "Testimony", "Testimony can provide evidence through a source whose access, sincerity, competence, and independence require evaluation.", "philosophy.epistemology"),
    ("justification", "Epistemic justification", "Justification concerns whether a belief is supported by appropriate reasons or processes and remains distinct from the belief being true by luck.", "philosophy.epistemology"),
    ("skepticism", "Skeptical challenge", "A skeptical challenge tests whether claimed knowledge survives alternatives, regress, circularity, or unreliable access.", "philosophy.epistemology"),
    ("humility", "Epistemic humility", "Epistemic humility calibrates confidence to evidence, expertise, model limits, and live counterarguments rather than requiring indecision.", "philosophy.epistemology"),
    ("consequence", "Consequentialist consideration", "A consequentialist analysis compares affected outcomes while retaining uncertainty, distribution, and measurement limits.", "philosophy.ethics"),
    ("duty", "Deontological consideration", "A deontological analysis tests duties, rights, permissions, and constraints that are not automatically traded against aggregate outcomes.", "philosophy.ethics"),
    ("virtue", "Virtue-ethical consideration", "A virtue-ethical analysis examines character, practical wisdom, motives, and cultivated dispositions in context.", "philosophy.ethics"),
    ("moral-uncertainty", "Moral uncertainty", "Moral uncertainty retains disagreement among ethical frameworks instead of disguising one framework as neutral fact.", "philosophy.ethics"),
    ("mind", "Philosophy of mind", "Philosophy of mind analyzes consciousness, representation, intentionality, embodiment, and the relation between mental and physical descriptions.", "philosophy.mind"),
    ("language", "Philosophy of language", "Philosophy of language analyzes meaning, reference, use, speech acts, context, and interpretation.", "philosophy.language"),
    ("metaphysics", "Metaphysical analysis", "Metaphysical analysis examines categories, identity, modality, dependence, persistence, and what a theory commits us to.", "philosophy.metaphysics"),
    ("identity", "Identity and persistence", "Identity analysis distinguishes numerical identity, qualitative similarity, criteria of persistence, and context-dependent individuation.", "philosophy.metaphysics"),
    ("technology-ai", "Philosophy of technology and AI", "Philosophy of technology and AI examines agency, responsibility, values, power, epistemic limits, and sociotechnical consequences.", "philosophy.technology-ai"),
    ("aesthetics", "Aesthetic analysis", "Aesthetic analysis examines experience, interpretation, form, expression, value, and institutional or historical context without reducing judgment to preference alone.", "philosophy.aesthetics"),
    ("law", "Philosophy of law", "Philosophy of law examines legal authority, interpretation, obligation, rights, institutions, and the relation between law and morality.", "philosophy.law"),
    ("religion", "Philosophy of religion", "Philosophy of religion analyzes arguments, experience, language, evil, faith, and plural traditions without assigning religious authority.", "philosophy.religion"),
    ("phenomenology", "Phenomenological analysis", "Phenomenological analysis describes structures of lived experience while keeping first-person description distinct from causal neuroscience.", "philosophy.phenomenology")
]


RHETORIC = [
    ("root", "Rhetorical analysis", "Rhetorical analysis examines how a message addresses an audience in context through claims, evidence, appeals, framing, arrangement, style, medium, and omission without confusing persuasion with truth.", "rhetoric-argumentation.rhetorical-situation"),
    ("speaker", "Speaker or rhetor", "The speaker is the attributed source persona of a message; the text may construct an ethos that differs from the person's full identity.", "rhetoric-argumentation.rhetorical-situation"),
    ("audience", "Audience", "An audience is the actual, intended, invoked, or excluded group whose knowledge, values, and constraints shape rhetorical choices.", "rhetoric-argumentation.rhetorical-situation"),
    ("purpose", "Rhetorical purpose", "Purpose identifies what a message attempts to make an audience believe, feel, value, or do.", "rhetoric-argumentation.rhetorical-situation"),
    ("exigence", "Exigence", "Exigence is the situation or problem that calls the discourse into being as represented by the message.", "rhetoric-argumentation.rhetorical-situation"),
    ("context", "Rhetorical context", "Context includes historical, cultural, institutional, interpersonal, and material conditions relevant to interpretation.", "rhetoric-argumentation.rhetorical-situation"),
    ("genre", "Genre", "Genre supplies recurring expectations for purpose, structure, evidence, style, and audience interaction while remaining historically changeable.", "rhetoric-argumentation.rhetorical-situation"),
    ("medium", "Medium", "Medium shapes what can be expressed, perceived, circulated, interacted with, and preserved.", "rhetoric-argumentation.digital"),
    ("kairos", "Kairos", "Kairos concerns the timeliness and situational fitness of a rhetorical act.", "rhetoric-argumentation.rhetorical-situation"),
    ("ethos", "Ethos", "Ethos is persuasive force arising from perceived character, credibility, competence, identification, or trustworthiness; it is not proof of a claim.", "rhetoric-argumentation.ethos-pathos-logos"),
    ("pathos", "Pathos", "Pathos is persuasive force arising through audience emotion, disposition, or value; emotional force does not establish factual truth.", "rhetoric-argumentation.ethos-pathos-logos"),
    ("logos", "Logos", "Logos is persuasive force arising from reasons, examples, evidence, and apparent inferential relations and must still be tested for validity and soundness.", "rhetoric-argumentation.ethos-pathos-logos"),
    ("enthymeme", "Enthymeme", "An enthymeme is a rhetorical argument whose premises or conclusion may rely on audience-supplied commitments rather than all being explicit.", "rhetoric-argumentation.argument-structure"),
    ("topos", "Topos", "A topos is a reusable place or pattern for discovering potentially persuasive considerations, not a guarantee that the resulting argument is true.", "rhetoric-argumentation.invention"),
    ("invention", "Invention", "Invention discovers claims, evidence, arguments, examples, and frames available for a rhetorical situation.", "rhetoric-argumentation.invention"),
    ("arrangement", "Arrangement", "Arrangement orders material to control emphasis, expectation, memory, and response.", "rhetoric-argumentation.arrangement"),
    ("style", "Style", "Style comprises lexical, syntactic, figurative, rhythmic, and tonal choices that shape interpretation and response.", "rhetoric-argumentation.style"),
    ("delivery", "Delivery", "Delivery includes voice, timing, embodiment, interface, and presentation choices through which a message reaches an audience.", "rhetoric-argumentation.style"),
    ("framing", "Framing", "Framing selects and organizes aspects of a situation so some interpretations, causes, values, or remedies become more salient.", "rhetoric-argumentation.framing"),
    ("metaphor", "Rhetorical metaphor", "Metaphor maps structure and associations from one domain to another, enabling insight while also importing selective emphasis and omission.", "rhetoric-argumentation.style"),
    ("narrative", "Rhetorical narrative", "Narrative organizes agents, events, causality, conflict, and resolution to make a position intelligible or compelling.", "rhetoric-argumentation.framing"),
    ("repetition", "Repetition", "Repetition can increase salience, familiarity, rhythm, and memorability without increasing evidential support.", "rhetoric-argumentation.style"),
    ("omission", "Rhetorical omission", "Omission excludes facts, alternatives, agents, or uncertainty and must be analyzed relative to relevance and genre constraints.", "rhetoric-argumentation.framing"),
    ("visual", "Visual rhetoric", "Visual rhetoric uses composition, scale, color, typography, sequence, and image-text relations to shape attention and interpretation.", "rhetoric-argumentation.visual"),
    ("digital", "Digital rhetoric", "Digital rhetoric includes platform affordances, algorithms, links, interaction, remix, metrics, and networked circulation.", "rhetoric-argumentation.digital"),
    ("scientific", "Scientific rhetoric", "Scientific rhetoric analyzes how methods, uncertainty, evidence, figures, genre, and disciplinary norms present a knowledge claim.", "rhetoric-argumentation.scientific"),
    ("technical", "Technical rhetoric", "Technical rhetoric adapts specialized information to users, tasks, risks, media, and operational constraints.", "rhetoric-argumentation.technical"),
    ("legal", "Legal rhetoric", "Legal rhetoric uses authority, precedent, text, analogy, policy, fact characterization, and procedural posture within a jurisdiction.", "rhetoric-argumentation.legal"),
    ("political", "Political rhetoric", "Political rhetoric constructs publics, identities, problems, values, responsibility, and possible action under institutional and power conditions.", "rhetoric-argumentation.political"),
    ("propaganda", "Propaganda", "Propaganda systematically organizes communication to advance a political or ideological objective, often through selective evidence, repetition, identity, and emotional framing.", "rhetoric-argumentation.propaganda"),
    ("manipulation", "Manipulative rhetoric", "Manipulative rhetoric attempts to bypass or distort an audience's reflective agency through deception, coercive pressure, concealment, or exploitative targeting.", "rhetoric-argumentation.propaganda"),
    ("effect", "Rhetorical effect", "A rhetorical effect is a measured or carefully qualified change in attention, interpretation, feeling, judgment, or action; textual analysis alone cannot prove actual audience effect.", "rhetoric-argumentation.rhetorical-situation"),
    ("intent", "Rhetorical intent", "Intent is an attributed purpose that requires evidence beyond merely observing a textual effect or device.", "rhetoric-argumentation.rhetorical-situation")
]


RELATIONS = [
    ("p-premise-inference", "p.premise", "p.inference", "enables", "Premises supply the explicit inputs to an inference."),
    ("p-inference-conclusion", "p.inference", "p.conclusion", "supports", "An inference supplies the claimed support relation to a conclusion."),
    ("p-validity-entailment", "p.validity", "p.entailment", "clarifies", "Deductive validity can be stated as model-theoretic entailment."),
    ("p-validity-soundness", "p.validity", "p.soundness", "prerequisite", "Validity is necessary but not sufficient for soundness."),
    ("p-premise-soundness", "p.premise", "p.soundness", "prerequisite", "Soundness also requires true premises."),
    ("p-counterexample-validity", "p.counterexample", "p.validity", "contradicts", "One admissible countermodel refutes an alleged deductive validity."),
    ("p-assumption-inference", "p.assumption", "p.inference", "qualifies", "Hidden assumptions qualify what an inference actually establishes."),
    ("p-ambiguity-equivocation", "p.ambiguity", "p.equivocation", "enables", "Unresolved ambiguity enables equivocation across an inference."),
    ("p-equivocation-soundness", "p.equivocation", "p.soundness", "undercuts", "Equivocation undercuts a soundness claim by changing the represented premise."),
    ("p-fallacy-inference", "p.fallacy", "p.inference", "undercuts", "A demonstrated fallacy undercuts the specific inferential support it diagnoses."),
    ("p-straw-steelman", "p.steelmanning", "p.straw-man", "prevents", "A faithful strongest-version reconstruction prevents the straw-man substitution."),
    ("p-objection-dialectic", "p.dialectic", "p.humility", "supports", "Serious objection and revision support calibrated epistemic humility."),
    ("p-testimony-justification", "p.testimony", "p.justification", "supports", "Reliable testimony can support justification when source access and independence are adequate."),
    ("p-skepticism-justification", "p.skepticism", "p.justification", "qualifies", "Skeptical alternatives test the boundary of a justification claim."),
    ("p-hypothesis-explanation", "p.hypothesis", "p.explanation", "enables", "A hypothesis supplies a candidate explanatory account."),
    ("p-abduction-hypothesis", "p.abductive-explanation", "p.hypothesis", "supports", "Abduction ranks explanatory hypotheses provisionally."),
    ("p-model-hypothesis", "p.model", "p.hypothesis", "clarifies", "A model makes a hypothesis's selected structure and idealizations explicit."),
    ("p-counterfactual-causal", "p.counterfactual", "p.causal-claim", "clarifies", "Controlled counterfactual dependence can clarify a causal claim under explicit assumptions."),
    ("p-probability-induction", "p.probability", "p.inductive-support", "grounds", "A probability model can quantify inductive support without making it deductive."),
    ("p-bayes-probability", "p.bayesian-update", "p.probability", "part_of", "Bayesian updating is one coherent use of probability under declared modeling choices."),
    ("p-ethical-uncertainty", "p.moral-uncertainty", "p.consequence", "qualifies", "Moral uncertainty prevents consequentialist analysis from silently standing for all ethical analysis."),
    ("p-duty-consequence", "p.duty", "p.consequence", "qualifies", "Duties and rights can constrain outcome aggregation rather than simply adding another consequence."),
    ("p-phenomenology-neuro", "p.phenomenology", "p.mind", "clarifies", "First-person phenomenological structure contributes to philosophy of mind without itself establishing a neural cause."),
    ("r-situation-purpose", "r.exigence", "r.purpose", "enables", "A represented exigence helps explain the message's rhetorical purpose."),
    ("r-audience-style", "r.audience", "r.style", "qualifies", "Audience knowledge and values qualify effective and ethical style choices."),
    ("r-medium-delivery", "r.medium", "r.delivery", "qualifies", "Medium constrains and enables forms of delivery."),
    ("r-context-framing", "r.context", "r.framing", "qualifies", "Historical and institutional context qualifies how a frame functions."),
    ("r-genre-arrangement", "r.genre", "r.arrangement", "qualifies", "Genre expectations shape arrangement without mechanically determining it."),
    ("r-kairos-delivery", "r.kairos", "r.delivery", "qualifies", "Timeliness qualifies how and when a message is delivered."),
    ("r-ethos-speaker", "r.speaker", "r.ethos", "enables", "The message's construction of the speaker enables an ethos appeal."),
    ("r-pathos-effect", "r.pathos", "r.effect", "predicts", "A pathos appeal predicts an audience response but does not prove that response occurred."),
    ("r-logos-enthymeme", "r.enthymeme", "r.logos", "part_of", "Enthymematic argument is one source of logos appeal."),
    ("r-topos-invention", "r.topos", "r.invention", "enables", "Topoi enable systematic discovery of potentially persuasive material."),
    ("r-invention-arrangement", "r.invention", "r.arrangement", "prerequisite", "Discovered material precedes its rhetorical arrangement."),
    ("r-arrangement-emphasis", "r.arrangement", "r.framing", "supports", "Arrangement supports framing by controlling sequence and emphasis."),
    ("r-metaphor-frame", "r.metaphor", "r.framing", "supports", "Metaphor supports a frame by importing selected structure and associations."),
    ("r-narrative-frame", "r.narrative", "r.framing", "supports", "Narrative supports a frame by assigning agents, causes, conflicts, and resolutions."),
    ("r-repetition-evidence", "r.repetition", "p.justification", "contradicts", "Repeated exposure does not by itself increase epistemic justification."),
    ("r-omission-effect", "r.omission", "r.effect", "predicts", "Omission can predict changed interpretation while actual effect still requires audience evidence."),
    ("r-visual-style", "r.visual", "r.style", "implements", "Visual composition, color, and typography implement rhetorical style in visual media."),
    ("r-digital-medium", "r.digital", "r.medium", "part_of", "Digital rhetoric operates through computational and networked media."),
    ("r-scientific-logos", "r.scientific", "r.logos", "supports", "Scientific rhetoric foregrounds methods, evidence, uncertainty, and disciplinary warrants as logos."),
    ("r-technical-purpose", "r.technical", "r.purpose", "qualifies", "Technical rhetoric is qualified by user tasks, risks, and operational outcomes."),
    ("r-propaganda-manipulation", "r.propaganda", "r.manipulation", "enables", "Propaganda can enable manipulation when it employs deception, concealment, or exploitative pressure."),
    ("r-intent-effect", "r.effect", "r.intent", "undercuts", "Observed or inferred effect alone undercuts neither alternative intent nor uncertainty; intent needs separate evidence."),
    ("bridge-argument-rhetoric", "p.inference", "r.logos", "clarifies", "Argument analysis clarifies whether a logos appeal supplies genuine inferential support or only its appearance."),
    ("bridge-truth-persuasion", "p.justification", "r.effect", "qualifies", "Epistemic justification and rhetorical effect are independent dimensions: a claim may be persuasive without being justified or justified without persuading."),
    ("bridge-ambiguity-frame", "p.ambiguity", "r.framing", "qualifies", "Ambiguity can multiply available frames and must be resolved before attributing a single rhetorical effect."),
    ("bridge-ethics-manipulation", "p.duty", "r.manipulation", "inhibits", "Respect for audience agency inhibits deceptive or coercive manipulation even when it could be effective.")
]


CONTROLS = [
    ("p-position-fact", "Position presented as fact", "A philosophical position must not be emitted as settled fact merely because it has a coherent argument."),
    ("p-label-fallacy", "Fallacy-label shortcut", "Naming a fallacy without reconstructing the inferential defect must not count as analysis."),
    ("p-false-consensus", "False consensus", "A disputed philosophical conclusion must retain live objections and status."),
    ("p-authority-proof", "Authority is not proof", "Expert or historical authority can supply testimony but cannot replace the argument or evidence at issue."),
    ("p-is-ought", "Is-ought boundary", "A descriptive premise alone must not silently generate a normative conclusion."),
    ("p-model-reality", "Model-reality conflation", "A useful model must not be treated as an exhaustive identity with its target."),
    ("p-counterfactual-observation", "Counterfactual as observation", "A simulated alternative must not be stored or cited as an observed event."),
    ("r-persuasion-truth", "Persuasion is not truth", "Persuasive force must never be treated as factual or logical warrant."),
    ("r-intent-mindread", "Intent mind-reading", "Textual features alone must not produce a confident claim about an author's private intent."),
    ("r-audience-effect", "Unmeasured audience effect", "A predicted audience response must remain a hypothesis unless reception or experimental evidence measures it."),
    ("r-ethos-authority", "Ethos is not authority", "Credibility cues must not substitute for checking a claim and its evidence."),
    ("r-pathos-false", "Emotion is not falsity", "Emotional language alone must not cause an otherwise supported argument to be dismissed as false."),
    ("r-context-erasure", "Context erasure", "A rhetorical device must not be interpreted without its genre, audience, time, and institutional setting."),
    ("r-propaganda-label", "Propaganda-label shortcut", "Calling a message propaganda without evidence of organized objective, selection, and circulation must not count as analysis."),
    ("r-omission-invention", "Invented omission", "Analysis must not accuse a text of omitting information that is irrelevant or outside its declared scope without argument.")
]


def make_base(identifier: str, domain: str, subject: str, lanes: list[str], sources: list[str], split: str, kind: str, epistemic: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "record_id": identifier,
        "world_id": WORLD,
        "domain_id": domain,
        "subject_id": subject,
        "lanes": lanes,
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"],
        "source_ids": sources,
        "scope": "philosophy and rhetorical-analysis foundation tranche",
        "limitations": ["The exhaustive historical, cultural, and specialist literature remains open in the coverage ledger."],
        "as_of": "2026-09-03",
        "version_boundary": "philosophy-rhetoric-v0",
        "split_group": identifier,
        "split": split,
        "tags": ["foundation", domain]
    }


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for prefix, entries, domain, lanes, sources, root in [
        ("p", PHILOSOPHY, "philosophy", PHIL_LANES, PHIL_SOURCES, "p.root"),
        ("r", RHETORIC, "rhetoric-argumentation", RHET_LANES, RHET_SOURCES, "r.root"),
    ]:
        for index, (identifier, label, statement, subject) in enumerate(entries):
            node_id = f"{prefix}.{identifier}"
            split = "validation" if index and index % 17 == 0 else "train"
            records.append({
                **make_base(node_id, domain, subject, lanes, sources, split, "concept", "interpretive"),
                "label": label,
                "statement": statement,
                "aliases": [label.lower()]
            })
            if node_id != root:
                membership = f"{prefix}.membership.{identifier}"
                records.append({
                    **make_base(membership, domain, subject, lanes, sources, "train", "relation", "interpretive"),
                    "label": f"{label} membership",
                    "statement": f"{label} is a distinct component of the declared {'philosophical' if prefix == 'p' else 'rhetorical'} analysis world.",
                    "aliases": [],
                    "relation": {
                        "source_node": node_id,
                        "target_node": root,
                        "kind": "part_of",
                        "polarity": 1,
                        "direction": "forward",
                        "conditions": [],
                        "exceptions": []
                    },
                    "coverage_axes": ["primitives_invariants", "within_domain_composition"]
                })
    for index, (identifier, source, target, kind, statement) in enumerate(RELATIONS):
        if index % 13 == 0:
            split = "sealed_test"
        elif index % 11 == 0:
            split = "validation"
        elif index % 17 == 0:
            split = "cross_domain_holdout"
        else:
            split = "train"
        domain = "rhetoric-argumentation" if identifier.startswith("r-") else "philosophy"
        sources = RHET_SOURCES if domain == "rhetoric-argumentation" else sorted(set(PHIL_SOURCES + RHET_SOURCES)) if identifier.startswith("bridge-") else PHIL_SOURCES
        records.append({
            **make_base(f"relation.{identifier}", domain, "rhetoric-argumentation.argument-structure" if domain == "rhetoric-argumentation" else "philosophy.logic", sorted(set(PHIL_LANES + RHET_LANES)), sources, split, "relation", "interpretive"),
            "label": identifier.replace("-", " "),
            "statement": statement,
            "aliases": [],
            "relation": {
                "source_node": source,
                "target_node": target,
                "kind": kind,
                "polarity": -1 if kind in {"inhibits", "prevents", "contradicts", "undercuts"} else 1,
                "direction": "forward",
                "conditions": ["the reconstructed context and meanings are held fixed"],
                "exceptions": []
            },
            "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"]
        })
    for index, (identifier, label, statement) in enumerate(CONTROLS):
        is_rhetoric = identifier.startswith("r-")
        domain = "rhetoric-argumentation" if is_rhetoric else "philosophy"
        lanes = RHET_LANES if is_rhetoric else PHIL_LANES
        records.append({
            **make_base(f"control.{identifier}", domain, "rhetoric-argumentation.fallacies" if is_rhetoric else "philosophy.logic", lanes, [], "validation" if index % 2 == 0 else "sealed_test", "synthetic_control", "synthetic_control"),
            "label": label,
            "statement": statement,
            "aliases": [label.lower()],
            "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
            "synthetic": True,
            "tags": ["negative-control", domain]
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

