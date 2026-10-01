---
kind: review_result
review_id: T-P4-MBD-PROJECTION-LIUCHUANAFENG-20261001T2316Z
task_id: T-P4-MBD-PROJECTION
source_agent: 流川枫
created_at: 2026-10-01T17:16:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: 6bdc2925c8e1b9e4cf32ea7ac796147b161b4e77
claim_commit: 025361b45e8d0c7ce9537870af06c9dc9b453a1b
---

# T-P4-MBD-PROJECTION audit: block-only remote bound is not a theorem

## Exact question

Given the recorded exact `M_BD(0) e1` obstruction, what is the smallest typed full-state / Schur premise that can replace an invalid block-only `gammaRemote` bound, and does the current repository already inhabit that premise?

## Inspected commit / paths

- Docs and checker read at `6bdc2925c8e1b9e4cf32ea7ac796147b161b4e77`.
- Claim written at `025361b45e8d0c7ce9537870af06c9dc9b453a1b`.
- `agent_review_inbox/task_queue.md` still lists `T-P4-MBD-PROJECTION` as `status: open`.
- `docs/routeb-p4-mbd-projection-obstruction.md` (blob `7ceed94da30a62ed2742bc7041cccbcef3731123`).
- `scripts/check_routeb_p4_mbd_obstruction.py` (blob `fb4da89369102f99f607c8cf53f5c9a05fee93c0`).
- `src/percolation_workflow/routeb_mbd_obstruction.py` (blob `b64409c75c420f1791d283afd8fcdddc0187f2ce`).
- Default checker source is the external path `../6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_fourier_mass_BD_rational.csv`. That file is not in this repository. The checker was not executed. Exit code: not applicable. No source SHA-256 was produced on this pass.

## Arithmetic check of the recorded countermodel

The document states, at `q=0`, with `B=(4,5)` and `D=(1,2,3,6)`,

`M_BD(0) e1 = (7/60, -21/80000)`

and

`||M_BD(0) e1||^2 = 784003969/57600000000 > 0`.

Independent exact arithmetic on those two rationals agrees:

`(7/60)^2 + (-21/80000)^2 = 784003969/57600000000 > 0`.

This confirms the document's norm identity. It does not re-sum the Fourier CSV, so it does not re-establish that the matrix entries themselves are the deployed source.

The checker contract matches that shape: it re-sums only rows in `BLOCK_ROWS=(4,5)` and columns in `REMOTE_COLS=(1,2,3,6)`, rejects a nonzero imaginary sum, and returns `PROJECTION_OBSTRUCTION_EXACT` only when there are no errors and the first-column squared norm is positive. Both `formal_certificate_allowed` and `registry_eligible` are hard-coded false.

## Typed replacement premise

Let `pi_B` forget the remote acceleration `a_D`. The recorded countermodel keeps the current block projection fixed and sets `a_D = lambda * e1`. Then

`rho_remote(lambda) = M_BD(0) a_D = lambda * (7/60, -21/80000)`,

so `||rho_remote||^2 = lambda^2 * 784003969/57600000000`. No finite bound that depends only on the image of `pi_B` can hold for all `lambda`. This is a projection countermodel, not a statement that any such `lambda` occurs on a physical trajectory, and not a disproof of the dynamics.

Smallest replacement contract, not yet inhabited here:

1. Projection map. A future theorem must take a full-state packet `(q, v, a_B, a_D)` and may project to block variables only after `a_D` has been bound. `pi_B` alone is not a sufficient premise for `gammaRemote`.
2. Preferred seam (exact Schur elimination). On the same source and the same `q`, assume a D-row identity

`M_DD(q) * a_D + M_DB(q) * a_B + c_D(q,v) = u_D`

and a left inverse `M_DD_inv * M_DD = I`. Then

`a_D = M_DD_inv * (u_D - c_D - M_DB * a_B)`,

`rho_remote = M_BD * a_D`

is a function of same-source block data plus the already-bound remote force/bias. The free-`lambda` countermodel is excluded because `a_D` is no longer an independent scalar.
3. Alternative seam (domain bound). If Schur elimination is not available, the premise must carry an explicit same-domain bound `||a_D|| <= A_D < infinity` together with an operator bound on the same-source `M_BD`. A block-only energy hypothesis does not supply `A_D`.

Either seam still needs source binding, domain coverage, and a separate Lean/comparator receipt before it can be consumed by a P4 PMI child.

## Explicit non-admissions

- Not proved: the Fourier CSV in the external tree matches the printed `M_BD(0)`.
- Not proved: `lambda * e1` is reachable, or that the obstruction falsifies the physical dynamics.
- Not proved: a full-state descriptor, Schur elimination, or remote residual enclosure exists in the current repository.
- Not proved: coverage, Float64 enclosure, residual absorption, flowpipe, terminal transfer, or registry admission.
- `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate.

## Admission label

`pending`

Strongest statement retained: the recorded rational countermodel, if its matrix entries are later source-bound, shows that a block-only `gammaRemote` premise is insufficient. The smallest typed repair is a same-source Schur elimination of `a_D`, or an explicit full-state `a_D` bound. Neither is inhabited by this review.

## Proposed integration (coordinator only)

1. Harvest this review as a pending decision memo on parent `T-P4-MBD-PROJECTION`. Do not close P4 or M4.
2. Do not write `state.json`, the verified registry, or external source from this file.
3. Do not treat the document's matrix printout as a fresh checker receipt.
4. Next child, out of scope here: run `scripts/check_routeb_p4_mbd_obstruction.py` against the pinned Fourier CSV and return status, exit code, and `source_sha256`. A `PROJECTION_OBSTRUCTION_EXACT` result would remain negative evidence, not admission.

## Unresolved blockers

1. External rational CSV was not present in this repository, so the checker was not run.
2. No same-source `M_DD` inverse or remote-force packet was inspected for the Schur seam.
3. No domain bound on `a_D` was found in the inspected obstruction note.

## Response / handoff

流川枫 claimed open `T-P4-MBD-PROJECTION` and recorded a pending fail-closed boundary: the block-only remote premise is the wrong interface, and the smallest replacement is a same-source Schur elimination or an explicit full-state `a_D` bound. No registry or formal-proof edit.
