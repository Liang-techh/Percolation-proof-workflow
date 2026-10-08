---
kind: review_result
review_id: review-T-P5-040-MIXED-RELATIVE-ADDITIVE-ADMISSION-liuchuanafeng-20261008T1416Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-08T14:16:00Z
inspected_commit: c7d2c0a0675c1dcc1f7fd0b94b65f72bc1aee4e1
claim_id: claim-T-P5-040-MIXED-RELATIVE-ADDITIVE-ADMISSION-liuchuanafeng-20261008T1414Z
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P5-040-honglianmozun-20260907T1950.md
  - agent_review_inbox/review-T-P5-040-honglianmozun-20260907T1950.md
  - agent_review_inbox/claim-T-P5-040-sumengchen-20260907T2013.md
  - agent_review_inbox/review-T-P5-040-sumengchen-20260907T2058.md
  - examples/routeb_p5_mixed_relative_additive_lean/P5MixedRelativeAdditive.lean
  - agent_review_inbox/review-T-P5-039-PARETO-OPTIMIZER-ADMISSION-liuchuanafeng-20261008T1117Z.md
task_id: T-P5-040
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
proposed_integration_target: documentation
requested_action: harvest_pending_admission_audit_do_not_promote_mixed_relative_additive
---

# T-P5-040 admission audit: mixed relative-additive absorption stays conditional

## Question

At the inspected tree `c7d2c0a0675c1dcc1f7fd0b94b65f72bc1aee4e1`, does the published T-P5-040 absorption, or the existing portable sidecar, already supply same-domain component contracts `|l_i| <= rho_i|u_i| + b_i`, square budgets `B4,B5` or `G4,G5`, Float64/solve/controller semantics, absolute cell-center coverage, ODE continuation, an independently re-executed pinned receipt, or registry admission for the block-(4,5) Pareto family

```text
Q >= c(r) V + a4(r) u4^2 + a5 u5^2,
c(r)=(109-r)/200, a4(r)=(250+53r)/1500, a5=1/6, 0 <= r <= 1?
```

May the sharp charge `b_i^2/(4 t_i)`, the division-free gate `300000 B4 A5 + 1200 B5 A4 < (109-r) A4 A5`, the zero-relative reduction to T-P5-039, or the incremental gate `900000 G4 A5 + 3600 G5 A4 < (109-r) A4 A5` be promoted?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The published child is one source-independent exact absorption of additive bias against unused Pareto quadratic reserve. It does not close a parent gate, and it does not replace the disjoint T-P5-036/T-P5-037 endpoint certificates or the T-P5-039 selector.

红莲魔尊 states that if `t4=a4(r)-rho4>0` and `t5=a5-rho5>0`, then

```text
V' <= -c(r) V + b4^2/(4 t4) + b5^2/(4 t5),
```

with equality on a channel at `|u|=b/(2t)`. The quarter-barrier consumer is the polynomial gate above, and `rho4=rho5=0` reduces it exactly to the T-P5-039 additive gate. 苏梦辰 records a portable sidecar whose published status is `compiled_candidate`, not `verified`.

This is not `rejected`: the one-channel completion, reserve numerators `A4=1500 t4` and `A5=6 t5`, the zero-relative reduction, and the incremental cross-multiplication match independent rational arithmetic, and the current Lean file still exports the stated theorem surface. It is not `architecture_only`: the review states an exact real inequality family. It is not upgraded to `compiled_candidate` by this pass: no kernel was run here. The earlier sidecar review remains a historical candidate receipt and is not re-certified.

Prior authorship is preserved. This file does not overwrite 红莲魔尊 or 苏梦辰.

## Evidence

1. **Queue does not close the parent.** `task_queue.md` at this commit has no later owner or closure for `T-P5-040`. The 2026-09-14 release still says a source-independent lemma cannot enter the verified registry. The neighbouring T-P5-039 admission audit already left the zero-relative optimizer pending.
2. **Published math review is conditional.** `review-T-P5-040-honglianmozun-20260907T1950.md` blob `80f950d571eb6124e6fb7df819f50d2eab67f1ea` states the mixed contract (0.4), the sharp charge (0.6)-(0.7), the reserve-exhausted unboundedness boundary in Section 3, the division-free gate (2.5), the zero-relative reduction (2.6), and the incremental gate (4.5). Section 6 leaves deployed residuals, Float64, ODE/flowpipe, provenance, and parent closure explicit. Its `admission_label` is `pending`.
3. **Sidecar exists but was not re-executed.** `examples/routeb_p5_mixed_relative_additive_lean/P5MixedRelativeAdditive.lean` blob `59b1de8a0ba11eb7f3023cc52dc3c0b88bdb6991` still defines `decayRate`, `a4`, `a5`, `reserve4`, `reserve5`, `A4`, `A5`, and the 11 named theorems listed by `review-T-P5-040-sumengchen-20260907T2058.md` blob `052bdac491a46fe970974a66f8b66105bd5163ab`, including `block45_pareto_mixed_residual_decay`, `block45_pareto_bias_first_exit_gate`, `block45_zero_relative_gate_reduces`, and `block45_pareto_incremental_gate_cross`. That review cites workflow `34181527795` / job `101921468341` with axiom set `[propext, Classical.choice, Quot.sound]` and explicitly keeps source, coverage, and admission open. This pass did not run `verify.sh`, did not print axioms, and did not treat the aggregate red portable-sidecar job as a T-P5-040 failure or a pass.
4. **Local rational checks only.** `A4 = 1500 t4` and `A5 = 6 t5` recover the stated numerators. Substituting `rho4=rho5=0` gives `A4=250+53r`, `A5=1`, so the quarter gate is exactly the T-P5-039 gate. The incremental comparison `G4/(4 t4)+G5/(4 t5) < c(r)/12` cross-multiplies to `900000 G4 A5 + 3600 G5 A4 < (109-r) A4 A5`. The one-channel identity `-t u^2 + b|u| = b^2/(4t) - t(|u|-b/(2t))^2` is the stated sharp completion. These are local rational checks, not kernel proofs and not source bounds.

## Receipt

```text
command: not run
exit_code: not claimed by this pass
axiom_print: not executed; historical sidecar review claims [propext, Classical.choice, Quot.sound] only
placeholder_scan: not a kernel scan
math_review_blob: 80f950d571eb6124e6fb7df819f50d2eab67f1ea
lean_review_blob: 052bdac491a46fe970974a66f8b66105bd5163ab
lean_file_blob: 59b1de8a0ba11eb7f3023cc52dc3c0b88bdb6991
sharp_charge: b^2/(4t) with equality at |u|=b/(2t), local identity check
quarter_gate: 300000*B4*A5 + 1200*B5*A4 < (109-r)*A4*A5, not a source witness
zero_relative_reduction: A5(0)=1, A4(r,0)=250+53r, exact arithmetic match to T-P5-039
incremental_gate: 900000*G4*A5 + 3600*G5*A4 < (109-r)*A4*A5, local cross-multiplication only
sidecar_theorems: 11 named theorems still present; not recompiled
same_domain_rho_b: not exhibited
square_budgets_B_G: not exhibited
float64_incremental_semantics: not exhibited
cell_center_inclusion: not exhibited
ode_continuation: not exhibited
```

## Obstruction

```text
identity_surface: square completion and cross-multiplied gates are exact inside the stated family
coefficient_surface: 109, 250, 53, 1500, 6, 300000, 1200, 900000, and 3600 are algebraic constants inherited from endpoint gates, not source witnesses
reserve_gap: t_i>0 is necessary for a finite source-independent bias charge; t_i<=0 with positive bias is unbounded and is not repaired here
contract_gap: rho_i and b_i remain hypotheses; no same-domain residual table is exhibited
budget_gap: B4, B5, G4, and G5 remain hypotheses
sidecar_gap: historical compiled_candidate is not re-executed and is not an admission receipt
parent_gap: T-P5-039 remains pending; this absorption does not close it or T-P5-041
coverage_gap: a positive abstract margin does not place an absolute cell center in a source box
calculus_gap: first-exit and ODE continuation are named and not proved
composition_gap: the mixed relative-plus-additive family must not be substituted for a stronger matrix/SPN/source-correlated certificate
obstruction_scope: missing same-domain rho/b contracts, square budgets, Float64/solve/controller difference semantics, center trajectory, flowpipe, and an independent pinned receipt remain failure boundaries
missing_for_parent_close:
  one same-domain residual table producing rho4, rho5, b4, b5 or their square budgets
  a decision routing Float64/solve/controller jumps into that table or an additive branch
  an independently certified cell-center trajectory and absolute source-domain inclusion
  a first-exit / ODE existence-continuation theorem on the actual pair
  an independent pinned Lean receipt for the selected algebraic leaf
forbidden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar creation
  promotion of the sharp charge, quarter gate, zero-relative reduction, or incremental gate
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
