---
kind: review_result
review_id: review-T-P5-143-root-free-singular-boundary-canonicalization-kuangmanmozun-20260909T0942Z
task_id: T-P5-143-SINGULAR-BOUNDARY-CANONICAL-SOLVE
reviewer: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T09:42:00Z
claim_commit: cc7fcbc676c154e7d6d924cda8b53e0a5489571d
inspected_commit: 482a5704b04cdc0947c69d55d728bd6927b37718
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-139-RANGE-SOLVE-SCHUR-RESET-kuangmanmozun-20260909T0834Z.md
    commit: f0198916eb5fe1783cbeb9055031c9d9bd0dc954
  - path: agent_review_inbox/review-T-P5-140-MULTIPLIER-SECANT-OPTIMIZATION-honglianmozun-20260909T0908Z.md
    commit: 6d4275c964d8f3481f87e8546d7bec8b020651c0
  - path: agent_review_inbox/review-T-P5-142-ROBUST-INEXACT-MULTIPLIER-BRACKET-guyuefangyuan-20260909T0931Z.md
    commit: 3e81bac2fe47fc97a041b32f311162d53ee5fdb7
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: replace_arbitrary_singular_range_solve_norm_by_the_canonical_G_orthogonal_representative; use_s_can_le_4R_as_the_intrinsic_boundary_optimality_gate; if_s_can_gt_4R_use_the_restricted_coercivity_small_step_descent_or_existing_exact_secant_search; do_not_require_an_explicit_irrational_nullspace_contact_vector_for_root_free_source_packets
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional quadratic-form algebra only
exit_code: n/a
---

# T-P5-143 — root-free canonicalization of the singular multiplier boundary

## 0. Narrow seam and non-overlap

T-P5-139 gives the exact fixed-multiplier Schur floor from a range solve

`K_tau y = b`,

T-P5-140 gives exact multiplier secants and global optimization, and T-P5-142
shows how inexact solves can still bracket the true intrinsic floor.

T-P5-140 deliberately leaves one singular-boundary point fail-closed: if the
left feasible shifted curvature `K_0` is singular, the affine solve class

`{ y : K_0 y = b }`

contains nullspace translates.  The scalar `b^T y` is intrinsic, but the
same-point metric norm `y^T G y` is not.  Hence finding one singular solve with
`y^T G y > 4R` says nothing by itself about whether the boundary multiplier is
optimal.

This child closes exactly that ambiguity.  The main observation is that the
solve class contains one distinguished representative: the unique solution
that is `G`-orthogonal to `ker K_0`.  It is simultaneously

1. the minimum-`G`-energy range solve;
2. rational whenever the matrix data and a rational kernel basis are rational;
3. the correct right-boundary stationarity datum;
4. sufficient to decide the singular hard-case branch without choosing an
   arbitrary nullspace representative;
5. enough to prove existence of the physical hard-case contact without putting
   an irrational square root into the trusted source packet.

No source binding, runtime semantics, provenance/admission audit, Lean compile,
P8 coverage, or parent closure is attempted here.

---

## 1. Setup

Work in a finite-dimensional real vector space.  Let

- `G` be symmetric positive definite;
- `K_0` be symmetric positive semidefinite and singular;
- `b` lie in `range(K_0)`;
- `N := ker(K_0)`, so `N != {0}`;
- `R >= 0`;
- `tau_0 >= 0`;
- `H := K_0 - tau_0 G`;
- `C` be the constant reset term.

The physical quadratic reset envelope is

`f(x) := b^T x - x^T H x + C`

on the ellipsoid

`x^T G x <= R`.

For every solution `y` of `K_0 y=b`, the intrinsic boundary multiplier floor is

`E_0 := C + tau_0 R + (b^T y)/4`.

The value `b^T y` is independent of the chosen solution because two solutions
differ by `n in N` and

`b^T n = y^T K_0 n = 0`.

The problem is only the nonintrinsic quantity `y^T G y`.

Write

`B_G(u,v) := u^T G v`,

`Q_G(u) := u^T G u`.

---

## 2. Canonical singular range solve

### Theorem A — existence and uniqueness of the canonical representative

There exists a unique vector `y_c` satisfying

**(2.1)** `K_0 y_c = b`,

and

**(2.2)** `B_G(y_c,n)=0` for every `n in N`.

Equivalently, `y_c` is the unique element of the affine solve class that lies
in the `G`-orthogonal complement

`M := N^{perp_G}`.

### Proof

Choose any solve `y_0` of `K_0 y_0=b`.  The complete solve class is

`y_0+N`.

Because `G>0`, its restriction to `N` is an inner product.  Decompose `y_0`
uniquely as

`y_0 = y_c + p`,

with

`p in N`, `y_c in N^{perp_G}`.

Since `K_0 p=0`,

`K_0 y_c = K_0 y_0=b`.

For uniqueness, if `y_c'` is another solution satisfying (2.2), then

`d:=y_c'-y_c in N`.

But both representatives are `G`-orthogonal to `N`, so

`Q_G(d)=B_G(d,d)=0`.

Positive definiteness of `G` gives `d=0`.

---

## 3. Exact Pythagorean identity and intrinsic minimum

### Theorem B — minimum-`G`-energy range solve

For every solution `y` of `K_0 y=b`, set

`n:=y-y_c`.

Then `n in N` and

**(3.1)** `Q_G(y) = Q_G(y_c) + Q_G(n)`.

Hence, with

**(3.2)** `s_c := Q_G(y_c)`,

one has

**(3.3)** `Q_G(y) >= s_c`

for every boundary range solve, with equality iff `y=y_c`.

### Proof

Expand

`Q_G(y_c+n)=Q_G(y_c)+2B_G(y_c,n)+Q_G(n)`.

The middle term vanishes by (2.2).

### Consequence

The statement

> there exists a singular range solve with `Q_G(y)<=4R`

is equivalent to the intrinsic scalar condition

**(3.4)** `s_c <= 4R`.

Thus the singular boundary no longer needs an arbitrary choice of range-solve
representative.

---

## 4. Rational, root-free construction from a kernel basis

The canonical solve does not require a square root, pseudoinverse, or spectral
basis in the producer packet.

Let the columns of a matrix `Z` form a basis of `N`.  Start from any exact solve

`K_0 y_0=b`.

Define the nullspace Gram matrix

**(4.1)** `M_N := Z^T G Z`.

Because `G>0` and the columns of `Z` are independent, `M_N>0`.

Let `alpha` solve the ordinary finite-dimensional system

**(4.2)** `M_N alpha = Z^T G y_0`.

Set

**(4.3)** `y_c := y_0 - Z alpha`.

Then

`K_0 y_c=b`

because `K_0 Z=0`, and

`Z^T G y_c = Z^T G y_0-M_N alpha=0`.

Since the columns of `Z` span the whole nullspace, this is exactly (2.2).

### Rationality corollary

If `K_0,G,b,y_0,Z` are rational, then `M_N` and the right side of (4.2) are
rational.  The unique solution `alpha` is rational, hence so is `y_c` and the
canonical scalar

`s_c=y_c^T G y_c`.

Therefore the singular-boundary decision below can be driven by exact rational
linear solves and scalar comparisons.  The theorem statement never needs
`G^{1/2}`, a Moore-Penrose inverse, or an eigenvector normalization.

---

## 5. Every interior shifted solve automatically uses the same complement

For `d>0`, define

**(5.1)** `K_d := K_0+dG`.

Because `K_0>=0` and `G>0`, one has `K_d>0`, so there is a unique exact solve

**(5.2)** `K_d y_d=b`.

### Lemma C — interior solve is `G`-orthogonal to the old nullspace

For every `n in N`,

**(5.3)** `B_G(n,y_d)=0`.

Hence

**(5.4)** `y_d in M=N^{perp_G}`.

### Proof

Since `b=K_0 y_c` and `K_0 n=0`, symmetry gives

`n^T b=0`.

On the other hand,

`0=n^T b=n^T K_d y_d`

` = n^T K_0 y_d + d n^T G y_d`

` = d B_G(n,y_d)`.

Because `d>0`, (5.3) follows.

This fact is useful: the interior branch chooses the same canonical complement
automatically.  The apparent singular same-point ambiguity exists only at the
boundary itself.

---

## 6. Canonical boundary optimality is an exact rational gate

Define

`q_0:=b^T y_c`.

For `d>0`, let

`q_d:=b^T y_d`,

`c_d:=B_G(y_c,y_d)`.

T-P5-140's exact secant identity gives

**(6.1)** `q_0-q_d=d c_d`,

and therefore

**(6.2)**

`4(E_d-E_0)=d(4R-c_d)`,

where

`E_d:=C+(tau_0+d)R+q_d/4`.

The cross-metric sandwich at the pair `(K_0,K_d)` gives

**(6.3)** `Q_G(y_d) <= c_d <= s_c`.

### Theorem D — canonical singular-boundary optimality

If

**(6.4)** `s_c <= 4R`,

then for every `d>0`,

**(6.5)** `E_d >= E_0`.

Thus `tau_0` is globally optimal on the feasible multiplier ray
`[tau_0,infinity)`.

### Proof

By (6.3), `c_d<=s_c<=4R`.  Insert this into (6.2).

### Why this is stronger than the old singular rule

T-P5-140 allowed any particular singular solve with norm `<=4R` as a sufficient
boundary witness.  Theorem B now says there is one intrinsic scalar to check:
`s_c`.  If it passes, the boundary is certified; if an arbitrary nullspace
translate has a huge norm, that huge norm is irrelevant.

---

## 7. Exact completion and physical contact

For any boundary solve `y`, the fixed-multiplier completion is

**(7.1)**

`E_0-f(x)`

` = (1/4)(2x-y)^T K_0(2x-y)`

`   + tau_0 (R-Q_G(x))`.

Both terms are nonnegative on the physical ellipsoid.

Use the canonical solve `y_c` from now on.

### 7.1 Non-hard contact: `s_c=4R`

If

`s_c=4R`,

then

`x_c:=y_c/2`

lies on the ellipsoid boundary and makes both terms in (7.1) zero.  Therefore

**(7.2)** `f(x_c)=E_0`.

### 7.2 Inactive constraint when `tau_0=0`

If `tau_0=0` and merely

`s_c<=4R`,

then `x_c=y_c/2` is feasible and the second term in (7.1) vanishes identically.
So again

**(7.3)** `f(x_c)=E_0`.

No boundary fill is needed in this zero-multiplier case.

### 7.3 Singular hard case when `tau_0>0` and `s_c<4R`

Now assume

`tau_0>0`, `s_c<4R`.

Because `K_0` is singular, choose any nonzero `v in N` and define

`a:=Q_G(v)>0`,

`h:=4R-s_c>0`.

Canonical orthogonality gives

**(7.4)** `B_G(y_c,v)=0`.

Hence for any real `t`,

**(7.5)** `Q_G(y_c+t v)=s_c+t^2 a`.

Since `a>0` and `h>=0`, there exists a real `t` with

**(7.6)** `a t^2=h`.

Set

`n:=t v`,

`x_*:=(y_c+n)/2`.

Then

`K_0 n=0`,

`Q_G(y_c+n)=4R`,

so

`Q_G(x_*)=R`

and both terms in (7.1) vanish. Therefore

**(7.7)** `f(x_*)=E_0`.

### Root-free trusted input

The trusted rational packet does **not** need to contain the generally
irrational scalar `t`.  It only needs rational data verifying

- `K_0 v=0` and `v!=0`;
- `a=Q_G(v)>0`;
- `h=4R-s_c>=0`.

Existence of a real `t` with `a t^2=h` is a source-independent real-algebra
lemma.  This separates rational certification from display of a particular
physical maximizer.

---

## 8. The opposite branch `s_c>4R` is genuinely nonoptimal

The condition `s_c>4R` is not just failure to certify Theorem D.  For the
canonical representative it is the true opposite branch.

Let

`M=N^{perp_G}`.

Since `K_0>=0` and its only zero directions are `N`, the restriction of `K_0`
to `M` is positive definite.  Hence in finite dimension there exists

**(8.1)** `m>0`

such that

**(8.2)** `m Q_G(z) <= z^T K_0 z`

for every `z in M`.

For a rational checker one may use any rational positive `m` below the true
restricted coercivity constant; a basis-level certificate is

`V^T K_0 V - m V^T G V >=0`

for a basis matrix `V` spanning `M`.

### Theorem E — explicit small-step descent from the singular boundary

Assume

**(8.3)** `s_c>4R`,

and choose `d>0` satisfying the division-free gate

**(8.4)** `d s_c < m (s_c-4R)`.

Then the sharp floor at the shifted multiplier `tau_0+d` is strictly smaller:

**(8.5)** `E_d<E_0`.

### Proof

Let

`z:=y_c-y_d`.

By Lemma C, both `y_c` and `y_d` lie in `M`, hence `z in M`.

From the two solve equations,

**(8.6)** `K_0 z=d G y_d`.

Therefore

`m Q_G(z)`

` <= z^T K_0 z`

` = d B_G(z,y_d)`

` <= d sqrt(Q_G(z) Q_G(y_d))`.

If `z=0`, the desired estimate below is trivial.  Otherwise divide the last
inequality by `sqrt(Q_G(z))` and square to obtain

**(8.7)**

`Q_G(z) <= (d^2/m^2) Q_G(y_d)`.

By the cross sandwich (6.3),

`Q_G(y_d)<=s_c`,

so

**(8.8)** `Q_G(z) <= d^2 s_c/m^2`.

Now

`s_c-c_d=B_G(y_c,z)`.

The cross sandwich already gives the left side nonnegative, and Cauchy plus
(8.8) gives

**(8.9)**

`s_c-c_d <= d s_c/m`.

Thus

**(8.10)** `c_d >= s_c-d s_c/m`.

Condition (8.4) is exactly

`d s_c/m < s_c-4R`,

so

**(8.11)** `c_d>4R`.

The exact secant formula (6.2) then gives `E_d-E_0<0`.

### Consequence — intrinsic iff classification

On the standard feasible multiplier ray with `K_0` the singular left boundary,

**(8.12)**

`tau_0 is multiplier-optimal  <=>  s_c<=4R`.

The forward implication uses Theorem E and existence of the restricted
coercivity constant `m`; the reverse implication is Theorem D.

This is the singular-boundary decision that was unavailable when one used an
arbitrary nullspace translate of a range solve.

---

## 9. Interior optimizer after the bad boundary branch

Assume now

`R>0`, `s_c>4R`.

For `d>0`, `K_d>0` and the unique solve `y_d` varies continuously with `d`.
The argument above shows

`Q_G(y_d) -> s_c`

as `d downarrow 0`.

As `d -> infinity`, `K_d>=dG`, so the solve tends to zero and

`Q_G(y_d)->0`.

Moreover T-P5-140's cross sandwich shows `Q_G(y_d)` is nonincreasing in `d`.
It is strictly decreasing in this branch: equality at two distinct positive
multipliers would force the two exact solves to agree; subtracting the solve
equations would then force `G y=0`, hence `b=0`, contradicting `s_c>0`.

Therefore there is a unique

**(9.1)** `d_*>0`

such that

**(9.2)** `Q_G(y_{d_*})=4R`.

By T-P5-140 this is the unique interior multiplier optimum, and

`x_*=y_{d_*}/2`

is the non-hard physical contact state.

### Important zero-radius exception

If `R=0` and `s_c>0`, the equation `Q_G(y_d)=4R=0` has no finite solution while
`b!=0`.  The sharp floor may decrease toward an infimum as `d->infinity`
without a finite stationary multiplier.  Therefore the claim

> bad singular boundary implies a finite interior stationary multiplier

requires `R>0`.

The small-step descent theorem itself does not require `R>0`.

---

## 10. Exact rational regressions

### 10.1 Arbitrary singular solve gives a false signal

Use the singular example already appearing downstream of T-P5-139:

`G=I`,

`K_0=diag(0,2)`,

`b=(0,3)`,

`R=1`.

The solve class is

`y_M=(M,3/2)`.

The canonical condition `y_c perp_G ker K_0` gives

`y_c=(0,3/2)`,

so

`s_c=9/4<4`.

Hence the boundary is globally optimal.

But choosing `M=2` gives

`Q_G(y_M)=4+9/4=25/4>4`.

Thus the raw same-point norm of an arbitrary singular solve would falsely
suggest the opposite branch.  Canonicalization removes this artifact exactly.

### 10.2 Root-free hard-case contact with irrational state

Take the full T-P5-139 reset packet

`G=I`, `R=1`,

`H=diag(-1,1)`,

`tau_0=1`,

`K_0=H+tau_0G=diag(0,2)`,

`b=(0,3)`, `C=0`.

The canonical solve is again

`y_c=(0,3/2)`, `s_c=9/4`.

The intrinsic floor is

`E_0=1+(9/2)/4=17/8`.

Choose the rational null vector

`v=(1,0)`.

Then

`a=Q_G(v)=1`,

`h=4-s_c=7/4`.

The trusted packet can remain entirely rational.  A physical contact uses a
real `t` satisfying

`t^2=7/4`,

so `t=sqrt(7)/2` is irrational.  Requiring the explicit contact vector to be
rational would incorrectly reject a perfectly sharp rational certificate.

### 10.3 Canonical norm above threshold: boundary is truly loose

Take

`G=I`,

`K_0=diag(0,1)`,

`tau_0=0`,

`H=K_0`,

`b=(0,4)`,

`R=1`, `C=0`.

The canonical solve is

`y_c=(0,4)`,

`s_c=16>4`.

The boundary floor is

`E_0=4`.

For `d>0`,

`K_d=diag(d,1+d)`,

`y_d=(0,4/(1+d))`,

and

`E_d=d+4/(1+d)`.

At

`d_*=1`,

`Q_G(y_{d_*})=4`

and

`E_{d_*}=3<E_0`.

The physical quadratic is

`f(x)=4x_2-x_2^2`

on the unit ball, whose maximum is exactly `3` at `x_2=1`.  Thus `s_c>4R`
is not a mere certificate failure: the singular boundary floor is genuinely
nonsharp.

For the explicit small-step theorem, the complement is `span(e_2)` and one may
take `m=1`.  Condition (8.4) becomes

`16d<12`, i.e. `d<3/4`.

Choosing the rational step `d=1/2` gives

`E_{1/2}=1/2+8/3=19/6<4`,

as predicted.

### 10.4 Zero-radius edge

Keep

`G=I`, `K_0=diag(0,1)`, `tau_0=0`, `H=K_0`,

but take

`b=(0,1)`, `R=0`, `C=0`.

Then `s_c=1>0=4R` and

`E_d=1/[4(1+d)]`.

The floor strictly decreases toward `0` as `d->infinity`, but no finite
`d` satisfies the stationarity equation `Q_G(y_d)=0`.  This is the exact
counterexample requiring the `R>0` hypothesis in Section 9.

---

## 11. Suggested Lean theorem split

The source-independent formalization can be small.

### L1 — `canonicalRangeSolve_pythagoras`

Inputs:

- `K` symmetric;
- `K y_c=b`, `K y=b`;
- `forall n, K n=0 -> <y_c,G n>=0`;
- `G` symmetric positive definite.

Conclusion:

`Q_G(y)=Q_G(y_c)+Q_G(y-y_c)`.

### L2 — `canonicalRangeSolve_unique`

Two range solves both `G`-orthogonal to `ker K` are equal.

### L3 — `interiorSolve_oldKernel_orthogonal`

Inputs:

- `K_0 n=0`;
- `K_d=K_0+dG`, `d>0`;
- `K_d y_d=b=K_0 y_c`.

Conclusion:

`<n,G y_d>=0`.

This is ring algebra plus division by the positive scalar `d`, or a
multiplication-form equivalent.

### L4 — `canonicalBoundary_optimal`

Compose the T-P5-140 secant/cross lemma with

`Q_G(y_c)<=4R`

to prove every larger feasible multiplier has floor at least `E_0`.

### L5 — `singularBoundary_contact_exists`

Inputs:

- `K_0` singular PSD;
- canonical solve `y_c`;
- `Q_G(y_c)<=4R`;
- `tau_0>0` for the active-constraint branch.

Conclusion:

there exists `n in ker K_0` with

`Q_G(y_c+n)=4R`.

A separate trivial branch handles `tau_0=0` with `n=0` and an inactive
constraint.

### L6 — `canonicalBoundary_smallStep_descent`

Inputs:

- restricted coercivity `m Q_G(z)<=Q_K0(z)` on `M`;
- `s_c>4R`;
- `d>0` and `d s_c < m(s_c-4R)`.

Conclusion:

`E_d<E_0`.

The proof needs only Cauchy-Schwarz in the `G` inner product and the existing
T-P5-140 secant identity.

### L7 — basis adapter

If columns of `Z` span `ker K_0`,

`K_0 y_0=b`,

`(Z^T G Z) alpha=Z^T G y_0`,

then

`y_c=y_0-Z alpha`

is canonical.  This is the best exact-rational producer-facing leaf.

---

## 12. Recommended source/checker packet

At a singular left multiplier boundary, retain under one source/reference/cell
key:

1. rational `G,K_0,b,R,tau_0,C`;
2. `G>0`, `K_0>=0`, and explicit singularity/kernel witness;
3. a basis `Z` of `ker K_0` or an equivalent typed kernel subspace witness;
4. one exact range solve `K_0 y_0=b`;
5. exact nullspace Gram solve
   `(Z^T G Z) alpha=Z^T G y_0`;
6. canonical vector `y_c=y_0-Z alpha`;
7. exact scalar `s_c=y_c^T G y_c`;
8. branch on `s_c<=4R` versus `s_c>4R`;
9. only in the bad branch, either use the existing exact T-P5-140 rational
   secant search or provide a restricted coercivity witness `m` and a rational
   small step satisfying `d s_c < m(s_c-4R)`.

Do **not** choose a convenient nullspace translate and feed its norm into a
boundary decision.  The canonical scalar is the intrinsic datum.

---

## 13. Fail-closed boundaries

1. `G` must be positive definite for the canonical minimum and nullspace Gram
   system used here.  A semidefinite `G` needs a quotient/range variant.
2. `K_0` must be symmetric PSD.  For an indefinite boundary matrix, quadratic
   zero directions and the kernel are not interchangeable.
3. `b` must lie in `range(K_0)`; otherwise no finite fixed-boundary Schur floor
   exists by the T-P5-139 range obstruction.
4. A list of null vectors is not enough for the rational canonicalization
   unless it spans the complete kernel.  Missing a null direction can produce a
   nonminimal `s_c`.
5. The hard-case contact fill `Q_G(y_c+n)=4R` is required only when
   `tau_0>0`; at `tau_0=0` an interior feasible `y_c/2` already saturates the
   completion.
6. `s_c>4R` proves the singular boundary is not optimal, but the explicit
   algebraic small-step certificate requires a correctly typed restricted
   coercivity constant `m`.  Do not substitute a full-space positive lower
   bound for `K_0`; none exists because `K_0` is singular.
7. The finite interior stationary optimizer in Section 9 additionally requires
   `R>0`.  At `R=0` the optimum may live only at infinite multiplier.
8. The root-free contact packet proves existence of a real contact state; it
   does not claim the contact coordinates are rational.
9. All multiplier statements remain conditional on the upstream exact
   quadratic reset model and same source key.  They do not bind the deployed
   controller/reference/runtime source.
10. No Lean/kernel receipt, independent verification by 封不觉, coverage,
    admission, registry promotion, or P5/M4 parent closure is claimed.

---

## 14. Result

The singular-boundary ambiguity in T-P5-140 can be removed completely at the
mathematical interface level.

There is a unique canonical range solve

`K_0 y_c=b`,

`y_c perp_G ker K_0`,

and it satisfies the exact Pythagorean identity

**`Q_G(y)=Q_G(y_c)+Q_G(y-y_c)`**

for every other boundary solve.  Thus

**`s_c:=Q_G(y_c)`**

is the intrinsic minimum same-point metric norm.

On the standard feasible multiplier ray,

**`tau_0 is globally multiplier-optimal iff s_c<=4R`.**

If `s_c<=4R`, the boundary floor is physically sharp.  For `tau_0>0` and
strict inequality, singularity supplies the classical nullspace hard-case
contact; the trusted input needs only rational `a>0` and `h=4R-s_c>=0`, not the
possibly irrational square root used to display the contact state.

If `s_c>4R`, the boundary is genuinely loose.  A fully algebraic sufficient
small-step gate is

**`d s_c < m(s_c-4R)`**,

where `m` is any positive coercivity constant for `K_0` on
`(ker K_0)^{perp_G}`; this forces the exact cross metric above `4R` and hence
`E_{tau_0+d}<E_0`.

For rational matrix data, the canonical representative itself is obtained by
the rational nullspace Gram solve

`(Z^T G Z) alpha=Z^T G y_0`,

`y_c=y_0-Z alpha`.

So the singular boundary can now be classified without pseudoinverses,
square-root coordinates, arbitrary nullspace representatives, or heuristic
same-point norms.

Current status remains `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending` until
actual same-key source packets, coverage, runtime semantics, Lean/kernel
validation, independent verification, and admission gates are supplied.
