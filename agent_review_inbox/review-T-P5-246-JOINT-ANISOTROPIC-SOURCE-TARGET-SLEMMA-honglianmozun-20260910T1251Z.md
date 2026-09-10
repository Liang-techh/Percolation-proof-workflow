---
kind: review_result
review_id: review-T-P5-246-joint-anisotropic-source-target-slemma-honglianmozun-20260910T1251Z
task_id: T-P5-246-JOINT-ANISOTROPIC-SOURCE-TARGET-SLEMMA
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T12:51:00Z
claim_commit: ff17dfceb339284aa034f631476569691c1c1183
inspected_commit: c472530e93129c6972b0ee8354327ea8b6b0e9d5
upstream_commits:
  - bfe7ba1932c69dad624c270495f7c87ee5722d5f  # T-P5-245 anisotropic source trust-region reserve
  - fb6c28d0f7492fc1f21856835e4c11a20047beed  # T-P5-244 source-ellipsoid outward sensitivity
  - e8ba5dc69b700621893313a4202255a98267ebef  # T-P5-243 strict-margin coefficient-error budget
  - aa8124d17a0bfbed3572ed7cd3c20cdbe924964e  # T-P5-242 2D cubic S-lemma elimination
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_joint_source_target_recentering_congruence; add_effective_recentered_error_packet; add_fraction_free_full_block_reserve_transfer; add_translation_covariance_zero_cost_corollary; preserve_source_coverage_float64_and_admission_gates
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact affine quadratic expansion, S-lemma congruence algebra, Schur/adjugate fraction-free completion, rational PSD regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-246 — Joint anisotropic source-target S-lemma and affine recentering

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-243 gives a fixed-source coefficient-error budget. T-P5-244/T-P5-245 give increasingly sharp source-motion budgets while keeping the target fixed. Their sequential composition is deliberately one-sided: move/enlarge the source, then pay target errors. That can lose an arbitrarily large amount of Lyapunov reserve when source motion and target-coefficient motion are correlated.

This child closes the smallest exact correlation seam.

For a perturbed quadratic target

`q'(y)=A' + 2 l'^T y + y^T G' y`

on a shifted anisotropic source

`E'={y:(y-h)^T M' (y-h)<=R'}`,

we first recenter by `z=y-h`. The shift does not need to be bounded by a norm. It produces the exact effective coefficients

`A_h=A'+2 l'^T h+h^T G' h`,

`l_h=l'+G'h`,

`G_h=G'`.

The shifted-source S-lemma block is congruent to the ordinary centered-source block. Hence source translation and target coefficient changes should be combined **before** any one-sided error charging. In particular, a target translated covariantly with its source has exactly zero translation cost: the base S-lemma certificate is recovered verbatim after recentering, no matter how large the absolute translation is.

Relative to a frozen strict base packet, the entire joint perturbation is one symmetric block. A fraction-free adjugate congruence converts the base certificate to `diag(d^2 K,dN)` and the joint perturbation to an exact rational block. This gives both:

- an exact fixed-multiplier/fixed-joint-multiplier PSD decision; and
- a reserve-fraction theorem that proves strict safety while retaining an explicit fraction of the original Lyapunov block margin.

A rational 2D regression shows a strict PASS that every source-first radial charging route misses: translating the unit ball by `(2,0)` makes the base-metric radius jump from `1` to `9`, but translating the target by the same amount leaves the entire centered S-lemma packet unchanged.

No actual P5 source/target pair, same-key binding, cell/tube/trajectory coverage, Float64/interval semantics, Lean/kernel receipt, independent validation, admission, registry mutation, or P5/P8/M4 parent closure is claimed.

---

# Part I — exact joint recentering

## 1. Perturbed source and target

Let

`M' in S_{++}^n`, `R'>0`, `h in R^n`,

and

`q'(y)=A'+2 l'^T y+y^T G'y`, `G'=G'^T`.

The admissible source is

`E'={y:(y-h)^T M'(y-h)<=R'}`.

Set

`z:=y-h`, so `y=z+h`.

Then

`q'(z+h)`

`=A'+2l'^T(z+h)+(z+h)^TG'(z+h)`

`=[A'+2l'^Th+h^TG'h]`

` +2[l'+G'h]^T z`

` +z^TG'z`.

Define

**`A_h:=A'+2l'^Th+h^TG'h`,**

**`l_h:=l'+G'h`,**

**`G_h:=G'`.**

Therefore

**`q'(z+h)=A_h+2l_h^Tz+z^TG_hz`.**

The source becomes the centered ellipsoid

**`z^TM'z<=R'`.**

This is an identity, not a relaxation.

---

## 2. Shifted and centered S-lemma blocks

For a multiplier `mu>=0`, define the block in the original `y` coordinates

`S_y(mu):=`

`[[mu M'-G',          -l'-mu M'h],`

` [-l'^T-mu h^TM', -A'-mu R'+mu h^TM'h]]`.

Indeed

`[y;1]^T S_y(mu)[y;1]`

`=-q'(y)-mu(R'-(y-h)^TM'(y-h))`.

After recentering, define

`S_z(mu):=`

`[[mu M'-G_h, -l_h],`

` [-l_h^T, -A_h-mu R']]`.

Let

`T_h=[[I,h],[0,1]]`, so `[y;1]=T_h[z;1]`.

Then direct expansion gives the exact congruence

**`S_z(mu)=T_h^T S_y(mu) T_h`.**

Because `T_h` is invertible and `det T_h=1`, we obtain simultaneously

**`S_y(mu)>=0 <=> S_z(mu)>=0`,**

and

**`det S_y(mu)=det S_z(mu)`.**

Thus the translated source should be handled by an affine congruence, not by first replacing it with a larger centered ball.

---

# Part II — lossless joint source-target S-lemma

## 3. Exact safety theorem

Since `M'>0` and `R'>0`, the centered source has strict Slater point `z=0`.

By the one-constraint lossless S-lemma,

**Theorem A — `jointShiftedSourceTarget_slemma`.**

The following are equivalent:

1. `q'(y)<=0` for every `y` satisfying `(y-h)^TM'(y-h)<=R'`;
2. there exists `mu>=0` with `S_y(mu)>=0`;
3. there exists `mu>=0` with `S_z(mu)>=0`.

This is the exact joint problem. No intermediate scalar radius, Loewner factor, norm bound, or separate coefficient budget is required.

### Radius-zero branch

If `R'=0`, Slater is absent and `E'={h}`. The exact test is simply

**`q'(h)<=0`.**

Do not invoke the S-lemma branch in this degenerate case.

---

# Part III — effective perturbations relative to a frozen base packet

## 4. Base packet

Let the base source and target be

`E={y:y^TMy<=R}`, `M>0`,

`q(y)=A+2l^Ty+y^TGy`, `G=G^T`.

Fix a base multiplier `lambda>=0` and define

`K:=lambda M-G`,

`c:=-A-lambda R`,

`S0:= [[K,-l],[-l^T,c]]`.

Assume the strict regular packet

**`K>0`**

and

**`epsilon:=c-l^TK^{-1}l>0`.**

Equivalently, `S0>0`.

Write the perturbed target as

`A'=A+DeltaA`,

`l'=l+Deltal`,

`G'=G+DeltaG`.

After recentering by the perturbed source center `h`, define the **effective recentered target errors**

**`deltaG := DeltaG`,**

**`deltal_h := Deltal + (G+DeltaG)h`,**

**`deltaA_h := DeltaA + 2(l+Deltal)^T h + h^T(G+DeltaG)h`.**

Then

`G_h=G+deltaG`,

`l_h=l+deltal_h`,

`A_h=A+deltaA_h`.

These combinations, not `h`, `DeltaA`, `Deltal`, and `DeltaG` separately, are what the Lyapunov certificate actually sees after source recentering.

---

## 5. One exact joint difference block

For any candidate perturbed-source multiplier `mu>=0`, define

`E(mu):=S_z(mu)-S0`.

Using the effective errors above,

**`E(mu)=`**

`[[mu M'-lambda M-deltaG, -deltal_h],`

` [-deltal_h^T, lambda R-mu R'-deltaA_h]]`.

Therefore

**`S_z(mu)=S0+E(mu)`.**

This is the desired joint source-target error packet. Directional cancellation is preserved automatically:

- source metric/radius motion enters the diagonal terms with the same multiplier `mu`;
- source translation is first absorbed into `deltaA_h,deltal_h`;
- target linear/quadratic changes can cancel translation-generated terms exactly;
- no absolute value is taken before the final PSD decision.

### Theorem B — `jointPerturbation_fixedMu_exact`

For any fixed `mu>=0`,

**`S_z(mu)>=0 <=> S0+E(mu)>=0`.**

Combined with Theorem A, existence of such a `mu` is exactly the joint safety question.

The identity is algebraically elementary, but it is the missing interface needed to prevent the sequential T-P5-243/T-P5-244/T-P5-245 budgets from destroying source-target correlation.

---

# Part IV — fraction-free full-block reserve coordinates

## 6. Adjugate completion of the strict base certificate

Assume rational data and rational `lambda`, with `K>0`.

Set

`d:=det K>0`,

`J:=adj(K)`,

`u:=J l`,

`N:=d c-l^T u`.

Then

`epsilon=N/d`,

and strictness is exactly `N>0`.

Define the integer/rational congruence matrix

**`That := [[d I,u],[0,d]]`.**

Since `d>0`, `That` is invertible. Using `KJ=dI` and `Ku=dl`, direct multiplication gives

**`That^T S0 That = D0`,**

where

**`D0:=diag(d^2 K, dN) >0`.**

This is the fraction-free version of completing the square around `K^{-1}l`.

No inverse is stored in the certificate.

---

## 7. Fraction-free joint perturbation block

Write

`E(mu)=[[A_mu,b_mu],[b_mu^T,r_mu]]`,

where

`A_mu:=mu M'-lambda M-deltaG`,

`b_mu:=-deltal_h`,

`r_mu:=lambda R-mu R'-deltaA_h`.

Then exact multiplication gives

**`Ehat(mu):=That^T E(mu) That`**

`= [[d^2 A_mu, d A_mu u+d^2 b_mu],`

`   [(...)^T, u^T A_mu u+2d b_mu^T u+d^2 r_mu]]`.

Hence

**`That^T S_z(mu) That = D0+Ehat(mu)`.**

Because congruence by `That` is invertible:

### Theorem C — `jointPerturbation_fractionFree_exact`

**`S_z(mu)>=0 <=> D0+Ehat(mu)>=0`.**

For rational `mu` and rational source/target data, every entry of this packet is rational. The trusted checker needs only exact matrix arithmetic and a PSD test; no inverse, square root, pseudoinverse, or eigenvector is required.

---

## 8. Retained reserve fraction

The exact fixed-`mu` test corresponds to consuming up to the whole base block reserve. Often one wants a strict reserve left for later FD/DH/Float64 debits.

Let `0<=rho<1`. If

**`Ehat(mu)+rho D0 >=0`,**

then by inverse congruence

`E(mu)+rho S0>=0`.

Therefore

`S_z(mu)`

`=(1-rho)S0 + [E(mu)+rho S0]`

`>= (1-rho)S0 >0`.

Thus:

### Theorem D — `jointPerturbation_retainedReserveFraction`

If `0<=rho<1` and `Ehat(mu)+rho D0>=0`, then the perturbed target is strictly safe on the perturbed source, and the S-lemma block retains at least the positive-definite reserve `(1-rho)S0`.

At `rho=1`, the condition reduces to the exact fixed-`mu` PSD test `D0+Ehat(mu)>=0`, but no strict reserve is guaranteed.

This is stronger structurally than a scalar vertical budget: it allows the perturbation to borrow directionally from the entire base quadratic certificate while still keeping a chosen fraction untouched.

---

# Part V — exact translation covariance

## 9. Covariantly translated source and target cost exactly zero

Take

`M'=M`, `R'=R`,

and translate the target with the source:

**`q'(y):=q(y-h)`.**

Expanding gives

`DeltaG=0`,

`Deltal=-Gh`,

`DeltaA=-2l^Th+h^TGh`.

The effective recentered errors are then

`deltal_h=-Gh+Gh=0`,

and

`deltaA_h`

`=(-2l^Th+h^TGh)+2(l-Gh)^Th+h^TGh`

`=0`.

Also `deltaG=0`.

Choose `mu=lambda`. Then

**`E(lambda)=0`.**

Hence

**`S_z(lambda)=S0`.**

This proves:

### Theorem E — `slemmaTranslationCovariance`

If the source ellipsoid and the quadratic target are translated by the same vector, the entire S-lemma/Lyapunov certificate is unchanged after recentering. Absolute translation amplitude has **zero** mathematical cost.

This is a structural fingerprint:

**common translation -> affine recentering -> exact target/source cancellation -> identical Lyapunov block.**

Any error budget that charges `||h||` and the induced target coefficient changes independently can therefore become arbitrarily conservative.

---

## 10. Only relative source-target translation matters

A useful refinement is to distinguish a source center `h_s` from a target translation `h_q`.

Suppose

`E_s={y:(y-h_s)^TM(y-h_s)<=R}`

and

`q_q(y)=q(y-h_q)`.

Recenter the source by `z=y-h_s` and define

**`delta:=h_s-h_q`.**

Then

`q_q(z+h_s)=q(z+delta)`.

Therefore the recentered coefficients are

`G_delta=G`,

`l_delta=l+G delta`,

`A_delta=A+2l^Tdelta+delta^TGdelta`.

The absolute locations `h_s,h_q` disappear. The safety problem depends only on the **relative translation mismatch** `delta`.

This is the exact obstruction to treating translation as a free gauge: common motion (`delta=0`) is free, mismatched motion is a real target perturbation.

---

# Part VI — rational separation regression

## 11. Base packet

Take dimension two and

`M=I_2`, `R=1`,

`q(y)=||y||^2-2`.

Thus

`A=-2`, `l=0`, `G=I_2`.

Choose

**`lambda=3/2`.**

Then

`K=lambda I-I=(1/2)I>0`,

`c=2-3/2=1/2`,

and

**`S0=diag(1/2,1/2,1/2)>0`.**

The vertical reserve is `epsilon=1/2`, so the T-P5-244/T-P5-245 fixed-radial envelope allows only

`B=R+epsilon/lambda`

`=1+(1/2)/(3/2)`

**`=4/3`.**

---

## 12. Move the source by two units and translate the target with it

Let

`h=(2,0)`,

`M'=I_2`, `R'=1`,

and

`q'(y)=||y-h||^2-2`.

In the original coordinates,

`q'(y)=||y||^2-4y_1+2`,

so relative to the base target

`DeltaA=4`,

`Deltal=(-2,0)`,

`DeltaG=0`.

The source is the shifted unit ball

`||y-h||^2<=1`.

### Separate source charging misses immediately

The maximum base-metric radius on this shifted source is

`max ||y||^2=(||h||+1)^2=9`.

But the frozen radial reserve only allows `B=4/3`.

Thus a source-first T-P5-245 radial transfer cannot certify the moved source under the frozen target packet. The target perturbation is also large (`DeltaA=4`, `Deltal=(-2,0)`), so separately charging target and source motion loses the exact cancellation.

### Joint recentering is exact

The effective errors are

`deltal_h=(-2,0)+(2,0)=0`,

and

`deltaA_h=4+2(-2,0)^T(2,0)+(2,0)^T(2,0)`

`=4-8+4=0`.

Also `deltaG=0`, `M'=M`, `R'=R`.

Hence with `mu=lambda=3/2`,

**`E(mu)=0`**

and therefore

**`S_z(mu)=S0`.**

The full strict Lyapunov reserve is retained: Theorem D holds already with `rho=0`.

For an independent check in the original `y` coordinates,

`S_y(3/2)=`

`[[1/2,0,-1],`

` [0,1/2,0],`

` [-1,0,5/2]]`.

Its leading principal minors are exactly

`1/2`, `1/4`, `1/8`,

so it is positive definite.

Thus the joint theorem gives a strict exact PASS while the source-first scalar/radial route reports only **reserve not covered**.

This separation can be made arbitrarily large: replace `h=(2,0)` by `(t,0)`. The joint recentered certificate stays identical for every `t`, while the base-metric radius of the moved source grows as `(|t|+1)^2`.

---

# Part VII — a real obstruction when covariance is absent

## 13. Moving only the source is not a free gauge

Keep the same base target

`q(y)=||y||^2-2`,

but move only the source to `h=(2,0)` and do **not** translate the target.

The shifted unit ball contains `y=(3,0)`, and

`q(3,0)=9-2=7>0`.

After source recentering, `z=e1` corresponds to that point, and

`q(z+h)=||z||^2+4z_1+2`.

The effective recentered errors are nonzero; there is no common-translation cancellation.

Therefore the correct rule is not “source translation is harmless.” The correct rule is:

**common source-target translation is a congruence symmetry; relative translation mismatch is a physical Lyapunov debit.**

This regression prevents an invalid gauge interpretation.

---

# Part VIII — relation to the 2D cubic classifier

## 14. Joint perturbations remain cubic in dimension two

For `n=2`, after recentering define

`K_mu:=mu M'-G_h`,

`c_mu:=-A_h-mu R'`.

On the regular branch `K_mu>0`,

`S_z(mu)>=0`

iff

**`p(mu):=det(K_mu)c_mu-l_h^T adj(K_mu)l_h >=0`.**

Because `det(K_mu)` is quadratic in `mu`, `adj(K_mu)` is affine, and `c_mu` is affine,

**`p(mu)` is cubic.**

The leading coefficient is

**`-R' det(M')<0`.**

Therefore the T-P5-242 spectral-floor / singular-hard / cubic-local-maximum machinery applies **without change** after substituting the effective recentered coefficients `(A_h,l_h,G_h,M',R')`.

This is useful operationally: joint source-target correlation does not increase the algebraic degree of the 2D exact classifier.

For rational source/target data and rational `h`, all recentered coefficients are rational. Under strict safety, the existing density argument again permits a rational regular multiplier, so a stored strict certificate need not contain algebraic roots.

---

# Part IX — checker-facing theorem skeletons

## 15. Candidate statements

A minimal theorem decomposition is:

1. `quadraticTarget_recenter`
   - proves the exact formulas for `A_h,l_h,G_h`.

2. `shiftedSlemmaBlock_congruent_centered`
   - proves `S_z=T_h^T S_y T_h` and PSD/determinant invariance.

3. `jointShiftedSourceTarget_slemma`
   - under `M'>0,R'>0`, equates safety with existence of `mu>=0` and centered block PSD.

4. `effectiveRecenteredError_blockIdentity`
   - proves the exact `E(mu)` formula relative to a frozen base `S0`.

5. `fractionFreeBaseCompletion`
   - proves `That^T S0 That=diag(d^2K,dN)`.

6. `jointPerturbation_fractionFree_exact`
   - proves `S_z(mu)>=0 <=> D0+Ehat(mu)>=0`.

7. `jointPerturbation_retainedReserveFraction`
   - `Ehat+rho D0>=0`, `0<=rho<1` implies strict safety with residual block reserve.

8. `slemmaTranslationCovariance`
   - common source-target translation gives `E(lambda)=0`.

9. `relativeTranslationMismatch_only`
   - source/target translations reduce to the single mismatch `delta=h_s-h_q`.

These are pure finite-dimensional quadratic-energy statements. A future Lean child may formalize them, but this review does not claim compilation.

---

# Part X — failure semantics and boundaries

## 16. Fail-closed rules

1. **No source binding, no physical closure.** The theorem packet is source-independent until actual P5 `M',R',h,A',l',G'` are bound to the same deployed source/key/cell.

2. **`R'=0` is separate.** Do not invoke the Slater S-lemma when the source is a singleton.

3. **Recenter before charging.** Bounding `h`, `DeltaA`, `Deltal`, and `DeltaG` independently may destroy exact cancellation. Use the effective recentered coefficients when the source/target relation is known.

4. **Common translation requires actual covariance.** If the deployed target is not literally the translated base target, Theorem E does not apply. Relative mismatch remains a real debit.

5. **Fixed-`mu` miss is not mathematical failure.** If one rational `mu` fails the PSD packet, another `mu` may work. Only the complete S-lemma multiplier decision can reject the joint quadratic target on the whole ellipsoid.

6. **Packet failure is not trajectory failure.** Even if the full ellipsoid contains a positive-debit point, a smaller reachable set may exclude it; that requires an independent trajectory/domain witness.

7. **Strict block reserve is not Float64 reserve.** Any floating evaluator, FD/DH halo, interval rounding, or source-coefficient error must still be charged through a separately bound packet.

Suggested nonterminal failure label:

**`JOINT_SOURCE_TARGET_SLEMMA_PACKET_NOT_CLOSED`.**

---

# Part XI — structural fingerprint and next seam

## 17. New structural fingerprint

The exact mechanism exposed here is

**shifted anisotropic source + correlated quadratic target change**

`-> affine source recentering`

`-> effective target errors `(deltaA_h,deltal_h,deltaG)``

`-> one joint S-lemma block`

`-> fraction-free full-block Lyapunov reserve`

`-> common translations cancel exactly`

`-> only relative source-target mismatch consumes reserve`.

This is distinct from scalar support/error bounds: it is a symmetry/covariance mechanism of the quadratic energy certificate itself.

## 18. Recommended next mathematical seam

The next genuinely distinct step is **full invertible affine chart covariance** rather than translation only.

For `y=Pz+h` with rational invertible `P`, the source and target quadratic blocks transform by the augmented congruence `diag-affine(P,h)`. Proving a fraction-free `GL(n)` transport theorem would let different local P5 charts share one Lyapunov certificate without treating chart scaling/shear as physical coefficient error. The key boundary is to separate exact coordinate covariance from a genuinely approximate/nonlinear chart, where a Lie/second-order defect must be charged.

Until an actual source packet requires that extension, the current result already closes the exact joint translation/source-target correlation seam left by T-P5-245.

---

## 19. Non-claims

This child does not establish:

- actual P5 same-key source/target equality;
- actual perturbation or center-shift values;
- tube/cell/trajectory/FD-halo coverage;
- Float64/interval enclosure;
- a Lean/kernel receipt;
- independent validation by 封不觉;
- admission/registry eligibility;
- P5/P8/M4 parent closure.

Status remains **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding**.