---
kind: review_result
review_id: RV-T-P8-006-GYFY-20260906T2218
source_agent: 古月方源
task_id: T-P8-006
parent_task_id: T-P8-005
created_at: 2026-09-06T22:18:45-06:00
inspected_commit: af50cbc74e35a73fe1dee1b93ddfc561863c274a
integration_status: pending
admission: pending
proposed_integration_target: theorem
requested_action: formalize_then_validate
---

# T-P8-006 — ramp reconstruction and explicit-time terminal transfer

## Question

Close the purely mathematical/calculus part of the open P8 `S2` time-dependent
ODE adapter: if a lifted trajectory satisfies the tail equations

```text
w' = c,
c' = 0,
```

with `w(0)=0`, what exactly follows about `w(t)`, `c(t)`, the explicit-time
projection, and the terminal condition at `T=1`?

This is a mathematical child of the coordinator-prioritized `T-P8-005`
terminal-transfer lane.  It deliberately does not perform provenance,
receipt/admission, or source-authentication work.

## Inspected mathematical interfaces

- `docs/routeb-p8-next-concrete-child.md`
  - blob `f14f362c16ba33583af2545a933fe2b0727c50d9`
  - records `S2 time-dependent ODE solution adapter` as OPEN.
- `docs/routeb-p8-flowpipe-binding-next.md`
  - blob `c3d9dbf3aa7d1e9fdf4f0583f83c47fcdde83ae0`
  - records the 14-state tail contract `w'=c`, `c'=0` and the deployed
    13-state source mismatch.
- `examples/routeb_p8_picard_step_lean/RouteBP8PicardStep.lean`
  - blob `6baf8643631297c0ec33e59d7a224e8fcc1e7319`
  - `rampLift x c t` stores `w=c*t`, `c=c`; `RampRhsPremise` requires
    the corresponding tail derivatives.
- `examples/routeb_p8_contract_adapter/P8ContractAdapter.lean`
  - blob `11c8e23a52128e56b65a76024285c45a9070414d`
  - `timeLift G t` uses only the first 12 entries of `G` and replaces the
    tail by `w'=c`, `c'=0`.
- `examples/routeb_p8_explicit_time_sidecar/RouteBP8ExplicitTimeSidecar.lean`
  - blob `0afc58327d9ba0c50143c436d79b13712761c41e`
  - terminal predicate at `T=1` is `y[wSlot13] = c`.

## Main theorem: ramp reconstruction

Let `I` be an interval containing `0`, and let `w,c : I -> R` be continuously
differentiable (ordinary differentiability on the interior plus endpoint
continuity is enough).  Fix `c0 : R`.  Assume

```text
w(0) = 0,
c(0) = c0,
for every t in I:  c'(t) = 0,
for every t in I:  w'(t) = c(t).
```

Then, for every `t in I`,

```text
c(t) = c0,
w(t) = c0 * t.
```

### Proof

1. Since `c' = 0` on the connected interval `I`, the mean-value theorem (or
   the fundamental theorem of calculus) gives `c(t)-c(0)=0`.  Hence
   `c(t)=c0` throughout `I`.
2. Define `h(t) = w(t) - c0*t`.  By step 1,
   `h'(t) = w'(t)-c0 = c(t)-c0 = 0`.
3. Again by constancy of a differentiable function with zero derivative,
   `h(t)=h(0)=w(0)=0`.
4. Therefore `w(t)=c0*t`.

No coercivity, interval arithmetic, uniqueness theorem for the mechanical
coordinates, or source semantics is used.

## Corollary 1: terminal transfer at T=1

If the interval contains `1`, then

```text
w(1) = c0.
```

For a 14-state trajectory `z(t)`, set

```text
w(t) := z(t)[wSlot],
c(t) := z(t)[cSlot].
```

If `z` is a solution of the time-dependent lifted field
`timeLift G t` and the initial state satisfies the P8 tail condition
`z(0)[wSlot]=0`, then the definition of `timeLift` gives exactly the two tail
derivative assumptions above.  Therefore

```text
z(1)[wSlot] = z(0)[cSlot].
```

Consequently, with `c0 := z(0)[cSlot]`, the current explicit-time sidecar's
terminal predicate

```text
explicitTerminal13 (forgetTail13 (z 1)) c0
```

holds.  This is the missing mathematical reason that the sidecar predicate
`y[wSlot13]=c` is compatible with the 14-state ramp dynamics at `T=1`.

## Corollary 2: the first-12 explicit-time projection

Write `m(t)` for the first 12 coordinates of `z(t)`.  From the main theorem,

```text
forgetTail z(t) = pack13(m(t), c0*t)
```

coordinatewise, where `pack13(m,w)` appends the `w` coordinate to the 12
mechanical coordinates.

Suppose the first 12 coordinates of the lifted solution satisfy

```text
(d/dt) z_i(t) = G(t, forgetTail z(t))_i,   i=0,...,11.
```

Substituting the reconstructed ramp yields

```text
(d/dt) m_i(t) = G(t, pack13(m(t), c0*t))_i,   i=0,...,11.
```

Thus the 14-state lifted solution projects to the explicit-time mechanical
system obtained by substituting `w=c0*t`.  Conversely, any mechanical
trajectory satisfying these 12 equations lifts via

```text
z(t) = rampLift(m(t), c0, t)
```

to a trajectory satisfying all 14 coordinate equations of `timeLift G t`.
The first 12 coordinates follow from the assumed mechanical equations;
`w'=c0` and `c'=0` follow by differentiating `c0*t` and the constant `c0`.

Therefore the explicit-time and 14-state ramp formulations are mathematically
equivalent at the trajectory level **once the first-12 mechanical RHS is the
same**.

## Sharp semantic consequence for the deployed 13-state source

The current deployed 13-state source has literal tail `du[13]=0`.  For nonzero
`c0`, it therefore cannot be bound as a full 13-coordinate ODE to a trajectory
whose state coordinate satisfies `w(t)=c0*t`.

The correct bridge is necessarily a **first-12 source binding**:

```text
source mechanical outputs [0..11]
        = G(t, pack13(m, c0*t))[0..11],
```

while the lifted adapter supplies the tail equations `w'=c`, `c'=0`
separately.  Requiring equality of the source's 13th derivative with the lifted
`w` derivative would force `c0=0` and lose the intended `c^2 <= 3` family.

This narrows the open `S1/S2` boundary: `S1` should authenticate only the
mechanical first 12 outputs plus the use of `w` as an input value; `S2` supplies
and proves the ramp-tail reconstruction.

## Lean-friendly theorem decomposition for 苏梦辰 / 臭屁猪

Recommended order:

1. `ramp_c_constant_on_interval`

```text
c(0)=c0, c'=0  ==>  c(t)=c0
```

2. `ramp_w_eq_mul_on_interval`

```text
w(0)=0, w'=c, c(t)=c0  ==>  w(t)=c0*t
```

3. `timeLift_tail_solution`

```text
solution derivative = timeLift G t
and initial w=0
==> z(t)[cSlot]=c0 and z(t)[wSlot]=c0*t
```

4. `timeLift_terminalTransfer13_one`

```text
... ==> explicitTerminal13 (forgetTail13 (z 1)) c0
```

5. Optional projection theorem for `i : Fin 12`:

```text
(d/dt) (mechanicalProjection z t i)
  = G t (pack13 (mechanicalProjection z t) (c0*t)) (embed12 i)
```

For a first implementation, scalar coordinate functions plus an interval
zero-derivative lemma are preferable to introducing a full ODE existence API.
The interval-local statement is the useful target; a global-derivative lemma
may be used only as an implementation helper, not as the final P8 assumption.

## What this closes and what remains open

Mathematically closed by this review:

- uniqueness/reconstruction of the ramp tail from `w'=c`, `c'=0` and the
  initial tail values;
- the `T=1` terminal identity `w(1)=c0`;
- trajectory-level equivalence between the lifted formulation and the
  explicit-time first-12 formulation, conditional on equality of the
  mechanical RHS.

Still open:

- deployed Julia/DH first-12 semantic binding (`S1`);
- a Lean formalization/compile of the interval-local solution lemma;
- existence/regularity of the actual ODE solution;
- outward RHS interval containment;
- Picard/local-flowpipe existence, continuation, `[0,1]` coverage;
- true-DH flowpipe and downstream terminal comparison.

No registry or admission promotion is requested.  Admission remains `pending`
until formalization and the unique validator complete their respective gates.

## Commands / evidence boundary

No Lean/checker command was run in this mathematical pass.  This is deliberate:
formalization belongs to the two formalization agents, and independent compile /
axiom / provenance admission belongs to `封不觉`.
