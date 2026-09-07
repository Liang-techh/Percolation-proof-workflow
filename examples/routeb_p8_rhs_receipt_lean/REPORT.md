# P8 RHS receipt report

Status: **LEAN_VERIFIED_INTERFACE_OPEN**

## Verified scope

The focused Lean compilation checks a strict 14-coordinate receipt interface:

1. `FiniteEndpointPayload` is total over `Fin 14`, with lower and upper
   endpoint functions and an explicit order witness.
2. `RhsReceipt` stores endpoint data, `sourceHash`, `RoundingMetadata`, and
   `FullRhsBindingStatus` as explicit fields.
3. `CoordinateWiseIntervalContainment` is the coordinate-wise interval
   condition for the abstract parent RHS field.
4. `receipt_to_routeBP8PicardStep_hbox` proves that containment has exactly
   the shape required by `RouteBP8PicardStep.RhsIntervalPremise`.
5. `receipt_usable_for_routeBP8PicardStep` applies that adapter to the parent
   `fullX0_ramp_picard_step_decomposition` theorem.

## Deliberate open boundary

No Julia source is imported, executed, hashed, or numerically re-created by
this leaf.  No endpoint values are supplied.  The deployed concrete
`full_rhs!` binding is **OPEN**; the only binding status constructor exposed by
the interface is `FullRhsBindingStatus.open`.  A future source-authenticated
producer must provide both the concrete RHS binding and the separate
kernel-checkable `Contains` proof.

Rounding metadata is preserved as explicit provenance data, but it does not
silently imply outward rounding or interval correctness.  The semantic
containment premise is the admission gate.

## Focused verification

`verify.sh` uses Lean `v4.33.1` from `/home/z5242/sos_lean`, compiles only the
parent P8 leaf and this receipt leaf in an isolated temporary directory, and
scans the compiled source for `sorry`, `admit`, `axiom`, and `unsafe` markers.
The intended result is:

```text
P8_RHS_RECEIPT_LOCAL_COMPILE=PASSED
SOURCE_RESTRICTION_CHECK=PASSED
JULIA_FULL_RHS_BINDING=OPEN
```
