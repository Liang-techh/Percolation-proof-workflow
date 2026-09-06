# Relative-eta denominator and direct-gate leaf

This is a narrow, independent Lean leaf for the positive-supply frontier.
It proves the exact implication

```text
rho > 0, 0 <= tau <= 1, |etaU| <= kappa*rho,
kappa < 36802229/24000000
  => rho*(rho*(A + tau*D) - tau*etaU) > 0,
```

with

```text
A = 2002229/24000000,
D = 29/20,
K = 36802229/24000000 = A + D.
```

It also exposes `directGate` and proves its equivalent additive form
`E <= b + a1 * denominator` without dividing by the denominator. This is an
algebraic interface only. It does not bind `etaU` to a physical source,
prove a uniform source enclosure, prove feasibility, prove continuation, or
prove `J <= 1`.

The verification script uses only the pinned Lean 4.33.1 toolchain and the
cached Mathlib revision. It does not modify the original target directory and
does not run a project-wide regression.
