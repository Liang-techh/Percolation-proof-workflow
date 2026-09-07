# Route-B P3 current local-box replay

Status: `E2_RIGOROUS_NUMERICAL_LOCAL_REPLAY_CANDIDATE`

This records one bounded replay under the current `routeB_dense_Mq` source
snapshot. It is not a global coverage result and is not eligible for the Lean
verified registry.

## Run contract

- Julia: `1.12.7`
- mode: `local`
- center: the pinned Route-B local witness in `routeB_interval_branch_bound.jl`
- radius: `1e-3`
- eta: `5.6`
- safety factor: `2`
- mass enclosure: `meanvalue`
- Coriolis/gravity enclosure: `meanvalue_fd`
- interval guard: `weighted_krawczyk`
- branch depth/nodes: `8 / 512`
- global tree, SDP solver, and regression suite: not run

## Result

The single local cell was classified
`BOX_BRACKET_LOWER_NONNEGATIVE`, with

```text
h_lo = 5.9399730579...
h_hi = 6.0769766897...
kappa = 3.5506751e-4
center_enclosed = true
```

The raw payload has SHA-256
`578e7bdd35726512dc125c65b2331ec704ad2e8d40cf8bdc1023b747004fd67c`.

The source bindings used by the replay were:

```text
routeB_interval_branch_bound.jl = c5349534fe1d01d87fb886bae94ea05f373bcbe4e24b9a2c12411a31234c0590
routeB_interval_bounds.jl        = 7c7b7254a00b5ce21f6b9f512d5de7145ca8386e0420ecf71e92a5aeb5ca789f
dhport_lib.jl                    = aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936
routeB_Mq_M0.csv                 = 28d98ad71d1d6c2cbe830872cad9077f2f7b4e2d932794217eb68868fd2e2b40
run_local_box_replay_current.jl  = 7a930b34ddd291d1e166e11042f78d505a3b55d725f95019beda3438ae90b4a8
```

## Admission boundary

This is a positive result for one explicit local box under the current
Float64/central-finite-difference DH-chain semantics. It does not prove
interval-library soundness independently, exact physical source semantics,
global partition coverage, residual absorption, flowpipe containment, or
terminal transfer. Therefore it remains E2 and must not be labeled
`formal`, `theorem-backed`, `LEAN_VERIFIED`, or `formal_certificate_allowed`.

The full raw payload and checker report remain in the local ignored artifact
directory `artifacts/task_routeb_local_box_replay_current/`.
