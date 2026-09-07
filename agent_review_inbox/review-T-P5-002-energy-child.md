---
kind: review_result
task_id: T-P5-002
source_agent: Codex
created_at: 2026-09-06T00:00:00-06:00
integration_status: pending
---

# T-P5-002: Route-B P5 energy child theorem review

## Scope

Bounded read-only review only. I inspected the energy bottleneck seam around Route-B P5 in:

- `examples/routeb_dh_power_binding/DHPowerBinding.lean`
- `examples/routeb_dh_power_binding/README.md`
- `examples/routeb_signed_gap_lean/SignedGap.lean`
- `examples/routeb_actual_energy_storage_lean/ActualStorage.lean`
- `examples/routeb_source_binding_audit/REPORT.md`
- `examples/routeb_source_binding_audit/snapshots/current_exact/ChristoffelPower.lean`

I did not run full regression, did not edit any existing source file, and did not touch StateStore/registry.

## Decision boundary

The smallest independently kernel/checker-verifiable child theorem I found is the pure Christoffel power identity, not the full Route-B physical energy claim. It can be checked independently because it is an exact finite-sum algebra theorem with no source-binding assumptions:

- `RouteBChristoffelPower.christoffel_power_identity`
- `RouteBChristoffelPower.mechanical_energy_hC`

The next layer up, `RouteBSignedGap.hasDerivAt_signedGap_from_source`, is still only a conditional source-space derivative bridge: it reuses the Christoffel identity and chain rules, but it does not prove the deployed DH source identification, actual trajectory existence, flowpipe coverage, or terminal transfer.

## Minimal child theorem statement

Best bounded child statement:

```text
(∑ i, v i * christoffelForce T v i) =
  (1 / 2 : ℝ) * ∑ i, v i * (∑ j, massRate T v i j * v j)
```

with the Fin 6 specialization exposed by `mechanical_energy_hC`.

Why this is the right child:

- it is purely algebraic and kernel-checkable;
- it captures the exact power cancellation seam needed by the P5 energy derivation;
- it is reusable by the signed-gap derivative theorem without importing any true-DH semantics;
- it stays below sparse SOS, source binding, flowpipe, and terminal transfer.

## Dependency chain

The narrow dependency stack is:

- `examples/routeb_source_binding_audit/snapshots/current_exact/ChristoffelPower.lean:18-28,44-101` for the finite-sum identity and its Fin 6 specialization.
- `examples/routeb_signed_gap_lean/SignedGap.lean:85-125,168-188` for the signed-gap derivative bridge that consumes the Christoffel theorem and chain rules.
- `examples/routeb_dh_power_binding/DHPowerBinding.lean:24-29,52-78` for the implementation-residual ledger and the final energy bound that still keeps concrete source binding separate.
- `examples/routeb_actual_energy_storage_lean/ActualStorage.lean:20-31,85-175` for the storage side, which still depends on explicit source hypotheses and does not itself close the physical binding.

## Evidence level

- `ChristoffelPower.lean`: exact kernel-checkable algebra; the file prints only the standard minimal axioms in its `#print axioms` block, so this is the strongest local proof artifact in the seam.
- `SignedGap.lean`: conditional theorem with explicit `HasDerivAt`/`HasFDerivAt` premises; evidence level is source-conditional, not deployed-source-verified.
- `DHPowerBinding.lean`: conditional residual accounting plus imported controller-power cancellation; evidence level is implementation-bound algebra, not true-DH binding.
- `ActualStorage.lean`: exact real algebra on a frozen literal model; evidence level is exact-real storage shape, not deployed source identification.

## Focused check

Focused check used for this review:

- inspected theorem statements and dependency lines in the files above;
- confirmed that the power identity is isolated from sparse SOS, flowpipe, and terminal transfer claims;
- confirmed that `SignedGap` explicitly says no hypothesis supplies the derivative of `Sgap`, kinetic power, or Christoffel power outside its source-side premises;
- confirmed that `ActualStorage` requires explicit hypotheses `H = H0`, `U = referencePotential q`, and `Uzero = ...`, so it does not promote a literal storage expression into a deployed true-DH theorem.

## Boundary summary

This review supports the following boundary statement:

- the child theorem boundary is the exact Christoffel power identity;
- the sparse SOS boundary stays separate and is not implied by the energy theorem;
- true-DH source binding remains separate from the Lean algebra;
- flowpipe and terminal transfer remain later obligations and are not discharged here.

The smallest useful next child, if one is needed, is a dedicated sidecar that instantiates the Christoffel power identity on the frozen Route-B mass tensor and exports the signed-gap derivative seam only as a conditional interface, without claiming any source-binding or reachability result.
