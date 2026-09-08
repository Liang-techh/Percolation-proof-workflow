---
kind: review_result
review_id: review-T-P5-070-triangular-multicontact-chart-guyuefangyuan-20260908T0545
task_id: T-P5-070-TRIANGULAR-MULTICONTACT-CHART
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-08T05:31:00-06:00
created_at: 2026-09-08T05:45:00-06:00
claim_commit: 1c0dd7f77e7f68f42b8d16768e1ff94b68c1787d
inspected_commits:
  - 3a4784366f29802d446f6c859ab528c99dd49a07
  - 6b4685d7e8952aa50de8f284247f96076987cb37
  - cfe49413a024e86c3b282af469797327d095799e
parent_tasks:
  - T-P5-066-ZERO-SURFACE-RECENTERING
  - T-P5-068-RECENTERED-UNIT-C11
  - T-P5-064-ANALYTIC-UNIT-PULLBACK
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add a source-independent finite triangular multi-contact recentering theorem after the scalar simple-root bridge; use it only when the source dependency graph is certified acyclic/triangular, and keep cyclic implicit systems, concrete source binding, Lean validation, coverage and admission separate
---

# T-P5-070 — finite triangular multi-contact recentering chart

## 0. Mathematical seam and non-overlap

T-P5-066 already closes the scalar parameterized root-graph problem. T-P5-068 then closes the C1,1 regularity of one recentered divided-difference unit, including its parameterized chart bound. T-P5-064 can transport valuation/parity once the source really has independent contact coordinates with nonvanishing units.

The remaining seam is **simultaneous geometry**: several simple zero surfaces may move together. Per-factor scalar simplicity does not by itself prove that the factors can be straightened into a common product chart. T-P5-066 explicitly leaves `multi-factor/intersection coordinate charts` open.

This child proves a strong exact theorem for the smallest structured class beyond independent fibers: a finite **acyclic/triangular dependency order**. Contact `i` may depend arbitrarily strongly on earlier physical contact variables, but never on later ones. The key payoff is that no contraction/small-gain hypothesis is needed. The chart inverse is controlled by a finite nilpotent polynomial.

This is mathematics only. It does not inspect or claim deployed CSE identities, Float64/libm, P8/ODE coverage, receipt/provenance, kernel compilation, admission, or registry mutation.

---

## 1. Triangular source packet

Let the base parameter space be a metric space `(Y,d)`. Let there be `n` scalar contact variables

`x = (x_1,...,x_n)`

with closed source intervals

`I_i = [c_i-H_i, c_i+H_i]`, `H_i>0`.

For each `i`, write the earlier physical coordinates as

`z = x_{<i} = (x_1,...,x_{i-1})`.

Assume a scalar factor

`h_i(s,z,y)`

with contact variable `s in I_i`, earlier variables `z in prod_{j<i} I_j`, and `y in Y`.

Fix signs `sigma_i in {+1,-1}` and exact constants

`0 < mu_i <= M_i`.

### 1.1 Uniform signed secants in the active contact coordinate

For all fixed `(z,y)` and all `s<t` in `I_i`, assume

**(1.1)**

`mu_i*(t-s)`
`<= sigma_i*(h_i(t,z,y)-h_i(s,z,y))`
`<= M_i*(t-s)`.

Assume each fiber has its unique scalar root

**(1.2)** `rho_i(z,y) in I_i`, `h_i(rho_i(z,y),z,y)=0`.

The existence/uniqueness can be supplied by T-P5-066's endpoint-sign/transversality theorem; it is not reproved here.

### 1.2 Cross-variable and base-parameter variation

Assume nonnegative exact coefficients `C_ij` for `j<i` and `L_i` such that at fixed contact argument `s`,

**(1.3)**

`|h_i(s,z,y)-h_i(s,z',y')|`
`<= sum_{j<i} C_ij |z_j-z'_j| + L_i d(y,y')`.

For division-free consumption, let the checker provide rational nonnegative numbers

`a_ij`, `b_i`

satisfying

**(1.4)** `C_ij <= mu_i a_ij`,

**(1.5)** `L_i <= mu_i b_i`.

No division by `mu_i` is needed in the stored certificate.

---

## 2. Scalar root transport with several transverse variables

Take two parameter points `(z,y)` and `(z',y')`, with roots

`r = rho_i(z,y)`, `r' = rho_i(z',y')`.

Suppose first `r<=r'`. The lower signed-secant bound in the first fiber gives

`mu_i(r'-r)`
`<= sigma_i(h_i(r',z,y)-h_i(r,z,y))`
`= sigma_i h_i(r',z,y)`.

Since `h_i(r',z',y')=0`,

`|h_i(r',z,y)|`
`= |h_i(r',z,y)-h_i(r',z',y')|`
`<= sum_{j<i} C_ij |z_j-z'_j| + L_i d(y,y')`.

The case `r'>r` reversed is identical after swapping the two fibers. Therefore:

**Theorem 2.1 — multi-parameter root variation**

**(2.1)**

`mu_i |rho_i(z,y)-rho_i(z',y')|`
`<= sum_{j<i} C_ij |z_j-z'_j| + L_i d(y,y')`.

Using (1.4)-(1.5), the division-free normalized consequence is

**(2.2)**

`|rho_i(z,y)-rho_i(z',y')|`
`<= sum_{j<i} a_ij |z_j-z'_j| + b_i d(y,y')`.

This is exactly the scalar T-P5-066 root-graph argument, but with all earlier contact coordinates retained explicitly rather than collapsed into one opaque parameter metric.

---

## 3. Exact triangular contact coordinates

Define the forward recentered coordinates recursively by

**(3.1)**

`xi_i = x_i - rho_i(x_{<i},y)`.

Because `rho_i` depends only on earlier physical coordinates, the inverse is also recursive:

**(3.2)**

`x_1 = xi_1 + rho_1(y)`,

`x_i = xi_i + rho_i(x_{<i},y)` for `i>=2`.

There is no implicit simultaneous solve in (3.2). Once `x_1,...,x_{i-1}` have been reconstructed, the next line is explicit.

### Theorem 3.1 — exact triangular invertibility

On every domain on which all root maps are defined, (3.1) and (3.2) are mutual inverses.

### Proof

Forward followed by inverse is immediate by induction. At step `i`, all earlier coordinates have already been reconstructed exactly, so the same `rho_i(x_{<i},y)` is subtracted and added. The reverse direction is the same induction.

Thus an acyclic source dependency order gives a genuine contact-coordinate chart without an inverse-function theorem and without solving a coupled nonlinear system.

---

## 4. Nilpotent exact-rational Lipschitz budget

Let `A` be the strictly lower-triangular nonnegative matrix

**(4.1)** `A_ij = a_ij` for `j<i`, and `A_ij=0` otherwise.

Let `b=(b_i)`.

For two physical/chart points define componentwise nonnegative difference vectors

`X_i = |x_i-x'_i|`,

`Xi_i = |xi_i-xi'_i|`,

and `D=d(y,y')`.

From (2.2) and the forward coordinate definition,

**(4.2)**

`Xi <= (I+A) X + b D`

componentwise.

For the inverse recursion,

**(4.3)**

`X <= Xi + A X + b D`.

Because `A` is strictly lower triangular of size `n`,

**(4.4)** `A^n = 0`.

Define the finite nonnegative matrix

**(4.5)**

`S = I + A + A^2 + ... + A^(n-1)`.

Iterating (4.3) exactly `n` times yields

`X <= (I+A+...+A^(n-1))(Xi+bD) + A^n X`.

The last term vanishes. Hence:

**Theorem 4.1 — exact inverse chart budget**

**(4.6)**

`X <= S (Xi + b D)`

componentwise.

This is the main quantitative result. Every entry of `S` is a finite polynomial with nonnegative integer coefficients in the rational `a_ij`. Therefore the trusted checker needs only exact rational addition and multiplication.

### Important structural consequence

There is **no small-gain condition** such as `||A||<1`.

Acyclicity is enough because `A` is nilpotent. Cross-coupling can be numerically huge and the chart still has a finite exact inverse budget.

---

## 5. Optional scalar l1 constants

T-P5-064/T-P5-062 often consume l1-type budgets. The componentwise theorem can be compressed without losing soundness.

Define the exact rational column-sum constants

**(5.1)**

`C_inv = max_j sum_i S_ij`,

`B_inv = sum_i (S b)_i`.

Then (4.6) gives

**(5.2)**

`sum_i X_i <= C_inv sum_i Xi_i + B_inv D`.

Similarly define

**(5.3)**

`C_fwd = max_j sum_i (I+A)_ij`,

`B_fwd = sum_i b_i`.

From (4.2),

**(5.4)**

`sum_i Xi_i <= C_fwd sum_i X_i + B_fwd D`.

Thus the triangular contact chart and its inverse are bi-Lipschitz on every common domain where they are both defined, with entirely rational constants.

The componentwise packet (4.2)/(4.6) is preferable as the canonical certificate; scalar norms can be derived downstream.

---

## 6. Common product core

A chart is useful only if a product neighborhood is guaranteed to remain inside the original source box.

Assume the source lane also provides exact rational displacement envelopes, uniform over all earlier coordinates and base parameters,

**(6.1)**

`|rho_i(z,y)-c_i| <= delta_i`,

with

**(6.2)** `0 <= delta_i < H_i`.

Define the recentered half-widths

**(6.3)** `K_i = H_i-delta_i > 0`.

Consider any chart point satisfying

**(6.4)** `|xi_i| <= K_i` for all `i`.

Reconstruct physical coordinates by (3.2). Inductively, the earlier reconstructed coordinates lie in their source intervals, so the next root bound (6.1) is applicable. Then

`|x_i-c_i|`
`<= |xi_i| + |rho_i(x_{<i},y)-c_i|`
`<= K_i+delta_i = H_i`.

Therefore:

**Theorem 6.1 — common triangular product core**

**(6.5)**

`prod_i [-K_i,K_i]`

in recentered coordinates maps entirely into

`prod_i I_i`

for every certified base parameter `y`.

This is the multi-contact analogue of T-P5-066's one-dimensional common core.

---

## 7. Simultaneous exact factorization

At a physical point `(x,y)`, set `z=x_{<i}` and

`r_i = rho_i(z,y)`.

By the signed-secant packet, define a recentered factor `v_i` exactly as in T-P5-066:

`h_i(x_i,z,y) = (x_i-r_i) v_i(x,y)`

with

**(7.1)**

`mu_i <= sigma_i v_i(x,y) <= M_i`.

But `x_i-r_i` is exactly `xi_i`. Hence on the triangular chart,

**Theorem 7.1 — simultaneous triangular normal-crossing form**

**(7.2)**

`h_i = xi_i * v_i`

for every `i`, with every `v_i` uniformly nonvanishing.

The word `normal-crossing` here is used only for this explicit triangular product chart; no claim is made about arbitrary analytic varieties.

If the actual shifted factors are C1,1 in their active coordinate with a joint parameter derivative packet, T-P5-068 can be applied to each row with parameter

`(x_{<i},y)`

and then transported through Theorem 4.1. Thus unit regularity is not reproved here.

Once those unit bounds are available, T-P5-064 may consume the factors as variable nonvanishing units times the **true independent chart coordinates** `xi_i`. The valuation/parity layer then no longer needs to pretend that the old nominal coordinates remained fixed after root displacement.

---

## 8. Exact positive control: large triangular coupling needs no contraction

Take two contacts with no base parameter,

`h_1(x_1)=x_1`,

`h_2(x_2,x_1)=x_2-100 x_1`.

Both active-coordinate derivatives are exactly `1`; both scalar roots are simple:

`rho_1=0`,

`rho_2(x_1)=100 x_1`.

The contact chart is

`xi_1=x_1`,

`xi_2=x_2-100 x_1`.

Here

`A = [[0,0],[100,0]]`,

so `A^2=0` and

`S=I+A = [[1,0],[100,1]]`.

The inverse is exactly

`x_1=xi_1`,

`x_2=xi_2+100 xi_1`.

A contraction test based on a norm of `A` would reject this system because the coupling is `100`, but the triangular chart is perfectly invertible. This is why nilpotence, not smallness, is the right certificate for an acyclic dependency graph.

---

## 9. Sharp obstruction: simple fibers do not solve a cyclic contact system

The triangular hypothesis is real structure, not a cosmetic ordering convention.

Take two cyclic factors

**(9.1)**

`h_1(x_1,x_2)=x_1-a x_2`,

`h_2(x_1,x_2)=x_2-b x_1`.

For every fixed transverse variable, each factor is a perfect simple scalar contact: the active derivative is exactly `1`, and the scalar root maps are

`rho_1(x_2)=a x_2`,

`rho_2(x_1)=b x_1`.

Yet the simultaneous contact map is

`xi = [[1,-a],[-b,1]] x`,

whose determinant is

**(9.2)** `1-ab`.

If `ab=1`, the two zero equations have an entire line of common zeros and there is no unique simultaneous contact center. The chart is singular even though **each individual scalar fiber is uniformly simple**.

If `ab != 1`, the inverse exists but carries the factor `1/(1-ab)`, which becomes arbitrarily large as `ab -> 1`.

Therefore:

- per-factor T-P5-066 PASS does not imply a simultaneous multi-factor chart;
- a cyclic dependency graph cannot be silently treated as triangular;
- cycles require a separate determinant/M-matrix/small-gain/implicit-function certificate;
- the present theorem is exact and nonconservative on the acyclic triangular class, but intentionally fail-closed outside it.

This is the required counterexample-guided boundary.

---

## 10. Source/checker decision layer

A source adapter should first build the dependency graph of shifted simple contacts.

If an exact topological order exists, it may emit:

- the ordered factor identities `h_i(s,x_<i,y)`;
- scalar T-P5-066 root witnesses/packets for every fiber;
- `mu_i,M_i`;
- cross-variation bounds `C_ij,L_i`;
- rational normalized charges `a_ij,b_i` proving `C_ij<=mu_i a_ij`, `L_i<=mu_i b_i`;
- uniform root displacement bounds `delta_i<H_i`.

The trusted math layer then constructs `A`, the finite nilpotent sum `S`, the common core, and the exact simultaneous factorization.

If the graph contains a directed cycle, this theorem must return `NOT_APPLICABLE`, not `FAIL`. A cycle is not itself a proof of non-invertibility; Section 9 only proves that simplicity alone no longer suffices. The source must switch to a cyclic implicit-system certificate.

---

## 11. Lean-friendly theorem decomposition

The minimal formal leaves are algebraically small.

### Leaf A — root variation with several parameters

```text
root_variation_of_signed_secant_and_cross_bound
  (h r z y = 0) (h r' z' y' = 0)
  (uniform lower signed secant mu)
  (crossBound:
    |h s z y - h s z' y'|
      <= sum j<i, C j * |z j-z' j| + L*d y y')
  : mu*|r-r'|
      <= sum j<i, C j * |z j-z' j| + L*d y y'
```

### Leaf B — division-free normalized root bound

```text
root_variation_of_scaled_charges
  (C j <= mu*a j)
  (L <= mu*b)
  (0 < mu)
  : |r-r'| <= sum j<i, a j*|dz j| + b*d
```

### Leaf C — finite triangular inverse by induction

Avoid a broad matrix API if desired. For `Fin n`, prove by induction that the recursion

`X_i <= Xi_i + sum_{j<i} a_ij X_j + b_i D`

produces explicit finite coefficients. A matrix version may state

```text
strictLower_pow_card_eq_zero
triangular_inverse_bound
  (X <= Xi + A*X + b*D)
  (A strictlyLower nonnegative)
  : X <= (sum k in range n, A^k) * (Xi+b*D)
```

### Leaf D — common recentered core

```text
triangular_core_subset
  (forall i z y, |rho_i z y-c_i| <= delta_i)
  (delta_i <= H_i)
  (|xi_i| <= H_i-delta_i)
  : reconstructed x_i in I_i
```

### Leaf E — simultaneous factorization

```text
triangular_contacts_factor
  (h_i (rho_i z y) z y = 0)
  (signed secant packet)
  : exists v_i,
      h_i x_i z y = xi_i*v_i
      ∧ mu_i <= sigma_i*v_i
      ∧ sigma_i*v_i <= M_i
```

### Regression leaf

`cyclic_simple_contacts_can_be_singular` with `a=b=1` is enough to prevent any later theorem from dropping the acyclicity/extra cyclic-invertibility premise.

No Lean compilation is claimed by this review.

---

## 12. Remaining boundary

**Closed mathematically here:**

- root variation for a simple contact depending on finitely many earlier contact variables;
- exact recursive forward/inverse chart for a certified triangular dependency order;
- finite exact-rational inverse Lipschitz packet `S=I+A+...+A^(n-1)`;
- proof that no contraction/small-gain condition is needed in the triangular class;
- common multi-contact product core from uniform root displacement bounds;
- simultaneous exact factorization `h_i=xi_i v_i` with nonvanishing units;
- cyclic two-contact obstruction proving that per-fiber simplicity alone is insufficient.

**Still open / not claimed:**

- whether the deployed factor graph is actually acyclic after exact source factorization;
- concrete `C_ij,L_i,mu_i,M_i,delta_i,H_i`;
- source independence/coverage of the resulting chart;
- cyclic contact systems and an exact determinant/M-matrix/implicit-function certificate;
- multiple roots/root clusters (T-P5-067 lane);
- C1,1 unit bounds beyond invoking T-P5-068 on each triangular row;
- reduced-packet bounds after the full chart substitution;
- Float64/libm/FD/controller/solve semantics;
- P8/ODE coverage;
- Lean/kernel/comparator/receipt/provenance;
- independent validation by 封不觉;
- P5/P8/M4 parent closure, admission, or registry mutation.

The main structural advance is that **acyclic zero-surface coupling admits exact simultaneous recentering with a finite rational polynomial budget, even when the cross-couplings are arbitrarily large**. Cyclic coupling is a genuinely different mathematical regime and must not be inferred safe from scalar simple-root certificates alone.