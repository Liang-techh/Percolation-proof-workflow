---
kind: review_result
task_id: T-P5-003
source_agent: Codex
created_at: 2026-09-06T00:00:00-06:00
integration_status: pending
---

# T-P5-003: Christoffel power sidecar review

## Scope

This review records the new isolated sidecar under
`examples/routeb_p5_christoffel_power_sidecar/`.

I did not modify `StateStore`, any registry, any existing source file, or
`task_queue`. The work is confined to the new sidecar directory plus this
review note.

## Exact theorem boundary

The sidecar reproduces the exact Christoffel power identity from the snapshot,
with the following key declarations:

- `RouteBP5ChristoffelPowerSidecar.christoffel_power_identity`
- `RouteBP5ChristoffelPowerSidecar.christoffel_power_identity_fin6`
- `RouteBP5ChristoffelPowerSidecar.mechanical_energy_hC`

The file also retains:

- `RouteBP5ChristoffelPowerSidecar.contraction_swap`
- `RouteBP5ChristoffelPowerSidecar.christoffelMatrix_mul_velocity`

## Imports

The Lean sidecar imports only:

- `Mathlib.Data.Real.Basic`
- `Mathlib.Algebra.BigOperators.Fin`
- `Mathlib.Tactic.Ring`

It does not import sparse SOS, flowpipe, terminal transfer, or any true-DH
source-binding theorem.

## Verification command

The intended verification command is:

```powershell
bash examples/routeb_p5_christoffel_power_sidecar/verify.sh
```

The script checks the pinned Lean executable and mathlib cache first. If either
is missing or mismatched, it emits a blocked report with the exact expected and
actual values and exits nonzero.

## Exit code and evidence

Observed run:

- command exit code: `0`
- Lean compile exit code: `0`
- `#print axioms` output:
  - `RouteBP5ChristoffelPowerSidecar.contraction_swap` -> `[propext, Classical.choice, Quot.sound]`
  - `RouteBP5ChristoffelPowerSidecar.christoffel_power_identity` -> `[propext, Classical.choice, Quot.sound]`
  - `RouteBP5ChristoffelPowerSidecar.christoffelMatrix_mul_velocity` -> `[propext, Classical.choice, Quot.sound]`
  - `RouteBP5ChristoffelPowerSidecar.christoffel_power_identity_fin6` -> `[propext, Classical.choice, Quot.sound]`
  - `RouteBP5ChristoffelPowerSidecar.mechanical_energy_hC` -> `[propext, Classical.choice, Quot.sound]`

## Boundary statement

This sidecar is intentionally narrow. It proves the exact algebraic Christoffel
power identity and its `Fin 6` specialization, but it does not claim:

- sparse SOS certification;
- flowpipe or reachability coverage;
- terminal transfer;
- deployed true-DH source binding;
- any registry or queue mutation.
