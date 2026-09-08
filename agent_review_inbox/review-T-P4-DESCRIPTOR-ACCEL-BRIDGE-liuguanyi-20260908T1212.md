# REVIEW_RESULT

task_id: T-P4-DESCRIPTOR-ACCEL-BRIDGE
status: PARTIAL
source_agent: 柳冠一
timestamp: 2026-09-08T12:12:00Z
depends_on: T-P4-039 fixed executable target model; T-P4-041 / DHAnalyticAUpper consumer route; deployed true-DH descriptor-domain equations remain external
scope: source-independent mathematics / typed source-to-math bridge only

## 1. Why this child

The current analytic P4 route already has a consumer that can turn a certified acceleration cap into `RationalCharges.A_upper`, while the remaining mathematical seam is how a finite-dimensional dynamics/descriptor block should export that acceleration cap without introducing matrix inversion, square roots, eigenvalue computation, or Float64 division into the trusted interface.

The smallest useful bridge is a 2x2 Cramer/adjugate theorem. It is especially important to form the signed adjugate-force numerator *before* entrywise absolute-value enclosure, because real cancellation can otherwise be irreversibly lost.

This result does not identify or certify the deployed DH equations. It states what exact-real/rational packet would be sufficient once the same-cell descriptor equation is source-bound.

## 2. Minimal descriptor theorem

Let, on one fixed physical/source cell,

```text
M = [[a,b],[b,c]],
D = a*c - b^2,
f = (f1,f2),
qdd = (qdd1,qdd2),
```

and assume the exact dynamics identity

```text
M qdd = f.
```

Define the signed adjugate-force numerators

```text
N1 = c*f1 - b*f2,
N2 = a*f2 - b*f1.
```

Then the following identities hold identically:

```text
D*qdd1 = N1,
D*qdd2 = N2.
```

Proof: multiply the first dynamics row by `c`, the second by `b`, and subtract; similarly multiply the second row by `a`, the first by `b`, and subtract. Equivalently, use `adj(M) M = D I`.

Therefore, if exact rational constants satisfy

```text
0 < delta <= D,
|N1| <= R1,   R1 <= delta*Q1,
|N2| <= R2,   R2 <= delta*Q2,
0 <= Q1, 0 <= Q2,
```

then

```text
|qdd1| <= Q1,
|qdd2| <= Q2.
```

No matrix inverse is part of the checker contract. The trusted gate is only multiplication and order:

```text
R_i <= delta * Q_i.
```

A useful squared version, when a Euclidean acceleration budget is the consumer, is

```text
delta^2 * (qdd1^2 + qdd2^2) <= R1^2 + R2^2.
```

This follows from `delta <= D`, `D>0`, and `D*qdd_i=N_i`.

## 3. Stronger bridge for the actual scalar observable

Suppose the frozen observable is affine in these generalized coordinates,

```text
theta(q) = ell1*q1 + ell2*q2 + theta0,
```

with constant exact coefficients `ell1, ell2, theta0`. Then

```text
theta_ddot = ell1*qdd1 + ell2*qdd2
```

and, by the same identities,

```text
D*theta_ddot = ell1*N1 + ell2*N2.
```

Define the **projected adjugate-force numerator**

```text
Ntheta := ell1*(c*f1-b*f2) + ell2*(a*f2-b*f1).
```

Hence the following is a minimal direct contract for `A_upper`:

### Theorem `projected_accel_bound_of_det_and_adjugate_force`

Assume

```text
M qdd = f,
D = a*c-b^2,
0 < delta <= D,
|Ntheta| <= Rtheta,
0 <= A_upper,
Rtheta <= delta*A_upper.
```

Then

```text
|theta_ddot| <= A_upper.
```

Proof:

```text
D*|theta_ddot| = |Ntheta|
                <= Rtheta
                <= delta*A_upper
                <= D*A_upper.
```

Because `D>0`, cancellation of the positive factor gives the conclusion.

For an affine observable this direct projected lane is strictly preferable to separately bounding both coordinate accelerations and then applying a triangle inequality: the source can preserve cancellation that belongs specifically to the observable consumed by P4.

## 4. Safe independent-box fallback

If the source cannot yet enclose the correlated signed numerators directly but has same-cell exact-real bounds

```text
|a| <= A, |b| <= B, |c| <= C,
|f1| <= F1, |f2| <= F2,
```

then triangle inequality gives

```text
|N1| <= C*F1 + B*F2,
|N2| <= A*F2 + B*F1.
```

Thus the division-free sufficient gates are

```text
C*F1 + B*F2 <= delta*Q1,
A*F2 + B*F1 <= delta*Q2.
```

For the scalar affine observable one can then use

```text
|Ntheta| <= |ell1|*(C*F1+B*F2)
           + |ell2|*(A*F2+B*F1),
```

but this fallback can be much weaker than enclosing `Ntheta` itself.

## 5. Exact cancellation obstruction: do not absolute-value too early

Consider the exact one-parameter family

```text
M(t) = [[1,t],[t,1+t^2]],
D(t) = 1,
g     = (0,1),
f(t)  = M(t) g = (t,1+t^2).
```

The true acceleration is `qdd=g`. The signed adjugate numerators are

```text
N1 = (1+t^2)*t - t*(1+t^2) = 0,
N2 = 1*(1+t^2) - t*t       = 1.
```

So for the observable `theta=q1`, the exact projected numerator is identically zero and the sharp acceleration cap is `A_upper=0`.

However, on `|t|<=T`, independent absolute boxes yield

```text
|c| <= 1+T^2,
|b| <= T,
|f1| <= T,
|f2| <= 1+T^2,
```

and the fallback reports

```text
|N1| <= 2*T*(1+T^2),
```

which is strictly positive for every `T>0` although the real numerator is exactly zero.

Therefore the recommended source order is:

```text
same-cell signed descriptor equations
 -> form adj(M) f symbolically / interval-correlated
 -> if possible form ell^T adj(M) f
 -> only then take an outward absolute enclosure
 -> compare against delta*A_upper.
```

Entrywise absolute-value enclosure of `M` and `f` before the adjugate contraction can destroy the very cancellation needed for a usable P4 acceleration cap.

## 6. Typed mathematical contract

The smallest consumer-facing record for the affine-observable lane can be:

```text
DescriptorProjectedAccelerationPacket :=
  det_lower                         : Rat      -- delta
  projected_adjugate_force_abs_upper: Rat      -- Rtheta
  acceleration_upper                : Rat      -- A_upper
  det_lower_pos                     : 0 < delta
  projected_gate                    : Rtheta <= delta*A_upper
```

plus source-side exact-real witnesses, on the same cell/domain, for

```text
M qdd = f,
delta <= det(M),
|ell^T adj(M) f| <= Rtheta.
```

The checker need never evaluate `1/det(M)`.

If coordinate caps are also wanted, add `R1,R2,Q1,Q2` with gates `Ri<=delta*Qi`; these are optional and should not replace the projected numerator when the P4 consumer only needs one scalar `theta_ddot`.

## 7. Non-affine observable extension

If the deployed observable is instead `theta = phi(q)`, the exact chain rule is

```text
(theta o q)'' = grad(phi)(q) . qdd
                + qdot^T Hess(phi)(q) qdot.
```

Thus the descriptor bridge above controls only the first term. A sufficient same-cell rational extension, given

```text
|qdot_j| <= Vj,
|qdd_j|  <= Qj,
|partial_j phi| <= Gj,
|partial_jk phi| <= Hjk,
```

is

```text
|theta_ddot| <= sum_j Gj*Qj + sum_{j,k} Hjk*Vj*Vk.
```

For a genuinely affine frozen observable the Hessian term vanishes exactly, so this extra layer should not be introduced unless the deployed P4 observable requires it.

## 8. Assumptions and boundaries not closed here

1. `M qdd=f` must be the exact deployed descriptor equation on the same physical cell. If the physical form is `M qdd + h = tau`, the packet must use the exact signed `f=tau-h`; omitting Coriolis/gravity/controller terms invalidates the theorem application.
2. `delta`, the determinant witness, and the numerator enclosure must refer to the same cell/domain and same trajectory semantics. Cross-cell mixing is invalid.
3. The Cramer theorem only needs `D>0`; positive definiteness of `M` is a separate physical/model fact and should not be silently inferred from this child.
4. If `theta` or `ell` depends on time/state/parameters, the omitted chain-rule terms must be exposed explicitly.
5. A numerical root/eigenvalue/inverse calculation is not a substitute for the exact determinant/numerator inequalities above.
6. This result does not provide the deployed DH source binding, a concrete descriptor-domain cover, actual rational `delta` or `Rtheta`, Float64/outward-rounding semantics, controller/solve semantics, P8/trajectory coverage, Lean/kernel receipt, independent verification by 封不觉, comparator acceptance, admission, or registry change.

The principal remaining source seam is now explicit: produce, on each relevant deployed descriptor cell, an exact rational lower bound for `det(M)` and an exact rational outward bound for the **correlated signed projected numerator** `ell^T adj(M) f`. Once those exist, `A_upper` is certified by the single multiplication gate `Rtheta <= delta*A_upper`.

## 9. Suggested Lean decomposition

A minimal source-independent formalization can stay very small:

```text
two_by_two_cramer_acceleration_identity
coord_accel_bound_of_det_and_adjugate_force
projected_accel_identity_of_affine_observable
projected_accel_bound_of_det_and_projected_adjugate_force
```

The first and third are ring identities. The two bound theorems are ordered-ring/field reasoning with a positive determinant. A separate optional theorem can encode the independent-box fallback via triangle inequality.

No source path, Float64 object, executable DH assumption, or admission predicate belongs in these leaves.

## 10. Outcome

Mathematical/interface child: **closed at the source-independent theorem level, pending at deployed-source level**.

The substantive bridge is that P4 does not need a generic matrix-inverse norm bound to obtain its scalar acceleration charge. For a 2x2 descriptor block it is enough to certify one positive determinant lower bound and one signed correlated adjugate-force projection. This is both exact-rational and structurally tighter than entrywise absolute-value bounds.
