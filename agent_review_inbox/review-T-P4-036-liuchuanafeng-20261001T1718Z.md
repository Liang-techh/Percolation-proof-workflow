---
kind: review_result
review_id: T-P4-036-LIUCHUANAFENG-20261001T1718Z
task_id: T-P4-036
source_agent: 流川枫
created_at: 2026-10-01T11:18:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: 8c07422dfcff39cb2f9513f46212da3a539419be
---

# T-P4-036 audit: Float64 angle/trig binding remains open

## Exact question

Can the P3 exact-real DH `theta`/`alpha` rows be bound to the deployed Julia `Float64` path through the four separated leaves — (i) `pi/2` and angle formation, (ii) argument range reduction, (iii) libm `sin`/`cos` enclosure, (iv) finite source-order propagation — with source hashes, per-link/per-atom index order, and a fail-closed status for each leaf? If not, record the obstruction and an uncompiled interface draft only.

## Inspected commit / paths

- Commit: `8c07422dfcff39cb2f9513f46212da3a539419be`.
- `agent_review_inbox/task_queue.md` (blob `b905132efb6e8a9b356a3023adb6d14905e6d686`): `T-P4-036` still `status: open`. Required output may be `INTERFACE_DRAFT__UNCOMPILED`. Boundary forbids discharging libm binding by sampling, pointwise Julia output, or a Taylor-only central-FD leaf. `formal_certificate_allowed=false` and `registry_promoted=false` must stay.
- `docs/routeb-p4-o2-minimal-proof-chain.md` (blob `aef9eeba421a5a3ed836b2cc9ec596ad4885e1e9`). Design only. Frozen source anchor `AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936`; operation-schedule hash `58209B231ED2BD1662B74B95CBBE5EE206AB1911BFDF03C8AED99C1BFF80C7C1`. The document states those hashes identify statements, not a runtime or numerical enclosure.
- Inbox already contains other agents' `T-P4-036.2` claims/reviews. They are not re-authored and are not treated as a close of parent `T-P4-036`. The queue harvest already records `.2` leaf-1 as `COMPILED_ENDPOINT_PROVENANCE_ONLY`, with parent/sibling authority still incomplete.
- No Lean compile, checker, Julia, or libm run was executed. Exit code: not applicable. Placeholder scan: not applicable.

## Leaf status

| leaf | recorded status | what this pass can say |
|---|---|---|
| A0 exact-real angle contract | design target only | formulas `theta_i = q_i + DH[i,1]`, `alpha_i = DH[i,4]`, phase vectors `theta: 0,-1,+1,0,0,0` and `alpha: -1,0,+1,-1,+1,0` are design inputs, not a source-text proof |
| `.1` Float64 angle formation | open | needs bit traces for `q_i`, DH constants, `pi`/`pi/2`, and each deployed add/constant conversion; decimal equality is insufficient |
| `.2` range/quadrant reduction | provenance-only child exists | queue says endpoint to `InRectBox` transport is compiled conditional; parent/sibling records and coverage join are absent; a chosen `k` plus Taylor cell is not libm reduction |
| `.3` libm `sin`/`cos` | open external receipt | source review, BigFloat sample, or Taylor interval does not create `externalLibmCertificate` |
| `.4` finite DH propagation | open | operation-schedule hash is not `dagRealizesSourceOrder`; two `fk_frames` calls and per-box coverage remain external |

Natural counts in the design, not discharged here: 12 formation inclusions, 12 reduction inclusions, 12 libm enclosures, 6 link-DAG enclosures.

## Typed interface draft (not admitted)

```text
structure AngleTrigTrace where
  qBits thetaBits alphaBits : Fin 6 → Bin64
  sinBits cosBits : Fin 6 → Fin 2 → Bin64
  quadrant : Fin 6 → Fin 2 → Int
  reduced sinBox cosBox : Fin 6 → Fin 2 → RatInterval
  sourceKey runtimeKey : String

theorem float64_angle_trig_conditional
    (tr : AngleTrigTrace)
    (hsrc : tr.sourceKey = canonicalDhportKey)
    (hform : angleFormationSound tr)
    (hred : rangeReductionSound tr)
    (hlibm : externalLibmCertificate tr)
    (hdag : sourceOrderDagSound tr)
    (hcov : boxCoverage tr) :
    angleContained tr ∧ sinCosContained tr ∧ linkGeometryContained tr
```

Index order intended by the design: link `i : Fin 6`, atom in `{theta, alpha}`. `z_i` must be the parent transform axis before `A_i`. No such theorem is compiled here. Classification of this draft: `INTERFACE_DRAFT__UNCOMPILED`. That label is not an admission.

## Explicit non-admissions

- Not proved: deployed `dhport_lib.jl` uses the recorded phase vectors or angle formulas. The source file is not in this repository; only the previously recorded SHA-256 was read.
- Not proved: Float64 formation, range reduction, libm `sin`/`cos`, or source-order DH propagation.
- Not proved: `.2` endpoint provenance covers parent/sibling boxes or the full partition.
- Not proved: P3 CSV, a point sample, or a Taylor central-FD leaf binds libm.
- Not proved: O2 parent closure, flowpipe, or registry promotion.
- `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate.

## Admission label

`pending`

Strongest statement retained: the in-repo O2 chain is a fail-closed design. Source and schedule hashes name the obligation; they do not enclose formation, reduction, libm, or finite propagation. Existing `.2` receipts stay provenance-only.

## Proposed integration (coordinator only)

1. Harvest this review as a pending obstruction on parent `T-P4-036`. Do not close O2.
2. Do not write `state.json`, the verified registry, or external source from this file.
3. Do not rewrite other agents' `.2` provenance.
4. Next child, out of scope here: one pinned formation trace for a single link atom, with bits, rounding mode, and source-key equality. A green interval print remains diagnostic until `.3` has an external libm certificate.

## Unresolved blockers

1. External `dhport_lib.jl` bytes were not re-hashed in this pass.
2. No per-atom Float64/libm receipt and no pinned Lean receipt for the conditional theorem.
3. `.2` parent/sibling authority and coverage join remain incomplete in the queue harvest.

## Response / handoff

流川枫 claimed open `T-P4-036` and recorded a pending fail-closed boundary: the four angle/trig leaves are specified but not discharged, and the typed adapter is only `INTERFACE_DRAFT__UNCOMPILED`. No registry or formal-proof edit.
