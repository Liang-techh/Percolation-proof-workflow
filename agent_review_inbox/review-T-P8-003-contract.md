---
kind: review_result
task_id: T-P8-003
source_agent: Codex
created_at: 2026-09-06T22:30:00-06:00
integration_status: pending
---

# T-P8-003 — freeze the state contract

## Scope and decision boundary

This is a read-only audit of the current P8 state contract choice. I inspected the
existing docs, the Lean adapter scaffold, and the source-contract metadata only.
No theorem target, state shape, registry entry, or external project was modified.
No broad test run was performed.

The question is not whether the deployed RHS is mathematically interesting. The
question is whether the currently deployed source can honestly inhabit the existing
14-state ramp contract, or whether it must be frozen as an explicit-time 13-state
contract instead.

## Inspected evidence

| artifact | SHA-256 | relevance |
|---|---|---|
| `docs/routeb-p8-next-concrete-child.md` | `9EF74058FB6711946A253A9DED55EB6CE91DDA01059A78999B413FF98E57AB0E` | states the 13-state source / 14-state ramp mismatch and the `c=1` witness |
| `docs/routeb-p8-flowpipe-binding-next.md` | `47681DFC4DE2153B34AD8B2269FF747583D09E3FADDACA50FDA27D94BC43A6AB` | coordinate map, source hash notes, and flowpipe chain boundary |
| `examples/routeb_p8_contract_adapter/P8ContractAdapter.lean` | `DC4BF1C7C0B1EE428EE3BF146E90801E08A2199FB931789699FE8073A82AB7F9` | exact negative `zeroTailLift_not_ramp` and conditional `timeLift_rampPremise` |
| `examples/routeb_p8_rhs_payload_generator/SOURCE_METADATA.json` | `C8045946C2E087FF8B31010A823F7EAD6A1AF56D2D84D68DD39D62C70A6EED34` | declares `julia_state_dimension=13`, `w_rhs=0`, and `c` as sidecar |
| `examples/routeb_p8_rhs_payload_generator/receipt.template.json` | `545E99CB45B95D804962F70A3B5EC4A44F88BD9F4D6649976A986512B453A207` | endpoint receipt is still pending; no hidden 14-state source binding |
| `examples/routeb_p8_picard_step_lean/RouteBP8PicardStep.lean` | `99D309B1D07439DFB7DE1088D6A2E34F7DCA664EFE72857F94ECE5F28A635741` | parent contract still expects `w'=c` and `c'=0` |

Commit context: current worktree head before this edit was `b667ccc`. The decision
below is based on the inspected files above, not on a new source mutation.

## Decision

Freeze the deployed source as an explicit-time 13-state contract, not as the
existing 14-state ramp theorem.

Why:

- the source metadata says the deployed RHS is 13-state;
- `w` is written as a constant source literal (`w_rhs=0`);
- `c` is marked as a sidecar parameter, not a consumed state;
- the 14-state parent requires `w'=c` and `c'=0`, which the current deployed source
  cannot satisfy on the legal `c=1` initial state;
- the Lean adapter already isolates the negative fact that the zero-tail lift does
  not satisfy the ramp premise.

In short: the 14-state ramp theorem is the wrong frozen contract for the current
deployed source. The semantically honest freeze is an explicit-time 13-state parent
with `c` external to the state vector.

## Minimal theorem signature

The smallest safe theorem family to freeze is:

```text
theorem P8_explicit_time_flowpipe
  (F13 : ℝ → ℝ → State13 → State13)
  (x₀ : State13) (c : ℝ)
  (hinit : explicitInitial13 x₀ c)
  (hbind : ∀ t x, F13 t c x = source_rhs13 t c x)
  (hreg : ...)
  (hbox : ...)
  (hcont : ...)
  : ∃ y, solution13 F13 c x₀ y ∧
      ∀ t ∈ Set.Icc 0 1, y t ∈ certifiedTube13 t
```

If the team wants the theorem to remain closer to the current adapter shape, the
type can be presented as a ramp-repair bridge, but only with `c` external:

```text
theorem P8_explicit_time_ramp_bridge
  (G : ℝ → State13 → State13)
  (c : ℝ)
  : RampShapeAfterLift G c
```

That second form is only an interface theorem. It is not enough for admission by
itself unless the source binding child is also proved.

## Selection advice

Choose the explicit-time 13-state contract if the deployed code is fixed and the
source contract cannot be changed immediately.

Choose the 14-state ramp contract only if the deployed source is repaired so that
`c` is an actual state coordinate and the RHS really satisfies `w'=c, c'=0` for
all admissible states.

Given the current evidence, the first option is the correct freeze.

## Initial-domain impact

The initial mechanical domain should stay the same:

- the `q/dq` energy or box conditions do not need to be weakened;
- `w(0)=0` stays explicit;
- `c^2 ≤ 3` remains a parameter restriction, but it is no longer encoded as a state
  coordinate.

So the initial family becomes dependent on `c`:

```text
X₀(c) := mechanicalInitialSet ∧ w(0)=0 ∧ c²≤3
```

That means any reuse of the old `FullX0` theorem needs a projection/forget-tail lemma.
Without that lemma, the 13-state contract would silently change the quantified
initial set.

## Terminal-transfer impact

Terminal transfer becomes a projection theorem, not a definitional reuse.

- If the terminal predicate does not mention `c`, then `w(t)=c*t` is the bridge
  needed to rewrite the terminal comparison.
- If the terminal predicate does mention `c`, then `c` must remain an explicit
  parameter in the terminal statement.

Either way, the old 14-state terminal theorem cannot be inherited by simple
definitional equality. The proof must first establish the time-indexed relation
`w(t)=c*t` in the selected 13-state semantics, and only then transfer the terminal
predicate.

## Admission blockers

The current blocker list is short and closed:

1. The deployed source is 13-state while the current ramp parent expects 14-state
   input/output semantics.
2. The deployed source does not consume `c`; the ramp parent requires `w'=c`.
3. The available Lean adapter shows the zero-tail lift is not ramp-compatible.
4. The current receipt template is still pending and does not provide a continuous
   RHS binding or an outward interval enclosure.
5. No solution existence, flowpipe coverage, or terminal-transfer theorem has been
   established for either contract yet.

These blockers are semantic, not numerical. No amount of endpoint padding or wider
sampling removes them.

## Recommendation

Freeze the state contract as:

- `13-state explicit-time source` as the deployed contract;
- `14-state ramp` retained only as a separate future theorem family, if the source
  is later repaired.

That gives the smallest honest theorem boundary and preserves the distinction
between the current deployed code and the intended ramp semantics.

No registry promotion is eligible from this audit alone.
