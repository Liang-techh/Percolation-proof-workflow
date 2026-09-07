---
kind: review_result
review_id: review-T-P5-027-juyangxianzun-20260907T1136
task_id: T-P5-027
source_agent: 巨阳仙尊
agent: 巨阳仙尊
created_at: 2026-09-07T11:36:00-06:00
status: compiled_candidate
admission_label: compiled_candidate
claim: agent_review_inbox/claim-T-P5-027-juyangxianzun-20260907T1127.md
math_input:
  - agent_review_inbox/review-T-P5-027-kuangmanmozun-20260907T1044.md
  - agent_review_inbox/companion-T-P5-027-kuangmanmozun-20260907T1048.md
sidecar: examples/routeb_p5_near_sharp_centered_gain_lean/
lean_source_blob: 2df9e607713a6b6bb5ce80eb1ca88dede11ce788
verify_blob: df5e2a5cb43fd1655552be740c95e3701b802a0f
toolchain_blob: 94b9f495baff80fd9cb44aad8f4762cb3b2066fe
ci_head: 9355e80d92468364934136bb5015a7323ed8f30b
ci_run: 34147918282
ci_job: 101823848202
---

# T-P5-027 near-sharp scalar centered-gain: Lean formalization result

## Scope

This review formalizes only the source-independent algebraic child proposed by 狂蛮魔尊 in `review-T-P5-027-kuangmanmozun-20260907T1044.md`, and **explicitly consumes the corrected arithmetic** in `companion-T-P5-027-kuangmanmozun-20260907T1048.md`.  It does not bind Julia/DH/Float64 semantics, a concrete `K_path`/`ell2_path`, P8 path/cell coverage, ODE continuation, provenance/admission, registry state, or final P5/P8/M4 closure.

Portable CI artifact:

- `examples/routeb_p5_near_sharp_centered_gain_lean/P5NearSharpCenteredGain.lean`
- `examples/routeb_p5_near_sharp_centered_gain_lean/lean-toolchain`
- `examples/routeb_p5_near_sharp_centered_gain_lean/verify.sh`
- `examples/routeb_p5_near_sharp_centered_gain_lean/README.md`

The sidecar pins Lean `4.32.0`; `verify.sh` resolves `lake` from `PATH`, verifies the sibling `examples/local_fkg/lake-manifest.json`, compiles with `-DwarningAsError=true`, requires an axiom report for every exported theorem, and fails closed on `sorryAx`, Lean errors, or missing axiom reports.

## Lean theorem decomposition

The following declarations compile in the pinned environment.

1. `weighted_joint_quadratic_bound_block45`

   Exact rational weighted comparison

   `75/106 * U + 106/75 * N <= 47984317/10000000 * Q`.

   The proof is not a floating-point eigenvalue check.  It expands the exact rational matrix gap into four explicitly frozen rational squares (an LDL/SOS witness), proves each weighted square nonnegative, and closes by linear arithmetic.

2. `weighted_amgm_75_106`

   `4*U*N <= (75/106*U + 106/75*N)^2`, obtained from the square
   `(75/106*U - 106/75*N)^2 >= 0`.

3. `qDissipation_nonneg`

   Derives `Q >= 0` from the weighted comparison and the manifest nonnegativity of `U,N`.

4. `near_sharp_joint_centered_gain`

   The main division-free near-sharp metric:

   `400000000000000 * U * N <= 2302494677956489 * Q^2`.

5. `abs_le_of_sq_le_sq_nonneg`

   Reusable square-to-absolute-value bridge used to keep the checker route square-only.

6. `near_sharp_scalar_residual_consumer`

   From

   `rcSq <= ell2*N`,

   `coupling^2 <= U*rcSq`,

   `400000000000000*U*N <= 2302494677956489*Q^2`,

   `2302494677956489*ell2 <= 400000000000000*mu^2`,

   together with the required nonnegativity hypotheses, Lean proves

   `|coupling| <= mu*Q`.

7. `block45_near_sharp_scalar_residual_consumer`

   Checker-facing specialization to the exact Route-B block-(4,5) definitions `sumSq`, `stateSq`, and `qDissipation`.

8. `old_minus_new_constant_corrected`

   Freezes the **corrected** companion-log identity

   `144/25 - 2302494677956489/400000000000000`
   `= 1505322043511/400000000000000 > 0`.

   This intentionally replaces the incorrect numerator in the original review text.

9. `sharpness_bracket_width`

   Freezes the exact bracket width

   `2302494677956489/400000000000000 - 11512473/2000000`
   `= 77956489/400000000000000 > 0`.

10. `lower_witness_rejects_57562365_over_1e7`

    Kernel-checks the exact rational lower witness

    `z0 = (2379, 73046, 1832, 68229)`,

    including

    `N = 9999930422`,

    `U = 19976358146`,

    `Q = 14138344959005123/2400000`,

    and the positive integer cross-multiplication

    `10000000*U*N*2400000^2 - 57562365*14138344959005123^2`
    `= 23290832775682489880381695029915 > 0`.

    Hence any asserted universal scalar constant at or below `57562365/10000000 = 11512473/2000000` is refuted by this witness.

## Real GitHub Actions result

The sidecar was exercised by the repository workflow at exact head
`9355e80d92468364934136bb5015a7323ed8f30b`:

- workflow run: `34147918282`
- job: `101823848202`
- runner: Ubuntu 24.04
- Lean: `4.32.0`
- Lake: `5.0.0-src+8c9756b`

The log contains, for this sidecar:

`AXIOM_AUDIT=PASS`

`P5_NEAR_SHARP_CENTERED_GAIN_FOCUSED_CHECK=PASS`

`SIDECAR_RESULT=PASS path=examples/routeb_p5_near_sharp_centered_gain_lean/verify.sh`

All ten exported declarations report only the standard axiom set
`[propext, Classical.choice, Quot.sound]`; **no `sorryAx` appears in this sidecar**.

The shared workflow as a whole is red because other independent lanes fail.  In this same run the unrelated failures include the pre-existing FLT quotient relative-path issue, `routeb_m4_cross_branch_budget_lean`, `routeb_p5_componentwise_relative_decay_lean`, `routeb_p5_weighted_dual_residual_lean`, `routeb_p7_tail_schur_completion_lean`, `routeb_p8_ramp_reconstruction_sidecar`, and 苏梦辰's newly added `routeb_p5_moving_frame_transport_lean`.  I did not modify or claim those lanes.

## What this closes and what it does not

This closes the **pure scalar block-(4,5) algebraic consumer** for T-P5-027: the old `144/25` product-of-bounds constant can be replaced by the compiled near-sharp rational constant

`C_new = 2302494677956489/400000000000000`,

with the exact lower witness showing that the remaining scalar slack is already very small.  The corresponding checker inequality is now the integer condition

`2302494677956489 * ell2 <= 400000000000000 * mu^2`.

Open obligations remain physical/source-facing rather than algebraic:

- produce a true same-domain `ell2_path` / `K_path` from the centered actual-minus-nominal source semantics;
- bind Julia/DH/Float64/controller/solve increments and keep nonzero anchor bias out of the homogeneous centered term;
- establish P8 path/cell coverage and the needed initial/ODE first-exit continuation facts;
- if stronger margin is needed, prefer the anisotropic feasible-cone/SPN route (`T-P5-025/T-P5-026`) rather than spending more effort squeezing the scalar constant.

No provenance/admission or registry mutation was performed.

**Status: `compiled_candidate` — 待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
