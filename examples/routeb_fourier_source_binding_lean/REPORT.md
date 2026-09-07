# P3 exact DH-to-Fourier 36-entry source-binding report

## Verdict

`PASS — EXACT_36_ENTRY_SOURCE_TO_FOURIER_COEFFICIENT_EQUALITY_CHECKED`

The artifact-local exact checker evaluates the current canonical
`routeB_dense_Mq/dhport_lib.jl` mass formula in the Laurent ring
`Q(i)[z_1^+/-1,...,z_6^+/-1]`.  It parses the source parameters, treats finite
decimals as rationals, treats every `+/-pi/2` as an exact quarter turn, and
keeps the source parent-frame axis, midpoint COM, `I_val/3` isotropic inertia,
and `1/1000000` diagonal regularizer visible in the construction.

It compares the resulting coefficient map with the frozen 610-row rational
Fourier mass table after the same exact diagonal regularizer is added:

```text
entries checked: 36/36
CSV rows checked: 610
support range: 0..99 nonzero Laurent modes per entry
source SHA-256: aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936
CSV SHA-256: a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8
```

Coefficient-map equality implies equality of the corresponding real Fourier
evaluators for every real `q`; no grid, random sample, `Float64`, or Julia
runtime result participates in this exact PASS.

## Lean status

`ExactCoefficientBridge.lean` compiles locally with the pinned environment and
proves that equal rational coefficient maps, on a common finite support, give
equal real Fourier matrix evaluators for every `q`.  The 36-entry cardinality
fact is also kernel checked.  The compiled theorem is deliberately conditional
on the coefficient-map equality premise; it does not pretend that a Python
checker output is a Lean definition.

## First missing equality

For a full Lean/kernel source-binding closure, the first missing equality is
the instantiation of the Lean coefficient maps:

```text
forall i j nu,
  exactizedDHSourceCoeff i j nu = frozenCsvCoeff i j nu
```

The Python checker establishes the corresponding exact coefficient comparison
executable-side, but the current Lean sidecar has no reified 610-row payload
and no Lean reimplementation of the DH Laurent recursion.  This is the first
missing equality before a `LEAN_VERIFIED` all-entry source-binding claim.

Separately, for the deployed numerical implementation, the first runtime
semantic equality remains:

```text
mass_matrix_Float64(q) = exactized_DH_mass(q)
```

including binary64 decoding of literals and `pi`, argument formation,
`sin`/`cos`, matrix multiplication and accumulation, and regularizer
addition.  This sidecar intentionally does not attempt that bridge.

Consequently `formal_certificate_allowed=false` and
`physical_certificate_allowed=false`; no registry promotion is implied.
