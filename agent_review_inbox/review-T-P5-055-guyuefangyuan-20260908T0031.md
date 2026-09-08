---
kind: review_result
review_id: review-T-P5-055-guyuefangyuan-20260908T0031
task_id: T-P5-055
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-08T00:19:00-06:00
created_at: 2026-09-08T00:31:00-06:00
claim_commit: 6d9e46018081f1cf66483b7422bf0f54fb7a02af
inspected_commit: 8672c6048c3b21bd0c890c7bc280d77135526cad
inspected_paths:
  - README.md
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-052-guyuefangyuan-20260907T2334.md
  - agent_review_inbox/review-T-P5-052-bernstein-cell-lean-juyangxianzun-20260907T2359.md
  - agent_review_inbox/review-T-P5-053-honglianmozun-20260907T2350.md
  - agent_review_inbox/review-T-P5-054-correlated-matrix-perturbation-liuguanyi-20260908T0013.md
  - agent_review_inbox/companion-T-P5-054-correlated-matrix-perturbation-liuguanyi-20260908T0016.md
continuation_of:
  - T-P5-052
  - T-P5-053
related_tasks:
  - T-P5-BRANCHFREE-AFFINE-MAJORANT
  - T-P5-054
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add a quantitative exact-rational completeness theorem for dyadic Bernstein subdivision under strict positivity, plus a zero-contact obstruction showing why mere nonnegativity can stall forever; keep negative noncorner controls tri-state and provide a rational-root/factorization escape hatch rather than false rejection
---

# T-P5-055 — quantitative dyadic Bernstein completeness and the exact zero-contact obstruction

## 0. Question

`T-P5-052` established the exact one-dimensional quadratic/cubic Bernstein gate and exact half-subdivision identities.  Its pinned Lean review explicitly left open the theorem that a **strictly positive** polynomial is eventually certified by sufficiently fine dyadic Bernstein subdivision.

`T-P5-053` tensorized the same correlated-energy idea to rational boxes and again left multivariate eventual-positive-control completeness open.

This child closes that mathematical gap and also identifies the sharp boundary:

1. for a strictly positive rational polynomial, exact dyadic subdivision is not merely a heuristic: after a finite explicitly bounded depth, **every** Bernstein control on **every** child is strictly positive;
2. for a merely nonnegative polynomial touching zero, this can fail forever, even for the rational quadratic `(t-1/3)^2`;
3. therefore `negative noncorner control -> SUBDIVIDE/UNDECIDED` is not only a temporary implementation convention.  At zero contact it can remain undecided at every dyadic depth unless the checker adds a different exact certificate such as a rational-root split, factorization, SOS, or pointwise zero-contact argument.

Everything below is source-independent algebra/analysis.  No deployed Float64, DH, FD, controller, solve, P8, receipt, provenance, or admission claim is made.

---

## 1. Tensor polynomial and child notation

Let

```text
P(u) = sum_beta c_beta * u^beta,
```

on the normalized box

```text
u=(u1,...,ud) in [0,1]^d,
```

with a finite degree vector `n=(n1,...,nd)` and rational coefficients `c_beta` when a checker instantiates the theorem.

Use the standard multi-index notation

```text
|beta| = beta1+...+betad,
u^beta = product_j uj^(beta_j).
```

Fix a uniform dyadic depth `N` and write

```text
h = 2^(-N).
```

A child box is

```text
Q(a,h) = product_j [a_j, a_j+h],
```

where every `a_j=k_j/2^N` and `0 <= a_j <= 1-h`.

Normalize the child again by

```text
u = a + h*t,
0 <= t_j <= 1.
```

Let

```text
B_I(P;a,h)
```

denote the tensor Bernstein control of `P(a+h*t)` at tensor index `I`, using any padded degree vector `n` dominating the monomial degrees of `P`.

The exact tensor monomial-to-Bernstein formula from `T-P5-053` is the only Bernstein identity needed below.

---

## 2. Exact child monomial expansion

For one monomial,

```text
(a+h*t)^beta
 = sum_{gamma <= beta}
     binom(beta,gamma)
     a^(beta-gamma)
     h^|gamma|
     t^gamma.                                           (2.1)
```

Therefore

```text
P(a+h*t)
 = sum_gamma q_gamma(a,h) * t^gamma,                    (2.2)
```

with

```text
q_gamma(a,h)
 = h^|gamma| *
   sum_{beta >= gamma}
     c_beta * binom(beta,gamma) * a^(beta-gamma).       (2.3)
```

In particular,

```text
q_0(a,h) = P(a).                                        (2.4)
```

For `a in [0,1]^d`, triangle inequality gives

```text
|q_gamma(a,h)|
 <= h^|gamma| *
    sum_{beta >= gamma}
      |c_beta| * binom(beta,gamma).                     (2.5)
```

All of (2.1)-(2.5) are finite ring/ordered-field identities and inequalities; no derivatives are needed.

---

## 3. A Bernstein control stays close to the child corner value

For the padded tensor degree vector `n`, the exact Bernstein control is

```text
B_I(P;a,h)
 = sum_{gamma <= I}
     q_gamma(a,h)
     product_j [binom(I_j,gamma_j)/binom(n_j,gamma_j)]. (3.1)
```

Whenever `gamma_j <= I_j <= n_j`, every ratio in (3.1) lies in `[0,1]`.  Hence, separating the constant term `gamma=0`,

```text
|B_I(P;a,h) - P(a)|
 <= sum_{gamma != 0} |q_gamma(a,h)|.                    (3.2)
```

Substitute (2.5) and reverse the two finite sums:

```text
sum_{gamma != 0} |q_gamma(a,h)|
 <= sum_beta |c_beta|
      * sum_{0 != gamma <= beta}
          binom(beta,gamma) h^|gamma|.                  (3.3)
```

By the tensor binomial theorem,

```text
sum_{gamma <= beta}
  binom(beta,gamma) h^|gamma|
 = product_j (1+h)^(beta_j)
 = (1+h)^|beta|.                                       (3.4)
```

Therefore define the exact rational control-error majorant

```text
E_P(h)
 := sum_{beta != 0}
      |c_beta| * ((1+h)^|beta| - 1).                    (3.5)
```

Then every child and every tensor control satisfy the uniform bound

```text
|B_I(P;a,h) - P(a)| <= E_P(h).                          (3.6)
```

This is the first main theorem.

### T-P5-055-A — exact control/corner deviation bound

For every polynomial `P`, every dyadic child `Q(a,h)` of `[0,1]^d`, and every padded tensor Bernstein control,

```text
P(a) - E_P(h)
 <= B_I(P;a,h)
 <= P(a) + E_P(h).                                      (3.7)
```

When the `c_beta` and `h` are rational, `E_P(h)` is rational.  No root, eigenvalue, minimizer, floating optimization, or interval dependency is involved.

---

## 4. Coarser linear-in-cell-size bound

For `0 <= h <= 1` and every integer `m>=1`,

```text
(1+h)^m - 1
 = sum_{r=1}^m binom(m,r) h^r
 <= h * sum_{r=1}^m binom(m,r)
 = h*(2^m-1).                                           (4.1)
```

Define the coefficient complexity

```text
C_P
 := sum_{beta != 0}
      |c_beta| * (2^|beta| - 1).                        (4.2)
```

Then

```text
E_P(h) <= h*C_P,                                        (4.3)
```

so every child control obeys

```text
B_I(P;a,h) >= P(a) - h*C_P.                             (4.4)
```

This coarser form is especially convenient for a trusted checker because it removes all dependence on the child location and leaves only one exact rational constant `C_P` for the parent polynomial.

---

## 5. Quantitative strict-positivity completeness

Assume a uniform semantic margin

```text
P(u) >= delta > 0
```

for every `u in [0,1]^d`.

At dyadic depth `N`, `h=2^(-N)`, so (4.4) gives

```text
B_I(P;a,2^-N)
 >= delta - 2^-N*C_P.                                  (5.1)
```

Thus the exact integer/rational inequality

```text
2^N * delta > C_P                                      (5.2)
```

implies

```text
B_I(P;a,2^-N) > 0                                      (5.3)
```

for **every** depth-`N` dyadic child and **every** Bernstein control on that child.

### T-P5-055-B — explicit finite stopping depth

If

```text
forall u in [0,1]^d, P(u) >= delta,
delta > 0,
2^N * delta > C_P,
```

then the complete depth-`N` tensor Bernstein packet is strictly positive.

The checker does not need logarithms to find such `N`: starting from `pow2=1`, repeatedly double the exact integer until

```text
pow2*delta > C_P.
```

Because `delta>0` and `C_P` is finite, this terminates.

The sharper test

```text
delta > E_P(2^-N)                                      (5.4)
```

may certify at a smaller depth, but (5.2) is the simplest proof-oriented gate.

---

## 6. The open theorem from T-P5-052 is therefore true

Suppose only that

```text
P(u) > 0
```

for every `u in [0,1]^d`.

A polynomial is continuous, and `[0,1]^d` is compact.  Hence `P` attains a minimum

```text
m = min_[0,1]^d P > 0.
```

Take, for example,

```text
delta = m/2 > 0.
```

By T-P5-055-B there exists finite `N` such that every Bernstein control on every depth-`N` dyadic child is strictly positive.

### T-P5-055-C — eventual positive-control completeness

For a polynomial strictly positive on a compact rational box, uniform exact dyadic Bernstein subdivision eventually produces an all-positive control packet.

This theorem is an analysis-level completeness statement.  The **trusted checker** does not need to know or formalize `m`; it only executes exact subdivision and exact control tests.  The theorem says that, if the semantic strict positivity assumption is true, that search cannot run forever.

For a proof artifact that already has an explicit rational lower margin `delta`, T-P5-055-B is preferable because it gives a constructive exact depth bound and avoids compactness entirely.

---

## 7. Degree-2 and degree-3 formulas used by the current P5 lane

For a one-dimensional quadratic

```text
P(t)=a0+a1*t+a2*t^2,
```

(3.5) gives

```text
E_P(h)
 = |a1|*h
   + |a2|*(2h+h^2),                                    (7.1)
```

and

```text
C_P = |a1| + 3|a2|.                                    (7.2)
```

Therefore

```text
P>=delta>0
and
2^N*delta > |a1|+3|a2|
```

is sufficient for every quadratic Bernstein control on every depth-`N` child to be positive.

For a cubic

```text
P(t)=a0+a1*t+a2*t^2+a3*t^3,
```

we get

```text
E_P(h)
 = |a1|*h
   + |a2|*(2h+h^2)
   + |a3|*(3h+3h^2+h^3),                               (7.3)
```

and

```text
C_P = |a1| + 3|a2| + 7|a3|.                            (7.4)
```

Thus

```text
2^N*delta > |a1|+3|a2|+7|a3|                          (7.5)
```

is an exact-rational finite-depth certificate for the current `T-P5-052` cubic lane.

These are small enough to formalize directly in the existing Lean sidecar without introducing multivariate polynomial APIs.

---

## 8. Nonnegative polynomials have a quantitative near-pass bound

If only

```text
P(u) >= 0
```

is known, (4.4) still yields

```text
B_I(P;a,2^-N) >= -2^-N*C_P.                             (8.1)
```

Therefore every negative Bernstein control must converge uniformly to zero at least at this coarse `O(2^-N)` rate under uniform subdivision.

Equivalently, for any rational `eps>0`,

```text
2^N*eps > C_P
```

implies

```text
B_I > -eps                                             (8.2)
```

on every child.

This is useful diagnostically, but it is **not** an exact nonnegativity proof: a control may remain strictly negative at every finite depth while tending to zero.

The next section shows that this is a real obstruction, not a weakness of the estimate.

---

## 9. Exact zero-contact obstruction: `(t-1/3)^2`

Consider the rational polynomial

```text
Z(t) = (t-1/3)^2
     = t^2 - (2/3)t + 1/9.                              (9.1)
```

Clearly

```text
Z(t) >= 0
```

for every real `t`, with the unique zero `t=1/3`.

For every dyadic depth `N>=0`, `1/3` is not a dyadic rational.  Hence it lies strictly inside a unique depth-`N` cell

```text
[a,a+h],
h=2^-N,
a=floor(2^N/3)/2^N.                                   (9.2)
```

Write

```text
x = a - 1/3 < 0,
x+h > 0.                                                (9.3)
```

After normalization `t=a+h*s`,

```text
Z(a+h*s) = (x+h*s)^2.                                   (9.4)
```

Its degree-2 Bernstein controls are

```text
beta0 = x^2,
beta1 = x*(x+h),
beta2 = (x+h)^2.                                         (9.5)
```

Because the root lies strictly inside the cell,

```text
beta1 < 0.                                              (9.6)
```

In fact the value is completely explicit.  Since

```text
2^N mod 3 is either 1 or 2,
```

one obtains

```text
beta1 = -2/(9*4^N) < 0.                                 (9.7)
```

So the all-controls-nonnegative quadratic checker **fails at every dyadic depth**, despite `Z>=0` globally.

### The obstruction survives cubic padding

If the same quadratic is degree-elevated to cubic Bernstein form on the root-containing cell, the root position inside the normalized cell is either

```text
alpha=1/3
```

or

```text
alpha=2/3.
```

For `(s-alpha)^2`, the two interior cubic controls are

```text
gamma1 = alpha*(3alpha-2)/3,
gamma2 = (alpha-1)*(3alpha-1)/3.                         (9.8)
```

Thus one of them is exactly

```text
-1/9,
```

and after restoring the child scale one cubic control is

```text
-1/(9*4^N) < 0.                                         (9.9)
```

Therefore the same zero-contact obstruction applies to a degree-3 padded checker as well.

### T-P5-055-D — no finite dyadic all-control certificate for this exact nonnegative polynomial

No finite dyadic partition of `[0,1]` can make all degree-2 Bernstein controls of `Z` nonnegative, because every finite dyadic partition contains one cell whose interior contains `1/3`, and that cell has the negative control (9.5).

The same remains true after padding to degree 3 by (9.8)-(9.9).

This proves that the strict positivity hypothesis in T-P5-055-C cannot simply be weakened to `P>=0` for the current all-controls-nonnegative dyadic decision rule.

---

## 10. Exact escape hatch at zero contact

The obstruction is specific to the **dyadic partition geometry**, not to Bernstein itself.

Split exactly at the rational zero `1/3`.

On the left interval, set

```text
t = s/3,
0<=s<=1.
```

Then

```text
Z = (1-s)^2/9,
```

whose degree-2 Bernstein controls are

```text
(1/9, 0, 0).                                            (10.1)
```

On the right interval, set

```text
t = 1/3 + (2/3)s.
```

Then

```text
Z = 4s^2/9,
```

with controls

```text
(0, 0, 4/9).                                            (10.2)
```

Both child packets pass exactly.

So a robust checker should preserve the following tri-state semantics:

```text
all controls >= 0
    -> PASS;

exact rational point with P<0
    -> genuine OBSTRUCTION;

negative noncorner control without a point witness
    -> SUBDIVIDE / UNDECIDED.
```

If subdivision keeps localizing around a zero-contact set, the mathematically correct next route is an exact factorization/root split/SOS/zero-contact certificate, not `REJECTED`.

This is especially relevant to `Rdet`, whose physically interesting branch-free boundary can be rank-deficient and therefore may naturally have exact zero contact.

---

## 11. Combined P5 branch-free stopping theorem

Suppose the exact source-independent correlated remainders on a normalized rational box are polynomials

```text
Rtr(u),
Rdet(u),
```

and suppose an independent mathematical argument establishes strict margins

```text
Rtr(u)  >= delta_tr  > 0,
Rdet(u) >= delta_det > 0                                (11.1)
```

throughout the box.

Compute their exact monomial coefficient complexities

```text
C_tr  = C_(Rtr),
C_det = C_(Rdet).                                       (11.2)
```

Choose any natural `N` satisfying the two division-free rational inequalities

```text
2^N * delta_tr  > C_tr,
2^N * delta_det > C_det.                                (11.3)
```

Then every tensor Bernstein control of both remainders is strictly positive on every depth-`N` child.  The existing `T-P5-053` branch-free consumer therefore proves the fixed-`kappa` affine-energy bound throughout the entire parent box.

### T-P5-055-E — finite exact Bernstein realization of strict branch-free margins

Strict semantic positivity of both correlated remainders implies finite exact dyadic Bernstein certification, with explicit rational stopping inequalities (11.3).

This is the missing logical direction needed to interpret adaptive Bernstein subdivision as a complete search method **inside the strict-margin regime**.

If one remainder is only nonnegative and touches zero, T-P5-055-D shows why no analogous termination claim is valid without an additional boundary certificate.

---

## 12. Relation to T-P5-054 approximate-source transport

`T-P5-054` inserts a nominal-plus-error layer:

```text
nominal Bernstein reserve
 + correlated perturbation correction
 -> actual Rtr/Rdet >= 0.
```

The present result sharpens how that pipeline should treat reserve.

If the nominal-minus-error transport leaves explicit **strict** actual margins

```text
Rtr_actual  >= delta_tr > 0,
Rdet_actual >= delta_det > 0,
```

then T-P5-055 gives a finite dyadic Bernstein stopping depth whenever the actual/lower-enclosure remainder is polynomial.

Near a singular PSD boundary, however, `delta_det` may genuinely be zero.  In exactly that regime:

- `T-P5-054` already warns not to destroy determinant correlation with independent entry boxes;
- `T-P5-055` now warns not to expect dyadic all-control positivity to terminate merely from exact nonnegativity.

The two warnings are compatible: singular correlated geometry needs a boundary-aware exact certificate, not progressively more aggressive absolute-value intervalization.

---

## 13. Lean-friendly theorem decomposition

The current compiled `T-P5-052` sidecar already contains the exact quadratic/cubic Bernstein identities and dyadic half-de Casteljau formulas.  A minimal next Lean child does **not** need a general multivariate polynomial library.

Recommended first layer:

```text
quad_child_control_lower_of_corner
```

For `P(t)=a0+a1*t+a2*t^2`, `0<=a`, `0<=h`, `a+h<=1`, prove every degree-2 child control is at least

```text
P(a) - h*(|a1|+3|a2|).
```

```text
cubic_child_control_lower_of_corner
```

Analogously prove the cubic lower bound

```text
P(a) - h*(|a1|+3|a2|+7|a3|).
```

```text
quad_dyadic_controls_pos_of_uniform_margin
cubic_dyadic_controls_pos_of_uniform_margin
```

Consume `P(t)>=delta>0` and the exact `2^N*delta>C` inequality.

```text
dyadic_one_third_square_middle_control
```

Formalize, for the unique depth-`N` cell containing `1/3`,

```text
beta1 = -2/(9*4^N).
```

```text
dyadic_one_third_square_cubic_negative_control
```

Formalize the padded-cubic negative control `-1/(9*4^N)`.

Only after the tensor Bernstein package itself is compiled should the generic finite-dimensional statement be added:

```text
tensor_child_control_corner_deviation

tensor_dyadic_controls_pos_of_uniform_margin
```

The exact coefficient formula (3.5) makes that later theorem finite-sum algebra plus absolute-value bounds; compactness is needed only for the theorem that derives existence of a positive `delta` from pointwise strict positivity.

---

## 14. Checker contract suggested by the mathematics

For each exact polynomial remainder packet, a checker may store

```text
cell_key,
normalized_box_key,
monomial_coefficients,
padded_degree_vector,
```

and optionally

```text
certified_uniform_margin_delta,
coefficient_complexity_C.
```

Then there are two valid execution modes.

### Constructive depth mode

If `delta>0` is already certified, choose `N` by exact doubling until

```text
2^N*delta > C.
```

At that depth, positive controls are mathematically guaranteed.

### Blind exact subdivision mode

If no `delta` is known, repeatedly exact-subdivide unresolved cells and test controls.  T-P5-055-C guarantees eventual termination if the polynomial is in fact strictly positive everywhere.

If the process keeps localizing around a zero-contact set, do **not** reinterpret this as negativity.  Switch to a boundary lane: exact point evaluation, rational-root split, factorization/SOS, or a dedicated correlated rank-deficient certificate.

---

## 15. What is closed and what remains open

This review proves:

- an exact tensor child-control/corner deviation inequality;
- an exact rational error majorant `E_P(h)`;
- the simpler coefficient complexity bound `E_P(h)<=h*C_P`;
- an explicit rational finite stopping depth under a certified positive margin;
- eventual dyadic Bernstein completeness for strict polynomial positivity on a compact box;
- an `O(2^-N)` near-pass bound under mere nonnegativity;
- an exact rational polynomial showing that nonnegative zero-contact can fail the all-controls-nonnegative dyadic test forever;
- persistence of that obstruction under cubic degree padding;
- an exact rational-root split that certifies the same zero-contact polynomial;
- the corresponding finite stopping theorem for the two correlated P5 branch-free remainders.

Still open and outside this child:

- deployed source `Rtr/Rdet` being exact polynomials or certified polynomial lower enclosures;
- exact monomial coefficients for real P5 source cells;
- the actual positive margins `delta_tr/delta_det`, if any;
- what zero-contact/rank-deficient certificate is best for a real physical cell whose determinant margin is exactly zero;
- Float64/libm/FD/controller/solve semantics;
- source-key and physical-domain binding;
- P8 trajectory/ODE coverage;
- tensor-package Lean compilation;
- independent verification, comparator, provenance, admission, or registry promotion.

Admission remains **pending mathematical child**.
