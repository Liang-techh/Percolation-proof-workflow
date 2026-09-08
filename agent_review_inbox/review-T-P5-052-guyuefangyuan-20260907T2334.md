---
kind: review_result
review_id: review-T-P5-052-guyuefangyuan-20260907T2334
task_id: T-P5-052
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-07T23:20:00-06:00
created_at: 2026-09-07T23:34:00-06:00
claim_commit: d28cb4cf5f7381c7667b76747b7ae5f273137a0e
inspected_commit: c78cd5ef6e662b9b011b0b0bdd4ebefdcfefa73d
inspected_paths:
  - agent_review_inbox/review-T-P5-BRANCHFREE-AFFINE-MAJORANT-liuguanyi-20260907T2312.md
  - agent_review_inbox/companion-T-P5-BRANCHFREE-AFFINE-MAJORANT-liuguanyi-20260907T2315.md
  - agent_review_inbox/review-T-P5-051-honglianmozun-20260907T2250.md
continuation_of:
  - T-P5-BRANCHFREE-AFFINE-MAJORANT
  - T-P5-051
related_tasks:
  - T-P5-049
  - T-P5-050
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add an exact-rational correlated polynomial cell-certification layer above the branch-free affine-energy majorant; use Bernstein controls and exact dyadic subdivision on Rtr/Rdet directly; preserve negative-control and undecided branches; keep deployed source/Float64/coverage separate
---

# T-P5-052 — exact correlated Bernstein cell gate for the branch-free affine-energy remainder

## 0. Question and result

`T-P5-BRANCHFREE-AFFINE-MAJORANT` reduces the two-channel affine energy problem to two same-point polynomial inequalities.  With

```text
Q(x,y)=p*x^2 + sigma*x*y + s*y^2,
d=b4*x+b5*y,
kappa>0,
```

define

```text
Rtr  := 4*kappa*(p+s) - (b4^2+b5^2),
Rdet := kappa*(4*p*s-sigma^2)
        - (s*b4^2-sigma*b4*b5+p*b5^2).
```

If `Rtr>=0` and `Rdet>=0` at the same source point, then the branch-free completion theorem gives

```text
-Q(x,y)-d <= kappa
```

for every real `(x,y)`.

The explicit obstruction left by that review is that intervalizing `D4=4ps-sigma^2` and `Nsig` independently can destroy the cancellation in `Rdet=kappa*D4-Nsig` near a singular boundary.

This child gives a source-independent exact-rational remedy for a one-dimensional rational cell:

1. if `p,s,sigma,b4,b5` are affine in one cell parameter, then `Rtr` has degree at most 2 and `Rdet` degree at most 3;
2. a degree-2 or degree-3 polynomial is a convex combination of its Bernstein control coefficients on `[0,1]`;
3. therefore nonnegative Bernstein controls give a rigorous global lower bound without roots, eigenvalues, division by a determinant, or independent extrema;
4. exact dyadic de Casteljau subdivision preserves the polynomial and all coefficients remain rational;
5. repeated dyadic subdivision is complete for **strict positivity** of degree `<=3` polynomials: if `P>0` on the compact cell, sufficiently fine subdivision eventually makes every local Bernstein control strictly positive;
6. a negative Bernstein control alone is **not** a rejection certificate.  It means `SUBDIVIDE/UNDECIDED`; an exact rational point with `P<0` is a genuine obstruction.

This yields a practical fail-closed checker interface for the correlated `Rtr/Rdet` packet while preserving the cancellation identified by T-P5-BRANCHFREE-AFFINE-MAJORANT.

No deployed source polynomiality, Float64 enclosure, physical coverage, ODE result, Lean compile, or admission is claimed.

---

## 1. Why the two remainders are only quadratic/cubic for an affine source cell

Let `t in [0,1]`, and suppose only for this mathematical child that

```text
p(t)     = p0     + p1*t,
s(t)     = s0     + s1*t,
sigma(t) = g0     + g1*t,
b4(t)    = u0     + u1*t,
b5(t)    = v0     + v1*t,
```

with fixed `kappa`.

Then

```text
Rtr(t) = 4*kappa*(p(t)+s(t)) - b4(t)^2-b5(t)^2
```

has degree at most 2.

For `Rdet`, the curvature piece

```text
4*p(t)*s(t)-sigma(t)^2
```

has degree at most 2.  Each bias-curvature term

```text
s(t)*b4(t)^2,
sigma(t)*b4(t)*b5(t),
p(t)*b5(t)^2
```

has degree at most 3.  Hence

```text
deg Rdet <= 3.
```

So the exact correlated source gate is low degree even though it contains the cancellation that separate interval extrema lose.

This degree statement is only a mathematical adapter.  A deployed source cell may be trigonometric, rational, interval-generated, or Float64; it may instantiate this child only after an exact polynomial remainder representation or a separately proved polynomial enclosure has been supplied.

---

## 2. Quadratic Bernstein identity

Let

```text
P(t)=a0+a1*t+a2*t^2.
```

Define the exact Bernstein controls

```text
beta0 := a0,
beta1 := a0 + a1/2,
beta2 := a0 + a1 + a2.
```

Then the ring identity is

```text
P(t)
 = beta0*(1-t)^2
   + 2*beta1*t*(1-t)
   + beta2*t^2.                                           (2.1)
```

For `0<=t<=1`, the three weights

```text
(1-t)^2,
2*t*(1-t),
t^2
```

are nonnegative and sum to 1.  Therefore

```text
min(beta0,beta1,beta2) <= P(t) <= max(beta0,beta1,beta2). (2.2)
```

In particular,

```text
beta0>=0 and beta1>=0 and beta2>=0
  -> P(t)>=0 for all t in [0,1].                           (2.3)
```

If all three controls are at least a rational `delta`, then `P(t)>=delta` uniformly.

Nothing here uses a root formula or an extremum solver.

---

## 3. Cubic Bernstein identity

Let

```text
P(t)=c0+c1*t+c2*t^2+c3*t^3.
```

Define

```text
gamma0 := c0,
gamma1 := c0 + c1/3,
gamma2 := c0 + 2*c1/3 + c2/3,
gamma3 := c0 + c1 + c2 + c3.
```

Then

```text
P(t)
 = gamma0*(1-t)^3
   + 3*gamma1*t*(1-t)^2
   + 3*gamma2*t^2*(1-t)
   + gamma3*t^3.                                         (3.1)
```

Again the four Bernstein weights are nonnegative on `[0,1]` and sum to 1.  Thus

```text
min(gamma0,gamma1,gamma2,gamma3)
  <= P(t)
  <= max(gamma0,gamma1,gamma2,gamma3).                   (3.2)
```

Hence

```text
forall j, gamma_j>=0
  -> forall t in [0,1], P(t)>=0.                          (3.3)
```

and strict positive controls give a certified strict lower bound.

For implementation simplicity, the quadratic `Rtr` can also be treated as a cubic with `c3=0`; one trusted cubic control packet can therefore certify both `Rtr` and `Rdet`.

---

## 4. Arbitrary rational cell transport

Let the physical scalar cell be `[a,b]` with rational `a<=b`, and set

```text
t = a + (b-a)*u,
0<=u<=1.
```

If `P` has rational coefficients, then

```text
P_ab(u):=P(a+(b-a)u)
```

also has rational coefficients.  The previous identities apply verbatim to `P_ab`.

For a degree `<=3` polynomial there is an especially useful derivative form.  Let `h=b-a`.  The cubic Bernstein controls of `P(a+h*u)` are

```text
gamma0 = P(a),
gamma1 = P(a) + (h/3)*P'(a),
gamma2 = P(a) + (2h/3)*P'(a) + (h^2/6)*P''(a),
gamma3 = P(b).                                             (4.1)
```

This follows by Taylor expansion, which is exact for degree at most 3, followed by the monomial-to-Bernstein conversion in Section 3.

Equation (4.1) is useful for the termination argument below and can also serve as an independent exact checker of a generated control vector.

---

## 5. Exact dyadic de Casteljau subdivision

A cell whose controls are not all nonnegative should not immediately be rejected.  Split it exactly at the midpoint and reuse the same polynomial.

### 5.1 Quadratic

For controls

```text
(b0,b1,b2),
```

the left-half controls are

```text
L0 = b0,
L1 = (b0+b1)/2,
L2 = (b0+2*b1+b2)/4,
```

and the right-half controls are

```text
R0 = (b0+2*b1+b2)/4,
R1 = (b1+b2)/2,
R2 = b2.                                                   (5.1)
```

### 5.2 Cubic

For controls

```text
(g0,g1,g2,g3),
```

the left-half controls are

```text
L0 = g0,
L1 = (g0+g1)/2,
L2 = (g0+2*g1+g2)/4,
L3 = (g0+3*g1+3*g2+g3)/8,
```

and the right-half controls are

```text
R0 = (g0+3*g1+3*g2+g3)/8,
R1 = (g1+2*g2+g3)/4,
R2 = (g2+g3)/2,
R3 = g3.                                                   (5.2)
```

These are exact de Casteljau identities at parameter `1/2`.  Starting from rational controls, every descendant control remains rational.

Thus a source checker can recursively refine a cell using only integer/rational addition and division by powers of two.  There is no root isolation and no floating optimization in the trusted arithmetic path.

---

## 6. Completeness for strict positivity

The Bernstein test is sufficient on one cell, but repeated subdivision gives a stronger theorem.

### Theorem

Let `P` be a real polynomial of degree at most 3.  If

```text
P(t) > 0 for every t in [0,1],
```

then there exists an integer `N` such that after splitting `[0,1]` into all `2^N` dyadic subcells, **every cubic Bernstein control on every subcell is strictly positive**.

Therefore an exact adaptive dyadic Bernstein checker is a complete semidecision procedure for strict positivity of degree `<=3` rational polynomials: whenever a strict positive margin exists, refinement eventually produces a finite rational certificate.

### Proof

Because `P` is continuous and `[0,1]` is compact, there exists

```text
delta := min_[0,1] P > 0.
```

Let

```text
M1 := max_[0,1] |P'|,
M2 := max_[0,1] |P''|.
```

Consider any subcell `[a,a+h]`.  By (4.1), its two interior cubic controls differ from `P(a)` by at most

```text
|gamma1-P(a)| <= h*M1/3,

|gamma2-P(a)| <= 2*h*M1/3 + h^2*M2/6.                     (6.1)
```

The endpoint controls are `P(a)>=delta` and `P(a+h)>=delta`.

Choose `h>0` small enough that both right sides in (6.1) are `<delta`.  Then all four controls are strictly positive on every subcell of width at most `h`.

Finally choose `N` with `2^(-N)<=h`.  Every level-`N` dyadic subcell has positive controls.

No statement of completeness is made for merely nonnegative polynomials with zero minima.  Some such cases terminate immediately (for example the identically-zero remainder), while a generic nonnegative polynomial touching zero may need a separate exact-zero/factor argument.

---

## 7. The original singular-boundary cancellation now passes exactly

T-P5-BRANCHFREE-AFFINE-MAJORANT gave the family

```text
p(t)=t^2,
s(t)=1,
sigma(t)=0,
b4(t)=2*t,
b5(t)=0,
kappa=1.
```

It has

```text
Rtr(t)=4,
Rdet(t)=0
```

identically on `[0,1]`.

The Bernstein packets are therefore simply

```text
Rtr:  (4,4,4,4),
Rdet: (0,0,0,0).
```

Both gates pass in one exact step, including the singular endpoint `t=0`.

This directly fixes the false negative produced by the independent-extrema test

```text
D4_lower=0,
Nsig_upper=4.
```

The relevant cancellation is preserved because the checker certifies `Rdet` itself.

---

## 8. Endpoint-only checking is unsound

A correlated polynomial gate cannot be certified from endpoints alone.

Take

```text
P(t)=1-5*t+5*t^2.
```

Then

```text
P(0)=1,
P(1)=1,
```

but

```text
P(1/2)=-1/4 < 0.
```

Its quadratic Bernstein controls are

```text
(1, -3/2, 1).
```

Thus the control packet immediately exposes interior danger that endpoint positivity misses.

This gives a useful regression test for any future source-cell implementation: a checker that accepts this polynomial from endpoint values alone is unsound.

---

## 9. A negative Bernstein control is not itself a counterexample

The convex-hull property is one-way for lower certification:

```text
all controls >=0  -> P>=0.
```

The converse on a fixed coarse cell is false.  Therefore the correct fail-closed states are:

```text
ALL_CONTROLS_NONNEGATIVE
    -> CERTIFIED on this cell;

EXACT_RATIONAL_POINT_WITH_P_NEGATIVE
    -> REJECTED / mathematical obstruction;

otherwise
    -> SUBDIVIDE or UNDECIDED.
```

This distinction matters for near-singular source cells.  Coarse Bernstein controls can be pessimistic even when the joint polynomial remains positive; exact subdivision is the mathematically legitimate way to recover the cancellation.

---

## 10. Source-facing finite-cell theorem

Let a finite collection of rational cells cover a declared one-dimensional parameter domain.  On each cell `C_j`, suppose exact polynomial representatives

```text
Rtr_j(u), Rdet_j(u),  0<=u<=1
```

are supplied and are definitionally/equationally bound to the same signed source coefficients and the same fixed `kappa>0`.

If every cell has Bernstein controls satisfying

```text
controls(Rtr_j)  >= 0 componentwise,
controls(Rdet_j) >= 0 componentwise,
```

then for every source point in the covered union and every real `(x,y)`,

```text
-Q(x,y)-b4*x-b5*y <= kappa.                              (10.1)
```

This is exactly the input needed by the branch-free affine-energy majorant.  The finite-cell layer does not need to classify positive-definite versus singular PSD branches.

If a downstream first-exit consumer has total budget `K` and needs strict reserve `m>0`, freeze

```text
kappa = K-m,
0<m<K,
```

**before** generating the two polynomial remainder certificates.  Then (10.1) gives

```text
J <= K-m < K.
```

Positive Bernstein slack at `kappa=K` must not silently be converted into an energy reserve without separately controlling how `Rtr/Rdet` vary with `kappa`.

---

## 11. Recommended exact checker algorithm

For each same-key source cell:

```text
1. Form signed sigma before any entrywise absolute-value operation.
2. Construct Rtr and Rdet as joint exact polynomials.
3. Affinely map the rational cell to u in [0,1].
4. Convert each remainder to a cubic Bernstein packet.
5. If every control of both packets is >=0, certify the cell.
6. Otherwise evaluate exact rational dyadic points already exposed by subdivision.
   If either remainder is <0 at one such point, return a mathematical obstruction.
7. Otherwise de Casteljau-split the unresolved cell and repeat.
```

For a strict-positive polynomial, Section 6 guarantees eventual success.  For a zero-touching polynomial, the checker may need an exact factor/identity child; lack of termination at a chosen depth is `UNDECIDED`, never `FAIL`.

The algorithm should preserve the full correlated expression.  It must not replace

```text
Rdet = kappa*(4ps-sigma^2)
       -(s*b4^2-sigma*b4*b5+p*b5^2)
```

by an independently lower-bounded first parenthesis and independently upper-bounded second parenthesis unless explicitly entering the older conservative fallback lane.

---

## 12. Suggested minimal Lean theorem decomposition

The trusted formal core can remain elementary.

### Ring identities

```text
quad_bernstein_identity
```

Statement shape:

```text
P t = beta0*(1-t)^2 + 2*beta1*t*(1-t) + beta2*t^2
```

under the definitions in Section 2.

```text
cubic_bernstein_identity
```

with the four controls from Section 3.

### Convex lower-bound consumers

```text
quad_nonneg_of_bernstein_coeff_nonneg
cubic_nonneg_of_bernstein_coeff_nonneg
```

These need only `0<=t`, `t<=1` and componentwise control nonnegativity.

A stronger reusable statement is

```text
bernstein_min_le_cubic
```

which consumes a common lower bound `delta<=gamma_j` and returns `delta<=P(t)`.

### Exact subdivision

```text
quad_decasteljau_half
cubic_decasteljau_half
```

stating equality between the parent polynomial restricted to each half-cell and the child control packets from (5.1)/(5.2).

### Branch-free P5 consumer

```text
affine_majorant_cell_of_bernstein_remainders_nonneg
```

Suggested premise surface:

```text
0 < kappa
Rtr polynomial identity on the cell
Rdet polynomial identity on the cell
all Rtr Bernstein controls >= 0
all Rdet Bernstein controls >= 0
```

Conclusion:

```text
forall cell_parameter x y,
  -Q - (b4*x+b5*y) <= kappa.
```

This theorem should call the already-formalized branch-free two-gate consumer rather than duplicate the 2x2 completion proof.

### Optional analysis theorem

```text
eventually_positive_cubic_bernstein_under_dyadic_subdivision
```

This is useful for checker completeness documentation but is not required in the smallest trusted execution path: every successful finite subdivision certificate is already independently checkable by the ring/nonnegativity lemmas.

---

## 13. Assumptions and boundaries

This child assumes only the exact polynomial cell representation presented to it.  It does **not** establish that the deployed system provides such a representation.

Still open:

- source-side signed `p,s,sigma,b4,b5` extraction;
- proof that any affine/polynomial model equals or encloses the deployed true-DH/FD/controller/solve remainder on the same cell;
- Float64 argument formation, libm and finite-DAG rounding semantics;
- multidimensional parameter/state coverage and a certified projection to the one-dimensional cell parameter;
- centered-to-full residual / anchor-bias binding;
- first-exit / ODE continuation / P8 flowpipe;
- pinned Lean compilation and independent validation;
- comparator/provenance/admission and P5/P8/M4 closure.

A negative Bernstein control is not to be recorded as a source obstruction unless accompanied by an exact negative point or another necessity proof.

Admission remains **pending mathematical child**.

---

## 14. Recommended next mathematical action

The source lane should not search for roots of `D4` or independently optimize `D4` and `Nsig`.  Instead, on the smallest cell for which signed coefficient formulas are available, construct the same-key exact `Rtr/Rdet` expression and determine whether it is genuinely polynomial of degree `<=3` after a rational cell coordinate change.

- If yes, this child gives an exact finite certificate path.
- If it is trigonometric but has an exact polynomial enclosure remainder, apply the child to that joint enclosure.
- If deployed Float64 destroys exact polynomiality, keep this theorem above a separately proved evaluator enclosure; do not fold IEEE semantics into the Bernstein algebra.

This is the smallest route that preserves the new branch-free cancellation while remaining compatible with a later Lean checker.
