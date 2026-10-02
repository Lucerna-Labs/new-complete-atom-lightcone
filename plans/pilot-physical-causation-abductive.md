# Pilot: physical-causation-v0 (general world) + reasoning-abductive-v0

Opened 2026-10-02 on branch `pilot-physical-causation` (from
`catalog-v3-lexical-ambiguity`). This is Phase A of `plans/NEW-WORLD-TRAINING-PLAN.md`.

**Jesse's choices (2026-10-02):**
- The general world is everyday physical causation.
- The first standalone reasoning world is abductive.
- "This time we should try to get as much coverage as possible."

## Sources (verified by fetching each page on 2026-10-02; registered `citation_only`)

- `nasa-glenn-beginners-guide`: forces, motion, drag, sound speed.
- `usgs-water-science-school`: water cycle, properties of water.
- `noaa-jetstream`: heat transfer, pressure, wind, lightning, thunder.
- `eia-energy-explained`: forms of energy, conversion, electricity, magnets.
- `nasa-ems-tour`: wave behaviours, visible light, infrared.
- Already registered: `nist-codata-2022` (constants), `sep-abduction`,
  `sep-scientific-discovery`.

Statements are original structured summaries. No source text is copied.

## Design rules (apply to every record)

- **Causal-first.** Non-membership relations are mostly `causes`, `enables`,
  `prevents`, `inhibits`, `prerequisite`, `transforms_to` and `predicts`.
- **Real polarity:** reductions and blocks are `inhibits` or `prevents`, with
  polarity −1.
- **One specific condition per relation**, plus exceptions where they exist. No
  boilerplate.
- **Myths are counterexample records** linked to what they misdescribe. Regime limits
  are boundary records.
- **Unambiguous labels:** mostly two or more words; no generated `label.lower()`
  aliases (v3 lesson). Aliases are added only when they are real synonyms.
- **Held-out statements name their target and contain relation cue words**,
  because the current gates are text-retrieval based.

## Coverage targets (Gate A, written before authoring)

**physical-causation-v0** (domain `physics`, no new domain, so ledger counts are
unchanged):
- Subfields: classical-mechanics, thermodynamics, fluid-dynamics, electromagnetism,
  optics, acoustics, condensed-matter, statistical-mechanics. Each has ≥ 10 concepts
  and ≥ 15 non-membership relations.
- Totals: ≥ 200 concepts; ≥ 300 non-membership relations, of which ≥ 70% use the
  causal kinds above; ≥ 25 negative-polarity relations.
- ≥ 20 counterexample (myth) records, ≥ 12 boundary records, ≥ 12 worked examples
  (including the dropped-ball question).
- No condition string reused by more than 3 relations.
- At least 14 of the 15 coverage axes credited (`adapter_accessibility` is exempt).
- ≤ 15% single-word labels.

**reasoning-abductive-v0** (domain `philosophy`, subject `philosophy.science`; lane
`reasoning.abductive`):
- ≥ 40 concepts.
- ≥ 60 non-membership relations encoding the method as directed structure:
  observation → candidate causes (past cone) → fit → rivals → discriminating evidence
  → elimination → best explanation (provisional) → revision on new evidence.
- ≥ 6 counterexamples (e.g. affirming the consequent, premature closure), and ≥ 8
  worked examples that bridge to physical causation (wet ground: rain or sprinkler; a
  ball on the floor: dropped or rolled).

**Both worlds:**
- The validators pass: `validate_sources`, `validate_curricula`, `validate_registry`,
  `sync_authored_coverage`.
- Both compile with `trainer/compile_curriculum.py`.
- The CPU smoke run trains both, with every non-TPU gate passing (`.venv/bin/python`).
- **Admission audit:** in a-rag-atom's `admit-batch`, the dropped-ball question seeds
  physical-causation concepts (gravity, falling, release). Every new label is checked
  for seeds in unrelated worlds, and collisions are reported.

Gate A results will be appended here. If a target isn't met, it's recorded as unmet,
and targets are never lowered after the fact.

## Gate A results (2026-10-02) — all targets met

**physical-causation-v0** (`tools/build_physical_causation_curriculum.py` with
`tools/physical_causation/*.py`, commit `102cf43`):

| Target | Required | Actual |
|---|---|---|
| Concepts | ≥ 200 | 221 |
| Non-membership relations | ≥ 300 | 314 |
| Causal share | ≥ 70% | 79% |
| Negative polarity | ≥ 25 | 56 |
| Counterexamples / boundaries / worked examples | ≥ 20 / 12 / 12 | 23 / 14 / 16 |
| Most-reused condition | ≤ 3 | 2 |
| Per subfield | ≥ 10 concepts and ≥ 15 relations | all 8 subfields (smallest: statistical, 15 / 17) |
| Coverage axes | ≥ 14 / 15 | 14 (all but adapter_accessibility) |
| Single-word labels | ≤ 15% | 2.7% |

Compiled to 280 nodes and 550 edges.

**reasoning-abductive-v0** (commit `a775b6f`):

| Target | Required | Actual |
|---|---|---|
| Concepts | ≥ 40 | 41 |
| Method relations | ≥ 60 | 60 |
| Fallacies | ≥ 6 | 8 |
| Physics-bridging worked examples | ≥ 8 | 8 |

Compiled to 65 nodes and 137 edges.

**Both worlds:**
- `validate_sources`, `validate_curricula` and `validate_registry` pass;
  `sync_authored_coverage` reports no uncredited axes.
- Both are appended last in `world_catalog.PILOT_WORLD_CONFIGS`, so all 178 existing
  generated configs are byte-identical.
- **CPU smoke:** `JAX_PLATFORMS=cpu .venv/bin/python tools/run_local_smoke_matrix.py
  --world physical-causation-v0 --world reasoning-abductive-v0 --reuse-compiled`:
  both `non_tpu_gates_passed`, the only open gate being `tpu_backend`. Run ids:
  `physical-causation-v0-20261002T184027Z`, `reasoning-abductive-v0-20261002T184032Z`.

**Still open:**
- The admission audit, done in Phase B with locally finalized diagnostic packs.
- A coverage-ledger reopen for the physics and philosophy items credited by the new
  records, needed before sealing (`tools/reopen_coverage.py`).
- The hardcoded world count in `build_catalog_evidence.py`.

## Admission audit (2026-10-02, Phase B setup)

**Scratch catalog:** 178 pinned v2 worlds plus both pilot worlds as **diagnostic
packs**. These were built by a-rag-atom `tools/diagnostic_pack.py` from the CPU smoke
output. Their receipts record `diagnostic_cpu_only` and the release validator's
errors ("training source was dirty"; "accelerator is not Kaggle TPU"). Admission ran
through `admit-batch --unpinned`, which keeps the production loader's hash checks but
not its 178-world pin.

- **Dropped-ball question:** "let go of" seeds `pc.release` (alias), the right entry.
  **Partly unmet:** gravity and falling are not seeded, because the question says
  "fall" while the lexicon holds "falling under gravity" / "free fall". Exact-term
  admission misses inflections (Phase D).
- **Hub effect:** the 2-hop cone from `pc.release` admitted 237 of 280 nodes, because
  every concept's `part_of` membership edge to `pc.root` puts the whole world within
  2 hops. This affects every catalog world with a root. Candidate fix for Phase D:
  exclude membership edges from traversal (`allowed_relations`). The 1-hop cone and
  AtomDB delivery are unaffected.
- **Collisions:** 16 of 330 physical terms and 3 of 69 abductive terms also occur in
  other worlds. All 19 are the same real concepts ("atmospheric pressure",
  "magnetic field", "base rate"), not ambiguous words.
