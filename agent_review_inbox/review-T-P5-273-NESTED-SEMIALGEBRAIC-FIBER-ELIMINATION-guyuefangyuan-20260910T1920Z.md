---
kind: review_result
review_id: review-T-P5-273-nested-semialgebraic-fiber-elimination-guyuefangyuan-20260910T1920Z
task_id: T-P5-273-NESTED-SEMIALGEBRAIC-FIBER-ELIMINATION
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T19:20:00Z
claim_commit: 2dc7a708d29a655b53824802f949ac234e742e10
inspected_commit: 58b13647bef268cb7dbfcc4a1862b82e2f6f1f84
upstream_commits:
  - 2a5617c335f912dda8ff720a9354e0f5b548740a # T-P5-272 finite Boolean one-fiber arrangement
  - 28be4ab630470caae390cfef4b534a0c96091076 # T-P5-271 multicomponent semialgebraic fiber decomposition
  - 796fdbafb703dd97bb6841632091174aac469e68 # T-P5-270 algebraic moving-fiber Thom closure
  - 5334199bdb2c7b093239ffb72ffd4c759294323c # T-P5-269 rational moving quadratic fiber clamp
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_nested_quadratic_quantifier_elimination; add_full_curvature_interval_dispatch; add_fraction_free_concave_chord_identity; add_degenerate_strict_endpoint_semantics; add_outer_violation_boolean_reduction; preserve_rational_endpoint_validity_and_algebraic_selector_boundary
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact ordered-field derivation; symbolic ring expansion of the new chord identity; exact rational counterexamples; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-273 — Nested semialgebraic fiber elimination

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-272 closes finite Boolean geometry when there is one continuous fiber variable. The next source geometry need not jump to general bivariate CAD. A large and useful two-variable class remains exactly reducible: a triangular or graph-like fiber

`(q,s,t)` with outer source predicate `Phi(q,s)` and inner section

`t in [a(q,s), b(q,s)]`,

provided the Lyapunov slack is at most quadratic in `t` and the interval endpoints are rational functions of `(q,s)` on the current source cell.

This review proves an explicit **one-step quantifier elimination theorem** for the inner variable `t`. The universal statement

`forall t in inner_section, p(q,s,t) >= 0`

is equivalent to a finite Boolean formula made only from signs of polynomials in `(q,s)`. Therefore the remaining problem is exactly in the T-P5-272 class: one fiber variable `s`, one parameter `q`, finite Boolean polynomial sign geometry. No two-dimensional optimizer, convex-hull replacement, or general CAD is required.

The child also adds a new full-curvature branch missing from the moving-fiber chain: when the quadratic slack is concave in the eliminated variable, endpoint nonnegativity is necessary and sufficient and admits a clean fraction-free chord identity. Degenerate width and strict endpoint semantics are treated exactly rather than silently closed.

No actual P5 source predicate, source key, chart, rational endpoint packet, state realization, trajectory/FD-halo coverage, Float64/libm semantics, Lean/kernel proof, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Let `I` be a compact rational interval for the outer parameter `q`. Let the outer source be described by a finite Boolean formula

`Phi(q,s)`

in polynomial sign atoms over `Q[q,s]`.

For every outer point where the inner parameterization is valid, let

`a(q,s) = Na(q,s) / Da(q,s)`,

`b(q,s) = Nb(q,s) / Db(q,s)`,

with `Na,Da,Nb,Db in Q[q,s]`.

On one regular outer cell, orient the representations so that

`Da > 0`, `Db > 0`.

Denominator zeros are not silently crossed; they are separate exceptional/source-validity cells.

Let the Lyapunov slack be

`p(q,s,t) = C(q,s) - B(q,s) t + H(q,s) t^2`,

where `B,C,H in Q[q,s]` after clearing any already certified positive common denominator. The desired safety statement is `p>=0`.

Define the fraction-free endpoint/order data

`L  := Nb Da - Na Db`,

`Ga := Da B - 2 Na H`,

`Gb := Db B - 2 Nb H`,

`Ea := Da^2 C - Na Da B + Na^2 H`,

`Eb := Db^2 C - Nb Db B + Nb^2 H`,

`F  := 4 H C - B^2`.

Then

`b-a = L/(Da Db)`,

`Ea = Da^2 p(a)`,

`Eb = Db^2 p(b)`,

and, when `H != 0`, `F/(4H)` is the slack at the stationary point `t=B/(2H)`.

All seven quantities lie in `Q[q,s]`.

---

## 2. Theorem A — full-curvature exact interval elimination

Assume at one fixed outer point

`Da>0`, `Db>0`, `L>0`.

Thus `a<b` and the closed inner section is nonempty.

### A1. Nonpositive curvature: `H<=0`

Then `p(t)` is concave/affine on `[a,b]`, so

`p(t)>=0 for every t in [a,b]`

if and only if

`Ea>=0` and `Eb>=0`.

Necessity is immediate because both endpoints belong to the closed interval. Sufficiency follows from concavity, but there is a stronger fraction-free identity in Section 3.

### A2. Positive curvature: `H>0`

Then `p` is strictly convex. The minimum is at the left endpoint, right endpoint, or the unique stationary point. Because

`Ga/Da = B-2aH = -p'(a)`,

`Gb/Db = B-2bH = -p'(b)`,

the exact branch formula is:

**LEFT**

`Ga <= 0` and `Ea >= 0`.

**RIGHT**

`Ga > 0`, `Gb >= 0`, and `Eb >= 0`.

**INTERIOR**

`Ga > 0`, `Gb < 0`, and `F >= 0`.

These three branches are exhaustive and disjoint under `H>0`, `L>0`.

Therefore define

`SafePos :=`

`  (Ga<=0 and Ea>=0)`

`  or (Ga>0 and Gb>=0 and Eb>=0)`

`  or (Ga>0 and Gb<0 and F>=0)`.

Then the exact closed-interval safety formula is

`SafeClosed :=`

`  (H<=0 and Ea>=0 and Eb>=0)`

`  or (H>0 and SafePos)`.

This is already a Boolean polynomial-sign formula in `(q,s)`.

### Proof of the positive-curvature dispatcher

Since `H>0`, `p'` is strictly increasing.

- If `Ga<=0`, then `p'(a)>=0`, hence `p' >=0` throughout `[a,b]`; the minimum is `a`.
- If `Ga>0` and `Gb>=0`, then `p'(a)<0` and `p'(b)<=0`; the minimum is `b`.
- If `Ga>0` and `Gb<0`, then `p'(a)<0<p'(b)`; the unique stationary point lies in `(a,b)` and is the minimum. Completing the square gives minimum `F/(4H)`.

Positive denominators preserve every sign. QED.

---

## 3. Theorem B — new fraction-free concave chord identity

The `H<=0` branch has a particularly useful division-free certificate.

For `t in [a,b]`, define scaled endpoint slacks

`x := Da t - Na = Da(t-a) >= 0`,

`y := Nb - Db t = Db(b-t) >= 0`.

Then the exact polynomial identity is

**(3.1)**

`L Da Db p(t)`

`= Db y Ea + Da x Eb - H L x y`.

This is the rational-endpoint version of the ordinary chord identity

`(b-a)p(t)`

`= (b-t)p(a) + (t-a)p(b) - H(b-a)(t-a)(b-t)`.

Under

`L>0`, `Da>0`, `Db>0`, `x>=0`, `y>=0`, `H<=0`, `Ea>=0`, `Eb>=0`,

every term on the right of (3.1) is nonnegative, hence `p(t)>=0`.

No inverse, square root, optimizer, or algebraic root is needed. This identity is also attractive for Lean because after the sign premises, the algebraic body is a single `ring_nf`-style equality.

The identity was checked by direct symbolic expansion from the definitions of `L,Ea,Eb,x,y,p`.

---

## 4. Theorem C — strict/weak endpoint semantics

The source inner section may be one of

`[a,b]`, `(a,b]`, `[a,b)`, `(a,b)`.

Let `leftWeak` and `rightWeak` record whether the corresponding boundary is included.

### Nondegenerate width: `L>0`

All four interval variants contain the open interval `(a,b)` and have closure `[a,b]`. Because `p` is continuous,

`p>=0` on the declared interval

if and only if

`p>=0` on `[a,b]`.

Hence **the same `SafeClosed` formula is exact for every strict/weak choice when `L>0`.** Excluded endpoints do not weaken the universal continuous inequality: a negative endpoint value would persist on nearby admitted points.

### Degenerate width: `L=0`

Now `a=b`.

- if both endpoint inequalities are weak, the section is the singleton `{a}` and safety is exactly `Ea>=0`;
- if either endpoint inequality is strict, the section is empty and universal safety is vacuous.

This branch must not be replaced by the closure rule.

### Negative width: `L<0`

For the literal pair of lower/upper inequalities, the section is empty and universal safety is vacuous.

If a source contract separately promises that `a,b` are ordered endpoints of a nonempty physical fiber, then observing `L<0` is instead a **source-parameterization obstruction**. These are different semantics and must not be conflated.

Thus, under valid oriented denominators, the exact nonempty-section predicate is

`Nonempty := (L>0) or (L=0 and leftWeak and rightWeak)`.

---

## 5. Theorem D — explicit inner quantifier elimination

Define the section-safety formula `Psi(q,s)` by

- `L<0`: `True` for literal interval semantics;
- `L=0` and at least one strict endpoint: `True`;
- `L=0` and both weak: `Ea>=0`;
- `L>0`: `SafeClosed` from Section 2.

Then, at every outer point with valid rational endpoints,

**(5.1)**

`Psi(q,s)`

if and only if

`forall t, [t satisfies the declared inner interval] -> p(q,s,t)>=0`.

Crucially, `Psi` is a finite Boolean formula in signs/equalities of the polynomial family

`{L,H,Ga,Gb,Ea,Eb,F}`.

Therefore eliminating the continuous variable `t` does **not** increase the algebraic variable dimension of the remaining certificate. It only enlarges the Boolean sign packet.

This is an exact special-purpose quantifier elimination theorem for a bounded quadratic variable.

---

## 6. Theorem E — nested triangular source reduces to T-P5-272

Consider the full source

`S = {(q,s,t): q in I, Phi(q,s), t in inner_section(q,s)}`.

Assume `Da,Db` are valid on all outer points whose inner section is physically used; denominator sign changes are refined into regular cells before applying the theorem.

Then

`forall (q,s,t) in S, p(q,s,t)>=0`

is equivalent to

`forall (q,s), Phi(q,s) -> Psi(q,s)`.

Equivalently, the outer violation set is

`V = {(q,s): Phi(q,s) and not Psi(q,s)}`.

Because both `Phi` and `Psi` are finite Boolean formulas in polynomial sign atoms over `Q[q,s]`, `V` is exactly a T-P5-272 one-fiber semialgebraic object.

Hence:

1. refine all source and elimination polynomials into one common squarefree factor basis;
2. add discriminants, distinct-factor resultants, leading coefficients, denominator zeros, and clipping-boundary events to the finite exceptional `q` set;
3. on every regular `q` cell, determine the full sign vector on each open `s` strip and root graph;
4. reject safety exactly when `Phi and not Psi` is true on a realizable strip/graph component;
5. specialize exceptional `q` point cells directly.

No outer numerical minimization is required. The outer stage is a sign/topology problem, not a second continuous optimization problem.

This is the main compositional result of the child:

**triangular two-variable source + quadratic inner target -> finite Boolean one-variable fiber problem.**

---

## 7. Graph and finite-union corollaries

### Exact graph fiber

If the inner source is the graph

`t = g(q,s) = Ng/Dg`, `Dg!=0`,

then

`Dg^2 p(q,s,g)`

`= Dg^2 C - Ng Dg B + Ng^2 H`.

Because `Dg^2>0`, graph safety is exactly one polynomial sign test. Thus graph-like two-variable sources are even cheaper than interval fibers.

### Finite union of interval/graph components

Suppose a source decomposition gives finitely many active inner components, each of which is either a rational interval with explicit strict/weak flags or a rational graph. Then universal safety is the conjunction of the componentwise `Psi_j` formulas, guarded by their activation predicates.

A finite conjunction/disjunction of such formulas remains a finite Boolean polynomial-sign formula in `(q,s)`. Hence the outer T-P5-272 arrangement still applies exactly.

This covers a substantial class of two-variable semialgebraic fibers without general CAD.

---

## 8. Exact regression 1 — triangular fidelity prevents a false obstruction

Take

`0<=s<=1`,

`0<=t<=s`,

`p(s,t)=s-t`.

The true triangular source is exactly safe because `t<=s` implies `p>=0`.

In the theorem notation,

`C=s`, `B=1`, `H=0`, `a=0`, `b=s`,

so

`L=s`, `Ga=Gb=1`, `Eb=s-s=0`.

For every `s>0`, the interval is nondegenerate and safe. At `s=0`, the width collapses to a weak/weak singleton and `Ea=0`, so the seam is also safe.

Now replace the triangular source by the rectangle

`0<=s<=1`, `0<=t<=1`.

The point `(s,t)=(0,1)` gives `p=-1`.

Therefore a rectangle/outer-box relaxation manufactures a false violation even though every true source state is safe. Nested elimination preserves the source correlation exactly and should be preferred whenever the source exposes it.

---

## 9. Exact regression 2 — endpoints alone are unsound for positive curvature

Take

`p(t)=t^2-t+3/16`, `t in [0,1]`.

Both endpoint values are `3/16>0`, but

`p(1/2)=-1/16<0`.

Here

`H=1`, `B=1`, `C=3/16`,

`Ga=1>0`, `Gb=-1<0`,

`F=4*(3/16)-1=-1/4<0`.

The INTERIOR branch detects the failure exactly. Thus the concave/affine endpoint theorem must not be extended across `H>0`.

---

## 10. Exact regression 3 — degenerate strict sections cannot be closed blindly

Let

`a=b=0`,

and let the declared inner section be `[0,0)`.

It is empty. Take the continuous slack `p(t)=-1`.

Universal safety on the true section is vacuously true, while replacing the section by its closure `{0}` produces a false failure.

Therefore the closure equivalence from nondegenerate intervals is valid only when `L>0`. At `L=0`, strict/weak endpoint truth must be retained explicitly, exactly as T-P5-272 retained graph-boundary truth for Boolean source fibers.

---

## 11. Denominator and representation semantics

The rational endpoint theorem is exact only where each endpoint representation is defined.

A source-facing checker must distinguish:

1. `Da=0` or `Db=0` on an active source component: **RATIONAL_ENDPOINT_UNDEFINED** unless another local chart supplies the endpoint;
2. denominator sign fixed but negative: reorient `(N,D)->(-N,-D)` on that regular cell before using `L,Ga,Gb` signs;
3. denominator sign changes: add the zero to the outer arrangement and treat the adjacent cells separately;
4. a removable common factor canceled only algebraically: the source must specify whether the uncanceled representation is physically undefined there. Cancellation cannot silently invent a source state.

All endpoint debit expressions use denominator squares, but branch orientation (`L,Ga,Gb`) does not. Denominator orientation is therefore a genuine soundness premise, not cosmetic normalization.

---

## 12. Algebraic-endpoint boundary

If `a(q,s)` or `b(q,s)` is a selected algebraic root rather than a rational function, the pointwise quadratic clamp remains true. However the current compositional theorem no longer automatically produces a Boolean formula over `Q[q,s]`.

Signs such as

`p(q,s,a(q,s))`, `B-2H a(q,s)`,

must be certified on the **selected root branch**. A raw resultant or field norm is not sign-faithful to a chosen real branch; T-P5-269/270 already record this obstruction in one-parameter form.

With two outer variables `(q,s)`, a fully general Thom-cell projection would begin to approach bivariate CAD. Therefore this child deliberately makes the exact closure claim only for rational endpoints (or graph values) after cellwise denominator orientation.

If the actual P5 source exposes algebraic nested endpoints, the next mathematical seam should be a selected-root sign-transport theorem specialized to the actual low-degree endpoint polynomial, not a generic CAD implementation.

---

## 13. Source-facing certificate packet

A minimal exact packet for this theorem is:

- outer Boolean source syntax `Phi(q,s)` and the exact source key;
- rational endpoint numerators/denominators `Na,Da,Nb,Db`;
- strict/weak endpoint flags;
- polynomial target coefficients `C,B,H` in the same chart/metric/source key;
- denominator-validity and cellwise orientation data;
- derived polynomials `L,Ga,Gb,Ea,Eb,F`;
- common-factor / sign-arrangement packet for `Phi and not Psi`;
- exact exceptional `q` point-cell packets;
- if the source declares every section nonempty, an explicit proof of the required width/order condition rather than treating empty sections as physical states.

No floating root coordinate is mathematically required for the rational-endpoint branch.

---

## 14. Suggested Lean decomposition

The useful leaves remain small:

1. `quadratic_chord_identity_fractionFree`:
   prove `L*Da*Db*p = Db*y*Ea + Da*x*Eb - H*L*x*y` by ring normalization;
2. `quadratic_nonneg_of_nonpos_curvature_endpoints`:
   consume the identity and sign hypotheses;
3. `quadratic_posCurvature_left`;
4. `quadratic_posCurvature_right`;
5. `quadratic_posCurvature_interior` with completed square `4H*p=(2Ht-B)^2+F`;
6. `quadratic_interval_nonneg_iff_dispatch` for `L>0`;
7. `continuous_nonneg_intervalVariant_iff_closed_of_lt` for strict/weak nondegenerate intervals;
8. `degenerate_interval_truth` for `L=0` and boundary flags;
9. `graph_substitution_fractionFree`;
10. `forall_nested_iff_outer_formula` as a pure logical quantifier-pushing lemma once `Psi` has been defined.

The common-root arrangement, factorization, resultants, and Thom preprocessing can remain external certified preprocessing as in T-P5-272.

---

## 15. Fail-closed semantics

The dispatcher should distinguish:

- rational endpoint denominator zero on an active source point: **RATIONAL_ENDPOINT_UNDEFINED**;
- denominator orientation unavailable: **DENOMINATOR_ORIENTATION_REQUIRED**;
- `L<0` under literal interval semantics: empty inner section, not target FAIL;
- `L<0` under a separate nonempty-section source contract: **SOURCE_ORDER_OBSTRUCTION**;
- `L=0` with any strict side: empty section, not singleton;
- `L=0` weak/weak: singleton, check endpoint exactly;
- positive-curvature interior branch with `F<0`: exact mathematical failure of the declared interval fiber;
- rectangle/box relaxation failure when the true triangular packet is available: only **OUTER_RELAXATION_OBSTRUCTION**, never a true-source counterexample;
- missing outer sign arrangement: **CERTIFICATE_NOT_FOUND**, not mathematical FAIL;
- algebraic endpoint without selected-root sign certificate: **ALGEBRAIC_BRANCH_SELECTOR_REQUIRED**;
- negative witness after exact source binding: only then eligible to propagate as a physical/source failure, subject to state realization and coverage.

---

## 16. Remaining obligations

Still open:

1. determine whether the actual P5 two-variable source fiber has triangular/graph structure after the chosen quotient/chart;
2. bind `Phi,q,s,t,Na,Da,Nb,Db,C,B,H` to one source key and one evaluator;
3. prove rational endpoint representations are valid on the active source cells;
4. retain exact strict/weak/equality semantics of every inner component;
5. produce the outer common-factor arrangement for `Phi and not Psi`;
6. prove clipping/domain restrictions and point-cell specializations;
7. bind target metric and any denominator clearing to certified positive factors;
8. state/trajectory realization of any negative witness;
9. cell/flowed-sheet/FD-halo/reference-halo coverage;
10. Float64/libm/interval enclosure;
11. Lean/kernel formalization of the leaves;
12. independent validation by 封不觉;
13. admission, registry mutation, and P5/P8/M4 propagation.

---

## 17. Next mathematical seam

This child shows that **rational triangular fibers are closed under exact quadratic elimination** and land directly back in the T-P5-272 class.

The next step should be source-sensitive rather than another generic relaxation:

- if the actual P5 packet has rational/affine triangular endpoints, instantiate `Psi` and build the outer violation arrangement immediately;
- if the endpoints are low-degree algebraic selected roots, prove a specialized parametric selected-root sign transport for the exact endpoint polynomial so that `Ea/Eb/Ga/Gb` signs can be pushed back to `Q[q,s]` without a full bivariate CAD;
- if the target is not quadratic in the inner variable, first determine whether its derivative has a certified monotonicity/convexity structure that yields a similarly finite endpoint/stationary-point dispatcher.

Until the actual source geometry chooses one of these branches, a general CAD jump would be premature and would lose the source-specific structure that has made T-P5-268 through T-P5-273 exact and fraction-free.