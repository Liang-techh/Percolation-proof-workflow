---
kind: review_result
review_id: review-T-P5-147-semidefinite-cell-affine-residual-cap-kuangmanmozun-20260909T1047Z
task_id: T-P5-147-SEMIDEFINITE-CELL-AFFINE-RESIDUAL-CAP
reviewer: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T10:47:00Z
claim_commit: 45068dc9dc926ff4cd443e9137caaf48690d73ff
inspected_commit: c1db98d6af0a35acc736424cda6762478ed49506
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-144-SEMIDEFINITE-CELL-NULLSPACE-ELIMINATION-honglianmozun-20260909T1003Z.md
    commit: 39889bbfd45bbc9bd541a7a8c51f0005a60b0881
  - path: agent_review_inbox/review-T-P5-145-CANONICAL-RANGE-DUAL-DESCENT-liuguanyi-20260909T1012Z.md
    commit: d5adca58a70ff24d658275d6cbd3c5f0d9e261c3
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: allow_sigma_A_minus_r_rT_psd_as_the_exact_finite_affine_escape_interface_for_the_T-P5-144_Au_eq_bN_seam; charge_only_sigma_over_4_in_the_quotient_constant; preserve_the_exact_cross_solve_A_L_eq_H_NM; reject_norm_small_residuals_with_unresolved_kerA_component; keep_T-P5-146_inexact_dual_work_disjoint
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional quadratic-form algebra only
exit_code: n/a
---

# T-P5-147 — semidefinite physical-cell affine residual: exact range cap and sharp additive tax

## 0. Narrow seam and non-overlap

T-P5-144 gives an exact nullspace elimination for a semidefinite physical-cell metric. In its null direction block it assumes

`A >= 0`,

`A u = b_N`,

`A L = H_NM`.

The review explicitly leaves approximate nullspace solves fail-closed because the physical cell is cylindrical in those directions: a numerically small residual can still produce an unbounded affine escape.

This child closes exactly one of those two approximate seams:

- keep the cross solve `A L = H_NM` **exact**;
- replace the affine solve `A u = b_N` by an approximate solve with residual

  `r := b_N - A u`;
- identify the exact algebraic condition under which `r` is harmless;
- isolate the smallest possible additive tax in the quotient reset floor.

This is disjoint from the active T-P5-146 claim by 古月方源. T-P5-146 concerns an inexact **dual solve for singular multiplier canonicalization**. The present child concerns the affine residual left inside the **unbounded physical-cell nullspace** before quotient multiplier theory is applied.

No source binding, provenance/admission, Lean/kernel work, runtime/Float64 semantics, coverage, registry mutation, or P5 parent closure is attempted.

---

## 1. The elementary residual problem on an unbounded PSD direction

Let `A=A^T >= 0` on a finite-dimensional real vector space and let `r` be a vector. Consider

`phi(e) := r^T e - e^T A e`.

This is the only new term produced when `A u=b_N` is replaced by an approximate solve after the exact T-P5-144 cross completion.

The central question is whether `phi` is uniformly bounded above when `e` is unrestricted.

### Theorem A — exact finite-escape classification

The following are equivalent:

1. `r in range(A)`;
2. there exists a finite `sigma >= 0` such that

   **(1.1)** `sigma A - r r^T >= 0`;

3. `sup_e phi(e) < +infinity`.

If `A z=r`, define the intrinsic residual energy

**(1.2)** `rho := r^T z = z^T A z`.

Then `rho` is independent of the chosen solution `z`, `rho>=0`, and

**(1.3)** `sup_e phi(e) = rho/4`.

Moreover the smallest admissible `sigma` in (1.1) is exactly

**(1.4)** `sigma_min = rho`.

Thus the rank-one PSD cap is not merely a sufficient numerical envelope; it is the exact finite-escape interface for this information model.

### Proof: cap implies range

If (1.1) holds and `n in ker(A)`, then

`0 <= n^T (sigma A-r r^T) n = -(r^T n)^2`.

Hence `r^T n=0` for every `n in ker(A)`. Because `A` is symmetric in finite dimension,

`range(A) = ker(A)^perp`,

so `r in range(A)`.

### Proof: range gives the sharp cap

Take any `z` with `A z=r`. For every `v`, PSD Cauchy-Schwarz for the seminorm induced by `A` gives

`(r^T v)^2 = (z^T A v)^2 <= (z^T A z)(v^T A v) = rho v^T A v`.

Therefore

**(1.5)** `rho A-r r^T >=0`.

So `sigma=rho` is admissible.

Conversely, if some `sigma` satisfies (1.1), evaluate it on `z`:

`0 <= sigma z^T A z-(r^T z)^2`

`   = rho(sigma-rho)`.

If `rho>0`, this forces `sigma>=rho`. If `rho=0`, then `z^T A z=0`; PSD of `A` implies `Az=0`, hence `r=0`, and the minimal cap is again zero. This proves (1.4).

### Proof: exact supremum

Using `Az=r`,

**(1.6)**

`r^T e-e^T A e`

`= rho/4-(e-z/2)^T A(e-z/2)`.

The second term is nonnegative and vanishes at `e=z/2`, proving (1.3).

### Failure ray if the range condition is absent

If `r notin range(A)`, symmetry gives some `n in ker(A)` with `r^T n !=0`. Along `e=t n`,

`phi(tn)=t r^T n`.

Choosing the sign of `t` sends this to `+infinity`. No finite additive budget can repair this branch.

---

## 2. Root-free consumer form: the tax is `sigma/4`

The exact correction solve `Az=r` is useful for sharpness, but a downstream checker need not construct it.

Assume only

`A>=0`, `sigma>=0`,

**(2.1)** `sigma A-r r^T >=0`.

For any `e`, define

`q := e^T A e >=0`,

`p := r^T e`.

The PSD cap gives

**(2.2)** `p^2 <= sigma q`.

If `q=0`, (2.2) gives `p=0`. If `q>0`, the same conclusion below follows from the polynomial identity

**(2.3)**

`4 q (q-p+sigma/4)`

`= (2q-p)^2 + (sigma q-p^2) >=0`.

Therefore, in all cases,

**(2.4)** `4(r^T e-e^T A e) <= sigma`,

or equivalently

**(2.5)** `r^T e-e^T A e <= sigma/4`.

No inverse, pseudoinverse, square root, eigenvalue, Young parameter, or explicit correction vector is needed in the trusted consumer.

The factor `1/4` is sharp because equality occurs when `sigma=rho` and `e=z/2`.

---

## 3. Apply the cap to T-P5-144 nullspace elimination

Use the T-P5-144 block notation. The physical metric is semidefinite and the nullspace coordinate `n` is unrestricted by the cell. Write

`f(m,n)`

`:= C + b_M^T m + b_N^T n`

`   - m^T H_MM m - 2 m^T H_MN n - n^T A n`.

Assume

**(3.1)** `A=A^T>=0`,

and keep the cross-range solve exact:

**(3.2)** `A L=H_NM`.

By symmetry,

`H_MN=L^T A`.

Now choose an arbitrary approximate affine solve `u` and define

**(3.3)** `r:=b_N-Au`.

Set

**(3.4)** `e:=n-u/2+Lm`.

A direct expansion gives the exact identity

### Theorem B — approximate affine nullspace completion

**(3.5)**

`f(m,n)`

`= C_hat + b_eff^T m - m^T H_eff m`

`  + r^T e - e^T A e`,

where

**(3.6)** `C_hat := C + (b_N^T u+r^T u)/4`,

**(3.7)** `b_eff := b_M-L^T b_N`,

**(3.8)** `H_eff := H_MM-L^T A L`.

Equivalent forms that may be convenient for a checker are

`4 C_hat = 4C + u^T A u + 2 r^T u`,

and

`b_eff = b_M-H_MN u-L^T r`.

Two structural facts are important.

1. **The affine residual does not perturb the quotient linear coefficient.** It remains the intrinsic quantity `b_M-L^T b_N`.
2. **The affine residual does not perturb the quotient curvature.** It remains `H_MM-L^T A L`.

All uncertainty is isolated in one scalar residual quadratic `r^T e-e^T A e`.

---

## 4. Sharp quotient bound from one PSD cap

Assume in addition that a producer/checker supplies

**(4.1)** `sigma A-r r^T >=0`, `sigma>=0`.

By Theorem A, this automatically proves the missing range condition `r in range(A)` and prevents every uncontrolled kernel escape. By (2.5) and (3.5),

### Theorem C — root-free quotient reduction with affine residual tax

**(4.2)**

`f(m,n) <= C_bar + b_eff^T m-m^T H_eff m`,

where

**(4.3)** `C_bar := C_hat+sigma/4`.

Thus replacing the exact affine solve of T-P5-144 by a certified residual does **not** require weakening the quotient Hessian or quotient covector. It costs only the additive scalar tax `sigma/4`.

This is the smallest universally valid tax available from the cap itself.

---

## 5. Relation to the exact corrected solve and exact overpayment

Because (4.1) implies `r in range(A)`, choose any exact correction `z` satisfying

`A z=r`.

Let

`rho:=r^T z`.

Then `0<=rho<=sigma`, and the corrected affine solve

**(5.1)** `u_*:=u+z`

satisfies

`A u_*=b_N`.

T-P5-144 applied to `u_*` has exact constant

`C_eff=C+b_N^T u_*/4`.

A direct calculation gives

### Theorem D — exact conservative-overpayment identity

**(5.2)** `C_eff = C_hat+rho/4`,

and therefore

**(5.3)** `C_bar-C_eff = (sigma-rho)/4 >=0`.

The quotient linear and quadratic coefficients agree exactly with the corrected T-P5-144 coefficients:

**(5.4)** `b_eff=b_M-H_MN u_* = b_M-L^T b_N`,

**(5.5)** `H_eff=H_MM-H_MN L = H_MM-L^T A L`.

Hence `sigma=rho` recovers the exact T-P5-144 nullspace elimination with no slack at all, while a loose residual cap produces a precisely quantified additive overpayment `(sigma-rho)/4` and nothing else.

---

## 6. Quotient multiplier composition

Let the positive-definite quotient physical metric be `G_M>0`, with cell

`m^T G_M m<=R`.

For a candidate multiplier `tau>=0`, assume

**(6.1)** `K_tau:=H_eff+tau G_M>=0`,

and provide an exact range solve

**(6.2)** `K_tau y=b_eff`.

Define

**(6.3)** `E_bar:=C_bar+tau R+(b_eff^T y)/4`.

Then Theorem C plus the existing fixed-multiplier completion gives

**(6.4)** `f(m,n)<=E_bar`.

If one exposes the correction `Az=r`, the full gap has the exact four-term decomposition

### Theorem E — affine-residual multiplier gap decomposition

**(6.5)**

`E_bar-f(m,n)`

`= (sigma-rho)/4`

`  + (e-z/2)^T A(e-z/2)`

`  + tau(R-m^T G_M m)`

`  + (m-y/2)^T K_tau(m-y/2)`.

Every term is nonnegative on the physical cell.

This isolates the approximate-affine-solve uncertainty from multiplier optimization. Existing T-P5-139/140/143/145 logic can operate on the quotient packet `(C_bar,b_eff,H_eff,G_M,R)` without inventing a new Hessian degradation.

---

## 7. Sharp examples and failure evidence

### Example 7.1 — sharp rational factor `1/4`

Take the one-dimensional null block

`A=1`, `r=1/3`.

An exact correction is `z=1/3`, so

`rho=1/9`.

The minimal PSD cap is `sigma=1/9`, and

`phi(e)=(1/3)e-e^2`.

At `e=1/6`,

**(7.1)** `phi(1/6)=1/36=sigma/4`.

Therefore the coefficient `1/4` in the additive tax cannot be improved under the stated information model.

### Example 7.2 — singular `A` is harmless when the residual is range-compatible

Take

`A=diag(1,0)`,

`r=(1/3,0)`.

Then `sigma=1/9` gives

` sigma A-r r^T = 0`,

and the flat second coordinate carries no affine forcing. The residual supremum is again exactly `1/36` despite the nontrivial kernel.

Thus singularity of `A` itself is not a reason to reject the packet; unresolved forcing in its kernel is the real obstruction.

### Example 7.3 — arbitrarily small kernel residual is fatal

Take

`A=diag(1,0)`,

`r=(0,epsilon)`

for any nonzero real or rational `epsilon`, however small.

For every finite `sigma`, the lower-right entry of

`sigma A-r r^T`

is `-epsilon^2<0`, so the PSD cap fails.

More importantly, this is a genuine mathematical obstruction, not a checker artifact. Along

`e=(0,t sign(epsilon))`,

`e^T A e=0`,

`r^T e=|epsilon| t -> +infinity`.

Therefore a Euclidean-small residual, a tiny Float64 solver residual, or a small componentwise tolerance is **not** sufficient on a cylindrical physical cell. The residual must be certified to have no unresolved `ker A` component, for example by the exact PSD/range packet above.

### Example 7.4 — zero nullspace curvature

If `A=0`, then

`sigma A-r r^T>=0`

holds iff `r=0`. Every nonzero affine residual produces immediate linear escape. This is the sharp endpoint of the theorem.

---

## 8. Minimal theorem statements for formalization

A future Lean sidecar can be split into small source-independent leaves.

### L1 — rank-one residual cap annihilates the kernel

Assume `A=A^T>=0`, `sigma>=0`, `sigma A-r r^T>=0`.

Conclusion:

`forall n, A n=0 -> r^T n=0`.

In finite dimension this yields `r in range(A)`.

### L2 — residual cap scalar consumer

Under the same assumptions, for every `e`, prove the division-free statement

**`4(r^T e-e^T A e) <= sigma`.**

This can be proved from `p^2<=sigma q` and the polynomial identity (2.3), with a separate `q=0` branch.

### L3 — exact correction sharpness

If `A z=r`, define `rho=r^T z`. Prove

`rho>=0`,

`rho A-r r^T>=0`,

and

`r^T e-e^T A e = rho/4-(e-z/2)^T A(e-z/2)`.

### L4 — approximate affine nullspace completion

Assume `A L=H_NM` and `r=b_N-Au`. Prove identity (3.5) with the exact `C_hat,b_eff,H_eff` above.

### L5 — residual-tax quotient theorem

Combine L2 and L4 to derive (4.2) with `C_bar=C_hat+sigma/4`.

### L6 — multiplier gap decomposition

With an exact correction `Az=r` and quotient multiplier solve `K_tau y=b_eff`, prove the four-term equality (6.5).

No theorem needs an inverse, pseudoinverse, square root, eigendecomposition, or floating solver semantics.

---

## 9. Suggested producer/checker packet

A minimal source-independent packet for this seam is

```text
SemidefiniteAffineResidualPacket
  cellKey / resetKey
  A : symmetric PSD nullspace curvature
  L : exact cross solve
  witness_cross : A L = H_NM
  u : approximate affine solve
  r : exact residual with r = b_N - A u
  sigma : nonnegative scalar
  witness_residual_cap : sigma A - r r^T >= 0
```

The consumer forms

```text
C_hat = C + (b_N^T u + r^T u)/4
b_eff = b_M - L^T b_N
H_eff = H_MM - L^T A L
C_bar = C_hat + sigma/4
```

and passes `(C_bar,b_eff,H_eff)` to the existing positive-definite quotient multiplier lane.

If an exact correction `Az=r` is also available, the producer may additionally expose

`rho=r^T z`

to quantify the exact conservatism `(sigma-rho)/4`; it is not required for soundness.

---

## 10. Fail-closed boundaries

1. **The cross solve remains exact.** This child does not handle `A L approximately H_NM`. A cross residual depends on the bounded quotient coordinate `m` but multiplies an unbounded null coordinate; it requires a separate matrix-valued residual theorem and must not be hidden inside `sigma` here.
2. **`A>=0` remains essential.** Negative nullspace curvature gives quadratic escape and no affine residual cap repairs it.
3. **A scalar norm bound on `r` is insufficient.** The required information is range compatibility with `A`; the rank-one PSD cap encodes exactly that plus the residual energy budget.
4. **The PSD cap must be exact at the theorem level.** A sampled or floating approximate PSD result is not a universal range certificate.
5. **Complete physical-metric nullspace splitting remains T-P5-144's premise.** Missing a direction of `ker G` can still hide an unbounded ray.
6. **T-P5-146 remains disjoint.** No claim is made about inexact dual canonical solves or singular-multiplier residual brackets.
7. **Source binding and coverage remain open.** Actual `A,L,u,r,sigma` must still be same-key and same-cell objects.
8. **No Lean/kernel/admission upgrade.** This result is a mathematical child only.

---

## 11. Result

The approximate-affine-solve seam in T-P5-144 can be closed sharply without a pseudoinverse and without weakening quotient curvature.

For the unbounded physical-cell null direction, the exact condition that a residual `r=b_N-Au` admit a finite universal quadratic charge is

**`r in range(A)`**,

which is equivalently certified by the existence of a finite nonnegative `sigma` with

**`sigma A-r r^T >=0`.**

The smallest such `sigma` is the intrinsic residual energy `rho=r^T z` for `Az=r`, and the exact worst residual charge is

**`rho/4`.**

A checker that knows only the PSD cap still gets the root-free sharp-form bound

**`4(r^T e-e^T A e) <= sigma`.**

Consequently the T-P5-144 quotient packet keeps its exact

`b_eff=b_M-L^T b_N`,

`H_eff=H_MM-L^T A L`,

and pays only

**`C_bar=C+(b_N^T u+r^T u)/4+sigma/4`.**

If an exact correction is later supplied, the entire conservatism is exactly `(sigma-rho)/4`.

The corresponding obstruction is equally sharp: any nonzero residual component in `ker A`, however numerically small, produces an unbounded affine ray because the semidefinite physical cell gives that direction zero geometric cost.
