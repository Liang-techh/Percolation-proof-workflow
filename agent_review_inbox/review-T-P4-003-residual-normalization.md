---
kind: review_result
task_id: T-P4-003
source_agent: Codex
created_at: 2026-09-06T19:45:00-06:00
integration_status: pending
---

# T-P4-003 review: force / acceleration residual typed normalization only

## Scope and evidence

This is a read-only audit. It only checks typed normalization for the force residual
`l = I f - M0 a` and the PMI-side residual `d`. It does not close true-DH binding,
coverage, P4 admission, or any global residual claim.

Inspected:

- `docs/routeb-c2-d-normalization-audit.md`
- `examples/routeb_force_accel_normalization_lean/README.md`
- `examples/routeb_force_accel_normalization_lean/RouteBForceAccelNormalization.lean`
- `examples/routeb_force_accel_normalization_lean/REPORT.md`
- `examples/routeb_force_accel_normalization_lean/verify.sh`
- focused compile output under `examples/routeb_force_accel_normalization_lean/output/run-BbbmCQRa`

The existing documentation already separates the relevant units:

- `I_B f_B` is a force-side generalized-force expression;
- `M0_BB a_B` is a reference mass times acceleration;
- their difference `l_F = I_B f_B - M0_BB a_B` is force residual, not acceleration residual;
- the PMI-side scalar `d` remains an abstract D-row/Schur parameter and is not
  silently identified with `l_F`.

## Theorem signature

The smallest reusable Lean shape for this audit is the conditional exact-real adapter
in `RouteBForceAccelNormalization.lean`:

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

For the normalization sanity instance, the file also instantiates the exact rational
block:

```text
exactBlockMass_acceleration_budget_conversion :
  (eA eF : Fin ι → Vec 2) (D B : ℝ) →
  0 < D →
  (∀ t, eF t = matVec exactBlockMass (eA t)) →
  forcePower D eF ≤ B →
  accelerationBudget eA ≤ 200 * D * B
```

The negative boundary lemma
`no_force_only_acceleration_bound_without_lower_bound` is also relevant because it
records that a force-only budget does not by itself produce an acceleration-side
conclusion.

## Dependencies

Direct mathematical dependencies in the sidecar are minimal:

- `Mathlib` only, with the exact-real finite-dimensional vector and matrix definitions
  internal to the file.
- An explicit factorization premise `eF = M eA`.
- A positive operator lower bound `OperatorLowerBound M κ`.
- A positive scalar budget parameter `D`.

Documentary dependencies for the audit boundary are:

- `docs/routeb-c2-d-normalization-audit.md`, which states that `l_F` is force-side and
  must not be renamed as acceleration-side without an explicit bridge.
- `examples/routeb_force_accel_normalization_lean/README.md`, which states that the
  sidecar is conditional exact-real math only and does not claim a DH, Float64, D-row,
  coverage, or registry result.

## Evidence boundary

What the current evidence supports:

- a typed conversion from force residual power to acceleration budget under an explicit
  linear factorization and lower operator bound;
- a small exact rational sanity instance for `diag(1/5, 1/10)`;
- a boundary lemma showing that force-only information is insufficient without a lower
  bound.

What it does not support:

- identifying deployed `l_F = I_B f_B - M0_BB a_B` with an actual acceleration residual;
- identifying the PMI-side scalar `d` with `l_F` or with any acceleration residual;
- claiming true-DH binding, cell coverage, or P4/M4 closure;
- claiming that the sidecar closes the physical Route-B admission obligation.

Focused compile evidence:

- `examples/routeb_force_accel_normalization_lean/verify.sh` completed successfully.
- compiled object hash:
  `15ae2631b4c7aa012440701d58ba0234492f648061bea62f73ecc11f3f5bdd57`
- compile log hash:
  `d6e88c20b6d369239ef7d3d1d637e2fc3b26aa19f0ad6fbd3888f3206fe609a2`
- axiom reports in the compile log: exactly 3, each only
  `propext`, `Classical.choice`, `Quot.sound`

## Blocker

The remaining blocker is not the typed normalization itself. The blocker is the missing
admitted bridge from the deployed Route-B force residual `l_F = I_B f_B - M0_BB a_B`
to the PMI-side `d` contract, together with the missing explicit source/coverage
receipt that would let that bridge be interpreted as a physical true-DH statement.

Until that bridge exists, this should remain a conditional exact-real normalization
adapter only. It is reusable downstream, but it is not a closure proof.

