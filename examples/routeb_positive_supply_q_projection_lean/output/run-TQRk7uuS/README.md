# Physical Q-norm projection leaf

This is an independent leaf for the physical side of the relative-eta
frontier.  It expands the current exact source-side matrix

```text
diag(Q) = (3, 8, 95/7, 165/7, 45, 90),
Q[2,3] = Q[3,2] = -5
```

using zero-based Lean indices.  For `u=e4+e5`, the exact projection constant
is

```text
u' Q⁻¹ u = 7/165 + 1/45 = 32/495,
|u' eta| <= sqrt(32/495) * epsilon_Q
```

under `eta' Q eta <= epsilon_Q^2` and `epsilon_Q >= 0`.  The Lean theorem
also records a sharp two-coordinate witness.

This result is only an absolute Q-norm projection bound.  It does **not**
prove `|etaU| <= kappa*rho`: that requires the source defect to vanish at
equilibrium or an independently proved state-relative scaling estimate such
as `epsilon_Q <= c*rho`.  Consequently this leaf is source-binding evidence,
not a uniform relative-eta theorem, and it is not registry-eligible by itself.
