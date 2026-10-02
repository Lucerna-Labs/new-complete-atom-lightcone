# Pilot: frontend-ux-causation-v0 (front-end, UX and UI)

Opened 2026-10-02 at Jesse's request: "make a front end set, for UX and UI; all models
struggle with that regardless of size." This branch (`pilot-frontend-ux`) lives in its
own git worktree, so the coder's checkout is untouched.

## Scope

A causal world of front-end and UX mechanisms, across three existing domains (no
ledger-count change):
- `frontend-web-development`: CSS layout, performance, accessibility, components and
  state;
- `human-computer-interaction`: interaction design, usability;
- `typography-color-visual-design`: visual hierarchy, readability, colour.

Content is cause and effect, never style opinion. For example: a stacking context
confines z-index; images without dimensions cause layout shift; placeholder-only
labels disappear while typing.

## Sources (verified by fetching on 2026-10-02; registered `citation_only`)

- New: `mdn-web-docs` (stacking context page), `web-dev-vitals` (LCP 2.5 s, INP
  200 ms, CLS 0.1), `nngroup-heuristics` (ten heuristics), `nngroup-response-times`
  (0.1/1/10 s), `nngroup-fitts`, `lawsofux-hicks`.
- Already registered: `w3c-wcag-22`, `w3c-wai-aria-12`, `w3c-css-color-4`.

## Coverage targets (written before the builder ran)

- ≥ 200 concepts across 7 areas; each area ≥ 18 concepts and ≥ 15 non-membership
  relations.
- ≥ 230 non-membership relations, ≥ 65% of them causal kinds (`causes`, `enables`,
  `prevents`, `inhibits`, `prerequisite`, `transforms_to`, `predicts`).
- ≥ 30 negative-polarity relations, ≥ 18 myths as counterexamples, ≥ 10 boundaries,
  ≥ 12 worked examples (real front-end bugs and design failures).
- No condition string reused by more than 3 relations; ≥ 14/15 coverage axes;
  ≤ 15% single-word labels.
- `validate_sources`, `validate_curricula` and `validate_registry` pass; the world
  compiles; the CPU smoke passes all non-TPU gates.

Unmet targets will be recorded as unmet.
