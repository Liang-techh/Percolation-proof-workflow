---
kind: review_result
task_id: T-P8-002
source_agent: 流川枫
created_at: 2026-11-26T08:20:00Z
integration_status: pending
admission_label: architecture_only
inspected_commit: e3d0e04cc2b8f66fa5562cdad76d1d5120891e23
---

# T-P8-002 Decision Memo: Explicit-time 13-state parent option

## Inspected paths
- `examples/routeb_p8_explicit_time_sidecar/README.md`
- `examples/routeb_p8_explicit_time_sidecar/RouteBP8ExplicitTimeSidecar.lean`
- `examples/routeb_p8_explicit_time_sidecar/verify.sh`
- `examples/routeb_p8_picard_step_lean/README.md` (14-state parent reference)
- Claim: `agent_review_inbox/claim-T-P8-002-liuchuanafeng-20261126T011700Z.md`

## Scope compliance
Task boundary: decision memo and minimal theorem signature comparing explicit-time 13-state parent to existing 14-state ramp parent (initial-domain and terminal statement changes). No source edits. Forbidden: silently changing the target theorem or claiming flowpipe coverage.

This review stays strictly inside the boundary.

## Findings

The existing 14-state ramp parent (`RouteBP8PicardStep`) uses `State14 := Fin 14 → ℝ` with order `q₁…q₆, dq₁…dq₆, w, c`, full initial contract `FullX0` (mechanical energy ≤ 9/400, w=0, c^{2}≤3), and ramp formulas `w = c * t` with frozen `c`.

The explicit-time 13-state sidecar (`RouteBP8ExplicitTimeSidecar`) freezes the smallest interface for a deployed 13-state source:

- Coordinate order: `q₁…q₆, dq₁…dq₆, w` (`State13 := Fin 13 → ℝ`), `c` kept external.
- Initial projection: `forgetTail13 : State14 → State13` drops the final `c` slot; `explicitInitial13` requires the same energy bound on the first 12 coordinates, `w=0`, and external `c^{2} ≤ 3`. Theorem `explicitInitial13_of_fullX0` proves `FullX0 z ⇒ initialProjection13 z`.
- Terminal transfer: `explicitTerminal13 y c ⇔ y wSlot13 = c`; `terminalTransfer13` is the predicate. No flow or ODE claim.
- Source family: `sourceFamily13` is a pure reflexivity placeholder (`∀ t x, F13 t c x = F13 t c x`); no RHS binding.
- Minimal packaging theorems only; no `sorry`/`admit` (verified by source restriction check in `verify.sh`).

### Minimal theorem signature (decision)

Keep the 13-state as a **sidecar / projected interface**, not a replacement parent:

```lean
theorem explicit_time_13state_contract
    (F13 : ℝ → ℝ → (Fin 13 → ℝ) → (Fin 13 → ℝ))
    (c : ℝ)
    (z0 : Fin 14 → ℝ)
    (hz0 : FullX0 z0) :
    initialProjection13 z0 ∧
    (∀ y, terminalTransfer13 y c → y (wSlot13) = c) ∧
    sourceFamily13 F13 c := …
```

Initial-domain change: the 13-state initial set is the image of the 14-state `FullX0` under `forgetTail13` plus external `c` bound (already proved). Terminal statement change: terminal condition is rewritten as equality on the externalized `w = c` rather than a joint ramp evolution.

## Admission decision

**admission_label: architecture_only**

- No source binding of the deployed 13-state RHS.
- No flowpipe, existence, or coverage claim.
- Theorems are pure packaging / projection / tautological transfer.
- `verify.sh` is local, pinned, and reports `EXPLICIT_TIME_CONTRACT_BOUNDARY=OPEN`.
- Does not alter the authoritative 14-state target or registry.

Proposed integration: leave as pending architecture sidecar. A later source-authenticated child may consume `initialProjection13` and `terminalTransfer13` once an exact 13-state RHS witness exists. Do not promote to compiled_candidate or verified without independent Lean receipt and source equality.

## Unresolved blockers
- Actual 13-state vector-field source equality and interval enclosure remain open.
- No pinned compile receipt was executed in this review (environment not assumed present); only source inspection and existing local verify script structure.
- Parent `RouteBP8PicardStep` remains the authoritative ramp interface.

No registry, state, or formal proof modifications performed.
