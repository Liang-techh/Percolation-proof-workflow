---
kind: review_result
task_id: T-P8-004
source_agent: Codex
created_at: 2026-09-06T00:00:00-06:00
integration_status: pending
---

# T-P8-004 — explicit-time contract sidecar

## Scope and decision boundary

This is a focused sidecar for the smallest explicit-time 13-state interface.
It does not modify the authoritative `RouteBP8PicardStep` theorem target, and it
does not claim a flowpipe, a solution theorem, or a source binding. The only new
code lives under `examples/routeb_p8_explicit_time_sidecar/`.

The purpose of the sidecar is to make three assumptions explicit and separate:

1. `c` is an external parameter, not a state coordinate.
2. the 14-state parent can be projected into the 13-state explicit-time family.
3. terminal transfer is stated as a separate predicate over the 13-state
   trajectory and `c`.

No broad regression was run.

## Implemented interface

The Lean leaf `examples/routeb_p8_explicit_time_sidecar/RouteBP8ExplicitTimeSidecar.lean`
defines:

- `State13` and `TimeVectorField13`;
- `forgetTail13` for the projection from the 14-state parent;
- `wSlot13` as the 13-state `w` coordinate;
- `explicitInitial13 x c`, which packages the mechanical energy bound, `w = 0`,
  and `c^2 ≤ 3`;
- `initialProjection13 z`, which is exactly the projected initial contract;
- `explicitTerminal13 y c` and `terminalTransfer13 y c`, which keep terminal
  transfer as a separate named assumption;
- `sourceFamily13`, a minimal placeholder stating that the explicit-time field
  is parameterized by `c`.

The sidecar also proves the single-direction bridge
`initialProjection13_from_fullX0 : FullX0 z → initialProjection13 z`.

## Verification result

The local verification script `examples/routeb_p8_explicit_time_sidecar/verify.sh`
compiled the pinned parent and the new sidecar successfully.

Observed result:

- `SOURCE_RESTRICTION_CHECK=PASSED`
- `P8_EXPLICIT_TIME_SIDECAR_COMPILE=PASSED`
- `EXPLICIT_TIME_CONTRACT_BOUNDARY=OPEN`

The verification remains local to the new leaf and the pinned parent leaf. It
does not attempt to prove any flowpipe coverage or theorem admission beyond the
minimal interface.

## Notes on the contract choice

This sidecar intentionally keeps the 13-state explicit-time contract separate
from the 14-state ramp theorem. That preserves the boundary established in the
earlier P8 reviews: `c` stays external, initial projection is explicit, and
terminal transfer is a separate predicate instead of a silent target rewrite.

The authoritative theorem target stays unchanged.
