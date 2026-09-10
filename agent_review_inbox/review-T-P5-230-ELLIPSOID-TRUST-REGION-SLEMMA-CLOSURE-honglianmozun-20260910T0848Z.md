---
kind: review_result
review_id: review-T-P5-230-ellipsoid-trust-region-slemma-closure-honglianmozun-20260910T0848Z
task_id: T-P5-230-ELLIPSOID-TRUST-REGION-SLEMMA-CLOSURE
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T08:48:00Z
claim_commit: f692385d6455f4e68dde99f343b571bc84c7db47
inspected_commit: 2f97819e7cdaee7a879c9dbb7f79cd5a1f6a5db8
upstream_commits:
  - 575e296e13600ee0aa7b043dde8dd3b0f97b2ca1  # T-P5-229 bounded flat-fiber support closure
  - db655d40ee23d1c71f03f46eb20d112d0553b2fa  # T-P5-228 flat-fiber radical annihilation
  - 6a10ef29433a4dd050d593d8053383f4ba7fd204  # T-P5-226 higher-corank maximal-anchor Schur
  - 467527fa4670608070e0d74e64e6b7087a8b3094  # T-P5-222 face-lift quotient debit descent
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_exact_ellipsoid_trust_region_lmi; add_fraction_free_rational_multiplier_packet; add_curvature_kernel_scaling_gate; connect_flat_T229_as_zero_curvature_limit
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic/convex energy algebra only; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-230 — exact ellipsoid trust-region closure for curved gauge fibers

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-229 closed the exactly flat bounded-fiber branch `G^T Q G = 0` by a support-function formula and explicitly left the curved branch open. This child closes the negative-curvature ellipsoid branch exactly and identifies the near-origin Lyapunov scaling gate that survives when the curvature is only semidefinite.

The main point is that once the pure-gauge block is nonpositive,

`A := G^T Q G = -H`, `H >= 0`,

the residual gauge problem is no longer a flat support-function problem. For an ellipsoidal fiber it is an exact trust-region problem with a single scalar multiplier. The entire safety statement is equivalent to one PSD block matrix. No inverse, square root, pseudoinverse, or eigenvector is needed by a trusted checker when a rational multiplier is supplied.

There is also a structural near-origin dichotomy that is important for Lyapunov closure:

- cross terms lying in `range(H)` are absorbed by negative gauge curvature and remain quadratic order even if the admissible gauge radius stays fixed;
- cross terms with a component on `ker(H)` still produce an `O(t)` leakage against an `O(t^2)` base margin and therefore force the same radical/range condition that appears in the signed-lineality Schur branch.

Thus T-P5-228/229 are not separate phenomena. They are the zero-curvature face of a more general `range(H)` versus `ker(H)` energy decomposition.

No actual P5 face/tangent source map, same-cell coverage, trajectory semantics, Float64 enclosure, Lean/kernel receipt, independent validation by 封不觉, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Let the gauge parameter be `alpha in R^g`. Fix

`q(alpha) := q0 + 2 b^T alpha - alpha^T H alpha`,

where

`H = H^T >= 0`.

Let the admissible bounded fiber be the ellipsoid

`K := { alpha : alpha^T R alpha <= T^2 }`,

with

`R = R^T > 0`, `T > 0`.

In the P5 face-lift notation one obtains exactly this form by expanding

`(w + G alpha)^T Q (w + G alpha)`

with

`q0 = w^T Q w`,

`b = G^T Q w`,

`H = - G^T Q G`.

The safe endpoint sign convention is

`q(alpha) <= 0` for every `alpha in K`.

---

## 2. T230-A — exact one-multiplier ellipsoid certificate

### Theorem A

Under the setup above, the following are equivalent:

1. `q(alpha) <= 0` for every `alpha` satisfying `alpha^T R alpha <= T^2`;
2. there exists a scalar `lambda >= 0` such that

`M(lambda) >= 0`,

where

`M(lambda) := [[H + lambda R, -b], [-b^T, -q0 - lambda T^2]]`.

This is an exact necessary-and-sufficient certificate for the curved bounded-fiber branch.

### Proof: sufficiency

For any `alpha`,

`[alpha;1]^T M(lambda) [alpha;1]`

`= alpha^T H alpha + lambda alpha^T R alpha - 2 b^T alpha - q0 - lambda T^2`

`= -q(alpha) - lambda (T^2 - alpha^T R alpha)`.

If `M(lambda) >= 0`, the left-hand side is nonnegative. On the ellipsoid,

`T^2 - alpha^T R alpha >= 0`,

and `lambda >= 0`, hence

`-q(alpha) >= lambda (T^2 - alpha^T R alpha) >= 0`.

Therefore `q(alpha) <= 0` on all of `K`.

### Proof: necessity

Consider the equivalent convex minimization problem

`min_{alpha in K} -q(alpha)`.

Because `H >= 0`, `-q` is convex. Because `R>0` and `T>0`, `alpha=0` is a strict Slater point for the constraint `alpha^T R alpha < T^2`. Therefore convex strong duality holds.

The Lagrangian for multiplier `lambda >= 0` is

`L(alpha,lambda)`

`= -q(alpha) - lambda (T^2 - alpha^T R alpha)`

`= [alpha;1]^T M(lambda) [alpha;1]`.

If the primal minimum is nonnegative, strong duality supplies a dual multiplier for which the global infimum of this quadratic is nonnegative. A quadratic polynomial is globally nonnegative exactly when its homogenized symmetric block matrix is PSD. Hence `M(lambda)>=0`.

QED.

### Interpretation

This is the exact ellipsoidal S-lemma specialized to the current nonpositive-curvature gauge branch, but the proof needs only ordinary convex strong duality because `H>=0`.

---

## 3. T230-B — trust-region optimum and KKT branches

Define the worst curved-fiber debit

`Theta := sup_{alpha in K} q(alpha)`.

For `lambda>0`, set

`S_lambda := H + lambda R > 0`,

`alpha_lambda := S_lambda^{-1} b`,

and

`psi(lambda) := q0 + lambda T^2 + b^T S_lambda^{-1} b`.

Completion of the square gives

`q(alpha) + lambda (T^2 - alpha^T R alpha)`

`= psi(lambda) - (alpha-alpha_lambda)^T S_lambda (alpha-alpha_lambda)`.

Therefore

`Theta <= psi(lambda)` for every `lambda>0`.

Strong duality makes this bound exact:

**`Theta = min_{lambda>=0} psi(lambda)`**, with the `lambda=0` endpoint interpreted by the range-compatible limit described below.

### Branch B1 — unconstrained curved completion

Suppose there exists `x` satisfying

`H x = b`

and

`x^T R x <= T^2`.

Then

`q(alpha)`

`= q0 + b^T x - (alpha-x)^T H (alpha-x)`.

Hence

**`Theta = q0 + b^T x`**, attained at `alpha=x`.

The value `b^T x` does not depend on which solution of `Hx=b` is chosen, because any two solutions differ by `ker(H)` and `b` is orthogonal to `ker(H)`.

This is the exact `lambda=0` branch. It needs only a linear solve and an ellipsoid-membership check; no pseudoinverse is mathematically necessary.

### Branch B2 — boundary-active trust region

If no solution of `Hx=b` lies in `K`, then the optimum is boundary-active. There exists `lambda_*>0` such that

`(H + lambda_* R) alpha_* = b`,

`alpha_*^T R alpha_* = T^2`.

Equivalently,

`alpha_* = (H + lambda_* R)^{-1} b`,

and `lambda_*` solves the secular equation

**`b^T (H+lambda R)^{-1} R (H+lambda R)^{-1} b = T^2`.**

At that multiplier,

**`Theta = psi(lambda_*)`.**

Moreover

`psi'(lambda) = T^2 - alpha_lambda^T R alpha_lambda`,

and

`psi''(lambda) = 2 alpha_lambda^T R (H+lambda R)^{-1} R alpha_lambda >= 0`.

For `b != 0`, the second derivative is strictly positive, so the positive boundary multiplier is unique.

Thus the curved ellipsoid branch reduces to a one-dimensional convex dual search, not a high-dimensional semialgebraic search.

---

## 4. T230-C — fraction-free rational trusted packet

Suppose all source matrices/scalars are rational and a rational multiplier is proposed as

`lambda = p/s`,

with integers/rationals `p>=0`, `s>0`.

Multiplying `M(lambda)` by the positive scalar `s` preserves PSD. Define

`Mhat(p,s) :=`

`[[s H + p R, -s b],`

` [-s b^T, -s q0 - p T^2]]`.

Then

**`M(lambda) >= 0  <=>  Mhat(p,s) >= 0`.**

Therefore a trusted rational checker can verify the complete curved-fiber safety theorem by checking only

1. `p>=0`, `s>0`;
2. exact rational PSD of `Mhat(p,s)`.

There is no inverse, no square root, no pseudoinverse, no eigenvector, and no numerical root in the proof object. If desired, all remaining rational denominators can be cleared by one additional positive global scale.

### Why the block PSD is stronger than separately checking a Schur formula

At `lambda=0`, `H` may be singular. The block PSD condition automatically enforces the hidden range compatibility

`b in range(H)`

and the correct generalized Schur inequality. Thus the trusted interface should keep the whole PSD block rather than requiring a pseudoinverse branch in the checker.

---

## 5. T230-D — strict-margin rationalization theorem

### Theorem D

Assume the data `H,R,b,q0,T^2` are rational and

`Theta < 0`.

Then there exists a **rational** multiplier `lambda=p/s>0` for which

`Mhat(p,s) > 0`.

In particular every strictly safe rational curved-ellipsoid instance admits a purely rational strict PSD certificate.

### Proof

Strong duality gives a real optimal multiplier `lambda_*>=0` with dual value `Theta<0`.

If `lambda_*>0`, `psi` is continuous near `lambda_*`. Therefore an open interval around `lambda_*` still satisfies `psi(lambda)<0`. Choose a positive rational `lambda` in that interval. Then `H+lambda R>0`, and the Schur complement of the upper-left block in `M(lambda)` is exactly

`-psi(lambda)>0`.

Hence `M(lambda)>0`.

If `lambda_*=0`, the zero-multiplier branch has finite value only when `b in range(H)`. Because the optimum is strictly negative, the right-limit of `psi(lambda)` as `lambda downarrow 0` is still negative. Choose a sufficiently small positive rational `lambda`; again the upper-left block is positive definite and the Schur complement is strictly positive.

QED.

### Exact-boundary caution

If `Theta=0`, strong duality still gives an exact **real** multiplier, but strict-margin rationalization no longer follows from density/continuity: a unique minimizing multiplier may be algebraic. Therefore the trusted policy should be:

- strict safety: rational multiplier packet is guaranteed to exist;
- exact zero margin: permit a separate exact-algebraic/interval-isolation route if no rational contact multiplier is available.

This is a mathematical boundary, not a Float64 implementation detail.

---

## 6. T230-E — T-P5-229 recovered as the zero-curvature limit

Set `H=0`. For `lambda>0`,

`psi(lambda)`

`= q0 + lambda T^2 + (1/lambda) b^T R^{-1} b`.

Minimizing over `lambda>0` gives

`lambda_* = sqrt(b^T R^{-1}b)/T`,

and therefore

**`Theta = q0 + 2 T sqrt(b^T R^{-1} b)`.**

This is exactly the ellipsoid support formula in T-P5-229.

Hence the new trust-region packet is not a competing formulation. It continuously extends the T229 flat support theorem from

`G^TQG=0`

to

`G^TQG=-H<=0`.

Also, because `-alpha^THalpha<=0`, one always has

`Theta_curved <= Theta_flat`.

Using the flat T229 bound on a genuinely curved fiber is therefore safe but can be strictly conservative.

### Exact rational separation E1

Take the one-dimensional fiber

`R=1`, `T=1`, `H=1`, `b=2`, `q0=-7/2`.

The flat surrogate gives

`Theta_flat = -7/2 + 4 = 1/2 > 0`,

so a flat support test would FAIL.

The true curved problem is

`q(alpha) = -7/2 + 4 alpha - alpha^2`, `|alpha|<=1`.

Its maximum occurs at `alpha=1` and equals

`Theta_curved = -1/2 <0`.

The exact boundary-active multiplier is `lambda=1`, and

`M(1) = [[2,-2],[-2,5/2]] > 0`

because its determinant is `1`.

Thus negative gauge curvature can provide real Lyapunov reserve that a flat absolute-support relaxation throws away.

---

## 7. T230-F — near-origin curvature/radical dichotomy

This is the main structural consequence for Lyapunov scaling.

Let a physical endpoint amplitude be `t>=0`, and suppose the local family has

`q_t(alpha) := t^2 c + 2 t b^T alpha - alpha^T H alpha`,

with the same fixed ellipsoid

`K={alpha:alpha^TRalpha<=T^2}`.

The flat T-P5-229 branch (`H=0`) has an `O(t)` support term unless the gauge radius shrinks like `O(t)` or the cross term vanishes. Negative curvature changes that conclusion, but only on `range(H)`.

### Theorem F1 — range-compatible cross terms remain quadratic order

Assume

`b in range(H)`.

Choose any `x` with

`H x = b`.

For all sufficiently small `t`, the point `t x` lies in the fixed ellipsoid `K`. Completing the square gives

`q_t(alpha)`

`= t^2 (c + b^T x) - (alpha-tx)^T H (alpha-tx)`.

Therefore, for all sufficiently small `t`,

**`sup_{alpha in K} q_t(alpha) = t^2 (c + b^T x)`.**

So the gauge correction stays exactly quadratic order even though the fiber radius is fixed and the cross term is nonzero.

This is the curved analogue of Schur absorption.

### Theorem F2 — kernel cross terms force an `O(t)` obstruction

Assume instead

`b notin range(H)`.

Because `H` is symmetric,

`range(H) = ker(H)^perp`.

Hence there exists `z in ker(H)` with

`b^T z != 0`.

Scale `z` so that some fixed nonzero

`alpha0 = delta sign(b^Tz) z`

lies in the interior of `K`. Since `H z=0`,

`q_t(alpha0) = t^2 c + 2 t |b^T alpha0|`.

For every finite `c`, this is strictly positive for all sufficiently small `t>0`.

Therefore:

**if a fixed-radius curved fiber is required to satisfy `q_t<=0` uniformly near `t=0`, then necessarily `b in range(H)`, equivalently `b` annihilates `ker(H)`.**

This is exactly the bounded-fiber version of the T-P5-224/226 signed-lineality range gate and the T-P5-228 flat-radical gate.

### Structural meaning

The pure-gauge curvature splits the fiber into two mathematically different directions:

- `range(H)`: penalized directions; cross terms can be Schur-completed and remain `O(t^2)`;
- `ker(H)`: genuinely flat directions; cross terms cannot be paid by quadratic curvature and revert to the T228/T229 support/radical obstruction.

So the correct dispatcher is not merely `flat` versus `curved`. It is

**curved range absorption + flat-kernel radicality.**

---

## 8. Exact rational regressions for the scaling gate

### Regression R1 — fixed radius is safe when the cross term lies in the curved range

Take

`H = diag(1,0)`, `R=I`, `T=1`,

`b=(1,0)`, `c=-2`.

Then `b in range(H)` and one may choose `x=(1,0)`.

For `0<=t<=1`, `tx in K`, and

`q_t(alpha1,alpha2)`

`= -2t^2 + 2t alpha1 - alpha1^2`.

The exact maximum is at `alpha1=t` and equals

**`-t^2 <=0`.**

The fiber radius does not shrink at all, yet the nonzero cross term is fully absorbed by negative curvature.

This would be impossible in the flat T229 branch.

### Regression R2 — any unresolved flat-kernel cross leaks at first order

Take

`H = diag(1,0)`, `R=I`, `T=1`,

`b=(0,1)`, `c=-100`.

Here `b notin range(H)` and `z=e2 in ker(H)`.

At the admissible constant gauge point `alpha=e2`,

`q_t(e2) = -100 t^2 + 2t`.

Hence

`q_t(e2)>0` for every `0<t<1/50`.

Even an arbitrarily large finite negative quadratic base margin cannot suppress the first-order leakage as `t->0`.

This is a sharp obstruction, not a conservatism of the trust-region certificate.

---

## 9. Relation to T-P5-226 signed-lineality Schur reduction

The near-origin gate

`b in range(H)`

is the one-vector analogue of the T-P5-226 matrix range condition

`range(B) subseteq range(P)`.

The algebra is the same:

- a PSD curvature block penalizes some signed/gauge directions;
- cross forcing must lie in the curvature range;
- range-compatible forcing is eliminated by a Schur completion;
- kernel forcing creates an unpayable signed or small-amplitude obstruction.

The difference is geometric:

- T226 treats genuinely free signed lineality;
- T230 treats a bounded ellipsoidal gauge fiber.

Once the unconstrained Schur center lies inside the ellipsoid, both reductions produce the same completed-square logic. Only when the center exits the fiber does the trust-region multiplier `lambda>0` become active.

---

## 10. Candidate theorem statements for integration

### Candidate theorem 1 — `ellipsoid_curved_fiber_nonpositive_iff_psd_multiplier`

Assumptions:

- `H=H^T>=0`;
- `R=R^T>0`;
- `T>0`.

Conclusion:

`forall alpha, alpha^T R alpha <= T^2 -> q0+2b^Talpha-alpha^THalpha <=0`

iff

`exists lambda>=0, [[H+lambda R,-b],[-b^T,-q0-lambda T^2]] >=0`.

### Candidate theorem 2 — `curved_fiber_unconstrained_completion`

If

`Hx=b`

and

`x^TRx<=T^2`,

then

`sup_K q = q0+b^Tx`.

### Candidate theorem 3 — `curved_fiber_strict_rational_multiplier`

For rational input data, strict negativity of the ellipsoid maximum implies existence of a rational `p/s>0` such that

`[[sH+pR,-sb],[-sb^T,-s q0-pT^2]] >0`.

### Candidate theorem 4 — `fixed_radius_kernel_cross_obstruction`

For

`q_t(alpha)=t^2 c+2t b^Talpha-alpha^THalpha`

on a fixed full-dimensional ellipsoid, uniform nonpositivity for all sufficiently small `t>0` forces

`b in range(H)`.

If the range gate holds, the exact small-`t` maximum is

`t^2(c+b^Tx)`

for any `Hx=b` once `tx` lies in the ellipsoid.

---

## 11. Failure boundaries

This result must fail closed outside its assumptions.

1. **Box/polytope fibers are not certified exactly by the single ellipsoid multiplier.** A box can be enclosed in an ellipsoid to obtain a safe sufficient bound, but that is not an iff theorem. Exact box closure requires its own active-set/QP or multi-multiplier packet.
2. **The convex-duality proof here uses `H>=0`.** If the pure-gauge quadratic has a positive-debit direction (`G^TQG` has a positive eigenvalue), one enters the general indefinite S-lemma/trust-region branch. The same ellipsoidal S-lemma may still be available, but that stronger statement is not proved by the present convex argument and is not claimed here.
3. **`T>0` matters for Slater.** A degenerate zero-radius fiber should be reduced directly to the singleton `alpha=0` rather than routed through this proof.
4. **Rational strict certificates require strict safety.** Exact contact at zero margin may need algebraic multiplier handling.
5. **The scaling range gate assumes a fixed full-dimensional neighborhood in gauge coordinates.** If the actual admissible fiber itself collapses anisotropically with `t`, the correct asymptotic support law must use that source geometry rather than the fixed-radius theorem.
6. **Actual P5 source identity remains open.** Nothing here proves that a concrete face/tangent lift has `-G^TQG>=0`, that its admissible fiber is ellipsoidal, or that the same key/cell is valid along a trajectory.

---

## 12. New structural fingerprint

The new energy/Lyapunov fingerprint is

**bounded curved gauge fiber**

`-> H=-G^TQG >=0`

`-> split cross forcing into range(H) and ker(H)`

`-> kernel component gives first-order/radical obstruction`

`-> range component is Schur-completable`

`-> if Schur center lies inside fiber: exact quadratic-order completion`

`-> otherwise: one-scalar ellipsoid trust-region multiplier`

`-> rational strict PSD block packet`

`-> zero-curvature limit recovers T-P5-229 support geometry`.

This is the precise bridge between flat-fiber radicality, signed-lineality Schur reduction, and bounded trust-region Lyapunov closure.

---

## 13. Remaining open items / next mathematical seam

Still open and not upgraded here:

- actual same-key P5 `G,Q,w` source binding;
- proof that the actual pure-gauge block is nonpositive and identification of its kernel;
- proof that the actual bounded gauge fiber is an ellipsoid or has a certified ellipsoidal inner/outer representation suitable for the sign direction;
- cell/trajectory coverage;
- Float64/interval enclosure;
- Lean/kernel receipt;
- independent validation by 封不觉;
- admission/registry and P5/P8/M4 parent closure.

A natural next mathematical child is the **anisotropically shrinking semidefinite fiber**: when `H` has a kernel and the admissible gauge radii along kernel directions shrink with physical amplitude at different rates, derive the exact exponent threshold separating `O(t^2)` absorbable cross terms from `O(t^p)` leakage. That would unify T229's `radius/amplitude` scaling law with the T230 `range(H)` gate without assuming a fixed-radius ellipsoid.
