---
kind: review_result
review_id: review-T-P5-066-zero-surface-recentering-liuguanyi-20260908T0420
task_id: T-P5-066-ZERO-SURFACE-RECENTERING
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-08T04:03:00-06:00
created_at: 2026-09-08T04:20:00-06:00
claim_commit: 924d1a87ff054643353370b7c73eae88d4e73876
inspected_commit: fb0ef3beff8e046cc44270288e5f5bd684003b79
parent_tasks:
  - T-P5-064-ANALYTIC-UNIT-PULLBACK
  - T-P5-065-RELATIVE-REMAINDER-ABSORPTION
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add a source-independent simple-zero displacement/recentering bridge before T-P5-064 when an additive lower-order remainder moves the zero surface; keep multiple roots, exact source root binding, unit Lipschitz regularity, Float64 and coverage separate
---

# T-P5-066 — simple-zero displacement, transversality, and exact recentering

## 0. Why this is the next mathematical seam

T-P5-064 handles exact factorizations of the form

`h(z) = u(z) * monomial(z)`

with a genuinely nonvanishing unit. T-P5-065 then proves that same/higher-order remainders can be absorbed without changing the nominal zero set when they are exactly divisible by the nominal monomial.

The remaining elementary case is different: a **lower-order additive remainder can move a simple zero without destroying it**. The canonical example is

`h(x) = x + a`.

The remainder `a` is not divisible by the nominal factor `x`, so T-P5-065 must reject reuse of the old factorization. Nevertheless the actual function has the exact factorization

`h(x) = (x + a) * 1`

around the shifted root `x_* = -a`.

This review proves the minimal theorem that justifies that recentering. The key point is that `C^0` smallness controls **where any zero may lie**, while a separate transversality / signed-secant condition is what upgrades the result to a **unique simple zero with a new nonvanishing unit**.

No provenance, receipt, admission, Float64, deployed CSE, P8 coverage, or Lean compile is inspected here.

---

## 1. Scalar source packet

Work on a real cell

`I = [c-H, c+H]`, with `H > 0`.

Let `sigma in {+1,-1}` and write the nominal simple factor plus additive remainder as

**(1.1)** `h(x) = u(x) * (x-c) + e(x)`.

Assume exact constants

`0 < m <= U`, `eps >= 0`, `Lu >= 0`, `Le >= 0`

such that for all `x,y in I`,

**(1.2)** `m <= sigma*u(x) <= U`,

**(1.3)** `|e(x)| <= eps`,

**(1.4)** `|u(y)-u(x)| <= Lu * |y-x|`,

**(1.5)** `|e(y)-e(x)| <= Le * |y-x|`.

Define the signed transversality reserve

**(1.6)** `mu = m - H*Lu - Le`

and the upper secant budget

**(1.7)** `M = U + H*Lu + Le`.

The two exact gates needed below are

**(1.8) ROOT-INSIDE:** `eps < m*H`,

**(1.9) SIMPLE-ROOT:** `H*Lu + Le < m`, equivalently `mu > 0`.

Both gates are multiplication/addition-only. No square root, eigenvalue, inverse, or numerical root search is part of the trusted statement.

---

## 2. Source bounds imply a uniform signed-secant inequality

Take `x<y` in `I`. Expand

`h(y)-h(x)`
`= u(y)(y-c) - u(x)(x-c) + e(y)-e(x)`
`= u(y)(y-x) + (u(y)-u(x))(x-c) + e(y)-e(x)`.

Multiplying by `sigma` and using `|x-c|<=H` gives

` sigma(h(y)-h(x))`
`>= m(y-x) - Lu*H*(y-x) - Le*(y-x)`
`= mu*(y-x)`.

The same expansion gives the upper bound

` sigma(h(y)-h(x)) <= M*(y-x)`.

Hence:

**Theorem 2.1 — signed secant packet**

For every `x<y` in `I`,

**(2.1)** `mu*(y-x) <= sigma*(h(y)-h(x)) <= M*(y-x)`.

Consequences:

- `h` is Lipschitz on the cell;
- if `mu>0`, then `sigma*h` is strictly increasing;
- therefore a zero, once it exists, is unique.

This is the precise reason an absolute remainder bound alone is insufficient: `eps` controls vertical displacement, while `Le` together with `Lu` controls folding of the graph.

---

## 3. Root existence and a division-free displacement bound

At the cell endpoints,

` sigma*h(c-H) <= -m*H + eps`,

` sigma*h(c+H) >=  m*H - eps`.

Under `eps < m*H`, these have opposite strict signs. Since the source packet already makes `h` Lipschitz, the intermediate value theorem gives a root

**(3.1)** `r in (c-H,c+H)` with `h(r)=0`.

Any root, even without uniqueness, satisfies the sharper pointwise identity

`u(r)(r-c) = -e(r)`.

Using `|u(r)| = sigma*u(r) >= m` gives the **division-free root-location theorem**

**(3.2)** `m * |r-c| <= eps`.

A checker does not need to materialize `eps/m`. It may provide any rational `delta` with

**(3.3)** `eps <= m*delta`, `0 <= delta`, `delta < H`,

and conclude

**(3.4)** `|r-c| <= delta`.

Thus root localization can remain exact rational even when the exact root itself is irrational or transcendental.

---

## 4. Exact recentered factorization from signed secants

Assume now `mu>0`, so the root `r` is unique.

The signed-secant inequality is stronger than mere root uniqueness: it directly constructs a new nonvanishing unit.

For `x != r`, define

`v(x) = h(x)/(x-r)`.

At `x=r`, choose for example

`v(r) = sigma*mu`.

Because `sigma^2=1`, the root value satisfies `sigma*v(r)=mu`.

For `x>r`, applying (2.1) to `(r,x)` and using `h(r)=0` gives

`mu <= sigma*h(x)/(x-r) <= M`.

For `x<r`, applying (2.1) to `(x,r)` gives the same inequality after dividing by the positive number `r-x`.

Therefore for every `x in I`,

**(4.1)** `h(x) = (x-r) * v(x)`,

**(4.2)** `mu <= sigma*v(x) <= M`.

This proves:

**Theorem 4.1 — simple-zero recentering / nonvanishing-unit bridge**

Under (1.1)–(1.5), `eps < mH`, and `HLu+Le < m`, there exist a unique root `r in I` and a function `v : I -> R` such that

`h(r)=0`,

`m|r-c| <= eps`,

`h(x)=(x-r)v(x)` for every `x in I`,

and

`0 < mu <= sigma*v(x) <= M` for every `x in I`.

So a lower-order remainder that moves a **simple** zero does not have to be rejected permanently. It can be consumed by changing the source contact coordinate from

`z = x-c`

to

**(4.3)** `xi = x-r`,

provided the transversality gate is proved.

The valuation in the new coordinate is exactly one and the parity is exactly odd. The old coordinate `x-c` must not be retained as the contact coordinate unless the root shift is separately proved to be zero.

---

## 5. Common product-core after recentering

A source-to-math adapter also needs to know that the shifted coordinate has a real domain, not merely a formal zero.

Suppose the checker chose a rational `delta` satisfying (3.3). Then `|r-c|<=delta`.

For every new coordinate value with

**(5.1)** `|xi| <= H-delta`,

we have

`|r + xi - c| <= |r-c| + |xi| <= delta + H-delta = H`.

Hence

**Theorem 5.1 — recentered core inclusion**

**(5.2)** `{r+xi : |xi|<=H-delta} subset I`.

This is the useful domain contract for T-P5-063/T-P5-064: after a root shift bounded by `delta`, the original cell still contains a common centered core of half-width `H-delta` in the **true** contact coordinate.

If `delta=H`, the common core collapses to a point. This is why the strict gate `eps<mH` is not cosmetic.

---

## 6. Parameterized root graph: the next coordinate-chart layer is still elementary

For a family `h_y(x)` on a common scalar interval, suppose every fiber has the same signed lower secant constant `mu>0` and unique root `r(y)`. Assume additionally that for every fixed `x`,

**(6.1)** `|h_y(x)-h_y'(x)| <= Lp * d(y,y')`.

Evaluate `h_y` at the root of the neighboring fiber. Since `h_y(r(y))=0` and `h_y'(r(y'))=0`,

`|h_y(r(y'))| = |h_y(r(y'))-h_y'(r(y'))| <= Lp*d(y,y')`.

The lower secant inequality in the `y` fiber gives

**(6.2)** `mu * |r(y)-r(y')| <= Lp * d(y,y')`.

Thus the root graph is quantitatively Lipschitz. In a division-free checker form, choose rational `Lr` with

**(6.3)** `Lp <= mu*Lr`

and conclude

**(6.4)** `|r(y)-r(y')| <= Lr*d(y,y')`.

This gives a triangular coordinate chart

`Phi(x,y) = (x-r(y), y)`.

On an `l1`-type product metric, both the forward and inverse coordinate changes have the elementary bound

`distance(Phi(p),Phi(q)) <= |x-x'| + (1+Lr)d(y,y')`

and the analogous reverse inequality after writing `x=xi+r(y)`.

This is enough to explain how a source checker may turn a parameter-dependent simple zero surface into an actual source coordinate without pretending that the zero stayed at the nominal center.

Important boundary: if the original source domain is not a common tube containing the graph, or if evaluating one fiber at the neighboring root leaves its domain, (6.2) cannot be used without an additional domain-overlap theorem.

---

## 7. Exact obstructions showing why each layer is separate

### 7.1 Small `C^0` error does not preserve a unique root

On `[-1/2,1/2]`, take the nominal factor

`g(x)=x`

and the actual function

`h(x)=x(x^2-1/16)=x^3-x/16`.

Then

`e(x)=h(x)-g(x)=x^3-(17/16)x`.

On this interval, `e` is monotone in magnitude and

`sup |e| = 13/32 < 1/2 = mH`

with nominal `m=1`.

So the root-inside `C^0` gate passes, yet the actual function has three roots

`-1/4, 0, 1/4`.

Therefore `eps<mH` localizes all roots but cannot by itself select a unique recentering.

### 7.2 Small `C^0` error can destroy the nonvanishing unit even with a unique root

Again on `[-1/2,1/2]`, let

`g(x)=x`, `h(x)=x^3`, `e(x)=x^3-x`.

Then

`sup |e| = 3/8 < 1/2`.

The actual function has the unique root `0`, but its exact factorization is

`h=x*x^2`,

whose unit candidate `x^2` vanishes at contact. Here the transversality reserve is exactly lost: `Le=1` is compatible with `mu=m-Le=0`.

Thus root uniqueness alone is still weaker than the nonvanishing-unit contract required by T-P5-064.

### 7.3 Equality `eps=mH` is boundary-only

Take `h(x)=x-H` on `[-H,H]`, with nominal `u=1`, `e=-H`. Then `eps=mH` and the only root is the endpoint `x=H`. There is no positive common recentered half-width `H-delta` if the displacement allowance is `delta=H`.

### 7.4 Old parity is not transported through a shifted zero

For `h(x)=x+a`, the true parity factor is `sign(x+a)`, not `sign(x)`. They disagree on the interval between `-a` and `0` whenever `a!=0`. Therefore a tiny root displacement cannot be hidden inside an amplitude budget when the consumer depends on sign/parity.

---

## 8. What this theorem does and does not repair

This child creates a clean decision split after T-P5-065:

- if the remainder is divisible by the nominal monomial, absorb it into the old unit and keep the old zero set;
- if the remainder is not divisible but the nominal contact is **simple**, use the present `C^0 + transversality` gate to locate the shifted zero and recenter exactly;
- if only `C^0` smallness is known, retain only the root-location envelope and do not claim a unique/unit factorization;
- if the nominal contact has multiplicity greater than one, this theorem does not apply. Small lower-order perturbations may split the root, so a separate multiple-root / root-cluster theorem is required.

The simple-root hypothesis is encoded mathematically by the existence of a nonvanishing nominal unit and the positive transversality reserve `mu>0`. No multiplicity metadata should be inferred from a sampled graph.

---

## 9. Lean-friendly theorem decomposition

The recommended first formalization remains small and source-independent.

### Leaf A — source packet to signed secants

```text
signed_secant_bounds_of_unit_plus_remainder
  (x y in I) (x <= y)
  (m <= sigma*u(t) <= U on I)
  (Lip u <= Lu) (Lip e <= Le)
  : (m-H*Lu-Le)*(y-x)
      <= sigma*(h y-h x)
    ∧ sigma*(h y-h x)
      <= (U+H*Lu+Le)*(y-x)
```

### Leaf B — root displacement without division

```text
root_displacement_mul_le
  (h r = 0)
  (h r = u r*(r-c)+e r)
  (m <= sigma*u r)
  (abs (e r) <= eps)
  : m * abs (r-c) <= eps
```

### Leaf C — unique root from endpoint signs plus strict secants

```text
existsUnique_root_of_signed_secant
  (sigma*h(left) < 0)
  (0 < sigma*h(right))
  (0 < mu)
  (mu*(y-x) <= sigma*(h y-h x) for x<y)
  (h continuous)
  : exists! r in [left,right], h r = 0
```

### Leaf D — recentered nonvanishing factor exists

```text
exists_recentered_unit_of_signed_secant
  (h r = 0)
  (0 < mu)
  (mu*(y-x) <= sigma*(h y-h x) <= M*(y-x) for x<y)
  : exists v,
      (forall x, h x = (x-r)*v x)
      ∧ (forall x, mu <= sigma*v x ∧ sigma*v x <= M)
```

The proof may construct `v` by a pointwise `if x=r then sigma*mu else h x/(x-r)`. The theorem statement itself does not expose a reciprocal to downstream consumers.

### Leaf E — common recentered core

```text
recentered_core_subset
  (abs (r-c) <= delta)
  (delta <= H)
  (abs xi <= H-delta)
  : abs ((r+xi)-c) <= H
```

### Optional Leaf F — parameter root-graph Lipschitz

```text
root_graph_lipschitz_mul
  (uniform signed secant lower mu)
  (abs (h y x - h y' x) <= Lp*d y y')
  : mu * abs (r y-r y') <= Lp*d y y'
```

This leaf should only be added when the same common interval/domain overlap has been typed explicitly.

---

## 10. Interface recommendation

A future source packet for a shifted simple zero should carry:

`nominal_center c`, `half_width H`, `sign sigma`, `unit_lower m`, `unit_upper U`, `unit_lipschitz Lu`, `remainder_sup eps`, `remainder_lipschitz Le`.

The exact checker then computes

`mu = m-H*Lu-Le`, `M = U+H*Lu+Le`

and requires

`eps < mH`, `0 < mu`.

It may also choose an exact rational `delta` satisfying `eps <= m*delta < m*H`. The mathematical layer returns a symbolic unique root `r`, the displacement theorem, an exact recentered factorization, and a common core width `H-delta`.

Crucially, an interval enclosure for `r` is **not** by itself an exact factorization witness. If a later source/Lean adapter needs the actual coordinate map, it must either carry the symbolic unique root defined by the theorem or provide an exact root equation `h(r)=0`; a decimal midpoint cannot be substituted for the root.

---

## 11. Remaining boundary

This result is a **pending mathematical/interface child** only.

Still open and not claimed here:

- whether the deployed CSE has a simple nominal factor satisfying this packet;
- exact rational `m,U,Lu,eps,Le,H` for any physical cell;
- exact source identity `h=u(x-c)+e`;
- a typed symbolic root or source-bound root equation for deployed factors;
- parameter-domain overlap and multi-factor/intersection coordinate charts;
- multiple-root splitting / root-cluster theory;
- Lipschitz regularity of the newly constructed unit `v` beyond its amplitude/sign bounds (this needs a normalized divided-difference or second-derivative/C1,1 packet);
- Float64/libm/FD/controller semantics;
- P8/ODE coverage;
- Lean compilation, kernel receipt, independent validation, comparator, admission, P5/P8/M4 closure, or registry mutation.

The main mathematical advance is that **non-divisible lower-order remainder is not automatically fatal for a simple contact**. It is fatal to the *old zero coordinate*, but under exact rational C0 and transversality gates it can be converted into a new exact contact coordinate with a quantitatively nonvanishing unit.