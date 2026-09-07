# P3 C2/C3 endpoint-uniform margin consumer

Status: `OPEN_UNCOMPILED`; conditional exact-real proof-attempt.

## Purpose

This sidecar consumes `C2C3SourceBinding` from
`NEW_CENTRAL_FD_HULL_C2C3_SOURCE_BINDING.lean`; it does not redefine the source
binding.  Its purpose is to expose the smallest downstream chain from a
source-bound C2/C3 derivative hull to a common endpoint margin.

## Exact same-box chain

For a domain point `x`, the proof selects the single box `b := boxOf x` and
requires, at that same `b` and `x`:

1. listed-box membership and region membership from `coverage`;
2. source derivative hulls, obtained by transporting the Taylor derivative
   hulls through `same_first_derivative`, `same_second_derivative`, and
   `same_third_derivative`;
3. the Taylor lower enclosure using the same source function, the same
   first/second derivative hulls, the same offset radius, and the same
   remainder bound;
4. comparison of that exact expression to `capLoad x - weightedLoad x`;
5. positive `gapLower b`, `gapLower b ≤ endpointLower b`, and the cap-load upper
   chain to `capMaxLoad x`;
6. equality of source rounded endpoints and certificate endpoints for the same
   listed box.

The finite common margin is `inf'` of the listed per-box `gapLower` values.
The only additional global condition is `boxes_nonempty`; domain coverage is
the pointwise `coverage` field already carried by `C2C3SourceBinding`.

## DH separation

`source_endpoint_to_common_uniform_margin` reports the independent DH identity
only as a separate conjunct.  The margin proof does not infer derivative hulls,
rounding, or coverage from `sourceM + sourceC + sourceG`.  Conversely, a DH
identity alone cannot produce the Taylor lower enclosure or a positive gap.

## Remaining obstruction

The sidecar's `taylor_lower_enclosure` and `taylor_to_cap_gap` are still
certificate premises.  They are exactly where a concrete source/interval
certificate must prove the C2/C3 remainder formula and its same-box soundness.
The sidecar does not prove those premises from Float64/libm code, samples,
central-FD values, or endpoint receipts.

If `coverage` is weakened, a domain point can be outside every region; if the
source-function or rounded-endpoint equalities are weakened, the certificate
can describe a different function or a different rounding.  Those are already
recorded by the source-binding obstructions and are not silently repaired here.

No concrete DH coefficient payload, numerical rounding proof, continuous-domain
upgrade, admission, registry promotion, or Lean compilation claim is made.
No source/state/registry file was modified and no wide regression was run.
