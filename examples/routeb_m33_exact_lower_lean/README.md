# Route-B exact M33 lower-bound child

This sidecar proves the exact rational bound

```text
M33(q) >= 3016537 / 12000000
```

from the exactized canonical-source Fourier formula

```text
12159703/48000000 + 399/200000*cos(q5)
+ 147/3200000 * (cos(2*q4) + cos(2*q5)
                - cos(2*q4)*cos(2*q5)).
```

The proof uses only `u = cos(q5) in [-1,1]`, `x = cos(2*q4) in [-1,1]`,
and `cos(2*q5) = 2*u^2 - 1`. The result is an exact algebraic child, not a
sampled or floating-point lower bound.

`check_exact_lower.py` independently checks the polynomial coefficient
identity and the positive rational endpoint gap using Python `Fraction`.
This is a pre-Lean consistency check only; the pinned Lean receipt remains
the authoritative proof evidence for the sidecar theorem.

## Provenance

Upstream exact source-to-Fourier artifact:
`task_routeb_source_fourier_binding_current`.

Canonical source:
`routeB_dense_Mq/dhport_lib.jl`, SHA-256
`AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936`.

## Boundary

This file does not prove the parser/source equality, Julia Float64/libm
rounding, all-entry mass binding, inverse-matrix bounds, partition coverage,
flowpipe semantics, or Route-B admission. It is not automatically eligible
for the verified theorem registry until the pinned coordinator statement and
upstream source receipt are joined.

## Verification

`verify.sh` is intended for the scheduled pinned Lean agent. Local policy for
the coordinator is to avoid Lean/Lake execution and consume its receipt.
