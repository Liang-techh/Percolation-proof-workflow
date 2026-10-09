---
kind: review_result
review_id: review-T-P5-054-CORRELATED-PERTURBATION-ADMISSION-liuchuanafeng-20261009T1014Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-09T10:14:00Z
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

# T-P5-054 admission audit: correlated matrix perturbation stays conditional

## Question

At the inspected tree `1943f37218ceaa3e79c80c1b46c40516e67ba695`, does the published T-P5-054 note already supply a deployed nominal/error split for `p,s,sigma,b4,b5`, a same-key cell packet, Float64/outward-rounding semantics, box coverage, ODE continuation, a pinned Lean receipt, or registry admission for the correlation-preserving matrix-perturbation bridge?

May the trace/determinant identities, the entry-radius fallback, the source-variable radii, or the rank-one regression be promoted?

## Decision

**No admission upgrade. Keep `admission_label: pending`.**

柳冠一 states a source-independent exact transport: form the scaled branch-free packet `G` first, then move a symmetric error `E` by the ring identity `det(G)-det(Ghat)=Cdet`. Independent entry radii give a sound but coarser penalty `Pdet`. The rank-one family `G(t)=[[1,t],[t,t^2]]` shows that the radius fallback can fail to certify a determinant that the correlated correction preserves exactly. The note keeps deployed nominal/error splits, trigonometric/rational enclosure, Float64, coverage, ODE, Lean, and admission open.

苏梦辰 claimed a portable Lean sidecar and did not leave a `review_result`. This pass does not compile, so it does not create a `compiled_candidate` label.

This is not `rejected`: the published identities match an independent rational replay. It is not `architecture_only`: the review states exact ring and ordered-field theorem surfaces under named hypotheses. It is not a fresh `compiled_candidate`: no pinned command was run here.

Prior authorship is preserved. This file does not overwrite 柳冠一 or 苏梦辰. The same-agent claim at `2026-10-09T10:12:00Z` is consumed; no second claim is added.

## Evidence

1. **Queue does not close the parent.** `task_queue.md` blob `b905132efb6e8a9b356a3023adb6d14905e6d686` has no `T-P5-054` owner or closure. The 2026-09-14 release still says a source-independent lemma cannot enter the verified registry. The neighbouring T-P5-053 admission audit already left the tensor Bernstein gate pending.
2. **Math review is conditional.** `review-T-P5-054-correlated-matrix-perturbation-liuguanyi-20260908T0013.md` blob `cd9e503808dc8c7f62d1a484ce4156c2f0be3fc9` states theorems T-P5-054-A, B, C1, and C2, identities (1.1)-(1.2), (2.1)-(2.5), (3.1)-(3.3), (5.1)-(5.6), and the rank-one regression (6.1)-(6.3). Section 10 leaves source nominal/error splits, Float64, coverage, kappa choice, Lean, and admission explicit. Its `admission_label` is `pending`. Claim blob `0d732e53bfc5e3a7e9c1e6478878455811c08185` excludes source and admission work. Companion blob `5609c18749865f06aad406f1c410182146eec6e6` repeats the same pending boundary.
3. **No Lean receipt is attached.** 苏梦辰 claim blob `8c02077487bb05f78a4acd76a232e79ebed38159` asks for a source-independent sidecar and a later `compiled_candidate`. The inbox tree has no matching review, axiom print, or CI run. Section 8 names are a decomposition proposal, not a receipt.
4. **Local rational checks only.** Python `fractions` reproduced the published surface:

```text
trace(G)=Rtr and det(G)=4*kappa*Rdet on two rational packets.
det update (2.1) matches on (a,m,c,e11,e12,e22)=(3/2,-1/5,7/3,-2/9,4/7,1/8).
source split (5.1) matches on (phat,ep,b4hat,e4,kappa)=(2/3,-1/6,3/4,1/5,2).
rank-one Cdet at Ghat=G(0) is 0; entry-radius Pdet on |t|<=1/5 is 2/25.
```

These checks do not instantiate a source box. `p,s,sigma,b4,b5`, `Ghat`, and `E` remain hypotheses, not deployed coefficients.

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
trace_identity: true on the replayed packets
det_identity: true on the replayed packets
det_update_identity: true on the replayed scalars
source_split_identity: true on the replayed scalars
rank_one_Cdet_zero: true
entry_radius_penalty_positive: true for eps=1/5, Pdet=2/25
deployed_nominal_error_packet: not exhibited
same_key_cell: not exhibited
float64_semantics: not exhibited
box_coverage: not exhibited
ode_continuation: not exhibited
fixed_kappa_choice: not exhibited
```

## Obstruction

```text
identity_surface: forming G before the error keeps the correlated correction Cdet; independent radii only give the coarser Pdet penalty
coefficient_surface: p, s, sigma, b4, b5, kappa, Ghat, and E are hypotheses; the rank-one figure is a regression, not a source witness
frontend_gap: no deployed nominal/error split or exact polynomial row is bound
budget_gap: a PASS of abstract Cdet or Pdet is not certified on any actual residual box
interval_gap: independent intervalization of 4ps-sigma^2 and the bias-curvature numerator remains forbidden; this audit does not supply the missing enclosure
near_singular_gap: the entry-radius fallback can reject a family whose exact determinant is identically zero; the direct Cdet lane is not instantiated on a source packet
consumer_gap: T-P5-053 and the branch-free majorant remain separate; a PASS here does not close them
formal_gap: section 8 names are not compiled; the Lean claim has no review, axiom print, or placeholder scan
coverage_gap: a finite abstract cell does not place an absolute cell in a source domain
calculus_gap: FTOC, first-exit on the actual pair, and ODE continuation are not proved
obstruction_scope: missing source polynomials, Float64 semantics, box trajectory, flowpipe, gate binding, and a pinned receipt remain failure boundaries
missing_for_parent_close:
  one same-key signed nominal packet plus a certified Cdet or full Rdet lower bound, not only entry radii
  an independently certified V<=Vstar sublevel and absolute source-domain inclusion
  a first-exit / ODE existence-continuation theorem on the actual pair
  an independent pinned Lean receipt after source binding
forbidden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar creation
  promotion of the perturbation bridge, the radius fallback, the rank-one regression, or the tensor Bernstein lane
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
