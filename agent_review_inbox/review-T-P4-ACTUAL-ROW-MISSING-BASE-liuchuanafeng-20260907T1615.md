---
kind: review_result
review_id: review-T-P4-ACTUAL-ROW-MISSING-BASE-liuchuanafeng-20260907T1615
source_agent: 流川枫
created_at: 2026-09-07T16:15:00-06:00
inspected_commit: 5036a3b88c4d2e03b7dfce91649ea69aa63cc464
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_ActualRowMissingBase.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_ActualRowMissingBase.review.md
integration_status: pending
admission_label: pending
---

# T-P4-ACTUAL-ROW-MISSING-BASE — target allocation vs missing base

## Question

Does `NEW_P4_032_ActualRowMissingBase.lean` state (i) an exact target-allocation equivalence for `youngMargin`, and (ii) a fixed-coefficient opposite-base counterexample, without upgrading decimal CSV tokens to Float64/source reification or registry evidence?

## Decision

**Yes on the statement/obstruction boundary; no on compile or physical admission.**

The sidecar is explicitly `OPEN_UNCOMPILED`. Public theorems match the queue contract. There is no `sorry`/`admit` in the inspected source text. This review did **not** run Lake, so there is no exit code, `#print axioms` output, or `compiled_candidate` label.

`admission_label: pending` — inspectable uncompiled obstruction leaf, not verified kernel evidence and not a rejected false statement.

## Exact statements consumed

Namespace `RouteBP4032ActualRowMissingBase`. Blob SHA `52b8d9d04bd774e80c515738a1e074fa6b7fd26d`.

Decimal-token rationals (header forbids Float64/interval/source reading):

- `candidateGamma = 1/5`
- `candidateCharge = 15698624457194343 / 10^17`
- `printedMargin = 4301375542805658 / 10^17`
- `printedRhoSquared = 7849312228597172 / 10^17`

Theorems (names only; proofs are `norm_num` / `linarith` in source):

1. `exact_decimal_external_slack`:
   `candidateGamma - candidateCharge = 4301375542805657 / 10^17`.
2. `external_slack_positive`:
   `candidateCharge < candidateGamma`.
3. `printed_subtraction_discrepancy`:
   printed margin exceeds the exact token difference by `1/10^17`.
4. `printed_young_discrepancy`:
   `2 * printedRhoSquared - candidateCharge = 1/10^17`.
5. **Required equivalence** `target_iff_base_allocation`:
   `target ≤ youngMargin base ell metric theta charge`
   ↔ `target + (1+theta)*ell^2 + charge*metric ≤ base`.
6. Sufficient consumer `consume_base_allocation` (needs `0 ≤ metric` and `charge ≤ gamma` plus a **gamma-scale** base allocation).
7. Same-domain functional wrapper `same_domain_consumer` — domain `D`, comparison to an external `margin`, still assumes the missing base allocation pointwise.
8. `row_slack_does_not_close_full_budget`:
   slack remains positive at `(base,ell,metric,theta)=(gamma,1,1,1)`, yet
   `youngMargin = -195698624457194343 / 10^17 < 0`.
9. `row_counterexample_blocks_every_positive_target`:
   no `target > 0` satisfies the inequality on that assignment.
10. **Required opposite-base pair** `same_coefficients_opposite_target_results`:
    coefficients/ell/metric/target `1/100` fixed;
    `youngMargin gamma 1 1 1 charge` fails the target;
    `youngMargin (gamma+2) 1 1 1 charge` succeeds.
11. `zero_metric_no_positive_floor`:
    `(gamma-charge)*0` cannot support a strictly positive constant target.

Hand check of the two displayed rationals agrees with the Lean numerals; this is decimal-token arithmetic, not a replay of the CSV generator floats.

## Companion in-tree review (not a compile receipt)

`NEW_P4_032_ActualRowMissingBase.review.md` (blob SHA `fe4645962a7ac3126ed83b924e5f58a7fab9c42c`) records CSV line 9 of `routeB_compact_external_budget_ledger.csv` and local hashes that are **not** present as those files in this Git tree. Those hashes are provenance notes from an external Route-B workspace; they are not independently rehashed here.

The companion already states: no Lean/Julia/solver execution; no physical F≤L verdict; no coverage/admission.

## Missing obligations (leave open)

- Pinned Lake/Mathlib compile, exit code 0, `#print axioms`, olean hash.
- Source identity of `b_base`, `l_base`, `A_up` on a declared DH domain.
- Rounding/interval meaning of the printed tokens.
- Prescribed P4 target and uniform base allocation on that domain.
- Any registry / true-DH / flowpipe claim.

## Integration target and requested action

- Target: documentation / DAG metadata only. Keep `T-P4-ACTUAL-ROW-MISSING-BASE` open until a Lean slot produces a pinned receipt.
- Requested action: consume the iff + opposite-base pair as an **obstruction against inferring full budget from external row slack**. Do **not** edit registry, `state.json`, or formal certificates.
- Lean compile remains for `:10`/`:40` slots if a pin is attached later.

## Commands / hashes

- Inspected commit: `5036a3b88c4d2e03b7dfce91649ea69aa63cc464`
- Lean blob SHA: `52b8d9d04bd774e80c515738a1e074fa6b7fd26d`
- Companion review blob SHA: `fe4645962a7ac3126ed83b924e5f58a7fab9c42c`
- Placeholder scan (source text): no `sorry`, `admit`, or `axiom` declarations in this file.
- Lean/Lake executed: no. Exit code: n/a.

## Forbidden-boundary compliance

- Did not treat decimal-token rationals as Float64 execution or source reification.
- Did not claim descriptor-feasible states or physical Schur margin.
- Did not promote registry / state / formal proof.
- Did not close P4/P5/M4 from this sidecar.
