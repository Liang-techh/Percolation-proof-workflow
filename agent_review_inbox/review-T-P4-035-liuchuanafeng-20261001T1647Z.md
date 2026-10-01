---
kind: review_result
task_id: T-P4-035
review_id: T-P4-035-LIUCHUANAFENG-20261001T1647Z
source_agent: 流川枫
created_at: 2026-10-01T10:47:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: 1b95b2c407193d0462fa6ea4b9bcf481945ebefd
claim_ref: agent_review_inbox/claim-T-P4-035-liuchuanafeng-20261001T0410.md
---

# T-P4-035 audit: force-descriptor block projection remains a source-contract obstruction

## Exact question

What is the smallest conditional statement that connects the deployed force descriptor to the Route-B block equation on `B=(4,5)` and `D=(1,2,3,6)`, and which terms are `M_BD*a_D`, which are the force-scale contributions `q5/100` and `q4/200`, and which are analytic-lifted surrogates? If source equality is unavailable, record the mismatch obstruction. Do not close O1 or the registry.

## Inspected commit / paths

- Commit: `1b95b2c407193d0462fa6ea4b9bcf481945ebefd`.
- Existing claim: `agent_review_inbox/claim-T-P4-035-liuchuanafeng-20261001T0410.md` (blob `47a50ce68e8fcdffbada8e457218deaee7f0be6c`). No prior `review-T-P4-035-*` was present in the inbox listing at claim time or in this pass.
- `agent_review_inbox/task_queue.md`: `T-P4-035` still `status: open`. Coordinator finding (2026-09-07) says the selected canonical deployed and lifted files contain no literal `q5/100` or `q4/200`; lifted nominal rows contain `+q5/20` and `+q4/20`; deployed `tau` contains only recorded controller channels. F0/F2/F3/F4 remain open.
- `docs/routeb-p4-kc-force-contract.md` (blob `bd673285371bbb7d0e55bd7ff86626a72b7c80a3`).
- `docs/routeb-p4-mbd-projection-obstruction.md` (blob `7ceed94da30a62ed2742bc7041cccbcef3731123`).
- No Lean compile, Julia run, or `scripts/audit_routeb_p4_source_contract.py` / `scripts/check_routeb_p4_mbd_obstruction.py` execution in this pass. Exit code: not applicable.

## Term ledger (index order held fixed)

Index order used by both inspected notes: `B=(4,5)`, `D=(1,2,3,6)`. This review does not reorder those blocks.

| term | classification in inspected docs | admission |
|---|---|---|
| `M_BD(q)*a_D` | remote acceleration action on `D`; at `q=0` the Fourier CSV re-sum gives `M_BD(0)e1=(7/60,-21/80000)` with squared norm `784003969/57600000000 > 0` | exact rational countermodel for block-only control; not a deployed-source equality |
| `rho_kc^f = (q5/20, q4/20)` | normalized PMI cross term from `kc=1/20` | algebraic identity inside the canonical PMI source note; not deployed `tau` |
| `rho_kc^F = diag(1/5,1/10)*(q5/20,q4/20) = (q5/100,q4/200)` | force-scale composition after `I4=1/5`, `I5=1/10` | conditional adapter child; absence of the literal string is not absence of the algebra, and presence of the algebra is not deployed equality |
| deployed `tau = -Kp*q - (Kd+b_fr)*dq + G0v + (gw_coef .* I_val)*w` | controller channels only; no `kc` torque in that note | mismatch against the PMI `kc` term; must be charged as an additive force residual, not deleted |
| analytic-lifted nominal `+q5/20`, `+q4/20` | lifted surrogate named by the coordinator finding | not silently identified with `q5/100` or `q4/200` |

Units stay split: a force residual and `M_BD*a_D` are not interchangeable until an explicitly bound positive mass operator and its inverse are supplied. That inverse binding is outside this leaf.

## Strongest conditional statement retained

If, on one shared source key and the same `q`, the canonical PMI force construction is accepted and the inertia scales are exactly `I4=1/5`, `I5=1/10`, `kc=1/20`, then the cross contribution in force coordinates is exactly `(q5/100, q4/200)`. Separately, if the rational Fourier snapshot `routeB_fourier_mass_BD_rational.csv` is the mass model, block-only PMI variables do not control `M_BD*a_D`, because the `q=0` projection countermodel has positive remote norm for `a_D=lambda*e1`.

Neither premise is discharged here as deployed `dhport_lib.jl` equality. The two statements must not be added into one residual without a typed mass/inverse bridge.

## Mismatch obstruction

F0 source selection remains open: deployed controller `tau` in the force-contract note has no `kc` term, while the lifted nominal rows use `1/20` coupling and the requested task scale is the composed `1/100` / `1/200` force term. F2 coefficient normalization is therefore only an algebraic composition, not a source identity. F3 true-DH block projection is not proved; the in-repo obstruction is a Fourier-snapshot countermodel, not a byte-level projection of `dhport_lib.jl`. F4 source-bound admission stays closed.

External `dhport_lib.jl` bytes were not re-read in this pass. Pointwise or sampled agreement is not used as source equality.

## Explicit non-admissions

- Not proved: deployed force descriptor equals the Route-B block equation.
- Not proved: `q5/100` and `q4/200` occur in deployed `tau`.
- Not proved: Float64 enclosure, positivity, coverage, residual absorption, flowpipe, terminal transfer, or O1 parent closure.
- `formal_certificate_allowed` and registry promotion are not changed. This file is not a formal certificate and does not edit `state.json`.

## Admission label

`pending`

## Proposed integration (coordinator only)

1. Harvest as a pending obstruction on the already-claimed leaf `T-P4-035`. Do not close the parent.
2. Do not write the verified registry, `state.json`, or external source from this file.
3. Next child, out of scope here: one same-key packet that names the authoritative source file/hash, the chosen coordinate (`f` vs `F`), and a separate `M_BD*a_D` premise. A green source-text checker remains non-admitting, as the force-contract note already says.

## Unresolved blockers

1. No fresh hash of deployed `dhport_lib.jl` in this pass.
2. No executed source-contract or projection checker exit code in this pass.
3. No pinned Lean receipt for the conditional force-scale adapter or the block-projection countermodel.

## Response / handoff

流川枫 completed the open claim on `T-P4-035` with a pending fail-closed boundary: force-scale `(q5/100,q4/200)` is only the composed PMI adapter, `M_BD*a_D` is a separate remote term with an in-repo projection countermodel, and deployed `tau` still mismatches both. No registry or formal-proof edit.
