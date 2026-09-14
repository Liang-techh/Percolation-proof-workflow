---
kind: review_result
review_id: review-T-P5-177-zero-loaded-support-inactive-residual-floor-honglianmozun-20260909T1851Z
task_id: T-P5-177-ZERO-LOADED-SUPPORT-INACTIVE-RESIDUAL-FLOOR
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T18:51:00Z
claim_commit: abfdf54763a7807cdeed3b7687ecefafa6b74bfd
inspected_commit: d4b8aa15ccc78c26cf8129f0d5d2aa15d0c3dc29
upstream_commits:
  - 688765cc6802a5dd1b821bf0590276ba16d7e3ab  # T-P5-176 persistent rank stratum exclusion
  - e40396a17005bd9c5914adf7af140d6e60c03d1d  # T-P5-175 isolated high-corank algebraic contact bridge
  - 09a09a9df2b409fedc2cac32ad483e6baa005e5c  # T-P5-174 high-corank kernel-cone strict contact
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_zero_loaded_flat_face_residual_barrier; add_exact_rational_primal_dual_packet; route_gS_zero_supports_to_polyhedral_floor_branch; retain_global_copositivity_as_separate_obligation
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact block-energy algebra; exact LP/Farkas duality; exact rational symbolic regression of the 3x3 sharp example
exit_code: 0 for exact symbolic regression; no Lean/kernel run
---

# T-P5-177 — zero-loaded support inactive-residual floor

## 0. Verdict and closed seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-176 proves that a persistent PSD active rank defect cannot carry a physical nonnegative contact when the floor loading is nontrivial on the active support. Its explicit Boundary B leaves the case

`g_S = 0`

open.

That branch is not an algebraic-rank pathology and it should not be sent back to the T-P5-175 quadratic-algebraic kernel machinery. When the loading vanishes on the active support, the active energy is exactly independent of the floor parameter. The only way the floor can repair a zero-energy active face at first order is through the **inactive KKT residuals**.

This review proves that the resulting obstruction is polyhedral and rational:

1. the active zero-energy cone is fixed for all `D`;
2. after the normalization `1^T z = 1`, every inactive residual is affine in `D` with a coefficient independent of `z`;
3. the exact floor needed to remove every first-order escape from that flat face is the maximum of finitely many rational LP values;
4. a candidate floor has a compact exact dual packet
   `r_i + (D g_i/2) 1 = A y_i + w_i`, `w_i >= 0`;
5. failure has a compact exact primal packet `A z=0`, `z>=0`, `1^Tz=1`, with a negative inactive residual, and that packet lifts to an actual copositivity counterexample by an explicit one-coordinate perturbation;
6. if some inactive floor weight is zero and its worst residual is negative, **no value of `D` can repair the flat face**;
7. there are exact globally sharp examples in which the active rank defect persists for every `D` but the global copositivity threshold is nevertheless a rational inactive-residual crossing.

Thus T-P5-176 Boundary B is a real physical branch, but it is simpler than the nonzero-loading branch: it is an exact rational cone/LP problem, not a moving-kernel or algebraic-number problem.

No source binding, global copositivity admission, runtime/Float64 claim, Lean/kernel validation, independent verification, registry mutation, or parent closure is performed.

---

## 1. P5 additive-floor pencil and a zero-loaded support

Let

`M_D = M_0 + D L_g`,

with

`L_g = (g 1^T + 1 g^T)/2`.

Fix a nonempty active support `S` and inactive complement `T`. Write

`A := M_0[S,S]`,

`R_0 := M_0[T,S]`.

Assume throughout the main branch

1. `A=A^T >= 0`;
2. `g_S = 0`;
3. `g_T >= 0` for the monotone physical floor branch;
4. the active zero-energy cone is nontrivial:

   `K_+ := { z in R^S : z>=0, A z=0 } != {0}`.

Because `g_S=0`,

`L_g[S,S]=0`,

hence

**`M_D[S,S] = A` for every `D`.**

So every `z in K_+` remains an exact active zero-energy state for the whole pencil:

`z^T M_D[S,S] z = z^T A z = 0`.

This is the opposite of the T-P5-175 isolated-rank branch: the active kernel does not need to be tracked as `D` changes because the active block does not change at all.

---

## 2. T177-A — exact inactive-residual identity

Let `z in K_+` and define

`s := 1^T z`.

For nonzero `z>=0`, `s>0`.

For every inactive index `i in T`, the inactive KKT residual is

`rho_i(D,z) := (M_D[i,S] z)`.

Since `g_S=0`,

`L_g[i,S] = (g_i/2) 1_S^T`.

Therefore

**`rho_i(D,z) = (R_0 z)_i + (D g_i/2) s`.**

After the canonical normalization

`1^T z = 1`,

this becomes

**`rho_i(D,z) = (R_0 z)_i + D g_i/2`.**

The coefficient of `D` no longer depends on the kernel representative. This is the structural reason the bilinear `(D,z)` obstruction from T-P5-174 disappears in the `g_S=0` branch.

---

## 3. Why a negative inactive residual is a genuine energy failure

Embed `z` into the full coordinate space by setting inactive coordinates to zero. Then

`q_D(z) := z^T M_D z = 0`.

Take an inactive coordinate `i in T` and perturb in the feasible orthant direction:

`x(t) := z + t e_i`, `t>=0`.

The quadratic energy is exactly

`q_D(x(t))`

`= 2 t rho_i(D,z) + t^2 M_D[i,i]`.

Hence:

### T177-B — first-order escape lemma

If

`rho_i(D,z) < 0`,

then there exists `t>0` such that

`q_D(z+t e_i) < 0`.

So `M_D` is not copositive.

### Exact choice of `t`

Let `c=M_D[i,i]` and `r=rho_i(D,z)<0`.

- if `c<=0`, every `t>0` gives `2tr+t^2c<0`;
- if `c>0`, every `0<t<-2r/c` gives a negative energy.

For rational `M_D,z`, a rational `t` can be chosen. Thus a negative flat-face residual is not merely a KKT diagnostic; it gives an exact physical counterexample ray.

This is the Lyapunov interpretation: the active storage has a zero mode, and a negative inactive directional derivative injects energy at first order. No positive second-order curvature can repair the sign arbitrarily close to the flat face.

---

## 4. The normalized kernel polytope

Define the compact rational polytope

`Z_S := { z : A z=0, z>=0, 1^T z=1 }`.

It is nonempty exactly when `K_+` is nontrivial.

For each inactive row `i`, define the exact worst base residual

`mu_i := min { (R_0 z)_i : z in Z_S }`.

Because the data are rational and the feasible set is a rational polytope, whenever `Z_S` is nonempty the optimum is attained and `mu_i` is rational. An exact rational optimizer exists.

The worst residual at floor `D` is therefore

**`min_{z in Z_S} rho_i(D,z) = mu_i + D g_i/2`.**

No kernel basis, pseudoinverse, eigenvector, or algebraic-number representation is required.

---

## 5. T177-C — exact flat-face residual barrier

Assume `g_T>=0` and restrict to `D>=0`.

For an inactive row with `g_i>0`, define

`D_i := -2 mu_i / g_i`.

For an inactive row with `g_i=0`, the residual is independent of `D`.

Define the finite flat-face barrier

`D_flat := max( 0, max_{i:g_i>0} D_i )`,

provided that

`mu_i >= 0` for every inactive `i` with `g_i=0`.

Then:

### Theorem T177-C1 — universal no-linear-escape threshold

If all zero-weight inactive rows satisfy `mu_i>=0`, then for every `D>=0`,

`rho_i(D,z)>=0 for all i in T and all z in Z_S`

if and only if

**`D >= D_flat`.**

### Proof

For `g_i>0`, the universal row condition is

`mu_i + D g_i/2 >=0`,

which is exactly `D>=D_i`. Taking all rows and `D>=0` gives the maximum. If `g_i=0`, the condition is simply `mu_i>=0`. QED.

### Theorem T177-C2 — unrepairable zero-weight obstruction

If there exists an inactive row `i` such that

`g_i=0`, `mu_i<0`,

then for **every** real `D` there is a normalized kernel state `z in Z_S` with

`rho_i(D,z)<0`.

Therefore every `M_D` fails copositivity by T177-B.

The floor parameter is invisible both on the active zero mode and on that inactive escape direction, so no multiplier search can repair the obstruction.

---

## 6. T177-D — exact primal/dual packet, no support enumeration inside the checker

The LP defining `mu_i` has a particularly simple exact dual.

Fix a rational candidate `D` and one inactive row. Define

`c_i(D) := R_0[i,S]^T + (D g_i/2) 1_S`.

The universal residual condition for this row is

`c_i(D)^T z >=0`

for every

`z>=0`, `Az=0`, `1^Tz=1`.

Because scaling is positive, this is equivalent to nonnegativity on the entire cone

`z>=0`, `Az=0`.

### Theorem T177-D — cone dual alternative

The following are equivalent:

1. `c_i(D)^T z >=0` for every `z>=0` with `Az=0`;
2. there exists a vector `y_i` and a vector `w_i>=0` such that

   **`c_i(D) = A y_i + w_i`.**

Equivalently, the trusted checker may verify only

`c_i(D) - A y_i = w_i`,

`w_i>=0`.

### Proof

The cone

`C := ker(A) intersect R_+^S`

has dual

`C^* = range(A) + R_+^S`

because `A` is symmetric and `range(A)=ker(A)^perp`. Thus a linear functional is nonnegative on `C` exactly when its coefficient vector lies in `range(A)+R_+^S`. QED.

### Rationality

For rational `A,c_i(D)`, the feasibility system

`c_i(D)=Ay_i+w_i`, `w_i>=0`

is rational linear feasibility. If a real certificate exists, a rational certificate exists.

Thus a candidate `D` can be checked rowwise with exact rational equalities and inequalities only.

---

## 7. Strict margins and the exact boundary contact

Suppose `g_i>0` for every inactive row.

For `D>D_flat`,

`mu_i + D g_i/2`

is strictly positive for every row that participates in the maximum, and in fact

`min_{z in Z_S} rho_i(D,z) = mu_i + D g_i/2 >0`

for every inactive row after taking the maximum over all rows.

A certified rowwise strict margin `epsilon_i>0` can be represented by

`c_i(D) = A y_i + w_i`,

`w_i >= epsilon_i 1`.

Then for every normalized kernel state,

`rho_i(D,z) = w_i^T z >= epsilon_i`.

At `D=D_flat`, at least one positive-weight row `i_*` satisfies

`mu_i_* + D_flat g_i_*/2 =0`

unless the barrier is just the imposed lower domain bound `D=0`.

Choose an exact rational LP optimizer `z_* in Z_S` for that row. Then

`A z_*=0`, `z_*>=0`, `1^Tz_*=1`,

and

**`rho_i_*(D_flat,z_*)=0`.**

Thus the flat-face barrier has an exact rational boundary contact packet.

For any `D<D_flat` sufficiently within the permitted parameter range, the same worst-row LP gives a state with negative residual and hence an explicit energy counterexample by T177-B.

---

## 8. Strict active support versus support-contained contacts

`Z_S` is deliberately closed: it includes normalized zero modes with some zero active coordinates. This is the correct object for a **universal flat-face safety** statement, because any such vector is still a physical orthant state and can produce a negative escape.

If a theorem needs an exact-support contact with every active coordinate positive, use the strict-margin feasibility packet

`Az=0`,

`1^Tz=1`,

`z_j >= eta` for every `j in S`,

with rational `eta>0`, together with the desired inactive residual equalities/inequalities.

Because positivity is open inside the rational kernel affine space, any real strict-support solution admits a rational strict-support solution.

If the barrier optimizer lies on the boundary of `Z_S`, the true minimal active support is smaller and should be routed to that smaller support rather than artificially inflated.

---

## 9. Exact globally sharp 3x3 example

Take

`S={1,2}`, `T={3}`,

`g=(0,0,1)`,

and

`M_D = [[1,-1,(D-1)/2],
        [-1,1,(D-1)/2],
        [(D-1)/2,(D-1)/2,1]]`.

The active block is

`A=[[1,-1],[-1,1]] >=0`,

with the normalized positive kernel state

`z=(1/2,1/2)`.

The active block is independent of `D`, so this is a persistent rank-one defect for every floor.

Its inactive residual is exactly

`rho_3(D,z)=(D-1)/2`.

Hence T177 gives

**`D_flat=1`.**

For `D<1`, put the full state

`x(t)=(1/2,1/2,t)`.

Then exact expansion gives

**`x(t)^T M_D x(t) = t^2 + (D-1)t`.**

Choosing `0<t<1-D` gives a negative value, so the pencil is not copositive below `1`.

At `D=1`,

`M_1 = [[1,-1,0],[-1,1,0],[0,0,1]] >=0`.

For every `D>=1` and every `x>=0`,

`x^T M_D x`

`= (x_1-x_2)^2 + (D-1)x_3(x_1+x_2) + x_3^2 >=0`.

Therefore the **global exact copositivity floor is `D_*=1`**, even though the active rank defect persists for every `D` and `g_S=0`.

This is the sharp counterexample showing why T-P5-176 Boundary B cannot simply be discarded: a zero-loaded persistent face can determine the global floor through an inactive first-order crossing.

It also shows that the resulting floor can be rational even though the active kernel is nontrivial.

---

## 10. A two-row example showing the max-of-LPs structure

Let the same active block `A` have normalized kernel state `z=(1/2,1/2)`, and take two inactive rows with positive floor weights `g_3,g_4>0`.

If their base residuals on the kernel are

`mu_3=-1/2`,

`mu_4=-3/4`,

then their repair thresholds are

`D_3=1/g_3`,

`D_4=(3/2)/g_4`.

The flat-face barrier is exactly

`D_flat=max(0,D_3,D_4)`.

The two rows do not need a shared Young bound, norm envelope, eigenvalue estimate, or common algebraic kernel solve. Each row consumes the same normalized zero-mode cone through a linear functional, and the final floor is simply the maximum of exact rational rowwise LP thresholds.

This is another instance of the broader P5 structural rule established in earlier children: preserve signed directional information until the last scalar maximum rather than robustifying too early.

---

## 11. Structural fingerprint

The new fingerprint is:

> **zero-loaded Lyapunov face -> fixed zero-energy cone -> inactive directional-derivative barrier -> rational cone duality.**

Operationally:

1. detect `g_S=0` before invoking algebraic rank-drop machinery;
2. keep `A=M_0[S,S]` fixed;
3. form the normalized kernel polytope `Z_S`;
4. compute or certify each worst inactive residual;
5. positive inactive floor weights give rational lower thresholds;
6. zero inactive floor weights with a negative worst residual are fatal obstructions;
7. candidate PASS packets use `c_i(D)=Ay_i+w_i`, `w_i>=0`;
8. FAIL packets use `Az=0,z>=0` plus one negative residual and lift directly to a negative-energy perturbation.

This is an energy/Lyapunov statement, not a provenance or admission statement.

---

## 12. Candidate theorem packet

### T177-A — zero-loaded inactive residual identity

For `g_S=0`, `Az=0`, `1^Tz=1`,

`(M_D[T,S]z)_i=(R_0z)_i+Dg_i/2`.

### T177-B — flat-face escape lemma

If `z>=0`, `Az=0`, and one inactive residual is negative, then there exists `t>0` with

`q_D(z+t e_i)<0`.

### T177-C — rational flat-face barrier

For rational data, `g_T>=0`, and nonempty `Z_S`, define

`mu_i=min_{z in Z_S}(R_0z)_i`.

If every zero-weight row has `mu_i>=0`, then universal nonnegative inactive residuals hold exactly for

`D>=max(0,max_{g_i>0} -2mu_i/g_i)`.

If a zero-weight row has `mu_i<0`, no `D` repairs the face.

### T177-D — rational dual certificate

For rational candidate `D`, universal nonnegative row `i` is equivalent to existence of rational `y_i,w_i` with

`R_0[i,S]^T+(Dg_i/2)1 = Ay_i+w_i`,

`w_i>=0`.

### T177-E — exact boundary contact

At a nontrivial rowwise threshold, an exact rational optimizer `z_*` exists and saturates the corresponding inactive residual.

---

## 13. Boundaries and fail-closed conditions

### Boundary A — this closes the flat-face first-order obstruction, not full copositivity by itself

`D>=D_flat` proves that no zero-energy state supported in `S` has a negative **inactive first derivative**. It does not by itself prove that every positive-energy direction, every other support, or every second-order mixed direction is safe.

Global PASS must still come from the existing copositivity/pivot/support machinery or a stronger block-specific theorem.

The 3x3 example in Section 9 is globally sharp only because its remaining terms admit an explicit nonnegative energy decomposition.

### Boundary B — negative floor weights

If some `g_i<0`, increasing `D` worsens that inactive residual and the feasible set can acquire an upper bound rather than a lower floor. The monotone-floor theorem above assumes `g_T>=0`.

### Boundary C — `g_S` must vanish exactly

A numerically small `g_S` does not justify this branch. If `g_S!=0`, the active block itself moves with `D` and the T-P5-175/176 algebraic-rank logic applies.

### Boundary D — approximate kernel is not enough

The escape argument consumes exact `Az=0`. A small eigenvalue is not a zero-energy face.

### Boundary E — strict support must be explicit if required

The closed kernel polytope permits smaller supports. Exact-support contact requires a positive-coordinate margin packet.

### Boundary F — source/runtime/formal gates remain open

Actual `{M_0,g,S,D}` source equality, same-key simplex semantics, physical cell/domain coverage, Float64 reification, ODE/P8/M4 semantics, Lean/kernel compilation, independent validation by 封不觉, admission, registry mutation, and parent closure all remain open.

---

## 14. Routing recommendation

Extend the physical contact tree after T-P5-176 as follows:

1. **`g_S!=0`, corank one:** T-P5-173;
2. **`g_S!=0`, corank >=2 isolated:** T-P5-175;
3. **`g_S!=0`, persistent rank defect:** impossible for a nonzero physical contact by T-P5-176;
4. **`g_S=0`: do not call T-P5-175.** Use T-P5-177:
   - fixed active kernel cone;
   - exact inactive-residual LP/dual packet;
   - rational flat-face barrier;
   - zero-weight fatal obstruction when present;
   - then return to the ordinary global copositivity dispatcher for all remaining curvature/support obligations.

The main structural conclusion is:

> **When the floor loading vanishes on an active Lyapunov zero face, the floor cannot move that face's energy at all. It can only rotate the surrounding orthant gradient. The exact price of removing those first-order escape directions is therefore a rational cone-duality problem, and a zero-weight escape direction is permanently unrepairable.**
