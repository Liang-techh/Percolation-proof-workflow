---
kind: review_result
review_id: review-T-P5-093-base-flow-lie-defect-honglianmozun-20260908T1758Z
task_id: T-P5-093-BASE-FLOW-LIE-DEFECT
agent: 红莲魔尊
source_agent: 红莲魔尊
reviewer: 红莲魔尊
created_at: 2026-09-08T17:58:00Z
claim_commit: 110ab12ef25c33893b80a87aa8b13ef983366cfb
inspected_commit: a7e73cccc6bd777fba17a3edaac37d7494c7c1e3
inspected_upstream:
  - agent_review_inbox/review-T-P5-090-moving-metric-contraction-congruence-liuguanyi-20260908T1710Z.md
  - agent_review_inbox/review-T-P5-091-variational-defect-robust-contraction-guyuefangyuan-20260908T1730Z.md
  - agent_review_inbox/review-T-P5-089-mechanical-skew-energy-honglianmozun-20260908T1104.md
  - examples/routeb_p5_moving_metric_contraction_lean/P5MovingMetricContraction.lean
status: CONDITIONAL_PASS
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_base_flow_lie_defect_leaf_then_bind_same_tube_b_Db_DW_packet
commands: none_math_derivation_only
---

# T-P5-093 — base-flow Lie-defect closure for moving-metric contraction

## 0. Question and scope

T-P5-090 proves the exact moving-metric contraction tensor for the nominal base
flow

`xdot = -F(t,x)`

and T-P5-091 proves robustness when the **variational equation alone** is
perturbed while the nominal base path is kept fixed.  T-P5-091 explicitly
leaves perturbations of the *base trajectory itself* open because changing the
base flow changes both:

1. the Jacobian seen by the variation, and
2. the material derivative of the state-dependent metric.

This child closes that exact-real mathematical gap.

The key result is that a base-flow perturbation `b` enters variational energy
through one signed tensor only,

`LIE_b(W) := D W[b] + (Db)^T W + W(Db)`.

This is the coordinate expression of the Lie derivative of the covariant
metric along `b`.  It must be assembled **before** absolute-value or norm
bounds.  A same-metric quadratic upper certificate on this tensor consumes the
nominal contraction rate linearly; any additional variational defect can then
be handled by T-P5-091 without double-counting the base perturbation.

Out of scope: deployed source binding, Lean compilation, Float64/FD/controller
execution, P8 tube coverage, receipt/provenance/admission, and registry changes.

---

## 1. Nominal packet from T-P5-090

Let

`xdot = -F(t,x)`

with

`A := D_x F`.

Let `W(t,x)` be a symmetric `C^1` metric and define the nominal material
metric derivative

`L_F W := W_t - D_x W[F]`.

T-P5-090's physical contraction tensor is

**(1.1)**

`C0 := A^T W + W A - L_F W`.

For the nominal variational energy

`V := xi^T W xi`,

and nominal variation `xidot=-A xi`,

`Vdot = - xi^T C0 xi`.

Assume the same-tube nominal certificate

**(1.2)**

`xi^T C0 xi >= 2 mu * xi^T W xi`

for every relevant `xi`.

No inverse of `W` is required for this quadratic-form statement.

---

## 2. Perturb the base trajectory itself

Now change the physical base flow to

**(2.1)**

`xdot = -F(t,x) + b(t,x)`.

Write

`B := D_x b`.

The exact variational equation of this perturbed base flow is

**(2.2)**

`xidot = (-A + B) xi`.

The metric is now transported along `-F+b`, so its exact derivative is

**(2.3)**

`W_t + D_x W[-F+b]`
`= L_F W + D_x W[b]`.

Therefore direct differentiation of `V=xi^T W xi` gives

**(2.4) EXACT BASE-PERTURBATION ENERGY IDENTITY**

`Vdot`
`= - xi^T C0 xi`
`  + xi^T ( D_xW[b] + B^T W + W B ) xi`.

Define the signed base-flow defect tensor

**(2.5)**

`S_b := D_xW[b] + B^T W + W B`.

Then simply

**(2.6)**

`Vdot = -Q_C0(xi) + Q_Sb(xi)`.

Equivalently, the exact contraction tensor of the perturbed flow is

**(2.7)**

`C_b = C0 - S_b`.

This formula is the main structural fingerprint of the child.

### Why the three terms must stay together

The two Jacobian terms `B^T W + W B` and the material-drift term `D_xW[b]`
are not independent generic error budgets.  They are the single metric
Lie-derivative object produced by changing the base vector field.  Bounding
them separately by entrywise absolute values can erase exact cancellation,
just as splitting the moving-frame terms in T-P5-090 erases chart covariance.

---

## 3. Signed relative Lie-defect theorem

Assume a same-tube source packet proves the signed quadratic upper bound

**(3.1)**

`xi^T S_b xi <= 2 rho * xi^T W xi`

for all relevant `xi`.

Here `rho` may be signed.  A negative `rho` means the perturbation is actually
favorable in the chosen metric.

Combining (1.2), (2.4), and (3.1) gives immediately

**(3.2)**

`Vdot <= -2 (mu-rho) V`.

Thus if

**(3.3)** `mu-rho > 0`,

the perturbed base flow remains differentially contracting with rate
`mu-rho` in the **same metric**.

The trusted interface is division-free:

- a lower quadratic-form certificate for `C0-2mu W`;
- an upper quadratic-form certificate for `S_b-2rho W`;
- the scalar order gate `rho < mu`.

No matrix inverse, square root, generalized eigenvalue, or condition number is
mathematically required.

### Constant-metric specialization

If `W` is constant in `x`, then `D_xW[b]=0` and

`S_b = B^T W + W B`.

So only the symmetric `W`-part of `Db` matters to contraction.  This is the
base-flow analogue of the skew-energy cancellation in T-P5-089.

---

## 4. Exact Killing/skew cancellation

Take constant metric `W=I` and let

`b(x)=K J x`

where `J^T=-J` is any skew matrix and `K` is arbitrarily large.  Then

`B=KJ`,

and

`S_b = B^T+B = K(J^T+J)=0`.

Therefore this perturbation costs **zero contraction rate** even though
`||b||` and `||Db||` may be arbitrarily large on a fixed nontrivial domain as
`|K|` grows.

Hence a source lane that first turns `b` or `Db` into an unsigned operator norm
can be arbitrarily more conservative than the true energy object.  The correct
order is

`b, Db, DW`
` -> form S_b = DW[b] + Db^T W + W Db`
` -> enclose the signed quadratic form`
` -> only then compare with 2 rho W`.

This is a genuine nonlinear-energy cancellation, not a numerical coincidence.

---

## 5. Hard obstruction A: a magnitude bound on b alone is insufficient

Even with constant metric, a uniform small bound on the base-flow perturbation
itself gives no differential-contraction control because contraction depends on
its derivative.

Take one dimension with

`W=1`,

`F(x)=mu x`, `mu>0`,

so the nominal system is `xdot=-mu x` and has exact contraction rate `mu`.

For fixed `epsilon>0`, define

**(5.1)**

`b_K(x)=epsilon sin(Kx)`.

For every `K`,

`|b_K(x)| <= epsilon`

uniformly.  But

`B_K(x)=epsilon K cos(Kx)`,

so at `x=0`,

`B_K(0)=epsilon K`.

Since `W=1`,

`S_b(0)=2 epsilon K`,

and the perturbed contraction scalar is

**(5.2)**

`C_b(0)=2mu-2epsilon K`.

Choosing

`K > mu/epsilon`

makes `C_b(0)<0` although the perturbation amplitude remains bounded by the
same arbitrarily small `epsilon`.

Therefore a packet of the form

`|b| <= epsilon`

cannot replace a derivative/Lie-defect certificate in a variational
contraction proof.  This is an information-theoretic obstruction.

---

## 6. Hard obstruction B: Db alone is insufficient for state-dependent W

When the metric depends on state, controlling only `Db` also fails because the
base perturbation moves the metric itself.

Use the one-dimensional domain `0 <= x <= 1` with

`W(x)=1+x`,

`F(x)=x/4`.

Then `A=1/4` and

`L_F W = - D_xW[F] = -x/4`.

Hence

`C0`
`= 2*(1/4)*(1+x) - (-x/4)`
`= 1/2 + 3x/4`.

With `mu=1/4`,

`2mu W = (1/2)(1+x)=1/2+x/2`,

so

**(6.1)**

`C0 - 2mu W = x/4 >= 0`.

Thus the nominal system contracts at rate at least `1/4` on this domain.

Now add the constant base perturbation

`b(x)=1`.

Then

`Db=0`,

but

`D_xW[b]=1`.

Therefore

`S_b=1`

and

**(6.2)**

`C_b = C0-1 = -1/2 + 3x/4`.

At `x=0`, `C_b=-1/2<0`.

A checker that looks only at `Db` sees a zero Jacobian defect and would miss the
entire loss of contraction.  The term `D_xW[b]` is mathematically mandatory
whenever `W=W(t,x)` moves with state.

This local counterexample is independent of the separate question of whether a
particular deployed trajectory stays inside `[0,1]`; same-tube coverage remains
an explicit downstream obligation.

---

## 7. Combine with an additional variational defect without double counting

Suppose the actual variational dynamics contains an additional defect `e`
beyond the exact Jacobian change generated by the base perturbation:

**(7.1)**

`xidot = (-A+B) xi + e`.

Then the exact energy identity is

**(7.2)**

`Vdot = -Q_C0(xi) + Q_Sb(xi) + 2 <xi,e>_W`.

The base perturbation must be charged through `S_b`; it must **not** be charged
again by pretending that `Bxi` is an unrelated variational residual.

Assume the signed base-flow rate packet

`Q_Sb(xi) <= 2 rho V`.

Decompose the truly additional defect as

`e = r + d`,

where

**(7.3)** `<xi,r>_W <= sigma V`,

and

**(7.4)** `Q_W(d) <= Ebar`.

Define the remaining contraction reserve

**(7.5)**

`nu := mu-rho-sigma`.

If

`nu > 0`,

then

`Vdot <= -2nu V + 2<xi,d>_W`.

Since PSD of `W` gives

`Q_W(nu xi-d) >= 0`,

we have

`2nu<xi,d>_W <= nu^2 V + Q_W(d)`.

Therefore:

**(7.6) MAIN MIXED BASE+VARIATIONAL DEFECT THEOREM**

`nu Vdot <= -nu^2 V + Ebar`.

Consequently any proposed invariant variational-energy level `Vstar>=0`
satisfying the division-free gate

**(7.7)**

`Ebar <= nu^2 Vstar`

has

**(7.8)**

`V=Vstar  =>  Vdot <= 0`.

With a strict inequality in (7.7), one gets strict inward pointing at the
boundary.  This is exactly T-P5-091's invariant-tube consumer after first
subtracting the signed base-flow Lie-defect rate `rho`.

---

## 8. Source/consumer typing rule

This child identifies three different data types that must not be merged:

1. **base-flow perturbation** `b`;
2. **base Jacobian perturbation** `B=Db`;
3. **additional variational residual** `e` after the exact `Bxi` term has been
   included.

For moving `W`, the correct base-flow energy packet is not any one of these
alone but

`S_b = DW[b] + B^T W + W B`.

If an executable variational model uses an approximation `Bhat` rather than the
exact `Db`, write

`Bhat = B + R`.

Then `B` belongs inside `S_b`, while the implementation mismatch `Rxi` belongs
in T-P5-091's relative variational-defect lane.  Charging both `Bxi` and
`S_b` would double count the physical base perturbation.

Likewise, a state-residual amplitude bound from an ordinary Lyapunov ledger is
not automatically a differential-contraction packet.  To consume it here,
source-side differentiation or a directly certified signed Lie-defect bound is
required.

---

## 9. Minimal theorem candidates for Lean

The first sidecar can stay exact-real, finite-dimensional, and source
independent.  In the existing 2x2 scalarized style of
`P5MovingMetricContraction.lean`, useful theorem targets are:

1. `base_flow_lie_defect_q2_identity`
   - exact polynomial identity corresponding to
     `Vdot = -Q_C0 + Q_Sb` once the derivative packet is supplied;

2. `base_flow_lie_defect_rate_loss`
   - from
     `Q_C0 >= 2mu Q_W` and `Q_Sb <= 2rho Q_W`, derive
     `Vdot <= -2(mu-rho)Q_W`;

3. `base_flow_plus_variational_defect_rate`
   - add a signed relative cross-power bound
     `<xi,r>_W <= sigma Q_W`;

4. `base_flow_mixed_defect_invariant_tube`
   - with `nu=mu-rho-sigma>0` and `Q_W(d)<=Ebar`, prove
     `nu*Vdot <= -nu^2*Q_W + Ebar` and the boundary gate
     `Ebar <= nu^2 Vstar`;

5. `constant_metric_skew_base_defect_zero`
   - regression `B^T W+WB=0` for a skew perturbation in `W=I`;

6. `base_amplitude_does_not_control_contraction`
   - scalar `epsilon sin(Kx)` obstruction;

7. `dropping_metric_transport_of_base_defect_counterexample`
   - scalar `W=1+x`, `F=x/4`, `b=1` regression showing `Db=0` but nonzero
     `DW[b]` destroys the nominal contraction sign.

The first algebraic leaf can reuse the existing `qform2`, `bilinear2`, and
`symJacobianQ2` definitions.  No differential-geometry library is required to
formalize the consumer boundary.

---

## 10. Exact closure boundary

### Closed mathematically by this child

- exact variational-energy identity when the **base flow itself** changes from
  `-F` to `-F+b`;
- identification of the single signed metric Lie-defect tensor
  `DW[b]+Db^T W+WDb`;
- exact linear contraction-rate loss `mu -> mu-rho`;
- exact zero-cost skew/Killing cancellation;
- mixed base-flow + relative/additive variational-defect invariant-tube theorem;
- proof that `|b|` alone is insufficient;
- proof that `Db` alone is insufficient when `W` depends on state.

### Still open

- a deployed same-tube binding for `b`, `Db`, `W`, and `DW`;
- proof that an actual controller/solver/FD defect induces the proposed `b` and
  derivative packet on the same domain;
- moving-chart transport of the **base-flow Lie defect** as a separate naturality
  theorem (expected to be a pullback congruence, but not claimed here);
- finite-step discrete integration of the perturbed base flow;
- Float64 execution semantics and P8 ODE/flowpipe coverage;
- Lean/kernel receipt and independent validation;
- registry/admission propagation.

**Admission remains `pending`.  This is a mathematical child theorem, not a
source certificate or parent closure.**
