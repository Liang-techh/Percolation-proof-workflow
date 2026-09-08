---
kind: review_result
review_id: review-T-P5-050-kuangmanmozun-20260907T2238
task_id: T-P5-050
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-07T22:30:00-06:00
created_at: 2026-09-07T22:38:00-06:00
claim_commit: 747caceda3e81a63fd97403814299cc7505dcbef
inspected_commit: 09ce4a35611a1dac9433c4b55a048c1b979ca8ab
continuation_of:
  - review-T-P5-048-sumengchen-20260907T2223
related_tasks:
  - T-P5-044
  - T-P5-048
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_a_pivot-free_singular-PSD_dispatcher_after_T-P5-044/T-P5-048; use_the_trace_completion_branch_for_nonzero_rank-one_H_and_a_separate_zero-matrix_branch; do_not_reuse_the_p-pivot_compatibility_equation_when_p_may_vanish
---

# T-P5-050 — complete singular PSD 2x2 affine-completion classifier

## 0. Result

T-P5-048 closes the singular branch

```text
det H = 0,     p > 0,
H = [[p,q],[q,s]],
p*b5 = q*b4.
```

That is enough when `p` is a certified positive pivot, but it is not an exhaustive singular-PSD dispatcher. In particular:

- a perfectly valid rank-one PSD matrix can have `p=0, s>0`;
- then the old `p*b5=q*b4` condition becomes vacuous because `p=q=0`;
- at `H=0`, even the two adjugate compatibility equations are vacuous, while a nonzero affine bias is unbounded.

This review gives an exact pivot-free classification of all singular PSD `2x2` matrices and a sharp finite completion cost whenever one exists.

Let

```text
H = [[p,q],[q,s]],
Q(x,y) = p*x^2 + 2*q*x*y + s*y^2,
B(x,y) = b4*x + b5*y,
J(x,y) = -Q(x,y)-B(x,y).
```

Assume

```text
p >= 0,
s >= 0,
Delta := p*s-q^2 = 0.                                  (0.1)
```

Define

```text
tau := p+s,
k4 := s*b4-q*b5,
k5 := p*b5-q*b4,
N  := s*b4^2 - 2*q*b4*b5 + p*b5^2.                    (0.2)
```

Thus `(k4,k5)=adj(H)*b` and `N=b^T adj(H)b`.

Then:

```text
There exists a finite C with J(x,y) <= C for every x,y

iff

  [tau > 0 and k4=0 and k5=0]
  or
  [tau = 0 and b4=0 and b5=0].                         (0.3)
```

For the nonzero rank-one branch `tau>0`, the sharp constant is

```text
sup J = (b4^2+b5^2)/(4*tau).                            (0.4)
```

For the zero-matrix branch `tau=0, b=0`, the sharp constant is `0`.

If either compatibility condition fails in the nonzero rank-one branch, or if `H=0` and `b!=0`, then `J` is unbounded above along an explicit kernel ray.

This is an exact obstruction theorem, not a sufficient Young bound.

---

## 1. Three division-free identities

Everything follows from three polynomial identities.

### 1.1 Adjugate vector is a determinant-scaled kernel vector

Direct expansion gives

```text
p*k4 + q*k5 = Delta*b4,
q*k4 + s*k5 = Delta*b5.                                (1.1)
```

Hence under `Delta=0`,

```text
H*(k4,k5)^T = 0.                                       (1.2)
```

In particular `Q(k4,k5)=0`.

### 1.2 Exact incompatibility numerator identity

One has

```text
k4^2+k5^2
  = tau*N - Delta*(b4^2+b5^2).                         (1.3)
```

Therefore on the singular branch,

```text
k4^2+k5^2 = tau*N.                                     (1.4)
```

If `tau>0` and `(k4,k5)!=(0,0)`, then `N>0` automatically.

### 1.3 Pivot-free trace completion identity

For arbitrary coefficients,

```text
[2*(p*x+q*y)+b4]^2 + [2*(q*x+s*y)+b5]^2

= 4*tau*(Q(x,y)+B(x,y)) + (b4^2+b5^2)
  - 4*[Delta*(x^2+y^2) + k4*x + k5*y].                 (1.5)
```

Thus if `Delta=0` and `k4=k5=0`,

```text
4*tau*(Q+B) + (b4^2+b5^2)
 = [2*(p*x+q*y)+b4]^2 + [2*(q*x+s*y)+b5]^2 >= 0.        (1.6)
```

Equivalently,

```text
4*tau*J(x,y) <= b4^2+b5^2.                             (1.7)
```

No square root, eigenvalue, inverse, or choice of positive diagonal pivot occurs in the core identity.

---

## 2. Nonzero rank-one branch: exact finite cost

Assume

```text
tau>0,
Delta=0,
k4=0,
k5=0.                                                (2.1)
```

The compatibility equations are exactly

```text
s*b4 = q*b5,
p*b5 = q*b4.                                          (2.2)
```

They are the pivot-free statement that `b` lies in `range(H)`.

From (1.7),

```text
J(x,y) <= (b4^2+b5^2)/(4*tau).                         (2.3)
```

This constant is sharp.  Compatibility implies

```text
H*b = tau*b,                                           (2.4)
```

because

```text
tau*b4-(p*b4+q*b5) = k4,
tau*b5-(q*b4+s*b5) = k5.
```

Therefore at

```text
(x*,y*) = -(b4,b5)/(2*tau),                            (2.5)
```

one has `H*(x*,y*)=-b/2`; both squares on the right of (1.6) vanish and equality holds in (2.3).

So (0.4) is the exact Moore-Penrose completion value, obtained here without introducing a pseudoinverse.

---

## 3. Nonzero rank-one incompatibility is genuinely unbounded

Now assume

```text
tau>0,
Delta=0,
(k4,k5)!=(0,0).                                        (3.1)
```

By (1.4), `N>0`.  Also

```text
Q(k4,k5)=0,
B(k4,k5)=N.                                            (3.2)
```

For an arbitrary proposed upper bound `C`, choose

```text
t := (C+1)/N,
(x,y) := -t*(k4,k5).                                   (3.3)
```

Then

```text
Q(x,y)=0,
B(x,y)=-t*N,
J(x,y)=t*N=C+1>C.                                      (3.4)
```

Hence no finite completion constant exists.

This provides a symmetric version of the kernel-ray obstruction in T-P5-048 and does not require deciding in advance whether `p` or `s` is the positive pivot.

---

## 4. Fully degenerate branch `H=0`

If `tau=0` under `p>=0,s>=0`, then

```text
p=s=0.                                                 (4.1)
```

Together with `Delta=0`, this gives `q=0`, hence `H=0` and

```text
J(x,y)=-(b4*x+b5*y).                                   (4.2)
```

### 4.1 Zero bias

If `b4=b5=0`, then

```text
J(x,y)=0                                               (4.3)
```

for every state.  The sharp finite completion cost is exactly zero.

### 4.2 Nonzero bias

If `(b4,b5)!=(0,0)`, let

```text
B2 := b4^2+b5^2 > 0.
```

For arbitrary `C`, choose

```text
(x,y) := -((C+1)/B2)*(b4,b5).                          (4.4)
```

Then

```text
J(x,y)=C+1>C.                                          (4.5)
```

Thus every nonzero bias is unbounded when `H=0`.

This is why `adj(H)b=0` is **not** a complete singular compatibility test at the zero matrix: `adj(0)=0` annihilates every `b`.

---

## 5. Exact exhaustive classifier

Combining Sections 2-4 yields the promised theorem.

Under

```text
p>=0, s>=0, p*s=q^2,
```

define

```text
FiniteUpper :<=> exists C, forall x y, J(x,y)<=C.
```

Then

```text
FiniteUpper
iff
(
  tau>0 and k4=0 and k5=0
)
or(
  tau=0 and b4=0 and b5=0
).                                                       (5.1)
```

Moreover:

```text
tau>0, compatible:
  sharp C = (b4^2+b5^2)/(4*tau);

tau>0, incompatible:
  explicit adjugate-kernel ray makes J unbounded;

tau=0, b=0:
  sharp C = 0;

tau=0, b!=0:
  explicit bias ray makes J unbounded.                  (5.2)
```

This is the complete source-independent singular PSD boundary for the current two-channel affine-completion model.

---

## 6. Relation to the existing T-P5-048 p-pivot theorem

When `p>0`, the new symmetric formula reduces exactly to the existing T-P5-048 cost.

From compatibility,

```text
p*(b4^2+b5^2) = tau*b4^2.                              (6.1)
```

Therefore

```text
(b4^2+b5^2)/tau = b4^2/p.                              (6.2)
```

Similarly, whenever `s>0`,

```text
s*(b4^2+b5^2) = tau*b5^2,
(b4^2+b5^2)/tau = b5^2/s.                              (6.3)
```

So the trace formula is not a weaker fallback; it is the same sharp rank-one completion written without choosing a pivot.

This gives immediate pivot-free versions of the two strict gates already exported by T-P5-048.  Under nonzero rank-one compatibility, the old p-pivot conditions

```text
200*b4^2 < (109-r)*p,
600*g4^2 < (109-r)*p                                   (6.4)
```

are exactly equivalent (when `p>0`) to

```text
200*(b4^2+b5^2) < (109-r)*(p+s),
600*(g4^2+g5^2) < (109-r)*(p+s).                       (6.5)
```

The symmetric form remains meaningful on the valid axis branch `p=0,s>0`, where the old p-pivot theorem cannot even be instantiated.

At `H=0,b=0`, however, (6.5) degenerates to `0<0`; the dispatcher must take the separate zero-cost branch rather than forcing a rank-one strict gate.

---

## 7. Counterexamples that must be kept as regressions

### 7.1 One p-pivot compatibility equation is unsafe if p can vanish

Take

```text
H = [[0,0],[0,1]],
b = (1,0).                                              (7.1)
```

Then `Delta=0`, `H` is rank-one PSD, and

```text
p*b5 = q*b4
```

holds vacuously as `0=0`.  But

```text
k4=1,
k5=0,
J(x,y)=-y^2-x.                                         (7.2)
```

Along `(x,y)=(-t,0)`, `J=t -> +infinity`.

So a checker must not reuse the T-P5-048 `p*b5=q*b4` condition unless it has separately proved `p>0`.

### 7.2 The symmetric axis branch is valid and has finite sharp cost

Take

```text
H = [[0,0],[0,2]],
b = (0,3).                                              (7.3)
```

Then `tau=2`, both pivot-free compatibility equations hold, and

```text
J(x,y)=-2*y^2-3*y <= 9/8,                              (7.4)
```

with equality at `y=-3/4`.  The trace formula gives

```text
(b4^2+b5^2)/(4*tau)=9/8.                               (7.5)
```

Thus excluding `p=0,s>0` would incorrectly reject a perfectly valid finite-cost singular branch.

### 7.3 Adjugate compatibility alone fails at H=0

Take

```text
H=0,
b=(1,1).                                               (7.6)
```

Then `k4=k5=0` vacuously, but

```text
J(x,y)=-(x+y)
```

is unbounded along `(-t,-t)`, where `J=2t`.

Hence the zero matrix requires the additional exact condition `b=0`.

### 7.4 Non-axis incompatible rank-one example

Take

```text
H=[[1,1],[1,1]],
b=(1,0).                                               (7.7)
```

Then `tau=2`, `k=(1,-1)`, and along `u=-t*(1,-1)` one has

```text
Q(u)=0,
J(u)=t -> +infinity.                                   (7.8)
```

This is the generic adjugate-kernel obstruction in the smallest rational example.

---

## 8. Lean-friendly theorem split

A minimal formal sidecar can avoid matrix libraries entirely.

Suggested scalar lemmas:

```text
singular_adj_kernel_coordinates
```

Prove (1.1) by `ring`.

```text
adj_norm_numerator_identity
```

Prove (1.3) by `ring`.

```text
singular_trace_completion_identity
```

Use the denominator-free form (1.5); the singular compatible theorem is an immediate specialization.

```text
singular_trace_completion_cleared
```

From `tau>0`, `Delta=0`, `k4=k5=0`, prove

```text
4*tau*(-Q-B) <= b4^2+b5^2.
```

```text
singular_trace_completion_sharp
```

Either expose the rational witness `u=-b/(2*tau)` after `tau>0`, or state the equality under the denominator-free equations

```text
2*tau*x+b4=0,
2*tau*y+b5=0.
```

```text
singular_incompatible_no_uniform_upper_bound
```

Use the adjugate ray from Section 3.

```text
zero_matrix_finite_iff_bias_zero
```

Use Section 4.

```text
singular_psd_finite_upper_iff
```

Combine the two branches into (5.1).

Optional adapter lemmas:

```text
p_pivot_cost_eq_trace_cost
s_pivot_cost_eq_trace_cost
```

Use the division-free identities (6.1)/(6.3), and export the symmetric versions of the `200` and `600` gates.

All core algebra is `ring`/ordered-field reasoning; no eigenvalue, square root, inverse matrix, pseudoinverse, source data, or Float64 semantics is needed.

---

## 9. Boundary and requested integration

This result closes only the **source-independent singular PSD affine-completion classification**.

It does **not** establish:

- that the deployed P5 Hessian/source matrix is PSD or singular on any concrete cell;
- that the exact equalities `Delta=0`, `k4=0`, `k5=0` hold for deployed rational/interval data;
- any Float64/FD/controller/true-DH semantics;
- first-exit/continuation or P8 coverage;
- P5/P8/M4 parent closure;
- registry admission.

Recommended dispatcher after formalization:

```text
Delta > 0:
  use T-P5-044 positive-definite completion;

Delta = 0 and tau > 0:
  require k4=k5=0 and use the pivot-free trace cost;

Delta = 0 and tau = 0:
  require b4=b5=0 and charge zero;

otherwise:
  exact affine-completion obstruction.                 (9.1)
```

The important implementation rule is fail-closed: a vanished pivot or vanished determinant is a branch change, not permission to keep using a formula whose denominator or compatibility premise disappeared.
