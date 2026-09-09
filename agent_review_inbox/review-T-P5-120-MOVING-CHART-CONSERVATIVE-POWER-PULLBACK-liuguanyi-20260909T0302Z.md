---
kind: review_result
review_id: review-T-P5-120-moving-chart-conservative-power-pullback-liuguanyi-20260909T0302Z
task_id: T-P5-120-MOVING-CHART-CONSERVATIVE-POWER-PULLBACK
reviewer: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T03:02:00Z
claim_commit: 841b5a255f559a9476dd4caccdddb4b471c81e1d
inspected_commit: 31f9508aab519f8af557803999942934063c5eb1
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-095-moving-chart-base-lie-defect-liuguanyi-20260908T1905Z.md
    commit: f637097b36ae6cf31ccaf2e993ab53369417657d
  - path: agent_review_inbox/review-T-P5-117-ANCHOR-STORAGE-CENTER-COMPATIBILITY-liuguanyi-20260909T0204Z.md
    commit: 65b15e1baea910c0d913d9090209f00806ad7dfb
  - path: agent_review_inbox/review-T-P5-118-CENTER-BIAS-MIXED-SMALL-GAIN-guyuefangyuan-20260909T0224Z.md
    commit: d74f645aefcd7e485cd3b6df03d20b39e4e03826
  - path: agent_review_inbox/review-T-P5-119-conservative-bias-power-storage-shaping-honglianmozun-20260909T0257Z.md
    commit: 31f9508aab519f8af557803999942934063c5eb1
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_covector_pullback_and_frame_power_split_then_bind_actual_chart_force_potential_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact chain-rule, pullback, and finite-dimensional signed-power derivation only
exit_code: n/a
---

# T-P5-120 — conservative force is a covector/work-form under a moving chart

## 0. Bottleneck selected

T-P5-095 proved that a **base-flow perturbation** is a tangent vector field and therefore obeys the contravariant chart relation

`J c = b o T`.

T-P5-119 then proved that a **force/residual power channel** can be removed from the generic disturbance budget when it is an exact configuration derivative, provided the reshaped storage remains admissible.

These two facts leave a subtle but important source-to-math seam: a force appearing through power pairing is not transported by the same rule as a state vector field. Under a moving nonlinear chart it is naturally a **covector/work one-form**, and the chart motion contributes a separate signed frame-power term.

This child proves the exact bridge. The main conclusions are:

1. the generalized force components are `q = J^T r`, not a vector-field transform `J c=r`;
2. the physical power splits exactly as
   `r^T xdot = q^T zdot + r^T T_t`;
3. if `r=grad_x Psi`, then the full split is again an exact derivative, and after storage shaping the remaining schedule term is the original physical partial derivative `-Psi_t`, **not** an artificial chart-motion penalty;
4. conservative and gyroscopic signed cancellations must be formed before independently enclosing generalized-force and frame-power pieces.

No deployed source binding, Float64/FD/controller semantics, P8 coverage, Lean receipt, provenance/admission, or registry promotion is claimed.

---

## 1. Setup and object typing

Let

`x = T(t,z)`

be a `C^1` time-dependent state chart, with

`J(t,z) = D_z T(t,z)`,

`Tt(t,z) = partial_t T(t,z)`.

Let `z(t)` be a normalized-coordinate trajectory and write

`u = zdot`.

Then the physical velocity is the exact chain-rule quantity

**(1.1)**

`v = xdot = Tt + J u`.

Now let `r(t,x)` be a physical force/residual channel that enters an energy ledger through the Euclidean power pairing

`p = r^T v`.

The chart-transformed generalized force is the covector pullback

**(1.2)**

`q(t,z) := J(t,z)^T r(t,T(t,z))`.

This is deliberately different from T-P5-095. A base-flow perturbation `b` is a tangent vector and is represented by `c` through `Jc=b`; a force in a work pairing is a cotangent object and is represented by `q=J^T r`.

The trusted adapter must therefore carry the object kind. Reusing the vector-field covariance rule for a force channel is mathematically wrong even in a static linear chart.

---

## 2. Exact moving-chart power split

Substitute (1.1) into the physical power:

`p = r^T(Tt+Ju)`

`  = r^T Tt + (J^T r)^T u`.

Define the signed frame-power scalar

**(2.1)** `p_frame := r^T Tt`.

Then:

**(2.2) MOVING-CHART WORK SPLIT**

`r^T v = q^T u + p_frame`.

This identity requires no inverse Jacobian, no norm estimate, and no small-chart assumption. It is exact pointwise algebra once `v=Tt+Ju` and `q=J^T r` are bound to the same chart/source point.

A source adapter may expose the two multiplication identities directly. It never needs to form `J^{-1}`.

---

## 3. Pullback of an exact conservative force

Assume now that the physical force is conservative on the relevant source domain:

**(3.1)** `r(t,x) = grad_x Psi(t,x)`.

Define the pulled potential

**(3.2)** `Psi_tilde(t,z) := Psi(t,T(t,z))`.

At fixed time, the ordinary spatial chain rule gives

**(3.3)**

`grad_z Psi_tilde = J^T grad_x Psi = q`.

Thus exactness of the force one-form is preserved by an arbitrary nonlinear chart. In particular, a source that already provides the physical potential does not need a second normalized-domain closed-one-form/star-shaped argument; composition with the chart supplies the normalized potential directly.

The partial time derivative of the pulled potential is

**(3.4)**

`partial_t Psi_tilde = Psi_t(t,T) + r(t,T)^T Tt`

`                    = Psi_t o T + p_frame`.

Along the actual normalized trajectory,

`d/dt Psi_tilde(t,z(t))`

`= partial_t Psi_tilde + (grad_z Psi_tilde)^T u`

`= Psi_t o T + p_frame + q^T u`.

Using (2.2), we obtain the main identity:

**(3.5) MOVING-CHART CONSERVATIVE POWER IDENTITY**

`r^T v = d/dt Psi_tilde - Psi_t o T`.

This is exactly the same remainder as in physical coordinates.

### Important consequence

If the physical potential is autonomous, `Psi_t=0`, then **an arbitrarily moving chart does not create a real conservative-power defect**. The two chart-generated pieces

- `partial_t Psi_tilde`, and
- `p_frame=r^T Tt`

cancel in the correct signed chain. Any nonzero “chart slew cost” obtained by dropping `p_frame` is an adapter artifact, not physics.

---

## 4. Storage shaping commutes with the moving chart

Suppose the physical energy ledger is

**(4.1)**

`Edot <= -D + p_other + r^T v`,

with `D>=0`.

Define the reshaped storage in normalized coordinates by

**(4.2)**

`V := E - Psi_tilde + C`,

where `C` is time independent.

Using (3.5),

`Vdot = Edot - d/dt Psi_tilde`

`     <= -D + p_other - Psi_t o T`.

Therefore:

**(4.3) CHART-INVARIANT STORAGE-SHAPING LEDGER**

`Vdot <= -D + p_other - Psi_t o T`.

The conservative-channel preprocessing rule from T-P5-119 is therefore coordinate invariant when the force is transported as a work covector and the frame power is retained.

If `Psi_t=0`, the channel consumes zero generic residual budget in every smooth moving chart for which the same trajectory/source identities are valid.

---

## 5. Why `J^T r` alone is insufficient in a moving chart

If one keeps only the normalized generalized-force power `q^T u`, then from (3.3)-(3.4)

**(5.1)**

`q^T u = d/dt Psi_tilde - partial_t Psi_tilde`

`      = d/dt Psi_tilde - Psi_t o T - p_frame`.

So `q^T u` is not the physical power unless `p_frame=0`.

This gives a strict typed boundary:

- for a time-independent chart, `Tt=0`, so `p_frame=0` and `q^T u=r^T v`;
- for a moving chart, the normalized force packet must carry either `p_frame` or an equivalent exact full-power identity.

A checker that knows `q=J^T r` but has no `Tt`/frame-power binding cannot reuse T-P5-119's physical storage-shaping conclusion.

---

## 6. Hard obstruction A: dropping frame power loses an O(1) term

Take one dimension:

`T(t,z)=z+t`,

`J=1`, `Tt=1`,

`Psi(x)=x`, `r=1`.

Choose the normalized trajectory `z(t)=0`, hence `u=0`. Then

`x(t)=t`, `v=1`.

The true physical power is

`r v = 1`.

The pulled generalized force is

`q=J^T r=1`,

but

`q u = 0`.

The missing frame power is exactly

`p_frame=r Tt=1`.

Also `Psi_tilde(t,0)=t`, so `d/dt Psi_tilde=1`, exactly matching the **full** power and not `q u` alone.

Thus omitting the moving-frame power is a first-order/exact error, not a second-order curvature remainder that can be hidden in T-P5-112/116.

---

## 7. Hard obstruction B: a force covector is not a tangent vector

Take the static one-dimensional scaling chart

`x=T(z)=2z`, so `J=2`,

and a constant physical force `r=1`. Let `u=1`, so the physical velocity is `v=2`.

True power:

`r v = 2`.

Correct force pullback:

`q=J^T r=2`, hence `q u=2`.

If one incorrectly reuses the tangent-vector rule from T-P5-095 and solves

`J c=r`,

one gets `c=1/2`, and the fake normalized pairing would be only `c u=1/2`.

So the two object types differ by a factor four in this elementary example. A source-to-math adapter must not use one generic “coordinate transform” field for both vector dynamics and generalized forces.

---

## 8. Gyroscopic zero-power cancellation also needs the full split

T-P5-119 also isolates physical gyroscopic channels

`r_g = G v`, `G^T=-G`,

for which

`v^T r_g = v^T G v = 0`.

Under a moving chart, define

`q_g = J^T r_g`,

`p_frame,g = r_g^T Tt`.

Then (2.2) gives

**(8.1)**

`q_g^T u + p_frame,g = 0`.

The two terms need not vanish separately.

Exact two-dimensional example:

`G = [[0,-1],[1,0]]`,

`J=I`, `Tt=e1`, `u=e2`, so `v=e1+e2`.

Then

`r_g=Gv=(-1,1)`,

`q_g^T u=1`,

`p_frame,g=-1`.

Their sum is exactly zero.

Therefore a moving-chart source adapter must form the signed total work before taking absolute enclosures. Bounding `q_g^T u` and `p_frame,g` independently would manufacture a nonzero disturbance budget from a physically zero-power channel.

---

## 9. Nonlinear-chart derivative interface

If a downstream source consumer needs the Jacobian of the pulled generalized force rather than only its potential, let

`A = D_x r`.

For a direction `eta`, differentiating `q=J^T(r o T)` gives

**(9.1)**

`D_z q[eta]`

`= (D_z J[eta])^T r + J^T A (J eta)`.

The first term is a genuine chart-Hessian/connection term. For `r=grad_x Psi`, the whole expression is exactly

`Hess_z(Psi o T)[eta]`.

Hence the full Jacobian is symmetric when it is the Hessian of a scalar potential, but a source that wants numerical derivative equality cannot silently replace it by `J^T A J` on a nonlinear chart.

A cleaner interface is often to transport the potential itself and prove (3.3), thereby avoiding a separately reconstructed Hessian whenever the consumer only needs conservative-power cancellation.

---

## 10. Spacetime one-form formulation

The preceding identities can be compressed into one geometric formula.

The physical work one-form is

`r^T dx`.

If `r=grad_x Psi`, then

`r^T dx = d Psi - Psi_t dt`.

Under the spacetime map

`Phi(t,z)=(t,T(t,z))`,

its pullback is

**(10.1)**

`Phi^*(r^T dx)`

`= (J^T r)^T dz + (r^T Tt) dt`

`= d(Psi o Phi) - (Psi_t o Phi) dt`.

This is the conceptual reason the physical `Psi_t` remainder is chart invariant. The correct adapter object is the full pulled-back work form, not merely its spatial coefficient `J^T r`.

---

## 11. Minimal source-facing packet

A source-to-math adapter that wants to consume T-P5-119 through a moving chart should bind, on one common point/tube key:

1. `T`, `J=D_zT`, and `Tt=partial_t T`;
2. the normalized velocity `u` and physical velocity identity `v=Tt+Ju`;
3. the actual signed force/residual `r` in the physical power ledger;
4. the generalized-force equality `q=J^T r`;
5. the frame-power equality `p_frame=r^T Tt` or the equivalent total-work equality `r^T v=q^T u+p_frame`;
6. an exact potential `Psi` with `grad_x Psi=r_cons` for the conservative subchannel;
7. `Psi_t` if the potential is explicitly time dependent;
8. a no-double-count statement removing `r_cons` from downstream generic residual packets after shaping.

For exact-rational affine/polynomial charts this packet uses only additions, multiplications, transpose, and exact equalities. No Jacobian inverse, square root, spectral norm, or eigenvalue is required.

The tangent-vector packet from T-P5-095 and this force-covector packet should remain distinct typed structures even when they share the same chart key.

---

## 12. Suggested Lean leaves

The source-independent formalization can be decomposed into small leaves:

```text
moving_chart_velocity_chain:
  v = Tt + J*u.

force_covector_pullback_power:
  q = J^T*r -> v=Tt+J*u
  -> <r,v> = <q,u> + <r,Tt>.

conservative_force_pullback_gradient:
  grad_x Psi = r
  -> grad_z (fun z => Psi (T z)) = J^T*r.

moving_chart_pulled_potential_time_derivative:
  grad_x Psi=r
  -> partial_t(Psi(t,T(t,z))) = Psi_t + <r,Tt>.

moving_chart_conservative_power_identity:
  q=J^T*r, v=Tt+J*u, grad_x Psi=r
  -> <r,v> = d/dt(Psi(t,T(t,z(t)))) - Psi_t.

storage_shaping_commutes_with_moving_chart:
  Edot <= -D + pOther + <r,v>, grad_x Psi=r
  -> d/dt(E-Psi(t,T(t,z))+C) <= -D + pOther - Psi_t.

moving_chart_gyroscopic_total_power_zero:
  r=G*v, G^T=-G, q=J^T*r, v=Tt+J*u
  -> <q,u> + <r,Tt> = 0.
```

The purely algebraic power-split and gyroscopic leaves are especially suitable for a first Lean sidecar; the chain-rule leaves can remain premise-driven so they do not require rebuilding the deployed differential geometry.

---

## 13. Open boundaries / non-claims

T-P5-120 is **CONDITIONAL_PASS / pending mathematical-interface child** only.

Still open:

- whether the actual deployed P5 force/residual channel is bound as a covector/work channel rather than a state-vector field;
- the actual moving chart `T/J/Tt`, physical/normalized velocity identity, and common source/tube key;
- exact source equality for any proposed `Psi`, `r_cons`, or gyroscopic `G`;
- whether the deployed controller/FD/solve decomposition preserves the signed frame-power cancellation before intervalization;
- positivity/coercivity and threshold normalization of the reshaped storage from T-P5-119;
- same-domain/path/FD/reference halo coverage;
- Float64/runtime semantics, P8 flowpipe, Lean/kernel, independent verifier 封不觉, admission and registry.

The mathematical advance is the missing object-typed coordinate bridge: **state perturbations transform as tangent vectors, force channels transform as covectors, and in a moving chart the frame-power term is part of the exact work form.** Once that term is retained, conservative storage shaping and gyroscopic zero-power cancellation remain exact and do not acquire artificial chart-motion budgets.
