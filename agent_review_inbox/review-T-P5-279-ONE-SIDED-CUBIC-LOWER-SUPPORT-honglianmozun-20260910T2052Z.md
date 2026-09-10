---
kind: review_result
review_id: review-T-P5-279-one-sided-cubic-lower-support-honglianmozun-20260910T2052Z
task_id: T-P5-279-ONE-SIDED-CUBIC-LOWER-SUPPORT
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T20:52:00Z
claim_commit: e6013ffa27afd80f9fac80aecf184629b390e788
inspected_commit: e91c53591227cb1d4197c5580d0e3c12dcc2b09e
upstream_commits:
  - d6c44a2fda8af5f197bd2a0032ab982cce577be6 # T-P5-278 structured quadratic-graph reserve
  - 1a6f2fb0616fd3d695673dbae48d4e0f7f789a94 # T-P5-277 strong-convexity reserve perturbation
  - d062e528bc248cd24f09973dcde7cfcf7c00ffae # T-P5-266 zero-margin univariate Sturm certificate
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_directionalThirdDerivative_lowerCubic; add_oneSidedCubic_robust_iff; add_cubicCritical_linearReduction; add_twoSided_oriented_split; add_signedCubic_beats_symmetricTube; preserve_orientation_and_source_boundaries
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact one-dimensional Taylor-integral derivation; cubic critical-point elimination; rational counterexample regressions; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
source_hashes: source_independent_mathematical_child
---

# T-P5-279 — One-sided cubic lower support from directional third derivatives

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-278 retained signed linear/quadratic perturbation data and then placed the unresolved part in a symmetric graph tube. Its final section left a precise optional seam: on a **one-sided clamp fiber**, an odd cubic contribution should not automatically be replaced by an absolute-value tube, because the sign of the cubic is physically meaningful on a fixed orientation.

This child closes that abstract mathematical seam without introducing another generic root solver.

The key observation is that for lower-bound / Lyapunov safety, a one-sided lower bound on the **directional third derivative** is already enough. No upper third-derivative bound is required.

Fix an orientation `sigma in {+1,-1}` and write the one-sided fiber as

`x(t) = y + sigma t`, `0 <= t <= U`.

Suppose the nominal target has the same strong-convexity support consumed in T-P5-277/T-P5-278,

`p(y+sigma t) >= p(y) + (mu/2)t^2`,

and the anchor reserve is

`p(y)+e(y)-eta >= R`.

Let

`a = e'(y)`, `d = e''(y)`.

If the directional third derivative satisfies

**(D3)** `sigma * e'''(y+sigma r) >= 6 c` for every `0<=r<=U`,

then the exact Taylor-integral lower support is

**(E3)**

`e(y+sigma t)-e(y) >= sigma a t + (d/2)t^2 + c t^3`.

Therefore

**(CubicSupport)**

`2[p(y+sigma t)+e(y+sigma t)-eta]`

`>= F_sigma(t)`

with

**`F_sigma(t) = 2R + 2 sigma a t + (mu+d)t^2 + 2c t^3`.**

Thus the one-sided safety problem is reduced to **one cubic polynomial** on `[0,U]`. It does not require the naive symmetric elimination

`H(t)^2 - K t^6 >= 0`

that appears when the same third-order information is first converted to `|w(t)| <= const*t^3`.

Moreover the reduction is **sharp relative to the directional-third-derivative abstraction**: the extremal cubic perturbation with `sigma e'''=6c` attains equality in (E3), so no uniformly stronger lower support can be deduced from only the anchor value, first two derivatives, and (D3).

For rational polynomial data, both producer and consumer remain exact-rational:

1. certify `sigma e'''(y+sigma t)-6c >= 0` on `[0,U]` by the existing T-P5-266 zero-margin univariate machinery (or Bernstein on a strict branch);
2. certify the cubic `F_sigma>=0` on `[0,U]` by the same machinery.

A smaller calculus packet is also available: the derivative of `F_sigma` is only quadratic, and the value of the cubic at any critical point reduces fraction-free to a **linear** expression in that quadratic root.

No actual P5 coefficient packet, selected algebraic root, FD evaluator, source key, moved endpoint, collar, whole-cell/trajectory/FD/reference-halo coverage, Float64/libm enclosure, Lean/kernel proof, independent validation, admission, registry mutation, or P5/P8/M4 propagation is claimed.

---

## 1. Orientation-aware setup

Fix one same-key scalar fiber context.

Let

- `sigma in {+1,-1}`;
- `U>=0`;
- `t in [0,U]`;
- `x(t)=y+sigma t`.

The orientation is part of the theorem data. It must not be discarded.

Assume:

**(N1)** `p(y+sigma t) >= p(y) + (mu/2)t^2` for every `t in [0,U]`;

**(N2)** `p(y)+e(y)-eta >= R`;

**(N3)** `e` is `C^3` on the oriented segment;

**(N4)** `a=e'(y)` and `d=e''(y)`;

**(N5)** `sigma e'''(y+sigma r) >= 6c` for every `r in [0,U]`.

In the T-P5-278 notation where

`e(y+s)-e(y)=a s+b s^2+...`,

one simply has `d=2b`, so

`mu+d = mu+2b`.

The theorem below therefore consumes exactly the same retained linear/quadratic data and adds one directional cubic lower coefficient.

---

## 2. Lemma A — oriented third derivative gives a cubic lower remainder

Define

`f(t)=e(y+sigma t)`.

Because `sigma^2=1` and `sigma^3=sigma`,

`f'(0)=sigma a`,

`f''(0)=d`,

`f'''(r)=sigma e'''(y+sigma r)`.

The second-order Taylor formula with integral remainder is

**(2.1)**

`f(t)-f(0)`

`= sigma a t + (d/2)t^2`

`  + (1/2) integral_0^t (t-r)^2 [sigma e'''(y+sigma r)] dr`.

Under (N5),

`(1/2) integral_0^t (t-r)^2 [sigma e'''(...)] dr`

`>= (1/2) integral_0^t (t-r)^2 6c dr`

`= 3c * (t^3/3)`

`= c t^3`.

Hence

**(2.2)**

`e(y+sigma t)-e(y)`

`>= sigma a t + (d/2)t^2 + c t^3`.

This proves (E3).

### Fraction-free producer form

The theorem does not require a serialized division by `6`.

A rational producer may submit `c in Q` together with the polynomial/nonlinear inequality

**`sigma e'''(y+sigma t) - 6c >= 0`.**

Thus the trusted packet contains only multiplication by the integer `6`.

### Why only a lower derivative bound is needed

For a lower Lyapunov reserve, arbitrarily large positive values of the directional third derivative only increase the target. The dangerous direction is downward. Therefore replacing (N5) by a symmetric square bound

`(e''')^2 <= K`

forgets useful sign information and can be strictly more conservative.

---

## 3. Theorem B — sharp one-sided cubic Lyapunov support

Under (N1)–(N5), define

`m := mu+d`,

`A := sigma a`,

and

**(3.1)** `F(t) := 2R + 2A t + m t^2 + 2c t^3`.

Then for every `t in [0,U]`,

**(3.2)**

`2[p(y+sigma t)+e(y+sigma t)-eta] >= F(t)`.

### Proof

By (N1),

`p(y+sigma t)-p(y) >= (mu/2)t^2`.

By Lemma A,

`e(y+sigma t)-e(y) >= A t + (d/2)t^2 + c t^3`.

Adding these inequalities to the anchor reserve (N2) gives

`p(y+sigma t)+e(y+sigma t)-eta`

`>= R + A t + ((mu+d)/2)t^2 + c t^3`.

Doubling yields (3.2).

Therefore

**(3.3)** `F(t)>=0 on [0,U]`

is a sound certificate for

`p(y+sigma t)+e(y+sigma t)>=eta` on the full one-sided fiber.

---

## 4. Theorem C — exactness relative to the one-sided derivative abstraction

The cubic support is not merely a convenient sufficient Young-style bound.

Fix numbers `R,A,m,c,U` and consider the abstract class in which the checker knows only:

1. the anchor lower reserve `R`;
2. the nominal quadratic lower support `mu`;
3. the first two perturbation derivatives summarized by `A` and `d=m-mu`;
4. the one-sided directional third-derivative lower bound `sigma e'''>=6c`.

Then the worst admissible perturbation is attained by the cubic extremal

**(4.1)**

`e_ext(y+sigma t)-e_ext(y) = A t + (d/2)t^2 + c t^3`,

for which

`sigma e_ext''' = 6c` identically.

Likewise the nominal lower support can be saturated by

**(4.2)**

`p_ext(y+sigma t)-p_ext(y) = (mu/2)t^2`.

Therefore the abstract robust statement

> every pair `(p,e)` satisfying the trusted lower-support premises is safe on `[0,U]`

holds **if and only if**

**`F(t)>=0 for every t in [0,U]`.**

If `F(t0)<0` at some `t0`, the extremal polynomial pair (4.1)–(4.2) is an admissible counterexample to the abstraction.

This exactness statement is deliberately about the **outer mathematical model**. Failure of `F>=0` does not by itself prove that a particular deployed P5 evaluator is unsafe unless the deployed source is actually known to realize the extremal model or an explicit same-key state witness is reconstructed.

---

## 5. Lemma D — robust half-tube interpretation

The same result can be written as an exact robust elimination theorem.

Let

`H0(t)=2R+2At+m t^2`.

Suppose the unresolved signed remainder `w(t)` is constrained only by the one-sided graph half-tube

**(5.1)** `w(t) >= c t^3`, `0<=t<=U`.

Then the following are equivalent:

**(D1)** for every `t` and every admissible `w`, `H0(t)+2w(t)>=0`;

**(D2)** `H0(t)+2c t^3>=0` for every `t`.

The proof is immediate:

- (D2) implies (D1) because `w>=ct^3`;
- if (D2) fails at `t0`, choose the admissible extremal `w(t0)=ct0^3`.

Thus the one-sided tube is eliminated by **substitution at its lower face**, not by squaring.

This is the structural reason the polynomial degree stays at three.

---

## 6. Exact bounded-fiber decision by a quadratic derivative

For

`F(t)=2R+2At+m t^2+2c t^3`,

the derivative is

**(6.1)** `F'(t)=2 q(t)`

with

**`q(t)=A+m t+3c t^2`.**

Therefore a complete calculus characterization on `[0,U]` is:

**(6.2)** `F>=0 on [0,U]`

if and only if

1. `F(0)=2R>=0`;
2. `F(U)>=0`;
3. `F(tau)>=0` for every real root `tau` of `q` in `(0,U)`.

There are at most two such critical points.

Hence the one-sided cubic path never requires solving a cubic equation. The only algebraic points are roots of a quadratic.

For rational data, an implementation may either:

- route the cubic directly through T-P5-266; or
- isolate the at-most-two roots of `q` using exact quadratic/Sturm/Thom machinery and evaluate the critical reserve using the fraction-free identity in the next section.

---

## 7. Lemma E — fraction-free linear reduction at cubic critical points

Assume `c!=0` and define

**(7.1)**

`L(t) := (12 A c - m^2)t + (18 R c - A m)`.

Then the following polynomial identity holds identically in `t`:

**(7.2)**

`9 c F(t) = (6 c t + m) q(t) + L(t)`.

### Verification

Using

`F=2R+2At+m t^2+2c t^3`

and

`q=A+m t+3c t^2`,

the cubic, quadratic, linear and constant coefficients agree term by term after expansion.

At any critical point `tau` satisfying `q(tau)=0`, (7.2) reduces to

**(7.3)** `9 c F(tau)=L(tau)`.

Multiplying by `c` gives

**(7.4)** `9 c^2 F(tau)=c L(tau)`.

Because `9c^2>0`,

**(7.5)**

`F(tau)>=0  <=>  c L(tau)>=0`.

So the value of the **cubic** at a critical point reduces exactly to the sign of a **linear polynomial** at a root of a quadratic.

This is a convenient checker/formalization packet:

- isolate a root of `q` in `(0,U)`;
- determine the sign of `cL` at that selected quadratic root by a signed-subresultant/Thom test;
- never serialize a radical.

The degenerate case `c=0` is simply the existing quadratic reserve problem and must be routed separately rather than dividing by `c`.

---

## 8. Two-sided collars must be split by orientation

Suppose the actual fiber crosses the anchor `y`:

`[y-U_-, y+U_+]`.

The odd cubic term cannot be represented by one unsigned coefficient without losing information.

Split the fiber into two oriented halves.

### Right side

Take `sigma=+1` and choose `c_+` satisfying

**(8.1)** `e'''(y+r) >= 6c_+`, `0<=r<=U_+`.

Then

**(8.2)**

`F_+(t)=2R+2a t+(mu+d)t^2+2c_+ t^3`.

### Left side

Take `sigma=-1` and choose `c_-` satisfying

**(8.3)** `-e'''(y-r) >= 6c_-`, `0<=r<=U_-`.

Equivalently,

`e'''(y-r) <= -6c_-`.

Then

**(8.4)**

`F_-(t)=2R-2a t+(mu+d)t^2+2c_- t^3`.

The complete two-sided certificate is simply

**(8.5)**

`F_+>=0 on [0,U_+]`

and

`F_->=0 on [0,U_-]`.

### If only a third-derivative interval is known

If a source packet gives

`L3 <= e''' <= U3`

on the entire collar, then a fraction-free choice is any rational pair satisfying

`6c_+ <= L3`,

`6c_- <= -U3`.

The right and left coefficients are generally different. This is not bookkeeping noise; it is the exact odd-parity content.

---

## 9. Strict separation from a symmetric cubic tube

There are cases where the one-sided signed certificate is strict PASS while the best natural symmetric cubic tube fails.

Take the right fiber `t in [0,1]`, anchor `y=0`, threshold `eta=0`, and define

**Nominal target**

`p(t)=1/2 + t^2/2`.

Thus `mu=1` and the anchor nominal value is `1/2`.

**Perturbation**

`e(t)=-t^2/2+t^3`.

Then

`a=e'(0)=0`,

`d=e''(0)=-1`,

`e'''(t)=6`.

Hence

`R=1/2`, `m=mu+d=0`, `c=1`.

The actual target is

**(9.1)** `p(t)+e(t)=1/2+t^3 >= 1/2`.

The present signed cubic support is

**(9.2)** `F(t)=1+2t^3 >= 1`.

So the certificate passes with a strict doubled reserve of at least `1`.

Now discard the sign of the cubic residual and encode only

`w(t)=t^3`,

`4w(t)^2 <= 4t^6`.

The retained quadratic support is only

`H0(t)=1`.

A symmetric robust elimination must allow the adversarial residual `w=-t^3`, so it requires

**(9.3)** `H0(t)^2 - 4t^6 = 1-4t^6 >=0`.

At `t=1`, (9.3) equals `-3` and fails.

Thus:

- actual/signed model: strict PASS;
- optimal symmetric magnitude information for this exact cubic residual: CERTIFICATE NOT FOUND.

The loss is entirely caused by forgetting the one-sided odd sign.

---

## 10. Orientation is a hard gate: reusing the right cubic on the left can false-pass

Use the same physical formulas as Section 9 but evaluate the left fiber `s=-t`, `0<=t<=1`.

The actual target is now

`p(-t)+e(-t)=1/2-t^3`.

At `t=1` this equals `-1/2`, so the left side is unsafe for threshold `0`.

For the left orientation `sigma=-1`,

`-e'''(-t)=-6`,

so the sharp directional coefficient is `c_-=-1`.

The correct left cubic support is

**(10.1)** `F_-(t)=1-2t^3`,

which detects the failure at `t=1`.

If one incorrectly copied the right-side coefficient `c_+=+1` onto the left side, one would instead obtain

`1+2t^3>0`

and produce a false PASS.

Therefore the orientation label / side-of-clamp information is a **soundness premise**, not merely an optimization hint.

---

## 11. Structural fingerprint

The new structural fingerprint is:

**one-sided clamp fiber**

`-> retain orientation sigma`

`-> lower-bound directional third derivative, not its magnitude`

`-> positive-kernel Taylor integral`

`-> signed cubic lower graph`

`-> cubic Lyapunov reserve`

`-> quadratic stationary equation`

`-> linear critical-value reduction`

`-> exact rational/Sturm-Thom checker`.

The key distinction from the T-P5-278 symmetric graph tube is geometric:

- a symmetric tube models ignorance in **both** signs and therefore pays an absolute-value debit;
- the present half-tube models a known **lower face** and therefore substitutes that face directly.

For lower-bound safety, upper deviations are beneficial and need not consume reserve.

---

## 12. Candidate theorem statements

A Lean/formal-math decomposition should keep calculus, robust elimination, and polynomial closure separate.

### 12.1 `directionalThirdDerivative_lowerCubic`

Inputs:

- `sigma^2=1`;
- `0<=t<=U`;
- `f` three-times differentiable on the oriented segment;
- `a=f'(y)`, `d=f''(y)`;
- `sigma*f'''(y+sigma*r)>=6*c` on the segment.

Conclusion:

`f(y+sigma*t)-f(y) >= sigma*a*t + (d/2)*t^2 + c*t^3`.

### 12.2 `oneSidedCubic_robust_iff`

For arbitrary `H0`,

`forall w>=c*t^3, H0+2w>=0`

iff

`H0+2c*t^3>=0`.

This is the exact half-tube elimination leaf.

### 12.3 `strongConvex_directionalCubic_reserve`

Combine the T-P5-277 nominal support and 12.1 to derive

`2*(p+e-eta) >= 2R+2*sigma*a*t+(mu+d)*t^2+2*c*t^3`.

### 12.4 `cubicCritical_linearReduction`

For

`F=2R+2At+m*t^2+2c*t^3`,

`q=A+m*t+3c*t^2`,

prove the polynomial identity

`9*c*F=(6*c*t+m)*q + (12*A*c-m^2)*t + (18*R*c-A*m)`.

At `q=0`, derive the fraction-free sign equivalence

`F>=0 <=> c*((12*A*c-m^2)*t+(18*R*c-A*m))>=0`

under `c!=0`.

### 12.5 `twoSidedDirectionalCubic_split`

Split `[y-U_-,y+U_+]` into `sigma=-1` and `sigma=+1` fibers and combine the two cubic certificates.

### 12.6 `signedCubic_strictlyBeatsSymmetricTube`

Hard-code Section 9's rational polynomial regression.

This should remain as a permanent guard against later refactors that replace directional third-derivative data by a symmetric square bound.

---

## 13. Checker routing

For a same-key rational polynomial perturbation on a one-sided fiber:

1. obtain `sigma,U,y,mu,R` from the already-certified clamp/strong-convexity context;
2. retain exact/safely enclosed `a=e'(y)` and `d=e''(y)` from the **same** perturbation source;
3. choose rational `c` and certify
   `sigma e'''(y+sigma t)-6c>=0` on `[0,U]`;
4. construct
   `F=2R+2sigma*a*t+(mu+d)t^2+2c*t^3`;
5. certify `F>=0` on `[0,U]`:
   - strict branch: Bernstein subdivision is a fast path;
   - touching branch: T-P5-266 is complete;
   - specialized branch: check endpoints plus the at-most-two roots of the quadratic derivative and use Lemma E for critical values;
6. if the fiber crosses the clamp anchor, repeat independently with `sigma=-1` and `sigma=+1`;
7. never reuse a right-side cubic lower coefficient on the left without the transformed derivative inequality;
8. failure of this outer lower-support certificate remains `CERTIFICATE_NOT_FOUND` unless a real same-key unsafe state is reconstructed.

No square root, cubic radical, sextic polynomial, pseudoinverse, eigenvector, or generic bivariate CAD is required in this lane.

---

## 14. Semantic and fail-closed boundaries

This child does **not** justify:

- using `a`, `d`, `c`, `R`, `mu`, `U` from different source keys;
- evaluating derivatives at a floating selected root and treating the result as exact;
- assuming the fiber is one-sided without a certified clamp/orientation witness;
- transporting `c_+` to the left fiber or `c_-` to the right fiber;
- replacing an FD/Float64 error by an exact-real `C^3` perturbation without enclosure;
- differentiating a merely interval-enclosed evaluator unless a valid derivative enclosure exists;
- treating failure of the outer derivative lower bound as a physical counterexample;
- inferring whole-cell, trajectory, FD-halo, reference-halo, or flowpipe coverage;
- changing registry/admission or closing P5/P8/M4 parents.

The exactness theorem is exact **relative to the abstract one-sided derivative model**, not a statement that the deployed source attains the extremal cubic.

---

## 15. Remaining obligations

Still open:

1. find an actual P5 same-key perturbation where `a,d` and a directional third-derivative lower bound can be extracted without unsafe floating selected-root substitution;
2. bind the orientation `sigma` and one-sided width `U` to the actual moved fiber;
3. determine whether the actual fiber crosses the clamp anchor and therefore needs both directional branches;
4. prove the derivative lower polynomial on the same collar/source key;
5. prove the cubic reserve polynomial on that same domain;
6. reconstruct an actual state witness before promoting outer-certificate failure to physical FAIL;
7. whole-cell/trajectory/FD/reference-halo coverage;
8. Float64/libm/interval semantics;
9. Lean/kernel formalization of the oriented Taylor remainder and cubic identity;
10. independent validation by 封不觉;
11. admission, registry mutation, and parent propagation.

---

## 16. Next nonduplicative mathematical seam

The abstract cubic lane is now sufficiently closed that another higher-degree graph abstraction has low value without source evidence.

The highest-value next mathematical seam is therefore **actual-source instantiation**:

- search one deployed P5 coefficient/FD perturbation for a certified one-sided clamp fiber;
- extract exact/enclosed `a=e'(y)`, `d=e''(y)`, and the best rational directional lower bound `sigma e'''>=6c` on the same collar;
- compare three packets on the same key: T-P5-277 secant, T-P5-278 symmetric quadratic graph, and the present directional cubic support;
- record which one closes the reserve and the exact obstruction for the others.

Only if a real source still fails after this comparison should the mathematical frontier move to a fourth-order signed graph or a general higher-degree half-tube.