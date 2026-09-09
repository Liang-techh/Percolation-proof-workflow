---
kind: review_result
review_id: review-T-P5-189-kernel-gauge-dini-lyapunov-envelope-honglianmozun-20260909T2150Z
task_id: T-P5-189-KERNEL-GAUGE-DINI-LYAPUNOV-ENVELOPE
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T21:50:00Z
claim_commit: 094ffab4880c27377d0acee187bf20bb60b3d5c2
inspected_commit: 75a500ba936290917b6c753af17bd7f72a1d6b80
upstream_commits:
  - e5d824609fe5e899225e17adb672eac18da6883c  # T-P5-188 residual-stratum canonical compression
  - 1b4d00d6d3c2cbcbf3c1eadc4d7a3e729b7d808e  # T-P5-187 active-fan overlap kernel gauge
  - 2cef444f49ae94b85815734cf4376812b76f824a  # T-P5-185 piecewise active-face Schur fan
  - 4c6c4ab0ae84f7e397975e6de14e8167efcd6bfa  # T-P5-186 singular PSD recession active fan
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_kernel_gauge_observable_switch_identity; add_kernel_gauge_nondifferentiability_gate; add_selection_free_upper_dini_lyapunov_bound; add_strict_stratum_range_checker
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional convex quadratic/KKT algebra; exact rational hand/symbolic regression
exit_code: 0 for exact algebraic regression; no Lean/kernel run
---

# T-P5-189 — kernel-gauge observable, switching kink, and selection-free Dini Lyapunov envelope

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-187 proves that, at one fixed external direction, all orthant minimizers of a PSD inherited quadratic differ only by `ker(P)` and have the same KKT residual and the same reduced energy. T-P5-188 then characterizes the entire minimizer set by one affine kernel slice on the zero-residual coordinates.

That closes **value gluing**, but it does not close a Lyapunov question that becomes essential as soon as the external state moves:

> If two minimizing representatives differ by a zero-energy kernel gauge, can an arbitrary choice of representative be differentiated through an active-face switch?

The answer is **not always**. The missing quantity is the retained observable `B u`.

For two minimizers `y,z` at the same external state `e0`, put `k=z-y`. T-P5-187 gives `Pk=0`. This review proves the exact perturbation identity

**`q_H(z,e0+h)-q_H(y,e0+h)=2 h^T B k`.**

Thus the gauge is invisible to future first-order energy only when `Bk=0`. If `Bk!=0` and `e0` lies in the interior of the external orthant, the two frozen minimizing states exchange order across arbitrarily small perturbations. More strongly, the inherited reduced value is a concave lower envelope whose active supergradients are `2Bu`; two minimizers with distinct `Bu` force genuine nondifferentiability.

The useful energy-method consequence is nevertheless favorable: **one never needs to differentiate an optimizer selection.** For every exact minimizer `y` at time `t0`, the reduced energy is bounded above by the smooth frozen branch `q_H(y,e(t))` touching it at `t0`. Therefore its upper right Dini derivative satisfies

**`D^+ Phi(e(t0)) <= 2 dot(e0)^T (B y + C e0)`**

for every active minimizer `y` (with `C=C^T`). Hence a dissipation proof may use any exact active KKT witness with a sufficiently negative frozen slope; switching to another branch can only decrease the lower envelope further.

This gives a sound nonsmooth Lyapunov closure across active-face seams and identifies exactly when a stronger differentiable gluing claim is forbidden.

No source identity, physical cell/domain coverage, Float64/controller semantics, Lean/kernel verification, independent validation, admission, or registry mutation is claimed.

---

## 1. Setup

Let

`H = [[P, B^T], [B, C]]`,

with

- `P=P^T >= 0` an `m x m` PSD matrix;
- `C=C^T` a `p x p` symmetric matrix;
- inherited coordinates `u in R_+^m`;
- retained/external coordinates `e in R_+^p`.

Define

`q_H(u,e) = u^T P u + 2 e^T B u + e^T C e`.

Whenever the minimum is finite and attained, define the reduced energy

`Phi(e) := min_{u>=0} q_H(u,e)`.

Also separate the smooth external quadratic:

`psi(e) := Phi(e) - e^T C e`

`       = min_{u>=0} [u^T P u + 2 e^T B u]`.

T-P5-186 supplies a sufficient/exact recession gate for finiteness/attainment in the singular-PSD case; this review assumes the pointwise minimizers under discussion exist and does not redo that gate.

Fix `e0>=0`. Let `M(e0)` denote all minimizing inherited states at `e0`.

By T-P5-187, if `y,z in M(e0)` and

`k := z-y`,

then

**(1.1)** `P k = 0`,

and the two states have the same KKT residual and the same value.

By T-P5-188, if `r=Py+B^T e0` is the canonical residual and

`I={i:r_i=0}`, `J={j:r_j>0}`,

then every minimizer has `u_J=0` and

`P_II u_I = -(B^T e0)_I`.

So all remaining ambiguity is an affine slice of `ker(P_II)` inside the orthant.

---

## 2. T189-A — exact frozen-state branch-switch identity

### Theorem

Let `y,z in M(e0)` and `k=z-y`. Then for every external state `e`,

**(2.1)** `q_H(z,e)-q_H(y,e) = 2 e^T B k`.

Since the two states tie at `e0`,

**(2.2)** `e0^T B k = 0`.

Therefore for every perturbation `h`,

**(2.3)**

`q_H(z,e0+h)-q_H(y,e0+h) = 2 h^T B k`.

### Proof

Expand the difference:

`q_H(z,e)-q_H(y,e)`

`= z^T P z-y^T P y + 2 e^T B(z-y)`.

Write `z=y+k`. Since `Pk=0`,

`z^T P z`

`= y^T P y + 2 y^T Pk + k^T Pk`

`= y^T P y`.

Thus only the retained observable remains:

`q_H(z,e)-q_H(y,e)=2e^TBk`.

At `e=e0`, both are minimizers and therefore have equal value, giving (2.2). Subtracting the `e0` equality gives (2.3). QED.

### Interpretation

`k in ker(P)` means that the inherited quadratic cannot see the gauge direction.

But the moving external state sees it through `Bk`.

So the correct structural fingerprint is

**kernel gauge -> retained observable `Bk` -> branch ordering under external motion.**

The condition `Pk=0` alone is not sufficient for differentiable Lyapunov gluing.

---

## 3. T189-B — exact local branch-order reversal

Assume now that `e0` is in the interior of the external orthant:

`e0_i>0` for every external coordinate.

Suppose there are two minimizers `y,z` with

`Bk != 0`.

Set `v:=Bk`.

Because `e0>0`, for sufficiently small `epsilon>0`, both

`e_+ := e0 + epsilon v`,

`e_- := e0 - epsilon v`

remain nonnegative.

By (2.3),

`q_H(z,e_+)-q_H(y,e_+) = 2 epsilon ||v||^2 > 0`,

while

`q_H(z,e_-)-q_H(y,e_-) = -2 epsilon ||v||^2 < 0`.

Therefore the two frozen states exchange strict order across arbitrarily small perturbations of `e0`.

This statement does **not** require either frozen state to remain the global minimizer on the perturbed side. It is already enough to show that the kernel gauge is physically visible and that one cannot regard `y` and `z` as a single smooth state selection through the seam.

If `e0` lies on the boundary of the external orthant, the exact identity (2.3) remains valid, but the two-sided perturbation argument must be replaced by feasible one-sided directions. This boundary is kept fail-closed.

---

## 4. T189-C — every active minimizer gives a supergradient of the inherited envelope

The inherited reduced value

`psi(e)=min_{u>=0}[u^TPu+2e^TBu]`

is the pointwise infimum of affine functions of `e`. Hence, wherever finite, it is concave.

Let `y in M(e0)`. For any other `e` in the finite domain,

`psi(e)`

`<= y^T P y + 2 e^T B y`

`= [y^T P y + 2 e0^T B y] + 2(e-e0)^T B y`

`= psi(e0)+2(e-e0)^T B y`.

Thus

**(4.1) `2 B y` is a supergradient of `psi` at `e0`.**

This is exact and uses no compactness theorem, pseudoinverse, optimizer differentiation, or choice of active face beyond one exact KKT minimizer.

### Nondifferentiability criterion

Assume `e0` lies in the interior of an open convex region on which `psi` is finite. If there exist `y,z in M(e0)` with

`B y != B z`,

then (4.1) supplies two distinct supergradients

`2By != 2Bz`.

A finite concave function differentiable at an interior point has a unique supergradient there. Therefore

**(4.2) `psi` is not differentiable at `e0`.**

Since `e^T C e` is smooth,

**(4.3) `Phi` is also not differentiable at `e0`.**

So T-P5-187's exact equality of reduced **values** on a seam does not imply equality of reduced **gradients**.

The missing condition is precisely whether the minimizing kernel gauge is annihilated by `B`.

---

## 5. T189-D — kernel-gauge invisibility checker on a strict zero-residual stratum

Use T-P5-188's canonical zero-residual partition `I,J` at `e0`.

Suppose there exists a minimizer `y` with

`y_J=0`,

`y_I>0` coordinatewise.

This means the canonical affine minimizer slice meets the relative interior of the `I`-orthant.

Let `k_I in ker(P_II)`. By T-P5-188's principal-kernel lifting lemma, the full vector

`k=(k_I,0_J)`

lies in `ker(P)`.

Because `y_I>0`, sufficiently small `epsilon>0` makes both

`y + epsilon k`,

`y - epsilon k`

nonnegative. They remain solutions of the same reduced linear system and therefore are both global minimizers.

Consequently, on such a strict stratum, the following are equivalent:

1. every minimizer has the same retained observable `Bu`;
2. every kernel gauge is invisible:

   **`B[:,I] k_I = 0` for every `k_I in ker(P_II)`;**

3. the kernel inclusion holds:

   **`ker(P_II) subseteq ker(B[:,I])`;**

4. because `P_II` is symmetric, the row/range inclusion holds:

   **`range(B[:,I]^T) subseteq range(P_II)`;**

5. there exists a matrix `X` satisfying the exact linear range solve

   **`P_II X = B[:,I]^T`.**

### Proof of the range equivalence

For a symmetric matrix,

`range(P_II) = ker(P_II)^perp`.

Thus every column of `B[:,I]^T` belongs to `range(P_II)` iff it is orthogonal to every `k_I in ker(P_II)`, which is exactly `B[:,I]k_I=0` for every such kernel vector.

### Consequence

At a strict zero-residual stratum, a single exact linear range solve can distinguish two cases:

- **PASS / gauge invisible:** all minimizing representatives induce the same `Bu`; the kernel nonuniqueness is irrelevant to first-order retained-energy coupling;
- **FAIL / gauge visible:** choose `k_I` with `B[:,I]k_I !=0`; small `y+-epsilon k` are two exact minimizers with different supergradients, so an interior external point is a genuine reduced-energy kink.

This is a mathematical differentiability diagnostic, not a source or admission certificate.

If no strictly positive minimizer exists on `I`, failure of the full range inclusion may involve kernel directions that are not feasible in both signs. Then T-P5-179/T-P5-188 support descent is required; the range test remains sufficient for invisibility but is not claimed necessary on a boundary-only minimizer slice.

---

## 6. T189-E — selection-free upper-Dini Lyapunov inequality

This is the main energy-method payoff.

Let `e(t)` be a trajectory in the external orthant, differentiable from the right at `t0`, with

`e0:=e(t0)`,

`dot_e0:=d e/dt (t0+)`.

Assume `Phi(e0)` is attained and choose **any** exact minimizer

`y in M(e0)`.

For every nearby `t>=t0`, by definition of the minimum,

`Phi(e(t)) <= q_H(y,e(t))`.

At `t=t0`, equality holds:

`Phi(e0)=q_H(y,e0)`.

Therefore

`[Phi(e(t))-Phi(e0)]/(t-t0)`

`<= [q_H(y,e(t))-q_H(y,e0)]/(t-t0)`.

Taking upper right limits gives

**(6.1)**

`D^+ Phi(e(t0))`

`<= 2 dot_e0^T B y + 2 e0^T C dot_e0`

`= 2 dot_e0^T (B y + C e0)`.

This bound holds **for every** `y in M(e0)`.

Hence, in extended-real notation,

**(6.2)**

`D^+ Phi(e(t0))`

`<= inf_{y in M(e0)} 2 dot_e0^T(B y + C e0)`.

No derivative of `y(t)` appears.

### Lyapunov closure corollary

Suppose a desired dissipation rate is `Delta(e0)>0`. If one can exhibit an exact active KKT minimizer `y` such that

**`2 dot_e0^T(B y + C e0) <= -Delta(e0)`,**

then automatically

**`D^+ Phi(e(t0)) <= -Delta(e0)`.**

Thus active-face switching is not, by itself, an obstruction to a Lyapunov proof. The lower envelope may be nonsmooth, but a smooth frozen branch touching it from above supplies a valid upper-Dini dissipation estimate.

This is strictly safer than choosing an optimizer `y(t)` and differentiating it as if it were smooth across face changes.

### Why the direction of the inequality is favorable

`Phi` is a minimum over inherited states. When the active face changes, the new branch can only make the envelope **lower** than the old frozen branch. Therefore a derivative estimate from any touching frozen branch is an upper bound—the direction needed for dissipation.

---

## 7. Exact rational regression: copositive smooth quadratic with a kinked reduced Lyapunov envelope

Take

`P = [[1,1],[1,1]]`,

`B = -I_2`,

`C = I_2`.

Then the full symmetric matrix is

`H =`

`[[ 1, 1,-1, 0],`

` [ 1, 1, 0,-1],`

` [-1, 0, 1, 0],`

` [ 0,-1, 0, 1]]`.

Its determinant is `-1`, so it is not PSD. Nevertheless it is copositive.

Indeed, for `u1,u2,e1,e2>=0`,

`q_H(u,e)`

`= (u1+u2)^2 - 2(e1 u1+e2 u2) + e1^2+e2^2`.

Let

`s=u1+u2`,

`m=max(e1,e2)`.

Because `e1u1+e2u2 <= m(u1+u2)=ms`,

`q_H(u,e)`

`>= s^2-2ms+e1^2+e2^2`

`= (s-m)^2 + e1^2+e2^2-m^2`

`= (s-m)^2 + min(e1,e2)^2`

`>=0`.

Equality in the minimization is attained by assigning all inherited mass `s=m` to a coordinate realizing the larger external component. Therefore the exact reduced energy is

**(7.1) `Phi(e1,e2)=min(e1,e2)^2`.**

The inherited envelope is

**(7.2) `psi(e1,e2)=-max(e1,e2)^2`.**

Both are continuous, but they are nondifferentiable on the positive switching line

`e1=e2=t>0`.

### Kernel-gauge data at the seam

At `e0=(t,t)`, every nonnegative `u` with

`u1+u2=t`

is a minimizer. In particular

`y=(t,0)`,

`z=(0,t)`.

Their difference

`k=z-y=(-t,t)`

satisfies

`Pk=0`,

but

`Bk=(t,-t) !=0`.

So the kernel gauge is energy-flat at `e0` but externally visible.

The two inherited supergradients are

`2By=(-2t,0)`,

`2Bz=(0,-2t)`,

which are distinct. Hence T189-C detects the kink exactly.

### Strict-stratum range checker

At the same seam, choose the strictly positive minimizer

`y_*=(t/2,t/2)`.

The canonical residual is zero on both inherited coordinates, so `I={1,2}`. Now

`ker(P)=span{(1,-1)}`,

while

`B(1,-1)^T=(-1,1)^T !=0`.

Thus

`range(B^T)` is not contained in `range(P)`,

and no solve `PX=B^T` exists. T189-D therefore flags derivative non-gluing without enumerating the continuum of minimizers.

### Dini Lyapunov check through the switch

Take `t=1` at the seam `e0=(1,1)` and perturb along

`h=(1,-1)`.

Then

`Phi(e0+tau h)=(1-|tau|)^2`

for sufficiently small `|tau|`.

The upper right derivative is exactly `-2`.

Using the active minimizer `y=(1,0)`, T189-E gives

`2 h^T(B y+C e0)`

`=2(1,-1)^T[(-1,0)+(1,1)]`

`=2(1,-1)^T(0,1)`

`=-2`,

which is sharp.

Using the other minimizer `z=(0,1)` gives the valid but weaker upper bound `+2`. Taking the best active frozen branch recovers the exact one-sided slope, but exactness is not needed for the Lyapunov implication.

### Additional structural point

The T-P5-186 nonnegative-kernel recession cone is trivial here:

`d>=0` and `Pd=0` imply `d1+d2=0`, hence `d=0`.

So the reduced-energy kink occurs **after** the singular recession obstruction has already been completely removed. It is a separate phenomenon caused by sign-changing kernel gauge directions, exactly the seam addressed by this review.

---

## 8. Recommended checker / theorem routing

For a PSD inherited block and one external state:

1. Use T-P5-186 to rule out negative nonnegative-kernel recession and obtain an attained minimizer.
2. Use T-P5-187/188 to canonicalize the KKT residual and full minimizer affine slice.
3. If downstream work needs only the reduced **value**, T-P5-187 seam equality is enough.
4. If downstream work differentiates the reduced energy or uses it as a Lyapunov functional, inspect the kernel observable:
   - direct pairwise witness: `Pk=0` and `Bk`;
   - on a strict zero-residual stratum, use the exact range test `range(B_I^T) subseteq range(P_II)`.
5. If the gauge is invisible, minimizer nonuniqueness creates no first-order `Bu` ambiguity at that state.
6. If the gauge is visible, do **not** differentiate an arbitrary optimizer selection. Use T189-E's frozen-branch upper-Dini inequality or an explicit piecewise/Dini argument.

This keeps the energy method fail-closed while avoiding an unnecessary demand for a globally smooth optimizer map.

---

## 9. Candidate theorem statements for formalization

The following are the smallest reusable mathematical statements suggested by this review.

### T189.1 — kernel-gauge observable switch

Assume `P=P^T>=0`, `y,z` minimize `u^TPu+2e0^TBu` over `u>=0`, and `k=z-y`. Then

`Pk=0`,

`e0^TBk=0`,

and for every `h`,

`q_H(z,e0+h)-q_H(y,e0+h)=2h^TBk`.

### T189.2 — active minimizer supergradient

If `y` minimizes the inherited quadratic at `e0`, then for every `e`,

`psi(e) <= psi(e0)+2(e-e0)^TBy`.

### T189.3 — kernel-visible nondifferentiability

If `psi` is finite on a neighborhood of interior `e0` and two minimizers satisfy `By!=Bz`, then `psi` and `Phi=psi+e^TCe` are not differentiable at `e0`.

### T189.4 — strict-stratum gauge invisibility

Under T-P5-188's zero-residual stratum, if some minimizer is strictly positive on `I`, then all minimizers have the same `Bu` iff

`ker(P_II) subseteq ker(B_I)`,

iff

`range(B_I^T) subseteq range(P_II)`.

### T189.5 — frozen-minimizer upper-Dini bound

If `e(t)` has right derivative at `t0`, `C=C^T`, and `y` minimizes at `e(t0)`, then

`D^+ Phi(e(t0)) <= 2 dot(e0)^T(B y+C e0)`.

This theorem is the preferred Lyapunov consumer because it never differentiates the optimizer.

---

## 10. Fail-closed boundaries and remaining obligations

1. **Boundary external states.** The branch-switch identity is global, but two-sided nondifferentiability arguments require feasible perturbations. At the boundary of `R_+^p`, use relative/one-sided directions.
2. **No strict minimizer on the zero-residual stratum.** Then the full range test is sufficient for gauge invisibility but is not claimed necessary; some algebraic kernel directions may be orthant-infeasible. Descend to the true support.
3. **No converse differentiability claim.** Equality of `Bu` across currently known minimizers removes this particular kernel-gauge obstruction; it does not by itself prove a globally `C^1` reduced energy or a smooth optimizer map.
4. **Dini, not classical derivative.** The sound Lyapunov consumer is the upper-Dini inequality. Classical differentiation through switching faces requires additional smoothness/active-set stability.
5. **Source binding open.** No actual Route-B/PDE/Newton-Euler source matrix has been identified with `(P,B,C)` here.
6. **Coverage open.** No physical cell, trajectory tube, parameter polytope, or support cover is closed.
7. **Runtime/Float64 open.** No floating-point or deployed-controller semantics are claimed.
8. **Lean/kernel open.** No Lean theorem was compiled in this review.
9. **Independent validation open.** 封不觉 has not been asked to validate this child.
10. **Admission/registry open.** This remains a mathematical sidecar with `pending` admission.

---

## 11. Final mathematical handoff

The active-face program now has a clean hierarchy:

- **value layer:** T-P5-187/188 show all PSD-kernel-related minimizing representatives have one canonical value/residual;
- **observable layer:** T-P5-189 shows the gauge may still change `Bu`, producing a real derivative seam;
- **Lyapunov layer:** the lower-envelope structure gives an upper-Dini derivative bound from any exact frozen minimizer, so dissipation can be proved without ever choosing a differentiable optimizer branch.

The new structural fingerprint is therefore:

**PSD flat energy -> kernel-gauge minimizers -> retained observable `Bu` -> possible switching kink -> frozen-branch Dini dissipation closure.**

That is the narrow mathematical advance of this review.