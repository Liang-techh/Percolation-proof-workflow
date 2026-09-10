---
kind: review_result
review_id: review-T-P5-254-shared-quotient-jacobian-leakage-certificate-honglianmozun-20260910T1451Z
task_id: T-P5-254-SHARED-QUOTIENT-JACOBIAN-LEAKAGE-CERTIFICATE
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T14:51:30Z
claim_commit: 9d9d67792b1d611df915cf6dcde27085e5f126b1
inspected_commit: 75167e8ec94ec46ef869c4bb37603832696854fa
upstream_commits:
  - ced7eda6a74e19487f9d5f7be60bc4610cb28c97  # T-P5-253 nonlinear source transversality reserve
  - 856e645297c3e65bd14a5b0cd90668bc21908dff  # T-P5-252 source-slice partial metric coercivity
  - ef68d2faa4e23bdad40c700937eccfa6e9b78306  # T-P5-251 semidefinite normal metric range bridge
source_hashes:
  - 40967ab38de580498a5bf0254c6e69b7e2637702  # T-P5-253 review blob
  - f7a2db1f9d55ee80ecc11c59ebe05a9120295082  # agent_review_inbox/README.md
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_algebraic_complement_selector; add_shared_quotient_jacobian_domination; add_tangential_reparameterization_bridge; add_nonlinear_backtracking_obstruction
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional linear algebra; segment integral/Jensen energy estimate; rational polynomial counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-254 — Shared-quotient Jacobian certificate for nonlinear leakage

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-253 reduced nonlinear source transversality to a clean relative-leakage
obligation.  After writing the true residual as

`r = u + e`,  `u in range(D)`,

its coercivity theorem consumes an estimate

`||e||^2 <= delta ||u||^2`.

The remaining producer problem was to certify such a bound without constructing
an orthogonal projector or pseudoinverse and without charging nonlinear motion
which merely reparameterizes `range(D)`.

This child gives an exact route.  The key is to use a **shared quotient
coordinate** `theta` for both the tangential residual and the leakage.  If

`u(theta)=D theta`,  `e(theta)=E b(theta)`,  `b(0)=0`,

and the Jacobian satisfies the pointwise Gram domination

**(J)**

`J_b(theta)^T E^T E J_b(theta) <= delta D^T D`,

then on every star-shaped source region

**`||E b(theta)||^2 <= delta ||D theta||^2`.**

More strongly, on a convex source region the same packet gives the pairwise
quotient-Lipschitz estimate

**`||E(b(theta1)-b(theta0))||^2
   <= delta ||D(theta1-theta0)||^2`.**

No projector, pseudoinverse, singular vector, matrix square root, or algebraic
Lipschitz constant is needed.  For rational data the matrix inequality is
already a square-root-free PSD obligation.

A second result gives an algebraic complement certificate

`N D = 0`,  `N E = I`,

which makes the coefficient `b` in `D a + E b` intrinsic and proves that the
chosen `E` directions are independent modulo `range(D)`.  This is the exact
projector-free replacement for saying that `E` is a transverse coordinate
bundle.

Finally, a rational polynomial counterexample shows that one **cannot** replace
the shared linear quotient coordinate by a generic nonlinear tangential map and
compare only Jacobians.  Pointwise

`|e'(z)|^2 <= |u'(z)|^2`

can hold everywhere while `u` backtracks to zero and `e` remains nonzero.
Thus the shared-coordinate/fiber-factorization hypothesis is structural, not a
technical artifact.

No actual P5 residual formula, same-key source chart, cell/tube/trajectory
coverage, Float64/interval semantics, Lean receipt, independent verification,
admission, registry mutation, or parent closure is claimed.

---

# Part I — algebraic transverse coordinates without orthogonal projection

## 1. Setup

Let

`D : R^m -> R^r`,

`E : R^p -> R^r`

be linear maps.  Think of `range(D)` as the already-coercive tangential residual
image from T-P5-252/253 and `E b` as a producer-selected leakage component.

Orthogonality of `range(E)` and `range(D)` is unnecessary.  What is needed for
`b` to be an intrinsic transverse coordinate is that the columns of `E` be
independent **modulo** `range(D)`.

## 2. Theorem 1 — algebraic complement selector

The following are equivalent:

1. there exists `N : R^r -> R^p` such that

   **`N D = 0`,  `N E = I_p`;**

2. whenever

   `D x + E y = 0`,

   one has `y=0`;

3. the columns of `E` are linearly independent in the quotient
   `R^r / range(D)`;

4. **`rank([D E]) = rank(D) + p`.**

When `D,E` are rational and these conditions hold, `N` can be chosen rational.

### Proof

`1 -> 2` is immediate: apply `N` to `D x+E y=0` to obtain `y=0`.

`2 <-> 3` is exactly the definition of independence of the quotient classes of
the columns of `E`.

`3 <-> 4` is the usual rank increment statement: adjoining the `p` columns of
`E` raises the dimension by exactly `p` iff their quotient classes are
independent.

For `2 -> 1`, define a linear map on `range(D)+range(E)` by

`N_0(Dx+Ey)=y`.

Condition 2 makes this definition well-defined.  Extend `N_0` linearly to the
ambient residual space.  Then `N D=0` and `N E=I_p`.

For rational matrices, the equations `N D=0`, `N E=I_p` form a consistent
rational linear system, so exact Gaussian elimination returns a rational
solution. QED.

## 3. Why this is the right decomposition certificate

Suppose a nonlinear remainder is explicitly represented as

`n(theta)=D a(theta)+E b(theta)`.

If an algebraic selector `N` as above is supplied, then

**`b(theta)=N n(theta)`.**

Hence `b` is independent of the particular tangential coefficient `a` and is
uniquely determined by the physical remainder inside
`range(D)+range(E)`.

This is weaker and more flexible than Euclidean orthogonality.  It does not
pretend that `E b` is an orthogonal projection.  It merely certifies a direct
sum at the algebraic quotient level, which is all the T-P5-253 split needs.

### Exact failure boundary

If no such `N` exists, the chosen decomposition need not be intrinsic.  For the
one-dimensional example

`D=[1]`, `E=[1]`,

the same residual can be moved arbitrarily between `D a` and `E b`.  There is
no scalar `N` satisfying simultaneously `ND=0` and `NE=1`.

A relative leakage estimate for one chosen split may still be a valid
*sufficient* estimate, but it cannot be interpreted as a canonical transverse
leakage packet.

---

# Part II — shared-quotient Jacobian domination

## 4. Theorem 2 — pairwise quotient energy bound

Let `Omega subset R^m` be convex.  Let

`b : Omega -> R^p`

be continuously differentiable, and let `D,E` be fixed matrices as above.
Assume a scalar `delta>=0` such that for every `theta in Omega`,

**(4.1)**

`J_b(theta)^T E^T E J_b(theta)
 <= delta D^T D`.

Then for every `theta0,theta1 in Omega`,

**(4.2)**

`||E(b(theta1)-b(theta0))||^2
 <= delta ||D(theta1-theta0)||^2`.

### Proof

Set

`h=theta1-theta0`,

`theta(t)=theta0+t h`,  `0<=t<=1`.

Convexity keeps the segment inside `Omega`.  By the fundamental theorem of
calculus,

`E(b(theta1)-b(theta0))
 = integral_0^1 E J_b(theta(t)) h dt`.

Write

`v(t)=E J_b(theta(t))h`.

Cauchy-Schwarz/Jensen on the unit interval gives

`||integral_0^1 v(t)dt||^2
 <= integral_0^1 ||v(t)||^2 dt`.

By (4.1), pointwise

`||v(t)||^2
 = h^T J_b(theta(t))^T E^T E J_b(theta(t))h
 <= delta h^T D^T D h
 = delta ||D h||^2`.

The right side is independent of `t`.  Integrating over an interval of length
one yields (4.2). QED.

## 5. Origin-relative version

For the T-P5-253 consumer one usually only needs a basepoint estimate.  Convexity
can then be weakened to star-shapedness about `0`.

If `0 in Omega`, every segment `[0,theta]` lies in `Omega`, `b(0)=0`, and (4.1)
holds, then

**(5.1)**

`||E b(theta)||^2 <= delta ||D theta||^2`.

This is exactly the relative leakage inequality required upstream.

## 6. The Jacobian packet automatically kills source-kernel directions

Take any `k in ker(D)`.  From (4.1),

`0 <= ||E J_b(theta)k||^2
 <= delta ||Dk||^2 = 0`.

Therefore

**(6.1)** `E J_b(theta) k = 0`

for every `theta` and every `k in ker(D)`.

Thus the matrix PSD condition already includes the hard kernel-direction gate
which T-P5-253 identified as necessary.  No floating nullspace computation is
needed by the theorem statement.

## 7. Quotient factorization follows from the same estimate

The pairwise estimate gives an even stronger structural conclusion.  If

`D theta0 = D theta1`,

then `D(theta1-theta0)=0`, so (4.2) yields

`E b(theta1)=E b(theta0)`.

Therefore the physical leakage `e(theta)=E b(theta)` is constant on every
source fiber of `D` contained in the convex region.  Hence there is a unique
map on the quotient image

`e_bar : D(Omega) -> range(E)`

such that

**`e(theta)=e_bar(D theta)`.**

If the algebraic complement selector from Theorem 1 is also present, `E` is
injective, so even `b(theta)` itself is constant on these fibers and factors
through `D theta`.

This is useful conceptually: the Jacobian Gram gate is not merely a norm bound;
it proves that the proposed leakage genuinely descends to the same quotient
coordinate used by the tangential residual.

---

# Part III — fraction-free producer form

## 8. Rational scalar and PSD form

Suppose the producer chooses a rational

`delta=p/q`,  `p>=0`, `q>0`.

Then (4.1) is equivalent to the division-free matrix inequality

**(8.1)**

`p D^T D - q J_b(theta)^T E^T E J_b(theta) >= 0`.

Thus no square root of `delta` is needed.

If `b` is polynomial/rational on a semialgebraic source cell, (8.1) becomes a
matrix-polynomial nonnegativity obligation which can be discharged by whatever
exact source-domain mechanism is accepted upstream: a matrix-SOS identity,
Bernstein/rational interval packet, exact cell decomposition, or another
trusted theorem.  This review does **not** claim any such deployed source
certificate; it identifies the exact mathematical target that a producer must
prove.

## 9. Candidate formal theorem statement

A Lean-facing mathematical statement can avoid quotient objects entirely:

`sharedQuotient_jacobian_domination`

Inputs:

- convex `Omega`;
- differentiable `b`;
- fixed linear maps `D,E`;
- `delta>=0`;
- for every `theta in Omega` and vector `h`,

  `||E (Db(theta) h)||^2 <= delta ||D h||^2`.

Conclusion:

for `theta0,theta1 in Omega`,

`||E (b theta1-b theta0)||^2
 <= delta ||D(theta1-theta0)||^2`.

A second theorem can specialize to `theta0=0`, `b 0=0`.

The proof is only the line-segment integral plus Jensen/Cauchy-Schwarz and does
not depend on finite-dimensional spectral decomposition.

---

# Part IV — exact bridge into T-P5-253

## 10. Shared nonlinear reparameterization is free

Let a deployed residual be written in the form

**(10.1)**

`r(z)=D phi(z)+E b_bar(phi(z))`,

where `theta=phi(z)` takes values in a star-shaped set `Omega`,
`b_bar(0)=0`, and the Jacobian Gram gate

`J_bbar(theta)^T E^T E J_bbar(theta)
 <= delta D^T D`

holds on `Omega`.

Define

`u(z)=D phi(z)`,  `e(z)=E b_bar(phi(z))`.

Theorem 2 immediately gives

**(10.2)**

`||e(z)||^2 <= delta ||u(z)||^2`.

The size and nonlinearity of `phi` do not enter this estimate at all.

This is the cleanest continuation of the T-P5-253 principle that in-image
nonlinear reparameterization is free.  Even if

`phi(z)=z+a(z)`

has a large tangential correction, no reserve is spent provided the transverse
leakage is expressed as a function of the **same** quotient coordinate
`theta=phi(z)`.

Combining (10.2) with the T-P5-253 source-image packet

`u^T W u >= gamma ||u||^2`,  `W<=L I`,

gives its nonlinear coercivity branch whenever

**`L delta < gamma`**

(with a rational Young parameter `tau` chosen strictly between
`L delta/gamma` and `1`).

## 11. Why the shared-coordinate factorization is a real producer obligation

If the raw source formula is instead

`r(z)=D phi(z)+E b(z)`

with `b` depending on the old coordinate `z`, one cannot silently replace it by
`b_bar(phi(z))`.  The producer must establish that `E b(z)` is constant on the
fibers of `phi`, or provide an explicit `b_bar` satisfying

`E b(z)=E b_bar(phi(z))`.

If `phi` is a certified bijective chart, this can of course be done by
composition with its inverse.  If `phi` folds or has nontrivial fibers, the
factorization is additional mathematics.

The next part shows that this distinction cannot be omitted.

---

# Part V — exact nonlinear backtracking obstruction

## 12. Counterexample: Jacobian domination against a nonlinear `u` is not enough

A tempting but false replacement for Theorem 2 is:

> if `||e'(z)||^2 <= delta ||u'(z)||^2` pointwise, then
> `||e(z)||^2 <= delta ||u(z)||^2`.

This fails even for scalar rational polynomials on `[0,1]`.

Take

`u(z)=z-z^2`,

`e(z)=z-2z^2+(4/3)z^3`.

Then

`u(0)=e(0)=0`,

`u'(z)=1-2z`,

`e'(z)=(1-2z)^2`.

For every `z in [0,1]`, `|1-2z|<=1`, hence

**`|e'(z)|^2=(1-2z)^4 <= (1-2z)^2=|u'(z)|^2`.**

So the strongest pointwise derivative comparison with `delta=1` holds.
Nevertheless at the endpoint

`u(1)=0`,

`e(1)=1/3`.

Therefore no finite `delta` can satisfy

`|e(1)|^2 <= delta |u(1)|^2`.

The obstruction is geometric backtracking: the integral of `u'` cancels while
the integral of `e'` does not.  The shared **linear quotient** `D theta` in
Theorem 2 avoids exactly this cancellation, because

`D(theta1-theta0)`

is already the endpoint chord and is independent of the path.

This counterexample is why a generic nonlinear-Jacobian comparison should be
fail-closed rather than treated as a relative-leakage certificate.

## 13. Basepoint obstruction

The condition `b(0)=0` in the origin-relative theorem is also necessary.  A
constant nonzero leakage has zero Jacobian and therefore satisfies (4.1) with
`delta=0`, but clearly cannot satisfy

`||E b(theta)||^2 <= 0 * ||D theta||^2`.

For a nonzero reference point `theta_*`, the correct statement is the pairwise
one:

`||E(b(theta)-b(theta_*))||^2
 <= delta ||D(theta-theta_*)||^2`,

and any fixed base leakage `E b(theta_*)` must be handled separately.

---

# Part VI — fallback when leakage remains in the old coordinate

## 14. Small tangential reparameterization adapter

Sometimes the producer can certify the leakage relative to `D z` but cannot
rewrite it in the new coordinate `phi(z)=z+a(z)`.  There is still a rational
fallback if the tangential change is quantitatively small.

Assume

**(14.1)** `||e(z)||^2 <= delta0 ||D z||^2`,

and

**(14.2)** `||D a(z)||^2 <= epsilon ||D z||^2`.

Choose any rational `sigma` satisfying

**`epsilon < sigma < 1`.**

Set `x=Dz`, `y=Da(z)`.  From

`||sqrt(sigma) x + y/sqrt(sigma)||^2 >=0`

—or, equivalently, from the square-root-free Young inequality

`2 x.y >= -sigma||x||^2-sigma^{-1}||y||^2`—

we obtain

`||x+y||^2`

`>= (1-sigma)||x||^2-(sigma^{-1}-1)||y||^2`

`>= ((1-sigma)(sigma-epsilon)/sigma)||x||^2`.

Therefore, with

**(14.3)**

`kappa=((1-sigma)(sigma-epsilon))/sigma >0`,

we have

`||D(z+a(z))||^2 >= kappa ||Dz||^2`.

Combining with (14.1),

**(14.4)**

`||e(z)||^2 <= (delta0/kappa) ||D(z+a(z))||^2`.

A producer need not serialize the quotient.  To claim a rational leakage
constant `delta`, it is enough to check the division-free scalar gate

**(14.5)**

`delta (1-sigma)(sigma-epsilon) >= sigma delta0`.

Thus T-P5-253 can still be reached without inverting the nonlinear chart.

## 15. Composed coercivity gate

With T-P5-253 parameters `gamma,L`, the fallback branch admits some positive
coercivity reserve whenever

`L (delta0/kappa) < gamma`.

Equivalently, entirely without division,

**(15.1)**

`L sigma delta0
 < gamma (1-sigma)(sigma-epsilon)`.

This is a useful producer-level scalar screen.  Failure of this sufficient gate
is not automatically physical failure; it says only that the old-coordinate
leakage bound plus the supplied tangential-smallness packet cannot reach the
T-P5-253 reserve.

---

# Part VII — structural fingerprint and exact dispatch

## 16. New structural fingerprint

The resulting nonlinear source dispatch is:

**nonlinear residual**

`->` explicit split `n=D a+E b`

`->` optional algebraic complement selector `ND=0, NE=I`

`->` prefer shared quotient coordinate `theta=z+a(z)`

`->` pointwise Jacobian Gram domination

`J_bbar^T E^T E J_bbar <= delta D^T D`

`->` segment/Jensen integration

`->` exact relative leakage

`||E bbar(theta)||^2 <= delta ||D theta||^2`

`->` T-P5-253 nonlinear coercivity.

If the shared quotient factorization is unavailable:

`->` certify leakage against `Dz`

`->` certify small tangential change

`->` use the rational lower-chord gate (14.5)/(15.1).

If neither route is available, return a structural obstruction rather than
silently comparing nonlinear Jacobians.

## 17. Minimal producer packet

A clean producer packet for the preferred branch contains:

1. rational matrices `D,E`;
2. an explicit nonlinear quotient-coordinate formula `theta=phi(z)`;
3. an exact identity
   `r(z)=D theta+E b_bar(theta)`;
4. a star-shaped/convex source-domain witness for the relevant `theta` region;
5. basepoint `b_bar(0)=0` (or a translated pairwise version);
6. rational `delta>=0`;
7. an exact proof of the pointwise PSD inequality
   `delta D^TD-J_bbar^T E^TE J_bbar>=0` on that region;
8. optionally, a rational selector `N` with `ND=0`, `NE=I` to make the
   transverse coefficient intrinsic;
9. T-P5-253's existing `W,D,gamma,L` reserve data and scalar gate
   `L delta<gamma`.

No projector or pseudoinverse is part of the trusted packet.

---

# Part VIII — boundaries and next seam

## 18. What this closes mathematically

This child closes the *producer-side mathematical implication*

`Jacobian Gram domination on a shared quotient coordinate`

`=> relative transverse leakage bound`

`=> consumable T-P5-253 coercivity packet`.

It also gives a finite-dimensional algebraic certificate for the meaning of a
chosen transverse coefficient and proves exactly why a naive nonlinear
Jacobian replacement is unsafe.

## 19. What remains independent

This review does not establish:

- an actual P5 residual formula `r`, `D`, `E`, `phi`, or `b_bar`;
- a same-key algebraic complement selector for deployed source code;
- a source-domain proof of the Jacobian matrix inequality;
- source/cell/tube/trajectory/flowpipe/stencil/continuation coverage;
- T-P5-251's multiplier range gate for a concrete source;
- Float64/interval semantics;
- Lean/kernel compilation;
- independent validation by `封不觉`;
- admission, registry, or P5/P8/M4 parent closure.

## 20. Next distinct mathematical seam

Once a real nonlinear source formula is supplied, the next non-redundant
mathematical step is a **second-derivative-to-Jacobian-Gram reserve**.  Namely,
if the transverse component satisfies

`b_bar(0)=0`,  `J_bbar(0)=0`,

and the producer has a Hessian bound on a source ellipsoid, derive a
fraction-free matrix/radius packet which proves

`J_bbar(theta)^T E^T E J_bbar(theta)
 <= delta(R) D^T D`

with `delta(R)=O(R)` (where `R` is the squared source radius), while preserving
anisotropy of `D^TD` rather than collapsing to an ambient Euclidean norm.
That would convert the common "quadratic nonlinear remainder" data directly
into the exact shared-quotient certificate proved here.

---

## 21. Non-claims

Status remains **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding**.
This is a mathematical theorem packet only.  No provenance/receipt/admission
upgrade, registry mutation, or parent closure is asserted.