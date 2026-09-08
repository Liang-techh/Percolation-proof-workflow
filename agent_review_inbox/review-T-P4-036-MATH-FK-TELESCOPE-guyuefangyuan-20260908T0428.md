---
kind: review_result
review_id: review-T-P4-036-MATH-FK-TELESCOPE-guyuefangyuan-20260908T0428
task_id: T-P4-036-MATH-FK-TELESCOPE
parent_task_id: T-P4-036
source_agent: 古月方源
created_at: 2026-09-08T04:28:00-06:00
integration_status: pending
admission_label: pending
claim_commit: 24d972035e4ebb643c5aa5b0d5624c73bbc8caed
inspected_commits:
  - 19f87c5e208c60051a1e3a0864c780ad07e445cf
  - a0ab71fe3342bed66944c5e19fe22b36ea656f55
  - c67ab76dd29509c5545466d13e53f09d3ae00a61
  - dfb96e8dfe275437e72d80a2e6d44d85210d8ccf
proposed_integration_target: theorem
requested_action: add a source-independent standard-DH link metric/telescoping child under the finite-DH propagation frontier; keep deployed source convention, Float64/libm, COM/Jacobian/M/C/G and coverage as separate obligations
---

# T-P4-036 — exact-real DH link metric and finite-chain telescoping bound

## 0. Why this is new rather than another phase-cell proof

The all-12 exact-real quarter-turn table is already frozen and compiled under `T-P4-036.2`; I therefore do not repeat it. The still-open mathematical seam is downstream: once an upstream leaf has supplied exact-real angle perturbation radii, how can a finite DH product consume them without independently intervalizing every `sin/cos` entry?

For the standard DH matrix, there is a much stronger structural answer. Its Frobenius geometry is almost constant: the one-link matrix norm is independent of both angles, the theta and alpha tangent directions are Frobenius-orthogonal, and their squared lengths are constant. This yields an exact rational square budget for a whole finite chain.

This review is source-independent mathematics. The deployed `dhport_lib.jl` convention must still be bound separately before using the theorem on Route-B execution.

---

## 1. Explicit standard-DH object

For real parameters `a,d,theta,alpha`, define

```text
A(a,d,theta,alpha) =
[ cθ   -sθ cα    sθ sα    a cθ ]
[ sθ    cθ cα   -cθ sα    a sθ ]
[  0       sα       cα       d ]
[  0        0        0        1 ]
```

where `cθ=cos(theta)`, `sθ=sin(theta)`, `cα=cos(alpha)`, `sα=sin(alpha)`.

Everything below refers to this explicitly defined matrix. A source adapter may consume it only after proving that the deployed link transform uses this convention or an exactly transported equivalent convention.

Write `||X||_F^2` for the sum of squares of all 16 real entries.

---

## 2. Exact one-link norm invariant

Using only `sin^2+cos^2=1`, the 3x3 rotation block has Frobenius square `3`, the translation column has square `a^2+d^2`, and the homogeneous bottom-right entry contributes `1`. Therefore

**Lemma 2.1**

```text
||A(a,d,theta,alpha)||_F^2 = 4 + a^2 + d^2.          (2.1)
```

The right-hand side is independent of `theta`, `alpha`, and every quarter-turn phase. Define

```text
M(a,d) := 4 + a^2 + d^2.                              (2.2)
```

This is useful for product propagation because every prefix/suffix factor gets the same exact angle-free square bound.

---

## 3. Exact theta-only difference identity

Keep `a,d,alpha` fixed and compare `theta` with `theta'`. Put

```text
Δc = cos(theta)-cos(theta')
Δs = sin(theta)-sin(theta').
```

Directly expanding the eight changing entries gives

```text
||A(theta,alpha)-A(theta',alpha)||_F^2
  = (2+a^2) * (Δc^2 + Δs^2).                           (3.1)
```

The chord identity gives

```text
Δc^2 + Δs^2
  = 2 - 2 cos(theta-theta')
  = 4 sin^2((theta-theta')/2).                         (3.2)
```

Hence the exact formula

```text
||ΔA_theta||_F^2
  = 4(2+a^2) sin^2((theta-theta')/2).                  (3.3)
```

and, from `|sin x|<=|x|`, the global square bound

```text
||ΔA_theta||_F^2
  <= (2+a^2) * (theta-theta')^2.                       (3.4)
```

No small-angle hypothesis is needed.

### Phase cancellation

If the source row is `theta=q+k*pi/2` and the comparison row uses the same frozen `k`, then

```text
theta-theta' = q-q'.                                   (3.5)
```

Thus every `k in {-1,0,+1}` has exactly the same link perturbation constant. The 12-row phase table is required for source identity, but it disappears from the quantitative theta perturbation budget.

---

## 4. Exact alpha-only difference identity

Keep `a,d,theta` fixed and vary `alpha` to `alpha'`. A direct expansion gives

```text
||A(theta,alpha)-A(theta,alpha')||_F^2
  = 2 * [ (cos alpha-cos alpha')^2
        + (sin alpha-sin alpha')^2 ]                    (4.1)
  = 8 sin^2((alpha-alpha')/2)                           (4.2)
  <= 2 (alpha-alpha')^2.                                (4.3)
```

Again the constant is independent of theta and of the alpha quarter-turn phase.

This matters for the deployed seam because ideal alpha is constant but the exact-real decoding of a formed/stored Float64 alpha may carry a nonzero formation error.

---

## 5. Strong simultaneous two-angle metric bound

The standard DH map has an even cleaner differential structure. Differentiate entrywise:

```text
A_theta := ∂A/∂theta,
A_alpha := ∂A/∂alpha.
```

A direct square expansion gives the exact identities

```text
||A_theta||_F^2 = 2 + a^2,                              (5.1)
||A_alpha||_F^2 = 2,                                    (5.2)
<A_theta,A_alpha>_F = 0.                                (5.3)
```

These hold at every `(theta,alpha)`.

For the straight parameter path

```text
gamma(t)=A(a,d, theta+t*δtheta, alpha+t*δalpha), 0<=t<=1,
```

its Frobenius speed is therefore constant:

```text
||gamma'(t)||_F^2
  = (2+a^2) δtheta^2 + 2 δalpha^2.                      (5.4)
```

Integrating the path and applying the norm triangle inequality yields

**Theorem 5.1 — standard-DH two-angle Lipschitz square**

```text
||A(theta,alpha)-A(theta',alpha')||_F^2
 <= (2+a^2)(theta-theta')^2
    + 2(alpha-alpha')^2.                                (5.5)
```

The coefficients are locally sharp: varying only theta or only alpha and taking the increment to zero recovers exactly the tangent squares `(2+a^2)` and `2`.

### Calculus-free fallback

If a first Lean implementation should avoid matrix-valued path integration, Sections 3 and 4 plus the triangle inequality give the weaker but purely elementary statement

```text
||ΔA||_F^2
 <= 2(2+a^2) δtheta^2 + 4 δalpha^2.                    (5.6)
```

So the route has both a sharp analytic theorem and a small algebraic fallback; neither requires source/runtime claims.

---

## 6. Exact finite-product telescoping theorem

Consider `n>=1` standard-DH links

```text
A_i = A(a_i,d_i,theta_i,alpha_i),
A_i' = A(a_i,d_i,theta_i',alpha_i')
```

with the same geometric constants `a_i,d_i`. Define

```text
P  = A_1 A_2 ... A_n,
P' = A_1' A_2' ... A_n'.
```

Use the exact telescoping identity

```text
P-P'
 = Σ_{i=1}^n
   A_1...A_{i-1} (A_i-A_i') A_{i+1}'...A_n'.          (6.1)
```

Define angle-free factor budgets

```text
M_i := 4 + a_i^2 + d_i^2,                              (6.2)
R_i := (2+a_i^2)(theta_i-theta_i')^2
       + 2(alpha_i-alpha_i')^2.                         (6.3)
```

By (2.1), (5.5), Frobenius submultiplicativity, and

```text
||Σ_i X_i||_F^2 <= n Σ_i ||X_i||_F^2,                  (6.4)
```

each telescoping summand has square at most

```text
R_i * Π_{j != i} M_j.                                   (6.5)
```

Therefore:

**Theorem 6.1 — finite-DH product perturbation**

```text
||P-P'||_F^2
 <= n * Σ_{i=1}^n [ R_i * Π_{j != i} M_j ].            (6.6)
```

This final certificate is square-only. If `a_i,d_i` and the angle-error radii are rational/dyadic, the right side is exact rational; the checker need not evaluate square roots, trigonometric functions, eigenvalues, or matrix inverses.

For the six-link Route-B shape, simply set `n=6`:

```text
||P-P'||_F^2
 <= 6 Σ_i R_i Π_{j != i} M_j.                           (6.7)
```

The factor `6` is the generic finite-sum Cauchy factor. It can later be improved by weighted summation if needed, but no optimization is necessary for soundness.

---

## 7. Two immediate exact-rational corollaries

### 7.1 Ideal q-box diameter

For the exact-real ideal chain, alpha is fixed per link and the frozen theta phase cancels. If both configurations satisfy

```text
|q_i| <= 3/20,
|q_i'| <= 3/20,
```

then

```text
|q_i-q_i'| <= 3/10,
R_i <= (2+a_i^2) * 9/100.
```

Thus

```text
||P(q)-P(q')||_F^2
 <= (27/50) * Σ_i (2+a_i^2) Π_{j != i}(4+a_j^2+d_j^2). (7.1)
```

This is a whole-box exact-real diameter bound with no rowwise trig intervals.

### 7.2 Radius from the q=0 center

Taking `q_i'=0` instead gives `|q_i-q_i'|<=3/20` and

```text
||P(q)-P(0)||_F^2
 <= (27/200) * Σ_i (2+a_i^2) Π_{j != i}(4+a_j^2+d_j^2). (7.2)
```

Again every coefficient is exact rational once the geometric constants are rationalized/bound by the source lane.

---

## 8. How this composes with the existing Frobenius consumer without duplicating it

The existing `T-P4-022` lane is the generic matrix-action theorem of the form

```text
||T z||_2^2 <= ||T||_F^2 ||z||_2^2
```

(or an entrywise upper-factor version). This review does not re-prove that generic bridge.

Instead it supplies a DH-specific bound on `||P-P'||_F^2`. For the homogeneous frame origin `e4=(0,0,0,1)`, the generic consumer then gives

```text
||(P-P') e4||_2^2 <= ||P-P'||_F^2.                     (8.1)
```

Therefore (6.6) can immediately become a frame-origin position perturbation theorem once the generic matrix-action seam is available. The same pattern works for any fixed homogeneous point with a separately bounded Euclidean norm.

This is the first finite-DAG target that uses the exact trigonometric correlation `sin^2+cos^2=1` all the way through the link matrix instead of widening each entry independently.

---

## 9. Important obstruction / semantic boundary

The theorem is **not convention-free**. A modified-DH ordering, a transposed convention, a different translation placement, or a transform that already includes another runtime correction may change the exact constants and the tangent orthogonality calculation.

Therefore the source adapter must prove one of:

1. deployed link transform equals the explicit matrix in Section 1; or
2. deployed transform is obtained from it by fixed orthogonal row/column operations that preserve Frobenius norm; or
3. a separate theorem is derived for the actual convention.

A textual label such as “DH matrix” is not enough.

Likewise, (5.5)/(6.6) compare exact real matrices evaluated at exact real angles. They do not prove that Julia/libm output equals those trigonometric values. A machine-output error must be added by the independent libm leaf.

---

## 10. Suggested Lean theorem decomposition

The smallest useful statements are:

```text
standardDH_frobenius_sq
  : frobSq (standardDH a d th al) = 4 + a^2 + d^2

standardDH_theta_diff_frobenius_sq
  : frobSq (standardDH a d th al - standardDH a d th' al)
    = (2+a^2) * ((cos th-cos th')^2 + (sin th-sin th')^2)

standardDH_theta_diff_sq_le
  : frobSq (...) <= (2+a^2)*(th-th')^2

standardDH_alpha_diff_frobenius_sq
  : frobSq (...) = 2*((cos al-cos al')^2 + (sin al-sin al')^2)

standardDH_alpha_diff_sq_le
  : frobSq (...) <= 2*(al-al')^2
```

For the first formal pass, the elementary simultaneous fallback is preferable:

```text
standardDH_two_angle_diff_sq_le_fallback
  : frobSq (A th al - A th' al')
    <= 2*(2+a^2)*(th-th')^2 + 4*(al-al')^2
```

Then isolate the finite-product lemma in square form:

```text
product_diff_sq_le_card_sum
  : frobSq (prod A - prod A')
    <= n * Σ i, Ri * Π j != i, Mi
```

The sharper constant-metric theorem (5.5) can be a second analytic sidecar if matrix-valued calculus imports make the first implementation unnecessarily large.

A source-facing six-link theorem should consume only typed `a_i,d_i`, real angle differences/error radii, and the exact matrix-convention binding. It should not parse receipts or mention Float64/libm.

---

## 11. Remaining obligations

This child does **not** close:

- deployed standard-vs-modified DH convention/source identity;
- actual rational/enclosed `a_i,d_i` constants and unit conventions;
- Float64 angle formation and exact-real decoding;
- libm `sin/cos` output inclusion;
- extra arithmetic error in matrix assembly/multiplication;
- COM location, Jacobian differentiation, mass/Coriolis/gravity propagation;
- central finite differences, regularization, backslash solve;
- P8/flowpipe/box coverage;
- Lean/kernel/comparator receipt or P4/M4 admission.

The current status is **pending mathematical child**. The useful next step is a very small Lean sidecar for Sections 2–4 and the square telescoping lemma, while the source lane separately proves the deployed transform convention.
