---
kind: companion_log
task_id: T-P7-002
source_agent: 红莲魔尊
agent: 红莲魔尊
created_at: 2026-09-07T08:54:00-06:00
inspected_commit: 2ecc106e5aa0208cd7a00021064cee2d6df8468e
continuation_of: companion-T-P7-002-honglianmozun-20260907T0455.md
claim_status: continued_existing_owner_assignment
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_normalization_safe_schur_transport_then_source_bind_the_normalization_map
---

# T-P7-002 continuation — normalization-safe Schur transport

## Result

The previous continuation showed that the intrinsic Schur energy charge for the **physical, unnormalized** cross covector `u` is

```text
Q_A(u) = u^T A^{-1} u,
```

and therefore the historical scalar `rho` can disappear from the energy ledger if the frozen P7 coefficient box already bounds that physical `u`.

The remaining mathematical interface question is what happens when a checker bounds a normalized coordinate `uhat` rather than `u` itself.  This note gives an exact transport theorem for that case.  It isolates the normalization as a typed linear map and proves that its cost enters quadratically.  It also proves a small impossibility result: an `eta < tau` certificate alone cannot produce any uniform rho-free physical energy charge if the normalization scale is left unbounded.

No deployed-source identification, hash/provenance claim, seven-term polynomial admission, P8 coverage, M4 closure, or registry promotion is made.

## 1. Diagonal coercivity version of Schur completion

Let the actual positive block be diagonal,

```text
A = diag(a,d),
```

and suppose only the lower coercivity data are exposed to the consumer:

```text
0 < a0 <= a,
0 < d0 <= d.
```

For any real `x1,x2,u1,u2,s`, weighted completion gives

```text
-2 s u1 x1 <= a0 x1^2 + (u1^2/a0) s^2,
-2 s u2 x2 <= d0 x2^2 + (u2^2/d0) s^2.
```

A square-root-free proof of the first line is obtained by multiplying the desired inequality by `a0>0`:

```text
a0 * (a0*x1^2 + (u1^2/a0)*s^2 + 2*s*u1*x1)
  = (a0*x1 + s*u1)^2 >= 0.
```

The second line is identical.  Since `a0*x1^2 <= a*x1^2` and `d0*x2^2 <= d*x2^2`, summing gives

```text
-2 s (u1*x1 + u2*x2)
 <= a*x1^2 + d*x2^2
    + s^2 * (u1^2/a0 + u2^2/d0).                 (1)
```

Thus a source interface does not need to expose the inverse of the actual block.  Positive lower diagonal bounds are enough.

## 2. Exact transport through a typed normalization map

Suppose the checker does not bound the physical covector directly.  Instead it exposes

```text
uhat = (h1,h2),
|h1| <= H1,
|h2| <= H2,
H1,H2 >= 0,
```

and a **typed normalization map**

```text
u = N uhat,
N = [[n11,n12],
     [n21,n22]].
```

Therefore

```text
u1 = n11*h1 + n12*h2,
u2 = n21*h1 + n22*h2.
```

Put

```text
D = diag(a0,d0),
R = N^T D^{-1} N.
```

Writing

```text
r11 = n11^2/a0 + n21^2/d0,
r12 = n11*n12/a0 + n21*n22/d0,
r22 = n12^2/a0 + n22^2/d0,
```

we have the exact identity

```text
u1^2/a0 + u2^2/d0
 = r11*h1^2 + 2*r12*h1*h2 + r22*h2^2.             (2)
```

Because `R=N^T D^{-1}N` is positive semidefinite, `r11,r22>=0`.  On the independent box for `uhat`, (2) gives

```text
u1^2/a0 + u2^2/d0
 <= r11*H1^2 + 2*|r12|*H1*H2 + r22*H2^2
 =: C_N(H1,H2).                                     (3)
```

Combining (1) and (3):

```text
-2 s u^T x
 <= x^T A x + C_N(H1,H2) * s^2.                    (4)
```

This is the normalization-safe Schur consumer.  The consumer sees only:

```text
(a0,d0), N, (H1,H2), s.
```

There is no hidden scalar normalization.

## 3. `C_N` is the exact box cost for a fixed normalization map

The upper bound in (3) is attained at a box vertex.  If `r12>=0`, choose

```text
h1 = H1,
h2 = H2.
```

If `r12<0`, choose

```text
h1 = H1,
h2 = -H2.
```

Then the mixed term equals `2|r12|H1H2`, while the diagonal terms attain `r11 H1^2` and `r22 H2^2`.  Hence

```text
max_{|h1|<=H1, |h2|<=H2} h^T R h
 = r11*H1^2 + 2*|r12|*H1*H2 + r22*H2^2.           (5)
```

So for fixed `(a0,d0,N,H1,H2)`, (3) is not merely a convenient sufficient estimate; it is the exact worst-case quadratic charge over the rectangular checker box.

As in the previous continuation, this is information-set sharpness.  It does not claim a deployed trajectory attains all extremal values simultaneously.

## 4. Scalar normalization is exactly quadratic

A common special case is

```text
N = alpha * I,
u = alpha * uhat.
```

Then `r12=0` and (5) reduces to

```text
C_{alpha I}(H1,H2)
 = alpha^2 * (H1^2/a0 + H2^2/d0).                  (6)
```

Therefore any hidden normalization factor enters the Schur energy charge as its **square**.

If the historical notation is

```text
u = sqrt(rho) * uhat
```

(or, without introducing a square root, simply `alpha^2=rho`), then

```text
Q_D(u) = rho * Q_D(uhat).                           (7)
```

This explains precisely when the previous rho-free simplification is valid:

- if the frozen `U1,U2` are already bounds on physical `u`, the interface is `N=I` and no `rho` appears;
- if they are bounds on normalized `uhat`, the normalization map must be transported, and scalar normalization contributes `rho` through (7);
- if the normalization is a non-scalar matrix, the exact cost is the full `N^T D^{-1}N` box expression (5), not a guessed scalar multiplier.

## 5. A clean impossibility theorem for an untyped normalized certificate

The historical normalized route can be written abstractly as

```text
eta = Q_A(u)/rho,
eta < tau,
rho > 0.
```

If no upper bound on `rho` and no typed map from the reported normalized coefficients to physical `u` is supplied, then `eta<tau` alone implies **no finite uniform upper bound** on the physical charge `Q_A(u)`.

Indeed, let `tau>0` and let `B>0` be any proposed finite physical-cost cap.  Choose

```text
eta = tau/2,
rho = 2*(B+1)/tau.
```

Then

```text
0 < eta < tau,
Q := rho*eta = B+1 > B.                              (8)
```

Since `B` was arbitrary, no theorem of the form

```text
eta < tau  ==>  Q_A(u) <= B(tau)
```

can hold without another premise controlling the normalization scale.  This is a mathematical obstruction, not a provenance or implementation issue.

Consequently the direct P7 seam may delete the historical `rho_bar<=16` gate only after one of the following typed contracts is established:

```text
(A) U1,U2 bound physical unnormalized u directly;
```

or

```text
(B) checker bounds uhat and supplies a bounded normalization map N,
    so C_N(H1,H2) can be charged explicitly.
```

A bare normalized `eta` certificate is insufficient.

## 6. Optional interval-normalization fallback

If source binding cannot expose an exact matrix `N` but can bound its entries, one can retain a safe componentwise theorem.  If

```text
|n11|<=N11, |n12|<=N12,
|n21|<=N21, |n22|<=N22,
```

then

```text
|u1| <= N11*H1 + N12*H2,
|u2| <= N21*H1 + N22*H2,
```

and (1) gives the safe charge

```text
C_interval
 = (N11*H1+N12*H2)^2/a0
   + (N21*H1+N22*H2)^2/d0.                         (9)
```

This is generally weaker than (5), because it forgets correlation between the two rows of `N`, but it is still normalization-safe and source-independent.

## 7. Lean-friendly theorem decomposition

The cleanest formal package is four small algebraic lemmas.

### `schur_cost_from_physical_box`

```lean
theorem schur_cost_from_physical_box
    (a d a0 d0 x1 x2 u1 u2 U1 U2 s : ℝ)
    (ha0 : 0 < a0) (hd0 : 0 < d0)
    (ha : a0 <= a) (hd : d0 <= d)
    (hU1 : 0 <= U1) (hU2 : 0 <= U2)
    (hu1 : |u1| <= U1) (hu2 : |u2| <= U2) :
    -2*s*(u1*x1+u2*x2)
      <= a*x1^2+d*x2^2+(U1^2/a0+U2^2/d0)*s^2
```

This is the physical-box theorem already implicit in the previous continuation, but stated with only diagonal coercivity premises.

### `transported_box_quadratic_cost`

For the definitions of `u1,u2,r11,r12,r22` above, prove

```text
u1^2/a0 + u2^2/d0
 <= r11*H1^2 + 2*|r12|*H1*H2 + r22*H2^2.
```

A separate equality-at-vertex theorem can record exactness if useful.

### `scalar_normalization_cost`

```text
u1=alpha*h1, u2=alpha*h2
```

implies the exact scale identity

```text
u1^2/a0 + u2^2/d0
 = alpha^2 * (h1^2/a0 + h2^2/d0).
```

This is the formal guard against silently dropping `rho=alpha^2`.

### `normalized_certificate_no_uniform_cost`

For `tau>0` and any proposed cap `B`, explicitly construct positive `eta,rho` with

```text
eta < tau
rho*eta > B.
```

A convenient witness is the one in (8).  This theorem makes the failure boundary executable rather than leaving it as prose.

All four statements are source-independent.  They should be amenable to `ring_nf`, positivity, `abs` case splits, and `nlinarith`; no matrix inverse, eigenvalue, square root, ODE, or integration API is required.

## 8. Recommended typed source interface

The mathematical consumer should accept one of two explicit tags/contracts:

```text
physical_covector:
  |u1|<=U1, |u2|<=U2
```

or

```text
normalized_covector:
  u=N*uhat,
  |h1|<=H1, |h2|<=H2,
  normalization_map=N.
```

The energy ledger then charges either

```text
U1^2/a0 + U2^2/d0
```

or the exact transported box cost `C_N` in (5).  A checker output that is merely labelled `normalized` but does not define `N` is mathematically insufficient for the direct-cost seam.

This is an interface theorem, not interface documentation: the substantive content is (2)--(8), which prove how normalization changes the energy charge and why an untyped normalized certificate cannot support rho elimination.

## Remaining blockers

1. Determine whether the frozen P7 `U1,U2` constants bound the physical unnormalized cross covector or a normalized representation.
2. If normalized, source-bind the actual map `N` (or interval bounds sufficient for (9)) on the same domain.
3. Retain the previous exact-real diagonal lower bounds and P8 ramp binding on that same domain.
4. Keep seven-term factorization/no-double-counting, Float64/source semantics, P8 coverage, and M4 base-residual premises separate.
5. Have the formalization lane implement the source-independent transport lemmas; then have `封不觉` independently verify them before any coordinator integration.

This continuation remains `pending`.  It strengthens the mathematical seam and gives a precise failure theorem, but does not close P7, P8, M4, or the registry.
