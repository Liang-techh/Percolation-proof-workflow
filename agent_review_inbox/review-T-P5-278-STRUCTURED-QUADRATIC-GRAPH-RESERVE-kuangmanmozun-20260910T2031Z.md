---
kind: review_result
review_id: review-T-P5-278-structured-quadratic-graph-reserve-kuangmanmozun-20260910T2031Z
task_id: T-P5-278-STRUCTURED-QUADRATIC-GRAPH-RESERVE
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T20:31:00Z
claim_commit: eb3d348fc07b235eeef504bb5e45861ef7154a42
inspected_commit: 1a6f2fb0616fd3d695673dbae48d4e0f7f789a94
upstream_commits:
  - 1a6f2fb0616fd3d695673dbae48d4e0f7f789a94 # T-P5-277 strong-convexity reserve perturbation
  - d062e528bc248cd24f09973dcde7cfcf7c00ffae # T-P5-266 zero-margin univariate Sturm certificate
  - 7409c5142691c1e3c220e7c5cf5d2864a1a26966 # T-P5-274 cubic inner-fiber reserve
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_secondDerivativeSq_to_quadraticGraphTube; add_quadraticGraphTube_robust_iff_polynomialPair; add_global_fractionFree_graphTube_gate; add_zeroMargin_global_graphTube_gate; add_secant_false_negative_regressions; route_bounded_quartic_to_T-P5-266
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact real-algebra derivation; fraction-free square identities; rational counterexample regressions; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
source_hashes: source_independent_mathematical_child
---

# T-P5-278 — Structured quadratic-graph reserve without direction-forgetting secant debit

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-277 gives a sharp reserve theorem for the abstraction

`(e(t)-e(y))^2 <= D (t-y)^2`.

That abstraction deliberately forgets both:

1. the **sign** of the first-order perturbation relative to the active side of the fiber; and
2. any **known quadratic curvature** in the perturbation.

This child closes the smallest structured lane below a generic polynomial root solver.

Write

`s = t-y`

and retain a signed quadratic model

`e(y+s)-e(y) = a s + b s^2 + w(s)`.

Assume only that the unresolved remainder lies in the second-order graph tube

**(Tube)** `4 w(s)^2 <= K s^4`, `K>=0`.

If the nominal target has the strong-convexity support

`p(y+s) >= p(y) + (mu/2) s^2`

and the anchored reserve satisfies

`p(y)+e(y)-eta >= R`,

define

**(m)** `m := mu + 2 b`

and the doubled structured support

**(H)** `H(s) := 2R + 2 a s + m s^2`.

Then the robust tube question is exact:

> for every admissible `w` satisfying (Tube), is `H(s)+2w >= 0`?

For any fixed bounded fiber `I`, the answer is equivalent to just two univariate polynomial inequalities:

**(P1)** `H(s) >= 0` on `I`,

**(P2)** `H(s)^2 - K s^4 >= 0` on `I`.

Thus the structured perturbation problem becomes **one quadratic plus one quartic**. With rational coefficients and a rational closed interval, T-P5-266 gives a complete exact zero-margin decision procedure; T-P5-265 remains the strict-margin Bernstein fast path.

For the full real line there is an even smaller closed form. If `R>0`, set

**(A)** `A := 2 R m - a^2`.

Then the tube is robustly safe on all `s in R` if and only if

**(G1)** `A >= 0`,

**(G2)** `A^2 >= 4 R^2 K`.

No square root appears in the checker packet. This condition is **necessary and sufficient relative to the graph-tube abstraction**, not merely a sufficient Young inequality.

The zero-margin branch is also exact: if `R=0`, global robust safety holds iff

`a=0`, `m>=0`, and `m^2>=K`.

The gain over T-P5-277 can be strict even when `D` is the **best possible secant-cone constant** on the same interval. A rational regression below has exact safety margin `1/2` while the optimal scalar secant gate fails by more than a factor of two.

No actual P5 coefficient packet, FD evaluator, source key, moved endpoint, collar, whole-cell/trajectory/halo coverage, Float64/libm enclosure, Lean/kernel proof, independent validation, admission, registry mutation, or P5/P8/M4 propagation is claimed.

---

## 1. Same-key setup

Fix one source key / chart / active fiber context. Let `y` be the selected nominal anchor, for example the clamp point supplied by T-P5-277.

Assume on a certified interval in the coordinate `s=t-y`:

**(N1)** `p(y+s) >= p(y) + (mu/2) s^2`, with `mu>0`;

**(N2)** `p(y)+e(y)-eta >= R`;

and decompose the perturbation as

**(E)**

`e(y+s)-e(y) = a s + b s^2 + w(s)`.

The scalar coefficients `a,b` are **signed**. They are not replaced by absolute values.

Define

`m = mu + 2b`.

Then

`2[p(y+s)+e(y+s)-eta]`

is bounded below by

**(1.1)**

`H(s)+2w(s)`

with

`H(s)=2R+2as+ms^2`.

The remainder model is

**(1.2)** `4w(s)^2 <= K s^4`.

This tube is centered on the retained signed graph `as+bs^2`; it is therefore strictly more informative than a cone centered on zero whenever `a` or `b` is useful.

---

## 2. Lemma A — a second-derivative square bound produces the quadratic graph tube

The tube (1.2) has a natural producer-side origin.

Let

`q(s) := e(y+s)-e(y)-a s-b s^2`

with

`a=e'(y)`.

Then

`q(0)=0`, `q'(0)=0`,

and

`q''(s)=e''(y+s)-2b`.

Assume on every segment from `0` to `s` under consideration that

**(2.1)** `(e''(y+r)-2b)^2 <= K`.

Then

**(2.2)** `4q(s)^2 <= K s^4`.

### Proof

By the twice-integrated fundamental theorem of calculus,

`q(s)=integral_0^s (s-r) q''(r) dr`.

Condition (2.1) implies

`|q''(r)| <= sqrt(K)`.

Hence

`|q(s)| <= sqrt(K) * |s|^2 / 2`.

Squaring gives (2.2):

`4q(s)^2 <= K s^4`.

The **serialized conclusion is fraction-free**. A checker never needs to store `sqrt(K)`.

### Why this producer is useful

A global secant cone would first bound all of

`a + b s + q(s)/s`

in magnitude and then square the result. Lemma A instead preserves `a` and `b` exactly and spends uncertainty only on the second-order residual `q`.

---

## 3. Theorem B — exact robust elimination of the graph-tube variable

Let `I` be any set of real `s`, let `K>=0`, and define

`H(s)=2R+2as+ms^2`.

Then the following are equivalent:

### (B1) Robust graph-tube safety

For every `s in I` and every real `w`,

`4w^2 <= K s^4`

implies

**(3.1)** `H(s)+2w >= 0`.

### (B2) Polynomial pair

For every `s in I`,

**(3.2)** `H(s)>=0`,

and

**(3.3)** `H(s)^2-Ks^4>=0`.

### Proof: (B2) -> (B1), no square roots needed

Fix an admissible `s,w`.

Suppose for contradiction that

`H+2w<0`.

Because `H>=0`, this forces

`2w < -H <= 0`,

hence

`4w^2 > H^2`.

But the tube gives

`4w^2 <= K s^4 <= H^2`,

a contradiction.

Thus `H+2w>=0`.

### Proof: (B1) -> (B2)

First take `w=0`, which is always admissible. Then `H>=0`.

For fixed `s`, let

`r=sqrt(K) s^2 >=0`

and choose

`2w=-r`.

This saturates the tube. Robust safety gives

`H-r>=0`.

Therefore

`H>=0`

and

`H^2>=r^2=K s^4`.

So (B2) follows.

### Important semantic point

This is **lossless for the uncertainty set defined by the tube**. If the actual producer supplies one fixed `w(s)` and the tube is only an outer bound, failure of (3.2)-(3.3) means only that the tube abstraction is too large; it is not a physical counterexample to the actual target.

---

## 4. Corollary C — bounded rational fibers reduce to quadratic + quartic sign closure

Assume

`I=[L,U]`, `L,U in Q`, `L<=U`,

and all of

`R,a,m,K`

are rational with `K>=0`.

Then robust tube safety on `I` is exactly the conjunction

`H(s)>=0`

and

`Q4(s):=H(s)^2-Ks^4>=0`

for all `s in [L,U]`.

The degrees are

`deg H <=2`,

`deg Q4 <=4`.

Therefore:

1. strict-margin cells can use Bernstein subdivision;
2. zero-margin/touching cells can use T-P5-266 multiplicity parity + Sturm counting;
3. no new multivariate CAD, SOS search, secular equation, or floating minimizer is required.

For algebraic moving endpoints, the same polynomial pair can be handed to the selected-root endpoint machinery of T-P5-270/T-P5-276. This child does not duplicate that endpoint atlas.

---

## 5. Theorem D — global fraction-free necessary-and-sufficient gate for positive reserve

Assume

`R>0`, `K>=0`.

Define

`A := 2 R m - a^2`.

Then the following are equivalent:

### (D1)

For every real `s` and every real `w` satisfying

`4w^2<=K s^4`, one has

`H(s)+2w>=0`.

### (D2)

**(5.1)** `A>=0`,

**(5.2)** `A^2>=4R^2K`.

### Proof

By Theorem B, (D1) is equivalent to

`H(s)>=sqrt(K)s^2`

for every real `s`.

Equivalently the quadratic

**(5.3)**

`2R+2as+(m-sqrt(K))s^2`

is globally nonnegative.

Since `R>0`, global nonnegativity of (5.3) is equivalent to

`m-sqrt(K)>=0`

and nonpositive discriminant:

`4a^2 - 8R(m-sqrt(K)) <=0`.

That is

**(5.4)**

`2Rm-a^2 >= 2R sqrt(K)`.

The left side is `A`. Because the right side is nonnegative, (5.4) is equivalent to

`A>=0`

and

`A^2>=4R^2K`.

This proves the fraction-free gate.

### Equivalent sharp reserve interpretation

When `m>sqrt(K)`, (5.4) is

**(5.5)**

`R >= a^2 / [2(m-sqrt(K))]`.

Thus:

- the retained signed quadratic coefficient `b` changes usable curvature from `mu` to `m=mu+2b`;
- the unresolved second-order graph tube consumes curvature only through `sqrt(K)`;
- the signed linear coefficient `a` then consumes reserve through the exact quadratic discriminant.

The checker should use (5.1)-(5.2), not (5.5), so no square root or division is serialized.

---

## 6. Theorem E — exact zero-margin global branch

Assume

`R=0`, `K>=0`.

Then global robust tube safety holds iff

**(6.1)** `a=0`,

**(6.2)** `m>=0`,

**(6.3)** `m^2>=K`.

### Proof

At zero reserve,

`H(s)=2as+ms^2`.

If `a!=0`, the linear term has opposite sign on one of the two sides of zero and dominates for sufficiently small `|s|`, so safety fails.

Thus `a=0`. The worst tube direction gives

`[m-sqrt(K)]s^2`.

This is nonnegative for all real `s` iff

`m>=sqrt(K)`,

which is exactly `m>=0` and `m^2>=K`.

This branch matters at touching certificates: using only the positive-reserve theorem would unnecessarily discard valid zero-margin cases.

---

## 7. Strict gain over the optimal scalar secant cone

Take the rational data

`mu=2`, `R=1`, `I=[-1,1]`,

and an **exact** perturbation

`e(y+s)-e(y)=2s+s^2`.

Thus

`a=2`, `b=1`, `K=0`,

so

`m=mu+2b=4`.

The structured support is

`H(s)=2+4s+4s^2`.

Equivalently the undoubled lower bound is

`1+2s+2s^2`.

Its exact minimum is at `s=-1/2` and equals

**`1/2`**.

So the target is safely positive on the whole interval, indeed on all of `R`.

The new global gate gives

`A=2*1*4-2^2=4`,

hence

`A>=0`, `A^2>=0`.

PASS.

Now compute the **best possible** T-P5-277 secant-cone constant on the same interval. For `s!=0`,

`(e(y+s)-e(y))^2/s^2=(2+s)^2`.

On `[-1,1]` its exact maximum is

**`D_opt=9`**.

T-P5-277's no-bonus gate requires

`D_opt <= 2 mu R = 4`.

It fails:

`9>4`.

Therefore the gain is not an artifact of using a loose derivative bound. Even the **optimal direction-forgetting secant cone** rejects a case where the signed quadratic graph packet proves an exact positive margin.

The reason is structural: the positive `+s^2` perturbation simultaneously enlarges secant magnitude and **improves curvature**. A scalar `D` sees only the first effect.

---

## 8. One-sided fibers can gain even more from sign information

Take

`mu=2`, `R=1`, `I=[0,1]`,

and

`e(y+s)-e(y)=10s`.

Then

`a=10`, `b=0`, `K=0`, `m=2`.

The actual undoubled lower support is

`1+s^2+10s >= 1`

on the one-sided fiber.

So bounded-fiber structured closure is immediate.

But the optimal secant constant is

`D=100`,

while T-P5-277 asks for

`D<=2muR=4`.

This is another exact false negative of the symmetric secant abstraction.

It also explains why the bounded polynomial-pair theorem should remain a first-class route even though the full-line closed form is available: the full-line problem deliberately includes the dangerous opposite side `s<0`, while a clamp-selected boundary fiber may not.

---

## 9. Counterexample — the sign guard `H>=0` cannot be dropped after squaring

A checker must not use only

`H^2-Ks^4>=0`.

Take

`R=1`, `a=-2`, `m=0`, `K=0`, `I=[0,1]`.

Then

`H(s)=2-4s`.

The squared inequality is trivially true because

`H(s)^2>=0`.

But at `s=1`,

`H(1)=-2`.

With admissible `w=0`, robust safety fails.

Thus the pair

`H>=0`

and

`H^2-Ks^4>=0`

is logically essential. Squaring without the sign guard is an unsound PASS rule.

---

## 10. Counterexample — `H>=0` alone does not control the graph tube

Take a single point `s=1` with

`R=1/2`, `a=0`, `m=0`, `K=4`.

Then

`H(1)=1>=0`.

But the tube allows

`w=-1`,

because

`4w^2=4=K s^4`.

Then

`H+2w=1-2=-1<0`.

Correspondingly

`H^2-Ks^4=1-4=-3<0`.

So the quartic condition is a real reserve obligation, not bookkeeping.

---

## 11. Counterexample — the sign gate `A>=0` cannot be deleted from the global square test

For the positive-reserve global theorem take

`R=1`, `a=2`, `m=0`, `K=1`.

Then

`A=2Rm-a^2=-4`.

The squared inequality alone says

`A^2=16 >= 4R^2K=4`.

Yet the robust lower quadratic in the worst tube direction is

`2+4s-s^2`,

which tends to `-infinity` as `|s|` grows.

Therefore the global checker must enforce both

`A>=0`

and

`A^2>=4R^2K`.

This is the exact analogue of the sign guard in T-P5-274/T-P5-266 square-elimination steps.

---

## 12. Sharpness relative to the tube abstraction

Theorem D is not a Young-inequality relaxation.

Let

`r=sqrt(K)`.

The worst admissible remainder at each fixed `s` is exactly

`2w=-r s^2`.

Hence the robust problem is literally the global nonnegativity of

`2R+2as+(m-r)s^2`.

If the gate fails strictly, that quadratic is negative at some real `s`.

Choosing the saturating remainder gives a genuine graph-tube counterexample.

If the negative value is strict and the coefficients are rational, continuity and density imply a rational `s` arbitrarily nearby with the same strict sign. Even when `sqrt(K)` is irrational, one may choose a rational `w` inside the nonempty interval between the unsafe threshold and the tube boundary. Thus strict mathematical FAIL of the tube packet admits rational witnesses after isolation.

At equality, the packet correctly permits touching: the worst-case quadratic has a double root.

---

## 13. Formalizable theorem statements

Suggested theorem leaves follow. Names are indicative only.

### 13.1 `secondDerivSqBound_implies_quadraticGraphTube`

Inputs:

- interval/collar `J`;
- `e : R -> R`, twice differentiable on the relevant segment;
- anchor `y`;
- rationals/reals `a,b,K` with `a=e' y`, `K>=0`;
- `(e'' x-2*b)^2<=K` on the segment.

Conclusion:

`4*(e(y+s)-e(y)-a*s-b*s^2)^2 <= K*s^4`.

### 13.2 `quadraticGraphTube_robust_iff_polynomialPair`

For `K>=0`, with

`H s = 2*R+2*a*s+m*s^2`,

prove

`(forall s in I, forall w, 4*w^2<=K*s^4 -> 0<=H s+2*w)`

iff

`(forall s in I, 0<=H s and K*s^4<=(H s)^2)`.

### 13.3 `quadraticGraphTube_global_posReserve_fractionFree`

Assume `R>0`, `K>=0`, define

`A=2*R*m-a^2`.

Then global robust safety iff

`0<=A`

and

`4*R^2*K<=A^2`.

### 13.4 `quadraticGraphTube_global_zeroReserve_fractionFree`

Assume `R=0`, `K>=0`.

Then global robust safety iff

`a=0 and 0<=m and K<=m^2`.

### 13.5 `structuredGraph_strictly_beats_optimalSecant`

Hard-code the rational regression

`mu=2`, `R=1`, `e(s)=2s+s^2`, `I=[-1,1]`.

Prove:

- the structured lower support is at least `1/2`;
- every secant constant must satisfy `D>=9`;
- T-P5-277's no-bonus gate would require `D<=4`.

This theorem is useful as a permanent regression preventing later refactors from collapsing the graph packet back to a scalar slope budget.

---

## 14. Checker routing

A source-side consumer can use the following exact route.

1. Obtain same-key `mu,R,y` from the nominal strong-convexity packet.
2. Retain signed `a,b` from the same perturbation model; do not absolute-value them.
3. Certify `K>=0` and either:
   - directly provide `4w^2<=Ks^4`, or
   - prove `(e''-2b)^2<=K` on the same collar and invoke Lemma A.
4. Set `m=mu+2b`.
5. For bounded rational fiber `I=[L,U]`, build
   - `H=2R+2as+ms^2`,
   - `Q4=H^2-Ks^4`,
   and prove both nonnegative on `I`.
6. Use Bernstein only as a strict-margin fast path; if a polynomial touches zero, use T-P5-266 Sturm/multiplicity closure rather than reporting failure.
7. If the physical consumer genuinely needs all real `s`, replace step 5 by the two scalar gates
   - `A=2Rm-a^2>=0`,
   - `A^2>=4R^2K`,
   with the separate `R=0` branch.
8. Failure of the graph-tube packet is not automatically physical FAIL unless the producer has declared the tube itself exact/adversarial. For an outer tube, it is `CERTIFICATE_NOT_FOUND` unless an actual same-key witness is reconstructed.

---

## 15. Interaction with T-P5-277

This child does not supersede the secant theorem.

The secant lane remains preferable when:

- only a first-derivative magnitude bound is available;
- the perturbation has no reliable signed model;
- the graph-tube quartic is more expensive than the available reserve requires.

The structured lane is preferable when:

- `a` has a favorable one-sided sign;
- `b>0` contributes real curvature;
- the residual is genuinely second order;
- the secant cone fails because it charges positive curvature as if it were dangerous slope.

Thus the correct consumer is a **two-route closure** rather than replacing one abstraction with the other.

---

## 16. Semantic boundaries

This child proves an abstract mathematical transport theorem only.

It does **not** justify:

- taking `a,b,K` from a different source key than `mu,R,y`;
- using a pointwise second-derivative bound outside the actual perturbed collar;
- treating an FD or Float64 error as an exact-real `e` without enclosure;
- inferring moved-bracket inclusion from coefficient closeness;
- inferring whole-cell, trajectory, FD-halo, or reference-halo coverage;
- calling graph-tube failure a physical counterexample when the tube is merely an outer approximation;
- changing admission, registry state, or any P5/P8/M4 parent.

In particular, the strict-gain regression proves only that a scalar secant abstraction can be conservative. It does not show that the actual deployed P5 packet has the needed signed `a,b,K` data.

---

## 17. Remaining obligations

Still open:

1. identify an actual P5 same-key perturbation where `a,b` can be extracted without floating selected-root substitution;
2. certify a same-collar `K` from the actual coefficient / FD / evaluator error;
3. bind `R` and `mu` to the same source key and moved fiber;
4. determine whether the bounded interval is one-sided around the clamp anchor and preserve that orientation;
5. route the resulting quadratic/quartic pair through the exact nonnegativity machinery;
6. reconstruct an actual state/trajectory witness before promoting any failed outer-tube gate to physical FAIL;
7. whole-cell/flowpipe/FD-halo/reference-halo coverage;
8. Float64/libm/interval enclosure;
9. Lean/kernel formalization;
10. independent validation by 封不觉;
11. admission, registry mutation, and P5/P8/M4 propagation.

---

## 18. Next nonduplicative mathematical seam

The next abstract extension should not be another generic root solver.

Two disjoint continuations are now meaningful:

1. **actual-source instantiation** — extract `a,b,K` from a real P5 coefficient/FD packet and test whether this quadratic-graph route succeeds where the T-P5-277 scalar gate fails;
2. **signed cubic remainder lane** — only if an actual packet still fails the quadratic tube, retain a one-sided cubic term `c s^3` before outer-bounding the remainder. On a one-sided clamp fiber, odd-sign information may reduce the resulting closure below the naive sextic `H^2-Ks^6` packet.

Unless a deployed source demonstrates the need for the second lane, source binding now has higher value than further abstract generalization.
