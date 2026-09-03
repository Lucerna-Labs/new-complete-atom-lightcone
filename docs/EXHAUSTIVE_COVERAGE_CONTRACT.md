# Exhaustive coverage contract

## Meaning of exhaustive

Exhaustive means systematic closure over the best available, explicitly
versioned ontology of Lightcone-suitable knowledge and reasoning. It does not
mean a handful of representative prompts, one broad claim per discipline, or a
large unstructured text dump.

No finite artifact can prove coverage of every possible future fact or prompt.
The enforceable requirement is stronger than sampling: enumerate all known
required fields and relationships, expose every known gap, close each ledger
entry with source and test evidence, and reopen coverage as knowledge,
software, standards, and scientific consensus change.

## Required axes for every coverage item

Unless an axis is formally inapplicable with a reason, every item must cover:

1. definitions and scope;
2. primitives and invariants;
3. mechanisms and causal laws;
4. representations and transformations;
5. deductions, predictions, and executable consequences;
6. assumptions and prerequisites;
7. exceptions, counterexamples, and boundary conditions;
8. uncertainty, competing hypotheses, and evidence quality;
9. common errors, adversarial framings, and misuse;
10. practical applications and toolchains;
11. historical or version-dependent change where relevant;
12. within-domain composition;
13. cross-domain composition;
14. unknown/out-of-scope abstention controls;
15. accessibility across supported model adapters.

## Status state machine

```text
discovered -> scoped -> sourced -> authored -> compiled -> trained
           -> locally_validated -> accelerator_validated -> sealed
```

`blocked` and `retired` are explicit side states with reasons. A parent cannot
be sealed while any required descendant or required coverage axis is below
`sealed`.

## Closure gate

A domain is exhaustive only when all of the following are true:

- its ontology has been reviewed for missing subfields and adjacent bridges;
- every required descendant and coverage axis is sealed;
- source, rights, and version checks pass;
- positive, negative, adversarial, counterfactual, and unknown controls pass;
- held-out mechanisms and held-out cross-domain compositions pass;
- geometry and exact graph invariants pass;
- artifacts reproduce from pinned inputs and seeds;
- at least the declared adapter compatibility matrix passes;
- the gap scanner returns no known open item for that domain;
- limitations and unresolved scientific disputes remain visible.

The project as a whole cannot be called exhaustive while any mandatory domain
is unsealed or the discovery ledger contains an unresolved candidate.

