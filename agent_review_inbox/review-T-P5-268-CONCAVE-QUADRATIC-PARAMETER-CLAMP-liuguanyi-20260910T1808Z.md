---
kind: review_result
review_id: review-T-P5-268-concave-quadratic-parameter-clamp-liuguanyi-20260910T1808Z
task_id: T-P5-268-CONCAVE-QUADRATIC-PARAMETER-CLAMP
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T18:08:00Z
claim_commit: 0b82f8f46d35b0c6e130fdde08a9749367c8ebfe
inspected_commit: e30ed917daeb5fa5ad46450b7b01b1110990749b
upstream_commits:
  - 3f2f9004e7fe2c1a0f3fc315f59d33a2ed4dbde5  # T-P5-267 parametric radial box certificate
  - d062e528bc248cd24f09973dcde7cfcf7c00ffae  # T-P5-266 zero-margin radial Sturm certificate
  - 913ed31d66c77016e82fe2371d3734b033e76e5f  # T-P5-265 rational Bernstein radial interval certificate
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_concave_quadratic_clamp_theorem; add_fraction_free_left_right_interior_identities; add_piecewise_interval_Slemma_multiplier; add_exact_reserve_shift; add_univariate_Sturm_sign_atlas_dispatcher; preserve_outer_box_and_source_realizability_boundaries
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact polynomial expansion of the three branch identities and two gluing identities; finite-dimensional convexity calculus; exact rational Sturm/sign-cell construction; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-268 — Concave quadratic parameter clamp with fraction-free branch certificates

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-267 proves that separately-convex parameter dependence reduces exactly to box vertices, but it deliberately leaves the first genuinely interior maximizer open. This child closes the one-parameter concave-quadratic branch.

For

`A(q,s)=A0(q)+A1(q)s-A2(q)s^2`, `s in [a,b]`,

with rational polynomial coefficients in the radial variable `q`, it is not necessary to introduce a bivariate optimizer or floating root finder. After proving only the non-strict concavity gate

`A2(q)>=0`,

the exact parameter maximum is determined by two derivative-sign polynomials. The interior branch has a rational expression `A0+A1^2/(4A2)`, but the actual safety test can be written without division as one polynomial inequality.

The stronger result is a three-branch family of **fraction-free identities**. They are exact interval S-lemma certificates and glue continuously at the clamp switches. Together with a one-dimensional Sturm sign atlas, they give a finite exact decision procedure over the full rational `(q,s)` rectangle. Every genuine box failure admits an exact rational witness `(q,s)`.

No deployed P5 coefficient family, same-key source realization, true parameter fiber, state realization of `q`, trajectory/cell/FD-halo coverage, Float64 semantics, Lean/kernel proof, independent verification, admission, registry mutation, or parent closure is claimed.

---

## 1. Setup

Let

`I=[0,R]`, `R in Q`, `R>0`,

`a,b,K in Q`, `a<b`,

and

`A0,A1,A2 in Q[q]`.

Define

**(1.1)** `A(q,s)=A0(q)+A1(q)s-A2(q)s^2`.

The desired upper bound is

**(1.2)** `A(q,s)<=K` for every `(q,s) in I x [a,b]`.

It is cleaner to work with the debit polynomial

**(1.3)**

`p(q,s):=K-A(q,s)`

`=C(q)-A1(q)s+A2(q)s^2`,

where

**(1.4)** `C(q):=K-A0(q)`.

Assume throughout the main theorem that

**(1.5)** `A2(q)>=0` on `I`.

This is intentionally **non-strict**. The zero-curvature affine degeneration is handled exactly rather than excluded by an artificial denominator gate.

Set

**(1.6)** `L:=b-a>0`,

**(1.7)** `g_a(q):=A1(q)-2a A2(q)`,

**(1.8)** `g_b(q):=A1(q)-2b A2(q)`.

Because

**(1.9)** `g_a-g_b=2L A2>=0`,

the two clamp derivatives are ordered for every `q`.

Finally define the three fraction-free reserve polynomials

**(1.10)** `E_a(q):=p(q,a)=C-aA1+a^2 A2`,

**(1.11)** `E_b(q):=p(q,b)=C-bA1+b^2 A2`,

**(1.12)** `F(q):=4A2 C-A1^2`.

All of these lie in `Q[q]`.

---

## 2. Theorem A — exact clamped minimizer without assuming strict curvature

For each fixed `q in I`, under `A2(q)>=0`, exactly one of the following deterministic branches applies if the tests are evaluated in order.

### LEFT branch

If

**(2.1)** `g_a(q)<=0`,

then

`partial_s p(q,a)=2aA2-A1=-g_a>=0`.

Since `p(q,.)` is convex, its derivative is nondecreasing. Hence `p` is nondecreasing on `[a,b]` and

**(2.2)** `min_{s in [a,b]} p(q,s)=E_a(q)`.

Equivalently,

**(2.3)** `max_{s in [a,b]} A(q,s)=A(q,a)`.

### RIGHT branch

Suppose `g_a(q)>0`. If

**(2.4)** `g_b(q)>=0`,

then

`partial_s p(q,b)=-g_b<=0`.

Convexity implies `partial_s p<=0` throughout `[a,b]`, so

**(2.5)** `min_{s in [a,b]} p(q,s)=E_b(q)`.

Equivalently,

**(2.6)** `max_{s in [a,b]} A(q,s)=A(q,b)`.

### INTERIOR branch

The remaining case is

**(2.7)** `g_a(q)>0` and `g_b(q)<0`.

Then (1.9) gives

`2L A2=g_a-g_b>0`,

so **strict positivity of `A2` follows automatically on this branch**. No independent division-safety assumption is needed.

The unique stationary point is

**(2.8)** `s_*(q)=A1(q)/(2A2(q))`,

and the inequalities in (2.7) are exactly

**(2.9)** `a<s_*(q)<b`.

Therefore

**(2.10)**

`min_{s in [a,b]} p(q,s)=F(q)/(4A2(q))`,

and

**(2.11)**

`max_{s in [a,b]} A(q,s)=A0(q)+A1(q)^2/(4A2(q))`.

### Degenerate overlap

If both endpoint predicates `g_a<=0` and `g_b>=0` hold, (1.9) forces

`g_a=g_b=0`, `A2=0`, `A1=0`.

Then `A(q,s)=A0(q)` is independent of `s`, and `E_a=E_b=C`. The deterministic priority `LEFT -> RIGHT -> INTERIOR` therefore has no ambiguity and does not lose any case.

---

## 3. Theorem B — exact pointwise safety criterion

Under (1.5), for a fixed `q`, the bound

**(3.1)** `A(q,s)<=K` for every `s in [a,b]`

is equivalent to the branch-selected scalar condition

**(3.2)**

- if `g_a<=0`: `E_a>=0`;
- else if `g_b>=0`: `E_b>=0`;
- else: `F>=0`.

The interior branch is fraction-free because `A2>0` there, so

`F>=0`

is exactly equivalent to

`F/(4A2)>=0`.

Thus the first genuine interior parameter maximizer still reduces to **univariate rational polynomial signs**.

---

## 4. Theorem C — three fraction-free interval certificates

Let

**(4.1)** `h(s):=(s-a)(b-s)`.

On `[a,b]`, `h(s)>=0`.

Direct polynomial expansion gives the following exact identities.

### LEFT identity

**(4.2)**

`L p(q,s)`

`=(-g_a) h(s) + L E_a + (L A2-g_a)(s-a)^2`.

If `g_a<=0`, `A2>=0`, and `E_a>=0`, every term on the right is nonnegative because

`L A2-g_a=L A2+(-g_a)>=0`.

Therefore `p>=0` on `[a,b]` with no division.

### RIGHT identity

**(4.3)**

`L p(q,s)`

`=g_b h(s) + L E_b + (L A2+g_b)(s-b)^2`.

If `g_b>=0`, `A2>=0`, and `E_b>=0`, every term is nonnegative.

### INTERIOR identity

**(4.4)**

`4A2 p(q,s)=(2A2 s-A1)^2+F`.

On the interior branch `A2>0`, so `F>=0` proves `p>=0` globally in `s`, and in particular on `[a,b]`.

These identities are stronger than an optimizer formula: they are directly checkable algebraic certificates suitable for a rational/Lean layer.

---

## 5. Exact piecewise interval S-lemma multiplier

The three identities also expose a lossless one-constraint S-lemma multiplier.

The interval is represented by

`h(s)=(s-a)(b-s)>=0`.

Define the piecewise multiplier

**(5.1)**

`lambda(q)=`

- `-g_a/L` on the LEFT branch;
- `g_b/L` on the RIGHT branch;
- `0` on the INTERIOR branch.

Every selected multiplier is nonnegative.

For LEFT,

**(5.2)**

`p-lambda h = E_a + (A2+lambda)(s-a)^2`.

For RIGHT,

**(5.3)**

`p-lambda h = E_b + (A2+lambda)(s-b)^2`.

For INTERIOR, `lambda=0` and (4.4) is the completed-square certificate.

Hence whenever the branch reserve in (3.2) is nonnegative,

**(5.4)** `p(q,s)-lambda(q)h(s)>=0` for every real `s`.

Because `lambda h>=0` on the interval, this proves `p>=0` there.

Conversely, the branch reserve is the exact interval minimum, so the construction is lossless. Thus the clamped optimizer and the one-constraint interval S-lemma are not merely compatible: this gives an explicit exact multiplier realizing their equivalence.

No pseudoinverse, square root, SDP solver, or floating KKT solve is involved.

---

## 6. Switch-gluing identities

The three branch certificates do not leave an uncovered seam at a clamp transition. Exact expansion gives

**(6.1)** `F=4A2 E_a-g_a^2`,

**(6.2)** `F=4A2 E_b-g_b^2`.

Therefore, at a nondegenerate LEFT/INTERIOR switch `g_a=0`,

**(6.3)** `F=4A2 E_a`.

At a nondegenerate INTERIOR/RIGHT switch `g_b=0`,

**(6.4)** `F=4A2 E_b`.

When the switch is genuinely adjacent to the interior branch, `A2>0`, so the endpoint and interior safety signs agree exactly.

The only case where `A2=0` and both derivative gates vanish is the constant-in-`s` degeneration already handled by the LEFT priority. Therefore no division-by-zero hole exists at the branch seams.

---

## 7. Exact strict-reserve transport

Suppose a downstream Lyapunov layer needs not merely `p>=0` but a rational vertical reserve

**(7.1)** `p(q,s)>=eta`, `eta in Q`, `eta>=0`.

Replace `p` by

`p_eta:=p-eta`.

The derivative gates `g_a,g_b` do not change. Only the reserve polynomials shift:

**(7.2)** `E_a -> E_a-eta`,

**(7.3)** `E_b -> E_b-eta`,

**(7.4)** `F -> F-4A2 eta`.

Hence the exact branch conditions for a common reserve `eta` are

**(7.5)**

- LEFT: `E_a>=eta`;
- RIGHT: `E_b>=eta`;
- INTERIOR: `F>=4A2 eta`.

This is useful for T-P5-243-style perturbation accounting: a producer can export a rational reserve without solving for the exact global maximizer. If a strict reserve exists, rational `eta` can be chosen below it; zero-margin branches remain valid with `eta=0` and must not be assigned invented slack.

---

## 8. Complete finite exact dispatcher over the radial interval

The remaining issue is that the active clamp branch can vary with `q`. This still does not require a bivariate solver.

### 8.1 Concavity gate

First decide

**(8.1)** `A2(q)>=0` on `[0,R]`.

This is exactly a univariate rational-polynomial nonnegativity problem and is decision-complete by T-P5-266. T-P5-265 remains the fast strict-margin Bernstein path.

If (8.1) fails, this child is **not applicable** on the whole interval. That is not a physical FAIL: on regions with `A2<0`, the original `A` is convex in `s` and T-P5-267's endpoint theorem is the natural lane.

### 8.2 Sign atlas

Assume (8.1). Form the finite family

**(8.2)** `{g_a,g_b,E_a,E_b,F}`,

removing members that are identically zero.

Let

**(8.3)** `Psi=sqfree(product of all nonzero members)`.

Use exact rational Sturm root isolation for `Psi` on `(0,R)`. This produces finitely many ordered real roots and hence finitely many open cells between consecutive roots and the rational endpoints.

On every open cell:

1. choose any rational sample `q0` in the cell;
2. evaluate the exact rational signs of `g_a(q0),g_b(q0),E_a(q0),E_b(q0),F(q0)`;
3. since no member of (8.2) has a root in the cell, every nonzero sign is constant throughout the cell;
4. select LEFT/RIGHT/INTERIOR by Theorem A and require the corresponding reserve sign from Theorem B.

No algebraic root value has to be converted to floating point.

### 8.3 Why point cells need no floating/algebraic evaluation

Define

**(8.4)** `m(q):=min_{s in [a,b]} p(q,s)`.

Because `p` is continuous on the compact product, `m` is continuous. Explicitly,

`|m(q)-m(q')| <= sup_{s in [a,b]} |p(q,s)-p(q',s)|`,

and the right side tends to zero with `q'->q`.

Therefore, if every adjacent open sign cell has `m>=0`, every isolated internal root point also has `m>=0` by continuity. Only the rational endpoints `q=0,R` need direct pointwise checks.

This gives a finite exact dispatcher using only rational polynomial arithmetic, squarefree/gcd operations, Sturm root isolation, and rational sign evaluations.

### 8.4 Bernstein fast path

Before constructing the full Sturm atlas, a checker may try the cheaper T-P5-265 path on globally valid branch packets, for example:

- prove `-g_a>=0` globally and then `E_a>=0` globally;
- prove `g_b>=0` globally and then `E_b>=0` globally;
- when a separate strict `A2>0` certificate is available, prove `g_a>=0`, `-g_b>=0`, and `F>=0` globally for an all-interior-or-boundary branch.

Failure of these fast packets only triggers the Sturm atlas; it is not mathematical failure.

---

## 9. Constructive rational failure witness

The dispatcher is constructive for the declared full rectangle.

If an open LEFT sign cell fails, its rational sample `q0` has `E_a(q0)<0`; then

**(9.1)** `(q0,s0)=(q0,a)`

is an exact rational witness with `A(q0,a)>K`.

If an open RIGHT cell fails, use

**(9.2)** `(q0,s0)=(q0,b)`.

If an open INTERIOR cell fails, then `q0` is rational, `A2(q0)>0`, and

**(9.3)** `s0=A1(q0)/(2A2(q0)) in (a,b)`

is rational. Since `F(q0)<0`,

**(9.4)** `p(q0,s0)=F(q0)/(4A2(q0))<0`.

A negative minimum cannot occur only at an isolated internal `q` because `m(q)` is continuous. Endpoint failure is also witnessed at rational `q=0` or `R`. Hence every failure of the declared polynomial box admits an exact rational `(q,s)` counterexample.

This is a **box-level** witness. It becomes a physical/source FAIL only after the workflow separately proves that the same-key source actually realizes that `(q,s)` pair (or an equivalent state witness).

---

## 10. Exact regressions / negative controls

### 10.1 Endpoint-only checking is unsound in the concave branch

Take `[a,b]=[0,1]`, `K=0`,

`A(s)=4s-4s^2`.

Then `A2=4`, `A1=4`, and both endpoint values are `0`, but

`A(1/2)=1>0`.

Here

`g_a=4>0`, `g_b=-4<0`, `F=-16<0`.

The exact dispatcher enters INTERIOR and rejects the false endpoint certificate.

### 10.2 Requiring the interior discriminant everywhere is too strong

Take `[0,1]`, `K=-1`,

`A(s)=-(s+1)^2=-1-2s-s^2`.

Then `A2=1`, `A1=-2`, and the true maximum on `[0,1]` is `A(0)=-1`, so the bound is sharp and valid.

But

`F=4A2(K-A0)-A1^2=-4<0`.

The stationary maximizer of `A` lies at `s=-1`, outside the admissible interval. A dispatcher that requires `F>=0` without checking the clamp branch would false-reject this safe packet. The LEFT branch correctly uses only `E_a=0`.

### 10.3 The sign of the quadratic coefficient cannot be ignored

If `A2` is allowed negative, `p(q,.)` is no longer convex. For the scalar example

`A2=-1`, `A1=0`, `C=-1`,

one has

`F=4>0`

but

`p(s)=-1-s^2<0`.

Thus `F>=0` by itself is meaningless without the concavity/branch geometry. The main theorem therefore first requires `A2>=0`; regions with `A2<0` must be routed to the convex-in-`A` vertex lane instead.

### 10.4 Zero curvature is safe if handled by branch priority

If `A2=0`, the problem is affine in `s`.

- `A1<0` gives `g_a=g_b<0`, hence LEFT;
- `A1>0` gives `g_a=g_b>0`, hence RIGHT;
- `A1=0` gives `g_a=g_b=0`, and the LEFT priority checks the constant value `E_a=C`.

Therefore there is no need to strengthen `A2>=0` to `A2>0` merely to avoid a denominator.

---

## 11. Source/geometry boundaries that remain open

The theorem is exact for the **declared full product** `[0,R] x [a,b]`. It must not silently rewrite source geometry.

1. **Moving parameter fiber.** If the real admissible set is `s in [a(q),b(q)]`, this is a different theorem. Substituting one frozen pair `(a,b)` is only an outer-envelope step unless source equality is proved.
2. **Curved/coupled source subset.** If `(q,s)` obeys an additional relation, a box witness outside the true relation is not a physical witness. Box PASS is sound for a containing set; box FAIL is only inconclusive for the smaller source set.
3. **Radial realizability.** `q=Q(u)` and the source parameter `s` must refer to the same source key/cell. A coefficient-level rational `q` is not automatically an actual state.
4. **Rational denominators in source coefficients.** If `A_i=N_i/D_i`, denominator signs must be proved on the same source domain before clearing them.
5. **Chart transport.** `s` must be the same typed parameter after any quotient/chart transform. A coordinate relabeling that changes the physical interval or mixes `s` with state variables requires a new transport lemma.
6. **Coverage.** Cell, trajectory, flowed-sheet, FD-halo and reference-halo coverage remain separate obligations.

A failed concavity gate is `CONCAVE_QUADRATIC_LANE_NOT_APPLICABLE`, not physical FAIL. A failed outer-box branch is `DECLARED_BOX_COUNTEREXAMPLE`; it upgrades to source FAIL only with source-membership/realizability evidence.

---

## 12. Minimal theorem statements for formalization

### Theorem 1 — concave quadratic clamp

Assume `a<b`, `A2>=0`, and

`p(s)=C-A1*s+A2*s^2`.

Set `ga=A1-2*a*A2`, `gb=A1-2*b*A2`.

Then:

- `ga<=0 -> inf_{s in [a,b]} p(s)=p(a)`;
- `ga>0 -> gb>=0 -> inf p=p(b)`;
- `ga>0 -> gb<0 -> A2>0` and `inf p=(4*A2*C-A1^2)/(4*A2)`.

### Theorem 2 — left fraction-free certificate

With `L=b-a`, `h=(s-a)(b-s)`,

`L*p = (-ga)*h + L*p(a) + (L*A2-ga)*(s-a)^2`.

### Theorem 3 — right fraction-free certificate

`L*p = gb*h + L*p(b) + (L*A2+gb)*(s-b)^2`.

### Theorem 4 — interior fraction-free certificate

`4*A2*p=(2*A2*s-A1)^2 + (4*A2*C-A1^2)`.

### Theorem 5 — clamp gluing

`F=4*A2*E_a-ga^2` and `F=4*A2*E_b-gb^2`.

### Theorem 6 — rational reserve shift

For rational `eta>=0`, the same clamp branches certify `p>=eta` after replacing

`E_a,E_b,F`

by

`E_a-eta, E_b-eta, F-4*A2*eta`.

These six statements are elementary ordered-ring identities/convexity facts and are preferable formalization targets before encoding the larger Sturm dispatcher.

---

## 13. Structural fingerprint

The reusable fingerprint is

`parametric radial energy with one quadratic nuisance parameter`

`-> prove A2(q)>=0`

`-> form ga=A1-2aA2, gb=A1-2bA2`

`-> LEFT / RIGHT / INTERIOR clamp`

`-> endpoint debit Ea / endpoint debit Eb / fraction-free interior debit F`

`-> exact branch SOS identity`

`-> one-dimensional Sturm sign atlas in q`

`-> rational reserve or rational box counterexample`.

This strictly extends T-P5-267's vertex lane while avoiding its general bivariate tensor-Bernstein fallback for this structured family.

---

## 14. Remaining obligations

Still open and explicitly not proved here:

1. actual deployed P5 source identity producing `A0,A1,A2`;
2. same-key identification of `q`, `s`, metric and cell;
3. proof that `A2>=0` for the actual source family;
4. proof that `[a,b]` is the real parameter fiber or a sound containing fiber;
5. actual rational coefficient extraction and denominator-sign semantics;
6. state realization of any negative box witness;
7. cell/trajectory/flowed-sheet/FD-halo/reference-halo coverage;
8. Float64/libm/interval semantics;
9. Lean/kernel formalization;
10. independent verification by 封不觉;
11. admission, registry mutation, or P5 parent closure.

---

## 15. Requested next step

The clean next non-overlapping source-to-math seam is the **moving quadratic fiber**:

`A(q,s)=A0(q)+A1(q)s-A2(q)s^2`,

but now the source proves rational/algebraic endpoint functions

`s in [a(q),b(q)]`

rather than a frozen box. The next child should determine when substitution of `a(q),b(q)` preserves a univariate fraction-free clamp certificate, including denominator-sign and endpoint-order gates, and when the moving fiber creates genuinely higher-degree/rational branch polynomials.

That would consume actual source geometry more faithfully than enlarging immediately to a fixed outer box, while preserving the present fail-closed source/coverage boundary.