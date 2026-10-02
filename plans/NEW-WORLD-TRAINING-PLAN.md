# Plan: train a new Lightcone world with real causal shape

Written 2026-10-02 at Jesse's request. It draws on the recovered prototype, the
E16R–E18T measurements in a-rag-atom
(`experiments/thermodynamic-context/docs/LIGHTCONE-RECOVERY-AND-FINDINGS-2026-10-02.md`),
and read-only surveys of this repo's pipeline and of AtomDB. Nothing here has been run
yet. Every phase is precommitted under the Atom rules before execution: 1–3
mechanically justified candidate orders, matched controls, and every candidate
reported.

## 0. Why this is needed (measured, not assumed)

- **The mechanism works where worlds hold causal shape.** In E16R, questions from
  catalog causal chains went from bare 73% to cone 96%; with the arrows reversed, 47%.
  Under misleading pressure, cone + reasoning + engine loop reached 82% (bare 8%).
- **The catalog mostly holds classification shape.** Of 138,956 edges, 100 are
  `causes`, 3 `predicts`, 0 `counterexample`, and 67 have negative polarity. The 155
  taxonomy shards contain only `part_of`, `qualifies` and `supports`. Conditions are
  one boilerplate sentence. On everyday questions the cone delivered "Blood qualifies
  Plasma"-style lines (E16N).
- **Training doesn't learn causal geometry.** Node coordinates are a function of
  hashed label and statement text; there is no free per-node position. Held-out gates
  are scored by TF-IDF text retrieval. Only `direction_accuracy` comes from geometry.
- **The runtime ignores what training produces.** Admission is exact lexicon seeds plus
  a breadth-first walk. Coordinates, polarity and conditions are loaded but unused.

So "superior training" means three things: (A) worlds authored with real causal
structure, (B) a training objective whose geometry *is* a causal cone, and (C) a runtime
that admits by that geometry.

## 1. Decisions for Jesse before work starts

1. **Pilot domain.** Recommended: an *everyday physical causation* world (forces,
   gravity, heat, phase change, fluids, electricity, motion). The ball question
   ("Why does a ball fall when you let go of it?") started this work and seeded
   nothing relevant. These causes are well documented, directional, and easy to test
   with reversed-question controls. The alternative is a domain Jesse uses daily
   (software systems, Rust).
2. **Sources.** Every non-synthetic record needs a `source_id` in
   `sources/source-registry.json` that passes `docs/SOURCE_AND_RIGHTS_POLICY.md`
   (OpenStax is excluded). The pilot's sources must be chosen and registered first.
3. **New world or new domain.** A new world inside an existing domain avoids changing
   the coverage ledger's item count (640). A new domain or subfield regenerates the
   ledger (`tools/init_coverage_ledger.py`) and the hardcoded counts in sealing.
4. **Kaggle.** `~/.kaggle/access_token` exists but hasn't been checked. Uploading a
   dataset and running a kernel uses Jesse's account and quota, so each run needs his
   go-ahead.

## 2. Phase A — author the world (local, no training)

**Authoring rules (new; they apply to this world):**
- **Causal-first composition.** Most relations use `causes`, `enables`, `prevents`,
  `inhibits`, `prerequisite`, `transforms_to` or `predicts`. Use `part_of` only for the
  required membership edges to `<world>.root`, and `qualifies` only where it carries
  meaning.
- **Real polarity.** Negative effects use `inhibits` or `prevents` with polarity −1;
  don't encode them as positive edges with negative wording.
- **Real conditions and exceptions per edge** (for example "in a gravitational field",
  "unless air resistance dominates"). No generic sentence.
- **Counterexamples and boundaries.** Add `counterexample` records for common
  misconceptions (heavier objects don't fall faster in a vacuum) and `boundary`
  records where a cause stops holding.
- **Chains, not stars.** Edges should compose into 2–5-step chains with branches, so
  that direction and reachability carry information.
- **Unambiguous labels.** No bare common words or acronym collisions ("Go", "Set",
  "lead"). Check every label and alias against the a-rag-atom admission (`admit-batch`)
  for unintended seeds in other worlds.
- **Held-out text discipline:** the current gates are text-retrieval based, so
  held-out edge statements must name their target node and contain relation cue words
  ("causes", "prevents"). The v2 coverage-closure failure
  (`receipts/failures/catalog-v2-kaggle-v3-coverage-closure-gates.json`) is the
  precedent.

**Mechanics** (all existing tools):
1. `tools/build_<world>_curriculum.py` in the pattern of
   `build_ai_development_curriculum.py`: `CONCEPTS`, `RELATIONS`, `CONTROLS`,
   `WORKED_EXAMPLES` tuples, `RelationSplitter` for splits, membership edges, and a
   `.root` concept so negative pairs exist (the trainer refuses without them).
2. Register the world in `tools/world_catalog.py` (`FOUNDATION_WORLD_CONFIGS`) and
   generate its config with `tools/build_world_training_configs.py`.
3. Validate: `tools/validate_curricula.py`, `validate_sources`, `validate_registry`,
   `sync_authored_coverage`, then `trainer/compile_curriculum.py --world-id <id>`.

**Gate A** (precommitted numbers):
- Validators pass.
- The causal-kind share of non-membership edges meets a stated target (proposed ≥ 60%).
- Negative-polarity and counterexample counts meet stated minimums.
- No label seeds an unrelated world in a-rag-atom admission.

## 3. Phase B — test the world's value *before* any TPU run

The runtime cone uses only nodes, edges and lexicon. So a compiled (untrained) world
can be tested in a-rag-atom right away. This is the cheapest way to learn whether the
authoring works.

1. **Candidate admission orders** (Rule 2), on the new world plus catalog v2:
   (i) the deployed 2-hop BFS; (ii) 1-hop; (iii) BFS restricted to causal kinds,
   following direction and polarity.
2. **Question sets, frozen before running:**
   - E16R-style chains from the new world (forward, reversed, unrelated).
   - E17R-style misleading premises.
   - **Natural questions about the domain that the bare model gets wrong**, written
     independently of the world. Collect failures first, then freeze.
3. **Arms:** bare, cone, out-of-cone, reversed cone, and engine loop with reasoning
   (the best order from E18T).
4. **Baseline:** standard retrieval of the same world's text (AtomDB `memory_search`
   over the node and edge statements, without cone gating). This answers "isn't this
   just graph retrieval?" with numbers.

**Gate B:** on the natural failing questions, the cone and the loop beat bare, beat the
retrieval baseline, and the reversed cone does worse. If Gate B fails, fix the
authoring before spending TPU time.

## 4. Phase C — training that learns causal geometry

The current protocol (v3) stays as the **control**, so the world can still be sealed
the existing way. Candidate objectives, precommitted and compared under the same
splits:

- **T0, protocol v3 unchanged** (control): 48-D, text-derived coordinates, TF-IDF gates.
- **T1, free node embeddings:** each node gets its own trainable position. Text
  features act only as initialization and a weak regularizer. The objective keeps the
  current TransE and classification terms. This removes the text-bound limitation.
- **T2, causal-cone embedding** (the literal Lightcone): each node gets a time-like
  coordinate `t` and spatial coordinates `x`. A positive causal edge u→v must place v
  inside u's future cone: `t_v − t_u ≥ ‖x_v − x_u‖ + margin`. Reversed pairs must fall
  outside, and unrelated pairs should be space-like. Negative polarity gets its own
  channel: a signed component or a separate inhibitory cone. Known prior art exists
  for order embeddings and Minkowski/causal-set embeddings. Read it before
  implementing, and cite it in the protocol.

**New geometric gates**, scored on held-out edges by geometry only, never by text:
- direction accuracy;
- reversed-edge rejection;
- containment of held-out multi-step chains;
- unrelated pairs space-like;
- beating random-placement and axis-shuffle placebos;
- beating a text-only baseline.

Existing gates stay as sanity checks.

**Mechanics:** the trainer changes live in `trainer/` (new objective module, config
keys and a new protocol id); `semantic_geometry.validate_protocol_v3_config` pins
current constants. Run the CPU smoke first:

```bash
JAX_PLATFORMS=cpu .venv/bin/python tools/run_local_smoke_matrix.py --world <id> --reuse-compiled --require-non-tpu-pass --output-root <scratch>
```

Use `.venv/bin/python`. The system Python has no JAX.

## 5. Phase D — runtime admission by geometry (a-rag-atom and lightcone-core)

- Add coordinate admission as a **candidate order**, compared with BFS: the cone is the
  set of nodes inside the future cone (T2) of the seeds, with no hop limit, plus the
  past cone for "why" questions. This is the "beyond hop limits" property Jesse
  described.
- Make polarity and conditions visible in the rendered cone ("A inhibits B, unless C").
  Keep admission passive, with no scoring.
- Bounded delivery: deliver large cones through **thermodynamic soft context**
  (ScratchPad fields via `platform/src/soft_context.rs`), not the 32K hard window,
  where the 2-hop cone overflowed in E16N. Compare hard-window delivery, soft
  delivery and hybrid.
- Gate D repeats Gate B's sets plus the misleading set, in the full order: cone +
  reasoning + engine loop.

## 6. Phase E — AtomDB attachment (harness-first, as Jesse always built it)

**Evidence (E19, 2026-10-02, a-rag-atom `docs/ATOMDB-CONE-E19.md`):** all 178 v2 worlds
were stored in a scratch AtomDB store (5 s, 153 MB) and delivered by AtomDB's
`activate` inside the cone.
- E16R: 43/45, the same as cone1/cone2, at a median of 115 prompt tokens (cone1 254,
  cone2 5,758).
- E17R pressure: 32/60, better than cone1 (29) and cone2 (26).
- With reasoning: 45/60, equal to cone1.
- With reversed packets the scores collapse (direction survives).
- **Required:** the cone must gate AtomDB's cues as well as its arcs. AtomDB as is
  delivered nothing on these questions. Arcs must follow edge direction.
- Prototype: `tools/atomdb-cone` + `tools/atomdb_cone.py` in a-rag-atom.

**This makes AtomDB the recommended delivery path for the cone.**

Use the AtomDb-MCP core (the newest and most correct line) as the substrate.

1. **Fix first:** in `src/store.rs` `commit_cell`, update the `incoming` index (it
   currently updates only `outgoing`; the bug is visible to long-lived writers).
2. **Store the world natively:**
   - nodes become name atoms plus content atoms;
   - edges become traversal bonds `(S, lightcone/rel/v1/<kind>/<polarity>, T)` plus an
     edge atom carrying kind, polarity, conditions and sources (bonds can't carry
     metadata);
   - each world release is one cell, with a root per world for versioning.
3. **Port `atom-projection-field`** from the gpt-6 fork onto the MCP core:
   - drop its `cognitive-engine` path dependency;
   - give each projection its own `located_at/<projection_id>` relation;
   - quantize float coordinates to fixed-point i64;
   - keep unpositioned helper nodes (terms, passages) instead of dropping them.
4. **Executable direction and polarity in retrieval:** today every bond conducts both
   ways and negative edges conduct like positive ones. Add direction-aware arcs and an
   inhibitory signal as a candidate order. Keep the current behaviour as the control.
5. **Token efficiency (measured gate).** AtomDB returns byte-budgeted context packets:
   only passages where several query cues converge, and nothing for unknown queries.
   In E16R, the raw 2-hop cone cost about 5,800 prompt tokens (it overflowed 32K once)
   against about 250 for 1-hop at equal accuracy. Compare tokens used and accuracy for:
   (i) the cone rendered into the prompt; (ii) cone-gated AtomDB packets; (iii) the cone
   held in thermodynamic soft context. The candidate should match (i)'s accuracy with
   far fewer tokens.
6. **Harness test without the LLM first:** cone-gated recall over the stored world
   against ungated recall and a placebo, as in D66 but with trained positions.
   Then add the LLM.

## 7. Phase F — Kaggle TPU training and sealing

- **Iterate per world:** a single-world kernel in the pattern of
  `kaggle/package_expansion_job.py` (v2's full catalog run took about 2 h on 8 TPU
  devices). Use the catalog-level run (`package_catalog_job.py`) only for the release.
- A real package requires a clean Git tree. Upload and launch are done by hand with
  the Kaggle CLI (`~/.local/bin/kaggle`), with Jesse's confirmation each time.
- **Sealing changes** (`tools/build_catalog_evidence.py`): the world count (178) and
  ledger counts (640 items, 9,600 axes) are hardcoded, and authorization requires
  *uniform* ledger statuses, so items reopened by v3 must be brought level first.
  Change these in a separate, reviewed commit.
- Fold in catalog v3 (Go/Set relabels; L05 passed under `.venv`) so a single TPU
  release carries both.

## 8. Order of work and checkpoints

1. Decisions (section 1) → Phase A authoring → **Gate A**.
2. Phase B testing in a-rag-atom → **Gate B**. Stop and revise authoring if it fails.
3. Phase C training candidates on CPU smoke → TPU single-world run → geometric gates.
4. Phase D geometric admission + soft-context delivery → **Gate D**.
5. Phase E AtomDB attachment, harness-first → then with the LLM.
6. Phase F release, seal, import into a-rag-atom (new catalog pin).

After each step, record the results in the step's doc and commit. Update
`LIGHTCONE-RECOVERY-AND-FINDINGS` with lessons, and run the verified backup
(`save_backup.py`, both HDDs) at each phase boundary.

## 9. Risks recorded up front

- Authored causal edges can encode the author's own errors. Every edge needs a source,
  and counterexamples guard against myths.
- Training scored by text can hide bad geometry, which is why Phase C adds geometric
  gates.
- Lexical admission noise persists until Phase D. New-world labels must be audited.
- One model (Bonsai 27B) has been tested so far. Add a second model before claiming
  generality.
