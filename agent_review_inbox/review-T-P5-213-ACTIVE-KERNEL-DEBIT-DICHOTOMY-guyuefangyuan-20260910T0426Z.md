---
kind: review_result
review_id: review-T-P5-213-active-kernel-debit-dichotomy-guyuefangyuan-20260910T0426Z
task_id: T-P5-213-ACTIVE-KERNEL-DEBIT-DICHOTOMY
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T04:26:00Z
claim_commit: e4804bf7263ababec402eb2bcb21a42139a39ce6
inspected_commit: 7fcad4d53fbddf6307e972b556f1c502c45fea0b
upstream_commits:
  - 2f952c3ff2704671a74123e51d58e80f4b53b223  # T-P5-212 high-corank reduced-kernel bridge
  - 8cba2b2fa9bb7fc26803b26833df2c44e6cdc0b3  # T-P5-210 common-zero second-order threshold
  - 953eb401979eeb1374e4e4c722a5c29588e6a498  # T-P5-178 critical mixed-block Schur bridge
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_active_kernel_debit_gate; add_flat_cross_vanishing; add_gauge_invariant_reduced_pullback; route_T212_boundaryA; add_exact_regressions
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional quadratic algebra; exact rational regressions; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-213 — active-kernel debit dichotomy

## 0. Verdict and seam closed

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-212 closes arbitrary high corank in the *reduced* PSD Schur block `K`, but deliberately keeps the active signed block `A` corank one. Its Boundary A therefore routes a higher-corank active kernel back to the older T-P5-178/T-P5-186 range/kernel machinery.

The present child does not duplicate that endpoint-Schur theorem. Instead it closes the next, narrower question needed by T-P5-210:

> once T-P5-178 has already described the endpoint zero sheet for an arbitrary-dimensional active kernel, can the higher active corank itself create a positive debit direction, and if not, does the problem reduce exactly to T-P5-212?

The answer is an exact dichotomy.

Let `N` be a complete basis of `ker(A)`. Pull the T-P5-210 debit form `Q` onto the active kernel and define

`E := N^T P N`,

where `P` is the active-active block of `Q`.

Under the T-P5-210 common-zero assumptions, `P` is PSD. Therefore:

1. if `E != 0`, a **pure active-kernel direction** is already an exact positive-debit zero-energy tangent, so T-P5-210 gives the sharp endpoint immediately;
2. if `E = 0`, then `P N=0`; moreover all active-kernel/reduced-kernel cross debit vanishes on the zero-loaded cone, and the problem collapses exactly to the T-P5-212 matrix `M0`;
3. hence, under a complete zero-loaded reduced-kernel generator packet, a positive T-P5-210 second-order witness exists iff

   **`E != 0 OR M0 != 0`.**

There is no third genuinely coupled `alpha-y` branch under the copositive common-zero hypotheses.

No actual P5 source, selector/cell/tube coverage, Float64/runtime semantics, Lean/kernel receipt, independent verification, admission, registry mutation, or parent closure is claimed.

---

## 1. Endpoint zero sheet from the existing Schur machinery

Consider the endpoint critical block

`H = [[A, R^T], [R, C]]`,

with signed active variable `u in R^m` and one-sided inactive critical variable

`eta in R_+^p`.

Assume the endpoint hypotheses already handled by T-P5-178:

1. `A=A^T >=0`;
2. there is a strict-positive active contact `z>0` with `Az=0`;
3. every critical row annihilates the full active kernel,

   `R n=0  for every n in ker(A)`;

4. equivalently, `range(R^T) subset range(A)`;
5. choose an exact range solve

   `A X = R^T`;

6. define the reduced Schur block

   `K := C-RX`;

7. on the present branch, assume `K=K^T>=0`.

Let `N` be an `m x r` full-column-rank matrix whose columns form a complete basis of `ker(A)`.

The standard completed-square identity is

`(u,eta)^T H (u,eta)`

`= (u+X eta)^T A (u+X eta) + eta^T K eta`.

Because both terms are PSD, the full zero-energy sheet is exactly

**`u = N alpha-X eta`, `alpha in R^r`, `eta in ker(K) cap R_+^p`.**

This is the only endpoint geometry used below; the proof of range compatibility itself remains T-P5-178's responsibility.

---

## 2. The common-zero debit makes the active block PSD

Partition the T-P5-210 debit matrix as

`Q = [[P,T^T],[T,U]]`,

and take the reference common-zero state

`x_*=(z,0)`.

Assume the actual T-P5-210 hypotheses:

- `Q` is copositive;
- `x_*>=0`;
- `x_*^T Q x_*=0`.

The standard orthant zero-contact argument gives

`Pz=0`,

`g:=Tz>=0`.

For this child one needs a slightly stronger active conclusion.

### Lemma T213-A — active debit PSD

**`P>=0` on all of `R^m`.**

### Proof

Fix arbitrary `d in R^m`. Because `z>0` coordinatewise, for sufficiently small positive `eps`, both

`z+eps d >=0`,

`z-eps d >=0`.

Copositivity of `Q` therefore gives

`(z +/- eps d,0)^T Q (z +/- eps d,0) >=0`.

Since `z^T Pz=0` and the two-sided first derivative vanishes, `Pz=0`; consequently

`(z+eps d)^T P(z+eps d)=eps^2 d^T P d`.

Hence `d^T P d>=0` for every signed `d`, so `P` is PSD. QED.

This is stronger than ordinary copositivity because the strict-positive active contact exposes both signs of every active tangent.

---

## 3. The bi-critical first-order condition ignores the active-kernel coordinate

For a zero-`H` tangent

`v(alpha,eta)=(N alpha-X eta, eta)`,

the T-P5-210 debit first-order term is

`(Qx_*)^T v`

`= (Pz)^T(N alpha-X eta)+(Tz)^T eta`

`= g^T eta`.

Therefore the bi-critical equality is exactly

**`g^T eta=0`,**

independent of the signed active-kernel coordinate `alpha`.

Now apply the T-P5-212 reduced-kernel geometry. Let columns of `V` be a complete finite generator family of

`ker(K) cap R_+^p`.

Define generator loads

`b:=V^T g>=0`.

Discard every generator with `b_j>0`, and let `V0` contain exactly the zero-loaded generators. Then the bi-critical reduced directions are precisely

**`eta=V0 y`, `y>=0`,**

provided the generator packet is complete.

This is the same zero-loaded filtering as T-P5-212. The only genuinely new issue is the arbitrary active-kernel coordinate `alpha`.

---

## 4. Exact debit pullback on the full high-corank zero sheet

Define

`E := N^T P N`,

`B := N^T (T^T-PX) V0`,

`G := U + X^T P X - T X - X^T T^T`,

`M0 := V0^T G V0`.

For

`eta=V0 y`,

`v=L(alpha,y):=(N alpha-XV0 y,V0 y)`,

a direct expansion gives the exact identity

**`v^T Q v = alpha^T E alpha + 2 alpha^T B y + y^T M0 y`.**

Because every such `v` is a T-P5-210 bi-critical tangent, the same small-`eps` argument used in T-P5-210 shows

**`alpha^T E alpha + 2 alpha^T B y + y^T M0 y >=0`**

for every `alpha in R^r` and every `y>=0`.

Thus the debit pullback is nonnegative on the mixed cone

`R^r x R_+^s`.

Also, because `P>=0`,

**`E=N^TPN>=0`.**

---

## 5. T213-B — nonzero active-kernel debit closes the threshold immediately

Assume

`E != 0`.

Since `E>=0`, at least one diagonal entry is strictly positive:

`E_ii>0` for some `i`.

Take

`alpha=e_i`, `y=0`.

Then

`v=(N e_i,0)`

lies entirely in the active kernel. It satisfies

`v^T H v=0`,

and the T-P5-210 first-order conditions automatically vanish because `eta=0`.

Its debit energy is

`v^T Qv=e_i^T E e_i=E_ii>0`.

Therefore it is an exact T-P5-210 second-order endpoint witness.

### Consequence

If `E!=0`, one does **not** need to enumerate the reduced `K`-kernel rays merely to decide witness existence. Higher active corank itself has already exposed the sharp endpoint.

For exact-rational data the trusted packet can be especially small: provide one exact kernel vector `n_i` and the rational scalar

`n_i^T P n_i>0`.

No eigenvector, pseudoinverse, square root, or floating nullspace tolerance is required.

---

## 6. T213-C — zero active-kernel debit forces `PN=0`

Now assume

`E=0`.

Because `P>=0`, each column `n_i` of `N` satisfies

`n_i^T P n_i=0`.

For a PSD matrix, zero quadratic energy implies kernel membership. Hence

`P n_i=0`

for every basis column. Therefore

**`PN=0`.**

Equivalently, `P` annihilates the **entire active kernel**, not merely the reference vector `z`.

This is exactly the structural fact absent from T-P5-212's corank-one setup because there the active kernel has only the already-known direction `z`.

---

## 7. T213-D — the mixed active/reduced debit cross term then vanishes

Under `E=0`, the exact mixed-cone nonnegativity becomes

`2 alpha^T B y + y^T M0 y >=0`

for every signed `alpha` and every `y>=0`.

Fix arbitrary `y>=0`. If `By !=0`, choose some `alpha` with `alpha^TBy !=0`; changing the sign of `alpha` and scaling its magnitude would send the linear term to `-infinity` while the `y^TM0y` term remains fixed, contradicting nonnegativity.

Therefore

`By=0  for every y>=0`.

Taking coordinate vectors `y=e_j` yields

**`B=0`.**

Thus when the active-kernel debit is flat, copositivity/common-zero semantics automatically eliminate all coupling between the signed active kernel and the zero-loaded reduced-kernel cone.

Since `PN=0`, the equality `B=0` can also be written as the useful orthogonality

**`N^T T^T V0=0`.**

So every zero-loaded reduced-kernel generator is debit-orthogonal to the entire active kernel.

---

## 8. T213-E — exact collapse back to T-P5-212

With `E=0` and hence `B=0`, the debit energy on every bi-critical zero-`H` tangent is simply

**`v^T Qv = y^T M0 y`.**

The signed active-kernel coordinate `alpha` disappears completely.

Furthermore the mixed-cone nonnegativity immediately implies

`y^T M0 y>=0  for all y>=0`,

so `M0` is copositive.

T-P5-212 already proves that for a symmetric copositive matrix

`exists y>=0, y^T M0 y>0`

iff

`M0 !=0`.

Therefore the higher-active-corank branch has the exact decision rule

### Main theorem T213-F

Under the T-P5-178 endpoint range/Schur hypotheses, the T-P5-210 copositive common-zero debit hypotheses, `K>=0`, a complete basis `N` of `ker(A)`, and a complete zero-loaded generator packet `V0` for `ker(K) cap R_+^p`, there exists a T-P5-210 bi-critical tangent satisfying

`v^T H v=0<v^T Qv`

**iff**

**`E !=0 OR M0 !=0`.**

Proof:

- `E!=0` gives the pure-active witness of Section 5;
- if `E=0`, Sections 6–8 reduce all debit energy to `y^TM0y`, and T-P5-212 gives a positive witness iff `M0!=0`;
- if both are zero, every bi-critical zero-`H` tangent has zero debit energy, so no T-P5-210 second-order witness exists on this contact sheet.

This is the central new compression:

**arbitrary active corank + arbitrary reduced PSD corank -> active PSD gate first, then exactly the old T-P5-212 reduced orthant gate.**

---

## 9. Gauge invariance at the flat active-kernel branch

The range solve `X` is not unique. If

`X' = X + N Gamma`,

then `AX'=R^T` still holds.

The coordinate `alpha` on the zero sheet changes correspondingly, so the full pulled quadratic transforms by a triangular change of variables. In general its individual `B/M0` blocks need not look identical.

However, once the exact active-flat gate `E=0` holds, we have `PN=0` and `B=0`. The reduced debit value on the physical zero sheet is then independent of the active-kernel gauge, and the restricted `M0` on the zero-loaded cone is unchanged.

Hence an implementation should use the following order:

1. test the active-kernel debit `E` first;
2. only if `E=0`, form/use the T-P5-212 reduced matrix `M0`;
3. at that point the reduced packet is canonical with respect to the Schur kernel gauge.

This avoids attaching meaning to a gauge-dependent intermediate cross block when the pure-active witness has already decided the branch.

---

## 10. Exact rational regression A — T-P5-212 alone misses a pure-active witness

Take two active coordinates and one inactive coordinate:

`A=[[0,0],[0,0]]`,

`R=[[0,0]]`,

`C=[1]`.

Then

`H=diag(0,0,1)`,

and choose the strict-positive contact

`z=(1,1)`.

The reduced Schur block is

`K=[1]`,

so

`ker(K) cap R_+={0}`.

There are no nonzero reduced-kernel rays at all; a T-P5-212-only search therefore has no candidate.

Now take the copositive, in fact PSD, debit

`P=[[1,-1],[-1,1]]`,

`T=0`, `U=0`.

The common-zero state is

`x_*=(1,1,0)`,

because `Pz=0`.

Take `N=I_2`, a complete basis of `ker(A)`. Then

`E=N^TPN=P !=0`.

The pure-active tangent

`v=(1,0,0)`

satisfies

`v^T H v=0`,

`v^T Qv=1>0`.

So T-P5-210 gives the exact threshold witness even though the reduced-kernel cone is trivial.

This proves that T-P5-212 Boundary A cannot be handled by simply ignoring the extra active-kernel directions and enumerating `K`-kernel rays.

---

## 11. Exact rational regression B — why Q copositivity is essential for cross-term collapse

Take

`A=0_2`, `K=0_1`, `z=(1,1)`,

`P=0`,

`T=[1,-1]`,

`U=0`.

Then

`g=Tz=0`,

so the inactive kernel ray is zero-loaded, and

`E=N^TPN=0`.

But with `N=I_2`,

`B=N^T T^T = (1,-1)^T !=0`.

The corresponding quadratic has

`Q(u1,u2,eta)=2 eta(u1-u2)`,

which is not copositive on the full orthant.

Thus the algebraic condition `E=0` alone does **not** imply `B=0`. The decisive input is the mixed nonnegativity inherited from the actual T-P5-210 assumption that `Q` is copositive at a common zero.

A checker must not apply the flat-cross-term theorem to an arbitrary signed debit matrix.

---

## 12. Exact rational regression C — flat active branch recovers the T-P5-212 cross-ray effect

Take an arbitrary flat active kernel, for example

`A=0_2`, `P=0`, `T=0`,

and let

`K=0_2`,

`U=[[0,1],[1,0]]`.

Then

`E=0`, `B=0`,

and the zero-loaded reduced generators are `e1,e2`. The reduced matrix is

`M0=[[0,1],[1,0]]`.

Each generator ray separately has zero debit energy, but

`(e1+e2)^T M0(e1+e2)=2>0`.

Thus after the active-flat reduction, one must still preserve T-P5-212's full cross-ray matrix rather than replace it by diagonal/raywise tests.

---

## 13. Exact-rational dispatcher

For an endpoint contact with a higher-corank active PSD block:

1. reuse T-P5-178 to certify the critical-row range condition and obtain one exact `AX=R^T`;
2. provide a **complete** exact basis `N` of `ker(A)`;
3. compute the active debit diagonal scalars

   `e_i=n_i^T P n_i`;

4. because `P>=0`, any `e_i>0` is an immediate pure-active T-P5-210 witness;
5. if every `e_i=0`, conclude `PN=0` and hence `E=0` exactly;
6. only now use T-P5-212 to enumerate a complete generator family of `ker(K) cap R_+^p` and apply the zero-load filter `g^Txi=0`;
7. form the full cross-ray matrix `M0`;
8. if `M0!=0`, obtain a positive reduced debit witness as in T-P5-212;
9. if `M0=0`, this contact sheet supplies no T-P5-210 second-order witness;
10. keep the global endpoint copositivity, source, coverage, runtime, and admission gates external.

For rational matrices this path uses only exact linear solves/kernel bases, matrix products, zero/sign comparisons, and the existing copositivity machinery. It requires no eigensystem, pseudoinverse, square root, determinant-root search, or generic nonlinear optimizer.

---

## 14. Minimal Lean theorem statements

Suggested formal leaves:

1. `copositive_commonZero_strictSupport_activeBlock_psd`
   - from copositive `Q` and strict-positive active common zero `(z,0)`, derive `P>=0`, `Pz=0`, `Tz>=0`.

2. `kernelPullback_psd`
   - `P>=0 -> N^T P N>=0`.

3. `activeKernelDebit_nonzero_gives_bicriticalWitness`
   - under the endpoint zero-sheet hypotheses, a positive diagonal of `N^TPN` gives a pure-active zero-`H`, positive-`Q` tangent.

4. `psd_basis_zeroQuadratic_imp_annihilates_span`
   - if `P>=0` and every basis column `n_i` has `n_i^TPn_i=0`, then `PN=0`.

5. `mixedNonneg_zeroSignedBlock_crossZero`
   - if `2 alpha^T B y+y^TMy>=0` for every signed `alpha` and every `y>=0`, then `B=0`.

6. `highCorankActive_flat_reduces_reducedKernel`
   - under `E=0`, the debit on the bi-critical zero sheet equals `y^TM0y`.

7. `highCorankActive_debitWitness_iff_activeOrReduced_nonzero`
   - with complete kernel/generator packets and T-P5-210 assumptions, witness existence iff `E!=0 or M0!=0`.

8. `flatActive_reducedPullback_gauge_invariant`
   - the flat-branch reduced debit is invariant under `X -> X+N Gamma`.

The first proof should be kept separate because it is the semantic reason `P` becomes PSD; merely assuming that its entries came from a copositive full matrix is not enough without the strict-positive common-zero contact.

---

## 15. Boundaries deliberately left open

### Boundary A — incomplete active-kernel basis

A list of valid kernel vectors is not enough. If `N` does not span all of `ker(A)`, all recorded `n_i^TPn_i` may vanish while an omitted kernel direction has positive debit. The basis-completeness theorem/receipt is a trusted premise.

### Boundary B — incomplete reduced-kernel generator list

The flat branch inherits T-P5-212's completeness requirement. Missing a zero-loaded extreme ray can falsely report `M0=0`.

### Boundary C — `K` not PSD

The zero-`H` sheet need not split as `ker(A)` times `ker(K) cap R_+^p`. Copositive-but-indefinite reduced blocks remain in the more general mixed critical-cone machinery; this child does not classify them.

### Boundary D — active contact not strict-positive on its declared support

If some declared active coordinate is actually zero, arbitrary signed active perturbations are not feasible. Canonically descend to the true positive support first, as in T-P5-179, before using the active-PSD lemma.

### Boundary E — Q not copositive/common-zero

Then `P` need not be PSD and `E=0` need not kill the cross block `B`; Regression B is an exact counterexample. Do not use the dichotomy outside the T-P5-210 semantic branch.

### Boundary F — actual P5 source and verification

No claim is made about same-key `A,R,C,P,T,U`, actual selector or tube, interval/Float64 semantics, path/trajectory coverage, Lean/kernel validation, 封不觉 verification, admission, registry, or parent closure.

---

## 16. Recommended handoff

The next producer-facing packet should not treat “active block has higher corank” as an undifferentiated fallback to a generic nullspace optimizer. It can first ask for a complete rational kernel basis `N` and compute only the active debit scalars `n_i^TPn_i`.

- Any positive scalar closes the local T-P5-210 sharpness witness immediately.
- If all are zero, exact PSD semantics force the whole active kernel into `ker(P)` and remove all active/reduced cross debit on the zero-loaded cone.
- Only that flat branch needs the T-P5-212 reduced-kernel extreme-ray packet.

This gives a strict dispatcher order and removes a potentially large mixed signed/orthant search without weakening the theorem.
