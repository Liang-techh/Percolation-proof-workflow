---
kind: review_result
review_id: review-T-P5-229-bounded-flat-fiber-support-closure-kuangmanmozun-20260910T0831Z
task_id: T-P5-229-BOUNDED-FLAT-FIBER-SUPPORT-CLOSURE
reviewer: 狂蛮魔尊
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T08:31:00Z
claim_commit: 84107c766579ef3f5b5d76b34dac39db223a2f56
inspected_commit: 2350a54641b43efe39203530f04279306b29af47
upstream_commits:
  - db655d40ee23d1c71f03f46eb20d112d0553b2fa  # T-P5-228 flat-fiber radical annihilation
  - 068792f0a320dfe3195ef2bfdf1081506b5b4db0  # T-P5-227 quotient/Schur commutation
  - 6a10ef29433a4dd050d593d8053383f4ba7fd204  # T-P5-226 higher-corank maximal-anchor Schur
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_bounded_flat_fiber_support_theorem; add_box_and_fraction_free_ellipsoid_specializations; add_polytope_dual_certificate; add_gauge_radius_scaling_dispatch
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic/convex support algebra only; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-229 — bounded flat-fiber support closure and gauge-radius scaling law

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-228 proved that an exactly flat, genuinely free two-sided gauge must be bilinearly radical against every consumed endpoint representative. It also correctly warned that a merely bounded fiber does not force radicality at a fixed representative.

This child closes the bounded-fiber inequality seam exactly. The key observation is that once

`G^T Q G = 0`,

all residual gauge dependence is linear, so the whole bounded-fiber problem is a support-function problem, not a new quadratic optimizer:

`sup_{alpha in K} (w+G alpha)^T Q (w+G alpha)`

`= w^T Q w + 2 h_K(G^T Q w)`.

This yields sharp closed forms for boxes, a square-root-free rational certificate for rational ellipsoids, and an LP-dual certificate for rational polytopes.

There is also a stronger structural result useful near the origin: if the admissible gauge radius does not shrink at least linearly with the physical amplitude, then boundedness does **not** save a nonzero cross term. Uniform sign validity on scaled representatives forces radicality. Thus the correct source-level discriminator is not simply `bounded` versus `unbounded`; it is the asymptotic ratio

`gauge radius / physical amplitude`.

No actual P5 source fiber, same-key state/tangent packet, trajectory/cell coverage, Float64 enclosure, Lean/kernel receipt, independent validation by 封不觉, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Let `Q=Q^T` be a real symmetric matrix, let `G` be a gauge/lift matrix, and let `w` be one consumed endpoint representative. Define

`q(x) := x^T Q x`,

`q0 := q(w)`,

`b := G^T Q w`.

Assume the **flat-gauge gate**

`G^T Q G = 0`.

Let `K` be the admissible set of gauge parameters. Its support function is

`h_K(b) := sup_{alpha in K} b^T alpha`.

The intended endpoint sign convention here is `q <= 0`.

---

## 2. T229-A — exact support-function closure

### Theorem A

For every `alpha`, flatness gives

`q(w+G alpha) = q0 + 2 b^T alpha`.

Therefore, whenever `h_K(b)` is finite,

**`sup_{alpha in K} q(w+G alpha) = q0 + 2 h_K(b)`.**

Consequently,

**`q(w+G alpha) <= 0 for all alpha in K`**

if and only if

**`q0 + 2 h_K(b) <= 0`.**

### Proof

Expand:

`q(w+G alpha)`

`= w^TQw + 2 alpha^T G^TQw + alpha^T G^TQG alpha`

`= q0 + 2 b^T alpha`.

Taking the supremum over `K` gives the formula immediately. QED.

### Consequence A1 — T-P5-228 recovered as the infinite-radius limit

If `K` contains arbitrarily large multiples of both signs of every direction in a subspace `L`, then finiteness of the support term forces `b` to annihilate `L`. For a genuine full two-sided gauge space this is exactly `G^TQw=0`, recovering T-P5-228.

### Consequence A2 — zero base margin

If `0 in K`, `q0=0`, and `K` is centrally symmetric, safety implies `h_K(b)=0`. If `span(K)=R^g`, this forces `b=0` even though `K` is bounded.

So a bounded fiber can carry a nonzero cross term only when there is strictly negative base margin available to pay for it.

---

## 3. T229-B — exact weighted-box formula

Let

`K_box = {alpha : |alpha_i| <= T_i}`, `T_i>=0`.

Then

`h_Kbox(b) = sum_i T_i |b_i|`,

because each coordinate can independently choose the maximizing sign.

Hence the exact necessary-and-sufficient bounded-fiber gate is

**`q0 + 2 sum_i T_i |b_i| <= 0`.**

No Young inequality and no norm relaxation is needed.

### Why separate per-axis tests are unsafe

It is not enough to prove, for each `i`,

`q0 + 2 T_i |b_i| <= 0`.

Those tests reuse the same negative base margin multiple times.

Exact rational counterexample:

`q0=-1`, `T_1=T_2=1`, `b_1=b_2=2/5`.

Each one-axis test gives

`-1 + 4/5 = -1/5 <=0`,

but the true two-dimensional box maximum is

`-1 + 2(2/5+2/5) = 3/5 >0`.

Thus coordinatewise acceptance would produce a false PASS. The correct box checker must aggregate the absolute cross debits before consuming the margin.

### Weighted simplex interpretation

If `q0<0`, define the available cross budget `m=-q0/2`. Safety is exactly

`sum_i T_i |b_i| <= m`.

So the flat bounded-gauge problem has the same resource-allocation geometry as the multi-support debit budget in T-P5-206: independent local allowances share one common scalar margin.

---

## 4. T229-C — rational ellipsoid gate without square roots

Let

`K_ell = {alpha : alpha^T R alpha <= T^2}`,

where `R=R^T>0` and `T>=0`.

The support function is

`h_Kell(b) = T sqrt(b^T R^{-1} b)`.

Therefore exact safety is

`q0 + 2 T sqrt(b^T R^{-1}b) <=0`.

For rational checking, set

`d := det(R) >0`,

`H := adj(R)`,

so `R^{-1}=H/d`. Since `R>0`, also `H>0`. Then the square-root condition is exactly equivalent to the pair

**`q0 <= 0`,**

**`d q0^2 >= 4 T^2 b^T H b`.**

This is a purely rational polynomial certificate when `R,T,q0,b` are rational.

### Proof of equivalence

Write `s=b^THb>=0`. The support inequality becomes

`q0 + 2T sqrt(s/d) <=0`.

It implies `q0<=0`. Under that sign gate, moving the square-root term to the other side and squaring is equivalence-preserving:

`2T sqrt(s/d) <= -q0`

iff

`4T^2 s <= d q0^2`.

QED.

### Exact rational PASS regression

Take

`R=diag(4,9)`, `T=1`, `b=(2,3)`, `q0=-3`.

Then

`d=36`, `H=diag(9,4)`, `b^THb=72`.

The rational gate reads

`36*9 =324 >= 4*72=288`,

so the whole ellipsoidal gauge fiber is safe. Analytically the exact maximum is `-3+2 sqrt(2)<0`.

### Exact rational FAIL regression

Keep `R,T,b` but set `q0=-2`. Then

`36*4=144 <288`,

and indeed the exact maximum is `-2+2 sqrt(2)>0`.

This shows the fraction-free gate detects the correct threshold without introducing an algebraic-number object into the checker.

---

## 5. T229-D — rational polytope gate by LP duality

Let

`K_poly = {alpha : F alpha <= g}`

be nonempty and compact. Then

`h_Kpoly(b) = max {b^T alpha : F alpha<=g}`.

By finite-dimensional LP strong duality,

`h_Kpoly(b) = min {g^T lambda : lambda>=0, F^T lambda=b}`.

Therefore the flat-fiber sign condition is equivalent to existence of a dual certificate `lambda` satisfying

**`lambda>=0`,**

**`F^T lambda=b`,**

**`q0 + 2 g^T lambda <=0`.**

For rational `F,g,b,q0`, a feasible exact rational dual witness can be used directly by the checker. This is the bounded-gauge analogue of T-P5-199's polyhedral support transport, but here the target objective is exactly the flat-fiber cross block `b=G^TQw`.

Important boundary: if `K_poly` is unbounded, one must first verify finite support in direction `b`; otherwise the correct conclusion is an unbounded positive-debit obstruction rather than LP-certificate failure.

---

## 6. T229-E — scaling law for bounded gauge fibers near a conic base

The phrase `bounded gauge` is not by itself enough to decide whether a nonzero cross block can survive near the origin.

Fix a centrally symmetric compact set `K` with `0 in K`. Along a physical base ray, consider the family

`x(t,u) = t w + G (rho(t) u)`,

where

`t>0`, `u in K`, `rho(t)>=0`.

Under `G^TQG=0`, Theorem A gives

`sup_{u in K} q(x(t,u))`

`= t^2 q0 + 2 t rho(t) h_K(b)`.

For `t>0`, safety is therefore exactly

**`t q0 + 2 rho(t) h_K(b) <=0`.**

Equivalently, after division by `t`,

**`q0 + 2 [rho(t)/t] h_K(b) <=0`.**

This ratio yields a sharp three-regime dispatcher.

### Regime E1 — superlinear relative gauge width forces radicality

Suppose sign validity holds for a sequence `t_n ->0+` and

`rho(t_n)/t_n -> +infinity`.

Then necessarily

`h_K(b)=0`.

If `span(K)=R^g`, central symmetry implies `b=0`.

Proof: otherwise `h_K(b)>0`, and the positive term `2[rho(t_n)/t_n]h_K(b)` diverges while `q0` is fixed, contradicting the inequality.

A constant absolute gauge radius `rho(t)=rho0>0` is in this regime. Thus **a uniformly thick bounded gauge tube around arbitrarily small physical states still forces the same cross-radicality as a free gauge.**

### Regime E2 — linearly shrinking gauge gives a finite exact budget

If

`rho(t)=c t`, `c>=0`,

then safety at every scale is exactly

**`q0 + 2 c h_K(b) <=0`.**

Nonzero cross terms are allowed when the base quadratic margin pays for them.

Exact counterexample showing radicality cannot be demanded here:

`q0=-2`, `K=[-1,1]`, `b=1`, `rho(t)=t`.

Then

`sup q = -2t^2 + 2t^2 =0`

for every `t`, even though `b!=0`.

### Regime E3 — faster-than-linear shrinking gauge is locally lower order

If

`rho(t)/t ->0`,

then the cross term is asymptotically negligible relative to the base quadratic term. In particular, if `q0<0`, there exists a sufficiently small neighborhood in which any fixed finite `h_K(b)` is safe.

Example: `q0=-1`, `K=[-1,1]`, `b=1`, `rho(t)=t^2`. Then

`sup q = -t^2 + 2t^3 = t^2(-1+2t) <=0`

for `0<t<=1/2`, despite `b!=0`.

### Power-law corollary

For `rho(t)=t^p`:

- `p<1`: nonzero cross term is impossible under sign validity arbitrarily close to zero;
- `p=1`: exact finite support budget;
- `p>1`: nonzero cross term can survive locally when `q0<0`.

This gives the source lane a concrete semantic question: how does the admissible lift ambiguity scale with the physical tangent/state amplitude?

---

## 7. T229-F — partial-dimensional fibers

If `K` lies in a proper subspace `L`, then `h_K(b)=0` only forces the projection of `b` onto `L` to vanish. It does **not** imply the full vector `b=0`.

Therefore any radicality conclusion must be relative to the actual span of admissible gauge changes. A numerical nullspace basis larger than the source-realizable fiber would overstate the theorem.

For a box with some `T_i=0`, the exact condition only consumes coordinates with positive radius. Under the E1 scaling regime, only those cross components are forced to vanish.

---

## 8. Formalizable theorem statements

The following theorem leaves are small and independent of quotient types.

### Leaf 1 — support reduction

`flatFiber_sup_eq_base_add_two_support`

Hypotheses:

- `Q` symmetric;
- `G^T Q G=0`;
- finite support of `K` in direction `G^TQw`.

Conclusion:

`sup_{a in K} quad Q (w+G a) = quad Q w + 2 support K (G^TQw)`.

### Leaf 2 — weighted box

`flatFiber_box_nonpos_iff`

Conclusion:

`forall a, (forall i, |a_i|<=T_i) -> quad Q (w+Ga)<=0`

iff

`quad Q w + 2 sum_i T_i*| (G^TQw)_i | <=0`.

### Leaf 3 — fraction-free ellipsoid

`flatFiber_ellipsoid_nonpos_iff_fractionFree`

For rational/SPD `R`, `d=det R`, `H=adj R`:

safety iff

`q0<=0` and `d*q0^2 >= 4*T^2*(b^T H b)`.

### Leaf 4 — polytope dual witness

`flatFiber_polytope_dual_certificate`

If `lambda>=0`, `F^Tlambda=b`, and `q0+2g^Tlambda<=0`, then every `alpha` with `Falpha<=g` satisfies `q(w+Galpha)<=0`.

The converse can be separated and imported from standard LP/Farkas infrastructure if desired.

### Leaf 5 — scaling radicality

`flatFiber_radius_ratio_unbounded_imp_cross_zero`

If the base ray/fiber is sign-valid along `t_n->0`, `rho(t_n)/t_n->infinity`, and `K` is centrally symmetric and spans the gauge coordinate space, then `G^TQw=0`.

A weaker span-relative statement should be proved first.

No pseudoinverse, eigensystem, generic nonlinear optimizer, or semialgebraic decomposition is needed for these leaves.

---

## 9. Checker/source dispatcher suggested by this child

For an exactly flat gauge block `G^TQG=0`:

1. identify the actual admissible gauge-parameter set `K` and whether it is fixed, state-dependent, or scale-dependent;
2. for a fixed bounded fiber, compute the exact support debit `h_K(G^TQw)` by the narrowest available route:
   - weighted absolute sum for a box;
   - fraction-free determinant/adjugate inequality for a rational ellipsoid;
   - rational LP dual witness for a rational polytope;
3. consume this debit **once** against the base margin `-q0/2`; do not reuse that margin independently per gauge coordinate;
4. if the physical base is scalable toward zero, inspect `rho(t)/t`:
   - unbounded ratio => demand span-relative radicality;
   - finite nonzero ratio => use the exact support budget;
   - vanishing ratio => cross term is locally lower order, but global state-domain checks remain necessary;
5. if `G^TQG` is not zero, return to the signed-Schur dispatcher of T-P5-224/225/226 rather than applying this flat theorem.

This cleanly separates three mathematically distinct objects that should not be conflated in source binding: a free gauge, a uniformly thick bounded fiber, and a fiber whose width shrinks with state amplitude.

---

## 10. Failure/obstruction summary

This child gives four explicit failure guards.

1. **Per-axis margin reuse is unsound.** The two-dimensional rational box example passes every one-axis test but fails the true joint box.
2. **Squaring an ellipsoid inequality without the sign gate `q0<=0` is unsound.** The fraction-free quadratic inequality alone loses the direction of the original square-root inequality.
3. **`bounded` does not mean `cross term allowed`.** A fixed nonzero radius near a conic origin forces radicality because the linear cross term dominates the quadratic base at small scale.
4. **`bounded` also does not mean `radicality required`.** If the gauge radius shrinks linearly or faster, explicit nonzero-cross PASS examples exist.

These are mathematical semantics, not implementation preferences.

---

## 11. Remaining boundaries and next child

Still open and not upgraded here:

- actual same-key P5 face/tangent lift map `G`;
- proof that the actual debit satisfies `G^TQG=0`;
- the actual source-realizable gauge set `K` and its scaling law `rho(t)`;
- state/cell/tube and trajectory coverage;
- Float64/interval enclosure semantics for numerical source matrices;
- Lean/kernel compilation;
- independent validation by 封不觉;
- admission/registry and P5/P8/M4 parent closure.

A natural next mathematical seam is the **curved bounded-fiber trust-region branch** `A=G^TQG<0`, where the exact maximum of

`q0 + 2 b^T alpha + alpha^T A alpha`

over a rational box/ellipsoid must be compared with the flat support bound. The negative-definite unconstrained branch should admit an exact Schur completion; the boundary-active branch becomes a genuine trust-region/KKT problem and needs a careful rational certificate rather than a false flat reduction.