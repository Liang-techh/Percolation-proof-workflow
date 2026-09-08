---
kind: review_result
review_id: review-T-P5-047-juyangxianzun-20260907T2210
task_id: T-P5-047
agent: 巨阳仙尊
source_agent: 巨阳仙尊
created_at: 2026-09-07T22:10:00-06:00
inspected_commit: b81904adc6a1f890065940d4426f04666a0e75ec
mathematical_input:
  - review-T-P5-047-shared-r-kuangmanmozun-20260907T2148.md
formalization_path: examples/routeb_p5_shared_r_optimizer_lean/
lean_source_blob: aebbd7e5355aeb1123e4c2097288c365959aed01
verify_blob: 5db6540f443a7de4586da1e36a819c5d582eda6e
readme_blob: ca044beb4a0cdf5ebd103cf160da2af8c2512fc7
integration_status: pending
admission_label: compiled_candidate
proposed_integration_target: theorem
requested_action: independent_verify_then_coordinator_harvest; do_not_promote_full_five_candidate_completeness
---

# T-P5-047 — shared-`r` optimizer Lean focused compile / axiom result

## 0. Scope

This review records the finished source-independent Lean seam for the same-curvature shared-`r` optimizer from 狂蛮魔尊's `T-P5-047` mathematics.  It does **not** claim the full necessity/completeness direction of the five-candidate theorem, source binding, Float64/controller semantics, P8 coverage, P5/P8/M4 closure, registry admission, or final integration.

Formalization artifact:

```text
examples/routeb_p5_shared_r_optimizer_lean/
  P5SharedROptimizer.lean
  README.md
  lean-toolchain
  verify.sh
```

The verifier is portable (`CI_PORTABLE=1`), resolves `lake`/`lean` from `PATH`, reuses the pinned `examples/local_fkg/lake-manifest.json`, checks the toolchain match, rejects `sorry`/`admit`, compiles with `-DwarningAsError=true`, and audits every public target theorem for `sorryAx`.

## 1. Kernel-facing theorem decomposition

The sidecar contains 17 public target theorems:

```text
same_curvature_difference_affine
same_curvature_vertex_square
scaled_vertex_value
scaled_difference_at_vertex_one
scaled_difference_at_vertex_two
shared_positive_of_active_vertex_one
shared_positive_of_active_vertex_two
crossover_inside_of_endpoint_sign_change
crossover_value_scaled
crossover_gate_equality
shared_positive_of_crossover
p5_barrier_parameter_difference_cancels
separated_regression_each_passes
shared_regression_positive_implies_eps_gt_sixteenth
eps_one_hundred_no_shared_witness
eps_one_sixteenth_boundary
eps_one_tenth_crossover_margin
```

The formalized content covers:

- exact affine difference for two concave gates with common curvature;
- denominator-cleared vertex completion-of-square and scaled vertex value;
- division-free active-vertex guards that construct an explicit shared strict witness in `[0,1]`;
- endpoint sign-change implying a strict interior crossover;
- square-root-free scaled crossover value and crossover equality;
- an explicit shared crossover witness under the polynomial positivity guard;
- exact cancellation of the common P5 determinant term in the two barrier margins;
- the shifted-square regression family proving that two independently feasible gates need not admit one shared `r`, including the exact `eps=1/100` obstruction, `eps=1/16` boundary, and `eps=1/10` positive crossover margin.

The deliberately unformalized theorem is the global equivalence

```text
shared positive witness iff L or R or V1 or V2 or X.
```

The present sidecar proves the nontrivial constructive/sufficiency seams and the regression obstruction, but leaves `FIVE_CANDIDATE_NECESSITY_COMPLETENESS=OPEN` rather than silently asserting the missing interval-case exhaustiveness.

## 2. Lean repair made before CI receipt

Commit

```text
b81904adc6a1f890065940d4426f04666a0e75ec
```

contains the final narrow Lean repair.  The patch kept the mathematical statements unchanged and fixed proof-script/toolchain issues only:

- removed redundant `ring` calls after `field_simp` where the goal was already discharged;
- removed the unused local `hden` rejected by `warningAsError`;
- added the missing `ring` normalization in `crossover_gate_equality`;
- made the `q=0` contradiction in `shared_positive_of_crossover` explicit by rewriting `hq0` into the sign hypothesis before `nlinarith`;
- replaced the regression proof sequence with `simpa using And.intro heps heps` to avoid tactic/linter fragility.

No theorem was weakened to make compilation succeed.

## 3. Real GitHub Actions evidence

Pinned GitHub-hosted verification at the inspected commit:

```text
workflow: Lean agent sidecars
run_id: 34185460045
job_id: 101932791127
head_sha: b81904adc6a1f890065940d4426f04666a0e75ec
runner: ubuntu-24.04
Lean: 4.32.0
Lake: 5.0.0-src+8c9756b
Mathlib revision: 81a5d257c8e410db227a6665ed08f64fea08e997
```

For this sidecar the actual job log reports:

```text
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
P5_SHARED_R_OPTIMIZER_FOCUSED_CHECK=PASS
FIVE_CANDIDATE_SUFFICIENCY_SEAMS=true
FIVE_CANDIDATE_NECESSITY_COMPLETENESS=OPEN
SEPARATE_PASS_DOES_NOT_IMPLY_SHARED_PASS=true
SOURCE_BINDING=OPEN
FLOAT64_CONTROLLER_SEMANTICS=OPEN
P8_SAME_DOMAIN_COVERAGE=OPEN
P5_P8_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_shared_r_optimizer_lean/verify.sh
```

Every one of the 17 target theorem `#print axioms` reports only:

```text
[propext, Classical.choice, Quot.sound]
```

There is no `sorryAx` in this lane.

The **shared workflow conclusion is still failure**, but that conclusion is not caused by `T-P5-047`.  The same job contains failures in other independent portable lanes (including legacy FLT path handling, M4 cross-branch, P5 componentwise/direct-two-channel/parameter-tube/weighted-dual, P7 tail-Schur, and P8 ramp-reconstruction).  This review therefore records a focused PASS for `routeb_p5_shared_r_optimizer_lean`, not a green result for the aggregate workflow.

## 4. Remaining formalization / interface boundary

Still open and not claimed here:

```text
FIVE_CANDIDATE_NECESSITY_COMPLETENESS=OPEN
SOURCE_BINDING=OPEN
FLOAT64_CONTROLLER_SEMANTICS=OPEN
P8_SAME_DOMAIN_COVERAGE=OPEN
P5_P8_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
```

In particular, a downstream checker may consume the currently kernel-checked explicit candidate seams, but it must not yet replace the mathematical `iff` in the T-P5-047 review with a Lean-certified equivalence.  Either the necessity/exhaustiveness theorem must be formalized independently, or the checker contract must clearly expose these as sufficient candidate branches only.

## 5. Status

`admission_label = compiled_candidate` for the source-independent T-P5-047 Lean seam only.

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
