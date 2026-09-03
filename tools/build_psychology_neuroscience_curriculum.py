#!/usr/bin/env python3
"""Author evidence-sensitive psychology and neuroscience foundation curricula."""

from __future__ import annotations

import json
from typing import Any

from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "psychology-neuroscience" / "foundations.jsonl"
WORLD = "psychology-neuroscience-v0"
PSY_LANES = ["psychology.evidence", "reasoning.inductive", "reasoning.causal", "reasoning.probabilistic"]
NEURO_LANES = ["neuroscience.evidence", "reasoning.causal", "thinking.bottom_up", "geometry.structural"]
PSY_SOURCES = ["openstax-psychology-2e"]
NEURO_SOURCES = ["ninds-brain-basics", "ncbi-neuroscience-2e"]


PSYCHOLOGY = [
    ("root", "Psychological evidence", "Psychological knowledge links constructs to operational measures, study designs, uncertainty, replication, population variation, and explicit non-diagnostic boundaries.", "psychology-cognitive-science.replication"),
    ("construct", "Psychological construct", "A psychological construct is a theoretical attribute used to organize behavior or experience and is not identical to any single measurement.", "psychology-cognitive-science.quantitative"),
    ("operationalization", "Operationalization", "Operationalization specifies the observable procedure used to measure or manipulate a construct.", "psychology-cognitive-science.quantitative"),
    ("reliability", "Measurement reliability", "Reliability concerns consistency of a measurement under defined repetitions or equivalent forms.", "psychology-cognitive-science.quantitative"),
    ("validity", "Measurement validity", "Validity concerns whether evidence supports the intended interpretation and use of a measurement.", "psychology-cognitive-science.quantitative"),
    ("replication", "Replication", "Replication tests whether a reported effect recurs under an explicitly related protocol and population.", "psychology-cognitive-science.replication"),
    ("correlation", "Correlation", "Correlation quantifies association under a measurement model and does not alone identify causal direction.", "psychology-cognitive-science.quantitative"),
    ("experiment", "Randomized experiment", "A randomized experiment can support causal inference when assignment, adherence, measurement, attrition, and interference assumptions are adequate.", "psychology-cognitive-science.quantitative"),
    ("observation-study", "Observational study", "An observational study measures naturally occurring variation and requires explicit control of confounding and selection before causal claims.", "psychology-cognitive-science.quantitative"),
    ("effect-size", "Effect size", "An effect size describes magnitude on a declared scale and must be accompanied by uncertainty and practical context.", "psychology-cognitive-science.quantitative"),
    ("population-variation", "Population and context variation", "Psychological findings can vary across populations, cultures, tasks, development, and settings.", "psychology-cognitive-science.social"),
    ("sensation", "Sensation", "Sensation begins with detection and transduction of physical stimulation by sensory systems.", "psychology-cognitive-science.perception"),
    ("perception", "Perception", "Perception organizes and interprets sensory information using both stimulus structure and prior context.", "psychology-cognitive-science.perception"),
    ("bottom-up-processing", "Bottom-up processing", "Bottom-up processing builds perceptual organization from incoming features and local evidence.", "psychology-cognitive-science.perception"),
    ("top-down-processing", "Top-down processing", "Top-down processing uses expectations, goals, and prior knowledge to influence interpretation.", "psychology-cognitive-science.perception"),
    ("attention", "Attention", "Attention allocates limited processing priority and can alter what is selected without creating the selected evidence.", "psychology-cognitive-science.cognitive"),
    ("working-memory", "Working memory", "Working memory temporarily maintains and manipulates a limited amount of task-relevant information.", "psychology-cognitive-science.cognitive"),
    ("encoding", "Memory encoding", "Encoding transforms an experience or representation into a form that can contribute to later memory.", "psychology-cognitive-science.learning"),
    ("consolidation", "Memory consolidation", "Consolidation comprises processes that stabilize or reorganize memory after initial encoding.", "psychology-cognitive-science.learning"),
    ("retrieval", "Memory retrieval", "Retrieval reconstructs accessible information from cues and can be incomplete or distorted.", "psychology-cognitive-science.learning"),
    ("forgetting", "Forgetting", "Forgetting can reflect decay, interference, retrieval failure, updating, or absent initial encoding and is not one mechanism.", "psychology-cognitive-science.learning"),
    ("classical-conditioning", "Classical conditioning", "Classical conditioning changes responding when predictive relations form between stimuli.", "psychology-cognitive-science.learning"),
    ("operant-conditioning", "Operant conditioning", "Operant conditioning changes behavior as consequences alter future response probability under context.", "psychology-cognitive-science.learning"),
    ("observational-learning", "Observational learning", "Observational learning acquires information or behavior by attending to models and outcomes without requiring direct reinforcement of every act.", "psychology-cognitive-science.learning"),
    ("concept", "Concept", "A concept organizes instances by features, relations, prototypes, exemplars, or theories depending on task and account.", "psychology-cognitive-science.cognitive"),
    ("problem-solving", "Problem solving", "Problem solving represents a current state, goal, operators, constraints, and a search or restructuring process.", "psychology-cognitive-science.cognitive"),
    ("heuristic", "Heuristic", "A heuristic reduces search or judgment cost but can create systematic error outside its useful conditions.", "psychology-cognitive-science.decision"),
    ("bias", "Cognitive bias", "A cognitive bias is a reproducible pattern of judgment relative to a declared normative or task benchmark, not a universal defect in every context.", "psychology-cognitive-science.decision"),
    ("decision", "Decision making", "Decision making combines beliefs, values, options, uncertainty, and constraints and is not reducible to probability alone.", "psychology-cognitive-science.decision"),
    ("language-cognition", "Language and cognition", "Language supports representation and communication while interacting with perception, memory, social context, and reasoning.", "psychology-cognitive-science.language"),
    ("development", "Development", "Psychological development reflects interacting biological, learning, social, cultural, and environmental processes across time.", "psychology-cognitive-science.developmental"),
    ("social-influence", "Social influence", "Social influence changes belief or behavior through informational, normative, relational, and institutional mechanisms.", "psychology-cognitive-science.social"),
    ("personality", "Personality", "Personality constructs describe relatively stable patterns with contextual variation and measurement uncertainty.", "psychology-cognitive-science.personality"),
    ("stress", "Stress", "Stress involves appraisal and physiological or behavioral responses to demands, with effects shaped by duration, control, resources, and context.", "psychology-cognitive-science.health"),
    ("clinical-classification", "Clinical classification", "Clinical classification organizes symptom patterns for communication and research but does not make a diagnosis without qualified individual assessment.", "psychology-cognitive-science.clinical"),
    ("treatment-evidence", "Psychological treatment evidence", "Treatment evidence compares benefits, harms, uncertainty, population fit, alternatives, and implementation rather than assuming one universal response.", "psychology-cognitive-science.clinical")
]


NEUROSCIENCE = [
    ("root", "Neuroscience evidence", "Neuroscience connects neural structure, signaling, circuits, systems, behavior, and disorders while retaining measurement, scale, uncertainty, and clinical boundaries.", "neuroscience-neurology.clinical-boundaries"),
    ("nervous-system", "Nervous system", "The nervous system coordinates information through central and peripheral structures with interacting sensory, motor, autonomic, and associational functions.", "neuroscience-neurology.neuroanatomy"),
    ("cns", "Central nervous system", "The central nervous system comprises the brain and spinal cord.", "neuroscience-neurology.neuroanatomy"),
    ("pns", "Peripheral nervous system", "The peripheral nervous system comprises neural structures outside the brain and spinal cord that connect receptors, effectors, and central circuits.", "neuroscience-neurology.neuroanatomy"),
    ("neuron", "Neuron", "A neuron is an excitable cell specialized to receive, integrate, and transmit signals through electrical and chemical processes.", "neuroscience-neurology.cellular"),
    ("glia", "Glial cell", "Glial cells support, regulate, insulate, defend, and interact with neural signaling; they are not merely inert filler.", "neuroscience-neurology.cellular"),
    ("dendrite", "Dendrite", "Dendrites are neuronal processes specialized in receiving and integrating many synaptic inputs, with substantial variation among cell types.", "neuroscience-neurology.cellular"),
    ("axon", "Axon", "An axon carries action potentials from a neuron toward synaptic or effector targets.", "neuroscience-neurology.cellular"),
    ("membrane-potential", "Membrane potential", "Membrane potential arises from ionic gradients and selective membrane permeability.", "neuroscience-neurology.cellular"),
    ("action-potential", "Action potential", "An action potential is a regenerative change in membrane voltage that propagates along an excitable membrane.", "neuroscience-neurology.cellular"),
    ("synapse", "Synapse", "A synapse is a specialized junction through which one cell influences another by chemical or electrical signaling.", "neuroscience-neurology.cellular"),
    ("neurotransmitter", "Neurotransmitter", "A neurotransmitter is released by a presynaptic cell and acts through receptors; its effect depends on receptor, circuit, and cellular context.", "neuroscience-neurology.cellular"),
    ("receptor", "Neural receptor", "A receptor transduces a chemical or physical signal into cellular effects under its molecular and circuit context.", "neuroscience-neurology.cellular"),
    ("excitation", "Excitatory influence", "An excitatory synaptic influence raises the probability or magnitude of a target response under the current membrane and circuit state.", "neuroscience-neurology.cellular"),
    ("inhibition", "Inhibitory influence", "An inhibitory synaptic influence reduces or controls target activity under the current membrane and circuit state.", "neuroscience-neurology.cellular"),
    ("circuit", "Neural circuit", "A neural circuit is a connected population whose interactions transform inputs into activity and outputs over time.", "neuroscience-neurology.systems"),
    ("sensory-system", "Sensory system", "A sensory system transduces environmental or bodily signals and processes them through distributed pathways.", "neuroscience-neurology.sensory-motor"),
    ("motor-system", "Motor system", "A motor system organizes commands, feedback, and control of muscles or other effectors.", "neuroscience-neurology.sensory-motor"),
    ("association-system", "Association system", "Association systems connect and transform information beyond primary sensory and motor pathways through distributed circuits.", "neuroscience-neurology.systems"),
    ("brainstem", "Brainstem", "The brainstem links spinal, cranial, autonomic, arousal, and sensorimotor functions through multiple nuclei and pathways.", "neuroscience-neurology.neuroanatomy"),
    ("cerebellum", "Cerebellum", "The cerebellum contributes to coordination, timing, prediction, adaptation, and learning through distributed loops rather than serving only one movement function.", "neuroscience-neurology.systems"),
    ("cerebrum", "Cerebrum", "The cerebrum contains cortical and subcortical systems supporting perception, action, cognition, emotion, and memory.", "neuroscience-neurology.neuroanatomy"),
    ("spinal-cord", "Spinal cord", "The spinal cord carries ascending and descending signals and contains circuits for sensation, movement, and autonomic regulation.", "neuroscience-neurology.neuroanatomy"),
    ("plasticity", "Neural plasticity", "Neural plasticity is activity-, experience-, development-, or injury-related change in neural structure or function across multiple time scales.", "neuroscience-neurology.neuroplasticity"),
    ("neural-learning", "Neural mechanisms of learning", "Learning can alter synaptic efficacy, intrinsic excitability, network dynamics, and systems organization without implying one universal storage site.", "neuroscience-neurology.learning-memory"),
    ("neural-memory", "Neural mechanisms of memory", "Memory depends on distributed encoding, consolidation, retrieval, and reconstruction across interacting neural systems.", "neuroscience-neurology.learning-memory"),
    ("development", "Neural development", "Neural development includes cell generation, migration, differentiation, axon guidance, circuit formation, pruning, and experience-dependent change.", "neuroscience-neurology.developmental"),
    ("neuroimaging", "Neuroimaging", "Neuroimaging measures signals related indirectly or directly to neural structure or activity and requires modality-specific inference limits.", "neuroscience-neurology.neuroimaging"),
    ("electrophysiology", "Electrophysiology", "Electrophysiology records electrical properties or activity at spatial and temporal scales determined by the instrument.", "neuroscience-neurology.neuroimaging"),
    ("lesion-evidence", "Lesion evidence", "Lesion evidence can identify necessity or network contribution under anatomical, compensatory, and selection limitations.", "neuroscience-neurology.neuroimaging"),
    ("localization", "Functional localization", "Functional localization relates measured activity or disruption to a function but must retain network, task, and measurement context.", "neuroscience-neurology.systems"),
    ("network", "Distributed neural network", "Many neural functions emerge from interactions across distributed regions and time rather than one isolated center.", "neuroscience-neurology.systems"),
    ("reverse-inference", "Reverse inference", "Reverse inference reasons from observed neural activity to a psychological process and requires selectivity and alternative-process evidence.", "neuroscience-neurology.cognitive"),
    ("disorder", "Neurological disorder evidence", "A neurological disorder claim requires clinical criteria, differential assessment, population evidence, and current professional guidance.", "neuroscience-neurology.neurological-disorders"),
    ("clinical-boundary", "Neurological clinical boundary", "Educational neural information cannot diagnose, rule out, or prescribe for an individual without qualified clinical assessment.", "neuroscience-neurology.clinical-boundaries")
]


RELATIONS = [
    ("psy-construct-operation", "psy.construct", "psy.operationalization", "requires", "A construct requires an operationalization before it can be empirically measured."),
    ("psy-operation-reliability", "psy.operationalization", "psy.reliability", "enables", "A specified operation enables reliability to be evaluated."),
    ("psy-operation-validity", "psy.operationalization", "psy.validity", "enables", "A specified operation enables evidence for or against an interpretation's validity."),
    ("psy-reliability-validity", "psy.reliability", "psy.validity", "qualifies", "Reliability is generally necessary but not sufficient for validity."),
    ("psy-replication-effect", "psy.replication", "psy.effect-size", "qualifies", "Replication evidence qualifies the stability and scope of an effect estimate."),
    ("psy-correlation-cause", "psy.correlation", "psy.experiment", "qualifies", "Correlation requires design and assumptions beyond association for causal identification."),
    ("psy-observation-cause", "psy.observation-study", "psy.correlation", "measures", "Observational studies commonly estimate associations that require confounding analysis."),
    ("psy-experiment-cause", "psy.experiment", "psy.correlation", "clarifies", "Randomized intervention can clarify causal direction under its validity assumptions."),
    ("psy-sensation-perception", "psy.sensation", "psy.perception", "enables", "Sensory transduction provides input that perceptual systems organize and interpret."),
    ("psy-bottom-perception", "psy.bottom-up-processing", "psy.perception", "supports", "Bottom-up feature processing supports perception from incoming structure."),
    ("psy-top-perception", "psy.top-down-processing", "psy.perception", "qualifies", "Prior knowledge and goals qualify interpretation of sensory input."),
    ("psy-attention-memory", "psy.attention", "psy.encoding", "supports", "Attention can support encoding without guaranteeing durable memory."),
    ("psy-encoding-consolidation", "psy.encoding", "psy.consolidation", "enables", "Initial encoding enables later consolidation processes."),
    ("psy-consolidation-retrieval", "psy.consolidation", "psy.retrieval", "supports", "Consolidation supports later retrieval while retrieval remains cue- and context-dependent."),
    ("psy-forgetting-retrieval", "psy.forgetting", "psy.retrieval", "inhibits", "Forgetting mechanisms can reduce successful retrieval."),
    ("psy-working-problem", "psy.working-memory", "psy.problem-solving", "supports", "Working memory supports temporary representation during problem solving."),
    ("psy-heuristic-bias", "psy.heuristic", "psy.bias", "enables", "A heuristic can enable systematic bias when its assumptions mismatch the task."),
    ("psy-probability-decision", "psy.bias", "psy.decision", "qualifies", "Bias evidence qualifies probabilistic judgments without determining every decision."),
    ("psy-development-variation", "psy.development", "psy.population-variation", "supports", "Developmental stage is one source of population and context variation."),
    ("psy-classification-diagnosis", "psy.clinical-classification", "psy.treatment-evidence", "qualifies", "Classification can organize treatment evidence but cannot choose treatment for an individual by itself."),
    ("neuro-system-cns", "neuro.cns", "neuro.nervous-system", "part_of", "The central nervous system is one major anatomical division of the nervous system."),
    ("neuro-system-pns", "neuro.pns", "neuro.nervous-system", "part_of", "The peripheral nervous system is one major anatomical division of the nervous system."),
    ("neuro-dendrite-neuron", "neuro.dendrite", "neuro.neuron", "part_of", "Dendrites are specialized neuronal processes."),
    ("neuro-axon-neuron", "neuro.axon", "neuro.neuron", "part_of", "An axon is a specialized neuronal process."),
    ("neuro-potential-spike", "neuro.membrane-potential", "neuro.action-potential", "prerequisite", "Ionic membrane potential dynamics are required for an action potential."),
    ("neuro-spike-axon", "neuro.action-potential", "neuro.axon", "transforms_to", "Action potentials propagate along axonal membrane under excitable conditions."),
    ("neuro-spike-synapse", "neuro.action-potential", "neuro.synapse", "enables", "Presynaptic electrical activity can enable synaptic transmission."),
    ("neuro-transmitter-receptor", "neuro.neurotransmitter", "neuro.receptor", "requires", "A neurotransmitter effect requires a compatible receptor and cellular context."),
    ("neuro-receptor-excitation", "neuro.receptor", "neuro.excitation", "enables", "Receptor activation can enable excitation depending on receptor and membrane context."),
    ("neuro-receptor-inhibition", "neuro.receptor", "neuro.inhibition", "enables", "Receptor activation can enable inhibition depending on receptor and membrane context."),
    ("neuro-synapse-circuit", "neuro.synapse", "neuro.circuit", "enables", "Synapses connect cells into neural circuits."),
    ("neuro-sensory-circuit", "neuro.sensory-system", "neuro.circuit", "part_of", "Sensory systems contain circuits that transform receptor signals."),
    ("neuro-motor-circuit", "neuro.motor-system", "neuro.circuit", "part_of", "Motor systems contain circuits that organize effectors and feedback."),
    ("neuro-plastic-learning", "neuro.plasticity", "neuro.neural-learning", "enables", "Plastic change is one mechanism through which experience can alter neural learning systems."),
    ("neuro-learning-memory", "neuro.neural-learning", "neuro.neural-memory", "supports", "Learning-related neural change supports later memory without defining one storage mechanism."),
    ("neuro-imaging-localization", "neuro.neuroimaging", "neuro.localization", "supports", "Neuroimaging can support localization claims within modality and design limits."),
    ("neuro-network-localization", "neuro.network", "neuro.localization", "qualifies", "Distributed network organization qualifies claims that one region alone implements a function."),
    ("neuro-reverse-localization", "neuro.reverse-inference", "neuro.localization", "qualifies", "Reverse inference requires selectivity evidence beyond observing activity in a region."),
    ("neuro-disorder-clinical", "neuro.disorder", "neuro.clinical-boundary", "requires", "Disorder-specific information remains inside the clinical evidence boundary."),
    ("bridge-sensation-neural", "neuro.sensory-system", "psy.sensation", "grounds", "Sensory neural systems ground the biological transduction component of sensation."),
    ("bridge-perception-network", "neuro.network", "psy.perception", "supports", "Distributed neural networks support perception while psychological organization remains a distinct explanatory level."),
    ("bridge-working-memory", "neuro.neural-memory", "psy.working-memory", "qualifies", "Neural memory mechanisms constrain but do not replace the task-level construct of working memory."),
    ("bridge-learning", "neuro.plasticity", "psy.observational-learning", "qualifies", "Neural plasticity can support learning but does not by itself identify the psychological learning mechanism."),
    ("bridge-stress", "neuro.nervous-system", "psy.stress", "supports", "Nervous-system responses contribute to stress while appraisal and social context remain relevant."),
    ("bridge-clinical", "neuro.clinical-boundary", "psy.clinical-classification", "supports", "Both neurological and psychological educational lanes require qualified individual assessment before diagnosis.")
]


CONTROLS = [
    ("psy-test-score-person", "Test score is not the whole person", "A single psychological score must not be treated as an exhaustive trait or diagnosis."),
    ("psy-population-individual", "Population-to-individual leap", "A group average must not be asserted as an individual's outcome without individual evidence."),
    ("psy-correlation-causation", "Correlation-causation boundary", "Association alone must not be emitted as causal direction."),
    ("psy-replication-blind", "Replication blindness", "A famous result must retain replication and measurement limitations."),
    ("psy-diagnosis", "No diagnosis from text", "General psychological information must not diagnose a user or third party."),
    ("psy-treatment", "No treatment prescription", "Curriculum knowledge must not select treatment without qualified current clinical assessment."),
    ("psy-universal", "Context-free universal", "A psychological effect must not be generalized across all people, cultures, tasks, or times without evidence."),
    ("neuro-region-function", "One-region one-function error", "Activity in one region must not be treated as proof that the region alone implements one psychological function."),
    ("neuro-reverse-inference", "Reverse-inference control", "Observed neural activity must not identify a unique mental process without selectivity evidence."),
    ("neuro-neurotransmitter", "Neurotransmitter slogan", "A neurotransmitter must not be labeled simply excitatory, inhibitory, happy, or fearful without receptor and circuit context."),
    ("neuro-brain-scan-diagnosis", "No diagnosis from a scan description", "Educational neuroimaging patterns must not diagnose an individual."),
    ("neuro-reduction", "Explanatory-level reduction", "A neural correlate must not erase psychological, behavioral, social, or task-level explanation."),
    ("neuro-plasticity-limitless", "Plasticity is not limitless", "Neural plasticity must not be presented as unlimited recovery or arbitrary rewiring."),
    ("neuro-stale-clinical", "Date-sensitive clinical boundary", "Neurological treatment or prognosis must not be emitted from stale or non-clinical curriculum records."),
    ("neuro-cause-after", "Temporal order control", "A neural event measured after behavior must not automatically be labeled its cause.")
]


def base(identifier: str, domain: str, subject: str, lanes: list[str], sources: list[str], split: str, kind: str, epistemic: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "record_id": identifier,
        "world_id": WORLD,
        "domain_id": domain,
        "subject_id": subject,
        "lanes": lanes,
        "record_kind": kind,
        "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws", "uncertainty_competing_hypotheses"],
        "source_ids": sources,
        "scope": "educational foundation; no individual diagnosis or treatment authority",
        "limitations": ["Date-sensitive and specialist evidence must be refreshed before clinical use.", "This foundation tranche is not exhaustive."],
        "as_of": "2026-09-03",
        "version_boundary": "psychology-neuroscience-v0",
        "split_group": identifier,
        "split": split,
        "tags": ["evidence-sensitive", domain]
    }


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for prefix, rows, domain, lanes, sources, root in [
        ("psy", PSYCHOLOGY, "psychology-cognitive-science", PSY_LANES, PSY_SOURCES, "psy.root"),
        ("neuro", NEUROSCIENCE, "neuroscience-neurology", NEURO_LANES, NEURO_SOURCES, "neuro.root")
    ]:
        for index, (identifier, label, statement, subject) in enumerate(rows):
            node_id = f"{prefix}.{identifier}"
            records.append({
                **base(node_id, domain, subject, lanes, sources, "validation" if index and index % 19 == 0 else "train", "concept", "established"),
                "label": label,
                "statement": statement,
                "aliases": [label.lower()]
            })
            if node_id != root:
                records.append({
                    **base(f"{prefix}.membership.{identifier}", domain, subject, lanes, sources, "train", "relation", "established"),
                    "label": f"{label} world membership",
                    "statement": f"{label} is a distinct evidence-bearing component of the {domain.replace('-', ' ')} world.",
                    "aliases": [],
                    "relation": {"source_node": node_id, "target_node": root, "kind": "part_of", "polarity": 1, "direction": "forward", "conditions": [], "exceptions": []},
                    "coverage_axes": ["primitives_invariants", "within_domain_composition"]
                })
    for index, (identifier, source, target, kind, statement) in enumerate(RELATIONS):
        if index % 13 == 0:
            split = "sealed_test"
        elif index % 9 == 0:
            split = "validation"
        elif index % 17 == 0:
            split = "cross_domain_holdout"
        else:
            split = "train"
        is_neuro = identifier.startswith("neuro-")
        is_bridge = identifier.startswith("bridge-")
        domain = "neuroscience-neurology" if is_neuro else "psychology-cognitive-science"
        lanes = sorted(set(PSY_LANES + NEURO_LANES)) if is_bridge else NEURO_LANES if is_neuro else PSY_LANES
        sources = sorted(set(PSY_SOURCES + NEURO_SOURCES)) if is_bridge else NEURO_SOURCES if is_neuro else PSY_SOURCES
        normalized_kind = "prerequisite" if kind == "requires" else kind
        records.append({
            **base(f"relation.{identifier}", domain, "neuroscience-neurology.cognitive" if is_neuro or is_bridge else "psychology-cognitive-science.cognitive", lanes, sources, split, "relation", "established"),
            "label": identifier.replace("-", " "),
            "statement": statement,
            "aliases": [],
            "relation": {
                "source_node": source,
                "target_node": target,
                "kind": normalized_kind,
                "polarity": -1 if normalized_kind in {"inhibits", "prevents", "contradicts", "undercuts"} else 1,
                "direction": "forward",
                "conditions": ["measurement scale and population are declared"],
                "exceptions": []
            },
            "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"]
        })
    for index, (identifier, label, statement) in enumerate(CONTROLS):
        is_neuro = identifier.startswith("neuro-")
        domain = "neuroscience-neurology" if is_neuro else "psychology-cognitive-science"
        lanes = NEURO_LANES if is_neuro else PSY_LANES
        records.append({
            **base(f"control.{identifier}", domain, "neuroscience-neurology.clinical-boundaries" if is_neuro else "psychology-cognitive-science.clinical", lanes, [], "validation" if index % 2 == 0 else "sealed_test", "synthetic_control", "synthetic_control"),
            "label": label,
            "statement": statement,
            "aliases": [label.lower()],
            "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"],
            "synthetic": True,
            "tags": ["negative-control", "non-diagnostic", domain]
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

