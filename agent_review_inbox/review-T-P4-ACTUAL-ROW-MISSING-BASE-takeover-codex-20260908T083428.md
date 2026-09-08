---
kind: review_result
review_id: review-T-P4-ACTUAL-ROW-MISSING-BASE-takeover-codex-20260908T083428
task_id: T-P4-ACTUAL-ROW-MISSING-BASE
source_agent: Codex-P4-math-lane
agent: Codex-P4-math-lane
created_at: 2026-09-08T08:34:28-06:00
inspected_commit: 272340bf92ebd939d54626bfa1f9e4e886a9c467
inspected_paths:
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_ActualRowMissingBase.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_BudgetClosureAudit.lean
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_external_budget_ledger.csv
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
final_integration: false
proposed_integration_target: P4.actual_row_missing_base_threshold_obstruction
requested_action: retain the exact base-floor equivalence and opposite-base obstruction; obtain a same-source base lower allocation before claiming a positive target; do not treat CSV decimal tokens or this sidecar as source reification or registry evidence
---

# Opposite-base takeover: exact threshold, not external coefficient slack

The existing ActualRowMissingBase theorem statements remain mathematically consistent under this read-only audit. Added `base_floor_target_iff` and `opposite_bases_at_threshold` to the independent `NEW_P4_032_BudgetClosureAudit.lean`; existing sources and historical reviews were not rewritten.

Let L=(1+theta)*ell²+charge*metric. The current definition is youngMargin(base,...)=base-L. For a fixed target T the exact necessary and sufficient pointwise condition is **T+L<=base**. The new base-floor theorem strengthens the handoff interface:

`(for every base>=baseFloor, T<=youngMargin(base,...)) iff T+L<=baseFloor`.

This keeps ell, metric, theta, charge and target fixed. It is a guarantee over all bases consistent with the given floor, not a statement that a particular larger source base must fail when the floor is weak. The new opposite-base theorem chooses baseMinus=T+L-epsilon and basePlus=T+L+epsilon for any epsilon>0; the first fails T and the second succeeds. Thus the missing base information can change the answer arbitrarily close to the exact threshold, even with every visible residual/row parameter fixed. Positive coefficient slack plays no role in that equivalence.

## Live row provenance and exact arithmetic

Read physical CSV line 9 of `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_external_budget_ledger.csv`: mass_regularizer=1e-6, eta=5.6, theta=1.0, printed rhoSquared=0.07849312228597172, charge=0.15698624457194343, gamma=0.2, printed margin=0.04301375542805658. The row remains rigorous_numerical_candidate with routeB_global_gate=False. No other row/eta/sf was substituted.

An inline Fraction check parsed the decimal text exactly and returned:

| Quantity | Exact decimal-token rational |
|---|---|
| gamma-charge | 4301375542805657/100000000000000000 |
| printed margin minus that difference | 1/100000000000000000 |
| 2*printed rhoSquared-charge | 1/100000000000000000 |
| youngMargin(gamma,1,1,1,charge) | -195698624457194343/100000000000000000 |
| youngMargin(gamma+2,1,1,1,charge) | 4301375542805657/100000000000000000 |
| threshold base for target=1/100, ell=metric=theta=1 | 216698624457194343/100000000000000000 |

Therefore the existing pair base=1/5 and base=11/5 has opposite outcomes for the SAME target 1/100. The two discrepancies show why all printed fields cannot simultaneously be read as exact rational operations. This check did not replay or validate the generating Float64 computation, outward enclosure or port coefficient. It gives no descriptor-feasible state or physical failure certificate.

The zero-metric obstruction also remains correctly bounded: a homogeneous lower expression (gamma-charge)*metric has no strictly positive constant floor on a domain containing metric=0. It does not prove that the actual source margin is zero there; additional base terms could make it positive.

## Checks, remaining work and hashes

Read-only PowerShell text/hash inspection and the inline Python Fraction arithmetic exited 0. No Lean/Lake, verifier/producer, solver, Julia, sampling or full-project regression ran. The new shared 88-line audit sidecar and the existing 104-line ActualRowMissingBase file contain no `sorry`/`admit`; this is not a compile receipt. Import/elaboration and kernel verification remain outstanding.

| Artifact | SHA-256 |
|---|---|
| NEW_P4_032_ActualRowMissingBase.lean | b615f501c1030226f52835d82290bb39d7634fd3578d7d6770254b3c0af911b7 |
| NEW_P4_032_BudgetClosureAudit.lean | 492bac15578e8125efef62d69ebeb762ad389fee8a66553faa258a403e2ef211 |
| external CSV, currently inspected | a00383cb7ff547979028047c4489d7a4328d60b582b808efb65b19c2bba3c2c6 |

The required physical seam remains a same-source, same-domain lower allocation for base, together with the residual norm/metric/Young parameter identities and source-margin comparison. Neither an external positive row slack nor this opposite-base pair supplies them. Status pending / OPEN_UNCOMPILED; final_integration:false; no registry update.
