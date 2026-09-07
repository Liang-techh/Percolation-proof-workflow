---
kind: review_result
review_id: T-P4-031-LIUCHUANAFENG-20260907T1408
task_id: T-P4-031
source_agent: 流川枫
created_at: 2026-09-07T14:08:00-06:00
integration_status: pending
admission_label: architecture_only
inspected_commit: eac34076032b55542632e44af93556bce5ed141a
---

# T-P4-031 Decision memo: deployed vs lifted controller damping

## Exact question

Reconcile the damping sums before accepting any full lifted descriptor:

- deployed `dhport_lib.jl`: `(Kd+b_fr) = (1.3, 1.1, 0.95, 0.8, 0.65, 0.5)`
- `routeB_fourier_lifted_descriptor_model.jl`: `(Kd+Bfr) = (1.8, 1.4, 0.95, 0.5, 0.65, 0.8)`

Deliver a source-of-truth decision, parameter receipt, affected-equation list, and whether the lifted model must be regenerated or explicitly rejected as a surrogate. Do not treat this as P4/M4/registry admission.

## Inspected commit / paths

- Commit: `eac34076032b55542632e44af93556bce5ed141a`
- `agent_review_inbox/task_queue.md` — `T-P4-031` (status `open`)
- `docs/routeb-dh-source-coefficient-binding-next.md` — canonical source is `dhport_lib.jl`; Float64 / FD / solve remain open bridges
- Prior 流川枫 P8 decision `review-T-P8-002-liuchuanafeng-20260907T1335.md` (deployed RHS fidelity over proof-only surrogate)
- This review does **not** fetch or rewrite the external Julia sources; the two vectors above are taken as the queue-recorded current pins.

## Parameter receipt (exact mismatch)

Index convention: 1-based joints `i=1..6`.

| i | deployed `Kd+b_fr` | lifted `Kd+Bfr` | difference (lifted − deployed) |
|---|---:|---:|---:|
| 1 | 1.3 | 1.8 | +0.5 |
| 2 | 1.1 | 1.4 | +0.3 |
| 3 | 0.95 | 0.95 | 0 |
| 4 | 0.8 | 0.5 | −0.3 |
| 5 | 0.65 | 0.65 | 0 |
| 6 | 0.5 | 0.8 | +0.3 |

Observations:

1. The two 6-vectors are **not equal**. Joints 1,2,4,6 differ; only joints 3 and 5 coincide.
2. The mismatch is not a uniform scale: signs mix (`+0.5,+0.3,0,−0.3,0,+0.3`). Component permutation of the last three entries of the deployed vector (`0.8,0.65,0.5` vs `0.5,0.65,0.8`) also fails to explain joints 1–2.
3. Pointwise agreement on a subset of coordinates is not a source proof (forbidden by the task).
4. Decimal literals here are **identity labels of the recorded pins**, not IEEE-754 inclusion certificates and not exact-rational DH equalities.

## Source-of-truth decision

**Authoritative physical controller damping is the deployed `dhport_lib.jl` vector**

```text
(Kd + b_fr)_deployed = (1.3, 1.1, 0.95, 0.8, 0.65, 0.5)
```

**The Fourier lifted descriptor model is an analytic surrogate until regenerated against that vector or explicitly rejected.**

```text
(Kd + Bfr)_lifted    = (1.8, 1.4, 0.95, 0.5, 0.65, 0.8)   # NOT source-bound
```

Rationale, consistent with the P3 source-binding note that `dhport_lib.jl` is the canonical deployed dynamics and that analytic Fourier probes do not replace it:

- Any residual / co-state / port-energy consumer that claims to speak about the deployed closed loop must use `_deployed`.
- A lifted-model theorem that internally uses `_lifted` may exist as a **conditional analytic object**, but its source-binding flag stays `open` and its nodes stay below the verified registry.
- Silent copy of one vector onto the other is forbidden: it would either falsify the deployed plant or invalidate every receipt that hashed the old lifted file.

## Affected descriptor / nominal equations (named, not edited)

These equation families inherit the damping pin. None are rewritten in this review.

1. Linear damping force/torque: `tau_damp = -(Kd + b_fr) .* dq` (componentwise).
2. Nominal closed-loop force residual / co-state ports that absorb `tau_damp`.
3. Lifted Fourier descriptor right-hand side that currently substitutes `(Kd+Bfr)_lifted`.
4. Any C2 / acceleration / Schur remainder that treats controller damping as a numeric constant in the residual envelope.
5. Receipts whose payload hash includes `routeB_fourier_lifted_descriptor_model.jl`.

Consequence: regenerating the lifted model to `_deployed` is a **new artifact + new hash + new child task**, not an in-place patch of old certificates.

## Explicit rejection / keep-open statements

- Rejected: treating the current lifted model as a source-bound full descriptor of the deployed controller.
- Rejected: inferring source equality from joints 3 and 5 matching, or from any sampled trajectory agreement.
- Rejected: changing the controller in `dhport_lib.jl` while preserving old certificate receipts.
- Open: exact-rational / IEEE enclosure of each decimal pin; Float64 vs exact-real evaluation of the damping map; residual/Schur/flowpipe closure; P4/M4 admission.

## Admission label

`architecture_only`

This is a source-of-truth decision memo. It is not Lean/kernel evidence, not a regenerated model, and not a registry or `formal_certificate_allowed` change.

## Proposed integration (coordinator only)

1. Record this review as the T-P4-031 decision: deployed vector wins; lifted model remains a surrogate.
2. Do not mutate `state.json`, the verified registry, or external Julia sources from this file.
3. Next bounded child (out of scope): either (A) regenerate the lifted descriptor from `_deployed` with a new source hash and a typed adapter, or (B) keep the lifted file and mark every consumer `source_binding=open` / below registry.
4. Independent provenance receipt (owner slot `封不觉` in the queue) may hash the two Julia blobs when those files are present in the checkout; this review does not invent blob hashes for absent external paths.

## Unresolved blockers

1. In-repo copies of `dhport_lib.jl` and `routeB_fourier_lifted_descriptor_model.jl` were not opened in this commit snapshot (they live on the external Route-B dense-Mq path). Harvest should attach SHA-256 when the blobs are ingested.
2. Exact `Kd` vs `b_fr` split inside the deployed sum is not recorded here; only the summed pin is decided.
3. No theorem, residual envelope, or coverage statement is discharged.

## Response / handoff

流川枫 claimed open decision leaf `T-P4-031` and recorded an architecture-only source-of-truth: use deployed `(1.3,1.1,0.95,0.8,0.65,0.5)`; treat the lifted `(1.8,1.4,0.95,0.5,0.65,0.8)` model as an unbound surrogate until regenerated. No proof, no coverage, no registry edit.
