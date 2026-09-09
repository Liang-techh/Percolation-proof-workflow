---
kind: review_result
review_id: review-T-P5-186-singular-psd-recession-active-fan-liuguanyi-20260909T2110Z
task_id: T-P5-186-SINGULAR-PSD-RECESSION-ACTIVE-FAN
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T21:10:00Z
claim_commit: dd24661825a9bf0d36f761dfa148286c42726055
inspected_commit: c3555ec03b269f226da4a18918c64d3f57ce9ebc
upstream_commits:
  - 2cef444f49ae94b85815734cf4376812b76f824a  # T-P5-185 piecewise active-face orthant Schur fan
  - aa8d1c1c47b9c5fedf6f5bb86691b6b6f89b7646  # T-P5-183 complementary orthant Schur transport
  - 038a8508822dd9f0603d2b8374191c91430d3686  # T-P5-182 orthant-feasible PSD-block Schur descent
  - a851e8ba5abd1fbb8578d668f9c00a14eeb2b879  # T-P5-184 PSD Z-matrix monotone range solve
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_singular_psd_recession_gate; add_farkas_residual_equivalence; extend_T185_active_fan_to_singular_psd_by_PD_principal_supports
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional convex quadratic/KKT algebra; exact rational symbolic regression
exit_code: 0 for hand-checked identities/regression; no Lean/kernel run
---

# T-P5-186 — singular PSD recession gate and automatic active-face fan

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-185 gives a complete finite active-face Schur fan when the inherited block `P` is positive definite, but explicitly leaves the automatic construction open when `P>=0` is singular. The concern is real: a singular kernel can carry one-sided recession directions, a face principal block can itself be singular, and a naive pseudoinverse face solve can either miss an unbounded direction or reject a bounded problem whose optimum lies on a smaller face.

This review closes that singular mathematical seam without using a pseudoinverse.

For

`H = [[P, B^T], [B, C]]`, `P=P^T>=0`,

with inherited coordinates `u>=0` and retained external coordinates `e>=0`, define the nonnegative kernel/recession cone

`N_+(P) := { d>=0 : P d = 0 }`.

The exact obstruction is:

> **negative kernel recession:** there exists `d in N_+(P)` with some component of `B d` strictly negative.

If this occurs, the full quadratic is unbounded below along a nonnegative ray and `H` is definitely non-copositive.

If it does not occur, then every external direction has an attained constrained minimum. Among its minimizers one may choose one with minimal support, and the principal block on that support is automatically **positive definite**. Therefore the singular problem never needs a singular active solve at the final minimizing support: the support shrinks until a PD principal block remains. Enumerating all PD principal supports gives a finite active-face fan that covers the whole external orthant.

Thus T-P5-185's `P>0` automatic fan extends to arbitrary `P>=0` after one exact recession gate.

A second key result identifies that recession gate with a Farkas-style version of the T-P5-183 residual packet. The condition

`B d >= 0` for all `d>=0` with `P d=0`

is equivalent to existence of an arbitrary-sign matrix `Y0` such that

`R0 := P Y0 + B^T >= 0` entrywise.

Here `Y0` is **not** a feasible minimizing transport and need not be nonnegative. It is a dual recession certificate only. This distinction is important for the typed interface.

No physical source equality, cell/support identity, path/domain coverage, Float64/controller semantics, Lean/kernel verification, independent validation, P8/M4 closure, admission, or registry mutation is claimed.

---

## 1. Setup

Let

- `P=P^T in R^{m x m}` with `P>=0` in the ordinary PSD sense;
- `B in R^{p x m}`;
- `C=C^T in R^{p x p}`.

For `u in R_+^m`, `e in R_+^p`, write

`q_H(u,e) = u^T P u + 2 e^T B u + e^T C e`.

For fixed `e`, define

`b(e) := B^T e`

and the inherited minimization problem

`phi(e) := inf_{u>=0} [u^T P u + 2 b(e)^T u]`.

The full copositivity question is equivalent to

`phi(e) + e^T C e >= 0` for all `e>=0`,

provided `phi(e)` is finite. The first task is therefore to characterize exactly when singular `P` creates `phi(e)=-infinity`.

---

## 2. T186-A — exact kernel recession obstruction

### Theorem `negativeKernelRecession_gives_nonCopositive`

Let `d>=0` satisfy

`P d = 0`.

Let `e>=0` satisfy

`e^T B d < 0`.

Then

`q_H(t d,e) -> -infinity` as `t -> +infinity`.

Hence `H` is not copositive.

### Proof

Because `P d=0`,

`d^T P d=0`.

Therefore

`q_H(t d,e)`

`= t^2 d^T P d + 2 t e^T B d + e^T C e`

`= 2 t e^T B d + e^T C e`.

The coefficient of `t` is strictly negative, so the expression tends to `-infinity`. QED.

### Coordinate witness

If `B d` has a negative component `(B d)_k<0`, choose `e` to be the `k`-th nonnegative coordinate vector. Then

`q_H(t d,e_k)=2t(Bd)_k+C_kk`.

For rational source data and rational `d`, any rational `t` satisfying

`2t (-(Bd)_k) > C_kk`

when `C_kk>=0` gives an exact finite negative witness. If `C_kk<0`, `t=0` already fails.

This is a genuine mathematical FAIL, not merely inability to construct an adapter.

---

## 3. T186-B — the global recession gate

Define

**(RC)** `B d >= 0` entrywise for every `d>=0` with `P d=0`.

Then T186-A gives immediately:

### Necessary condition for copositivity

If `H` is copositive, `(RC)` must hold.

The point of the next sections is that `(RC)` is also exactly what is needed to make the singular active-face construction finite and complete.

---

## 4. T186-C — Farkas/residual equivalence

The infinite-looking condition `(RC)` has an exact finite-dimensional dual form.

### Theorem `recessionGate_iff_nonnegativeResidualTransport`

For symmetric `P`, the following are equivalent:

1. `B d >=0` for every `d>=0` satisfying `P d=0`;
2. for every external basis vector `e_k`, the column `B^T e_k` lies in
   `range(P) + R_+^m`;
3. there exist matrices `Y0 in R^{m x p}` and `R0 in R^{m x p}` such that

   `R0 = P Y0 + B^T`,

   `R0 >= 0` entrywise.

### Proof

Let

`K := ker(P) intersect R_+^m`.

For any column `q in R^m`,

`q^T d >=0` for all `d in K`

means exactly `q in K^*`, the dual cone. Since `K` is the intersection of the subspace `ker(P)` and the nonnegative orthant,

`K^* = (ker P)^perp + R_+^m`.

Because `P` is symmetric,

`(ker P)^perp = range(P)`.

Thus

`K^* = range(P) + R_+^m`.

Apply this columnwise to `q_k=B^T e_k`. Therefore `(RC)` holds iff for every `k` there are `x_k` and `r_k>=0` with

`B^T e_k = P x_k + r_k`.

Set the `k`-th column of `Y0` to `-x_k` and of `R0` to `r_k`. Then

`R0 = P Y0 + B^T >=0`.

The converse follows by multiplying by any `d>=0` with `Pd=0`:

`d^T B^T e = d^T R0 e >=0`

for every `e>=0`, hence `Bd>=0`. QED.

### Important typed distinction from T-P5-183

T-P5-183 uses a transport `Y` as a proposed minimizing map and obtains exactness only when feasibility/complementarity also hold.

Here `Y0` has a different type:

`recession_dual_transport`.

It may have arbitrary signs. Only

`R0 = P Y0 + B^T >=0`

is consumed. Its role is solely to prove that no nonnegative kernel direction carries negative linear work.

Do **not** infer `u=Y0 e` is feasible or minimizing.

---

## 5. T186-D — boundedness and attainment under `(RC)`

Fix `e>=0`. By T186-C there exist `x` and `r>=0` such that

`b(e)=P x+r`.

Then for every `u>=0`,

`u^T P u + 2 b(e)^T u`

`= (u+x)^T P (u+x) - x^T P x + 2 r^T u`

`>= -x^T P x`.

So the inherited convex quadratic is bounded below.

To pass from boundedness to an actual minimizer, use the finite-dimensional Frank-Wolfe/polyhedral quadratic lemma:

> A quadratic function bounded below on a nonempty polyhedron attains its infimum.

Here the polyhedron is the orthant `R_+^m` and the Hessian is `2P>=0`.

For this special PSD case an elementary proof can be obtained by taking a minimizing sequence, extracting any unbounded recession direction, observing that bounded objective forces that direction into `ker(P)` with zero linear work, and translating along it until a lower-dimensional face is reached; finite face descent terminates at a bounded minimizing sequence. No compactness or coercivity of the full singular coordinates is assumed.

Hence:

### Theorem `recessionGate_gives_attainedOrthantMinimum`

Under `(RC)`, for every `e>=0` there exists `u_*(e)>=0` attaining `phi(e)`.

This theorem is the missing existence step behind the singular fan.

---

## 6. T186-E — minimal-support minimizer has a PD principal block

Fix `e>=0` and choose, among all minimizers of the inherited problem, one with minimal support. Let

`S := supp(u_*) = {i : (u_*)_i>0}`.

### Theorem `minimalSupportMinimizer_principalPD`

`P_SS` is positive definite.

### Proof

`P_SS` is PSD because it is a principal submatrix of a PSD matrix.

Assume it is singular. Then there is a nonzero vector `n_S` with

`P_SS n_S=0`.

Extend `n_S` by zero outside `S`, obtaining `n in R^m`.

Because

`n^T P n = n_S^T P_SS n_S = 0`

and `P>=0`, zero quadratic energy implies

`P n=0`.

Since every coordinate of `(u_*)_S` is strictly positive, for sufficiently small positive and negative `t`, both

`u_* + t n`

remain nonnegative.

Along this line,

`q_inherited(u_*+tn)`

`= q_inherited(u_*) + 2t b(e)^T n`,

because `Pn=0`.

Both signs of small `t` are feasible and `u_*` is minimizing, hence necessarily

`b(e)^T n=0`.

Therefore the inherited objective is actually constant along the whole feasible segment in direction `n`.

Choose `t` at one endpoint of the maximal interval around zero for which `u_*+tn>=0`. At least one positive support coordinate becomes zero, while no coordinate becomes negative. The resulting point is another minimizer with strictly smaller support, contradicting minimality of `S`.

Hence `P_SS` cannot be singular. Since it is PSD, it is positive definite. QED.

### Consequence

Singularity of the full inherited block does **not** force a pseudoinverse solve at the true minimizing active support. The support automatically descends until its principal quadratic is nondegenerate.

This is the key bridge from the singular problem back into T-P5-185's exact PD face algebra.

---

## 7. T186-F — KKT cone for each PD principal support

Let `S` be any subset for which `P_SS>0`. Let `J=S^c`.

Define the exact face transport `Y^S` by

`Y^S_J = 0`,

and solve

**(7.1)** `P_SS Y^S_S = -B_S^T`.

Because `P_SS>0`, this solve is unique; the checker need not form an inverse.

Define

`R^S := P Y^S + B^T`.

Then automatically

`R^S_S=0`.

Define the polyhedral external cone

**(7.2)**

`C_S := { e>=0 : Y^S_S e >=0, R^S_J e >=0 }`.

For `e in C_S`,

- `Y^S e>=0`;
- `R^S e>=0`;
- support separation gives `(Y^S e)^T(R^S e)=0`.

Therefore T-P5-185/T-P5-183 applies exactly, and

**(7.3)**

`min_{u>=0} q_H(u,e) = e^T K_S e`,

where

**(7.4)**

`K_S := C - (Y^S_S)^T P_SS Y^S_S`.

The same formula can be written using the exact solve identity as

`K_S = C + B_S Y^S_S`,

and symmetry follows from `P_SS Y^S_S=-B_S^T`.

### Empty support

Include `S=empty` as a special face:

`Y^empty=0`, `K_empty=C`,

`C_empty={e>=0:B^T e>=0}`.

This is the region where `u=0` satisfies the inherited KKT inequalities.

---

## 8. T186-G — singular PSD automatic finite fan cover

### Main cover theorem `singularPSD_activeFaceFan_cover`

Assume `(RC)`.

Then

`R_+^p = union_{S: P_SS>0 or S=empty} C_S`.

### Proof

Fix arbitrary `e>=0`.

By T186-D, an inherited minimizer exists. Choose a minimizer `u_*` with minimal support `S`.

By T186-E, `P_SS>0` unless `S` is empty.

Because `(u_*)_S` lies in the relative interior of its support face, first-order optimality in each active coordinate gives

`P_SS (u_*)_S + B_S^T e =0`.

Thus, by uniqueness of the PD solve,

`(u_*)_S = Y^S_S e >=0`.

For each inactive coordinate `j in J`, increasing `u_j` from zero by a small positive amount cannot lower the objective, so

`(P_JS (u_*)_S + B_J^T e)_j >=0`.

Equivalently,

`R^S_J e>=0`.

Therefore `e in C_S`.

Since `e>=0` was arbitrary, the union of these finitely many cones covers the external orthant. QED.

### Why this is stronger than the T-P5-185 boundary

T-P5-185-F required `P>0` and enumerated inherited faces whose restricted quadratic was automatically PD.

T186 proves that when `P>=0` is singular, one should not enumerate singular face solves. Instead:

1. first rule out negative kernel recession;
2. enumerate only principal supports with `P_SS>0`;
3. the minimal-support argument guarantees these PD supports still cover every external direction.

No singular inverse, pseudoinverse, or canonical kernel gauge appears in the final face packet.

---

## 9. T186-H — complete singular-PSD copositivity decomposition

Combining T186-A, T186-G, and the regional exact value theorem gives:

### Theorem `copositive_iff_recessionGate_and_PDsupportFan`

Let `P=P^T>=0`. Then `H` is copositive if and only if both conditions hold:

1. **recession gate**:

   `B d>=0` for every `d>=0` with `P d=0`;

2. **regional reduced nonnegativity**:

   for every subset `S` with `P_SS>0` (and the empty support),

   `e^T K_S e >=0` for every `e in C_S`.

### Proof

**Necessity of 1.** T186-A.

**Necessity of 2.** For `e in C_S`, `u=Y^S e>=0` attains the inherited minimum and

`q_H(Y^S e,e)=e^T K_S e`.

Copositivity of `H` forces this to be nonnegative.

**Sufficiency.** By 1 and T186-G, every `e>=0` lies in some `C_S`. On that cone T186-F computes the exact inherited minimum, and condition 2 makes the minimum nonnegative after the `C` term. Therefore `q_H(u,e)>=0` for every `u,e>=0`. QED.

This is an exact decision decomposition at the finite-dimensional mathematical level.

---

## 10. Checker-facing recession packet

There are two exact routes.

### Route A — positive residual dual certificate

Producer supplies one arbitrary-sign rational matrix `Y0` and defines

`R0=P Y0+B^T`.

Checker verifies only

- exact matrix equality;
- `R0>=0` entrywise.

Then `(RC)` follows.

For rational `P,B`, if `(RC)` is true, a rational packet of this form exists because the dual feasibility system is rational polyhedral.

This route is usually cheaper than enumerating kernel rays.

### Route B — explicit negative recession FAIL witness

Producer supplies

- `d>=0` rational;
- `P d=0` exactly;
- an index `k` with `(B d)_k<0`.

Checker then has a sound non-copositivity witness; it may additionally construct a rational `t` with

`2t(Bd)_k+C_kk<0`.

### Do not conflate the routes

Failure to find Route-A `Y0` is not itself a FAIL unless accompanied by a valid Farkas/negative-recession witness. Conversely, a Route-A `Y0` is not a minimizing transport and does not replace the regional `Y^S` packets.

---

## 11. Exact rational regression — rank-one singular block, no range inclusion, no global linear minimizer transport

Take

`P = [[1,1],[1,1]]`,

`B = [[1,-1],[-1,1]]`,

`C = I_2`.

Then `P>=0` and `rank(P)=1`.

### 11.1 Recession gate

`P d=0` means

`d_1+d_2=0`.

With `d>=0`, this forces `d=0`.

Hence `N_+(P)={0}` and `(RC)` is automatic.

However

`range(P)=span{(1,1)^T}`,

while the first external coupling column is

`B^T e_1=(1,-1)^T`,

so

`range(B^T) subseteq range(P)` is false.

Therefore ordinary singular Schur range compatibility is strictly stronger than the true one-sided recession condition.

### 11.2 Exact minimizer

For `e=(e_1,e_2)>=0`, put

`a=e_1-e_2`.

The inherited part is

`(u_1+u_2)^2 + 2 a (u_1-u_2)`.

If `a>=0`, its unique minimum is attained at

`u=(0,a)`.

If `a<=0`, its unique minimum is attained at

`u=(-a,0)`.

The minimum inherited value is

`-a^2`.

Adding `e^T C e=e_1^2+e_2^2` gives

`min_{u>=0} q_H(u,e)`

`= e_1^2+e_2^2-(e_1-e_2)^2`

`= 2 e_1 e_2 >=0`.

Thus the full `4x4` matrix

`[[1,1, 1,-1],`

` [1,1,-1, 1],`

` [1,-1,1,0],`

` [-1,1,0,1]]`

is copositive.

### 11.3 Two PD principal-support cones

For `S={2}`,

`P_SS=[1]`,

`Y^S_S=[1,-1]`,

so

`u_2=e_1-e_2`.

The inactive residual is

`R_1 e = 2(e_1-e_2)`.

Hence

`C_{2}={e>=0:e_1>=e_2}`.

The reduced matrix is

`K_2 = [[0,1],[1,0]]`.

For `S={1}` symmetrically,

`C_{1}={e>=0:e_2>=e_1}`

and

`K_1=[[0,1],[1,0]]`.

These two cones cover the entire external orthant, and on either cone

`e^T K_S e = 2e_1e_2`.

The singular full support `{1,2}` is never needed.

### 11.4 Why no single global T-P5-183 complementary linear transport exists

At `e=(1,0)`, the unique minimizer is `(0,1)`.

At `e=(0,1)`, the unique minimizer is `(1,0)`.

Any single linear transport `Y` that attained both minima would therefore satisfy

`Y(1,0)=(0,1)`,

`Y(0,1)=(1,0)`.

Linearity forces

`Y(1,1)=(1,1)`.

But at `e=(1,1)`, the unique minimizer is `u=0` because the inherited objective is simply `(u_1+u_2)^2`.

Contradiction.

So this example lies strictly beyond the single-global-transport branch of T-P5-183 and beyond the `P>0` automatic branch of T-P5-185, while T186 closes it exactly with two PD principal-support cones.

---

## 12. Boundary A — range inclusion is not the correct singular one-sided gate

Do not require

`range(B^T) subseteq range(P)`

as a necessary condition for the one-sided problem.

The regression above violates it but is perfectly bounded and copositive. Range inclusion is the correct gate only when the active variables are signed/free, as in T-P5-178's mixed Schur setting, or when one insists on a zero-residual global exact solve.

For one-sided inherited coordinates the exact global obstruction is only the nonnegative kernel cone `N_+(P)`.

---

## 13. Boundary B — no-negative-recession does not itself prove copositivity

`(RC)` proves only that every external inherited minimization is finite and attained.

The regional reduced matrices `K_S` can still be negative on their cones. Each surviving cone therefore needs its own cone-restricted quadratic certificate, exactly as in T-P5-185.

Do not promote a recession PASS into a full matrix PASS.

---

## 14. Boundary C — PD support enumeration may be combinatorial but is finite

The theorem is structural, not a claim of polynomial-time complexity.

In the worst case there are many subsets `S` with `P_SS>0`. Practical dispatch may prune cones by exact infeasibility tests or exploit negative-edge/component structure from T-P5-165/T-P5-167, but pruning must preserve cover.

The mathematical gain is that no singular face solve is ever required at a minimal-support optimum.

---

## 15. Boundary D — physical coverage remains separate

The cover

`R_+^p = union_S C_S`

is a mathematical cover of the retained external orthant for one fixed exact block `(P,B,C)`.

It does not prove that the repository's physical trajectory, cell family, uncertainty family, controller runtime, or FD/DH evaluator is represented by that exact block. Same-key source binding and physical domain/path coverage remain external obligations.

---

## 16. Suggested formal theorem interface

Minimal theorem leaves:

1. `psd_zero_energy_mulVec_zero`
   - `P>=0`, `x^T P x=0 -> P x=0`.

2. `negativeKernelRecession_nonCopositive`
   - exact ray witness.

3. `recessionDual_iff_exists_nonnegativeResidual`
   - Farkas dual of `ker(P) intersect orthant`.

4. `orthantQuadratic_attains_of_noNegativeRecession`
   - finite-dimensional bounded-below convex quadratic on orthant attains its minimum.

5. `minimalSupportMinimizer_principal_posDef`
   - minimal support removes all singular principal directions.

6. `pdPrincipalFace_transport`
   - exact solve `P_SS Y=-B_S^T`, inactive residual cone, completion identity.

7. `singularPSD_pdPrincipalFan_cover`
   - under recession gate, PD principal support cones cover the external orthant.

8. `copositive_iff_recession_and_pdPrincipalFan`
   - final exact decomposition.

The Farkas theorem may be formalized later using a finite-dimensional polyhedral duality library. The purely algebraic leaves 1, 2, 5, and 6 are independent and should be easier to pin first.

---

## 17. Recommended routing

For a one-sided inherited PSD block after T-P5-179/T-P5-182:

1. if `P` is a PSD Z-matrix and the T-P5-184 sign corridor applies, use that cheapest route;
2. otherwise try one global T-P5-183 complementary transport;
3. if that fails and `P>0`, T-P5-185's PD active-face fan applies;
4. if `P>=0` is singular, run the T186 recession gate:
   - negative kernel recession -> exact FAIL;
   - no negative recession -> enumerate only PD principal supports and use the T186/T185 regional cones;
5. on each surviving cone, reduce the regional quadratic to the existing cone/copositivity dispatcher;
6. only after all cones pass may the mathematical block be called closed.

This routing prevents two opposite errors:

- falsely declaring failure because a singular range solve does not exist;
- falsely ignoring a genuine nonnegative-kernel ray that makes the energy unbounded below.

---

## 18. Remaining obligations

Still open:

1. actual same-key production of `P,B,C` on the physical P5 path;
2. exact classification of the actual inherited block and its nonnegative kernel cone;
3. an actual recession dual packet `R0=P Y0+B^T>=0` or a negative-recession witness;
4. exact construction/pruning of surviving PD principal-support cones;
5. cone-restricted copositivity certificates for every surviving `K_S`;
6. source identity, cell/path/domain coverage, Float64/controller/FD semantics, P8/M4;
7. Lean/kernel compilation and theorem/axiom receipt;
8. independent validation by 封不觉;
9. admission/registry integration.

The mathematical child remains

**`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`.**
