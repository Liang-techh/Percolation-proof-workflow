---
kind: review_result
review_id: review-T-P5-105-NONSYMMETRIC-REFERENCE-COLLAR-liuguanyi-20260908T2210Z
task_id: T-P5-105-NONSYMMETRIC-REFERENCE-COLLAR
source_agent: 柳冠一
created_at: 2026-09-08T22:10:00Z
claim_commit: 1ebd3f503003b523137ae2e9f7a5ba2ff08b18da
inspected_commit: 051e08b78f19539124b37d5a2e9a910ec999d025
upstream_reference_review_commits:
  - 8ccfd27b9a314f11383c5126feb6257ac5526af5
  - 6bbb8bd15c07a96bf4deabce3b165bc53a5119c2
upstream_math_source_blob: 510ada470ce283b2300b2e34c1b22243603155e6
status: CONDITIONAL_PASS_WITH_EXACT_RATIONAL_PACKET
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize the skew-stiffness reference collar and bind one chosen exact-real reference coefficient semantics; then consume the resulting Vref collar in the P5-098 hybrid anchor budget without exporting qbar/vbar tables
lean_compile_status: not_run
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

# T-P5-105 — nonsymmetric Route-B reference collar and hybrid-budget bridge

## 0. Why this child is needed

T-P5-104 gives a clean cross-energy collar for a nominal equation with a symmetric stiffness matrix. The concrete Route-B block isolated by T-P5-018 is not of that form:

```text
M = diag(350003/3000000, 200739/4000000),
D = diag(4/5, 13/20),
B = [[3/4,   -1/100],
     [-1/200, 29/50]],
g = (1/5,1/10)^T.
```

Its stiffness splits exactly as

```text
B = K - A,
K = [[3/4,-3/400],[-3/400,29/50]],
A = [[0,1/400],[-1/400,0]],
A^T = -A.
```

Therefore one may not instantiate T-P5-104 by silently replacing `B` with `K`: that changes the ODE. The skew term must be transported into the dissipation identity. This review proves that bridge and, for the already-recorded 2x2 coefficient packet, obtains a much sharper fully rational collar that can feed the P5-098 hybrid anchor budget.

The result is exact-real mathematics only. It does not prove which of the ideal decimal, CSV-token, or binary64-decoded coefficient semantics is the deployed reference law.

---

## 1. Exact skew-reference derivative identity

Let `M,D,K` be symmetric, `A` skew-symmetric, and let

```text
q' = v,
M v' + D v + (K-A)q = g w.
```

Equivalently,

```text
M v' + D v + K q = A q + g w.
```

Define

```text
V(q,v)
 := 1/2 v^T M v
  + 1/2 q^T K q
  + q^T M v
  + 1/2 q^T D q.
```

A direct differentiation, using `q^T A q=0`, gives the exact identity

```text
V'
 = - v^T(D-M)v
   - q^T K q
   + v^T A q
   + (q+v)^T g w.                              (1)
```

Define `x=(q,v)` and

```text
P := [[K+D, M],
      [M,   M]],

Q := [[K,      A/2],
      [A^T/2, D-M]],

c := (g,g).
```

Then

```text
V = 1/2 x^T P x,
Qd := x^T Q x
    = q^T K q + v^T(D-M)v - v^T A q,
V' = -Qd + w c^T x.                              (2)
```

This is the correct nonsymmetric analogue of T-P5-104. The skew stiffness does not disappear; it becomes the signed cross block of `Q`.

### Minimal theorem statement

`skew_reference_cross_energy_derivative`

Inputs: symmetry of `M,D,K`, skew-symmetry of `A`, and the two first-order reference equations.

Output: (1)/(2) exactly.

No inverse, square root, eigenvalue, or trajectory table is needed.

---

## 2. Coarse rational collar already follows from T-P5-018 constants

Let

```text
N := ||q||^2 + ||v||^2.
```

The T-P5-018 rational estimates remain applicable:

```text
v^T(D-M)v + q^T K q >= (229/400) N,
v^T A q <= (1/800) N,
V <= (21/25) N.
```

Hence

```text
Qd >= (457/800) N.                              (3)
```

For `g=(1/5,1/10)` we have exactly `||g||^2=1/20`; therefore

```text
((q+v)^T g)^2 <= (1/10) N.                      (4)
```

If `w^2 <= Wbar`, then the input power `p=w(q+v)^Tg` satisfies

```text
p^2 <= (Wbar/10) N.
```

Use the exact completed-square absorption

```text
|p| <= (457/1600)N + (40/457)Wbar,              (5)
```

because four times the product of the two right-hand charges is exactly `Wbar*N/10`.
Combining (2),(3),(5) and `V<=21N/25` gives

```text
V' <= -(457/1344) V + (40/457) Wbar.            (6)
```

Thus a non-strict invariant collar level `R` only needs the division-free gate

```text
53760 Wbar <= 208849 R,                          (7)
```

and strict first-exit inwardness uses `<`.

This coarse theorem is useful because it needs only scalar rational inequalities. It is not the best packet for the P5-098 budget; the next section gives a substantially sharper exact certificate.

---

## 3. Sharpened exact rational packet for the Route-B 2x2 reference

For the concrete coefficient packet above, the following three rational constants work simultaneously:

```text
lambda = 9/10,
chi    = 3/20,
C_B    = 67/2.
```

Let

```text
W_B := diag(3/2,3/2,4/5,4/5),
pB(q,v) := x^T W_B x.
```

The required exact quadratic certificates are

```text
2 Q - (9/10) P >= 0,                            (R)
(3/20) Q - c c^T >= 0,                          (I)
(67/2) P - 2 W_B >= 0.                          (B)
```

For the T-P5-018 ideal exact `M`, direct Sylvester checks give strictly positive leading principal minors for all three matrices. For example:

```text
(R): 21/200,
     87951/16000000,
     158649107930333/25000000000000000,
     3398603864895036402951109643/
       480000000000000000000000000000;

(I): 29/400,
     328719/64000000,
     171712901343/1280000000000000,
     215671782413865069/102400000000000000000000;

(B): 1957/40,
     1196234559/640000,
     746202500032751919/200000000000000,
     6883183787574508470066821641/
       256000000000000000000000000.
```

All are positive, so the three matrices are positive definite.

A separate exact-rational sanity check on the P5-098 CSV decimal-token mass

```text
m11 = 116667666666667/10^15,
m22 = 200739/4000000
```

also leaves all four leading principal minors of (R),(I),(B) strictly positive. The same is true for the exact binary64 fractions recorded by P5-098. This is only arithmetic robustness evidence: deployed Julia parse/assembly/source equality remains an independent obligation.

From (R),

```text
Qd >= (9/10) V.                                 (8)
```

From (I),

```text
(c^T x)^2 <= (3/20) Qd.                         (9)
```

If `w^2<=Wbar`, then

```text
p^2 <= (3/20) Wbar Qd.
```

Choose `theta=1/2` and `beta=(3/40)Wbar`. Then

```text
4 theta beta = (3/20)Wbar,
```

so the T-P5-104 power-square absorption applies with equality at the scalar gate. Consequently

```text
V' <= -(9/20) V + (3/40) Wbar.                  (10)
```

Multiplying by `9/20` gives the collar syntax

```text
(9/20)V' <= -(81/400)V + (27/800)Wbar.          (11)
```

The inward boundary test is now exceptionally simple:

```text
Wbar <= 6 R,                                     (12)
```

with `<` for strict first-exit inwardness.

Finally (B) gives the exact storage-to-anchor-budget bridge

```text
pB(q,v) <= (67/2) V(q,v).                       (13)
```

This is the missing cross-layer theorem between a compact RefSpec-generated reference collar and the P5-098 hybrid physical-domain predicate.

---

## 4. Direct hybrid-anchor consumer

Suppose on a time interval:

```text
w(t)^2 <= Wbar,
Vref(t) <= R,
pD(actual(t)) <= PDbar.
```

Then (13) implies

```text
pD(actual) + pB(reference) <= PDbar + (67/2)R.
```

Therefore the P5-098 physical anchor condition `pD+pB<=rho` follows from the division-free scalar gate

```text
2 PDbar + 67 R <= 2 rho.                         (14)
```

If one chooses the smallest non-strict collar level allowed by (12), `R=Wbar/6`, then (14) becomes

```text
PDbar + (67/12) Wbar <= rho.                     (15)
```

For the currently used ideal `rho=28/5`, this is exactly

```text
60 PDbar + 335 Wbar <= 336.                      (16)
```

This is a useful quantitative seam: no qbar/vbar trajectory table is needed in the trusted interface. A source lane may instead provide a canonical `RefSpec`, the common input amplitude `Wbar`, the reference initial binding, and an actual remote budget `PDbar`.

For example, at `Wbar=1` the sufficient remaining remote allowance is only

```text
PDbar <= 1/60.
```

This does **not** say the anchor fails when `PDbar>1/60`: (16) is a sufficient consumer based on this particular rational packet, not a necessary physical bound. It does show exactly how much source budget this packet leaves.

---

## 5. Initial reference identity composes cleanly with P5-103

P5-103 proved that the canonical reference can be chosen with the same initial block state. Then, without evaluating a trajectory table,

```text
qbar(t0)=qB(actual(t0)),
vbar(t0)=vB(actual(t0)).
```

The existing initial ball gives `N0<=9/400`. Using `V<=21N/25`,

```text
Vref(t0) <= (21/25)(9/400) = 189/10000.          (17)
```

Hence the complete reference-side source contract may be reduced to:

```text
ReferenceKey -> RefSpec
+ same initial block identity
+ exact coefficient semantics M,D,B,g
+ input amplitude w^2<=Wbar
+ rational matrix certificates (R),(I),(B)
+ first-exit/domain coverage for the chosen collar R.
```

The reference trajectory itself is derived by the unique ODE solution and need not be a primitive artifact.

---

## 6. Exact obstruction to a naive T-P5-104 instantiation

The concrete matrix has

```text
B45=-1/100,
B54=-1/200,
```

so `B` is not symmetric. Its symmetric part has both off-diagonals `-3/400`; the difference is precisely the nonzero skew matrix `-A`.

Therefore a theorem requiring a symmetric stiffness cannot be source-bound by simply writing `K:=B`. Nor may one replace the actual equation by `M v'+Dv+Kq=gw`, because the missing term `Aq` changes the vector field. The correct bridge is either:

1. retain `Aq` as a state-dependent signed input and prove its correlation with the storage; or
2. use the exact skew-reference storage above, where the term is absorbed into the signed dissipation matrix `Q` before any absolute-value enclosure.

This review takes route 2. As elsewhere in P4/P5, forming the correlated signed quadratic form before enclosure is essential.

---

## 7. Suggested formalization interface

Small source-independent Lean leaves:

```text
skew_reference_cross_energy_derivative
skew_reference_rate_of_psd
skew_reference_power_square_of_psd
reference_block_budget_of_storage_psd
reference_collar_theta_half
hybrid_budget_of_reference_storage
```

The final scalar consumer can be stated without matrix inverses or square roots:

```text
w2 <= Wbar
Vref <= R
pD <= PDbar
Wbar <= 6*R
2*PDbar + 67*R <= 2*rho
-----------------------------------
pD + pB(reference) <= rho
```

The concrete `9/10`, `3/20`, `67/2` matrix certificates should be a separate exact-rational sidecar so that coefficient/source semantics can be swapped without changing the abstract theorem.

---

## 8. Still open

This result remains `pending` because the following are not proved here:

- which exact coefficient semantics is the actual canonical `referenceKey`;
- equality of deployed Float64/Julia parse/assembly/solve with any exact-real matrix packet;
- actual general-time `w^2<=Wbar` and `pD<=PDbar` on one common path/tube;
- nominal/reference and actual context identity used by the centered anchor;
- derivative/FD/reference halos, graph lift, P8 flowpipe/continuation;
- Lean/kernel receipt, independent 封不觉 validation, comparator/admission/registry.

No authoritative P5/P8/registry status is changed by this review.
