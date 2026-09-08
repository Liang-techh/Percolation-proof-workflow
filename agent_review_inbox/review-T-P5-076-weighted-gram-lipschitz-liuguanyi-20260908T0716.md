---
kind: review_result
review_id: review-T-P5-076-weighted-gram-lipschitz-liuguanyi-20260908T0716
task_id: T-P5-076-WEIGHTED-GRAM-LIPSCHITZ
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-08T07:16:00-06:00
claim_commit: 251dd8cb79feefbce10272376a4c5b2a387f22f9
inspected_commits:
  - 48c78207c758636227a8bb3f5be2e1f6c247e6c4
  - 038772083818be60fa274d5e9d60162a686d2dde
inspected_paths:
  - agent_review_inbox/review-T-P5-074-weighted-strong-monotone-scc-guyuefangyuan-20260908T0700.md
  - agent_review_inbox/review-T-P5-075-damped-corrector-energy-honglianmozun-20260908T0712.md
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: >-
  Add this as the missing source-to-secant squared-Lipschitz bridge between
  T-P5-074 and T-P5-075. The preferred source packet must form weighted Gram
  cross terms after signed summation, then bound them; the entrywise-absolute
  packet is only a safe fallback. Keep deployed source binding, numerical
  semantics, coverage, Lean/kernel and admission separate.
---

# T-P5-076 — weighted Gram certificate for a radical-free squared-Lipschitz SCC packet

## 0. Result in one line

T-P5-075 needs, in the **same weighted norm** used by T-P5-074, a source-valid
secant inequality

`||Phi(x)-Phi(y)||_W^2 <= Lambda ||x-y||_W^2`.

The missing bridge can be generated without a matrix inverse, eigenvalue,
square root, or floating operator norm.  Let

`J(z) = D Phi(z)`,

`H(z) = J(z)^T W J(z)`.

If the source first forms the **signed weighted Gram entries**

`H_jk(z) = sum_i w_i J_ij(z) J_ik(z)`

and proves rational cell bounds

`H_jj <= a_j`,

`|H_jk| <= c_jk = c_kj` for `j != k`,

with

`a_j + sum_{k != j} c_jk <= Lambda w_j`

for every column `j`, then pointwise

`||J(z)v||_W^2 <= Lambda ||v||_W^2`,

and convex-cell integration gives the desired secant squared-Lipschitz packet.

For implicit contact roots, every denominator can be cleared **before** the
trusted checker sees the packet, while retaining the signed sum inside each
Gram cross term.  This supplies exactly the new analytic input requested by
T-P5-075 and is compatible with the signed-symmetric strong-monotonicity packet
of T-P5-074.

This is mathematics only.  It does not bind a deployed SCC/source Jacobian,
prove a corrector implementation, Float64/FD/controller/solve semantics,
P8/ODE coverage, Lean/kernel evidence, provenance, admission, registry mutation,
or parent closure.

---

## 1. Weighted setting

Fix positive weights

`w_i > 0`

and write

`W = diag(w_1,...,w_n)`,

`Q_W(v) = ||v||_W^2 = sum_i w_i v_i^2`.

Let `B subset R^n` be convex and let

`Phi : B -> R^n`

be continuously differentiable on a neighborhood of every segment used below.
Write

`J(z) = D Phi(z)`.

For each `z`, define the weighted Gram matrix

**(1.1)**

`H(z) = J(z)^T W J(z)`.

Its entries are

**(1.2)**

`H_jk(z) = sum_i w_i J_ij(z) J_ik(z)`.

Unlike the symmetric-part packet of T-P5-074, which is linear in `J`, this is
the exact quadratic object controlling the squared-Lipschitz constant.

---

## 2. Algebraic weighted-Gram row theorem

Assume on one certified cell that rational numbers `a_j` and symmetric
`c_jk=c_kj>=0` satisfy

**(2.1)** `H_jj(z) <= a_j`,

**(2.2)** `|H_jk(z)| <= c_jk` for `j != k`,

and for a rational `Lambda>=0`,

**(2.3)**

`a_j + sum_{k != j} c_jk <= Lambda w_j`

for every `j`.

Then for every real vector `v`,

`Q_W(Jv) = v^T H v`

`= sum_j H_jj v_j^2 + 2 sum_{j<k} H_jk v_j v_k`.

Using only

`2 |v_j v_k| <= v_j^2 + v_k^2`,

we get

`v^T H v`

`<= sum_j a_j v_j^2 + 2 sum_{j<k} c_jk |v_j v_k|`

`<= sum_j (a_j + sum_{k!=j} c_jk) v_j^2`

`<= Lambda sum_j w_j v_j^2`.

Hence:

### Theorem 2.1 — weighted Gram row upper certificate

Under (2.1)-(2.3),

**(2.4)**

`||J(z)v||_W^2 <= Lambda ||v||_W^2`

for every `z` in the certified cell and every `v`.

The trusted scalar arithmetic is only addition, multiplication, absolute-value
bounds and order.  No `sqrt(Lambda)` is needed.

A slightly tighter checker interface can skip the intermediate `a_j,c_jk` and
prove directly

**(2.5)**

`H_jj + sum_{k!=j} |H_jk| <= Lambda w_j`.

The separated packet is useful only because source interval/SOS systems often
want one named enclosure per polynomial.

---

## 3. Jacobian-to-secant squared-Lipschitz bridge

Take `x,y in B` and set

`d = x-y`.

Because `B` is convex, the segment

`gamma(t)=y+t d`, `0<=t<=1`,

lies in `B`.  The fundamental theorem along the segment gives

**(3.1)**

`Phi(x)-Phi(y) = integral_0^1 J(gamma(t)) d dt`.

Let

`z(t)=J(gamma(t))d`.

For each weighted coordinate, scalar Cauchy/Jensen on `[0,1]` gives

`(integral z_i)^2 <= integral z_i^2`.

Multiplying by `w_i>0`, summing over `i`, and applying (2.4),

`||Phi(x)-Phi(y)||_W^2`

`<= integral_0^1 ||J(gamma(t))d||_W^2 dt`

`<= integral_0^1 Lambda ||d||_W^2 dt`

`= Lambda ||x-y||_W^2`.

Therefore:

### Theorem 3.1 — weighted Jacobian Gram implies secant squared-Lipschitz

If Theorem 2.1 holds uniformly on a convex source cell, then

**(3.2)**

`||Phi(x)-Phi(y)||_W^2 <= Lambda ||x-y||_W^2`

for all `x,y` in that cell.

This is exactly T-P5-075's `(L2)` premise, in exactly the same `W` used by
T-P5-074.

No vector-valued mean-value theorem is required.  The only analytic transport
is segment integration plus scalar square convexity.

---

## 4. Why the source must form Gram cross terms before absolute values

The off-diagonal Gram term is

`H_jk = sum_i w_i J_ij J_ik`.

The sum can cancel between physical/output rows.  If source intervalization
replaces it first by

`sum_i w_i |J_ij| |J_ik|`,

that cancellation is permanently lost.

### Exact 2x2 obstruction

Take `W=I` and

`J = [[1, 1],
     [1,-1]]`.

Then

`J^T J = [[2,0],[0,2]]`.

So the exact squared operator bound is

`||Jv||^2 = 2 ||v||^2`,

and `Lambda=2` is certified by the signed Gram packet because `H_12=0`.

If one takes entrywise absolute values first, then

`|J| = [[1,1],[1,1]]`,

and the fallback Gram bounds become

`H_11 <= 2`, `H_22 <= 2`, `|H_12| <= 2`.

The same diagonal-dominance gate now needs

`Lambda >= 4`.

Thus absolute-first preprocessing doubles the squared-Lipschitz charge even in
the smallest example.  Scaled Hadamard families make the gap grow with the SCC
dimension.

This is the same source-interface principle already seen in T-P5-074's signed
symmetric pair sum: **form the mathematically relevant correlated polynomial
first; only then enclose its magnitude**.

---

## 5. Safe entrywise fallback

If the source cannot retain those correlations but can prove exact cell bounds

**(5.1)** `|J_ij| <= A_ij`, with `A_ij>=0`,

then a safe fallback is

**(5.2)**

`D_j = sum_i w_i A_ij^2`,

**(5.3)**

`C_jk = sum_i w_i A_ij A_ik`.

These imply

`H_jj <= D_j`,

`|H_jk| <= C_jk`.

Hence the exact-rational row gate

**(5.4)**

`D_j + sum_{k!=j} C_jk <= Lambda w_j`

still proves (3.2).

This lane is universally safe but should be marked fallback because it destroys
cross-row sign cancellation and may make T-P5-075's admissible step interval
artificially small.

---

## 6. Implicit-root specialization without division in the checker

Now specialize to the contact-root structure of T-P5-074.  For each row `i`,
let the active contact equation be

`h_i(x_i,x_-i,y)=0`,

with orientation-gauged active derivative

**(6.1)** `d_i = partial_i h_i > 0`.

Let `rho_i(x_-i,y)` be the corresponding root and

`Phi_i(x,y)=x_i-rho_i(x_-i,y)`.

Then

`partial_i Phi_i = 1`,

and for `j != i`, implicit differentiation gives

`partial_j Phi_i = (partial_j h_i)/d_i`.

Define the denominator-cleared Jacobian row

**(6.2)**

`A_ii = d_i`,

`A_ij = partial_j h_i` for `j != i`.

Then exactly

**(6.3)** `A_ij = d_i J_ij`.

The weighted Gram entries are therefore

**(6.4)**

`H_jk = sum_i w_i A_ij A_ik / d_i^2`.

A naive implementation would introduce divisions here.  They are unnecessary.

### Common clearing-scale packet

Choose any positive common scale `Delta>0` and nonnegative quantities `eta_i`
satisfying

**(6.5)**

`Delta = eta_i d_i^2`

for every `i`.

The canonical polynomial choice is

`Delta = product_r d_r^2`,

`eta_i = product_{r!=i} d_r^2`,

but the theorem does not require that particular representation; a source CSE
may use a smaller common denominator when available.

Define the cleared Gram numerators

**(6.6)**

`P_jk = sum_i w_i eta_i A_ij A_ik`.

Then the exact identity is

**(6.7)**

`P_jk = Delta H_jk`.

Hence a completely division-free source packet may provide rational
`alpha_j`, `gamma_jk>=0` with

**(6.8)** `P_jj <= alpha_j Delta`,

**(6.9)** `|P_jk| <= gamma_jk Delta`,

and checker rows

**(6.10)**

`alpha_j + sum_{k!=j} gamma_jk <= Lambda w_j`.

Because `Delta>0`, (6.8)-(6.10) imply the unscaled Gram bounds and therefore
the global secant inequality (3.2).

Even more directly, a polynomial/SOS source can certify

**(6.11)**

`P_jj + sum_{k!=j} |P_jk| <= Lambda w_j Delta`.

The checker never divides by `d_i`, `d_i^2`, or `Delta`.

Crucially, each `P_jk` must be formed as the **signed sum**

`sum_i w_i eta_i A_ij A_ik`

before its absolute value is bounded.  This retains cancellation across rows
even though the implicit-root derivatives originally have different
denominators.

---

## 7. One unified Jacobian packet now feeds both T-P5-074 and T-P5-075

The same source Jacobian supports two different quadratic objects:

1. lower strong-monotonicity object from T-P5-074,

   `S = WJ + J^T W`;

2. upper squared-Lipschitz object from this result,

   `H = J^T W J`.

The first source route should preserve the signed pair sum

`w_i J_ij + w_j J_ji`.

The second should preserve the signed Gram sum

`sum_r w_r J_rj J_rk`.

If the first yields `mu>0` and the second yields `Lambda>=0`, then T-P5-075
can consume the pair directly:

`q_h = 1 - 2 h mu + h^2 Lambda`,

with strict rational step gate

`h>0`, `h Lambda < 2 mu`.

### Compatibility lemma

On any nontrivial weighted space, the two valid source inequalities imply

**(7.1)** `mu^2 <= Lambda`.

Indeed, for any nonzero `v`, strong monotonicity gives

`mu Q_W(v) <= <Jv,v>_W`,

weighted Cauchy gives

`<Jv,v>_W^2 <= Q_W(Jv) Q_W(v)`,

and the Gram packet gives

`Q_W(Jv) <= Lambda Q_W(v)`.

Cancelling the positive `Q_W(v)^2` yields (7.1).

Thus T-P5-075's `mu^2<=Lambda` compatibility premise does not require an
independent physical source certificate once both Jacobian packets are valid.
It may still be checked explicitly as a cheap consistency assertion.

---

## 8. Minimal theorem statements for formalization

A useful decomposition is:

### Leaf A — pure finite-sum algebra

`weighted_gram_row_upper`

Premises:

- `w_i>0`;
- `H_jj<=a_j`;
- `|H_jk|<=c_jk`;
- `a_j+sum_{k!=j}c_jk<=Lambda*w_j`.

Conclusion:

`v^T H v <= Lambda * sum_j w_j v_j^2`.

### Leaf B — instantiate the Gram

`weighted_jacobian_pointwise_sq_le`

With `H=J^T W J`, conclude

`Q_W(Jv)<=Lambda Q_W(v)`.

### Leaf C — analytic segment transport

`weighted_jacobian_bound_implies_secant_sq_le`

On a convex set, pointwise Leaf B implies

`Q_W(Phi(x)-Phi(y))<=Lambda Q_W(x-y)`.

### Leaf D — denominator-cleared implicit root algebra

`cleared_implicit_weighted_gram_identity`

From `A_ij=d_i J_ij` and `Delta=eta_i*d_i^2`, prove

`P_jk=Delta*H_jk`.

### Leaf E — compatibility with T-P5-074

`strong_monotone_and_sq_lipschitz_imply_mu_sq_le`

This is source-independent Hilbert/Cauchy algebra.

Leaf A, B and D are the best first Lean targets; they avoid analytic integration
and should be tiny.  Leaf C can be added once the project chooses its preferred
finite-dimensional segment-integral API.

---

## 9. Typed source-to-math contract

For one SCC/cell, the smallest useful mathematical packet is:

- positive rational weights `w_i` shared with T-P5-074;
- rational target `Lambda>=0`;
- either signed weighted-Gram bounds `a_j,c_jk`, or denominator-cleared
  `Delta,P_jk` bounds;
- same-cell proof that all bounds refer to the same `J=D Phi`;
- convex-cell / segment-validity witness for the Jacobian-to-secant transport.

For the implicit-root route additionally:

- active derivatives `d_i>0`;
- cleared row entries `A_ij=d_i J_ij`;
- exact common-scale identities `Delta=eta_i d_i^2`.

The packet does **not** need:

- `sqrt(Lambda)`;
- singular values or eigenvalues;
- a matrix inverse;
- numerical condition numbers;
- a floating nonlinear solve.

---

## 10. Remaining boundary

This result closes only the abstract mathematics seam

`source Jacobian packet -> same-weight squared-Lipschitz secant packet`.

Still open:

1. identifying the deployed P5 SCC/contact chart whose `Phi` is being inverted;
2. exact source binding of every active `h_i`, `d_i`, and cross derivative;
3. producing same-cell signed Gram or cleared-Gram enclosures;
4. proving the actual cell is convex/segment-valid for the source formulas;
5. evaluator defect and actual corrector implementation binding required by
   T-P5-075;
6. Float64/libm/FD/controller/solve semantics;
7. P8/ODE/first-exit coverage;
8. Lean/kernel compilation and `#print axioms`;
9. independent 封不觉 validation, comparator/admission, and registry state.

Failure of the Gram diagonal-dominance gate means only

`NOT_CERTIFIED_BY_WEIGHTED_GRAM_ROW_BOUND`.

It is not evidence that the true squared-Lipschitz constant is too large; a
full PSD/SOS certificate for `Lambda W-J^T W J`, a tighter block certificate,
or a different weight may still succeed.

---

## 11. Admission boundary

**Admission label: `pending`.**

This review proposes a source-independent bridge lemma and an exact-rational
checker contract.  It is not a proof receipt for the deployed model and changes
no P5/P8/M4 authoritative state.
