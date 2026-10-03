#!/usr/bin/env python3
"""Author the Rust coding causation world (standalone pilot world, 2026-10-02).

Content lives in tools/rust_coding/*.py. Design rules mirror the
physical-causation pilot: causal-first relations, real polarity, one specific
condition per relation, no generated lowercase aliases.
"""

from __future__ import annotations

import collections
import json
import sys
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT

sys.path.insert(0, str(ROOT / "tools"))
from rust_coding import ownership_borrowing  # noqa: E402

OUTPUT = ROOT / "curricula" / "rust-coding" / "foundations.jsonl"
WORLD = "rust-coding-v0"
PREFIX = "rc"
DOMAIN = "language-ecosystems"
SUBJECT = ownership_borrowing.SUBJECT
LANES = ["reasoning.causal", "reasoning.deductive", "thinking.bottom_up"]
SUBFIELDS = [ownership_borrowing]
NEGATIVE = {"inhibits", "prevents", "contradicts", "undercuts", "counterexample"}
LIMITATIONS = [
    "Statements describe Rust 1.63+ ownership, standard-library and Cargo behavior; sources were checked against Rust 1.99 documentation on 2026-10-02.",
    "Statements are original structured summaries of cited sources, not quotations.",
    "Safe-code guarantees assume sound unsafe dependencies; explicit scope, lifetime, panic-strategy and implementation conditions remain part of each relation.",
]
# (id, label, statement, target concept)
MYTHS = [
    ("unsafe-disables-checker", "unsafe blocks turn off the borrow checker",
     "Ordinary reference borrowing is still checked inside unsafe blocks; unsafe permits specified extra operations whose safety obligations remain the programmer's responsibility.", "borrow-checker"),
    ("hidden-gc", "Rust requires a hidden tracing garbage collector",
     "Rust has no mandatory tracing collector; ownership and drop govern ordinary values, while Rc and Arc provide explicit reference counting and can leak cycles.", "drop-at-scope"),
    ("clone-moves-source", "clone() moves the original value",
     "Clone::clone borrows the source through &self and returns another value without moving that source; Rc, Arc and reference clones may share their referent.", "clone-call"),
    ("generics-checked-at-runtime", "Generic type checking waits until run time",
     "Rust checks generic type constraints at compile time; rustc specializes used generic code, but a generic body may still contain dynamic trait-object calls.", "monomorphization"),
    ("rc-thread-safe", "The same Rc ownership group can safely cross threads",
     "Standard Rc is neither Send nor Sync; its ownership group cannot be transferred or shared through APIs requiring those traits merely because its payload is thread-safe.", "rc-sharing"),
    ("rust-kills-all-bugs", "Rust's compile checks eliminate every kind of bug",
     "Safe Rust with sound unsafe dependencies rules out undefined memory accesses and data races; logic errors, leaks, deadlocks and higher-level race conditions can remain.", "compile-rejection"),
]
# (id, label, statement, target concept)
BOUNDARIES = [
    ("unsafe-extra-operations", "unsafe extends permitted operations",
     "References inside unsafe blocks still obey borrowing, aliasing and validity requirements; unsafe operations such as raw-pointer dereference require additional proof and do not disable the borrow checker.", "borrow-checker"),
    ("leaks-are-safe", "Leaks do not imply memory unsafety",
     "Safe code may forget a value or retain a strong reference cycle, so eventual destruction and deallocation are not universal Rust safety guarantees.", "leaked-memory"),
    ("races-beyond-data-races", "Safe Rust excludes data races, not all races",
     "With sound unsafe dependencies, safe Rust excludes data races; separately locked operations can still interleave into logical errors, and locking can deadlock.", "data-race"),
    ("scoped-threads-borrow", "Scoped threads admit non-static references",
     "std::thread::scope has been stable since Rust 1.63 and permits references to data that outlives the scope; its scoped threads are joined before it returns, unlike the 'static requirement of std::thread::spawn.", "thread-spawn"),
    ("static-does-not-mean-immortal", "A static type bound does not make a value immortal",
     "An owned value satisfying the static lifetime bound can be dropped normally; the bound limits borrowed references it contains, rather than forcing its allocation to last for the entire program.", "thread-spawn"),
    ("drop-retains-borrow", "Destructor use extends required borrows",
     "The last explicit read does not end a borrow if a Drop implementation may later access the stored reference; drop checking preserves that required lifetime.", "last-use"),
]
# (id, label, statement, clarified concepts)
EXAMPLES = [
    ("string-move", "Passing a String to a function",
     "Passing s: String by value consumes s; reading s afterward is rejected unless it is reinitialized, while passing s.clone() leaves the original binding initialized.",
     ["move-of-value", "moved-binding", "clone-call"]),
    ("loop-push-conflict", "Iterating a vector while pushing",
     "A for loop borrowing &values keeps the iterator's shared borrow required while values.push needs a conflicting mutable borrow of the same vector, so the compiler rejects that overlap.",
     ["aliasing-rule", "shared-borrow", "mutable-borrow"]),
    ("arc-mutex-counter", "Sharing a counter across threads",
     "Arc<Mutex<u64>> handles can move into threads; each thread locks the same mutex before updating the counter and guard drop unlocks it.",
     ["arc-sharing", "mutex-guard", "send-marker", "mutex-unlock"]),
    ("file-question-mark", "Reading a file with the question mark",
     "In a function returning Result<String, std::io::Error>, applying ? to an Err from a file operation returns that error early; an Ok value continues normally.",
     ["question-mark", "result-enum"]),
]
CONTROLS = [
    ("checker-runtime", "Borrow checking happens while the program runs",
     "Rust compiler borrow checking must not be treated as runtime checking; RefCell's separate dynamic borrow checks do not change that distinction."),
    ("drop-frees-nothing", "Dropping an ordinary owning Box releases nothing",
     "Dropping an ordinary Box that retains a nonzero allocation and completes destruction must not be treated as leaving that allocation unreleased."),
    ("cargo-edits-source", "Cargo compilation automatically repairs source code",
     "Ordinary Cargo compilation must not be treated as automatically repairing program source; custom build scripts are separately executable code."),
    ("send-adds-lock", "The Send marker adds a run-time lock",
     "The Send marker trait must not be treated as adding a runtime lock or making every operation thread-safe."),
]


def node(identifier: str) -> str:
    return f"{PREFIX}.{identifier}"


def base(record_id: str, subject: str, sources: list[str], split: str, kind: str,
         axes: list[str], epistemic: str = "established") -> dict[str, Any]:
    return {
        "schema_version": 1, "record_id": record_id, "world_id": WORLD, "domain_id": DOMAIN,
        "subject_id": subject, "lanes": LANES, "record_kind": kind, "epistemic_class": epistemic,
        "coverage_axes": axes, "source_ids": sorted(set(sources)),
        "scope": "Everyday Rust programming: ownership, moves, borrows, lifetimes, drop, shared ownership, thread safety, error handling, generics, cargo builds",
        "limitations": LIMITATIONS, "as_of": "2026-10-02", "version_boundary": WORLD,
        "split_group": record_id, "split": split, "tags": ["rust-coding"],
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


def relation_axes(kind: str) -> list[str]:
    axes = ["mechanisms_causal_laws", "within_domain_composition"]
    axes.append({"predicts": "deductions_predictions_execution", "transforms_to": "representations_transformations",
                 "prerequisite": "assumptions_prerequisites", "inhibits": "exceptions_boundaries",
                 "prevents": "exceptions_boundaries"}.get(kind, "primitives_invariants"))
    return sorted(set(axes))


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    subject_of: dict[str, str] = {}
    sources_of: dict[str, list[str]] = {}
    labels: dict[str, str] = {}
    all_sources = sorted({s for m in SUBFIELDS for s in m.SOURCES})
    records.append({
        **base(node("root"), SUBJECT, all_sources, "train", "concept",
               ["definitions_scope", "primitives_invariants"]),
        "label": "Rust coding causation world",
        "statement": "Root of the Rust coding causation world: how ownership, borrowing, lifetimes and their toolchain enforce what Rust programs can and cannot do.",
        "aliases": [],
    })
    index = 0
    for module in SUBFIELDS:
        for identifier, label, statement, aliases in module.CONCEPTS:
            index += 1
            assert identifier not in subject_of, f"duplicate concept {identifier}"
            subject_of[identifier], sources_of[identifier], labels[identifier] = module.SUBJECT, module.SOURCES, label
            records.append({**base(node(identifier), module.SUBJECT, module.SOURCES, split_for(index), "concept",
                                   ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"]),
                            "label": label, "statement": statement, "aliases": aliases})
            records.append(relation(f"{PREFIX}.membership.{identifier}", module.SUBJECT, module.SOURCES,
                                    split_for(index), identifier, "root", "part_of",
                                    f"{label} is a distinct part of the Rust coding causation world.",
                                    f"{label.lower()} applies to Rust code compiled by the current stable compiler", "",
                                    ["primitives_invariants", "within_domain_composition"], f"{label} membership"))

    authored = [(m.SUBJECT, r) for m in SUBFIELDS for r in m.RELATIONS]
    for _, (identifier, src, dst, *_rest) in authored:
        for endpoint in (src, dst):
            assert endpoint in subject_of, f"relation {identifier} references unknown concept {endpoint}"
    splitter = RelationSplitter([r[3] for _, r in authored])
    for (subject, (identifier, src, dst, kind, statement, condition, exception)) in authored:
        records.append(relation(f"{PREFIX}.relation.{identifier}", subject,
                                sorted(set(sources_of[src]) | set(sources_of[dst])), splitter.split(kind),
                                src, dst, kind, statement, condition, exception,
                                relation_axes(kind), identifier.replace("-", " ")))

    myth_splits = ["train", "validation", "sealed_test", "train"]
    for index, (identifier, label, statement, target) in enumerate(MYTHS):
        subject, sources = subject_of[target], sources_of[target]
        split = myth_splits[index % 4]
        myth_id = f"myth-{identifier}"
        records.append({**base(node(myth_id), subject, sources, split, "counterexample",
                               ["errors_adversarial_misuse", "exceptions_boundaries"]),
                        "label": label, "statement": statement, "aliases": []})
        records.append(relation(f"{PREFIX}.relation.counter-{identifier}", subject, sources, split, myth_id, target,
                                "counterexample",
                                f"{label} is a counterexample corrected by how {labels[target].lower()} actually works.",
                                f"the claim is applied to {labels[target].lower()}", "",
                                ["errors_adversarial_misuse", "exceptions_boundaries"],
                                f"counterexample {identifier.replace('-', ' ')}"))
        subject_of[myth_id], sources_of[myth_id], labels[myth_id] = subject, sources, label

    boundary_splits = ["train", "validation", "sealed_test"]
    for index, (identifier, label, statement, target) in enumerate(BOUNDARIES):
        subject, sources = subject_of[target], sources_of[target]
        split = boundary_splits[index % 3]
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
    for index, (identifier, label, statement, clarified) in enumerate(EXAMPLES):
        split = example_splits[index % 4]
        example_id = f"example-{identifier}"
        sources = sorted({s for c in clarified for s in sources_of[c]})
        records.append({**base(node(example_id), SUBJECT, sources, split, "worked_example",
                               ["applications_toolchains", "deductions_predictions_execution", "within_domain_composition"]),
                        "label": label, "statement": statement, "aliases": []})
        records.append(relation(f"{PREFIX}.example-membership.{identifier}", SUBJECT, sources, split, example_id,
                                "root", "part_of", f"The {label.lower()} example is part of the Rust coding causation world.",
                                "the example is a typical everyday Rust case", "",
                                ["applications_toolchains", "within_domain_composition"], f"{label} membership"))
        for target in clarified:
            records.append(relation(f"{PREFIX}.relation.clarifies-{identifier}-{target}", SUBJECT, sources, split,
                                    example_id, target, "clarifies",
                                    f"The {label.lower()} example clarifies {labels[target].lower()} in a concrete case.",
                                    f"the example's everyday Rust conditions hold for {labels[target].lower()}", "",
                                    ["applications_toolchains", "deductions_predictions_execution"],
                                    f"example clarifies {target.replace('-', ' ')}"))

    control_splits = ["train", "validation", "sealed_test", "cross_domain_holdout"]
    for index, (identifier, label, statement) in enumerate(CONTROLS):
        records.append({**base(node(f"control.{identifier}"), SUBJECT, [],
                               control_splits[index % 4], "synthetic_control",
                               ["unknown_abstention", "errors_adversarial_misuse"], "synthetic_control"),
                        "label": label, "statement": statement, "aliases": [], "synthetic": True,
                        "tags": ["negative-control", "rust-coding"]})
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
