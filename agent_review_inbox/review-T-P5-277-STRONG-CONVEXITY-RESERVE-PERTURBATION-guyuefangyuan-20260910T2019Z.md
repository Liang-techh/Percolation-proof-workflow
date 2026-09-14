---
kind: review_result
review_id: review-T-P5-277-strong-convexity-reserve-perturbation-guyuefangyuan-20260910T2019Z
task_id: T-P5-277-STRONG-CONVEXITY-RESERVE-PERTURBATION
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T20:19:00Z
claim_commit: 852a9dee2dd5042865ef9b2b22e854bc6474a8b0
inspected_commit: 027071e5a48bbb6ba67788c47479a24681aeca08
upstream_commits:
  - 20817a3e4dea7e68dcc1c02b52667b9ef995c115 # T-P5-276 algebraic-endpoint Sturm-Tarski bridge
  - 796fdbafb703dd97bb6841632091174aac469e68 # T-P5-270 selected algebraic endpoint sign machinery
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_strong_convex_clamp_minimizer; add_fraction_free_secant_cone_reserve_gate; add_constrained_minimizer_displacement; add_bracket_collar_transport; add_interior_branch_stability_gate; preserve_target_vs_source_perturbation_boundary
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact strong-convexity derivation; fraction-free square identity; constrained minimizer sensitivity; rational counterexamples; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-277 — Strong-convexity reserve perturbation without rebuilding the algebraic atlas

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-276 left a precise next seam: once the active one-dimensional fiber has a strict convexity margin and a strict reserve at its selected minimizer, small coefficient / FD / endpoint perturbations should not force reconstruction of the complete algebraic endpoint and Sturm–Tarski atlas.

This review closes the abstract mathematical part of that seam.

The main result is stronger than a root-displacement estimate. Suppose the nominal target `p` has a critical point `tau` and

`p'' >= mu > 0`

on a certified collar containing the perturbed fiber. Let the perturbed target be

`p_tilde = p + e`.

For the perturbed interval `C=[a,b]`, let

`y = clamp(tau,a,b)`

be the nominal minimizer of `p` on the new interval. If

`p(tau)-eta >= rho`,

`e(y) >= -eps`,

and the target perturbation satisfies the secant cone

`(e(t)-e(y))^2 <= D (t-y)^2` for all `t in C`,

then any certified lower bound

`(y-tau)^2 >= S >= 0`

produces the completely rational reserve gate

**(R2)** `R2 := 2(rho-eps) + mu S >= 0`,

**(Gate)** `D <= mu R2`.

Under these two scalar inequalities,

**`p_tilde(t) >= eta` for every `t in C`.**

No square root, minimizer solve, algebraic root matching, inverse, floating optimization, or rebuilt Sturm atlas is needed.

In the common no-bonus case `S=0`, this is simply

**`D <= 2 mu (rho-eps)`**.

The gate is sharp for the direction-forgetting secant-cone relaxation.

A separate theorem proves minimizer displacement. If `x` is any minimizer of `p+e` on `C` and `e'(x)^2 <= D`, then

**`mu^2 (x-y)^2 <= D`.**

Thus target perturbation moves the constrained minimizer by at most the derivative-error scale divided by the strong-convexity scale, while movement of the bracket itself is handled independently through `y=clamp(tau,C)`.

The key structural distinction is:

- **target perturbation consumes reserve** through the anchor debit `eps` and slope/secant debit `D`;
- **bracket perturbation by itself consumes no reserve** as long as the new fiber stays inside a collar where the same nominal `p` remains strongly convex around `tau`;
- if the new bracket leaves every certified convexity collar, old interval data alone cannot certify safety, even for an arbitrarily small endpoint expansion.

No actual P5 source packet, coefficient key, endpoint perturbation source, FD semantics, state realization, whole-cell/trajectory/FD/reference-halo coverage, Float64/libm enclosure, Lean/kernel proof, independent validation, admission, registry mutation, or parent closure is claimed.

---

## 1. Same-key setup

Fix one outer source key / chart / metric context. Let `J` be a real interval and let

`p : J -> R`

be twice differentiable. Assume there exists `tau in J` with

**(Crit)** `p'(tau)=0`

and a rationally certifiable constant `mu>0` such that

**(SC)** `p''(t)>=mu` for every `t in J`.

Let `eta` be the requested lower threshold and assume the old selected minimizer has reserve

**(Res)** `p(tau)-eta >= rho`.

Let the new source fiber be a closed interval

`C=[a,b] subset J`, `a<=b`.

The endpoint pair may be rational or algebraic. The theorem only consumes the already-proved same-key inclusion `C subset J`; it does not manufacture endpoint provenance.

Define

`y = clamp(tau,a,b)`.

Finally let a target/coefficient/FD perturbation be represented on this same coordinate by

`p_tilde(t)=p(t)+e(t)`.

A change in the scalar threshold `eta` can be absorbed into `e` as a constant perturbation, so no separate theorem is needed for `eta_tilde-eta`.

---

## 2. Lemma A — strong convexity makes the clamp the exact nominal minimizer on any moved bracket

From (SC), for any `s,t in J`,

**(2.1)**

`p(t) >= p(s) + p'(s)(t-s) + (mu/2)(t-s)^2`.

Because `p'(tau)=0` and `p'` is strictly increasing, `p` decreases to the left of `tau` and increases to the right.

Therefore on `C=[a,b]`,

**`y=clamp(tau,a,b)` is the unique minimizer of `p` on `C`.**

Moreover, for every `t in C`,

**(2.2)**

`p(t) >= p(y) + (mu/2)(t-y)^2`.

Indeed the constrained first-order term has the correct sign:

`p'(y)(t-y)>=0`.

Applying (2.1) from `tau` to `y` also gives the bracket-exclusion bonus

**(2.3)**

`p(y) >= p(tau) + (mu/2)(y-tau)^2`.

Consequences:

1. if the new interval still contains `tau`, then `y=tau` exactly;
2. if the interval excludes `tau`, the nominal minimum moves to the nearest endpoint and its value **increases**, rather than consuming reserve;
3. source/bracket movement inside the certified collar is therefore intrinsically non-damaging for the unchanged target.

This is the first important separation from a generic source-domain perturbation budget.

---

## 3. Lemma B — derivative-square error implies a fraction-free secant cone

Let `e` be differentiable on `C`. If

**(DerSq)** `(e'(u))^2 <= D` for every `u in C`,

then for every `t in C`,

**(3.1)**

`(e(t)-e(y))^2 <= D (t-y)^2`.

For a polynomial or `C^1` perturbation this follows immediately from the mean value theorem: for `t!=y`,

`e(t)-e(y)=e'(xi)(t-y)`

for some `xi` between `t` and `y`, and squaring removes every sign/square-root issue.

Thus a producer may either submit the secant cone directly or certify the univariate polynomial bound `(e')^2<=D` on the same new fiber/collar.

The checker never needs to serialize `sqrt(D)`.

---

## 4. Theorem C — fraction-free reserve gate

Assume Lemma A and the secant cone

**(Sec)** `(e(t)-e(y))^2 <= D (t-y)^2` for every `t in C`, with `D>=0`.

Assume an anchor bound

**(Anchor)** `e(y)>=-eps`.

Optionally assume a rational lower witness for the nominal bracket displacement

**(Bonus)** `(y-tau)^2 >= S`, `S>=0`.

Define

**(4.1)** `R2 = 2(rho-eps)+mu S`.

If

**(4.2)** `R2>=0`

and

**(4.3)** `D <= mu R2`,

then

**(4.4)** `p(t)+e(t) >= eta` for every `t in C`.

### Proof

Fix `t in C` and set

`s=t-y`,

`z=e(t)-e(y)`.

By (Res), (2.2), (2.3), (Anchor), and (Bonus),

`p(t)+e(t)-eta`

`>= rho - eps + (mu/2)S + (mu/2)s^2 + z`

`= R + (mu/2)s^2 + z`,

where

`R = R2/2 >= 0`.

The crucial fraction-free identity is

**(4.5)**

`(2R + mu s^2)^2 - 4D s^2`

`= (2R - mu s^2)^2 + 4(2muR-D)s^2`.

Because `D<=2muR`, the right-hand side is nonnegative. Hence

`(2R+mu s^2)^2 >= 4D s^2 >= 4z^2`.

Also `2R+mu s^2>=0`, so

`2R+mu s^2 >= 2|z| >= -2z`.

Therefore

`R+(mu/2)s^2+z>=0`.

This proves (4.4). QED.

### Checker form

The mathematical checker only needs rational scalars

`mu,rho,eps,D,S`

and the two scalar gates

`2(rho-eps)+mu S >= 0`,

`D <= mu(2(rho-eps)+mu S)`.

There is no division and no square root.

---

## 5. Corollaries

### 5.1 Same bracket / same minimizer

If the new interval contains `tau`, take `y=tau` and `S=0`. Then

`D <= 2mu(rho-eps)`

is sufficient.

If the perturbation is anchored exactly at the old minimizer, `e(tau)=0`, this becomes

**`D <= 2mu rho`.**

### 5.2 Pure bracket perturbation

If `e=0`, then `eps=D=0`. Every new interval `C subset J` is safe with at least the old reserve:

`p(t)-eta>=rho` for all `t in C`.

If `C` excludes `tau`, the true nominal reserve is in fact larger by at least

`(mu/2) dist(tau,C)^2`.

Thus endpoint motion is **zero debit** inside a common strong-convexity collar.

### 5.3 Uniform value-error lane

If a producer already has the stronger direct bound

`e(t)>=-eps_inf` for every `t in C`,

then no curvature argument is needed:

`p_tilde(t)-eta>=rho-eps_inf`.

Therefore the secant-cone lane is useful specifically when an anchor is accurate but the perturbation varies across the fiber; it should not replace a cheaper uniform value bound when one is already available.

### 5.4 Threshold perturbation

If the desired inequality changes from `p>=eta` to `p+delta_p >= eta+delta_eta`, set

`e = delta_p-delta_eta`.

The derivative/secanthood charge is unchanged by the constant `delta_eta`; only the anchor debit changes.

---

## 6. Theorem D — constrained minimizer displacement without solving the perturbed critical equation

Let `x` be any global minimizer of `p+e` on the new interval `C`, and let `y=clamp(tau,C)` be the nominal minimizer from Lemma A.

Assume only

`(e'(x))^2 <= D`.

Then

**(6.1)** `mu^2 (x-y)^2 <= D`.

### Proof

Because `y` minimizes differentiable convex `p` on the interval,

`p'(y)(x-y)>=0`.

Because `x` minimizes differentiable `p+e` on the interval, its one-dimensional first-order variational inequality with comparison point `y` gives

`(p'(x)+e'(x))(x-y)<=0`.

Strong monotonicity of `p'` gives

`(p'(x)-p'(y))(x-y)>=mu(x-y)^2`.

Combining,

`mu(x-y)^2 <= -e'(x)(x-y)`.

If `x=y`, (6.1) is trivial. Otherwise divide by `|x-y|>0`, then square:

`mu^2(x-y)^2 <= (e'(x))^2 <= D`.

QED.

### Why this is stronger than a root-displacement lemma

No assumption that `x` is an interior critical root is required. The result remains valid when the perturbed minimizer sits at a moved endpoint. It also does not require `p+e` itself to remain convex; any global minimizer obeys the interval first-order condition.

The perturbed algebraic critical equation therefore need not be solved merely to bound minimizer motion.

---

## 7. Theorem E — separate bracket motion from target-induced motion

Suppose the old interval is `[ell,r]` with `tau in [ell,r]`, and the new interval is `[a,b]`.

Assume an endpoint-motion square budget

`(a-ell)^2 <= H`,

`(b-r)^2 <= H`.

Then for `y=clamp(tau,a,b)`,

**(7.1)** `(y-tau)^2 <= H`.

Proof is by the three clamp branches. If `tau<a`, then `ell<=tau<a`, so

`0<a-tau<=a-ell`.

The right-exclusion branch is symmetric; the containing branch is zero.

Combining (7.1) with Theorem D gives the completely rational fallback

**(7.2)**

`mu^2 (x-tau)^2 <= 2D + 2mu^2 H`.

This follows from

`(x-tau)^2 <= 2(x-y)^2+2(y-tau)^2`.

For the same bracket (`H=0`, hence `y=tau`) one should use the sharper Theorem D directly rather than the factor-2 fallback.

The conceptual split is now exact:

- `H` measures **source/bracket location movement**;
- `D` measures **target slope movement**;
- reserve loss itself is governed by Theorem C and need not pay `H` at all when a common strong-convexity collar is available.

---

## 8. Theorem F — interior branch can be kept without rebuilding root matching

Sometimes downstream code wants to preserve the exact T-P5-276 INTERIOR branch rather than merely prove safety.

Let the new bracket be `C=[a,b]`. Assume the nominal derivative has certified endpoint margins

`p'(a) <= -sigma_L`,

`p'(b) >= sigma_R`,

with `sigma_L,sigma_R>0`.

Assume

`(e'(a))^2 <= D_L < sigma_L^2`,

`(e'(b))^2 <= D_R < sigma_R^2`.

Then

`(p+e)'(a)<0<(p+e)'(b)`.

No square root is required: `e'(a)^2<sigma_L^2` implies `-sigma_L<e'(a)<sigma_L`, and likewise on the right.

If in addition a curvature perturbation lower bound

`e''(t)>=-nu` on `C`

is available with

`0<=nu<mu`,

then

`(p+e)'' >= mu-nu >0`.

Hence the perturbed target again has a unique interior minimizer on `C`.

This gives a cheap **branch-stability lane**:

1. keep the old selected endpoints / new endpoint selectors;
2. prove two rational endpoint slope-margin inequalities;
3. prove one curvature-margin inequality;
4. use Theorem D for displacement and Theorem C for reserve.

No cubic/quartic root equation for the perturbed minimizer has to be solved unless its exact algebraic value is independently needed.

---

## 9. Sharpness of the reserve gate

The no-bonus gate

`D <= 2mu rho`

is sharp for the secant-cone relaxation.

Take

`p(t)=eta+rho+(mu/2)t^2`,

`tau=0`,

and the linear perturbation

`e(t)=-delta t`.

Then

`D=delta^2`,

`e(0)=0`,

and the perturbed unconstrained minimizer is

`t*=delta/mu`.

Its reserve is exactly

`p(t*)+e(t*)-eta = rho - D/(2mu)`.

Therefore:

- `D<2mu rho` gives strict positive reserve;
- `D=2mu rho` gives exact touching;
- `D>2mu rho` gives a genuine negative point whenever the interval contains `t*`.

A fully rational regression is

`mu=2`, `rho=1`, `p(t)=1+t^2`, `e(t)=-3t`, `D=9`.

The gate requires `D<=4` and fails. At `t=3/2`,

`p+e = 1 + 9/4 - 9/2 = -5/4`.

So the quadratic slope charge is not an artifact of the proof.

At the exact boundary, `e(t)=-2t`, `D=4`, and the perturbed minimum at `t=1` is exactly zero.

---

## 10. Exact obstruction — bracket expansion is not free outside every certified collar

The zero-debit bracket theorem must not be misread as saying that endpoint expansion is always safe from old interval data alone.

For any rational `h>0`, choose rational

`A > (1+h)^2 / h^3`

and define

`p_A(t)=t^2 + A(1-t)^3`.

On the old interval `[0,1]`,

`p_A''(t)=2+6A(1-t) >= 2`,

so the target is strongly convex there. Also

`p_A'(0)=-3A<0`,

`p_A'(1)=2>0`,

so there is a unique interior minimizer.

For `A>=1`, the old interval even has the explicit positive reserve

`p_A(t)>=1/8`:

- on `[0,1/2]`, `A(1-t)^3>=1/8`;
- on `[1/2,1]`, `t^2>=1/4`.

But at the expanded endpoint `1+h`,

`p_A(1+h)=(1+h)^2-Ah^3<0`.

Thus an arbitrarily small endpoint expansion can expose a violation if no convexity/value collar outside the old fiber has been certified.

This is a **source/collar certificate obstruction**, not a physical impossibility theorem. For a concrete known polynomial one can of course certify a larger collar directly.

---

## 11. Optional coarse collar lane when strong convexity is unavailable outside the old interval

Suppose only the old interval safety

`p>=eta+rho` on `I=[ell,r]`

is known. If a new interval lies within Hausdorff distance `h` of `I`, and a collar derivative bound

`|p'|<=G`

is independently certified on the connecting collar, then projection to `I` gives

`p(t)>=eta+rho-Gh`

on the new interval.

A uniform target-value perturbation `e>=-eps_inf` then gives the coarse sufficient gate

`Gh+eps_inf <= rho`.

This lane is deliberately separated from Theorem C:

- the **strong-convexity collar** charges zero for bracket motion and quadratically for anchored target slope error;
- the **Lipschitz collar** pays a first-order `Gh` endpoint-motion debit.

A dispatcher should choose the stronger available packet rather than silently assume one from the other.

---

## 12. Suggested exact checker packet

For each same-key outer cell/fiber, the source-facing producer can serialize:

1. nominal `mu>0`, `rho`;
2. a collar `J` containing the new bracket and the old critical point `tau`;
3. proof/certificate of `p''>=mu` on `J`;
4. the new selected interval `[a,b]` and same-key inclusion `[a,b] subset J`;
5. clamp branch for `y=clamp(tau,a,b)`;
6. anchor lower bound `e(y)>=-eps`;
7. secant-cone coefficient `D>=0`, preferably from `(e')^2<=D` on the relevant interval;
8. optional bracket bonus `S<= (y-tau)^2`;
9. scalar checks
   - `R2=2(rho-eps)+mu S >=0`,
   - `D<=mu R2`;
10. only if the exact interior branch object is required: endpoint derivative margins and optional curvature perturbation `nu<mu`.

The consumer can then prove safety without reconstructing the algebraic critical-root atlas.

For rational `mu,rho,eps,D,S`, the decisive reserve checks are rational scalar inequalities. Algebraic machinery is needed only to justify source selectors / anchor evaluations that are algebraic in the actual packet, not for the perturbation theorem itself.

---

## 13. Lean-oriented decomposition

A minimal formalization can avoid real-algebraic geometry entirely at first.

Suggested theorem leaves:

1. `strongConvex_deriv_lower_bound`
   - `p''>=mu` -> strong monotonicity of `p'` and quadratic support inequality.

2. `strongConvex_clamp_is_intervalMin`
   - `p' tau=0`, `mu>0` -> `clamp tau a b` is nominal constrained minimizer.

3. `strongConvex_clamp_quadratic_support`
   - for `y=clamp tau a b`, `p t>=p y + mu/2*(t-y)^2` on the interval.

4. `derivSqBound_implies_secantSqBound`
   - MVT specialization for differentiable scalar `e`.

5. `fractionFree_secantCone_nonneg`
   - scalar core using the identity
     `(2R+mu*s^2)^2-4D*s^2=(2R-mu*s^2)^2+4*(2*mu*R-D)*s^2`.

6. `strongConvex_perturbation_reserve_fractionFree`
   - Theorem C.

7. `constrainedMinimizer_perturbation_displacementSq`
   - Theorem D.

8. `endpointShift_clampDistanceSq`
   - Theorem E first half.

9. `combinedBracketTarget_displacementSq`
   - `mu^2*(x-tau)^2 <= 2D+2mu^2 H`.

10. `interiorBranch_preserved_of_derivSq_margin`
   - endpoint derivative-square margins preserve strict signs.

The exact source/algebraic endpoint layer should call these leaves after T-P5-270/T-P5-276 has supplied the needed ordered endpoint facts; the scalar perturbation theorem should not itself depend on a Thom encoding implementation.

---

## 14. Semantic boundaries

This child proves a mathematical transport theorem only.

It does **not** justify any of the following shortcuts:

- using a reserve `rho` from one source key with perturbation coefficients from another;
- treating a changed chart or metric as a scalar `e` without proving the pullback identity;
- assuming the new bracket lies in the old strong-convexity region merely because its endpoints are numerically close;
- deriving whole-cell, trajectory, FD-halo, or reference-halo coverage from pointwise interval safety;
- replacing Float64/libm error by an exact-real coefficient perturbation without enclosure;
- declaring physical FAIL merely because the scalar gate is not met.

Failure of

`D<=mu(2(rho-eps)+mu S)`

means only that this anchored secant-cone reserve packet is insufficient. The actual target may still be safe because of signed higher-order structure, a smaller realized error graph, endpoint exclusion, or a direct algebraic certificate.

Conversely, the bracket-expansion counterexample means a new source interval outside every certified collar requires new target/domain information before PASS can be transported.

---

## 15. Remaining obligations

Still open:

1. identify the actual P5 same-key nominal target `p`, threshold `eta`, selected minimizer reserve `rho`, and new perturbation `e`;
2. certify an actual strong-convexity margin `mu` on a collar that contains every perturbed source fiber being transported;
3. bind the moved endpoints and clamp branch to the true source predicate, including strict/weak/open/empty semantics;
4. derive an actual rational `D` for coefficient / FD / evaluator perturbations, or a direct secant-cone witness;
5. bind `e(y)` to the same selected anchor and obtain `eps` without floating root substitution;
6. exploit any genuine positive bracket-exclusion bonus `S` only after its same-key ordering proof;
7. if downstream requires the exact perturbed interior root, certify the branch-stability margins from Theorem F;
8. state/trajectory realization for any negative counterexample;
9. whole-cell/flowpipe/FD-halo/reference-halo coverage;
10. Float64/libm/interval enclosure;
11. Lean/kernel formalization;
12. independent validation by 封不觉;
13. admission, registry mutation, and P5/P8/M4 propagation.

---

## 16. Next nonduplicative mathematical seam

The next abstract extension should **not** be another generic root solver.

Two genuinely disjoint continuations remain:

1. **structured perturbation graph lane** — when the scalar secant cone `z^2<=D s^2` is too coarse, preserve the actual polynomial relation between `z=e(t)-e(y)` and `s=t-y` (for example a signed quadratic/cubic remainder) and derive a lower-degree exact reserve polynomial instead of paying the sharp but direction-forgetting `D/(2mu)` debit;
2. **actual-source lane** — instantiate `mu,rho,e,D` on a real P5 quartic/FD packet and test whether the perturbation theorem actually avoids an atlas rebuild.

The first lane is worthwhile only if an actual reserve packet fails the scalar gate; otherwise source binding has higher value than further abstract generalization.
