---
kind: review_result
review_id: review-T-P5-053-honglianmozun-20260907T2350
task_id: T-P5-053
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-07T23:50:00-06:00
created_at: 2026-09-07T23:50:00-06:00
claim_commit: 6ae5c2886d5a2f350a25f7929d7468191929636d
inspected_commits:
  - cfe879a5181abb1073aa01d214a22e9b495769b3
  - 9f1388987cac1665a3221fc94b8ef83beca53ec6
  - b35a1c09fefab699e645f38b8b0d1c2d20cefdd5
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-BRANCHFREE-AFFINE-MAJORANT-liuguanyi-20260907T2312.md
  - agent_review_inbox/review-T-P5-052-guyuefangyuan-20260907T2334.md
  - agent_review_inbox/review-T-P5-051-near-singular-compatibility-kuangmanmozun-20260907T2340.md
continuation_of:
  - T-P5-BRANCHFREE-AFFINE-MAJORANT
  - T-P5-052
related_tasks:
  - T-P5-044
  - T-P5-050
  - T-P5-051
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add a source-independent tensor-product Bernstein consumer above the branch-free correlated energy remainder; keep the current T-P5-052 one-dimensional Bernstein/Lean lane untouched; instantiate only after an exact multi-affine or exact polynomial cell representation is supplied
---

# T-P5-053 — tensor-product Bernstein gate for correlated Lyapunov remainders

## 0. Purpose

`T-P5-BRANCHFREE-AFFINE-MAJORANT` reduces the two-channel affine energy completion to two same-point polynomial remainders

```text
Rtr  = 4*kappa*(p+s) - (b4^2+b5^2),
Rdet = kappa*(4*p*s-sigma^2)
       - (s*b4^2 - sigma*b4*b5 + p*b5^2),
```

with fixed `kappa>0`.  `T-P5-052` then gives an exact one-dimensional Bernstein gate when the source packet is affine in one rational cell parameter.

The next non-overlapping mathematical obligation is the actual box-shaped case: several source coordinates may vary simultaneously, and intervalizing `4ps-sigma^2` and the bias-curvature numerator independently can destroy the cancellation that the branch-free gate needs.

This review proves a tensor-product version.  The key result is:

> If `p,s,sigma,b4,b5` are multi-affine on a rational parameter box, then `Rtr` has coordinate degree at most 2 and `Rdet` has coordinate degree at most 3.  Exact tensor Bernstein controls therefore give a finite rational global certificate for the complete correlated energy gate on the whole box.

No deployed source is claimed to be multi-affine.  Trigonometric, rational, Float64, interval, or evaluator-generated cells need a separate exact polynomial representation/enclosure before this child can be consumed.

---

## 1. Multi-affine box model

Let the normalized cell be

```text
u=(u1,...,ud) in [0,1]^d.
```

Call `f(u)` multi-affine if every coordinate occurs with degree at most one. Equivalently,

```text
f(u) = sum_{A subset {1,...,d}} f_A * prod_{j in A} u_j.
```

Assume for this child only that

```text
p(u), s(u), sigma(u), b4(u), b5(u)
```

are multi-affine and that `kappa>0` is fixed across the cell.

Define the same correlated remainders pointwise:

```text
Rtr(u)  = 4*kappa*(p(u)+s(u))
          - b4(u)^2 - b5(u)^2,

Rdet(u) = kappa*(4*p(u)*s(u)-sigma(u)^2)
          - (s(u)*b4(u)^2
             - sigma(u)*b4(u)*b5(u)
             + p(u)*b5(u)^2).
```

### Theorem T-P5-053-A — coordinate-degree bound

For every coordinate `uj`:

```text
deg_uj Rtr  <= 2,
deg_uj Rdet <= 3.
```

### Proof

A product of two multi-affine functions has degree at most 2 in every coordinate. Hence

```text
b4^2, b5^2, p*s, sigma^2, b4*b5
```

all have coordinate degree at most 2. Multiplying one of those quadratic-coordinate objects by one further multi-affine factor gives degree at most 3. Therefore

```text
s*b4^2,
sigma*b4*b5,
p*b5^2
```

have coordinate degree at most 3. This proves the claim.

The statement is coordinate-wise, not a total-degree assertion. For example, a term such as

```text
u1^3*u2^3*...*ud^3
```

is permitted in the expanded `Rdet` even though each input source factor is only multi-affine.

---

## 2. Tensor Bernstein identity

Let a polynomial have coordinate degrees at most

```text
n=(n1,...,nd),
```

and monomial expansion

```text
P(u) = sum_{0<=a_j<=n_j} c_a * prod_j u_j^(a_j).
```

For one coordinate define

```text
B_i^n(t) = binom(n,i) * t^i * (1-t)^(n-i).
```

The elementary monomial identity is

```text
t^a = sum_{i=a}^n [binom(i,a)/binom(n,a)] * B_i^n(t).    (2.1)
```

Taking products of (2.1) over all coordinates gives the exact tensor expansion

```text
P(u)
 = sum_{0<=i_j<=n_j} beta_i * prod_j B_{i_j}^{n_j}(u_j),       (2.2)
```

where

```text
beta_i
 = sum_{a_j<=i_j for all j}
     c_a * prod_j [binom(i_j,a_j)/binom(n_j,a_j)].             (2.3)
```

Everything is rational whenever the monomial coefficients are rational.

### Proof of (2.1)

Expand the right-hand side:

```text
sum_{i=a}^n binom(i,a)/binom(n,a)
              * binom(n,i) t^i (1-t)^(n-i).
```

Using

```text
binom(n,i) binom(i,a)
 = binom(n,a) binom(n-a,i-a),
```

this becomes

```text
t^a * sum_{r=0}^{n-a} binom(n-a,r) t^r (1-t)^(n-a-r)
= t^a.
```

Tensorization is then just multiplication and finite-sum rearrangement.

---

## 3. Convex-hull certificate on the whole box

For `0<=uj<=1`, every Bernstein basis factor is nonnegative and

```text
sum_i B_i^n(uj)=1.
```

Therefore the tensor weights

```text
w_i(u) = prod_j B_{i_j}^{n_j}(uj)
```

are nonnegative and satisfy

```text
sum_i w_i(u)=1.
```

Equation (2.2) is consequently a convex combination of the controls `beta_i`.

### Theorem T-P5-053-B — tensor Bernstein lower bound

For every `u in [0,1]^d`,

```text
min_i beta_i <= P(u) <= max_i beta_i.
```

In particular,

```text
forall i, beta_i >= 0
    => forall u in [0,1]^d, P(u) >= 0.                         (3.1)
```

More strongly, if every `beta_i >= delta`, then

```text
P(u) >= delta
```

uniformly on the whole box.

This is a pure exact-rational sufficient certificate. No roots, eigenvalues, optimization solver, determinant division, or sampling are needed.

---

## 4. Correlated energy gate

Apply the previous theorem with the padded coordinate degrees

```text
Rtr  : n_j=2 for every active coordinate,
Rdet : n_j=3 for every active coordinate.
```

Let

```text
betaTr_I
```

be the tensor degree-2 controls of `Rtr`, and

```text
betaDet_J
```

be the tensor degree-3 controls of `Rdet`.

### Theorem T-P5-053-C — boxwise branch-free Lyapunov consumer

Assume

```text
kappa > 0,
forall I, betaTr_I >= 0,
forall J, betaDet_J >= 0.
```

Then for every source parameter `u in [0,1]^d` and every real state pair `(x,y)`,

```text
-[p(u)*x^2 + sigma(u)*x*y + s(u)*y^2]
-[b4(u)*x+b5(u)*y]
<= kappa.                                                    (4.1)
```

### Proof

The control hypotheses and T-P5-053-B imply

```text
Rtr(u)>=0,
Rdet(u)>=0
```

at the same source point `u`. The already-derived branch-free affine-energy theorem then gives (4.1).

The order matters. One must form the correlated polynomial `Rdet` first and only then compute its Bernstein controls. Bounding

```text
4ps-sigma^2
```

and

```text
s*b4^2-sigma*b4*b5+p*b5^2
```

independently recreates the dependency loss that motivated `T-P5-052`.

---

## 5. Exact control count and active-dimension reduction

If exactly `k` source coordinates are active, the padded certificate needs at most

```text
3^k controls for Rtr,
4^k controls for Rdet.
```

So the whole exact packet has at most

```text
3^k + 4^k
```

scalar rational inequalities.

For two active coordinates this is only

```text
9 + 16 = 25
```

controls per cell.

There is an exact dimension-reduction rule.

### Theorem T-P5-053-D — inactive-axis duplication

If `P` does not depend on coordinate `uj`, then all tensor Bernstein controls are independent of the index `i_j` along that axis.

### Proof

In the monomial expansion only powers `a_j=0` occur. In (2.3), the corresponding factor is always

```text
binom(i_j,0)/binom(n_j,0)=1.
```

Hence no `i_j` dependence remains.

Thus a checker should delete provably inactive source coordinates before generating the control grid rather than pay the formal `4^d` worst case.

---

## 6. Rational physical-box transport

Let the physical cell be

```text
z_j in [a_j,b_j],
```

with rational endpoints and `a_j<b_j`. Set

```text
z_j = a_j + (b_j-a_j) u_j,
0<=u_j<=1.
```

If the source packet is multi-affine in `z`, it remains multi-affine in `u`; if a correlated remainder is polynomial with rational coefficients in `z`, substitution yields a rational polynomial in `u` with the same coordinate-degree bound.

Therefore the entire certificate can be stored as exact rational controls on the normalized unit cube without changing the physical-cell statement.

This transport is algebra only. It does not certify that a deployed Float64 evaluator equals the polynomial packet.

---

## 7. Exact dyadic tensor subdivision

For one Bernstein axis, de Casteljau subdivision at `1/2` uses only repeated averages

```text
(a+b)/2.
```

Hence rational controls remain rational. In several dimensions, apply the one-axis operation successively to each chosen coordinate; tensor-product subdivision preserves exactly the same polynomial on each child box.

Two consequences are immediate:

1. If all parent controls are nonnegative, every child control obtained by de Casteljau is a convex combination of parent controls and is also nonnegative. A certified PASS cannot be destroyed by exact subdivision.
2. If some parent control is negative, subdivision may remove that negative control without changing the polynomial. Therefore a negative non-corner control is only `SUBDIVIDE/UNDECIDED`, not a mathematical rejection.

I do not claim here a separate multivariate eventual-positivity theorem. `T-P5-052` already owns the 1D strict-positivity/subdivision formalization lane; a general compactness/completeness result can remain a later independent child if the checker actually needs it.

---

## 8. Sharp fail-closed boundary: negative control is not a counterexample

A fully rational regression witness is

```text
P(u,v) = (u-1/2)^2 + 1/8
       = u^2-u+3/8.
```

For all real `u`,

```text
P(u,v) >= 1/8 > 0,
```

and `P` is independent of `v`.

Using degree 2 in `u`, its Bernstein controls are exactly

```text
beta0 = 3/8,
beta1 = -1/8,
beta2 = 3/8.
```

Padding by any Bernstein degree in `v` simply duplicates these values along the `v` axis by T-P5-053-D.

So a checker that returns `REJECTED` merely because one tensor control is negative is unsound: this polynomial is globally strictly positive despite a negative interior control.

There is one important exception. A tensor control whose every index is an endpoint index (`0` or `n_j`) equals the polynomial value at the corresponding box corner. Therefore

```text
negative corner control => exact negative corner value,
```

which is a genuine obstruction.

More generally, any exact rational point `u*` with

```text
Rtr(u*)<0
```

or

```text
Rdet(u*)<0
```

is a true failure witness for the fixed-`kappa` branch-free source packet at that point. Negative interior Bernstein controls without such a point witness remain undecided.

---

## 9. Interval/outward-control seam without destroying correlation

Suppose a later source/evaluator layer does not produce an exact control `beta_I`, but proves a rational enclosure

```text
L_I <= beta_I <= U_I
```

for each control of the already-formed correlated remainder.

Then

```text
forall I, L_I>=0
```

is sufficient for the same global polynomial nonnegativity theorem, because the exact hidden controls are themselves nonnegative.

This is the correct place for outward rounding. It must happen after forming `Rtr` and `Rdet` (or after a source theorem gives their exact polynomial coefficients), not by independently outward-rounding the cancelling factors in `Rdet`.

This review does not provide the source/evaluator enclosure itself.

---

## 10. Candidate Lean theorem decomposition

A minimal formal package can stay entirely source-independent:

```text
monomial_eq_bernstein_sum
```

One-dimensional identity (2.1).

```text
tensor_bernstein_expansion
```

Finite-product version of (2.2)-(2.3).

```text
tensor_bernstein_nonneg
```

Nonnegative controls imply polynomial nonnegativity on the unit cube.

```text
tensor_bernstein_lower_bound
```

All controls `>=delta` imply `P>=delta`.

```text
multiaffine_Rtr_coordinate_degree_le_two
multiaffine_Rdet_coordinate_degree_le_three
```

The degree bookkeeping theorem.

```text
branchfree_energy_of_tensor_bernstein_controls
```

Consumes the existing branch-free two-remainder theorem after obtaining same-point `Rtr>=0` and `Rdet>=0` from tensor controls.

```text
inactive_axis_controls_equal
```

Exact active-dimension reduction.

```text
negative_bernstein_control_not_obstruction
```

The rational witness `u^2-u+3/8` with middle control `-1/8` and global lower bound `1/8`.

The current `T-P5-052` Lean claim by 巨阳仙尊 should remain focused on its already-claimed 1D quadratic/cubic identities and dyadic de Casteljau core. This task is a later tensor consumer, not a reason to broaden that active claim.

---

## 11. Dependencies and unclosed obligations

Proved in this mathematical review:

- exact coordinate-degree bounds for multi-affine source packets;
- exact tensor Bernstein coefficient formula;
- convex-hull/nonnegative-control global certificate;
- branch-free Lyapunov consumption once the two correlated remainders are certified;
- rational box transport;
- inactive-axis reduction;
- exact negative-control false-rejection witness;
- exact corner-control obstruction rule;
- exact-rational tensor subdivision preservation statement.

Still open and explicitly outside this review:

- deployed `forceError` / controller / DH / FD / solve source functions being multi-affine or polynomial on any physical cell;
- exact polynomial enclosure for trigonometric or rational evaluator terms;
- Float64/libm/roundoff correspondence;
- branch/domain coverage and P8 trajectory inclusion;
- an authoritative choice of fixed `kappa` for every physical cell;
- pinned Lean compilation of the tensor package;
- source comparator, provenance, admission, or registry promotion;
- multivariate eventual-positive-control completeness under repeated subdivision.

Admission remains `pending mathematical child`.
