---
kind: review_result
review_id: review-T-P5-208-ray-threshold-contact-support-bridge-liuguanyi-20260910T0300Z
task_id: T-P5-208-RAY-THRESHOLD-CONTACT-SUPPORT-BRIDGE
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T03:00:00Z
claim_commit: 0c588a505236189827e83a4449a8b38f0cd637f3
inspected_commit: cef966458475f2f5df7402a1bf64587a970cca62
upstream_commits:
  - 37f9f4fb4865e4bd61b0541636f46ba622d17ca7  # T-P5-204 support-slack Lyapunov margin
  - 5855b175ab9794baab7c72a878942d5d95b2d0ac  # T-P5-207 copositive error polar cuts
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_ray_threshold_attainment; add_contact_to_active_support_kernel; add_negative_inactive_residual_rejection; add_support_contact_exact_threshold; retain_persistent_singular_pencil_branch
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: compact-simplex extremum argument; exact copositive perturbation argument; principal-support kernel algebra; exact rational 2x2 regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-208 — ray-threshold contact to active-support kernel bridge

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-207 identifies the safe simultaneous support-error region as an intersection of state-wise halfspaces. Along a fixed nonnegative error profile this gives a scalar safe ray, but it leaves one important cross-layer seam implicit: when the ray reaches its exact boundary, how does the touching state become the support/kernel object consumed by the existing P5 principal-minor, contact, and support machinery?

This child closes that seam.

For a fixed error profile `d>=0`, write

`Q_d := sum_k d_k Q_k`,

`M(t) := C0 - t Q_d`.

Under a strictly copositive reference `C0` and a nontrivial copositive debit `Q_d`, the exact safe ray threshold is attained by a normalized orthant state `z`. At the threshold,

`z^T M(t_*) z = 0`.

Copositivity then forces the full one-sided KKT/contact relations

`M(t_*) z >= 0`,

`z_i (M(t_*)z)_i = 0` for every `i`.

If `S=supp(z)`, this becomes the active-support certificate

**`M(t_*)[S,S] z_S = 0`, `z_S>0`, and `M(t_*)[S^c,S] z_S >= 0`.**

Thus an exact error-ray contact is automatically a positive principal-kernel witness, even when the full matrix is nonsingular. Conversely, once a candidate `M(t)` has already been certified copositive, one such positive active-support kernel with positive debit energy proves that `t` is the exact ray threshold: every larger `s` is killed by the same contact state.

A second useful theorem makes the interface fail-closed before any global copositivity call: if a proposed principal-kernel state has a **negative inactive residual**, then the full matrix cannot be copositive. This gives an exact local rejection certificate rather than a solver failure.

No actual P5 `C0/Q_k/d`, source/selector binding, physical coverage, Float64 enclosure, Lean/kernel proof, independent 封不觉 verification, admission, registry promotion, or parent closure is claimed.

---

## 1. Setup and typed contracts

Let `C0,Q_1,...,Q_m` be real symmetric `n x n` matrices. Let

`d=(d_1,...,d_m) >= 0`

be a fixed nonnegative error profile and define

`Q_d := sum_{k=1}^m d_k Q_k`.

Assume each `Q_k` is copositive. Then `Q_d` is copositive because the copositive cone is a convex cone.

Define the affine ray pencil

`M(t) := C0 - t Q_d`, `t>=0`.

For any `y>=0`, abbreviate

`c0(y) := y^T C0 y`,

`q_d(y) := y^T Q_d y = sum_k d_k y^T Q_k y`.

Then

**`y^T M(t)y = c0(y) - t q_d(y)`.**

The scalar safe set along profile `d` is

`T_d := {t>=0 : M(t) is copositive}`.

Because `Q_d` is copositive, `T_d` is downward closed: if `t in T_d` and `0<=s<=t`, then

`M(s)=M(t)+(t-s)Q_d`

is a sum of copositive matrices and is therefore copositive.

This monotonicity is the ray-specialized version of the downward geometry in T-P5-204/207.

---

## 2. T208-A — strict-reference ray threshold is attained

Let

`Sigma := {y>=0 : 1^T y = 1}`.

Assume:

1. `C0` is **strictly copositive**, i.e. `c0(y)>0` for every nonzero `y>=0`;
2. `Q_d` is copositive;
3. `Q_d` is nontrivial on the orthant, i.e. there exists `y>=0` with `q_d(y)>0`.

Since `Sigma` is compact and `c0` is continuous and strictly positive on `Sigma`,

`mu0 := min_{y in Sigma} c0(y) > 0`.

Therefore the ratio

`rho(y) := q_d(y)/c0(y)`

is a continuous nonnegative function on `Sigma`. By assumption it is not identically zero. Hence it attains a strictly positive maximum

`rho_* := max_{y in Sigma} rho(y) > 0`.

Define

**`t_* := 1/rho_*`.**

### Theorem

**`T_d = [0,t_*]`.**

Moreover there exists `z in Sigma` with

`q_d(z)>0`

and

**`z^T M(t_*) z = 0`.**

### Proof

For every `y in Sigma`,

`q_d(y) <= rho_* c0(y)`.

If `0<=t<=t_*`, then `t rho_*<=1`, so

`c0(y)-t q_d(y) >= c0(y)(1-t rho_*) >=0`.

By homogeneity this holds for every `y>=0`; hence `M(t)` is copositive.

Choose `z in Sigma` attaining `rho_*`. Then

`q_d(z)=rho_* c0(z)>0`

and

`z^T M(t_*)z = c0(z) - (1/rho_*)q_d(z)=0`.

For every `s>t_*`,

`z^T M(s)z = z^T M(t_*)z -(s-t_*)q_d(z)`

`= -(s-t_*)q_d(z)<0`.

Thus `M(s)` is not copositive. QED.

### Why strict reference is used here

The strict-reference assumption is not cosmetic. It guarantees a positive denominator on the compact normalized orthant and therefore gives an ordinary compact maximum problem with an attained contact. T-P5-207 already contains a division-free formulation for zero-reference-energy directions; this child does not silently divide on those faces.

When `C0` is only weakly copositive, the later contact/support theorems below still apply **whenever an actual positive-debit contact is supplied**, but T208-A's global attainment proof is not asserted without additional zero-face compatibility hypotheses.

---

## 3. T208-B — copositive zero contact implies orthant KKT

Let `M` be any symmetric copositive matrix. Suppose

`z>=0`, `z!=0`, and `z^T M z=0`.

### Theorem

Then

**`Mz>=0`**

and, coordinatewise,

**`z_i (Mz)_i = 0`.**

### Proof of `Mz>=0`

Fix coordinate `i`. For every `eps>=0`, the perturbed state

`z+eps e_i >=0`.

Copositivity gives

`0 <= (z+eps e_i)^T M(z+eps e_i)`

`= z^TMz + 2 eps (Mz)_i + eps^2 M_ii`

`= 2 eps (Mz)_i + eps^2 M_ii`.

For `eps>0`, divide by `eps`:

`0 <= 2(Mz)_i + eps M_ii`.

Let `eps -> 0+`. Then `(Mz)_i>=0`.

Since `i` was arbitrary, `Mz>=0`.

### Complementarity

Now every term `z_i(Mz)_i` is nonnegative and

`sum_i z_i(Mz)_i = z^TMz =0`.

A sum of nonnegative terms can vanish only if every term vanishes. Therefore

`z_i(Mz)_i=0` for all `i`. QED.

This is the exact one-sided first-order condition for a zero of a copositive quadratic form. No differentiability/KKT solver is needed.

---

## 4. T208-C — contact becomes a positive principal kernel

Let `S:=supp(z)={i:z_i>0}` and `J:=S^c`.

From T208-B, every active coordinate satisfies

`(Mz)_i=0` for `i in S`.

Because `z_J=0`, the active equations are exactly

**`M[S,S] z_S = 0`.**

Also

**`z_S>0`.**

For inactive coordinates,

`(Mz)_J = M[J,S] z_S >=0`.

Therefore every copositive zero contact yields the typed support packet

**`z_S>0`,**

**`M_SS z_S=0`,**

**`r_J:=M_JS z_S>=0`.**

In particular,

**`det(M_SS)=0`.**

### Important distinction

The conclusion is a kernel statement for the **active principal block**, not necessarily for the full matrix.

The full residual can be strictly positive on inactive coordinates. Therefore a threshold contact can occur while the full matrix is nonsingular. Any adapter that replaces `M_SS z_S=0` by `Mz=0` is too strong and can reject valid sharp contacts.

---

## 5. T208-D — exact local rejection by a negative inactive residual

The support packet also gives a cheap exact failure test before global copositivity is attempted.

Let `M` be symmetric. Let `S` be nonempty, let `z_S>0`, extend by zero to `z>=0`, and assume

`M_SS z_S=0`.

Then `z^TMz=0` automatically.

Suppose some inactive coordinate `j in J` has

`r_j := (M_JS z_S)_j <0`.

### Theorem

**`M` is not copositive.**

### Proof

For `eps>0`, set

`x_eps := z + eps e_j >=0`.

Then

`x_eps^T M x_eps`

`= z^TMz + 2 eps (Mz)_j + eps^2 M_jj`

`= 2 eps r_j + eps^2 M_jj`.

The linear coefficient is strictly negative. Therefore the expression is negative for all sufficiently small positive `eps`. Hence `M` is not copositive. QED.

### Interface consequence

A proposed support-root candidate has three logically distinct states:

1. `r_J` has a negative entry: **mathematical FAIL**, with explicit nearby orthant witness;
2. `r_J>=0`: first-order contact compatibility PASS, but global copositivity is still OPEN;
3. `r_J>=0` and global copositivity is independently certified: the support packet is a genuine copositive contact and can be used for exact-threshold closure.

This prevents a common false promotion: nonnegative KKT residuals are necessary local data, not a global copositivity certificate.

---

## 6. T208-E — active-support contact plus safe candidate gives exact ray threshold

Return to

`M(t)=C0-tQ_d`

with `Q_d` copositive.

Suppose a candidate `t>=0` is given together with a nonempty support `S` and vector `z_S>0`. Extend it by zero to `z>=0`. Assume

1. **global safe-side premise:** `M(t)` is copositive;
2. **active kernel:** `M(t)[S,S] z_S=0`;
3. **positive debit:** `q_d(z)=z^TQ_d z>0`.

The inactive residual `M(t)[J,S]z_S>=0` follows automatically from 1 and 2 by T208-B, although it is useful to check it earlier as T208-D.

### Theorem

**`t` is the exact endpoint of `T_d`.**

That is,

- `M(s)` is copositive for every `0<=s<=t`;
- `M(s)` is not copositive for every `s>t`.

### Proof: safe side

For `0<=s<=t`,

`M(s)=M(t)+(t-s)Q_d`.

Both summands are copositive, so `M(s)` is copositive.

### Proof: unsafe side

The active-kernel identity gives

`z^T M(t) z = z_S^T M(t)[S,S]z_S=0`.

For `s>t`,

`z^T M(s)z`

`= z^T M(t)z -(s-t) z^TQ_dz`

`= -(s-t)q_d(z)<0`.

Thus `M(s)` is not copositive. QED.

### Division-free character

This theorem does not require computing the ratio

`c0(z)/q_d(z)`.

The trusted side only needs:

- an already-certified copositive matrix `M(t)`;
- an exact active principal-kernel equality;
- positivity of one quadratic debit value.

The same contact state then proves every larger scale unsafe by one exact subtraction identity.

---

## 7. T208-F — T-P5-207 halfspace contact equals support-kernel contact

T-P5-207 gives the ray halfspace inequality

`t q_d(y) <= c0(y)`

for every `y>=0`.

At a sharp boundary contact `z` with `q_d(z)>0`, equality holds:

`c0(z)=t_* q_d(z)`.

Equivalently,

`z^T M(t_*)z=0`.

T208-B/C then upgrades this **scalar touching equality** to the much richer structural packet

`S=supp(z)`,

`z_S>0`,

`M(t_*)[S,S]z_S=0`,

`M(t_*)[S^c,S]z_S>=0`.

Conversely, T208-E says that once the safe-side copositivity of `M(t)` is independently proved, this support packet plus `q_d(z)>0` turns the touching halfspace into an **exact ray endpoint certificate**.

So the cross-layer bridge is

`T207 state cut touches error ray`

`=> copositive zero contact`

`=> positive active principal kernel + inactive residual`

`=> support/minor algebra`

and in reverse

`safe candidate + positive support kernel + positive debit`

`=> exact T207 ray threshold`.

---

## 8. T208-G — determinant/root routing in the regular-support branch

For a fixed support `S`, define the active pencil

`A_S(t):=C0[S,S]-t Q_d[S,S]`.

Any T208 contact on `S` satisfies

`A_S(t) z_S=0`

with `z_S>0`.

Hence

**`p_S(t):=det(A_S(t))=0`.**

If `C0` and `Q_d` have rational entries, then

`p_S(t) in Q[t]`

and

`deg p_S <= |S|`.

Therefore, whenever `p_S` is not the zero polynomial, every contact threshold carried by this support is an algebraic root of a finite rational polynomial. If `Q_d[S,S]` has rank at most `r`, the determinant degree can be sharpened to at most `r` by the usual rank-`r` perturbation expansion, but no low-rank assumption is required for the basic theorem.

### Candidate filtering order

A mathematically clean support-root producer may therefore use:

1. propose a root `t` of nonzero `p_S`;
2. produce `z_S>0` with `A_S(t)z_S=0`;
3. check inactive residual `A_{J,S}(t)z_S`;
4. reject immediately if any inactive residual is negative by T208-D;
5. check `z^TQ_dz>0`;
6. independently prove global copositivity of `M(t)`;
7. conclude exact ray threshold by T208-E.

Steps 2--5 are support/contact algebra. Step 6 remains the global cone certificate and must not be silently omitted.

---

## 9. Persistent singular-support boundary

The determinant route above is intentionally restricted to

`p_S not identically 0`.

If

`det(A_S(t)) == 0`

as a polynomial identity, then `det=0` does not isolate a threshold. This can happen when the active pencil carries a persistent singular stratum, possibly with a signed/null direction unrelated to the eventual positive contact.

In that case the correct next object is not another numerical root of the identically-zero determinant. One must inspect rank-revealing minors, a persistent kernel subspace, or a parameter-dependent kernel orientation/positivity condition.

Two cases must be distinguished:

- **rank-drop contact:** generic rank is `r` and rank drops at `t_*`; then a nonzero generic `r x r` minor gives a genuine polynomial root at `t_*`;
- **persistent-rank contact:** rank does not drop and the relevant kernel already exists generically; then threshold formation is controlled by how that kernel meets the nonnegative orthant and by inactive residual/debit signs, not by the full determinant.

This child does not claim a complete algebraic classifier for the persistent-rank case. That remains a separate higher-corank/persistent-stratum obligation rather than being hidden under `det=0`.

---

## 10. Exact rational regressions

### Regression A — threshold contact need not be a full kernel

Take

`C0 = [[1,1],[1,2]]`,

`Q_d = [[1,0],[0,0]]`.

For `x=(x1,x2)>=0`,

`x^T C0 x = x1^2 + 2x1x2 + 2x2^2 >0`

for every nonzero `x`, so `C0` is strictly copositive.

Also `Q_d` is copositive.

The pencil is

`M(t)=[[1-t,1],[1,2]]`.

At `t=1`,

`M(1)=[[0,1],[1,2]]`.

For `x>=0`,

`x^TM(1)x = 2x1x2+2x2^2 >=0`,

so `M(1)` is copositive.

Take `z=e1`. Then

`z^TM(1)z=0`,

`q_d(z)=1>0`,

`S={1}`,

`M(1)[S,S]=[0]`,

and the inactive residual is

`M(1)[2,1] z_1 = 1>0`.

Thus the exact threshold is `t_*=1`.

But

`det M(1) = -1`,

so the **full matrix is nonsingular**. The correct kernel object is only the active principal block. This is a direct negative control against any adapter that requires `M(t_*)z=0`.

### Regression B — negative inactive residual is an exact failure

Let

`M=[[0,-1],[-1,2]]`.

Take support `S={1}` and `z_S=1`.

The active block satisfies

`M_SS z_S=0`,

but the inactive residual is

`r_2=-1<0`.

For `0<eps<1`,

`(1,eps)^T M (1,eps) = -2eps+2eps^2 <0`.

So the matrix is not copositive. The failure is structural and exact; no global optimizer is needed to reject this proposed contact.

### Regression C — debit positivity is necessary for an upper threshold

Suppose a contact state `z` satisfies

`z^TM(t)z=0`

but

`z^TQ_dz=0`.

Then for every `s`,

`z^TM(s)z = z^TM(t)z -(s-t)z^TQ_dz =0`.

This state supplies no upper exclusion for larger error scale. Therefore the condition

**`q_d(z)>0`**

must remain explicit in the exact-threshold theorem. A zero-debit contact may describe a permanent zero-energy face of the reference geometry rather than the active error budget.

---

## 11. Suggested minimal formalization leaves

The mathematics can be split into small independent theorem leaves without importing any source semantics:

1. `copositive_subtract_ray_downward`
   - assumptions: `Copositive (C0-t*Q)`, `Copositive Q`, `0<=s<=t`;
   - conclusion: `Copositive (C0-s*Q)`.

2. `strictCopositive_ray_threshold_attained`
   - compact normalized orthant;
   - positive continuous denominator;
   - maximum ratio and exact endpoint.

3. `copositive_zero_contact_mulVec_nonneg`
   - `z>=0`, `z^TMz=0`, `Copositive M`;
   - conclusion `Mz>=0`.

4. `copositive_zero_contact_complementarity`
   - conclusion `z_i(Mz)_i=0`.

5. `zero_contact_activePrincipal_kernel`
   - support restriction gives `M_SS z_S=0`, `z_S>0` and inactive residual nonnegative.

6. `negative_inactiveResidual_not_copositive`
   - active principal kernel plus one negative inactive residual;
   - construct `z+eps e_j` with negative quadratic value.

7. `safe_support_contact_exact_ray_threshold`
   - global `Copositive M(t)` + active kernel + positive debit;
   - all smaller scales safe, all larger scales unsafe.

8. `activeKernel_det_zero`
   - finite-dimensional determinant corollary for nonempty support.

The source-facing adapter should carry support indices and extension-by-zero explicitly. It should not require a full-space kernel.

---

## 12. What this changes in the P5 dispatcher

Before T208, the T204--T207 chain gave increasingly sharp scalar/multi-error budget geometry but did not fully specify how an exact boundary witness should be handed to the older support/contact layer.

After T208, a query along profile `d` can be organized as follows:

- safe anchors / reserve certificates provide lower bounds on the ray threshold;
- T207 failure states provide upper halfspace cuts;
- when a cut touches a safe candidate, T208 converts that touching state into an active principal-kernel packet;
- support-root algebra can then retain the state in a compact typed form;
- a negative inactive residual is an exact immediate rejection;
- a nonnegative inactive residual is only a local compatibility pass;
- global copositivity at the candidate remains the decisive safe-side gate;
- once that gate passes and debit energy is positive, the same support contact proves exact sharpness for the whole ray.

This makes the division between local algebra and global cone verification explicit and prevents either layer from impersonating the other.

---

## 13. Boundaries remaining OPEN

This review does **not** prove:

1. the actual source-bound `C0,Q_k` or error profile `d` for any physical P5 sector;
2. selector/cell/tube identity or same-key coverage;
3. strict copositivity of a real source reference matrix;
4. that a real threshold lies in the regular-support determinant branch rather than a persistent singular stratum;
5. a complete classifier for persistent-rank parameter-dependent kernel positivity;
6. global copositivity of any actual candidate `M(t)`;
7. a complete support enumeration algorithm or finite global termination result;
8. algebraic-number / interval reification for an irrational root and its contact vector;
9. Float64, interval, controller, ODE, PDE, trajectory, or physical-source semantics;
10. Lean/kernel compilation or independent 封不觉 verification;
11. admission, registry eligibility, or parent theorem closure.

All remain external/pending.

---

## 14. Structural fingerprint

The new bridge is

**`error profile d`**

`=> copositive debit Q_d`

`=> scalar pencil M(t)=C0-tQ_d`

`=> strict-reference compact ratio maximum`

`=> exact boundary contact z`

`=> orthant KKT/complementarity`

`=> positive active principal kernel + inactive residual`

`=> regular support determinant/root candidate or persistent-stratum branch`

`=> local negative-residual FAIL or global copositivity gate`

`=> positive debit contact`

`=> exact ray threshold without division`.

The main interface lesson is simple: **sharp error-budget geometry and support-kernel algebra are the same contact viewed in two coordinate layers, but neither local support conditions nor determinant roots replace global copositivity.**