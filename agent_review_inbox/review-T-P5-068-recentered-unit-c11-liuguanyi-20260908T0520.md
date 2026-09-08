---
kind: review_result
review_id: review-T-P5-068-recentered-unit-c11-liuguanyi-20260908T0520
task_id: T-P5-068-RECENTERED-UNIT-C11
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-08T05:05:00-06:00
created_at: 2026-09-08T05:20:00-06:00
claim_commit: 3db0d0af20ff6bdf88ef924ca8cb5023c165aa08
parent_tasks:
  - T-P5-066-ZERO-SURFACE-RECENTERING
  - T-P5-064-ANALYTIC-UNIT-PULLBACK
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add a source-independent C1,1 divided-difference bridge after T-P5-066, so the exact shifted simple-root factorization acquires the quantitative nonvanishing and Lipschitz unit packet required by T-P5-064; keep multiple-root, deployed source, Float64, coverage, Lean validation and admission separate
---

# T-P5-068 — C1,1 regularity of the exact recentered unit

## 0. Mathematical seam

T-P5-066 proves that a lower-order perturbation of a simple contact can be handled by moving the contact coordinate to the **actual unique root** `r`. Under its `C0 + transversality` packet it produces an exact factorization

`h(x) = (x-r) v(x)`

with a quantitative sign/amplitude bound

`0 < mu <= sigma*v(x) <= M`.

What T-P5-066 deliberately does **not** prove is a Lipschitz bound for the newly constructed unit `v`. Its pointwise construction can be written as

`v(x) = h(x)/(x-r)` for `x != r`,

with a separately chosen value at `r`; from secant bounds alone this gives amplitude control but no quantitative regularity at the root.

That missing regularity matters because T-P5-064's analytic-unit transport consumes a unit packet of the form

`m <= sigma*u <= U`, `Lip(u) <= L_u`.

This child proves that one extra source-independent hypothesis — a Lipschitz derivative for the shifted factor — closes the seam exactly. The root may remain symbolic; no numerical root evaluation is needed.

No provenance, receipt, admission, deployed CSE, Float64, P8 coverage, or Lean compilation is claimed here.

---

## 1. Scalar C1,1 packet

Let `I` be a convex real interval, let `r in I`, and let

`h : I -> R`

be `C1` on `I`, with

**(1.1)** `h(r)=0`.

Assume a sign `sigma in {+1,-1}` and exact constants

`0 < mu <= M`, `L2 >= 0`

such that for every `z in I`,

**(1.2)** `mu <= sigma*h'(z) <= M`,

and for all `x,y in I`,

**(1.3)** `|h'(x)-h'(y)| <= L2*|x-y|`.

Define the canonical recentered divided-difference unit

**(1.4)**

`v_r(x) = h(x)/(x-r)` if `x != r`,

`v_r(r) = h'(r)`.

The value at the root is no longer arbitrary. It is the unique continuous extension of the punctured divided difference.

For the direct continuation of T-P5-066, condition (1.2) does not need to be a new independent source claim. T-P5-066 already yields, for `x<y`,

`mu*(y-x) <= sigma*(h(y)-h(x)) <= M*(y-x)`.

If `h` is differentiable, taking the secant limit at each point recovers (1.2). Thus the genuinely new quantitative datum in this child is the `C1,1` bound (1.3).

---

## 2. Exact segment-average identity

Because `I` is convex, the segment

`gamma_x(t) = r + t(x-r)`, `0<=t<=1`

stays in `I`. The fundamental theorem of calculus gives

`h(x)-h(r) = integral_0^1 h'(r+t(x-r))*(x-r) dt`.

Using `h(r)=0`, for `x != r` we obtain

**(2.1)**

`h(x)/(x-r) = integral_0^1 h'(r+t(x-r)) dt`.

At `x=r`, the right-hand side is exactly `h'(r)`. Therefore the identity extends to every `x in I`:

**Theorem 2.1 — canonical recentered unit as an averaged derivative**

**(2.2)**

`v_r(x) = integral_0^1 h'(r+t(x-r)) dt`.

This is the main bridge. It removes the apparent singularity `1/(x-r)` before any quantitative bound is taken.

The source/math interface should therefore regard `v_r` as a **divided difference / averaged derivative**, not as a floating-point quotient near the root.

---

## 3. Nonvanishing bounds transport with no loss

By (1.2), for every `t in [0,1]`,

`mu <= sigma*h'(r+t(x-r)) <= M`.

Averaging preserves the interval. Hence from (2.2):

**Theorem 3.1 — derivative sign bounds are inherited exactly**

For all `x in I`,

**(3.1)** `mu <= sigma*v_r(x) <= M`.

So the C1,1 canonical unit agrees with the amplitude packet already obtained abstractly in T-P5-066, but now with the correct root value `v_r(r)=h'(r)` and a canonical regular extension.

In particular:

- `v_r` never vanishes;
- it has the same fixed sign `sigma` on the entire interval;
- recentering does not weaken the transversality margin;
- the symbolic root `r` causes no denominator reserve to appear in the final bound.

---

## 4. Sharp Lipschitz constant: the factor 1/2

Take `x,y in I`. From the average representation,

`v_r(x)-v_r(y)`
`= integral_0^1 [h'(r+t(x-r))-h'(r+t(y-r))] dt`.

At each `t`, the two derivative arguments differ by exactly

`t*(x-y)`.

Therefore (1.3) gives

`|h'(r+t(x-r))-h'(r+t(y-r))|`
`<= L2*t*|x-y|`.

Integrating `t` from `0` to `1` yields

**Theorem 4.1 — recentered-unit C1,1 bridge**

**(4.1)**

`|v_r(x)-v_r(y)| <= (L2/2)*|x-y|`.

For an exact-rational checker it is preferable to store the division-free equivalent

**(4.2)**

`2*|v_r(x)-v_r(y)| <= L2*|x-y|`.

Thus the unit Lipschitz budget needed by T-P5-064 is simply

**(4.3)** `L_v = L2/2`.

No dependence on `|r-c|`, the old center `c`, or a lower bound on `|x-r|` appears.

### Sharpness

The constant `1/2` cannot be improved uniformly. Take `r=0` and

`h(x) = a*x + (L2/2)*x^2`.

Then

`h'(x)=a+L2*x`,

so `Lip(h')=L2`, while

`v_0(x)=a+(L2/2)*x`.

Hence

`Lip(v_0)=L2/2`.

The bridge is therefore quantitatively sharp already for quadratic functions.

---

## 5. Why C1 plus transversality is insufficient

It would be unsafe to replace (1.3) by mere continuity of `h'`.

Consider, near the origin,

**(5.1)** `h(x)=x*(1+sqrt(|x|))`.

Then `h(0)=0`, and `h` is `C1` with

`h'(0)=1`,

`h'(x)=1+(3/2)*sqrt(|x|)` for `x != 0`.

On any sufficiently small symmetric interval the derivative is strictly positive, so the root is unique and uniformly transverse. However the exact recentered unit is

**(5.2)** `v_0(x)=1+sqrt(|x|)`,

which is **not Lipschitz at 0**.

Therefore:

- root uniqueness is not enough;
- a nonvanishing secant packet is not enough;
- `C1` regularity is not enough;
- a quantitative modulus of continuity for `h'` is the actual missing hypothesis.

This obstruction is directly relevant to interface design: a source checker must not populate T-P5-064's `unit_lipschitz` field merely because the recentered unit is continuous and nonzero.

---

## 6. More general modulus-of-continuity theorem

The C1,1 result is a special case of a useful exact transport rule.

Suppose instead of (1.3) that

**(6.1)** `|h'(x)-h'(y)| <= omega(|x-y|)`

for a nondecreasing modulus `omega`. The same average argument gives

**(6.2)**

`|v_r(x)-v_r(y)| <= integral_0^1 omega(t*|x-y|) dt`.

In particular, if

`|h'(x)-h'(y)| <= L_alpha*|x-y|^alpha`

for `0<alpha<=1`, then

**(6.3)**

`|v_r(x)-v_r(y)| <= [L_alpha/(alpha+1)]*|x-y|^alpha`.

Thus recentering preserves the derivative's Hölder exponent and improves its coefficient by the exact averaging factor `1/(alpha+1)`.

For the current exact-rational pipeline the `alpha=1` branch is the preferred typed contract, because it uses only rational arithmetic. The general statement is useful mathematically but does not need to enter the first trusted Lean leaf.

---

## 7. Parameterized root-chart bridge

T-P5-066 also proved a root-graph Lipschitz estimate for a family of simple contacts. The divided-difference representation composes cleanly with that theorem.

Let `y` range over a metric parameter domain. For each `y`, let

`h_y(x)`

have a unique root `r(y)`. Work on a common recentered core where every point

`r(y)+xi`

under consideration lies inside the source cell.

Write

`g_y(x)=partial_x h_y(x)`.

Assume exact constants `Lx,Ly,Lr >= 0` such that

**(7.1)**

`|g_y(x)-g_y'(x')| <= Lx*|x-x'| + Ly*d(y,y')`,

and

**(7.2)**

`|r(y)-r(y')| <= Lr*d(y,y')`.

Define the recentered unit in triangular coordinates by

**(7.3)**

`V(y,xi) = integral_0^1 g_y(r(y)+t*xi) dt`.

For two chart points `(y,xi)` and `(y',xi')`,

`|[r(y)+t xi]-[r(y')+t xi']|`
`<= |r(y)-r(y')| + t|xi-xi'|`
`<= Lr*d(y,y') + t|xi-xi'|`.

Using (7.1) and integrating gives:

**Theorem 7.1 — parameterized recentered-unit chart bound**

**(7.4)**

`|V(y,xi)-V(y',xi')|`
`<= (Lx*Lr + Ly)*d(y,y') + (Lx/2)*|xi-xi'|`.

Again the half factor only charges motion in the recentered contact coordinate. Root motion itself is charged at full strength through `Lx*Lr`.

If T-P5-066 supplies the division-free root-graph packet

`mu*|r(y)-r(y')| <= Lp*d(y,y')`,

a checker may choose any rational `Lr` satisfying

`Lp <= mu*Lr`

and then use (7.4) without ever dividing by `mu` inside the trusted theorem.

This gives a concrete source-to-math triangular chart:

`(x,y) -> (xi,y) = (x-r(y), y)`

with an exact quantitative unit regularity budget.

---

## 8. Relation to T-P5-066 and T-P5-064

The simple-contact lane can now be decomposed without ambiguity.

### Stage A — T-P5-066

From

`h(x)=u(x)(x-c)+e(x)`

plus `C0`, Lipschitz and transversality gates, obtain:

- a symbolic unique root `r`;
- exact `h(r)=0`;
- rational displacement envelope for `r-c`;
- exact new coordinate `xi=x-r`;
- nonvanishing amplitude bounds for some recentered factor.

### Stage B — present T-P5-068

Add `C1,1` regularity for the actual shifted factor `h` and canonically choose

`v_r(r)=h'(r)`,

`v_r(x)=h(x)/(x-r)` away from the root.

Then obtain:

- exact factorization `h=(x-r)v_r`;
- the same sign/amplitude bounds;
- `Lip(v_r)<=L2/2`;
- parameterized chart regularity when the derivative packet is uniform.

### Stage C — T-P5-064

Now the actual recentered factor has exactly the analytic-unit packet needed for valuation/parity transport:

`factor = (nonvanishing Lipschitz unit) * (new contact coordinate)`.

The old nominal coordinate `x-c` never needs to be reused after a nonzero root displacement.

---

## 9. Source packet recommendation

A deployed simple-contact source lane should not try to evaluate `h(x)/(x-r)` numerically near `r`. The minimal mathematical packet is instead:

- exact/symbolic root witness `r` with `h(r)=0`, supplied by T-P5-066 or an equivalent theorem;
- same-cell differentiability / `C1` witness for `h`;
- signed derivative bounds `mu <= sigma*h' <= M` (or the T-P5-066 signed-secant packet plus differentiability);
- exact rational `L2` with `|h'(x)-h'(y)|<=L2|x-y|` on the whole relevant cell;
- for parameter transport, exact `Lx,Ly` and the T-P5-066 root-graph budget.

The adapter should then construct the canonical divided-difference unit symbolically and publish

`unit_lower = mu`,

`unit_upper = M`,

`unit_lipschitz_twice = L2`,

where the last field means `2|Delta v|<=L2|Delta x|`.

This is safer than publishing a floating quotient or sampling near the root.

A second-derivative enclosure can generate the packet: whenever `h'` is absolutely continuous and `|h''|<=L2` almost everywhere on the interval, `h'` is `L2`-Lipschitz. That source theorem is separate from the present divided-difference bridge.

---

## 10. Lean-friendly theorem decomposition

The first formalization should remain source-independent and small.

### Leaf A — average derivative identity

```text
recentered_unit_eq_segment_average_deriv
  (h r = 0)
  (h C1 on interval I)
  (r in I) (x in I)
  : recenteredUnit h r x
      = integral t in [0,1], deriv h (r+t*(x-r))
```

The exact Mathlib integral spelling can be chosen by the formalization Agent; the mathematical contract is only the segment-average identity.

### Leaf B — amplitude bounds

```text
recentered_unit_bounds_of_deriv_bounds
  (mu <= sigma*deriv h z <= M on I)
  : mu <= sigma*recenteredUnit h r x
      ∧ sigma*recenteredUnit h r x <= M
```

### Leaf C — sharp Lipschitz transport

Prefer the multiplication-only conclusion:

```text
recentered_unit_lipschitz_twice_of_deriv_lipschitz
  (abs (deriv h x - deriv h y) <= L2*abs(x-y) on I)
  : 2*abs (recenteredUnit h r x - recenteredUnit h r y)
      <= L2*abs(x-y)
```

### Optional Leaf D — secant packet to derivative bounds

```text
deriv_bounds_of_signed_secant_bounds
  (mu*(y-x) <= sigma*(h y-h x) <= M*(y-x) for x<y)
  (h differentiable at x)
  : mu <= sigma*deriv h x ∧ sigma*deriv h x <= M
```

This lets T-P5-066 feed the new child without duplicating the sign-bound premise.

### Optional Leaf E — parameter chart

```text
recentered_unit_chart_lipschitz
  (joint derivative packet Lx Ly)
  (root graph Lip <= Lr)
  : abs (V y xi - V y' xi')
      <= (Lx*Lr+Ly)*d(y,y') + (Lx/2)*abs(xi-xi')
```

If division-free arithmetic is preferred, multiply the full conclusion by `2`.

The C1 counterexample in Section 5 should be retained as a design test, not as a theorem dependency.

---

## 11. Important boundary: C1,1 of what object?

The new derivative packet must apply to the **actual shifted factor `h` on the same physical cell**, not merely to the old nominal factor.

For example, knowing that the nominal `x-c` has constant derivative says nothing about the derivative modulus of an arbitrary additive remainder. If the source decomposition is

`h = h_nom + e`,

then a valid `L2` may be assembled from derivative-Lipschitz budgets for both pieces, but only after a theorem identifies the exact same `h` consumed by T-P5-066.

Likewise, a finite-difference estimate of `h'` is not automatically the analytic derivative packet used here. FD/truncation/rounding semantics remain a separate source theorem.

---

## 12. Remaining boundary

This result is a **pending mathematical/interface child** only.

Still open and not claimed here:

- whether the deployed CSE has a simple contact entering the T-P5-066 lane;
- exact source binding of the symbolic root `r` and the actual shifted factor `h`;
- exact rational derivative sign bounds and `C1,1`/`L2` constant on each physical cell;
- derivation of `L2` from source trig/Taylor/interval code or second-derivative packets;
- parameter-domain overlap beyond the stated common-core hypothesis;
- multiple-root / root-cluster splitting (owned by the separate T-P5-067 lane);
- multi-factor intersection charts and invertibility of higher-dimensional coordinate changes;
- Float64/libm/FD/controller/solve semantics;
- P8/ODE/first-exit coverage;
- Lean compilation, kernel receipt, independent validation by 封不觉, comparator, admission, P5/P8/M4 closure, or registry mutation.

The mathematical advance is precise: **once T-P5-066 has moved a simple contact to its true root, one Lipschitz-derivative packet turns the symbolic divided difference into the exact nonvanishing Lipschitz unit required downstream, with the sharp loss `L_v=L2/2` and no root-denominator reserve.**