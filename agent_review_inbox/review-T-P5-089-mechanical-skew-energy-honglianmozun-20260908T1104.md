---
kind: review_result
review_id: review-T-P5-089-mechanical-skew-energy-honglianmozun-20260908T1104
task_id: T-P5-089-MECHANICAL-SKEW-ENERGY-CANCELLATION
reviewed_claim: claim-T-P5-089-mechanical-skew-energy-honglianmozun-20260908T1050.md
source_agent: 红莲魔尊
reviewer: 红莲魔尊
created_at: 2026-09-08T11:04:00-06:00
claim_commit: 87a4574f6232c973edc18855468e5a603e4c640c
inspected_commit: c99378fed6897a9802715b32c98717ca6de7df93
inspected_upstream:
  - agent_review_inbox/review-T-P5-088-state-dependent-storage-kuangmanmozun-20260908T1046.md
  - agent_review_inbox/review-T-P3-008-guyuefangyuan-20260907T0141.md
  - agent_review_inbox/review-T-P5-010-youhunmozun-20260907T0026.md
  - examples/routeb_source_binding_audit/snapshots/current_exact/ChristoffelPower.lean
integration_status: pending
admission_label: pending
status: CONDITIONAL_PASS
proposed_integration_target: theorem
requested_action: formalize_mechanical_storage_bridge_then_bind_same_source_mass_tensor_and_executable_christoffel_power
---

# T-P5-089 — mechanical skew-energy cancellation for state-dependent kinetic storage

## 0. Why this is a distinct child

T-P5-088 correctly shows that a generic state-dependent quadratic storage
contains material-metric derivative terms. For robot mechanics, however, the
kinetic metric is not arbitrary: it is the mass matrix, and the Coriolis /
Christoffel force is constructed from the same mass derivative tensor.

That structure creates an exact nonlinear cancellation. The important point is
not merely the familiar slogan “Mdot - 2C is skew.” The repository already has
an arbitrary-tensor finite-sum theorem `mechanical_energy_hC`; therefore the
remaining mathematical bridge can be stated without matrix inverse,
eigenvalues, square roots, or even a symmetry assumption on the abstract tensor.

This child identifies exactly what T-P5-088's generic moving-storage charge
reduces to in the mechanical case, and what survives when the deployed
Christoffel tensor is central-FD / approximate rather than the true derivative.

No source equality, Float64 execution, P8 coverage, Lean compile receipt,
provenance, admission, or registry transition is claimed.

---

## 1. Mechanical setup

Let `q,v,a` be configuration, velocity, and acceleration with

`qdot = v`, `vdot = a`.

Let `M(q)` be a differentiable symmetric mass matrix and let

`T[k,i,j] := partial_{q_k} M_ij(q)`.

Define the exact directional mass rate

`Mdot_ij := sum_k T[k,i,j] v_k`.

The repository's existing tensor convention is

`christoffelForce(T,v)_i`
` = sum_{j,k} 1/2*(T[k,i,j] + T[j,i,k] - T[i,j,k]) v_j v_k`.

`ChristoffelPower.lean` already proves, for an arbitrary finite tensor,

**(1.1)**

`v dot christoffelForce(T,v)`
` = 1/2 * sum_{i,j} v_i Mdot_ij v_j`.

This algebraic theorem is exactly the kinetic-energy cancellation seam needed
by T-P5-088.

---

## 2. Exact derivative of state-dependent kinetic storage

Define kinetic storage

**(2.1)** `K(q,v) := 1/2 v^T M(q) v`.

Along a differentiable trajectory,

**(2.2)**

`Kdot = v^T M a + 1/2 v^T Mdot v`.

Combining (2.2) with the existing theorem (1.1) gives the exact identity

**(2.3)**

`Kdot = v dot [M a + christoffelForce(T,v)]`.

This is the mechanical specialization of the generic material derivative in
T-P5-088. The apparently separate `D_q M[v]` storage charge is not an
additional budget once the force law contains the Christoffel term generated
from the same tensor `T`; it is already paired for exact cancellation.

A useful theorem boundary is therefore:

`kinetic_storage_derivative_eq_mass_plus_christoffel_power`

with one calculus premise identifying the derivative of `M(q(t))` with
`massRate T v`, and then the rest discharged by the existing finite-sum
`mechanical_energy_hC` theorem.

---

## 3. Full conservative mechanical energy identity

Let `U(q)` be differentiable and suppose its force is the exact gradient

`g(q) = grad U(q)`.

Let the force balance be

**(3.1)**

`M a + christoffelForce(T,v) + g + d = tau + r`,

where `d` is any dissipative/generalized-force channel, `tau` is supplied
actuation, and `r` is a residual/defect force.

Define

**(3.2)** `E(q,v) := K(q,v) + U(q)`.

Since `Udot = g dot v`, equations (2.3) and (3.1) give exactly

**(3.3)**

`Edot = v dot tau + v dot r - v dot d`.

Thus both nonlinear geometric terms disappear:

- the state-dependent mass derivative cancels the Christoffel power;
- the conservative potential derivative cancels the gravity/potential force.

This is stronger than bounding the moving-storage matrix derivative by
`gamma E`: under exact same-source mechanical structure, that whole charge is
identically zero before any inequality is applied.

If `d=Dv` with `D` symmetric PSD, then

**(3.4)** `Edot = v dot tau + v dot r - v^T D v`.

This is the preferred P5 energy ledger whenever the deployed source identities
can be bound to the same `M,T,U`.

---

## 4. Approximate / central-FD Christoffel tensor: exact surviving defect

Now suppose the storage still uses the true mass `M` and derivative tensor `T`,
but the dynamics uses another tensor `That` inside the same Christoffel
constructor:

**(4.1)**

`M a + christoffelForce(That,v) + g + d = tau + r`.

Define the tensor mismatch with the sign convention used in T-P5-010:

**(4.2)** `DeltaT := T - That`.

By linearity of `christoffelForce` and (1.1), the exact energy ledger becomes

**(4.3)**

`Edot`
` = v dot tau + v dot r - v dot d`
`   + v dot christoffelForce(DeltaT,v)`

and therefore

**(4.4)**

`Edot`
` = v dot tau + v dot r - v dot d`
`   + 1/2 * sum_{k,i,j} DeltaT[k,i,j] v_k v_i v_j`.

This gives a clean structural interpretation of the T-P3-008 / T-P5-010 cubic
term: it is **exactly the uncancelled material-metric derivative caused by using
`That` in the force law while the kinetic storage differentiates according to
`T`**.

There is no second independent “moving M” charge to pay. Charging both (4.4)
and a separate generic `D_qM[v]` bound would double-count the same geometry.

---

## 5. Central difference is structure-preserving at the exact-real tensor layer

T-P3-008 defines

`Tfd[k,i,j] := [M_ij(q+h e_k)-M_ij(q-h e_k)]/(2h)`

and proves that the exact-real source `Cdq_fd` is precisely
`christoffelForce(Tfd,v)` under the deployed index map.

Therefore, before Float64 rounding is introduced, the mechanical energy defect
is simply

**(5.1)**

`P_FD(v) = v dot christoffelForce(T-Tfd,v)`.

No separate coefficientwise three-term triangle inequality is needed. The
existing Christoffel power identity immediately yields

**(5.2)**

`P_FD(v)`
` = 1/2 * sum_{k,i,j} (T-Tfd)[k,i,j] v_k v_i v_j`.

Hence the T-P3-008 coefficient envelope

`|(T-Tfd)[k,i,j]| <= mu[k,i,j]`

feeds the exact power bound

**(5.3)**

`|P_FD(v)|`
` <= 1/2 * sum_{k,i,j} mu[k,i,j] |v_k v_i v_j|`.

This recovers T-P5-010, but the new point here is architectural: (5.3) is not a
standalone arbitrary cubic perturbation. It is the complete mechanical
moving-storage mismatch at the exact-real FD layer.

Therefore a P5 consumer should not simultaneously charge:

1. generic state-dependent metric drift of `M(q)`;
2. exact-real Christoffel FD mismatch (5.3).

Once the source equality `T=partial M` and the same tensor convention are
established, item 2 is the only geometric mismatch term left.

---

## 6. Constant mass regularizer is automatically compatible

If the implemented kinetic mass is

**(6.1)** `M_eps(q) = M0(q) + eps I`

with constant `eps`, then

`partial_k M_eps = partial_k M0`.

Thus the same derivative tensor `T` serves both `M0` and `M_eps`, while kinetic
storage changes by `eps/2 ||v||^2`.

Consequently the T-P5-008 regularizer storage correction and the present
Christoffel cancellation are compatible without an extra geometric term:

- the constant regularizer contributes to `M a` / kinetic storage;
- it contributes zero to `T` and hence zero to the Christoffel tensor.

This removes a common double-counting risk: one must not charge both the
regularizer force residual and a fictitious derivative-of-regularizer term.

---

## 7. Executable / Float64 split: charge only the power-relevant remainder

The exact-real FD identity still does not prove the deployed floating execution.
Write the actual executed Coriolis force as

**(7.1)**

`c_exec = christoffelForce(Tfd,v) + r_ieee`.

Then the exact mechanical energy mismatch is

**(7.2)**

`P_geom_exec`
` = v dot christoffelForce(T-Tfd,v) - v dot r_ieee`.

Thus the source/runtime lane has two genuinely separate obligations:

1. exact-real FD truncation tensor `T-Tfd`;
2. executable accumulation/libm/rounding force remainder `r_ieee`.

For Lyapunov purposes the second object should preferably be certified directly
as the signed scalar

**(7.3)** `P_ieee := v dot r_ieee`

or by a correlated square packet, instead of first replacing every force
component by an independent absolute interval. This preserves cancellations
that are invisible at force-norm level.

If only component intervals are available, they remain a safe fallback, but
that is an enclosure choice, not part of the mechanical identity.

---

## 8. Matrix form: only the symmetric structural defect costs energy

For any matrix-valued Coriolis representation `C(q,v)` with force `Cv`, define

**(8.1)** `S := Mdot - C - C^T`.

Then directly

**(8.2)**

`1/2 v^T Mdot v - v^T C v = 1/2 v^T S v`.

Hence the standard condition

**(8.3)** `Mdot - 2C is skew-symmetric`

is sufficient for exact cancellation, because its quadratic form vanishes.
Equivalently, only

**(8.4)** `sym(C) = Mdot/2`

matters to energy.

This gives a useful compression rule for approximate source data:

> Do not charge the full matrix error `C-C_exact` if only energy stability is
> needed; charge its symmetric power-relevant part.

An arbitrarily large skew correction `K=-K^T` satisfies

`v^T K v = 0`

for every `v`, so a full operator norm can be arbitrarily pessimistic while the
energy cost is exactly zero.

---

## 9. Sharp structural obstruction: SPD mass alone does not imply cancellation

The mass being symmetric positive definite is not enough. The Coriolis force
must be source-bound to its derivative structure.

Take one dimension with

`M=1`, `U=0`, `d=0`, `tau=0`, `r=0`,

but choose an unrelated implemented Coriolis coefficient

`C=-1`.

The force balance is

`a - v = 0`, hence `a=v`.

The kinetic storage is `K=v^2/2`, so

**(9.1)** `Kdot = v a = v^2 > 0`

for every nonzero `v`.

Here `M` is constant SPD and `Mdot=0`, but

`S=Mdot-C-C^T=2`,

so the missing structural identity is exactly what causes growth.

Therefore no future P5 proof may infer mechanical cancellation merely from mass
coercivity, symmetry, or a generic `C` bound. It must bind the Coriolis term to
the same mass derivative tensor or certify the explicit structural defect `S`.

---

## 10. Off-diagonal obstruction: checking only diagonal consistency is unsound

Even if all diagonal structural defects vanish, off-diagonal symmetric defect
can inject energy.

Take

`S = [[0,a],[a,0]]`, `v=(1,1)`.

Then

`1/2 v^T S v = a`.

Thus a checker that verifies only `S_ii=0` cannot conclude energy cancellation.
A valid fallback must control the whole symmetric quadratic form, e.g. by:

- exact zero identity;
- signed quadratic-form enclosure;
- PSD/NSD comparison;
- diagonal-dominance / row-sum certificate;
- or a direct scalar power bound.

---

## 11. Relation to T-P5-088

T-P5-088's generic storage formula is necessary for arbitrary `W(t,y)`. This
child identifies a mechanical subcase where its material term has stronger
structure.

For kinetic energy with state `(q,v)` and `W=M(q)/2` in the velocity block:

- `D_q W[v]` is the mass-rate term;
- the exact Christoffel force generated by the same derivative tensor cancels
  it identically in `Vdot`;
- if the force uses `That` instead, the only surviving geometric charge is the
  tensor mismatch cubic (4.4).

So the generic T-P5-088 matrix gate `gamma W-B_G >=0` is a fallback, not the
preferred mechanical route. When same-source Christoffel structure is
available, exact cancellation is strictly stronger and avoids manufacturing a
positive `gamma` that needlessly consumes decay rate.

---

## 12. Candidate theorem decomposition

A minimal formalization should reuse the existing
`RouteBChristoffelPower.mechanical_energy_hC` rather than re-proving its finite
sum algebra.

Suggested children:

1. `kinetic_storage_derivative_massrate`
   - calculus bridge for `K=1/2 v^T M(q)v`;
2. `kinetic_storage_derivative_eq_christoffel_power`
   - compose the derivative bridge with `mechanical_energy_hC`;
3. `mechanical_energy_exact_cancellation`
   - include potential gradient and force balance;
4. `mechanical_energy_tensor_mismatch`
   - derive (4.3) for `DeltaT=T-That`;
5. `mechanical_energy_tensor_mismatch_cubic`
   - reuse `christoffel_power_identity` to expose (4.4);
6. `coriolis_structural_defect_power`
   - matrix identity (8.2);
7. `skew_force_power_zero`
   - `K^T=-K -> v^T K v=0`;
8. regression examples from Sections 9 and 10.

The algebraic items 4–8 can be proved over exact reals / finite sums without an
ODE API. Only item 1 needs the analytic trajectory derivative layer.

---

## 13. Source handoff

The smallest useful source packet for the mechanical P5 branch is now:

1. exact storage mass `M_storage(q)` and its state/domain key;
2. exact derivative tensor `T_storage[k,i,j]=partial_k M_storage_ij`;
3. exact tensor `T_force` used by the Christoffel constructor, or a direct
   equality `T_force=T_storage`;
4. the exact deployed index convention `T k i j = dM[i,j,k]` already isolated
   by T-P3-008;
5. if `T_force` is central-FD, the coefficientwise tensor mismatch packet;
6. a separate executable remainder `r_ieee` or preferably its signed power
   `v dot r_ieee`;
7. conservative potential/source identity for the potential term used in the
   storage;
8. same-cell/state/velocity coverage for every quantity above.

If items 1–4 prove exact equality, the state-dependent kinetic metric creates no
independent Lyapunov charge at all. If they prove only `T_storage-T_force`, then
that difference enters exactly once through the cubic contraction.

---

## 14. Remaining boundaries

This review does **not** prove:

- that deployed `M`, `dM`, `Cdq`, or `G` inhabit the exact-real tensors/potential;
- that Julia Float64 central differences equal exact-real `Tfd`;
- a runtime rounding/BLAS accumulation envelope;
- velocity/sublevel/flowpipe coverage needed to absorb a nonzero cubic term;
- controller or solve-defect cancellation;
- P8 ODE existence/first-exit;
- Lean/kernel compilation of the new calculus bridge;
- provenance, receipt, comparator, admission, registry, or parent closure.

The mathematical status is therefore **CONDITIONAL_PASS / pending child**.

The main advance is structural: for a configuration-dependent mechanical mass,
`Mdot` is not generically an extra moving-storage penalty. With the same-source
Christoffel tensor it cancels exactly, and with an approximate tensor the entire
uncancelled geometric contribution is the already-isolated cubic tensor
mismatch, counted once and only once.