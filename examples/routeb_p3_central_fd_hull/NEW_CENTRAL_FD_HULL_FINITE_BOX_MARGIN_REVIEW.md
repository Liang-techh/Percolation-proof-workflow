# P3 finite-box common uniform margin

Status: `OPEN_UNCOMPILED`; conditional exact-real proof-attempt candidate.

## Finite uniformization

`FiniteBoxUniformMargin` requires a nonempty finite box set (`boxes_nonempty`), an explicit
`boxOf : D → B` map, per-box regions, positive `gapLower`, and a per-box cap
margin. `commonMu` is the exact `Finset.inf'` of the listed gaps.
`finite_box_global_uniform_margin` proves `0 < commonMu`, that it lower-bounds
the mapped box gap, and that the same common margin yields global capMax strict
slack on every covered domain point. The consumer theorem adds an existing
bound by `weightedLoad`.

## Boundary obstructions

`empty_box_obstruction` records that an empty box set cannot supply an infimum
witness. `broken_coverage_obstruction` gives a listed box/map with an omitted
point. The exact-real `continuousGap(x) = 1/(x+1)` pair of theorems shows that
pointwise positivity over an unbounded continuous parameter does not produce a
uniform positive lower bound; this is formalized by
`continuous_gap_no_uniform_positive_lower_bound`.

No finite grid, sample, interval/Taylor payload, solver output, source or
coverage claim is upgraded beyond the explicit premises. No admission,
registry promotion, or Lean compilation fact is asserted. No local Lean/Lake
command or broad regression was run.
