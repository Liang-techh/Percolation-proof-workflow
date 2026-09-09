---
kind: review_result
review_id: review-T-P5-178-zero-loaded-face-critical-cone-schur-bridge-liuguanyi-20260909T1904Z
task_id: T-P5-178-ZERO-LOADED-FACE-CRITICAL-CONE-SCHUR-BRIDGE
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T19:04:00Z
claim_commit: 2c38f69ebd61799eae271f8aeba970e1c2d3f7c8
inspected_commit: eea9886a66fe2c8ea80b05a28010da1ac7015603
upstream_commits:
  - 7d1827e843a23ede07165af1be09ce4626bc6916  # T-P5-177 zero-loaded flat-face residual floor
  - 688765cc6802a5dd1b821bf0590276ba16d7e3ab  # T-P5-176 persistent rank stratum exclusion
  - e40396a17005bd9c5914adf7af140d6e60c03d1d  # T-P5-175 isolated high-corank bridge
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_flat_face_critical_cone_characterization; add_hidden_kernel_shear_obstruction; add_range_solve_schur_bridge; route_T177_boundary_contacts_to_existing_copositivity_dispatcher
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact quadratic block expansion; exact range/kernel linear algebra; exact rational hand/SymPy regressions
exit_code: 0 for exact symbolic regressions; no Lean/kernel run
---

# T-P5-178 — zero-loaded face critical-cone Schur bridge

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-177 computes the exact first-order floor required to make every inactive derivative nonnegative along a zero-loaded active Lyapunov face. Its Boundary A correctly leaves open the second-order question: a zero inactive residual can still expose negative curvature, and a higher-corank active kernel can hide an additional signed shear even when the residual vanishes on the chosen contact state.

This review closes that local mathematical seam at one strict positive active contact.

The result is an exact critical-cone theorem:

> once T-P5-177 has made all inactive first-order residuals nonnegative, only the rows whose residual is exactly zero remain second-order critical; local orthant nonnegativity at the contact is equivalent to nonnegativity of one smaller mixed block on `R^S x R_+^I`.

That mixed condition has an inverse-free Schur characterization:

1. every critical inactive row must annihilate the **entire** active kernel, not merely the chosen zero state;
2. equivalently, every critical row transpose must lie in `range(A)`;
3. after exact range solves `A X = B_I^T`, the remaining condition is ordinary copositivity of

   `H = C_II - B_I X`.

Thus T-P5-177's flat-face LP floor is only the first stage. At a boundary row, the next trusted object is not another scalar floor but a typed **critical-row range solve + reduced copositive Schur block**.

No global source binding, whole-simplex copositivity, runtime/Float64 claim, Lean/kernel validation, independent validation, registry mutation, or parent closure is performed.

---

## 1. Contact geometry after the T-P5-177 first-order barrier

Let `M=M^T` be partitioned by a nonempty active support `S` and inactive complement `T`:

`M = [[A, B^T], [B, C]]`.

Let `z in R^S` satisfy

1. `z>0` coordinatewise;
2. `A z = 0`;
3. `A>=0`.

Embed the contact in the full orthant as

`x_*=(z,0)`.

Its inactive residual vector is

`r := B z`.

Assume the T-P5-177 first-order gate has already established

`r>=0`.

Split the inactive indices into

`I := { i in T : r_i = 0 }`,

`J := { j in T : r_j > 0 }`.

Write

`B_I := B[I,S]`,

`C_II := C[I,I]`.

The point of the split is exact: rows in `J` have a strict linear barrier, while rows in `I` have no first-order protection and therefore expose the true second-order contact geometry.

---

## 2. T178-A — exact critical-direction identity

Take an arbitrary active signed direction `u in R^S` and a nonnegative critical inactive direction `y in R_+^I`. Extend `y` by zero on `J` and consider

`x(t) = (z+t u, t y)`.

Because `z>0`, for every fixed `u` there exists `eps>0` such that `z+t u>=0` for all `0<=t<=eps`.

Since `Az=0` and `B_I z=0`, the constant and linear terms vanish exactly:

`x(t)^T M x(t)`

`= t^2 Q_I(u,y)`,

where

**(2.1)**

`Q_I(u,y) := u^T A u + 2 y^T B_I u + y^T C_II y`.

Therefore:

> if `Q_I(u,y)<0` for one `u` and `y>=0`, the contact fails copositivity arbitrarily close to `x_*`.

This is stronger than saying that a KKT residual is suspicious: it gives an exact feasible negative-energy path.

---

## 3. T178-B — local contact iff the critical block is nonnegative

Define the critical mixed block

`K_I := [[A, B_I^T], [B_I, C_II]]`.

### Theorem `strict_flat_face_local_copositive_iff_critical_block`

Under the hypotheses of Section 1, the following are equivalent.

1. There exists a neighborhood `U` of `x_*` such that

   `x>=0` and `x in U` imply `x^T M x >= 0`.

2. For every `u in R^S` and every `y in R_+^I`,

   `Q_I(u,y)>=0`.

Equivalently, `K_I` is nonnegative on the mixed cone

`R^S x R_+^I`.

### Necessity

This is immediate from (2.1). Any negative critical direction remains orthant-feasible for sufficiently small positive `t` because all active coordinates of `z` are strictly positive.

### Sufficiency

For a general small orthant perturbation write

`delta=(u,y_I,y_J)`

with `y_I,y_J>=0`. Exact expansion gives

`q(x_*+delta)`

`= 2 r_J^T y_J`

`  + Q_I(u,y_I)`

`  + 2 y_J^T B_J u`

`  + 2 y_J^T C_JI y_I`

`  + y_J^T C_JJ y_J`.

By assumption `Q_I>=0`. Because `J` is finite and every `r_j>0`, let

`rho := min_{j in J} r_j >0`

when `J` is nonempty. The remaining terms involving `y_J` are quadratic and therefore admit a finite constant `L` with

`|2 y_J^T B_J u + 2 y_J^T C_JI y_I + y_J^T C_JJ y_J|`

`<= L ||y_J|| ||delta||`.

Also

`r_J^T y_J >= rho ||y_J||`.

Hence for sufficiently small `||delta||`,

`q(x_*+delta) >= (2 rho - L ||delta||)||y_J|| >=0`.

If `J` is empty, the identity reduces directly to `Q_I>=0`.

Thus the strict-positive rows are locally harmless after T-P5-177; all second-order work is concentrated in the zero-residual critical set `I`. QED.

### Why strict active support matters

The argument uses `z>0` so arbitrary signed `u` are feasible for sufficiently small `t`. If some active coordinates vanish, the active tangent cone is itself one-sided and the correct reduced problem is a nested support/face problem. That boundary remains open below.

---

## 4. T178-C — hidden-kernel shear obstruction

The mixed condition from Section 3 can fail before any Schur curvature calculation.

Let `n in ker(A)`. For fixed `y>=0`, substituting `u=t n` into `Q_I` gives

`Q_I(t n,y) = 2 t y^T B_I n + y^T C_II y`.

If

`y^T B_I n != 0`,

choosing the sign and magnitude of `t` makes `Q_I(tn,y)<0`.

Therefore local copositivity forces

**(4.1)** `B_I n = 0` for every `n in ker(A)`.

Equivalently,

**(4.2)** `range(B_I^T) subseteq range(A)`.

The equivalence uses symmetry:

`range(A) = ker(A)^perp`.

This is the **hidden-kernel shear obstruction**.

A zero residual on the chosen contact only proves

`B_i z=0`.

When `corank(A)>1`, that says nothing about another kernel mode `n`. If a critical inactive row couples to such a mode, a signed active correction can decrease the quadratic at order `t^2` while remaining arbitrarily close to the positive contact.

So a higher-corank flat face requires more than T-P5-177's scalar residual LP.

---

## 5. T178-D — inverse-free range-solve / Schur equivalence

The hidden-kernel condition has an exact checker-friendly form.

### Theorem `mixed_cone_nonnegative_iff_range_solve_and_copositive_schur`

Assume `A=A^T>=0`. Then the following are equivalent.

### (i)

For every `u in R^S` and `y in R_+^I`,

`u^T A u + 2 y^T B_I u + y^T C_II y >=0`.

### (ii)

There exists a matrix `X` satisfying

**(5.1)** `A X = B_I^T`,

and the reduced matrix

**(5.2)** `H := C_II - B_I X`

is copositive:

`y>=0 => y^T H y >=0`.

### Proof `(i) => (ii)`

Take any `n in ker(A)` and any standard basis vector `e_i>=0` in the critical inactive coordinates. The polynomial

`Q_I(tn,e_i)=2t(B_I n)_i + C_ii`

must be nonnegative for every real `t`; hence `(B_I n)_i=0`. Thus `B_I ker(A)=0`, proving

`range(B_I^T) subseteq range(A)`.

Therefore an exact solve `AX=B_I^T` exists.

Now choose `u=-Xy`. Since `AX=B_I^T`,

`B_I X = X^T A X`

is symmetric, and

`Q_I(-Xy,y)=y^T(C_II-B_I X)y=y^T H y`.

Condition (i) therefore implies copositivity of `H`.

### Proof `(ii) => (i)`

Using `AX=B_I^T`, complete the square exactly:

**(5.3)**

`Q_I(u,y)`

`= (u+Xy)^T A (u+Xy) + y^T H y`.

The first term is nonnegative because `A>=0`; the second is nonnegative because `H` is copositive. QED.

### Gauge invariance

If `X'` is another solve of `AX'=B_I^T`, then every column of `X'-X` lies in `ker(A)`. Since `B_I ker(A)=0`,

`B_I X' = B_I X`.

Therefore the reduced matrix `H` is intrinsic even when the range solve is nonunique. No pseudoinverse or canonical nullspace representative is required.

---

## 6. Division-free / rational packet

For rational source data and rational candidate floor `D`, the trusted packet can be purely rational.

If the real linear system

`A X = B_I^T`

is solvable and all coefficients are rational, exact Gaussian elimination gives a rational solution `X`.

The checker only needs:

1. exact symmetry and PSD evidence for `A` from the upstream active-contact branch;
2. exact residual classification `I={i:B_i z=0}`, `J={j:B_j z>0}`;
3. exact matrix equality `A X = B_I^T`;
4. formation of

   `H=C_II-B_I X`;

5. a copositivity certificate for `H` using the existing P5 dispatcher.

No inverse, pseudoinverse, eigenvector, square root, condition number, or floating tolerance is part of the mathematical interface.

If step 3 has no solution, the result is not an approximation issue: Section 4 gives an exact local negative-energy obstruction.

---

## 7. T178-E — specialization to the T-P5-177 zero-loaded floor branch

Return to

`M_D=M_0+D L_g`,

`L_g=(g 1^T+1 g^T)/2`,

and an active support `S` with

`g_S=0`.

Let

`A=M_0[S,S]`.

For inactive row `i`,

`B_i(D)=M_D[i,S]`

`=R_0[i,S] + (D g_i/2) 1_S^T`.

For a normalized zero state `z` with

`Az=0`, `z>0`, `1^T z=1`,

T-P5-177 gives

`r_i(D,z)=B_i(D)z=(R_0 z)_i + Dg_i/2`.

After choosing a candidate `D` that passes the T-P5-177 first-order barrier:

1. rows with `r_i>0` are locally protected by their strict linear margin;
2. rows with `r_i=0` form the critical set `I`;
3. for these rows, solve

   `A X = B_I(D)^T`;

4. then check copositivity of

   `H_D = C_II(D) - B_I(D) X`.

This is the exact missing bridge from the rational flat-face floor to the existing second-order copositivity machinery.

### Corank-one simplification

If

`ker(A)=span{z}`, 

then for every critical row `i`,

`B_i(D)z=0`

already implies that `B_i(D)` annihilates the whole kernel. Hence

`B_i(D)^T in range(A)`

automatically.

So on a corank-one zero-loaded face, **T-P5-177 plus critical-row Schur copositivity is enough; no separate range-obstruction branch is needed.**

### Higher-corank branch

If `dim ker(A)>=2`, criticality at the chosen `z` does not imply range compatibility. The exact solves `AX=B_I^T` are then a genuine additional obligation.

This distinction is mathematically sharp and should be preserved in the typed interface.

---

## 8. Exact regression A — first-order PASS, hidden-kernel shear FAIL

Take

`A = [[0,0],[0,0]]`,

`z=(1,1)>0`,

one inactive critical row

`B=[1,-1]`,

and `C=[0]`.

Then

`Az=0`,

`Bz=0`.

So the first-order residual at the contact is exactly zero and T-P5-177's directional derivative test does not fail.

But

`range(A)={0}`

while

`B^T !=0`,

so the range-solve gate fails.

Choose

`u=(-2,0)`, `y=1`.

Then

`Q_I(u,1)=2Bu=-4`.

Hence for

`x(t)=(1-2t,1,t)`,

any sufficiently small `0<t<1/2` is orthant-feasible and

**`x(t)^T M x(t) = -4 t^2 <0`.**

This is the minimal exact example showing that a zero inactive residual can hide a higher-corank kernel shear.

---

## 9. Exact regression B — range PASS, reduced Schur curvature FAIL

Take

`A=[[1,-1],[-1,1]]`,

`z=(1,1)>0`,

`B=[1,-1]`,

`C=[1/2]`.

Again

`Az=0`, `Bz=0`.

Now the range condition does hold. An exact solve is

`X=(1/2,-1/2)^T`,

because

`A X = B^T`.

But

`B X = 1`,

so

`H = C-BX = -1/2`.

Thus the reduced one-dimensional Schur block is not copositive.

Choose

`u=-X=(-1/2,1/2)`, `y=1`.

Then

`Q_I(u,1)=-1/2`.

Therefore

`x(t)=(1-t/2,1+t/2,t)`

is orthant-feasible for small `t>0` and

**`x(t)^T M x(t) = -t^2/2 <0`.**

This proves that first-order residual PASS plus exact range compatibility is still not enough; the reduced Schur curvature is a separate necessary condition.

---

## 10. Exact regression C — sharp safe boundary

Keep the same

`A=[[1,-1],[-1,1]]`,
`z=(1,1)`,
`B=[1,-1]`,
`X=(1/2,-1/2)^T`,

but take

`C=[1]`.

Then

`H=0`.

The critical quadratic becomes the exact square

`Q_I(u,y)=(u_1-u_2+y)^2 >=0`.

So the boundary is second-order safe even though the inactive first-order residual is exactly zero and the reduced Schur margin is also exactly zero.

This regression is useful because it shows the theorem is not a strict-margin heuristic: semidefinite critical contacts are accepted exactly when their reduced copositive block permits them.

---

## 11. Suggested formal theorem interface

A minimal Lean/typed decomposition is:

1. `flatFace_criticalPath_energy`
   - exact identity `q(z+t(u,y))=t^2 Q_I(u,y)` under `Az=0` and `B_I z=0`;

2. `mixedCone_nonneg_implies_kernel_annihilation`
   - from universal `Q_I>=0`, prove `B_I n=0` for every `n in ker A`;

3. `kernel_annihilation_iff_range_rows`
   - symmetric finite-dimensional bridge `B_I ker A=0 <-> range(B_I^T)<=range(A)`;

4. `rangeSolve_completion_identity`
   - if `AX=B_I^T`, prove (5.3);

5. `rangeSolve_schur_copositive_iff_mixedCone_nonneg`;

6. `strictFlatFace_local_nonneg_of_criticalBlock`
   - finite-dimensional local sufficiency using the positive residual margin on `J`;

7. `corankOne_criticalRow_range_automatic`
   - if `ker A=span{z}` and `B_i z=0`, derive row range compatibility.

These leaves are independent of P5 source provenance and can be formalized without admitting any runtime data.

---

## 12. Boundaries and fail-closed conditions

### Boundary A — local contact, not whole-matrix copositivity

The theorem characterizes a neighborhood of one strict positive zero contact. It does not by itself prove `M_D` copositive on every support or every remote orthant direction.

After the reduced `H` check, the global dispatcher must still handle all other supports/contacts.

### Boundary B — non-strict active support

If `z` has zero coordinates inside the declared support, active signed directions are no longer all feasible. The correct object is a smaller active face/tangent cone. Recurse to the true positive support rather than applying T178 blindly.

### Boundary C — approximate residual zero is not exact criticality

A numerically small positive or negative residual cannot be classified as `I` without a signed exact/interval proof. Positive rows use a true positive margin; negative rows already fail by T-P5-177.

### Boundary D — approximate range solve cannot hide kernel shear

If `AX=B_I^T` is only approximate, a residual component along `ker(A)` can create the exact failure in Section 8. Any inexact adapter must preserve a signed range residual and prove its kernel component vanishes; a norm tolerance alone is not enough.

### Boundary E — zero-loaded assumption remains exact

The P5 specialization consumes `g_S=0` exactly. If `g_S!=0`, the active block moves with `D` and the T-P5-175/176 algebraic-contact route remains the correct branch.

### Boundary F — source/runtime/formal gates remain open

Actual same-key `{M_0,g,S,D,z}` equality, exact residual classification, physical parameter/cell coverage, Float64/interval semantics, P8/M4/ODE meaning, Lean/kernel compilation, independent validation by 封不觉, admission, registry mutation, and parent closure are all still open.

---

## 13. Routing recommendation

Refine the T-P5-177 branch as follows.

1. Use T-P5-177 to compute/certify the rational first-order flat-face floor.
2. At a candidate strict positive zero contact `z`, split inactive rows by exact residual sign.
3. Ignore strictly positive rows for the local second-order problem; their first-order margin dominates sufficiently close to the contact.
4. For zero-residual rows:
   - if `corank(A)=1`, range compatibility is automatic;
   - if `corank(A)>1`, require exact `AX=B_I^T` or return the hidden-kernel shear obstruction;
   - form `H=C_II-B_I X`;
   - send `H` to the existing copositivity machinery.
5. Only after all supports/contacts are covered may any global floor claim be made.

The structural conclusion is:

> **T-P5-177 removes first-order escape from a zero-loaded Lyapunov face. The rows that exactly saturate that barrier expose a second-order critical cone. On that cone, local safety is equivalent to an exact range-compatibility condition plus copositivity of an intrinsic reduced Schur block. Higher active corank creates a genuine hidden-kernel shear obstruction that scalar residual floors cannot see.**
