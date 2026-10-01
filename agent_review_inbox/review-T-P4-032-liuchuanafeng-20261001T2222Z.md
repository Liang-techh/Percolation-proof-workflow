---
kind: review_result
review_id: T-P4-032-LIUCHUANAFENG-20261001T2222Z
task_id: T-P4-032
source_agent: 流川枫
created_at: 2026-10-01T16:22:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: 75d7f71bb1fb8909d6e7ef2b7310a49d299e7f78
---

# T-P4-032 audit: exact-real port identity remains uncompiled

## Exact question

Does the in-repo candidate prove, under `M_DD_inv * M_DD = 1`, `M_DD * v + DeltaM_DB * a_B = 0`, and `r_B - M_BD * v = 0`, that `R_port * a_B = r_B` for `R_port = -M_BD * M_DD_inv * DeltaM_DB`, with column vectors, `Matrix.mulVec`, shape `(B×D)(D×D)(D×B) = B×B`, and the leading minus preserved? If the file is only an uncompiled candidate, record that boundary and do not admit it.

## Inspected commit / paths

- Commit: `75d7f71bb1fb8909d6e7ef2b7310a49d299e7f78`.
- `agent_review_inbox/task_queue.md` still lists `T-P4-032` as `status: open`. Required output includes zero-sorry, allowed-axiom, pinned-toolchain, statement-comparator, and source-binding receipts if compilation succeeds. File presence is explicitly not a kernel receipt. Recorded candidate SHA-256 in the queue is `403C41C6F325E906A9D3555B6886D1371DFA2D84826ABCC7BF83C12E21293BFB`; this pass did not recompute that historical digest.
- Candidate read: `artifacts/task_routeb_o1_lean_api_audit_20260907/RouteBO1PortIdentity.lean` (blob `c9bd41c4e18d6581bf899958b4d06d64cf165d23`).
- No Lean, Lake, `#print axioms`, placeholder scan, or statement comparator was run. Exit code: not applicable.

## Statement check (text only)

The candidate defines

`R_port M_BD M_DD_inv DeltaM_DB = -(M_BD * M_DD_inv * DeltaM_DB)`

and theorem `routeB_port_identity` concludes

`(R_port M_BD M_DD_inv DeltaM_DB).mulVec a_B = r_B`

from a left inverse `M_DD_inv * M_DD = 1`, the D-row `M_DD.mulVec v + DeltaM_DB.mulVec a_B = 0`, and `r_B - M_BD.mulVec v = 0`.

Observed interface facts, not a compile receipt:

- Uses `Matrix.mulVec` / `*ᵥ`, not `vecMul`.
- Factor order is `M_BD * M_DD_inv * DeltaM_DB`, with a leading minus.
- Declared shapes are `M_BD : B×D`, `M_DD_inv : D×D`, `DeltaM_DB : D×B`, so the product is `B×B` if the matrix product elaborates.
- Inverse premise is left-sided only. No right inverse, invertibility witness, or source matrix is supplied.
- Proof text uses `Matrix.mul_assoc` and `linarith`; `Mathlib.Tactic.Linarith` is imported. No `sorry` or `admit` token appears in the file text. Absence of those tokens is not a kernel check.
- `M_DD` is used only in the left-inverse and D-row premises. It is not identified with a deployed DH block.

## Relation to the T-P4-030 sign boundary

The candidate does not state `r_B = R_gain * a_B`. Its conclusion is the allowed `R_port * a_B = r_B` form. That does not discharge the T-P4-030 consumer audit, and it does not authorize using `R_gain = -R_port` outside a norm-square/Frobenius cancellation. This review does not re-audit those consumers.

## Explicit non-admissions

- Not proved: the candidate compiles, is zero-sorry under a pinned toolchain, or has an allowed axiom set. No `#print axioms` receipt.
- Not proved: statement-comparator agreement with a producer, or source binding to deployed `dhport_lib.jl` / a lifted descriptor.
- Not proved: Float64 enclosure, positivity, coverage, residual absorption, flowpipe, terminal transfer, or registry admission.
- Not proved: the three premises hold for any physical block `(4,5)` state. They remain hypotheses.
- `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate.

## Admission label

`pending`

Strongest statement retained: the inspected Lean file is a conditional exact-real interface candidate whose text matches the requested `mulVec` / leading-minus / shape contract. It is not a compiled or source-bound theorem.

## Proposed integration (coordinator only)

1. Harvest this review as a pending receipt audit of parent `T-P4-032`. Do not close O1.
2. Do not write `state.json`, the verified registry, or external source from this file.
3. Do not rewrite other agents' T-P4-032 repair or compile reviews.
4. Next child, out of scope here: one pinned compile of `routeB_port_identity` with exit code, `#print axioms`, and a statement comparator. A green compile would still be `compiled_candidate` until source binding is separate.

## Unresolved blockers

1. No pinned Lean/Lake receipt on this pass.
2. Historical candidate SHA-256 was not recomputed against the current blob.
3. Left inverse and both row premises are uninhabited by a deployed source packet.

## Response / handoff

流川枫 claimed open `T-P4-032` and recorded a pending fail-closed boundary: the port-identity candidate matches the typed algebra contract on inspection, but remains uncompiled and unbound. No registry or formal-proof edit.
