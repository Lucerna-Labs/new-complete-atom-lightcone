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
