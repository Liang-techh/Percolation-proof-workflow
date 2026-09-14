---
kind: review_result
review_id: review-T-P5-209-weak-reference-residual-contact-threshold-guyuefangyuan-20260910T0320Z
task_id: T-P5-209-WEAK-REFERENCE-RESIDUAL-CONTACT-THRESHOLD
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T03:20:00Z
claim_commit: f787673ba8f32da466259c8556c07e7488d63076
inspected_commit: 2bd2d321e09d5572152b92da3415d5465f280298
upstream_commits:
  - f3c7325dd1cb49f0e93523c11bed546502e77981  # T-P5-205 copositive reference reserve extraction
  - 84f4d490036164a8a7654c2781f7dea8864cb695  # T-P5-208 ray-threshold contact/support bridge
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_weak_reference_zero_face_compatibility; add_common_zero_residual_ceiling; add_zero_debit_residual_contact_exact_threshold; add_persistent_support_residual_root_branch; add_two_level_contact_dispatcher
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact copositive zero-contact perturbation; affine inactive-residual algebra; exact rational 2x2 regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-209 — weak-reference zero-debit residual contact and exact ray threshold

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-208 proves exact ray-threshold attainment from a **strictly copositive** reference and proves sharpness from a zero contact carrying strictly positive debit energy. It explicitly leaves the weak-reference case open because the normalized ratio can approach its supremum on a zero-reference face where both numerator and denominator vanish.

This child identifies the missing first-order mechanism.

For a weakly copositive reference, the exact endpoint may be sharp even though **no positive-debit zero state exists at the endpoint**. The endpoint can instead be detected by a state `z` that remains a zero-energy state of the whole pencil while one inactive orthant residual reaches zero. Increasing the debit parameter then makes that residual negative, and the T-P5-208 perturbation argument immediately produces a nearby negative quadratic witness.

The resulting branch is especially useful on the persistent-singular support strata that T-P5-208 deliberately did not classify: the active principal block may be singular for every parameter value, so there is no determinant root to find, while an inactive residual is an affine function of the ray parameter and gives the exact endpoint.

No actual P5 source matrices, selector/cell/tube binding, global coverage, Float64 enclosure, Lean/kernel proof, independent 封不觉 verification, admission, registry promotion, or parent closure is claimed.

---

## 1. Setup

Let `C,Q` be real symmetric `n x n` matrices and define

`M(t) := C - t Q`, `t>=0`.

Assume throughout the main ray statements that

- `C` is copositive;
- `Q` is copositive.

For `x>=0`, write

`c(x) := x^T C x`,

`q(x) := x^T Q x`,

`m_t(x) := x^T M(t)x = c(x)-t q(x)`.

Let

`T := {t>=0 : M(t) is copositive}`.

As in T-P5-208, `T` is downward closed: if `t in T` and `0<=s<=t`, then

`M(s)=M(t)+(t-s)Q`

is a sum of copositive matrices.

The new issue is what happens when `C` is only weakly copositive and a normalized minimizing sequence approaches a zero of `C`.

---

## 2. T209-A — every positive safe radius imposes a two-level zero-face compatibility condition

Suppose there exists `t0>0` such that `M(t0)` is copositive. Let `z>=0`, `z!=0`, satisfy

`c(z)=0`.

Because `Q` is copositive, `q(z)>=0`. Copositivity of `M(t0)` gives

`0 <= m_t0(z) = -t0 q(z)`.

Hence necessarily

**`q(z)=0`.**

Therefore every zero of the reference must also be a zero of the debit if any strictly positive safe radius exists.

But zero-energy compatibility is not enough. Since

`z^T M(t0)z=0`

and `M(t0)` is copositive, the T-P5-208 zero-contact lemma gives

`M(t0)z >= 0`.

Thus

**`Cz >= t0 Qz` coordinatewise.**

Since `C` and `Q` are themselves copositive and both vanish quadratically at `z`, their zero-contact residuals satisfy

`Cz>=0`, `Qz>=0`.

Consequently, for every coordinate `i`,

**`(Cz)_i=0  =>  (Qz)_i=0`.**

Equivalently,

**`supp_+(Qz) subset supp_+(Cz)`.**

This is the first missing weak-reference condition behind T-P5-208's warning about zero faces.

### Immediate zero-radius obstructions

A reference zero `z` kills every positive ray radius in either of two ways:

1. **zeroth-order obstruction:** `q(z)>0`;
2. **first-order obstruction:** `q(z)=0` but some coordinate has `(Cz)_j=0<(Qz)_j`.

The first makes the quadratic value itself negative for every `t>0`. The second keeps the quadratic value zero at `z`, but makes the orthant residual negative for every `t>0`, so a nearby perturbation has negative quadratic value.

Thus merely checking `q(z)=0` on the zero set of `C` is not a sufficient weak-reference adapter.

---

## 3. T209-B — common-zero residual ceilings

Fix a nonzero `z>=0` such that

`c(z)=0`, `q(z)=0`.

Because both matrices are copositive zero contacts,

`a := Cz >=0`,

`b := Qz >=0`.

For every safe `t in T`, the same state remains a zero of the pencil:

`z^T M(t)z = 0`.

Therefore copositivity forces

`M(t)z = a-tb >=0`.

For each coordinate with `b_j>0`, this gives the exact scalar upper bound

`t <= a_j/b_j`.

Define the **residual ceiling**

`tau_res(z) := min_{j : b_j>0} a_j/b_j`

when `b` has at least one positive coordinate. Then

**`T subset [0,tau_res(z)]`.**

No generalized eigenvalue, determinant, square root, inverse, or optimizer is involved. For rational source data the candidate ratios are rational.

If `b=0`, this particular common zero gives no first-order ray ceiling; the next information must come from a different contact or from a second-order critical/tangent reduction.

---

## 4. T209-C — zero-debit residual contact is an exact sharp-threshold certificate

The ratio notation above is convenient for discovery, but the actual theorem is division-free.

Let `t>=0`. Assume:

1. `M(t)` is copositive;
2. `z>=0`, `z!=0`;
3. `z^T M(t)z=0`;
4. `q(z)=0`;
5. for some coordinate `j`, `(M(t)z)_j=0` and `(Qz)_j>0`.

### Theorem

**`t` is the exact endpoint of the safe ray `T`.**

That is,

- `M(s)` is copositive for every `0<=s<=t`;
- `M(s)` is not copositive for every `s>t`.

### Safe side

For `0<=s<=t`,

`M(s)=M(t)+(t-s)Q`,

so copositivity follows from the copositivity of `M(t)` and `Q`.

### Unsafe side

Since `q(z)=0`,

`z^T M(s)z = z^T M(t)z -(s-t)q(z)=0`

for every `s`.

But the selected residual changes as

`(M(s)z)_j`

`= (M(t)z)_j -(s-t)(Qz)_j`

`= -(s-t)(Qz)_j <0`

for every `s>t`.

Now perturb in the nonnegative coordinate direction:

`x_eps := z + eps e_j >=0`.

Then

`x_eps^T M(s)x_eps`

`= 2 eps (M(s)z)_j + eps^2 M(s)_jj`.

The linear coefficient is strictly negative, so the expression is negative for all sufficiently small `eps>0`. Hence `M(s)` is not copositive.

QED.

### Why `j` is automatically inactive in the common-zero branch

If additionally `q(z)=0` and `Q` is copositive, then `Qz>=0` and complementarity gives

`z_i(Qz)_i=0` for every `i`.

Therefore `(Qz)_j>0` implies `z_j=0`. The sharpness witness is genuinely an **inactive-residual contact**, not a signed perturbation through a positive support coordinate.

---

## 5. T209-D — persistent active support turns the residual ceiling into a linear root branch

Let

`S := supp(z)`, `J:=S^c`,

and assume the common-zero hypotheses

`c(z)=q(z)=0`.

Write `z_S>0` for the support restriction.

Since `C` is copositive and `c(z)=0`, T-P5-208 complementarity gives

`C[S,S] z_S=0`.

Likewise,

`Q[S,S] z_S=0`.

Hence for **every** ray parameter `t`,

**`M(t)[S,S] z_S=0`.**

Therefore

**`det M(t)[S,S] = 0` for every `t`.**

This support lies in a persistent singular pencil branch. A regular determinant-root dispatcher cannot locate the threshold because the active determinant is identically zero along the ray.

The first nontrivial support condition is instead the inactive residual

`r_J(t) := M(t)[J,S] z_S`

`= C[J,S]z_S - t Q[J,S]z_S`.

Both coefficient vectors are nonnegative. Each row with positive debit residual gives one affine ceiling, and the first row to hit zero gives `tau_res(z)`.

### Exact persistent-support theorem

Suppose `Q[J,S]z_S` has a positive entry and let `tau=tau_res(z)`. If

**`M(tau)` is globally copositive,**

then

**`T=[0,tau]`.**

Proof: at least one inactive row `j` satisfies `r_j(tau)=0` with positive debit residual, so T209-C applies.

This is the weak-reference analogue of T-P5-208's positive-debit support contact, but it lives precisely in the branch where the active principal determinant never leaves zero.

---

## 6. T209-E — exact rational / division-free packet

Suppose a candidate threshold is represented as

`t=p/r`, with `p>=0`, `r>0`.

Instead of dividing, define the scaled candidate matrix

`H := r C - p Q`.

A source/checker packet may verify:

1. `H` is copositive;
2. `z>=0`, `z!=0`;
3. `z^T C z=0`;
4. `z^T Q z=0`;
5. `Hz>=0`;
6. for some `j`, `(Hz)_j=0` and `(Qz)_j>0`.

Because positive scaling preserves copositivity, item 1 is the safe-side certificate for `M(p/r)`. Items 3--4 imply `z^T H z=0`. Item 6 is the residual saturation.

Therefore `p/r` is the exact ray endpoint.

All source-facing arithmetic is matrix-vector multiplication, dot products, integer/rational addition and multiplication, equality, and order comparison. There is no root reification at all on this branch.

If the candidate is discovered from a fixed common zero, one may equivalently scan the finite set of cross-multiplied residual ratios:

`r a_j - p b_j >=0`

for all `j`, with equality at one `j` satisfying `b_j>0`.

---

## 7. Regression 1 — a sharp weak-reference threshold with no positive-debit zero contact

Take

`C = [[1,1],[1,0]]`,

`Q = [[0,1],[1,0]]`.

For `x,y>=0`,

`[x,y] C [x,y]^T = x^2+2xy >=0`,

`[x,y] Q [x,y]^T = 2xy >=0`.

Thus both matrices are copositive, but `C` is only weakly copositive because it vanishes on the ray `z=e_2`.

The pencil is

`M(t) = [[1,1-t],[1-t,0]]`,

with quadratic form

`m_t(x,y)=x^2+2(1-t)xy`.

### Safe side

If `0<=t<=1`, both coefficients are nonnegative, so `M(t)` is copositive.

### Unsafe side

Let `h=t-1>0` and choose `(x,y)=(h,1)`. Then

`m_t(h,1)=h^2-2h^2=-h^2<0`.

Hence the exact threshold is

**`t_*=1`.**

At the endpoint,

`M(1)=diag(1,0)`.

Every nonzero zero contact has `x=0`; therefore

`q(x,y)=2xy=0`

on every endpoint zero contact. In particular there is **no** T-P5-208 positive-debit zero contact that could certify sharpness.

Nevertheless, with `z=e_2`,

`Cz=(1,0)`,

`Qz=(1,0)`.

Thus the inactive first coordinate has residual

`(M(t)z)_1 = 1-t`,

which hits zero exactly at `t=1` and becomes negative immediately afterwards. T209-C detects the exact endpoint.

### Ratio nonattainment

On the normalized simplex with `x>0,y>0`,

`q/c = 2xy/(x^2+2xy) <1`,

but as `x -> 0+` with `y>0`,

`q/c -> 1`.

The supremum is approached at the weak-reference zero face, where both `c` and `q` vanish, and is not attained by a positive-debit state. This is exactly why T-P5-208's strict-reference compact-ratio proof cannot simply be reused.

---

## 8. Regression 2 — zero-energy compatibility alone does not buy any positive radius

Take

`C = [[1,0],[0,0]]`,

`Q = [[0,1],[1,0]]`.

Again both matrices are copositive. The only normalized reference zero is `z=e_2`, and

`q(z)=0`.

So a checker that tests only

`c(z)=0 => q(z)=0`

would incorrectly believe the zero face is harmless.

But

`Cz=(0,0)`,

`Qz=(1,0)`.

Thus the first-order compatibility condition fails in coordinate 1. For every `t>0`,

`(M(t)z)_1=-t<0`.

Equivalently, choosing `(x,y)=(t,1)` gives

`m_t(t,1)=t^2-2t^2=-t^2<0`.

Therefore

**the exact safe threshold is `0`.**

This regression should prevent the source adapter from promoting mere zero-set inclusion `Z(C) subset Z(Q)` to a positive reserve/error radius.

---

## 9. Two-level contact dispatcher

The weak-reference ray can now be routed by contact order.

### Level 0 — energy contact

If a safe candidate `t` has a contact `z>=0` with

`z^T M(t)z=0`,

`z^TQz>0`,

then T-P5-208 proves exact sharpness: increasing `t` makes the same state's quadratic value negative.

### Level 1 — residual contact

If all endpoint contacts have zero debit energy, search the common-zero supports. If there exists `z` with

`z^TCz=z^TQz=0`

and a positive debit residual coordinate satisfying

`(M(t)z)_j=0`, `(Qz)_j>0`,

then T209 proves exact sharpness: increasing `t` preserves zero energy at `z` but makes an inactive residual negative.

### Deeper branch

If a common zero also satisfies

`Qz=0`

as a full vector, then that state provides neither a Level-0 nor Level-1 ceiling. One must descend to the second-order critical/tangent cone or find another contact/support. This is naturally compatible with the existing T-P5-179/T-P5-183 mixed-cone and Schur machinery.

This child does **not** claim that Level 0 plus Level 1 is a complete classifier for all weakly copositive pencils. It only adds a new exact branch and exact obstructions.

---

## 10. Source-facing implications

For a weak-reference source packet, before attempting a compact ratio search, perform zero-face checks in the following logical order:

1. if a reference zero has positive debit energy, the positive safe radius is exactly impossible;
2. if debit energy also vanishes, compare the zero-contact residuals `Cz` and `Qz`;
3. a positive `Qz_j` with zero `Cz_j` again collapses the safe radius to zero;
4. otherwise every positive `Qz_j` gives a rational first-order upper bound on the ray parameter;
5. if a globally copositive candidate reaches one such residual bound, it is an exact endpoint by T209-C;
6. if `Qz=0`, retain the support as a deeper critical-cone obligation rather than declaring PASS.

In particular, a persistent singular active block is not a dead end. Its inactive residual pencil may contain the sharp threshold in a much simpler affine form than the determinant/root route.

---

## 11. Suggested minimal Lean leaves

The mathematics can be split into small leaves:

1. `positiveRay_copositive_zeroFace_debitZero`
   - `Copositive Q`, `Copositive (C-t*Q)`, `t>0`, `z>=0`, `z^TCz=0`;
   - conclude `z^TQz=0`.

2. `positiveRay_zeroFace_residual_domination`
   - under the same hypotheses;
   - conclude `Cz >= t Qz` coordinatewise.

3. `commonZero_residual_ray_bound`
   - `z^TCz=z^TQz=0`, safe `M(t)`;
   - conclude `Cz-tQz>=0`.

4. `zeroDebit_residualContact_exactRayThreshold`
   - safe candidate, zero debit energy, saturated positive debit residual;
   - conclude every larger parameter is noncopositive by `z+eps e_j`.

5. `commonZero_activeKernel_persistent`
   - support restriction gives `C_SS z_S=Q_SS z_S=0`;
   - conclude `M(t)_SS z_S=0` for every `t`.

6. `persistentSupport_residualCeiling_exact`
   - finite inactive minimum plus global copositivity at the candidate;
   - conclude exact ray endpoint.

7. `scaledResidualContact_exactRayThreshold`
   - rational packet `H=rC-pQ` with `r>0`;
   - avoid division in the checker-facing theorem.

The two 2x2 regressions above should be formalized with `norm_num`/`ring_nf` once the generic leaves exist.

---

## 12. Boundaries remaining OPEN

This review does **not** prove:

1. a complete characterization of the radial cone of the copositive cone at an arbitrary weak reference;
2. sufficiency of zero-face residual compatibility when all Level-0 and Level-1 obstructions are absent;
3. the second-order critical-cone recursion when `Qz=0` on a common zero;
4. finite enumeration of all relevant weak-reference zero supports;
5. actual P5 `C,Q,z,p,r` source binding or selector/cell/tube identity;
6. global copositivity of any actual candidate threshold matrix;
7. Float64 / interval / trajectory / controller / PDE semantics;
8. Lean/kernel compilation or independent 封不觉 verification;
9. admission, registry eligibility, or parent theorem closure.

All remain external/pending.

---

## 13. Structural fingerprint

The new weak-reference branch is

**`reference zero z`**

`=> check debit energy q(z)`

`=> q(z)>0 : zero-radius energy obstruction`

or

`=> q(z)=0 : compare residuals Cz and Qz`

`=> Cz_j=0<Qz_j : zero-radius first-order obstruction`

or

`=> residual ceiling t <= (Cz)_j/(Qz)_j`

`=> global copositivity at a saturated candidate`

`=> persistent zero energy + negative residual immediately above`

`=> nearby orthant witness`

`=> exact ray threshold`.

The main interface lesson is:

**for weak copositive references, sharpness need not be carried by a positive-debit zero state. A persistent zero-energy support can lose safety one derivative later, through an inactive residual root. That residual root is the correct exact branch when the active determinant is identically singular.**
