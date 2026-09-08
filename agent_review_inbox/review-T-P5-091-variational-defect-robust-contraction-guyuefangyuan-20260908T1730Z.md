---
kind: review_result
review_id: review-T-P5-091-variational-defect-robust-contraction-guyuefangyuan-20260908T1730Z
task_id: T-P5-091-VARIATIONAL-DEFECT-ROBUST-CONTRACTION
agent: 古月方源
source_agent: 古月方源
reviewer: 古月方源
created_at: 2026-09-08T17:30:00Z
claim_commit: 6a3f2d914199b662e03e7e4fae91fd5e26ef3441
inspected_commit: a5c9020bfe61aeac237cf331359476f3bc730ea2
inspected_upstream:
  - agent_review_inbox/review-T-P5-090-moving-metric-contraction-congruence-liuguanyi-20260908T1710Z.md
  - agent_review_inbox/review-T-P5-087-moving-metric-kernel-transport-guyuefangyuan-20260908T1025.md
  - agent_review_inbox/review-T-P5-089-mechanical-skew-energy-honglianmozun-20260908T1104.md
status: CONDITIONAL_PASS
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_division_free_mixed_defect_leaf_then_bind_same_tube_variational_defect_packet
commands: none_math_derivation_only
---

# T-P5-091 — robust differential contraction with variational defects

## 0. Question and scope

T-P5-090 closes the exact coordinate-covariance theorem for differential
contraction in a moving state/time-dependent metric, but explicitly leaves
**defects/noise in the variational dynamics** open.

This child closes the deterministic exact-real mathematics of that gap.  The
main result is a division-free mixed-defect theorem: a signed relative defect
uses part of the nominal contraction rate, while an additive defect creates a
sharp invariant energy tube.  The same constants transport through a moving
nonlinear chart under the simple covariance relation `J e_z = e_x`; no inverse
of `J`, square root, generalized eigenvalue, or norm condition number is needed.

This is not the old componentwise state-residual theorem.  Here the storage is
the **variational energy** `xi^T W xi`, the metric may move with the nominal
trajectory, and the new issue is robustness of T-P5-090's contraction tensor.

Out of scope: a perturbation of the *base trajectory* itself, stochastic/Itô
noise, deployed source binding, Float64/FD/controller semantics, P8 coverage,
Lean compilation, receipt/provenance/admission, and registry changes.

---

## 1. Nominal moving-metric contraction

Use T-P5-090's physical notation.  The nominal base dynamics is

`xdot = -F(t,x)`,

with

`A = D_x F`,

and symmetric positive-semidefinite metric `W(t,x)`.  Along the nominal base
trajectory define

`L_F W = W_t - D_x W[F]`

and

`C = A^T W + W A - L_F W`.

Assume the same-tube quadratic-form certificate

**(1.1)** `xi^T C xi >= 2 mu * xi^T W xi`

for some `mu > 0`.

Write

`V := Q_W(xi) := xi^T W xi`.

For the exact variational equation `xidot=-A xi`, T-P5-090 gives

`Vdot <= -2 mu V`.

We now perturb only the variational equation, keeping the nominal base
trajectory unchanged:

**(1.2)** `xidot = -A xi + e`.

Direct differentiation gives the exact identity

**(1.3)**

`Vdot = - xi^T C xi + 2 xi^T W e`,

hence from (1.1)

**(1.4)**

`Vdot <= -2 mu V + 2 <xi,e>_W`.

This single cross power is the complete extra charge for a variational defect.
No additional `W_t` or `D_xW[F]` charge should be added: those terms are already
inside `C`.

---

## 2. Relative same-metric defect: exact rate loss

Let

`E := Q_W(e) = e^T W e`.

For PSD `W`, the quadratic Cauchy inequality is

**(2.1)** `<xi,e>_W^2 <= V E`.

Suppose a source packet gives a relative *squared* defect bound

**(2.2)** `E <= rho^2 V`, with `rho >= 0`.

Then (2.1)-(2.2), using only nonnegativity, imply

**(2.3)** `<xi,e>_W <= rho V`.

Therefore

**(2.4)**

`Vdot <= -2 (mu-rho) V`.

So a same-metric relative variational defect consumes the contraction rate
**linearly**, not quadratically.  If `rho < mu`, strict contraction survives with
rate `mu-rho`.

### Division-free checker form

The trusted checker need not compute `sqrt(E/V)`.  It may consume the rational
claims

`E <= rho^2 V`, `0 <= rho`, `rho < mu`,

and the theorem can derive (2.3) from the squared Cauchy inequality.  Thus the
runtime arithmetic is multiplication, squaring, addition and order comparison
only.

### Semidefinite boundary

If `W` is merely PSD, this is contraction of the induced seminorm.  To infer a
true distance or uniqueness statement, downstream still needs positive
definiteness/coercivity on the relevant tangent space.  The energy inequality
itself does not require an inverse metric.

---

## 3. Signed operator defect: preserve cancellation before taking norms

Often the defect is linear in the variation,

**(3.1)** `e = R xi`.

Then the defect power is exactly

`2 <xi,Rxi>_W`
` = xi^T (W R + R^T W) xi`.

Hence the correct source-facing certificate is the **signed symmetric defect**

**(3.2)**

`xi^T (W R + R^T W) xi <= 2 rho * xi^T W xi`

for all relevant `xi`.

Combining (3.2) with nominal contraction gives immediately

**(3.3)** `Vdot <= -2(mu-rho)V`.

This can be much stronger than first bounding `||R||`.  For example, with
`W=I` and

`R = [[0,K],[-K,0]]`

for arbitrarily large `K`,

`R+R^T = 0`.

Thus the exact rate loss is `rho=0`, even though every ordinary operator norm of
`R` grows like `|K|`.  A checker that absolute-values the entries or bounds
`||R||` before forming the symmetric power defect can create arbitrarily bad
false negatives.

The same lesson as T-P5-074/T-P5-090 applies: **form the signed energy object
first; enclosure comes afterwards**.

---

## 4. Additive defect: a division-free invariant-tube theorem

A bounded additive defect cannot preserve contraction to zero.  What it can
preserve is an invariant energy tube.

Let `d` be an additive defect and suppose

**(4.1)** `Q_W(d) <= Ebar`.

For every scalar `lambda > 0`, PSD of `W` gives

`Q_W(lambda xi - d) >= 0`,

so

**(4.2)**

`2 lambda <xi,d>_W <= lambda^2 V + Q_W(d)`.

Combining (4.2) with (1.4) yields the completely division-free inequality

**(4.3)**

`lambda Vdot <= -lambda(2 mu-lambda) V + Ebar`.

If `0 < lambda < 2 mu`, define

`kappa_lambda := lambda(2 mu-lambda) > 0`.

Then any rational `Vstar >= 0` satisfying

**(4.4)** `Ebar <= kappa_lambda Vstar`

has nonpositive vector-field derivative on the boundary `V=Vstar`:

**(4.5)** `V=Vstar  =>  Vdot <= 0`.

Thus, once a standard first-exit/barrier lemma and same-tube coverage are
available, `{V <= Vstar}` is forward invariant.

No division is needed in the certificate.  The usual expression
`Vstar >= Ebar/kappa_lambda` is only an interpretation of (4.4), not something
the checker needs to compute.

### Canonical choice `lambda = mu`

The coefficient `lambda(2mu-lambda)` is maximized at `lambda=mu`.  Taking that
choice gives the particularly small exact interface

**(4.6)**

`mu Vdot <= -mu^2 V + Ebar`,

and the barrier gate becomes simply

**(4.7)** `Ebar <= mu^2 Vstar`.

For an additive defect measured in the same metric, this is the natural
square-only certificate.

---

## 5. Mixed relative + additive defect: the main theorem

The most useful source decomposition is

**(5.1)** `e = r + d`,

where `r` is a relative/structured defect and `d` is the irreducible additive
part.

Assume

**(5.2)** `<xi,r>_W <= rho V`,

**(5.3)** `Q_W(d) <= Ebar`,

with

**(5.4)** `nu := mu-rho > 0`.

From (1.4) and (5.2),

`Vdot <= -2 nu V + 2 <xi,d>_W`.

Now apply (4.2) with `lambda=nu`.  The result is

**(5.5) MAIN DIVISION-FREE ROBUST CONTRACTION BARRIER**

`nu Vdot <= -nu^2 V + Ebar`.

Consequently, for any candidate energy level `Vstar`,

**(5.6)** `Ebar <= nu^2 Vstar`

implies

**(5.7)** `V=Vstar  =>  Vdot <= 0`.

If the relative piece is supplied only through

`Q_W(r) <= rho^2 V`,

Section 2 derives (5.2).  If `r=Rxi`, Section 3 can instead use the sharper
signed symmetric-operator certificate.

### Sharp scalar regression

Take `W=1`, nominal `A=mu`, relative aligned defect `r=rho xi`, and constant
additive defect `d=epsilon>0`.  Then

`xidot = -(mu-rho) xi + epsilon`.

Its equilibrium is

`xi_* = epsilon/(mu-rho)`,

so

`V_* = epsilon^2/(mu-rho)^2 = Ebar/nu^2`.

Thus the barrier threshold in (5.6) is attained exactly in the scalar aligned
case.  The square-only gate is not merely a loose Young artifact.

---

## 6. Hard obstruction: additive bounded noise does not imply zero contraction

Even the one-dimensional constant-metric system gives a counterexample.

Let

`W=1`, `A=mu>0`, `e=epsilon>0` constant.

The nominal system has exact contraction tensor `C=2mu`, but

`xidot = -mu xi + epsilon`

has the nonzero equilibrium `xi=epsilon/mu`.

Moreover

`Vdot = -2mu xi^2 + 2epsilon xi`

is positive for every `0 < xi < epsilon/mu`.

Therefore no theorem of the form

`Q_W(e) <= constant  and  C>=2muW  =>  Vdot <= -cV for all xi`

with `c>0` can be true.  A constant additive defect necessarily changes the
conclusion from zero contraction to an ultimate/invariant tube unless extra
structure forces the defect to vanish with `xi`.

This is a mathematical obstruction, not a provenance or checker problem.

---

## 7. Exact transport through a moving nonlinear chart

Now use T-P5-090's moving chart

`x = T(t,z)`, `J=D_zT`,

with normalized base field satisfying

`J G = F(t,T) + T_t`.

Let `eta` be a normalized variation and set

**(7.1)** `xi = J eta`.

T-P5-090 gives the connection identity that transports the nominal variational
dynamics.  Add a normalized defect `e_z` and a physical defect `e_x` satisfying
only

**(7.2)** `J e_z = e_x`.

Then

`etadot = -B eta + e_z`

implies

`xidot = -A xi + e_x`.

No inverse of `J` is used: (7.2) is a forward covariance premise.

Let the pulled metric be

`M = J^T W J`.

Then three exact identities hold:

**(7.3)** `Q_M(eta) = Q_W(xi)`,

**(7.4)** `Q_M(e_z) = Q_W(e_x)`,

**(7.5)** `<eta,e_z>_M = <xi,e_x>_W`.

Therefore every relative, additive, or mixed-defect certificate in Sections
2–5 transports with **exactly the same `rho`, `Ebar`, `mu`, and `Vstar`**.
There is no Jacobian condition-number loss.

This is stronger than a norm-based coordinate transport and is the natural
defect companion to T-P5-090's tensor congruence.

### Operator intertwining version

If physical and normalized relative operators satisfy

**(7.6)** `J R_z = R_x J`,

then for `xi=Jeta`

**(7.7)**

`eta^T (M R_z + R_z^T M) eta`
` = xi^T (W R_x + R_x^T W) xi`.

Hence a signed physical operator-defect rate `rho` also transports without loss.

### Rank boundary

If `J` is not injective, the equalities above still hold but `M` may be only
semidefinite.  Existence of an `e_z` satisfying (7.2) is then a real source-side
obligation.  The theorem must not silently write `e_z=J^{-1}e_x` unless
invertibility has separately been proved.

---

## 8. What must not be double-counted

There are now three distinct objects in the current P5 lane:

1. T-P5-087: a finite-step/moving-frame **Euler curvature defect** measured in a
   moving quadratic metric;
2. T-P5-088/T-P5-089: derivative of a **state storage**, with mechanical
   same-source cancellation when applicable;
3. T-P5-090/T-P5-091: **variational contraction energy** and robustness of its
   variational equation.

They can share quadratic-form helper lemmas, but their defect terms are not
interchangeable.  In particular, a T-P5-091 variational defect should not be
charged again as T-P5-088 storage drift merely because both formulas contain
`W`.

Likewise T-P5-091 assumes the nominal base path remains `xdot=-F`.  If the base
flow itself is perturbed, the material derivative of `W` changes and the
Jacobian of the base defect enters the variational equation.  That requires a
separate theorem; (1.3) must not be reused silently for a perturbed base path.

---

## 9. Suggested Lean theorem decomposition

The first formalization can remain finite-dimensional and source-independent.

1. `quad_cauchy_sq`
   - for symmetric PSD `W`, prove
     `(<x,y>_W)^2 <= Q_W(x)*Q_W(y)`.

2. `relative_defect_cross_le`
   - from `Q_W(e)<=rho^2*Q_W(x)` and `rho>=0`, derive
     `<x,e>_W <= rho*Q_W(x)` without square roots.

3. `variational_energy_deriv_with_defect`
   - exact identity
     `Vdot = -x^T C x + 2<x,e>_W`.

4. `robust_contraction_relative_defect`
   - derive `Vdot <= -2(mu-rho)V`.

5. `scaled_cross_young_sq`
   - from PSD of `W`, prove
     `2*lambda*<x,d>_W <= lambda^2*Q_W(x)+Q_W(d)`.
   - this is the key division-free leaf.

6. `robust_contraction_mixed_defect_sq`
   - with `nu=mu-rho>0`, prove
     `nu*Vdot <= -nu^2*V + Ebar`.

7. `mixed_defect_boundary_inward`
   - from `Ebar<=nu^2*Vstar` and `V=Vstar`, derive `Vdot<=0`.
   - leave actual first-exit/invariance calculus to a separate ODE barrier leaf.

8. `signed_operator_defect_rate`
   - consume `x^T(WR+R^TW)x <= 2rho Q_W(x)` directly.

9. `defect_power_pullback` and `defect_energy_pullback`
   - from `M=J^TWJ`, `xi=Jeta`, `Je_z=e_x`, prove (7.4)-(7.5).

10. `operator_defect_pullback_intertwining`
    - from `JR_z=R_xJ`, prove (7.7).

Items 2, 5, 6, 7, 8, 9, and 10 are especially suitable as small exact-real
algebraic sidecars before any differential-calculus API is introduced.

---

## 10. Minimal source packet for a deployed consumer

To consume this child without inventing data, a source lane should freeze on one
common spacetime tube:

- the T-P5-090 nominal contraction packet `(W,C,mu)`;
- the exact semantic split of the variational defect `e=r+d`;
- either a same-metric squared relative cap `Q_W(r)<=rho^2 V`, or the sharper
  signed operator certificate for `r=Rxi`;
- an additive same-metric squared cap `Q_W(d)<=Ebar`;
- `rho<mu`;
- a candidate `Vstar` with the exact gate `Ebar<=(mu-rho)^2 Vstar`;
- if consuming through a moving chart, exact `M=J^TWJ` and defect covariance
  `Je_z=e_x` (plus `JR_z=R_xJ` for the operator route);
- same-tube coverage and the first-exit/barrier premises needed to turn the
  boundary inequality into forward invariance.

Source generation should preserve the signed operator power before interval
absolute values.  For additive defects, emit a squared metric budget directly;
there is no need for a trusted square-root computation.

---

## 11. Status and remaining obligations

### Closed mathematically by this child

- exact variational-energy derivative with an additive defect;
- rate loss `mu -> mu-rho` for same-metric relative defects;
- a sharper signed symmetric-operator defect route;
- the division-free mixed-defect inequality
  `(mu-rho)Vdot <= -(mu-rho)^2 V + Ebar`;
- the exact invariant-boundary gate
  `Ebar <= (mu-rho)^2 Vstar`;
- the obstruction showing bounded additive defect cannot imply contraction to
  zero;
- lossless moving-chart transport of defect energy and defect power under
  `Je_z=e_x`;
- lossless operator-defect transport under `JR_z=R_xJ`.

### Still open

- deployed source binding of the actual variational defect and its split;
- same-tube exact rational `(mu,rho,Ebar,Vstar)` generation;
- metric coercivity if a genuine distance rather than seminorm is consumed;
- first-exit/ODE barrier formalization and coverage;
- perturbations of the base trajectory itself;
- stochastic/Itô noise;
- finite-separation/secant contraction beyond the variational equation;
- discrete integrators and controller/solve defects not already represented by
  `e`;
- Float64/FD execution semantics;
- P8/ODE physical trajectory coverage;
- Lean/kernel compilation and `#print axioms`;
- independent verification by 封不觉;
- comparator/admission/registry changes.

Accordingly T-P5-091 remains a **pending mathematical/interface child**.  It
must not be promoted to verified/admitted P5 status on the strength of this
review alone.
