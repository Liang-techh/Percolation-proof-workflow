---
kind: review_result
review_id: review-T-P5-067-multiple-root-cluster-kuangmanmozun-20260908T0450
task_id: T-P5-067-MULTIPLE-ROOT-CLUSTER
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-08T04:34:00-06:00
created_at: 2026-09-08T04:50:00-06:00
claim_commit: a1bb63ca9e838713291a990c689f28ca180daf1a
inspected_commit: 6fb6919be713810136da5cda950c6de2894ef362
parent_tasks:
  - T-P5-065-RELATIVE-REMAINDER-ABSORPTION
  - T-P5-066-ZERO-SURFACE-RECENTERING
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add a radical-free multiple-contact root-cluster / outer-sign gate after T-P5-065 and before any attempt to reuse T-P5-066; do not infer a unique recentering or preserved multiplicity for k>=2 from C0 smallness
---

# T-P5-067 — multiple-contact root cluster, outer-sign reserve, and lower-order unfolding obstruction

## 0. Seam addressed

T-P5-066 gives the correct repair for a moved **simple** zero: a small vertical displacement plus a strict signed-secant reserve yields a unique shifted root and a new nonvanishing unit.

Its explicit open boundary is multiplicity `k>1`. In that regime a lower-order perturbation can do three qualitatively different things even when its coefficient is arbitrarily small:

- split one multiple contact into several simple contacts;
- lower the multiplicity of the old contact;
- for even multiplicity, remove the real contact entirely.

Therefore the next trusted object cannot be a guessed shifted root. The robust source-independent object is a **root cluster** plus exact nonvanishing/sign reserves outside that cluster.

This review gives that gate with integer powers only. No radical, numerical root search, provenance, Float64, receipt, admission, coverage, or deployed source binding is used.

---

## 1. Multiple-contact source packet

Let

`I = [c-H,c+H]`, `H>0`,

and let `k` be an integer with `k>=2`.

Assume

`h(x) = u(x) * (x-c)^k + e(x)`

with `u,e,h` continuous on `I`. Fix `sigma in {+1,-1}` and exact constants `m>0`, `eps>=0` such that

`m <= sigma*u(x)` for every `x in I`,

`|e(x)| <= eps` for every `x in I`.

No derivative or Lipschitz hypothesis is needed for the cluster localization itself.

Choose a rational/exact radius `delta` satisfying

`0 < delta <= H`.

Define the division-free outer reserve

`rho = m*delta^k - eps`.

The useful strict gate is

`rho > 0`, equivalently `eps < m*delta^k`.

A checker never needs to form `(eps/m)^(1/k)`.

---

## 2. Sharp root-cluster localization

Suppose `r in I` and `h(r)=0`. Then

`u(r)*(r-c)^k = -e(r)`.

Taking absolute values and using `|u(r)| = sigma*u(r) >= m` gives

**(2.1)** `m*|r-c|^k <= eps`.

Hence:

### Theorem 2.1 — division-free multiple-root cluster

If `eps <= m*delta^k`, every real zero of `h` in `I` satisfies

`|r-c| <= delta`.

If the inequality is strict,

`eps < m*delta^k`,

then every real zero satisfies

`|r-c| < delta`.

This is the exact higher-multiplicity analogue of the T-P5-066 displacement inequality `m|r-c|<=eps` for `k=1`.

### Sharpness

The power `k` and the constant `1` cannot be improved from these assumptions. Take `u=m` and

`h(x)=m(x-c)^k-eps`.

Any positive real root `r` satisfies exactly

`m|r-c|^k = eps`.

For even `k` there are two equality roots whenever they lie in the cell. Thus the natural geometric radius is indeed of order `(eps/m)^(1/k)`, but the trusted certificate can remain radical-free through `eps <= m*delta^k`.

---

## 3. Exact sign and coercivity outside the cluster

The cluster theorem is stronger than a root-location statement: the same arithmetic gives a positive lower bound for `|h|` on both outer wings.

Assume `rho=m*delta^k-eps>0`.

### Right wing

For `x-c >= delta`, `(x-c)^k >= delta^k`, hence

` sigma*h(x)`
`= (sigma*u(x))*(x-c)^k + sigma*e(x)`
`>= m*delta^k - eps`
`= rho > 0`.

Therefore

**(3.1)** `sigma*h(x) >= rho` on `[c+delta,c+H]`.

### Left wing, even k

If `k` is even and `x-c <= -delta`, then `(x-c)^k=|x-c|^k >= delta^k`, so again

**(3.2-even)** `sigma*h(x) >= rho` on `[c-H,c-delta]`.

### Left wing, odd k

If `k` is odd and `x-c <= -delta`, then `(x-c)^k=-|x-c|^k`. Since `sigma*u(x)>=m`,

` sigma*h(x) <= -m*delta^k + eps = -rho < 0`.

Thus

**(3.2-odd)** `sigma*h(x) <= -rho` on `[c-H,c-delta]`.

### Theorem 3.1 — root-cluster / outer-sign certificate

Under `rho>0`:

- every zero lies in the open middle cluster `(c-delta,c+delta)`;
- `|h(x)|>=rho` on both outer cells;
- if `k` is even, the signed value `sigma*h` is positive on both outer cells;
- if `k` is odd, `sigma*h` is negative on the left outer cell and positive on the right outer cell.

Operationally this gives an exact three-cell split

`left outer | unresolved root cluster | right outer`

with a certified nonvanishing denominator reserve `rho` on the two outer pieces. The middle cell is the only place where new source factorization/root isolation is needed.

This is useful for T-P5-063/T-P5-064 because parity/valuation logic may continue on the two outer cells without pretending that the old contact survived inside the cluster.

---

## 4. What existence survives from parity of the nominal multiplicity

Continuity plus the outer-sign packet gives the strongest universal existence statements available from `C^0` data alone.

### 4.1 Odd k: at least one real zero survives

For odd `k`, under `rho>0`,

`sigma*h(c-delta) < 0 < sigma*h(c+delta)`.

By the intermediate value theorem there is at least one

`r in (c-delta,c+delta)`

with `h(r)=0`.

So odd nominal degree preserves a real root **as a cluster-level existence statement**.

It does **not** preserve uniqueness or multiplicity.

### 4.2 Even k: C0 smallness alone does not preserve any real zero

For even `k`, both outer signs are positive. There is no topological sign change forcing a zero.

Two opposite constant perturbations already show the sharp dichotomy:

`h_+(x)=(x-c)^2+a^2` has no real zero,

while

`h_-(x)=(x-c)^2-a^2` has two simple real zeros `c-a` and `c+a`

when `0<a<H`.

Both are arbitrarily small `C^0` perturbations of the same double contact as `a->0`.

### 4.3 A minimal even-k two-root gate

Although C0 smallness alone gives no existence, one extra signed center test is enough to force a split.

Assume `k` even, `rho>0`, and

` sigma*h(c) = sigma*e(c) < 0`.

The outer values at `c-delta` and `c+delta` are strictly positive. Hence IVT on the two half intervals gives two **distinct** roots

`r_- in (c-delta,c)`,

`r_+ in (c,c+delta)`.

Thus:

### Theorem 4.1 — even-contact split witness

For even `k`, the exact gate

`eps < m*delta^k`

plus

`sigma*e(c)<0`

forces at least two real roots, one on each side of the nominal center.

No uniqueness of either wing root is implied without additional monotonicity/derivative information.

### 4.4 A minimal no-root gate

If `k` is even and

`sigma*e(x) >= 0` for every `x in I`,

then

`sigma*h(x) >= m|x-c|^k >= 0`.

For `x!=c` this is strictly positive. Therefore the only possible zero is `x=c`; if additionally `sigma*e(c)>0`, there is no real zero at all.

This makes explicit that even contacts require a sign/topology branch, not merely a displacement budget.

---

## 5. Lower-order perturbations destroy multiplicity at arbitrarily small coefficient

The following exact family shows why T-P5-065's same/higher-order divisibility condition is essentially sharp.

Let the nominal contact be

`g(z)=z^k`

and perturb it by a lower-order monomial

`e_a(z)=a*z^j`,

where

`0 <= j < k`, `a != 0`.

Then

**(5.1)** `h_a(z)=z^k+a*z^j = z^j*(z^(k-j)+a)`.

At `z=0` the second factor equals `a`, hence is nonzero. Therefore:

- if `j=0`, the nominal contact at zero disappears;
- if `j>=1`, the actual multiplicity at zero is **exactly `j`**, not `k`.

The coefficient `a` can be arbitrarily small. Consequently:

### Theorem 5.1 — no coefficient-smallness multiplicity preservation

For every `k>=2`, every `j<k`, and every coefficient tolerance `eta>0`, there exists `a` with `0<|a|<eta` such that the perturbation `a z^j` changes the contact multiplicity from `k` to `j` (or removes the center contact when `j=0`).

So there is no theorem of the form

`small lower-order coefficient => preserve old valuation/parity at z=0`.

Preserving the old contact order requires structural divisibility (T-P5-065), not merely a small norm.

---

## 6. Exact split / annihilation examples and parity migration

### 6.1 Double contact: remove versus split

Take nominal `g(z)=z^2`.

For any small `a>0`,

`z^2+a^2 > 0`

has no real contact, while

`z^2-a^2=(z-a)(z+a)`

has two simple real contacts.

Thus a double zero cannot in general be repaired by selecting one shifted double root. The correct robust object is a cluster containing zero, one, or several actual roots depending on extra sign data.

### 6.2 Tiny linear term flips local parity

Take

`h(z)=z^2+a z = z(z+a)`, `a!=0`.

The old contact at `z=0` had even multiplicity `2`; the actual contact at zero is simple, hence odd. There is a second simple root at `z=-a`.

Therefore arbitrarily small lower-order perturbation can change the local sign parity from even to odd. The old `beta=k mod 2` must not be transported into the unresolved cluster.

### 6.3 Triple contact: one real root versus three

Take

`h_a(z)=z^3+a z = z(z^2+a)`.

If `a>0`, the only real root is `z=0`, now simple.

If `a<0`, there are three simple real roots

`0`, `+sqrt(-a)`, `-sqrt(-a)`.

Thus even for fixed nominal odd multiplicity, small perturbations preserve only the **existence of at least one real root**, not the number of roots or their multiplicities.

The trusted cluster theorem in Sections 2–4 states exactly that amount and no more.

---

## 7. Why a naive extension of T-P5-066 is unsound

A tempting but invalid rule would be:

> nominal contact has multiplicity k, perturbation is small, therefore there is a nearby root r and `h=(x-r)^k v` with v nonvanishing.

For `k=2`, `h=x^2-a^2` disproves this immediately: there are two distinct simple roots and no shifted double root.

The opposite perturbation `h=x^2+a^2` disproves even the existence of a nearby real root.

Therefore for `k>=2` a checker must not emit a single recentered `k`-fold factor merely from `C^0` closeness. It may emit only:

1. the exact root cluster radius inequality;
2. the exact outer nonvanishing/sign reserve;
3. parity-dependent existence information (odd: at least one; even: none forced);
4. any stronger factorization only after a separate root-isolation / multiplicity theorem has been supplied.

---

## 8. Boundary and failure branches

### 8.1 Equality is boundary-only

If `eps=m*delta^k`, outer nonvanishing can fail exactly at the cluster boundary. For example

`h(z)=m z^k-eps`

has a positive root at `z=delta` whenever `delta^k=eps/m`.

Therefore the strict three-cell nonvanishing certificate needs

`eps < m*delta^k`,

not merely `<=`.

### 8.2 No upper root-count bound from C0 control alone

The present hypotheses control root location and outer sign, not oscillation inside the middle cell. Without derivative/variation or polynomial-degree information, no uniqueness claim is justified there. The T-P5-066 signed-secant mechanism is special to the simple-root/transversal branch.

### 8.3 Old contact parity is valid only outside the quarantined cluster

For odd `k`, left/right outer signs retain the nominal sign flip. For even `k`, both outer signs retain the nominal same-sign behavior. Inside the cluster, lower-order perturbations can change the number and parity of individual contacts, so T-P5-057/T-P5-059 sign consumers must use newly certified factors, not `sign(x-c)`.

---

## 9. Lean-friendly leaf statements

A minimal formalization can remain almost entirely ordered-ring arithmetic plus IVT.

### Leaf A — root localization

```text
multiple_contact_root_mul_pow_le
  (h r = 0)
  (h r = u r * (r-c)^k + e r)
  (m <= sigma*u r)
  (abs (e r) <= eps)
  : m * abs (r-c)^k <= eps
```

### Leaf B — outer right reserve

```text
multiple_contact_right_outer_reserve
  (delta <= x-c)
  (eps < m*delta^k)
  : rho <= sigma*h x
```

### Leaf C — outer left reserve, parity split

```text
multiple_contact_left_outer_reserve_even
  (x-c <= -delta) (Even k)
  : rho <= sigma*h x

multiple_contact_left_outer_reserve_odd
  (x-c <= -delta) (Odd k)
  : sigma*h x <= -rho
```

### Leaf D — odd contact existence

```text
exists_root_in_cluster_of_odd_contact
  (Odd k) (0 < rho) (Continuous h)
  : exists r, abs (r-c) < delta ∧ h r = 0
```

### Leaf E — even split from center sign

```text
exists_two_roots_of_even_contact_center_negative
  (Even k) (0 < rho) (sigma*h c < 0) (Continuous h)
  : exists rminus rplus,
      c-delta < rminus ∧ rminus < c ∧ h rminus = 0 ∧
      c < rplus ∧ rplus < c+delta ∧ h rplus = 0
```

### Leaf F — exact lower-order multiplicity drop

For polynomial/valuation infrastructure:

```text
zpow_add_lower_factor
  : z^k + a*z^j = z^j * (z^(k-j) + a)
```

with `a!=0`, `j<k`; the second factor is nonzero at `z=0`, so the contact order is exactly `j`.

No radical-bearing theorem is required for the trusted cluster layer.

---

## 10. Recommended decision routing

After the factor/remainder normalization from T-P5-063/T-P5-064/T-P5-065:

- **remainder divisible by old monomial:** use T-P5-065 and retain the old contact coordinate;
- **nondivisible remainder, k=1:** use T-P5-066's transversality gate and recenter a unique simple zero;
- **nondivisible remainder, k>=2:** use T-P5-067 to create a rational root cluster and exact outer-sign reserve; quarantine the middle cell until source-specific root isolation/factorization is proved;
- never preserve the old multiplicity/parity inside that cluster from coefficient smallness alone.

This split is sharp already for quadratic examples.

---

## 11. Status / non-claims

This is a **pending mathematical child** only.

It does not claim:

- a concrete deployed P5 factor has multiplicity `k>=2`;
- source CSE has supplied the packet `u,e,m,eps,k`;
- any actual root count inside a concrete middle cell;
- Float64/controller/FD realization;
- P8 coverage;
- Lean/kernel compilation;
- P5/M4 or registry admission.

The next smallest child, only if a concrete multiple-contact source requires it, would be a polynomial-degree/derivative-controlled **root isolation inside the cluster**. Until then, the three-cell outer-sign certificate is the maximal source-independent closure justified by the available hypotheses.
