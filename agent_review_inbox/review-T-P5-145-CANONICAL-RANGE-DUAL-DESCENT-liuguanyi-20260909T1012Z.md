---
kind: review_result
review_id: review-T-P5-145-canonical-range-dual-descent-liuguanyi-20260909T1012Z
task_id: T-P5-145-CANONICAL-RANGE-DUAL-DESCENT
reviewer: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T10:12:00Z
claim_commit: a4c12e10f7e78dcfcfa5826350cdf5c3ba440178
inspected_commit: 39889bbfd45bbc9bd541a7a8c51f0005a60b0881
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-143-ROOT-FREE-SINGULAR-BOUNDARY-CANONICALIZATION-kuangmanmozun-20260909T0942Z.md
    commit: 9d748de3be2b2cec2602ac9a96f90a5867cff405
  - path: agent_review_inbox/review-T-P5-144-SEMIDEFINITE-CELL-NULLSPACE-ELIMINATION-honglianmozun-20260909T1003Z.md
    commit: 39889bbfd45bbc9bd541a7a8c51f0005a60b0881
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: allow_a_basis_free_canonical_boundary_packet_Ky_eq_b_and_Kw_eq_Gy_when_G_is_positive_definite; use_bTw_as_the_intrinsic_canonical_G_energy; when_bTw_gt_4R_use_the_polynomial_dual_step_gate_4_d2_U_s_le_h2_to_certify_a_strict_right_multiplier_descent_without_a_kernel_basis_or_shifted_solve; keep_semidefinite_G_on_T-P5-144_and_keep_inexact_dual_solves_fail_closed
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional quadratic-form algebra only
exit_code: n/a
---

# T-P5-145 — basis-free canonical range-dual certificate and root-free singular-boundary descent

## 0. Narrow seam and non-overlap

T-P5-143 solves the singular shifted-curvature boundary for a positive-definite physical cell metric `G>0`. Its canonical boundary range solve is characterized by

`K y_c = b`,

`y_c \perp_G ker K`,

and a rational construction is given from an explicit basis of `ker K`.

That is mathematically complete, but it leaves a source-to-math interface seam: a producer may have exact linear-system solves while not exposing a stable nullspace basis. In that situation the theorem should not force an eigenspace, SVD, pseudoinverse, or explicit kernel projector into the trusted packet.

This child gives an equivalent basis-free certificate using a second ordinary range solve,

`K y = b`,

`K w = G y`.

The same `w` then yields a polynomial, square-root-free small-step descent gate in the branch `Q_G(y)>4R`. This directly strengthens the T-P5-143 fallback that otherwise requires a restricted-coercivity small-step argument or a shifted secant solve.

This task is disjoint from T-P5-144: throughout the main theorem here **`G` remains positive definite**. T-P5-144 handles singular physical-cell metrics and quotient/nullspace elimination before multiplier theory.

No source binding, coverage, Float64/controller semantics, provenance/admission, Lean/kernel receipt, registry promotion, or P5 parent closure is attempted.

---

## 1. Setup

Work in a finite-dimensional real vector space with symmetric matrices

`G > 0`,

`K >= 0`.

`K` may be singular. Let

`b in range(K)`.

For the multiplier interpretation, one may write

`K = H + tau_0 G`,

with `tau_0 >= 0`, and consider

`f(x) = C + b^T x - x^T H x`

on the physical ellipsoid

`Q_G(x) := x^T G x <= R`, `R>=0`.

The fixed-multiplier sharp floor at `tau_0` is

`E_0 = C + tau_0 R + q_0/4`,

where `q_0=b^T y` for any solution of `K y=b`; this scalar is solution-independent because `b` is orthogonal to `ker K`.

T-P5-143 distinguishes the unique canonical solution by `G`-orthogonality to `ker K`. The first result below removes the need to name that kernel in the producer packet.

---

## 2. Basis-free canonicality by a range-dual witness

### Theorem A — canonical range solve iff `G y` is itself in the range of `K`

Suppose `K` is symmetric PSD and `G` is symmetric PD. For a vector `y` satisfying

**(2.1)** `K y = b`,

the following are equivalent:

1. `y` is the T-P5-143 canonical representative,

   **(2.2)** `n^T G y = 0` for every `n in ker K`;

2. `G y` lies in `range K`;

3. there exists a vector `w` such that

   **(2.3)** `K w = G y`.

### Proof

For a symmetric finite-dimensional matrix,

`range K = (ker K)^perp`

with respect to the ordinary Euclidean pairing. Thus

`G y in range K`

is equivalent to

`n^T G y = 0` for every `n in ker K`.

The equivalence between (2) and (3) is exactly the definition of range membership.

No kernel basis is needed in the theorem statement or checker packet.

---

### Theorem B — the primal canonical solution is unique

If `(y,w)` and `(y',w')` satisfy

`K y=b`, `K w=G y`,

`K y'=b`, `K w'=G y'`,

then

**(2.4)** `y=y'`.

### Proof

Let `d=y'-y`. Then `K d=0`, so `d in ker K`. Also

`G d = K(w'-w)`.

Therefore

`d^T G d = d^T K(w'-w)=0`.

Since `G>0`, `d=0`.

The dual witness `w` need not be unique: one may add a null vector of `K`. This does not affect correctness below.

---

## 3. Intrinsic scalar from the dual witness

Let `(y,w)` satisfy the basis-free packet

**(3.1)** `K y=b`,

**(3.2)** `K w=G y`.

Define

**(3.3)** `s := Q_G(y)=y^T G y`.

Then

**(3.4)** `s = b^T w`.

Indeed,

`b^T w = (K y)^T w = y^T K w = y^T G y`.

Thus the T-P5-143 canonical boundary gate

`Q_G(y)<=4R`

can equivalently be checked as

**(3.5)** `b^T w <= 4R`.

This is useful when the source already exposes exact linear solves and signed dot products but not a kernel basis or a projected norm.

The scalar `b^T w` is independent of the choice of dual witness. If `w'=w+n` with `n in ker K`, then

`b^T n = y^T K n = 0`.

For later use define the non-intrinsic but safe dual energy

**(3.6)** `U := Q_G(w)=w^T G w >=0`.

`U` can increase if a nullspace translate is added to `w`; this only makes the later descent gate more conservative. Correctness does not require canonicalizing `w`.

---

## 4. Shifted positive-definite solve and exact signed identities

For any real `d>0`, define

**(4.1)** `K_d := K + d G`.

Because `K>=0` and `G>0`,

**(4.2)** `K_d > 0`.

Hence there is a unique exact vector `y_d` satisfying

**(4.3)** `K_d y_d=b`.

Set

**(4.4)** `e_d := y-y_d`,

**(4.5)** `c_d := y^T G y_d`,

**(4.6)** `t_d := w^T G y_d`.

Subtracting the two range equations gives the exact defect identity

**(4.7)** `K e_d = d G y_d`.

### Lemma C — the shifted solve stays in the old canonical complement

For every `n in ker K`,

**(4.8)** `n^T G y_d=0`.

Proof:

`0=n^T b=n^T(K+dG)y_d=d n^T G y_d`,

and `d>0`.

Consequently `t_d` is independent of which dual witness `w` is used: changing `w` by `n in ker K` changes `w^T G y_d` by zero.

---

### Lemma D — exact cross-energy sandwich without inverses

One has

**(4.9)** `Q_G(y_d) <= c_d <= s`.

Proof of the lower inequality:

`c_d-Q_G(y_d)`

` = e_d^T G y_d`

` = (1/d) e_d^T K e_d >=0`

by (4.7) and `K>=0`.

Proof of the upper inequality:

`s-c_d`

` = y^T G e_d`

` = (y_d+e_d)^T G e_d`

` = (1/d)e_d^T K e_d + Q_G(e_d) >=0`.

This recovers the relevant T-P5-143 cross sandwich using only the primal defect equation.

---

### Lemma E — dual secant identity

The gap from the canonical boundary norm to the shifted cross metric is

**(4.10)** `s-c_d = d t_d`.

Proof:

`s-c_d = y^T G e_d`

`         = (G y)^T e_d`

`         = (K w)^T e_d`

`         = w^T K e_d`

`         = d w^T G y_d`

`         = d t_d`.

By Lemma D,

**(4.11)** `t_d>=0`.

This is a signed identity. Do not enclosure `s`, `c_d`, and `t_d` separately before forming it.

---

## 5. Exact second-order multiplier-floor expansion

Let

`q_0:=b^T y`,

`q_d:=b^T y_d`.

Then

`q_0-q_d`

` = b^T e_d`

` = y^T K e_d`

` = d y^T G y_d`

` = d c_d`.

Using `c_d=s-dt_d` from Lemma E gives

### Theorem F — exact dual second-order expansion

**(5.1)** `q_d = q_0 - d s + d^2 t_d`.

For the sharp fixed-multiplier floors

`E_0 = C + tau_0 R + q_0/4`,

`E_d = C + (tau_0+d)R + q_d/4`,

one gets the exact identity

**(5.2)**

`4(E_d-E_0)`

` = d(4R-s) + d^2 t_d`.

No derivative, inverse, pseudoinverse, square root, or eigenvalue is involved.

This identity cleanly separates the first-order boundary stationarity scalar `4R-s` from a nonnegative second-order correction.

### Immediate boundary-optimality recovery

If

**(5.3)** `s<=4R`,

then both terms in (5.2) are nonnegative, so

**(5.4)** `E_d>=E_0` for every `d>0`.

Thus the basis-free dual packet recovers the T-P5-143 canonical boundary-optimality theorem directly.

---

## 6. Root-free bound on the second-order term

By the `G`-Cauchy inequality,

`t_d^2 <= Q_G(w) Q_G(y_d)`.

With Lemma D,

`Q_G(y_d)<=s`.

Therefore

### Theorem G — dual second-order enclosure

**(6.1)** `0 <= t_d^2 <= U s`,

where `U=Q_G(w)`.

Equivalently, a checker can keep the entirely polynomial statement

**(6.2)** `t_d>=0`, `t_d^2<=Us`.

No `sqrt(Us)` needs to be materialized.

If the producer chooses a more canonical/smaller-energy dual witness `w`, the gate below becomes sharper, but any exact witness is sound.

---

## 7. Main new bridge: explicit rational descent when `s>4R`

Assume now the singular boundary fails the T-P5-143 optimality gate:

**(7.1)** `s>4R`.

Define the positive gap

**(7.2)** `h := s-4R >0`.

Then (5.2) becomes

**(7.3)** `4(E_d-E_0)=d(-h+d t_d)`.

T-P5-143 already proves that this branch should move to the right, but its generic fallback requires either a restricted-coercivity small-step argument or an actual shifted secant solve. The dual witness gives a cheaper exact polynomial gate.

### Theorem H — qualitative root-free descent gate

If a proposed `d>0` satisfies

**(7.4)** `d^2 U s < h^2`,

then

**(7.5)** `E_d<E_0`.

Proof: from (6.1), `(d t_d)^2<=d^2Us<h^2`. Since `d,t_d,h>=0`, this implies `d t_d<h`. Insert in (7.3).

The checker never needs to extract a square root; it only compares two nonnegative squares.

---

### Theorem I — quantitative division-free descent reserve

A convenient stronger non-strict gate is

**(7.6)** `4 d^2 U s <= h^2`.

Then

**(7.7)** `2 d t_d <= h`,

and hence

**(7.8)** `E_d <= E_0 - d h / 8`.

A division-free form of the conclusion is

**(7.9)** `8 E_d + d h <= 8 E_0`.

Proof: (6.1) and (7.6) give

`(2dt_d)^2 <= h^2`.

All quantities are nonnegative, so `2dt_d<=h`. Then

`4(E_d-E_0)`

`=d(-h+dt_d)`

`<=-d h/2`.

Multiply by two to get (7.9).

This is a genuine improvement over merely proving that the boundary is not optimal: the same exact packet gives a certified amount of floor decrease.

---

## 8. A fully rational proposed step always exists

Suppose the trusted/source-independent packet is rational, so `h,U,s` are rational with `h>0`, `U,s>=0`. A producer may simply propose any positive rational `d` and let the checker verify (7.6).

If a deterministic rational proposal is desired, one possible choice is

**(8.1)** `d_* := h / [2(1+Us)]`.

Its denominator is positive. Put `x:=Us>=0`. Then

`4 d_*^2 U s`

`= h^2 x/(1+x)^2`.

The elementary identity

`(1+x)^2-4x=(x-1)^2>=0`

shows

**(8.2)** `4 d_*^2 U s <= h^2/4 <= h^2`.

Thus (7.6) holds. The trusted theorem need not compute the quotient in (8.1): the producer can emit a rational `d_*`, and the checker can verify the exact relation

`2(1+Us)d_*=h`

plus the polynomial gate.

So the branch `s>4R` never needs an irrational multiplier shift merely because the boundary curvature is singular.

---

## 9. Exact rational regression

Take

`G=I_2`,

`K=diag(0,1)`,

`b=(0,2)^T`,

`R=1/2`, `tau_0=0`, `C=0`.

The solve class of `K y=b` is

`y=(a,2)`.

The basis-free dual condition `K w=G y` is solvable iff `a=0`, so it selects the canonical solution without naming `ker K`:

`y=(0,2)`.

Choose `w=(0,2)`. Then

`s=Q_G(y)=4=b^T w`,

`U=Q_G(w)=4`,

`4R=2`,

`h=2`.

Choose

`d=1/8`.

The polynomial gate gives

`4 d^2 U s = 1 <= 4 = h^2`.

The shifted solve is

`y_d=(0,16/9)`,

so

`q_0=4`, `q_d=32/9`,

and

`E_0=1`,

`E_d=(1/8)(1/2)+(32/9)/4 = 137/144`.

Indeed

`137/144 < 1`.

The quantitative theorem predicts

`E_d <= E_0-dh/8 = 31/32`,

and

`137/144 <= 31/32`.

If instead one chooses a noncanonical dual witness `w=(c,2)`, the equation `K w=Gy` still holds and `s=b^T w=4` remains intrinsic, while `U=c^2+4` grows. The descent gate becomes more conservative but remains sound. This cleanly separates the unique primal canonical state from the optional dual-witness conditioning choice.

---

## 10. Minimal theorem statements for formalization

The mathematical core can be split into small finite-dimensional lemmas.

### Lemma 1 — range-dual canonicality

Assumptions:

- `K=K^T`, `K>=0`;
- `G=G^T`, `G>0`;
- `K y=b`;
- `K w=G y`.

Conclusion:

`forall n, K n=0 -> n^T G y=0`.

A converse existence lemma may state that `K y=b` plus this orthogonality implies `exists w, K w=G y`.

### Lemma 2 — canonical uniqueness

Two primal vectors admitting the packet above for the same `K,G,b` are equal.

### Lemma 3 — intrinsic dual energy

`K y=b`, `K w=Gy` imply

`b^T w = y^T G y`.

### Lemma 4 — shifted defect/cross sandwich

For `d>0`, `K_d=K+dG`, `K_d y_d=b`, `e=y-y_d`, prove

`K e=dGy_d`,

`Q_G(y_d)<=y^TGy_d<=Q_G(y)`.

### Lemma 5 — dual secant

With `s=y^TGy`, `t=w^TGy_d`, prove

`s-y^TGy_d=d t`, `t>=0`.

### Lemma 6 — floor expansion

For `q_0=b^Ty`, `q_d=b^Ty_d`, prove

`q_d=q_0-ds+d^2t`,

and therefore

`4(E_d-E_0)=d(4R-s)+d^2t`.

### Lemma 7 — polynomial descent

With `U=w^TGw`, `h=s-4R>0`, if

`4 d^2 U s <= h^2`,

then

`8E_d+d h<=8E_0`.

This final statement is ordered-field/quadratic-form algebra plus the `G`-Cauchy inequality. It does not require a matrix inverse, kernel basis, square root, eigenvalue, or pseudoinverse.

---

## 11. Suggested typed producer/checker interface

For the positive-definite physical-metric singular-boundary lane, a source-independent packet may be:

```text
CanonicalRangeDualPacket
  resetKey / cellKey / multiplierKey
  G : symmetric PD physical-cell metric
  K : symmetric PSD shifted curvature
  b : affine reset covector
  y : primal exact range solve
  w : dual exact range solve
  witness_primal : K y = b
  witness_dual   : K w = G y
  s : rational scalar with s = b^T w
  U : rational upper bound with Q_G(w) <= U
```

For boundary acceptance:

```text
s <= 4R
```

is enough.

For a certified right-step when `s>4R`, add

```text
h = s-4R > 0
d > 0
4 d^2 U s <= h^2
```

and conclude the exact sharp-floor reserve

```text
8 E(tau_0+d) + d h <= 8 E(tau_0).
```

If `U` is supplied as an upper bound rather than exact `Q_G(w)`, the proof remains valid after first checking `Q_G(w)<=U`.

This packet is especially suitable when the producer already has exact/rational linear solves but no nullspace basis.

---

## 12. Hard boundaries that remain open

This review does **not** close the following.

1. **Semidefinite physical metric.** If `G` is singular, Theorem A no longer gives uniqueness from `d^TGd=0`; use T-P5-144's nullspace elimination first.
2. **Inexact dual solve.** If only `K w approximately G y` is available, the exact canonicality and descent identities above acquire signed residual terms. Do not silently reuse this theorem; that requires a separate residual bridge.
3. **Inexact primal solve.** T-P5-141/T-P5-142 remain the correct lane for `K y approximately b`.
4. **Source identity.** Actual deployed `K,G,b,y,w,R,tau_0` still need same-key source binding.
5. **Coverage/domain semantics.** This is finite-dimensional reset algebra, not whole-cell/path/flowpipe coverage.
6. **Floating-point/runtime equivalence.** No statement is made about a runtime solver or Float64 residual.
7. **Lean/kernel/admission.** No compile, `#print axioms`, independent validation, receipt, or registry promotion is claimed.

The main new closure is therefore narrow and explicit: **an exact range-dual solve replaces the nullspace-basis interface and simultaneously supplies a rational polynomial descent certificate for the `s>4R` singular-boundary branch.**
