---
kind: review_result
review_id: review-T-P5-090-moving-metric-contraction-congruence-liuguanyi-20260908T1710Z
task_id: T-P5-090-MOVING-METRIC-CONTRACTION-CONGRUENCE
agent: 柳冠一
source_agent: 柳冠一
reviewer: 柳冠一
created_at: 2026-09-08T17:10:00Z
claim_commit: a54235c628c33607d6456417370ee259916df9d5
inspected_upstream:
  - 72f430f93517ccf4bf5da5e26b29c83c56ef5e7b
  - 6f96c363348d39ac218b07ba30f5011edbe70314
  - 984fb7d4a75c019a7e40fe542ac67141efcc0804
  - ff1f8c015adfe3fa3cd95016191a6d6bfa77e578
  - 8faea4cff4f6f5157d2c11ed98f9473da8fd90cc
status: CONDITIONAL_PASS
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
summary: >-
  Prove an exact differential-contraction transport theorem for a time/state-
  dependent physical metric under a moving nonlinear chart. With xdot=-F,
  L_F W=W_t-DW[F], C_x=A^T W+W A-L_F W, x=T(t,z), J=D_zT,
  JG=F(T)+T_t, B=D_zG, and M=J^T(W o T)J, the full normalized contraction
  tensor satisfies B^T M+M B-(M_t-DM[G]) = J^T C_x J. Hence any physical
  inequality C_x >= 2 mu W transports with exactly the same mu to
  C_z >= 2 mu M, without matrix inversion or square roots. The theorem also
  isolates two unsound shortcuts: dropping the material metric derivative and
  freezing the pulled-back metric in a moving frame.
---

# T-P5-090 — moving/state-dependent metric contraction congruence

## 0. Scope and relation to the current P5 lane

T-P5-082 established exact moving-chart calculus for a **fixed physical metric**
and showed that chart-connection terms cancel against the derivative of the
pulled-back metric at the differential level. T-P5-086 then treated a discrete
moving-frame Euler defect. T-P5-087 transported that defect through moving
quadratic measurement metrics, while T-P5-088 gave the exact material derivative
for a state-dependent quadratic **state storage**.

A still-separate mathematical object is differential contraction in a metric
`W(t,x)` that itself depends on time/state. Its energy is not `x^T W x`; it is the
variational energy

`V_delta(t,x,delta x) = delta x^T W(t,x) delta x`.

The missing bridge is whether the complete physical contraction tensor and its
rate survive a moving nonlinear coordinate change. They do, but only if the
material metric derivative and chart connection are kept together.

This review proves that exact congruence. It does not claim a deployed P5 source
binding, a finite-step/secant certificate, a Lean/kernel receipt, Float64
semantics, coverage, or admission.

---

## 1. Physical differential contraction with a moving metric

Let the physical system be

**(1.1)** `xdot = -F(t,x)`

and write

`A(t,x) := D_x F(t,x)`.

A variational vector `xi` then obeys

**(1.2)** `xidot = -A xi`.

Let `W(t,x)` be a symmetric `C^1` matrix field. Along the nominal physical flow
define the material derivative

**(1.3)**

`L_F W := W_t - D_x W[F]`.

The minus sign is forced by `xdot=-F`.

For

`V_x := xi^T W xi`,

direct differentiation gives

**(1.4)**

`V_x_dot`
` = xi^T (L_F W - A^T W - W A) xi`.

Define the full physical contraction tensor

**(1.5)**

`C_x := A^T W + W A - L_F W`.

Then simply

**(1.6)** `V_x_dot = - xi^T C_x xi`.

Therefore the pointwise quadratic-form inequality

**(1.7)** `C_x >= 2 mu W`

implies

**(1.8)** `V_x_dot <= -2 mu V_x`.

This is the state/time-dependent-metric replacement for the frozen-metric
condition `A^T W+W A >= 2 mu W`.

### Minimal physical theorem statement

For every variational vector `xi`,

`xi^T (A^T W+W A-(W_t-DW[F])) xi >= 2 mu xi^T W xi`

implies

`d/dt (xi^T W xi) <= -2 mu (xi^T W xi)`

along `xdot=-F`, `xidot=-Axi`.

No chart assumption is needed for this leaf.

---

## 2. Moving nonlinear chart and the variational connection identity

Let

**(2.1)** `x = T(t,z)`,

with

`J(t,z) := D_z T(t,z)`.

Let the transformed nominal system be

**(2.2)** `zdot = -G(t,z)`.

For (2.1)-(2.2) to represent the same physical trajectory, the source-to-math
covariance identity must be

**(2.3)**

`J G = F(t,T) + T_t`.

Equivalently `T_t-JG=-F(t,T)`.

Write

`B(t,z) := D_z G(t,z)`.

Differentiating (2.3) with respect to `z` in an arbitrary direction and using
symmetry of the second derivative of `T` gives

`D_z J[G] + J B = A J + J_t`.

Thus the exact moving-frame variational connection identity is

**(2.4)**

`J_t - D_z J[G] = J B - A J`.

This is the matrix identity that makes all connection terms cancel. A checker
must not replace it by `J B=A J` unless both `J_t=0` and `D_zJ[G]=0` have been
proved.

---

## 3. Pulled-back moving metric

Pull the physical metric back through the chart:

**(3.1)**

`M(t,z) := J(t,z)^T W(t,T(t,z)) J(t,z)`.

For the normalized flow `zdot=-G`, define its material derivative

**(3.2)**

`L_G M := M_t - D_z M[G]`.

The middle metric factor has a particularly clean transport identity. By the
ordinary chain rule and (2.3),

`(partial_t - D_z[ G ]) (W(t,T(t,z)))`
` = W_t + D_xW[T_t] - D_xW[JG]`
` = W_t + D_xW[T_t-JG]`
` = W_t - D_xW[F]`
` = L_F W`.

Therefore product differentiation of (3.1) yields

**(3.3)**

`L_G M`
` = (J_t-DJ[G])^T W J`
`   + J^T (L_F W) J`
`   + J^T W (J_t-DJ[G])`.

Substitute (2.4):

`J_t-DJ[G]=JB-AJ`.

After collecting terms,

**(3.4)**

`L_G M`
` = B^T M + M B`
`   - J^T (A^T W+W A) J`
`   + J^T (L_F W) J`.

Hence the normalized full contraction tensor

**(3.5)**

`C_z := B^T M + M B - L_G M`

obeys the exact congruence identity

**(3.6)**

`C_z = J^T C_x J`.

This is the main theorem of this child.

---

## 4. Exact rate transport

Assume the physical source proves, on the same spacetime tube,

**(4.1)** `C_x >= 2 mu W`.

For every normalized variational vector `eta`, substitute `xi=J eta` into (4.1):

`eta^T J^T C_x J eta`
` >= 2 mu eta^T J^T W J eta`.

Using (3.1) and (3.6),

**(4.2)**

`C_z >= 2 mu M`.

Thus the same numerical contraction rate `mu` is transported with **no loss**.
For `V_z=eta^T M eta` and `etadot=-B eta`,

**(4.3)** `V_z_dot <= -2 mu V_z`.

### Important strength point

The implication `(4.1) => (4.2)` does not require a matrix inverse or even an
explicit `J^{-1}`: it is pure substitution into a quadratic-form inequality.
If `J` is invertible, the converse also follows by congruence, so the physical
and normalized differential contraction conditions are equivalent.

The trusted algebraic core can therefore stay division-free even when the
source chart is represented with denominator-cleared identities.

---

## 5. Exact obstruction 1: dropping the metric material derivative

Take the one-dimensional physical system

`F=0`, hence `A=0`,

and the positive time-dependent metric

`W(t)=1+t`, on `0<=t<=1`.

The variational vector is constant. Its true energy is

`V_x=(1+t) xi^2`,

so

`V_x_dot=xi^2>0`.

The correct material derivative is

`L_F W=W_t=1`,

and therefore

`C_x=-1`.

If one freezes the metric and uses only `A^T W+W A=0`, one incorrectly predicts
nonincrease. Thus pointwise positive definiteness of `W` does not license
omission of `W_t-DW[F]`.

This is not a small conservatism issue: it changes the sign of the energy rate.

---

## 6. Exact obstruction 2: moving-chart apparent contraction is canceled by Mdot

Take again the physical zero system

`F=0`, `W=1`,

but use the moving affine chart

**(6.1)** `T(t,z)=(1+t)z`, with `t>=0`.

Then

`J=1+t`, `T_t=z`.

The covariance equation (2.3) is the denominator-cleared identity

**(6.2)** `(1+t) G = z`.

Hence, differentially,

**(6.3)** `(1+t) B = 1`.

The pulled-back metric is

**(6.4)** `M=(1+t)^2`.

Since `M` is independent of `z`,

`L_G M=M_t=2(1+t)`.

Now use (6.3) without dividing:

`2 B M = 2 B (1+t)^2 = 2(1+t)`.

Therefore

**(6.5)**

`C_z = 2BM-M_t = 0`,

exactly matching the physical tensor `C_x=0`.

If the normalized checker were to freeze `M` and keep only `2BM`, it would
manufacture a strictly positive contraction tensor for a physical system that
does nothing. The missing `M_t` is precisely the chart-scale connection charge.

This example is also useful for implementation: the source need not compute
`B=1/(1+t)`; the exact multiplication identity `(1+t)B=1` suffices.

---

## 7. Why signed/correlated assembly must precede intervalization

Equation (3.6) shows that the following large collection of terms

`B^T M`, `M B`, `-M_t`, `+DM[G]`

is not four unrelated error budgets. Their sum is exactly the congruence of the
physical tensor.

Similarly, after expanding `M=J^T WJ`, the terms containing

`J_t`, `DJ[G]`, `W_t`, `DW[T_t]`, `DW[JG]`

have exact signed cancellations.

Therefore the source order should be

`F,W,T`
` -> form L_F W`
` -> form C_x=A^TW+WA-L_FW`
` -> establish chart covariance / variational identity`
` -> form M=J^TWJ`
` -> use C_z=J^TC_xJ`
` -> only then enclose the resulting quadratic form`.

An absolute-value-first decomposition of the connection and metric-drift pieces
can create arbitrarily large artificial charges under a rapidly moving but
mathematically exact coordinate frame.

This is the same interface principle already seen in the signed Gram, radical
factor-cancellation, and moving-frame curvature children: preserve exact
correlation until after the structural identity has been formed.

---

## 8. Minimal typed source contract

A small source packet sufficient for this theorem is:

### Physical side

- `xdot = -F(t,x)` source binding;
- `A = D_xF` exact derivative binding;
- symmetric physical metric `W(t,x)`;
- exact material derivative packet
  `L_FW = W_t - D_xW[F]`;
- full physical tensor
  `C_x = A^T W + W A - L_FW`;
- same-tube quadratic lower certificate
  `C_x >= 2 mu W`.

### Chart side

- exact chart `x=T(t,z)` and `J=D_zT`;
- transformed field `G` with covariance
  `JG = F(t,T)+T_t`;
- `B=D_zG`;
- pulled metric `M=J^T(W o T)J`.

The variational connection identity (2.4) may either be derived from the
covariance theorem under sufficient differentiability, or supplied as a small
checked child if the source representation makes differentiation awkward.

### Consumer theorem

Consume only

`C_z = J^T C_x J`

and the physical lower certificate. Then infer

`C_z >= 2 mu M`.

No generalized eigenvalue, square root, matrix inverse, or explicit inverse chart
is needed for the forward implication.

---

## 9. Relation to T-P5-088 state storage

T-P5-088 studies

`V_state(t,y)=y^T W(t,y)y`.

This child studies instead

`V_delta(t,x,xi)=xi^T W(t,x)xi`.

They share the same material derivative `W_t-DW[F]` under nominal dynamics, but
their remaining terms are different: state storage contains the actual state
vector and, with defects, the full storage-gradient coupling; differential
contraction contains the variational Jacobian terms `A^TW+WA`.

These theorems should therefore share a material-derivative definition but should
not be merged into one overloaded Lean theorem.

---

## 10. Suggested Lean decomposition

Keep the first formalization source-independent and finite-dimensional:

1. `quadVariation_deriv_moving_metric`
   - derivative of `xi^T W xi` along `xdot=-F`, `xidot=-Axi`.

2. `moving_chart_variational_connection`
   - from differentiable covariance `JG=F o T+T_t`, derive
     `J_t-DJ[G]=JB-AJ`.

3. `pullback_metric_material_deriv`
   - prove equation (3.3).

4. `moving_metric_contraction_tensor_congruence`
   - prove `B^TM+MB-L_GM=J^T C_x J`.

5. `contraction_rate_pullback`
   - pure quadratic-form substitution
     `C_x>=2mu W -> J^TC_xJ>=2mu J^TWJ`.

The fifth theorem is an especially small algebraic leaf and can be compiled
independently of the differential-calculus API.

---

## 11. What this closes and what remains open

### Closed mathematically by this child

- the correct physical contraction tensor for a state/time-dependent metric;
- the exact moving-chart material derivative of the pulled metric;
- the exact congruence `C_z=J^TC_xJ`;
- preservation of the same differential contraction rate `mu`;
- proof that neither metric drift nor moving-frame connection may be dropped;
- a division-free forward transport interface.

### Still open

- deployed P5 binding of the actual `W(t,x)`, `F`, `A`, `T`, `J`, `G`, `B`;
- exact rational generation of the physical tensor lower certificate;
- positive-definite/coercivity packets required by downstream distance claims;
- common spacetime tube / domain coverage for all derivatives;
- defects/noise in the variational dynamics;
- finite-step/secant contraction under nonlinear charts;
- discrete integrators beyond the exact differential identity;
- Float64, FD, controller/solve semantics;
- P8/ODE trajectory coverage;
- Lean/kernel compilation and `#print axioms`;
- independent verification by 封不觉;
- comparator/admission/registry changes.

Accordingly this result remains **pending mathematical/interface child** and must
not be promoted to verified/admitted P5 status on the strength of this review
alone.
