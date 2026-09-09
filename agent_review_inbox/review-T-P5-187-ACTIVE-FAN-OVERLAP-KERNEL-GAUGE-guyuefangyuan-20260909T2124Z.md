---
kind: review_result
review_id: review-T-P5-187-active-fan-overlap-kernel-gauge-guyuefangyuan-20260909T2124Z
task_id: T-P5-187-ACTIVE-FAN-OVERLAP-KERNEL-GAUGE
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-09T21:24:00Z
claim_commit: 0b168cf060a30285eb25ed7e94e037cfc1b92761
inspected_commit: e556c364d7fe77cd2d34042b4eb786bfe87aa57f
upstream_commits:
  - aa8d1c1c47b9c5fedf6f5bb86691b6b6f89b7646  # T-P5-183 complementary orthant Schur transport
  - 2cef444f49ae94b85815734cf4376812b76f824a  # T-P5-185 piecewise active-face orthant Schur fan
  - 4c6c4ab0ae84f7e397975e6de14e8167efcd6bfa  # T-P5-186 singular PSD recession active fan
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_kkt_solution_kernel_gauge; add_active_fan_overlap_seam_identity; use_residual_uniqueness_to_prune_face_packets
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional LCP/quadratic algebra; exact rational SymPy replay of the two-cone regression
exit_code: 0 for the exact symbolic regression; no Lean/kernel run
---

# T-P5-187 — active-fan overlap kernel gauge and canonical seam energy

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-185 replaces one global orthant transport by a finite active-face fan. T-P5-186 then shows how to construct such a fan when the inherited block `P>=0` is singular, after the recession gate. That leaves a natural stitching question:

> If two face packets are simultaneously valid on a cone boundary, can their minimizing transports, KKT residuals, or reduced Schur quadratics disagree?

The answer is exact and favorable.

For one fixed external direction, **all valid orthant KKT minimizers differ only by a vector in `ker(P)`**. More strongly, their KKT residual vector is identical. Consequently their reduced Schur energy is identical. Thus the singular case has only a kernel gauge freedom, not an energy ambiguity.

For two linear face transports valid on an overlap cone `Omega`, the difference satisfies

`P (Y_alpha-Y_beta) e = 0` for every `e in Omega`.

By linearity it therefore vanishes on `span(Omega)`. Hence the two reduced quadratic forms agree as bilinear forms on that span. If `V` is any generator/span matrix for the overlap,

**`V^T (K_alpha-K_beta) V = 0`.**

No extra continuity or seam-energy certificate is mathematically needed once both regional KKT packets are valid. However, this identity is a useful exact consistency check for a source/CSE producer. It is also important **not** to demand `K_alpha=K_beta` globally when the overlap is lower-dimensional; a rational two-cone example below shows that would reject a perfectly valid active fan.

No source identity, physical domain/path coverage, Float64/controller semantics, Lean/kernel verification, independent validation, admission, or registry mutation is claimed.

---

## 1. Setup

Let

`P=P^T >= 0`

be an `m x m` real PSD matrix. For a fixed external direction `e`, abbreviate

`b := B^T e`.

The inherited constrained quadratic is

`f(u) := u^T P u + 2 b^T u`, for `u>=0`.

A valid orthant KKT point is a pair `(y,r)` satisfying

`y>=0`,

`r := P y + b >=0`,

`y^T r = 0`.

This is exactly the pointwise transport condition used by T-P5-183/T-P5-185 after setting `y=Y e` and `r=R e`.

Take two such KKT points

`(y,r_y)` and `(z,r_z)`

for the **same** `P` and `b`.

Define

`d := z-y`.

---

## 2. Exact two-KKT-point identity

Expanding around `y`,

`f(z)-f(y)`

`= d^T P d + 2 d^T(P y+b)`

`= d^T P d + 2 d^T r_y`.

Because `y^T r_y=0`,

`d^T r_y = z^T r_y-y^T r_y = z^T r_y`.

Therefore

**(2.1)**

`f(z)-f(y) = d^T P d + 2 z^T r_y >= 0`,

since `P>=0`, `z>=0`, and `r_y>=0`.

Interchanging `y,z` gives

**(2.2)**

`f(y)-f(z) = d^T P d + 2 y^T r_z >= 0`.

The left sides are negatives of one another. Hence both are zero:

**(2.3)** `f(y)=f(z)`.

Returning to (2.1), a sum of two nonnegative terms is zero, so

**(2.4)** `d^T P d=0`,

**(2.5)** `z^T r_y=0`.

Similarly,

**(2.6)** `y^T r_z=0`.

For a symmetric PSD matrix,

`d^T P d=0  =>  P d=0`.

Thus

**(2.7)** `P(z-y)=0`.

This is the basic kernel-gauge theorem.

---

## 3. Residual uniqueness

Since

`r_z-r_y = P(z-y)`,

(2.7) immediately gives

**(3.1) `r_z=r_y`.**

So although a singular PSD block may admit many nonnegative minimizers, the KKT residual is canonical.

This yields a useful active-set invariant. Let

`J := { i : r_i > 0 }`,

`I := { i : r_i = 0 }`.

Because every minimizer `y>=0` satisfies `y_i r_i=0`, every coordinate in `J` is zero in **every** minimizer. All ambiguity between active faces can occur only inside the zero-residual critical set `I`.

This matches the T-P5-179 separation between first-order protected coordinates and zero-residual second-order critical coordinates, but now the separation is independent of which minimizing face representative is chosen.

---

## 4. Reduced Schur energy is canonical

Let the full block be

`H = [[P,B^T],[B,C]]`.

For a transport `Y`, T-P5-183/T-P5-185 use

`K_Y := C-Y^T P Y`.

At a fixed external direction `e`, put `y=Y e`. KKT complementarity implies

`y^T(P y+b)=0`,

so

`b^T y = - y^T P y`.

Hence the constrained inherited minimum is

`f(y)=y^T P y+2b^T y=-y^T P y`,

and the full minimum is

`e^T C e-y^T P y = e^T K_Y e`.

Now let `y,z` be two valid KKT minimizers. By (2.7), `z=y+d` with `P d=0`. Therefore

`z^T P z`

`= y^T P y + 2 y^T P d + d^T P d`

`= y^T P y`.

Thus

**(4.1)**

`e^T K_{Y_alpha} e = e^T K_{Y_beta} e`

whenever both face transports are valid at the same `e`.

There is therefore no seam jump in the exact reduced energy.

---

## 5. Cone-overlap theorem

Let `Omega` be any subset of the external orthant. Suppose two linear transports `Y_alpha,Y_beta` are both valid KKT transports for every `e in Omega`:

`Y_gamma e>=0`,

`R_gamma e>=0`,

`(Y_gamma e)^T(R_gamma e)=0`,

where

`R_gamma := P Y_gamma+B^T`,

for `gamma in {alpha,beta}`.

Define

`D := Y_alpha-Y_beta`.

Applying (2.7) pointwise gives

**(5.1)** `P D e=0` for every `e in Omega`.

Since `P D` is linear,

**(5.2)** `P D x=0` for every `x in span(Omega)`.

Likewise, because

`R_alpha-R_beta=P D`,

we obtain

**(5.3)** `R_alpha x=R_beta x` for every `x in span(Omega)`.

So even when the transport itself changes across the seam, the residual map is identical on the seam span.

---

## 6. Restricted reduced-matrix identity

Let

`L := span(Omega)`.

For `x,w in L`, (5.2) gives

`P D x=0`, `P D w=0`.

Write

`Y_alpha=Y_beta+D`.

Then

`x^T(K_alpha-K_beta)w`

`= - x^T[Y_alpha^T P Y_alpha-Y_beta^T P Y_beta]w`

`= -(Y_beta x)^T P(Dw)`

`  -(D x)^T P(Y_beta w)`

`  -(D x)^T P(D w)`

`= 0`.

Therefore the two reduced forms agree **bilinearly** on the entire overlap span:

**(6.1)**

`K_alpha|_L = K_beta|_L` as quadratic/bilinear forms.

Equivalently, if the columns of a matrix `V` span a subspace contained in `L`, then

**(6.2)**

`V^T (K_alpha-K_beta) V = 0`.

In particular, when `V_overlap` is the generator matrix of a finitely generated overlap cone, the exact seam checker can use

`P(Y_alpha-Y_beta)V_overlap = 0`

and then obtain the reduced-matrix pullback identity for free.

No interior-point or polynomial-identity argument is needed; linearity plus PSD kernel gauge is enough.

---

## 7. Positive-definite specialization

If `P>0`, then `ker(P)={0}`. Equation (2.7) strengthens to

**(7.1)** `y=z`.

Thus on every overlap,

**(7.2)** `(Y_alpha-Y_beta)e=0`.

For a generator matrix `V_overlap`,

**(7.3)** `(Y_alpha-Y_beta)V_overlap=0`.

So in the PD T-P5-185 fan, different declared active faces may both describe a boundary point, but they cannot produce different actual minimizing inherited states there.

For singular `P`, equality of `Y` is generally false and should **not** be required. Only the kernel-gauge relation is canonical.

---

## 8. Exact singular-gauge regression

Take

`P = [[1,-1],[-1,1]]`,

which is PSD with

`ker(P)=span{(1,1)}`.

Take one external scalar `e>=0`, `B=0`, and any scalar `C=c`. Consider

`Y_0 e = (0,0)`,

`Y_1 e = (e,e)`.

Both are nonnegative and satisfy

`P Y_0 e=0`,

`P Y_1 e=0`.

Hence both have the same residual `r=0` and satisfy complementarity for every `e>=0`, but

`Y_0 != Y_1`.

Their difference is exactly the kernel gauge

`(Y_1-Y_0)e=e(1,1) in ker(P)`.

Moreover

`Y_0^T P Y_0 = Y_1^T P Y_1 = 0`,

so both reduced quadratics are exactly `C`.

This shows why a singular active-fan seam must not impose equality of transports themselves.

---

## 9. Exact two-cone regression: global `K` equality is too strong

Take one inherited coordinate and two external coordinates:

`P=[1]`,

`B^T=[-1, 1]`,

`C=[[1,-1],[-1,1]]`.

Then

`q_H(u,e1,e2)`

`= u^2 + 2u(-e1+e2) + (e1-e2)^2`

`= (u-e1+e2)^2`.

So the full quadratic is nonnegative.

Split the external orthant into

`C_1={e>=0 : e1>=e2}`,

`C_2={e>=0 : e2>=e1}`.

On `C_1`, use

`Y_1=[1,-1]`.

Then

`Y_1 e=e1-e2>=0`,

`R_1=P Y_1+B^T=[0,0]`,

and

`K_1=C-Y_1^T P Y_1=0`.

On `C_2`, use

`Y_2=[0,0]`.

Then

`Y_2 e=0`,

`R_2=B^T=[-1,1]`,

`R_2 e=e2-e1>=0`,

and

`K_2=C`.

The overlap is the ray

`Omega={t(1,1):t>=0}`.

On that ray both transports produce the same minimizer `u=0`, the same residual `0`, and the same reduced energy `0`.

But globally

**`K_1 != K_2`.**

Indeed

`K_1=0`,

`K_2=[[1,-1],[-1,1]]`.

For the overlap generator

`v=(1,1)^T`,

we have exactly

`v^T(K_1-K_2)v=0`.

This is the correct seam contract: equality on the overlap span, not equality of the ambient matrices.

The rational symbolic replay also gives

`R_1=[0,0]`, `R_2=[-1,1]`, `K_1=0`, `K_2=C`

with exact arithmetic.

---

## 10. Checker consequence for finitely generated fan overlaps

Suppose T-P5-185/T-P5-186 produces two regional packets with overlap cone

`Omega=cone(V)`.

If both regional generator/KKT gates are already proved, then mathematically the following identities are forced:

1. **kernel seam**

   `P(Y_alpha-Y_beta)V=0`;

2. **residual seam**

   `(R_alpha-R_beta)V=0`;

3. **reduced-energy seam**

   `V^T(K_alpha-K_beta)V=0`.

Thus these are best treated as cheap exact producer-consistency assertions, not as an additional conceptual proof obligation.

A nonzero exact mismatch on a claimed common generator means at least one of the following is wrong:

- the generator is not really in both cones;
- one regional KKT packet is invalid;
- the two packets do not use the same `P,B,C` source/key;
- the source/CSE producer mixed coordinate order or normalization.

It is **not** a new kind of mathematical discontinuity.

---

## 11. Canonical pruning information

Residual uniqueness gives a stronger pruning invariant than transport equality.

For each external `e`, define the canonical residual

`r_*(e)`

from any valid KKT minimizer. Then

- coordinates with `r_*i(e)>0` are forced to zero in every minimizing inherited state;
- only coordinates with `r_*i(e)=0` may change support through kernel gauge;
- if two candidate face packets give different residuals at the same overlap generator, they cannot both be valid;
- when `P>0`, even the minimizing state is unique, so face packets agreeing on a seam can be merged at the state level there.

This suggests that a singular fan producer should key boundary transitions by the **canonical residual-zero set** first, and only then by one chosen minimal-support representative. That avoids interpreting kernel-gauge support changes as physically distinct energy branches.

---

## 12. Suggested Lean theorem decomposition

The most valuable leaves are small and do not require matrix inverses.

### `orthantKKT_twoSolutions_kernelDiff`

Assumptions:

- `P` symmetric PSD;
- `y,z,rY,rZ` finite vectors;
- `rY=P*y+b`, `rZ=P*z+b`;
- `y,z,rY,rZ>=0` coordinatewise;
- `dot y rY=0`, `dot z rZ=0`.

Conclusion:

`P*(z-y)=0`.

Proof path: expand `f(z)-f(y)` and the reverse, use nonnegativity, then use the PSD zero-quadratic-form lemma.

### `orthantKKT_residual_unique`

Reuse the previous theorem to prove

`rY=rZ`.

### `orthantKKT_energy_unique`

Prove

`quad P y = quad P z`

and therefore equality of the reduced full energy.

### `transportOverlap_kernelGauge`

If two linear transports satisfy the pointwise KKT packet on all generators of a cone, prove

`P*(Y1-Y2)*V=0`.

### `transportOverlap_reducedPullback_eq`

From the previous identity and symmetry of `P`, prove

`V^T*(K1-K2)*V=0`.

### `pd_transportOverlap_state_eq`

Under positive definiteness, strengthen the generator identity to

`(Y1-Y2)*V=0`.

A separate tiny lemma should establish

`P PSD` and `x^T P x=0  =>  P x=0`.

No pseudoinverse or spectral decomposition is required in the theorem statements.

---

## 13. Routing recommendation

After T-P5-185/T-P5-186 constructs a finite active fan:

1. verify each regional KKT packet and regional reduced copositivity as already required;
2. for every nonempty declared overlap, optionally run the exact generator seam checks above as a source/CSE consistency diagnostic;
3. do **not** require ambient `Y_alpha=Y_beta` when `P` is singular;
4. do **not** require ambient `K_alpha=K_beta` for lower-dimensional overlaps;
5. use the canonical residual-zero set to normalize/prune duplicated boundary faces;
6. if an overlap seam identity fails, fail closed on packet/source consistency rather than inventing an energy discontinuity;
7. retain the existing source, coverage, Float64, Lean/kernel, independent-validation, and admission gates.

---

## 14. Remaining obligations

Still open:

1. actual same-key `P,B,C` production for the physical P5 block;
2. actual construction of the regional face cones and overlap generators;
3. regional copositivity certificates for all surviving reduced forms;
4. source/domain/path/Float64/controller/FD/P8/M4 binding;
5. Lean/kernel implementation of the KKT kernel-gauge leaves;
6. independent validation by 封不觉;
7. admission/registry integration.

The mathematical child remains

**`CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`.**