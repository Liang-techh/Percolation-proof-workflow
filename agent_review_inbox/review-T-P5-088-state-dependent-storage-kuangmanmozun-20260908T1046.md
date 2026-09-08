---
kind: review_result
review_id: review-T-P5-088-state-dependent-storage-kuangmanmozun-20260908T1046
reviewed_claim: claim-T-P5-088-state-dependent-storage-kuangmanmozun-20260908T1029.md
task_id: T-P5-088-STATE-DEPENDENT-STORAGE-DERIVATIVE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
reviewer: 狂蛮魔尊
created_at: 2026-09-08T10:46:00-06:00
claim_commit: a30a8f5c96be386736f665d0627e95f05f781294
inspected_upstream:
  - 6f96c363348d39ac218b07ba30f5011edbe70314
  - 984fb7d4a75c019a7e40fe542ac67141efcc0804
status: CONDITIONAL_PASS
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
summary: >-
  Close the state/time-dependent Lyapunov-storage derivative gap explicitly left
  by T-P5-087. For V(t,y)=y^T W(t,y)y and actual dynamics ydot=-G+e, the exact
  derivative contains both the material metric term y^T(W_t-DW[G])y and an
  additional defect-metric coupling y^T DW[e] y. The entire defect contribution
  equals e dot grad_y V, so a checker that charges only 2<y,e>_W is unsound when
  W depends on state. One-sided relative/additive packets give an exact decay /
  first-exit gate, while gamma W-(W_t-DW[G]) PSD gives a division-free matrix
  certificate. A rational counterexample shows that even W_t=0 and uniformly
  positive W can have true Vdot>0 where the frozen-metric term predicts Vdot<0.
---

# T-P5-088 — state-dependent quadratic storage: exact material derivative and closure gate

## 0. Why this child is needed

T-P5-086 and T-P5-087 handle a metric used to **measure an Euler defect**. In
T-P5-087 the endpoint/path metric may move, but the quadratic form is held fixed
at the moment where Jensen/Cauchy is applied. That review explicitly leaves open
the different situation in which the Lyapunov storage itself is

`V(t,y) = y^T W(t,y) y`.

In that case `W_t` and `D_y W[ydot]` enter the derivative of the storage. They are
not optional comparator losses. This child gives the exact identity, a minimal
one-sided closure, a source-friendly rational matrix gate, and exact
counterexamples against the two most dangerous shortcuts.

This is a mathematics/interface result only. No deployed P5 source packet,
Float64/controller semantics, P8 coverage, Lean/kernel receipt, provenance,
admission, or registry update is claimed.

---

## 1. Exact material derivative identity

Let `W(t,y)` be a `C^1` symmetric matrix field on a spacetime cell and define

`V(t,y) := y^T W(t,y) y`.

For a direction `v`, write

`D_y W(t,y)[v] := sum_k v_k partial_{y_k} W(t,y)`.

Let the actual dynamics be

**(1.1)** `ydot = f(t,y)`.

Then the chain rule gives the exact identity

**(1.2)**

`Vdot`
` = 2 y^T W f`
`   + y^T (W_t + D_y W[f]) y`.

Define the material metric derivative along `f`

**(1.3)** `B_f := W_t + D_y W[f]`.

Then

**(1.4)** `Vdot = 2 <y,f>_W + y^T B_f y`.

Nothing here is an estimate. In particular, replacing `B_f` by `W_t` is valid
only when `D_yW[f]=0` has separately been proved.

### Minimal formal statement

A Lean-facing theorem can be stated first for a differentiable matrix-valued map
and a differentiable trajectory, then specialized to a vector field:

`quadStorage_deriv = 2 * dot y (W * ydot) + dot y ((Wdot) * y)`

with `Wdot = W_t + D_yW[ydot]` supplied by the ordinary chain rule.

---

## 2. Exact nominal + defect split

Write the actual dynamics in the P5-style form

**(2.1)** `ydot = -G(t,y) + e(t,y)`.

Because `D_yW[.]` is linear in its direction argument,

`B_f = W_t - D_yW[G] + D_yW[e]`.

Hence (1.2) becomes

**(2.2)**

`Vdot`
` = [-2 <y,G>_W + y^T (W_t - D_yW[G]) y]`
`   + [ 2 <y,e>_W + y^T D_yW[e] y ]`.

Define

**(2.3) nominal storage charge**

`N_W := -2 <y,G>_W + y^T (W_t - D_yW[G]) y`,

and

**(2.4) defect storage charge**

`E_W := 2 <y,e>_W + y^T D_yW[e] y`.

Then simply

**(2.5)** `Vdot = N_W + E_W`.

This is the correct split if a state-dependent metric is used as the storage.
The second term in (2.4) must not be dropped or double-counted elsewhere.

---

## 3. The defect couples to the full storage gradient

There is a useful exact compression of (2.4). Define the vector `g_W(t,y)` by

**(3.1)** `(g_W)_k := y^T (partial_{y_k} W) y`.

Since `W` is symmetric,

**(3.2)** `grad_y V = 2 W y + g_W`.

Therefore

**(3.3)**

`E_W = e dot grad_y V`.

So for a state-dependent storage the residual/evaluator/controller defect does
**not** couple merely to `2Wy`; it couples to the entire gradient of the storage.
This is the source-level object that should be formed before taking absolute
values or interval envelopes.

This also gives a direct handoff to the correlation-aware P5 lane: if source CSE
can prove a favorable signed bound on `e dot grad V`, consume that signed scalar
packet directly. Do not separately absolute-bound `2<y,e>_W` and
`y^T D_yW[e]y` unless no correlated source theorem is available.

---

## 4. Minimal one-sided relative/additive closure

Assume on the same certified spacetime cell that

**(4.1) nominal packet**

`N_W <= -c V - D`,

with `c>=0`, `D>=0`, and

**(4.2) defect packet**

`E_W <= alpha V + beta`,

with `alpha>=0`, `beta>=0`.

Then by (2.5)

**(4.3)**

`Vdot <= -(c-alpha) V - D + beta`.

Thus:

- homogeneous strict decay needs **`alpha < c`** and `beta=0`;
- a first-exit barrier `V=Vstar` is strictly inward whenever

**(4.4)** `beta < (c-alpha) Vstar`,

assuming `alpha<c` and `D>=0`.

No division or square root is needed.

The strict rate condition is information-level sharp. With constant scalar
`W=1`, choose `G=(c/2)y` and `e=(alpha/2)y`. Then

`Vdot = -(c-alpha)V`.

At `alpha=c` the storage is exactly constant, and for `alpha>c` it grows. Hence a
checker cannot upgrade the equality boundary to strict decay from only
(4.1)-(4.2).

### Source-friendly split of the nominal packet

Often source gives the two nominal pieces separately. If

**(4.5)** `2 <y,G>_W >= d V + D`,

and

**(4.6)** `y^T (W_t-D_yW[G]) y <= gamma V + b0`,

then with the defect packet (4.2),

**(4.7)**

`Vdot <= -(d-gamma-alpha)V - D + (b0+beta)`.

Therefore the exact scalar gate is

**(4.8)** `gamma + alpha < d`,

and for a candidate first-exit level

**(4.9)** `b0 + beta < (d-gamma-alpha) Vstar`.

Again, only addition, multiplication, and order are required.

---

## 5. Division-free matrix certificate for the moving-storage charge

Let

**(5.1)** `B_G := W_t - D_yW[G]`.

To certify the purely relative bound

`y^T B_G y <= gamma y^T W y`

for every vector in the cell, it is enough to prove the pointwise PSD statement

**(5.2)** `C := gamma W - B_G >= 0`.

This is stronger and cleaner than separately bounding `W_t` and `D_yW[G]`,
because their signed cancellation is preserved in `B_G` before enclosure.

A rational source/checker can reuse the same diagonal-dominance pattern as
T-P5-087. If for every source point:

- `C` is symmetric;
- `|C_ij| <= c_ij` for `i != j`, with `c_ij=c_ji>=0`;
- `C_ii >= sum_{j != i} c_ij`,

then `C` is PSD and (5.2) follows by

`2 c_ij |v_i v_j| <= c_ij(v_i^2+v_j^2)`.

No eigenvalue, inverse, square root, or floating generalized-eigenvalue estimate
is required by the trusted consumer.

### Coercivity fallback

If source instead has

**(5.3)** `m ||v||^2 <= v^T W v`, `m>0`,

and a one-sided Euclidean packet

**(5.4)** `v^T B_G v <= b ||v||^2`,

then any rational `gamma>=0` satisfying

**(5.5)** `b <= gamma m`

implies

`v^T B_G v <= gamma v^T W v`.

This avoids the explicit quotient `b/m`.

---

## 6. Exact counterexample: `W_t=0` is not enough

A time-independent metric can still contribute a decisive material derivative if
it depends on state.

Take the one-dimensional cell `0 <= y <= 3/4`,

**(6.1)** `W(y)=1-y`,

so `W>=1/4>0` on the whole cell, and take the stable-looking dynamics

**(6.2)** `ydot=-y`, i.e. `G=y`, `e=0`.

The storage is

`V=(1-y)y^2`.

If one incorrectly freezes the metric and keeps only the ordinary quadratic
pairing, one predicts

**(6.3)**

`Vdot_frozen = -2(1-y)y^2 < 0`

for every nonzero `y` in the cell.

But `W_t=0` and `D_yW[G]=(-1)y=-y`, hence

`B_G = W_t-D_yW[G]=y`.

The **true** derivative is

**(6.4)**

`Vdot = -2(1-y)y^2 + y^3`
`     = -2y^2 + 3y^3`.

At the exact rational point `y=3/4`,

`V = 9/64`,

`Vdot_frozen = -9/32`,

but

**(6.5)** `Vdot = 9/64 > 0`.

So omitting `D_yW[ydot]` does not merely loosen a constant; it can reverse the
sign of the Lyapunov derivative while `W` remains uniformly positive definite
and `W_t` is identically zero.

This is a strict mathematical obstruction to treating state-dependent storage as
T-P5-087's moving defect-measurement metric.

---

## 7. Exact counterexample: defect pairing `2<y,e>_W` alone is incomplete

The missing `D_yW[e]` term can also change the sign of the defect contribution.
An especially clean two-dimensional example makes the ordinary weighted pairing
vanish exactly.

Let

**(7.1)** `W(y) = (1+y_1) I`

on the slab `-1/2 <= y_1 <= 1/2`, so `W>= (1/2)I`. At the state

**(7.2)** `y=(0,1)`

and defect direction

**(7.3)** `e=(1,0)`,

we have

`2<y,e>_W = 0`.

However,

`D_yW[e] = I`,

so

**(7.4)** `y^T D_yW[e] y = 1`.

Hence

**(7.5)** `E_W = e dot grad V = 1`.

A checker that sees zero ordinary pairing and therefore charges zero defect would
be unsound. The full storage-gradient pairing (3.3) is the correct object.

---

## 8. Square-packet fallback for additive defects; no sqrt

If source cannot prove a signed linear bound (4.2), a useful fallback is to form
the **whole** defect charge `P:=E_W=e dot grad V` and prove the squared packet

**(8.1)** `P^2 <= H V`,

with `H>=0`.

Choose rational bookkeeping charges `alpha,beta>=0` satisfying

**(8.2)** `H <= 4 alpha beta`.

Then

**(8.3)** `P <= alpha V + beta`.

Indeed,

`P^2 <= H V <= 4 alpha beta V`,

while

`(alpha V + beta)^2 - 4 alpha beta V`
` = (alpha V-beta)^2 >=0`.

Since `alpha V+beta>=0`, (8.3) follows without square roots.

The factor `4` is sharp from only (8.1): equality is attained whenever
`P=2 sqrt(alpha beta V)` and `alpha V=beta`. A concrete trusted checker does not
need to form that square root; the example only establishes information-level
sharpness.

A useful obstruction follows immediately. If `beta=0`, gate (8.2) forces `H=0`.
Thus a generic `P^2<=H V` packet with `H>0` cannot by itself produce a purely
relative linear charge `P<=alpha V` near `V=0`. This is exactly the expected
`O(sqrt(V))` behavior of a persistent additive vector-field defect. To obtain a
homogeneous rate branch, source must prove stronger vanishing/correlation, e.g.
`P<=alpha V` directly or `P^2<=H V^2`.

This fallback should feed the existing additive/bias first-exit machinery rather
than be disguised as pure relative decay.

---

## 9. Correlation rule: form the material/Lie derivative first

There are two places where premature absolute values lose real reserve:

1. nominal metric motion:

`B_G = W_t - D_yW[G]`;

2. defect coupling:

`E_W = 2<y,e>_W + y^T D_yW[e]y = e dot grad V`.

The source order should therefore be

`signed W_t, D_yW, G, e`
` -> form B_G and/or E_W exactly`
` -> form the consumer quadratic/scalar quantity`
` -> only then interval/rational enclosure`.

Absolute-bounding `W_t`, `D_yW[G]`, `2<y,e>_W`, and `D_yW[e]` independently is a
safe fallback but may destroy exact cancellations. This is the same structural
lesson as T-P5-076/T-P5-080/T-P5-086: correlation belongs upstream of norm or
interval collapse.

---

## 10. Relation to moving charts and to T-P5-087

T-P5-087 proves a comparison theorem for a metric used to measure an integrated
Euler defect. That theorem remains valid and is not modified here.

If the **storage** itself uses `W(t,y)`, however, then its evolution must use
(1.2). A path metric comparator does not imply a material-derivative bound and
cannot replace (5.2).

Conversely, a material-derivative theorem does not by itself compare the metrics
used to measure a finite Euler defect. The two obligations are logically
separate:

- T-P5-087: finite-defect metric transport/comparison;
- T-P5-088: derivative of the moving storage itself.

If `W` is an exact pullback/transported metric generated by a moving chart, some
connection terms may cancel, as in the affine special case of T-P5-081. Such a
cancellation must be established by the exact pullback identity; it should then
be reflected as a sharp bound on `B_G` rather than assumed from coordinate
intuition.

---

## 11. Suggested minimal Lean decomposition

A small formalization can be split into:

1. `quad_storage_material_derivative`
   - exact chain-rule identity (1.2);
2. `quad_storage_nominal_defect_split`
   - algebraic split (2.2);
3. `state_metric_defect_eq_grad_pair`
   - identity (3.3);
4. `moving_storage_relative_additive_decay`
   - ordered-ring closure (4.3);
5. `moving_storage_first_exit_gate`
   - scalar gate (4.4)/(4.9);
6. `material_metric_rel_of_psd_gap`
   - `gamma W-B_G >=0 -> y^T B_G y <= gamma V`;
7. `material_metric_rel_of_coercive_euclid`
   - division-free fallback (5.3)-(5.5);
8. `full_gradient_defect_absorption_sq`
   - square identity (8.1)-(8.3);
9. two exact regression examples from Sections 6 and 7.

The matrix diagonal-dominance helper can reuse the theorem shape already proposed
in T-P5-087 rather than creating a competing implementation.

---

## 12. Source handoff and remaining obligations

For an actual P5 cell, the most useful source packet is now:

- exact storage matrix `W(t,y)` and storage domain;
- proof that `W` is symmetric and coercive on that domain;
- exact or CSE representation of `B_G=W_t-D_yW[G]` **before** absolute enclosure;
- either a direct PSD gap `gamma W-B_G>=0`, or rational data sufficient for the
  diagonal-dominance/coercivity fallback;
- actual defect field `e` and the whole signed scalar
  `E_W=e dot grad_y V`;
- either a direct one-sided `E_W<=alpha V+beta` packet or the squared fallback
  `E_W^2<=H V`;
- same-cell coverage for all of the above.

Still open and explicitly not claimed here:

- deployed source identity for `W`, `G`, or `e`;
- rational enclosure values `c,d,gamma,b0,alpha,beta,H` for the real P5 domain;
- moving-chart pullback/source semantics beyond the already separated P5
  children;
- Float64/FD/controller/solve semantics;
- P8/ODE path or invariant-set coverage;
- Lean/kernel compilation and independent verification by 封不觉;
- provenance, receipt, comparator, admission, registry, or P5/P8/M4 parent
  closure.

Status remains **pending mathematical child / conditional pass** until those
source and formal obligations are supplied.