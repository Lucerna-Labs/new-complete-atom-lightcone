#!/usr/bin/env python3
"""Author computer-science and distributed cloud/data-system foundations."""

from __future__ import annotations

import json
from typing import Any

from curriculum_split import RelationSplitter
from registry_lib import ROOT


OUTPUT = ROOT / "curricula" / "computer-data-systems" / "foundations.jsonl"
WORLD = "computer-data-systems-v0"
LANES = ["reasoning.deductive", "reasoning.causal", "thinking.bottom_up", "geometry.structural", "reasoning.probabilistic"]
CS_SOURCES = ["cs2023-curricula", "msc2020", "open-logic-project", "llvm-langref", "riscv-unprivileged", "webassembly-core"]
DATA_SOURCES = ["raft-consensus-paper", "postgresql18-docs", "nist-cloud-800-145", "kubernetes-concepts", "nist-sp800-218"]


CS = [
    ("computer-science.algorithms", "algorithms", "Algorithms", "Algorithms are finite, precisely specified procedures whose correctness and resource use are analyzed over declared inputs and computation models.", "Algorithm invariant", "An invariant relates intermediate state to the specification before and after each step.", "Correctness and complexity", "Preconditions, transitions, termination, postconditions, and cost recurrence jointly establish an algorithm's result and resource bounds.", "Fast examples prove asymptotic efficiency", "A few timings must not establish asymptotic complexity, correctness, or performance on another machine model."),
    ("computer-science.data-structures", "data-structures", "Data structures", "Data structures organize values and relationships to support operations under time, space, locality, mutability, persistence, and concurrency tradeoffs.", "Representation invariant", "A representation invariant defines which memory or graph states correspond to valid abstract values.", "Operation preservation", "Each constructor and mutator transforms valid state to valid state while meeting the abstract operation contract.", "Same big-O means equivalent", "Equal asymptotic bounds must not erase constants, locality, memory, update pattern, concurrency, and workload differences."),
    ("computer-science.complexity", "complexity", "Computational complexity", "Complexity theory classifies problems and algorithms by resource growth, reductions, models, approximation, randomness, and parameterization.", "Problem language", "A decision problem is represented as a language of encoded instances with an input-size measure.", "Reduction", "A reduction transforms instances while preserving answers and bounding resources, transferring hardness or algorithmic consequences.", "NP means impossible", "Membership or hardness in NP must not be described as a proof that every practical instance is unsolvable."),
    ("computer-science.computability", "computability", "Computability", "Computability theory studies which functions and decision problems can be solved by idealized effective procedures and which cannot.", "Computable function", "A computable function is produced by a terminating effective procedure on every input in its domain.", "Diagonalization", "Self-reference and enumeration can construct an object differing from every listed candidate and prove noncomputability or incompleteness results.", "Undecidable means no instance can be solved", "Undecidability of a general problem must not imply that no restricted instance or incomplete method can be useful."),
    ("computer-science.automata", "automata", "Automata and formal languages", "Automata theory relates machines, grammars, languages, state, memory, parsing, closure, and expressive power.", "Automaton state", "An automaton state summarizes the history relevant to future acceptance under its transition model.", "Language recognition", "Reading symbols transforms machine state, and acceptance conditions determine membership in the recognized language.", "Regex and parser are universally equivalent", "Regular expressions must not be used for language structures requiring memory beyond the selected regular model."),
    ("computer-science.concurrency", "concurrency", "Concurrency", "Concurrency studies overlapping activities, synchronization, memory ordering, races, deadlocks, progress, communication, and composition.", "Concurrent history", "A history records invocation, response, reads, writes, messages, synchronization, and ordering relations among operations.", "Synchronization relation", "Locks, atomics, channels, transactions, and barriers constrain allowed interleavings and visibility under a memory model.", "No data race means correct", "Race freedom must not be treated as freedom from deadlock, starvation, atomicity, ordering, and higher-level logic errors."),
    ("computer-science.distributed-theory", "distributed-theory", "Distributed computing theory", "Distributed theory studies computation by independent nodes communicating with delay, loss, reordering, duplication, failure, partial knowledge, and adversarial schedules.", "Distributed execution", "A distributed execution is a partially ordered set of local steps, messages, failures, and observations rather than one global clock sequence.", "Impossibility boundary", "Failure and timing assumptions determine whether safety, liveness, consensus, and failure detection can be achieved.", "Timeout proves node failure", "A timeout must not distinguish failed, slow, partitioned, overloaded, and lost-message nodes without stronger assumptions."),
    ("computer-science.computer-architecture", "computer-architecture", "Computer architecture", "Computer architecture connects instruction sets, pipelines, memory hierarchies, parallel execution, I/O, coherence, accelerators, and performance.", "Architectural state", "Architectural state is the programmer-visible registers, memory, control, and exception state promised by the ISA.", "Microarchitectural execution", "Pipelines, speculation, caches, predictors, out-of-order scheduling, and coherence implement architectural effects under ordering constraints.", "Instruction count alone predicts speed", "Instruction count must not replace latency, parallelism, cache, branch, vector, frequency, and memory-system evidence."),
    ("computer-science.graphics", "graphics", "Computer graphics", "Computer graphics models geometry, materials, light, cameras, sampling, animation, rasterization, and interaction to synthesize images.", "Scene representation", "A scene represents geometry, transforms, materials, lights, cameras, animation, and spatial relationships.", "Rendering equation approximation", "Light transport, visibility, scattering, sampling, and reconstruction transform a scene into pixel estimates with error and noise.", "Rendered image proves physical reality", "A plausible rendering must not be treated as a calibrated photograph, physical simulation, or evidence of a real event."),
    ("computer-science.computational-science", "computational-science", "Computational science", "Computational science combines mathematical models, discretization, algorithms, software, high-performance execution, verification, validation, and uncertainty.", "Discretized model", "A discretization maps continuous equations and domains into finite algebraic state with resolution and truncation error.", "Verification-validation loop", "Code verification, solution verification, calibration, validation, sensitivity, and uncertainty connect computation to scientific claims.", "More resolution guarantees truth", "Grid refinement must not establish model validity, correct boundary conditions, stable numerics, or agreement with reality."),
    ("computer-science.quantum-computing", "quantum-computing", "Quantum computing", "Quantum computing studies algorithms, circuits, complexity, compilation, noise, error correction, hardware, and classical coordination for quantum information processors.", "Quantum computational state", "A quantum computation evolves amplitudes over a Hilbert space while measurement exposes only sampled classical outcomes.", "Circuit compilation", "Logical operations are decomposed, routed, scheduled, error-managed, and mapped to calibrated hardware instructions.", "Exponential state dimension gives free exponential answers", "A quantum state containing many amplitudes must not be described as allowing all classical values to be read out."),
]


DATA = [
    ("distributed-cloud-data.distributed-systems", "distributed-systems", "Distributed systems", "Distributed systems coordinate independent processes across networks while preserving identity, state, time, failures, retries, and observable contracts.", "Distributed component", "A component owns local state and communicates through messages whose delivery and ordering are uncertain.", "End-to-end protocol", "Correlation, idempotency, timeouts, retries, deduplication, state machines, and reconciliation compose a reliable service from unreliable boundaries.", "Happy path is system behavior", "Successful local calls must not establish behavior under partition, duplicate, delay, restart, overload, and partial failure."),
    ("distributed-cloud-data.consensus", "consensus", "Consensus and replication", "Consensus lets fault-tolerant nodes agree on an ordered decision or log under explicit failure and timing assumptions.", "Replicated log", "A replicated log is an ordered sequence of commands whose committed prefix must agree across state-machine replicas.", "Quorum leadership", "Terms, elections, majorities, log matching, commitment, and state-machine application preserve safety and conditional progress.", "Majority alive always guarantees progress", "A live majority must not guarantee progress when timing, configuration, disk, networking, or repeated split votes violate liveness assumptions."),
    ("distributed-cloud-data.storage", "storage", "Storage systems", "Storage systems map logical objects and bytes onto media through caching, indexing, redundancy, checksums, logs, compaction, recovery, and lifecycle policies.", "Durability boundary", "A durability boundary defines which acknowledged state survives specified failures across process, cache, controller, device, zone, and region scopes.", "Write and recovery path", "Buffering, logging, replication, ordering, checksums, flush, compaction, and replay determine persisted and recovered state.", "Acknowledged write survives every disaster", "A successful write must not be reported as universally durable without the exact failure scope and replication evidence."),
    ("distributed-cloud-data.relational-databases", "relational-databases", "Relational databases", "Relational databases represent data as typed relations and use keys, constraints, algebra, transactions, indexes, and declarative queries.", "Relational schema", "A schema declares relations, attributes, domains, keys, constraints, and references independently of one physical layout.", "Constraint-preserving update", "An update transforms relation state only if type, key, reference, check, transaction, and authorization constraints hold.", "Table equals spreadsheet", "A relation must not be reduced to visual rows without keys, types, constraints, null semantics, transactions, and set or bag behavior."),
    ("distributed-cloud-data.nosql", "nosql", "Non-relational databases", "Non-relational databases use key-value, document, wide-column, graph, time-series, search, or other models with system-specific consistency and query contracts.", "Access-pattern model", "Partition key, document boundary, graph relation, index, query, update, and growth patterns qualify the chosen data model.", "Partitioned operation", "Routing and replication transform logical operations across shards under consistency, availability, and rebalancing rules.", "NoSQL means no schema", "A non-relational store must not be described as schema-free when application and index contracts still constrain data."),
    ("distributed-cloud-data.query-processing", "query-processing", "Query processing and optimization", "Query engines parse, bind, rewrite, plan, optimize, execute, spill, parallelize, and monitor declarative operations.", "Logical query plan", "A logical plan represents relational or data operations independent of specific algorithms and placement.", "Cost-based planning", "Statistics, cardinality estimates, physical operators, indexes, memory, parallelism, and cost models select an executable plan.", "Optimizer chosen plan is globally best", "A selected plan must not be treated as optimal when statistics, cost models, parameter values, and runtime conditions are uncertain."),
    ("distributed-cloud-data.transactions", "transactions", "Transactions and consistency", "Transactions group operations under atomicity, consistency constraints, isolation, durability, conflict, and recovery semantics.", "Transaction history", "A transaction history records operation order, reads-from, commits, aborts, and concurrency relations.", "Concurrency control", "Locks, timestamps, validation, multiversion state, serialization, logging, and replication constrain transaction histories.", "ACID has one universal meaning", "An ACID label must not replace exact isolation, durability, failure, replication, and application-invariant contracts."),
    ("distributed-cloud-data.data-modeling", "data-modeling", "Data modeling", "Data modeling represents entities, events, values, relationships, identity, time, constraints, provenance, and access patterns for a domain.", "Data identity", "A data identity specifies what makes a record or event the same across updates, sources, versions, and representations.", "Schema evolution", "Compatibility rules, defaults, migrations, dual reads or writes, backfill, validation, and retirement transform a data model over time.", "Nullable field is harmless", "Adding optional data must not be assumed compatible when semantics, validation, indexing, authorization, and old consumers differ."),
    ("distributed-cloud-data.data-pipelines", "data-pipelines", "Data pipelines", "Data pipelines ingest, validate, transform, join, enrich, partition, publish, backfill, and observe data with lineage and replay.", "Data lineage", "Lineage links each output to source versions, code, parameters, schema, time, and execution identity.", "Idempotent transformation", "Stable input and operation identity allow replay without duplicating intended output effects.", "Pipeline green means data correct", "Task completion must not establish semantic correctness, completeness, freshness, lineage, and downstream compatibility."),
    ("distributed-cloud-data.stream-processing", "stream-processing", "Stream processing", "Stream processing computes over unbounded event sequences using event time, windows, watermarks, state, checkpoints, ordering, and delivery semantics.", "Event-time record", "A stream event has identity, event time, ingestion time, key, schema, payload, and provenance.", "Windowed state", "Keys, windows, watermarks, late-data policy, triggers, deduplication, and checkpoints transform events into bounded results.", "Exactly once means event occurred once", "Exactly-once processing must not be confused with one physical delivery or one external side effect without transactional sinks."),
    ("distributed-cloud-data.cloud-architecture", "cloud-architecture", "Cloud architecture", "Cloud architecture composes on-demand compute, storage, networking, identity, managed services, regions, automation, elasticity, metering, and shared responsibility.", "Cloud resource", "A cloud resource has identity, region, configuration, dependencies, policy, lifecycle, quota, cost, and provider responsibility.", "Declarative reconciliation", "Desired state, controllers, observed state, replacement, health, rollout, and eventual convergence automate resource lifecycle.", "Cloud service removes operations", "Managed infrastructure must not be treated as removing configuration, identity, data, cost, reliability, and provider-dependency responsibilities."),
    ("distributed-cloud-data.site-reliability", "site-reliability", "Site reliability engineering", "SRE applies software engineering to service reliability through objectives, error budgets, observability, incident response, capacity, automation, and learning.", "Service-level objective", "An SLO defines a measured reliability target for a service indicator over a window and eligible population.", "Error-budget control", "The difference between target and observed unreliability governs release pace, remediation, and risk decisions under policy.", "One hundred percent availability is free", "A perfect target must not be assumed feasible or desirable without cost, innovation, dependency, measurement, and user-value analysis."),
]


CROSS_RELATIONS = [
    ("cs-invariant-algorithm", "cs.algorithms.primitive", "cs.algorithms.mechanism", "supports", "An algorithm invariant supports correctness and termination reasoning."),
    ("cs-structure-algorithm", "cs.data-structures.mechanism", "cs.algorithms.mechanism", "qualifies", "Representation and operation costs qualify algorithm complexity."),
    ("cs-reduction-complexity", "cs.complexity.mechanism", "cs.computability.mechanism", "supports", "Reductions support transfers of complexity and undecidability."),
    ("cs-automata-compute", "cs.automata.mechanism", "cs.computability.primitive", "supports", "Automata recognition supports formal models of effective computation."),
    ("cs-concurrent-history", "cs.concurrency.primitive", "cs.distributed-theory.primitive", "analogous_to", "Concurrent and distributed histories share partial order while distributed failure adds independent-node uncertainty."),
    ("cs-architecture-concurrency", "cs.computer-architecture.mechanism", "cs.concurrency.mechanism", "qualifies", "Cache coherence and memory order qualify software synchronization observations."),
    ("cs-graphics-architecture", "cs.graphics.mechanism", "cs.computer-architecture.mechanism", "qualifies", "Rendering workloads qualify parallel architecture and memory design."),
    ("cs-compute-algorithm", "cs.computational-science.mechanism", "cs.algorithms.mechanism", "qualifies", "Verification and numerical error qualify algorithms used for scientific claims."),
    ("cs-quantum-complexity", "cs.quantum-computing.mechanism", "cs.complexity.primitive", "qualifies", "Quantum circuit compilation qualifies the computational resource model."),
    ("data-component-system", "data.distributed-systems.primitive", "data.distributed-systems.mechanism", "part_of", "Independent components compose an end-to-end distributed protocol."),
    ("data-consensus-system", "data.consensus.mechanism", "data.distributed-systems.mechanism", "supports", "Replicated consensus supports a fault-tolerant state-machine service."),
    ("data-consensus-storage", "data.consensus.primitive", "data.storage.mechanism", "qualifies", "Committed replicated-log order qualifies durable state application."),
    ("data-schema-relational", "data.relational-databases.primitive", "data.data-modeling.mechanism", "qualifies", "Relational constraints qualify schema evolution."),
    ("data-nosql-access", "data.nosql.primitive", "data.data-modeling.primitive", "qualifies", "Access patterns qualify non-relational data identity and partitioning."),
    ("data-plan-relational", "data.query-processing.mechanism", "data.relational-databases.primitive", "supports", "Query plans implement relational operations over physical storage."),
    ("data-transaction-storage", "data.transactions.mechanism", "data.storage.primitive", "qualifies", "Concurrency control and logging qualify storage durability and isolation."),
    ("data-model-pipeline", "data.data-modeling.mechanism", "data.data-pipelines.mechanism", "qualifies", "Schema evolution qualifies compatible pipeline backfill and publication."),
    ("data-pipeline-stream", "data.data-pipelines.primitive", "data.stream-processing.mechanism", "supports", "Lineage and idempotency support replayable stream processing."),
    ("data-stream-transaction", "data.stream-processing.mechanism", "data.transactions.mechanism", "qualifies", "Transactional sinks qualify exactly-once external effects."),
    ("data-cloud-system", "data.cloud-architecture.mechanism", "data.distributed-systems.primitive", "implements", "Declarative cloud reconciliation implements distributed resource management."),
    ("data-sre-cloud", "data.site-reliability.mechanism", "data.cloud-architecture.primitive", "qualifies", "Error budgets qualify cloud rollout and remediation decisions."),
    ("bridge-alg-query", "cs.algorithms.mechanism", "data.query-processing.mechanism", "supports", "Algorithm and data-structure analysis supports query operator and plan selection."),
    ("bridge-concurrent-transaction", "cs.concurrency.mechanism", "data.transactions.primitive", "qualifies", "Concurrent histories qualify database isolation and serializability."),
    ("bridge-distributed-consensus", "cs.distributed-theory.mechanism", "data.consensus.mechanism", "qualifies", "Failure and timing assumptions qualify consensus safety and liveness."),
    ("bridge-architecture-storage", "cs.computer-architecture.mechanism", "data.storage.mechanism", "qualifies", "Memory hierarchy, persistence, and ordering qualify storage write and recovery paths."),
    ("bridge-graphics-data", "cs.graphics.primitive", "data.data-modeling.primitive", "qualifies", "Scene identity and geometry qualify data models for graphics assets."),
]


WORKED_EXAMPLES = [
    ("cs", "loop-proof", "Loop invariant proof", "Initialization establishes a sorted prefix, each iteration extends it while preserving permutation, and termination makes the prefix the full sorted array.", "computer-science.algorithms"),
    ("cs", "race-history", "Concurrent lost update", "Two threads read the same counter and write the same incremented value; the history exposes a lost update despite individually atomic reads and writes.", "computer-science.concurrency"),
    ("cs", "cache-performance", "Architecture performance decomposition", "A benchmark separates instruction dependencies, branch misses, cache misses, memory bandwidth, and vector utilization instead of attributing time to language alone.", "computer-science.computer-architecture"),
    ("data", "raft-partition", "Raft quorum partition", "A five-node cluster with three mutually connected members can elect and commit while two isolated members cannot form a conflicting majority.", "distributed-cloud-data.consensus"),
    ("data", "timeout-idempotency", "Distributed timeout reconciliation", "A caller times out after sending a create request and queries by idempotency key before retrying, preserving one logical resource." , "distributed-cloud-data.distributed-systems"),
    ("data", "serializable", "Serializable write skew", "Two transactions read a shared invariant and write disjoint rows; predicate-conflict detection aborts one to preserve a serial order." , "distributed-cloud-data.transactions"),
    ("data", "query-cardinality", "Query cardinality correction", "A plan chooses a nested loop from an underestimated join size; runtime evidence refreshes statistics and selects a hash join for the same bounded query class." , "distributed-cloud-data.query-processing"),
    ("data", "late-event", "Late stream event", "A watermark closes a window, then an allowed late event triggers a correction with the same result identity while events beyond allowed lateness enter a side output." , "distributed-cloud-data.stream-processing"),
    ("data", "schema-migration", "Compatible schema migration", "Writers add a versioned field, readers accept old and new forms, a backfill is verified, use migrates, and only then is the old path retired." , "distributed-cloud-data.data-modeling"),
    ("data", "slo-budget", "SLO error-budget decision", "A service with a 99.9 percent monthly target consumes its error budget early, so risky rollout pauses and reliability remediation takes priority." , "distributed-cloud-data.site-reliability"),
]


GROUPS = [
    ("cs", "computer-science", CS, CS_SOURCES, "Computer science", "Computer science studies computation, representation, algorithms, complexity, machines, concurrency, architecture, graphics, scientific computing, and quantum models."),
    ("data", "distributed-cloud-data", DATA, DATA_SOURCES, "Distributed cloud and data systems", "Distributed data systems coordinate replicated state, storage, queries, transactions, schemas, pipelines, streams, cloud resources, and reliability across partial failures."),
]


def split_for(index: int) -> str:
    if index and index % 19 == 0:
        return "cross_domain_holdout"
    if index and index % 17 == 0:
        return "sealed_test"
    if index and index % 13 == 0:
        return "validation"
    return "train"


def base(identifier: str, domain: str, subject: str, sources: list[str], split: str, kind: str, epistemic: str = "established") -> dict[str, Any]:
    return {
        "schema_version": 1, "record_id": identifier, "world_id": WORLD,
        "domain_id": domain, "subject_id": subject, "lanes": LANES,
        "record_kind": kind, "epistemic_class": epistemic,
        "coverage_axes": ["definitions_scope", "primitives_invariants", "mechanisms_causal_laws"],
        "source_ids": sorted(set(sources)),
        "scope": "computer-science and distributed cloud-data foundation tranche",
        "limitations": [
            "Correctness and availability claims retain computation, failure, timing, consistency, workload, and implementation assumptions.",
            "Vendor products and living platforms require version-specific worlds beyond these transferable mechanisms.",
        ],
        "as_of": "2026-09-03", "version_boundary": "computer-data-systems-v0",
        "split_group": identifier, "split": split, "tags": ["foundation", domain],
    }


def context(prefix: str) -> tuple[str, list[str], str]:
    for item_prefix, domain, profiles, sources, _label, _statement in GROUPS:
        if item_prefix == prefix:
            return domain, sources, profiles[0][0]
    raise ValueError(prefix)


def build() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    index = 0
    for prefix, domain, profiles, sources, domain_label, domain_statement in GROUPS:
        records.append({**base(f"{prefix}.root", domain, profiles[0][0], sources, "train", "concept"), "label": domain_label, "statement": domain_statement, "aliases": [domain_label.lower()]})
        for subject, slug, label, definition, primitive_label, primitive_statement, mechanism_label, mechanism_statement, control_label, control_statement in profiles:
            for offset, (suffix, node_label, statement) in enumerate([("root", label, definition), ("primitive", primitive_label, primitive_statement), ("mechanism", mechanism_label, mechanism_statement)]):
                node_id = f"{prefix}.{slug}.{suffix}"
                records.append({**base(node_id, domain, subject, sources, "train" if suffix == "root" else split_for(index + offset), "concept"), "label": node_label, "statement": statement, "aliases": [node_label.lower()]})
                target = f"{prefix}.root" if suffix == "root" else f"{prefix}.{slug}.root"
                relation_id = f"cds.membership.{prefix}.{slug}.{suffix}"
                records.append({
                    **base(relation_id, domain, subject, sources, split_for(index + offset + 4), "relation"),
                    "label": f"{node_label} system membership", "statement": f"{node_label} is a distinct component of {label} with explicit computation and failure conditions.", "aliases": [],
                    "relation": {"source_node": node_id, "target_node": target, "kind": "part_of", "polarity": 1, "direction": "forward", "conditions": ["the declared computation and system model applies"], "exceptions": []},
                    "coverage_axes": ["primitives_invariants", "within_domain_composition"],
                })
            control_id = f"cds.control.{prefix}.{slug}"
            records.append({
                **base(control_id, domain, subject, [], ["train", "validation", "sealed_test", "cross_domain_holdout"][index % 4], "synthetic_control", "synthetic_control"),
                "label": control_label, "statement": control_statement, "aliases": [control_label.lower()], "synthetic": True,
                "coverage_axes": ["exceptions_boundaries", "errors_adversarial_misuse", "unknown_abstention"], "tags": ["negative-control", domain],
            })
            index += 1

    all_sources = sorted(set(CS_SOURCES + DATA_SOURCES))
    splitter = RelationSplitter([kind for _id, _source, _target, kind, _statement in CROSS_RELATIONS])
    for identifier, source, target, kind, statement in CROSS_RELATIONS:
        prefix = source.split(".", 1)[0]
        domain, sources, subject = context(prefix)
        cross = prefix != target.split(".", 1)[0] or identifier.startswith("bridge-")
        records.append({
            **base(f"cds.relation.{identifier}", domain, subject, all_sources if cross else sources, splitter.split(kind, cross_requested=cross), "relation"),
            "label": identifier.replace("-", " "), "statement": statement, "aliases": [],
            "relation": {"source_node": source, "target_node": target, "kind": kind, "polarity": -1 if kind in {"inhibits", "prevents", "contradicts", "undercuts"} else 1, "direction": "forward", "conditions": ["the stated computation, consistency, failure, and timing assumptions hold"], "exceptions": []},
            "coverage_axes": ["mechanisms_causal_laws", "within_domain_composition", "cross_domain_composition"],
        })

    for example_index, (prefix, identifier, label, statement, subject) in enumerate(WORKED_EXAMPLES):
        domain, sources, _root_subject = context(prefix)
        split = ["train", "validation", "sealed_test", "cross_domain_holdout"][example_index % 4]
        node_id = f"cds.example.{prefix}.{identifier}"
        records.append({**base(node_id, domain, subject, sources, split, "worked_example"), "label": label, "statement": statement, "aliases": [], "coverage_axes": ["applications_toolchains", "deductions_predictions_execution", "within_domain_composition"], "tags": ["worked-example", domain]})
        records.append({
            **base(f"cds.example-membership.{prefix}.{identifier}", domain, subject, sources, split, "relation"),
            "label": f"{label} membership", "statement": f"The {label.lower()} operationalizes one bounded computer or data-system mechanism.", "aliases": [],
            "relation": {"source_node": node_id, "target_node": f"{prefix}.root", "kind": "part_of", "polarity": 1, "direction": "forward", "conditions": ["the example remains bounded"], "exceptions": []},
            "coverage_axes": ["applications_toolchains", "within_domain_composition"],
        })
    return sorted(records, key=lambda row: row["record_id"])


def main() -> int:
    records = build(); OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in records), encoding="utf-8")
    counts: dict[str, int] = {}; kinds: dict[str, int] = {}
    for row in records:
        counts[row["split"]] = counts.get(row["split"], 0) + 1; kinds[row["record_kind"]] = kinds.get(row["record_kind"], 0) + 1
    print(f"wrote {OUTPUT} with {len(records)} records: splits={dict(sorted(counts.items()))} kinds={dict(sorted(kinds.items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
