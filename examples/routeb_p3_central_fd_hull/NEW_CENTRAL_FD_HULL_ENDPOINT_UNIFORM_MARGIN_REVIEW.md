# P3 finite-box endpoint certificate to common uniform margin

Status: `OPEN_UNCOMPILED`; conditional exact-real proof-attempt candidate.

## Combined bridge

`EndpointUniformMarginCertificate` requires nonempty finite boxes
(`boxes_nonempty`), an explicit
`boxOf` map and same-point region membership, per-box positive `gapLower`, and
rounded endpoint data with `rounding_interval_sound`. The endpoint-to-cap and
cap-load upper chain are explicit fields.

`commonMu` is the exact finite `Finset.inf'` of the box gaps.
`endpoint_to_common_uniform_margin` maps a domain point to one box, consumes
the rounding/endpoint and cap inequalities at that same point, and proves the
common quantitative margin plus weighted strictness. The consumer theorem
adds only `consumer ≤ weightedLoad`.

## Obstructions

`empty_boxes_endpoint_obstruction` blocks an infimum witness for an empty box
set. `broken_endpoint_coverage_obstruction` leaves `true` outside the listed
box region, and `zero_common_mu_endpoint_obstruction` records why zero margin
cannot imply strictness.

No interval/Taylor implementation, source or numerical payload, continuous
coverage theorem, admission, registry promotion, or Lean compilation fact is
inferred. No local Lean/Lake command or broad regression was run.
