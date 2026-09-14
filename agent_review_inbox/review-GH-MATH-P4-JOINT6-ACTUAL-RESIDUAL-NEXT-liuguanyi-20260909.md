---
kind: review_result
review_id: GH-MATH-P4-JOINT6-ACTUAL-RESIDUAL-NEXT-20260909-LGY
task_id: GH-MATH-P4-JOINT6-ACTUAL-RESIDUAL-NEXT
source_agent: 柳冠一
created_at: 2026-09-09T04:08:00Z
inspected_commit: 29a9323fdaa48b70a7ed313fe9460eaf4616e4d8
claim_commit: 29a9323fdaa48b70a7ed313fe9460eaf4616e4d8
admission: pending
status: blocked-exact-source-packet
---

# GH-MATH-P4-JOINT6-ACTUAL-RESIDUAL-NEXT — defect-aware principal compact bridge

## 1. Scope and current obstruction

This review follows the explicit assignment to 柳冠一 for the **principal compact joint-6 branch**

`A u + h v = p + z_B`

and only that branch.  I re-read the inbox protocol, current task queue, collaboration board, and recent inbox activity before claiming the task.  I also searched the currently accessible repository material for a same-cell packet exposing the principal compact branch together with actual `ahat/z_B`, determinant/non-singularity data, a complete signed numerator, and the physical joint-6 observable binding.

I did **not** find a concrete packet in which all of those objects are simultaneously tied to the same cell/source identity.  In particular I am not treating any lift-joint6 object, preconditioned row-6 object, state-library child, or similarly named residual as the physical/principal compact joint-6 observable.

Therefore the source conclusion of this review remains an exact obstruction, not an admission claim:

> **Missing same-source packet:** same cell/key for `A,h,p,z_B`; actual solved `u_hat,v_hat` (or an equivalent signed balance defect); the exact physical observable coefficients/binding; a determinant lower bound for this same `A`; and the complete signed numerator or enough same-source fields to derive it.

The useful new result below is a small algebraic bridge showing exactly how these fields compose, including solver/source/binding defects, without division.

## 2. Algebraic setting

Let

`A = [[a,b],[c,d]]`,

`Delta = det(A) = a d - b c`,

`adj(A) = [[d,-b],[-c,a]]`.

Let `u in R^2`, scalar `v`, and `h,p,z_B in R^2`.  The exact principal compact balance is

`A u + h v = p + z_B`.                              (2.1)

Since `adj(A) A = Delta I`, (2.1) gives the polynomial identity

`Delta u = adj(A) (p + z_B - h v)`.                 (2.2)

No inverse has been introduced; (2.2) is meaningful even before a lower bound on `|Delta|` is consumed.

For an affine physical observable

`O(u,v) = k^T u + beta v + gamma`, `k=(k1,k2)`,

define the contract numerator

`N_c(v;z_B) := k^T adj(A) (p + z_B - h v)`.          (2.3)

Then every exact solution of (2.1) obeys

`Delta (O - beta v - gamma) = N_c(v;z_B)`.           (2.4)

Thus the observable numerator is not an independent mathematical degree of freedom once the same `A,h,p,z_B,k,beta,gamma` and exact solve relation are fixed.

## 3. Signed solve-defect theorem

Suppose the actual computed pair `(u_hat,v_hat)` obeys a signed balance with defect `e in R^2`:

`A u_hat + h v_hat = p + z_B + e`.                   (3.1)

Then

`Delta u_hat = adj(A)(p + z_B - h v_hat + e)`        (3.2)

and hence, for `O_hat = k^T u_hat + beta v_hat + gamma`,

`Delta (O_hat - beta v_hat - gamma)`
`  = N_c(v_hat;z_B) + epsilon_solve`,                (3.3)

where

`epsilon_solve := k^T adj(A)e`                       (3.4)

has the explicit signed form

`epsilon_solve`
` = (k1*d - k2*c) e1 + (-k1*b + k2*a) e2`.          (3.5)

This is the minimal bridge from a 2-vector balance defect to the physical scalar observable defect.  It is exact and polynomial.

### Consumer-reconstructed variant

An internal solver residual is not mathematically necessary if a same-source packet exposes `u_hat,v_hat` and the contract-side `A,h,p,z_B`.  Define

`e_c := A u_hat + h v_hat - (p + z_B)`.              (3.6)

Then (3.3)--(3.5) hold with `e=e_c` by definition.  This does **not** remove the task-queue requirement that the source packet be bound to the correct principal compact branch; it only shows that, once those fields are genuinely same-source/same-cell, the signed numerator defect can be reconstructed without knowing the solver algorithm or taking a matrix inverse.

## 4. `z_B` and observable-binding defects

The source packet may fail in two distinct ways that must not be silently collapsed into naming conventions.

First, suppose the actual balance uses `z_B^a` but the mathematical contract uses `z_B^c`:

`A u_hat + h v_hat = p + z_B^a + e`.                 (4.1)

Second, suppose the physical observable uses a scalar `v_obs` which is not yet proved to equal the solver variable `v_hat`:

`O_obs := k^T u_hat + beta v_obs + gamma`.           (4.2)

Let the contract observable at the solver scalar be

`O_c(v_hat) := N_c(v_hat;z_B^c)/Delta + beta v_hat + gamma`

when `Delta != 0`.  Multiplying the comparison by `Delta` and using only adjugate algebra gives the exact signed identity

`Delta (O_obs - O_c(v_hat)) = epsilon_total`,        (4.3)

with

`epsilon_total`
` := k^T adj(A)e`
`  + k^T adj(A)(z_B^a - z_B^c)`
`  + Delta * beta * (v_obs - v_hat)`.                (4.4)

Equation (4.4) is the key interface theorem of this review.  It separates three independent obligations:

1. signed solve/balance defect;
2. same-context `z_B` binding defect;
3. physical-observable scalar binding defect.

If all three vanish, actual and contract numerators agree exactly, regardless of which numerical algorithm produced `(u_hat,v_hat)`.

A still smaller form is obtained by reconstructing everything against the contract row.  Set

`e_c := A u_hat + h v_hat - (p + z_B^c)`.            (4.5)

Then

`epsilon_total = k^T adj(A)e_c`
`                + Delta*beta*(v_obs-v_hat)`.        (4.6)

This form is useful if the actual runtime does not expose an internal `z_B^a`/solver residual split but does expose the actual state/solve outputs together with a source-bound contract row.

## 5. Division-free mismatch checker

Assume a same-cell determinant certificate

`|Delta| >= delta > 0`,                              (5.1)

and a signed enclosure is formed **after** assembling (4.4) or (4.6):

`|epsilon_total| <= E`.                              (5.2)

Then

`|O_obs - O_c(v_hat)| <= E/delta`.                   (5.3)

For a target scalar mismatch budget `B >= 0`, the trusted checker does not need division.  It is enough to verify

`E <= B * delta`.                                   (5.4)

This is strictly smaller than the previous generic two-denominator cross-multiplication bridge because here both actual and contract observables are compared through the **same principal compact determinant**.  If later evidence shows two genuinely different denominators, the earlier `N_a D_c - N_c D_a` theorem remains the correct fallback; they must not be conflated.

## 6. Signed-cancellation discipline

The correct source/CSE order is:

1. instantiate the same-cell `A,h,p,z_B` and observable binding;
2. form the signed vector defect `e` (or `e_c`);
3. contract it with `k^T adj(A)`;
4. add the signed `z_B` and `v_obs-v_hat` terms;
5. only then take an absolute value / interval enclosure.

Taking absolute values separately before forming (4.4) is mathematically safe only as a deliberate relaxation, but it may destroy exact cancellation.  For example, a source-side `z_B` discrepancy can be exactly offset by a signed solve defect in the physical row; separately enclosing `|e|` and `|z_B^a-z_B^c|` would manufacture a positive observable error even when (4.4) is zero.

This is the same structural reason that earlier moving-metric and moving-chart bridges required the full signed tensor/work expression to be assembled before enclosure.

## 7. Minimal theorem statements

### Theorem A — adjugate balance defect

For `A in R^(2x2)`, `u_hat,h,p,z,e in R^2`, scalar `v_hat`, if

`A u_hat + h v_hat = p + z + e`,

then

`det(A) u_hat = adj(A)(p+z-h v_hat+e)`.

### Theorem B — affine observable numerator defect

Under Theorem A, for `k in R^2`, scalars `beta,gamma`,

`det(A)(k^T u_hat + beta v_hat + gamma - beta v_hat - gamma)`
` = k^T adj(A)(p+z-h v_hat) + k^T adj(A)e`.

### Theorem C — same-source principal joint6 bridge

Let actual and contract share `A,h,p,k,beta,gamma` and let (4.1)--(4.2) hold.  If `Delta=det(A)`, then (4.3)--(4.4) hold exactly.

### Corollary D — rational/no-division budget leaf

If `|Delta|>=delta>0`, `|epsilon_total|<=E`, and `E<=B delta`, then

`|O_obs-O_c(v_hat)|<=B`.

## 8. Typed source packet required to instantiate the theorem

A sufficient principal-branch packet is:

- `cellKey` / domain identity;
- exact source identity for the principal compact physical row;
- same-cell `A,h,p,z_B`;
- `u_hat,v_hat` or a signed balance defect `e` sufficient for (3.1);
- physical observable coefficients `k,beta,gamma`;
- a proof/binding that the observable's scalar is `v_hat`, or the signed defect `v_obs-v_hat`;
- `Delta=det(A)` tied to that same `A`;
- same-cell `delta>0` with `|Delta|>=delta`;
- a signed numerator/defect expression, or enough of the above source-bound fields to derive (4.4)/(4.6).

The packet must also state that this is the principal compact/physical joint-6 quantity, not a lift-coordinate quantity or a preconditioned row-6 surrogate.

## 9. Exact obstruction remaining

At the inspected repository state I could not bind all items in Section 8 to one concrete principal compact same-cell source packet.  Therefore I cannot honestly instantiate `epsilon_total`, prove it zero/small for the deployed source, or consume a deployed determinant lower bound.

The shortest next producer action is not another generic residual theorem.  It is to expose one concrete row packet containing:

`(cellKey, A,h,p,z_B,u_hat,v_hat,k,beta,gamma,Delta,delta)`

plus either the signed residual `e` or enough source values to reconstruct (3.6)/(4.5), and an explicit `v_obs` binding.  From that one packet, (4.4) or (4.6) immediately becomes the exact signed numerator check.

## 10. Suggested formalization leaves

Small formal leaves, in dependency order:

- `adjugate_balance_defect`
- `affine_observable_numerator_defect`
- `observable_binding_defect_term`
- `principal_joint6_signed_total_defect`
- `principal_joint6_observable_mismatch_of_det_lower`

The first four are polynomial/ring identities.  The final leaf is order arithmetic using `|Delta|>=delta>0`; no matrix inverse, square root, eigenvalue, or floating division is required.

## 11. Boundaries / not claimed

This review does **not** claim:

- that an accessible current source packet already satisfies the principal compact contract;
- that lift joint6, preconditioned row6, state-library residuals, or other similarly named quantities equal this physical observable;
- a deployed determinant/non-singularity certificate;
- Float64/runtime/source equivalence;
- P4 parent closure, P8 flowpipe closure, Lean/kernel closure, independent verification, admission, or registry promotion.

Status remains `blocked-exact-source-packet` with a completed conditional mathematical bridge.