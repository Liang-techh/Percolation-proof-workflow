---
kind: review_result
review_id: review-T-P5-274-cubic-inner-fiber-sharp-reserve-kuangmanmozun-20260910T1933Z
task_id: T-P5-274-CUBIC-INNER-FIBER-SHARP-RESERVE
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T19:33:00Z
claim_commit: bd57b88eac762ce1321365cc32fcd0910559184d
inspected_commit: c1140d3ca48a9976f161c19b42b1e6201b6f6524
upstream_commits:
  - 2452690d4c89057795bd9c3b27b6974cc304ccac # T-P5-273 nested semialgebraic fiber elimination
  - 2a5617c335f912dda8ff720a9354e0f5b548740a # T-P5-272 finite Boolean one-fiber arrangement
  - 28be4ab630470caae390cfef4b534a0c96091076 # T-P5-271 multicomponent semialgebraic fiber decomposition
  - 796fdbafb703dd97bb6841632091174aac469e68 # T-P5-270 algebraic moving-fiber Thom closure
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_cubic_interval_nonneg_dispatch; add_fraction_free_local_min_location_gate; add_cubic_sharp_reserve_comparator; add_cubic_discriminant_contact_classifier; preserve_quadratic_fallback_and_source_binding_boundary
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact symbolic derivation and rational counterexample checks; randomized numerical sanity check of dispatcher; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-274 — Cubic inner-fiber sharp reserve

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-273 proved that a nested triangular/graph-like source with an inner **quadratic** slack can eliminate the inner variable exactly and return a finite Boolean polynomial-sign formula to the T-P5-272 outer arrangement. The next nonquadratic case does not yet require general CAD either.

For an inner slack of degree three,

`p(t) = A t^3 + B t^2 + C t + D`,

there is at most one local minimum. This review proves a complete exact interval lower-bound dispatcher. The only non-endpoint candidate is that local minimum, and both

1. whether it lies inside a rational moving interval, and
2. whether its value is at least a requested rational reserve `eta`,

reduce to finite **polynomial sign tests over Q**. No radicals need be evaluated, no numerical root finder is needed, and no bivariate optimizer appears.

The strongest useful corollary is a sharp reserve gate: once the local minimum lies in the fiber, the exact comparison `min p >= eta` is equivalent to

`R_eta >= 0` and `R_eta^2 >= 4 Delta^3`,

where

`Delta = B^2 - 3 A C`,

`R_eta = 2 B^3 - 9 A B C + 27 A^2 (D-eta)`.

Equivalently, using the cubic discriminant,

`R_eta >= 0` and `Disc(p-eta) <= 0`.

Thus the quadratic nested-fiber chain extends one full degree without abandoning exact fraction-free closure.

No actual P5 cubic target, source key, endpoint representation, state realization, trajectory/FD/reference-halo coverage, Float64/libm semantics, Lean/kernel proof, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Let

`p(t) = A t^3 + B t^2 + C t + D`

with real coefficients and first treat the genuinely cubic branch

`A != 0`.

Let the nondegenerate inner source fiber be the closed interval

`[ell, r]`, `ell < r`.

For reserve checking define

`p_eta(t) := p(t) - eta`.

The derivative is independent of `eta`:

`p'(t) = 3 A t^2 + 2 B t + C`.

Define the two standard cubic invariants

`Delta := B^2 - 3 A C`,

`R := 2 B^3 - 9 A B C + 27 A^2 D`,

and for the shifted polynomial

`R_eta := R - 27 A^2 eta`

`       = 2 B^3 - 9 A B C + 27 A^2 (D-eta)`.

The derivative discriminant is `4 Delta`.

---

## 2. Critical-point geometry

### Lemma 2.1 — `Delta <= 0` is monotone

If `Delta < 0`, the quadratic derivative has no real root. Since its leading coefficient is `3A`,

- `A>0` implies `p'(t)>0` for every `t`;
- `A<0` implies `p'(t)<0` for every `t`.

If `Delta=0`,

`p'(t) = 3 A (t + B/(3A))^2`,

so the derivative again has the sign of `A`, except at one double zero.

Therefore for **all `Delta<=0`**, `p` is monotone and its minimum on any compact interval is an endpoint.

### Lemma 2.2 — `Delta>0` has exactly one local minimum

Let `s=sqrt(Delta)>0`. The two stationary points are

`t_plus  = (-B+s)/(3A)`,

`t_minus = (-B-s)/(3A)`.

A direct substitution into the second derivative gives

`p''(t_plus)=2s>0`,

`p''(t_minus)=-2s<0`.

Hence

`tau := (-B+sqrt(Delta))/(3A)`

is the **unique local minimum**, regardless of the sign of `A`. The other stationary point is a local maximum and can never be a new minimum of `p` on an interval once the endpoints are included.

Consequently, for `Delta>0`, the minimum of `p` on `[ell,r]` is attained among

`{p(ell), p(r)}`

plus `p(tau)` only when `tau in (ell,r)`.

This observation is the whole reason the cubic case remains one-dimensional and finite.

---

## 3. Exact stationary value without evaluating the radical

### Lemma 3.1 — local-minimum value identity

For `Delta>0` and `tau=(-B+sqrt(Delta))/(3A)`,

**(3.1)**

`27 A^2 p(tau) = R - 2 Delta^(3/2)`.

More generally,

**(3.2)**

`27 A^2 p_eta(tau) = R_eta - 2 Delta^(3/2)`.

Because `27A^2>0`,

`p(tau)>=eta`

if and only if

`R_eta >= 2 Delta^(3/2)`.

Since the right-hand side is nonnegative, this is equivalent to the fully radical-free pair

**(3.3)**

`R_eta >= 0`,

`R_eta^2 >= 4 Delta^3`.

### Proof

Set `s=sqrt(Delta)`, so `s^2=Delta`. Substitute

`tau=(-B+s)/(3A)`

into `27A^2 p_eta(tau)`. Straight expansion gives

`R_eta + s(6AC-2B^2)`.

But

`6AC-2B^2 = -2(B^2-3AC) = -2Delta`,

hence the expression is

`R_eta - 2 Delta s = R_eta - 2 Delta^(3/2)`.

Squaring is lossless only after retaining `R_eta>=0`, giving (3.3). QED.

---

## 4. Discriminant form of the same gate

Let `Disc(p_eta)` denote the ordinary cubic discriminant of `p_eta`:

`Disc(p_eta)`

`= 18 A B C (D-eta)`

`  - 4 B^3 (D-eta)`

`  + B^2 C^2`

`  - 4 A C^3`

`  - 27 A^2 (D-eta)^2`.

The exact invariant identity is

**(4.1)**

`R_eta^2 - 4 Delta^3 = -27 A^2 Disc(p_eta)`.

Therefore on the interior-minimum branch `Delta>0`,

**(4.2)**

`p(tau)>=eta`

iff

`R_eta>=0` and `Disc(p_eta)<=0`.

This version is useful if an algebraic checker already has a cubic discriminant primitive; the `R_eta^2-4Delta^3` version is usually simpler for a fraction-free arithmetic kernel.

### Zero-margin contact

If `tau` is strictly interior, then exact contact

`p(tau)=eta`

is equivalent to

`R_eta>0` and `R_eta^2=4Delta^3`,

or equivalently

`R_eta>0` and `Disc(p_eta)=0`.

Thus a double root of `p_eta` at the local minimum is classified exactly rather than treated as a numerical near-zero event.

---

## 5. Fraction-free test that the local minimum is inside a rational moving interval

Now let the endpoints be rational functions of outer variables:

`ell = Nl/Dl`,

`r   = Nr/Dr`,

on a regular outer cell with

`Dl>0`, `Dr>0`, `ell<r`.

Define

`YL := 3 A Nl + B Dl`,

`YR := 3 A Nr + B Dr`.

Then

`YL/Dl = 3A ell + B`,

`YR/Dr = 3A r + B`,

while the local minimum satisfies

**(5.1)**

`3 A tau + B = sqrt(Delta)`.

For `Delta>0`, define the two fraction-free comparison atoms

`Below(X,Q) := (X<=0) or (X^2 < Delta Q^2)`,

`Above(X,Q) := (X>0) and (Delta Q^2 < X^2)`.

Because `Q>0` and `sqrt(Delta)>0`, these are exactly

`Below(X,Q)  <-> X/Q < sqrt(Delta)`,

`Above(X,Q)  <-> sqrt(Delta) < X/Q`.

Therefore the strict interior predicate is

**(5.2)**

`InsideMin :=`

`  (A>0 and Below(YL,Dl) and Above(YR,Dr))`

`  or`

`  (A<0 and Below(YR,Dr) and Above(YL,Dl))`.

No square root occurs in (5.2). Every atom is a polynomial sign test.

### Why the orientation flips when `A<0`

The map

`t -> 3At+B`

is increasing for `A>0` and decreasing for `A<0`. Equation (5.1) therefore places `sqrt(Delta)` between the transformed endpoint values in opposite orders. This sign reversal is essential; treating the `A<0` branch as if `A>0` selects the wrong stationary point/domain relation.

### Boundary contact

If `tau=ell` or `tau=r`, one strict comparison in (5.2) becomes equality, so `InsideMin=false`. That is intentional: endpoint reserve checks already include the contact exactly. There is no need to count the same minimizer twice.

---

## 6. Fraction-free endpoint reserve

For a rational reserve `eta`, define

`EL_eta := A Nl^3`

`          + B Nl^2 Dl`

`          + C Nl Dl^2`

`          + (D-eta) Dl^3`,

`ER_eta := A Nr^3`

`          + B Nr^2 Dr`

`          + C Nr Dr^2`

`          + (D-eta) Dr^3`.

Since `Dl,Dr>0`,

`EL_eta >=0 <-> p(ell)>=eta`,

`ER_eta >=0 <-> p(r)>=eta`.

Again these are polynomial sign tests after any certified positive outer denominator has been cleared.

---

## 7. Main theorem — exact cubic interval lower-bound dispatcher

### Theorem A

Assume

- `A != 0`;
- `Dl>0`, `Dr>0`;
- `ell=Nl/Dl < r=Nr/Dr`.

Let `Delta`, `R_eta`, `EL_eta`, `ER_eta`, and `InsideMin` be defined as above.

Then

**(7.1)**

`p(t)>=eta for every t in [ell,r]`

if and only if

**(7.2)**

`EL_eta>=0`

and

`ER_eta>=0`

and

`(`

`  Delta<=0`

`  or not InsideMin`

`  or (R_eta>=0 and R_eta^2>=4 Delta^3)`

`)`.

### Proof

If `Delta<=0`, Lemma 2.1 makes `p` monotone, so the minimum is an endpoint.

If `Delta>0`, Lemma 2.2 shows the only possible non-endpoint minimum is `tau`. Formula (5.2) decides exactly whether `tau` is strictly inside the interval.

- If `InsideMin=false`, the minimum is again an endpoint.
- If `InsideMin=true`, endpoint nonnegativity is necessary but not sufficient; one must additionally check `p(tau)>=eta`, which by Lemma 3.1 is exactly the two polynomial inequalities in (7.2).

No other critical point can lower the interval minimum because the second stationary point is a local maximum. QED.

---

## 8. Sharp reserve corollary

Define the exact interval reserve

`eta_star := inf_{t in [ell,r]} p(t)`.

Because `p` is continuous on a compact interval, this infimum is a minimum.

### Case 1 — no interior local minimum

If

`Delta<=0`

or

`InsideMin=false`,

then

**(8.1)**

`eta_star = min(p(ell), p(r))`.

For rational coefficients and rational endpoints this is rational.

### Case 2 — interior local minimum

If `Delta>0` and `InsideMin=true`, then

**(8.2)**

`eta_star = p(tau)`

`         = (R - 2 Delta sqrt(Delta))/(27 A^2)`.

This is an algebraic number of degree at most two over the coefficient field.

A checker never needs to evaluate it numerically. For any rational candidate reserve `eta`, Theorem A decides

`eta <= eta_star`

by the polynomial gate

`R_eta>=0`,

`R_eta^2>=4Delta^3`.

Thus a rational lower reserve can be certified exactly even when the sharp reserve itself is irrational.

---

## 9. Moving-fiber quantifier elimination consequence

Suppose the outer variables are collectively `x` (for example `x=(q,s)` in T-P5-273), and

`A(x),B(x),C(x),D(x),Nl(x),Dl(x),Nr(x),Dr(x)`

are rational polynomials on a regular outer cell with certified denominator orientation.

Then every atom in Theorem A is a polynomial sign condition in `x`:

- `A>0`, `A<0`;
- `Delta<=0`, `Delta>0`;
- `YL<=0`, `YL^2 < Delta Dl^2`;
- `YR>0`, `Delta Dr^2 < YR^2`;
- `EL_eta>=0`, `ER_eta>=0`;
- `R_eta>=0`;
- `R_eta^2-4Delta^3>=0`.

Therefore the quantified statement

`forall t in [ell(x),r(x)], p(x,t)>=eta`

is equivalent on that regular cell to a finite Boolean formula over polynomial signs in `x`.

This is exactly the output type expected by the T-P5-272 one-fiber arrangement. Hence the nested chain can now consume a **cubic** inner Lyapunov slack without escalating to general two-variable CAD.

---

## 10. Degenerate degree and interval branches

The dispatcher must be fail-closed about degree drops.

### 10.1 `A=0`

Do **not** divide by `A` or instantiate the cubic formulas. Route to the exact quadratic/affine dispatcher from T-P5-273.

### 10.2 `ell=r`

Under weak/weak closed semantics the fiber is a singleton, so check only `p(ell)>=eta`.

If either side is strict and the literal source section is empty, the universal target statement is vacuous on that inner section; whether this is acceptable depends on the outer source contract exactly as in T-P5-273.

### 10.3 `ell>r`

Under literal interval semantics the fiber is empty, not a target counterexample. Under a separate source contract that promises a nonempty ordered fiber, this is a source-order obstruction.

### 10.4 open/half-open nondegenerate intervals

For the weak inequality `p>=eta`, continuity means the statement on any nondegenerate open/half-open interval has the same truth value as on its closure. A strictly negative endpoint value would persist into nearby interior points. Hence Theorem A may consume the closed interval after the same continuity lemma used by T-P5-273.

---

## 11. Counterexamples and checker bugs

### Counterexample 11.1 — endpoints alone are not enough for a cubic

Take

`p(t)=t^3-t`, `t in [0,1]`.

Then

`p(0)=p(1)=0`,

but

`Delta=3`,

`tau=1/sqrt(3) in (0,1)`,

and

`p(tau)=-2/(3sqrt(3))<0`.

So an endpoint-only extension of the T-P5-273 concave/quadratic logic gives a false PASS.

Our gate catches the failure because `InsideMin=true`, `R=0`, and

`R^2=0 < 4 Delta^3=108`.

### Counterexample 11.2 — do not apply the global stationary gate when the local minimum is outside the fiber

Take

`p(t)=t^3-3t`, `t in [2,3]`.

The global local minimum is at `tau=1`, where `p(1)=-2`, but `tau` is outside the fiber. On `[2,3]`,

`p'(t)=3(t^2-1)>0`,

so

`p(t)>=p(2)=2>0`.

A checker that tests the global stationary reserve without first testing `InsideMin` would false-REJECT this safe fiber.

Fraction-free location catches it: `Delta=9`, `YL=6`, while `sqrt(Delta)=3`; for `A>0`, the required `YL<sqrt(Delta)` fails.

### Counterexample 11.3 — squaring without the sign condition is invalid

Take

`p(t)=t^3-3t-3`.

Here

`Delta=9`, `R=-81`.

The local minimum at `t=1` equals `-5`, so the stationary reserve is negative. Yet

`R^2=6561 > 4 Delta^3=2916`.

Thus the squared comparison alone would incorrectly accept the local-minimum value. The sign condition `R_eta>=0` is part of the theorem and must not be deleted by a simplifier.

### Counterexample 11.4 — cubic formulas are invalid on the quadratic degree-drop cell

If `A=0`, then `tau=(-B+sqrt(Delta))/(3A)` is meaningless even though the original polynomial may be perfectly regular. Degree-drop cells must dispatch to T-P5-273 rather than being interpreted as cubic singularities of the source.

### Counterexample 11.5 — exact zero-margin contact is not a numerical failure

Take

`p(t)=t^3-3t+3`, `t in [0,2]`.

Then

`Delta=9`, `tau=1`, `p(tau)=1`.

For reserve `eta=1`,

`R_eta=54`,

`R_eta^2=2916=4Delta^3`.

The exact packet therefore certifies `p>=1` with an interior touching point.

For the slightly larger rational reserve `eta=101/100`,

`R_eta=5373/100`,

and

`4Delta^3 - R_eta^2 = 290871/10000 >0`,

so the gate rejects it exactly. This is a useful zero-margin/strict-margin regression pair.

---

## 12. Exact FAIL versus certificate obstruction

Once all source/endpoint bindings are actual and same-key:

- `EL_eta<0` gives an exact rational endpoint counterexample;
- `ER_eta<0` gives an exact rational endpoint counterexample;
- `Delta>0`, `InsideMin=true`, and failure of the stationary gate proves a genuine mathematical failure on the declared interval;
- when `R_eta<0`, the local minimum is strictly below `eta` immediately;
- when `R_eta>=0` but `R_eta^2<4Delta^3`, the local minimum is again strictly below `eta`.

The last two failures identify an algebraic witness `tau`; a physical/source FAIL still requires the normal state-realization and coverage gates before propagation.

By contrast:

- denominator orientation missing;
- outer-cell polynomial arrangement missing;
- actual target not known to be cubic in the inner variable;
- source endpoint representation missing;

are **CERTIFICATE_NOT_FOUND / SOURCE_BINDING_REQUIRED**, not mathematical FAIL.

---

## 13. Suggested theorem decomposition for Lean

A minimal formalization should avoid starting with a huge quantifier-elimination theorem. Suggested leaves:

1. `cubic_deriv_discriminant_nonpos_monotone`
   - assumptions `A != 0`, `Delta<=0`;
   - conclusion monotonicity direction from the sign of `A`.

2. `cubic_stationary_points_and_curvature`
   - under `Delta>0`, define the two roots and prove `p''(tau)=2*sqrt Delta`, the other curvature negative.

3. `cubic_local_min_value_identity`
   - prove
     `27*A^2*(p tau-eta)=R_eta-2*Delta*sqrt Delta`.

4. `cubic_local_min_reserve_iff_fractionFree`
   - under `Delta>0`, prove
     `p tau>=eta <-> R_eta>=0 ∧ R_eta^2>=4*Delta^3`.

5. `rat_lt_sqrt_iff_fractionFree`
   - for `Q>0`, `Delta>0`, prove
     `X/Q < sqrt Delta <-> X<=0 ∨ X^2<Delta*Q^2`.

6. `sqrt_lt_rat_iff_fractionFree`
   - prove
     `sqrt Delta < X/Q <-> X>0 ∧ Delta*Q^2<X^2`.

7. `cubic_local_min_inside_rational_interval_iff`
   - combine the previous two with sign of `A`.

8. `cubic_lower_on_Icc_iff_dispatch`
   - main compact interval theorem.

9. `cubic_discriminant_identity`
   - pure ring theorem
     `R_eta^2-4*Delta^3=-27*A^2*Disc(p_eta)`.

10. `cubic_nested_elimination_formula`
    - logical wrapper returning a finite Boolean sign formula once rational endpoint/source premises are supplied.

11. degree-drop wrapper
    - `A=0` delegates to the T-P5-273 quadratic interval theorem rather than duplicating it.

This decomposition keeps square-root lemmas local. The final checker-facing contract can be entirely fraction-free.

---

## 14. Checker-facing branch order

A deterministic exact checker can use the following order.

1. Validate endpoint denominator orientation and interval semantics.
2. If `A=0`, route to quadratic T-P5-273.
3. Check fraction-free endpoint reserve `EL_eta,ER_eta`.
4. Compute `Delta=B^2-3AC`.
5. If `Delta<=0`, PASS the cubic inner fiber once endpoints pass.
6. If `Delta>0`, compute `InsideMin` using (5.2).
7. If `InsideMin=false`, PASS once endpoints pass.
8. If `InsideMin=true`, compute `R_eta` and require
   `R_eta>=0` and `R_eta^2>=4Delta^3`.
9. Record whether equality occurs at an endpoint or at the interior discriminant contact.

Every operation is addition, multiplication, exact comparison, and Boolean branching over the coefficient field after denominator clearing.

---

## 15. What this child changes

Before this review, the nested exact-elimination chain had a natural stopping point at inner degree two. A cubic target appeared to require selected algebraic critical roots or a more general CAD step.

This review shows that degree three has a special stronger structure:

- only one stationary point can be a local minimum;
- its location inside a rational interval is a fraction-free square comparison;
- its reserve value is a single cubic-discriminant inequality plus one sign bit;
- therefore the eliminated result is still a finite Boolean formula in the outer variables.

So cubic inner fibers belong to the same exact one-dimensional closure architecture as the quadratic chain.

---

## 16. Remaining obligations

Still open:

1. determine whether the actual P5 target/slack is cubic in any chosen inner fiber variable;
2. bind `A,B,C,D,Nl,Dl,Nr,Dr` to one source key/evaluator;
3. prove positive denominator orientation and interval order on each active cell;
4. preserve strict/weak/equality source semantics;
5. construct the outer T-P5-272 common-factor arrangement after substituting this dispatcher;
6. source/domain clipping and point-cell handling;
7. state/trajectory realization of any negative algebraic witness;
8. whole-sheet/flowpipe/FD-halo/reference-halo coverage;
9. Float64/libm/interval semantics where deployed evaluation is floating point;
10. Lean/kernel formalization;
11. independent validation by 封不觉;
12. admission, registry mutation, and P5/P8/M4 propagation.

---

## 17. Next mathematical seam

The next useful step should not be a blind jump to quartic CAD.

Two structurally distinct extensions are now visible:

- **quartic with certified convexity**: if `p''(t)>=0` on the whole inner fiber, the derivative is monotone and there is at most one interior minimizer; one can try to eliminate the cubic stationary equation by a Sturm-Tarski selected-root sign packet while retaining a finite outer formula;
- **cubic algebraic endpoints**: combine this cubic reserve invariant with T-P5-270 selected algebraic endpoint/Thom data, so that local-minimum location is decided against selected algebraic endpoint branches without expanding to a full bivariate CAD.

If the actual P5 source exposes a cubic inner target with rational endpoints, however, no new generic mathematics is needed: instantiate Theorem A immediately and send its finite polynomial-sign formula to T-P5-272.