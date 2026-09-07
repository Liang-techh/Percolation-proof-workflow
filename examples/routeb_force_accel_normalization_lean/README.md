# Route-B C2 force-vs-acceleration normalization sidecar

This directory is a minimal Lean 4.33.1 exact-real, conditional math adapter
for the normalization issue recorded in
`docs/routeb-c2-d-normalization-audit.md`.

The main contract is:

```text
eF(t) = M eA(t)
||M x||² >= κ ||x||²,   κ > 0
```

If the force residual power is

```text
Σ_t ||eF(t)||² / (2 D) <= B,   D > 0,
```

then the exact finite-budget adapter proves

```text
Σ_t ||eA(t)||² <= 2 D B / κ.
```

Equivalently, with a lower singular-value bound `m > 0` and
`||M x||² >= m² ||x||²`, the factor is `2 D B / m²`.

The file also instantiates the abstract theorem for the exact rational block
`diag(1/5, 1/10)`. Its smallest singular value is `1/10`, so the resulting
bound is `Σ ||eA||² <= 200 D B`. This is a normalization sanity check only.

The counterexample theorem in the file records the boundary explicitly: a
force-only budget cannot bound acceleration when no positive lower operator
bound is supplied (take `M = 0`, `eF = 0`, and nonzero `eA`).

## Admission boundary

This is `CONDITIONAL_EXACT_REAL_FINITE_DIMENSIONAL_MATH_ADAPTER` only. It is
not a physical DH admission, not a Julia/Float64 source-binding theorem, not a
proof that the deployed `l_F = I_B f_B - M0_BB a_B` equals `M eA`, and not a
global residual, D-row, coverage, flowpipe, terminal-transfer, or registry
closure. In particular, the audit's distinction between the exact `I_B` block
and the distinct frozen `M0_BB` is preserved.

## Verification

From the workflow root, run:

```text
bash examples/routeb_force_accel_normalization_lean/verify.sh
```

The runner checks the toolchain pin, compiles only this sidecar with
`warningAsError=true`, rejects proof-escape tokens, and checks the printed
axiom dependencies. It does not run the repository test suite or modify
workflow state, receipts, registries, or any file outside this directory.
