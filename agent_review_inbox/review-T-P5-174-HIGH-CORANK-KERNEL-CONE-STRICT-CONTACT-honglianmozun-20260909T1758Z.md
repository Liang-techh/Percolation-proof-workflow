---
kind: review_result
review_id: review-T-P5-174-high-corank-kernel-cone-strict-contact-honglianmozun-20260909T1758Z
task_id: T-P5-174-HIGH-CORANK-KERNEL-CONE-STRICT-CONTACT
reviewer: 红莲魔尊
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T17:58:00Z
claim_commit: 38848196d3332b1f6c50c223707bbf91721c3f6a
inspected_commit: cb3aea20020e690eb7f835da1999a89e07b2ad39
upstream_commits:
  - 1b63698a429d0b2530de38e6632d29076b52e475  # T-P5-173 corank-one strict-complementarity minors
  - 8caf78bf7ce97b3a727a46c12739583a12d777f7  # T-P5-171 contact/KKT transport
  - f1eb76d8657edac28a04aaec289a7198a8c648d1  # T-P5-170 iterated pivot energy chain
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_high_corank_zero_energy_contact_linear_alternative; use_primal_exact_kernel_contact_or_dual_range_obstruction_packets; keep_corank_one_adjugate_as_fast_path_and_symbolic_D_high_corank_as_separate_open_branch
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional linear/quadratic algebra; exact SymPy rational regression for the two displayed 4x4 examples
exit_code: 0 for exact symbolic regression; no Lean/kernel run
---

# T-P5-174 — high-corank kernel-cone strict-contact alternative

## 0. Verdict and exact seam

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-173 closes the strict-complementarity contact problem when the active principal block has corank one: a nonzero adjugate column supplies the positive kernel witness and inactive residuals become row-replacement determinants. It explicitly leaves the higher-corank case open because then `adj(A)` may vanish identically even though a genuine positive zero-energy contact exists.

This review closes exactly that higher-corank fixed-candidate seam.

The key point is that once the active energy block is PSD, its zero-energy set is a **linear kernel subspace**. Asking whether that flat Lyapunov face contains a physical contact with strictly positive active coordinates and strictly positive inactive KKT residuals is therefore not a nonlinear eigenvector problem at all. It is one finite system of strict linear inequalities on the kernel.

Even better, failure has an exact dual energy obstruction: there exist nonnegative weights on the active-positivity and inactive-residual constraints whose weighted vector lies in `range(A)`. Such a vector is orthogonal to every zero-energy direction, so no kernel direction can make all requested quantities strictly positive. For rational data, either the positive contact or this obstruction can be returned with exact rational witnesses; no pseudoinverse, eigenvector, square root, or floating optimization is required.

No source/provenance audit, runtime/Float64 claim, Lean/kernel validation, independent re-audit, admission, registry mutation, or parent closure is performed.

---

## 1. Active zero energy is exactly the kernel

Let `M=M^T` be a finite real symmetric matrix and fix a proposed positive support `S`. Let `T` denote the complementary inactive index set. Write

`A := M[S,S]`,

`R := M[T,S]`.

Assume the active block is PSD:

**(1.1)** `A >= 0`.

T-P5-173 proves that this premise is automatic once a globally copositive matrix already has a positive-support zero contact on `S`. Here it is taken as the branch premise because we want to characterize **all** active zero-energy directions.

### Theorem T174-A — `psd_zero_energy_iff_kernel`

For every real vector `z` on `S`,

**(1.2)** `z^T A z = 0`

iff

**(1.3)** `A z = 0`.

The reverse implication is immediate. For the forward implication, fix any real `y` and consider

`p(t)=(z+t y)^T A(z+t y)`.

By PSD, `p(t)>=0` for every real `t`. Under `z^T A z=0`,

`p(t)=2t y^T A z+t^2 y^T A y`.

If `y^T A z` were nonzero, choosing sufficiently small `t` with the opposite sign would make `p(t)<0`. Hence `y^T A z=0` for every `y`, so `Az=0`.

Thus the flat Lyapunov/energy face is not merely contained in the kernel; it **is** the kernel.

### Contact interpretation

Pad an active vector `z` by zeros on `T`:

`x := pad_S(z)`.

If `Az=0`, then

**(1.4)** `q_M(x)=x^T Mx=z^T A z=0`,

and

**(1.5)** `(Mx)_S=0`,

**(1.6)** `(Mx)_T=Rz`.

Therefore a strict orthant-KKT zero contact with **exact support `S`** is precisely an active vector satisfying

**(1.7)** `Az=0`,

**(1.8)** `z>0`,

**(1.9)** `Rz>0`.

Global copositivity remains a separate PASS gate. The equations above construct the contact geometry; they do not by themselves certify that `M` is copositive away from the contact.

---

## 2. Kernel-basis reduction: strict contact is one linear cone problem

Let `Z` be any exact basis matrix for `ker(A)`:

**(2.1)** `AZ=0`,

**(2.2)** `im(Z)=ker(A)`.

Every active zero-energy vector is uniquely represented up to the chosen basis coordinates as

`z=Zc`.

Define the stacked contact matrix

**(2.3)**

`B := [ Z ; RZ ]`.

The upper block records physical positivity on active coordinates; the lower block records strict inactive KKT residuals.

### Theorem T174-B — `strict_contact_iff_kernel_cone_hits_positive_orthant`

There exists a strict zero-energy contact on support `S` iff

**(2.4)** there exists `c` such that `Bc>0` componentwise.

Equivalently, directly in state coordinates, iff there exists `z` satisfying (1.7)-(1.9).

This is exact and finite-dimensional. No normalization is mathematically necessary.

### Scale-normalized checker form

Because all inequalities are homogeneous, strict feasibility is equivalent to the closed rational-looking system

**(2.5)** `Az=0`,

**(2.6)** `z_i>=1` for every `i in S`,

**(2.7)** `(Rz)_j>=1` for every `j in T`.

Indeed, any strict solution can be multiplied by a positive scalar so that the minimum of all finitely many positive coordinates/residuals is at least one. Conversely a solution of (2.5)-(2.7) is strict.

This is the preferred producer interface in the higher-corank branch: **one exact linear feasibility packet** replaces a pseudoinverse/nullvector search.

---

## 3. Exact Gordan/Stiemke alternative

The strict cone feasibility above has a sharp dual obstruction.

### Theorem T174-C — `kernel_contact_gordan_alternative`

Exactly one of the following two statements holds.

### Primal strict contact

There exists `z` such that

`Az=0`, `z>0`, `Rz>0`.

### Dual range obstruction

There exist vectors

`u>=0` on `S`,

`v>=0` on `T`,

not both zero, and some real `h` on `S`, such that

**(3.1)**

`A h = u + R^T v`.

#### Mutual exclusion

Suppose both existed. Multiply (3.1) by a primal kernel vector `z`:

`z^T u + (Rz)^T v`

`= z^T A h`

`= (Az)^T h`

`=0`.

But `z>0`, `Rz>0`, and `u,v>=0` with at least one positive component imply

`z^T u+(Rz)^T v>0`,

a contradiction.

#### Why one alternative must exist

Using a kernel basis `Z`, primal feasibility is exactly

`[Z;RZ] c >0`.

If no such `c` exists, the Gordan/Stiemke theorem of alternatives yields a nonzero vector

`y=(u,v)>=0`

with

`[Z;RZ]^T y=0`.

Thus

`Z^T(u+R^T v)=0`.

Because `A` is symmetric and `im(Z)=ker(A)`,

`ker(A)^perp = range(A)`.

Therefore `u+R^T v in range(A)`, which is exactly (3.1) for some `h`.

Conversely any (3.1) gives `Z^T(u+R^Tv)=Z^TAh=0`, hence the Gordan dual witness.

So this is a true **iff alternative**, not merely a sufficient obstruction.

---

## 4. Energy meaning of the dual obstruction

The dual packet has a useful structural interpretation.

The vector

`w := u + R^T v`

is a nonnegative weighted combination of two things we want to make strictly positive along a zero-energy direction:

1. the active state coordinates themselves (`u`), and
2. the inactive gradient/KKT residuals (`R^T v`).

The equation

`w=Ah`

says this weighted combination lies entirely in the **restoring/dissipative range** of the active quadratic energy.

Every flat direction `z in ker(A)` is orthogonal to that range:

`z^T w=z^TAh=0`.

Hence the weighted positive quantity

**(4.1)** `u^T z+v^T Rz`

is forced to vanish on every zero-energy direction. If `u,v` are nonnegative and nontrivial, no such direction can make every active coordinate and every selected inactive residual strictly positive.

This yields a reusable structural fingerprint:

> **PSD active energy + higher-dimensional kernel:** first search the kernel cone. If it misses the strict physical/KKT cone, return a nonnegative range(A) dual obstruction instead of choosing a pseudoinverse-based nullvector or perturbing the matrix numerically.

The obstruction is invariant under the choice of kernel basis.

---

## 5. Rational exact certificates

Assume now that `A` and `R` are rational matrices.

### Theorem T174-D — `rational_strict_contact_or_rational_range_obstruction`

Exactly one of the following rational certificate types exists.

### Rational primal packet

A rational vector `z` with

**(5.1)** `Az=0`,

**(5.2)** `z>=1`,

**(5.3)** `Rz>=1`.

### Rational dual packet

Rational vectors `u,v,h` satisfying

**(5.4)** `u>=0`, `v>=0`,

**(5.5)** `1^T u + 1^T v = 1`,

**(5.6)** `Ah=u+R^T v`.

#### Why rational witnesses exist

If a real strict primal solution exists, strict inequalities define an open subset of the rational affine space `ker(A)`. Rational points are dense in that affine subspace, so there is a rational strict solution; positive scaling gives (5.2)-(5.3).

If the primal does not exist, the normalized dual feasible set

`u,v>=0`, `sum(u)+sum(v)=1`, `u+R^Tv in range(A)`

is a nonempty rational polyhedron. A nonempty rational polyhedron has a rational feasible point. Since `A` and the right-hand side are rational, the consistent system `Ah=u+R^Tv` also has a rational solution `h`.

Thus the higher-corank branch admits a purely exact rational handshake in either direction.

### Checker consequence

The trusted checker does not need to compute a kernel basis at all. It can accept either:

- **PASS/contact:** exact rational `z` and verify (5.1)-(5.3), or
- **NO-STRICT-CONTACT obstruction:** exact rational `u,v,h` and verify (5.4)-(5.6).

All checks are additions, multiplications, equality, and order comparisons.

A kernel basis remains useful for discovery, but it is not required in the final trusted packet.

---

## 6. Exact higher-corank example where T-P5-173 adjugate fast path is silent

Take the active block

`A = [[ 1,-1, 0],`
`     [-1, 1, 0],`
`     [ 0, 0, 0]]`.

Then

`A = a a^T`, with `a=(1,-1,0)^T`,

so `A>=0`, `rank(A)=1`, and

**(6.1)** `corank(A)=2`.

Because a `3x3` matrix of rank one has every `2x2` minor zero,

**(6.2)** `adj(A)=0`.

Thus every T-P5-173 adjugate column vanishes and the corank-one fast path is correctly inapplicable.

Now choose one inactive coordinate with

`R=[1,1,1]`.

The active vector

`z=(1,1,1)^T`

satisfies

**(6.3)** `Az=0`,

**(6.4)** `z>0`,

**(6.5)** `Rz=3>0`.

Hence T174 gives a strict contact immediately.

To show this is compatible with a genuine copositive full matrix, take inactive diagonal `1`:

`M = [[ 1,-1, 0, 1],`
`     [-1, 1, 0, 1],`
`     [ 0, 0, 0, 1],`
`     [ 1, 1, 1, 1]]`.

For `x1,x2,x3,t>=0`,

**(6.6)**

`x^T M x`
`=(x1-x2)^2 + 2t(x1+x2+x3)+t^2`
`>=0`.

So `M` is copositive (although it is not ordinary PSD). At

`x_*=(1,1,1,0)^T`,

**(6.7)** `q_M(x_*)=0`,

**(6.8)** `Mx_*=(0,0,0,3)^T`.

This is a strict inactive KKT contact with a **two-dimensional active kernel and identically zero adjugate**. It is the exact branch T-P5-173 said must be handled separately.

---

## 7. Exact obstruction example: positive zero-energy contact exists, strict complementarity does not

Keep the same active block `A`, but change the inactive row to

`R=[1,-1,0]`.

Every active kernel vector satisfies `z1=z2`, hence

**(7.1)** `Rz=0`

for every `z in ker(A)`.

There are many positive zero-energy vectors, e.g. `z=(1,1,1)`, but **no** one of them can have a strictly positive inactive residual.

The dual obstruction is one line:

choose

`u=0`, `v=1`, `h=e1`.

Then

**(7.2)**

`Ah=(1,-1,0)^T=R^T=u+R^T v`.

The dual normalization is already `sum(u)+sum(v)=1`.

Thus T174-D certifies impossibility of strict complementarity without searching the kernel.

Again this is compatible with a fully safe matrix. With inactive diagonal `1`,

`M = [[ 1,-1,0, 1],`
`     [-1, 1,0,-1],`
`     [ 0, 0,0, 0],`
`     [ 1,-1,0, 1]]`,

and for every real state

**(7.3)**

`x^T Mx=(x1-x2+t)^2>=0`.

So the full matrix is PSD. The contact `x=(1,1,1,0)` is real and nonnegative, but its inactive residual is exactly zero. This proves that

- existence of a positive higher-corank kernel contact,
- and strict complementarity of that contact

are genuinely different obligations.

---

## 8. Relation to T-P5-170/171 and sharp-floor consumers

T-P5-170/171 remain the preferred route when a sign-compatible pivot chain cheaply reduces the dimension.

If the terminal or lifted active contact block lands in corank one, use T-P5-173's determinant/adjugate fast path.

If the active adjugate vanishes or a higher-dimensional kernel is otherwise known, use T174 instead:

1. keep the exact active block `A` and inactive row block `R`;
2. submit either a rational strict-contact vector `z`, or a rational dual range obstruction `(u,v,h)`;
3. if a strict contact exists at a candidate sharp floor, hand that contact to T-P5-169/T-P5-171 for the lower-floor FAIL witness and support transport;
4. do not resolve a pseudoinverse merely to select one arbitrary kernel representative.

T174 does **not** redo global copositivity. A contact packet is consumed only after the candidate matrix has a separate copositivity PASS route.

---

## 9. Boundaries and remaining obligations

### Boundary A — symbolic `D` in a changing high-corank locus

This review is a **fixed-candidate exact theorem**. If `A=A_D` and the higher-dimensional kernel itself changes with an algebraic floor parameter `D`, the joint symbolic problem `A_D z=0`, `z>0`, `R_D z>0` is bilinear in `(D,z)` and is not being claimed to remain a rational LP.

T-P5-172/T-P5-173 remain the efficient symbolic branch for corank-one contacts. Higher-corank symbolic continuation needs a separate elimination/stratification theorem.

### Boundary B — non-strict residuals

Replacing `Rz>0` by `Rz>=0` changes the theorem of alternatives and permits support expansion / degenerate KKT contacts. A dual strict-contact obstruction does not imply that no non-strict zero contact exists; Section 7 is the explicit counterexample.

### Boundary C — PSD premise and global PASS

For a certified copositive zero contact the active PSD property follows from T-P5-173. Outside that composition, T174's linear equations can construct a KKT zero point even if the full matrix fails elsewhere. Do not interpret a primal contact packet as a copositivity certificate.

### Boundary D — source/runtime/admission

No actual source matrix, physical cell, uncertainty coverage, Float64 implementation, Lean theorem, independent verification, admission, or registry state is closed here.

---

## 10. Candidate theorem statements for formalization

The minimal reusable theorem layer is:

1. `psd_zero_energy_iff_mulVec_zero`
   - `A=A^T`, `A>=0`;
   - `z^T A z=0 <-> Az=0`.

2. `strictOrthantContact_of_kernel`
   - `Az=0`, `z>0`, `Rz>0`;
   - padded state has zero quadratic energy, zero active residual, positive inactive residual.

3. `strictKernelContact_gordanAlternative`
   - exactly one of `exists z, Az=0 and z>0 and Rz>0`, or
   - `exists u>=0,v>=0,h, (u,v)!=0 and Ah=u+R^Tv`.

4. `rationalStrictKernelContactCertificate`
   - for rational data, normalize the primal to `z>=1,Rz>=1`, or the dual to `sum u+sum v=1`.

The main practical recommendation is therefore:

> **corank-one:** use T-P5-173 minors;
>
> **higher-corank:** use T-P5-174 exact linear primal/dual packets;
>
> **never infer “no contact” merely because `adj(A)=0`.**
