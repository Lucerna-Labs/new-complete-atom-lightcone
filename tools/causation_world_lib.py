#!/usr/bin/env python3
"""Shared builder for standalone causation worlds (2026-10-02 sweep).

Each world is a data module in tools/causation_worlds/ exporting WORLD, PREFIX,
DOMAIN, SUBJECT, SOURCES, SCOPE, CONCEPTS, RELATIONS, MYTHS, BOUNDARIES,
EXAMPLES and CONTROLS; a thin tools/build_<name>_causation_curriculum.py calls
build_cli(module). Design rules mirror the physical-causation pilot: causal-first
relations, real polarity, one specific condition per relation, no generated
lowercase aliases.
"""

from __future__ import annotations

import collections
import json
import sys
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT

sys.path.insert(0, str(ROOT / "tools"))

LANES = ["reasoning.causal", "reasoning.deductive", "thinking.bottom_up"]
NEGATIVE = {"inhibits", "prevents", "contradicts", "undercuts", "counterexample"}
DEFAULT_LIMITATIONS = [
    "Statements are original structured summaries of the module's registered sources, not quotations.",
    "Facts are textbook-level and typical unless a condition narrows them.",
]


def node(prefix: str, identifier: str) -> str:
    return f"{prefix}.{identifier}"


def base(world: str, domain: str, record_id: str, subject: str, sources: list[str], split: str, kind: str,
         axes: list[str], tags: list[str], epistemic: str = "established") -> dict[str, Any]:
    return {
        "schema_version": 1, "record_id": record_id, "world_id": world, "domain_id": domain,
        "subject_id": subject, "lanes": LANES, "record_kind": kind, "epistemic_class": epistemic,
        "coverage_axes": axes, "source_ids": sorted(set(sources)),
        "split_group": record_id, "split": split, "tags": tags,
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


def relation(prefix: str, world: str, domain: str, record_id: str, subject: str, sources: list[str], split: str,
             src: str, dst: str, kind: str, statement: str, condition: str, exception: str,
             axes: list[str], label: str, tags: list[str], epistemic: str = "established") -> dict[str, Any]:
    return {
        **base(world, domain, record_id, subject, sources, split, "relation", axes, tags, epistemic),
        "label": label, "statement": statement, "aliases": [],
        "relation": {
            "source_node": node(prefix, src), "target_node": node(prefix, dst), "kind": kind,
            "polarity": -1 if kind in NEGATIVE else 1, "direction": "forward",
            "conditions": [condition] if condition else [], "exceptions": [exception] if exception else [],
        },
    }


def relation_axes(kind: str) -> list[str]:
    axes = ["mechanisms_causal_laws", "within_domain_composition"]
    axes.append({"predicts": "deductions_predictions_execution", "transforms_to": "representations_transformations",
                 "prerequisite": "assumptions_prerequisites", "inhibits": "exceptions_boundaries",
                 "prevents": "exceptions_boundaries"}.get(kind, "primitives_invariants"))
    return sorted(set(axes))


def build(module: Any) -> list[dict[str, Any]]:
    prefix, world, domain = module.PREFIX, module.WORLD, module.DOMAIN
    subject, sources, tags = module.SUBJECT, module.SOURCES, ["causation-world", world]
    limitations = getattr(module, "LIMITATIONS", None) or DEFAULT_LIMITATIONS
    subject_of: dict[str, str] = {}
    sources_of: dict[str, list[str]] = {}
    labels: dict[str, str] = {}
    records: list[dict[str, Any]] = []
    fill = {"scope": module.SCOPE, "limitations": limitations, "as_of": "2026-10-02",
            "version_boundary": world}

    def b(record_id: str, sub: str, srcs: list[str], split: str, kind: str, axes: list[str],
          epistemic: str = "established") -> dict[str, Any]:
        return {**fill, **base(world, domain, record_id, sub, srcs, split, kind, axes, tags, epistemic)}

    records.append({**b(node(prefix, "root"), subject, sources, "train", "concept",
                        ["definitions_scope", "primitives_invariants"]),
                    "label": module.ROOT_LABEL,
                    "statement": module.ROOT_STATEMENT, "aliases": []})
    index = 0
    for identifier, label, statement, aliases in module.CONCEPTS:
        index += 1
        assert identifier not in subject_of, f"duplicate concept {identifier}"
        subject_of[identifier], sources_of[identifier], labels[identifier] = subject, sources, label
        records.append({**b(node(prefix, identifier), subject, sources, split_for(index), "concept",
                            ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"]),
                        "label": label, "statement": statement, "aliases": aliases})
        records.append(relation(prefix, world, domain, f"{prefix}.membership.{identifier}", subject, sources,
                                split_for(index), identifier, "root", "part_of",
                                f"{label} is a distinct part of the {module.ROOT_LABEL.lower()}.",
                                f"{label.lower()} is described at everyday scale", "",
                                ["primitives_invariants", "within_domain_composition"],
                                f"{label} membership", tags))

    for identifier, src, dst, *_rest in module.RELATIONS:
        for endpoint in (src, dst):
            assert endpoint in subject_of, f"relation {identifier} references unknown concept {endpoint}"
    splitter = RelationSplitter([r[3] for r in module.RELATIONS])
    for (identifier, src, dst, kind, statement, condition, exception) in module.RELATIONS:
        records.append(relation(prefix, world, domain, f"{prefix}.relation.{identifier}", subject,
                                sorted(set(sources_of[src]) | set(sources_of[dst])), splitter.split(kind),
                                src, dst, kind, statement, condition, exception,
                                relation_axes(kind), identifier.replace("-", " "), tags))

    myth_splits = ["train", "validation", "sealed_test", "train"]
    for index, (identifier, label, statement, target) in enumerate(module.MYTHS):
        split = myth_splits[index % 4]
        myth_id = f"myth-{identifier}"
        records.append({**b(node(prefix, myth_id), subject_of[target], sources_of[target], split, "counterexample",
                            ["errors_adversarial_misuse", "exceptions_boundaries"]),
                        "label": label, "statement": statement, "aliases": []})
        records.append(relation(prefix, world, domain, f"{prefix}.relation.counter-{identifier}",
                                subject_of[target], sources_of[target], split, myth_id, target, "counterexample",
                                f"{label} is a counterexample corrected by how {labels[target].lower()} actually works.",
                                f"the claim is applied to {labels[target].lower()}", "",
                                ["errors_adversarial_misuse", "exceptions_boundaries"],
                                f"counterexample {identifier.replace('-', ' ')}", tags))
        labels[myth_id] = label

    boundary_splits = ["train", "validation", "sealed_test"]
    for index, (identifier, label, statement, target) in enumerate(module.BOUNDARIES):
        split = boundary_splits[index % 3]
        boundary_id = f"boundary-{identifier}"
        records.append({**b(node(prefix, boundary_id), subject_of[target], sources_of[target], split, "boundary",
                            ["exceptions_boundaries", "assumptions_prerequisites"]),
                        "label": label, "statement": statement, "aliases": []})
        records.append(relation(prefix, world, domain, f"{prefix}.relation.qualifies-{identifier}",
                                subject_of[target], sources_of[target], split, boundary_id, target, "qualifies",
                                f"{label} qualifies where {labels[target].lower()} holds.",
                                f"the regime described by the boundary applies to {labels[target].lower()}", "",
                                ["exceptions_boundaries", "assumptions_prerequisites"],
                                f"boundary {identifier.replace('-', ' ')}", tags))

    example_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, label, statement, clarified) in enumerate(module.EXAMPLES):
        split = example_splits[index % 4]
        example_id = f"example-{identifier}"
        example_sources = sorted({s for c in clarified for s in sources_of[c]})
        records.append({**b(node(prefix, example_id), subject, example_sources, split, "worked_example",
                            ["applications_toolchains", "deductions_predictions_execution", "within_domain_composition"]),
                        "label": label, "statement": statement, "aliases": []})
        records.append(relation(prefix, world, domain, f"{prefix}.example-membership.{identifier}", subject,
                                example_sources, split, example_id, "root", "part_of",
                                f"The {label.lower()} example is part of the {module.ROOT_LABEL.lower()}.",
                                "the example is a typical everyday case", "",
                                ["applications_toolchains", "within_domain_composition"], f"{label} membership", tags))
        for target in clarified:
            records.append(relation(prefix, world, domain, f"{prefix}.relation.clarifies-{identifier}-{target}",
                                    subject, example_sources, split, example_id, target, "clarifies",
                                    f"The {label.lower()} example clarifies {labels[target].lower()} in a concrete case.",
                                    f"the example's everyday conditions hold for {labels[target].lower()}", "",
                                    ["applications_toolchains", "deductions_predictions_execution"],
                                    f"example clarifies {target.replace('-', ' ')}", tags))

    control_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, label, statement) in enumerate(module.CONTROLS):
        records.append({**b(node(prefix, f"control.{identifier}"), subject, [], control_splits[index % 4],
                            "synthetic_control", ["unknown_abstention", "errors_adversarial_misuse"],
                            "synthetic_control"),
                        "label": label, "statement": statement, "aliases": [], "synthetic": True,
                        "tags": ["negative-control", *tags[1:]]})
    for record in records:
        record.update(fill)
    return sorted(records, key=lambda record: record["record_id"])


def build_cli(module: Any) -> int:
    records = build(module)
    output = ROOT / "curricula" / module.WORLD / "foundations.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in records),
                      encoding="utf-8")
    print(f"wrote {output} with {len(records)} records")
    print("splits:", dict(sorted(collections.Counter(r["split"] for r in records).items())))
    print("kinds:", dict(sorted(collections.Counter(r["record_kind"] for r in records).items())))
    return 0
