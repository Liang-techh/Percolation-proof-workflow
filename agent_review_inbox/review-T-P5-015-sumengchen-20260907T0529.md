---
kind: review_result
review_id: review-T-P5-015-sumengchen-20260907T0529
task_id: T-P5-015
source_agent: 苏梦辰
parent_reviews:
  - review-T-P5-015-guyuefangyuan-20260907T0438
integration_status: compiled_candidate
admission_label: pending
proposed_integration_target: theorem
created_at: 2026-09-07T05:29:00-06:00
---

# T-P5-015 formalization result — damping-split certificate

## Scope

Formalized the source-independent scalar mathematics from 古月方源's `T-P5-015` review. This result does **not** bind source values, IEEE/solve semantics, P8 coverage, registry admission, or final P5/M4 status.

## Portable Lean sidecar

Path:

`examples/routeb_p5_damping_split_lean/`

Files:

- `P5DampingSplit.lean`
- `README.md`
- `verify.sh`
- `lean-toolchain` pinned to `leanprover/lean4:v4.32.0`

`verify.sh` is CI-portable (`CI_PORTABLE=1`), obtains `lake`/`lean` from `PATH`, checks the local-FKG toolchain, compiles with `-DwarningAsError=true`, checks every exported theorem's `#print axioms`, and rejects `sorryAx`.

## Kernel statements implemented

### 1. Generic division-free damping split

`damping_split_certificate`

Assumptions:

- `Q > 0`, `g0 > 0`, `alpha < 1`,
- `4 Q (1-alpha) g0 E + Q T Rbar < 4 alpha^2 (1-alpha) g0^3`.

Conclusion:

`E + T * (Rbar / (4 * ((1-alpha)*g0))) < alpha^2 * g0^2 / Q`.

This is the source-independent checker-to-headroom bridge. The proof clears denominators only under the required positivity and does not add spurious nonnegativity hypotheses on `E,T,Rbar`.

### 2. Exact `2/3 : 1/3` rational specialization

Implemented:

- `two_thirds_checker_to_generic`
- `two_thirds_split_certificate`

The checker-facing certificate is exactly

`36 Q g0 E + 27 Q T Rbar < 16 g0^3`.

It implies the generic headroom inequality at `alpha = 2/3`.

### 3. Dominance over the old half split

`two_thirds_dominates_half`

For nonnegative physical loads, the old condition

`4 Q g0 E + 2 Q T Rbar < g0^3`

implies the new `2/3` certificate

`36 Q g0 E + 27 Q T Rbar < 16 g0^3`.

Also implemented:

- `two_thirds_strictly_better_than_half`: for every `e >= 0`, `H_e(1/2) < H_e(2/3)`;
- `half_rejects_two_thirds_accepts_counterexample`: exact rational witness `e=0`, `rho=7/50`, showing the old half split can reject an instance admitted by `2/3`.

### 4. Calculus-free stationary optimizer algebra

Implemented:

- `split_objective_stationary_identity`
- `stationary_witness_maximizes`
- `stationary_objective_value`

For `H_e(alpha)=(1-alpha)(alpha^2-e)` and a stationary witness satisfying

`e = 3 s^2 - 2 s`, 

Lean proves the exact factorization

`H_e(s) - H_e(alpha) = (alpha-s)^2 * (2s+alpha-1)`.

Thus if `s >= 2/3` and `alpha >= 0`, then `H_e(alpha) <= H_e(s)` without differentiation or square roots. Lean also proves the exact stationary value

`H_e(s)=2s(1-s)^2`.

### 5. Current C-FD integer reduction

Implemented:

- `cfd_integer_certificate_implies_two_thirds`
- `t1_cfd_two_thirds_certificate`

With

`Q = 13*S_F / 72000000000000000`,

the exact integer certificate

`52 S_F g0 E + 39 S_F T Rbar < 128000000000000000 g0^3`

implies the rational `2/3` checker certificate. The `T=1`, `E=Z0+Hbar` specialization is also kernel-checked:

`52 S_F g0 (Z0+Hbar) + 39 S_F Rbar < 128000000000000000 g0^3`.

## Real GitHub Actions compile/fix loop

The sidecar was not treated as complete until it survived the repository's real portable-sidecar workflow.

1. **Run `34115608413`, job `101721649335`**: the first implementation failed in `damping_split_certificate` because Lean 4.32 could not synthesize the ordered multiplication instance for a direct `mul_lt_mul_left` cancellation (`MulRightStrictMono ℝ`). Replaced the cancellation with a contradiction + `mul_le_mul_of_nonneg_left` proof.

2. **Run `34115990970`, job `101722803070`**: all target theorems typechecked and printed only standard axioms, but `-DwarningAsError=true` rejected a redundant trailing `ring` after `field_simp` (`'ring' tactic does nothing`). Removed the redundant tactic rather than disabling the linter.

3. **Run `34116404083`, job `101724144187`**: target sidecar passed:

   - `AXIOM_AUDIT=PASS`
   - `P5_DAMPING_SPLIT_FOCUSED_CHECK=PASS`
   - `SIDECAR_RESULT=PASS path=examples/routeb_p5_damping_split_lean/verify.sh`

All 11 exported theorems printed only

`[propext, Classical.choice, Quot.sound]`

and no target theorem depends on `sorryAx`.

The aggregate portable-sidecars job is still red for **unrelated pre-existing sidecars**:

- `examples/anthropic_flt_quotient_transport_sidecar/verify.sh`: bad `../local_fkg` relative path;
- `examples/routeb_p5_weighted_dual_residual_lean/`: existing unused `hκ1`, invalid disjunction projection, and `sorryAx` in the zero-κ branch.

Those are not part of `T-P5-015` and were not taken over in this claim.

## Interface boundary / remaining blockers

This formalization closes only the scalar damping-allocation algebra. P5 still needs external evidence for:

1. exact source/checker binding of `S_F` and hence `Q`;
2. source-domain values/bounds for `Z0`, `Hbar`, and weighted-dual `Rbar`;
3. runtime Float64/controller/linear-solve remainder semantics;
4. first-exit / ODE existence-continuation theorem on the actual trajectory;
5. P8 same-domain ramp/flowpipe coverage.

No registry, DAG-final-state, admission, or overall P5/M4 conclusion was modified.

**Status: `compiled_candidate` — 待封不觉独立验证 / 待梁智炜最终整合。**
