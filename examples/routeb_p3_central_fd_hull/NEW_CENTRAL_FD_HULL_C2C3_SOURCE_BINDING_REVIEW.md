# P3 C2/C3 derivative-hull to source-function binding

Status: `OPEN_UNCOMPILED`; conditional exact-real proof-attempt.

## Identified gap

`NEW_CENTRAL_FD_HULL_C2C3_REMAINDER.lean` proves a sound consumer for an
abstract `C2C3TaylorCertificate`.  Its derivative hulls bound the certificate's
derivative fields on a box region, but that certificate does not itself identify
those fields with the deployed DH source function.

`NEW_CENTRAL_FD_HULL_ROUTEB_REAL_BINDING.lean` binds only the value field:
`taylorFunction x = M x + Cfd x + Gfd x` after separate entry bindings.  It
does not yet bind the first/second/third derivative fields, their hulls, the
rounded endpoints, and the coverage map to that same source function and same
box.

## Minimal binding contract

`C2C3SourceBinding` makes the missing seams explicit:

1. `same_function` binds the Taylor value to the exact source function on the
   same `region b x`.
2. `same_first_derivative`, `same_second_derivative`, and
   `same_third_derivative` bind all derivative fields to derivatives of that
   same source function on the same box.
3. `coverage` supplies one common `boxOf x`, proves that it is listed, and
   proves `region (boxOf x) x` for every domain point.
4. `same_rounded_endpoints` binds source rounded endpoints to the certificate's
   endpoints for the same listed box; endpoint ordering remains a separate
   soundness premise.
5. `source_dh_identity` binds the exact source function to the same DH
   coefficient decomposition `sourceM + sourceC + sourceG` on the domain.

The four extraction theorems show exactly what these premises buy: source
derivative hulls, DH identity, same-box rounded endpoints, and value binding at
one covered point.  A later Taylor lower-enclosure consumer may use these facts,
but no source-specific numerical or analytic premise is silently inferred.

## Minimal obstructions

`missing_same_function_obstruction` uses constant functions `1` and `0` to show
that an abstract Taylor value cannot be substituted for the source value without
an equality premise.  `missing_same_box_coverage_obstruction` uses domain
`Bool`, one listed box `{false}`, and a region containing only `false`; the
domain point `true` is then uncovered.  `missing_same_rounding_obstruction`
uses rounded endpoint values `1` and `0` to show that endpoint order or a
certificate endpoint does not establish identity with the source rounding.

## Remaining boundary

This closes only the logical shape of the binding seam.  It does not prove that
the deployed `Float64`/libm `M`, `Cfd`, `Gfd`, central finite-difference step,
mass regularizer, derivatives, rounded endpoints, or interval hulls satisfy the
fields.  The same exact-real source, same box, same rounding evidence, and
whole-domain coverage must still be supplied by an independent source/interval
certificate.  No continuous-domain, PDE, admission, registry, or Lean
compilation claim is made; status remains `OPEN_UNCOMPILED`.

No source, numerical artifact, state, coverage, admission, or registry file was
modified, and no wide regression was run.
