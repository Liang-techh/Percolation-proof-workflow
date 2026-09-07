---
kind: review_result
task_id: T-P4-004
source_agent: Codex
created_at: 2026-09-06T20:37:58-06:00
integration_status: pending
---

# T-P4-004: typed normalization Lean sidecar

## Scope and evidence

This is a focused audit of the smallest existing Lean sidecar for the typed
normalization boundary between the force residual `l = I f - M0 a` and the
PMI-side residual `d`. The only admissible connection is an explicit interface
premise; nothing here upgrades that relation to a physical true-DH claim,
coverage statement, or P4 parent closure.

Inspected:

- `examples/routeb_force_accel_normalization_lean/README.md`
- `examples/routeb_force_accel_normalization_lean/RouteBForceAccelNormalization.lean`
- `examples/routeb_force_accel_normalization_lean/verify.sh`
- focused compile output in
  `examples/routeb_force_accel_normalization_lean/output/run-A2NyxPf6`
- `agent_review_inbox/task_queue.md`

The sidecar already keeps the typed distinction in place:

- `forcePower` is defined on `eF` as a force-side quantity;
- `accelerationBudget` is defined on `eA` as a separate acceleration-side
  quantity;
- `acceleration_budget_le_of_force_power_budget` only concludes an
  acceleration bound after an explicit factorization premise
  `hfactor : ∀ t, eF t = matVec M (eA t)`;
- `exactBlockMass_acceleration_budget_conversion` is only a rational sanity
  instantiation of the same adapter;
- `no_force_only_acceleration_bound_without_lower_bound` records the boundary
  that force-only information does not suffice without a positive operator
  lower bound.

## Typed normalization boundary

The relevant normalization statement is the one already present in
`RouteBForceAccelNormalization.lean`:

```text
acceleration_budget_le_of_force_power_budget :
  (M : Mat n) (eA eF : Fin ι → Vec n) (D κ B : ℝ) →
  0 < D →
  0 < κ →
  (∀ t, eF t = matVec M (eA t)) →
  OperatorLowerBound M κ →
  forcePower D eF ≤ B →
  accelerationBudget eA ≤ 2 * D * B / κ
```

This is the correct minimum shape for the sidecar because it preserves both
typed objects and only links them through an explicit interface premise. The
force residual and the PMI residual remain distinct objects; `d` is not
implicitly promoted into `l`, and `l` is not silently retyped as `d`.

The exact rational block theorem:

```text
exactBlockMass_acceleration_budget_conversion
```

is just a compact witness that the adapter compiles for a concrete operator.
It does not imply any broader DH or coverage result.

## Focused compile evidence

The sidecar compiled successfully with the repository's pinned Lean 4.33.1 /
Mathlib environment.

Run:

```text
bash ./examples/routeb_force_accel_normalization_lean/verify.sh
```

Observed results:

- compile status: `PASS`
- axioms reported for the three exposed theorems:
  `propext`, `Classical.choice`, `Quot.sound`
- object hash:
  `15ae2631b4c7aa012440701d58ba0234492f648061bea62f73ecc11f3f5bdd57`
- compile log hash:
  `d6e88c20b6d369239ef7d3d1d637e2fc3b26aa19f0ad6fbd3888f3206fe609a2`

## What this does not claim

This sidecar remains conditional exact-real normalization only. It does not:

- close the P4 parent;
- mutate the authoritative checkpoint;
- establish true-DH binding;
- establish coverage;
- identify `l = I f - M0 a` with the PMI residual `d` without an explicit
  interface premise.

That boundary is the whole point of the file.

