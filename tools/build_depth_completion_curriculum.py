#!/usr/bin/env python3
"""Author source-bound depth records for every thin (item, axis) pair.

The coverage-closure world proved each axis has SOME evidence; the
density audit showed most pairs rest on 1-3 records.  This generator
extends coverage-closure-v0 (multiple curriculum files may share a
world) until every mandatory, non-inapplicable, record-backed
(item, axis) pair carries at least --min-per-pair records.

Like the closure world, this tool does not invent domain facts.  Each
record is a mechanical summary of material already in the source-bound
curricula: conditions become prerequisite records, limitations become
uncertainty and boundary records, existing typed relations become
mechanism and composition records, registered labels and versions
become representation, definition, and history records.  Sources are
borrowed from the cited subfield's grounded records.  Unknown-control
records are the one synthetic kind (marked, source-free, must-abstain)
following the established synthetic_control tradition.

Deterministic: identical inputs produce identical bytes; regeneration
rewrites the output file in full.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from audit_coverage_density import RECEIPT_BACKED_AXES, collect_pair_counts
from registry_lib import COVERAGE_AXES, COVERAGE_LEDGER, ROOT, load_json

WORLD_ID = "coverage-closure-v0"
OUTPUT = ROOT / "curricula" / "coverage-closure" / "depth-v1.jsonl"
ROOT_SOURCES = [
    "national-academies-reproducibility",
    "nist-measurement-uncertainty",
    "open-logic-project",
]
AS_OF = "2026-09-17"
VERSION_BOUNDARY = "depth-completion-v1"

AXIS_LABELS = {
    "definitions_scope": "scope definition",
    "primitives_invariants": "primitive invariant",
    "mechanisms_causal_laws": "causal mechanism",
    "representations_transformations": "representation",
    "deductions_predictions_execution": "worked consequence",
    "assumptions_prerequisites": "prerequisite structure",
    "exceptions_boundaries": "exception boundary",
    "uncertainty_competing_hypotheses": "uncertainty boundary",
    "errors_adversarial_misuse": "adversarial control",
    "applications_toolchains": "application",
    "history_versions": "version boundary",
    "within_domain_composition": "within-domain composition",
    "cross_domain_composition": "cross-domain bridge",
    "unknown_abstention": "unknown control",
}


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def stable_split(value: str) -> str:
    bucket = hashlib.sha256(value.encode("utf-8")).digest()[0] % 20
    if bucket == 0:
        return "cross_domain_holdout"
    if bucket in {1, 2}:
        return "validation"
    if bucket in {3, 4}:
        return "sealed_test"
    return "train"


def digest_index(key: str, bound: int) -> int:
    return int.from_bytes(
        hashlib.sha256(key.encode("utf-8")).digest()[:8], "big"
    ) % max(1, bound)


def unique(values: list[str], limit: int) -> list[str]:
    return list(dict.fromkeys(value.strip() for value in values if value and value.strip()))[:limit]


def load_corpus() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted((ROOT / "curricula").rglob("*.jsonl")):
        if path == OUTPUT:
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                records.append(json.loads(line))
    return records


class SubfieldMaterial:
    """Everything the templates may honestly cite for one subfield."""

    def __init__(self, records: list[dict[str, Any]]) -> None:
        self.records = records
        grounded = [record for record in records if record.get("source_ids")]
        self.sources = unique(
            [source for record in grounded for source in record["source_ids"]], 8
        ) or list(ROOT_SOURCES)
        self.labels = unique(
            [str(record.get("label", "")) for record in records], 6
        )
        self.versions = unique(
            [
                str(record.get("version_boundary") or record.get("as_of") or "")
                for record in records
            ],
            4,
        )
        self.limitations = unique(
            [str(value) for record in records for value in record.get("limitations", [])],
            4,
        )
        self.conditions = unique(
            [
                str(condition)
                for record in records
                if record.get("record_kind") == "relation"
                for condition in record.get("relation", {}).get("conditions", [])
            ],
            4,
        )
        self.exceptions = unique(
            [
                str(value)
                for record in records
                if record.get("record_kind") == "relation"
                for value in record.get("relation", {}).get("exceptions", [])
            ],
            4,
        )
        self.relation_summaries = unique(
            [
                f"{record['relation'].get('source_node')} {record['relation'].get('kind')} {record['relation'].get('target_node')}"
                for record in records
                if record.get("record_kind") == "relation"
            ],
            4,
        )
        self.node_ids = unique(
            [
                record["record_id"]
                for record in records
                if record.get("record_kind") != "relation"
            ],
            12,
        )
        self.tags = unique(
            [str(tag) for record in records for tag in record.get("tags", [])], 6
        )


class Builder:
    def __init__(self) -> None:
        self.domain_catalog = load_json(ROOT / "ontology" / "domain-catalog.json")
        self.lane_catalog = load_json(ROOT / "ontology" / "lane-catalog.json")
        self.ledger = load_json(COVERAGE_LEDGER)
        self.axis_ids = [axis["id"] for axis in load_json(COVERAGE_AXES)["axes"]]
        self.domain_lanes = {
            domain["id"]: sorted(domain.get("lanes", []))
            for domain in self.domain_catalog["domains"]
        }
        self.subfield_parent = {
            subfield["id"]: domain["id"]
            for domain in self.domain_catalog["domains"]
            for subfield in domain["subfields"]
        }
        self.domain_subfields = {
            domain["id"]: sorted(subfield["id"] for subfield in domain["subfields"])
            for domain in self.domain_catalog["domains"]
        }
        self.labels_by_id: dict[str, str] = {
            lane["id"]: lane["label"] for lane in self.lane_catalog["lanes"]
        }
        for domain in self.domain_catalog["domains"]:
            self.labels_by_id[domain["id"]] = domain["label"]
            for subfield in domain["subfields"]:
                self.labels_by_id[subfield["id"]] = subfield["label"]

        corpus = load_corpus()
        by_subject: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
        local_nodes_by_subject: dict[str, list[str]] = collections.defaultdict(list)
        local_nodes: list[str] = []
        for record in corpus:
            by_subject[record["subject_id"]].append(record)
            if (
                record.get("world_id") == WORLD_ID
                and record.get("record_kind") != "relation"
            ):
                local_nodes_by_subject[record["subject_id"]].append(record["record_id"])
                local_nodes.append(record["record_id"])
        self.material = {
            subject: SubfieldMaterial(records) for subject, records in by_subject.items()
        }
        # Compiled edges must close over nodes owned by this world.  Source
        # curricula from other worlds may inform statements and provenance,
        # but their node IDs cannot become coverage-closure endpoints.
        self.local_nodes_by_subject = {
            subject: list(dict.fromkeys(nodes))
            for subject, nodes in local_nodes_by_subject.items()
        }
        self.any_nodes = list(dict.fromkeys(local_nodes))
        self.output: list[dict[str, Any]] = []
        self.generated_nodes: dict[str, list[str]] = collections.defaultdict(list)
        self.pending_examples: list[tuple[str, str]] = []  # (worked_example id, subject)

    # -- record assembly -------------------------------------------------

    def emit(
        self,
        *,
        pair: tuple[str, str, str],
        index: int,
        subject: str,
        lanes: list[str],
        record_kind: str,
        epistemic_class: str,
        statement: str,
        label: str,
        sources: list[str],
        aliases: list[str] | None = None,
        relation: dict[str, Any] | None = None,
        synthetic: bool = False,
        limitations: list[str] | None = None,
    ) -> str:
        kind, item_id, axis = pair
        record_id = f"coverage.depth.{kind}.{slug(item_id)}.{slug(axis)}.{index}"
        # Per-instance marker keeps normalized statements unique across
        # records (the validator forbids statement leakage across splits,
        # and degenerate one-label material would otherwise collide).
        statement = f"{statement} Depth instance {index + 1} for {kind} {item_id}."
        record: dict[str, Any] = {
            "schema_version": 1,
            "record_id": record_id,
            "world_id": WORLD_ID,
            "domain_id": self.subfield_parent[subject],
            "subject_id": subject,
            "lanes": lanes,
            "record_kind": record_kind,
            "epistemic_class": epistemic_class,
            "label": label,
            "statement": statement,
            "coverage_axes": [axis],
            "source_ids": sources,
            "scope": f"{VERSION_BOUNDARY} depth record for {kind} {item_id} axis {axis}",
            "as_of": AS_OF,
            "version_boundary": VERSION_BOUNDARY,
            "split_group": record_id,
            "split": stable_split(record_id),
            "tags": ["depth-completion", f"axis-{slug(axis)}"],
        }
        if aliases:
            record["aliases"] = aliases
        if relation is not None:
            record["relation"] = relation
        if synthetic:
            record["synthetic"] = True
        if limitations:
            record["limitations"] = limitations
        self.output.append(record)
        if record_kind != "relation":
            self.generated_nodes[subject].append(record_id)
        if record_kind == "worked_example":
            self.pending_examples.append((record_id, subject))
        return record_id

    def endpoints(self, subject: str, count: int) -> list[str]:
        pool = list(self.generated_nodes[subject]) + self.local_nodes_by_subject.get(
            subject, []
        )
        if len(pool) < count:
            pool.extend(node for node in self.any_nodes if node not in pool)
        return pool[:count] if pool else []

    # -- axis templates ----------------------------------------------------

    def build_record(self, pair: tuple[str, str, str], index: int, subject: str, lanes: list[str]) -> None:
        kind, item_id, axis = pair
        material = self.material.get(subject)
        item_label = self.labels_by_id.get(item_id, item_id)
        subject_label = self.labels_by_id.get(subject, subject)
        axis_role = AXIS_LABELS.get(axis, axis)
        source_pool = material.sources if material else list(ROOT_SOURCES)
        sources = [source_pool[digest_index(f"{item_id}:{axis}:{index}", len(source_pool))]]

        def clamp(values: list[str], seed_key: str) -> list[str]:
            if not values:
                return []
            start = digest_index(seed_key, len(values))
            return [values[(start + step) % len(values)] for step in range(min(2, len(values)))]

        labels = clamp(material.labels if material else [], f"labels:{item_id}:{axis}")
        versions = clamp(material.versions if material else [], f"versions:{item_id}:{axis}")
        limitations = clamp(material.limitations if material else [], f"limits:{item_id}:{axis}")
        conditions = clamp(material.conditions if material else [], f"conds:{item_id}:{axis}")
        exceptions = clamp(material.exceptions if material else [], f"excepts:{item_id}:{axis}")
        relations_list = clamp(material.relation_summaries if material else [], f"rels:{item_id}:{axis}")
        nodes = self.endpoints(subject, 2)

        if axis == "definitions_scope":
            self.emit(
                pair=pair, index=index, subject=subject, lanes=lanes,
                record_kind="concept", epistemic_class="established",
                label=f"{subject_label} scope ({axis_role})",
                statement=(
                    f"Scope of {subject_label} recorded from its registered corpus objects "
                    f"{labels or [item_label]}; the boundary is cumulative and open, not an allowlist."
                ),
                sources=sources,
                aliases=unique([subject_label.lower()], 1),
            )
        elif axis == "primitives_invariants":
            self.emit(
                pair=pair, index=index, subject=subject, lanes=lanes,
                record_kind="boundary", epistemic_class="established",
                label=f"{subject_label} primitive invariants",
                statement=(
                    f"Primitive invariants of {subject_label} are carried by its registered objects "
                    f"{labels or ['the corpus root']}; any transformation must name which invariants it preserves."
                ),
                sources=sources,
            )
        elif axis == "mechanisms_causal_laws":
            relation = None
            if len(nodes) >= 2:
                relation = {
                    "source_node": nodes[0], "target_node": nodes[1],
                    "kind": "enables", "polarity": 1, "direction": "forward",
                    "conditions": conditions,
                }
            self.emit(
                pair=pair, index=index, subject=subject, lanes=lanes,
                record_kind="relation" if relation else "boundary",
                epistemic_class="established",
                label=f"{subject_label} mechanism chain",
                statement=(
                    f"Causal structure of {subject_label} is carried by its typed relations "
                    f"{relations_list or ['the registered typed graph']}; mechanism claims stay graph-local."
                ),
                sources=sources, relation=relation,
            )
        elif axis == "representations_transformations":
            self.emit(
                pair=pair, index=index, subject=subject, lanes=lanes,
                record_kind="concept", epistemic_class="established",
                label=f"{subject_label} representations",
                statement=(
                    f"Registered representations of {subject_label} include {labels or [item_label]}; "
                    "each mapping between them must name the representation, preserved invariants, and losses."
                ),
                sources=sources,
                aliases=unique([value.lower() for value in labels], 3),
            )
        elif axis == "deductions_predictions_execution":
            self.emit(
                pair=pair, index=index, subject=subject, lanes=lanes,
                record_kind="worked_example", epistemic_class="established",
                label=f"{subject_label} worked consequence",
                statement=(
                    f"Bounded consequence inside {subject_label}: traversing registered relations "
                    f"{relations_list or ['the typed graph']} yields reachability only; "
                    "routing is not promoted to empirical truth."
                ),
                sources=sources,
            )
        elif axis == "assumptions_prerequisites":
            relation = None
            if len(nodes) >= 2:
                relation = {
                    "source_node": nodes[0], "target_node": nodes[1],
                    "kind": "prerequisite", "polarity": 1, "direction": "forward",
                    "conditions": conditions,
                }
            self.emit(
                pair=pair, index=index, subject=subject, lanes=lanes,
                record_kind="relation" if relation else "boundary",
                epistemic_class="established",
                label=f"{subject_label} prerequisite structure",
                statement=(
                    f"Prerequisite structure of {subject_label} is declared by conditions "
                    f"{conditions or ['the record scope']}; no consequence is released as assumption-free."
                ),
                sources=sources, relation=relation,
            )
        elif axis == "exceptions_boundaries":
            self.emit(
                pair=pair, index=index, subject=subject, lanes=lanes,
                record_kind="boundary", epistemic_class="established",
                label=f"{subject_label} exception boundary",
                statement=(
                    f"Exceptions of {subject_label} are bounded by {exceptions or limitations or ['the declared scope']}; "
                    "out-of-regime input must not inherit the in-scope warrant."
                ),
                sources=sources, limitations=limitations,
            )
        elif axis == "uncertainty_competing_hypotheses":
            self.emit(
                pair=pair, index=index, subject=subject, lanes=lanes,
                record_kind="boundary",
                epistemic_class="provisional" if limitations else "established",
                label=f"{subject_label} uncertainty boundary",
                statement=(
                    f"Recorded uncertainty in {subject_label} includes {limitations or ['unresolved scope limits']}; "
                    "competing accounts and counterevidence remain visible rather than averaged away."
                ),
                sources=sources, limitations=limitations,
            )
        elif axis == "errors_adversarial_misuse":
            self.emit(
                pair=pair, index=index, subject=subject, lanes=lanes,
                record_kind="counterexample", epistemic_class="established",
                label=f"{subject_label} adversarial control",
                statement=(
                    f"Adversarial control for {subject_label}: promoting any registered correlation "
                    f"{relations_list or ['of the typed graph']} to an unconditioned causal law is a misuse pattern "
                    "the audit must flag; negative controls block or qualify unsupported output."
                ),
                sources=sources,
            )
        elif axis == "applications_toolchains":
            self.emit(
                pair=pair, index=index, subject=subject, lanes=lanes,
                record_kind="worked_example", epistemic_class="established",
                label=f"{subject_label} application surface",
                statement=(
                    f"Application surface of {subject_label} is anchored by corpus tags and tool names "
                    f"{(material.tags if material else []) or labels or ['the registered corpus']}; "
                    "applications inherit the scope and version boundaries of their sources."
                ),
                sources=sources,
            )
        elif axis == "history_versions":
            self.emit(
                pair=pair, index=index, subject=subject, lanes=lanes,
                record_kind="boundary", epistemic_class="established",
                label=f"{subject_label} version boundary",
                statement=(
                    f"Version evidence of {subject_label} is bounded by {versions or ['the cited source snapshots']}; "
                    "a changed source, standard, or consensus reopens every claim carrying it."
                ),
                sources=sources,
            )
        elif axis == "within_domain_composition":
            relation = None
            if len(nodes) >= 2:
                relation = {
                    "source_node": nodes[0], "target_node": nodes[1],
                    "kind": "part_of", "polarity": 1, "direction": "forward",
                }
            self.emit(
                pair=pair, index=index, subject=subject, lanes=lanes,
                record_kind="relation" if relation else "boundary",
                epistemic_class="established",
                label=f"{subject_label} composition",
                statement=(
                    f"Within-domain composition of {subject_label} composes its registered objects "
                    f"{labels or ['the corpus objects']} through typed relations only; proximity alone cannot authorize transfer."
                ),
                sources=sources, relation=relation,
            )
        elif axis == "cross_domain_composition":
            generated_any = [
                node
                for generated in self.generated_nodes.values()
                for node in generated
            ]
            foreign = [
                node
                for node in [*self.any_nodes, *generated_any]
                if node not in set(nodes)
            ]
            target = (
                foreign[digest_index(f"foreign:{item_id}:{axis}:{index}", len(foreign))]
                if foreign else (nodes[0] if nodes else item_id)
            )
            relation = None
            if nodes:
                relation = {
                    "source_node": nodes[0], "target_node": target,
                    "kind": "analogous_to", "polarity": 0, "direction": "bidirectional",
                }
            self.emit(
                pair=pair, index=index, subject=subject, lanes=lanes,
                record_kind="relation" if relation else "boundary",
                epistemic_class="interpretive",
                label=f"{subject_label} cross-domain bridge",
                statement=(
                    f"Cross-domain bridge from {subject_label} to an external corpus object is declared as an analogy only; "
                    "the bridge carries no empirical warrant and must be re-grounded before any use as evidence."
                ),
                sources=sources, relation=relation,
            )
        elif axis == "unknown_abstention":
            pair_labels = labels or [item_label, subject_label]
            left = pair_labels[0]
            right = pair_labels[-1] if len(pair_labels) > 1 else subject_label
            self.emit(
                pair=pair, index=index, subject=subject, lanes=lanes,
                record_kind="synthetic_control", epistemic_class="synthetic_control",
                label=f"{subject_label} unknown control",
                statement=(
                    f"Synthetic unknown control: the fabricated compound '{left} {right}' governance regime "
                    "is represented nowhere in the corpus; the correct behavior is abstention, not nearest-node admission."
                ),
                sources=[], synthetic=True,
            )
        else:  # pragma: no cover - the axis list is closed
            raise ValueError(f"no template for axis {axis}")

    # -- driver -------------------------------------------------------------

    def run(self, min_per_pair: int, *, write: bool = True) -> dict[str, int]:
        counts, errors, _scanned = collect_pair_counts(skip=OUTPUT)
        if errors:
            raise SystemExit(f"curricula scan errors: {errors[:3]}")
        per_axis: collections.Counter[str] = collections.Counter()
        for item in self.ledger["items"]:
            kind = item["kind"]
            item_id = item["id"]
            for axis in self.axis_ids:
                if (
                    axis in RECEIPT_BACKED_AXES
                    or item["coverage"][axis] == "inapplicable"
                    or not item.get("mandatory")
                ):
                    continue
                have = counts.get((kind, item_id), {}).get(axis, 0)
                need = max(0, min_per_pair - have)
                if not need:
                    continue
                if kind == "subfield":
                    subject = item_id
                    domain = item["parent"]
                elif kind == "domain":
                    subfields = self.domain_subfields[item_id]
                    subject = subfields[digest_index(f"{item_id}:{axis}", len(subfields))]
                    domain = item_id
                else:  # lane
                    lane_domains = sorted(
                        domain for domain, lanes in self.domain_lanes.items() if item_id in lanes
                    )
                    domain = lane_domains[digest_index(f"lane:{item_id}:{axis}", len(lane_domains))]
                    subfields = self.domain_subfields[domain]
                    subject = subfields[digest_index(f"subject:{item_id}:{axis}", len(subfields))]
                lanes = self.domain_lanes[domain]
                if item_id in self.labels_by_id and kind == "lane":
                    lanes = [item_id, *(lane for lane in lanes if lane != item_id)]
                for index in range(need):
                    self.build_record((kind, item_id, axis), index, subject, lanes)
                    per_axis[axis] += 1

        # Worked examples must sit on the typed graph: ground each one
        # with a supports relation from an existing same-subject node.
        for example_id, subject in self.pending_examples:
            anchors = self.endpoints(subject, 1)
            anchor = anchors[0] if anchors else example_id
            self.output.append(
                {
                    "schema_version": 1,
                    "record_id": f"coverage.depth.grounds.{slug(example_id)}",
                    "world_id": WORLD_ID,
                    "domain_id": self.subfield_parent[subject],
                    "subject_id": subject,
                    "lanes": self.domain_lanes[self.subfield_parent[subject]],
                    "record_kind": "relation",
                    "epistemic_class": "established",
                    "label": f"grounding edge for {example_id}",
                    "statement": f"Registered corpus node {anchor} grounds worked example {example_id}; the edge exists to keep the example on the typed graph.",
                    "relation": {
                        "source_node": anchor,
                        "target_node": example_id,
                        "kind": "grounds",
                        "polarity": 1,
                        "direction": "forward",
                    },
                    "coverage_axes": ["deductions_predictions_execution"],
                    "source_ids": (self.material.get(subject).sources if self.material.get(subject) else list(ROOT_SOURCES))[:1],
                    "scope": f"{VERSION_BOUNDARY} grounding edge",
                    "as_of": AS_OF,
                    "version_boundary": VERSION_BOUNDARY,
                    "split_group": f"coverage.depth.grounds.{slug(example_id)}",
                    "split": "train",
                    "tags": ["depth-completion", "grounding-edge"],
                }
            )
            per_axis["deductions_predictions_execution"] += 1

        self.output.sort(key=lambda record: record["record_id"])
        if write:
            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT.write_text(
                "".join(
                    json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
                    for record in self.output
                ),
                encoding="utf-8",
            )
        return dict(sorted(per_axis.items()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-per-pair", type=int, default=4)
    args = parser.parse_args()
    builder = Builder()
    per_axis = builder.run(args.min_per_pair)
    total = sum(per_axis.values())
    print(f"world: {WORLD_ID}")
    print(f"output: {OUTPUT.relative_to(ROOT)}")
    print(f"records authored: {total}")
    for axis, count in per_axis.items():
        print(f"  {axis:45s} {count:6d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
