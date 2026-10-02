#!/usr/bin/env python3
"""Author the everyday physical causation world (pilot general world, 2026-10-02).

Content lives in tools/physical_causation/*.py, one module per physics subfield plus
cross.py (bridges, myths, boundaries, worked examples). Design rules are in
plans/pilot-physical-causation-abductive.md: causal-first relations, real polarity,
one specific condition per relation, no generated lowercase aliases.
"""

from __future__ import annotations

import collections
import json
import sys
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT

sys.path.insert(0, str(ROOT / "tools"))
from physical_causation import (  # noqa: E402
    acoustics, cross, electromagnetism, fluids, kitchen, materials, mechanics, optics, statistical, thermodynamics,
)

OUTPUT = ROOT / "curricula" / "physical-causation" / "foundations.jsonl"
WORLD = "physical-causation-v0"
PREFIX = "pc"
LANES = ["reasoning.causal", "reasoning.deductive", "thinking.bottom_up"]
SUBFIELDS = [mechanics, thermodynamics, fluids, electromagnetism, optics, acoustics, materials, statistical, kitchen]
NEGATIVE = {"inhibits", "prevents", "contradicts", "undercuts", "counterexample"}
LIMITATIONS = [
    "Everyday-scale classical description; relativistic, quantum and extreme regimes are bounded by explicit boundary records.",
    "Statements are original structured summaries of cited sources, not quotations.",
    "Quantities are typical sea-level, room-temperature values unless a condition states otherwise.",
]
CONTROLS = [
    ("tides-lightning", "Lightning drives ocean tides", "Lightning must not be treated as a cause of ocean tides; tides come from the Moon's and Sun's gravity."),
    ("colour-weight", "Paint colour changes an object's weight", "Repainting an object a different colour must not be treated as changing its weight."),
    ("music-boiling", "Loud music makes water boil sooner", "Sound in a kitchen must not be treated as a cause of water boiling sooner."),
    ("magnet-rain", "Magnets cause rainfall", "Household magnets must not be treated as a cause of precipitation."),
    ("shadow-cooling-gravity", "Shadows weaken gravity", "Standing in a shadow must not be treated as reducing an object's weight."),
    ("rust-sound", "Rust makes metal louder", "Rusting must not be treated as a cause of louder sound."),
]


def node(identifier: str) -> str:
    return f"{PREFIX}.{identifier}"


def base(record_id: str, subject: str, sources: list[str], split: str, kind: str,
         axes: list[str], epistemic: str = "established") -> dict[str, Any]:
    return {
        "schema_version": 1, "record_id": record_id, "world_id": WORLD, "domain_id": "physics",
        "subject_id": subject, "lanes": LANES, "record_kind": kind, "epistemic_class": epistemic,
        "coverage_axes": axes, "source_ids": sorted(set(sources)),
        "scope": "Everyday physical causation: mechanics, heat, fluids, electricity and magnetism, light, sound, materials, statistical physics",
        "limitations": LIMITATIONS, "as_of": "2026-10-02", "version_boundary": WORLD,
        "split_group": record_id, "split": split, "tags": ["physical-causation", "pilot"],
    }


def split_for(index: int, *, root: bool = False) -> str:
    if root:
        return "train"
    if index % 41 == 0:
        return "cross_domain_holdout"
    if index % 31 == 0:
        return "sealed_test"
    if index % 23 == 0:
        return "validation"
    return "train"


def edge_split_for(index: int) -> str:
    if index and index % 37 == 0:
        return "cross_domain_holdout"
    if index and index % 29 == 0:
        return "sealed_test"
    if index and index % 19 == 0:
        return "validation"
    return "train"


def relation(record_id: str, subject: str, sources: list[str], split: str, src: str, dst: str, kind: str,
             statement: str, condition: str, exception: str, axes: list[str], label: str,
             epistemic: str = "established") -> dict[str, Any]:
    return {
        **base(record_id, subject, sources, split, "relation", axes, epistemic),
        "label": label, "statement": statement, "aliases": [],
        "relation": {
            "source_node": node(src), "target_node": node(dst), "kind": kind,
            "polarity": -1 if kind in NEGATIVE else 1, "direction": "forward",
            "conditions": [condition] if condition else [], "exceptions": [exception] if exception else [],
        },
    }


def relation_axes(kind: str, cross_subfield: bool) -> list[str]:
    axes = ["mechanisms_causal_laws", "within_domain_composition"]
    if cross_subfield:
        axes.append("cross_domain_composition")
    axes.append({"predicts": "deductions_predictions_execution", "transforms_to": "representations_transformations",
                 "prerequisite": "assumptions_prerequisites", "inhibits": "exceptions_boundaries",
                 "prevents": "exceptions_boundaries"}.get(kind, "primitives_invariants"))
    return sorted(set(axes))


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    subject_of: dict[str, str] = {}
    sources_of: dict[str, list[str]] = {}
    labels: dict[str, str] = {}
    concepts: list[tuple[str, str, str, list[str], str, list[str]]] = []
    for module in SUBFIELDS:
        for identifier, label, statement, aliases in module.CONCEPTS:
            concepts.append((identifier, label, statement, aliases, module.SUBJECT, module.SOURCES))
    for identifier, label, statement, aliases, subject in cross.CONCEPTS:
        module_sources = next(m.SOURCES for m in SUBFIELDS if m.SUBJECT == subject)
        concepts.append((identifier, label, statement, aliases, subject, module_sources))

    all_sources = sorted({s for m in SUBFIELDS for s in m.SOURCES})
    records.append({
        **base(node("root"), "physics.classical-mechanics", all_sources, "train", "concept",
               ["definitions_scope", "primitives_invariants"]),
        "label": "Everyday physical causation world",
        "statement": "Root of the everyday physical causation world: how forces, heat, fluids, electricity, light, sound and materials cause the changes people observe.",
        "aliases": [],
    })
    for index, (identifier, label, statement, aliases, subject, sources) in enumerate(concepts, start=1):
        assert identifier not in subject_of, f"duplicate concept {identifier}"
        subject_of[identifier], sources_of[identifier], labels[identifier] = subject, sources, label
        split = split_for(index)
        records.append({**base(node(identifier), subject, sources, split, "concept",
                               ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"]),
                        "label": label, "statement": statement, "aliases": aliases})
        records.append(relation(f"{PREFIX}.membership.{identifier}", subject, sources, edge_split_for(index),
                                identifier, "root", "part_of",
                                f"{label} is a distinct part of the everyday physical causation world.",
                                f"{label.lower()} is described at everyday scale", "",
                                ["primitives_invariants", "within_domain_composition"], f"{label} membership"))

    authored = [(m.SUBJECT, r) for m in SUBFIELDS for r in m.RELATIONS] + [(None, r) for r in cross.BRIDGES]
    for _, (identifier, src, dst, *_rest) in authored:
        for endpoint in (src, dst):
            assert endpoint in subject_of, f"relation {identifier} references unknown concept {endpoint}"
    crossing = [subject_of[src] != subject_of[dst] or identifier.startswith("bridge-")
                for _, (identifier, src, dst, *_rest) in authored]
    splitter = RelationSplitter([r[3] for _, r in authored], cross_plan=crossing)
    for (_, (identifier, src, dst, kind, statement, condition, exception)), is_cross in zip(authored, crossing):
        subject = subject_of[src]
        records.append(relation(f"{PREFIX}.relation.{identifier}", subject,
                                sorted(set(sources_of[src]) | set(sources_of[dst])), splitter.split(kind),
                                src, dst, kind, statement, condition, exception,
                                relation_axes(kind, is_cross), identifier.replace("-", " ")))

    special = {"heavier-falls-faster": (["history_versions"], "established"),
               "hot-water-freezes-faster": (["uncertainty_competing_hypotheses"], "contested"),
               "equal-transit-lift": (["uncertainty_competing_hypotheses"], "established")}
    myth_splits = ["train", "validation", "sealed_test", "train"]
    for index, (identifier, label, statement, target) in enumerate(cross.MYTHS):
        subject, sources = subject_of[target], sources_of[target]
        extra_axes, epistemic = special.get(identifier, ([], "established"))
        split = myth_splits[index % 4]
        myth_id = f"myth-{identifier}"
        records.append({**base(node(myth_id), subject, sources, split, "counterexample",
                               sorted({"errors_adversarial_misuse", "exceptions_boundaries", *extra_axes}), epistemic),
                        "label": label, "statement": statement, "aliases": []})
        records.append(relation(f"{PREFIX}.relation.counter-{identifier}", subject, sources, split, myth_id, target,
                                "counterexample",
                                f"{label} is a counterexample corrected by how {labels[target].lower()} actually works.",
                                f"the claim is applied to {labels[target].lower()}", "",
                                sorted({"errors_adversarial_misuse", "exceptions_boundaries", *extra_axes}),
                                f"counterexample {identifier.replace('-', ' ')}", epistemic))
        subject_of[myth_id], sources_of[myth_id], labels[myth_id] = subject, sources, label

    boundary_splits = ["train", "validation", "sealed_test", "train"]
    for index, (identifier, label, statement, target) in enumerate(cross.BOUNDARIES):
        subject, sources = subject_of[target], sources_of[target]
        split = boundary_splits[index % 4]
        boundary_id = f"boundary-{identifier}"
        records.append({**base(node(boundary_id), subject, sources, split, "boundary",
                               ["exceptions_boundaries", "assumptions_prerequisites"]),
                        "label": label, "statement": statement, "aliases": []})
        records.append(relation(f"{PREFIX}.relation.qualifies-{identifier}", subject, sources, split, boundary_id,
                                target, "qualifies", f"{label} qualifies where {labels[target].lower()} holds.",
                                f"the regime described by the boundary applies to {labels[target].lower()}", "",
                                ["exceptions_boundaries", "assumptions_prerequisites"],
                                f"boundary {identifier.replace('-', ' ')}"))

    example_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, label, statement, subject, clarified) in enumerate(cross.EXAMPLES):
        split = example_splits[index % 4]
        example_id = f"example-{identifier}"
        sources = sorted({s for c in clarified for s in sources_of[c]})
        records.append({**base(node(example_id), subject, sources, split, "worked_example",
                               ["applications_toolchains", "deductions_predictions_execution", "within_domain_composition"]),
                        "label": label, "statement": statement, "aliases": []})
        records.append(relation(f"{PREFIX}.example-membership.{identifier}", subject, sources, split, example_id,
                                "root", "part_of", f"The {label.lower()} example is part of the everyday physical causation world.",
                                "the example is a typical everyday case", "",
                                ["applications_toolchains", "within_domain_composition"], f"{label} membership"))
        for target in clarified:
            records.append(relation(f"{PREFIX}.relation.clarifies-{identifier}-{target}", subject, sources, split,
                                    example_id, target, "clarifies",
                                    f"The {label.lower()} example clarifies {labels[target].lower()} in a concrete case.",
                                    f"the example's everyday conditions hold for {labels[target].lower()}", "",
                                    ["applications_toolchains", "deductions_predictions_execution"],
                                    f"example clarifies {target.replace('-', ' ')}"))

    control_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, label, statement) in enumerate(CONTROLS):
        records.append({**base(node(f"control.{identifier}"), "physics.classical-mechanics", [],
                               control_splits[index % 4], "synthetic_control",
                               ["unknown_abstention", "errors_adversarial_misuse"], "synthetic_control"),
                        "label": label, "statement": statement, "aliases": [], "synthetic": True,
                        "tags": ["negative-control", "physical-causation"]})
    return sorted(records, key=lambda record: record["record_id"])


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
