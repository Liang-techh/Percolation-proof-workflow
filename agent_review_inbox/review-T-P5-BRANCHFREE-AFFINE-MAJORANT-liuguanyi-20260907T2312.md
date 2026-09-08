---
kind: review_result
review_id: review-T-P5-BRANCHFREE-AFFINE-MAJORANT-liuguanyi-20260907T2312
task_id: T-P5-BRANCHFREE-AFFINE-MAJORANT
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-07T23:03:00-06:00
created_at: 2026-09-07T23:12:00-06:00
claim_commit: 86c5b3ba4ad32eb779db43c6042f83f80ff913e6
inspected_commit: 589ab0c4211cc94d2c4164eda7f2c30b4690955e
inspected_paths:
  - agent_review_inbox/review-T-P5-051-honglianmozun-20260907T2250.md
  - agent_review_inbox/review-T-P5-050-kuangmanmozun-20260907T2238.md
  - agent_review_inbox/review-T-P5-045-liuguanyi-20260907T2108.md
continuation_of:
  - T-P5-045
  - T-P5-051
related_tasks:
  - T-P5-044
  - T-P5-048
  - T-P5-050
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add a branch-free fixed-budget source-to-energy adapter above the PD/singular dispatcher; expose the two correlated polynomial remainders directly to interval/source checkers; keep T-P5-051 for sharp branch classification and obstruction rays
---

# T-P5-BRANCHFREE-AFFINE-MAJORANT — branch-free affine-energy cost bridge

## 0. Question

T-P5-051 gives a complete pointwise branch classifier for the two-channel affine energy term

```text
J(x,y) = -Q(x,y) - b4*x - b5*y,
```

with separate positive-definite, nonzero singular-PSD, zero-matrix, and unbounded branches. That classification is mathematically complete, but a source/interval cell that approaches the positive-definite / singular boundary should not be forced to divide by `Delta` or switch proof APIs when `Delta=0`.

This review derives a single fixed-budget certificate that is exact across all of those branches.

The result is especially compatible with T-P5-045's scaled signed cross coordinate

```text
sigma = k45+k54 = 2*q.
```

No square root, inverse, eigenvalue, pseudoinverse, or branch test is needed in the trusted source-facing gate.

---

## 1. Scaled coordinates

Write

```text
Q(x,y) = p*x^2 + sigma*x*y + s*y^2,
d(x,y) = b4*x + b5*y.
```

Thus the symmetric effective dissipation matrix is

```text
H = [[p, sigma/2],
     [sigma/2, s]].
```

Use the exact polynomial invariants

```text
tau  := p+s,
D4   := 4*p*s - sigma^2,
B2   := b4^2+b5^2,
Nsig := s*b4^2 - sigma*b4*b5 + p*b5^2.
```

Relative to the `q` notation of T-P5-051,

```text
D4 = 4*(p*s-q^2) = 4*Delta,
Nsig = s*b4^2 - 2*q*b4*b5 + p*b5^2 = N.
```

So this is not a new physical convention; it is the division-free form already natural for T-P5-045.

---

## 2. The branch-free majorant matrix

Fix one energy charge `kappa > 0` and define

```text
G_kappa := 4*kappa*H - b*b^T.
```

In scaled scalar coordinates,

```text
G11 = 4*kappa*p - b4^2,
G22 = 4*kappa*s - b5^2,
G12 = 2*kappa*sigma - b4*b5.
```

The two invariants of this symmetric `2x2` matrix are exactly

```text
trace(G_kappa)
  = 4*kappa*tau - B2,                                    (2.1)

det(G_kappa)
  = 4*kappa*(kappa*D4 - Nsig).                           (2.2)
```

Equivalently, if one stays entirely with scaled quadratic-form coefficients,

```text
4*G11*G22 - (4*kappa*sigma-2*b4*b5)^2
  = 16*kappa*(kappa*D4-Nsig).                            (2.3)
```

All expressions are polynomial and exact-rational when the inputs are exact-rational.

---

## 3. Exact completion identity

For every `x,y`, let `d=b4*x+b5*y`. Then

```text
4*kappa * (Q(x,y) + d + kappa)
 = [x,y] * G_kappa * [x,y]^T
   + (d + 2*kappa)^2.                                    (3.1)
```

This is a ring identity. Expanding the first term gives

```text
(4*kappa*p-b4^2)*x^2
+ (4*kappa*sigma-2*b4*b5)*x*y
+ (4*kappa*s-b5^2)*y^2.
```

Hence, if `G_kappa` is PSD and `kappa>0`, the right-hand side of (3.1) is nonnegative and

```text
-Q(x,y)-d <= kappa                                       (3.2)
```

for all real `x,y`.

The important point is that the completion is valid without choosing the PD or singular branch.

---

## 4. A matrix-free 2x2 lemma

The required PSD check itself can be kept outside a matrix API.

For

```text
R(x,y)=a*x^2 + m*x*y + c*y^2,
```

a sufficient and, over the reals, necessary condition for `R>=0` for all `x,y` is

```text
a+c >= 0,
4*a*c-m^2 >= 0.                                         (4.1)
```

A division-free proof of sufficiency uses

```text
4*a*R = (2*a*x+m*y)^2 + (4*a*c-m^2)*y^2                (4.2)
```

when `a>0`. If `a=0`, (4.1) forces `m=0` and `c>=0`. If `a<0`, then `a*c>=m^2/4>=0` forces `c<=0`, contradicting `a+c>=0`. Thus no spectral/eigenvalue theorem is needed.

Apply this to the quadratic form of `G_kappa`. By (2.1)–(2.3), it is PSD exactly when

```text
B2   <= 4*kappa*tau,                                    (G1)
Nsig <= kappa*D4.                                       (G2)
```

because `kappa>0`.

---

## 5. Main theorem: only two scalar gates

### Theorem — branch-free affine-energy budget

Let `kappa>0`. For real `p,s,sigma,b4,b5`, the following are equivalent:

```text
(A) for every real x,y,

    -(p*x^2 + sigma*x*y + s*y^2)
    -(b4*x+b5*y)
    <= kappa;
```

and

```text
(B1) b4^2+b5^2
     <= 4*kappa*(p+s),

(B2) s*b4^2 - sigma*b4*b5 + p*b5^2
     <= kappa*(4*p*s-sigma^2).
```

So a positive fixed energy charge needs only **two correlated polynomial inequalities**.

No separate hypotheses `p>=0`, `s>=0`, `D4>=0`, or `H PSD` are necessary in this fixed-positive-budget theorem: (B1)–(B2) say exactly that `G_kappa` is PSD, and then

```text
H = (G_kappa + b*b^T)/(4*kappa)
```

is automatically PSD.

### Proof of `(B) => (A)`

(B1) is `trace(G_kappa)>=0`. By (2.2), (B2) and `kappa>0` give `det(G_kappa)>=0`. Section 4 therefore gives `G_kappa PSD`; identity (3.1) gives (A).

### Proof idea of `(A) => (B)`

Fix a vector `u=(x,y)` and write

```text
a = u^T H u,
d = b^T u.
```

Applying (A) to every scalar multiple `t*u` gives

```text
a*t^2 + d*t + kappa >= 0    for every real t.           (5.1)
```

First, `a<0` is impossible by `|t| -> infinity`. If `a=0`, (5.1) forces `d=0`. If `a>0`, evaluate at `t=-d/(2*a)` to get

```text
d^2 <= 4*kappa*a.                                       (5.2)
```

Thus

```text
u^T G_kappa u = 4*kappa*a-d^2 >=0
```

for every `u`; hence `G_kappa` is PSD. Its trace and determinant are nonnegative, and (2.1)–(2.2) give (B1)–(B2).

This shows that the two-gate source contract is not merely sufficient: for positive fixed `kappa` it is mathematically exact.

---

## 6. How the PD and singular branches reappear automatically

This theorem does not invalidate T-P5-051. T-P5-051 remains useful for the **sharp minimum cost** and explicit unbounded rays. The new theorem is the correct adapter when the downstream consumer already supplies a candidate budget `kappa`.

### 6.1 Positive-definite branch

If `D4>0`, (G2) is

```text
kappa >= Nsig/D4.
```

Since `D4=4*Delta`, this is exactly

```text
kappa >= N/(4*Delta),
```

which is the T-P5-051 sharp PD charge. The trusted gate itself need not perform this division.

### 6.2 Nonzero singular PSD branch

Suppose `D4=0` and the effective matrix is nonzero PSD. Then (G2) forces

```text
Nsig <= 0.
```

But for singular PSD `H`, `Nsig=b^T adj(H)b>=0`, so necessarily

```text
Nsig=0,
```

which is exactly the kernel/range compatibility condition. The remaining magnitude condition is (G1):

```text
B2 <= 4*kappa*tau,
```

or

```text
kappa >= B2/(4*tau),
```

which is the T-P5-050/T-P5-051 sharp rank-one cost.

### 6.3 Zero matrix

If `H=0`, then `tau=0`; (G1) forces `B2=0`, hence `b=0`. So the zero-matrix boundary is also fail-closed without a branch statement.

### 6.4 Non-PSD branch

Because `G_kappa PSD` implies `H PSD`, a non-PSD `H` cannot satisfy the two gates for any `kappa>0`. Thus the unbounded non-PSD rays from T-P5-051 are automatically excluded.

---

## 7. Source-cell contract: enclose the correlated remainders directly

For a source state/cell parameter `z`, define

```text
Rtr(z)  := 4*kappa*(p(z)+s(z))
           - b4(z)^2-b5(z)^2,

Rdet(z) := kappa*(4*p(z)*s(z)-sigma(z)^2)
           - [s(z)*b4(z)^2
              - sigma(z)*b4(z)*b5(z)
              + p(z)*b5(z)^2].
```

A uniform source-to-math certificate over a domain `D` is simply

```text
kappa > 0,
forall z in D, 0 <= Rtr(z),
forall z in D, 0 <= Rdet(z).                             (7.1)
```

Then for every `z in D` and every residual-power coordinate `(x,y)`, the affine energy contribution is at most `kappa`.

This is the preferred interval/checker interface. It keeps the cancellation between curvature degeneration and bias degeneration inside the polynomial that must be enclosed.

---

## 8. Important obstruction: do NOT intervalize `D4` and `Nsig` independently near the singular boundary

Independent extrema can destroy an exact valid certificate.

Take the exact polynomial family, for `t in [0,1]`,

```text
p(t)=t^2,
s(t)=1,
sigma(t)=0,
b4(t)=2*t,
b5(t)=0,
kappa=1.
```

Then

```text
tau  = 1+t^2,
D4   = 4*t^2,
B2   = 4*t^2,
Nsig = 4*t^2.
```

Therefore

```text
Rtr  = 4*(1+t^2)-4*t^2 = 4,
Rdet = 4*t^2-4*t^2 = 0
```

identically. The branch-free theorem proves the uniform sharp bound

```text
-t^2*x^2-y^2-2*t*x <= 1
```

through the entire cell, including the singular endpoint `t=0`.

Indeed, for `t>0` the maximum is `1`, attained at `x=-1/t,y=0`; at `t=0` the maximum is `0`.

But independent interval extrema give

```text
D4_lower = 0,
Nsig_upper = 4,
```

and the decoupled test

```text
kappa*D4_lower >= Nsig_upper
```

falsely becomes `0>=4`.

So if a cell approaches `D4=0`, the source checker should interval-evaluate the **joint remainder** `Rdet=kappa*D4-Nsig` itself. A lower bound on `D4` plus a separate upper bound on `Nsig` is only a fallback and can lose an otherwise exact certificate.

This is a source-interface issue, not a weakness in the energy theorem.

---

## 9. Both gates are necessary; determinant compatibility alone is not enough

The singular boundary also shows why `Rtr` must not be dropped.

Take

```text
p=0, s=1, sigma=0,
b4=0, b5=2,
kappa=1/2.
```

Then

```text
D4=0,
Nsig=0,
```

so the determinant/compatibility gate passes exactly. But

```text
B2=4 > 4*kappa*tau=2,
```

and

```text
J(0,y)=-y^2-2*y
```

has maximum `1`, which exceeds `kappa=1/2`.

Conversely, trace alone cannot detect a kernel component. With

```text
p=0, s=1, sigma=0,
b4=1, b5=0,
kappa=1/4,
```

(G1) holds at equality, but

```text
Nsig=1 > 0=kappa*D4,
```

and `J(x,0)=-x` is unbounded above as `x -> -infinity`.

Thus the pair `(Rtr,Rdet)` is the minimal natural 2x2 invariant packet for a positive fixed charge.

---

## 10. Monotonicity and strict reserve

If the two gates hold for `kappa0>0`, then they also hold for every `kappa>=kappa0` because the theorem already gives `J<=kappa0<=kappa`. Algebraically, after `H PSD` is known, both source remainders are monotone in `kappa`.

For a consumer that needs a strict reserve `m>0` below an available budget `K`, do not introduce a new completion formula. Set

```text
kappa := K-m
```

and certify the same two gates with `K-m>0`. Then

```text
J <= K-m < K.
```

This keeps strictness in the scalar budget layer rather than mixing it into the source Jacobian semantics.

---

## 11. Suggested minimal Lean/theorem interface

The trusted mathematical core can be very small and matrix-free:

```text
sym2_scaled_qf_nonneg_of_trace_det4
```

```text
4*a*c-m^2 >= 0,
a+c >= 0
  -> 0 <= a*x^2+m*x*y+c*y^2.
```

```text
affine_majorant_scaled_identity
```

```text
4*kappa*(Q+d+kappa)
 = Gquad + (d+2*kappa)^2.
```

```text
affine_energy_le_of_two_invariant_gates
```

```text
0 < kappa
-> B2 <= 4*kappa*tau
-> Nsig <= kappa*D4
-> -Q-d <= kappa.
```

Optionally, over `Real`, add the converse:

```text
affine_energy_global_iff_two_invariant_gates
```

```text
0 < kappa
-> ((forall x y, -Q-d <= kappa)
    <-> (B2 <= 4*kappa*tau
         and Nsig <= kappa*D4)).
```

The source adapter should quantify `z` outside this theorem and feed the same fixed rational `kappa` plus the two lower-bound witnesses `Rtr(z)>=0`, `Rdet(z)>=0`.

No matrix PSD API, `Real.sqrt`, eigenvalue, inverse, pseudoinverse, or branch-dependent division is required for the forward consumer.

---

## 12. Typed interface requirements

The theorem is only sound as a source adapter if the following remain same-key and same-coordinate:

1. `p,s,sigma` are the signed symmetric effective-dissipation coefficients for the same state/cell.
2. `sigma` is formed before entrywise absolute-value intervalization; in the T-P5-045 convention it is `k45+k54`.
3. `b4,b5` are the affine/transverse/anchor remainder in the same `(u4,u5)` power coordinates.
4. `kappa` is one fixed positive energy charge for the consumer scope being certified.
5. The source checker encloses `Rtr` and `Rdet` on the same domain as the consumer.

A `K_path` absolute envelope that has already destroyed the signed `sigma` cancellation cannot silently instantiate this contract; it must use the older conservative fallback lane.

---

## 13. Boundaries / not closed

This review does **not** prove:

- that the deployed source exports signed `p,s,sigma,b4,b5` on any physical cell;
- that interval/Float64 evaluation encloses `Rtr` or `Rdet`;
- centered-to-full residual or anchor-bias binding;
- controller/FD/solve remainders;
- first-exit, ODE, trajectory, P8, or domain coverage;
- Lean compilation, axioms, independent verification, comparator, provenance admission, registry promotion, P5/M4 closure.

It also does not replace T-P5-049 shared-`r` / varying-curvature work or T-P5-050 Lean work.

Admission remains **pending mathematical/interface child**.
