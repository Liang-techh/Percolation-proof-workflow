---
kind: review_result
review_id: review-T-P5-126-moving-chart-recenter-coercivity-liuguanyi-20260909T0518Z
task_id: T-P5-126-MOVING-CHART-RECENTER-COERCIVITY
reviewer: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T05:18:00Z
claim_commit: a530c2b2eae84003b89dec76b6bb48a6ebc21f72
inspected_commit: 119338bc1d5cc8ab789ce2bc9f55fd656dba3c29
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-120-MOVING-CHART-CONSERVATIVE-POWER-PULLBACK-liuguanyi-20260909T0302Z.md
    commit: 282c801638022fcb40220e1f92f44f3ec0a3993d
  - path: agent_review_inbox/review-T-P5-122-CURL-METRIC-PULLBACK-CLOSURE-kuangmanmozun-20260909T0342Z.md
    commit: 1ad2545fbe4175bed3808d77c49b533cded84b88
  - path: agent_review_inbox/review-T-P5-125-STRONG-CONVEX-RECENTER-EXISTENCE-honglianmozun-20260909T0455Z.md
    commit: 119338bc1d5cc8ab789ce2bc9f55fd656dba3c29
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_affine_invariance_and_nonlinear_connection_defect_bridge_then_bind_same_cell_chart_hessian_metric_and_center_force_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional chain-rule, quadratic-form, convexity, and root-free scalar algebra only
exit_code: n/a
---

# T-P5-126 — moving-chart transport of strong-convex recenter certificates

## 0. Bottleneck selected

T-P5-120 proves that a conservative force is a work covector under a nonlinear chart and records the derivative identity

`D_z(J^T r)[eta] = (D_z J[eta])^T r + J^T (D_x r) J eta`.

T-P5-125 then gives a root-free strong-convexity gate

`B < 4 mu^2 R`

which forces a unique interior critical point of the shaped scalar potential on one fixed ellipsoidal cell.

A remaining interface gap is easy to miss:

> does the T-P5-125 certificate survive a normalized coordinate chart unchanged, and if not, exactly what extra mathematical term has to be certified?

The answer is:

1. **affine invertible charts preserve the entire `mu/B/R` recenter certificate exactly**, with no condition-number loss;
2. a genuinely nonlinear chart contributes the contracted connection term
   `<grad F, D^2 T[eta,eta]>` to the pulled Hessian;
3. strong convexity is therefore **not** invariant under arbitrary nonlinear reparameterization, even for a smooth one-dimensional diffeomorphism;
4. a minimal division-free nonlinear bridge consists of a lower tangent-metric transport, a signed connection-defect lower bound, and two scalar gates;
5. a chart critical point is a full physical critical point only when the pulled covector map has trivial kernel, e.g. `J` is square nonsingular.

This closes the mathematical coordinate-transform seam only. It does not bind any deployed P5 chart, potential, Hessian, source packet, path/FD halo, P8 flowpipe, Float64/controller semantics, Lean/kernel receipt, independent verification, admission, or registry state.

---

## 1. Frozen-time setup and object types

Work at one fixed time. Let physical configuration space be finite-dimensional Euclidean space and let

`F : q -> R`

be the already shaped scalar potential, for example `F=U-Psi` in T-P5-124/125.

Let `P` be symmetric positive definite and write

`Q_P(x) := x^T P x`.

Let a `C^2` normalized chart be

`q = T(z)`,

with Jacobian

`J(z) = D T(z)`.

Fix an old normalized anchor `z0`, put

`q0 := T(z0)`,

`J0 := J(z0)`,

and define the fixed anchor metric

**(1.1)**

`M0 := J0^T P J0`,

`Q0(eta) := eta^T M0 eta`.

For the root-free ellipsoid theorem below, assume `M0` is positive definite. A square nonsingular `J0` is sufficient; more generally it is enough that `J0` be injective on the normalized coordinate space.

Define the normalized ellipsoid

**(1.2)**

`E0(R) := { z0+eta : Q0(eta) <= R }`,  `R>0`.

The pulled potential is

**(1.3)**

`Ftilde(z) := F(T(z))`.

Its old-center force mismatch is the covector pullback

**(1.4)**

`b := grad F(q0)`,

`b0 := grad Ftilde(z0) = J0^T b`.

This is exactly the object typing from T-P5-120: center force is a covector, not a tangent vector.

---

## 2. Exact pulled-Hessian identity

For any normalized direction `eta`, the second chain rule gives

**(2.1)**

`Hess Ftilde(z)[eta,eta]`

`= Hess F(T(z))[J(z)eta, J(z)eta]`

`  + <grad F(T(z)), D^2 T(z)[eta,eta]>`.

Equivalently, in matrix form,

**(2.2)**

`Hess_z Ftilde = J^T (Hess_q F) J + C_T,F`,

where the symmetric contracted chart-curvature matrix is

`(C_T,F)_{ab}`

`:= sum_i (partial_i F)(T(z)) * partial_{ab} T_i(z)`.

This is the symmetric Hessian version of T-P5-120's generalized-force derivative formula. The first term is the ordinary congruence. The second term is not optional on a nonlinear chart.

A source adapter that supplies only `J^T Hess(F) J` is mathematically incomplete unless either

- `D^2 T=0` (affine chart), or
- `grad F=0` on the entire region, which is far stronger than merely knowing one recentered critical point.

---

## 3. Affine chart: exact invariance of the T-P5-125 certificate

Assume first

**(3.1)**

`T(z)=q0 + J0 (z-z0)`

with square nonsingular constant `J0`.

Then `D^2T=0` and

`Hess Ftilde(z)=J0^T Hess F(T(z)) J0`.

Suppose the physical T-P5-125 strong-Hessian packet is

**(3.2)**

`y^T Hess F(q) y >= 2 mu Q_P(y)`

on the physical ellipsoid

`EP(R):={q0+x : Q_P(x)<=R}`.

Because

`Q_P(J0 eta)=Q0(eta)`,

the affine map sends `E0(R)` bijectively onto `EP(R)`. Congruence gives

**(3.3)**

`eta^T Hess Ftilde(z) eta >= 2 mu Q0(eta)`.

Now assume the physical center-force dual packet

**(3.4)**

`<b,x>^2 <= B Q_P(x)`

for all physical `x`. Substituting `x=J0 eta` gives

**(3.5)**

`<b0,eta>^2 = <b,J0 eta>^2 <= B Q0(eta)`.

Since `J0` is onto, the sharp dual constant is actually preserved, not merely upper-bounded.

Therefore the entire T-P5-125 gate

**(3.6)**

`B < 4 mu^2 R`

is unchanged under the affine chart. The unique normalized critical point `z_*` satisfies

`grad Ftilde(z_*)=0`,

and because `J0^T` is nonsingular,

`grad F(T(z_*))=0`.

The displacement certificate is also identical:

**(3.7)**

`4 mu^2 Q0(z_*-z0) <= B`

iff

`4 mu^2 Q_P(T(z_*)-q0) <= B`.

### Consequence

An affine coordinate normalization must not pay a Jacobian condition number in the strong-convex recenter gate when the metric itself is transported by congruence. Any such loss is an artifact of replacing the exact quadratic form by unrelated Euclidean norm caps.

---

## 4. Nonlinear chart: minimal signed connection-defect bridge

Return to a general `C^2` chart. Assume the physical strong-Hessian packet on the chart image:

**(4.1)**

`Hess F(T(z))[y,y] >= 2 mu Q_P(y)`

for every `z in E0(R)` and every physical direction `y`, with `mu>0`.

To compare the varying tangent metric to the fixed anchor metric, assume a nonnegative lower transport factor `a`:

**(4.2) LOWER TANGENT-METRIC TRANSPORT**

`Q_P(J(z)eta) >= a Q0(eta)`

for every `z in E0(R)` and `eta`.

In matrix language:

`J(z)^T P J(z) - a M0 >= 0`.

Next keep the chart-curvature contribution signed. Assume `kappa>=0` with

**(4.3) CONNECTION-DEFECT LOWER BOUND**

`<grad F(T(z)), D^2T(z)[eta,eta]> >= -kappa Q0(eta)`

for every `z in E0(R)` and `eta`.

Equivalently,

`C_T,F(z)+kappa M0 >= 0`.

Choose a desired normalized strong-convexity constant `mu_z>0` satisfying the root-free scalar gate

**(4.4)**

`2 mu_z + kappa <= 2 mu a`.

Then (2.1), (4.1), (4.2), and (4.3) give

`Hess Ftilde(z)[eta,eta]`

`>= 2 mu Q_P(J eta) - kappa Q0(eta)`

`>= (2 mu a-kappa) Q0(eta)`

`>= 2 mu_z Q0(eta)`.

Hence:

**(4.5) NONLINEAR PULLBACK STRONG-CONVEXITY BRIDGE**

`Hess Ftilde(z)[eta,eta] >= 2 mu_z Q0(eta)`

on the whole normalized ellipsoid.

No Jacobian inverse, square root, eigenvalue, or division is required by the trusted theorem. A producer proposes rational `a,kappa,mu_z`; the checker verifies PSD/order statements and (4.4).

---

## 5. Center mismatch transports without an extra nonlinear penalty

The nonlinear Hessian pays a connection term because a derivative of `J^T` appears. The **first derivative at the old center** does not.

From (1.4), for every normalized `eta`,

`<b0,eta>=<b,J0 eta>`.

Thus any physical dual packet restricted to the anchor tangent image,

**(5.1)**

`<b,J0 eta>^2 <= B Q_P(J0 eta)`,

immediately becomes

**(5.2)**

`<b0,eta>^2 <= B Q0(eta)`.

There is no `D^2T` term here.

Therefore, once (4.5) holds, the T-P5-125 root-free existence theorem applies in normalized coordinates under the unchanged mismatch constant `B` with only the reduced curvature `mu_z`:

**(5.3) NORMALIZED ROOT-FREE RECENTER GATE**

`B < 4 mu_z^2 R`.

It yields a unique `z_* in int(E0(R))` with

**(5.4)**

`grad Ftilde(z_*)=0`.

The same strong-monotonicity argument yields the a-posteriori displacement bound

**(5.5)**

`4 mu_z^2 Q0(z_*-z0) <= B`.

This step is also division-free: if `d=z_*-z0`, strong monotonicity gives

`-<b0,d> >= 2 mu_z Q0(d)`;

squaring and using `<b0,d>^2<=B Q0(d)` gives (5.5), with the `Q0(d)=0` case trivial.

---

## 6. When is the chart critical point a physical critical point?

The normalized criticality condition is

`0 = grad Ftilde(z_*) = J(z_*)^T grad F(T(z_*))`.

This only proves full physical criticality if the covector pullback is injective:

**(6.1)**

`J(z_*)^T g = 0  ->  g=0`.

For an ordinary square chart it is enough to prove `J(z_*)` nonsingular. The trusted theorem can consume (6.1) directly; it does not need to construct `J^{-1}`.

Under (6.1),

**(6.2)**

`grad F(T(z_*))=0`.

If instead `J:R^k->R^n` is only an immersion with `k<n`, then `J^T grad F=0` means only that `T(z_*)` is critical **along the chart image/submanifold**. It must not be promoted to a full physical equilibrium without an additional normal-direction condition.

This distinction is important for any future reduced-coordinate or block-only adapter.

---

## 7. Same-cell image coverage without inverse charts

The nonlinear theorem above assumes the physical Hessian packet is valid on `T(E0(R))`. That image inclusion can itself be certified without solving for `T^{-1}`.

Assume an upper tangent transport on the whole normalized ellipsoid:

**(7.1)**

`Q_P(J(z)eta) <= Lambda Q0(eta)`

for every `z in E0(R)` and `eta`, with `Lambda>=0`.

Because `E0(R)` is convex, for any `z=z0+d in E0(R)` the straight segment `z_s=z0+s d` stays in the cell. The fundamental theorem of calculus gives

`T(z)-T(z0)=integral_0^1 J(z_s)d ds`.

Quadratic Jensen yields

**(7.2)**

`Q_P(T(z)-q0) <= Lambda Q0(d)`.

Therefore if the physical strong-Hessian certificate is known on

`EP(R_phys)={q0+x:Q_P(x)<=R_phys}`

and the scalar gate

**(7.3)**

`Lambda R <= R_phys`

holds, then

**(7.4)**

`T(E0(R)) subset EP(R_phys)`.

This is the same segment discipline as T-P5-122's secant metric bridge: endpoint-only Jacobian bounds are insufficient.

For the recentered point specifically, (5.5) and (7.2) give the optional physical displacement certificate

**(7.5)**

`4 mu_z^2 Q_P(T(z_*)-q0) <= Lambda B`.

Again no division or square root is needed.

---

## 8. Hard obstruction: nonlinear diffeomorphisms do not preserve strong convexity

The connection term in (2.1) is mathematically necessary.

Take one dimension with

`F(q)=q^2/2`,

`P=1`.

Then

`F''(q)=1`,

so the physical potential is globally strongly convex with the T-P5-125 convention `mu=1/2` because

`F'' >= 2 mu = 1`.

Use the smooth nonlinear chart

**(8.1)**

`T(z)=z+z^2`

on the interval `[-1/3,1/3]`. Its derivative is

`T'(z)=1+2z >= 1/3 >0`,

so it is a genuine one-dimensional diffeomorphism onto its image.

The pulled potential is

`Ftilde(z)=1/2 (z+z^2)^2`.

Its second derivative is

**(8.2)**

`Ftilde''(z)=(T'(z))^2 + T(z) T''(z)`

`             = 1+6z+6z^2`.

At `z=-1/3`,

**(8.3)**

`Ftilde''(-1/3) = -1/3 < 0`.

Thus the pullback is not even convex there.

The two chain-rule pieces are explicitly

`(T')^2 = 1/9`,

`T*T'' = (-2/9)*2 = -4/9`,

whose signed sum is `-1/3`.

So a theorem that transports physical strong convexity through a nonlinear chart using only `J^T Hess(F) J` is false even for a smooth invertible scalar reparameterization. The missing object is exactly the signed connection defect (4.3).

---

## 9. Why signed contraction must precede enclosure

The source-facing connection matrix is

`C_T,F = sum_i (partial_i F) Hess(T_i)`.

Its entries can contain large cancellations between coordinates and between positive/negative gradient components. Therefore the correct order is:

1. form the complete signed contraction `C_T,F` from the **same point/source/chart key**;
2. then prove `C_T,F + kappa M0 >=0` or an equivalent quadratic inequality.

A producer that first replaces every `partial_i F` and every `Hess(T_i)` by independent absolute intervals can manufacture a large artificial `kappa`, just as separately enclosing the two moving-frame power pieces in T-P5-120 destroys exact work cancellation.

This is not merely a numerical optimization issue: an unnecessarily large `kappa` directly reduces the available normalized curvature through

`2 mu_z + kappa <= 2 mu a`

and can make the root-free existence gate fail even when the exact signed pulled Hessian is strongly positive.

When actual exact/rational matrices are available, the preferred direct gate is simply

**(9.1)**

`Hess Ftilde(z) - 2 mu_z M0 >=0`

on the cell. The factored `(mu,a,kappa)` bridge is a source decomposition when direct certification is unavailable, not an intrinsic condition-number theorem.

---

## 10. Minimal theorem statements

### Theorem A — affine recenter certificate invariance

Given square nonsingular `J`, SPD `P`, `M=J^TPJ`, affine `T(z)=q0+J(z-z0)`, and physical packets

`Hess F >= 2 mu P`,

`<b,x>^2 <= B x^TPx`,

on `EP(R)`, then the pulled potential on `E0(R)` satisfies the same packets with exactly the same `mu,B,R`. Hence `B<4mu^2R` produces a unique chart/physical critical point and the same displacement bound.

### Theorem B — nonlinear connection-defect strong-convexity bridge

Assume on `E0(R)`:

`Hess F(Tz)[y,y] >= 2mu y^TPy`,

`J(z)^TPJ(z) >= a M0`,

`C_T,F(z) >= -kappa M0`,

and

`2mu_z+kappa <= 2mu a`, `mu_z>0`.

Then

`Hess(F o T)(z) >= 2mu_z M0`.

### Theorem C — nonlinear root-free recenter

Add

`<J0^Tb,eta>^2 <= B eta^TM0eta`,

`B<4mu_z^2R`.

Then there exists a unique `z_* in int(E0(R))` with

`grad(F o T)(z_*)=0`

and

`4mu_z^2 Q0(z_*-z0)<=B`.

If `ker(J(z_*)^T)={0}`, then `grad F(T(z_*))=0`.

### Theorem D — inverse-free chart-image coverage

If additionally

`J(z)^TPJ(z) <= Lambda M0`

on `E0(R)` and `Lambda R<=R_phys`, then

`T(E0(R)) subset EP(R_phys)`.

This can supply the same-cell premise of Theorem B from a physical ellipsoid certificate.

---

## 11. Suggested Lean decomposition

The source-independent formalization can be split into small leaves:

```text
pulled_hessian_quadratic_identity
  Hess(F o T)[eta,eta]
    = Hess(F)[J eta,J eta] + <grad F,D2T[eta,eta]>.

affine_pulled_hessian_congruence
  D2T=0 -> Hess(F o T)=J^T Hess(F) J.

affine_recenter_dual_packet_transport
  M=J^TPJ -> <J^Tb,eta>^2 <= B*Q_M(eta).

nonlinear_pulled_strong_convexity
  physical Hess lower
  -> tangent metric lower
  -> signed connection lower
  -> 2*mu_z+kappa <= 2*mu*a
  -> pulled Hess lower.

normalized_root_free_recenter_exists_unique
  pulled Hess lower
  -> dual mismatch packet
  -> B < 4*mu_z^2*R
  -> unique interior grad zero.

chart_critical_to_physical_critical
  J^T g=0 -> ker(J^T)={0} -> g=0.

whole_segment_tangent_upper_implies_secant_upper
  uniform J^TPJ <= Lambda*M0 on convex segment
  -> Q_P(Tz-Tz0) <= Lambda*Q0(z-z0).

normalized_cell_maps_into_physical_cell
  secant upper + Lambda*R <= R_phys
  -> T(E0(R)) subset EP(R_phys).
```

The trusted core can stay entirely in addition, multiplication, transpose, quadratic-form order, compact convex minimization, and the chain rule. No explicit matrix inverse is required.

---

## 12. Source-facing typed packet

A future actual P5 instantiation should bind the following under one chart/cell/reference key:

1. physical shaped potential `F=U-Psi` and its `grad F`, `Hess F` semantics;
2. normalized chart `T`, `J=DT`, and the contracted second-chart term `C_T,F` or equivalent `D2T` packet;
3. old centers `z0`, `q0=T(z0)`;
4. physical SPD metric `P` and exact anchor pullback `M0=J0^TPJ0`;
5. normalized radius `R` and, if needed, physical radius `R_phys`;
6. physical strong-Hessian constant `mu`;
7. tangent lower factor `a` and signed connection debit `kappa`, or a direct pulled-Hessian PSD witness;
8. center mismatch `b=grad F(q0)` and dual constant `B` for `J0^T b`;
9. optional tangent upper `Lambda` for chart-image/physical displacement coverage;
10. a no-kernel/nonsingularity witness for `J(z_*)^T` if the consumer needs a **physical** critical point rather than only a chart-constrained one.

The scalar checker gates are only

`2 mu_z + kappa <= 2 mu a`,

`B < 4 mu_z^2 R`,

and optionally

`Lambda R <= R_phys`.

All source equality, whole-cell coverage, runtime semantics, and downstream dynamic-storage use remain external obligations.

---

## 13. Boundaries deliberately left open

This review does **not** claim:

- that the deployed P5 normalization chart is affine, `C^2`, or globally injective;
- that actual `J/D2T` or the contracted connection matrix have been exported;
- that the physical shaped `F=U-Psi` and its Hessian share the same source/cell key as the chart;
- that any concrete `mu,a,kappa,B,Lambda,R,R_phys` have been certified;
- that a frozen-time recenter `z_*` varies smoothly with time;
- that a moving recenter introduces no derivative term in a time-dependent storage ledger;
- that physical/chart/FD/reference/P8 path halos are covered;
- that Float64/controller/runtime evaluation matches the exact-real functions;
- that any Lean theorem has compiled;
- that 封不觉 has independently verified the child;
- that P5/P8 parent state, formal certificate gate, or registry eligibility has changed.

In particular, **time-dependent recenter transport remains a separate theorem**. T-P5-120 handles moving-chart power exactly, but if the chosen critical center itself becomes `z_*(t)`, differentiability and same-tube tracking of that center must be proved before using a time-varying recentered storage.

---

## 14. Final disposition

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending.**

The interface gap is mathematically closed as follows:

- affine chart: T-P5-125 is exactly coordinate invariant in the congruent metric;
- nonlinear chart: pay only the signed connection defect required by the second chain rule;
- use `2mu_z+kappa<=2mu a` and `B<4mu_z^2R` as the root-free normalized recenter gate;
- require `ker(J^T)=0` before upgrading chart criticality to full physical criticality;
- use a whole-segment tangent upper bound, not an endpoint Jacobian, to transport the recenter cell/displacement back to physical space.

The next useful child is not another generic convexity proof. It is an actual same-cell packet for `F/gradF/HessF/T/J/D2T/P/M0`, or—if the chart is known affine—an exact source identity proving `D2T=0` so the connection debit disappears completely.