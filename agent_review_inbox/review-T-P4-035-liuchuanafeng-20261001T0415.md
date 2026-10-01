---
kind: review_result
review_id: T-P4-035-LIUCHUANAFENG-20261001T0415
task_id: T-P4-035
source_agent: 流川枫
created_at: 2026-10-01T04:15:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: 348c50b1c56256df23839845f8fb5b41c156f42d
---

# T-P4-035 audit: force-scale source contract remains an obstruction

## Exact question

Smallest conditional statement connecting the deployed force descriptor to the Route-B block equation on `B=(4,5)` and `D=(1,2,3,6)`, with an explicit split of `M_BD*a_D`, force-scale terms `q5/100` and `q4/200`, and analytic-lifted surrogates. If equality is unavailable, return the strongest one-sided or conditional statement that remains valid.

## Inspected commit / paths

- Commit: `348c50b1c56256df23839845f8fb5b41c156f42d` (`Record GitHub Actions runner allocation recovery`, 2026-09-15T04:15:02Z).
- `agent_review_inbox/task_queue.md` — `T-P4-035` still `status: open`; coordinator finding 2026-09-07 records that selected canonical deployed and lifted files contain no literal/structural `q5/100` or `q4/200`, while lifted nominal rows contain `+q5/20` and `+q4/20`.
- `docs/routeb-dh-source-coefficient-binding-next.md` (blob `963ab5fdccc55f8852afd18fdb7625c97d55693d`) — canonical DH parameter ledger and source hashes; admission left `PENDING`.
- `docs/routeb-p4-mbd-projection-obstruction.md` (blob `7ceed94da30a62ed2742bc7041cccbcef3731123`) — exact rational remote-term obstruction at `q=0`.
- Inbox tree at the same commit: no prior `claim-T-P4-035-*` or `review-T-P4-035-*`.
- External Julia blobs were not reopened in this pass. Hashes below are the values already recorded in the in-repo binding note, not a fresh hash of an absent checkout.

## Index / order ledger (typed, not a theorem)

| object | convention recorded in inspected docs |
|---|---|
| block `B` | `(4,5)` one-based |
| complement `D` | `(1,2,3,6)` one-based; zero-based `[0,1,2,5]` when an O1 path is later typed |
| CSV / source rows | one-based; Lean `Fin 6` is zero-based |
| canonical dynamics file named by the binding note | `routeB_dense_Mq/dhport_lib.jl` |
| recorded SHA-256 of that file | `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936` |

The same SHA-256 appears in the queue as the `T-P4-036.4` canonical source hash. That match is a cross-note identity of a recorded digest, not a new byte-level rehash.

## Coefficient normalization finding

The task asks for force-scale contributions `q5/100` and `q4/200`. The queue coordinator finding states those literals are absent from the selected deployed and lifted files, and that the lifted nominal rows instead contain `+q5/20` and `+q4/20`. Deployed `tau` is described there as controller channels only.

This review does not reinterpret `1/20` as `1/100` or `1/200`. The factors differ:

```text
1/20 = 5/100 = 10/200
1/100 = (1/5)*(1/20)
1/200 = (1/10)*(1/20)
```

So the requested scale is not an index-order alias of the observed lifted coupling. F2 (coefficient normalization) stays open.

## What remains conditionally valid

1. Index split only: any later theorem that speaks about this seam must use `B=(4,5)` and `D=(1,2,3,6)` as above, and must not permute `D`.
2. Remote inertia term is not controlled by block-only PMI variables. The adjacent obstruction note re-sums `routeB_fourier_mass_BD_rational.csv` at `q=0` to

```text
M_BD(0) =
  [  7/60          0          0       1/60    ]
  [ -21/80000   41827/800000 8189/160000  0    ]
M_BD(0) e1 = (7/60, -21/80000)
||M_BD(0) e1||^2 = 784003969/57600000000 > 0
```

with checker `scripts/check_routeb_p4_mbd_obstruction.py` reported as `PROJECTION_OBSTRUCTION_EXACT`. This is a projection countermodel for `M_BD a_D` under `a_D = lambda e1`, not a source binding of the force descriptor and not a discharge of `T-P4-035`.
3. Analytic Fourier / lifted descriptor rows are surrogates until an authoritative source/config exhibits the requested force-scale terms. The binding note already says the exact-rational Fourier probe does not replace `dhport_lib.jl`.

## Explicit non-admissions

- Not proved: deployed force descriptor equals the Route-B block equation.
- Not proved: `q5/100` or `q4/200` occur in deployed `tau` or in the lifted nominal rows.
- Not proved: lifted `+q5/20` / `+q4/20` may be substituted for the requested scales.
- Not proved: Float64 enclosure, positivity, coverage, residual absorption, flowpipe, terminal transfer, or O1 parent closure.
- `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate.

## Admission label

`pending`

Strongest statement retained: source-contract obstruction. F0 source selection, F2 coefficient normalization, F3 true-DH `B=(4,5)` block projection, and F4 source-bound admission stay open. The exact `M_BD(0) e1` calculation is neighboring evidence for the remote-term seam only.

## Proposed integration (coordinator only)

1. Harvest this review as a pending obstruction on `T-P4-035`. Do not close the parent.
2. Do not write `state.json`, the verified registry, or external Julia sources from this file.
3. Next child, out of scope here: an authoritative source/config that either exhibits `q5/100` and `q4/200` with a fresh SHA-256, or replaces the task contract with the observed `1/20` coupling under an explicit user decision. Until then, do not feed O1 from the lifted model.

## Unresolved blockers

1. External `dhport_lib.jl` and the lifted descriptor were not present in this checkout; the recorded hash was not recomputed.
2. No sign-consistent `DeltaM_DB` contract can be stated until the force-scale literals are identified in one authoritative file.
3. No Lean receipt, axiom print, or comparator was run.

## Response / handoff

流川枫 claimed open `T-P4-035` and recorded a pending source-contract obstruction: requested `q5/100` and `q4/200` are not established, must not be rewritten as lifted `q5/20` and `q4/20`, and the block equation is not source-bound. No registry or formal-proof edit.
