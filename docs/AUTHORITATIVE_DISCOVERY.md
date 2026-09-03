# Authoritative taxonomy discovery

An exhaustive program must expose the frontier it has not yet trained. The
discovery ledger imports authoritative classification entries as work items;
it does not mistake a taxonomy label for a fact, mechanism, causal relation, or
trained world.

## Current imports

- **MSC2020**: 6,603 Mathematics Subject Classification entries. MSC2020 is
  jointly maintained by Mathematical Reviews and zbMATH and published under
  CC BY-NC-SA 4.0.
- **MeSH 2026**: 31,110 Medical Subject Headings descriptors. MeSH is produced
  by the U.S. National Library of Medicine and reused under the NLM MeSH Terms
  and Conditions. The project acknowledges NLM as the source and does not
  imply NLM endorsement.

The downloaded source files are not committed. Their exact SHA-256 values,
versions, rights, and acknowledgements are pinned in
`sources/taxonomy-inputs.json`; the normalized discovery ledger is hash-bound
by `ontology/discovery-manifest.json`.

## State semantics

Every imported entry begins as `unmapped`. Mapping requires a deliberate link
to one or more coverage-ledger items. Exclusion requires a reason. A taxonomy
term remains a discovery item until sourced curriculum supplies definitions,
scope, mechanisms, boundaries, controls, compositions, and sealed tests.

The project cannot be called exhaustive while any authoritative discovery is
unmapped. `tools/validate_registry.py --require-sealed` enforces that rule.

## Work shards

`tools/plan_taxonomy_training_shards.py` deterministically assigns every
discovery exactly once to a bounded curriculum-work shard. Current planning
uses 256 entries per shard and produces:

- 29 MSC2020 shards;
- 128 MeSH 2026 shards;
- 157 shards total covering all 37,713 entries with zero duplicates.

These are work manifests, not training claims. Every shard still requires
sourcing, authoring, isolated splits, Kaggle TPU training, sealed evaluation,
and adapter-independent artifact verification.

