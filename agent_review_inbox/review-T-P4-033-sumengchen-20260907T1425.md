kind: review_result
review_id: review-T-P4-033-sumengchen-20260907T1425
task_id: T-P4-033
source_agent: 苏梦辰
created_at: 2026-09-07T14:25:00-06:00
status: compiled_candidate
admission: pending
proposed_integration_target: theorem_sidecar

# T-P4-033 — joint defect metric bridge Lean decomposition

## Mathematical input consumed

This formalization consumes 柳冠一's source-independent joint defect metric bridge from `agent_review_inbox/review-T-P4-033-joint-defect-metric-liuguanyi-20260907T1422.md` (math-review commit `2c937063d2a5cea199fc6a13c534988e5d4a3c43`).  I did not redo the source audit or the physical derivation.  The formalization deliberately stops before concrete deployed-source binding, matrix interval verification, coverage, provenance/admission, or final P4/P8/M4 integration.

## New sidecar

- `examples/routeb_p4_joint_defect_metric_lean/P4JointDefectMetric.lean`
- `examples/routeb_p4_joint_defect_metric_lean/README.md`
- `examples/routeb_p4_joint_defect_metric_lean/verify.sh`
- `examples/routeb_p4_joint_defect_metric_lean/lean-toolchain`

The verifier is `CI_PORTABLE=1`, resolves `lake`/`lean` from `PATH`, checks the sidecar toolchain against `examples/local_fkg/lean-toolchain`, checks Mathlib revision `81a5d257c8e410db227a6665ed08f64fea08e997` from `examples/local_fkg/lake-manifest.json`, runs Lean with `-DwarningAsError=true`, requires an axiom report for every exported theorem, and rejects any `sorryAx`.

## Kernel theorem decomposition

The sidecar exports the following source-independent statements.

1. `weighted_square_identity`:
   `(beta*tau^2+alpha)*(alpha*x^2+beta*y^2) - alpha*beta*(tau*x+y)^2 = (alpha*x-beta*tau*y)^2`.

2. `scalar_weighted_square_le`:
   `alpha*beta*(tau*x+y)^2 <= (beta*tau^2+alpha)*(alpha*x^2+beta*y^2)`.
   This is the division-free scalar core and does not need positivity hypotheses.

3. `weighted_defect_pushforward_add`:
   for a normed additive commutative group, if `alpha,beta,tau,x >= 0`, `||u|| <= tau*x`, and
   `alpha*x^2 + beta*||b||^2 <= E`, then
   `alpha*beta*||u+b||^2 <= (beta*tau^2+alpha)*E`.
   Here the typed source adapter is responsible for supplying `u = T d` (or just the certified norm image); the theorem itself does not invent matrix semantics.

4. `weighted_defect_pushforward_sub`: the same bound for `||-u+b||`, matching the force-side sign convention.

5. `weighted_defect_relative_additive`: the same pushforward with source budget `kappa*A+B0`, preserving the relative-plus-additive ledger shape.

6. `quadratic_domination_pullback`: universal quadratic domination is preserved by coordinate pullback.  This is the function-level kernel core of the congruence rule; a concrete finite-dimensional adapter may instantiate the quadratic forms and coordinate map later.

7. `singular_metric_kernel_obstruction`: if the source metric functional is zero at a state while the correction-energy functional is strictly positive there, then no finite universal multiplier `mu` can satisfy `c <= mu*q`.  This formalizes the kernel obstruction without pretending that a concrete source matrix has already been bound.

8. `joint_metric_sign_flip`: for the scalar correlated two-block model `a*d^2 + 2*cross*d*b + c*b^2`, changing force/O1 coordinate by `d -> -d` requires `cross -> -cross` to represent the same quadratic source metric.

9. `correction_sign_flip`: `tau*(-d)+b = -tau*d+b`.

10. `block_diagonal_metric_sign_invariant`: if the joint metric has zero cross term, the metric is invariant under the force/O1 sign flip.

The intended concrete 6x6 matrix theorem `C^* C <= mu W => ||Cz||^2 <= mu <z,Wz>` is intentionally not claimed here.  The current sidecar exposes the minimal kernel-checkable scalar weighted specialization, convention bridge, pullback bridge, and singular obstruction.  A future matrix sidecar should only be added once the concrete `W`, `T=M_BD M_DD_inv`, dimensions, and source/checker certificate format are fixed.

## Real CI repair loop

Initial portable Actions run `34158522154`, job `101855491649`, reached this new sidecar and exposed three Lean-4.32 issues rather than a mathematical failure:

- `add_le_add_right hu ||b||` produced the opposite additive orientation from the target `||u||+||b|| <= tau*x+||b||`;
- `joint_metric_sign_flip` had `simp [jointMetric]` already close the goal, so the following `ring` generated `No goals to be solved` under `warningAsError`;
- the same redundant `ring` occurred in `block_diagonal_metric_sign_invariant`.

Because the first error interrupted `weighted_defect_pushforward_add`, the dependent add/sub/relative-additive theorems temporarily printed `sorryAx` in that failed run.

Repair commit `71e0c35a34a7e30433930023c8d1a246e41ae52a` changed the inequality step to explicit
`add_le_add hu (le_refl ||b||)` and removed the two redundant `ring` calls.  No theorem constant, mathematical hypothesis, source boundary, or target inequality was weakened.

Final portable Actions run `34158983349`, job `101856640525`, on Lean `4.32.0` / Lake `5.0.0`, contains the focused result:

- `AXIOM_AUDIT=PASS`
- `P4_JOINT_DEFECT_METRIC_FOCUSED_CHECK=PASS`
- `SIDECAR_RESULT=PASS path=examples/routeb_p4_joint_defect_metric_lean/verify.sh`

All ten exported theorems print only `[propext, Classical.choice, Quot.sound]`; this sidecar has no `sorryAx`.

The aggregate `portable-sidecars` job is still red because the workflow intentionally runs every portable sidecar and several unrelated pre-existing candidates still fail.  In the same final run, examples include `anthropic_flt_quotient_transport_sidecar` path resolution, `routeb_m4_cross_branch_budget_lean`, `routeb_p5_componentwise_relative_decay_lean`, `routeb_p5_parameter_tube_gain_lean`, `routeb_p5_weighted_dual_residual_lean`, `routeb_p7_tail_schur_completion_lean`, and `routeb_p8_ramp_reconstruction_sidecar`.  I did not modify or claim those tasks.

## Remaining formal/source obligations

Still open and explicitly outside this sidecar:

- deployed source binding of the actual distal/port defect pair;
- typed proof that the physical transfer is the intended `T = M_BD M_DD_inv`, including whatever left-inverse/invertibility contract is used;
- a concrete 6x6 joint source metric `W`, or certified scalar `alpha,beta,tau` data, on the same domain;
- Float64/controller/solve semantics and any additive runtime remainder;
- physical/source-domain and P8 trajectory/flowpipe coverage;
- P4/P8/M4 composition, provenance/admission, registry mutation, and final conclusion.

Recommended next formal interface once source/checker data exist: instantiate `weighted_defect_pushforward_add/sub` from the typed transfer norm certificate; if a correlated `W` is retained instead of block-diagonal `alpha,beta`, first freeze a concrete rational PSD/generalized-eigenvalue certificate and then add a separate finite-dimensional congruence sidecar.  Do not silently reuse the same cross block under the force/O1 sign flip unless it is zero.

## Status

`compiled_candidate` only.  待封不觉独立验证 / 待梁智炜最终整合。
