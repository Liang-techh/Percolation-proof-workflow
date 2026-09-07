# P3 C2/C3 Taylor remainder contract

Status: `OPEN_UNCOMPILED`; conditional exact-real proof-attempt candidate.

## Regularity and same-box fields

`C2C3TaylorCertificate` explicitly carries function value, first/second/third
derivative functions, same-box first/second/third derivative hulls, offset radius,
remainder bound, rounded endpoints, and per-box gap/cap data.
`c2c3Regularity` and `regularity_sound` are separate premises; no C2/C3 fact is
inferred from samples.

`c2c3_to_per_box_margin` consumes the Taylor lower enclosure, endpoint-to-gap
relation, cap-load upper chain, and positive gap to produce the per-box margin
needed by endpoint-uniform consumers. The optional consumer theorem requires an
explicit domain-to-box coverage witness.

## Obstructions

`underestimated_remainder_obstruction` rejects an exact remainder `1` with a
claimed bound `0`. `missing_regularity_obstruction` is the fail-closed marker
for an absent regularity premise. Neither sampled positivity nor an endpoint
receipt supplies these missing mathematical obligations.

No concrete Taylor implementation, interval library, numerical/source payload,
continuous coverage, admission, registry promotion, or Lean compilation fact is
asserted. No local Lean/Lake command or broad regression was run.
