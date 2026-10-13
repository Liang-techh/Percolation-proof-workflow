---
kind: review_result
review_id: review-T-P8-002-explicit-time-13-state-parent-liuchuanafeng-20261013T1015Z
source_agent: 流川枫
created_at: 2026-10-13T10:15:00Z
task_id: T-P8-002
inspected_commit: 92f83e089404dab10ff1f526f849a8e37a3088cc
admission_label: architecture_only
---

# Review Result: T-P8-002 — explicit-time 13-state parent option

**Agent**: 流川枫  
**Question inspected**: 比较新的 explicit-time 13-state parent 与现有 14-state ramp parent，包括 initial-domain 与 terminal statement 变化；交付决策 memo + 最小定理签名。无 source 编辑、无 flowpipe/coverage 声明、无 registry/state 变更。

## Evidence inspected
- `agent_review_inbox/task_queue.md` (T-P8-002 status open; prior claim by this agent exists)
- `docs/routeb-p8-next-concrete-child.md` (13→14 contract decision, zeroTailLift_not_ramp, timeLift scaffold)
- `docs/routeb-p8-flowpipe-binding-next.md` (source vs Lean coordinate map, RampRhsPremise incompatibility)
- Related: `examples/routeb_p8_picard_step_lean/`, `examples/routeb_p8_contract_adapter/`, receipt templates, source metadata (13-state `full_rhs!` with `du[13]=0`)

No runtime, no Lean compile this round, no external source access. All conclusions are from existing static audit + structural contracts.

## Decision memo

### Current 14-state ramp parent
- State: `Fin 14 = q1..q6, dq1..dq6, w, c`
- `RampRhsPremise F`: ∀z. `F z wSlot = z cSlot` ∧ `F z cSlot = 0` (i.e. w'=c, c'=0)
- Initial domain: FullX0 includes mechanical energy bound + c²≤3
- Terminal: Picard/flowpipe assembly over [0,1] under the ramp field

### Source fact (audited)
True-DH probe `full_rhs!` is **13-state**: reads u[1:13], writes du[1:12]=dynamics, du[13]=0. No c state is consumed. Natural lift of 13-state source to 14-state with zero tails contradicts `RampRhsPremise` on FullX0 points with c≠0 (explicit counterexample in `zeroTailLift_not_ramp`).

### Explicit-time 13-state alternative
Redefine parent as time-explicit 13-state RHS:

```text
G : ℝ → State13 → State13          -- true dynamics (q,dq,w)
F13(t) z := G t z
w(t) := c * t                 -- explicit integral of constant c (sidecar parameter)
c' := 0                       -- c remains constant parameter, not state
```

Minimal theorem signature (architecture only):

```lean
theorem explicitTime13_parent_contract
    (G : ℝ → State13 → State13)
    (c : ℝ)
    (FullX0_13 : State13 → Prop)   -- mechanical + w bound only
    : ∀ t ∈ [0,1], ∀ z0 : State13, FullX0_13 z0 →
        let w_t := c * t
        -- Picard / flowpipe image of the 13-state field G t
        -- stays inside certified tube; terminal transfer uses w_t as explicit
        True := by
  sorry   -- placeholder; not a proof
```

### Comparison (initial-domain & terminal changes)
| Aspect              | 14-state ramp parent                  | Explicit-time 13-state parent          |
|---------------------|---------------------------------------|----------------------------------------|
| State dimension     | 14 (w,c both dynamic)                 | 13 (c parameter; w=c*t explicit)       |
| RHS premise         | ∀z. F_w = z_c ∧ F_c = 0               | ∀t. F13(t) matches source G t; w' not in state |
| Initial domain      | FullX0 includes c²≤3                    | FullX0_13 drops c from state; c²≤3 becomes parameter bound |
| Terminal statement  | Tube over joint (q,dq,w,c)            | Tube over (q,dq,w(t)); c fixed         |
| Source compatibility| Incompatible with current 13-state source | Compatible by construction (no lift contradiction) |
| Flowpipe obligation | Requires true 14-state source binding | Requires only 13-state source-to-G binding + explicit w(t) |

### Recommendation
Prefer the **explicit-time 13-state parent** as the shorter consistent contract:
- Eliminates the documented zeroTailLift contradiction without inventing a 14-state source.
- Preserves the mathematical intent (linear ramp w(t)=c*t) via explicit formula rather than dynamic state.
- Initial-domain change is local (c moves from state to parameter); terminal transfer statements must be rewritten to use w(t) explicitly but do not enlarge coverage claims.
- Does **not** close source binding, interval enclosure, Picard existence, partition coverage, or any flowpipe theorem. All remain open.

Existing timeLift scaffold (conditional_interface_only) can be reused as a reference shape but is not itself a parent replacement.

## Admission boundary (strict)
- admission_label: `architecture_only`
- source_binding: OPEN
- flowpipe_coverage: OPEN (not claimed)
- registry / state / formal proofs: unchanged (forbidden respected)
- No source edits performed

This review is planning/decision input only. Integration gates remain authoritative.
