---
kind: review_result
review_id: review-T-P5-049-VARYING-CURVATURE-HELLY-ADMISSION-liuchuanafeng-20261009T0314Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-09T03:14:00Z
inspected_commit: 099959bc971ebc357f012b1e1c2f3faf12d7180a
parent_tree_before_claim: ab10774ca47c799f51f65a512488e5479b8f8c5b
claim_id: claim-T-P5-049-VARYING-CURVATURE-HELLY-ADMISSION-liuchuanafeng-20261009T0312Z
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P5-049-VARYING-CURVATURE-HELLY-ADMISSION-liuchuanafeng-20261009T0312Z.md
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

# T-P5-049 admission audit: varying-curvature Helly stays conditional

## Question

At inspected commit `099959bc971ebc357f012b1e1c2f3faf12d7180a` (parent `ab10774ca47c799f51f65a512488e5479b8f8c5b`), does the published T-P5-049 child already supply a deployed signed Jacobian exporter, a same-cell `A_i/B_i/d_i` packet, Float64/solve semantics, absolute cell-center coverage, ODE continuation, an independently re-executed pinned Lean receipt, or registry admission?

May the root-free Local/pairwise criterion, the one-dimensional Helly step, the rational-witness corollary, or the two regression examples be promoted?

## Decision

**No admission upgrade. Keep `admission_label: pending`.**

古月方源 answers the varying-curvature gap left by the shared-`r` child of T-P5-048. For `f_i(r)=A_i+B_i r-d_i r^2` with `d_i>0` and `r` in `[0,1]`, strict shared feasibility is equivalent to every row meeting the root-free `Local_i` predicate and every pair meeting `S_ij<=0 or S_ij^2 < K_ij`. The argument is one-dimensional finite Helly on the open positivity intervals together with `[0,1]`. The companion correctly repairs the Section 9 pseudo-Lean quantifiers to `exists r, 0<=r and r<=1 and f r>0`; the original review is left immutable.

This is not `rejected`: the square identity and both published regressions match an independent rational replay. It is not `architecture_only`: the review states an exact ordered-field decision interface. It is not reclassified as `compiled_candidate`: no Lean file or pinned receipt was exhibited, and this pass did not compile.

The criterion remains a proof-design interface. It does not decide whether the P5 package must freeze one common `r`, and it does not instantiate any source row. An unpivoted common-curvature minorant failure is not a true obstruction of the original family; the review already says that. Prior authorship is preserved. This file does not overwrite 古月方源. The same-agent claim at `2026-10-09T03:12:00Z` is consumed.

## Evidence

1. **Queue does not close the parent.** `task_queue.md` at the parent tree has no later owner or closure for `T-P5-049`. The 2026-09-14 release still says a source-independent lemma cannot enter the verified registry. The T-P5-048 admission audit left the shared-`r` architecture question unresolved and did not consume this child.
2. **Math review is conditional.** `review-T-P5-049-guyuefangyuan-20260907T2234.md` blob `adc70b61c9b09d2ae61dec9641cc52df503fd6c7` states theorem `finite_varying_curvature_shared_r_iff`, identity `4 d f(r)=Delta-(2 d r-B)^2`, the three local branches, and the pair predicate `S<=0 or S^2<4 d_i^2 d_j^2 Delta_i Delta_j`. Section 10 leaves common-`r` architecture, source values, Float64, coverage, ODE, Lean, provenance, and admission open. Its `admission_label` is `pending`.
3. **Companion is a statement correction, not a receipt.** `companion-T-P5-049-guyuefangyuan-20260907T2238.md` blob `bbea7f7a7bfafe11b8df22fb3a60a5d05b3032a6` repeats the pending boundary and corrects the local-theorem quantifiers. It is not a kernel receipt.
4. **Local rational checks only.** Python `fractions` reproduced the published examples:

```text
positive family: Delta1=4/25, Delta2=4, C=0, S=-20 <= 0, so the pair predicate passes.
unpivoted D=10 minorant of row 1 has discriminant -536/25 < 0.
negative family: Delta1=1/25, Delta2=4/25, C=-2, S=92/25, S^2=8464/625 > K=64/625, so the pair predicate fails.
square identity holds on the negative-family coefficients at r=4/5: both sides -117/100.
```

These checks do not instantiate a source block. `r` remains a proof-design parameter. The replay does not formalize finite Helly or the rational-witness extraction.

## Receipt

```text
command: local fractions replay only; repo checker not run
exit_code: 0 for the local replay; not a workflow checker
axiom_print: not executed
placeholder_scan: not a kernel scan
math_review_blob: adc70b61c9b09d2ae61dec9641cc52df503fd6c7
claim_blob: fb1319b416528c86436b3697cf0ddbb42c4a0423
companion_blob: bbea7f7a7bfafe11b8df22fb3a60a5d05b3032a6
historical_review_commit: 23bfff2bf59d479a3b8acfa0f87edaba0a6052f5
positive_pair_S: -20
unpivoted_minorant_discriminant: -536/25
negative_pair_S2_vs_K: 8464/625 > 64/625
deployed_signed_exporter: not exhibited
same_cell_ABd_packet: not exhibited
float64_semantics: not exhibited
cell_center_inclusion: not exhibited
ode_continuation: not exhibited
fresh_lean_receipt: not exhibited
finite_helly_formalized: false
common_r_architecture: unresolved
```

## Obstruction

```text
identity_surface: strict shared feasibility of finitely many positive-curvature quadratic gates on [0,1] is a root-free Local-plus-pairwise predicate
coefficient_surface: A_i, B_i, and d_i are hypotheses, not a source witness
architecture_gap: whether the bundled certificate must freeze one r is not decided; this child does not close that T-P5-048 question
frontend_gap: no same-cell signed enclosure of the gate coefficients is exhibited
budget_gap: a PASS of the Helly predicate is not certified on any actual residual cell
interval_gap: a FAIL obstructs only this separated shared-r envelope; it does not prove the true pointwise block fails
consumer_gap: T-P5-046, T-P5-047, and T-P5-048 remain pending; a PASS here does not close them
formal_gap: no Lean sidecar was present; finite Helly and rational extraction are unformalized; the companion quantifier repair is not a kernel statement
coverage_gap: a positive abstract margin does not place an absolute cell center in a source box
calculus_gap: FTOC, first-exit on the actual pair, and ODE continuation are not proved
obstruction_scope: missing signed Jacobian exporter, same-cell coefficient packet, Float64 semantics, center trajectory, flowpipe, shared-r architecture decision, and an independent pinned receipt remain failure boundaries
missing_for_parent_close:
  an explicit architecture decision that one common r is required, if this child is consumed
  one same-cell signed enclosure of every consumed (A_i,B_i,d_i) in the V' force coordinates
  an independently certified V<=Vstar sublevel and absolute source-domain inclusion
  a first-exit / ODE existence-continuation theorem on the actual pair
  an independent pinned Lean receipt for the square identity, local branches, pair predicate, and finite Helly step
forbidden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar creation
  promotion of the Helly criterion, the regression witnesses, or the companion correction
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
