---
kind: review_result
review_id: review-T-P5-133-reference-knot-chart-switch-covariance-liuguanyi-20260909T0710Z
task_id: T-P5-133-REFERENCE-KNOT-CHART-SWITCH-COVARIANCE
reviewer: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T07:10:00Z
claim_commit: 08832ef00891d0b2a8a96fe94b786ef195ab00f7
inspected_commit: a521dbad9a0c1dac213ed61e745dff9c2c54cc4f
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-129-MOVING-CHART-CENTER-TRACKING-COVARIANCE-liuguanyi-20260909T0615Z.md
    commit: 7bfca9b203efb1e1f27f218ecffd572d222ca58d
  - path: agent_review_inbox/review-T-P5-130-REFERENCE-KNOT-RECENTER-RESET-guyuefangyuan-20260909T0630Z.md
    commit: 7c48ca222df55971d46c3a1ec6b37cdd5aba27c9
  - path: agent_review_inbox/review-T-P5-131-SHARP-PARAMETER-FREE-KNOT-RESET-kuangmanmozun-20260909T0642Z.md
    commit: bd54dbc6226fb2eeafcac3d233a709148af4b96f
  - path: agent_review_inbox/review-T-P5-132-BOUNDED-CELL-KNOT-RESET-honglianmozun-20260909T0658Z.md
    commit: a521dbad9a0c1dac213ed61e745dff9c2c54cc4f
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_chart_gluing_affine_covariance_and_nonlinear_secant_leaves_then_bind_one_same_knot_physical_chart_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact coordinate/pullback/FTC algebra only
exit_code: n/a
---

# T-P5-133 — reference-knot chart-switch covariance and nonlinear secant correction

## 0. Narrow seam selected

T-P5-130/131/132 now give a sharp physical reference-knot reset chain.  Their scalar packet is built from a **single physical state at the knot**, a fixed physical quadratic metric `P`, the pre/post potentials, and one common pre/post physical cell.  T-P5-132 explicitly warns that a radius from another chart cannot simply be inserted into its gate.

T-P5-129, on the other hand, treats continuous motion in a time-dependent chart and proves the correct covector/metric covariance at a moving critical center.

What was still missing is the interface when a **reference knot and a chart switch occur at the same instant**.  There are two distinct questions:

1. how the same physical state is glued across two coordinate systems;
2. whether the sharp reset constants `m,B,mu,ell,R` survive the coordinate change.

For invertible affine charts the answer is exact: the whole T-P5-130/131/132 packet is congruence-covariant with **no Jacobian condition-number tax**.  For a nonlinear chart, however, replacing the physical secant displacement by the anchor tangent `J_* xi` is generally false.  The exact object is an averaged/secant Jacobian, and the potential-jump Hessian also acquires a nonzero connection term because the jump gradient at the old center need not vanish.

This review proves those statements and gives a fail-closed typed interface.  It does not redo the sharp scalar reset optimization of T-P5-131/132.

---

## 1. Physical reset packet

Let the physical state space be finite-dimensional real coordinates.  Fix an SPD matrix `P` and

`Q_P(x) := x^T P x`.

At one reference knot let

`F-`, `F+`

be the pre/post shaped potentials, with critical centers

`grad F-(q-) = 0`,

`grad F+(q+) = 0`.

Define

`W-(q) := F-(q)-F-(q-)`,

`W+(q) := F+(q)-F+(q+)`,

`DeltaF := F+ - F-`,

`g := grad DeltaF(q-) = grad F+(q-)`,

`x := q-q-`,

`Qx := Q_P(x)`,

`p := <g,x>`.

The T-P5-130/131/132 scalar interface consists of premises of the form

`m*Qx <= W-(q)`,

`p^2 <= B*Qx`,

`4*mu*C <= B`,

`W+(q) <= W-(q)+p+ell*Qx+C`,

and, for the bounded-cell branch,

`Qx <= R`.

The sharp consumers then form

`A := m*(kappa-1)-ell`

and use only polynomial comparisons in `m,B,mu,ell,R,kappa,E`.

The purpose of the present review is to prove when this **same scalar packet** can be transported through a coordinate switch without changing those constants.

---

## 2. The first typed rule: glue physical state, not coordinate labels

Let the pre and post charts at the knot be

`T- : Z- -> Qphys`,

`T+ : Z+ -> Qphys`.

Let `z-` and `z+` be the coordinate representations of the physical state immediately before/after the reference-definition switch.  If the physical state itself is continuous, the correct knot condition is

**(2.1)**

`T-(z-) = T+(z+) = q`.

There is in general **no theorem** saying

`z+ = z-`.

Define pulled storage values

`Wtilde-(z) := W-(T-(z))`,

`Wtilde+(z) := W+(T+(z))`.

Then (2.1) gives the exact scalar identity

**(2.2)**

`Wtilde+(z+) - Wtilde-(z-) = W+(q)-W-(q)`.

Hence every already-proved physical reset conclusion

`W+(q) <= kappa*W-(q)+E`

immediately transports to

**Theorem A — same-physical-state reset gluing**

**(2.3)**

`Wtilde+(z+) <= kappa*Wtilde-(z-)+E`.

No inverse chart is needed in the theorem statement.  A source/checker can simply carry the two chart evaluations plus the physical equality witness (2.1).

### Exact obstruction to `z+=z-`

Take one dimension with

`T-(z)=z`,

`T+(z)=2z`,

and physical state `q=1`.

The correct coordinates are

`z-=1`, `z+=1/2`.

Silently setting `z+=z-=1` evaluates the post storage at physical state `2`, not at the continuous state `1`.  Therefore coordinate-label equality is not a permissible substitute for the physical gluing equation.

---

## 3. Invertible affine chart switch: exact packet covariance

Assume now

`T_sigma(z) = a_sigma + J_sigma z`, `sigma in {-,+}`,

with square invertible matrices `J_sigma`.

Let `c-` and `c+` represent the physical critical centers:

`T-(c-) = q-`,

`T+(c+) = q+`.

Define the pulled quadratic metrics

**(3.1)**

`M_sigma := J_sigma^T P J_sigma`.

For the pre-knot displacement

`xi := z- - c-`,

we have the exact identity

**(3.2)**

`x = q-q- = J_- xi`.

Therefore

**(3.3)**

`Qx = xi^T M_- xi`.

So a physical radius `Qx<=R` is exactly the normalized radius

`xi^T M_- xi <= R`;

the scalar `R` does not change.

### 3.1 Covector pairing

Let

**(3.4)**

`gtilde_- := J_-^T g`.

Then

**(3.5)**

`p = <g,x> = <gtilde_-,xi>`.

Consequently the dual inequality

`<g,y>^2 <= B*y^T P y`

is equivalent, under the invertible affine change `y=J_- eta`, to

**(3.6)**

`<gtilde_-,eta>^2 <= B*eta^T M_- eta`.

The same `B` is used.  There is no singular-value or condition-number factor because both the covector and the metric are transported by the same congruence.

### 3.2 Pre-storage coercivity

Since scalar storage is composition-invariant,

`Wtilde-(z-) = W-(q)`.

Thus

`m*Qx <= W-(q)`

is exactly

**(3.7)**

`m*xi^T M_- xi <= Wtilde-(z-)`.

The same `m` is used.

### 3.3 Signed Hessian-jump coefficient

Let

`DeltaH(q) := Hess F+(q)-Hess F-(q)`.

Because `T-` is affine,

**(3.8)**

`Hess_z (DeltaF o T-)(z) = J_-^T DeltaH(T-(z)) J_-`.

Moreover the normalized straight segment

`c- + s*xi`

maps exactly to the physical straight segment

`q- + s*x`.

Hence the physical signed bound

`y^T DeltaH(q-+s*x)y <= 2*ell*y^T P y`

transports exactly to

**(3.9)**

`eta^T Hess_z(DeltaF o T-)(c-+s*xi) eta <= 2*ell*eta^T M_- eta`.

The same signed `ell` is retained, including favorable `ell<0`.

### 3.4 Post strong convexity and relocation packet

If on the common physical cell

`y^T Hess F+(q)y >= 2*mu*y^T P y`,

then in the post chart

**(3.10)**

`eta^T Hess_z(F+ o T+)(z) eta >= 2*mu*eta^T M_+ eta`.

Again the same `mu` is used.

The relocation scalar

`C := F+(q-) - F+(q+)`

is a physical scalar and therefore unchanged by chart representation.  The bound `4*mu*C<=B` therefore also retains the same `mu` and `B`.

### Theorem B — affine covariance of the sharp knot-reset packet

Under the same-physical-state gluing (2.1), center identities, and invertible affine charts, the physical T-P5-130/131/132 packet

`(m,B,mu,ell,R,kappa,E)`

is equivalent to the pulled packet using

`M-=J_-^T P J_-`, `M+=J_+^T P J_+`, `gtilde_-=J_-^T g`.

In particular:

- `A=m*(kappa-1)-ell` is unchanged;
- the T-P5-131 branch/product gate is unchanged;
- the T-P5-132 branch comparison `B ? 4*A^2*R` is unchanged;
- the sharp additive floor `E` is unchanged.

**No Jacobian condition-number penalty is mathematically required.**  Such a penalty appears only if a consumer discards the congruence metric and replaces it by an unrelated Euclidean norm.

For an affine switch, even the state-gluing equation can be left inverse-free:

**(3.11)**

`a_- + J_- z_- = a_+ + J_+ z_+`.

The checker does not need to form `J_+^{-1}`.

---

## 4. Nonlinear chart: the exact displacement is secant, not tangent

Let the pre chart `T` be `C^1` on the normalized straight segment from the old-center coordinate `c` to `c+xi`.  Set

`J(s) := D T(c+s*xi)`.

By the fundamental theorem of calculus,

**(4.1)**

`T(c+xi)-T(c) = Integral_0^1 J(s) xi ds`.

Define the averaged/secant Jacobian

**(4.2)**

`Jbar(xi) := Integral_0^1 J(s) ds`.

Then the physical displacement is exactly

**(4.3)**

`x = Jbar(xi) xi`.

Therefore the two scalar objects consumed by T-P5-130/131/132 are exactly

**(4.4)**

`Qx = xi^T [Jbar(xi)^T P Jbar(xi)] xi`,

and

**(4.5)**

`p = <Jbar(xi)^T g, xi>`.

This is the correct nonlinear source-to-math bridge.  The knot-reset scalar theorem remains valid without modification if the producer keeps the **physical** `x,Qx,p`; alternatively, a normalized-only producer must use the secant object or certify the error made by replacing it.

### Corollary — exact secant packet

Define

`Msec(xi) := Jbar(xi)^T P Jbar(xi)`,

`gsec(xi) := Jbar(xi)^T g`.

Then

`Qx = xi^T Msec(xi) xi`,

`p = <gsec(xi),xi>`.

Thus the T-P5-132 radius/dual premises can be represented in normalized coordinates without any pointwise inverse, provided `Msec/gsec` are genuinely bound to the same chart segment and physical knot.

---

## 5. Exact tangent-substitution remainder

Let

`J0 := D T(c)`.

Define the chart secant remainder

**(5.1)**

`r_T(xi) := x-J0*xi`.

From (4.1),

**(5.2)**

`r_T(xi) = Integral_0^1 [J(s)-J0] xi ds`.

If `T` is `C^2`, integrate once more:

**(5.3)**

`r_T(xi) = Integral_0^1 (1-s) D^2 T(c+s*xi)[xi,xi] ds`.

The physical linear mismatch is therefore

**(5.4)**

`p = <J0^T g,xi> + <g,r_T(xi)>`.

The physical quadratic radius is

**(5.5)**

`Qx = Q_P(J0*xi) + 2*(J0*xi)^T P r_T(xi) + Q_P(r_T(xi))`.

So replacing `Jbar` by `J0` does **not** merely relabel coordinates.  It drops a signed second-order contribution from both the linear mismatch and the radius metric.

### Exact 1D obstruction

Take

`P=1`, `T(z)=z+z^2`, `c=0`, `xi=1/4`, `g=1`.

Then

`J0=1`,

`x=T(1/4)-T(0)=5/16`.

Hence the true knot quantities are

`p=5/16`,

`Qx=25/256`.

The anchor-tangent substitution would use

`p_tan=1/4`,

`Q_tan=1/16=16/256`.

It underestimates both quantities; the missing signed linear term is exactly `1/16`.  Therefore a normalized knot packet containing only `J0` cannot safely instantiate the sharp T-P5-131/132 gates unless it also carries a certified chart-remainder budget.

---

## 6. Nonlinear Hessian jump has a connection term that does not vanish at a reference knot

There is a second, independent nonlinear-chart issue.  For a `C^2` chart,

**(6.1)**

`Hess_z(DeltaF o T)(z)[eta,eta]`

` = Hess_q DeltaF(Tz)[J(z)eta,J(z)eta]`

`   + <grad_q DeltaF(Tz), D^2 T(z)[eta,eta]>`.

T-P5-129 showed that at a true critical center of a single potential the analogous connection term disappears because the physical gradient is zero.

At the **old center of a reference knot**, however,

`grad DeltaF(q-) = grad F+(q-) = g`

is generally nonzero.  Therefore the connection term in (6.1) is generally nonzero precisely where the reset calculation starts.

### Exact obstruction

Take one dimension,

`F-(q)=q^2`,

`F+(q)=q^2+q`,

so

`DeltaF(q)=q`, `DeltaH=0`, `q-=0`, `g=1`.

Use

`T(z)=z+z^2`, `c=0`.

The physical Hessian jump is identically zero, but

`DeltaF(T(z)) = z+z^2`

has normalized Hessian

**(6.2)**

`d^2/dz^2 [DeltaF(T(z))] = 2`.

Thus a consumer that simply writes

`Hess_z DeltaFtilde = J^T DeltaH J`

would infer `0` instead of `2` and can undercharge the signed `ell` term.

### Consequence

For nonlinear charts there are only two sound lanes:

1. **physical reset lane:** keep T-P5-130/131/132 in physical coordinates and use chart equality only for state/reference binding;
2. **normalized-only lane:** prove a whole-segment signed bound for the full pullback Hessian (6.1), including the connection term, and separately certify the secant/tangent relation needed for `Qx` and `p`.

There is no sound third lane in which one imports the physical `ell` unchanged while using only `J_*` and dropping `D^2T`.

---

## 7. Minimal theorem statements for formalization

The mathematical content can be split into small leaves.

### Leaf 1 — same physical state glues storage reset

Assumptions:

`Tminus zminus = q`,

`Tplus zplus = q`,

`Wplus q <= kappa*Wminus q + E`.

Conclusion:

`(Wplus o Tplus) zplus <= kappa*(Wminus o Tminus) zminus + E`.

### Leaf 2 — affine quadratic congruence

For `x=J*xi`, `M=J^T P J`, prove

`x^T P x = xi^T M xi`.

### Leaf 3 — affine covector pairing

For `gtilde=J^T g`, prove

`g^T(J xi)=gtilde^T xi`,

and, for invertible `J`, equivalence of the dual `B` bounds.

### Leaf 4 — affine Hessian congruence

For affine `T(z)=a+Jz`, prove

`Hess(F o T)=J^T(Hess F o T)J`.

Use it to transport both `mu` and the signed `ell` without changing constants.

### Leaf 5 — nonlinear secant displacement

For `C^1 T` on the segment,

`T(c+xi)-T(c)=Integral_0^1 DT(c+s xi) xi ds`.

### Leaf 6 — tangent remainder

For `C^2 T`,

`T(c+xi)-T(c)-DT(c)xi`

`=Integral_0^1 (1-s) D^2T(c+s xi)[xi,xi] ds`.

### Leaf 7 — pullback Hessian connection for a potential jump

`Hess(DeltaF o T)[eta,eta]`

`=Hess DeltaF[J eta,J eta] + <grad DeltaF,D^2T[eta,eta]>`.

This leaf should carry an explicit negative test showing that `grad DeltaF(q-)=0` is not available at a generic reference knot.

---

## 8. Suggested typed source contract

A minimal same-knot adapter should bind the following under one immutable knot identity.

### Common physical fields

- `knotKey`;
- `physicalStateKey` and physical state `q`;
- `preReferenceKey`, `postReferenceKey`;
- `potentialMinusKey`, `potentialPlusKey`;
- physical metric `PKey`;
- center identities `q-`, `q+`;
- physical T-P5-130/131/132 scalar packet or enough fields to derive it.

### Chart-gluing fields

- `chartMinusKey`, `chartPlusKey`;
- `z-`, `z+`;
- exact gluing witness `T-(z-)=q=T+(z+)`;
- center-coordinate witnesses `T-(c-)=q-`, `T+(c+)=q+`.

### Affine lane

- `a-`, `J-`, `a+`, `J+`;
- exact affine chart identities on the certified cell;
- `M-=J-^T P J-`, `M+=J+^T P J+`;
- `gtilde-=J-^T g`.

No condition number belongs in this lane.

### Nonlinear lane

Prefer keeping the physical reset packet.  If a normalized-only packet is required, additionally bind either

- a genuine secant/averaged-Jacobian object for the whole old-center-to-state segment,

or

- a `C^2` chart remainder bound that charges (5.4)-(5.5),

and a signed full pullback-Hessian bound including the connection term in (6.1).

A lone anchor Jacobian `J_*` is not enough.

---

## 9. Boundaries and non-claims

This child proves only the mathematical coordinate bridge.  The following remain open:

1. actual source identity for the deployed pre/post chart keys and reference keys;
2. proof that the same physical knot/state is represented on both sides;
3. actual affine-vs-nonlinear classification of the deployed normalization chart;
4. if nonlinear, whole-segment `C^1/C^2` coverage, secant/remainder and connection-term bounds;
5. source binding for `F-/F+/P/g/m/B/mu/ell/R`;
6. actual reference schedule, controller/FD/Float64/solve semantics;
7. P8 flowpipe, physical/reference/FD halo and whole-path coverage;
8. Lean/kernel receipt;
9. independent verification by 封不觉;
10. admission/registry/formal-certificate promotion.

In particular, this theorem does **not** authorize transporting a radius or `ell` from one chart to another by matching field names.  The exact affine congruence or nonlinear secant/connection contract must be present.

---

## 10. Integration recommendation

The cleanest consumer architecture is:

- keep T-P5-130/131/132 as the canonical **physical knot-reset theorem**;
- add a very small chart-gluing leaf for `T-(z-)=T+(z+)=q`;
- for affine deployed charts, instantiate Theorem B and reuse the exact same sharp scalar reset constants;
- for nonlinear charts, keep physical `x,Qx,p` whenever possible; only build a normalized-only packet if the producer can supply whole-segment secant/connection evidence.

This avoids both false coordinate continuity and artificial condition-number inflation, while keeping the sharp scalar reset work of T-P5-131/132 unchanged.