# P3 Taylor/interval remainder certificate

Status: `OPEN_UNCOMPILED`; conditional exact-real proof-attempt candidate.

## Minimal exact contract

`TaylorRemainderCertificate` explicitly carries function values, derivative
hulls, offset bounds, remainder bounds, lower/upper rounding endpoints,
`rounding_interval_sound`, and per-box gap/cap fields. The theorem
`taylor_remainder_to_per_box_margin` consumes the Taylor lower enclosure,
endpoint-to-gap relation, cap-load upper chain, and positive gap to produce the
per-box quantitative margin expected by the endpoint-uniform consumer.

The derivative, offset, and remainder nonnegativity fields remain explicit;
they are not inferred from sampled values or receipt metadata. The optional
consumer theorem additionally requires an explicit domain-to-box coverage
witness.

## Obstructions

`underestimated_remainder_obstruction` records that an exact remainder `1`
cannot be certified by a claimed bound `0`. `omitted_point_coverage_obstruction`
records a finite box list whose region omits `true`. Thus an unsound remainder
or missing coverage cannot support the downstream uniform-margin claim.

No Taylor implementation, interval library, numerical/source payload,
continuous coverage, admission, registry promotion, or Lean compilation fact is
asserted. No local Lean/Lake command or broad regression was run.
