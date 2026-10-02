#!/usr/bin/env python3
"""Author the standalone abductive reasoning world (pilot reasoning world, 2026-10-02).

Abduction reasons backward from an observed effect, through the past cone of known
causal structure, to candidate causes; it tests rivals by their differing predictions
and holds the best explanation provisionally. This world encodes that method as
directed structure (how to move), not domain content (what is connected); domain
content comes from a general world such as physical-causation-v0.
"""

from __future__ import annotations

import collections
import json
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT

OUTPUT = ROOT / "curricula" / "reasoning-abductive" / "foundations.jsonl"
WORLD = "reasoning-abductive-v0"
PREFIX = "abd"
LANES = ["reasoning.abductive"]
SOURCES = ["sep-abduction", "sep-scientific-discovery"]
NEGATIVE = {"inhibits", "prevents", "contradicts", "undercuts", "counterexample"}
LIMITATIONS = [
    "Abduction yields provisional explanations, never deductive certainty.",
    "The method depends on the completeness and accuracy of the background causal knowledge it searches.",
    "Statements are original structured summaries of the cited sources.",
]

# (id, label, statement, aliases, subject)
CONCEPTS = [
    ("surprising-observation", "Surprising observation", "An observed effect that current expectations did not predict and that calls for an explanation.", [], "philosophy.science"),
    ("observation-confirmation", "Confirming the observation is real", "Checking that the effect actually occurred and is not a misreading before explaining it.", [], "philosophy.science"),
    ("observation-error", "Observation error", "A misread instrument, illusion or mistaken report that makes an effect seem to exist.", [], "philosophy.science"),
    ("evidence-reliability", "Reliability of the evidence", "How trustworthy the instruments, observers and records behind an observation are.", [], "philosophy.science"),
    ("effect-description", "Precise description of the effect", "Stating exactly what happened, when, where and how much, so that candidate causes can be matched to it.", [], "philosophy.science"),
    ("background-causal-knowledge", "Background causal knowledge", "Known cause-and-effect relations, such as a general causal world, that say which causes produce which effects.", [], "philosophy.science"),
    ("backward-search", "Backward search for causes", "Tracing back from the effect through known causal structure to every cause that could produce it; the past cone of the effect.", ["past cone search"], "philosophy.science"),
    ("temporal-precedence", "Cause precedes effect", "Only events occurring before the effect can be candidate causes of it.", [], "philosophy.logic"),
    ("causal-access", "Causal access to the effect", "A candidate cause must be able to reach the effect through some mechanism and contact.", [], "philosophy.science"),
    ("candidate-explanations", "Candidate explanations", "The set of causes that, if present, would produce the observed effect.", [], "philosophy.science"),
    ("explanatory-fit", "Explanatory fit", "A candidate explains the observation only if it makes the observation expected, not merely compatible.", [], "philosophy.science"),
    ("multiple-sufficient-causes", "Multiple sufficient causes", "Different causes can each produce the same effect on their own, as rain and a sprinkler can each wet a lawn.", [], "philosophy.science"),
    ("rival-explanations", "Rival explanations", "Two or more candidates that each fit the observation so far.", [], "philosophy.science"),
    ("forward-consequence-check", "Forward consequence check", "Running each candidate cause forward to list every effect it would produce, not only the observed one.", [], "philosophy.logic"),
    ("predicted-side-effects", "Predicted side effects", "Further effects a candidate cause would also produce if it were present.", [], "philosophy.science"),
    ("discriminating-prediction", "Discriminating prediction", "A further consequence that rival explanations predict differently.", [], "philosophy.science"),
    ("targeted-check", "Targeted check for evidence", "Deliberately looking for the observation that would separate the rivals.", [], "philosophy.science"),
    ("discriminating-evidence", "Discriminating evidence", "An observation that one rival predicted and another ruled out.", [], "philosophy.science"),
    ("missing-side-effect", "Missing predicted side effect", "The absence of an effect that a candidate cause requires, which counts against that candidate.", [], "philosophy.science"),
    ("rival-elimination", "Rival elimination", "Rejecting candidates whose predictions failed against the evidence.", [], "philosophy.science"),
    ("prior-plausibility", "Prior plausibility of a cause", "How common or likely a cause is in this kind of situation before the new evidence; the base rate.", ["base rate"], "philosophy.science"),
    ("explanatory-scope", "Scope of an explanation", "How many of the observed facts an explanation accounts for at once.", [], "philosophy.science"),
    ("explanatory-simplicity", "Simplicity of an explanation", "Requiring fewer independent assumptions or unobserved causes.", [], "philosophy.science"),
    ("background-coherence", "Coherence with background knowledge", "Agreement of a candidate with well-established causal knowledge.", [], "philosophy.science"),
    ("explanation-testability", "Testability of an explanation", "An explanation that makes checkable predictions that could prove it wrong.", [], "philosophy.science"),
    ("specific-mechanism", "Specific causal mechanism", "A candidate that names how the cause produces the effect, step by step.", [], "philosophy.science"),
    ("best-explanation", "Best available explanation", "The surviving candidate that accounts for the evidence better than its rivals; inference to the best explanation.", ["inference to the best explanation"], "philosophy.science"),
    ("provisional-acceptance", "Provisional acceptance", "Holding the best explanation as tentative and open to revision rather than as proven.", [], "philosophy.science"),
    ("new-contrary-evidence", "New contrary evidence", "A later observation the accepted explanation did not predict or ruled out.", [], "philosophy.science"),
    ("explanation-revision", "Explanation revision", "Reopening the set of candidates when contrary evidence appears.", [], "philosophy.science"),
    ("evidential-tie", "Tie between rivals", "Rivals that the available evidence cannot yet separate; underdetermination.", ["underdetermination"], "philosophy.science"),
    ("suspended-judgement", "Suspended judgement", "Declining to name a best explanation while rivals remain tied, and saying what would separate them.", [], "philosophy.science"),
    ("no-fitting-candidate", "No fitting candidate cause", "A situation in which no cause in background knowledge fits the observation.", [], "philosophy.science"),
    ("knowledge-gap", "Gap in background knowledge", "Missing causal knowledge that may hide the true cause.", [], "philosophy.science"),
    ("novel-hypothesis", "Novel hypothesis proposal", "Proposing a cause not yet in background knowledge; a creative step that must then be tested.", [], "philosophy.science"),
    ("common-cause", "Common cause of two observations", "One cause producing two observed effects, which can make the effects look causally linked to each other.", [], "philosophy.science"),
    ("coincidence", "Coincidence hypothesis", "The possibility that two observations co-occurred by chance with no causal link.", [], "philosophy.science"),
    ("controlled-intervention", "Controlled intervention test", "Changing a suspected cause deliberately while holding other factors fixed to see whether the effect follows.", [], "philosophy.science"),
    ("deduction-contrast", "Deductive certainty", "Deduction guarantees its conclusion when its premises are true; abduction never does.", [], "philosophy.logic"),
    ("induction-contrast", "Inductive generalisation", "Induction generalises a pattern from many cases; abduction explains a particular observation.", [], "philosophy.logic"),
]

# (id, source, target, kind, statement, condition, exception)
RELATIONS = [
    ("observation-confirmation", "surprising-observation", "observation-confirmation", "prerequisite", "A surprising observation makes confirming the observation is real a prerequisite step before explaining it.", "the observation could be mistaken", ""),
    ("reliability-confirmation", "evidence-reliability", "observation-confirmation", "enables", "Reliability of the evidence enables confirming the observation is real.", "independent instruments or observers are available", ""),
    ("error-observation", "observation-error", "surprising-observation", "undercuts", "Observation error undercuts a surprising observation by showing the effect may not exist.", "the error source is plausible", ""),
    ("confirmation-description", "observation-confirmation", "effect-description", "enables", "Confirming the observation is real enables a precise description of the effect.", "the effect was actually observed", ""),
    ("description-search", "effect-description", "backward-search", "enables", "A precise description of the effect enables a backward search for causes.", "the description states what, when, where and how much", ""),
    ("knowledge-search", "background-causal-knowledge", "backward-search", "enables", "Background causal knowledge enables a backward search for causes through known cause-effect links.", "the knowledge covers the domain of the effect", "outside the known domain the search finds nothing"),
    ("search-candidates", "backward-search", "candidate-explanations", "causes", "A backward search for causes causes the set of candidate explanations to be listed.", "the search reaches every known cause of the effect", ""),
    ("precedence-candidates", "temporal-precedence", "candidate-explanations", "prerequisite", "Cause precedes effect is a prerequisite for admitting anything into the candidate explanations.", "the timing of events is known", ""),
    ("access-candidates", "causal-access", "candidate-explanations", "prerequisite", "Causal access to the effect is a prerequisite for admitting a cause into the candidate explanations.", "the mechanism of contact is known", ""),
    ("multiple-rivals", "multiple-sufficient-causes", "rival-explanations", "causes", "Multiple sufficient causes cause rival explanations for the same effect.", "more than one known cause can produce the effect", ""),
    ("candidates-fit", "candidate-explanations", "explanatory-fit", "prerequisite", "Candidate explanations must each pass explanatory fit as a prerequisite for staying in contention.", "the candidate is evaluated against the precise description", ""),
    ("candidates-rivals", "candidate-explanations", "rival-explanations", "transforms_to", "Candidate explanations transform into rival explanations once more than one passes explanatory fit.", "at least two candidates fit", ""),
    ("rivals-forward", "rival-explanations", "forward-consequence-check", "prerequisite", "Rival explanations make a forward consequence check a prerequisite for choosing between them.", "the rivals still tie on the original observation", ""),
    ("forward-sideeffects", "forward-consequence-check", "predicted-side-effects", "causes", "A forward consequence check causes the predicted side effects of each candidate to be listed.", "each candidate is run forward through causal knowledge", ""),
    ("sideeffects-discriminating", "predicted-side-effects", "discriminating-prediction", "enables", "Predicted side effects enable a discriminating prediction where the rivals differ.", "the rivals predict different side effects", "rivals with identical side effects stay tied"),
    ("discriminating-check", "discriminating-prediction", "targeted-check", "enables", "A discriminating prediction enables a targeted check for evidence.", "the predicted effect can be observed", ""),
    ("check-evidence", "targeted-check", "discriminating-evidence", "causes", "A targeted check for evidence causes discriminating evidence to be found or ruled out.", "the check is carried out honestly and recorded", ""),
    ("evidence-elimination", "discriminating-evidence", "rival-elimination", "causes", "Discriminating evidence causes rival elimination of candidates whose predictions failed.", "the evidence is reliable", ""),
    ("missing-elimination", "missing-side-effect", "rival-elimination", "causes", "A missing predicted side effect causes rival elimination of the candidate that required it.", "the side effect would have been noticed if present", ""),
    ("missing-candidates", "missing-side-effect", "candidate-explanations", "inhibits", "A missing predicted side effect inhibits the candidate explanations that required it.", "the absence is confirmed", ""),
    ("elimination-best", "rival-elimination", "best-explanation", "enables", "Rival elimination enables a best available explanation to emerge.", "at least one candidate survives", ""),
    ("fit-best", "explanatory-fit", "best-explanation", "prerequisite", "Explanatory fit is a prerequisite for a best available explanation.", "the explanation makes the observation expected", ""),
    ("prior-best", "prior-plausibility", "best-explanation", "supports", "Prior plausibility of a cause supports choosing it as the best available explanation when evidence ties.", "base rates for the situation are known", ""),
    ("scope-best", "explanatory-scope", "best-explanation", "supports", "Scope of an explanation supports it as the best available explanation.", "it accounts for more of the facts", ""),
    ("simplicity-best", "explanatory-simplicity", "best-explanation", "supports", "Simplicity of an explanation supports it as the best available explanation.", "rivals fit equally well", ""),
    ("coherence-best", "background-coherence", "best-explanation", "supports", "Coherence with background knowledge supports a candidate as the best available explanation.", "the background knowledge is well established", ""),
    ("testability-best", "explanation-testability", "best-explanation", "supports", "Testability of an explanation supports it as the best available explanation.", "its predictions can be checked", ""),
    ("mechanism-best", "specific-mechanism", "best-explanation", "supports", "A specific causal mechanism supports a candidate as the best available explanation.", "the mechanism is consistent with background knowledge", ""),
    ("best-provisional", "best-explanation", "provisional-acceptance", "transforms_to", "A best available explanation transforms into provisional acceptance, never into proof.", "the evidence supports it", ""),
    ("contrary-provisional", "new-contrary-evidence", "provisional-acceptance", "undercuts", "New contrary evidence undercuts provisional acceptance of the explanation.", "the contrary evidence is reliable", ""),
    ("contrary-revision", "new-contrary-evidence", "explanation-revision", "causes", "New contrary evidence causes explanation revision.", "the evidence conflicts with the accepted explanation", ""),
    ("revision-search", "explanation-revision", "backward-search", "causes", "Explanation revision causes a renewed backward search for causes including the new evidence.", "the candidate set is reopened", ""),
    ("tie-suspend", "evidential-tie", "suspended-judgement", "causes", "A tie between rivals causes suspended judgement rather than an arbitrary choice.", "no further evidence is yet available", ""),
    ("tie-best", "evidential-tie", "best-explanation", "prevents", "A tie between rivals prevents a best available explanation from being named.", "the rivals fit all evidence equally", ""),
    ("suspend-check", "suspended-judgement", "targeted-check", "enables", "Suspended judgement enables a targeted check for evidence by naming what would separate the rivals.", "a discriminating prediction exists", ""),
    ("nocandidate-gap", "no-fitting-candidate", "knowledge-gap", "predicts", "No fitting candidate cause predicts a gap in background knowledge.", "the observation is confirmed real", ""),
    ("gap-novel", "knowledge-gap", "novel-hypothesis", "enables", "A gap in background knowledge enables a novel hypothesis proposal.", "the proposal is marked as untested", ""),
    ("novel-testability", "novel-hypothesis", "explanation-testability", "prerequisite", "A novel hypothesis proposal needs testability of the explanation as a prerequisite before it can be accepted.", "the hypothesis is not in background knowledge", ""),
    ("search-nocandidate", "backward-search", "no-fitting-candidate", "causes", "A backward search for causes that finds nothing causes the no fitting candidate cause situation.", "the search was complete over known causes", ""),
    ("commoncause-rivals", "common-cause", "rival-explanations", "causes", "A common cause of two observations causes a rival explanation to the claim that one observation caused the other.", "the two observations co-occur", ""),
    ("coincidence-rivals", "coincidence", "rival-explanations", "causes", "The coincidence hypothesis causes a rival explanation that must be ruled out for co-occurring observations.", "the co-occurrence is rare or brief", ""),
    ("intervention-elimination", "controlled-intervention", "rival-elimination", "causes", "A controlled intervention test causes rival elimination by showing which suspected cause changes the effect.", "the cause can be manipulated safely", ""),
    ("intervention-commoncause", "controlled-intervention", "common-cause", "undercuts", "A controlled intervention test undercuts a spurious link explained by a common cause.", "the intervention holds the common cause fixed", ""),
    ("precedence-elimination", "temporal-precedence", "rival-elimination", "causes", "Cause precedes effect causes rival elimination of candidates that occurred after the effect.", "event timing is reliable", ""),
    ("knowledge-coherence", "background-causal-knowledge", "background-coherence", "grounds", "Background causal knowledge grounds coherence with background knowledge.", "the knowledge is well established", ""),
    ("mechanism-forward", "specific-mechanism", "forward-consequence-check", "enables", "A specific causal mechanism enables a forward consequence check by saying what else must happen.", "the mechanism is stated step by step", ""),
    ("deduction-provisional", "deduction-contrast", "provisional-acceptance", "contradicts", "Deductive certainty contradicts provisional acceptance: an abductive conclusion must never be stated with deductive certainty.", "the conclusion came from abduction", ""),
    ("induction-prior", "induction-contrast", "prior-plausibility", "grounds", "Inductive generalisation grounds the prior plausibility of a cause through observed frequencies.", "enough comparable cases have been observed", ""),
    ("reliability-error", "evidence-reliability", "observation-error", "inhibits", "Reliability of the evidence inhibits observation error.", "instruments are calibrated", ""),
    ("description-fit", "effect-description", "explanatory-fit", "enables", "A precise description of the effect enables a strict explanatory fit test.", "the description includes quantities and timing", ""),
    ("sideeffects-missing", "predicted-side-effects", "missing-side-effect", "enables", "Predicted side effects enable a missing predicted side effect to be noticed.", "the side effects are looked for", ""),
    ("best-testability", "best-explanation", "discriminating-prediction", "predicts", "A best available explanation predicts further discriminating predictions that can test it.", "it states a mechanism", ""),
    ("prior-rivals", "prior-plausibility", "rival-explanations", "qualifies", "Prior plausibility of a cause qualifies how strongly each of the rival explanations is held before testing.", "base rates differ between rivals", ""),
    ("revision-candidates", "explanation-revision", "candidate-explanations", "causes", "Explanation revision causes new candidate explanations to be considered.", "the contrary evidence points to causes previously ignored", ""),
    ("access-elimination", "causal-access", "rival-elimination", "causes", "Lack of causal access to the effect causes rival elimination of a candidate that could not have reached it.", "the candidate was physically or causally isolated", ""),
    ("scope-simplicity", "explanatory-scope", "explanatory-simplicity", "qualifies", "Scope of an explanation qualifies simplicity: the simpler rival wins only if it explains as much.", "rivals differ in both scope and simplicity", ""),
    ("observation-search", "surprising-observation", "backward-search", "enables", "A surprising observation enables a backward search for causes.", "the observation is confirmed", ""),
    ("candidates-forward", "candidate-explanations", "forward-consequence-check", "enables", "Candidate explanations enable a forward consequence check on each candidate.", "background causal knowledge covers the candidates", ""),
    ("check-missing", "targeted-check", "missing-side-effect", "causes", "A targeted check for evidence causes a missing predicted side effect to be established.", "the predicted effect is absent", ""),
    ("best-revision", "best-explanation", "explanation-revision", "inhibits", "A well-tested best available explanation inhibits needless explanation revision without contrary evidence.", "no contrary evidence has appeared", ""),
    ("gap-suspend", "knowledge-gap", "suspended-judgement", "causes", "A gap in background knowledge causes suspended judgement when no tested candidate remains.", "the novel hypothesis is still untested", ""),
]

# Myths and fallacies: (id, label, statement, target)
MYTHS = [
    ("affirming-consequent", "Fallacy: affirming the consequent", "From 'rain wets the lawn' and 'the lawn is wet' it does not follow that it rained; a sprinkler also wets the lawn.", "candidate-explanations"),
    ("premature-closure", "Fallacy: premature closure", "Accepting the first candidate that fits, without listing rivals, misses other sufficient causes.", "rival-explanations"),
    ("abduction-as-proof", "Fallacy: treating the best explanation as proven", "The best available explanation is provisional; new evidence can overturn it.", "provisional-acceptance"),
    ("ignoring-base-rates", "Fallacy: ignoring base rates", "A rare cause that fits slightly better can still be less likely than a common cause that fits well.", "prior-plausibility"),
    ("post-hoc", "Fallacy: after it, therefore because of it", "An event that merely came first is not thereby the cause; it must also have causal access and fit.", "temporal-precedence"),
    ("confirmation-bias", "Fallacy: seeking only confirming evidence", "Looking only for evidence a favoured explanation predicts skips the discriminating checks that could refute it.", "targeted-check"),
    ("unfalsifiable-explanation", "Fallacy: explanations that fit any outcome", "An explanation compatible with every possible observation predicts nothing and explains nothing.", "explanation-testability"),
    ("correlation-cause", "Fallacy: correlation proves causation", "Two observations moving together may share a common cause or co-occur by chance.", "common-cause"),
]

BOUNDARIES = [
    ("not-deduction", "Boundary: abduction is not deduction", "Abductive conclusions remain defeasible even when every premise is true.", "best-explanation"),
    ("not-induction", "Boundary: abduction is not induction", "Explaining one observation differs from generalising a pattern across many.", "candidate-explanations"),
    ("closed-knowledge", "Boundary: limited by background knowledge", "Abduction can only find causes present in the knowledge searched; unknown causes need novel hypotheses.", "backward-search"),
    ("creative-step", "Boundary: novel hypotheses belong to the creative lane", "Proposing causes outside known structure is creative and must be tested before it joins causal knowledge.", "novel-hypothesis"),
]

# Worked examples bridging to physical causation: (id, label, statement, clarified concepts)
EXAMPLES = [
    ("wet-lawn", "Wet lawn in the morning", "The lawn is wet. Candidates: overnight rain, a sprinkler, dew. Rain predicts wet streets and roofs too; a sprinkler predicts a dry street; dew predicts wet cars. Checking the street separates them.", ["multiple-sufficient-causes", "discriminating-prediction"]),
    ("ball-on-floor", "Ball found on the floor", "A ball lies on the floor below a shelf. Candidates: it rolled off, someone dropped it, it was placed there. A slight tilt in the shelf and a scuff at the edge favour rolling; a forward check asks what each would leave behind.", ["backward-search", "forward-consequence-check"]),
    ("fogged-window", "Fogged inside of a window", "Moisture on the inside of a cold window. Candidates: condensation from humid indoor air, a leak. Condensation predicts droplets that clear as the glass warms; a leak predicts water at the frame edge.", ["candidate-explanations", "targeted-check"]),
    ("dead-circuit", "Lights out in one room", "One room's lights fail. Candidates: a blown fuse, a failed bulb, a power cut. A power cut predicts other rooms dark; one bulb predicts other lamps working; a fuse predicts the whole circuit dead.", ["predicted-side-effects", "rival-elimination"]),
    ("rust-spot", "Rust spot on a car", "A rust spot appears on a car door. Background knowledge says rust needs water and oxygen at exposed iron, so the search looks for a scratch through the paint, then checks for salt exposure.", ["background-causal-knowledge", "specific-mechanism"]),
    ("cracked-glass", "Cracked drinking glass", "A glass cracked after hot water was poured in. Candidates: thermal shock, an earlier flaw. Thermal shock predicts a crack starting where hot met cold; an old flaw predicts a crack from a chip.", ["explanatory-fit", "discriminating-evidence"]),
    ("puddle-kitchen", "Puddle on the kitchen floor", "A puddle under the fridge. Candidates: defrost drain blocked, spilled drink, leaking pipe. Taste and stickiness, recurrence after wiping, and location separate them; holding judgement until one check is done.", ["evidential-tie", "suspended-judgement"]),
    ("no-sound-space", "Silent film of an explosion in space", "A documentary claims a loud explosion was heard in space. Background knowledge that sound needs a medium rules the candidate out; the best explanation is added sound effects.", ["causal-access", "background-coherence"]),
]

CONTROLS = [
    ("random-cause", "Any earlier event explains the effect", "An earlier event must not be accepted as the cause merely because it came first."),
    ("single-candidate", "Only one cause is ever possible", "A single listed candidate must not be treated as the only possible cause."),
    ("proof-claim", "The best explanation is certain", "An abductive conclusion must not be reported as certain."),
    ("unknown-forced", "Always name a cause", "An explanation must not be forced when no candidate fits; the answer is unknown."),
]


def node(identifier: str) -> str:
    return f"{PREFIX}.{identifier}"


def base(record_id: str, subject: str, split: str, kind: str, axes: list[str], sources: list[str] | None = None,
         epistemic: str = "established") -> dict[str, Any]:
    return {
        "schema_version": 1, "record_id": record_id, "world_id": WORLD, "domain_id": "philosophy",
        "subject_id": subject, "lanes": LANES, "record_kind": kind, "epistemic_class": epistemic,
        "coverage_axes": axes, "source_ids": sorted(set(SOURCES if sources is None else sources)),
        "scope": "Abductive reasoning as a method: backward search, rivals, discrimination, provisional acceptance",
        "limitations": LIMITATIONS, "as_of": "2026-10-02", "version_boundary": WORLD,
        "split_group": record_id, "split": split, "tags": ["reasoning-abductive", "pilot"],
    }


def split_for(index: int) -> str:
    if index % 13 == 0:
        return "cross_domain_holdout"
    if index % 11 == 0:
        return "sealed_test"
    if index % 7 == 0:
        return "validation"
    return "train"


def relation(record_id: str, subject: str, split: str, src: str, dst: str, kind: str, statement: str,
             condition: str, exception: str, axes: list[str], label: str) -> dict[str, Any]:
    return {
        **base(record_id, subject, split, "relation", axes),
        "label": label, "statement": statement, "aliases": [],
        "relation": {"source_node": node(src), "target_node": node(dst), "kind": kind,
                     "polarity": -1 if kind in NEGATIVE else 1, "direction": "forward",
                     "conditions": [condition], "exceptions": [exception] if exception else []},
    }


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    subject_of, labels = {}, {}
    records.append({**base(node("root"), "philosophy.science", "train", "concept", ["definitions_scope", "primitives_invariants"]),
                    "label": "Abductive reasoning world",
                    "statement": "Root of the abductive reasoning world: how to move backward from an observed effect to its best provisional explanation.",
                    "aliases": []})
    for index, (identifier, label, statement, aliases, subject) in enumerate(CONCEPTS, start=1):
        subject_of[identifier], labels[identifier] = subject, label
        split = split_for(index)
        records.append({**base(node(identifier), subject, split, "concept",
                               ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"]),
                        "label": label, "statement": statement, "aliases": aliases})
        records.append(relation(f"{PREFIX}.membership.{identifier}", subject, split_for(index + 3), identifier, "root",
                                "part_of", f"{label} is a distinct step or element of the abductive reasoning world.",
                                f"{label.lower()} is used within an abductive inquiry", "",
                                ["primitives_invariants", "within_domain_composition"], f"{label} membership"))
    for _identifier, src, dst, *_rest in RELATIONS:
        assert src in subject_of and dst in subject_of, _identifier
    splitter = RelationSplitter([r[3] for r in RELATIONS], cross_plan=[r[0].startswith("bridge-") for r in RELATIONS])
    for identifier, src, dst, kind, statement, condition, exception in RELATIONS:
        axes = {"mechanisms_causal_laws", "within_domain_composition",
                {"predicts": "deductions_predictions_execution", "transforms_to": "representations_transformations",
                 "prerequisite": "assumptions_prerequisites", "supports": "uncertainty_competing_hypotheses",
                 "undercuts": "uncertainty_competing_hypotheses"}.get(kind, "primitives_invariants")}
        records.append(relation(f"{PREFIX}.relation.{identifier}", subject_of[src], splitter.split(kind), src, dst, kind,
                                statement, condition, exception, sorted(axes), identifier.replace("-", " ")))
    splits = ["train", "validation", "sealed_test", "train"]
    for index, (identifier, label, statement, target) in enumerate(MYTHS):
        myth = f"fallacy-{identifier}"
        axes = ["errors_adversarial_misuse", "exceptions_boundaries"] + (["history_versions"] if identifier == "post-hoc" else [])
        records.append({**base(node(myth), subject_of[target], splits[index % 4], "counterexample", axes),
                        "label": label, "statement": statement, "aliases": []})
        records.append(relation(f"{PREFIX}.relation.counter-{identifier}", subject_of[target], splits[index % 4], myth, target,
                                "counterexample", f"{label} is a counterexample showing how {labels[target].lower()} is misused.",
                                f"the fallacy is applied to {labels[target].lower()}", "", axes,
                                f"counterexample {identifier.replace('-', ' ')}"))
    for index, (identifier, label, statement, target) in enumerate(BOUNDARIES):
        b = f"boundary-{identifier}"
        records.append({**base(node(b), subject_of[target], splits[index % 4], "boundary",
                               ["exceptions_boundaries", "assumptions_prerequisites"]),
                        "label": label, "statement": statement, "aliases": []})
        records.append(relation(f"{PREFIX}.relation.qualifies-{identifier}", subject_of[target], splits[index % 4], b, target,
                                "qualifies", f"{label} qualifies how far {labels[target].lower()} can be trusted.",
                                f"the boundary applies to {labels[target].lower()}", "",
                                ["exceptions_boundaries", "assumptions_prerequisites"], f"boundary {identifier.replace('-', ' ')}"))
    example_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, label, statement, clarified) in enumerate(EXAMPLES):
        ex = f"example-{identifier}"
        split = example_splits[index % 4]
        records.append({**base(node(ex), "philosophy.science", split, "worked_example",
                               ["applications_toolchains", "deductions_predictions_execution", "cross_domain_composition"]),
                        "label": label, "statement": statement, "aliases": []})
        records.append(relation(f"{PREFIX}.example-membership.{identifier}", "philosophy.science", split, ex, "root",
                                "part_of", f"The {label.lower()} example is part of the abductive reasoning world.",
                                "the example is an everyday physical case", "",
                                ["applications_toolchains", "within_domain_composition"], f"{label} membership"))
        for target in clarified:
            records.append(relation(f"{PREFIX}.relation.clarifies-{identifier}-{target}", "philosophy.science", split, ex,
                                    target, "clarifies", f"The {label.lower()} example clarifies {labels[target].lower()} in practice.",
                                    f"the everyday case exercises {labels[target].lower()}", "",
                                    ["applications_toolchains", "deductions_predictions_execution"],
                                    f"example clarifies {target.replace('-', ' ')}"))
    control_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, label, statement) in enumerate(CONTROLS):
        records.append({**base(node(f"control.{identifier}"), "philosophy.science", control_splits[index % 4],
                               "synthetic_control", ["unknown_abstention", "errors_adversarial_misuse"], [], "synthetic_control"),
                        "label": label, "statement": statement, "aliases": [], "synthetic": True,
                        "tags": ["negative-control", "reasoning-abductive"]})
    return sorted(records, key=lambda r: r["record_id"])


def main() -> int:
    records = build()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in records), encoding="utf-8")
    print(f"wrote {OUTPUT} with {len(records)} records")
    print("splits:", dict(sorted(collections.Counter(r["split"] for r in records).items())))
    print("kinds:", dict(sorted(collections.Counter(r["record_kind"] for r in records).items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
