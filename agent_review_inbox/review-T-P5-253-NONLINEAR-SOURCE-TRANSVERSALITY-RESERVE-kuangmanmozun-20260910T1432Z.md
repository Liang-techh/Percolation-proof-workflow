---
kind: review_result
review_id: review-T-P5-253-nonlinear-source-transversality-reserve-kuangmanmozun-20260910T1432Z
task_id: T-P5-253-NONLINEAR-SOURCE-TRANSVERSALITY-RESERVE
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T14:35:30Z
claim_commit: 461b03702537fe92dc237612c9d060321c8aae67
inspected_commit: ac53dcf85333b57d4f77276d3638335a55b7b3c3
upstream_commits:
  - 856e645297c3e65bd14a5b0cd90668bc21908dff  # T-P5-252 source-slice partial metric coercivity
  - f01ba94dd82e9c4d1749f010e1a5fa6f1a6a1d8f  # T-P5-248 nonlinear chart defect reserve
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_range_preserving_nonlinear_residual_lemma; add_relative_leakage_coercivity_packet; add_second_order_radius_adapter; add_kernel_direction_obstruction_dispatch
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional PSD/Young algebra; rational threshold and kernel counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-253 — Nonlinear source transversality reserve

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-252 established the affine source-image packet

`u=Dz`,  `u^T W u >= gamma ||u||^2`,

with `W=W^T>=0`, even when `W` is singular in the ambient residual space.  Its
next seam was the nonlinear residual chart

`r(z)=Dz+n(z)`.

The main point of this child is that **not all of `n(z)` should be charged**.
A nonlinear reparameterization that remains inside `range(D)` is mathematically
free.  Only the component which leaks outside the already-coercive residual
image can rotate the true residual toward `ker(W)`.

This child therefore gives:

1. an exact no-loss theorem for range-preserving nonlinear residuals;
2. a rational, square-root-free Young/PSD packet for a small transverse
   leakage;
3. a sharp information-level threshold `L*delta < gamma` for the relative
   leakage ratio;
4. a second-order-radius adapter with the exact condition
   `L*K*R < gamma*m`;
5. a rational counterexample showing that generic `O(||z||^2)` remainder
   control is insufficient when `D` has a kernel;
6. a separate obstruction showing that a semidefinite `W`-energy bound on the
   leakage alone cannot imply Euclidean residual coercivity.

No actual P5 source/chart, same-cell/tube binding, coverage, Float64/interval
semantics, Lean receipt, independent verification, registry mutation, or
P5/P8/M4 parent closure is claimed.

---

# Part I — only transverse leakage costs reserve

## 1. Base affine packet

Let `W=W^T>=0` on a finite-dimensional Euclidean residual space.  Let
`U=range(D)` and assume a producer has supplied the T-P5-252 Gram gap

`D^T W D >= gamma D^T D`,  `gamma>0`.

Equivalently, every `u in U` satisfies

**(1)** `u^T W u >= gamma ||u||^2`.

Assume also an upper metric packet

**(2)** `W <= L I`,  `L>=0`,

or the same upper bound restricted to the span actually used below.  In exact
rational work (2) is just the PSD check `L I-W>=0`.

## 2. Theorem 1 — range-preserving nonlinear reparameterization is free

Suppose

`r(z)=D z+n(z)`

and for every relevant `z` there exists some (possibly nonlinear) `a(z)` with

`n(z)=D a(z)`.

Then

`r(z)=D(z+a(z)) in U`,

so by (1)

**`r(z)^T W r(z) >= gamma ||r(z)||^2`.**

There is **no degradation at all**, irrespective of the size or nonlinearity of
`a(z)`.

This is the correct first dispatch.  Charging the full nonlinear remainder by
an ambient norm can be arbitrarily conservative if the remainder merely
reparameterizes the same residual image.

### Formalizable statement

`coerciveOnRange_preserved_of_rangeValuedRemainder`:

If `forall v in range(D), gamma*||v||^2 <= v^T W v` and
`forall z, n z in range(D)`, then

`gamma*||D z+n z||^2 <= (D z+n z)^T W (D z+n z)`.

No inverse, projector, basis, or square root is required.

---

# Part II — exact rational reserve for transverse leakage

## 3. Tangential/leakage split

More generally, suppose the producer gives an explicit algebraic split

`r = u+e`,

where

- `u in U=range(D)` is the in-image/tangential part (it may already include a
  nonlinear reparameterization `D a(z)`);
- `e` is the remaining leakage.

Assume

**(3)** `||e||^2 <= delta ||u||^2`,  `delta>=0`.

The point of (3) is that it controls only the dangerous leakage.  It does not
penalize the range-preserving part.

## 4. Algebraic W-Young inequality without square roots

For every `tau>0`, PSD of `W` gives

`(tau*u+e)^T W (tau*u+e) >=0`.

Dividing by the positive scalar `tau` yields

**(4)** `2 u^T W e >= -tau u^T W u -(1/tau)e^T W e`.

Therefore, for `0<tau<1`,

`(u+e)^T W (u+e)`

`>= (1-tau) u^T W u -(1/tau-1)e^T W e`.

Using (1), (2), and (3),

**(5)**

`(u+e)^T W (u+e)`

`>= ((1-tau)(gamma*tau-L*delta)/tau) ||u||^2`.

Hence positivity of the numerator is exactly the simple scalar gate

**(6)** `L*delta < gamma*tau`, with `0<tau<1`.

No square root occurs anywhere in the checker packet.

## 5. Algebraic Euclidean upper comparison

To compare against the norm of the *true* residual `r=u+e`, choose any
`sigma>0`.  The identity

`||sigma*u-e||^2>=0`

gives

`2 u.e <= sigma||u||^2 +(1/sigma)||e||^2`.

Thus

**(7)**

`||u+e||^2`

`<= [(1+sigma)+(1+1/sigma)delta] ||u||^2`

`= ((sigma+1)(sigma+delta)/sigma)||u||^2`.

Combining (5) and (7) gives the main quantitative theorem.

## 6. Theorem 2 — rational degraded coercivity

Assume (1)--(3) and choose rational parameters

`0<tau<1`,  `sigma>0`,  `L*delta < gamma*tau`.

Define

**(8)**

`Gamma_eff = sigma(1-tau)(gamma*tau-L*delta)`

`            / [tau(sigma+1)(sigma+delta)]`.

Then `Gamma_eff>0` and

**(9)**

`(u+e)^T W (u+e) >= Gamma_eff ||u+e||^2`.

This is a directly checkable nonlinear-source transversality packet.

### Division-free checker form

A producer does not need to serialize the quotient in (8).  It can provide a
rational `g>0` and prove

**(10)**

`g*tau*(sigma+1)*(sigma+delta)`

`<= sigma*(1-tau)*(gamma*tau-L*delta)`.

Together with the sign gates this implies

`r^TWr >= g||r||^2`.

Thus an exact checker needs only rational scalar inequalities plus the existing
PSD packets for the base lower gap and upper metric bound.

### Suggested theorem statement

`nonlinearResidual_coercive_of_relativeLeakage`:

Given `W>=0`, `W<=L I`, `u^TWu>=gamma||u||^2`,
`||e||^2<=delta||u||^2`, `0<tau<1`, `sigma>0`, and
`L*delta<gamma*tau`, conclude (9), or conclude the division-free version with a
producer-supplied `g` satisfying (10).

---

# Part III — the leakage threshold and its sharp obstruction

## 7. Qualitative threshold

If

**(11)** `L*delta < gamma`,

then because the rationals are dense one can choose a rational

`L*delta/gamma < tau < 1`.

Theorem 2 then yields some rational `Gamma_eff>0`.  Therefore the affine
transversality survives every relative leakage satisfying (3) whenever (11)
holds.

The exact numerical `Gamma_eff` from a chosen `tau,sigma` is not claimed sharp;
the important point is that the **domain of guaranteed survival** reaches the
natural threshold `L*delta<gamma` without square roots.

## 8. Rational threshold counterexample

The strict inequality in (11) cannot be replaced by a universal non-strict
condition using only the information `(gamma,L,delta)`.

Take

`W = [[1,0],[0,0]]`,  so `L=1`.

Let the one-dimensional affine residual image be spanned by

`d=(3/5,4/5)`.

Since `||d||=1` and

`d^T W d = 9/25`,

the exact base gap is

`gamma=9/25`.

Choose the leakage

`e=(-3/5,0)`.

Then

`||e||^2=9/25 = delta ||d||^2`

with

`delta=9/25 = gamma/L`.

But

`d+e=(0,4/5) in ker(W)`,

so

`(d+e)^T W(d+e)=0`

while `||d+e||^2=16/25>0`.

Thus no positive effective coercivity constant exists at the threshold.
This is an exact rational counterexample; no floating eigenvector is involved.

### Geometric interpretation

The base residual image may approach `ker(W)` at an angle controlled only by
the ratio `gamma/L`.  A leakage of exactly that information-level size can
rotate a nonzero residual all the way into the invisible kernel.  The strict
reserve in (11) is therefore not a proof artifact.

---

# Part IV — second-order nonlinear chart remainder

## 9. From coordinate-quadratic leakage to relative leakage

A common source packet does not initially give (3).  Instead it may give a
second-order estimate

**(12)** `||e(z)||^2 <= K ||z||^4`,

on a coordinate ball

**(13)** `||z||^2 <= R`.

To turn this into a relative residual estimate, one needs a lower singular gap
for the *source coordinate quotient* actually being used:

**(14)** `||D z||^2 >= m ||z||^2`,  `m>0`.

Then

`||e(z)||^2 <= K R ||z||^2 <= (K R/m)||Dz||^2`.

Hence Theorem 2 applies with

**(15)** `delta = K R/m`.

The radius gate (11) becomes the completely fraction-free condition

**(16)** `L*K*R < gamma*m`.

This is the exact radius-squared scaling one expects: a second-order chart
remainder consumes a first-order transversality angle only linearly in the
coordinate radius-squared `R`.

## 10. Corollary — certified nonlinear radius

Assume

- `D^T W D >= gamma D^T D`, `gamma>0`;
- `W<=L I`;
- `D^T D >= m I` on the chosen source-coordinate quotient, `m>0`;
- `||e(z)||^2 <= K||z||^4` for `||z||^2<=R`;
- `L K R < gamma m`.

Then there exists an explicit rational `g>0`, obtained from any rational
`tau,sigma` satisfying Theorem 2, such that

`r(z)^T W r(z) >= g ||r(z)||^2`

throughout that certified radius.

This is the direct bridge from T-P5-252's affine Gram gap to the second-order
nonlinear-chart style of T-P5-248.

---

# Part V — why kernel(D) cannot be ignored

## 11. Exact obstruction to a naive O(||z||^2) theorem

The lower coordinate gap (14), or an equivalent quotient/tangent restriction,
is essential.  A generic second-order remainder in source coordinates does
**not** preserve transversality when `D` has a kernel.

Take

`W = [[1,0],[0,0]]`,

`D = [[1,0],[0,0]]`,

and the polynomial nonlinear remainder

`n(z1,z2) = (0,z2^2)`.

For the linear residual `Dz=(z1,0)`,

`(Dz)^T W(Dz)=||Dz||^2`,

so the affine packet has the strongest possible constants

`gamma=L=1`.

Moreover

`||n(z)||^2=z2^4 <= (z1^2+z2^2)^2 = ||z||^4`,

so (12) holds with `K=1` on every radius.

However along the source-kernel direction `z=(0,t)`, `t!=0`,

`Dz=0`,

`r(z)=n(z)=(0,t^2) in ker(W)`,

and therefore

`r(z)^TWr(z)=0 < g||r(z)||^2`

for every `g>0`.

This fails in **every punctured neighborhood**, no matter how small the radius
is.

### Dispatch consequence

When `ker(D)` is nontrivial, a producer must do at least one of the following:

1. quotient/fix the source gauge so that `D` has a positive lower gap `m`;
2. prove the nonlinear remainder vanishes on `ker(D)` and supply a relative
   leakage estimate against `||Dz||`;
3. prove the nonlinear residual generated by kernel directions remains inside a
   separate W-coercive subspace;
4. keep those kernel fibers as an independent nonlinear obligation.

Silently applying a coordinate `O(||z||^2)` estimate is unsound.

---

# Part VI — W-energy control alone is not Euclidean coercivity

## 12. Second obstruction

Because `W` is allowed to be singular, a bound only on the leakage's W-energy
cannot control its invisible Euclidean component.

Again take

`W=diag(1,0)`, `U=span(e1)`, `gamma=L=1`.

Let `u=e1` and `e=T e2`.  Then

`e^TWe=0`

for every `T`, so even the strongest possible seminorm statement

`e^TWe <= 0*u^TWu`

holds.  But

`(u+e)^TW(u+e)=1`,

while

`||u+e||^2=1+T^2`.

No positive coercivity constant uniform in `T` follows.

Therefore, if a T-P5-248-style producer supplies the nonlinear remainder only
in a **singular** W-seminorm, that packet is insufficient for the Euclidean
transversality conclusion of T-P5-252.  One additionally needs an Euclidean
leakage bound, a coercive remainder metric `V>=m_e I`, or a structural range
constraint.

A convenient metric adapter is:

if `V>=m_e I`, `m_e>0`, and

`e^T V e <= delta_V ||u||^2`,

then

`||e||^2 <= (delta_V/m_e)||u||^2`,

so Theorem 2 applies with `delta=delta_V/m_e`.

---

# Part VII — exact checker packet

## 13. Minimal producer packet for the relative-leakage branch

A checker can consume:

1. exact rational `W,D,gamma,L`;
2. PSD witness `D^TWD-gamma D^TD>=0`;
3. PSD witness `L I-W>=0` (or a restricted-span version);
4. an exact residual split `r=u+e` with `u in range(D)`;
5. exact rational `delta>=0` and a source theorem
   `||e||^2<=delta||u||^2`;
6. rational `tau,sigma,g`;
7. scalar sign checks
   `0<tau<1`, `sigma>0`, `g>0`, `L*delta<gamma*tau`;
8. the division-free scalar budget (10).

Then the conclusion is simply

`r^TWr >= g||r||^2`.

No pseudoinverse, projector, singular vector, square root, or floating angle is
needed.

## 14. Minimal producer packet for the second-order-radius branch

Replace item 5 by:

- `D^TD>=m I` on the chosen source quotient, `m>0`;
- `||e(z)||^2<=K||z||^4`;
- `||z||^2<=R`;
- exact radius gate `L K R < gamma m`.

Then set `delta=K R/m`, or keep the entire proof fraction-free by cross
multiplying all positive denominators.

---

# Part VIII — relation to the current P5 frontier

## 15. What this closes mathematically

T-P5-252's affine statement can now be extended to nonlinear residual charts in
three explicit lanes:

- **range-preserving lane:** no reserve loss at all;
- **relative transverse-leakage lane:** rational Young packet (8)--(10);
- **second-order coordinate lane:** after quotient coercivity, radius condition
  `L K R < gamma m`.

The theorem also identifies two exact failure/route conditions rather than
allowing a generic optimizer fallback:

- `ker(D)` plus unconstrained nonlinear kernel-fiber residuals;
- leakage known only in a singular W-seminorm.

These are structural obligations, not numerical conditioning accidents.

## 16. What remains independent

This child does not establish:

- actual P5 `W,D,n` or a same-key nonlinear residual chart;
- the algebraic tangential/leakage decomposition for deployed source code;
- source/cell/tube/trajectory/flowpipe/stencil/continuation coverage;
- the T-P5-251 multiplier range gate;
- Float64/interval semantics;
- Lean/kernel compilation;
- independent validation by `封不觉`;
- admission, registry, or P5/P8/M4 parent closure.

## 17. Next distinct mathematical seam

The useful next seam is to certify the **relative leakage inequality itself**
without constructing an orthogonal projector or pseudoinverse.  A natural
packet is a producer-supplied factorization

`n(z)=D a(z)+E b(z)`

with exact quadratic/Jacobian bounds on `b(z)` and an algebraic separation
certificate for `range(E)` versus `range(D)`.  The goal should be a block-PSD or
fraction-free Jacobian condition that directly proves

`||E b(z)||^2 <= delta ||D(z+a(z))||^2`

on a source radius.  That would connect the theorem here to deployed nonlinear
source formulas while preserving the distinction between free tangential
reparameterization and dangerous normal leakage.

---

## 18. Non-claims

Status remains **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding**.
No registry/admission/provenance claim is made by this mathematical result.