# Route-B P3 proof-facing domain patch

Status: applied to the external Route-B source with a recoverable backup.

Canonical file:

`C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\routeB_interval_branch_bound.jl`

Backup:

`routeB_interval_branch_bound.jl.bak-20260906-p3-proof-domain`

## Mathematical change

The branch-and-bound coverage driver now uses the exact proof-facing weights

```text
P_W_PROOF = (3/2, 4/5)
```

for `p_bounds`, ellipsoid tightening, split-width heuristics, and the global
root box.  The runtime Float64 `p_w` coefficients remain unchanged in the
dynamics implementation.  The root radii are computed with directed upward
rounding before interval construction.

This closes the one-ulp semantic mismatch where Float64 `0.8` is strictly
larger than exact `4/5` and can make the rectangular root box exclude a thin
shell of the exact mathematical ellipsoid.

## Evidence

- Old source SHA-256: `81DC1069EAAC8BD25B5F7213B4F6003EBB2B10994D0F7C7C1025E859659ABEF1`
- Patched source SHA-256: `C5349534FE1D01D87FB886BAE94EA05F373BCBE4E24B9A2C12411A31234C0590`
- The patch was syntax-inspected by source review.
- Julia was not on the Windows PATH in this session, so no runtime branch-and-bound
  execution is claimed here.  The existing report remains the evidence for the
  pre-patch diagnostic; a Julia/interval rerun is still required before any
  `coverage_complete` result is promoted.

This patch does not prove true-DH residual enclosure, global coverage, flowpipe
containment, or the final block-(4,5) theorem.  Those remain open frontier
obligations.
