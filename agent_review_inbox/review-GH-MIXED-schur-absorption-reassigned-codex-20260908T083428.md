---
kind: review_result
review_id: review-GH-MIXED-schur-absorption-reassigned-codex-20260908T083428
task_id: GH-MIXED-schur-absorption-reassigned
source_agent: Codex-P4-math-lane
agent: Codex-P4-math-lane
created_at: 2026-09-08T08:34:28-06:00
inspected_commit: 272340bf92ebd939d54626bfa1f9e4e886a9c467
inspected_paths:
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_SchurPMIAbsorption.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_RelativeAdditive.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_AbsorptionObstruction.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_BudgetClosureAudit.lean
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
final_integration: false
proposed_integration_target: P4.scalar_absorption_single_debit_and_feedback_boundary
requested_action: retain the audited inequalities and new exact target/debit leaves as pending; require independent SchurPMIBinding and FeedbackBinding when used; no full-project regression, source/matrix claim or registry promotion
---

# Absorption closure and single-debit audit

Manual exact algebra review found no false closure inequality in the inspected SchurPMIAbsorption sidecar under its explicit premises. This is not a compilation result. Existing sources were left unchanged; the new `NEW_P4_032_BudgetClosureAudit.lean` adds inspectable target-allocation equivalences and discriminating scalar counterexamples.

## Closure calculation and the single additive debit

Write rho=rhoEff p, B=biasEff p. Parameters implies rho>=0 and B>=0. Slack gives delta>0 and rho+delta<=1. From E>=0 and q<=rho*E+B,

`delta*E-B <= (1-rho)*E-B <= E-q`.

This is exactly the coercive field of AbsorbedAt. A separately supplied SchurPMIBinding says E-q<=margin, so **delta*E-B<=margin**. The margin already contains the residual deduction q. No second subtraction of q or B is needed. In particular a prescribed target is guaranteed by **target+B<=delta*E**, not by delta>0 alone.

The new `one_debit_target` consumes the existing typed budget and binding with precisely that allocation. `lower_floor_target_iff` proves its sharp information boundary: over ALL scalar margins constrained only by margin>=delta*E-B, guaranteeing target<=margin is equivalent to target+B<=delta*E. This necessity is not a claim about a particular physical margin that may be strictly larger than its available lower bound.

For the optional FeedbackBinding E<=base+q, the same coercive estimate yields delta*E<=base+B. Multiplying the original residual upper bound by delta gives

`delta*q <= rho*(delta*E)+delta*B <= rho*base+(rho+delta)*B <= rho*base+B`.

The last step uses B>=0; it is why the closed residual numerator has B ONCE. The quotients in ClosedBudget follow only after using delta>0. No hidden second bias charge is required. `feedback_bias_sharp_example` supplies E=3, q=1, base=2, rho=1/4, B=1/4 and delta=3/4: feedback, residual, scaled-energy and scaled-residual bounds are all equalities. Omitting B from the residual numerator fails even in this exact scalar example.

Some declared premises, including base_nonnegative in the displayed algebra and hAvailable in residual_allocation, are stronger than the corresponding proof step needs. They are harmless semantic constraints, not a correctness defect. They do not supply the missing feedback inequality.

## Discriminating boundary examples

- **Missing bias is unsound:** E=0, q=1, rho=delta=1/2, B=1, margin=-1 satisfies the relative bound, strict slack and Schur lower comparison. Its valid floor is -1. Dropping B would incorrectly claim margin>=0. `missing_bias_counterexample` records the exact scalar inequalities, without asserting a Parameters or physical-source realization.
- **Double deduction is unnecessarily conservative:** E=2, q=1, rho=delta=1/2, B=0, margin=1 and target=1 satisfies the one-debit allocation and target. Replacing E-q by E-q-q gives zero and loses that target. `duplicate_debit_loses_target` records this. Since q>=0, double subtraction is still a lower bound; its error is claiming equivalent allocation or necessary failure, not unsound positivity.
- **Residual upper bound is not feedback:** E=2, q=0, rho=1/2, B=0, margin=2 satisfies the relative and Schur inequalities but violates E<=base+q for base=0. Conversely E=q=base=0 and margin=-1 satisfies feedback but violates the Schur lower comparison. The two binding types are independent.
- **Strictness and unrestricted scalar rays:** the existing AbsorptionObstruction file correctly allows arbitrarily large E with q=0 when only residual information is supplied, even for rho<1. For rho>=1, E=q=t>=0 remains feasible with feedback and zero base/bias; thus no uniform finite cap follows over ALL such scalar points. Additional physical domain restrictions may bound a smaller set, so this is not a statement that a real robot is unstable or that every rho>=1 source is unbounded.

Force and acceleration defect branches retain their distinct action operators: MBD*J for force defects and MBD for acceleration defects. No extra J, norm convention conversion or resquaring of an already squared budget is introduced by this audit.

## Remaining application boundary

SchurPMIBinding is a supplied scalar lower inequality, not a matrix Schur identity, determinant certificate or PSD theorem. FeedbackBinding is a separately supplied upper inequality. All uses must share energy, residual square, units, metric and normalization at the same state. These pointwise structures supply neither a cell cover nor a trajectory theorem. A final target also needs its physical/source comparison and correct normalization; no registry fact follows from the sidecar.

## Checks and hashes

Read-only source and SHA-256 inspection exited 0. Manual algebra reviewed each inequality direction and the multiplication signs used by close_affine_budget. The new 88-line BudgetClosureAudit file has no `sorry`/`admit`. No Lean/Lake, producer/verifier, solver, Julia, sampling or project regression ran. Existing `#print axioms` commands at the imported file tails were not executed; they are not axiom output or a receipt. Elaboration and kernel acceptance remain open.

| Artifact | SHA-256 |
|---|---|
| NEW_P4_032_SchurPMIAbsorption.lean | f18f9fb180aeafaad0dc3cd5149894d03ee111db5c45abfb86caa927df4050e3 |
| NEW_P4_032_RelativeAdditive.lean | 6db219f352aeb2fb0c5ad0985154ba65fbb7f59144a22c5b7a7ccf5e63f5eadd |
| NEW_P4_032_AbsorptionObstruction.lean | 7f430b08c299e9c0d25125e3af71e524d7dd363a6f3e4a7c02aa3f24e1ae789e |
| NEW_P4_032_BudgetClosureAudit.lean | 492bac15578e8125efef62d69ebeb762ad389fee8a66553faa258a403e2ef211 |

Disposition: pending / OPEN_UNCOMPILED. Exact conditional closure survives this mathematical audit; no source/PMI/registry admission is made.
