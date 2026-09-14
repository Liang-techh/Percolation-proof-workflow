---
kind: review_result
review_id: review-T-P5-276-algebraic-endpoint-sturm-tarski-bridge-liuguanyi-20260910T2004Z
task_id: T-P5-276-ALGEBRAIC-ENDPOINT-STURM-TARSKI-BRIDGE
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T20:04:00Z
claim_commit: 063adbeece8213b9164e299f4db4820e17426795
inspected_commit: 39fa033206a1caadf489f146923b58e3f087735c
upstream_commits:
  - 0614631ed6a730a60242ece09090c1d57af12a8f # T-P5-275 convex quartic selected-root reserve
  - 796fdbafb703dd97bb6841632091174aac469e68 # T-P5-270 algebraic moving-fiber Thom closure
  - 2a5617c335f912dda8ff720a9354e0f5b548740a # T-P5-272 Boolean semialgebraic fiber arrangement
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_algebraic_bracket_unique_critical_root_bridge; add_selected_endpoint_sturm_tarski_wrapper; add_interval_selected_contact_transport; add_squarefree_gcd_active_branch_dispatch; avoid_explicit_tau_thom_matching; preserve_source_binding_and_point_cell_boundaries
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact ordered-field/continuity derivation; selected-root Sturm-Tarski reduction; squarefree-gcd/resultant branch analysis; exact rational regressions; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-276 — Algebraic-endpoint Sturm–Tarski bridge for the convex quartic lane

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-275 closed a convex quartic on a rational moving interval and left the genuinely algebraic-endpoint case open. T-P5-270 already solved the generic problem “evaluate the sign of a polynomial at one selected algebraic endpoint”. The missing bridge is therefore not another generic Thom/resultant theorem. It is the interface between those selected endpoint signs and the **interval-selected critical root** used by the quartic Sturm–Tarski certificate.

This review proves that the algebraic endpoints do not force a three-root matching problem and do not force bivariate CAD.

The central simplification is:

> under the quartic convexity gate, the active critical root `tau` never needs its own Thom selector.

If `g=p_t` and the selected algebraic endpoints satisfy

`g(ell)<0<g(r)`,

then convexity alone proves that there is exactly one root `tau` of `g` in `(ell,r)`. Thus the interval itself selects the physical critical root. The two ordering tests `ell<tau<r` are replaced by two T-P5-270 selected-endpoint sign queries.

At a fixed algebraic outer parameter, the remaining reserve sign is computed exactly by the same Sturm–Tarski query as T-P5-275. Its signed Sturm/Habicht endpoint signs are themselves just polynomial signs at the selected algebraic roots `ell,r`, so T-P5-270 supplies them directly.

Across a regular one-dimensional outer `q` cell, the active root is continuous even if it is multiple, and its reserve sign cannot change without an exact selected contact. A squarefree/gcd reduction separates persistent contact on the active root from irrelevant common factors on inactive derivative roots. Therefore one exact algebraic sample per open cell plus finitely many resultant/subresultant point cells suffices.

No actual P5 endpoint equation, source key, source-fiber identity, state realization, domain/trajectory/FD/reference-halo coverage, Float64/libm semantics, Lean/kernel proof, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Let `q` vary on a connected regular outer cell `J`. For each `q`, let

`p_q(t)=a4(q)t^4+a3(q)t^3+a2(q)t^2+a1(q)t+a0(q)`

and let `eta(q)` be the requested reserve.

Write

`g(q,t)=partial_t p_q(t)`

and let `K_eta(q,t)` be the quadratic stationary-reserve polynomial from T-P5-275, so at every critical root `g(q,t)=0`,

**(1.1)** `16 a4(q)^2 (p_q(t)-eta(q)) = K_eta(q,t)`.

Assume `a4(q) != 0` on the regular cell.

The endpoints are selected simple algebraic branches

`L(q,ell(q))=0`,

`R(q,r(q))=0`,

with `L,R in Q[q,z]` after denominator clearing, together with branch selectors (isolating interval or Thom encoding). Assume the endpoint branches are real, continuous on `J`, and satisfy

**(Ord)** `ell(q)<r(q)`.

Finally assume the same-fiber convexity premise

**(Cvx)** `partial_t^2 p_q(t)>=0` for every `t in [ell(q),r(q)]`.

The source-binding obligation is deliberately external: this theorem consumes a proved same-key interval and does not manufacture one from endpoint equations.

---

## 2. Theorem A — the algebraic bracket selects the critical root, so no `tau` Thom code is needed

Assume (Ord), (Cvx), and

**(Int)** `g(q,ell(q))<0<g(q,r(q))`.

Then for every `q in J` there exists a unique

`tau(q) in (ell(q),r(q))`

such that

`g(q,tau(q))=0`.

Moreover `tau(q)` is the global minimizer of `p_q` on `[ell(q),r(q)]`.

### Proof

By (Cvx), `g(q,.)` is nondecreasing on the active interval. The strict endpoint signs give existence by the intermediate value theorem. If two distinct zeros existed, monotonicity would force `g` to vanish on the entire interval between them. Since `g` is a nonzero cubic when `a4!=0`, that is impossible. Hence the zero is unique.

The derivative is negative before the unique zero and positive after it, so `p_q` decreases up to `tau` and increases after `tau`. Therefore `tau` is the global interval minimizer. QED.

### Interface consequence

The checker must **not** solve three separate algebraic root equations and then compare their Thom encodings. Under (Cvx), the statement

`ell < tau < r`

is already encoded by the two selected-endpoint signs

`g(ell)<0` and `g(r)>0`.

Each is exactly a T-P5-270 selected-root sign problem:

- evaluate `g(q,z)` at the selected root `L(q,z)=0` carrying `ell`;
- evaluate `g(q,z)` at the selected root `R(q,z)=0` carrying `r`.

This removes a whole branch-matching layer from the source adapter.

---

## 3. Theorem B — the interval-selected critical root is continuous even when it is multiple

Under the hypotheses of Theorem A, assume the coefficients of `g` and the endpoint branches are continuous in `q`. Then the unique root map

`q -> tau(q)`

is continuous on `J`.

### Proof

Fix `q0 in J` and a sequence `qn -> q0`. Because `ell,r` are continuous, the intervals `[ell(qn),r(qn)]` are locally bounded. Thus every subsequence of `tau(qn)` has a convergent subsubsequence, say to `t*`.

From

`ell(qn)<tau(qn)<r(qn)`

and continuity of the endpoints,

`ell(q0)<=t*<=r(q0)`.

From `g(qn,tau(qn))=0` and continuity of `g`,

`g(q0,t*)=0`.

The strict endpoint signs at `q0` exclude `t*=ell(q0)` and `t*=r(q0)`. Theorem A gives a unique zero in the open interval, hence `t*=tau(q0)`.

Every convergent subsequence has the same limit, so `tau(qn)->tau(q0)`. QED.

### Why this matters

No implicit-function denominator `1/g_t(tau)` is required. In particular the argument remains valid at a flat convex contact such as a cubic derivative with an odd multiple root. A discriminant-zero critical root is therefore not automatically a mathematical failure or a reason to leave the algebraic-endpoint lane.

---

## 4. Theorem C — quartic safety reduces to one interval-selected reserve sign

Under Theorem A,

`p_q(t)>=eta(q) for every t in [ell(q),r(q)]`

if and only if

**(4.1)** `K_eta(q,tau(q))>=0`.

### Proof

Theorem A identifies `tau` as the global minimizer. Therefore interval safety is equivalent to `p_q(tau)>=eta`. Identity (1.1) multiplies this difference by `16a4^2>0`, so it has exactly the same sign as `K_eta(q,tau)`. QED.

Thus the algebraic-endpoint INTERIOR branch needs only:

1. selected sign `g(ell)<0`;
2. selected sign `g(r)>0`;
3. selected reserve sign at the **unique derivative root lying between them**.

The third selector is supplied by the interval/Sturm query, not by an explicit root object.

---

## 5. Theorem D — fixed-`q` Sturm–Tarski query with algebraic endpoints

Fix one exact outer value `q=q0`, possibly itself real algebraic. Work in the exact real-algebraic ordered field generated by `q0` and the selected endpoint roots `ell,r`.

Assume

`g(ell)<0<g(r)`.

Then `g` has exactly one distinct root `tau` in `(ell,r)`, so

**(5.1)**

`TaQ_(ell,r)(K_eta,g)=sign(K_eta(tau))`.

The Sturm–Tarski theorem computes this query as the Cauchy index of

`g_t K_eta / g`

on `(ell,r)`, using a finite signed Sturm/Habicht or signed-subresultant remainder chain.

Every endpoint datum required by that computation has the form

`sign S_j(ell)` or `sign S_j(r)`

for a polynomial `S_j(t)` over the exact coefficient field. Because `ell` and `r` are already selected algebraic roots, these signs are exactly the T-P5-270 primitive:

`selected_root_sign(endpoint_polynomial, endpoint_selector, S_j)`.

Therefore the complete interior reserve sign is computable without:

- a radical/cubic formula for `tau`;
- a floating approximation to `ell,r,tau`;
- comparing Thom codes of roots of three unrelated polynomials;
- a general bivariate CAD.

At a fixed point cell the computation is finite and exact.

---

## 6. Theorem E — open-cell sign transport by an exact contact polynomial

Continue on a connected `q` cell satisfying Theorems A–B. Define

`h(q)=K_eta(q,tau(q))`.

Then `h` is continuous.

If

`Res_t(g,K_eta)(q) != 0`

for every `q` in the cell, then `h(q) != 0` everywhere, and hence `sign h(q)` is constant on the connected cell.

### Proof

Continuity follows from Theorem B and continuity of the polynomial coefficients. If `h(q*)=0`, then `tau(q*)` is a common root of `g(q*,.)` and `K_eta(q*,.)`; therefore their resultant vanishes at `q*`. Contradiction. A continuous nonzero real function on a connected set has constant sign. QED.

### Practical consequence

On the generic coprime branch, the outer atlas does **not** need to transport the full parametric Sturm chain. It may split at the finite real roots of the contact resultant, then compute the exact algebraic-endpoint Tarski query once at one rational sample per open cell. The query’s sign propagates to the whole cell by Theorem E.

This is strictly smaller than treating every signed-PRS endpoint evaluation as an independent parametric projection atom.

---

## 7. Important obstruction — a zero global resultant need not be contact of the active critical root

A global resultant multiplies information from all derivative roots. It is therefore only a safe **noncontact** certificate when nonzero; zero is ambiguous.

Take

`g(t)=t(t-2)(t-3)=t^3-5t^2+6t`

and integrate

`p(t)=t^4/4-(5/3)t^3+3t^2`.

On the active interval

`[-1/2,1/2]`,

`p''(t)=3t^2-10t+6`.

This quadratic is decreasing on that interval and

`p''(1/2)=7/4>0`,

so the quartic is strictly convex there. Also

`g(-1/2)=-35/8<0`,

`g(1/2)=15/8>0`,

so the interval-selected minimizer is exactly `tau=0`.

Choose

`eta=p(2)=8/3`.

Because `a4=1/4`, identity (1.1) has factor `16a4^2=1`, hence

`K_eta(0)=p(0)-eta=-8/3<0`.

But `t=2` is another root of `g`, outside the active interval, and

`K_eta(2)=p(2)-eta=0`.

Therefore

`Res_t(g,K_eta)=0`

although the **active** selected reserve is strictly negative.

So neither

`Res=0 -> active contact`

nor any verdict derived from that implication is valid. Zero-resultant cells require branch-aware gcd/root membership or a direct interval Sturm–Tarski query.

---

## 8. Theorem F — persistent gcd reduction separates active structural contact from inactive common roots

The exact generic coefficient field is `Q(q)`. Let

`g_sf = sqfree_t(g)`

be the squarefree part of the derivative over `Q(q)[t]`, and define

`D = gcd(g_sf,K_eta)`,

`G = g_sf / D`.

Then `g_sf` and `g` have the same distinct roots, while

`gcd(G,K_eta)=1`.

On a regular open `q` cell where specialization preserves these degrees/factors, Theorem A gives exactly one distinct derivative root in `(ell,r)`. Exactly one of the following holds.

### F1. Active structural-contact branch

`D` has one root in `(ell,r)`.

Since the derivative has exactly one root there, that root is `tau`; because `D|K_eta`,

`K_eta(tau)=0`

throughout the branch cell. This is a genuine zero reserve, not a missing certificate.

### F2. Active coprime branch

`D` has no root in `(ell,r)`.

Then `tau` is a root of `G`. Since `gcd(G,K_eta)=1` over `Q(q)[t]`, the reduced contact resultant

`R_act(q)=Res_t(G,K_eta)`

is a nonzero rational function of `q`. After clearing coefficient denominators, its numerator is a nonzero polynomial. On every connected subcell avoiding its real zeros,

`K_eta(tau)` is nonzero and has constant sign by Theorem E.

### How branch membership is decided

At one exact sample `q*`, count roots of `D(q*,.)` in the algebraic interval `(ell(q*),r(q*))` by a Sturm count whose endpoint signs again use the T-P5-270 selected-root evaluator. Because the whole derivative has exactly one active root, the count is `0` or `1`.

To propagate the membership label, include the ordinary specialization/degree factors and the collision resultant `Res_t(D,G)` (when nonconstant), plus the already-required endpoint-contact events. At their zeros, specialize as point cells and recompute. Thus inactive persistent common factors do not poison the whole outer cell.

---

## 9. One-dimensional exact dispatcher

A source adapter for the genuinely algebraic-endpoint convex-quartic branch can use the following finite exact route.

### 9.1 Build endpoint/source regularity atoms

From T-P5-270 / T-P5-272 retain:

- leading coefficients and discriminants needed to keep the selected endpoint branches real/simple;
- endpoint collision/order factors;
- all denominator-orientation factors;
- the exact source Boolean semantics selecting the branches.

### 9.2 Build quartic structural atoms

Add:

- `a4` degree-drop factor;
- exact convexity projection factors for `p''>=0` on the same algebraic interval;
- selected endpoint contact resultants for `g(ell)=0` and `g(r)=0` (with T-P5-270 gcd membership semantics if a resultant vanishes identically).

### 9.3 Build reserve-contact atoms

Compute `g_sf,D,G` over `Q(q)[t]` and add the nonzero specialization factors needed to preserve them. In the coprime active branch add the numerator of

`Res_t(G,K_eta)`.

### 9.4 Open cells

Each connected open `q` cell now has fixed:

- endpoint branch identities and order;
- convexity truth;
- LEFT / RIGHT / INTERIOR branch;
- persistent-gcd membership of the unique active derivative root;
- in the noncontact interior branch, the sign of `K_eta(tau)`.

Choose one rational sample `q*` in the cell. Evaluate endpoint signs by selected-root algebraic sign determination. In the INTERIOR branch compute one exact algebraic-endpoint Sturm–Tarski query. The resulting safety truth applies to the whole open cell.

### 9.5 Point cells

At every projection root, specialize all polynomials exactly in the corresponding real-algebraic field and rerun the fixed-`q` dispatcher of Theorem D. Degree drops, endpoint collisions, repeated critical roots, zero reserve, and strict/weak source atoms are therefore retained rather than discarded as measure-zero.

The output remains a **finite one-dimensional `q` atlas**, not a general two-variable CAD.

---

## 10. Algebraic-endpoint regression with no explicit critical-root object

Take

`p(t)=t^4+t`, `eta=-1`,

and let the endpoints be the two selected roots of

`E(z)=z^2-2`:

`ell=-sqrt(2)`, `r=+sqrt(2)`.

Then

`p''(t)=12t^2>=0`,

`g(t)=4t^3+1`.

Selected-root sign determination gives

`g(ell)=1-8sqrt(2)<0`,

`g(r)=1+8sqrt(2)>0`.

Therefore the interval itself selects the unique critical root `tau`; no cubic radical or Thom code for `tau` is part of the certificate.

Here T-P5-275 gives

`K_eta(t)=12t+16`.

The active root satisfies `-1<tau<0` because `g(-1)=-3<0<g(0)=1`. Hence

`K_eta(tau)>4>0`,

so the reserve is strictly positive. An exact algebraic-endpoint Sturm–Tarski implementation returns the same `+1` sign using only endpoint sign oracles.

This regression exercises the intended source-facing shape: algebraic endpoints, unique interval-selected cubic root, and no numerical root serialization.

---

## 11. Failure boundaries

The following distinctions are mandatory.

- Missing endpoint selector / source branch identity: `SOURCE_BINDING_REQUIRED`, not mathematical FAIL.
- Convexity not proved on the exact same moving interval: this lane is inapplicable; do not use a sum over several critical roots.
- `g(ell)=0` or `g(r)=0`: route to the endpoint-contact specialization; do not reuse the strict INTERIOR query unchanged.
- `Res(g,K_eta)=0`: ambiguous global contact; it may come from an inactive derivative root. Use squarefree/gcd membership or fixed-`q` interval Tarski evaluation.
- Active branch lies in `D=gcd(g_sf,K_eta)`: exact zero reserve, not “certificate not found”.
- Reduced resultant / endpoint discriminant / factor-specialization zero: isolate a point cell and recompute exactly.
- Algebraic-endpoint Tarski query negative on a proved same-key source fiber: mathematical failure of the declared algebraic fiber. Physical P5 FAIL still requires state realization and coverage.
- Failure of a heuristic algebraic package, floating root matcher, or finite SOS search: `CERTIFICATE_NOT_FOUND`, never physical FAIL.

Strict inequalities in the source remain strict. Continuous closure may justify a nonnegative target limit on an excluded endpoint, but a violation existing only on an excluded boundary is not automatically a realized source counterexample.

---

## 12. Minimal theorem statements for formalization

The mathematical interface can be decomposed without formalizing all real algebraic geometry at once.

1. `continuous_unique_zero_in_moving_bracket`
   - continuous `ell,r,g`, strict endpoint signs, uniqueness of the zero on each fiber -> continuous selected zero `tau`.

2. `convex_quartic_algebraic_bracket_selects_critical`
   - `p''>=0`, `g ell<0<g r` -> unique global minimizer inside the bracket.

3. `quartic_interval_selected_reserve_iff_K`
   - combine the minimizer theorem with T-P5-275 identity `16a4^2(p-eta)=K` on `g=0`.

4. `tarski_query_single_root_algebraic_endpoints`
   - over a real closed/exact ordered field, one root in `(ell,r)` turns the Tarski query into `sign K(tau)`.

5. `selected_endpoint_sign_supplies_sturm_endpoint`
   - every signed-PRS endpoint evaluation required by the Cauchy index is an instance of a generic selected-root polynomial-sign oracle.

6. `resultant_nonzero_transports_interval_selected_sign`
   - continuous unique active root + nonzero resultant -> active polynomial value has constant sign on a connected base cell.

7. `squarefree_gcd_active_contact_dichotomy`
   - with `g_sf=D*G`, the unique active root is either in `D` and has structural zero reserve, or in `G` and is controlled by the reduced resultant.

The Sturm/subresultant computation itself may remain checker-side until a pinned Mathlib real-algebraic API is selected. That does not justify replacing it with floating root evaluation.

---

## 13. What this child changes

Before this review, T-P5-275’s algebraic-endpoint continuation appeared to require simultaneously tracking three moving algebraic roots: `ell(q)`, the cubic critical root `tau(q)`, and `r(q)`.

The new bridge removes that requirement:

`selected algebraic ell,r`

`-> selected signs g(ell),g(r)`

`-> convexity makes the interval itself a selector for the unique tau`

`-> fixed-q Tarski query uses signed-PRS endpoint signs`

`-> those endpoint signs are T-P5-270 selected-root queries`

`-> continuity + reduced contact resultant transports the active reserve sign across open q-cells`

`-> projection roots are handled as exact algebraic point cells`.

Hence **genuinely algebraic moving endpoints remain within the finite one-dimensional P5 dispatcher without an explicit critical-root Thom matching layer.**

---

## 14. Remaining obligations

Still open:

1. identify an actual P5 quartic target and actual algebraic endpoint equations;
2. prove the endpoint selectors are the true same-key source-fiber endpoints;
3. prove endpoint continuity/reality/simple-root domains and `ell<r` on the actual source cells;
4. prove convexity on those exact same algebraic fibers;
5. instantiate the selected-root endpoint sign oracle and Sturm–Tarski chain in a pinned exact checker;
6. bind all coefficient/endpoint/resultant packets to one source key/chart/metric;
7. preserve Boolean strict/weak/equality semantics and all exceptional point cells;
8. construct state/trajectory realization for any negative algebraic witness;
9. whole-cell/flowpipe/FD-halo/reference-halo coverage;
10. Float64/libm/interval semantics where deployed evaluation is floating point;
11. Lean/kernel formalization;
12. independent validation by 封不觉;
13. admission, registry mutation, and P5/P8/M4 propagation.

---

## 15. Next nonduplicative mathematical seam

The next source-facing seam is no longer “how do we compare three algebraic roots”. That is removed here.

The highest-value continuation is a **strict convexity reserve perturbation / root-displacement theorem**: starting from a same-key packet `p''>=mu>0` and strict selected reserve `p(tau)-eta>=rho>0`, quantify how coefficient/FD endpoint perturbations move the interval-selected minimizer and consume `rho` without rebuilding the complete algebraic atlas. The theorem should distinguish perturbations of `p` from perturbations of the bracket, and should preserve a rational/fraction-free budget when possible.

A second disjoint seam is actual-source instantiation: if the deployed source endpoints come from specific polynomial predicates, bind their Thom selectors and test whether the quartic lane is really present before extending the abstract algebra further.
