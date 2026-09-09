---
kind: review_result
review_id: review-T-P5-191-metzler-lift-finite-cone-viability-guyuefangyuan-20260909T2225Z
task_id: T-P5-191-METZLER-LIFT-FINITE-CONE-VIABILITY
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T22:25:00Z
claim_commit: ee342a9f5d40df942ebbfa531012038b8b19a783
inspected_commit: 2994cd0857cc87ef77e9f45f65b1d46a36a85718
upstream_commits:
  - 4c6c4ab0ae84f7e397975e6de14e8167efcd6bfa  # T-P5-186 singular PSD recession active fan
  - e5d824609fe5e899225e17adb672eac18da6883c  # T-P5-188 residual-stratum canonical compression
  - ed292584c6b459fff851a0fbc6f54bf4087cb7a0  # T-P5-190 finite-domain tangent LP derivative
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_polyhedral_finite_value_cone_matrix; add_exact_metzler_lift_checker; add_affine_viability_theorem; add_convex_mode_and_normal_defect_extensions
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional cone duality, affine ODE, positive-system, and Farkas algebra; no source/provenance audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-191 — exact Metzler lift for global viability of the finite-value cone

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-190 closes the pointwise question: at a fixed finite-valued external state `e0`, an external direction `v` is safe precisely when it lies in the tangent cone of the finite-value parameter cone. Its explicit next mathematical bridge was to turn that pointwise condition into a trajectory-level viability checker.

For affine external dynamics

`e' = A e + c`,

that bridge has an exact finite answer.

Let a polyhedral cone be represented by

`E_N := {e : N e >= 0}`

with rows `n_i`. Then the following are equivalent:

1. every active face of `E_N` satisfies the affine tangent condition;
2. `N c >= 0` and every row functional `n_i A` is nonnegative on the face `{e : N e>=0, n_i e=0}`;
3. there exists a matrix `Lambda` such that

   **`N A = Lambda N`,**

   **`Lambda_ij >= 0` for every `i != j`,**

   **`N c >= 0`.**

Thus `Lambda` is Metzler: only the off-diagonal entries are required to be nonnegative; its diagonal is free.

Under this packet, every affine trajectory starting in `E_N` remains in `E_N` for all forward times. Conversely, if the packet fails, there is an exact face-level obstruction: either the drift already points out of the cone at the origin, or a Farkas witness gives a boundary ray along which the linear part points strictly outward.

Specializing `N` to T-P5-190's finite-value cone therefore precompiles the continuum of state-dependent critical-recession checks into finite matrix equalities and sign tests. No runtime active-set enumeration, pseudoinverse, eigenvector, square root, or SDP is required.

This does **not** prove that the actual Route-B/PDE external vector field is affine, source-bind `A,c,N`, prove physical trajectory coverage, or close the Lyapunov derivative sign. Those remain separate obligations.

---

## 1. Setup: a single matrix for the T-P5-190 finite domain

T-P5-190 defines

`K := {d>=0 : P d=0}`

and

`D_fin := {e : e^T B d >=0 for every d in K}`.

Choose finite generators `d^1,...,d^R` of the polyhedral cone `K`. If the physical external contract also requires `e>=0`, define the matrix `N` by stacking

- the `p` coordinate rows of `I_p`, and
- the rows `(B d^r)^T`, `r=1,...,R`.

Then exactly

**`E = R_+^p intersect D_fin = {e : N e >=0}`.**

Redundant generators or redundant rows are harmless for the theorem below; irredundant facet extraction is an optimization, not a mathematical precondition.

This is the key specialization: every T-P5-190 critical-recession inequality is now one active row of a fixed rational polyhedral cone packet.

---

## 2. T191-A — active-face tangent condition separates into drift and homogeneous parts

Let the rows of `N` be `n_1,...,n_m`. For row `i`, define its closed face cone

`F_i := {e : N e>=0, n_i e=0}`.

For affine dynamics `f(e)=A e+c`, the row-`i` tangent condition is

`n_i(A e+c) >=0` for every `e in F_i`.

Because `F_i` is a cone, this is equivalent to the two independent conditions

**`n_i c >=0`,**

and

**`n_i A e >=0` for every `e in F_i`.**

### Proof

Necessity of `n_i c>=0` follows from `0 in F_i`.

Now take any `x in F_i`. For every `t>=0`, also `t x in F_i`, so tangency gives

`t n_i A x + n_i c >=0`.

If `n_i A x<0`, the left side becomes negative for sufficiently large `t`, contradiction. Hence `n_i A x>=0`.

The converse is immediate by addition.

### Consequence

A positive constant inward drift cannot compensate a bad homogeneous face direction globally on an unbounded cone. This is exactly why the global viability checker can be made homogeneous plus one independent drift sign test.

---

## 3. T191-B — exact Farkas/Metzler lift

For each row `i`, consider the condition

`n_i A x >=0` for every `x` satisfying

`N x>=0`, `n_i x=0`.

The dual cone of this face is

`F_i^* = { alpha_i n_i + sum_{j != i} mu_ij n_j : mu_ij>=0 }`,

where `alpha_i` is unrestricted because `n_i x=0` is an equality.

Therefore finite-dimensional Farkas duality gives the exact equivalence

`n_i A >= 0 on F_i`

iff there exist

`alpha_i in R`, `mu_ij>=0 (j != i)`

such that

**`n_i A = alpha_i n_i + sum_{j != i} mu_ij n_j`.**

Assemble these coefficients row by row into `Lambda` by

`Lambda_ii=alpha_i`, `Lambda_ij=mu_ij` for `i != j`.

Then all row identities become one matrix identity:

**`N A = Lambda N`,**

with

**`Lambda_ij>=0` for all `i != j`.**

Combining with T191-A gives the exact theorem:

### Theorem T191-B

For `E_N={e:N e>=0}` and `f(e)=Ae+c`, the following are equivalent:

- `f(e)` belongs to the tangent cone of `E_N` at every `e in E_N`;
- there exists a Metzler matrix `Lambda` such that

  `N A = Lambda N`,

  `N c>=0`.

No rank, pointedness, full-dimensionality, or irredundancy assumption on `N` is required.

---

## 4. Why the diagonal of `Lambda` must remain unrestricted

It would be incorrect to require `Lambda>=0` entrywise.

Take the invariant half-line

`E=R_+`, `N=[1]`,

with stable dynamics

`e'=-e`.

Here `A=[-1]`, so the only possible lift is

`Lambda=[-1]`.

The cone is obviously forward invariant, but `Lambda` has a negative diagonal entry.

The correct positivity class is therefore **Metzler**:

- diagonal: arbitrary;
- off-diagonal: nonnegative.

By contrast, a negative off-diagonal coefficient is a genuine danger. For `N=I_2` and

`A=[[0,-1],[0,0]]`,

start from `(0,1)`. The first coordinate has derivative `-1`, so the nonnegative orthant is not invariant.

---

## 5. T191-C — direct forward-invariance proof from the lift

Assume

`N A=Lambda N`,

`Lambda` Metzler,

`b:=N c>=0`.

Along an affine trajectory define

`y(t):=N e(t)`.

Then exactly

**`y' = Lambda y + b`.**

Choose any scalar `kappa>=0` such that

`G:=Lambda+kappa I`

is entrywise nonnegative. Such a `kappa` exists because only the diagonal entries of `Lambda` may be negative.

Set

`z(t)=exp(kappa t) y(t)`.

Then

`z' = G z + exp(kappa t) b`.

Because `G>=0` entrywise, every power `G^k` is entrywise nonnegative, hence the matrix exponential

`exp(G t)=sum_{k>=0} t^k G^k/k!`

is entrywise nonnegative for `t>=0`.

Variation of constants yields

`z(t)=exp(Gt) z(0) + integral_0^t exp(G(t-s)) exp(kappa s) b ds`.

Every term is componentwise nonnegative whenever `z(0)=N e(0)>=0` and `b>=0`. Therefore

`N e(t)=y(t)>=0`

for every `t>=0`.

Hence:

### Theorem T191-C

**`N A=Lambda N`, `Lambda` Metzler, and `N c>=0` imply forward invariance of `E_N`.**

Together with T191-B this is not merely sufficient: for affine dynamics on the full cone it is the exact algebraic form of the all-face tangent condition.

---

## 6. T191-D — exact failure witnesses

The checker is also fail-closed in a mathematically meaningful way.

### D1. Bad drift

If for some row `i`

`(N c)_i<0`,

then the origin lies in `E_N` and

`d/dt (N e(t))_i |_(t=0) = (N c)_i<0`.

Thus the trajectory starting at the origin immediately leaves the cone.

So the `N c>=0` gate is essential; the homogeneous matrix identity alone is insufficient.

### D2. Bad linear face action

Suppose `(N c)_i>=0` but no Farkas representation exists for row `n_i A`.

By separation/Farkas there is an exact face witness `x` with

`N x>=0`,

`n_i x=0`,

**`n_i A x<0`.**

For the boundary starting point `e0=T x`,

`n_i f(e0)=T n_i A x+n_i c`.

Choosing `T` sufficiently large makes this strictly negative. Therefore `f(e0)` points strictly outside the cone on face `i`.

For rational `N,A,c`, the Farkas feasibility problem is rational polyhedral. If the lift exists it admits a rational `Lambda`; if it fails, a rational face/separation witness can be chosen. Thus the PASS and FAIL packets can both remain exact-rational.

---

## 7. T191-E — specialization to the finite-value cone

Return to the T-P5-190 construction

`E = R_+^p intersect {e : e^T B d>=0 for all d>=0, P d=0}`.

After choosing finite rays `d^r` of the nonnegative kernel cone and stacking

`N=[I_p; (B d^1)^T; ...; (B d^R)^T]`,

the entire trajectory-level finite-valuedness problem for affine external dynamics reduces to:

1. produce exact `N,A,c` under one mathematical/source key;
2. produce exact `Lambda`;
3. check

   `N A=Lambda N`,

   `Lambda_ij>=0` for `i != j`,

   `N c>=0`.

If these pass, every trajectory starting in the finite-value cone remains finite-valued for all forward time.

Therefore T-P5-190's pointwise tangent precondition is automatically available at every time on that trajectory, including active-face switches.

### Important boundary

This does **not** prove the reduced Lyapunov derivative is nonpositive. It only guarantees that the reduced value remains finite and that the T-P5-190 exact right-directional derivative theorem is legally applicable to the actual affine direction `v=Ae+c` along the path. The derivative sign still needs its own LP/margin certificate.

---

## 8. T191-F — finite robust uncertainty: vertexwise lifts are exact

Suppose the external dynamics is allowed to vary in a finite convex family

`f_theta(e)=sum_k theta_k (A_k e+c_k)`,

where

`theta_k>=0`, `sum_k theta_k=1`,

and `theta` may vary with time/state.

If for every vertex `k` there is a Metzler lift `Lambda_k` with

`N A_k=Lambda_k N`,

`N c_k>=0`,

then

`N f_theta(e) = (sum_k theta_k Lambda_k) N e + sum_k theta_k N c_k`.

A convex combination of Metzler matrices is Metzler, and the convex combination of nonnegative drift vectors is nonnegative. Therefore `E_N` is robustly invariant for every time-varying convex blend.

Conversely, if the whole convex family is robustly invariant, each vertex is an allowed dynamics and must itself satisfy the active-face condition; by T191-B each vertex has its own Metzler lift.

Hence:

### Theorem T191-F

For a finite convex affine differential inclusion, robust invariance of `E_N` is equivalent to checking the exact Metzler-lift packet **vertex by vertex**.

No common `Lambda` is required.

This is useful for interval/branch producers: a common lift may be unnecessarily restrictive, whereas separate exact vertex lifts remain complete for a genuine convex-hull model.

---

## 9. T191-G — conservative normal-defect extension

Actual source dynamics may be only approximately affine. Write

`e' = A e+c+rho(t,e)`.

Assume the affine core has a Metzler lift

`N A=Lambda N`.

Let `S=diag(sigma_i)` with `sigma_i>=0`, and let `delta>=0`. Suppose source analysis proves the **normal defect inequality**

**`N rho(t,e) >= -S N e - delta`**

componentwise on the intended domain, together with

**`N c>=delta`.**

Then for `y=N e`,

`y' >= (Lambda-S)y + (N c-delta)`.

The matrix `Lambda-S` is still Metzler because only its diagonal changed, and the forcing `N c-delta` is nonnegative. Thus the same positive-system/first-active-face argument preserves `y>=0`.

Therefore the cone remains forward invariant.

### Structural meaning

The state-proportional defect term `-sigma_i (N e)_i` is harmless at face `i` because it vanishes exactly when that face is active. A constant outward defect is different: it must be paid by a genuine inward drift margin `N c-delta>=0`.

This is deliberately only a sufficient extension. It is attractive for source/interval work because it asks for one-sided error in the physically relevant **facet normals** rather than a Euclidean norm bound.

---

## 10. Counterexamples that pin the checker contract

### 10.1 Forgetting the drift gate creates a false PASS

Take

`E=R_+`, `N=[1]`, `A=[0]`, `c=-1`.

The homogeneous lift `N A=0* N` passes with Metzler `Lambda=0`, but the origin immediately moves negative. Therefore `N c>=0` cannot be omitted.

### 10.2 Requiring nonnegative diagonal creates a false FAIL

Take

`E=R_+`, `e'=-e`.

The cone is invariant, but the unique scalar lift is `Lambda=-1`. Therefore only off-diagonal nonnegativity is valid.

### 10.3 External orthant invariance does not imply finite-value-cone invariance

T-P5-190 already exhibited an external direction that stays in `e>=0` while violating a critical recession inequality. In the present global form, this simply means that checking only the `I_p` rows of `N` is insufficient: the additional `(B d^r)^T` rows must participate in the same Metzler lift.

### 10.4 A common lift across uncertainty vertices is not necessary

T191-F allows a different `Lambda_k` for each affine vertex. Requiring one common `Lambda` would add an artificial coupling not present in the robust tangent condition and could reject a genuinely invariant convex family.

---

## 11. Exact checker packet

For rational data the trusted-side packet can be tiny.

### `FiniteConeAffineViabilityPacket`

- rational matrix `N`;
- rational affine field `A,c`;
- rational matrix `Lambda`;
- exact equality `N*A = Lambda*N`;
- exact signs `Lambda_ij>=0` for `i!=j`;
- exact signs `N*c>=0`.

### Optional robust packet

- one packet per affine uncertainty vertex, or
- a normal-defect packet `S,delta` with
  `S` diagonal/nonnegative,
  `N rho >= -S N e-delta`,
  `N c>=delta`.

No square root, matrix inverse, determinant, eigenvalue, pseudoinverse, active-face enumeration at runtime, or nonlinear optimizer is required by the affine core checker.

---

## 12. Suggested Lean theorem leaves

The cleanest decomposition is:

1. `affineFacetTangent_iff_drift_and_homogeneous`
   - scaling argument on a cone;
2. `faceDual_farkas_rowRepresentation`
   - `n_i A` nonnegative on `F_i` iff row representation with nonnegative off-diagonal coefficients;
3. `allFacetRows_iff_exists_metzlerLift`
   - assemble the row certificates into `N A=Lambda N`;
4. `metzler_affine_nonneg_invariant`
   - positive-system invariance for `y'=Lambda y+b`, `b>=0`;
5. `polyhedralCone_affine_invariant_iff_metzlerLift`
   - combine 1–4;
6. `finiteValueCone_affine_invariant_of_metzlerLift`
   - instantiate `N` from T-P5-190 generator rows;
7. `convexAffineFamily_invariant_of_vertexMetzler`
   - T191-F;
8. `normalDefect_invariant_of_metzlerLift`
   - T191-G.

For an initial formal pass, theorem 4 can be proved independently from matrix-exponential APIs by a standard orthant-positive ODE lemma; the Farkas row representation can remain a separate dependency so that the core matrix identity and sign transport stay elementary.

---

## 13. What remains open

This child does not provide:

1. actual source-bound `P,B` and generator matrix `N` under a Route-B/PDE key;
2. proof that the real external vector field is affine `A e+c`, convex-affine, or satisfies the normal-defect inequality;
3. source/trajectory domain coverage for the proposed affine or defect packet;
4. the T-P5-190 directional derivative **sign** or a uniform Lyapunov margin over all states;
5. Float64/interval outward-rounding semantics for `N,A,c,Lambda` or defect bounds;
6. Lean/kernel compilation;
7. independent validation by 封不觉;
8. P8/M4 propagation, admission, or registry closure.

The shortest next mathematical step after an actual `N,A,c` packet exists is not another abstract cone theorem: it is to combine this viability lift with T-P5-190's zero-residual derivative LP and ask for a **facet/stratum-uniform negative derivative margin**. Without source-bound dynamics, further abstraction would risk outrunning the real obstruction.

---

## 14. Recommended producer/consumer handoff

For the source/CSE lane, the most useful next packet is:

- finite nonnegative-kernel rays `d^r` or directly the exact row matrix `N`;
- one exact affine/vertex-affine external dynamics packet `A,c` on the same key;
- one rational `Lambda` per affine vertex satisfying the three T191 gates.

If the actual field is not affine, do not force it into this theorem. Instead produce a candidate affine core plus a one-sided normal defect bound `N rho >= -S N e-delta`; the theorem then states exactly how much inward drift margin must pay the constant defect.

This keeps trajectory viability, directional-derivative negativity, source identity, Float64 semantics, and final admission as separate proof obligations rather than hiding them in one opaque flowpipe claim.