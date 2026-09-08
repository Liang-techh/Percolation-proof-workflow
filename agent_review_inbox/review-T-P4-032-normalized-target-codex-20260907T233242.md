---
kind: review_result
review_id: review-T-P4-032-normalized-target-codex-20260907T233242
task_id: T-P4-032
agent: Codex-P4-math-lane
source_agent: Codex-P4-math-lane
created_at: 2026-09-07T23:32:42-06:00
inspected_commit: 138c90d84546f2037eb2fae8e71023033e383c1e
inspected_paths:
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_ExactCellLambdaConsumer.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_SameSourceConsumerPacket.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_NormalizedTargetGuard.lean
related_tasks:
  - T-P4-039
  - T-P4-040
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
final_integration: false
proposed_integration_target: P4.same_source_normalized_prescribed_target
requested_action: retain the normalization audit and typed target-transfer contract as pending mathematical evidence; require independent elaboration and source equalities before consuming it; do not promote registry status
---

# P4 normalization: common rational s guarantees nu*t

The inspected `source_floor_to_P4` has the correct mathematical direction under its stated premises. It takes the source floor `t≤b_base-q`, q being the TOTAL squared generalized-force residual, and uses at the same state:

`nominal=nu*b_base`, `gain*beta=nu`, `nominal-gain*(beta*q)≤margin`, `nu>0`.

Reassociation produces exactly `nu*(b_base-q)≤margin`, hence **nu*t≤margin**, with nu*t>0. The common rational s determines a valid Young allocation; it neither determines nu nor cancels beta. No concrete source equality or new Lean compilation is claimed by this audit.

## Minimal typed target transfer

New artifact: `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_NormalizedTargetGuard.lean`.

`TargetTransfer nu sourceTarget requestedTarget` stores `requestedTarget>0` and `requestedTarget≤nu*sourceTarget`. `common_guard_requested_target` connects the actual rational guard/source-floor theorem to the actual P4 normalization theorem, then consumes this transfer. It does not construct a fixed-theta=1 Allocation or infer an unscaled old target.

`universal_floor_transfer_iff` proves the sharp information boundary:

`(for every margin≥floor, target≤margin) iff target≤floor`.

Consequently, when only nu*t is known, a separately requested positive T requires `T≤nu*t`. For t>0, preserving the same numerical target in the fixed P4 output units is justified from this floor alone **iff nu≥1** (`old_target_fits_iff`). Equality nu=1 is sufficient but not necessary. If the actual margin is known to be larger, that additional evidence can support other targets; the floor-only criterion does not claim otherwise.

## Directions and indispensable conditions

- Exact adapter: residual must be the same q, nominal must equal nu*b_base, and the PRODUCT gain*beta must equal nu. Gain=nu alone does not suffice. Coordinate/norm conversions cannot be hidden inside a scalar label.
- A sound one-sided alternative is `nu*b_base≤nominal`, `gain*beta≤nu`, q≥0, and the same LOWER margin comparison. `conservative_normalization` proves this sufficient scalar version. P4's independent nonnegative gain/beta contracts remain intact; this scalar lemma does not construct or relax them.
- For the one-sided version, nominal is bounded BELOW, while the residual multiplier product is bounded ABOVE. An upper bound `nominal≤nu*b_base` cannot replace the lower bound. Exact equalities are the current adapter contract, not logically necessary for every conservative adapter.
- nu≥0 suffices for a non-strict scalar inequality. To inherit strict positivity from t>0 through normalization, nu>0 is needed. A zero normalization would leave a zero guaranteed target.
- Alpha and the front factor are not premises of the direct scalar route. If a caller substitutes the front expression for nominal/base, it must supply `offset+alpha*(mu*frontEnergy(front))=nu*b_base` (or a separately proved correctly directed replacement), together with the residual-product condition. No alpha=beta or alpha=nu identity follows from the front decomposition.
- The optional `FrontFactorization` proves only the body-expression equality. It does not prove RemainderMargin, PSD, source composition, domain coverage, or any physical storage inequality. Those prerequisites remain necessary for a claim that uses that separate front route.

## Exact factor counterexamples

All examples are rational scalar assignments demonstrating invalid implications, not claimed physical source states.

1. **Normalization swallowed:** b=2,q=1,t=1,nu=1/2 and exact matching nominal/product yield margin=1/2. The promised nu*t=1/2 holds; the old t=1 fails.
2. **Beta swallowed:** b=2,q=1,t=1,nu=gain=1,beta=3,nominal=2 and margin=−1. The source floor holds but t fails because gain*beta=3, not nu.
3. **Front factor mistaken for residual factor:** alpha=nu=1/2,b=2,q=1,t=1 gives front/nominal=1, but gain=beta=1 yields margin=0. The claimed alpha*t=1/2 fails even though the base side has the chosen front factor.
4. **Nominal direction reversed:** b=2,q=1,t=1,nu=gain=beta=1,nominal=0. The nominal upper bound 0≤2 holds, yet margin=−1 cannot support target=1.

The four `*_counterexample`/direction declarations in the new artifact encode these exact failures. They show why factor deletion or a reversed inequality cannot be repaired by a passing rational lambda guard.

## Evidence and verification boundary

- Read `source_floor_to_P4` at ExactCellLambdaConsumer lines 136–150 and `P4Binding`/`FrontFactorization` at SameSourceConsumerPacket lines 151–158 and 183–186 directly. The proof above is a manual algebra/interface review.
- PowerShell text scan of the new Lean artifact: 0 proof placeholders and 0 trailing-whitespace lines; command exit code 0. Hash collection also returned exit code 0.
- No Lean/Lake, local verifier, solver, simulation, wide regression or registry action was performed. The inspected commit anchors the checkout; the new file hash anchors the actual added artifact. All new declarations remain OPEN_UNCOMPILED.

| File | SHA-256 |
|---|---|
| `NEW_P4_032_NormalizedTargetGuard.lean` | `2ef0bcc07df168b5f0c8c65db4026dd6c66df09591ee648c252b9b3695c232a4` |
| `NEW_P4_032_ExactCellLambdaConsumer.lean` | `b4f99ab8b9ced4dfb09fdc5ab1344ac8b7271363ed3af7e06bf2f696da5b8122` |
| `NEW_P4_032_SameSourceConsumerPacket.lean` | `8c49603aa1c2193a5440026474d8ddc4b90e3a308c7c32ac862ace7b8c1a160e` |

Disposition: **pending/open**. The next source obligation remains the correctly normalized same-state equations and real DH scalar inequalities; no factor may be inferred from a similarly named row field.
