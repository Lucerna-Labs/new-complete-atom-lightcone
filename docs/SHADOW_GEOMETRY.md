# Four-dimensional shadow geometry

## Boundary

Every trained world retains two authoritative structures:

1. the exact typed causal graph for reachability and provenance;
2. the full 48-dimensional learned coordinates for geometric evaluation.

The four-dimensional shadow is a passive observer derived from the full
coordinates. It is never used to admit a node, change an edge, create a fact,
rank epistemic authority, or issue a verdict. Its axes are `x`, `y`, `z`, and
`w`; all four are spatial and none represents time.

```text
exact causal graph ------------------------> admission authority
full 48D coordinates ----------------------> full geometric evidence
                  |
                  | train-only orthonormal projection
                  v
             4D all-spatial shadow --------> observer only
                  |
                  +-- drop one axis -------> four 3D views
                  +-- retain two axes -----> six 2D views
```

## Projection law

After full-coordinate training, the trainer fits a centered PCA basis using
only nodes assigned to the training split. The four basis rows are
orthonormal and sign-canonicalized. For full coordinates `a` and `b` and basis
`P`:

```text
shadow(a) = P(a - center)
||shadow(a) - shadow(b)||_2 <= ||a - b||_2
```

The inequality follows from orthogonal projection and is exhaustively checked
over every node pair before an artifact can pass. It means a same-radius
shadow cannot lose a full-space neighbor. It does not make the shadow
lossless: distance contraction can merge distinct points and create false
proximity.

The PCA center and basis are world artifacts, not model-adapter state. Their
training-node identity set, source-coordinate payload, basis, configuration,
and files are hash-bound in the training receipt and final world manifest.

## Required distortion accounting

Every run reports:

- orthonormal error, spectral norm, maximum distance expansion, and expansion
  violation count;
- a second deterministic build of the complete shadow artifact set and its
  canonical replay hash;
- quantized collision classes and collided placements;
- exact graph edges whose endpoints become indistinguishable in the declared
  shadow cell quantization;
- full-far pairs admitted as shadow-near false proximity;
- full-neighborhood recall and distance correlation for every split;
- held-out edge-distance stress;
- deterministic random-orthonormal-basis and axis-shuffle placebos.

Collisions, invisible edges, and false proximity are properties of an
observer. They never alter the exact graph.

## Composition law

Dropping a named 4D axis must equal applying the corresponding three-row
direct basis to the original 48D coordinate. Retaining any named pair must
likewise equal the corresponding direct two-row projection. All four 3D and
six 2D compositions are generated and checked for every node.

## Artifacts

- `coordinates.json` — full learned coordinates;
- `shadow-projection.json` — center, basis, method, hashes, placebos, and
  non-expansion certificate;
- `shadow-coordinates.json` — four-dimensional node shadows;
- `shadow-observers.json` — composed 3D and 2D observer views;
- `shadow-metrics.json` — distortion, held-out, and placebo measurements;
- `training-receipt.json` — gates and hashes binding all of the above.

Finalized packs place observer artifacts at their root and retain numeric
arrays under `training/`. The Rust loader verifies hashes, recomputes every
shadow coordinate, checks orthonormality, and exhaustively rechecks
non-expansion before exposing an observer view.

## Operator interface

```bash
lightcone-cli shadow <world-pack> <node-id>
lightcone-cli shadow <world-pack> <node-id> --drop-axis w
lightcone-cli shadow <world-pack> <node-id> --drop-axis z --drop-axis w
```

The returned receipt records the world and projection hashes, full/shadow/view
dimensions, kept and dropped axes, quantized cell, and the invariants
`observer_only=true`, `used_for_admission=false`, `holds_verdict=false`.
