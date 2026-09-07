# P3 derivative-hull endpoint to gap bridge

Status: `OPEN_UNCOMPILED`; conditional exact-real proof-attempt candidate.

## Typed bridge

`DerivativeEndpointCertificate` explicitly carries function values,
per-box derivative and offset bounds, remainder bounds, lower/upper endpoints,
and `rounding_interval_sound`. The endpoint theorem requires the derivative-hull
inequality, the function-to-cap gap inequality, endpoint-to-gap relation, and
per-box positive gap. `derivative_endpoint_to_gap_lower` then derives the exact
per-box lower bound consumed downstream.

The nonnegativity fields remain visible as obligations for derivative, offset,
and remainder budgets; they are not silently inferred from endpoint metadata.
The rounding enclosure is likewise a separate soundness premise.

## Obstructions

`sampled_positivity_not_global_hull` gives a sampled point with positive exact
value and an omitted point with nonpositive value. `unsound_remainder_bound_obstruction`
records that a claimed remainder `0` cannot upper-bound an exact remainder `1`.
Thus sampled positivity or an incorrect remainder cannot support the derivative
hull endpoint inequality.

No Taylor implementation, interval library, numerical payload, source evidence,
continuous coverage, admission, registry promotion, or Lean compilation fact is
asserted. No local Lean/Lake command or broad regression was run.
