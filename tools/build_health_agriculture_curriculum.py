#!/usr/bin/env python3
"""Author non-diagnostic medicine/health and agriculture/food/ecology foundations."""

from __future__ import annotations

import json
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "health-agriculture" / "foundations.jsonl"
WORLD = "health-agriculture-v0"
LANES = ["reasoning.causal", "reasoning.inductive", "reasoning.probabilistic", "thinking.bottom_up", "psychology.evidence"]
HEALTH_SOURCES = ["mesh2026", "cdc-field-epidemiology", "fda-drug-development", "dietary-guidelines-2025-2030", "ninds-brain-basics", "national-academies-reproducibility"]
AG_SOURCES = ["usda-nifa", "usgs-earth-water-science", "mesh2026", "cdc-field-epidemiology", "iupac-goldbook-500"]


HEALTH = [
    ("medicine-health.anatomy", "anatomy", "Human anatomy", "Human anatomy describes spatial organization and variation of cells, tissues, organs, vessels, nerves, compartments, and body regions.", "Anatomical relation", "An anatomical relation specifies position, orientation, containment, adjacency, continuity, and individual variation in a reference frame.", "Structure-function constraint", "Geometry, tissue properties, development, and connections constrain but do not uniquely determine physiological function.", "Diagram matches every person", "A canonical anatomy diagram must not be treated as an individual's exact anatomy or used for diagnosis."),
    ("medicine-health.physiology", "physiology", "Human physiology", "Human physiology studies integrated transport, signaling, metabolism, mechanics, regulation, and homeostasis across organ systems.", "Physiological state", "A physiological state contains time-varying measured variables whose normal range depends on person, method, activity, and context.", "Regulatory feedback", "Sensors, neural and hormonal signals, organs, effectors, delays, and compensations regulate body variables dynamically.", "Reference range means healthy diagnosis", "A value inside or outside a population reference range must not independently diagnose health or disease."),
    ("medicine-health.pathology", "pathology", "Pathology", "Pathology studies structural, molecular, cellular, tissue, and organ changes associated with disease mechanisms and clinical findings.", "Pathologic finding", "A finding is a measured or observed alteration with specimen, method, site, grading, uncertainty, and differential interpretation.", "Disease mechanism", "Etiology, susceptibility, injury, response, adaptation, progression, repair, and treatment jointly produce pathologic patterns.", "One finding uniquely identifies disease", "A pathologic feature must not establish one diagnosis without sampling, context, differential, and qualified interpretation."),
    ("medicine-health.pharmacology", "pharmacology", "Pharmacology", "Pharmacology studies drug targets, dose, absorption, distribution, metabolism, elimination, response, interactions, efficacy, toxicity, and population variation.", "Exposure-response relation", "Drug concentration and effect vary with dose, formulation, route, time, physiology, genetics, other substances, and adherence.", "Drug development evidence", "Discovery, preclinical, clinical, regulatory, manufacturing, labeling, and post-market evidence qualify approved uses and risks.", "Approved drug is safe for everyone", "Approval must not be treated as universal safety or suitability independent of indication, person, dose, interaction, and current labeling."),
    ("medicine-health.epidemiology", "epidemiology", "Epidemiology", "Epidemiology studies distributions and determinants of health events in populations through surveillance, studies, causal inference, and intervention evaluation.", "Case definition", "A case definition specifies clinical, laboratory, person, place, and time criteria for consistent population investigation.", "Outbreak inference", "Descriptive patterns generate hypotheses, analytic comparison tests them, laboratory and environmental evidence refine causes, and interventions feed back into surveillance.", "Case count equals risk", "Raw case counts must not be compared without population denominator, ascertainment, time, place, and case-definition consistency."),
    ("medicine-health.public-health", "public-health", "Public health", "Public health protects population health through surveillance, prevention, policy, environment, communication, services, equity, preparedness, and evaluation.", "Population intervention", "A public-health intervention has target population, mechanism, delivery, uptake, benefit, harm, distribution, resources, and evaluation plan.", "Evidence-to-action", "Scientific evidence, urgency, feasibility, law, ethics, community input, uncertainty, and monitoring jointly inform public-health action.", "Population benefit erases individual harm", "Aggregate benefit must not erase subgroup, individual, rights, access, and unintended-harm analysis."),
    ("medicine-health.diagnostics-evidence", "diagnostics-evidence", "Diagnostic evidence and uncertainty", "Diagnostic reasoning updates probabilities among possible conditions from history, examination, tests, prevalence, time course, and response while retaining uncertainty.", "Diagnostic test", "A test has sensitivity, specificity, likelihood ratios, thresholds, reference standard, spectrum, prevalence, and operational error.", "Differential update", "Prior probabilities and conditionally informative findings update a differential rather than allowing one result to dictate a diagnosis.", "Positive test means disease certainty", "A positive result must not be treated as diagnostic certainty without false positives, prevalence, test validity, and clinical context."),
    ("medicine-health.treatment-evidence", "treatment-evidence", "Treatment evidence", "Treatment evidence compares benefits, harms, alternatives, timing, dose, adherence, patient goals, subgroups, quality, and uncertainty.", "Comparative treatment effect", "A treatment effect is a population contrast under design, outcome, follow-up, adherence, and estimand definitions.", "Individual decision", "Current evidence, diagnosis, comorbidities, interactions, values, access, monitoring, and clinician judgment jointly inform individual treatment.", "Average trial effect prescribes individual", "A group average must not become an individual treatment recommendation without qualified clinical assessment."),
    ("medicine-health.nutrition", "nutrition", "Nutrition science", "Nutrition science studies foods, nutrients, dietary patterns, metabolism, requirements, behavior, access, culture, and health across populations and life stages.", "Dietary exposure", "Dietary exposure includes amount, pattern, preparation, timing, substitution, supplements, measurement error, and person context.", "Nutrition-health inference", "Biochemistry, feeding studies, trials, cohorts, substitution models, and population evidence jointly qualify nutrition claims.", "Single nutrient explains whole diet", "One nutrient or food must not be treated as determining health independent of dietary pattern, dose, substitution, and person."),
    ("medicine-health.mental-health", "mental-health", "Mental-health evidence", "Mental-health science studies distress, functioning, development, social context, neurobiology, diagnosis, treatment, recovery, and variation without reducing people to labels.", "Clinical assessment", "Assessment integrates symptoms, duration, impairment, risk, medical causes, development, culture, history, supports, and individual goals.", "Evidence-based care", "Therapeutic relationship, intervention evidence, person fit, monitoring, safety, shared decisions, and access shape care outcomes.", "Text description diagnoses a person", "General or conversational information must not diagnose, rule out, or prescribe for an individual."),
    ("medicine-health.safety-boundary", "safety-boundary", "Medical safety and referral boundary", "Medical information requires urgency screening, uncertainty, current evidence, scope, referral, and emergency escalation when individual harm could result.", "Red-flag condition", "A red flag is a symptom or context requiring urgent professional or emergency evaluation under current guidance, not a standalone diagnosis.", "Safe escalation", "Uncertainty, severity, time sensitivity, vulnerability, medication risk, and inability to assess cause trigger referral or emergency direction.", "Educational answer replaces clinician", "A general model or curriculum must not replace examination, diagnosis, prescribing, emergency services, or licensed care."),
]


AGRICULTURE = [
    ("agriculture-food-ecology.agronomy", "agronomy", "Agronomy", "Agronomy integrates crops, soils, water, climate, genetics, nutrients, pests, machinery, economics, and management for production and stewardship.", "Crop system", "A crop system has species and cultivar, rotation, soil, weather, inputs, operations, pests, yield goals, and environmental boundaries.", "Yield formation", "Establishment, canopy, photosynthesis, water, nutrients, stress, reproduction, management, and harvest jointly determine yield and quality.", "More input always gives more yield", "Additional fertilizer, water, pesticide, or density must not be assumed beneficial beyond response, loss, toxicity, lodging, resistance, and cost limits."),
    ("agriculture-food-ecology.soil", "soil", "Soil management", "Soil management maintains structure, organic matter, nutrients, water, biology, erosion control, salinity, contamination, and long-term function.", "Soil test", "A soil test has sampling depth, spatial design, method, units, calibration, crop, timing, and interpretation region.", "Nutrient-management cycle", "Soil supply, amendments, mineralization, uptake, immobilization, leaching, runoff, erosion, and harvest removal determine nutrient balance.", "One soil sample represents field", "A single sample must not represent a spatially variable field without a justified sampling design."),
    ("agriculture-food-ecology.plant-health", "plant-health", "Plant health", "Plant health studies diseases, pests, weeds, nutrient disorders, environmental stress, diagnosis, resistance, and integrated management.", "Plant symptom", "A symptom is a plant response pattern with host, organ, distribution, timing, environment, and possible biotic or abiotic causes.", "Integrated pest management", "Monitoring, thresholds, prevention, biological and cultural controls, targeted chemicals, resistance management, and evaluation form an integrated strategy.", "Symptom photo proves pathogen", "A photograph must not uniquely diagnose a plant disease without host, distribution, signs, environment, tests, and differential evidence."),
    ("agriculture-food-ecology.animal-science", "animal-science", "Animal science", "Animal science studies genetics, nutrition, physiology, behavior, welfare, reproduction, housing, production, environment, and management.", "Animal production state", "Species, breed, age, sex, health, diet, environment, group, behavior, and purpose qualify animal measurements.", "Welfare-production interaction", "Nutrition, housing, handling, social conditions, disease, genetics, and management jointly shape welfare and production outcomes.", "Production metric proves welfare", "Growth or output must not establish welfare without health, behavior, affective, injury, and environmental evidence."),
    ("agriculture-food-ecology.veterinary", "veterinary", "Veterinary science", "Veterinary science studies animal health, disease, diagnostics, treatment, prevention, welfare, zoonoses, population medicine, and food systems.", "Veterinary patient context", "Species, breed, age, weight, physiology, use, environment, exposure, signs, and owner observations qualify clinical evidence.", "Veterinary differential", "History, examination, tests, epidemiology, toxicology, nutrition, and species-specific mechanisms update possible diagnoses.", "Human medicine transfers directly to animals", "Human drug, dose, symptom, and treatment information must not be applied across species without veterinary authority."),
    ("agriculture-food-ecology.food-science", "food-science", "Food science", "Food science studies composition, structure, processing, preservation, safety, sensory properties, packaging, quality, and supply chains.", "Food matrix", "A food matrix combines water, proteins, lipids, carbohydrates, minerals, microbes, structure, and additives that affect processing and stability.", "Hazard-control process", "Time, temperature, water activity, pH, atmosphere, sanitation, packaging, and monitoring control biological, chemical, and physical hazards.", "Appearance proves food safe", "Smell, color, taste, or date alone must not establish microbiological or chemical safety."),
    ("agriculture-food-ecology.forestry", "forestry", "Forestry", "Forestry manages forest ecology, growth, regeneration, harvest, habitat, fire, pests, carbon, water, products, and communities across long time scales.", "Forest stand", "A stand has species, ages, sizes, density, structure, site, disturbance, ownership, and management history.", "Forest succession and management", "Recruitment, competition, mortality, disturbance, climate, harvest, regeneration, and landscape connectivity transform forest structure.", "Tree planting alone restores forest", "Planting count must not establish ecosystem restoration without species, survival, soils, hydrology, diversity, disturbance, and long-term care."),
    ("agriculture-food-ecology.fisheries", "fisheries", "Fisheries science", "Fisheries science studies populations, harvest, recruitment, mortality, habitat, food webs, fleets, uncertainty, governance, and communities.", "Fish stock", "A stock is an operational population unit with age or size structure, distribution, recruitment, growth, natural mortality, and harvest.", "Stock assessment", "Catch, effort, surveys, biology, tagging, environment, and population models estimate stock state and uncertainty.", "Catch decline proves stock decline", "Observed catch must not uniquely indicate abundance without effort, regulation, targeting, market, distribution, and reporting."),
    ("agriculture-food-ecology.agricultural-systems", "agricultural-systems", "Agricultural systems", "Agricultural systems couple farms, labor, land, water, energy, inputs, ecology, markets, infrastructure, policy, culture, and food security.", "Farm-system boundary", "A farm-system boundary declares enterprises, resources, households, landscape, suppliers, buyers, risks, and time horizon.", "Resilience pathway", "Diversity, reserves, soil and water health, knowledge, insurance, infrastructure, institutions, and adaptation shape recovery from shocks.", "One yield metric proves sustainable agriculture", "Yield alone must not establish profitability, nutrition, labor, water, soil, biodiversity, emissions, resilience, and equity."),
]


CROSS_RELATIONS = [
    ("health-anatomy-phys", "health.anatomy.mechanism", "health.physiology.primitive", "qualifies", "Anatomical structure qualifies physiological state and transport."),
    ("health-phys-path", "health.physiology.mechanism", "health.pathology.mechanism", "qualifies", "Regulatory feedback and compensation qualify disease expression."),
    ("health-pharm-treatment", "health.pharmacology.mechanism", "health.treatment-evidence.mechanism", "supports", "Drug-development and post-market evidence support comparative treatment decisions."),
    ("health-epi-public", "health.epidemiology.mechanism", "health.public-health.mechanism", "supports", "Outbreak inference supports evidence-to-action in public health."),
    ("health-diagnostic-treatment", "health.diagnostics-evidence.mechanism", "health.treatment-evidence.primitive", "qualifies", "Differential diagnosis qualifies which treatment evidence is relevant."),
    ("health-nutrition-public", "health.nutrition.mechanism", "health.public-health.primitive", "supports", "Population nutrition evidence supports public-health interventions."),
    ("health-mental-safety", "health.mental-health.primitive", "health.safety-boundary.mechanism", "qualifies", "Clinical assessment and risk context qualify safe mental-health escalation."),
    ("ag-crop-soil", "ag.soil.mechanism", "ag.agronomy.mechanism", "qualifies", "Nutrient and water balances qualify crop yield formation."),
    ("ag-plant-agronomy", "ag.plant-health.mechanism", "ag.agronomy.primitive", "supports", "Integrated plant-health management supports crop-system performance."),
    ("ag-animal-vet", "ag.animal-science.primitive", "ag.veterinary.mechanism", "qualifies", "Species and production context qualify veterinary differentials."),
    ("ag-vet-food", "ag.veterinary.mechanism", "ag.food-science.mechanism", "supports", "Animal-health and zoonotic evidence support food hazard controls."),
    ("ag-forest-system", "ag.forestry.mechanism", "ag.agricultural-systems.mechanism", "qualifies", "Landscape forest dynamics qualify agricultural-system resilience."),
    ("ag-fish-system", "ag.fisheries.mechanism", "ag.agricultural-systems.primitive", "qualifies", "Stock assessment qualifies aquatic food-system decisions."),
    ("bridge-food-nutrition", "ag.food-science.primitive", "health.nutrition.primitive", "qualifies", "Food matrices and processing qualify dietary exposure and nutrient availability."),
    ("bridge-one-health", "ag.veterinary.mechanism", "health.epidemiology.mechanism", "supports", "Veterinary and human epidemiology jointly support zoonotic outbreak inference."),
    ("bridge-public-ag", "health.public-health.mechanism", "ag.agricultural-systems.mechanism", "qualifies", "Population health, environment, food access, and production resilience jointly qualify agricultural interventions."),
]


WORKED_EXAMPLES = [
    ("health", "test-probability", "Diagnostic probability update", "A positive test combines pretest probability with sensitivity and specificity; the result remains one differential probability, not a diagnosis.", "medicine-health.diagnostics-evidence"),
    ("health", "trial-individual", "Trial-to-individual boundary", "A trial effect is checked against diagnosis, eligibility, baseline risk, comorbidity, interaction, goals, monitoring, and current labeling before clinician discussion.", "medicine-health.treatment-evidence"),
    ("health", "outbreak", "Field outbreak investigation", "A case definition and epidemic curve generate hypotheses, comparison and laboratory evidence test them, immediate controls are monitored, and uncertainty remains explicit.", "medicine-health.epidemiology"),
    ("health", "red-flag", "Medical escalation", "Severe or rapidly worsening symptoms plus inability to assess cause trigger urgent professional or emergency evaluation instead of speculative diagnosis.", "medicine-health.safety-boundary"),
    ("ag", "nutrient-budget", "Field nutrient budget", "Soil supply plus amendments and mineralization minus crop removal, leaching, runoff, and immobilization yields a bounded nutrient balance with sampling uncertainty.", "agriculture-food-ecology.soil"),
    ("ag", "plant-differential", "Plant-health differential", "Host pattern, field distribution, weather, signs, soil, nutrient test, and laboratory evidence distinguish pathogen, pest, toxicity, and abiotic stress hypotheses.", "agriculture-food-ecology.plant-health"),
    ("ag", "food-haccp", "Food hazard control", "A process identifies a microbial hazard, validates a time-temperature control, monitors each lot, defines corrective action, and verifies records and calibration.", "agriculture-food-ecology.food-science"),
    ("ag", "stock-assessment", "Fishery stock uncertainty", "Catch, effort, survey, age, growth, mortality, and environmental data feed competing models whose uncertainty constrains harvest advice.", "agriculture-food-ecology.fisheries"),
]


GROUPS = [
    ("health", "medicine-health", HEALTH, HEALTH_SOURCES, "Medicine and health sciences", "Medicine and health connect anatomy, physiology, pathology, pharmacology, epidemiology, public health, diagnostic and treatment evidence, nutrition, mental health, and safety boundaries without granting individual clinical authority."),
    ("ag", "agriculture-food-ecology", AGRICULTURE, AG_SOURCES, "Agriculture, food, and applied ecology", "Agricultural systems connect soils, plants, animals, food, forests, fisheries, environment, people, markets, safety, and resilience across sites and seasons."),
]


def split_for(index: int) -> str:
    if index and index % 17 == 0: return "cross_domain_holdout"
    if index and index % 13 == 0: return "sealed_test"
    if index and index % 11 == 0: return "validation"
    return "train"


def base(identifier: str, domain: str, subject: str, sources: list[str], split: str, kind: str, epistemic: str = "established") -> dict[str, Any]:
    return {"schema_version": 1, "record_id": identifier, "world_id": WORLD, "domain_id": domain, "subject_id": subject, "lanes": LANES, "record_kind": kind, "epistemic_class": epistemic, "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"], "source_ids": sorted(set(sources)), "scope": "non-diagnostic health and applied agriculture foundation tranche", "limitations": ["No record diagnoses, prescribes, or replaces current qualified medical or veterinary assessment.", "Clinical, drug, food, agricultural, and regulatory claims require current jurisdiction, species, site, product, person, dose, and professional guidance."], "as_of": "2026-09-03", "version_boundary": "health-agriculture-v0", "split_group": identifier, "split": split, "tags": ["foundation", domain]}


def context(prefix: str) -> tuple[str, list[str], str]:
    for p, domain, profiles, sources, _label, _statement in GROUPS:
        if p == prefix: return domain, sources, profiles[0][0]
    raise ValueError(prefix)


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []; index = 0
    for prefix, domain, profiles, sources, domain_label, domain_statement in GROUPS:
        records.append({**base(f"{prefix}.root", domain, profiles[0][0], sources, "train", "concept"), "label": domain_label, "statement": domain_statement, "aliases": [domain_label.lower()]})
        for subject, slug, label, definition, primitive_label, primitive_statement, mechanism_label, mechanism_statement, control_label, control_statement in profiles:
            for offset, (suffix, node_label, statement) in enumerate([("root", label, definition), ("primitive", primitive_label, primitive_statement), ("mechanism", mechanism_label, mechanism_statement)]):
                nid = f"{prefix}.{slug}.{suffix}"; records.append({**base(nid, domain, subject, sources, "train" if suffix == "root" else split_for(index + offset), "concept"), "label": node_label, "statement": statement, "aliases": [node_label.lower()]})
                target = f"{prefix}.root" if suffix == "root" else f"{prefix}.{slug}.root"; rid = f"ha.membership.{prefix}.{slug}.{suffix}"
                records.append({**base(rid, domain, subject, sources, split_for(index + offset + 4), "relation"), "label": f"{node_label} world membership", "statement": f"{node_label} is a distinct component of {label} with explicit population, site, evidence, and safety boundaries.", "aliases": [], "relation": {"source_node": nid, "target_node": target, "kind": "part_of", "polarity": 1, "direction": "forward", "conditions": ["the declared population, species, site, time, and evidence context apply"], "exceptions": []}, "coverage_axes": ["primitives_invariants", "within_domain_composition"]})
            cid = f"ha.control.{prefix}.{slug}"; records.append({**base(cid, domain, subject, [], ["train", "validation", "sealed_test", "cross_domain_holdout"][index % 4], "synthetic_control", "synthetic_control"), "label": control_label, "statement": control_statement, "aliases": [control_label.lower()], "synthetic": True, "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"], "tags": ["negative-control", "non-diagnostic", domain]}); index += 1
    all_sources = sorted(set(HEALTH_SOURCES + AG_SOURCES)); splitter = RelationSplitter(
        [kind for _id, _s, _t, kind, _st in CROSS_RELATIONS],
        cross_plan=[
            source.split(".", 1)[0] != target.split(".", 1)[0]
            or identifier.startswith("bridge-")
            for identifier, source, target, _kind, _statement in CROSS_RELATIONS
        ],
    )
    for identifier, source, target, kind, statement in CROSS_RELATIONS:
        prefix = source.split(".",1)[0]; domain, sources, subject = context(prefix); cross = prefix != target.split(".",1)[0] or identifier.startswith("bridge-")
        split = splitter.split(kind)
        records.append({**base(f"ha.relation.{identifier}", domain, subject, all_sources if cross else sources, split, "relation"), "label": identifier.replace("-"," "), "statement": statement, "aliases": [], "relation": {"source_node": source, "target_node": target, "kind": kind, "polarity": -1 if kind in {"inhibits","prevents","contradicts","undercuts"} else 1, "direction": "forward", "conditions": ["population, species, site, exposure, intervention, and evidence assumptions hold"], "exceptions": []}, "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"]})
    for ei, (prefix, identifier, label, statement, subject) in enumerate(WORKED_EXAMPLES):
        domain, sources, _ = context(prefix); split = ["train","validation","sealed_test","cross_domain_holdout"][ei%4]; nid=f"ha.example.{prefix}.{identifier}"
        records.append({**base(nid,domain,subject,sources,split,"worked_example"),"label":label,"statement":statement,"aliases":[],"coverage_axes":["applications_toolchains","deductions_predictions_execution","uncertainty_competing_hypotheses"],"tags":["worked-example",domain]})
        records.append({**base(f"ha.example-membership.{prefix}.{identifier}",domain,subject,sources,split,"relation"),"label":f"{label} membership","statement":f"The {label.lower()} operationalizes one bounded health or agriculture evidence chain.","aliases":[],"relation":{"source_node":nid,"target_node":f"{prefix}.root","kind":"part_of","polarity":1,"direction":"forward","conditions":["the example remains non-diagnostic and bounded"],"exceptions":[]},"coverage_axes":["applications_toolchains","within_domain_composition"]})
    return sorted(records,key=lambda x:x["record_id"])


def main() -> int:
    records=build();OUTPUT.parent.mkdir(parents=True,exist_ok=True);OUTPUT.write_text("".join(json.dumps(x,ensure_ascii=False,sort_keys=True)+"\n" for x in records),encoding="utf-8");counts={};kinds={}
    for x in records:counts[x["split"]]=counts.get(x["split"],0)+1;kinds[x["record_kind"]]=kinds.get(x["record_kind"],0)+1
    print(f"wrote {OUTPUT} with {len(records)} records: splits={dict(sorted(counts.items()))} kinds={dict(sorted(kinds.items()))}");return 0


if __name__=="__main__":raise SystemExit(main())
