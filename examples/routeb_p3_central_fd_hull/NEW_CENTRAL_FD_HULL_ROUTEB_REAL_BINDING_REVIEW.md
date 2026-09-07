# P3 current six-DOF Route-B real binding

Status: `OPEN_UNCOMPILED`; source-specific conditional proof-attempt candidate.

## Identified deployed semantics

Read-only source inspection identifies the following exact code-level names and
locations:

- `arm_MCG.m:12-17` uses central finite differences of `mass_matrix` with
  `h = 1e-5`; `:31-36` uses the same step for `G = dP/dq`.
- `robot_final/dhport_lib.jl:22-29` declares `MASS_REGULARIZER = 1e-6`,
  `CG_FINITE_DIFF_STEP = 1e-5`, and the `M/C/G` semantics string; `:46-60`
  builds regularized `M`, and `:73-99` computes `Cfd` and `Gfd`.
- The byte-identical `routeB_dense_Mq/dhport_lib.jl` has the same relevant
  source semantics; both copies were read-only hash-matched during this audit.
- `routeB_dense_Mq/routeB_pmi_certificate.jl:98-100` contains nominal `f1/f2`
  rows, which are not automatically the full deployed `arm_MCG` functions.

`RouteBExactSource` records the exact-real contract needed to bind those names:
the same `M`, `Cfd`, `Gfd`, potential, central-difference `h`, regularizer, and
their identities. `RouteBRealBinding` then binds the selected M/C/G entries to
the same box/domain Taylor function and per-box remainder/gap/cap chain.

## Current obstruction

The source is Julia/MATLAB `Float64`/libm code, while the sidecar contract is
over `ℝ`. The source does not by itself prove the exact equalities for
`h = 1/100000` and `mu = 1/1000000`, the stored `pi`/`sin`/`cos` rounding, the
finite operation-DAG enclosure, or the matrix/solve error bounds. The existing
`robot_final/routeB_interval_bounds.jl:7-17` is explicitly a rigorous-numerical
candidate interface, not a completed theorem certificate.

The current `routeB_partition_coverage.csv` marks geometric coverage complete
but dynamics coverage incomplete, and `routeB_interval_witness.csv` is a
single-point witness with radius `1e-10`. These cannot fill the global
`domain_binding` or per-box Taylor premises. `routeB_real_binding` therefore
remains conditional and cannot be promoted to a formal or registry claim.

No source files, numeric artifacts, state, coverage, admission, or registry
were modified. No local Lean/Lake command or broad regression was run.
