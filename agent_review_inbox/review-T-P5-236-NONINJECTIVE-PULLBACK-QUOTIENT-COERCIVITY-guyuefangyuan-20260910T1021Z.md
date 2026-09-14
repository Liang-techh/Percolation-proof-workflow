---
kind: review_result
review_id: review-T-P5-236-noninjective-pullback-quotient-coercivity-guyuefangyuan-20260910T1021Z
task_id: T-P5-236-NONINJECTIVE-PULLBACK-QUOTIENT-COERCIVITY
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T10:21:00Z
claim_commit: e47d86396a61948e4635cbcf10d50710d9e00561
inspected_commit: 0967f2fe734c4c3d2b15d379a03a044dadf639ff
upstream_commits:
  - fde193bcd1c1231efc817e804d5d985b7a244d5b  # T-P5-235 equality + ellipsoid rank-free KKT
  - 69e1214a25f1e14137fb606bb6025b33ae187dd3  # T-P5-234 rank-deficient equality quotient dual
  - 580ac9aef688269631f738f61bb24b4a7e196625  # T-P5-232 coupled-fiber conditional Schur reduction
  - db655d40ee23d1c71f03f46eb20d112d0553b2fa  # T-P5-228 fiber-sign radical annihilation
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_noninjective_quadratic_pullback; add_rankfree_quotient_coercivity_completion; add_affine_quotient_recentering; extend_fixedLambda_lift_to_psd; extend_equality_ellipsoid_packet_to_quotient_coercive_psd
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic / kernel / KKT algebra only; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-236 — non-injective source pullback and equality-quotient coercivity

## 0. Verdict and seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-235 closed the equality + bounded ellipsoid KKT packet under the ambient hypothesis `P>0` and explicitly left the next seam: a real source energy/ellipsoid may be transported into redundant lifted coordinates by a non-injective map. Then the pulled matrix is only positive semidefinite in the ambient lifted space even though it can be strictly coercive after imposing the exact equality constraints.

This child removes that unnecessarily strong ambient-PD assumption.

The main conclusions are:

1. A physical quadratic bound pulled through `x = e + L y` has exact matrix `P=L^T W L`; non-injectivity appears only through `ker(P)`.
2. The pulled quadratic is positive definite on the equality quotient `A y=0` iff `ker(A) ∩ ker(P)={0}`. This can be certified **without a nullspace basis** by one ambient equality-penalty completion `P + A^T R A > 0`.
3. A rational lower certificate `P + A^T R A - kappa I >= 0`, `kappa>0`, gives the division-free bound `kappa ||y||^2 <= y^T P y` on `A y=0` and hence compactness of the equality-restricted source fiber.
4. An affine physical ellipsoid can be recentered **inside the equality quotient** by a rank-free KKT pair `(y_c,nu_c)` satisfying `A y_c=0` and `P y_c + A^T nu_c + h=0`. This produces an exact centered radius and an exact transformed Lyapunov debit.
5. T-P5-235's fixed-`lambda` quotient/lift equivalence actually remains true for an arbitrary PSD ambient quadratic block `K>=0`; ambient invertibility is unnecessary.
6. Consequently the full equality + ellipsoid safety theorem remains necessary-and-sufficient when `P>=0` is only coercive on `ker(A)`.

No actual P5 source map, source ellipsoid, equality packet, same-cell/tube coverage, Float64 enclosure, Lean/kernel receipt, independent validation, admission, registry mutation, or parent closure is claimed.

---

# Part I — exact physical-to-lifted quadratic transport

## 1. Setup

Let the centered/affine physical state be

`x = e + L y`,

where

- `y in R^n` is the redundant lifted coordinate used by the P5 fiber/KKT branch,
- `x in R^d` is the physical coordinate on which a source energy/ellipsoid is known,
- `L : R^n -> R^d` may be non-injective,
- `e` is the physical center offset relative to the source quadratic center.

Let `W=W^T>=0` and suppose the physical source bound is

`x^T W x <= rho`.

Define

`P := L^T W L >= 0`,

`h := L^T W e`,

`c := e^T W e`.

Then the exact pulled source inequality is

**`phi(y) := y^T P y + 2 h^T y + c <= rho`.**

This is an identity, not an estimate.

### Theorem A — `quadraticSource_affinePullback_exact`

For every `y`,

`(e+Ly)^T W (e+Ly)`

`= y^T(L^TWL)y + 2(L^TWe)^T y + e^TWe`.

Hence any exact/outer physical source bound transports to the lifted coordinate with the same exact/outer semantics, provided the affine map itself is source-bound.

### Semantic boundary

For a PASS theorem, an outer physical ellipsoid plus an exact source map is sufficient: every actual lifted state maps into the pulled outer set.

For a FAIL theorem, a witness in the pulled outer set is not automatically an actual source/reachable state. A failure witness requires exact-set semantics or a separate source-membership/reachability witness.

---

## 2. Kernel of a non-injective quadratic pullback

### Theorem B — `quadraticPullback_kernel`

For `W>=0` and `P=L^TWL`,

**`ker(P) = { y : Ly in ker(W) }`.**

If `W>0`, this simplifies to

**`ker(P)=ker(L)`.**

### Proof

For every `y`,

`y^T P y = (Ly)^T W (Ly) >= 0`.

For a PSD symmetric matrix, `v^T W v=0` iff `Wv=0`. Therefore

`y^TPy=0`

iff `Ly in ker(W)`.

Because `P>=0`, `y^TPy=0` iff `Py=0`, proving the first identity. If `W>0`, its kernel is zero, giving `ker(P)=ker(L)`. QED.

This is the exact mathematical reason why a genuine physical ellipsoid can become singular in redundant lifted coordinates.

---

# Part II — coercivity only on the equality quotient

## 3. Equality-restricted positive definiteness

Let the exact centered lifted equality be

**`A y = 0`**

with arbitrary row rank.

Define the equality subspace

`E := ker(A)`.

The correct replacement for ambient `P>0` is:

**`y != 0 and Ay=0  =>  y^T P y > 0`.**

Call this **quotient coercivity**.

### Theorem C — `pullback_quotientCoercive_iff_kernelIntersection`

For `P>=0`, the following are equivalent:

1. `P` is positive definite on `ker(A)`;
2. **`ker(A) ∩ ker(P) = {0}`.**

For a physical pullback `P=L^TWL`, this becomes

`ker(A) ∩ {y : Ly in ker(W)} = {0}`.

If `W>0`, it is simply

**`ker(A) ∩ ker(L) = {0}`.**

Thus the physical map need not be injective on the whole lifted coordinate space; it only needs to be injective after the exact equality quotient is imposed.

---

## 4. Rank-free equality-penalty completion

A nullspace basis is unnecessary for checking quotient coercivity.

Let `R=R^T>0` be any positive-definite equality weight and define

**`Q_R := P + A^T R A`.**

### Theorem D — `quotientCoercive_iff_equalityPenaltyPD`

For `P>=0` and `R>0`,

**`P is positive definite on ker(A)` iff `Q_R>0`.**

Indeed, for every `y`,

`y^T Q_R y = y^TPy + (Ay)^T R(Ay)`.

The right side is zero iff both `Py=0` and `Ay=0`; hence `Q_R` is PD exactly when the kernel intersection is trivial.

The statement holds for **every** choice of `R>0`; the equality weight only changes the conditioning of the checker packet, not the mathematical criterion.

### Rational checker corollary

If `P,A,R` are rational and quotient coercivity holds, then `Q_R` is rational SPD. Hence there exists a rational `kappa>0` such that

**`Q_R - kappa I >= 0`.**

Conversely, any submitted exact certificate

`R>0`, `kappa>0`, `Q_R-kappa I>=0`

immediately proves quotient coercivity.

No eigenvalue needs to be reified in the theorem. The producer may supply any convenient rational `kappa`; the checker only verifies a PSD inequality.

### Division-free coercivity bound

On the equality subspace `Ay=0`,

`Q_R=P`, so

**`kappa ||y||^2 <= y^T P y`.**

Therefore from

`Ay=0`, `y^TPy<=rho`

one gets

**`kappa ||y||^2 <= rho`.**

This proves boundedness with no square root.

---

## 5. Compactness of the singular ambient ellipsoid on the quotient

Assume `rho>=0` and quotient coercivity. Then

`F_rho := {y : Ay=0, y^TPy<=rho}`

is closed and bounded, hence compact.

If `rho>0`, `y=0` is a strict interior point relative to `ker(A)`.

This is exactly the compactness/Slater input T-P5-235 needed from ambient `P>0`; ambient PD itself was stronger than necessary.

### Regression 1 — ambient singular, quotient perfectly coercive

Take

`P = [[1,0],[0,0]]`,

`A = [0,1]`.

Then `P` is singular, but the equality forces `y2=0`. On `ker(A)`,

`y^TPy=y1^2`.

With `R=[1]`,

`Q_R=P+A^TRA=I_2`.

So the rank-free certificate holds with `kappa=1` exactly. A theorem requiring ambient `P>0` would reject this harmless redundant coordinate representation.

---

# Part III — exact affine recentering inside the equality quotient

## 6. Why dropping the pullback linear term is unsound

The exact pulled source set is generally

`y^TPy + 2h^Ty + c <= rho`,

not `y^TPy<=rho`.

The linear term may be deleted on `Ay=0` only when it is equality-normal:

`h in range(A^T)`.

Equivalently, `h^Ty=0` for every `Ay=0`.

In general the correct operation is to recenter the quadratic **within the equality subspace**.

---

## 7. Rank-free quotient-center KKT packet

Assume `P>=0` is quotient-coercive on `ker(A)`.

Then there exists a unique `y_c in ker(A)` minimizing

`y^T P y + 2 h^T y`

on `Ay=0`.

Moreover there exists at least one multiplier `nu_c` such that

**`A y_c = 0`,**

**`P y_c + A^T nu_c + h = 0`.**

No row-rank assumption on `A` is required; `nu_c` may be nonunique when rows are dependent, but `y_c` is unique.

For rational `P,A,h`, a rational pair `(y_c,nu_c)` exists because the reduced coercive linear system has rational coefficients. A source/checker packet therefore does not need a pseudoinverse: it may simply submit rational `y_c,nu_c` and verify the two displayed equations.

### Theorem E — `affineQuadratic_recenter_onEqualityQuotient`

Let `z:=y-y_c`. Since both `Ay=0` and `Ay_c=0`, one has `Az=0`. Also

`P y_c+h = -A^Tnu_c`,

so the cross term against every equality tangent `z` vanishes. Therefore

**`phi(y) = z^T P z + phi(y_c)`**

for every `Ay=0`.

Hence the affine source inequality is exactly equivalent on the equality fiber to

**`z^T P z <= rho_eff`,**

where

**`rho_eff := rho - phi(y_c)`.**

Using stationarity dotted with `y_c`,

`y_c^T P y_c + h^T y_c = 0`,

so an equivalent scalar formula is

`phi(y_c)=c+h^T y_c = c-y_c^TPy_c`.

Everything is rational whenever the input packet is rational.

### Radius trichotomy

- `rho_eff>0`: genuine bounded quotient ellipsoid with strict relative interior; use the KKT/S-lemma packet below.
- `rho_eff=0`: quotient coercivity forces `z=0`; the source fiber is the singleton `{y_c}` and safety reduces to one point evaluation.
- `rho_eff<0`: the mathematical source fiber is empty. This may make an abstract universal statement vacuous, but if the source model is intended to contain actual states it is a **source inconsistency/coverage obstruction**, not a physical PASS certificate.

---

## 8. Exact transport of the Lyapunov debit under recentering

Let the debit be

`q(y)=q0 + 2g^Ty - y^T H y`,

with `H=H^T>=0`.

Under `y=y_c+z`, define

**`g_c := g - H y_c`,**

**`q0_c := q(y_c) = q0 + 2g^Ty_c - y_c^THy_c`.**

Then exactly

**`q(y_c+z) = q0_c + 2 g_c^T z - z^T H z`.**

Thus a real affine physical ellipsoid can be transported to the centered T-P5-235 coordinate form without inventing a new optimizer or dropping center terms.

---

# Part IV — the fixed-lambda equality lift does not require ambient PD

## 9. Semidefinite fixed-lambda lift theorem

This is the key algebraic extension needed to reuse T-P5-235 after a singular pullback.

Let

`K=K^T>=0`,

`A` arbitrary rank,

`g in R^n`, `c in R`,

and let `N` be any full-column matrix with `range(N)=ker(A)`.

Define

`S := N^T K N >=0`,

`h := N^T g`.

The quotient homogenized matrix is

`M_N := [[S,-h],[-h^T,c]]`.

The full equality-multiplier matrix is

`M(nu) := [[K,A^Tnu-g],[(A^Tnu-g)^T,c]]`.

### Theorem F — `fixedLambda_psdQuotient_iff_rankFreeEqualityLift`

**`M_N>=0` iff there exists `nu` such that `M(nu)>=0`.**

No positive definiteness of `K` is required.

### Proof: full to quotient

Restrict the full quadratic to vectors `y=Nxi`. Since `AN=0`, the equality-multiplier term disappears and one obtains exactly the quotient block. Hence full PSD implies quotient PSD.

### Proof: quotient to full

Assume `M_N>=0`.

A PSD block with leading block `S>=0` forces

`h in range(S)`.

Indeed, if `z in ker(S)` but `z^Th !=0`, evaluating the quadratic on `(tz,1)` with either sign of `t` produces a negative value for large enough `|t|`.

Choose `xi` with

`S xi = h`,

and set

`y_* := N xi`.

Then

`N^T(Ky_*-g)=0`,

so

`g-Ky_* in (ker A)^perp = range(A^T)`.

Therefore choose `nu` satisfying

`A^Tnu = g-Ky_*`.

The full off-diagonal block becomes

`A^Tnu-g = -K y_*`.

Also quotient PSD gives

`c >= xi^T S xi = y_*^T K y_*`.

Now for every `x,t`,

`x^T K x + 2t(A^Tnu-g)^T x + c t^2`

`= (x-t y_*)^T K (x-t y_*)`

`  + (c-y_*^TKy_*) t^2`

`>=0`.

Hence `M(nu)>=0`. QED.

### Consequence

T-P5-235's equality multiplier is an **extension device**, not an ambient-invertibility device. Singular directions outside the equality quotient do not matter provided the quotient block itself is PSD.

---

# Part V — generalized equality + ellipsoid certificate

## 10. Quotient-coercive semidefinite ellipsoid theorem

Let

`H=H^T>=0`,

`P=P^T>=0`,

`rho>0`,

`A` arbitrary rank,

and assume `P` is positive definite on `ker(A)`.

Define

`q(z)=q0+2g^Tz-z^THz`,

`F={z:Az=0, z^TPz<=rho}`.

For `lambda>=0` and multiplier `nu`, define

`K_lambda := H + lambda P >=0`,

`c_lambda := -q0-lambda rho`,

and

**`M(lambda,nu) := [[K_lambda,A^Tnu-g],[(A^Tnu-g)^T,c_lambda]]`.**

### Theorem G — `equalitySemidefiniteEllipsoid_safe_iff_rankFreePSDMultiplier`

The following are equivalent:

1. `q(z)<=0` for every `z in F`;
2. there exist `lambda>=0` and `nu` such that

**`M(lambda,nu)>=0`.**

This is exactly T-P5-235 with ambient `P>0` replaced by the weaker and source-natural condition `P>0` only on `ker(A)`.

### Proof of sufficiency

For `Az=0`,

`[z;1]^T M(lambda,nu)[z;1]`

`= -q(z) + lambda(z^TPz-rho)`.

If the block is PSD and `z^TPz<=rho`, then

`-q(z) >= lambda(rho-z^TPz)>=0`.

### Proof of necessity without convex-duality formalization

Choose any basis matrix `N` of `ker(A)`.

By quotient coercivity,

`P_N:=N^TPN>0`.

Also `H_N:=N^THN>=0`.

Write `z=Nxi`. The problem becomes the ordinary bounded trust-region problem

`xi^T P_N xi <= rho`

for the concave quadratic

`q_N(xi)=q0+2(N^Tg)^Txi-xi^TH_Nxi`.

T-P5-230's exact ellipsoid/S-lemma theorem applies because `P_N>0`, yielding some `lambda>=0` for which the quotient homogenized block is PSD.

Now use Theorem F with

`K=H+lambda P>=0`

to lift that quotient PSD block to a full rank-free equality multiplier `nu`.

Thus the generalized theorem follows by composition. QED.

### Lean significance

The formal route need not import a general constrained convex-duality library. It can reuse the already intended trust-region theorem on the coercive quotient plus one finite-dimensional semidefinite lifting lemma.

---

## 11. Complete source-to-KKT transport pipeline

A same-key source packet may now proceed as follows.

1. Provide the exact physical quadratic source model
   `x=e+Ly`, `W>=0`, `x^TWx<=rho`.
2. Compute exactly
   `P=L^TWL`, `h=L^TWe`, `c=e^TWe`.
3. Provide the exact lifted equality `Ay=0`.
4. Prove quotient coercivity by a rank-free completion packet
   `R>0`, `kappa>0`,
   `P+A^TRA-kappa I>=0`.
5. Provide rational quotient-center witnesses `y_c,nu_c` satisfying
   `Ay_c=0`,
   `Py_c+A^Tnu_c+h=0`.
6. Compute
   `rho_eff=rho-phi(y_c)`.
7. If `rho_eff>0`, transform the debit to
   `q0_c`, `g_c`, `H` and apply Theorem G.
8. If `rho_eff=0`, check the singleton state `y_c` directly.
9. If `rho_eff<0`, record a source-model inconsistency/empty-fiber obstruction rather than a physical safety result.

Every step is exact finite-dimensional linear/quadratic algebra. No pseudoinverse, square root, eigenvector, floating nullspace tolerance, or generic nonlinear optimizer is required by the checker interface.

---

# Part VI — obstructions and negative controls

## 12. Failure of quotient coercivity is not automatically Lyapunov FAIL

If

`G := ker(A) ∩ ker(P)`

is nontrivial, then the physical quadratic source bound does not bound motion along `G`.

However this alone does **not** imply the debit becomes positive.

### Unsafe example

Take

`P=diag(1,0)`, `A=0`, `H=0`, `g=e2`, `q0=0`.

The source set contains every `(0,t)`, and

`q(0,t)=2t`,

so the supremum is `+infinity`.

### Safe despite noncoercivity

Keep the same `P,A`, but take

`H=diag(0,1)`, `g=0`, `q0=0`.

Then

`q(y)=-y2^2<=0`

on the entire unbounded source set.

Therefore `ker(A)∩ker(P) != {0}` is an obstruction to the **compact quotient-ellipsoid adapter**, not a universal safety failure.

The correct fallback is the signed-flat/gauge analysis already developed in T-P5-224/T-P5-228: inspect whether the debit supplies curvature or radical annihilation on the unobserved lifted directions.

---

## 13. Center mismatch cannot be silently discarded

Even if the physical source inequality is a perfect ellipsoid, the pulled set is affine unless the quotient center is handled.

A naive replacement

`y^TPy+2h^Ty+c<=rho`

by

`y^TPy<=rho`

changes the source set and can reverse a sharp sign result.

### Exact one-dimensional regression

Let the equality force `y2=0` and take

`P=diag(1,0)`,

`h=(1,0)`,

`c=1`,

`rho=4`.

Then on the equality line the source set is

`y1^2+2y1+1 <=4`,

i.e.

`(y1+1)^2<=4`,

so `y1 in [-3,1]`.

The quotient center is

`y_c=(-1,0)`,

and `rho_eff=4`.

Dropping the linear term instead gives `y1 in[-2,2]`, a genuinely different set. The correct adapter is exact recentering, not deletion.

---

## 14. Physical non-injectivity versus gauge redundancy

For `W>0`, a lifted null direction is physically invisible exactly when it lies in `ker(L)`.

If such a direction is also allowed by the equality (`ker(A)`), then it is a true unresolved gauge of the source representation. If the equality kills it, there is no physical obstruction at all.

This distinction should be preserved in source metadata:

- `ambient_pullback_singular=true` is harmless by itself;
- `quotient_kernel_nontrivial=true` means the compact-ellipsoid route is incomplete;
- only a debit analysis on the surviving gauge decides PASS/FAIL.

---

# Part VII — minimal theorem decomposition

## 15. Suggested Lean leaves

The first formalization pass can stay entirely in finite-dimensional real linear algebra.

Suggested leaves:

1. `quadraticPullback_psd`
   - `W>=0 -> L^T W L>=0`.

2. `quadraticPullback_kernel`
   - `ker(L^T W L) = {y | Ly in ker W}` for symmetric PSD `W`.

3. `quotientCoercive_iff_kernelIntersection`
   - `P>=0`: positivity on `ker A` iff `ker A ∩ ker P = {0}`.

4. `quotientCoercive_iff_equalityPenaltyPD`
   - `R>0`: positivity on `ker A` iff `P+A^T R A>0`.

5. `equalityPenalty_rationalKappa_consumer`
   - from `P+A^TRA-kappa I>=0`, `kappa>0`, `Ay=0`, conclude
     `kappa*||y||^2<=y^TPy`.

6. `affineQuadratic_recenter_onEqualityQuotient`
   - consume `Ay_c=0` and `Py_c+A^Tnu_c+h=0`; prove exact centered identity.

7. `debit_recenter_exact`
   - transform `(q0,g,H)` to `(q0_c,g-Hy_c,H)`.

8. `psdHomogeneousBlock_offdiag_mem_range`
   - PSD `[[S,-h],[-h^T,c]]` implies `h in range S`.

9. `fixedLambda_psdQuotient_iff_rankFreeEqualityLift`
   - Theorem F; no inverse or row-rank assumption.

10. `equalitySemidefiniteEllipsoid_safe_iff_rankFreePSDMultiplier`
    - compose quotient coercivity + T-P5-230 trust-region theorem + leaf 9.

11. `zeroEffectiveRadius_singleton`
    - quotient coercivity plus `z^TPz<=0` and `Az=0` implies `z=0`.

Formalization should keep source binding, Float64/interval semantics, actual cell/tube coverage, and admission outside these leaves.

---

## 16. What this child removes from the P5 source adapter

T-P5-235 previously required ambient `P>0`. A real lifted source packet no longer needs to prove that.

It is enough to show a same-key exact completion such as

**`P + A^T R A - kappa I >= 0`, `R>0`, `kappa>0`.**

This is particularly useful when `(v,z)` contains redundant coordinates or constraint auxiliaries: the source energy may be blind to those coordinates, while the equality equations remove them exactly.

The packet is also stable under redundant equality rows: `A` need not have full row rank because only `Ay=0`, `A^TRA`, and `range(A^T)` are used.

---

## 17. Remaining obligations and next seam

Still open:

- actual same-key physical quadratic/energy source `W,rho`;
- actual affine map `(e,L)` from P5 source/tangent variables into the lifted `(v,z)` coordinates;
- actual homogeneous equality `Ay=0` on the same cell/tube and the exact centering relation;
- exact/outer/inner model semantics for both source map and source quadratic;
- a concrete rational quotient-coercivity packet `R,kappa`;
- a concrete rational recenter pair `(y_c,nu_c)` and positive `rho_eff`;
- interval/Float64 enclosure for all source coefficients;
- concrete Lyapunov multiplier `(lambda,nu)` or a strict reserve;
- trajectory/cell/tube/global coverage;
- Lean implementation and pinned compile;
- independent validation by 封不觉;
- admission / registry / parent closure.

The next smallest mathematical seam is **multi-quadratic source intersection after quotient recentering**: an actual tube may provide several simultaneous quadratic/energy caps rather than one ellipsoid. The useful question is when the equality-quotient coercivity supplied by one positive combination of their pullbacks is sufficient to obtain a lossless or controlled multi-multiplier PSD certificate, and when the ordinary multi-constraint S-procedure becomes conservative. That seam should be attacked with an exact two-constraint counterexample/positive class rather than assuming a generic lossless S-procedure.