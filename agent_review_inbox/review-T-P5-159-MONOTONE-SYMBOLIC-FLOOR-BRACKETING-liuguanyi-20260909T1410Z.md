---
kind: review_result
review_id: review-T-P5-159-monotone-symbolic-floor-bracketing-liuguanyi-20260909T1410Z
task_id: T-P5-159-MONOTONE-SYMBOLIC-FLOOR-BRACKETING
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T14:10:00Z
claim_commit: ad5f7ca962580f82b1ce6bf0ff8d584a02100b26
inspected_commit: 56d393af62f2437a82eb43d68ae1c7c1c768bdd5
upstream_commits:
  - c9b94c1f931c76c20a0f22e428425a4d659b57bb  # T-P5-154 fixed-D copositive matrix
  - fce11e2368dfd33d225a49adfbeb4a880a7c01ae  # T-P5-158 exact fixed-D support/KKT decision
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: use_monotone_floor_interval_as_the_symbolic_D_bridge; keep_T158_as_fixed_rational_decider; allow_rational_PASS_FAIL_brackets_when_the_sharp_floor_is_algebraic_or_irrational; use_active_support_kernel_only_as_a_sharpness_candidate_not_source_admission
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional real/rational algebra only
exit_code: n/a
---

# T-P5-159 — monotone symbolic-floor bracketing and active-support singularity

## 0. Verdict and seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-154 turns a fixed additive floor `D` into copositivity of a rational matrix `M_D`. T-P5-158 then gives an exact fixed-`D` support/KKT decision procedure, but explicitly leaves symbolic optimization over `D` open because the joint equations look bilinear.

The smallest useful bridge is not to force symbolic `D` into the fixed-floor LP. The family has an additional one-dimensional monotonic structure:

`q_D(lambda) = Delta(lambda) + D g_lambda`, with `g_lambda>0`.

This child proves that the valid floors form one upward interval, identifies the exact sharp floor as a generalized nonnegative-orthant Rayleigh quotient, shows that a sharp active support forces a **zero-level kernel** of a principal `M_D` block, and gives a rational PASS/FAIL bracketing protocol that consumes T-P5-158 without ever requiring the sharp floor itself to be rational.

A two-vertex rational example has sharp floor `3-2*sqrt(2)`, so any interface demanding an exact rational optimizer is mathematically over-constrained.

No source/provenance audit, runtime/Float64 claim, registry mutation, Lean compile, or independent validation is performed.

---

## 1. Setup inherited from T-P5-154

Let the uncertainty simplex be

`Delta_N = {lambda_i>=0, sum_i lambda_i=1}`,

with rational or real data

`g_i>0`,

and symmetric pair coefficients `K_ij=K_ji`, `K_ii=0`.

Define

`g_lambda = sum_i g_i lambda_i > 0`,

`Delta(lambda) = sum_{i<j} K_ij lambda_i lambda_j`,

and

`q_D(lambda) = Delta(lambda) + D g_lambda`.

For homogeneous `x>=0`, `x!=0`, define

`Q_0(x)=sum_{i<j}K_ij x_i x_j`,

`L(x)=(sum_i x_i)(sum_i g_i x_i)>0`.

Then T-P5-154's homogenization is exactly

`x^T M_D x = Q_0(x)+D L(x)`.

On the simplex this reduces to `q_D(lambda)`.

Call `D` **valid** when `D>=0` and `q_D(lambda)>=0` for every simplex `lambda`.

---

## 2. Monotonicity: valid floors form an upward interval

### Theorem T159-A — `uniform_floor_monotone`

If `D_2>=D_1`, then for every simplex point

`q_{D_2}(lambda) = q_{D_1}(lambda) + (D_2-D_1) g_lambda`.

Since `g_lambda>0`:

1. if `D_1` is valid, every `D_2>=D_1` is valid;
2. if `D_1` fails at `lambda`, every `D_0<=D_1` fails at the same `lambda`;
3. if `q_D(lambda)=0`, then every `D'<D` fails at the same `lambda`.

So the valid set is either empty or an interval `[D_*,infinity)`.

It is not empty: for example any `U>=0` satisfying the finite coefficient gates

`K_ij + U(g_i+g_j) >= 0` for every `i<j`

is valid, because T-P5-154 expands

`q_U(lambda)`

as a sum of the nonnegative diagonal terms `U g_i lambda_i^2` and the nonnegative cross terms `[K_ij+U(g_i+g_j)]lambda_i lambda_j`.

Hence a finite least valid floor `D_*` always exists for finite data with `g_i>0`.

### Interface consequence

A checker never needs a symbolic copositivity oracle over `(D,lambda)`. It may keep a scalar bracket `L<=D_*<=U` and use the exact fixed-rational T-P5-158 checker at rational test values.

---

## 3. Exact generalized-Rayleigh formula for the sharp floor

Because the simplex is compact and

`g_lambda >= min_i g_i > 0`,

the continuous ratio

`R(lambda) = -Delta(lambda)/g_lambda`

attains a maximum.

### Theorem T159-B — `sharp_floor_eq_simplex_ratio`

The least valid floor is

**`D_* = max(0, max_{lambda in Delta_N} [-Delta(lambda)/g_lambda])`.**

Equivalently, in homogeneous coordinates,

**`D_* = max(0, sup_{x>=0,x!=0} [-Q_0(x)/L(x)])`.**

Proof is immediate from

`q_D(lambda)>=0  <=>  D >= -Delta(lambda)/g_lambda`

for each fixed `lambda`, followed by maximization over the simplex.

This formula is exact and makes the geometry clear: the symbolic floor is a generalized Rayleigh quotient on the nonnegative orthant, not a generic unconstrained eigenvalue.

---

## 4. A fixed-D FAIL witness gives a stronger lower bound

T-P5-158 returns, on failure of a rational fixed floor `D_0`, a rational support witness `lambda` and a negative value

`alpha = q_{D_0}(lambda) < 0`.

For the same physical simplex point,

`q_L(lambda) = alpha + (L-D_0) g_lambda`.

### Theorem T159-C — `fail_witness_continuation_lower_bound`

If a proposed scalar `L` satisfies

`alpha + (L-D_0) g_lambda <= 0`,

then

**`L <= D_*`.**

If equality holds, then the same witness is exactly zero at `L`, and every `D<L` is strictly invalid.

The strongest continuation value is

`L_w = D_0 - alpha/g_lambda`,

which is rational whenever `D_0`, `alpha`, `g_i`, and `lambda_i` are rational.

The trusted interface does not need division: a producer may propose rational `L_w`, and the checker verifies only

`g_lambda>0`,

`alpha + (L_w-D_0) g_lambda = 0`.

Thus a T-P5-158 FAIL branch is more informative than the boolean statement `D_0<D_*`: it yields an exact signed lower-floor extrapolation.

---

## 5. PASS + zero witness proves exact sharpness

### Theorem T159-D — `valid_floor_with_zero_witness_is_sharp`

Assume `D>=0` is valid and there exists a simplex point `lambda` with

`q_D(lambda)=0`.

Then

**`D=D_*`.**

Indeed, for every `D'<D`,

`q_{D'}(lambda)=-(D-D')g_lambda<0`,

so no smaller floor can be valid.

This gives a very small exact sharpness packet:

1. one fixed-`D` copositivity PASS;
2. one same-`D` nonnegative zero witness.

No optimizer trace is mathematically necessary.

---

## 6. At a positive sharp floor, an active support is singular

Let `D_*>0`, and let `lambda_*` attain the ratio in T159-B. Then

`q_{D_*}(lambda_*)=0`.

Let

`S={i: lambda_{*,i}>0}`.

On the relative interior of the face `Delta_S`, `lambda_*` minimizes `q_{D_*}` with minimum zero. Therefore every tangent direction `v` with `1_S^T v=0` satisfies

`v^T M_{D_*,SS} lambda_{*,S}=0`.

Hence

`M_{D_*,SS} lambda_{*,S}=a 1_S`

for some scalar `a`. Multiplying by `lambda_{*,S}^T` gives

`a = lambda_*^T M_{D_*} lambda_* = 0`.

So:

### Theorem T159-E — `sharp_floor_has_positive_support_kernel`

For every positive sharp floor there exists a support `S` and a vector

`lambda_S>0`, `1_S^T lambda_S=1`

such that

**`M_{D_*,SS} lambda_S = 0`.**

In particular,

**`det(M_{D_*,SS})=0`.**

The support cannot be a singleton when `D_*>0`, because its diagonal entry is `D_* g_i>0`.

### Converse sharpness certificate

If a candidate `D` is already fixed-D valid and some support has a positive normalized kernel vector

`M_{D,SS} lambda_S=0`,

then T159-D shows immediately that `D` is the exact sharp floor.

This is the useful symbolic bridge: the sharp floor is selected by a principal-face zero mode, while global validity is still checked by the fixed-D copositivity machinery.

---

## 7. Algebraicity of the sharp floor

Every entry of `M_D` is affine in `D`. For a support `S`,

`p_S(D)=det(M_{D,SS})`

is therefore a polynomial in `D` of degree at most `|S|`.

If the source `g_i,K_ij` are rational, every coefficient of `p_S` is rational.

By T159-E, every positive sharp floor is a real root of at least one nonzero principal determinant polynomial, unless that determinant polynomial vanishes identically, in which case one may use the corresponding lower-rank kernel equations directly.

Therefore the symbolic optimum is generally an **algebraic number**, not necessarily a rational number.

A safe finite candidate architecture is:

`support S -> real root candidate of p_S -> positive kernel candidate -> fixed-D global copositivity check`.

But the repository does not need to represent those algebraic roots exactly in order to certify useful rational floors; the rational bracketing route below is simpler and fail-closed.

---

## 8. Rational data can have an irrational exact floor

Take two vertices with

`g_1=1`, `g_2=2`, `K_12=-1`.

Write `lambda=(t,1-t)`. Then

`q_D(t)`

`= -t(1-t) + D[t+2(1-t)]`

`= t^2 -(1+D)t + 2D`.

For `0<=D<=1/3`, the quadratic minimum lies in the open edge. Since the leading coefficient is `1`, edge validity is equivalent to nonpositive discriminant:

**`D^2 - 6D + 1 <= 0`.**

The least valid value is therefore the smaller root

**`D_* = 3 - 2 sqrt(2)`.**

This is irrational, although every input coefficient is rational.

The maximizing simplex point is

`t_*=2-sqrt(2)`,

and the ratio is

`t_*(1-t_*)/(2-t_*) = 3-2sqrt(2)`.

For `D>=1/3`, the cross coefficient `-1+3D` is already nonnegative, so validity is trivial by the coefficient gate; hence the smaller root is indeed the global sharp floor.

### Hard protocol consequence

A source/checker contract that requires the **sharp** uniform floor to be represented as an exact rational number is incorrect in general. The correct exact-rational interface is a certified bracket or a rational safe upper floor, with the real sharp value remaining an algebraic mathematical object.

---

## 9. General two-vertex root-free threshold gate

Take

`g_1,g_2>0`,

`K_12=-kappa`, `kappa>0`.

On the edge `lambda=(t,1-t)`,

`q_D(t)=kappa t^2 + [D(g_1-g_2)-kappa]t + D g_2`.

If

`0<=D` and `D(g_1+g_2)<=kappa`,

the quadratic vertex lies inside `[0,1]`. Its discriminant is

**`P(D)=(g_1-g_2)^2 D^2 - 2 kappa(g_1+g_2)D + kappa^2`.**

Therefore in this branch

**edge valid iff `P(D)<=0`.**

If instead

`D(g_1+g_2)>=kappa`,

then the cross coefficient `-kappa+D(g_1+g_2)` is nonnegative, so the edge is automatically valid coefficientwise.

This gives a completely root-free exact rational gate for a proposed rational `D`.

Moreover, in the small-`D` branch with `P(D)>0`, the rational vertex

`t_v=[kappa-D(g_1-g_2)]/(2kappa)`

is an explicit FAIL witness and

`q_D(t_v) = -P(D)/(4kappa) < 0`.

Again the checker can clear the positive denominator instead of dividing.

---

## 10. Exact rational bracketing protocol

Assume `g_i,K_ij` are rational.

### Initial upper bound

Propose any rational `U>=0` satisfying

`K_ij + U(g_i+g_j)>=0`

for all pairs. T159-A proves `U` valid. This is finite and uses only multiplication/addition/sign checks.

### Lower bound

Run the T-P5-158 exact checker at `D=0` or any rational trial `D_0`.

- If PASS, `D_*<=D_0`.
- If FAIL with rational `(lambda,alpha)`, use T159-C to produce a rational lower continuation `L_w` by the signed equation

  `alpha+(L_w-D_0)g_lambda=0`.

Then `L_w<=D_*`.

### Bisection / support-guided refinement

Given rational `L<=D_*<=U`, test the rational midpoint `m=(L+U)/2` with T-P5-158.

- PASS: set `U:=m`;
- FAIL: at minimum set `L:=m`, or use the stronger witness-continuation lower bound from T159-C.

Ignoring witness acceleration, the interval width halves every round. Hence for every rational tolerance `eps>0`, finitely many exact fixed-floor checks produce

`L<=D_*<=U`, `U-L<=eps`.

No numerical copositivity oracle, irrational arithmetic, eigenvalue computation, or symbolic bilinear optimization is required for this certified approximation.

---

## 11. Minimal theorem statements for formalization

A Lean-facing implementation should avoid defining the sharp floor by a fragile executable minimizer. A relational API is enough.

### `validFloor`

`ValidFloor D := 0<=D and forall lambda in simplex, Delta lambda + D*g lambda >=0`.

### T159-L1 — monotonicity

`ValidFloor D1 -> D1<=D2 -> ValidFloor D2`.

### T159-L2 — signed witness lower bound

If `lambda` is simplex, `q_D0(lambda)=alpha`, `alpha<0`, and

`alpha+(L-D0)g_lambda<=0`,

then every valid floor is `>=L`.

### T159-L3 — sharpness from a zero witness

`ValidFloor D` plus simplex `lambda` with `q_D(lambda)=0` implies

`forall D'<D, not (ValidFloor D')`.

### T159-L4 — active-support kernel

If `D>0` is the least valid floor, there exists nonempty support `S` and positive normalized `lambda_S` with

`M_D,SS * lambda_S = 0`.

This theorem is the only one that needs compactness/attainment and face-tangent calculus. L1-L3 are elementary ordered-field algebra.

### T159-L5 — two-vertex polynomial gate

Under `g1,g2,kappa>0`, `0<=D`, `D(g1+g2)<=kappa`, edge validity is equivalent to

`(g1-g2)^2 D^2 - 2kappa(g1+g2)D + kappa^2 <=0`.

This is a useful root-free regression theorem.

---

## 12. Dependencies and non-overlap

This result consumes only:

- T-P5-154's exact identity defining `M_D` and `q_D`;
- T-P5-158's fixed-rational PASS/FAIL support checker as an optional downstream decision engine.

It does **not** duplicate:

- T-P5-155's three-vertex closed form;
- T-P5-157's four-vertex face/KKT closure;
- T-P5-158's support enumeration or LP-margin proof.

Instead it supplies the missing one-dimensional `D` bridge around those fixed-floor tools.

---

## 13. Open boundaries

1. **Actual source equality is open.** No deployed reset/cell packet has been identified with a concrete `g_i,K_ij` family here.
2. **Physical cell/boundary attainability is open.** The copositive floor is only the algebraic robust-reset child inherited from T-P5-154.
3. **Algebraic-root isolation is not implemented.** The theorem shows why it is possible, but the recommended trusted route is rational bracketing through fixed-`D` decisions.
4. **Degenerate determinant families need a rank/kernel branch.** `det(M_D,SS)` may vanish identically; determinant roots alone must never be treated as a complete support checker.
5. **Infinite uncertainty sets remain outside scope.** They still require finite simplex/polytope reduction or another compactness theorem.
6. **No Lean/kernel receipt was run.** Candidate theorem statements remain mathematical children.
7. **No admission, registry, P4/P5 parent, P8, or M4 state is changed.**

---

## 14. Recommended next interface

For a real source-bound robust-reset family, the smallest reusable packet is:

`(parameterKey, cellKey, g_i, K_ij, D_trial)`

plus either

- fixed-`D_trial` PASS evidence, or
- fixed-`D_trial` FAIL witness `(S,lambda,alpha)`.

The consumer should maintain a signed rational interval `[L,U]` for the sharp floor. On FAIL, preserve `alpha` and `g_lambda` and update the lower side using

`alpha+(L_new-D_trial)g_lambda=0`

before any absolute enclosure. On PASS, update only the upper side. If a same-`D` positive kernel witness appears together with global PASS, T159-D/E upgrades that `D` to an exact mathematical sharp floor, but source/coverage/admission gates remain separate.

Current status remains **pending** until actual same-key source and physical-domain packets, Lean/kernel validation, and the repository's normal independent gates are supplied.