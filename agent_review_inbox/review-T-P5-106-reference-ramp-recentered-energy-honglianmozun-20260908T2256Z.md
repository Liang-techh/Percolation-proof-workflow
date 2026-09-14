---
kind: review_result
review_id: review-T-P5-106-reference-ramp-recentered-energy-honglianmozun-20260908T2256Z
task_id: T-P5-106-REFERENCE-RAMP-RECENTERED-ENERGY
source_agent: 红莲魔尊
created_at: 2026-09-08T22:56:00Z
claim_commit: d933bdd59d8bbd386d2860bea82404666391588b
inspected_commit: c1bc01495c5589ce13b2b36950dd6c4307c44b95
upstream_review_commits:
  - 6bbb8bd15c07a96bf4deabce3b165bc53a5119c2
  - 805f5ac6d2cbbc9bda42a08cf6f01636fe64affc
status: CONDITIONAL_PASS_WITH_EXACT_RATIONAL_PACKET
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize the position-only input recenter identity and bind B/g/a/w to one actual referenceKey; then use the slope collar plus shifted pB bridge in the P5-098/P5-100 collar budget
commands: none_math_derivation_only
lean_compile_status: not_run
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

# T-P5-106 — position-only ramp recentering for the Route-B reference energy

## 0. Result

T-P5-104/T-P5-105 bound the nominal reference directly in the original coordinates. For a persistent forcing `g w(t)`, that necessarily creates an additive energy charge proportional to the **input amplitude**. The present child identifies an exact structural cancellation that is better adapted to a continuous ramp.

For

`q' = v`,

`M v' + D v + B q = g w(t)`,

choose a constant vector `a` satisfying the algebraic center identity

**(0.1)** `B a = g`.

Define only a **position** recentering

**(0.2)** `z := q-a w`,  `s := v`.

Then the input amplitude disappears identically from the second-order balance:

**(0.3)** `M s' + D s + B z = 0`,

while the kinematic equation becomes

**(0.4)** `z' = s-a w'`.

For the T-P5-105 skew-stiffness cross-energy, the resulting Lyapunov derivative depends on `w'` but not on `w` and not on `w''`. Consequently, on a constant-input plateau the recentered energy decays homogeneously, while on an affine ramp it pays only a slope-squared collar budget.

This position-only choice is structurally preferable to simultaneously shifting velocity by `a w'`: it remains continuous through a continuous piecewise-affine ramp even when the slope jumps, so it does not create an artificial storage reset at ramp corners.

For the exact rational Route-B coefficient packet already used by T-P5-105, an explicit center is

**(0.5)** `a = (2340/8699, 1520/8699)^T`,

with

`det B = 8699/20000 > 0`

and `B a = g` exactly. A rational quadratic certificate then gives a slope-only invariant-level gate

**(0.6)** `20 R_in >= 7 Sbar`

whenever `(w')^2 <= Sbar` on the ramp segment. A second exact PSD certificate reconnects the centered energy to the absolute P5 reference weight:

**(0.7)** `pB(q,v) <= (67/2) Vc(z,v) + (41/200) w^2`.

Thus the derivative budget is slope-controlled, while the unavoidable absolute reference displacement appears only in the value/domain bridge.

All statements below are exact-real mathematics. No actual `referenceKey`, runtime coefficient semantics, Float64/controller behavior, P8 coverage, Lean receipt, admission, or registry mutation is claimed.

---

## 1. Exact input-center identity

Use the same exact rational coefficient packet as T-P5-105:

`M = diag(350003/3000000, 200739/4000000)`,

`D = diag(4/5, 13/20)`,

`B = [[3/4,-1/100],[-1/200,29/50]]`,

`g = (1/5,1/10)^T`.

As in T-P5-105, split

`B = K-A`,

`K = [[3/4,-3/400],[-3/400,29/50]]`,

`A = [[0,1/400],[-1/400,0]]`,  `A^T=-A`.

The determinant of `B` is

`det B = (3/4)(29/50)-(-1/100)(-1/200)`
`      = 8699/20000 > 0`.

The exact vector

`a = (2340/8699,1520/8699)^T`

satisfies

`B a = (1/5,1/10)^T = g`.

No inverse primitive is needed by a checker: `a` may be supplied as a rational witness and `B a=g` verified by ring normalization.

### Candidate theorem

`reference_input_center_exact`

Inputs: constant `B,g,a` and the equality `B a=g`.

Output: after `z=q-a*w`, `s=v`, the original reference equation is equivalent to (0.3)-(0.4).

---

## 2. Position-only recentering removes amplitude forcing exactly

Let `w` be differentiable on the current flow segment and define

`z=q-a w`, `s=v`.

Then

`z' = q'-a w' = s-a w'`.

The dynamic equation gives

`M s' + D s + B z`
` = M v' + D v + B(q-a w)`
` = g w - B a w`
` = 0`.

Thus the potentially large amplitude `w` has disappeared before any inequality is taken.

This is a nonlinear-energy bookkeeping point: one should perform the exact source cancellation `B a=g` **before** taking norms or allocating Young budgets. Otherwise a persistent input is charged as an additive disturbance even when it is merely moving the static equilibrium.

---

## 3. Exact recentered cross-energy identity

Use the T-P5-105 storage, now on `(z,s)`:

**(3.1)**

`Vc(z,s)`
` := 1/2 s^T M s`
`  + 1/2 z^T K z`
`  + z^T M s`
`  + 1/2 z^T D z`.

Let

`x=(z,s)`,

`P = [[K+D,M],[M,M]]`,

`Q = [[K,A/2],[A^T/2,D-M]]`.

Then

`Vc = 1/2 x^T P x`.

Define

**(3.2)**

`Qd(z,s) := z^T K z + s^T(D-M)s - s^T A z`
`          = x^T Q x`.

Differentiate (3.1), using `z'=s-a w'`, `M s'=-D s-(K-A)z`, symmetry of `M,D,K`, and `z^T A z=0`. All homogeneous cross terms cancel exactly and one obtains

**(3.3) POSITION-RECENTER ENERGY IDENTITY**

`Vc' = -Qd - w' * a^T[(K+D)z + M s]`.

Equivalently, define the stacked slope observable

**(3.4)**

`c_s := ((K+D)a, M a)`.

Then

`Vc' = -Qd - w' c_s^T x`.

For the current rational packet,

`(K+D)a = (18078/43495, 37041/173980)^T`,

`M a = (13650117/434950000, 3814041/434950000)^T`.

This is the main structural gain over the uncentered collar: the derivative no longer pays `w^2`; it only pays `(w')^2`.

### Candidate theorem

`reference_position_recenter_cross_energy_derivative`

Inputs:

- symmetric `M,D,K`, skew `A`, `B=K-A`;
- `B a=g`;
- reference equations and `z=q-a*w`, `s=v`.

Output: (3.3) exactly.

No inverse, eigenvalue, square root, or trajectory table appears.

---

## 4. Exact rational slope-power certificate

T-P5-105 already supplies the exact rational rate matrix certificate

**(4.1)** `2 Q - (9/10) P >= 0`,

so

**(4.2)** `Qd >= (9/10) Vc`.

For the new slope observable `c_s`, the following additional exact rational matrix is positive definite:

**(4.3)**

`(63/200) Q - c_s c_s^T > 0`.

Its leading principal minors are

`3844070901/60538080800`,

`227000789066079/484304646400000000`,

`138287662191264442465413/2421523232000000000000000000`,

`3946032434741296429406990515311/387443717120000000000000000000000000`,

all strictly positive. Hence

**(4.4)** `(c_s^T x)^2 <= (63/200) Qd`.

If the ramp slope has the source-certified bound

**(4.5)** `(w')^2 <= Sbar`,

then the signed power `p_s=-w' c_s^T x` satisfies

**(4.6)** `p_s^2 <= (63/200) Sbar Qd`.

Now use the same square-only absorption pattern as T-P5-104. For `0<theta<1`, any `beta>=0` satisfying

**(4.7)** `(63/200) Sbar <= 4 theta beta`

implies

`p_s <= theta Qd + beta`,

and therefore

**(4.8)**

`Vc' <= -(1-theta)Qd + beta`
`    <= -(1-theta)(9/10) Vc + beta`.

Everything is division-free at the trusted gate.

---

## 5. Optimal slope-only collar level inside this packet

Let

`lambda=9/10`, `chi_s=63/200`.

For fixed `theta`, the smallest additive charge allowed by (4.7) is

`beta = chi_s Sbar/(4 theta)`.

The corresponding rate is

`nu=(1-theta)lambda`.

A non-strict invariant level requires `beta <= nu R_in`, equivalently

`chi_s Sbar <= 4 lambda theta(1-theta) R_in`.

But

`4 theta(1-theta) <= 1`

is exactly the square identity

`1-4theta(1-theta)=(2theta-1)^2 >= 0`.

Therefore the smallest collar level attainable from **this rate packet and this slope-power packet** is achieved at

`theta=1/2`,

and is

**(5.1)**

`R_in >= (chi_s/lambda) Sbar`
`     = (7/20) Sbar`.

Thus the exact division-free gate is simply

**(5.2)** `20 R_in >= 7 Sbar`.

For strict inwardness use `>`.

At `theta=1/2`, one may record explicitly

`nu=9/20`,

`beta=63 Sbar/400`,

and

`Vc' <= -(9/20)Vc + 63 Sbar/400`.

On a constant-input plateau, `Sbar=0`; (3.3) becomes `Vc'=-Qd`, so the stronger homogeneous decay

**(5.3)** `Vc' <= -(9/10) Vc`

holds with zero additive budget.

This cleanly separates the physical roles of amplitude and slew rate.

---

## 6. Absolute reference-weight bridge back to P5-098

A centered collar by itself does not bound the absolute nominal reference coordinates, because `q=z+a w` carries the static offset. The amplitude must re-enter the **value/domain** bridge even though it disappeared from `Vc'`.

Let the P5 reference weight be

`pB(q,v) = (3/2)||q||^2 + (4/5)||v||^2`.

With `q=z+a w`, `v=s`, there is an exact rational quadratic certificate

**(6.1)**

`pB(z+a w,s) <= (67/2) Vc(z,s) + (41/200) w^2`.

A direct checker can verify (6.1) as positivity of one `5 x 5` rational symmetric matrix in `(z1,z2,s1,s2,w)`. Its leading principal minors are

`1957/80`,

`1196234559/2560000`,

`746202500032751919/1600000000000000`,

`6883183787574508470066821641/4096000000000000000000000000`,

`177811929644590927976132543432087881/61990994739200000000000000000000000000`,

all strictly positive.

Therefore, if

`Vc <= Rref`, `(w)^2 <= Wbar`,

then the absolute P5 nominal block obeys

**(6.2)** `pB(q,v) <= (67/2) Rref + (41/200) Wbar`.

This is the correct handoff to a hybrid anchor/domain budget: slope controls the **invariance cost**, while amplitude controls the **moving-center location**. Conflating these two roles is unnecessarily conservative.

For reference, the exact center itself has

`||a||^2 = 7786000/75672601`,

so the static q-offset contribution is only

`(3/2)||a||^2 w^2 = (11679000/75672601) w^2`,

but (6.1) deliberately keeps a simple global rational coefficient and absorbs the cross term with the same quadratic storage.

### Candidate theorem

`absolute_reference_weight_le_of_position_recenter`

Inputs: the rational PSD certificate behind (6.1).

Output: (6.1), hence (6.2) after the two scalar caps.

---

## 7. Why position-only recentering is preferable for a piecewise-affine ramp

A tempting alternative is to define

`z=q-a w`,  `r=v-a w'`.

Then `z'=r` and the dynamic residual becomes

`M r' + D r + B z = -D a w' - M a w''`.

This looks canonical, but it creates an artificial hybrid reset whenever a continuous piecewise-affine ramp changes slope. If `w` is continuous and `w'` jumps by `Delta`, then the physical `(q,v)` is continuous but

`r^+ = r^- - a Delta`.

For the same cross storage, the exact jump is

**(7.1)**

`V(z,r^+) - V(z,r^-)`
` = -Delta * a^T M(z+r^-)`
`   + (Delta^2/2) a^T M a`.

The first term has state-dependent sign and magnitude. Hence a nonzero slope jump cannot be ignored as a zero-cost coordinate change; a same-level ellipsoidal collar generally needs a reset budget.

The position-only center avoids this issue. If `w` is continuous, both

`z=q-a w` and `s=v`

remain continuous even when `w'` has a finite jump. On each affine segment (3.3) holds with its constant slope, and the storage itself matches continuously at the knot. Thus a continuous piecewise-affine source law can be handled segment-by-segment without inventing a storage reset.

This is a genuine structural fingerprint, not merely a smaller Young constant.

---

## 8. Fail-closed boundaries and exact mismatch formula

### 8.1 Same-semantics `B a=g` is essential

Suppose the actual source semantics give a mismatch

`delta_g := g-B a`.

Then (0.3) becomes

`M s'+D s+Bz = delta_g w`,

and the exact energy identity is

**(8.1)**

`Vc'`
` = -Qd`
`   - w' c_s^T x`
`   + w (z+s)^T delta_g`.

Thus any coefficient/source mismatch immediately restores an amplitude-driven power channel. It is invalid to use the slope-only gate merely because an ideal rational transcription admits `B a=g`.

The future source packet must bind `B`, `g`, `a`, and the input law to the **same referenceKey / coefficient semantics**. If deployed binary64/CSV coefficients differ, either prove the corresponding exact `B_actual a_actual=g_actual` or carry the last term of (8.1) as a separate residual budget.

### 8.2 Input jumps require a reset theorem

If `w` itself jumps, then even the position-only center jumps:

`z^+ = z^- - a Delta w`.

The storage generally changes instantaneously, so the flow inequality cannot by itself prove collar preservation across that event. The no-reset advantage above requires continuity of `w`.

### 8.3 A slope cap is not an amplitude/domain cap

Small `Sbar` does not bound `w`. A long slow ramp can move the static center arbitrarily far while paying little derivative budget. Therefore (5.2) cannot replace the independent `Wbar`/source-domain condition in (6.2). Invariance around the moving center and absolute tube membership are different typed obligations.

### 8.4 The result is not a deployed-reference theorem yet

T-P5-105 already notes that ideal rational, CSV-token, and binary64-decoded coefficient semantics have not been identified as the deployed reference law. This child inherits that boundary. The exact rational packet above is therefore a source-independent candidate until one canonical reference source is selected.

---

## 9. Minimal next handoff

A narrow source/Lean handoff can now be stated without exporting a whole nominal trajectory:

1. choose the actual `referenceKey` and bind its constant `B,M,D,g` plus continuous input law `w(t)`;
2. provide an exact or source-certified center witness `a` with `B a=g`;
3. provide `w^2 <= Wbar` for absolute-domain placement and `(w')^2 <= Sbar` on each flow segment;
4. formalize (3.3), the rational PSD gate `(63/200)Q-c_s c_s^T >=0`, and the scalar collar gate `20 Rin >= 7 Sbar`;
5. formalize the shifted absolute-weight certificate (6.1) and use `(67/2)Rref+(41/200)Wbar` in the existing hybrid anchor/domain budget;
6. if `w` is continuous piecewise affine, glue segments by continuity of `(z,s,Vc)`; if `w` jumps, add an explicit reset-energy obligation instead of reusing the flow inequality.

If the same-source equality `B a=g` fails, the exact obstruction is already isolated by (8.1): the project must pay the residual amplitude channel `w(z+s)^T(g-Ba)`. If the equality holds, persistent input amplitude is not a Lyapunov dissipation defect; it is only a moving-center/domain-placement cost.

No source identity, runtime evaluator, Float64/controller semantics, flowpipe/coverage, Lean/kernel receipt, comparator/admission, registry mutation, or final P5/M4 closure is claimed by this review.
