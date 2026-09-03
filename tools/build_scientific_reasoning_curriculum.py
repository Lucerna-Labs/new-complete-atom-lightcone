#!/usr/bin/env python3
"""Author scientific theories, hypotheses, prediction, and evidence curricula."""

from __future__ import annotations

import json
from typing import Any

from registry_lib import ROOT
from curriculum_split import RelationSplitter


OUTPUT = ROOT / "curricula" / "scientific-reasoning" / "foundations.jsonl"
WORLD = "scientific-reasoning-v0"
LANES = [
    "reasoning.deductive", "reasoning.inductive", "reasoning.abductive",
    "reasoning.analogical", "reasoning.causal", "reasoning.counterfactual",
    "reasoning.probabilistic", "thinking.bottom_up", "thinking.lateral"
]
SOURCES = [
    "sep-scientific-discovery", "sep-inductive-logic", "sep-abduction",
    "sep-causal-models", "sep-counterfactuals", "sep-probability",
    "national-academies-reproducibility", "nist-measurement-uncertainty"
]


CONCEPTS = [
    ("root", "Scientific reasoning", "Scientific reasoning connects observations, measurements, hypotheses, models, theories, predictions, tests, uncertainty, and revision while preserving the distinction between evidence and proposal.", "research-scientific-method.theories"),
    ("phenomenon", "Phenomenon", "A phenomenon is an observed or measurable occurrence or regularity selected for investigation.", "research-scientific-method.question-formation"),
    ("observation", "Observation", "An observation is a recorded interaction with a phenomenon under stated conditions and instruments.", "research-scientific-method.observational"),
    ("measurement", "Measurement", "Measurement assigns a value or category to a measurand through a declared procedure, reference, and uncertainty model.", "research-scientific-method.measurement"),
    ("measurand", "Measurand", "A measurand is the quantity or property intended to be measured and must be distinguished from the instrument reading.", "research-scientific-method.measurement"),
    ("uncertainty", "Measurement uncertainty", "Measurement uncertainty characterizes dispersion or limits associated with values reasonably attributable to a measurand.", "research-scientific-method.uncertainty"),
    ("error", "Measurement error", "Measurement error is the difference between a measured value and a reference value under a declared model and is not synonymous with uncertainty.", "research-scientific-method.measurement"),
    ("operational-definition", "Operational definition", "An operational definition specifies how a variable or construct is observed, measured, or manipulated.", "research-scientific-method.measurement"),
    ("data", "Research data", "Research data are recorded observations, measurements, derived values, or annotations with provenance and processing history.", "research-scientific-method.open-science"),
    ("question", "Research question", "A research question states the phenomenon, population or system, relationship, and answerable uncertainty without presupposing its conclusion.", "research-scientific-method.question-formation"),
    ("hypothesis", "Scientific hypothesis", "A scientific hypothesis is a proposed explanation or relationship that yields testable consequences and possible defeaters.", "research-scientific-method.hypotheses"),
    ("alternative-hypothesis", "Alternative hypothesis", "An alternative hypothesis represents a distinct live account capable of explaining or predicting relevant evidence.", "research-scientific-method.hypotheses"),
    ("auxiliary-assumption", "Auxiliary assumption", "An auxiliary assumption connects a hypothesis to a prediction through background theory, instruments, initial conditions, or analysis choices.", "research-scientific-method.hypotheses"),
    ("prediction", "Prediction", "A prediction states an expected observable consequence under specified conditions before the relevant outcome is used for evaluation.", "forecasting-prediction.model-building"),
    ("retrodiction", "Retrodiction", "A retrodiction derives expectations about already occurred but independently unobserved evidence and must avoid using that evidence during model construction.", "forecasting-prediction.model-building"),
    ("test", "Scientific test", "A test compares predictions with observations under a protocol capable of distinguishing at least some rival accounts.", "research-scientific-method.experimental"),
    ("control", "Scientific control", "A control isolates alternative explanations, background change, measurement artifact, or treatment-independent behavior.", "research-scientific-method.experimental"),
    ("falsifier", "Potential falsifier", "A potential falsifier is an admissible outcome that would count against a hypothesis given its auxiliaries and scope.", "research-scientific-method.hypotheses"),
    ("evidence", "Evidence", "Evidence is information that changes rational support among hypotheses under a declared inferential model.", "research-scientific-method.uncertainty"),
    ("confirmation", "Confirmation", "Confirmation increases support for a hypothesis relative to prior support or alternatives without establishing certainty.", "research-scientific-method.hypotheses"),
    ("disconfirmation", "Disconfirmation", "Disconfirmation lowers support or reveals a failed prediction while retaining uncertainty about which hypothesis or auxiliary failed.", "research-scientific-method.hypotheses"),
    ("explanation", "Scientific explanation", "A scientific explanation accounts for phenomena through laws, mechanisms, models, causes, or unifying structure under a declared explanatory standard.", "research-scientific-method.theories"),
    ("mechanism", "Mechanism", "A mechanism specifies organized entities, activities, interactions, and conditions capable of producing a phenomenon.", "research-scientific-method.theories"),
    ("law", "Scientific law", "A scientific law expresses a stable regularity or relationship within a stated domain and does not by itself explain why the relation holds.", "research-scientific-method.theories"),
    ("model", "Scientific model", "A scientific model represents selected structure to explain, predict, simulate, or measure while exposing idealizations and validity limits.", "research-scientific-method.theories"),
    ("theory", "Scientific theory", "A scientific theory is an organized explanatory framework connecting concepts, mechanisms, laws, models, and evidence across a domain.", "research-scientific-method.theories"),
    ("idealization", "Idealization", "An idealization deliberately simplifies or distorts selected features to make reasoning tractable and requires a known domain of adequacy.", "research-scientific-method.theories"),
    ("scope", "Domain of validity", "A domain of validity states the systems, scales, conditions, precision, and purposes within which a claim or model is supported.", "research-scientific-method.theories"),
    ("causal-identification", "Causal identification", "Causal identification states the assumptions and design features that let an intervention effect be distinguished from association.", "research-scientific-method.causal-inference"),
    ("counterfactual-model", "Counterfactual model", "A counterfactual model evaluates outcomes under a declared intervention while keeping simulated claims separate from observations.", "research-scientific-method.causal-inference"),
    ("probability-model", "Probability model", "A probability model defines events, assignments, conditioning, and interpretation for representing uncertainty.", "probability-statistics.probability-foundations"),
    ("bayesian-update", "Bayesian evidence update", "A Bayesian evidence update uses a prior and likelihood to obtain a posterior under the assumed probability model.", "probability-statistics.bayesian-inference"),
    ("calibration", "Predictive calibration", "Predictive calibration compares stated probabilities with outcome frequencies or other declared calibration targets across comparable cases.", "forecasting-prediction.calibration"),
    ("scoring-rule", "Forecast scoring rule", "A scoring rule evaluates probabilistic forecasts and should be selected before inspecting outcomes used for evaluation.", "forecasting-prediction.scoring"),
    ("base-rate", "Base rate", "A base rate summarizes outcome frequency in a relevant reference class and constrains plausible predictions.", "forecasting-prediction.base-rates"),
    ("scenario", "Scenario", "A scenario is a coherent conditional future or system state used to explore consequences, not a probability claim unless probabilities are separately justified.", "forecasting-prediction.scenario"),
    ("robustness", "Robustness", "A result is robust when it persists across justified variations in data, model, assumptions, methods, or measurement.", "research-scientific-method.reproducibility"),
    ("reproducibility", "Computational reproducibility", "Computational reproducibility obtains consistent computational results using the same data, code, methods, and analysis conditions.", "research-scientific-method.reproducibility"),
    ("replicability", "Replicability", "Replicability concerns consistent results from a new study aimed at the same scientific question with newly collected evidence.", "research-scientific-method.reproducibility"),
    ("meta-analysis", "Meta-analysis", "Meta-analysis combines comparable study estimates under an explicit model of variation, bias, and dependence.", "research-scientific-method.meta-analysis"),
    ("systematic-review", "Systematic review", "A systematic review uses a predeclared search, selection, appraisal, and synthesis process to reduce selective evidence use.", "research-scientific-method.meta-analysis"),
    ("anomaly", "Anomaly", "An anomaly is an observation that strains current expectations and may reflect error, auxiliary failure, scope failure, or a need for theory change.", "research-scientific-method.theory-change"),
    ("underdetermination", "Underdetermination", "Evidence underdetermines a conclusion when multiple incompatible accounts remain consistent with the available observations and assumptions.", "research-scientific-method.uncertainty"),
    ("theory-change", "Theory change", "Theory change compares empirical adequacy, explanatory reach, coherence, problem solving, assumptions, and novel predictions rather than using novelty alone.", "research-scientific-method.theory-change"),
    ("consensus", "Scientific consensus", "Scientific consensus summarizes convergent expert judgment and evidence at a time; it is strong social-epistemic evidence but remains revisable and domain-specific.", "research-scientific-method.theories"),
    ("open-science", "Open science", "Open science practices expose methods, materials, data, code, provenance, and limitations where rights, privacy, and safety permit.", "research-scientific-method.open-science")
]


RELATIONS = [
    ("phenomenon-question", "phenomenon", "question", "enables", "Observed phenomena enable answerable research questions to be framed."),
    ("question-hypothesis", "question", "hypothesis", "enables", "A research question enables candidate hypotheses to be proposed."),
    ("observation-data", "observation", "data", "causes", "Recorded observations produce research data with provenance."),
    ("measurand-measurement", "measurand", "measurement", "prerequisite", "The intended measurand must be specified before interpreting a measurement."),
    ("operation-measurement", "operational-definition", "measurement", "enables", "An operational definition enables a measurement procedure."),
    ("measurement-uncertainty", "measurement", "uncertainty", "requires", "An interpreted measurement requires an uncertainty account."),
    ("error-uncertainty", "error", "uncertainty", "qualifies", "Measurement error and uncertainty are related but non-identical quantities."),
    ("hypothesis-prediction", "hypothesis", "prediction", "enables", "A hypothesis plus auxiliaries enables observable predictions."),
    ("auxiliary-prediction", "auxiliary-assumption", "prediction", "qualifies", "Auxiliary assumptions qualify what a hypothesis predicts."),
    ("prediction-test", "prediction", "test", "prerequisite", "A prediction must be fixed before its test outcome is interpreted."),
    ("control-test", "control", "test", "supports", "Controls support discrimination among causal or methodological alternatives."),
    ("falsifier-test", "falsifier", "test", "qualifies", "A potential falsifier specifies which outcomes count against the tested account."),
    ("test-evidence", "test", "evidence", "causes", "A completed test produces evidence under its design and measurement assumptions."),
    ("evidence-confirm", "evidence", "confirmation", "supports", "Evidence can increase support for a hypothesis relative to alternatives."),
    ("evidence-disconfirm", "evidence", "disconfirmation", "supports", "Evidence can lower support for a hypothesis or its auxiliaries."),
    ("alternatives-abduction", "alternative-hypothesis", "explanation", "enables", "Live alternative hypotheses enable comparative explanatory inference."),
    ("mechanism-explanation", "mechanism", "explanation", "supports", "A supported mechanism strengthens a how-or-why explanation."),
    ("law-model", "law", "model", "supports", "A law can constrain a model within its domain."),
    ("model-prediction", "model", "prediction", "enables", "A model enables predictions under specified inputs and conditions."),
    ("model-idealization", "idealization", "model", "qualifies", "Idealizations qualify a model's domain and interpretation."),
    ("scope-theory", "scope", "theory", "qualifies", "A theory's warranted claims are bounded by its domain of validity."),
    ("theory-model", "model", "theory", "part_of", "Models can be components of a broader scientific theory."),
    ("law-theory", "law", "theory", "part_of", "Laws and regularities can be components of a broader theory."),
    ("mechanism-theory", "mechanism", "theory", "part_of", "Mechanisms can be components of a broader theory."),
    ("causal-counterfactual", "causal-identification", "counterfactual-model", "enables", "Causal identification assumptions enable intervention counterfactuals."),
    ("probability-bayes", "probability-model", "bayesian-update", "enables", "A coherent probability model enables a Bayesian update."),
    ("base-rate-probability", "base-rate", "probability-model", "supports", "A relevant base rate supports prior or predictive probability assignments."),
    ("probability-calibration", "probability-model", "calibration", "predicts", "Repeated probability statements predict calibration behavior across comparable cases."),
    ("scoring-calibration", "scoring-rule", "calibration", "measures", "A proper scoring rule measures probabilistic forecast performance."),
    ("scenario-probability", "scenario", "probability-model", "qualifies", "A coherent scenario is not automatically probable; probability requires separate support."),
    ("reproduce-robust", "reproducibility", "robustness", "supports", "Computational reproducibility supports trust in an analysis pipeline but is only one robustness check."),
    ("replicate-robust", "replicability", "robustness", "supports", "Successful replication supports robustness across newly collected evidence."),
    ("review-meta", "systematic-review", "meta-analysis", "prerequisite", "A systematic evidence-selection process precedes defensible quantitative synthesis."),
    ("meta-consensus", "meta-analysis", "consensus", "supports", "Meta-analysis can support consensus when study comparability, bias, and dependence are handled."),
    ("anomaly-theory", "anomaly", "theory-change", "enables", "Persistent well-validated anomalies can motivate theory revision or replacement."),
    ("underdetermination-humility", "underdetermination", "confirmation", "qualifies", "Underdetermination qualifies how strongly confirmation selects one account."),
    ("discovery-lateral", "alternative-hypothesis", "hypothesis", "enables", "Lateral generation expands candidate hypotheses before evidence-based selection."),
    ("bottom-up-theory", "observation", "theory", "supports", "Bottom-up scientific reasoning composes observations, mechanisms, and models toward theory without skipping their evidence chain."),
    ("open-reproducibility", "open-science", "reproducibility", "supports", "Accessible code, data, and methods support computational reproducibility where rights and safety allow."),
    ("retrodiction-leakage", "retrodiction", "prediction", "qualifies", "Retrodiction is only an out-of-sample test when the target evidence was not used to construct the account.")
]


CONTROLS = [
    ("hypothesis-fact", "Hypothesis is not fact", "A plausible or elegant hypothesis must not be emitted as an established finding."),
    ("theory-guess", "Theory is not a casual guess", "A scientific theory must not be described as merely an unsupported guess."),
    ("law-explanation", "Law is not full explanation", "A fitted regularity must not be assumed to identify its mechanism."),
    ("model-reality", "Model is not reality", "A model must not be treated as exhaustive identity with the target system."),
    ("correlation-cause", "Association is not causal identification", "Observed association must not cross into a causal claim without design and assumptions."),
    ("pvalue-proof", "Statistical threshold is not proof", "Crossing a statistical threshold must not be treated as certainty, practical importance, or absence of bias."),
    ("nonreplication-fraud", "Non-replication is not automatically fraud", "A non-replication must be diagnosed across method, population, power, variation, and error before attributing misconduct."),
    ("reproducible-true", "Reproducible computation is not truth", "Reproducing the same computation proves pipeline consistency, not that its data or assumptions are correct."),
    ("consensus-infallible", "Consensus is not infallibility", "Scientific consensus must be treated as strong current evidence, not an unrevisable authority."),
    ("single-study", "Single-study overreach", "One study must not establish universal mechanism, population coverage, or causal effect beyond its design."),
    ("scenario-forecast", "Scenario is not forecast probability", "A coherent scenario must not receive a probability merely because it is imaginable."),
    ("forecast-certainty", "Forecast is not certainty", "A forecast must retain uncertainty, calibration limits, and reference class."),
    ("retrodiction-leak", "Retrodiction leakage", "Evidence used to build a model must not be presented as an independent successful prediction."),
    ("auxiliary-erasure", "Auxiliary-assumption erasure", "A failed prediction must not be attributed uniquely to the headline hypothesis when auxiliary assumptions could have failed."),
    ("unknown-domain", "Unknown-domain abstention", "The scientific lane must abstain when no sourced model, mechanism, or evidence covers the question's domain.")
]


def base(identifier: str, subject: str, split: str, kind: str, epistemic: str, sources: list[str]) -> dict[str, Any]:
    domain = "forecasting-prediction" if subject.startswith("forecasting-") else "probability-statistics" if subject.startswith("probability-") else "research-scientific-method"
    return {
        "schema_version": 1,
        "record_id": f"science-reasoning.v0.{identifier}",
        "world_id": WORLD,
        "domain_id": domain,
        "subject_id": subject,
        "lanes": LANES,
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "mechanisms_causal_laws", "uncertainty_competing_hypotheses", "deductions_predictions_execution"],
        "source_ids": sources,
        "scope": "cross-domain scientific-reasoning foundation",
        "limitations": ["Discipline-specific theories and evidence require their own worlds and versioned sources."],
        "as_of": "2026-09-03",
        "version_boundary": "scientific-reasoning-v0",
        "split_group": f"science-reasoning.v0.{identifier}",
        "split": split,
        "tags": ["science", "hypothesis", "prediction", "evidence"]
    }


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, (identifier, label, statement, subject) in enumerate(CONCEPTS):
        records.append({
            **base(identifier, subject, "validation" if index and index % 17 == 0 else "train", "concept", "established", SOURCES),
            "label": label,
            "statement": statement,
            "aliases": [label.lower()]
        })
        if identifier != "root":
            records.append({
                **base(f"membership-{identifier}", subject, "train", "relation", "established", SOURCES),
                "label": f"{label} scientific-reasoning membership",
                "statement": f"{label} is a distinct component of the scientific-reasoning world.",
                "aliases": [],
                "relation": {"source_node": f"science-reasoning.v0.{identifier}", "target_node": "science-reasoning.v0.root", "kind": "part_of", "polarity": 1, "direction": "forward", "conditions": [], "exceptions": []},
                "coverage_axes": ["primitives_invariants", "within_domain_composition"]
            })
    normalized_kinds = ["prerequisite" if kind == "requires" else kind for _identifier, _source, _target, kind, _statement in RELATIONS]
    splitter = RelationSplitter(normalized_kinds)
    for index, (identifier, source, target, kind, statement) in enumerate(RELATIONS):
        normalized_kind = "prerequisite" if kind == "requires" else kind
        split = splitter.split(normalized_kind, cross_requested=index % 17 == 0)
        records.append({
            **base(identifier, "research-scientific-method.theories", split, "relation", "established", SOURCES),
            "label": identifier.replace("-", " "),
            "statement": statement,
            "aliases": [],
            "relation": {
                "source_node": f"science-reasoning.v0.{source}",
                "target_node": f"science-reasoning.v0.{target}",
                "kind": normalized_kind,
                "polarity": 1,
                "direction": "forward",
                "conditions": ["scope, evidence, and assumptions are explicit"],
                "exceptions": []
            },
            "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"]
        })
    for index, (identifier, label, statement) in enumerate(CONTROLS):
        control_split = "train" if index == 0 else "sealed_test" if index == len(CONTROLS) - 1 or index % 2 else "validation"
        records.append({
            **base(identifier, "research-scientific-method.uncertainty", control_split, "synthetic_control", "synthetic_control", []),
            "label": label,
            "statement": statement,
            "aliases": [label.lower()],
            "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
            "synthetic": True,
            "tags": ["science", "negative-control"]
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
