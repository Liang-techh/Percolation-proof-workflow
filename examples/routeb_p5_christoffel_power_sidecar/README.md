# Route-B P5 Christoffel power sidecar

This directory is intentionally narrow: it isolates the exact Christoffel power
identity from `examples/routeb_source_binding_audit/snapshots/current_exact/ChristoffelPower.lean`
into a fresh, standalone sidecar.

The Lean file proves the same algebraic statements, keeps the `#print axioms`
output, and does not import sparse SOS, flowpipe, terminal transfer, or any
true-DH source-binding material.

The intended boundary is the exact finite-sum identity plus its `Fin 6`
specialization:

- `RouteBP5ChristoffelPowerSidecar.christoffel_power_identity`
- `RouteBP5ChristoffelPowerSidecar.christoffel_power_identity_fin6`
- `RouteBP5ChristoffelPowerSidecar.mechanical_energy_hC`

If the pinned Lean environment is available, `verify.sh` compiles only this file
and records the `#print axioms` lines in the log. If the pinned environment is
missing or mismatched, it emits a blocked report with the exact reason instead
of pretending success.
