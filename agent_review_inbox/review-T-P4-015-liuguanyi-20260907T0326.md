---
kind: review_result
review_id: review-T-P4-015-liuguanyi-20260907T0326
task_id: T-P4-015
source_agent: 柳冠一
claimed_at: 2026-09-07T03:10:00-06:00
created_at: 2026-09-07T03:26:00-06:00
inspected_commit: f11d818d82565db494d8d01e1daba4d03dab463d
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_slice_increment_bridge_then_bind_each_execution_remainder_by_direct_increment_or_smooth_derivative_witness
---

# T-P4-015 — slice-Lipschitz transport from execution remainders to the P4 Schur reserves

## Scope

`T-P4-007` decomposed the real-lift execution residual into semantically distinct pieces, including centered gravity mismatch, controller/runtime mismatch and solve defect. `T-P4-014` then gave the sharp consumer once a remainder is already known to be either same-coordinate relative or transverse-relative. The missing interface mathematics is the bridge between those two statements:

> What source-side mathematical contract is actually sufficient to turn a centered execution term into a same-coordinate term plus a transverse term carrying an existing quadratic reserve?

The answer is a slice decomposition plus one-dimensional transport. It also separates three notions that must not be conflated:

1. `R(0,0)=0` (centering only at the full reference state),
2. `R(0,z)=0` for every transverse state `z` (vanishing on the whole `q_cross=0` slice),
3. a quantitative increment/Lipschitz bound along the slice.

Only (2)+(3), or (1)+(3) plus an independently charged transverse base slice, can justify a relative envelope.

Inputs used:

- `review-T-P4-007-liuguanyi-20260907T0212.md` and its compiled algebra follow-up `review-T-P4-007-juyangxianzun-20260907T0245.md`;
- `review-T-P4-013-kuangmanmozun-20260907T0145.md` for the normalized `kc` same-coordinate budget;
- `review-T-P4-014-kuangmanmozun-20260907T0247.md` for the sharp relative-plus-transverse Schur consumer;
- `review-T-P5-012-honglianmozun-20260907T0304.md` only to keep the P5 conservative-force routing distinct from this P4 residual routing.

No IEEE/source numerical bound, validation, provenance, P4/M4 closure or registry admission is asserted.

## 1. Exact slice decomposition

For one P4 channel, split the typed state into

```text
y : the scalar Schur/cross coordinate,
z : all other coordinates that may carry a positive quadratic reserve.
```

Let `R(y,z)` be one scalar execution remainder and let the reference be `(0,0)`. The identity

```text
R(y,z)-R(0,0)
 = [R(y,z)-R(0,z)] + [R(0,z)-R(0,0)]                       (1)
```

is exact.

Define

```text
R0       := R(0,0),
R_y      := R(y,z)-R(0,z),
R_trans  := R(0,z)-R(0,0).                                 (2)
```

Then

```text
R(y,z) = R0 + R_y + R_trans.                               (3)
```

This is the correct routing adapter for the execution terms in `T-P4-007`:

- `R0` is a genuine reference bias;
- `R_y` is the candidate same-coordinate relative part;
- `R_trans` is the candidate transverse-reserve part.

The split is semantic, not numerical, and does not change units or coordinates.

## 2. Same-coordinate transport lemma

Fix `z`. Suppose the one-variable map

```text
f_z(s) := R(s,z)
```

is differentiable on the segment joining `0` and `y`, and

```text
|f_z'(s)| <= beta                                             (4)
```

throughout that segment. The mean-value theorem (equivalently the fundamental theorem of calculus) gives

```text
|R(y,z)-R(0,z)| <= beta*|y|.                                (5)
```

Hence a bounded partial derivative in the cross coordinate is a valid witness for a same-coordinate increment bound.

There is an important stronger special case. If

```text
R(0,z)=0 for every admissible z,                              (6)
```

then (5) immediately gives

```text
|R(y,z)| <= beta*|y|.                                       (7)
```

Thus the precise contract for a pure one-coordinate envelope is **slice vanishing plus slice Lipschitz control**, not mere centering at the single equilibrium.

## 3. Full centering does not imply slice-relative scaling

The distinction is necessary. Consider

```text
R(y,z)=z.
```

Then `R(0,0)=0`, but on the `y=0` slice one has `R(0,z)=z`. For every finite `beta` and every nonzero `z`,

```text
|R(0,z)| > beta*|0| = 0.                                    (8)
```

So full-reference centering alone cannot justify `|R|<=beta|y|`.

Even slice vanishing without quantitative regularity is not enough for a finite linear coefficient on a domain touching `y=0`: `R(y,z)=sqrt(|y|)` satisfies `R(0,z)=0` but `|R(y,z)|/|y|=1/sqrt(|y|)` is unbounded as `y->0`.

Therefore the source contract must contain an actual increment/Lipschitz witness; a zero value is only the anchoring condition.

## 4. Transverse coordinate transport on a box

For a finite transverse state `z=(z_1,...,z_m)` in an axis-aligned covered box, define the telescoping points

```text
z^(0)=0,
z^(j)=(z_1,...,z_j,0,...,0).                               (9)
```

Assume the corresponding coordinate derivative is bounded by `gamma_j` on every coordinate segment from `z^(j-1)` to `z^(j)`:

```text
|partial_{z_j} R(0, path_j(s))| <= gamma_j.                 (10)
```

One-dimensional transport on each segment gives

```text
|R(0,z^(j))-R(0,z^(j-1))| <= gamma_j*|z_j|.                 (11)
```

Telescoping and the triangle inequality yield

```text
|R(0,z)-R(0,0)| <= sum_j gamma_j*|z_j|.                     (12)
```

Combining (5) and (12), if `R(0,0)=0`, then

```text
|R(y,z)| <= beta*|y| + sum_j gamma_j*|z_j|.                 (13)
```

This is exactly the source-to-math shape needed by `T-P4-014`.

The box assumption is not cosmetic: the coordinate paths used in (9) must remain inside the same source-certified/P8-covered domain. A derivative bound on a larger or different domain cannot silently be substituted.

## 5. Convert transverse slopes to an existing quadratic reserve

Suppose the actual certificate supplies the transverse positive reserve

```text
H(z) := sum_j h_j*z_j^2,    h_j>0.                           (14)
```

From (12), weighted Cauchy-Schwarz gives

```text
[R_trans(z)]^2 <= kappa * H(z),                              (15)

kappa := sum_j gamma_j^2 / h_j.                              (16)
```

This coefficient is sharp under only the component slope information. For the linear extremal family

```text
R_trans(z)=sum_j gamma_j z_j
```

with compatible signs, the supremum of `R_trans(z)^2/H(z)` is exactly `kappa`, attained in the direction `z_j` proportional to `gamma_j/h_j`.

Therefore an interval/source lane that can certify coordinate increment slopes does **not** need to invent a scalar transverse state. It can return the single rational dual-reserve number `kappa` in (16).

For formalization, an even cleaner boundary is to make

```text
R_trans^2 <= kappa*H                                        (17)
```

the consumer premise and keep the finite-dimensional weighted Cauchy theorem as a separate bridge. This avoids square roots in the Schur theorem.

## 6. Ellipsoidal form of the T-P4-014 consumer

Let the already-composed same-coordinate coefficient be `a>=0`, so that the total residual obeys

```text
|r| <= a*|y| + |b|,
b^2 <= kappa*H,                                              (18)
```

where `H>=0`. Consider

```text
Q = p*x^2 + 2*x*r + d*y^2 + H.                              (19)
```

Set

```text
Delta := p*d-a^2.                                            (20)
```

If

```text
p>0,
Delta>0,
d*kappa <= Delta,                                           (21)
```

then `Q>=0`.

The proof is the same sharp Schur geometry as `T-P4-014`, but now no artificial scalar `z` is needed. Put `Y=|y|`, `B=|b|`. The exact division-free identity is

```text
Delta * [p*d*Y^2 + p*H - (a*Y+B)^2]
 = (Delta*Y-a*B)^2 + p*(Delta*H-d*B^2).                     (22)
```

Because `Delta>0` and `p>0`, one gets `d>0`. From `B^2<=kappa H` and `d*kappa<=Delta`,

```text
d*B^2 <= Delta*H.                                           (23)
```

So the right side of (22) is nonnegative. Finally

```text
p*Q = (p*x+r)^2 + p*(d*y^2+H)-r^2,                          (24)
```

and (18)-(23) imply the final remainder is nonnegative.

Equivalently, the sharp joint information budget is

```text
a^2 + d*kappa <= p*d.                                       (25)
```

When `kappa>0`, this automatically leaves strict same-coordinate Schur reserve. Equation (25) makes the routing tradeoff explicit: every new same-coordinate slope spends `a`, while every transverse derivative spends the dual quadratic budget `kappa`.

## 7. Concrete block-4 source target

For block 4, `T-P4-013/014` give

```text
p4 = 3/5,
d4 = 116667666666667 / 10^15,
normalized kc coefficient c4 = 1/100.                       (26)
```

Let `beta_total` denote the **sum of all** same-`q5` slope budgets assigned to this channel, not just one execution term:

```text
a4 = 1/100 + beta_total.                                    (27)
```

Let `kappa4` be the weighted transverse dual budget from (16)/(17). The source-facing closure target is

```text
a4^2 + d4*kappa4 <= p4*d4.                                  (28)
```

If the same-coordinate part is deliberately capped at the existing quarter envelope, `a4=1/4`, then

```text
Delta4 = 37503000000001 / 5000000000000000,                 (29)
```

and the exact transverse target is

```text
kappa4 <= 37503000000001 / 583338333333335.                 (30)
```

This is the vector/ellipsoidal version of the scalar condition in `T-P4-014`. It also shows that the historical `beta<=6/25` is a **shared** same-coordinate budget: if centered gravity, controller increment, solve increment, etc. each contribute a `q5` slope, their total must fit that budget. One must not grant `6/25` independently to every term.

## 8. Reference bias remains a separate obstruction

The reference value `R0=R(0,0)` from (3) is not affected by any derivative bound. In an unchanged homogeneous Schur block with no state-independent positive slack, set `y=0`, `z=0`, so all quadratic state reserves vanish. Then

```text
Q(x,0,0)=p*x^2+2*x*R0.                                     (31)
```

At `x=-R0/p`,

```text
Q = -R0^2/p < 0                                             (32)
```

whenever `R0!=0`.

Thus a nonzero reference solve defect/controller execution bias cannot be repaired merely by proving that the *increment* is Lipschitz. It needs a separate scalar slack/ultimate-bound route, a cancellation theorem, a storage redesign, or an exact source theorem forcing the reference bias to zero.

This is particularly relevant to the `solveDefect_B` term in `T-P4-007`: the mathematically correct first source query is not only “how large is the defect?”, but

```text
what is solveDefect_B at the reference state,
and what direct increment bound holds away from that reference?                 (33)
```

Those are different obligations.

## 9. Important Float64 boundary: do not differentiate the real-lift execution map for free

The derivative argument in Sections 2 and 4 is valid for a genuinely differentiable exact-real semantic map. It is **not automatically valid for a Float64 execution map lifted to real numbers**. Rounding/branching can make the lifted map discontinuous or piecewise constant, so a symbolic derivative of the underlying analytic formula is not a proof of a Lipschitz bound for the deployed execution.

For an IEEE/source term, the preferred typed contract is therefore directly incremental:

```text
|R_exec(y,z)-R_exec(0,z)| <= beta*|y|,                      (34)
[R_exec(0,z)-R_exec(0,0)]^2 <= kappa*H(z).                  (35)
```

A smooth derivative/Jacobian enclosure is only one admissible witness for (34)-(35), after a semantic decomposition has separated the smooth exact-real part from the IEEE remainder.

In particular, a generic uniform roundoff envelope

```text
|delta_ieee(x)| <= eps                                      (36)
```

only gives

```text
|delta_ieee(x)-delta_ieee(x0)| <= 2 eps,                    (37)
```

which is an additive bound, not a relative one. Centering by subtraction does not magically turn (37) into `O(|x-x0|)`.

This prevents a likely false proof route for the centered gravity/runtime term from `T-P4-007`: exact centering is useful, but source-level relative routing still needs an incremental/correlated-roundoff theorem.

## 10. Application to the current execution ledger

The bridge suggests the following non-overlapping classification for each channel of `T-P4-007`:

```text
centered gravity DeltaG(q)-DeltaG(0):
    reference bias = 0 by construction;
    exact-real smooth increment -> derivative/interval route;
    IEEE increment -> direct correlated increment bound, otherwise additive remainder.

controller/runtime mismatch delta_ctrl:
    split delta_ctrl(ref) + centered increment;
    route the increment by (34)-(35) if proved;
    keep delta_ctrl(ref) as a bias unless another structural theorem removes it.

solve defect -s_B:
    split -s_B(ref) - [s_B(x)-s_B(ref)];
    same rule; do not infer a relative bound from a uniform backward-error norm.

exact-real remote M_BD a_D:
    remains on T-P4-012 mass-metric route and is not reassigned here.
```

`T-P5-012` may consume a controller mismatch differently by conservative-force extraction in the energy ledger. That does not imply the same term is automatically conservative or harmless in the P4 generalized-force residual. The P4 and P5 consumers must keep their typed contracts separate.

## 11. Minimal formalizable theorem statements

The smallest Lean decomposition should avoid calculus first:

```lean
-- Pure algebraic slice identity.
theorem slice_decomposition ... :
  R y z - R 0 z0 = (R y z - R 0 z) + (R 0 z - R 0 z0)

-- Increment contract -> same + transverse envelope.
theorem slice_increment_envelope
    (hY : |R y z - R 0 z| <= beta*|y|)
    (hZ : |R 0 z - R 0 z0| <= B) :
    |R y z - R 0 z0| <= beta*|y| + B

-- Square-only transverse Schur consumer.
theorem relative_plus_quadratic_transverse_schur
    (hp : 0 < p)
    (hDelta : 0 < p*d-a^2)
    (hr : |r| <= a*|y| + |b|)
    (hH : 0 <= H)
    (hkappa : 0 <= kappa)
    (hb : b^2 <= kappa*H)
    (hbudget : d*kappa <= p*d-a^2) :
    0 <= p*x^2 + 2*x*r + d*y^2 + H
```

Then add two independent bridges only if needed:

1. a one-variable mean-value/interval lemma that discharges `hY` for smooth exact-real functions;
2. a finite weighted Cauchy lemma producing `b^2<=kappa*H` with `kappa=sum gamma_j^2/h_j`.

This theorem decomposition keeps the Float64 source problem outside the exact-real calculus and makes the source boundary visible in the statement.

## 12. Remaining blockers and next interface

The mathematics above closes the **classification rule**, not any deployed coefficient. The remaining source obligations are now sharper:

1. for each `DeltaM/DeltaC/DeltaG/delta_ctrl/s` component, give its reference value separately from its centered increment;
2. for each centered increment, provide a same-domain direct increment bound, or a smooth semantic decomposition plus a valid derivative witness;
3. name the actual positive quadratic transverse reserve `H` in the P4 certificate and its coordinate order;
4. compute the single dual budget `kappa` and check (25), rather than hiding all terms inside one historical residual constant;
5. if a reference bias is nonzero and no scalar slack/storage redesign exists, keep the obstruction explicit.

Admission remains `pending`. This child neither authenticates deployed Float64 semantics nor closes P4/M4.
