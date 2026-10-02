---
kind: review_result
review_id: T-P4-MBD-PROJECTION-LIUCHUANAFENG-20261002T0014Z
task_id: T-P4-MBD-PROJECTION
source_agent: 流川枫
created_at: 2026-10-01T18:14:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: 3bd3712f024430f47bdcef3c0df4757419d21008
claim_file: agent_review_inbox/claim-T-P4-MBD-PROJECTION-liuchuanafeng-20261001T2313Z.md
---

# T-P4-MBD-PROJECTION audit: block-only remote premise stays open

## Exact question

Can the recorded nonzero `M_BD(0)e1` projection replace the invalid block-only `gammaRemote` premise by a smallest full-state descriptor / exact Schur / typed remote-enclosure contract, without treating arbitrary `lambda` as a physical trajectory or closing P4/M4?

## Claim status

This result closes the existing claim `claim-T-P4-MBD-PROJECTION-liuchuanafeng-20261001T2313Z.md`. No second claim was written. No prior `review-T-P4-MBD-PROJECTION-liuchuanafeng-*` was present at inspection. Other agents' files, `task_queue.md`, `agent_roster.md`, `state.json`, and the registry were not edited.

Roster note: `agent_roster.md` and the 2026-09-14 release note still mark 流川枫 unavailable. This envelope is a user-dispatched inbox result only; it does not restore a dispatch slot.

## Inspected commit / paths

- Commit reported by the contents API resource URI: `3bd3712f024430f47bdcef3c0df4757419d21008`.
- Queue leaf: `agent_review_inbox/task_queue.md`, section `T-P4-MBD-PROJECTION`, still `status: open`. Owner recorded there is `大爱仙尊`. This review does not transfer that ownership.
- `docs/routeb-p4-mbd-projection-obstruction.md` (blob `7ceed94da30a62ed2742bc7041cccbcef3731123`).
- `scripts/check_routeb_p4_mbd_obstruction.py` (blob `fb4da89369102f99f607c8cf53f5c9a05fee93c0`).
- `src/percolation_workflow/routeb_mbd_obstruction.py` (blob `b64409c75c420f1791d283afd8fcdddc0187f2ce`).
- The checker default source is outside this repository: `ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized" / "routeB_dense_Mq" / "routeB_fourier_mass_BD_rational.csv"`. That CSV was not present in the inspected tree and was not re-summed on this pass. Exit code: not applicable.

## Statement check

The obstruction note states, with `B=(4,5)` and `D=(1,2,3,6)`,

```text
M_BD(0) =
  [  7/60          0          0       1/60       ]
  [ -21/80000   41827/800000 8189/160000  0     ]
M_BD(0)e1 = (7/60, -21/80000)
||M_BD(0)e1||^2 = 784003969/57600000000 > 0
```

Independent rational arithmetic on the stated vector agrees:

`(7/60)^2 + (-21/80000)^2 = 784003969/57600000000 > 0`.

The in-repo checker implements the same countermodel shape: re-sum Fourier rows for `BLOCK_ROWS=(4,5)` and `REMOTE_COLS=(1,2,3,6)` at `q=0`, require a zero imaginary sum, and set status `PROJECTION_OBSTRUCTION_EXACT` only when that factor is positive. Both `formal_certificate_allowed` and `registry_eligible` are hard-coded false. A missing CSV returns `OPEN_FAIL_CLOSED` with exit 2.

Consequence retained from the note, as a projection countermodel only: if the currently projected block variables stay fixed and `a_D = lambda * e1`, then `rho_remote(lambda) = lambda * (7/60, -21/80000)` and its squared norm grows like `lambda^2`. No finite remote bound whose premises mention only those block variables can cover every such `lambda`. This is not a dynamics disproof and does not say an arbitrary `lambda` occurs on a physical trajectory.

## Smallest replacement premise (interface only)

The note already lists the three admissible repairs. The smallest typed premise that can replace block-only `gammaRemote`, and that this review does not inhabit, is:

1. Full-state map: a covered domain `Q` and a bound `||a_D(q)|| <= A_D` on that same domain, with `a_D` an actual descriptor acceleration, not a free `lambda`.
2. Exact Schur elimination on the same source packet: bind `M_BD`, `M_DD`, and the remote force so the eliminated remote residual is a function of the bound above, not of the block projection alone.
3. Equivalent typed adapter: `||M_BD a_D||^2 <= gammaRemote` only after (1) or (2) is discharged. A block-projection hypothesis is not an acceptable premise.

No one of these three is supplied by the inspected files. The projection factor is therefore negative evidence against the block-only premise, not a remote-enclosure theorem.

## Explicit non-admissions

- Not proved: the Fourier CSV re-sum. The matrix entries are taken from the obstruction note; this pass did not recompute the input SHA-256 or rerun `check_routeb_p4_mbd_obstruction.py`.
- Not proved: a physical trajectory reaches `q=0` with `a_D = lambda * e1` for arbitrary `lambda`.
- Not proved: full-state `a_D` bound, exact Schur elimination, or a typed remote residual enclosure.
- Not proved: source binding to deployed `dhport_lib.jl`, coverage, Float64 enclosure, positivity, or P4/M4 closure.
- `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate.

## Admission label

`pending`

Strongest statement retained: the stated `M_BD(0)e1` vector has exact positive squared norm `784003969/57600000000`, and the in-repo checker is fail-closed negative evidence against a block-only remote bound. The required full-state replacement premise is not inhabited.

## Proposed integration (coordinator only)

1. Harvest this review as a pending receipt on parent `T-P4-MBD-PROJECTION`. Do not close the leaf.
2. Do not write `state.json`, the verified registry, or external source from this file.
3. Do not rewrite the existing claim or other agents' files.
4. Next child, out of scope here: re-run the checker on the pinned Fourier CSV and record status, exit code, and `source_sha256`; separately supply one of the three replacement premises with a source packet.

## Unresolved blockers

1. External Fourier CSV was not re-summed on this pass.
2. No bounded full-state `a_D`, Schur packet, or typed remote enclosure is present.
3. Queue owner remains `大爱仙尊`; this result does not transfer ownership.

## Response / handoff

流川枫 completed the already-open `T-P4-MBD-PROJECTION` claim with a pending fail-closed boundary: the projection obstruction blocks a block-only `gammaRemote` premise, and the smallest full-state replacement is not proved. No registry or formal-proof edit.
