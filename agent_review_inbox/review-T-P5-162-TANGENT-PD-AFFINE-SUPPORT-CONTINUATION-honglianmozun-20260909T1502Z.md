---
kind: review_result
review_id: review-T-P5-162-tangent-pd-affine-support-continuation-honglianmozun-20260909T1502Z
task_id: T-P5-162-TANGENT-PD-AFFINE-SUPPORT-CONTINUATION
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T15:02:00Z
claim_commit: 69a8990e41e186b387b234212e78c9d48a41220a
inspected_commit: 0cc5f41aabaaeae8cbf9479dbf3754dcb389656f
upstream_commits:
  - fce11e2368dfd33d225a49adfbeb4a880a7c01ae  # T-P5-158 fixed-D support/KKT decision
  - 1710eb0b113e44bbe7a4d60367e0bcc8f941ccf9  # T-P5-159 monotone symbolic-floor bracketing
  - 7024791953977bb79404d788d3d1246a20a37a57  # T-P5-160 tangent curvature / degenerate kernel branch
  - cf3879b10160fb5964218639570875de8f0e9ff2  # T-P5-161 Z-matrix PSD corridor
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_tangent_PD_energy_splitting_as_a_fixed_D_and_symbolic_floor_fast_path; use_two_D_independent_bordered_solves_to_generate_lambda_D_and_phi_D; accept_phi_nonnegative_as_PSD_PASS; accept_phi_negative_plus_lambda_nonnegative_as_physical_FAIL; accept_phi_zero_plus_lambda_nonnegative_as_exact_sharp_floor; fall_back_to_support_KKT_when_the_zero_mode_is_signed_or_tangent_curvature_is_degenerate
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional real/rational algebra only
exit_code: n/a
---

# T-P5-162 — tangent-PD affine support continuation and exact energy splitting

## 0. Verdict and seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-159 turns the uniform additive floor into a one-parameter copositivity family and gives exact rational bracketing. T-P5-160 observes that the T-P5-154 loading contributes zero curvature on the simplex tangent space and treats the tangent-degenerate/common-kernel branch. T-P5-161 supplies a different fast path when the fixed-D matrix is a symmetric Z-matrix.

There remains a useful non-Z, nondegenerate branch: the base quadratic can be **strictly positive on the simplex tangent space** even though the full floor matrix is not obviously PSD or Z. In that branch, the entire D-dependence can be separated into one scalar normal energy.

The main result here is an exact decomposition

`x^T M_D x = z^T M_0 z + s^2 phi(D)`,

where `s=1^T x`, `z=x-s lambda(D)` is tangent, `lambda(D)=u+Dv`, and `phi(D)` is a scalar quadratic. Consequently:

- `phi(D)>=0` is an exact ordinary PSD certificate for the whole `M_D`;
- if `phi(D)<0` and `lambda(D)>=0`, then `lambda(D)` is an exact physical copositivity FAIL witness;
- if `phi(D)=0` and `lambda(D)>=0`, then D is the **exact sharp uniform floor**;
- if `phi(D)<0` but `lambda(D)` has a negative coordinate, PSD failure is not automatically physical, so the checker must fall back to T-P5-158/support recursion rather than declaring failure.

This is a source-independent energy/Lyapunov theorem only. No source identity, runtime semantics, coverage, Lean/kernel receipt, admission, or registry promotion is claimed.

---

## 1. Structured floor family

Fix one finite vertex set/support of size n. Let

`1 = (1,...,1)^T`,

`g_i>0`,

and let `M_0` be the symmetric base matrix from T-P5-154. Define

`L_g = (g 1^T + 1 g^T)/2`,

`M_D = M_0 + D L_g`.

For every vector x,

**(1.1)** `x^T L_g x = (1^T x)(g^T x)`.

Hence on the affine simplex hyperplane `1^T lambda=1`,

**(1.2)**

`q_D(lambda) := lambda^T M_D lambda`

`= lambda^T M_0 lambda + D g^T lambda`.

Let the tangent space be

`T = {z : 1^T z=0}`.

The branch assumption is strict tangent curvature:

**(TPD)** `z^T M_0 z>0` for every nonzero `z in T`.

This is weaker than requiring `M_0>0` on the ambient space and is exactly the curvature relevant to the simplex energy.

---

## 2. Two D-independent bordered solves generate every stationary point

Under (TPD), solve

**(2.1)**

`2 M_0 u = eta_0 1`,

`1^T u=1`,

and

**(2.2)**

`2 M_0 v + g = eta_1 1`,

`1^T v=0`.

### Theorem T162-A — `tangentPD_bordered_unique`

Under (TPD), both bordered systems have unique solutions.

### Proof

Consider the homogeneous bordered system

`2 M_0 z = eta 1`, `1^T z=0`.

Multiplication by `z^T` gives

`2 z^T M_0 z = eta 1^T z = 0`.

By (TPD), `z=0`, hence `eta=0`. The square bordered matrix is injective and therefore invertible. Thus (2.1) and (2.2) each have a unique solution. ∎

Define

**(2.3)** `lambda_D = u + D v`,

`eta_D = eta_0 + D eta_1`.

Then

`1^T lambda_D=1`,

and

**(2.4)** `2 M_0 lambda_D + D g = eta_D 1`.

Thus `lambda_D` is the unique stationary point of `q_D` on the whole affine hyperplane `1^T lambda=1`. Importantly, the producer never needs to solve a new linear system when D changes: all D-dependence is the affine continuation `u+Dv`.

For rational `M_0,g`, the bordered matrix and right-hand sides are rational, so `u,v,eta_0,eta_1` are rational whenever supplied by exact solve certificates.

---

## 3. Exact affine-hyperplane energy gap

### Theorem T162-B — `affine_stationary_energy_gap`

For every `mu` satisfying `1^T mu=1`,

**(3.1)**

`q_D(mu)-q_D(lambda_D)`

`= (mu-lambda_D)^T M_0 (mu-lambda_D)`.

### Proof

Set `delta=mu-lambda_D`, so `1^T delta=0`. Expanding (1.2),

`q_D(mu)-q_D(lambda_D)`

`= 2 delta^T M_0 lambda_D + D g^T delta + delta^T M_0 delta`.

The first two terms equal

`delta^T(2M_0 lambda_D+Dg)=eta_D delta^T1=0`

by (2.4). ∎

Under (TPD), `lambda_D` is therefore the unique global minimizer of `q_D` over the entire affine hyperplane. If `lambda_D>=0`, it is in particular the unique minimizer over the physical simplex.

This identity is the energy-method core of the child: the D-dependent linear tilt moves the center but never changes tangent curvature.

---

## 4. Scalar quadratic normal energy

Define

**(4.1)** `phi(D)=q_D(lambda_D)`.

Using `lambda_D=u+Dv`, one obtains

**(4.2)**

`phi(D)=a+bD+cD^2`,

where

`a=u^T M_0 u`,

`b=g^T u`,

**`c=-v^T M_0 v <= 0`.**

Indeed, (2.1) multiplied by `v^T` gives `u^T M_0 v=0`, while (2.2) multiplied by `v^T` gives

`2 v^T M_0 v + g^T v=0`.

Hence

`v^T M_0 v + g^T v = -v^T M_0 v`.

Moreover

**(4.3)** `phi'(D)=g^T lambda_D` algebraically, because

`g^T v=-2v^T M_0v=2c`.

No analytic differentiation theorem is needed; both sides are the same affine polynomial.

### Physical-corridor monotonicity

Whenever `lambda_D>=0`, `1^Tlambda_D=1`, and all `g_i>0`,

**(4.4)** `phi'(D)=g^Tlambda_D >= min_i g_i >0`.

Therefore `phi` is strictly increasing on every interval on which the affine stationary path stays in the simplex.

The simplex corridor itself is checked only by affine inequalities

**(4.5)** `u_i + D v_i >=0` for every i.

For rational endpoints `L<=U`, if (4.5) holds at both L and U, then it holds for every D in `[L,U]` by affine interpolation. No division is required to certify the corridor.

---

## 5. Stronger identity: full ambient energy splits into tangent + one scalar mode

The stationary point satisfies a useful ambient identity.

### Lemma T162-C — `stationary_vector_maps_to_phi_one`

**(5.1)** `M_D lambda_D = phi(D) 1`.

### Proof

From (2.4),

`M_0 lambda_D + (D/2)g = (eta_D/2)1`.

Since `1^Tlambda_D=1`,

`M_Dlambda_D`

`=M_0lambda_D +(D/2)g +(D/2)(g^Tlambda_D)1`

`=[eta_D+Dg^Tlambda_D]1/2`.

Multiplying (2.4) by `lambda_D^T` gives

`eta_D=2lambda_D^TM_0lambda_D+Dg^Tlambda_D`,

so the scalar in brackets divided by two equals

`lambda_D^TM_0lambda_D+Dg^Tlambda_D=phi(D)`. ∎

Now take an arbitrary signed vector x and set

`s=1^T x`,

`z=x-s lambda_D`.

Then `1^Tz=0`.

### Theorem T162-D — `exact_tangent_normal_energy_split`

For every real x,

**(5.2)**

`x^T M_D x = z^T M_0 z + s^2 phi(D)`.

### Proof

Expand `x=s lambda_D+z`. The cross term is

`2s z^T M_Dlambda_D = 2s phi(D) z^T1=0`.

Also, because z is tangent,

`z^T M_D z=z^TM_0z+D(1^Tz)(g^Tz)=z^TM_0z`.

Finally `lambda_D^TM_Dlambda_D=phi(D)`. ∎

This decomposition has several exact consequences under (TPD):

1. `phi(D)>0  ==>  M_D` is positive definite;
2. `phi(D)=0  ==>  M_D` is PSD and `ker(M_D)=span{lambda_D}`;
3. `phi(D)<0  ==>  M_D` is indefinite, with the signed vector `lambda_D` giving value `phi(D)<0`.

Thus a potentially high-dimensional matrix PSD question has collapsed to one fixed tangent-PD check plus one scalar quadratic sign.

---

## 6. Exact copositivity and sharp-floor consequences

### Theorem T162-E — `tangentPD_scalar_PASS`

Assume (TPD). If

`phi(D)>=0`,

then `M_D>=0`, hence `M_D` is copositive and D is a valid uniform floor.

This PASS does **not** require `lambda_D>=0`; PSD is an ambient statement.

### Theorem T162-F — `tangentPD_physical_FAIL`

Assume (TPD), `lambda_D>=0`, and

`phi(D)<0`.

Then `lambda_D` itself is an exact physical FAIL witness:

`lambda_D>=0`, `1^Tlambda_D=1`,

`lambda_D^T M_Dlambda_D=phi(D)<0`.

### Theorem T162-G — `tangentPD_zero_mode_is_exact_sharp_floor`

Assume

- `D_*>=0`;
- (TPD);
- `lambda_*=u+D_*v >=0`;
- `phi(D_*)=0`.

Then **`D_*` is the exact global sharp uniform floor.**

### Proof

At `D_*`, T162-D gives `M_{D_*}>=0`, so `D_*` is valid. For every `D<D_*`, evaluate at the same nonnegative simplex vector `lambda_*`:

`q_D(lambda_*)`

`=q_{D_*}(lambda_*)+(D-D_*)g^Tlambda_*`

`=(D-D_*)g^Tlambda_* <0`,

because `g_i>0` and `lambda_*` is a simplex point. Hence every smaller D fails. ∎

This theorem removes the fixed-D support enumeration entirely when the sharp zero mode lies in the physical simplex and the full base tangent curvature is strict.

If `lambda_*` has zeros, the statement is still valid: the zero mode lies on a proper face, but the full matrix is already PSD at `D_*`, while the same boundary vector proves failure below it.

---

## 7. Determinant factorization: no extraneous determinant roots in the strict tangent branch

Choose any rational/full-rank tangent basis matrix P with columns spanning `T`, so `1^T P=0`. Let

`H_T=P^T M_0 P`.

Under (TPD), `H_T>0`.

Form

`B_D=[lambda_D | P]`.

Because `lambda_D=u+Dv`, `v in T=range(P)`, replacing u by `u+Dv` changes the first column only by a linear combination of the tangent columns. Hence

**(7.1)** `det(B_D)=det([u|P]) !=0`, independent of D.

T162-D gives the exact congruence

**(7.2)**

`B_D^T M_D B_D = diag(phi(D), H_T)`.

Taking determinants,

**(7.3)**

`det(M_D) = C_T phi(D)`,

where

`C_T = det(H_T)/det([u|P])^2 >0`.

Consequences:

- in the strict tangent-PD branch, the principal determinant polynomial is not merely degree at most two as in T-P5-160; it is **exactly a positive constant times the scalar stationary energy phi(D)**;
- there are no determinant roots unrelated to the scalar normal mode;
- an identically-zero determinant family cannot occur in this branch. Such degeneracy necessarily belongs to the tangent-semidefinite/common-kernel branch handled by T-P5-160.

For rational data and rational P, `C_T` is rational and can be checked without eigenvalues or square roots.

---

## 8. Root-free rational checker packet

For rational `M_0,g`, a producer may hand the checker:

1. a rational tangent basis P and an exact positive-definite certificate for `H_T=P^TM_0P`;
2. rational `u,v,eta_0,eta_1` satisfying (2.1)-(2.2);
3. rational coefficients `a,b,c` with
   `a=u^TM_0u`, `b=g^Tu`, `c=-v^TM_0v`;
4. any proposed rational floor D.

Then the checker computes only

`lambda_D=u+Dv`,

`phi_D=a+bD+cD^2`.

The exact branch logic is:

- `phi_D>=0` -> **PASS** by T162-E;
- `phi_D<0` and `lambda_D>=0` -> **FAIL** with explicit witness `lambda_D` by T162-F;
- `phi_D=0` and `lambda_D>=0` -> **EXACT SHARP FLOOR** by T162-G;
- `phi_D<0` and some coordinate of `lambda_D` is negative -> **do not infer copositivity failure**; recurse to proper supports / T-P5-158.

### Rational isolation of an irrational sharp floor

If rational `L<U` satisfy

- `lambda_L>=0`, `lambda_U>=0`;
- `phi(L)<0`;
- `phi(U)>0`,

then affine interpolation keeps `lambda_D>=0` throughout `[L,U]`, while (4.4) makes phi strictly increasing there. Therefore there is a unique sharp root `D_* in (L,U)`. Rational bisection now needs only scalar quadratic evaluations; it does not need a new copositivity/support solve at every midpoint.

---

## 9. Exact examples

### 9.1 Rational sharp floor with a constant center

Take two vertices,

`g=(1,1)`,

`K_12=-4`,

so

`M_0=[[0,-2],[-2,0]]`.

On the tangent vector `(t,-t)`,

`(t,-t) M_0 (t,-t)^T = 4t^2>0`,

so (TPD) holds.

The bordered continuation is

`u=(1/2,1/2)`, `v=0`,

and

`phi(D)=D-1`.

Thus `D_*=1`, `lambda_*=(1/2,1/2)`, and

`M_1=[[1,-1],[-1,1]]>=0`

with kernel spanned by `(1,1)`. For every `D<1`, the same simplex vector gives `q_D(lambda_*)=D-1<0`. The floor 1 is therefore exactly sharp.

### 9.2 T-P5-159 irrational example collapses to one scalar quadratic

Take

`g=(1,2)`, `K_12=-1`,

`M_0=[[0,-1/2],[-1/2,0]]`.

Then

`u=(1/2,1/2)`,

`v=(1/2,-1/2)`,

and

**`phi(D)=(-1+6D-D^2)/4`.**

The physical continuation is

`lambda_D=((1+D)/2,(1-D)/2)`,

which is nonnegative for `0<=D<=1`. The first zero of phi is

`D_*=3-2 sqrt(2)`,

exactly the irrational sharp floor found in T-P5-159. The present theorem explains it without a determinant search: it is simply the zero of the unique scalar normal energy while the tangent energy remains positive.

### 9.3 Why the lambda>=0 gate is essential for declaring sharpness

Take three vertices with

`g=(1,2,10)`,

`K_12=-1`, `K_13=-5`, `K_23=-2`.

Using the tangent basis `P=[e_1-e_3,e_2-e_3]`,

`P^TM_0P=[[5,3],[3,2]]`,

whose determinant is 1 and first leading minor is 5, so (TPD) holds exactly.

The bordered solves give

`u=(2,-5/2,3/2)`,

`v=(-3,13/2,-7/2)`,

and

`phi(D)=-5/2+12D-(25/2)D^2`.

Its smaller zero is

`D_PSD=(12-sqrt(19))/25`.

At that zero,

`lambda_2(D_PSD)=(31-13sqrt(19))/50 <0`.

Therefore `M_{D_PSD}` is PSD by T162-D, but its zero mode is signed, not a physical simplex witness. It is a valid PSD upper floor, yet T162-G correctly refuses to call it sharp. In fact the physical sharpness is controlled by a proper face before this full-matrix PSD contact.

This is the exact obstruction behind the fallback rule: **ordinary PSD contact with a signed kernel is not the same as copositive sharpness.**

---

## 10. Relation to T-P5-158/159/160/161

The intended decision stack is now:

1. Build the T-P5-154 matrix family `M_D=M_0+D L_g`.
2. If a support has strict tangent curvature, use T-P5-162 first:
   - precompute two bordered solves once;
   - reduce every fixed-D query to `phi(D)` and `lambda_D`;
   - if a nonnegative zero mode appears, sharpness closes exactly.
3. If tangent curvature is semidefinite/singular, use T-P5-160's kernel deflation branch.
4. Independently, if a tested `M_D` lies in T-P5-161's Z-matrix corridor, ordinary PSD is an exact copositivity decider even without the tangent-PD continuation.
5. Whenever the tangent-PD scalar mode is negative but signed, or neither structural fast path applies, fall back to T-P5-158 exact support/KKT enumeration.
6. T-P5-159 remains the global monotone rational-bracketing wrapper, especially when the exact floor is algebraic.

This avoids using the expensive generic support lattice where the energy geometry already gives a one-dimensional exact answer.

---

## 11. Failure boundaries / nonclaims

1. **Tangent semidefinite is different.** If `M_0` has a nonzero tangent kernel, the bordered system may be singular or nonunique and `lambda_D=u+Dv` is not a canonical unique continuation. Do not perturb it silently; use T-P5-160.
2. **Signed stationary mode is not a physical FAIL witness.** `phi(D)<0` proves ordinary indefiniteness, but copositivity can still hold if `lambda_D` has negative coordinates.
3. **A PSD zero with signed kernel is not sharpness.** It is only a valid upper floor unless a nonnegative zero witness is separately available.
4. **The theorem assumes the exact T-P5-154 rank-two loading.** A different D-dependent Hessian generally changes tangent curvature and destroys the affine continuation/scalar split.
5. **No source or uncertainty-domain binding is supplied here.** The actual `g_i,K_ij` must still be tied to one physical same-key packet.
6. **No runtime/Float64, Lean/kernel, provenance, admission, or registry claim is made.**

---

## 12. Minimal candidate theorem statements

A formal sidecar can be decomposed into:

- `tangentPD_bordered_unique`;
- `affine_stationary_energy_gap`;
- `stationary_vector_maps_to_phi_one`;
- `exact_tangent_normal_energy_split`;
- `phi_coefficients_and_signed_curvature`;
- `phi_strictMono_on_nonnegative_stationary_corridor`;
- `tangentPD_scalar_PASS`;
- `tangentPD_physical_FAIL`;
- `tangentPD_zero_mode_is_exact_sharp_floor`;
- `det_factor_eq_positive_constant_mul_phi`.

The trusted proof surface can remain purely rational/ordered-ring plus finite-dimensional quadratic algebra once tangent positive-definiteness is supplied as an exact matrix certificate.