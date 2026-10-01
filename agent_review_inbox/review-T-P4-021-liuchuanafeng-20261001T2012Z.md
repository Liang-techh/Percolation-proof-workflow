---
kind: review_result
review_id: T-P4-021-LIUCHUANAFENG-20261001T2012Z
task_id: T-P4-021
source_agent: 流川枫
created_at: 2026-10-01T20:12:00Z
integration_status: pending
admission_label: pending
inspected_commit: 45a7961ae4f088014102918783cd3c7ddfbc6d7d
---

# T-P4-021 audit: Frobenius port-bound lift is not source-bound

## Exact question

Can `P4.residual_port_frobenius_bound` and its five hashed source artifacts be consumed by the residual PMI through the combined-Schur Young route, after replaying the 5120 resolved cells and the exact rational Young budgets at `eta=2.7` and `eta=5.6`, without changing residual semantics or equating `||R a_B||^2` with robust-PMI `E_k`? If not, record the obstruction and the minimal typed interface only.

## Inspected commit / paths

- Commit: `45a7961ae4f088014102918783cd3c7ddfbc6d7d`.
- `agent_review_inbox/task_queue.md` (blob `b905132efb6e8a9b356a3023adb6d14905e6d686`): `T-P4-021` is still `status: open` (candidate leaf recorded locally at Route-B revision 407). The queue already records that a local replay found Frobenius does not pointwise dominate the induced bound: 22 cells at `eta=2.7` and 39 cells at `eta=5.6`. That comparison is an obstruction, not a license to pick a norm by pointwise order.
- Inbox tree at the same commit: no prior `claim-T-P4-021-*` or `review-T-P4-021-*`.
- Repository examples tree: no path containing `frobenius` or `residual_port_frobenius`. The five hashed source artifacts and the 5120-cell ledger are not present in this checkout.
- Related in-repo sidecar, not a discharge of this leaf: `examples/routeb_p4_young_feasibility_lean/P4YoungFeasibility.lean` (blob `038e3944fa19fadec331234bc9a47c166b2af03d`) and its README (blob `0a70cc92f91dc58f1c9061b9f2faeaa666580e82`). It freezes the source-independent scalar cost `(1+theta)*A + (1+1/theta)*P` and states that it does not bind concrete P4 values of `A`, `P`, `D`, or `m`, and does not prove true-DH, Float64, coverage, provenance, or registry admission.
- No Lean compile, cell replay, checker, or hash verification of the five external artifacts was executed. Exit code: not applicable. `#print axioms`: not applicable. Placeholder scan: not applicable.

## Recorded comparison, not re-certified

The queue text is the only in-repo source of the cell counts. This pass does not re-derive them:

| eta | queue-recorded cells where Frobenius fails to dominate the induced bound | this pass |
|---|---:|---|
| 2.7 | 22 | not replayed |
| 5.6 | 39 | not replayed |

Those counts, if later confirmed against the hashed ledger, block any claim that the Frobenius port bound can replace the induced bound by pointwise order. They do not by themselves prove the converse induced bound either.

## Quantity separation

- Port-energy quantity named by the task: `||R a_B||^2`.
- Robust-PMI factor: `E_k` in `l_true = l_poly,k + E_k xi`.
- Scalar Young sidecar symbols `A` and `P` are not identified here with `A_up = a_B^T B_up a_B` or with `rho_F^2`.

No typed descriptor/source adapter equating the port-energy quantity with `E_k` was found. They remain non-interchangeable.

## Typed interface draft (not admitted)

```text
structure FrobeniusPortTrace where
  eta : Rat
  cellCount : Nat
  sourceHashes : Fin 5 -> String
  coverHash : String
  leftOutputMetric : Bool
  upwardSevenDecimal : Bool

theorem frobenius_port_conditional
    (tr : FrobeniusPortTrace)
    (hs : hashesMatch tr.sourceHashes canonicalFive)
    (hc : coverHashMatch tr.coverHash)
    (hor : tr.leftOutputMetric = true)
    (hround : upwardSevenDecimalSound tr)
    (hdom : pointwiseDominatesInduced tr) :
    portEnergyConsumed tr
```

`hdom` is the premise the queue says already fails on 22 and 39 cells. This draft is `INTERFACE_DRAFT__UNCOMPILED`. That label is not an admission. A positive Young margin, a `RESOLVED` flag, or `implicit_HG_spd` is not a hypothesis of this statement and must not be added as a discharge.

## Explicit non-admissions

- Not proved: the five source artifacts exist at the declared hashes, or that 5120 cells were covered.
- Not proved: exact rational Young budgets at `eta=2.7` and `eta=5.6`.
- Not proved: left-output metric orientation or the upward seven-decimal rounding contract.
- Not proved: Frobenius dominates, or is dominated by, the induced bound. The queue obstruction is preserved, not independently replayed.
- Not proved: `||R a_B||^2` may be substituted for robust-PMI `E_k`.
- Not proved: the scalar Young sidecar instantiates this leaf.
- Not proved: residual PMI closure, Float64/DH correctness, flowpipe, or registry promotion.
- `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate.

## Admission label

`pending`

Strongest statement retained: the in-repo record already forbids selecting the Frobenius norm by pointwise order, and the source ledger required to consume the bound is absent from this commit. The scalar Young sidecar stays source-independent.

## Proposed integration (coordinator only)

1. Harvest this review as a pending obstruction on `T-P4-021`. Do not close the residual PMI parent.
2. Do not write `state.json`, the verified registry, or external source from this file.
3. Do not treat `examples/routeb_p4_young_feasibility_lean` as a source-binding receipt for this leaf.
4. Next child, out of scope here: one hashed cell ledger with the 22/39 counterexample indices, eta, and both norms, still below registry.

## Unresolved blockers

1. `P4.residual_port_frobenius_bound` and its five hashed artifacts are not in the inspected tree.
2. The 5120-cell replay and exact rational Young budgets were not re-executed.
3. No pinned Lean theorem binds port energy to `E_k` or to the induced-norm comparison.

## Response / handoff

流川枫 claimed open `T-P4-021` and recorded a pending fail-closed boundary: the Frobenius port-bound cannot be lifted on the evidence present at `45a7961ae4f088014102918783cd3c7ddfbc6d7d`, and the queue's non-dominance counts stay an unreplayed obstruction. No registry or formal-proof edit.
