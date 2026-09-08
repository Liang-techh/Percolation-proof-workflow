---
kind: review_result
review_id: review-T-P5-072-signed-simple-cycle-contact-guyuefangyuan-20260908T0648
task_id: T-P5-072-SIGNED-SIMPLE-CYCLE-CONTACT
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-08T06:31:00-06:00
created_at: 2026-09-08T06:48:00-06:00
claim_commit: 0bb60e65d7a64974dd44032965baca0f43f71ecc
inspected_commits:
  - a3aca25105c5523ed4c0d98ef2a7c3aa8353e14a
  - 628211d6ff10ed09c10eb0380539048ec24c0459
  - 5a298beed9a85c918c75c8cbe02027b1b897d8e0
  - f2dfaec6a9ab3e7cb81f613feb2b13dd27d5661e
parent_tasks:
  - T-P5-070-TRIANGULAR-MULTICONTACT-CHART
  - T-P5-071-SIGNED-TWO-CYCLE-CONTACT
  - T-P5-066-ZERO-SURFACE-RECENTERING
  - T-P5-068-RECENTERED-UNIT-C11
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: >-
  Add a source-independent finite simple-cycle contact theorem after T-P5-071. For a certified simple cycle, test negative orientation parity first: odd sign parity gives a unique chart and denominator-free path-sum inverse bound with no small-gain requirement. Otherwise use the strict full-cycle gain-product gate. Treat failure of both as NOT_APPLICABLE, not noninvertibility. Keep concrete source graph extraction, Lean validation, coverage and admission separate.
---

# T-P5-072 — signed finite simple-cycle contact chart

## 0. Mathematical seam

T-P5-070 closes acyclic/triangular multi-contact charts by nilpotence. T-P5-071 closes the smallest cyclic SCC, a two-contact cycle, and proves that opposite root orientation is negative feedback: it gives uniqueness without a small-gain hypothesis.

The next smallest open mathematical obligation is a directed simple cycle with `n >= 3` contacts. The main question is whether T-P5-071's negative-feedback phenomenon is special to two variables.

It is not. For a simple cycle, all signed orientation information collapses to **one parity bit**, the product of the edge orientations around the cycle. If that product is negative, scalar elimination turns every coordinate equation into `t = F(t)` with `F` antitone. This yields a unique inverse on the common core and an exact path-sum stability bound with **no denominator `1-product(gain)`**. If the orientation product is positive or unknown, the usual strict gain-product gate remains available.

This child is mathematics only. It does not claim a deployed P5 cycle, source binding, Float64/libm, P8/ODE coverage, receipt/provenance, Lean/kernel validation, admission, registry mutation, or parent closure.

---

## 1. Simple-cycle root-map packet

Let indices be cyclic modulo `n`, with `n >= 2`. For each `i`, let

`I_i = [c_i-H_i, c_i+H_i]`, `H_i>0`,

and let `(Y,d)` be the base-parameter metric space. Assume continuous scalar root maps

`rho_i : I_{i+1} x Y -> I_i`.

The recentered cycle coordinates are

**(1.1)** `xi_i = x_i - rho_i(x_{i+1},y)`.

Assume nonnegative exact variation charges `a_i,p_i`:

**(1.2)**

`|rho_i(z,y)-rho_i(z',y')| <= a_i |z-z'| + p_i d(y,y')`.

Assume also a uniform root-displacement packet

**(1.3)** `|rho_i(z,y)-c_i| <= delta_i`, `0 <= delta_i < H_i`,

and define the common chart-core radii

**(1.4)** `K_i = H_i-delta_i`.

Finally, when signed information is available, assume an orientation bit

`eps_i in {+1,-1}`

uniformly on the certified source box:

- `eps_i=+1`: `rho_i(.,y)` is nondecreasing for every `y`;
- `eps_i=-1`: `rho_i(.,y)` is nonincreasing for every `y`.

Define the full-cycle orientation

**(1.5)** `E = product_i eps_i in {+1,-1}`

and the unsigned gain product

**(1.6)** `A = product_i a_i`.

No differentiability is needed for the main theorem.

---

## 2. Common-core existence is still one-dimensional

A cycle may look like an `n`-dimensional fixed-point problem, but a **simple** cycle can be eliminated to one scalar fixed point.

Fix a start index `i` and a trial value `t in I_i`. Set `x_i=t`. Then recursively use the equations in reverse around the cycle:

`x_{i-1} = xi_{i-1} + rho_{i-1}(x_i,y)`,

`x_{i-2} = xi_{i-2} + rho_{i-2}(x_{i-1},y)`,

and so on, until `x_{i+1}` is constructed. Finally define

**(2.1)** `F_i(t) = xi_i + rho_i(x_{i+1},y)`.

If `|xi_j| <= K_j`, then at every recursion step

`|x_j-c_j| <= |xi_j| + |rho_j-c_j| <= K_j+delta_j = H_j`.

So every intermediate point remains inside its required interval and

**(2.2)** `F_i(I_i) subset I_i`.

Continuity of the root maps gives continuity of `F_i`. Therefore the same one-dimensional interval fixed-point lemma used in T-P5-071 gives a fixed point `t=F_i(t)`. The recursively constructed variables then satisfy all equations (1.1).

### Theorem 2.1 — simple-cycle common-core existence

Under (1.3)-(1.4), every chart point with

`|xi_i| <= K_i` for all `i`

has at least one physical preimage in `prod_i I_i`.

No Brouwer theorem and no small-gain assumption are needed; scalar IVT is enough because the dependency SCC is a simple cycle.

---

## 3. Only the orientation product matters

Additive shifts by the `xi_i` do not change monotonicity. The scalar return map `F_i` contains every `rho_j` exactly once, so its orientation is the product `E`.

### Lemma 3.1 — cycle orientation parity

For every start index `i`:

- if `E=+1`, `F_i` is nondecreasing;
- if `E=-1`, `F_i` is nonincreasing.

The conclusion is independent of the chosen start index.

Thus an odd number of orientation-reversing root graphs makes the entire return map antitone, no matter how large the absolute cross gains are.

---

## 4. Exact path-sum perturbation packet

Take two physical/chart/base triples satisfying (1.1). Write

`X_i = |x_i-x_i'|`,

`Z_i = |xi_i-xi_i'|`,

`D = d(y,y')`.

From (1.1)-(1.2),

**(4.1)** `X_i <= Z_i + a_i X_{i+1} + p_i D`.

For cyclic indices define prefix gains

**(4.2)**

`A_{i,0}=1`,

`A_{i,k}=product_{r=0}^{k-1} a_{i+r}` for `1<=k<=n`.

Hence `A_{i,n}=A`, independent of `i`.

Define the one-lap path charge

**(4.3)**

`C_i(Z,D)`

`= sum_{k=0}^{n-1} A_{i,k} Z_{i+k}`

`  + D * sum_{k=0}^{n-1} A_{i,k} p_{i+k}`.

Unrolling (4.1) exactly one lap gives

**(4.4)** `X_i <= C_i(Z,D) + A X_i`.

This identity is the unsigned backbone. It will be consumed differently by the positive/unknown and negative-orientation branches.

---

## 5. Negative orientation product: no small gain

Assume now

**(5.1)** `E=-1`.

Fix one of the two data sets `(xi,y)` and define

`H_i(t)=t-F_i(t)`.

By Lemma 3.1, `F_i` is antitone. Hence for `t>s`,

`H_i(t)-H_i(s)`

`= (t-s) - (F_i(t)-F_i(s))`

`>= t-s`.

Therefore

**(5.2)** `|H_i(t)-H_i(s)| >= |t-s|`.

This is the same unit coercivity mechanism found in T-P5-071, now for any cycle length.

Let `x_i` and `x_i'` be fixed points of the return maps built from the two data sets. Since `H_i(x_i)=0`, strong monotonicity gives

`X_i <= |H_i(x_i')-H_i(x_i)| = |H_i(x_i')|`.

But the primed return equation gives `x_i'=F_i'(x_i')`, so

`|H_i(x_i')| = |F_i'(x_i')-F_i(x_i')|`.

Compare the two nested return maps at the **same** terminal argument `x_i'`. Propagating (1.2) through the nested composition produces exactly the one-lap charge (4.3), with no final `A X_i` term because the terminal argument is held fixed. Therefore:

### Theorem 5.1 — negative-parity simple-cycle inverse bound

If `E=-1`, then for every `i`

**(5.3)** `X_i <= C_i(Z,D)`.

Consequences:

1. Taking `Z=0,D=0` gives `X_i=0` for every `i`, so the cycle chart is injective.
2. Together with Theorem 2.1, it has a unique inverse on the common product core.
3. **No condition on `A=product a_i` is needed.**
4. There is no conditioning denominator `1-A`; negative feedback removes the positive-feedback singularity.

This is the main result of this child.

---

## 6. Optional stronger reserve from quantitative signed lower gain

The unit coercivity in Section 5 is optimal if the checker knows only orientation. If the source provides more, the negative-feedback reserve can be sharpened.

Assume each root map has a signed lower secant modulus `ell_i>=0`: for `z>z'`,

**(6.1)**

`eps_i * (rho_i(z,y)-rho_i(z',y)) >= ell_i (z-z')`.

Let

**(6.2)** `Lambda = product_i ell_i`.

When `E=-1`, the return map satisfies for `t>s`

`F_i(t)-F_i(s) <= -Lambda (t-s)`.

Hence

**(6.3)** `H_i(t)-H_i(s) >= (1+Lambda)(t-s)`.

The same fixed-point comparison proves:

### Theorem 6.1 — strong negative-cycle reserve

**(6.4)** `(1+Lambda) X_i <= C_i(Z,D)`.

For a linear signed cycle this recovers the exact characteristic denominator `1+Lambda`. This branch is optional: absence of `ell_i` must fall back to Theorem 5.1, not fail the cycle.

---

## 7. Positive or unknown orientation: strict product small gain

Without negative orientation, (4.4) remains valid. If

**(7.1)** `A<1`,

then

### Theorem 7.1 — unsigned simple-cycle small-gain inverse

**(7.2)** `(1-A) X_i <= C_i(Z,D)`

for every `i`.

Thus the chart is injective, and Theorem 2.1 supplies a unique inverse on the common core.

This theorem does not require any sign/orientation data. Therefore the decision order should be:

1. negative orientation parity first;
2. otherwise strict gain product;
3. otherwise `NOT_APPLICABLE_CYCLIC`.

Testing small gain first would create false negatives in negative-feedback cycles.

---

## 8. Fully source-cleared exact-rational form

T-P5-066/T-P5-070 often expose root variation before division. Assume exact nonnegative source charges

`mu_i>0`, `g_i>=0`, `L_i>=0`

with

**(8.1)**

`mu_i |rho_i(z,y)-rho_i(z',y')|`

`<= g_i |z-z'| + L_i D`.

Conceptually `a_i=g_i/mu_i`, `p_i=L_i/mu_i`, but the certificate need not store these quotients.

For a fixed start `i`, define cyclic prefix products

`G_{i,k}=product_{r=0}^{k-1} g_{i+r}`,

with `G_{i,0}=1`.

Define the complementary active products

`Mtail_{i,k}=product_{r=k}^{n-1} mu_{i+r}`,

and `Mtail_{i,n}=1`.

Let

**(8.2)** `M = product_j mu_j`, `G = product_j g_j`.

Define the division-free one-lap numerator

**(8.3)**

`R_i(Z,D)`

`= sum_{k=0}^{n-1} [G_{i,k} * Mtail_{i,k}] Z_{i+k}`

`  + D * sum_{k=0}^{n-1} [G_{i,k} * L_{i+k} * Mtail_{i,k+1}]`.

This is exactly `M*C_i(Z,D)` after clearing all root-slope denominators.

Therefore:

### Theorem 8.1 — source-cleared negative-parity branch

If `E=-1`,

**(8.4)** `M X_i <= R_i(Z,D)`.

### Theorem 8.2 — source-cleared unsigned branch

If

**(8.5)** `G < M`,

then

**(8.6)** `(M-G) X_i <= R_i(Z,D)`.

All quantities in (8.4)-(8.6) are finite sums/products and order comparisons. If the source charges are rational/dyadic, the checker is exact-rational and needs no division, root finding, matrix inverse, determinant evaluation, or floating optimization.

For `n=2`, (8.6) reduces exactly to T-P5-071's reserve `mu1*mu2-C12*C21` and its cleared two-row formulas.

---

## 9. Sign gauge: a simple cycle has exactly one signed invariant

There is a useful structural compression for the checker. Flip the orientation of contact coordinate `x_i` by a sign `tau_i in {+1,-1}`. The edge orientation transforms as

**(9.1)** `eps_i' = tau_i * eps_i * tau_{i+1}`.

Multiplying around the cycle gives

`product eps_i' = (product tau_i^2)(product eps_i) = E`.

So `E` is gauge invariant.

Conversely, choose `tau_1=1` and recursively `tau_{i+1}=tau_i eps_i` for `i<n`. Then every transformed edge except the last has orientation `+1`, while the last has orientation exactly `E`.

### Lemma 9.1 — parity completeness

For a directed simple cycle, all edge-orientation patterns with the same product `E` are equivalent under contact sign flips. Thus the main uniqueness decision genuinely needs only one sign bit:

- `E=-1`: negative-feedback class;
- `E=+1`: positive-feedback class.

This is why the two-cycle result extends without a combinatorial explosion of sign cases.

---

## 10. Exact regressions and obstructions

### 10.1 Three-cycle negative feedback passes although absolute small gain fails

On `[-1,1]`, take

`rho1(t) = -(1/2)t - (2/5)t^3`,

`rho2(t)=t`,

`rho3(t)=t`.

`rho1' = -1/2-(6/5)t^2 < 0`, while `rho2,rho3` are increasing. Hence `E=-1`.

An exact Lipschitz envelope is

`a1=17/10`, `a2=a3=1`,

so

**(10.1)** `A=17/10>1`.

The unsigned small-gain branch therefore fails. But at `xi=0` the cycle reduces to

`t = -(1/2)t-(2/5)t^3`,

or

`(3/2)t+(2/5)t^3=0`,

whose unique real solution is `t=0`. Theorem 5.1 certifies the whole class without using `A<1`.

This is a strict regression against any implementation that tests absolute gain before sign parity.

### 10.2 Positive-parity boundary can be genuinely singular

Take all three root maps to be the identity and `xi=0`. Then `E=+1`, `A=1`, and every point

`x1=x2=x3=t`

is a solution. Thus the strict boundary `A=1` cannot be admitted generically in the positive/unsigned branch.

### 10.3 Positive parity with `A>1` can still be unique

Take

`rho1(t)=(1/2)t+(2/5)t^3`,

`rho2(t)=rho3(t)=t`

on `[-1,1]`. Then `rho1` is increasing with derivative between `1/2` and `17/10`, so an available upper-gain product is `17/10>1`. Yet the fixed-point equation is

`t=(1/2)t+(2/5)t^3`,

hence

`t(1/2-(2/5)t^2)=0`.

The nonzero roots would require `t^2=5/4`, outside `[-1,1]`; therefore the source-box fixed point is unique.

So failure of the strict small-gain gate is **not** a proof of noninvertibility.

### 10.4 Positive parity with `A>1` can also be nonunique

Take

`rho1(t)=t+(1/5)t(1-t^2)`,

`rho2(t)=rho3(t)=t`

on `[-1,1]`. Its derivative is

`6/5-(3/5)t^2`,

which stays positive and has upper bound `6/5`. Hence `E=+1` and an upper-gain product is `6/5>1`. But

`rho1(t)=t`

at `t=-1,0,1`, producing three cycle fixed points at `xi=0`.

Therefore for positive/unknown parity with failed small gain the mathematically correct label is `NOT_APPLICABLE_CYCLIC`, not `FAIL_NONINVERTIBLE`.

---

## 11. Recommended decision layer

For each source-certified simple-cycle SCC:

### Branch A — negative parity

If

`product eps_i = -1`,

return

`PASS_NEGATIVE_PARITY_CYCLE`

and consume (5.3) or the source-cleared (8.4). If quantitative lower signed secants are also available, optionally strengthen to (6.4).

### Branch B — unsigned strict full-cycle gain

Otherwise, if

`product g_i < product mu_i`

(or normalized `product a_i<1`), return

`PASS_SIMPLE_CYCLE_SMALL_GAIN`

with (8.6).

### Branch C — unresolved cyclic regime

Otherwise return

`NOT_APPLICABLE_CYCLIC`.

Do not infer noninvertibility. A source-specific determinant, monotone-operator, interval-Newton, degree, or stronger signed certificate may still close that SCC.

---

## 12. Lean-friendly theorem decomposition

The main formal leaves are small.

```text
simpleCycle_nested_selfmap
  (displacement/core hypotheses)
  : MapsTo F_i (Icc lo_i hi_i) (Icc lo_i hi_i)
```

Then reuse the interval fixed-point leaf already isolated in T-P5-071.

```text
simpleCycle_orientation_product
  (edge monotone/antitone witnesses)
  : E = -1 -> Antitone F_i
```

Reuse T-P5-071's `sub_antitone_strongMono_one` for the unit coercivity step.

```text
simpleCycle_path_charge_same_terminal
  (root variation packets)
  : |F_i' t - F_i t| <= C_i Z D
```

This is a finite induction over the nested composition.

```text
negativeParityCycle_inverse_bound
  (hE : E = -1)
  : X_i <= C_i Z D
```

```text
simpleCycle_smallGain_cleared
  (hrec : forall i, X_i <= Z_i + a_i*X_(i+1) + p_i*D)
  (hA : product a < 1)
  : (1-product a)*X_i <= C_i Z D
```

For the division-free source layer:

```text
negativeParityCycle_sourceCleared
  : M*X_i <= R_i Z D

simpleCycle_smallGain_sourceCleared
  (hDelta : product g < product mu)
  : (product mu - product g)*X_i <= R_i Z D
```

Optional strengthening:

```text
negativeParityCycle_strongLowerGain
  (signed lower secant ell_i)
  : (1 + product ell_i)*X_i <= C_i Z D
```

Sign compression:

```text
cycleOrientationProduct_gaugeInvariant
cycleOrientation_gaugeNormalForm
```

Regression leaves should include the exact cubic examples from Section 10 so future refactors cannot silently replace parity-first logic with an unsigned-only gain test.

---

## 13. Dependencies and remaining boundary

**Closed mathematically in this child:**

- common-core existence for any finite directed simple cycle by scalar elimination + interval IVT;
- exact reduction of all cycle orientation data to the product parity `E`;
- no-small-gain uniqueness for every negative-parity simple cycle, any length;
- exact one-lap path-sum inverse/transport bound with no `1-A` denominator in that branch;
- optional `1+product ell_i` strong negative-feedback reserve when lower signed secants exist;
- strict unsigned full-cycle gain theorem for positive/unknown orientation;
- exact division-free source-cleared reserves `M` versus `M-G`;
- exact regressions proving parity-first ordering is necessary and failed positive small gain is only `NOT_APPLICABLE`.

**Still open / not claimed:**

- whether a deployed P5 factor graph contains any simple cycle and what its exact orientation/gain packets are;
- SCCs with chords or one root depending on multiple simultaneous contact variables;
- general strongly connected multi-input contact graphs;
- positive-parity cycles lacking strict small gain;
- source-specific determinant / P-matrix / monotone-operator / interval-Newton certificates for those cases;
- multiple-root cluster interaction from T-P5-067;
- reduced-packet bounds after concrete cyclic substitution;
- Float64/libm/FD/controller/solve semantics;
- P8/ODE coverage;
- Lean compile/kernel/comparator/receipt/provenance;
- independent validation by 封不觉;
- P5/P8/M4 closure, admission or registry mutation.

The structural takeaway is concise: **a finite simple contact cycle is controlled by one signed parity bit plus one unsigned gain product. Negative parity removes the positive-feedback denominator at every cycle length; positive or unknown parity retains the strict product-gain branch.**
