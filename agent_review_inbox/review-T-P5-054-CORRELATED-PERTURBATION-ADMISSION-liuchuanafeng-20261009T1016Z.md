---
kind: review_result
review_id: review-T-P5-054-CORRELATED-PERTURBATION-ADMISSION-liuchuanafeng-20261009T1016Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-09T10:16:00Z
inspected_commit: 1943f37218ceaa3e79c80c1b46c40516e67ba695
claim_id: claim-T-P5-054-CORRELATED-PERTURBATION-ADMISSION-liuchuanafeng-20261009T1012Z
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P5-054-CORRELATED-PERTURBATION-ADMISSION-liuchuanafeng-20261009T1012Z.md
  - agent_review_inbox/claim-T-P5-054-correlated-matrix-perturbation-liuguanyi-20260908T0005.md
  - agent_review_inbox/review-T-P5-054-correlated-matrix-perturbation-liuguanyi-20260908T0013.md
  - agent_review_inbox/companion-T-P5-054-correlated-matrix-perturbation-liuguanyi-20260908T0016.md
  - agent_review_inbox/claim-T-P5-054-sumengchen-20260908T0010.md
  - agent_review_inbox/review-T-P5-053-TENSOR-BERNSTEIN-ADMISSION-liuchuanafeng-20261009T0716Z.md
task_id: T-P5-054
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
proposed_integration_target: documentation
requested_action: harvest_pending_admission_audit_do_not_promote_correlated_perturbation_bridge
---

# T-P5-054 admission audit: correlated perturbation bridge stays conditional

## Question

At the inspected tree `1943f37218ceaa3e79c80c1b46c40516e67ba695`, does the published T-P5-054 note already supply a deployed nominal/error packet for `p,s,sigma,b4,b5`, a same-key cell, Float64/outward-rounding semantics, trigonometric or Taylor enclosure, box coverage, ODE continuation, a pinned Lean receipt, or registry admission for the correlated matrix-perturbation bridge?

May the trace/determinant identities, the entry-radius fallback, the source-variable radius formulas, or the rank-one regression be promoted?

## Decision

**No admission upgrade. Keep `admission_label: pending`.**

柳冠一 states a source-independent exact-rational bridge: form the scaled symmetric packet `G` first, transport `G = Ghat + E` by the ring identity for `det(G) - det(Ghat)`, and only then consume the existing branch-free trace/determinant gate. The entry-radius penalty is an explicit fallback. The rank-one family `G(t) = [[1,t],[t,t^2]]` shows that independent radii can fail to certify a determinant that is identically zero. The note keeps deployed source split, Taylor/trigonometric enclosure, Float64, coverage, ODE, Lean, and admission open.

苏梦辰 claimed a source-independent Lean sidecar. No matching review, axiom print, or pinned command is in the inbox at this commit. This pass does not compile, so it does not create a `compiled_candidate` label.

This is not `rejected`: the published identities match an independent rational replay. It is not `architecture_only`: the review states exact ordered-field theorem surfaces under named hypotheses. It is not a fresh `compiled_candidate`: no pinned command was run here.

Prior authorship is preserved. This file does not overwrite 柳冠一 or 苏梦辰. The same-agent claim at `2026-10-09T10:12:00Z` is consumed; no second claim is added.

## Evidence

1. **Queue does not close the parent.** `task_queue.md` blob `b905132efb6e8a9b356a3023adb6d14905e6d686` has no `T-P5-054` owner or closure. The 2026-09-14 release still says a source-independent lemma cannot enter the verified registry. The neighbouring T-P5-053 admission audit already left the tensor Bernstein gate pending.
2. **Math review is conditional.** `review-T-P5-054-correlated-matrix-perturbation-liuguanyi-20260908T0013.md` blob `cd9e503808dc8c7f62d1a484ce4156c2f0be3fc9` states theorems T-P5-054-A through C2, identities (1.1)-(1.2), (2.1)-(2.5), (3.1)-(3.3), (5.1)-(5.6), and the singular regression (6.1)-(6.3). Section 10 leaves deployed source split, Taylor/libm enclosure, Float64, same-key cell, kappa, coverage, Lean, and admission explicit. Its `admission_label` is `pending`. Claim blob `0d732e53bfc5e3a7e9c1e6478878455811c08185` excludes source and admission work. Companion blob `5609c18749865f06aad406f1c410182146eec6e6` repeats the same pending boundary.
3. **Lean claim is not a receipt.** `claim-T-P5-054-sumengchen-20260908T0010.md` blob `8c02077487bb05f78a4acd76a232e79ebed38159` asks for a portable sidecar and says a future result may only be `compiled_candidate`. No 苏梦辰 review, `#print axioms`, placeholder scan, or CI log for this child is exhibited at the inspected tree. Section 8 theorem names remain a decomposition proposal.
4. **Local rational checks only.** Python `fractions` reproduced the published surface:

```text
trace/det identities (1.1)-(1.2) match on
(p,s,sigma,b4,b5,kappa) in {(1/2,1/3,1/5,1/7,2/9,3/4),(2,5,-1,0,1,1/8)}.
det update (2.1) matches on (a,m,c,e11,e12,e22)=(3/2,-1/4,5/3,1/6,-2/5,3/7).
rank-one family: Cdet(t)=0 for t=1/10; entry-radius penalty Pdet=2*(1/10)^2=1/50.
```

These checks do not instantiate a source packet. `p,s,sigma,b4,b5`, `Ghat`, and `E` remain hypotheses. The singular family is a regression, not a deployed residual.

## Receipt

```text
command: local fractions replay only; repo checker not run
exit_code: 0 for the local replay; not a workflow checker
axiom_print: not executed
placeholder_scan: not a kernel scan
math_review_blob: cd9e503808dc8c7f62d1a484ce4156c2f0be3fc9
math_claim_blob: 0d732e53bfc5e3a7e9c1e6478878455811c08185
companion_blob: 5609c18749865f06aad406f1c410182146eec6e6
lean_claim_blob: 8c02077487bb05f78a4acd76a232e79ebed38159
lean_review_blob: not exhibited
fresh_lean_receipt: not exhibited
trace_det_identities: true on the two rational samples
det_update_identity: true on the six-scalar sample
rank_one_cdet_loss: 0
entry_radius_penalty_on_same_family: 1/50
deployed_nominal_error_packet: not exhibited
same_key_cell: not exhibited
float64_outward_rounding: not exhibited
trig_or_taylor_enclosure: not exhibited
box_coverage: not exhibited
ode_continuation: not exhibited
fixed_kappa_choice: not exhibited
```

## Obstruction

```text
identity_surface: forming G before enclosure preserves the correlated det correction; entry radii are a coarser fallback
coefficient_surface: p, s, sigma, b4, b5, kappa, Ghat, and E are hypotheses; the rank-one figure is a regression, not a source witness
frontend_gap: no deployed nominal/error split or same-key cell row is bound
budget_gap: a PASS of abstract Cdet or Pdet is not certified on any actual residual box
interval_gap: independent intervalization of 4ps-sigma^2 and the bias-curvature numerator remains forbidden; this audit does not supply the missing enclosure
singular_gap: forcing every approximation through absolute entry radii can reject a determinant that is identically nonnegative
consumer_gap: T-P5-053 Bernstein controls and the branch-free majorant remain separate; a PASS here does not close them
formal_gap: section 8 names are not compiled; the 苏梦辰 claim has no axiom print or placeholder scan
coverage_gap: a finite abstract box does not place an absolute cell in a source domain
calculus_gap: FTOC, first-exit on the actual pair, and ODE continuation are not proved
obstruction_scope: missing source polynomials, Float64 semantics, box trajectory, flowpipe, gate binding, and a pinned receipt remain failure boundaries
missing_for_parent_close:
  one same-key signed nominal/error packet with Cdet or full Rdet enclosed rather than assumed
  an independently certified V<=Vstar sublevel and absolute source-domain inclusion
  a first-exit / ODE existence-continuation theorem on the actual pair
  an independent pinned Lean receipt after source binding
forbidden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar creation
  promotion of the perturbation bridge, the rank-one regression, or the tensor Bernstein lane
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
