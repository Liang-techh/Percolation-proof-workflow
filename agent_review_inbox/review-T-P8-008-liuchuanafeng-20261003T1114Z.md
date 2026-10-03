---
kind: review_result
review_id: review-T-P8-008-liuchuanafeng-20261003T1114Z
source_agent: 流川枫
created_at: 2026-10-03T11:14:00Z
inspected_commit: 504e79ca8d01fa3870ad12966c95455a632f46ed
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/review-T-P8-008-guyuefangyuan-20260907T0231.md
  - agent_review_inbox/review-T-P8-008-sumengchen-20260907T0333.md
  - examples/routeb_p8_contract_adapter/P8ContractAdapter.lean
  - examples/routeb_p8_contract_adapter/verify.sh
  - docs/routeb-p8-flowpipe-binding-next.md
task_id: T-P8-008
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-P8-008 audit: first-12 projection is stated only as an adapter, not as source equality

## Question

At commit `504e79ca8d01fa3870ad12966c95455a632f46ed`, does the current P8 contract adapter formulate the exact first-12 trajectory projection that combines source mechanical outputs with the adapter ramp tail `w=c0*t, c=c0`, while keeping the 13th source derivative `du[13]=0` explicit? Can that projection be admitted as a 13-state source trajectory or as P8 reachability?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The adapter states a conditional 14-state repair and an explicit obstruction for the literal zero-tail lift. It does not yet contain the first-12-on-ramp algebraic lemmas recommended by the earlier mathematical review, and it does not bind Julia `full_rhs!`. This pass did not run Lean, so the file is not a `compiled_candidate`. It is not `verified`. It is not `rejected`: the queue contract is still the right child. It is not `architecture_only`: the mismatch is pinned to `du[13]=0` versus `w'=c`.

Prior reviews are left intact. `review-T-P8-008-guyuefangyuan-20260907T0231.md` already gave the source-independent identities. This pass only checks whether those identities are now present in the adapter at the current commit.

## Evidence inspected (read-only)

1. **Queue contract is still open.** `task_queue.md` lists `T-P8-008` as `open`. Required object: the exact first-12 projection combining source mechanical outputs with adapter ramp `w=c0*t, c=c0`, keeping `du[13]=0` explicit. Forbidden: identifying the 13-state source with the 14-state ramp ODE, claiming existence/coverage, or changing the target theorem silently.

2. **Blobs at this commit.**
   - `examples/routeb_p8_contract_adapter/P8ContractAdapter.lean` blob `11c8e23a52128e56b65a76024285c45a9070414d` (same blob cited by the 2026-09-07 mathematical review)
   - `examples/routeb_p8_contract_adapter/verify.sh` blob `863b96391d30b12813c8e0d6c5ecfd8671aeddd9`
   - `docs/routeb-p8-flowpipe-binding-next.md` blob `c3d9dbf3aa7d1e9fdf4f0583f83c47fcdde83ae0`

3. **Literal source tail is kept distinct from the ramp repair.**
   - `zeroTailLift` copies slots `0..11` from a 13-state field and writes slots 12 and 13 as `0`.
   - `zeroTailLift_w` and `zeroTailLift_c` conclude those slots are `0`.
   - `zeroTailLift_not_ramp` states `¬ RampRhsPremise (zeroTailLift G)` by taking a state with `cSlot = 1` and all other coordinates `0`.
   - `timeLift` copies slots `0..11` from a time-indexed 13-state field, sets slot 12 to `z cSlot`, and sets slot 13 to `0`.
   - `timeLift_rampPremise` and `timeLift_is_conditional` state only `F z wSlot = z cSlot` and `F z cSlot = 0`.
   - The module docstring says no source binding, interval receipt, ODE existence, or true-DH claim is made.

4. **The requested first-12 projection is not yet a theorem in this file.** There is no `pack13`, `explicitMechanical`, `forgetTail_rampLift`, `timeLift_first12_on_ramp`, or `repair13_eq_source_iff_c_zero`. The file therefore does not yet prove `proj12(timeLift (S) (rampLift m c t)) = sourceMechanical S (pack13 m (c*t))`. That identity remains a review-side formula, not a checked Lean statement.

5. **Documented source mismatch is unchanged.** `docs/routeb-p8-flowpipe-binding-next.md` records the external probe as 13-state `full_rhs!` with `du[13]=0`, no `c=u[14]`, and ReachabilityAnalysis `dim:13`. The natural lift `F14[12]=0` fails `RampRhsPremise` at `c=1`. Only the degenerate `c=0` subfamily avoids the contradiction. Recorded hashes there are probe `12292f8841ef79cfa58d07facbec4ca739e27346b11b6ec57e290638b7d8b93a` and `dhport_lib.jl` `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`. This pass did not re-hash external files.

6. **Proof-token note, not a compile receipt.** `zeroTailLift_not_ramp` simplifies with the token `full_rhs!`, which is not defined in `P8ContractAdapter.lean`. Whether that name is supplied by `RouteBP8PicardStep` was not checked by a compiler. No exit code is claimed. `verify.sh` was not executed.

7. **Placeholder scan of the inspected adapter text.** No `sorry` or `admit` token appears. `#print axioms` lines are present for `zeroTailLift_not_ramp` and `timeLift_rampPremise`, but their axiom lists were not captured from a compiler log.

## Obstruction

```text
source_tail: du[13] = 0 on the documented 13-state full_rhs!
adapter_tail: timeLift sets w' = c and c' = 0
zero_lift: zeroTailLift writes w' = 0 and is stated not to meet RampRhsPremise
missing_theorem: first-12 equality on rampLift(m,c,t) with w = c*t
missing: pinned lake env lean exit and #print axioms
missing: Julia mechanical-output binding for slots 0..11
source_binding: not claimed
```

## Assumptions still required

- a pinned receipt for `zeroTailLift_not_ramp` and `timeLift_rampPremise` on the declared toolchain;
- the four algebraic lemmas from the 2026-09-07 mathematical review, especially `timeLift_first12_on_ramp`;
- a source proof that slots `0..11` of `full_rhs!` equal the mechanical projection at `(q,dq,w=c*t)`, with `du[13]=0` kept as a separate fact;
- ODE existence, interval enclosure, and `[0,1]` coverage before any parent promotion.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P8-008` open.
- Requested action: next formalization owner should add the first-12-on-ramp lemmas without rewriting `zeroTailLift` into a source ramp. Do not treat `timeLift_rampPremise` as source equality. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not identify the 13-state source with the 14-state ramp ODE.
- Did not claim existence, coverage, or flowpipe closure.
- Did not change the target theorem or any Lean file.
- Did not run a whole-project regression or this sidecar checker; no exit code is claimed.
- Did not edit registry, state, task queue, or formal proofs.
