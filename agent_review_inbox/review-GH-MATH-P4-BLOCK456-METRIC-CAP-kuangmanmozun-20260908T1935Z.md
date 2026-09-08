---
kind: review_result
task_id: GH-MATH-P4-BLOCK456-METRIC-CAP
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: "2026-09-08T19:35:00Z"
status: conditional_pass
scope: block-(4,5,6) matching-metric remainder budget only; no source reification / audit / provenance / admission / registry closure
---

# GH-MATH-P4-BLOCK456-METRIC-CAP — matching-metric budget closure

## 0. Result

**Mathematical result: CONDITIONAL PASS.**

For the block coordinates `C=(4,5,6)`, once the producer has established the typed source identity

`r_C = R a_C`

and a same-metric operator cap in the fixed metric

`H = M0_CC^{-1}`,

then the generic remainder requirement

`r_C^T H r_C <= W`

closes with **zero metric-conversion loss** by taking

`W(x) = rho2_m0_upper * (a_C(x)^T B_up a_C(x))`.

Here `rho2_m0_upper` is already a **squared operator cap**. It must not be squared a second time.

The source-reification obligation remains separate: this review does not claim that the deployed probe has already certified the exact aliases, block ordering, Cholesky semantics, or interval enclosure needed to instantiate the theorem.

---

## 1. Exact fixed metric on block (4,5,6)

Let

`N = 5000400003`.

The upstream direct block transport gives

`H = M0_CC^{-1}`

with

`H_11 = 50003000000/N`,
`H_22 = 4000000/200739`,
`H_33 = 350003000000/N`,
`H_13 = H_31 = -50000000000/N`,

all other entries zero.

Equivalently, with

`a = 1/7`,
`w3 = 350003000000/N`,
`w2 = 4000000/200739`,
`w1 = 375030000000/(7*N)`,

one has the exact weighted-square identity

`z^T H z = w1*z4^2 + w2*z5^2 + w3*(z6 - z4/7)^2`.

Therefore the downstream target can be written without any matrix inverse as

`w1*r4^2 + w2*r5^2 + w3*(r6-r4/7)^2 <= W`.

This is the preferred small trusted leaf if exact rational arithmetic is desired.

---

## 2. Minimal typed theorem: PSD port budget

### Theorem `psd_port_budget`

Assume:

1. `H` is symmetric positive semidefinite;
2. `B` is symmetric positive semidefinite;
3. `rho2 >= 0`;
4. `r = R a`;
5. the matrix inequality

   `rho2 * B - R^T H R >= 0`

   holds in Loewner order.

Then

`r^T H r <= rho2 * (a^T B a)`.

### Proof

Substitute `r=Ra`. Then

`rho2*a^T B a - r^T H r`

`= a^T (rho2*B - R^T H R) a`

`>= 0`.

No square root, division, condition number, eigenvalue computation, or norm conversion is needed in this consumer theorem.

### Corollary for this task

With `H=M0_CC^{-1}`, `B=B_up`, `rho2=rho2_m0_upper`, and the producer-side PSD witness

`rho2_m0_upper * B_up - R^T H R >= 0`,

set

`W_metric(x) = rho2_m0_upper * (a_C(x)^T B_up a_C(x))`.

Then exactly

`r_C(x)^T H r_C(x) <= W_metric(x)`.

If a scalar source bound `a_C^T B_up a_C <= A_C` is additionally available, one may further collapse to

`W0 = rho2_m0_upper * A_C`.

However, if the generic theorem accepts state-dependent `W(x)`, retaining the actual input energy `a_C^T B_up a_C` is strictly preferable to introducing a coarse scalar `A_C`.

---

## 3. Why the producer name `rho2_m0_upper` is the right typed quantity

A standard producer realization is the following. Suppose

`M0_CC = C0 C0^T`,

hence

`H = M0_CC^{-1} = C0^{-T} C0^{-1}`,

and suppose `B_up` is positive definite. If the source establishes

`|| C0^{-1} R B_up^{-1/2} ||_2^2 <= rho2_m0_upper`,

then for every vector `a`,

`||C0^{-1} R a||_2^2`

`<= rho2_m0_upper * ||B_up^{1/2} a||_2^2`.

The left side is exactly `(Ra)^T H (Ra)`, while the right side is exactly `rho2_m0_upper * a^T B_up a`. Therefore

`R^T H R <= rho2_m0_upper * B_up`.

This derivation explains the `rho2` naming: the producer already returns the **square** of the induced norm. The consumer multiplies by `rho2_m0_upper`; it does not use `rho2_m0_upper^2`.

For trusted implementation, it is cleaner for the source-reification lane to emit the rational/interval **PSD witness directly**:

`rho2_m0_upper * B_up - R^T H R >= 0`.

That removes Cholesky and matrix-square-root semantics from the final consumer checker.

---

## 4. Matching metric means zero conversion tax

Suppose a producer instead controls an output quadratic metric `J`:

`r^T J r <= rho2_J * A`.

To infer an `H`-metric budget one needs an explicit comparison

`H <= kappa * J`.

Only then may one conclude

`r^T H r <= kappa * rho2_J * A`.

The least admissible `kappa` is the corresponding generalized top eigenvalue when the metrics are positive definite.

For `J=H`, the exact comparison constant is `kappa=1`. Therefore a genuine `rho2_m0_upper` packet in the same `M0_CC^{-1}` metric incurs **no condition-number or metric-conversion loss at all**.

This is precisely why `rho2_upper` and `rho2_bchol_upper` must remain separate typed quantities unless their output metrics and comparison factors are explicitly reified.

---

## 5. Counterexample: Euclidean cap cannot be substituted for the matching metric cap

Take a scalar input `a`, `B=1`, and let the port map be

`R a = a e6`

in the block ordering `(4,5,6)`.

Then the Euclidean squared operator cap is exactly

`||Ra||_2^2 = a^2`,

so an Euclidean producer could legitimately return `rho2_upper=1`.

But the matching-metric energy is

`(Ra)^T H (Ra) = H_33 * a^2`

with

`H_33 = 350003000000 / 5000400003`.

Moreover

`350003000000 > 69 * 5000400003 = 345027600207`,

hence

`H_33 > 69`.

Therefore the false substitution

`rho2_m0_upper := rho2_upper = 1`

would underbudget this exact direction by a factor larger than `69`.

So `rho2_upper`, `rho2_bchol_upper`, and `rho2_m0_upper` are not interchangeable merely because all are scalar upper bounds on a squared norm. The metric is part of the theorem type.

---

## 6. Sharpness of the matching-metric constant

Assume `H>0` and `B>0`. The least scalar `rho2_*` satisfying

`R^T H R <= rho2_* B`

is exactly

`lambda_max(B^{-1/2} R^T H R B^{-1/2})`

which equals

`|| H^{1/2} R B^{-1/2} ||_2^2`.

Under the factorization `H=C0^{-T}C0^{-1}`, this is

`||C0^{-1} R B^{-1/2}||_2^2`.

Equality is attained on a top generalized singular/eigenvector whenever the finite-dimensional maximum is attained. Hence, given only this induced-norm information, no universal multiplicative improvement `theta*rho2_*` with `theta<1` is valid.

The matching-metric theorem is therefore sharp in its natural information class.

---

## 7. Applicability / failure branches

### A. Source alias mismatch

If the deployed remainder is not proved to satisfy the exact identity

`r_C = R a_C`

for the same block ordering `(4,5,6)`, the result is

`NOT_APPLICABLE_SOURCE_ALIAS`,

not a mathematical failure of the inequality.

### B. Coordinate permutation

A permutation of the block coordinates must simultaneously conjugate the metric `H`. Merely reordering the vector while keeping the displayed `H` unchanged is invalid. A global sign of `r_C` is harmless because the budget is quadratic, but component reordering is not.

### C. Extra additive remainder

If the real remainder is

`r_total = R a + e`,

the matching cap covers only the `R a` component. The extra `e` requires its own additive/correlation budget; it must not be silently absorbed into `rho2_m0_upper`.

### D. Wrong scalar producer

If only `rho2_upper` or `rho2_bchol_upper` is available, either:

1. reify its exact output metric `J` and prove `H <= kappa J`, paying the explicit `kappa`; or
2. leave this matching-metric child unclosed.

Absent such a comparison, substitution is unsound.

### E. Strict versus non-strict consumer

For a target `r_C^T H r_C <= W`, equality is valid.

If a later theorem needs a strict reserve `r_C^T H r_C < W_star`, then a source packet that only proves equality at the proposed `W_star` is boundary-only and cannot be upgraded to strictness without a positive margin.

---

## 8. Minimal formalization targets

The mathematical work can be split into small leaves:

1. `psd_port_budget`
   - hypotheses: `r=Ra`, `rho2*B - R^T H R` PSD;
   - conclusion: `r^T H r <= rho2*a^T B a`.

2. `block456_metric_quadratic`
   - exact rational identity
     `z^T H z = w1*z4^2 + w2*z5^2 + w3*(z6-z4/7)^2`.

3. `matching_metric_zero_conversion`
   - the comparison constant from `H` to itself is exactly `1`.

4. `euclidean_cap_not_matching_metric`
   - regression with `R a = a e6` showing Euclidean squared cap `1` but matching energy coefficient `H_33>69`.

A Cholesky/spectral-norm theorem may remain source-side if the producer directly emits the PSD witness. That is the smallest trusted interface.

---

## 9. Requested source packet / next step

The source-reification lane should provide, in the exact block order `(4,5,6)`, at least one of the following equivalent packets.

### Preferred packet

- exact source identity `r_C = R a_C`;
- exact `H=M0_CC^{-1}` matching the displayed block metric;
- exact/validated `B_up`;
- rational `rho2_m0_upper >= 0`;
- a machine-checkable PSD witness

  `rho2_m0_upper * B_up - R^T H R >= 0`.

### Alternate producer packet

- exact `M0_CC=C0 C0^T`;
- validated norm bound

  `||C0^{-1} R B_up^{-1/2}||_2^2 <= rho2_m0_upper`;

- exact alias `r_C=R a_C`.

Once either packet is available, this matching-metric budget closes immediately with

`W = rho2_m0_upper * a_C^T B_up a_C`.

No additional metric conversion factor is mathematically justified or needed.

---

## 10. Scope discipline

This result does **not** upgrade source reification, deployed probe correctness, Float64/interval implementation, Lean/kernel checking, provenance, admission, registry state, full P4 closure, or any P5/M4 milestone. It only closes the mathematical matching-metric inequality once the typed producer packet is supplied.
