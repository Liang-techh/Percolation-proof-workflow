---
kind: review_result
review_id: review-T-P5-049-VARYING-CURVATURE-SHARED-R-ADMISSION-liuchuanafeng-20261009T0314Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-09T03:14:00Z
inspected_commit: f728793c0d9b7c91cf3b07ffdf1768b54ba4d92d
parent_tree_before_claim: ab10774ca47c799f51f65a512488e5479b8f8c5b
claim_id: claim-T-P5-049-VARYING-CURVATURE-SHARED-R-ADMISSION-liuchuanafeng-20261009T0312Z
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P5-049-VARYING-CURVATURE-SHARED-R-ADMISSION-liuchuanafeng-20261009T0312Z.md
  - agent_review_inbox/claim-T-P5-049-guyuefangyuan-20260907T2225.md
  - agent_review_inbox/review-T-P5-049-guyuefangyuan-20260907T2234.md
  - agent_review_inbox/companion-T-P5-049-guyuefangyuan-20260907T2238.md
  - agent_review_inbox/review-T-P5-048-RANK-ONE-AND-SHARED-R-ADMISSION-liuchuanafeng-20261009T0122Z.md
task_id: T-P5-049
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
proposed_integration_target: documentation
requested_action: harvest_pending_admission_audit_do_not_promote_T-P5-049_helly_child
---

# T-P5-049 admission audit: varying-curvature Helly child stays conditional

## Question

At the inspected commit `f728793c0d9b7c91cf3b07ffdf1768b54ba4d92d` (parent `ab10774ca47c799f51f65a512488e5479b8f8c5b`), does the published T-P5-049 completion already supply deployed `A_i/B_i/d_i` rows, a same-cell residual packet, Float64/solve semantics, absolute cell-center coverage, ODE continuation, an independently re-executed pinned Lean receipt, or registry admission?

May the exact Local + pairwise-Helly criterion, the two regression examples, or the companion statement correction be promoted?

## Decision

**No admission upgrade. Keep `admission_label: pending`.**

古月方源 closes the varying-curvature gap left by T-P5-048's homogenization bridge. For finite gates `f_i(r)=A_i+B_i r-d_i r^2` with `d_i>0` on `[0,1]`, strict shared feasibility is equivalent to every row meeting the rational `Local_i` predicate and every pair meeting `S_ij<=0 or S_ij^2<K_ij`. The argument is the square identity `4 d f(r)=Delta-(2 d r-B)^2`, three endpoint/vertex branches, one square-root cancellation for open-interval overlap, and one-dimensional finite Helly. The companion correctly rejects the Section 9 pseudo-Lean implication quantifiers; the intended statement is `exists r, 0<=r and r<=1 and f r>0`.

The review itself leaves the common-`r` architecture question, source rows, Float64, ODE, coverage, Lean, and admission open, and labels the child a pending mathematical child. This pass does not merge it with T-P5-048, does not treat homogenization failure as a true obstruction, and does not treat a Helly PASS as source coverage.

This is not `rejected`: the published identities match an independent rational replay on their stated hypotheses. It is not `architecture_only`: the review states an exact ordered-field equivalence. It is not `compiled_candidate`: no Lean sidecar for this child was in the inspected files, and none was executed here.

Prior authorship is preserved. This file does not overwrite 古月方源. The same-agent claim at `2026-10-09T03:12:00Z` is consumed; no second claim is added.

## Evidence

1. **Queue does not close the parent.** `task_queue.md` at the parent tree has no later owner or closure for `T-P5-049`. The 2026-09-14 release still says a source-independent lemma cannot enter the verified registry. The neighbouring T-P5-048 admission audit already left both of its children pending.
2. **Math review is conditional.** `review-T-P5-049-guyuefangyuan-20260907T2234.md` blob `adc70b61c9b09d2ae61dec9641cc52df503fd6c7` states theorem `finite_varying_curvature_shared_r_iff`, predicates (0.6) and (0.7), the positive regression whose unpivoted `D=max d_i` minorant has discriminant `-536/25`, and the negative pair with `S=92/25` and `S^2=8464/625>64/625=K`. Section 10 leaves source values, Float64, ODE, coverage, Lean, provenance, and admission explicit. Its `admission_label` is `pending`.
3. **Companion corrects the statement, not the admission.** `companion-T-P5-049-guyuefangyuan-20260907T2238.md` blob `bbea7f7a7bfafe11b8df22fb3a60a5d05b3032a6` keeps the child pending and replaces the pseudo-code implication quantifiers with a conjunction. Claim blob `fb1319b416528c86436b3697cf0ddbb42c4a0423` forbids touching T-P5-048 Lean, rank-one, source receipts, provenance, coverage, or admission.
4. **No Lean receipt to re-execute.** The inspected T-P5-049 files contain a suggested theorem split only. This pass did not compile, did not print axioms, and did not create a sidecar.
5. **Local rational checks only.** Python `fractions` reproduced the published identities:

```text
positive: Delta1=4/25, Delta2=4, C=0, S=-20<=0, so the pair predicate passes.
at r=4/5, f1=1/25 and f2=1/10; 4*d1*f1 equals Delta1-(2*d1*r-B1)^2.
unpivoted D=10 minorant of row 1 has discriminant -536/25<0.
negative: both Local predicates pass; Delta1=1/25, Delta2=4/25, C=-2, S=92/25, K=64/625, S^2=8464/625>K, so the pair predicate fails.
intervals (3/20,7/20) and (13/20,17/20) are disjoint.
```

These checks do not instantiate a source block. `r` remains a proof-design parameter, not a source coordinate. The replay does not re-prove the finite Helly completeness direction beyond the published examples.

## Receipt

```text
command: local fractions replay only; repo checker not run
exit_code: 0 for the local replay; not a workflow checker
axiom_print: not executed
placeholder_scan: not a kernel scan
math_review_blob: adc70b61c9b09d2ae61dec9641cc52df503fd6c7
companion_blob: bbea7f7a7bfafe11b8df22fb3a60a5d05b3032a6
claim_blob: fb1319b416528c86436b3697cf0ddbb42c4a0423
lean_receipt: absent
positive_pair_predicate: pass on the published example
unpivoted_homogenization_false_negative: true on that example
negative_pair_obstruction: true on the published example
statement_quantifier_correction: companion only; original review not rewritten
deployed_ABd_rows: not exhibited
same_cell_residual_packet: not exhibited
float64_semantics: not exhibited
cell_center_inclusion: not exhibited
ode_continuation: not exhibited
fresh_lean_receipt: not exhibited
common_r_architecture_question: unresolved
```

## Obstruction

```text
identity_surface: varying-curvature shared strict feasibility is a rational Local plus pairwise overlap test
coefficient_surface: A_i, B_i, and d_i are hypotheses; the 4/25, -536/25, and 92/25 figures are regression data, not a source witness
architecture_gap: whether the bundled certificate must freeze one r is not decided; a Helly PASS does not answer it
frontend_gap: no deployed row of (A_i,B_i,d_i) is bound
budget_gap: a PASS of the pair predicate is not certified on any actual residual cell
interval_gap: a FAIL obstructs only this separated envelope; it does not prove the true pointwise block fails
consumer_gap: T-P5-046, T-P5-047, and T-P5-048 remain pending; a PASS here does not close them
formal_gap: the suggested Lean split is not a receipt; the original Section 9 quantifiers are not kernel text
coverage_gap: a positive abstract margin does not place an absolute cell center in a source box
calculus_gap: FTOC, first-exit on the actual pair, and ODE continuation are not proved
obstruction_scope: missing source rows, Float64 semantics, center trajectory, flowpipe, shared-r architecture decision, and an independent pinned receipt remain failure boundaries
missing_for_parent_close:
  an explicit architecture decision that one common r is required, if this child is consumed
  one same-cell signed enclosure of every consumed (A_i,B_i,d_i) row
  an independently certified V<=Vstar sublevel and absolute source-domain inclusion
  a first-exit / ODE existence-continuation theorem on the actual pair
  an independent pinned Lean receipt of the corrected conjunction statement
forbidden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar creation
  promotion of the Helly child, the regression witnesses, or the companion correction
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
