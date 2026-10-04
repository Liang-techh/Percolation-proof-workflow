---
kind: review_result
review_id: review-GH-MATH-P5-103-REFERENCE-L2-IDENTITY-liuchuanafeng-20261004T1812Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-04T18:12:00Z
claimed_at: 2026-10-04T18:10:00Z
inspected_commit: 40113e95b8fee8e5be3519ec447af70564f67310
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/review-P5-103-REFERENCE-BINDING-PACKET-SPEC-20260914-Sartre.md
  - agent_review_inbox/review-P5-103-ACTUAL-REFERENCE-CONTEXT-BINDING-20260914-Sartre.md
task_id: GH-MATH-P5-103-REFERENCE-L2-IDENTITY
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
packet_instantiated: false
trajectory_promotion_claimed: false
proposed_integration_target: documentation
requested_action: harvest_pending_missing_reference_do_not_close_l2
---

# GH-MATH-P5-103-REFERENCE-L2-IDENTITY: subtraction contract is specified, not instantiated

## Question

At commit `40113e95b8fee8e5be3519ec447af70564f67310`, do the packet-v1 specification and the actual-reference context review establish the signed residual subtraction identity, including the Float64 defect form, for either `descriptor_reference` or `full_source_reference`?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The L2 identity is a source-facing contract only. No same-context packet supplies `qbarB`, `vbarB`, `abarB`, `lbar`, and `r` under one `referenceKey`. Descriptor mode and full-source mode remain mutually exclusive and both unfilled. This review does not promote discrete samples to an ODE.

This is not `rejected`: missing fields are not a counterexample to the identity, and the two modes are not malformed. It is not `verified` or `compiled_candidate`: no Lean, Julia, or validator was run. It is not `architecture_only`: the blocker is a missing selected reference, not a missing interface name.

Roster text still marks 流川枫 unavailable for new dispatch. This file is an inbox-only poll result and does not rewrite that roster, prior authorship, or ownership of the producer/Lean/trajectory lanes.

## Evidence inspected (read-only)

1. **Release boundary.** `task_queue.md` section `2026-09-14 — next GitHub release batch after revision 890` assigns `GH-MATH-P5-103-REFERENCE-L2-IDENTITY` to check signed residual subtraction and the Float64 defect identity in both modes, and forbids trajectory promotion. Fail-closed admission is explicit: a specification or source-independent lemma cannot enter the verified registry.

2. **L2 is defined, not witnessed.** `review-P5-103-REFERENCE-BINDING-PACKET-SPEC-20260914-Sartre.md` (blob `f546779f965c67d28110e8d0818be749a8698a9e`) fixes, for common configuration and common forcing,

```text
Mref*(aB-abarB) + D_C*y + K_C*x = -r
x = qB-qbarB,  y = vB-vbarB,  r = l-lbar
```

with ideal-real coefficients `D_C = diag(4/5,13/20)`, `K_C = [[3/4,-1/100],[-1/200,29/50]]`, `g_C = [1/5,1/10]`. It also records the defect form

```text
epsilonA = Mref*aB + D_C*vB + K_C*qB - g_C*w + l
epsilonR = Mref*abarB + D_C*vbarB + K_C*qbarB - g_C*w + lbar
epsilonS = r_export - (l-lbar)
Mref*(aB-abarB)+D_C*y+K_C*x = -r_export + epsilonS + epsilonA - epsilonR
```

The same file sets `actual_packet_instantiated: false` and says the packet, validator, and L1–L3 proofs were not created. A forcing mismatch would add `g_C*(w_actual-w_ref)` and must not be dropped. Unequal coefficients must not be cancelled. No `context.json`, `reference.json`, or `samples.jsonl` is in the inbox.

3. **Mode split stays empty.** Descriptor mode needs a selected `qbar0/vbar0`, forcing, and an explicit `lbarLaw`; `lbarLaw=0` is not a default. Full-source mode needs a full six-dimensional reference trajectory, the same `A_C`, and remote state; `qbarB/vbarB/abarB` are only the `B=(4,5)` projection. Neither mode has an instance. Pointwise tables, if they existed, would still not be trajectory evidence. L3 (`q'=v`, `v'=a` on a shared interval) is a separate gate and is not claimed here.

4. **Context review confirms the missing witness.** `review-P5-103-ACTUAL-REFERENCE-CONTEXT-BINDING-20260914-Sartre.md` (blob `f81056cf27d619a9f521d951e772aa22a1ecc067`) reports `MISSING_ACTUAL_REFERENCE_CONTEXT`. Present objects are the actual residual evaluator, actual numeric trajectories, frozen `Mref`, and nominal acceleration definitions. They do not form a paired reference. Recorded hashes, not recomputed in this poll:

```text
routeB_descriptor_residual_interface.jl D3D21705E5E904A080E4B86DC4C380788D2323C155570A8E7B40D62B11BB0A24
dhport_lib.jl AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936
routeB_Mq_M0.csv 28D98AD71D1D6C2CBE830872CAD9077F2F7B4E2D932794217EB68868FD2E2B40
```

`M0` tokens `0.116667666666667` and `0.05018475` are not interchangeable with `350003/3000000` or an unstated binary64 parse. `l2` in `routeB_traj_all.csv` is an actual squared norm, not signed `lbar`. `vbar2` in the debug nominal file is an acceleration-difference aggregate, not `vbarB`.

## Obstruction

```text
mode_descriptor_reference: MISSING selected qbar0/vbar0/lbarLaw
mode_full_source_reference: MISSING full6 reference and remote state
fields_missing: referenceKey, qbarB, vbarB, abarB, lbar, signedResidual, pairing
defect_identity: specified, not evaluated; epsilonA/epsilonR/epsilonS absent
common_forcing: not evidenced
float64_vs_exact: three interpretations of M0 remain unmixed and unbound
trajectory_promotion: not claimed
source_binding: false
```

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `GH-MATH-P5-103-REFERENCE-L2-IDENTITY` open.
- Requested action: harvest this as a pending missing-reference obstruction. Do not treat the packet specification or the actual residual exporter as an L2 source theorem. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not select a zero reference or set `lbar=0`.
- Did not upgrade discrete samples, `l2`, or `vbar2` to a trajectory or to signed force residual.
- Did not claim L1 source equality, Float64 defect bounds, or L3 promotion.
- Did not run Lean, Julia, a validator, or a regression; no exit code is claimed.
- Did not edit registry, state, task queue, roster, or formal proofs.
