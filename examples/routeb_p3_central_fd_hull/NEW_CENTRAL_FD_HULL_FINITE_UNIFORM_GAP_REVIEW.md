# P3 finite-grid uniform gap extraction

Status: conditional exact-real proof-attempt candidate, pending independent review.

## Finite theorem

`finite_uniform_gap_positive` takes a nonempty `Finset grid`, an exact-real
gap function, and `0 < gap x` for every `x ∈ grid`. It identifies the finite
infimum `finiteUniformGap grid hGrid gap` with one attained grid value, hence
proves it is positive. `finite_uniform_gap_lower` gives the lower-bound
consumer for every point in the same grid, and
`finite_uniform_gap_certificate` packages both facts.

## Finite-grid-only boundary

The exact `Bool` example uses `boundaryGrid = {false}` with gap values
`boundaryGap false = 1` and `boundaryGap true = 0`. The grid has the lower
bound `1`, while the omitted point violates it. Thus a finite-grid theorem is
not a continuous-domain coverage theorem and cannot justify claims at points
outside the supplied `Finset`. This obstruction is packaged by the theorem
`finite_grid_lower_bound_not_global`.

## External obligations

Nonemptiness, grid membership, and any map from the continuous family/domain to
the finite grid remain external premises. Sampling, numerical positivity,
central-FD coverage, derivative-hull coverage, source evidence, cap transfer,
admission, registry promotion, and Lean compilation are not asserted. No local Lean/Lake
command or broad regression was run.
