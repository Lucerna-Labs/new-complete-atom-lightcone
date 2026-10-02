# Catalog revision v3: lexical ambiguity in seed terms

Opened 2026-10-01 at the owner's request, from sealed v2 (`ae52d30`). Work stops
before the Kaggle TPU run. v2 remains the sealed, deployed revision until a v3
seal exists.

## Evidence that opened the revision

The a-rag-atom model adapter admitted the question "Why does a ball fall
toward the ground when you let go of it?" through the lexicon term `go` ->
`lang.go.root`. A catalog survey found more everyday words that are seed terms
only because of label/alias generation:

- `tools/build_languages_compilers_curriculum.py` gives every concept, language
  and control record `aliases: [label.lower()]`. The lexicon already normalizes
  labels to lowercase, so the alias adds no term. Its only effect is erasing the
  source's case evidence for acronym labels (`C`, `R`, `PHP`, `C++`). A runtime
  that matches acronym-only forms exactly (as a-rag-atom now does) cannot
  distinguish `C` from the word "c" while that alias exists.
- `lang.go.root` (label `Go`) and `math.set` (label `Set`) are ordinary words.
  Their bare term comes from the label itself, so only a label change removes
  it.

Other builders use the same generated-alias pattern. No collision is known
there; they are recorded as a remaining item, not changed in v3.

## Frozen changes

1. Languages builder: stop generating `label.lower()` aliases for concept,
   language and control records. Authored aliases elsewhere are untouched.
2. Languages builder: the Go root node only gets label
   `Go programming language` and aliases `golang`, `go language`. Derived
   labels ("Go type model", ...) and statements are unchanged.
3. Math builder: `math.set` label `Set` -> `Set (mathematics)`. Its generated
   alias follows the label, as for every math entry.

## Gates and predictions

- **L01 record diff.** Comparing every curriculum record (by `record_id`)
  between `ae52d30` and the regenerated curricula, the only changes are
  (a) `aliases` that equaled `label.lower()` in languages-compilers records
  becoming empty, (b) the Go root label/aliases, and (c) the `math.set`
  label/alias. No record is added or removed. Prediction: MEASURED.
- **L02 compiled lexicons.** In compiled `languages-compilers-v0`: no bare
  `go` term; `golang`, `go language` and `go programming language` map to
  `lang.go.root`. Terms `c`, `r`, `php` and `c++` still map to their roots, and
  every label/alias form of those roots that normalizes to the term is an
  all-caps acronym. In `math-probability-information-v0`: no bare `set` term;
  `set mathematics` maps to `math.set`. Prediction: MEASURED.
- **L03 reopen.** A deterministic, repository-owned tool reopens every ledger
  item credited by a changed record (its domain, subfield and lanes) to
  `authored`, reopens the axes those records declare, and records the reason.
  `validate_registry.py` passes and `validate_registry.py --require-sealed`
  fails, because the revision is honestly open. Prediction: MEASURED.
- **L04 validators and tests.** The source, curricula, registry, adapter,
  taxonomy-shard, revocation, authored-coverage and training-protocol
  validators pass, together with repository Python and Rust tests.
  Prediction: MEASURED.
- **L05 CPU diagnostic.** `run_local_smoke_matrix.py --require-non-tpu-pass`
  passes for both changed worlds. This is diagnostic only, never accelerator
  acceptance. Prediction: MEASURED; the main risk is a retrieval gate that
  depends on the old Go or Set label text.
- **L06 package preflight.**
  `kaggle/package_catalog_job.py --kernel-version 5 --validate-only` passes
  without creating upload files. Prediction: MEASURED.

## Stop condition

No upload, no Kaggle run, no ledger promotion beyond `authored`, no seal, no
push. Remaining steps: a real eight-device TPU run, validation, authorization
and completion receipts, then importing the v3 packs into a-rag-atom.
