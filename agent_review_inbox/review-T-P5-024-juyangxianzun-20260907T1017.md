---
kind: review_result
review_id: review-T-P5-024-juyangxianzun-20260907T1017
task_id: T-P5-024
source_agent: 巨阳仙尊
agent: 巨阳仙尊
claimed_at: 2026-09-07T09:56:00-06:00
created_at: 2026-09-07T10:17:00-06:00
upstream_review: review-T-P5-024-kuangmanmozun-20260907T0945.md
inspected_commit: ac041a6639b6fff9341947d357dd0edc2c815561
integration_status: pending
admission_label: compiled_candidate
proposed_integration_target: theorem
requested_action: independent_verify_then_coordinator_harvest_without_source_or_registry_promotion
---

# T-P5-024 — Lean formalization of the joint centered residual metric

## Result

The source-independent mathematics from 狂蛮魔尊's `T-P5-024` review is now a
portable Lean 4.32.0 sidecar:

```text
examples/routeb_p5_joint_centered_gain_lean/
  P5JointCenteredGain.lean
  README.md
  lean-toolchain
  verify.sh
```

The focused sidecar compiles in the repository's real GitHub pinned environment
with `-DwarningAsError=true` and reports

```text
AXIOM_AUDIT=PASS
P5_JOINT_CENTERED_GAIN_FOCUSED_CHECK=PASS
SIDECAR_RESULT=PASS path=examples/routeb_p5_joint_centered_gain_lean/verify.sh
```

This result formalizes only the exact block-(4,5) algebra, its centered
small-gain consumer, exact checker arithmetic, and the rational regression
counterexample.  It does not prove a concrete source Jacobian/increment bound,
T-P5-023 cell/path coverage, anchor-bias closure, P8 flowpipe coverage, ODE
continuation, P5/P8/M4 closure, provenance, admission, or registry promotion.

## Mathematical contract formalized

The sidecar defines

```text
N = x4^2 + x5^2 + y4^2 + y5^2
U = (x4+y4)^2 + (x5+y5)^2

Q = (3/4)x4^2 + (29/50)x5^2 - (3/200)x4*x5
  + (2049997/3000000)y4^2
  + (2399261/4000000)y5^2
  + (1/400)x4*y5 - (1/400)x5*y4.
```

The core compiled theorem is

```lean
block45_joint_residual_metric
```

with statement

```text
25 * U * N <= 144 * Q^2.
```

This is the joint metric from `T-P5-024`; it is strictly stronger, at the
checker-constant level, than composing the older separate `U <= (17/5)Q` and
`N <= (160/457)Q` bounds.

## Exact LDL/SOS theorem decomposition

Rather than importing an opaque matrix-positive-definite premise, the sidecar
formalizes the key quadratic comparison directly as an exact rational SOS.
Define

```text
w1 = x4 - (63/2575)x5 - (49/103)y4 + (21/5150)y5
w2 = x5 - (208425/5899112)y4 - (6307427/5899112)y5
w3 = y4 - (282250198125/10550522799949)y5
w4 = y5.
```

Lean proves the exact identity

```text
(24/5)Q - (7/10)U - (10/7)N
=
(103/70) w1^2
+ (1474778/2253125) w2^2
+ (10550522799949/12904307500000) w3^2
+ (302371148712671469/184634148999107500000) w4^2.
```

Every displayed coefficient is positive, so the public theorem

```lean
joint_quadratic_comparison
```

proves

```text
(7/10)U + (10/7)N <= (24/5)Q.
```

Separately,

```lean
weighted_amgm_7_10
```

proves the exact weighted square inequality

```text
4 U N <= ((7/10)U + (10/7)N)^2
```

from the nonnegativity of `((7/10)U-(10/7)N)^2`.  The combination yields
`25 U N <= 144 Q^2` without a square root, spectral norm, floating-point
constant, or imported matrix inverse.

The same comparison also gives the standalone compiled theorem

```lean
qDissipation_nonneg
```

so the downstream absolute-value consumer has the required sign premise on
`Q` internally rather than asking the checker to restate it.

## Centered small-gain consumer

The generic theorem

```lean
centered_small_gain_joint
```

accepts

```text
U >= 0,
Q >= 0,
ell2 >= 0,
mu >= 0,
rcSq <= ell2*N,
coupling^2 <= U*rcSq,
25*U*N <= 144*Q^2,
144*ell2 <= 25*mu^2
```

and proves

```text
|coupling| <= mu*Q.
```

The checker-facing specialization

```lean
block45_centered_small_gain
```

instantiates `U,N,Q` with the exact Route-B block forms and consumes only

```text
rcSq <= ell2*N,
coupling^2 <= U*rcSq,
144*ell2 <= 25*mu^2,
ell2 >= 0,
mu >= 0.
```

No source semantics are hidden in this theorem: `rcSq` and the coupling bound
remain explicit premises.

Two additional pure consumers are compiled:

```lean
centered_no_bias_decay
centered_no_bias_strict_decay
```

They show that once the centered coupling obeys `|coupling|<=mu*Q`, a
no-anchor-bias derivative estimate `Vdot <= -Q + |coupling|` leaves
`Vdot <= -(1-mu)Q`, and gives `Vdot<0` when `mu<1` and `Q>0`.

## Exact checker arithmetic and regression witness

The sidecar also compiles

```lean
gain_improvement_exact
```

with

```text
(25/144)/(457/2720) = 4250/4113 > 1,
25/144 - 457/2720 = 137/24480.
```

For the common choice `mu=1/2`, theorem

```lean
half_gain_checker_constants
```

proves the exact equivalences

```text
2720*ell2 <= 457*(1/2)^2  <-> 10880*ell2 <= 457,
144*ell2  <= 25*(1/2)^2   <-> 576*ell2 <= 25.
```

Finally,

```lean
counterexample_23_quarter
```

formalizes the rational state `(x4,x5,y4,y5)=(0,15,0,14)`:

```text
N = 421,
U = 841,
Q = 248063789/1000000,
4*U*N - 23*Q^2 = 924201500160017/1000000000000 > 0.
```

Thus the stronger universal candidate `4UN <= 23Q^2` is formally ruled out by
an exact rational witness; the sidecar does not overstate the joint constant.

## Lean / CI repair loop

The first real GitHub compilation was:

```text
Lean agent sidecars
run: 34141335894
job: 101803840936
head: fc37dceca16f676ca0bc7864444899a3d83533f1
Lean: 4.32.0
```

It exposed two concrete proof-script defects:

```text
P5JointCenteredGain.lean:124:2: `dsimp` made no progress
P5JointCenteredGain.lean:224:34: linarith failed to find a contradiction
```

The first left `sorryAx` in `block45_joint_residual_metric` and therefore in
`block45_centered_small_gain`; the second left `sorryAx` in
`half_gain_checker_constants`.

The fixes were mathematical/proof-local rather than linter suppression:

1. the final joint-metric step now proves a local theorem
   `25*U*N <= 144*Q^2` before `simpa [U,N,Q]`, avoiding the no-progress
   `dsimp` on the outer goal;
2. each direction of the two checker equivalences now explicitly introduces
   its implication hypothesis before `nlinarith`.

Fix commit:

```text
49f53d40f726e74380dc8e9089116e65de717395
```

That direct run was superseded/cancelled during concurrent repository activity,
but the immediately following merge head contains the fix as a parent and
compiled it in the real portable workflow:

```text
compiled head: ac041a6639b6fff9341947d357dd0edc2c815561
Lean agent sidecars
run: 34141997761
job: 101805907409
runner: ubuntu-24.04
Lean: 4.32.0
Lake: 5.0.0-src+8c9756b
Mathlib revision used by local_fkg: 81a5d257c8e410db227a6665ed08f64fea08e997
```

The log for this sidecar prints all twelve theorem axiom reports, each exactly
with

```text
[propext, Classical.choice, Quot.sound]
```

and then

```text
AXIOM_AUDIT=PASS
P5_JOINT_CENTERED_GAIN_FOCUSED_CHECK=PASS
SIDECAR_RESULT=PASS path=examples/routeb_p5_joint_centered_gain_lean/verify.sh
```

There is no `sorryAx` in this sidecar.

The shared workflow remains red for independent lanes.  In the same real log,
examples include the pre-existing FLT quotient relative-path failure and the
old `routeb_p5_weighted_dual_residual_lean` zero-kappa errors; concurrent new
sidecars also have their own Lean errors (`routeb_m4_cross_branch_budget_lean`,
`routeb_p5_componentwise_relative_decay_lean`, and
`routeb_p7_tail_schur_completion_lean`, plus a concurrently modified
`routeb_p8_ramp_reconstruction_sidecar`).  None is in `T-P5-024`; this round
did not preempt their owners.

## Portable verification contract

`verify.sh` contains `CI_PORTABLE=1`, locates `lake` from `PATH`, verifies the
sidecar `lean-toolchain` against `examples/local_fkg/lean-toolchain`, requires
the pinned `lake-manifest.json`, compiles with

```text
lake env lean -DwarningAsError=true P5JointCenteredGain.lean
```

and rejects missing expected axiom reports, `sorryAx`, generic unexpected axiom
diagnostics, unknown-module errors, or Lean `error:` output.  No
machine-specific absolute path is used.

## Remaining formalization / source obligations

The compiled theorem starts after source/path geometry.  The remaining
obligations are therefore sharply separated:

1. `T-P5-023` (or an equivalent source theorem) must provide a same-cell /
   same-path centered increment bound yielding the concrete `ell2` premise;
2. Julia/DH/Float64/controller/solve pieces that are not justified by a smooth
   exact-real Jacobian must receive their own centered-increment bounds rather
   than being silently folded into `ell2`;
3. any nonzero anchor residual remains additive bias and needs its separate
   `B2` / discriminant / barrier ledger; it is not covered by this homogeneous
   centered theorem;
4. the resulting source bound and nominal trajectory/tube must live on the
   same P8 domain;
5. initial-state binding, ODE existence/continuation, and first-exit/flowpipe
   coverage remain outside this algebraic sidecar.

## Admission boundary

`compiled_candidate` only.

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**.  No P5/P8/M4 or registry
status is changed by this review.
