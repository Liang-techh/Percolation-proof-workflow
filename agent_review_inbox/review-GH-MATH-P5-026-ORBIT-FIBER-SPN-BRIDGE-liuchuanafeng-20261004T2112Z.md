---
kind: review_result
review_id: review-GH-MATH-P5-026-ORBIT-FIBER-SPN-BRIDGE-liuchuanafeng-20261004T2112Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-04T21:12:00Z
claimed_at: 2026-10-04T21:11:00Z
inspected_commit: 850ce7208495aafd5acf541f0ed02a6911eb6392
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/review-T-P5-026-CONE-INDEX-ORBIT-FIBER-20260914T211830Z.md
  - agent_review_inbox/review-T-P5-026-ORBITFIBER-SPN-DAG-20260914T212915Z.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_CONE_INDEX_SPNBridge20260914.lean
task_id: GH-MATH-P5-026-ORBIT-FIBER-SPN-BRIDGE
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
lean_rerun: false
hrep_instantiated: false
spn_witnesses_present: false
proposed_integration_target: documentation
requested_action: harvest_pending_interface_audit_do_not_promote_compiled_candidate
---

# GH-MATH-P5-026-ORBIT-FIBER-SPN-BRIDGE: shortest interface is typed, not admitted

## Question

At commit `850ce7208495aafd5acf541f0ed02a6911eb6392`, what is the shortest interface from the OrbitFiber cardinality lemma to an 18-representative SPN certificate, and does that interface already separate the origin guard from weighted invariance?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The interface is already written as a source-independent typed candidate. This poll does not rerun Lean, so it does not reconfirm the historical `compiled_candidate` execution and does not promote it.

The shortest main path does not use the cardinality lemma. It is signed gap, then the 18-SPN consumer, then component power. OrbitFiber's multiplicity formula is only an optional weighted-audit branch. The origin guard and weighted invariance remain separate.

## Evidence inspected (read-only)

1. **Release boundary.** `task_queue.md` section `2026-09-14 — next GitHub release batch after revision 890` assigns `GH-MATH-P5-026-ORBIT-FIBER-SPN-BRIDGE` to study the shortest interface between the OrbitFiber cardinality lemma and the 18 representative SPN certificate, distinguishing the origin guard from weighted invariance. Compiled candidates cannot enter the verified registry.

2. **No prior claim for this task id.** Inbox names for `GH-MATH-P5-026-ORBIT-FIBER-SPN-BRIDGE` are only this claim and this review. Older `T-P5-026` claims and reviews are different task ids and are not rewritten.

3. **Cardinality lemma is not the SPN premise.** `review-T-P5-026-CONE-INDEX-ORBIT-FIBER-20260914T211830Z.md` records `exact_multiplicity_formula`: label multiplicity is `2*card(R_z)` at `z=0` and `card(R_z)` otherwise, with `card(R_0)=18` and 36 covering labels at the origin. It explicitly does not drop orientation from weighted witnesses and does not make membership flip-invariant.

4. **Current bridge matches that split.** Git blob `6e9c86ea130803ab653e09b535ca50b18de40a5e` of `NEW_CONE_INDEX_SPNBridge20260914.lean` still declares:
   - `eighteen_spn_envelope`: 18 matrices `H/S/N` on `Representative`, both orientations via `expand (r,b)`, premise `hgap`, then `global_abs_envelope_of_spn`. No `z≠0` hypothesis and no multiplicity factor.
   - `signed_gap_of_even`: reuses the same nonnegative `u` only through scalar evenness, not through unique orientation.
   - `signed_gap_origin`: `G(0)=0` from the gap contract at `u=0`, not from the count 18.
   - `weighted_gap_factor` / `envelope_iff_weighted_nonneg`: optional lane; consumes `exact_multiplicity_formula`; counts alone do not prove positivity.
   - `residual_power_of_envelope`: residual row envelope stays an explicit premise.

5. **Historical execution is not this poll's receipt.** `review-T-P5-026-ORBITFIBER-SPN-DAG-20260914T212915Z.md` reports a local stdin bundle pass at commit `e5f3f7ec984511e5eec1fc17ff9cb17a652e00ec`, Lean/checker exit 0, and source SHA-256 `da9eba42c611d31e019dbdf4a1f4d06bb7d4e82c5cbdf9c138d98f3278dae10a` for the bridge file. This poll did not recompute that hash or rerun the checker. Standalone import, Lake, cached Mathlib authentication, physical hrep, and 18 SPN witnesses were already absent there.

## Interface split

```text
shortest_main_path: signed_gap -> eighteen_spn_envelope -> residual_power_of_envelope
optional_branch: OrbitFiber exact_multiplicity_formula -> weighted_gap_factor -> envelope_iff_weighted_nonneg
origin_guard: z=0 has 18 orbits and 36 labels; factor 2 is bookkeeping, not a doubling of mu
nonzero_guard: one covering orientation per covering orbit; boundary orbits may still overlap
weighted_invariance: not implied by unique orientation; W(flip c,u) needs an explicit transport identity
missing_leaf: typed hrep for frozen L, P/Q, representative charts, and constructed H
missing_source: K_path, same-domain component envelopes, 18 SPN witnesses
```

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `GH-MATH-P5-026-ORBIT-FIBER-SPN-BRIDGE` open.
- Requested action: harvest this as a pending interface audit. Do not treat the historical local exit 0 as a new admission receipt. Do not close P5. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not compile, repair, or rerun Lean/checker; no new exit code is claimed.
- Did not supply `hrep`, representative `H/S/N`, or a concrete gain.
- Did not identify weighted values across orientations or erase the origin factor 2.
- Did not edit registry, state, task queue, roster, or formal proofs.
- Roster text still marks 流川枫 unavailable for new dispatch. This file is an inbox-only poll result and does not rewrite that roster or prior authorship.
