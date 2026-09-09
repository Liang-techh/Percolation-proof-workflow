---
kind: review_result
review_id: review-T-P5-149-inexact-augmented-range-solve-cap-liuguanyi-20260909T1110Z
task_id: T-P5-149-INEXACT-AUGMENTED-RANGE-SOLVE-CAP
reviewer: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T11:10:00Z
claim_commit: 1c17586001ceaed4962ce9c3eb001d6fd3035f56
inspected_commit: 0ff84435666cfabc8486eced18e42e484462181f
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-148-SEMIDEFINITE-CELL-CROSS-RESIDUAL-SCHUR-CAP-honglianmozun-20260909T1059Z.md
    commit: 6daae6877be6f6d19d2263d170c21b6d090ba1e8
  - path: agent_review_inbox/review-T-P5-141-INEXACT-RANGE-SOLVE-RESIDUAL-BRIDGE-liuguanyi-20260909T0904Z.md
    commit: 138a9ecb30323619bcac1b6b2b39c4d56435e100
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: allow_a_candidate_matrix_range_solve_X_with_signed_residual_R_eq_Q_minus_AX_to_generate_a_valid_T-P5-148_augmented_cap_via_one_residual_block_PSD_certificate; use_the_exact_congruence_to_preserve_affine_cross_cancellation; fail_closed_on_any_kerA_component_of_R; recover_the_same_Loewner_minimal_cap_after_an_exact_residual_correction; do_not_charge_approximate_solve_error_twice
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional matrix/quadratic-form algebra only
exit_code: n/a
---

# T-P5-149 — inexact augmented range solve: exact congruence and residual Schur correction

## 0. Narrow seam and non-overlap

T-P5-148 reduces simultaneous affine and cross residuals in an uncontrolled semidefinite physical-cell direction to the augmented quadratic

`Phi(e,xi) := e^T Q xi - e^T A e`,

with `A=A^T>=0`, and shows that a finite cap is equivalent to a block PSD condition

`[[A,-Q/2],[-Q^T/2,Sigma]] >= 0`.

Its Loewner-minimal cap may be written using an **exact** matrix range solve

`A X = Q`.

A realistic producer may instead expose a candidate matrix `X` and the signed residual

`R := Q-A X`.

This review proves that the inexact solve can be consumed without changing the T-P5-148 architecture.  There is an exact triangular congruence which moves all solve error into one smaller residual Schur block.  Consequently:

- a residual with any unresolved `ker A` component is still an infinite-escape obstruction, however small its norm;
- a range-compatible residual can be absorbed by one root-free block PSD packet;
- an exact residual correction recovers **the same** Loewner-minimal cap as an exact solve of `A X=Q` from the start;
- approximate-solve error is therefore a certificate decomposition issue, not an intrinsic extra tax, unless the residual cap itself is loose.

This does not repeat T-P5-146's dual-canonical residual, T-P5-147's scalar affine residual, or T-P5-148's exact augmented-cap classification.  No source binding, runtime/Float64 semantics, coverage, provenance/admission audit, Lean/kernel compile, registry mutation, or P5 parent closure is attempted.

---

## 1. Setup

Let

- `A=A^T>=0` be an `n x n` real symmetric PSD matrix;
- `Q` be an `n x p` residual map, where in T-P5-148 `p=1+dim(m)` and `Q=[r,-2D]`;
- `X` be an arbitrary `n x p` candidate range solve;
- `R := Q-A X` be its **signed matrix residual**;
- `Sigma=Sigma^T` be a candidate augmented cap.

For `e in R^n`, `xi in R^p`, define

**(1.1)** `Phi(e,xi) := e^T Q xi - e^T A e`.

T-P5-148 asks for

**(1.2)** `Phi(e,xi) <= xi^T Sigma xi`

for every `e,xi`.

Introduce the shifted uncontrolled coordinate

**(1.3)** `v := e-X xi/2`.

Define the signed candidate-solve correction matrix

**(1.4)**

`Gamma_X := (1/4) [ X^T A X + X^T R + R^T X ]`.

`Gamma_X` is symmetric, but it need not be PSD.  Its signed off-diagonal terms are part of the affine/cross cancellation and should not be clipped or separately absolutized.

---

## 2. Main identity: the original cap is congruent to a residual cap

### Theorem A — exact inexact-solve completion identity

For every `e,xi`, with `v=e-Xxi/2`,

**(2.1)**

`Phi(e,xi)`

`= xi^T Gamma_X xi`

`  + v^T R xi - v^T A v`.

Equivalently, for any symmetric `Theta`, if

**(2.2)** `Sigma := Gamma_X + Theta`,

then

**(2.3)**

`xi^T Sigma xi - Phi(e,xi)`

`= [v;xi]^T [[A,-R/2],[-R^T/2,Theta]] [v;xi]`.

### Proof

Use `Q=AX+R` and `e=v+Xxi/2`.  Then

`e^T Q xi-e^T A e`

`= e^T(AX+R)xi-e^T A e`.

The `AX` terms complete exactly:

`e^T AXxi-e^TAe`

`= -(e-Xxi/2)^T A(e-Xxi/2)`

`  + (1/4)xi^T X^T A X xi`.

The residual term is

`e^T Rxi = v^T Rxi + (1/2)xi^T X^T Rxi`.

Since a scalar quadratic only sees the symmetric part,

`(1/2)xi^T X^T Rxi`

`= (1/4)xi^T(X^T R+R^T X)xi`.

Combining gives (2.1), and rearranging gives (2.3).

---

## 3. Exact matrix congruence

Let

**(3.1)**

`M_Q(Sigma) := [[A,-Q/2],[-Q^T/2,Sigma]]`,

**(3.2)**

`M_R(Theta) := [[A,-R/2],[-R^T/2,Theta]]`,

and the invertible block-triangular matrix

**(3.3)**

`T_X := [[I,X/2],[0,I]]`.

A direct block multiplication gives

### Theorem B — triangular residual congruence

**(3.4)**

`T_X^T M_Q(Sigma) T_X`

`= M_R(Sigma-Gamma_X)`.

Therefore

**(3.5)**

`M_Q(Sigma)>=0`

**iff**

`M_R(Sigma-Gamma_X)>=0`.

This is stronger than a one-way estimate: consuming an approximate matrix solve is exactly a congruence transformation of the T-P5-148 cap.

### Consequence

A producer may expose any convenient candidate `X`; the trusted consumer need only verify the signed residual `R=Q-AX`, construct/check `Gamma_X`, and verify a residual block PSD cap.  No inverse, pseudoinverse, square root, eigenbasis, singular value, or kernel basis is needed.

---

## 4. Root-free residual packet

Choose a symmetric matrix `Theta` satisfying

**(4.1)**

`[[A,-R/2],[-R^T/2,Theta]] >= 0`.

Then by Theorem A,

**(4.2)**

`Phi(e,xi) <= xi^T (Gamma_X+Theta) xi`

for all `e,xi`.

Thus

**(4.3)** `Sigma := Gamma_X+Theta`

is a valid T-P5-148 augmented cap.

### Division-free rational checker form

For exact-rational data, halves and quarters may be removed completely.  Define

**(4.4)**

`C_X := X^T A X + X^T R + R^T X`.

Instead of (4.1)-(4.3), a checker may verify

**(4.5)** `R = Q-A X`,

**(4.6)**

`[[4A,-2R],[-2R^T,4Theta]] >= 0`,

**(4.7)**

`4 Sigma = C_X + 4 Theta`.

Then automatically

**(4.8)**

`[[4A,-2Q],[-2Q^T,4Sigma]] >= 0`.

So the whole interface is polynomial/rational matrix arithmetic plus PSD checking.

---

## 5. Exact obstruction: approximate solve error cannot hide a nullspace escape

Because `AX` has every column in `range(A)`,

**(5.1)**

`range(R) subseteq range(A)`

**iff**

`range(Q) subseteq range(A)`.

Indeed, `Q=AX+R` and `AX` is already range-valued.

Applying T-P5-148's exact range criterion to the residual block gives:

### Theorem C — residual-cap existence classification

For `A=A^T>=0`, the following are equivalent:

1. there exists a finite symmetric `Theta` satisfying (4.1);
2. `range(R) subseteq range(A)`;
3. `range(Q) subseteq range(A)`;
4. there exists a finite original augmented cap `Sigma` satisfying `M_Q(Sigma)>=0`.

Hence an approximate solve does not weaken or strengthen the true finite-escape condition.

### Fail-closed nullspace test

If there exist `k in ker A` and `xi` such that

`k^T R xi != 0`,

then with `v=t k`,

`v^T Rxi-v^TAv = t k^T Rxi`

is unbounded above for one sign of `t`.  No finite `Theta`, no quotient multiplier, and no additive scalar budget can repair that branch.

A tiny Euclidean residual is therefore irrelevant if it has any unresolved `ker A` component.

---

## 6. Exact residual correction recovers the same Loewner-minimal cap

Assume the range condition holds and choose any exact residual correction `Z` satisfying

**(6.1)** `A Z=R`.

Define

**(6.2)** `X_* := X+Z`.

Then

**(6.3)** `A X_*=Q`.

The Loewner-minimal residual cap is

**(6.4)**

`Theta_* := (1/4) R^T Z = (1/4) Z^T A Z >=0`.

By T-P5-148 applied to `R`, every admissible `Theta` satisfies

**(6.5)** `Theta-Theta_*>=0`.

Now add the signed candidate-solve term:

### Theorem D — exact minimal-cap recovery

**(6.6)**

`Gamma_X + Theta_*`

`= (1/4) Q^T X_*`

`= (1/4) X_*^T A X_*`.

The right-hand side is exactly the Loewner-minimal T-P5-148 cap that would have been obtained from the exact solve `AX_*=Q` at the start.

### Proof

Use `R=AZ` and `Q=A(X+Z)`:

`4(Gamma_X+Theta_*)`

`= X^TAX + X^TR + R^TX + R^TZ`

`= X^TAX + X^TAZ + Z^TAX + Z^TAZ`

`= (X+Z)^T A(X+Z)`.

Also `A(X+Z)=Q`, giving (6.6).

Therefore an inexact `X` creates **no intrinsic mathematical tax**.  Any overpayment comes only from choosing a residual cap `Theta>Theta_*`.

More precisely, if `Sigma=Gamma_X+Theta`, then

**(6.7)**

`Sigma-Sigma_* = Theta-Theta_* >=0`,

where `Sigma_*=(1/4)Q^TX_*` is the intrinsic minimal augmented tax.

The solve error and the residual-cap slack are not two separate debits; they are two descriptions of the same completion.

---

## 7. Exact gap factorization after correction

With `AZ=R`, the residual block at its minimal cap factors as

**(7.1)**

`[v;xi]^T M_R(Theta_*)[v;xi]`

`= (v-Zxi/2)^T A(v-Zxi/2)`.

Since `v=e-Xxi/2`,

**(7.2)**

`v-Zxi/2 = e-(X+Z)xi/2 = e-X_*xi/2`.

Hence the original T-P5-148 gap is exactly

**(7.3)**

`xi^T Sigma_* xi-Phi(e,xi)`

`= (e-X_*xi/2)^T A(e-X_*xi/2) >=0`.

This gives a clean proof-level bridge from an approximate producer solve to the exact completion without changing the target quadratic.

---

## 8. Gauge invariance of the candidate solve

Suppose two candidate matrices `X` and `X'` have the **same** residual `R`:

`Q-AX = Q-AX' = R`.

Then

`A(X'-X)=0`.

If a finite residual cap exists, `range(R) subseteq range(A)`, hence every column of `R` is orthogonal to `ker A`.  Therefore all terms involving `X'-X` vanish in (1.4), and

### Lemma — nullspace-gauge invariance

**(8.1)** `Gamma_X = Gamma_X'`.

Thus the inexact-solve packet is insensitive to arbitrary `ker A` components of the candidate `X` once the residual branch is actually admissible.  A producer need not canonicalize `X` before presenting it.

This is useful for singular solves: different linear solvers may return different nullspace representatives, but the mathematically consumable signed cap is unchanged.

---

## 9. Exact rational regression examples

### Example 9.1 — singular `A`, nonzero residual, exact recovery

Take

`A = diag(1,0)`,

`Q = [[2,-1],[0,0]]`,

and candidate

`X = [[1,0],[7,3]]`.

Then

`AX = [[1,0],[0,0]]`,

so

`R = Q-AX = [[1,-1],[0,0]]`.

The arbitrary second row of `X` is a pure `ker A` gauge and does not affect the packet.

Choose

`Z = [[1,-1],[0,0]]`,

so `AZ=R`.  Then

`X_* = X+Z`

has first row `(2,-1)` and satisfies `AX_*=Q`.

The minimal residual cap is

`Theta_* = (1/4) [[1,-1],[-1,1]]`.

The signed candidate term is

`Gamma_X = (1/4) [[3,-1],[-1,0]]`.

Hence

`Sigma_* = Gamma_X+Theta_*`

`= (1/4) [[4,-2],[-2,1]]`

`= [[1,-1/2],[-1/2,1/4]]`.

Directly,

`(1/4)Q^T X_*`

gives the same matrix.  Thus the approximate solve plus its exact residual correction recovers the exact T-P5-148 optimum with zero artificial slack.

### Example 9.2 — arbitrarily small nonrange residual is fatal

Take

`A=diag(1,0)`,

`Q=(1,epsilon)^T`,

`X=(1,0)^T`,

with any nonzero rational `epsilon`, however small.

Then

`R=(0,epsilon)^T`.

Let `k=(0,1)^T in ker A`.  Since

`k^T R=epsilon !=0`,

for `v=t k`, `xi=1`,

`v^T Rxi-v^TAv = t epsilon`

is unbounded above.  Therefore no finite residual block cap `Theta` and no original augmented cap `Sigma` exist.

This is the exact reason an ordinary solver tolerance such as `||R||<=10^-12` cannot replace range compatibility on an unbounded semidefinite direction.

---

## 10. T-P5-148 affine/cross specialization

For the actual T-P5-148 structure

`Q=[r,-2D]`,

one may choose a candidate correction matrix

`X=[z,-2Z]`.

Then

**(10.1)**

`R=Q-AX`

`=[ r-Az , -2(D-AZ) ]`.

The first residual column is the remaining affine-range defect and the other columns are the remaining cross-range defects.  They must be kept together in the same residual block cap.

The correction matrix `Gamma_X` contains signed constant/linear/curvature coupling between these columns.  Splitting them into independent absolute scalar and matrix budgets before forming `Gamma_X+Theta` destroys the cancellation that T-P5-148 was designed to preserve.

Hence the preferred source-to-math interface is:

1. form the full signed augmented `Q=[r,-2D]`;
2. expose one candidate matrix solve `X`;
3. form the full signed residual `R=Q-AX`;
4. check one residual block PSD cap `M_R(Theta)>=0`;
5. transport by `Sigma=Gamma_X+Theta`;
6. only then partition `Sigma` into constant/linear/curvature pieces for the positive-definite quotient consumer.

---

## 11. Minimal theorem statements for formalization

A small formal library could expose the following leaves.

### Leaf A — exact congruence

Assumptions:

- `A=A^T`;
- `R=Q-AX`;
- `Gamma=(X^TAX+X^TR+R^TX)/4`.

Conclusion:

`T_X^T [[A,-Q/2],[-Q^T/2,Sigma]] T_X`

`= [[A,-R/2],[-R^T/2,Sigma-Gamma]]`.

### Leaf B — residual cap transport

Assumptions:

- `A>=0`;
- `[[A,-R/2],[-R^T/2,Theta]]>=0`;
- `Sigma=Gamma+Theta`.

Conclusion:

`[[A,-Q/2],[-Q^T/2,Sigma]]>=0`.

### Leaf C — exact range obstruction

Assumptions:

- `A=A^T>=0`.

Conclusion:

A finite residual cap exists iff `range(R) subseteq range(A)`, equivalently iff `range(Q) subseteq range(A)`.

### Leaf D — minimal correction recovery

Assumptions:

- `AZ=R`;
- `X_*=X+Z`.

Conclusion:

`Gamma_X + (R^TZ)/4 = (Q^T X_*)/4`,

and every admissible residual cap is Loewner-above `(R^TZ)/4`.

### Preferred exact-rational checker contract

Avoid division by storing fourfold quantities:

- exact matrices `A,Q,X,R`;
- exact identity `R=Q-AX`;
- symmetric `Theta4=4Theta`;
- PSD witness for `[[4A,-2R],[-2R^T,Theta4]]`;
- exact `C_X=X^TAX+X^TR+R^TX`;
- exact `Sigma4=C_X+Theta4`.

Then the consumer only needs to infer the PSD of

`[[4A,-2Q],[-2Q^T,Sigma4]]`.

---

## 12. Dependencies and open boundaries

This mathematical child depends on the semantic meaning of the T-P5-148 matrices, but it does **not** prove any actual source binding.

Still open:

- actual same-key `A,Q,X` from the deployed/source packet;
- exact reification of the signed matrix residual `R=Q-AX` from runtime or producer arithmetic;
- proof that the relevant physical-cell null direction is genuinely uncontrolled as assumed by T-P5-144/148;
- any cell/tube/path/FD/reference-halo coverage;
- actual quotient `G_M,R_cell` and downstream multiplier packet;
- Float64 solver semantics and any relation between numerical tolerance and exact-real `R`;
- Lean/kernel formalization and independent validation by 封不觉;
- provenance/admission/registry/P5-parent closure.

A numerical norm bound on `R` is **not** a substitute for the block PSD/range condition.  If actual runtime only provides floating residual entries, they first need an exact-real enclosure/reification whose possible set is itself proven range-compatible or safely capped; otherwise the semidefinite escape remains open.

---

## 13. Requested handoff

The shortest useful next source packet is now:

`(cellKey, resetKey, A, Q, X, R, Theta4)`

with exact same-key identities

`R=Q-AX`

and

`[[4A,-2R],[-2R^T,Theta4]] >= 0`.

The mathematical adapter then constructs

`Sigma4 = X^TAX + X^TR + R^TX + Theta4`

and hands the resulting signed constant/linear/curvature correction to the existing T-P5-148 quotient path.

If an exact residual correction `AZ=R` is available, the producer can instead expose it and recover the intrinsic minimal cap exactly.  If no such range-compatible packet exists, the correct outcome is an explicit obstruction, not a larger scalar tolerance.
