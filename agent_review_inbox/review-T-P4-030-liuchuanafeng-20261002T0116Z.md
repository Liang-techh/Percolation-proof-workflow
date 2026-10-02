---
kind: review_result
review_id: T-P4-030-LIUCHUANAFENG-20261002T0116Z
task_id: T-P4-030
source_agent: 流川枫
created_at: 2026-10-01T19:16:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: 2f030748037ea177d91fef8c15de14eaa2fd60bd
claim_commit: 2a9b612c3f2c12b6f7bec291ae1e992efd8a4fc1
---

# T-P4-030 audit: port sign is local to one uncompiled candidate

## Exact question

After the corrected identity `R_port = -M_BD * M_DD(mu)^(-1) * (M_DB - M0_DB)`, does any inspected theorem simultaneously state `M_DD * v + DeltaM_DB * a_B = 0`, `r_B - M_BD * v = 0`, and `r_B = R_gain * a_B`? Does the typed adapter use `R_port * a_B = r_B`, and is `R_gain = -R_port` confined to norm-square/Frobenius cancellation? If downstream residual/co-state consumers are not source-bound, record the obstruction and do not admit the sign repair.

## Inspected commit / paths

- Queue and candidate inspected at `2f030748037ea177d91fef8c15de14eaa2fd60bd`. Claim-only commit `2a9b612c3f2c12b6f7bec291ae1e992efd8a4fc1` adds this agent's claim and is not evidence.
- `agent_review_inbox/task_queue.md` still lists `T-P4-030` as `status: open`. Required deliverable is a coefficient/sign ledger, affected theorem names/files, and a pinned Lean or exact-algebra receipt if available. Downstream consumers that are not source-bound must be returned as an obstruction.
- Candidate read: `artifacts/task_routeb_o1_lean_api_audit_20260907/RouteBO1PortIdentity.lean` (blob `c9bd41c4e18d6581bf899958b4d06d64cf165d23`).
- Prior algebraic child left untouched: `agent_review_inbox/review-T-P4-030-honglianmozun-20260908T0301.md`. This review does not rewrite it and does not adopt its scalar `R_port := -(Cs/2) D` shorthand as a source identity.
- Repository code search for `R_gain` and `R_port` returned `total_count: 0` with `incomplete_results: true`. That is not a proof of absence.
- No Lean, Lake, `#print axioms`, placeholder scan, or statement comparator was run. Exit code: not applicable.

## Sign ledger on the inspected candidate

The file defines

`R_port M_BD M_DD_inv DeltaM_DB = -(M_BD * M_DD_inv * DeltaM_DB)`

and `routeB_port_identity` concludes

`(R_port M_BD M_DD_inv DeltaM_DB).mulVec a_B = r_B`

from `M_DD_inv * M_DD = 1`, `M_DD.mulVec v + DeltaM_DB.mulVec a_B = 0`, and `r_B - M_BD.mulVec v = 0`.

Observed interface facts, not a compile receipt:

- The forbidden triple is not present in this file. The two row premises appear, but the conclusion is `R_port * a_B = r_B`, not `r_B = R_gain * a_B`.
- `R_gain` is not defined in this file. Nothing here licenses `R_gain = -R_port` outside a later norm-square/Frobenius consumer.
- Factor order is `M_BD * M_DD_inv * DeltaM_DB` with a leading minus. Shapes are `M_BD : B×D`, `M_DD_inv : D×D`, `DeltaM_DB : D×B`.
- Uses `Matrix.mulVec` / `*ᵥ`. No `sorry` or `admit` token appears in the file text. Absence of those tokens is not a kernel check.
- `M_DD`, `M_BD`, and `DeltaM_DB` are hypotheses. They are not identified with deployed `dhport_lib.jl` or a lifted descriptor.

## Consumer obstruction

The queue asks for propagation into every linear `r_B`, co-state, and cross-term consumer, including the sign of `s_B' r_B`, `a_B' r_B`, and Young/S-lemma cross terms. This pass found no source-bound consumer theorem that exposes `R_port`, `R_gain`, and a co-state orientation together. The 2026-09-08 algebraic child already recorded the ring-level parity rule and the same-co-state obstruction `Cs λ ΔM_DB = 0`; that child explicitly left typed source-to-consumer binding open. This audit does not close that gap and does not treat a square/norm identity as evidence that an unsquared residual sign is correct.

## Explicit non-admissions

- Not proved: the candidate compiles, is zero-sorry under a pinned toolchain, or has an allowed axiom set.
- Not proved: statement-comparator agreement, source binding, Float64 enclosure, domain coverage, residual absorption, or co-state sign repair in any consumer.
- Not proved: `R_gain = -R_port` may be used in a linear residual, co-state, or cross term.
- Not proved: the three premises hold for any physical block `(4,5)` state.
- `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate and is not a port-norm proof.

## Admission label

`pending`

Strongest statement retained: the only inspected typed adapter uses the allowed `R_port * a_B = r_B` conclusion and does not state the forbidden `r_B = R_gain * a_B` form. Downstream sign propagation remains an unbound obstruction.

## Proposed integration (coordinator only)

1. Harvest this review as a pending sign-consistency receipt for parent `T-P4-030`. Do not close the parent.
2. Do not write `state.json`, the verified registry, or external source from this file.
3. Do not rewrite 红莲魔尊's algebraic child or other agents' port-identity reviews.
4. Next child, out of scope here: one source-bound consumer that names `R_port` versus `R_gain` and checks each unsquared cross term. A green compile of `routeB_port_identity` would still be `compiled_candidate` until that binding exists.

## Unresolved blockers

1. No pinned Lean/Lake receipt on this pass.
2. No source-bound residual/co-state consumer was identified.
3. Code search was incomplete, so absence of `R_gain` outside the inspected file is not established.

## Response / handoff

流川枫 claimed open `T-P4-030` and recorded a pending fail-closed boundary: the port-identity candidate matches the required `R_port * a_B = r_B` sign on inspection, but consumer propagation is unbound. No registry or formal-proof edit.
