---
task_id: T-P4-030
agent: 红莲魔尊
source_agent: 红莲魔尊
status: pending
result: mathematical_child
created_at: 2026-09-08
scope: dissipation/co-state algebra only
dependencies:
  - agent_review_inbox/task_queue.md fixed Route-B sign convention
  - artifacts/task_routeb_o1_lean_api_audit_20260907/RouteBO1PortIdentity.lean (read-only API dependency; not edited)
claim_file: agent_review_inbox/claim-T-P4-030-honglianmozun-20260908T0255.md
---

# Review result — T-P4-030

## 1. Fixed convention and lane boundary

This child uses the coordinator-fixed convention

- `D := ΔM_DB = M_DF - M_BF`,
- `g := Cs/2`,
- `R_port := -g D`,
- `R_gain := +g D = -R_port`.

No alternative positive-prefactor definition of `R_port` is used anywhere below.

This review covers only the mathematical propagation into signed co-state/multiplier power and quadratic Lyapunov/dissipation consumers. It does **not** edit the typed theorem/API adapter lane owned by Mercurius and does **not** claim the wider Route-B residual package complete.

## 2. Exact port/gain involution

The corrected convention immediately gives the exact involution

`R_gain = -R_port`.

Therefore the orientation change `port -> gain` is the scalar sign involution `S=-1`, with `S^2=1`.

This simple identity has two very different consequences depending on whether the downstream consumer is odd or even in the residual.

## 3. Signed co-state power: same co-state flips the power

Let `λ` be any scalar co-state or multiplier and define

`P_port := λ R_port`,

`P_gain := λ R_gain`.

Then

`P_port = -(Cs/2) λ D`,

`P_gain = +(Cs/2) λ D = -P_port`.

Hence a downstream consumer that switches from `R_port` to `R_gain` while keeping the **same** co-state coefficient must flip the signed linear power.

### Exact obstruction to same-co-state invariance

If one tries to assert simultaneously

`λ R_port = λ R_gain`,

then, since `R_gain=-R_port`, one obtains

`2 λ R_port = 0`,

or equivalently

`Cs λ ΔM_DB = 0`.

Thus away from the degenerate locus `Cs λ ΔM_DB=0`, same-co-state invariance of the signed power is mathematically impossible. This is an exact obstruction, not a looseness of an estimate.

## 4. Correct co-state transformation: contragredient sign flip

To preserve the physical bilinear contraction under the representation change, transform the co-state by the same sign involution:

`λ_gain := -λ_port`.

Then

`λ_gain R_gain`
`= (-λ_port)(-R_port)`
`= λ_port R_port`.

So the correct representation-invariant statement is

**joint residual/co-state sign flip preserves the pairing**.

In scalar form:

`(-λ)(-r) = λ r`.

In vector form, the same mechanism is: for any orthogonal sign involution `S` with `S^T S=I`, if

`r' = S r`, `λ' = S λ`,

then

`(λ')^T r' = λ^T r`.

The Route-B port/gain conversion is exactly the one-dimensional case `S=-1`.

## 5. Quadratic Lyapunov/dissipation consumers are orientation-invariant

Because the port/gain change is a sign flip,

`R_gain^2 = R_port^2 = (Cs^2/4) D^2`.

Therefore, for every `a >= 0`,

`-a R_gain^2 = -a R_port^2 <= 0`.

More generally, any consumer depending only on `|R|`, `R^2`, or the scalar norm is blind to the port/gain orientation.

This yields an important fail-closed warning: a sign error in an **unsquared** residual API can be completely hidden by a downstream square/norm-only energy check. Correctness of the quadratic dissipation term is therefore not evidence that the signed co-state convention is correct.

## 6. Affine-quadratic Lyapunov consumer: exact parity decomposition

Consider the scalar affine-quadratic consumer

`F(r) := c + l r + q r^2`.

Under the port/gain orientation change `r -> -r`,

`F(-r) = c - l r + q r^2`,

hence

**`F(-r) - F(r) = -2 l r`.**

Thus:

- the even part `c + q r^2` is orientation-invariant;
- the odd linear part `l r` changes sign;
- if the paired multiplier is also transformed `l -> -l`, then the complete affine-quadratic scalar is invariant.

This is the exact structural fingerprint downstream consumers should implement: every odd residual factor changes orientation; its paired co-state/multiplier coefficient must transform contragrediently if the represented scalar is intended to remain unchanged.

## 7. General polynomial parity rule

For a polynomial consumer

`F(r) = Σ_n a_n r^n`,

port/gain conversion gives

`F(-r) = Σ_n (-1)^n a_n r^n`.

Hence all even-degree residual contributions are unchanged and all odd-degree contributions flip. The same rule applies termwise to a local Taylor/energy expansion. This separates sign-sensitive co-state terms from sign-insensitive dissipation terms without any positivity or magnitude assumptions on `Cs`.

## 8. Candidate theorem statements for the typed API lane

These are proposed mathematical statements only; this child does not edit Mercurius's Lean/API artifact.

1. `routeB_port_gain_opposite`
   - assumptions/definitions: `R_port = -(Cs/2)*D`, `R_gain = +(Cs/2)*D`
   - conclusion: `R_gain = -R_port`.

2. `routeB_port_gain_square_invariant`
   - conclusion: `R_gain^2 = R_port^2`.

3. `routeB_same_costate_power_flip`
   - conclusion: `λ*R_gain = -(λ*R_port)`.

4. `routeB_joint_costate_flip_invariant`
   - conclusion: `(-λ)*R_gain = λ*R_port`.

5. `routeB_same_costate_power_obstruction`
   - assumptions: `λ*R_gain = λ*R_port`
   - conclusion: `Cs*λ*D = 0`.

6. `routeB_affine_quadratic_consumer_parity`
   - conclusion: `(c + l*(-r) + q*(-r)^2) - (c + l*r + q*r^2) = -2*l*r`.

All six are ring-level identities; no spectral, floating-point, interval, provenance, or admission machinery is required for the mathematics.

## 9. Exact failure boundaries

### 9.1 Wrong port prefactor cannot coexist generically

If an API simultaneously states

`R_port = +(Cs/2)D`

and the fixed convention

`R_port = -(Cs/2)D`,

then subtraction yields

`Cs D = 0`.

Therefore both signs can coexist only on a degenerate locus; no generic theorem may expose both prefactor conventions.

### 9.2 Square-only consumers cannot detect the sign bug

Because `(-r)^2=r^2`, any proof that tests only quadratic residual magnitude has zero power to distinguish the two orientations. An unsquared signed theorem or typed orientation adapter is necessary whenever a co-state/multiplier term is consumed.

### 9.3 No sign assumption on `Cs` is needed for the algebra

The port/gain involution and all pairing/parity identities above hold for arbitrary real `Cs`. Positivity of `Cs` may be required by a later physical/dissipative interpretation, but it is not part of this sign-propagation child.

## 10. Remaining consumer-side binding gap

In the checked current Route-B artifact/API material, the exact real matrix/port identity is present, but I did not identify a typed downstream residual/co-state consumer theorem exposing `R_port`, `R_gain`, and the corresponding co-state orientation as a single API contract. Repository code search during this review also returned no indexed `R_port` / `co-state` consumer match.

Therefore this mathematical child closes the **algebraic sign/co-state propagation** only. The remaining integration obligation is to bind the typed source residual representation to one explicit orientation and, where an invariant physical co-state pairing is intended, apply the joint sign transformation above. That typed theorem/API adapter work remains in Mercurius's assigned lane.

## 11. Status

`pending mathematical child`.

Mathematical progress: exact corrected Route-B residual sign has been propagated through linear co-state power, quadratic dissipation, affine-quadratic energy, and the general parity rule, with explicit impossible branches recorded.

Not claimed here: typed source-to-consumer binding, wider Route-B residual completion, Float64 semantics, trajectory/coverage, provenance, receipt, audit, or admission.
