---
kind: review_result
review_id: review-T-P5-033-sumengchen-20260907T1632
task_id: T-P5-033
agent: 苏梦辰
source_agent: 苏梦辰
claimed_at: 2026-09-07T16:10:00-06:00
created_at: 2026-09-07T16:32:00-06:00
upstream_review: review-T-P5-033-honglianmozun-20260907T1604
inspected_commit: 5517ca9f3d745c117cab1b82cf127117bd28a009
integration_status: pending
admission_label: compiled_candidate
proposed_integration_target: theorem
requested_action: independent_kernel_review_then_coordinator_integration
---

# T-P5-033 — exact `93/100` block-(4,5) SOS Lean formalization

## Scope

This review formalizes the source-independent mathematical core supplied by 红莲魔尊 in `review-T-P5-033-honglianmozun-20260907T1604.md`. It does not establish source residual bounds, true-DH/Float64 execution semantics, P8 trajectory coverage, provenance/admission, or final P5/M4 integration.

Portable sidecar:

`examples/routeb_p5_block45_93_sos_lean/`

Files:

- `P5Block45NinetyThreeSOS.lean`
- `README.md`
- `lean-toolchain`
- `verify.sh`

The sidecar uses the repository-compatible `leanprover/lean4:v4.32.0` toolchain. `verify.sh` resolves `lake` and `lean` through `PATH`, checks the local toolchain pin, invokes `lake env lean -DwarningAsError=true`, checks every exported `#print axioms` report, and rejects `sorryAx`. It is registered with `CI_PORTABLE=1` for `.github/workflows/lean-agent-sidecars.yml`.

## Kernel statements

The Lean file freezes the exact scalar block-(4,5) storage `V45` and dissipation `Q45` from the upstream mathematical derivation, then exports the following minimal statements.

1. `block45_Q_minus_93_100_V_sos`

   Exact weighted nine-square identity

   `Q45 - (93/100) V45 = Σ nine explicitly rational nonnegative squares`.

   The coefficients are exactly those supplied upstream:

   `3542407/600000000`, `155697/800000000`, `69762071/150000000`, `29216493/80000000`, `321/80000`, `10850093/600000000`, `1/800`, `1/800`, `18668727/7200000000`.

2. `block45_Q_ge_93_100_V`

   From the exact SOS identity:

   `(93/100) V45 ≤ Q45`.

   No matrix-positivity API or floating-point spectral calculation is used.

3. `lyapunov_ledger_of_93_100_coercivity`

   Abstract downstream replacement theorem:

   if `(93/100)V ≤ Q` and `Vdot ≤ -(1/2)Q + (17/10)L2`, then

   `Vdot ≤ -(93/200)V + (17/10)L2`.

4. `block45_lyapunov_ledger`

   Concrete specialization of the previous theorem to the exact `V45,Q45` definitions.

5. `quarter_barrier_gate`

   Division-free checker gate:

   `1360 L2 < 93  ->  (17/10)L2 < (93/200)(1/4)`.

6. `incremental_Kc_one_twelfth_gate`

   Division-free `Kc=1/12` checker gate:

   `340 mu + 4080 nu < 93  ->  (17/10)(mu/12 + nu) < (93/200)(1/12)`.

7. `exact_capacity_improvement_ratio`

   Exact comparison against the previous `8/9` coercivity consumer:

   `(93/200)/(4/9) = 837/800`.

8. `ultimate_residual_coefficient`

   Exact residual coefficient and comparison:

   `(17/10)/(93/200) = 340/93` and `340/93 < 153/40`.

## Real Lean/CI repair loop

### First CI failure

Initial portable run:

- Actions run: `34165979190`
- job: `101876984468`
- head commit: `4baf6eea39bbada57e572fe9e7a191283ac6fc3b`

Lean 4.32 exposed two real portability issues:

- `V45` and `Q45` were definitions over `ℝ` division and therefore needed a `noncomputable section`;
- the exact polynomial SOS proof needed the definitions explicitly unfolded before `ring`.

Because the first theorem failed, dependent theorems in that failed run temporarily inherited `sorryAx`. The fix did not weaken any theorem statement or change any rational constant. The SOS proof was changed to explicit normalization followed by polynomial closure:

`simpa/simp [Q45, V45]` followed by `ring`.

### Second CI failure

After commit `76182228996bdc0fee5580692a4fb70ee50d62db`, theorem bodies typechecked and all printed axiom reports were already clean, but Lean correctly rejected the file because the newly opened `noncomputable section` was not closed. This was a scope/syntax error, not a mathematical failure.

The final repair added the missing section `end`, again without changing any statement or constant.

### Final focused CI pass

Final head commit:

`5517ca9f3d745c117cab1b82cf127117bd28a009`

Actions:

- run: `34166671632`
- portable-sidecars job: `101878956881`
- Lean: `4.32.0`
- Lake: `5.0.0-src+8c9756b`

The focused sidecar emitted:

`AXIOM_AUDIT=PASS`

`P5_BLOCK45_93_SOS_FOCUSED_CHECK=PASS`

`SIDECAR_RESULT=PASS path=examples/routeb_p5_block45_93_sos_lean/verify.sh`

All eight exported theorems have exactly the standard dependency set

`[propext, Classical.choice, Quot.sound]`

and no `sorryAx`.

The aggregate `portable-sidecars` workflow remains red because other, already existing sidecars still fail independently. Examples include the FLT quotient path lookup, M4 cross-branch warnings/noncomputable declarations, older P5 componentwise/parameter-tube/weighted-dual files, P7 tail-Schur, and the old P8 ramp-reconstruction sidecar. This task did not modify or take ownership of those files.

## Formal interface boundary

This sidecar proves only the exact mathematical consumer layer. The following obligations remain open and must not be inferred from this compile pass:

- `P5_RESIDUAL_L2_SOURCE_BINDING`: produce and bind a certified source-side `L2` residual quantity to the same residual convention consumed by the ledger;
- `TRUE_DH_FLOAT64_SEMANTICS`: connect exact rational/model quantities to the Julia/Float64 execution path, including model/FD/controller/solve defects as appropriate;
- `ODE_FIRST_EXIT_COVERAGE`: connect the pointwise inward inequality to a real trajectory/first-exit or continuation theorem on the certified domain;
- same-domain/P8 coverage and any concrete source authentication required by the final theorem path.

No P5/M4 final status was changed and no registry/admission mutation was made.

## Suggested independent check

封不觉 can independently kernel-check the eight exported statements and verify that the exact nine-square identity matches the upstream coefficient ledger. 梁智炜 can then decide whether this `93/100` coercivity result replaces the older `8/9` consumer in the integration DAG and which source-side `L2` certificate is allowed to feed it.

**Status: `compiled_candidate` — 待封不觉独立验证 / 待梁智炜最终整合。**
