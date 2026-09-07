# P4 sharp one-channel Schur sidecar

This directory formalizes the exact-real mathematics proposed by 柳冠一 in
`agent_review_inbox/review-T-P4-005-liuguanyi-20260906T2206.md`.

## Theorems

`P4SharpSchur.lean` contains:

- `schur_residual_nonnegative_iff`:
  for `p > 0`,
  `∀ x, 0 ≤ p*x^2 + 2*x*r + d*y^2` iff `r^2 ≤ p*d*y^2`;
- `zero_y_forces_zero_residual`:
  the universal quadratic at `y=0` forces `r=0`;
- `quarter_sq_lt_p4d4`:
  for the concrete block-4 coefficients,
  `(1/4)^2 < p4*d4`;
- `quarter_residual_absorption`:
  the relaxed rational source envelope
  `residual^2 ≤ (1/4)^2*y^2` is sufficient for the same scalar P4 quadratic.

The sidecar intentionally does **not** bind a Julia/DH source, Float64
execution, residual units, domain coverage, receipt, registry state, or P4/M4
admission.

## Focused verification

Pinned Lean toolchain:

```text
leanprover/lean4:v4.33.1
```

Run:

```bash
./verify.sh
```

The verifier uses the same nearby `../local_fkg` Mathlib environment convention
as the existing P4 child. If `lake` is unavailable it fails closed with
`BUILD_ENV_BLOCKED` and exit code 2.

At creation time, the automation environment did not expose `lean` or `lake`,
so no compile PASS is claimed in the corresponding review result. The intended
next step is a focused compile by the formalization/validation lane, followed by
the unique validator's independent axiom/admission check.
