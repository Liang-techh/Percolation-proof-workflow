# Route-B P8 ramp reconstruction child

This sidecar formalizes the exact calculus core from `T-P8-006`:

- `c' = 0` and `c(0)=c₀` imply `c(t)=c₀`;
- `w' = c` and `w(0)=0` imply `w(t)=c₀ t`;
- at `T=1`, `w(1)=c₀`.

The interface is intentionally expressed with `HasDerivAt` on all real times,
which is a minimal Lean implementation of the interval-local mathematical
argument.  It does not establish ODE existence, uniqueness of the mechanical
coordinates, `[0,1]` flowpipe coverage, deployed true-DH binding, or P8/M4
admission.

The source is a pending candidate until the assigned validation agent runs the
pinned Lean verifier and supplies the compile receipt and axiom audit.
