# Positive-supply frontier: two-regime algebraic leaf

This independent sidecar formalizes the smallest useful split for the current
positive-supply frontier:

1. At the equilibrium slice, use the direct gate and charge an explicit floor
   to `beta0`; no denominator is formed.
2. On a nonzero slice, a projected state-relative bound
   `|etaU| <= kappa * rho` gives a positive first-order denominator when
   `kappa < A + D`.

For the B45 slice the exact threshold is
`A + D = 36802229/24000000`.

The sidecar also proves the matching obstruction: at `tau=1` and
`eta=kappa*rho`, any `kappa >= A+D` makes the denominator nonpositive.

The Lean file is intentionally source-unbound. It does not prove that the
deployed implementation has `eta(0)=0`, does not derive state-relative eta
scaling from the Q-ball, and does not prove the physical supply gate or
`J <= 1`. Those remain explicit parent obligations.
