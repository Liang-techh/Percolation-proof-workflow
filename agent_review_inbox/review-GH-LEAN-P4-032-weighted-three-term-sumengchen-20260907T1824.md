---
kind: review_result
review_id: GH-LEAN-P4-032-weighted-three-term-SUMENGCHEN-COMPILE-20260907T1824
task_id: GH-LEAN-P4-032-weighted-three-term
agent: 苏梦辰
source_agent: 苏梦辰
created_at: 2026-09-07T18:24:00-06:00
scope: lean_theorem_decomposition_and_focused_compile
admission_label: compiled_candidate
final_integration: false
---

# T-P4-032 weighted three-term quadratic budget — focused Lean compile result

## Result

The source-independent weighted three-term defect budget now compiles under the repository-pinned Lean environment through the portable focused verifier.

Final source commit:

- `292961a3f9d5d0d4085c42ba2e27379b72523b72`
- source: `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_WeightedThreeTerm.lean`
- source blob: `a84e9ccfdf5861048b51bbb24c189490e5358bc8`
- focused verifier: `examples/routeb_p4_weighted_three_term_focused/verify.sh`
- verifier blob: `d13c6da7700ad63def0817411f0015ed10c1cc40`

The two imported P4-032 support modules had already been repaired for the same pinned environment in commits `482a80d401b5f7e4b6c86b51a3a584abae3362be` and `ef81e9d0f507af8cb1b815c5fd5846892a5c2c64`.

## Kernel theorem surface

The focused verifier checks the following exported statements:

1. `reciprocal_iff_polynomial`
2. `ofPolynomial`
3. `weighted_scalar`
4. `weighted_three_term_norm_sq`
5. `routeB_port_defect_quadratic_budget`
6. `action_squared_budget`
7. `force_accel_term_identity`
8. `force_defect_budget`
9. `accel_defect_budget`

The decomposition preserves the intended interface boundary:

- the port term, transported distal defect, and local defect are combined by a weighted square budget rather than by repeating a scalar triangle estimate;
- squared distal budgets are transported through `ActionBound` without choosing square roots;
- `DistalForceDefect` and `DistalAccelDefect` remain distinct typed states;
- the force-defect route uses `(MBD * J) *ᵥ e`, while the acceleration-defect route uses `MBD *ᵥ e`;
- conversion between the two routes requires the explicit hypothesis `ea.value = J *ᵥ ef.value`; no backward-residual sign convention or approximate inverse is inferred.

## Real CI repair loop

The target was repaired against real GitHub Actions / Lean 4.32 failures rather than by weakening theorem statements.

Earlier target repair replaced a Lean-4.32-incompatible multiplication cancellation expression based on `(mul_le_mul_right hp).mp` with an explicit multiplied inequality followed by `le_of_mul_le_mul_right hm hp`. It also removed a tactic after a `field_simp` that had already closed its goal.

Run `34172592911`, job `101895633914`, then exposed one remaining `warningAsError` portability issue: the `field_simp` proving the reciprocal-clearing identity already solved the goal, so the following `<;> ring` was reported as an unreachable tactic. Commit `292961a3f9d5d0d4085c42ba2e27379b72523b72` removed only that unreachable tactic; theorem statements and constants were unchanged.

Final real run:

- Actions run: `34172887981`
- job: `101896479480`
- focused sidecar output:
  - `AXIOM_AUDIT=PASS`
  - `P4_WEIGHTED_THREE_TERM_FOCUSED_CHECK=PASS`
  - `FORCE_ACCEL_TYPED_DISTINCTION=PRESERVED`
  - `SOURCE_BINDING=OPEN`
  - `COVERAGE=OPEN`
  - `ADMISSION_MUTATION=false`
  - `P4_M4_FINAL_INTEGRATION=false`
  - `SIDECAR_RESULT=PASS path=examples/routeb_p4_weighted_three_term_focused/verify.sh`

Pinned environment recorded by the same Actions run:

- Lean toolchain: `leanprover/lean4:v4.32.0`
- Lean: `4.32.0`
- Lake: `5.0.0-src+8c9756b`
- local-fkg mathlib revision: `81a5d257c8e410db227a6665ed08f64fea08e997`

## Axiom status

All nine audited target declarations report only the standard Mathlib/kernel dependency set `[propext, Classical.choice, Quot.sound]`. The focused verifier found no `sorryAx`.

This is a focused compile result only. It does not establish source semantics, trajectory/domain coverage, a concrete numerical weight instance, Float64 realization, registry admission, or final P4/M4 integration.

## Remaining formal/source obligations

The next consumer must supply, on the same certified domain:

- the concrete source identity producing the three B-force terms;
- squared budgets for the port, distal, and local terms;
- the concrete `ActionBound` for `MBD * J` or `MBD`, according to whether the source defect is force-typed or acceleration-typed;
- positive weights satisfying either the reciprocal condition or its polynomial form;
- P8 same-domain trajectory/flowpipe coverage before this budget can be used as a parent-level certificate.

Suggested integration target, subject to coordinator choice: `P4.weighted_three_term_defect_budget`.

The aggregate `lean-agent-sidecars` workflow is still red because unrelated pre-existing/unclaimed portable sidecars fail; the P4 weighted-three-term focused sidecar itself passed. Those unrelated failures are not treated as evidence against this result and were not modified in this task.

**Status: compiled_candidate — 待封不觉独立验证 / 待梁智炜最终整合。**
