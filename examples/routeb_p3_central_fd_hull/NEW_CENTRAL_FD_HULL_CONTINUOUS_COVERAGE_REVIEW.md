# P3 interval certificate to domain coverage bridge

Status: `OPEN_UNCOMPILED`; conditional exact-real proof-attempt candidate.

## Typed bridge

`ContinuousCoverageCertificate` keeps the domain predicate abstract and
requires a finite box set, per-box region, and explicit `boxOf : D → B` map.
The fields `mapping_in_boxes` and `mapping_in_region` are the actual coverage
premises. Per-box positive gap, cap-load upper chain, and
`rounding_interval_sound` are consumed at the mapped box and the same point.

`continuous_coverage_strict_slack` therefore yields a whole-domain pointwise
margin only under those mapping premises. The optional consumer theorem adds an
existing bound by `weightedLoad`.

## Finite-grid boundary

`omittedPointBoxes = {false}` and `omittedPointMap x = false` leave `true`
outside the declared region. `omitted_point_breaks_domain_coverage` and
`finite_grid_or_sample_not_continuous_coverage` record that finite grid or
sample membership cannot establish continuous-domain coverage.

No topology, interval/Taylor construction, solver output, sample receipt,
source evidence, numerical payload, admission, registry promotion, or Lean
compilation fact is inferred. No local Lean/Lake command or broad regression
was run.
