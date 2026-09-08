---
kind: review_result
review_id: review-T-P5-064-analytic-unit-pullback-liuguanyi-20260908T0321
task_id: T-P5-064-ANALYTIC-UNIT-PULLBACK
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-08T03:05:00-06:00
created_at: 2026-09-08T03:21:00-06:00
claim_commit: 5e39140167c44fd0add97320288710302025c499
parent_tasks:
  - T-P5-061
  - T-P5-062-MULTIFACTOR-LIPSCHITZ-STRATA
  - T-P5-063-UNDERCANCELLED-AGGREGATE-GATE
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add a nonvanishing-unit pullback theorem showing that monomial valuation/parity transport survives multiplication by variable units, with exact rational unit budgets and a fail-closed lower-margin/sign contract
---

# T-P5-064 — nonvanishing analytic-unit pullback bridge

## 0. Bottleneck and non-overlap

T-P5-063 gives an exact correlated-source rescue when the source factors are *pure monomials up to constants*,

`h_a(z) = c_a * prod_j z_j^(W_aj)`,

and explicitly leaves **nonconstant analytic-unit transport** open. In actual local factorization one normally expects the more flexible normal-crossing form

`h_a(z) = u_a(z) * prod_j z_j^(W_aj)`,

where `u_a` is nonzero on the cell but is not constant.

The mathematical question is whether the T-P5-063 transport

`E' = W^T E`, `beta' = W^T beta mod 2`

remains sound, and if so what quantitative price must be paid for the variable unit.

This child proves that it does remain sound under an explicit nonvanishing-unit contract. The variable unit changes only a bounded/Lipschitz reduced multiplier; it does **not** change the pulled-back valuation or parity. It also gives a sharp obstruction showing why pointwise nonzero on a punctured domain is not enough.

No deployed-source factorization, Float64/libm, ODE/coverage, Lean compilation, provenance, independent validation, admission, or registry state is claimed here.

---

## 1. Exact monomial-times-unit packet

Let `z=(z_1,...,z_d)` be the independent source coordinates. For active factors `a=1,...,r`, assume the exact identity

**(1.1)**

`h_a(z) = u_a(z) * prod_j z_j^(W_aj)`,

with `W_aj in N`.

For one already-aggregated nonlinear consumer packet from T-P5-063, let

`E_a in Z`,

`beta_a in F_2`.

On the punctured coordinate set define

**(1.2)**

`Psi_(E,beta)(h) := prod_a sign(h_a)^(beta_a) |h_a|^(E_a)`.

The important source contract is not merely `u_a(z) != 0` pointwise. Fix signs `sigma_a in {+1,-1}` and exact positive bounds

**(1.3)**

`0 < m_a <= sigma_a u_a(z) <= M_a`

for every `z` in the same closed cell `D`.

Thus every unit has one certified sign on the cell and a uniform nonvanishing margin. For the quantitative result also assume

**(1.4)**

`|u_a(z)-u_a(w)| <= L_a ||z-w||_1`.

Analyticity is not needed by the trusted bridge once (1.1), (1.3), and (1.4) are available; analyticity is only one possible upstream way of proving them.

---

## 2. Exact unit-pullback identity

Define the same integer/parity transport as in T-P5-063:

**(2.1)**

`E'_j := sum_a W_aj E_a in Z`,

**(2.2)**

`beta'_j := (sum_a W_aj beta_a) mod 2`.

Also define the positive unit amplitudes

`v_a(z) := sigma_a u_a(z) > 0`

and the unit multiplier

**(2.3)**

`U_E(z) := prod_a v_a(z)^(E_a)`

using integer powers, together with the constant sign

**(2.4)**

`sigma_beta := prod_a sigma_a^(beta_a) in {+1,-1}`.

### Theorem 2.1 — exact monomial-times-unit transport

On the punctured coordinate set,

**(2.5)**

`Psi_(E,beta)(h(z))`

`= sigma_beta * U_E(z)`

`  * prod_j sign(z_j)^(beta'_j) |z_j|^(E'_j)`.

### Proof

For each `a`, exact factorization gives

`sign(h_a) = sigma_a * prod_j sign(z_j)^(W_aj)`

and

`|h_a|^(E_a) = v_a^(E_a) * prod_j |z_j|^(W_aj E_a)`

whenever the relevant factors are nonzero. Multiplying over `a`, the source-coordinate magnitude exponents collect to

`sum_a W_aj E_a = E'_j`,

while sign exponents are reduced modulo two to

`sum_a W_aj beta_a = beta'_j mod 2`.

The remaining factors are exactly `sigma_beta U_E(z)`.

**Key consequence:** a genuinely nonvanishing variable unit does not alter the valuation vector or the parity mask. It is a multiplicative reduced-packet factor only.

---

## 3. Structural gate is invariant under nonvanishing units

Because of (1.3), `U_E` is finite and strictly positive on the whole cell even when some `E_a<0`. In fact it has a positive lower bound and finite upper bound derived below.

Let

`P_(E',beta')(z) := prod_j sign(z_j)^(beta'_j) |z_j|^(E'_j)`.

Then (2.5) is simply

`Psi(h(z)) = sigma_beta U_E(z) P(z)`.

### Theorem 3.1 — universal boundedness gate survives units

Assume the source coordinates range over a full product box around the relevant coordinate strata and (1.3) holds. Then the following are equivalent:

1. `Psi(h(z)) R(z)` is bounded for every bounded reduced packet `R`;
2. `E'_j >= 0` for every source coordinate `j`.

### Proof

If every `E'_j>=0`, `P` is bounded on the box and `U_E` is bounded above, so the product is bounded.

Conversely, choose `R=1`. If some `E'_j<0`, fix every other source coordinate nonzero and let `z_j -> 0`. The pure contact factor `|z_j|^(E'_j)` diverges. Since (1.3) gives a strictly positive lower bound for `U_E`, the variable unit cannot suppress that pole. Hence the product is unbounded.

### Theorem 3.2 — universal continuous/Lipschitz contact gate survives units

Under the same full-box assumptions, and with continuous units satisfying (1.3), the universal contact factor has a continuous extension through every coordinate stratum if and only if for every `j`,

**(3.1)**

`E'_j > 0`,

or

`E'_j = 0 and beta'_j = 0`.

With the Lipschitz hypotheses (1.4), the same condition yields a locally/globally Lipschitz extension on the certified box.

Necessity is preserved because `U_E` has a positive lower bound: it can neither hide a pole nor cancel a zero-order odd sign jump. Sufficiency follows by multiplying the T-P5-062 contact extension by the continuous/Lipschitz unit multiplier.

Thus the exact T-P5-063 structural decision layer survives replacement of constant `c_a` by variable nonvanishing units.

---

## 4. Exact rational quantitative budget for integer unit powers

Assume all `m_a,M_a,L_a` are exact rationals and satisfy

`0 < m_a <= M_a`, `L_a>=0`.

For one integer exponent `n`, define an upper amplitude factor

**(4.1)**

`B(n;m,M) :=`

- `M^n` if `n>=0`,
- `m^n = 1/m^(-n)` if `n<0`.

Define a positive lower amplitude factor

**(4.2)**

`b(n;m,M) :=`

- `m^n` if `n>=0`,
- `M^n = 1/M^(-n)` if `n<0`.

Finally define the Lipschitz charge

**(4.3)**

`C(n;m,M,L) :=`

- `0` if `n=0`,
- `n M^(n-1) L` if `n>0`,
- `(-n) m^(n-1) L` if `n<0`.

For `n=-d<0`, the last line is exactly

`d m^(-d-1) L`,

the standard reciprocal-power derivative bound.

### Lemma 4.1 — one-unit integer-power bound

If `m <= v(z),v(w) <= M` and `|v(z)-v(w)|<=L||z-w||_1`, then

**(4.4)**

`b(n;m,M) <= v(z)^n <= B(n;m,M)`,

and

**(4.5)**

`|v(z)^n-v(w)^n| <= C(n;m,M,L) ||z-w||_1`.

For positive `n`, use the finite difference-of-powers factorization. For negative `n=-d`, write

`x^(-d)-y^(-d) = (y^d-x^d)/(x^d y^d)`

and use `x,y>=m`; equivalently apply the mean-value bound on `[m,M]`.

No floating arithmetic or square root is needed.

---

## 5. Product unit budget

For each factor set

`B_a := B(E_a;m_a,M_a)`,

`b_a := b(E_a;m_a,M_a)`,

`C_a := C(E_a;m_a,M_a,L_a)`.

Then define

**(5.1)**

`B_U := prod_a B_a`,

**(5.2)**

`b_U := prod_a b_a > 0`,

and

**(5.3)**

`L_U := sum_a C_a * prod_(c != a) B_c`.

### Theorem 5.1 — exact unit multiplier envelope

For every `z,w` in the certified cell,

**(5.4)**

`b_U <= U_E(z) <= B_U`,

and

**(5.5)**

`|U_E(z)-U_E(w)| <= L_U ||z-w||_1`.

The proof is the standard telescoping product estimate. Because every input is rational and every exponent is an integer, `B_U,b_U,L_U` are exact rationals.

The lower bound `b_U>0` is not bookkeeping: it is exactly what makes the structural *necessity* direction in Section 3 valid.

---

## 6. Composition with the T-P5-062 source-coordinate contact factor

Assume the transported packet passes the structural gate:

`E'_j>=0`, and `beta'_j=0` whenever `E'_j=0`.

Let the source box satisfy

`|z_j|<=H_j`, `H_j>0` rational.

Define

**(6.1)**

`B_P := prod_j H_j^(E'_j)`.

For the `l1` metric define the T-P5-062 contact Lipschitz constant

**(6.2)**

`L_P := max_(j:E'_j>0)`

`  [ E'_j H_j^(E'_j-1) prod_(k != j) H_k^(E'_k) ]`,

with `L_P=0` if every `E'_j=0`.

Now suppose the remaining reduced packet `R` satisfies

`|R(z)|<=M_R`,

`|R(z)-R(w)|<=L_R ||z-w||_1`.

### Theorem 6.1 — full monomial consumer budget

The extended monomial

`F(z)=sigma_beta U_E(z) P_(E',beta')(z) R(z)`

satisfies

**(6.3) sup bound**

`|F(z)| <= B_U B_P M_R`,

and

**(6.4) Lipschitz bound**

`Lip(F) <=`

`L_U B_P M_R`

`+ B_U L_P M_R`

`+ B_U B_P L_R`.

### Proof

Use

`UPR - U'P'R'`

`= (U-U')PR + U'(P-P')R + U'P'(R-R')`

and apply the three uniform envelopes.

This is the precise quantitative price of replacing T-P5-063's constants `c_a` by variable units: one extra multiplicative amplitude budget and one additive Lipschitz charge. The valuation/parity gate itself is unchanged.

---

## 7. Exact rational worked example

Take one independent coordinate with

`|z|<=1/2`,

and two source factors

**(7.1)**

`h_1(z)=(2+z) z`,

`h_2(z)=(3-z) z^2`.

The units are positive on the whole box:

`3/2 <= 2+z <= 5/2`,

`5/2 <= 3-z <= 7/2`,

and both have Lipschitz constant `1`.

Choose aggregate packet

`E=(-1,+1)`,

`beta=(1,1)`.

The exponent matrix is `W=(1,2)^T`, hence

`E' = -1 + 2 = 1`,

`beta' = 1 + 2 = 1 mod 2`.

Therefore

**(7.2)**

`Psi(h(z)) = U(z) * sign(z)|z| = U(z) z`,

with

`U(z)=(3-z)/(2+z)`.

The generic rational unit budgets are

for `(2+z)^(-1)`:

`B_1=2/3`, `b_1=2/5`, `C_1=4/9`;

for `(3-z)`:

`B_2=7/2`, `b_2=5/2`, `C_2=1`.

Hence

**(7.3)**

`1 <= U(z) <= 7/3`,

and

**(7.4)**

`Lip(U) <= (4/9)(7/2) + (2/3)(1) = 20/9`.

For `P(z)=z`, `B_P=1/2`, `L_P=1`. With `R=1`, Theorem 6.1 gives the completely rational whole-consumer bound

**(7.5)**

`Lip(Psi) <= (20/9)(1/2) + 7/3 = 31/9`.

This example also shows why individual negative unit exponents are harmless once a true nonvanishing margin is available: the reciprocal unit is just another bounded rationally-controlled factor.

---

## 8. Sharp obstruction: pointwise nonzero on the punctured set is NOT enough

The lower-margin hypothesis in (1.3) cannot be weakened to

`u(z) != 0 whenever z != 0`.

Take one coordinate and deliberately misclassify

**(8.1)**

`h(z)=u(z)`, `W=0`, `u(z)=z`

on the punctured interval `0<|z|<=1`.

For packet

`E=-1`, `beta=0`,

the formal monomial transport with `W=0` gives

`E'=0`, `beta'=0`,

which would look completely safe if `u` were treated as a genuine unit.

But the actual factor is

**(8.2)**

`Psi(h(z))=1/|z|`,

which diverges.

The failure is exactly that `u` has no positive lower bound on the closure and actually contains a hidden zero factor.

An equally sharp parity version uses `E=0,beta=1`: pure transport with `W=0` would predict no source-coordinate parity, while the actual factor is `sign(z)` and jumps across the contact.

**Conclusion:** any zero or sign change of a purported unit must be promoted into the explicit factor/exponent packet. It cannot remain hidden inside `u_a`.

---

## 9. Connected-cell / sign boundary

If `u_a` is continuous and nonzero on a connected compact cell, its sign is automatically constant and a positive minimum exists. However, the theorem interface should still consume an explicit rational sign/lower-bound packet rather than rely on topology or an unevaluated existential minimum.

On a disconnected source domain, a nonzero continuous `u_a` may have different signs on different components. Then there is no single global `sigma_a`; either:

1. split the source cell into sign-stable components, or
2. carry the component sign as a discrete reachable-state key and fold it into the T-P5-061 sign-action layer.

Silently choosing one sign would lose a real discrete contact degree of freedom.

---

## 10. Exactness boundary for approximate factorization

This bridge requires the factor identity (1.1) to be exact on the declared cell. A packet of the form

`h_a = u_a prod_j z_j^(W_aj) + remainder_a`

cannot be sent through the exponent transport without an additional zero-location / domination theorem. Even a small additive remainder can move or remove a zero surface and therefore change valuation and parity.

Thus source code should either:

- prove an exact factor identity and then use this bridge, or
- keep the remainder as a separate source obligation and prove a stronger local factor theorem before declaring `W`.

Numerical closeness of `h_a` to a monomial-times-unit expression is not a valuation certificate.

---

## 11. Minimal typed source-to-math contract

For each factor `a`, the smallest useful packet is:

- exact natural exponents `W_aj`;
- exact same-cell identity `h_a = u_a * prod_j z_j^(W_aj)`;
- a sign bit `sigma_a in {+1,-1}`;
- rational `m_a,M_a,L_a` with `0<m_a<=sigma_a u_a<=M_a` and `Lip_1(u_a)<=L_a`;
- the same source-coordinate box radii `H_j` used by the contact consumer.

For each canonical consumer monomial, the symbolic layer provides only:

- aggregate integer valuation `E`;
- parity mask `beta`;
- reduced-packet sup/Lipschitz bounds `M_R,L_R`.

The math adapter deterministically computes:

`E'=W^T E`,

`beta'=W^T beta mod 2`,

`B_U,b_U,L_U`,

then either rejects on the structural gate or returns the exact rational `B_F,L_F` from Section 6.

This keeps factor discovery/source semantics separate from the trusted valuation and inequality layer.

---

## 12. Lean-friendly theorem leaves

No Lean lane is claimed. The smallest formal statements are:

1. `unit_monomial_integer_pullback_identity`
   - exact identity (2.5) on the punctured source set;
   - integer exponents may be represented as positive/negative natural parts if avoiding a broad `zpow` API.

2. `integer_power_bounds_of_positive_interval`
   - prove (4.4) for `m<=v<=M`, `m>0`.

3. `integer_power_lipschitz_of_positive_interval`
   - prove (4.5), splitting `n>0`, `n=0`, `n<0`.

4. `finite_product_unit_envelope`
   - prove (5.4) and (5.5) by a finite telescoping product.

5. `unit_pullback_bounded_iff`
   - under `b_U>0`, universal boundedness iff every `E'_j>=0`.

6. `unit_pullback_contact_safe_iff`
   - under `b_U>0`, universal continuity iff positive valuation or zero valuation with even parity coordinatewise.

7. `unit_contact_times_reduced_lipschitz`
   - prove the three-term composition bound (6.4).

8. `hidden_zero_not_unit_counterexample`
   - `u(z)=z`, `W=0`, `E=-1` gives the regression `1/|z|`.

The structural leaves 5–6 need only a positive lower bound for the unit multiplier; the quantitative leaves 2–4 consume explicit rational intervals and Lipschitz constants.

---

## 13. Status boundary

**Result:** mathematical/interface child complete; integration pending.

**Closed here:**

- exact transport for `h_a=u_a(z) prod_j z_j^(W_aj)`;
- proof that variable nonvanishing units leave `E'=W^T E` and `beta'=W^T beta mod 2` unchanged;
- universal boundedness/contact regularity equivalence under a positive unit lower bound;
- exact rational upper/lower/Lipschitz budgets for positive and negative integer unit powers;
- product-unit and full monomial Lipschitz composition bounds;
- an exact rational worked example;
- sharp hidden-zero/sign obstruction when the lower-margin contract is omitted;
- connected/disconnected sign boundary and exact-factorization boundary.

**Still open / not claimed:**

- concrete deployed CSE factorization into explicit `u_a,W`;
- proof that the chosen source coordinates are independent on the declared cell;
- actual rational `m_a,M_a,L_a` source enclosures;
- reduced-packet `M_R,L_R` bounds;
- source reachability and partial-stratum coverage;
- approximate-factorization / remainder-to-exact-factor theorem;
- Float64/libm/FD/controller/solve semantics;
- P8/ODE interface and trajectory coverage;
- Lean/kernel compilation;
- comparator/receipt/provenance;
- independent final validation by 封不觉;
- parent closure, P5/P8/M4 admission, or registry mutation.
