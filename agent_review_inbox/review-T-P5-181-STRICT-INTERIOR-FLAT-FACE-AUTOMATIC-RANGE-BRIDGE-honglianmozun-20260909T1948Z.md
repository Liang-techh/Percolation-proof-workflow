---
kind: review_result
review_id: review-T-P5-181-strict-interior-flat-face-automatic-range-bridge-honglianmozun-20260909T1948Z
task_id: T-P5-181-STRICT-INTERIOR-FLAT-FACE-AUTOMATIC-RANGE-BRIDGE
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T19:48:00Z
claim_commit: 87f3bf96816614e17241a9305846895a5a1bd62a
inspected_commit: b8a80378eb645891007d53d5d77855afd64e958b
upstream_commits:
  - 7d1827e843a23ede07165af1be09ce4626bc6916  # T-P5-177 zero-loaded flat-face residual floor
  - 953eb401979eeb1374e4e4c722a5c29588e6a498  # T-P5-178 critical-cone Schur bridge
  - a0fba26798157e76c4e0ed1fab78da0c05059605  # T-P5-179 canonical support descent
  - 1762b755f4bd220efe4e108d9588f0fa3697f6fa  # T-P5-180 corank-one anchor Schur reduction
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_interior_flat_face_range_bridge; reuse_T177_dual_variables_as_T178_range_solves; add_arbitrary_corank_strict_contact_fast_path; preserve_boundary_support_descent
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional kernel/tangent algebra; exact Fraction regression for corank-two and boundary examples
exit_code: 0 for exact rational regressions; no Lean/kernel run
---

# T-P5-181 — strict-interior flat-face contact automatically closes the hidden-kernel range gate

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-177 gives an exact first-order residual floor on a zero-loaded active face. T-P5-178 then says that a zero-residual inactive row is not yet safe: at second order it must annihilate the **entire** active kernel, equivalently lie in `range(A)`. T-P5-180 removes that extra range gate when `corank(A)=1`.

This review closes a different and complementary branch:

> **If the T-P5-177 row is first-order safe on the whole normalized kernel polytope and reaches zero at a strictly positive kernel state, then the row automatically annihilates the whole kernel, regardless of the corank of `A`.**

Equivalently, in the exact T-P5-177 primal/dual packet, a strictly positive zero contact forces the nonnegative dual slack to vanish coordinatewise. The existing T-P5-177 dual variable is therefore already an exact T-P5-178 range solve.

This is useful because it bypasses both a kernel-basis search and the corank-one restriction. The only extra mathematical datum is a strict-positive normalized zero contact. If the optimizer lies on the boundary, the conclusion is false and T-P5-179 support descent remains mandatory.

No actual source identity, whole-support/global copositivity, physical coverage, runtime/Float64 semantics, Lean/kernel validation, independent verification, admission, registry mutation, or P5 parent closure is claimed.

---

## 1. Setup: the T-P5-177 zero-loaded kernel polytope

Let

`A=A^T >= 0` in `R^{m x m}`

and assume the normalized nonnegative kernel section is nonempty:

`Z := { z in R^m : A z=0, z>=0, 1^T z=1 }`.

For one inactive row, write its active coupling at the candidate floor as a column vector

`ell in R^m`.

In the T-P5-177 specialization,

`ell(D) = r_0 + (D g_i/2) 1`,

where `r_0=R_0[i,S]^T` and the active loading is exactly `g_S=0`.

The row is first-order safe on the whole flat face exactly when

`ell^T z >=0` for every `z in Z`.

A critical contact is a `z_* in Z` with

`ell^T z_*=0`.

The new branch assumes additionally

`z_*>0` coordinatewise.

The active kernel may have arbitrary dimension.

---

## 2. T181-A — interior zero of a nonnegative kernel-linear functional annihilates the whole kernel

### Theorem

Assume

1. `A=A^T`;
2. `z_* in ker(A)`;
3. `z_*>0`;
4. `1^T z_*=1`;
5. `ell^T z >=0` for every `z in Z`;
6. `ell^T z_*=0`.

Then

**`ell^T n =0` for every `n in ker(A)`.**

Therefore, by symmetry,

**`ell in ker(A)^perp = range(A)`.**

### Proof

Take arbitrary `n in ker(A)` and define

`alpha := 1^T n`,

`h := n-alpha z_*`.

Then

`A h=0`

and

`1^T h = 1^T n-alpha 1^T z_* =0`.

Because every coordinate of `z_*` is strictly positive, there exists `eps>0` such that both

`z_*+eps h >=0`

and

`z_*-eps h >=0`.

Both vectors remain in `ker(A)` and remain normalized because `1^T h=0`. Hence both belong to `Z`.

First-order safety and `ell^T z_*=0` give

`0 <= ell^T(z_*+eps h) = eps ell^T h`,

`0 <= ell^T(z_*-eps h) = -eps ell^T h`.

Thus

`ell^T h=0`.

Finally

`ell^T n = alpha ell^T z_* + ell^T h =0`.

Since `n` was arbitrary, `ell` annihilates `ker(A)`. For symmetric `A`, `range(A)=ker(A)^perp`, so `ell in range(A)`.

QED.

### Stronger consequence: the entire normalized kernel face ties

Because `ell` annihilates the whole kernel,

**`ell^T z=0` for every `z in Z`.**

So a linear residual that is nonnegative on `Z` cannot have an isolated zero at a strictly positive kernel point. An interior zero forces the whole normalized kernel polytope to become a zero-residual face.

This is the key geometric fingerprint.

---

## 3. T181-B — exact primal/dual complementarity makes the range solve explicit

T-P5-177 supplies a checker-friendly dual form for row safety. Suppose the trusted packet contains

**`ell = A y + w`, with `w>=0`.**

Let `z_*>0` satisfy

`A z_*=0`, `ell^T z_*=0`.

Then

`0 = ell^T z_*`

`  = y^T A z_* + w^T z_*`

`  = w^T z_*`.

Every coordinate of `z_*` is strictly positive and every coordinate of `w` is nonnegative. Therefore

**`w=0`.**

Hence the T-P5-177 dual packet collapses to

**`A y = ell`.**

So the dual variable `y` is already the exact T-P5-178 range solve. No second Gaussian elimination, pseudoinverse, kernel basis, corank test, or approximate range residual is needed.

### Matrix version for all critical rows

Let `I` be the set of inactive rows whose residual is exactly zero at the same strict-positive contact `z_*`. Stack them as

`B_I in R^{p x m}`.

Suppose the rowwise T-P5-177 dual packet is stacked as

**`B_I^T = A Y + W`, `W>=0` entrywise.**

The critical-contact equations are

**`B_I z_*=0`.**

Multiplying the dual identity by `z_*^T` gives

`0 = z_*^T W`.

Because `z_*>0` and `W>=0`, every column of `W` is zero. Thus

**`W=0`, hence `A Y=B_I^T`.**

This is exactly the hidden-kernel compatibility demanded by T-P5-178.

---

## 4. T181-C — direct continuation into the T-P5-178 Schur energy

After Section 3, define

`H := C_II - B_I Y`.

Because

`A Y=B_I^T`,

we have

`B_I Y = Y^T A Y`,

so `H` is symmetric. For arbitrary signed active direction `u in R^m` and nonnegative critical inactive direction `eta in R_+^p`,

`u^T A u + 2 eta^T B_I u + eta^T C_II eta`

has the exact decomposition

**`= (u+Y eta)^T A (u+Y eta) + eta^T H eta`.**

Therefore the local critical-cone condition is now reduced immediately to

**`H` copositive on `R_+^p`.**

The important routing point is that the first-order LP and second-order Schur stage share the same `Y`:

`T-P5-177 dual safety packet`

`+ strict-positive zero contact`

`=> dual slack vanishes`

`=> T-P5-178 exact range solve already available`

`=> only reduced copositivity remains`.

This removes an entire proof seam in the strict-interior branch.

---

## 5. T181-D — specialization to a sharp zero-loaded row floor

Return to

`ell(D)=r_0+(D g_i/2)1`.

Assume `g_i>0` and define

`mu_i := min_{z in Z} r_0^T z`.

T-P5-177 gives the rowwise sharp first-order floor

`D_i = -2 mu_i/g_i`

when `mu_i<0`.

Suppose the minimum is attained by some

`z_*>0`.

At `D=D_i`,

`ell(D_i)^T z_* = mu_i + D_i g_i/2 =0`,

and by construction

`ell(D_i)^T z>=0`

for all `z in Z`.

T181-A therefore gives

**`ell(D_i) in range(A)`.**

Equivalently,

**`r_0 - mu_i 1 in range(A)`.**

Even more strongly, for every `z in Z`,

**`r_0^T z = mu_i`.**

Thus a strict-positive optimizer of the rowwise residual LP certifies that the base residual was actually constant over the whole normalized kernel polytope. The LP is geometrically degenerate in exactly the way needed to remove the hidden-kernel shear.

This statement is valid at arbitrary corank.

### Zero-loading on the inactive row

If `g_i=0`, the same logic still applies whenever the row is uniformly safe and has a strict-positive zero contact. Then `r_0 in range(A)` directly. If instead T-P5-177 has `mu_i<0`, no `D` can repair the row, exactly as already recorded there.

---

## 6. Relation to T-P5-180: complementary, not redundant

T-P5-180 assumes

`corank(A)=1`

and only needs the pointwise critical equation

`b^T z=0`.

That is enough because the one positive kernel generator spans the whole kernel.

T181 instead allows

**arbitrary `corank(A)`**

but uses the stronger information already available in the T-P5-177 branch:

`ell^T z>=0` on the **whole** normalized kernel polytope (or equivalently a T177 dual safety packet).

Thus the two fast paths are complementary:

- `corank(A)=1` + pointwise zero residual -> T-P5-180;
- arbitrary corank + global first-order safety + strict-positive zero contact -> T-P5-181;
- arbitrary corank + boundary contact -> T-P5-179 support descent / general T-P5-178.

---

## 7. Exact corank-two regression — T181 closes a branch T180 cannot enter

Take

`v=(1,-1,0)^T`,

`A=v v^T`

so

`A=[[1,-1,0],[-1,1,0],[0,0,0]]`.

Then

`A>=0`, `rank(A)=1`, `corank(A)=2`.

The normalized nonnegative kernel polytope is

`Z={ (a,a,1-2a) : 0<=a<=1/2 }`.

It contains the strict-positive point

`z_*=(1/3,1/3,1/3)`.

Choose one inactive row with base coupling

`r_0=(0,-2,-1)^T`

and `g_i=1`. For every `z in Z`,

`r_0^T z = -1`.

Hence

`mu=-1`

and T-P5-177 gives the exact first-order floor

**`D_*=2`.**

At this floor,

`ell(D_*)=r_0+1=(1,-1,0)^T=v`.

Thus

`ell(D_*)^T z=0`

for every `z in Z`, and in particular at `z_*>0`.

T180 cannot be used because `corank(A)=2`. T181 gives immediately

`ell(D_*) in range(A)`.

Indeed the exact solve is

`y=v/2`,

because

`A(v/2)=v`.

Now choose the inactive diagonal at the contact to be

`C_II=[1]`.

Then

`H = 1-v^T(v/2)=1-1=0`.

The entire mixed second-order energy becomes the perfect square

**`u^T A u + 2 eta v^T u + eta^2 = (v^T u+eta)^2 >=0`.**

So this is a genuine higher-corank strict-interior contact where the first-order floor and the second-order range solve close seamlessly.

For a literal zero-loaded affine family one may take the inactive diagonal base value `C_0=-1`, since the same `g_i=1` contributes `+D` on the inactive diagonal; at `D=2` the contact diagonal is exactly `1` as above.

### Exact Fraction regression

The exact rational checks give

- `r_0^T(a,a,1-2a)=-1` at `a=0,1/3,1/2` and symbolically for all `a`;
- `ell(D_*)^T z=0` on the same polytope;
- `A(v/2)=v`;
- `v^T(v/2)=1`.

No floating tolerance is involved.

---

## 8. Strict positivity is essential — exact boundary counterexample

Use the same corank-two active matrix

`A=[[1,-1,0],[-1,1,0],[0,0,0]]`

and the same kernel polytope

`Z={ (a,a,1-2a) : 0<=a<=1/2 }`.

Take

`ell=(1,1,0)^T`.

Then for every `z=(a,a,1-2a) in Z`,

`ell^T z = 2a >=0`.

The minimum is zero at the boundary contact

`z_0=(0,0,1)`.

But

`ell` is **not** in `range(A)=span{(1,-1,0)}`.

Equivalently, take the exact T-P5-177-style dual packet

`y=0`,

`w=ell>=0`,

so

`ell=A y+w`.

At the boundary contact

`w^T z_0=0`

but `w!=0`: complementary slack can live entirely on coordinates where the contact is zero.

This is exactly why the strict-positive hypothesis cannot be weakened to mere `z>=0`.

It is also why a boundary contact must first be canonicalized by T-P5-179. If one falsely treats coordinates 1 and 2 as two-sided active directions, the missing range condition looks like a hidden-kernel failure; physically those coordinates start at zero and are one-sided, so the signed shear argument is invalid until support descent is performed.

---

## 9. Structural fingerprint

The new reusable fingerprint is:

**interior flat-face contact -> primal/dual complementarity -> dual slack extinction -> automatic range compatibility -> Schur energy continuation.**

In practical terms:

1. T-P5-177 proves a row nonnegative over the normalized zero-energy kernel polytope and returns `ell=A y+w`, `w>=0`;
2. if an exact contact has `z>0` and `ell^T z=0`, do **not** launch a new kernel/range search;
3. exact complementarity forces `w=0`;
4. reuse the same `y` as the T-P5-178 range solve;
5. only the reduced copositivity of `H` remains;
6. if the contact has zero coordinates, fail closed and route through T-P5-179 support descent.

This is a Lyapunov-energy statement, not merely LP bookkeeping: the first-order barrier certificate itself supplies the second-order completion variable once the contact is interior.

---

## 10. Candidate formal theorem statements

### `interior_kernel_linear_zero_mem_range`

Given symmetric `A`, normalized `z>0` with `Az=0`, and `ell` nonnegative on

`{x>=0 | Ax=0, sum x=1}`,

if `ell dot z=0`, conclude

`ell in LinearMap.range A`.

### `nonnegative_slack_vanishes_at_strict_contact`

If

`ell=A y+w`, `w>=0`, `Az=0`, `z>0`, and `ell dot z=0`,

then

`w=0` and `A y=ell`.

### `critical_rows_reuse_flat_face_duals`

If

`B^T=A Y+W`, `W>=0`, `Az=0`, `z>0`, and `Bz=0`,

then

`W=0` and `A Y=B^T`.

### `strict_interior_flat_face_schur`

Under the previous theorem, define

`H=C-BY`.

Then

`u^T A u+2 eta^T B u+eta^T C eta`

`=(u+Y eta)^T A(u+Y eta)+eta^T H eta`,

and mixed-cone nonnegativity is equivalent to copositivity of `H`.

These are source-independent theorem candidates only; no Lean compile is claimed.

---

## 11. Checker-facing rational packet

For a strict-positive T-P5-177 contact, a division-free trusted packet can contain

1. exact rational `A,z,B_I,C_II`;
2. `A=A^T>=0` evidence from the upstream active-face branch;
3. `Az=0`;
4. `z_j>0` for every active coordinate;
5. `1^T z=1`;
6. `B_I z=0`;
7. the already-produced T-P5-177 dual matrices `Y,W` satisfying
   `B_I^T=A Y+W` and `W>=0`.

The checker then proves `W=0` by exact positive/nonnegative complementarity, rewrites the same packet as

`A Y=B_I^T`,

forms

`H=C_II-B_IY`,

and dispatches `H` to the existing P5 copositivity machinery.

No inverse, pseudoinverse, kernel basis, SVD/eigenvector, root extraction, floating tolerance, or second range-solve packet is required.

---

## 12. Boundaries and fail-closed conditions

### Boundary A — boundary contacts do not kill dual slack

The exact example in Section 8 shows `z>=0`, `ell^T z=0`, `w>=0`, `w^Tz=0` does not imply `w=0` when some coordinates of `z` vanish. Route through T-P5-179.

### Boundary B — pointwise zero alone is insufficient at higher corank

Without either T-P5-177 whole-face safety/dual slack or the T-P5-180 corank-one assumption, `ell^T z=0` at one positive kernel vector does not by itself prove `ell in range(A)`. T-P5-178's hidden-kernel obstruction remains authoritative.

### Boundary C — automatic range closure does not imply reduced copositivity

T181 removes the range gate only. The reduced matrix

`H=C_II-B_IY`

can still fail copositivity, especially with multiple critical rows. Existing T-P5-155/158/164/165/166/170-style copositivity/energy dispatch remains necessary.

### Boundary D — local contact is not global P5 closure

The theorem concerns one flat-face contact/support. All other supports and remote orthant directions remain part of the global dispatcher.

### Boundary E — exact residual classification is required

A numerically small residual cannot be treated as zero. Positive rows need a signed positive margin; negative rows already fail the first-order gate.

### Boundary F — external gates remain open

Same-key source identity, physical domain/cell coverage, Float64/runtime semantics, ODE/P8 meaning, Lean/kernel receipt, independent 封不觉 validation, admission, registry mutation, and P5 parent closure are all outside this review and remain pending.

---

## 13. Recommended routing after T181

For a T-P5-177 zero-loaded active face:

1. compute/prove the rowwise first-order floor and retain its exact dual packet;
2. canonicalize any returned zero contact to its true positive support (T-P5-179);
3. if the canonical active contact is strict-positive in the current face and the T177 dual certificate is still the same-face certificate, apply T181 and reuse the dual variable as the range solve;
4. if `corank(A)=1` but whole-face first-order safety is not available, T-P5-180 remains the cheaper pointwise branch;
5. otherwise use the full T-P5-178 hidden-kernel/range-solve route;
6. after range closure, dispatch only the reduced `H` to the existing copositivity stack.

This keeps first-order Lyapunov residual geometry and second-order Schur completion coupled instead of recomputing them as unrelated certificates.
