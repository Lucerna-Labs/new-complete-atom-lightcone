# Exact formal execution

The formal engine is a typed sidecar to the passive Lightcone. Admission may
provide relevant premises and definitions, but the Lightcone does not perform
arithmetic, prove a theorem, or turn an execution result into a verdict. The
host explicitly submits a `lightcone_formal::Request` and receives an
`ExecutionReceipt` only when two independently shaped exact implementations
agree.

## Current primitive families

- exact rational addition, subtraction, multiplication, and division;
- integer greatest common divisor, least common multiple, and bounded
  primality testing;
- one-variable and two-by-two linear systems plus polynomial evaluation;
- exact polynomial derivatives and definite integrals;
- binomial coefficients and arithmetic-series sums;
- squared Euclidean distance, twice-triangle area, Pythagorean checks,
  orientation, rational midpoint, point-on-segment classification, segment
  intersection, twice-polygon area, and rational line intersection;
- disjoint probability union, conditional probability, and binary Bayes
  updates;
- typed rate-distance, unit-rate, percent-of, and percent-change problems.

Inputs are bounded where computation could become unreasonably expensive.
Division by zero, singular systems, degenerate line definitions, non-unique
line intersections, malformed polygons, invalid probabilities, and exact
integer overflow fail closed.

## CLI example

```bash
cargo run -q -p lightcone-cli -- formal \
  '{"primitive":"geometry_line_intersection","arguments":{"first_start":{"x":0,"y":0},"first_end":{"x":3,"y":3},"second_start":{"x":0,"y":2},"second_end":{"x":4,"y":0}}}'
```

The returned rational point is accompanied by the independently computed
oracle value, an agreement flag, the primitive identity, and the formal runtime
identity. Downstream prose generation may explain this receipt, but cannot
rewrite its value or erase its assumptions.
