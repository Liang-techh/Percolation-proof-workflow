---
kind: review_result
review_id: review-T-P5-041-liuguanyi-20260907T2020
task_id: T-P5-041
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-07T20:04:00-06:00
created_at: 2026-09-07T20:20:00-06:00
inspected_commit: 06ef9ccc4aa6055a6a3bd7d6f0a5bb9055220f47
claim_commit: 176a30a210d37344905c1a74760afbdf8288267b
inspected_paths:
  - agent_review_inbox/review-T-P5-022-liuguanyi-20260907T0820.md
  - agent_review_inbox/review-T-P5-037-honglianmozun-20260907T1856.md
  - agent_review_inbox/review-T-P5-040-honglianmozun-20260907T1950.md
source_hashes:
  review-T-P5-022: b52b7a9c9026cae0bbead03bf87682447f3276c4
  review-T-P5-037: 04a873d968bac4832de40f2890cc2fd1e73077a0
  review-T-P5-040: 80f950d571eb6124e6fb7df819f50d2eab67f1ea
continuation_of:
  - review-T-P5-022-liuguanyi-20260907T0820
  - review-T-P5-028-liuguanyi-20260907T1112
related_tasks:
  - T-P5-023
  - T-P5-028
  - T-P5-039
  - T-P5-040
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_the_energy_diagonal_coordinate_bridge_and_preserve_transformed_signed_Jacobian_or_component_UX_rows_before_absolute_scalarization; feed_only_the_resulting_rho_i_B_i_to_T-P5-040_or_zero-rho_E_i_to_T-P5-039
---

# T-P5-041 — exact `u=x+y` energy diagonalization and `K_path -> mixed relative/additive` source bridge

## 0. Result

The newest P5 consumer `T-P5-040` asks for componentwise mixed residual contracts

```text
|l4| <= rho4*|u4| + bias4,
|l5| <= rho5*|u5| + bias5,
```

with `u=x+y`, positive remaining quadratic reserves, and square budgets on the additive terms.  The older source lane `T-P5-022/023/028` naturally emits component transport rows in the original consumer coordinates

```text
z = (x4,x5,y4,y5).
```

The missing mathematical bridge is not another Young inequality.  It is the coordinate identity hidden in the frozen Lyapunov function itself.

For the exact `V` used by `T-P5-037/T-P5-040`, define

```text
u := x+y,
H := K + D - M.
```

Then the storage diagonalizes exactly as

```text
V(x,y) = (1/2) u^T M u + (1/2) x^T H x.                (0.1)
```

Thus `(u4,u5)` are precisely the residual-power coordinates and `x` is a transverse coordinate orthogonal to them in the energy metric.  This makes it possible to transport one component source row into a relative coefficient `rho_i` plus an exact rational additive **square budget** on every `V<=Vstar` sublevel.

The bridge has two source frontends:

1. **legacy nonnegative `K_path` fallback**: an `(x,y)` absolute row is safely converted to a `(u,x)` row by `r=q`, `t=p+q`;
2. **preferred signed-Jacobian frontend**: transform the signed Jacobian first,

```text
(J_x,J_y) -> (J_u,J_xtrans) = (J_y, J_x-J_y),          (0.2)
```

and only then take interval/absolute caps.  This preserves exact `x+y` cancellation that an entrywise-absolute `K_path` irreversibly loses.

This child stops at the source-to-math contract.  It does not redo the T-P5-040 energy absorption or T-P5-039 optimizer.

---

## 1. Frozen storage and exact coordinate identity

Use the exact forms frozen in T-P5-037:

```text
M = diag(m4,m5)

m4 = 350003/3000000,
m5 = 200739/4000000,

D = diag(4/5,13/20),

K = [[3/4,    -3/400],
     [-3/400, 29/50]].
```

The storage is

```text
V
 := (1/2)y^T M y
  + (1/2)x^T K x
  + x^T M y
  + (1/2)x^T D x.                                      (1.1)
```

Set `u=x+y`, hence `y=u-x`.  The `M` part satisfies

```text
(1/2)(u-x)^T M (u-x) + x^T M (u-x)
 = (1/2)u^T M u - (1/2)x^T M x.                        (1.2)
```

Therefore

```text
V
 = (1/2)u^T M u
   + (1/2)x^T(K+D-M)x
 = (1/2)u^T M u + (1/2)x^T Hx.                         (1.3)
```

For this concrete system,

```text
H = [[4299997/3000000,  -3/400],
     [-3/400,            4719261/4000000]].             (1.4)
```

Its determinant is

```text
det(H) = 6764044380739/4000000000000 > 0,              (1.5)
```

and both diagonal entries are positive, so `H` is positive definite.

The inverse is exact rational:

```text
H^{-1}
 = 1/20292133142217
   * [[14157783000000,    90000000000],
      [   90000000000, 17199988000000]].                (1.6)
```

In particular every entry of `H^{-1}` is positive.

This identity is stronger for the present interface than the earlier Euclidean coercivity `||z||^2 <= (125/3)V`: it exposes exactly which direction is the residual-power coordinate and which directions should be charged as transverse bias.

---

## 2. Exact energy-dual square bound in `(u,x)` coordinates

Let

```text
d4,d5,t4,t5 >= 0
```

and define the nonnegative linear envelope

```text
B(u,x)
 := d4*|u4| + d5*|u5| + t4*|x4| + t5*|x5|.             (2.1)
```

Define

```text
C(d,t)
 := d4^2/m4 + d5^2/m5 + t^T H^{-1} t.                  (2.2)
```

Then

```text
B(u,x)^2 <= 2 V(x,y) * C(d,t).                          (2.3)
```

### Proof

For the current signs of `u4,u5,x4,x5`, write the left side before squaring as a linear functional of `(u,x)`.  The energy matrix in (1.3) is block diagonal, `diag(M,H)`, up to the factor `1/2`.  Weighted Cauchy gives

```text
B^2
 <= [u^T M u + x^T Hx]
    * [d4^2/m4 + d5^2/m5 + s_x^T H^{-1}s_x],           (2.4)
```

where `s_x=(sigma4*t4,sigma5*t5)` and each `sigma_i` is a sign.

Because every entry of `H^{-1}` is nonnegative,

```text
s_x^T H^{-1}s_x <= t^T H^{-1}t.                        (2.5)
```

Finally `u^TMu+x^THx=2V`, proving (2.3).

No square root is required by the theorem statement or by a checker.  The exact transverse dual term is

```text
t^T H^{-1} t
 = [14157783000000*t4^2
    +180000000000*t4*t5
    +17199988000000*t5^2]
   /20292133142217.                                     (2.6)
```

A Lean implementation can avoid matrix inverse APIs entirely.  For a symmetric `2x2` matrix `[[a,h],[h,b]]`, the exact adjugate identity

```text
(a*x1^2 + 2*h*x1*x2 + b*x2^2)
*(b*d1^2 - 2*h*d1*d2 + a*d2^2)
-(a*b-h^2)*(d1*x1+d2*x2)^2
 = (a*d2*x1 - b*d1*x2 - d1*h*x1 + d2*h*x2)^2           (2.7)
```

proves the required two-dimensional weighted Cauchy step by one square.

---

## 3. Core source contract: a `(u,x)` component row -> T-P5-040 data

Suppose a source checker proves, on the same domain as the Lyapunov consumer, one residual component bound

```text
|l_a|
 <= r4*|u4| + r5*|u5| + t4*|x4| + t5*|x5|,             (3.1)
```

with all coefficients nonnegative.

Choose a target channel `i in {4,5}` and let `j` be the other channel.  Choose any rational relative charge

```text
0 <= rho_i <= r_i.                                      (3.2)
```

Define

```text
delta_i := r_i-rho_i >= 0,                              (3.3)

beta_i(u,x)
 := delta_i*|u_i|
    + r_j*|u_j|
    + t4*|x4| + t5*|x5|.                               (3.4)
```

Then pointwise

```text
|l_a| <= rho_i*|u_i| + beta_i(u,x).                     (3.5)
```

By Section 2,

```text
beta_i(u,x)^2 <= 2V * C_i(rho_i),                       (3.6)
```

where

```text
C_4(rho4)
 = (r4-rho4)^2/m4 + r5^2/m5 + t^T H^{-1}t,             (3.7)

C_5(rho5)
 = r4^2/m4 + (r5-rho5)^2/m5 + t^T H^{-1}t.             (3.8)
```

Hence on a sublevel

```text
V <= Vstar,                                             (3.9)
```

we have the uniform square budgets

```text
beta_4^2 <= B4(rho4) := 2*Vstar*C_4(rho4),              (3.10)

beta_5^2 <= B5(rho5) := 2*Vstar*C_5(rho5).              (3.11)
```

This is exactly the source-side information T-P5-040 needs.  Its proof never requires the additive witness called `b_i` there to be a state-independent constant; it only uses a pointwise nonnegative witness and a uniform bound on its square.  Indeed

```text
-t_i*u_i^2 + beta_i(z)*|u_i|
 <= beta_i(z)^2/(4*t_i)
 <= B_i/(4*t_i).                                        (3.12)
```

So the source-facing typed contract should preferably store

```text
rho_i,
B_i,
Vstar,
coordinate_tag = block45_u_x,
```

rather than inventing an irrational constant `sqrt(B_i)`.

For the current quarter barrier `Vstar=1/4`, these become

```text
B4(rho4)
 = (1/2)*[
     (3000000/350003)*(r4-rho4)^2
    +(4000000/200739)*r5^2
    +t^T H^{-1}t],                                      (3.13)

B5(rho5)
 = (1/2)*[
     (3000000/350003)*r4^2
    +(4000000/200739)*(r5-rho5)^2
    +t^T H^{-1}t].                                      (3.14)
```

Every quantity is rational whenever the component row and `rho_i` are rational.

---

## 4. Legacy `K_path` fallback

The current T-P5-022/023 lane naturally produces a nonnegative row in the original coordinate order

```text
|l_a|
 <= p4*|x4| + p5*|x5| + q4*|y4| + q5*|y5|.             (4.1)
```

Since `y=u-x`,

```text
|y_k| <= |u_k|+|x_k|.                                   (4.2)
```

Therefore (4.1) implies (3.1) with the exact safe map

```text
r4 = q4,
r5 = q5,
t4 = p4+q4,
t5 = p5+q5.                                             (4.3)
```

Thus every existing nonnegative `K_path` row already has a deterministic route into T-P5-040:

```text
K_path row in (x4,x5,y4,y5)
 -> (r4,r5,t4,t5) via (4.3)
 -> choose rho_i
 -> B_i(rho_i) via (3.10)/(3.11)
 -> T-P5-040 reserve/gate.                              (4.4)
```

For the two residual rows, use their own coefficients independently.  In particular, if the row for `l4` is `K[4,*]`, compute `(rho4,B4)` from that row; if the row for `l5` is `K[5,*]`, compute `(rho5,B5)` from that row.

At `rho4=rho5=0`, this bridge gives pure additive component square caps `E4=B4(0)`, `E5=B5(0)`, which can be fed directly into the already formalized T-P5-039 exact Pareto optimizer.  Therefore the same source object supports both lanes:

```text
rho=0       -> T-P5-039 additive Pareto optimizer,
0<rho<reserve -> T-P5-040 mixed relative/additive consumer.              (4.5)
```

No new scalar Frobenius collapse is required.

---

## 5. Preferred source lane: transform the signed Jacobian before taking absolute values

The fallback (4.3) is safe but can destroy the exact cancellation that makes a residual relative to `u_i=x_i+y_i`.

Let one source residual component have signed Jacobian row, in `(x,y)` coordinates,

```text
J = (J_x,J_y).                                           (5.1)
```

Under the exact coordinate map

```text
(x,y) = (x,u-x),                                        (5.2)
```

the chain rule gives

```text
J_u       = J_y,
J_xtrans  = J_x-J_y.                                    (5.3)
```

Equivalently,

```text
J_x dx + J_y dy
 = J_y du + (J_x-J_y) dx.                               (5.4)
```

This is the source-to-math Jacobian adapter that should be applied **before** entrywise absolute values.

If a cell/segment checker can certify interval magnitudes

```text
|J_y,4|          <= r4,
|J_y,5|          <= r5,
|J_x,4-J_y,4|    <= t4,
|J_x,5-J_y,5|    <= t5,                                (5.5)
```

then FTOC immediately produces the `(u,x)` row (3.1), and Section 3 applies.

This can be strictly stronger than first constructing the old nonnegative row, because

```text
|J_x-J_y|
```

may be much smaller than

```text
|J_x|+|J_y|.                                             (5.6)
```

The same principle applies cell-by-cell in T-P5-023: transform each signed/interval Jacobian block into `(u,x)` coordinates before absolute enclosure and cell-chain aggregation.  Cancellation across unrelated cells is not assumed; only the exact coordinate cancellation inside each derivative block is preserved.

---

## 6. Exact information-loss example: absolute `K_path` cannot recover a pure `u` residual

Take the simple exact residual

```text
l4 = alpha*(x4+y4) = alpha*u4,
alpha > 0.                                              (6.1)
```

Its signed Jacobian satisfies

```text
J_x,4 = alpha,
J_y,4 = alpha.                                          (6.2)
```

The preferred transform (5.3) gives

```text
J_u,4      = alpha,
J_xtrans,4 = 0.                                         (6.3)
```

Hence the exact mixed contract is

```text
|l4| <= alpha*|u4|,
B4 = 0.                                                 (6.4)
```

By contrast, if one first takes entrywise absolute values in `(x,y)`, the legacy row is

```text
(p4,q4)=(alpha,alpha).                                  (6.5)
```

The fallback (4.3) gives

```text
r4=alpha,
t4=2*alpha,                                             (6.6)
```

so even when choosing `rho4=alpha`, the produced additive square budget is strictly positive on every nontrivial `Vstar>0`:

```text
B4 = 2*Vstar*(2*alpha)^2*(H^{-1})_44 > 0.               (6.7)
```

Thus an entrywise-absolute `K_path` has irreversibly forgotten the equality of the two signed derivatives.  This is not a weakness of T-P5-040; it is an information-loss boundary in the source interface.

Consequently:

- if the mixed/bias lane is sufficient, the old `K_path` fallback is valid;
- if a small or zero additive budget is important, the source checker must preserve signed Jacobian intervals, paired derivative information, or a direct `(u,x)` component row before absolute scalarization.

A generic operator/Frobenius norm cannot reconstruct this cancellation after it has been erased.

---

## 7. Relative/additive tradeoff is explicit and rational

For a fixed `(u,x)` row, the only `rho_i`-dependent part of `B_i` is

```text
2*Vstar*(r_i-rho_i)^2/m_i.                              (7.1)
```

Therefore for

```text
0 <= rho1 <= rho2 <= r_i,
```

one has

```text
B_i(rho1)-B_i(rho2)
 = (2*Vstar/m_i)
   *[(r_i-rho1)^2-(r_i-rho2)^2]
 >= 0.                                                   (7.2)
```

Increasing the relative charge monotonically decreases the additive square budget, but T-P5-040 simultaneously requires

```text
rho4 < a4(r),
rho5 < 1/6.                                             (7.3)
```

So the source/consumer interface now exposes the real Pareto tradeoff instead of hiding it inside a scalar residual norm.

I do not optimize this new `rho` tradeoff here; that would overlap the energy/optimizer lane.  A checker may simply emit rational candidate `rho4,rho5` and let the exact T-P5-040 polynomial gate decide feasibility.

---

## 8. Direct composition with the current T-P5-040 gate

For each residual row, compute `B4(rho4)` and `B5(rho5)` as above.  For the Pareto energy parameter `0<=r<=1`, T-P5-040 defines

```text
A4 := 250 + 53*r - 1500*rho4,
A5 := 1 - 6*rho5.                                      (8.1)
```

If

```text
A4 > 0,
A5 > 0,                                                 (8.2)
```

then the complete source-facing quarter-barrier test becomes the exact rational inequality

```text
300000*B4(rho4)*A5
+ 1200*B5(rho5)*A4
< (109-r)*A4*A5.                                        (8.3)
```

Thus the new deterministic lane is

```text
source Jacobian / K_path
 -> exact `(u,x)` row
 -> exact energy-dual square budget `(rho_i,B_i)`
 -> T-P5-040 polynomial gate.                           (8.4)
```

This closes a mathematical interface that was previously implicit.  It still does not supply any concrete deployed Jacobian interval.

---

## 9. Centered residual versus full residual: anchor must remain typed

T-P5-022's `K_path` is naturally a **centered** residual transport.  If the one-trajectory residual used by T-P5-040 is

```text
l_i = l_centered,i + a_i,                               (9.1)
```

then the centered bridge above is not by itself a proof of the full contract.

The earlier T-P5-022 anchor adapter already forms component boxes before collapsing them to the scalar

```text
B2 = C4^2+C5^2.                                         (9.2)
```

For the anisotropic T-P5-040 lane, the source checker should preserve the individual `C4,C5`; do not discard them after forming `B2`.

If

```text
beta_centered,i^2 <= Bc_i,
|a_i| <= C_i,                                           (9.3)
```

then for any rational `theta_i>0`, the full additive witness satisfies the square bound

```text
(beta_centered,i + C_i)^2
 <= (1+theta_i)*Bc_i + (1+1/theta_i)*C_i^2.             (9.4)
```

Hence a safe full-residual budget is

```text
Bfull_i(theta_i)
 := (1+theta_i)*Bc_i + (1+1/theta_i)*C_i^2.             (9.5)
```

This is only a merge adapter.  If source evidence gives signed correlation between the centered term and the anchor, a tighter direct component bound may replace it.  What is forbidden is silently treating a centered `K_path` as a full one-trajectory residual row.

The same one-time normalization rule from T-P5-022 remains in force: the residual row and anchor must already be in the generalized-force coordinates used by `V'=-Q-u^T l`, or the raw-PMI force map must be applied exactly once.

---

## 10. Minimal theorem surface

The mathematical core can be formalized without ODE, source, matrix-spectrum, or optimizer APIs.

### `block45_storage_ux_diagonalization`

For the frozen `M,K,D`, with `u=x+y`, prove

```text
V x y = (1/2)*(u^T M u + x^T H x),
H=K+D-M.                                                (10.1)
```

This is a `ring` identity.

### `block45_transverse_dual_square_bound`

For nonnegative `d4,d5,t4,t5`, prove (2.3), preferably using the explicit rational `H^{-1}` or the adjugate square identity (2.7).

### `ux_component_row_to_mixed_square_budget`

Consume (3.1), `0<=rho_i<=r_i`, and `V<=Vstar`; produce the pointwise mixed envelope (3.5) and square budget (3.10)/(3.11).

### `xy_absolute_row_to_ux_row`

Pure triangle theorem implementing

```text
(p4,p5,q4,q5) -> (q4,q5,p4+q4,p5+q5).                  (10.2)
```

### `signed_jacobian_to_ux_jacobian`

Pure linear coordinate theorem implementing

```text
(J_x,J_y) -> (J_y,J_x-J_y).                             (10.3)
```

### Negative-control regression

Formalize the family `l=alpha*(x_i+y_i)` to show:

- signed transform has zero transverse coefficient;
- legacy absolute transform has positive transverse coefficient for `alpha>0`.

This prevents a future source refactor from accidentally claiming that absolute `K_path` preserves cancellation.

A small optional theorem can expose (9.4) for componentwise centered-plus-anchor merging; it should stay separate from the core centered-row bridge.

---

## 11. Dependencies and open boundaries

Mathematical dependencies only:

- T-P5-022/023: source/FTOC component transport semantics;
- T-P5-028: moving-frame/source-coordinate identity and common-parameter boundary;
- T-P5-037: frozen `V`, `M`, `K`, `D` and exact moving-frame power identity;
- T-P5-040: downstream mixed relative-plus-additive consumer;
- T-P5-039: optional `rho=0` additive Pareto consumer.

This review proves only the interface mathematics above.  It does **not** prove:

- a concrete Julia/Float64 Jacobian or signed interval row;
- that the deployed source preserves paired `J_x,J_y` information;
- anchor/source values `C4,C5` on a real first-exit domain;
- common-`c` or parameter-mismatch physical binding beyond the already stated T-P5-028 premises;
- controller/solve/finite-difference remainder bounds;
- trajectory, cell-chain, ODE, or P8 coverage;
- Lean compilation, `#print axioms`, comparator, provenance/admission, P5/P8/M4 closure, or registry promotion.

The most important source-interface recommendation is narrow: **perform the exact `(x,y)->(u,x)` signed Jacobian transform before entrywise absolute enclosure whenever relative residual structure matters.**  Existing `K_path` remains a safe fallback, but it cannot recover cancellation after absolute values have erased it.

**Status: pending mathematical/interface child — 待封不觉独立验证 / 待梁智炜最终整合。**
