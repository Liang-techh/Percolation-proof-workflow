---
kind: review_result
review_id: review-T-P5-065-relative-remainder-absorption-kuangmanmozun-20260908T0344
task_id: T-P5-065-RELATIVE-REMAINDER-ABSORPTION
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-08T03:30:00-06:00
created_at: 2026-09-08T03:44:00-06:00
claim_commit: 7478825892f97f8c369bc52be49426763b59c15f
inspected_commit: 71cb0572f48238f48576dfa14f79c081e5daff70
parent_tasks:
  - T-P5-063-UNDERCANCELLED-AGGREGATE-GATE
  - T-P5-064-ANALYTIC-UNIT-PULLBACK
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add a fail-closed approximate-factorization bridge that absorbs certified same/higher-order remainders into a nonvanishing unit, preserves valuation/parity exactly, and exposes a sharp division-free cell-width gate
---

# T-P5-065 — relative remainder absorption and factor-stability gate

## 0. Bottleneck and non-overlap

T-P5-063 gives the exact aggregate valuation/parity gate once active factors are represented by monomials in independent source coordinates. T-P5-064 extends this to exact monomial-times-nonvanishing-unit factorizations

`h_a(z)=u_a(z) M_a(z)`,

with `M_a(z)=prod_j z_j^(W_aj)`, but explicitly leaves the **approximate-factorization / remainder-to-exact-factor theorem** open.

That missing seam matters in practice: factor discovery or Taylor/CSE analysis may produce

`h = u M + r`

rather than literal exact equality `h=uM`. A small numerical or absolute remainder is not enough near `M=0`; it may change the contact order, parity, or create a hidden zero. The correct question is what remainder contract lets us absorb `r` into the unit without changing the T-P5-063/T-P5-064 structural decision layer.

This review proves a sharp relative-error gate, an exact divisibility-based absorption theorem, a higher-order rational cell-width corollary, and counterexamples showing why each hypothesis is needed.

No deployed CSE/source factorization, Float64/libm/FD/controller semantics, reachability/coverage, provenance, admission, or registry mutation is claimed.

---

## 1. Sharp punctured relative-remainder theorem

Let `D*` be the punctured part of a declared source cell and suppose `g(z) != 0` there. Let

`h(z)=g(z)+r(z)`

and assume an exact bound

**(1.1)** `|r(z)| <= alpha |g(z)|` for every `z in D*`, with `0 <= alpha < 1`.

Define `delta(z)=r(z)/g(z)` on `D*`. Then

`|delta(z)|<=alpha`,

hence

**(1.2)** `1-alpha <= 1+delta(z) <= 1+alpha`.

Therefore

**(1.3)** `h(z)=g(z)(1+delta(z))`,

with a strictly positive multiplicative correction. In particular,

**(1.4)** `sign(h)=sign(g)` on `D*`,

and

**(1.5)** `(1-alpha)|g| <= |h| <= (1+alpha)|g|`.

### Theorem 1.1 — integer-power structural stability

For every integer `E`, define

`c_low(E,alpha) = (1-alpha)^E` and `c_high(E,alpha)=(1+alpha)^E` when `E>=0`,

and reverse the two endpoints when `E<0`.

Then

**(1.6)**

`c_low(E,alpha) |g|^E <= |h|^E <= c_high(E,alpha) |g|^E`.

Thus a relative remainder strictly below 100% cannot change the pole/zero order of any integer-power consumer and cannot change its sign parity. It only multiplies the reduced packet by a positive bounded factor.

For many factors `h_a=g_a+r_a` with `alpha_a<1`, the full aggregate contact factor acquires exactly the positive multiplier

`V_E(z)=prod_a (1+delta_a(z))^(E_a)`.

Its rational envelope is obtained by multiplying the one-factor bounds in (1.6). Therefore the T-P5-063 valuation vector and parity mask remain unchanged.

### Sharpness of `alpha<1`

The strict threshold is optimal for a uniform theorem. At `alpha=1`, choose `r=-g`; then `h=0`. The nominal factor can be completely cancelled, so neither fixed sign nor the original valuation survives. Hence a checker must not replace `<1` by `<=1` if it wants a nonvanishing-unit conclusion.

This theorem is useful even when the quotient `delta` has not yet been proved continuous: it certifies **structural boundedness/order/sign stability on the punctured domain**. It does not by itself certify Lipschitz regularity; Section 5 gives the required extra contract.

---

## 2. Exact monomial-divisibility absorption theorem

For the kernel-facing route, the cleanest certificate avoids division by `g` entirely.

Let

`M_W(z)=prod_j z_j^(W_j)`, `W_j in N`,

and suppose the source proves the exact identities

**(2.1)** `g(z)=M_W(z) u(z)`,

**(2.2)** `r(z)=M_W(z) e(z)`.

Assume there is a fixed sign `sigma in {+1,-1}` and exact rational bounds

**(2.3)** `0 < m <= sigma u(z) <= M` on the full cell,

**(2.4)** `|e(z)| <= epsilon`, with `epsilon < m`.

Define

`u_tilde = u+e`.

Then exactly

**(2.5)** `h=g+r=M_W u_tilde`,

and

**(2.6)** `m-epsilon <= sigma u_tilde <= M+epsilon`.

Hence `u_tilde` is a genuine nonvanishing unit with the same certified sign as `u`, and T-P5-064 applies **without changing `W`, valuation transport, or parity transport**.

### Theorem 2.1 — fail-closed exact absorption

Under (2.1)–(2.4), replacing the nominal unit packet `(u,m,M)` by

`(u_tilde, m_tilde, M_tilde)` with

**(2.7)** `m_tilde = m-epsilon > 0`,

**(2.8)** `M_tilde = M+epsilon`

is sound. Every T-P5-063/T-P5-064 structural gate is unchanged; only the unit amplitude/Lipschitz budgets are recomputed with `(m_tilde,M_tilde)`.

The proof is just

`sigma(u+e) >= sigma u - |e| >= m-epsilon`

and the analogous upper bound. No square root, optimization, or floating arithmetic occurs.

### Why exact divisibility is the right trusted surface

A statement such as `|r| <= epsilon |M_W|` on the punctured cell lets one *define* `e=r/M_W` there and prove `|e|<=epsilon`, but it does not by itself provide a continuous or Lipschitz extension of `e` to the zero strata. For a formal reusable bridge, either

1. source/CSE proves the exact identity `r=M_W e`, or
2. source provides a separately certified extension of the normalized quotient.

Otherwise the structural order may be safe while the regularity contract remains open.

---

## 3. Higher-order remainder gives a division-free cell-width gate

A frequent Taylor/CSE situation is stronger:

**(3.1)** `r(z)=M_W(z) M_S(z) v(z)`,

where

`M_S(z)=prod_j z_j^(S_j)`, `S_j in N`,

and the declared box has

`|z_j| <= H_j`, `H_j>=0`.

If

**(3.2)** `|v(z)| <= B`,

then the normalized remainder is

`e=M_S v`

and therefore

**(3.3)** `|e| <= epsilon_cell := B prod_j H_j^(S_j)`.

Combining with Theorem 2.1 yields the exact rational condition

**(3.4) CELL GATE**

`B prod_j H_j^(S_j) < m`.

This is the useful checker form: it is multiplication-only and division-free. If all inputs are rationals, the decision is exact rational arithmetic.

### Corollary 3.1 — higher-order remainder absorption

If (3.1)–(3.2) hold and (3.4) passes, then

`h=M_W [u + M_S v]`

with the same sign and exponent vector `W`, and the new unit margin is at least

**(3.5)** `m_res = m - B prod_j H_j^(S_j) > 0`.

This is a concrete closure mechanism: shrink the source cell until the higher-order remainder fits under the unit margin.

### Same-order versus genuinely higher-order remainder

If `S=0`, shrinking the cell does not improve the gate; one simply needs the coefficient-level inequality `B<m`. If at least one extra order is present, shrinking the corresponding `H_j` drives the normalized remainder charge toward zero.

So the theorem separates two qualitatively different situations:

- **same-order uncertainty:** requires a true coefficient margin;
- **higher-order remainder:** can be absorbed locally by a sufficiently small certified cell.

### Sharp full-cell boundary

The strict inequality in (3.4) is also sharp for a uniform nonvanishing margin. In one dimension, take `u=m>0`, `M_S(H)=H^S`, and choose `v=-B` with `B H^S=m`. At `z=H`, the perturbed unit is zero. Thus equality gives at best a boundary-touching packet and cannot be admitted as a strictly nonvanishing unit on the declared closed cell.

---

## 4. Absolute smallness does NOT preserve contact order

A factor checker must normalize the remainder by the candidate monomial order. A tiny absolute error can dominate arbitrarily close to contact.

Take

**(4.1)** `g_epsilon(z)=z^2`,

**(4.2)** `r_epsilon(z)=epsilon z`, `epsilon>0`.

On a fixed box `|z|<=H`,

`||r_epsilon||_infty <= epsilon H`,

which can be made arbitrarily small by taking `epsilon` small. But

**(4.3)** `h_epsilon(z)=z^2+epsilon z = z(z+epsilon)`

has order **one**, not two, at `z=0`.

Thus the nominal exponent/parity packet changes for every `epsilon>0`, however tiny the absolute error is.

This rules out a tempting but invalid certificate rule:

> `sup |r| is numerically small => reuse the nominal zero factorization`.

Near a zero, the required notion is relative/same-order smallness or an exact divisibility statement, not raw `L_infinity` smallness.

The same counterexample shows why a lower-order remainder cannot be rescued by cell shrinking while retaining the old exponent: as `z->0`, `|epsilon z|/|z^2|=epsilon/|z| -> infinity`.

---

## 5. Structural stability is weaker than Lipschitz stability

The `alpha<1` gate preserves sign and valuation but does not control oscillation of the normalized remainder.

Take one variable, nominal factor `g(z)=z`, and for `z!=0`

**(5.1)** `r(z)=(1/2) z sin(1/z)`, with `r(0)=0`.

Then

`|r(z)| <= (1/2)|g(z)|`,

so Theorem 1.1 gives the same sign and first-order valuation:

`h(z)=z[1+(1/2)sin(1/z)]`,

and the bracket stays in `[1/2,3/2]`.

However the normalized correction `delta=(1/2)sin(1/z)` is not continuous at contact, and `h` is not Lipschitz near zero: phase changes of order one occur on `z`-separations of order `z^2`, while the corresponding function change is order `z`.

Therefore:

- `alpha<1` is enough for structural order/sign and boundedness transport;
- a T-P5-064 **continuous/Lipschitz** consumer budget additionally needs a regularity contract for the normalized remainder/unit.

Two exact interfaces are sufficient.

### Additive normalized remainder interface

If `r=M_W e` exactly and

`Lip(u)<=L_u`, `Lip(e)<=L_e`,

then

**(5.2)** `Lip(u_tilde) <= L_u + L_e`.

### Relative quotient interface

If `h=g(1+delta)`, `|delta|<=alpha<1`,

`m<=sigma u<=M`, `Lip(u)<=L_u`, and `Lip(delta)<=L_delta`, then

`u_tilde=u(1+delta)` satisfies

**(5.3)** `m(1-alpha) <= sigma u_tilde <= M(1+alpha)`,

and

**(5.4)** `Lip(u_tilde) <= (1+alpha)L_u + M L_delta`.

These are exact rational budgets whenever the input bounds are rational.

---

## 6. Consumer-level consequence for T-P5-063/T-P5-064

For each active factor `a`, suppose a nominal packet

`g_a = u_a prod_j z_j^(W_aj)`

is accompanied by an absorbable remainder satisfying either Theorem 2.1 or Corollary 3.1. Define the perturbed unit `u_tilde_a` and its positive margin.

Then the actual factors are **exactly**

**(6.1)** `h_a = u_tilde_a prod_j z_j^(W_aj)`.

Therefore for every already-aggregated nonlinear consumer with factor-space data `(E,beta)`, the source-coordinate transport remains exactly

**(6.2)** `E' = W^T E`,

**(6.3)** `beta' = W^T beta mod 2`.

Nothing about the remainder changes these integer/parity objects. The only price is replacement of T-P5-064's unit bounds by the perturbed-unit bounds.

This is particularly important for T-P5-063 under-cancelled consumers: negative individual/factor-space exponents are still allowed whenever the **pulled-back aggregate** gate passes. One must not separately charge the remainder as an additive singular term after it has been proven divisible and absorbed into the same unit; doing so would double-count the same uncertainty and can create a false obstruction.

---

## 7. Fail-closed decision protocol

For one proposed source factorization `h ~= u M_W`, the checker should classify the remainder in this order:

1. **Exact zero remainder:** consume T-P5-064 directly.
2. **Exact same/higher-order divisibility:** prove `r=M_W e`; require `sup|e|<m`. If `e=M_S v`, use the division-free gate `B H^S < m`.
3. **Relative punctured bound only:** if `|r|<=alpha|g|` with `alpha<1`, valuation/sign are stable on the punctured domain, but continuous/Lipschitz unit transport remains pending until the quotient regularity/extension is certified.
4. **Only absolute remainder bound:** do not reuse the nominal valuation/parity; lower-order contamination is still possible.
5. **Boundary `alpha=1` or `epsilon=m`:** classify as boundary-only / non-strict; do not manufacture a positive unit margin.
6. **Remainder not divisible by the nominal monomial:** either refactor using the true lowest order or return an obstruction. Do not hide the lower-order term in an `L_infinity` budget.

This protocol is compatible with T-P5-063 exact-CSE-first logic and T-P5-064 unit envelopes.

---

## 8. Lean-friendly theorem statements

The smallest useful formal leaves are source-independent and do not need `sqrt`.

### Leaf A — additive unit margin

```text
same_monomial_remainder_absorption
  (0 < m)
  (m <= sigma*u)
  (sigma*u <= M)
  (abs e <= eps)
  (eps < m)
  : m-eps <= sigma*(u+e) ∧ sigma*(u+e) <= M+eps
```

Core proof: `linarith [neg_abs_le e, le_abs_self e]` / ordered-ring arithmetic.

### Leaf B — higher-order cell charge

```text
higher_order_remainder_unit_margin
  (abs v <= B)
  (forall j, abs z_j <= H_j)
  (B * prod_j H_j^(S_j) < m)
  : abs (prod_j z_j^(S_j) * v)
      < m
```

Then feed Leaf A with `e=M_S*v`.

### Leaf C — relative sign stability

```text
relative_remainder_same_sign
  (abs r <= alpha * abs g)
  (0 <= alpha) (alpha < 1)
  (g != 0)
  : sign (g+r) = sign g
```

A division-free proof can instead show `(g+r)*g > 0` from

`|r| < |g|`.

### Leaf D — sharp boundary counterexample

`g=1`, `r=-1`, `alpha=1` gives `h=0`.

### Leaf E — lower-order contamination regression

`g=z^2`, `r=eps*z`, `eps>0`: the actual factor equals `z(z+eps)` and is not divisible by `z^2` as a polynomial/rational-function identity.

The finite-product/matrix exponent transport should continue to reuse T-P5-063/T-P5-064 rather than duplicating those proofs here.

---

## 9. Status and remaining obligations

**Mathematical result of this child:**

- strict relative error `<1` is the sharp uniform gate preserving punctured sign and valuation;
- exact remainder divisibility by the nominal monomial plus `epsilon<m` upgrades an approximate factorization to an exact nonvanishing-unit factorization;
- higher-order remainders admit the rational, division-free cell gate `B prod H_j^(S_j) < m`;
- equality is boundary-only and cannot yield a strict unit margin;
- arbitrary absolute smallness does not preserve contact order;
- structural remainder control alone does not imply Lipschitz regularity; normalized remainder regularity must be certified separately.

**Still open / not claimed here:**

- deployed CSE identities `r_a=M_{W_a}e_a`;
- actual exact rational `m_a,M_a,B_a,H_j,L_e` values;
- independence/reachability of the chosen source coordinates;
- reduced-packet bounds and P8/ODE coverage;
- Float64/libm/FD/controller remainder semantics;
- Lean compilation / kernel receipt;
- provenance, comparator, independent validation, admission, P5/P8/M4 closure, or registry mutation.

Admission remains **pending mathematical child**.
