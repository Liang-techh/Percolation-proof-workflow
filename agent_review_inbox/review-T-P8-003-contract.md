---
kind: review_result
task_id: T-P8-003
source_agent: Codex
created_at: 2026-09-06T23:30:00-06:00
integration_status: pending
---

# T-P8-003 — freeze the state contract

## Scope and decision boundary

This is a read-only contract freeze audit for the current Route-B P8 leaf.
It only compares the deployed 13-state source contract against the existing
14-state ramp parent and the explicit-time 13-state fallback. No theorem
target, state registry entry, source file, or external project was modified.
No broad test run was performed.

The inspected evidence is the same contract layer already reflected in:

- `docs/routeb-p8-next-concrete-child.md`
- `docs/routeb-p8-flowpipe-binding-next.md`
- `examples/routeb_p8_picard_step_lean/RouteBP8PicardStep.lean`
- `examples/routeb_p8_contract_adapter/P8ContractAdapter.lean`
- `examples/routeb_p8_rhs_payload_generator/SOURCE_METADATA.json`
- `examples/routeb_p8_rhs_payload_generator/receipt.template.json`

## Freeze decision

Freeze the contract as follows:

- the deployed source is currently only a 13-state RHS with `w` as the last
  state and `c` as an open sidecar parameter;
- the existing 14-state parent is not directly instantiated by that source;
- the correct frozen decision is therefore a named explicit-time 13-state
  theorem family, unless the source itself is repaired into a genuine 14-state
  ramp RHS.

In other words, the current evidence supports “explicit-time 13-state parent
now” as the admission-safe freeze. The 14-state ramp parent remains the
preferred semantic target only if the source contract is later changed to
`w' = c, c' = 0`.

## Minimum theorem signature

The smallest semantically honest signature is an explicit-time 13-state one:

```text
State13 := Fin 13 → ℝ
F13 : ℝ → ℝ → State13 → State13

theorem explicit_time_flowpipe
  (F13 : ℝ → ℝ → State13 → State13)
  (x₀ : State13) (c : ℝ)
  (hinit : mechanicalEnergy13 x₀ ≤ 9/400 ∧ x₀[w] = 0 ∧ c^2 ≤ 3)
  (hbinding : ∀ t x, F13 t c x = source_rhs13 t c x)
  (hregular : ...)
  (hbox : ...)
  :
  ∃ y, solution13 F13 c x₀ y ∧
    ∀ t ∈ Set.Icc 0 1, y t ∈ certifiedTube13 t
```

If the source is later repaired into a genuine 14-state ramp RHS, the parent
signature can stay closer to the existing Lean scaffold:

```text
RampRhsPremise(F) := ∀ z, F z wSlot = z cSlot ∧ F z cSlot = 0
```

That 14-state form is not currently justified by the deployed source contract.

## Selection advice

Prefer the explicit-time 13-state contract for the current freeze. It matches
the deployed source shape and keeps the ramp parameter `c` explicit rather than
pretending it has been consumed by the RHS.

Keep the 14-state ramp parent only as the long-term semantic target if the
source is re-bound to a true 14-state ODE. The current source metadata and
payload template both record `julia_state_dimension = 13` and `ramp_binding =
OPEN`, so the 14-state parent cannot be treated as a drop-in theorem target.

## Initial-domain impact

The initial domain changes only in how it is quantified.

- In the 14-state parent, `c` lives in the state and the full initial set is a
  single `FullX0(z)` predicate.
- In the explicit-time 13-state contract, the initial set becomes a dependent
  family `X₀(c)`, with `c² ≤ 3` as an external parameter condition.

The mechanical ball itself should not change: keep the same `9/400` bound on
the 12 mechanical coordinates and `w(0) = 0`. What changes is the logical
shape of the quantifier. The 13-state version must prove both directions of the
state projection relation, not just a one-way forgetful map.

Concretely, the following transfer lemmas matter:

- `FullX0(z) → ExplicitInitial13(forgetTail z, z[c])`
- `ExplicitInitial13(x, c) → FullX0(rampLift x c 0)`

Without both directions, a 13-state parent can silently weaken or enlarge the
original initial set.

## Terminal-transfer impact

Terminal transfer depends on which contract is frozen.

- For the explicit-time 13-state parent, terminal comparison must rewrite
  through the explicit relation `w(t) = c * t`.
- For a future genuine 14-state ramp parent, terminal transfer can remain a
  direct projection once the ramp premise is proved.

The important blocker is that the endpoint payload alone does not establish
full transfer. A terminal equality at `t = 1` is not enough; the theorem still
needs a continuous-time tube covering every `t ∈ [0,1]` and a domain
continuation statement in the selected contract.

## Admission blockers

The current admission blockers are:

1. the deployed source is 13-state, while the existing Lean parent expects a
   14-state ramp RHS with `w' = c` and `c' = 0`;
2. `examples/routeb_p8_rhs_payload_generator/SOURCE_METADATA.json` marks
   `ramp_binding` as `OPEN` and `c` as a sidecar parameter;
3. `examples/routeb_p8_rhs_payload_generator/receipt.template.json` keeps the
   dynamic endpoint payload pending, with no authenticated outward rounding;
4. the current adapter theorem
   `examples/routeb_p8_contract_adapter/P8ContractAdapter.lean` only proves
   the conditional interface shape, not source binding or flowpipe existence;
5. no outward RHS enclosure, solution existence, local flowpipe, partition
   continuation, or `[0,1]` coverage has been established for either contract.

So the freeze decision is admission-closed for the 14-state ramp theorem in the
current source state, and admission-open only for a new explicit-time 13-state
parent family.

## Recommendation

Freeze the contract on the explicit-time 13-state path now, and keep the
14-state ramp parent as a future source-repair target rather than a current
theorem target. That preserves semantic honesty, avoids silently changing the
state contract, and matches the evidence already recorded in the docs and
payload metadata.

## Evidence notes

The current docs and examples already agree on the central mismatch:

- the Lean parent is 14-state and expects `w' = c, c' = 0`;
- the deployed source is 13-state and records `du[13] = 0`;
- the payload generator keeps `c` open as a sidecar;
- the explicit-time adapter is only a conditional scaffold.

This audit therefore freezes the contract choice rather than claiming a
flowpipe result.
