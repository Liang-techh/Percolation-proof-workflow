---
kind: review_result
review_id: review-T-P8-002-explicit-time-13state-parent-option-liuchuanafeng-20261107T0413Z
source_agent: 流川枫
created_at: 2026-11-07T04:13:00Z
inspected_commit: a7be4b1826a8f79fe787dd0e646c8d8d492b42fa
task_id: T-P8-002
admission_label: architecture_only
proposed_action: keep pending; do not promote registry or formal gate
---

# Review result: T-P8-002 — explicit-time 13-state parent option

**Agent**: 流川枫  
**Claim**: claim-T-P8-002-explicit-time-13state-parent-option-liuchuanafeng-20261106T1116Z  
**Inspected**: docs/routeb-p8-flowpipe-binding-next.md (SHA of related sources noted therein), task_queue.md, existing P8 Picard/receipt examples.  
**Boundary**: decision memo + minimal theorem signature only. No source edits, no Lean/Julia execution, no flowpipe coverage claim, no registry/state/formal-proof mutation.

## Exact question inspected

Compare a prospective explicit-time 13-state parent with the existing 14-state ramp parent (`RouteBP8PicardStep`), focusing on initial-domain compatibility and terminal-statement changes. Deliver a decision memo and the minimal signature of any new parent theorem. Forbidden: silently rewriting the target theorem or claiming any flowpipe coverage.

## Evidence summary

From `docs/routeb-p8-flowpipe-binding-next.md` (2026-09-06, still authoritative for this leaf):

- Existing parent fixes `Fin 14` coordinates: `q1..q6, dq1..dq6, w, c` with
  ```
  RampRhsPremise F ⇒ F z wSlot = z cSlot ∧ F z cSlot = 0
  ```
  i.e. the autonomous ramp `w' = c`, `c' = 0`.
- Current true-DH source (`routeB_reachability_full_dh_probe.jl`, SHA-256 `12292f88…`) is strictly 13-state: reads `q,dq,w`, writes `du[13] = 0`, ReachabilityAnalysis `dim:13`. No `c` state variable.
- Natural lift of the 13-state RHS into 14 dimensions immediately falsifies `RampRhsPremise` for any nonzero `c` (witness: `q=dq=w=0, c=1` lies in `FullX0` yet produces `F14[12] = 0 ≠ 1`).
- Therefore the existing 14-state ramp parent is currently uninstantiable against the real source. The only consistent options are (a) supply a genuine 14-state RHS proving the ramp identities, or (b) switch the parent contract to an explicit-time 13-state system `F13(t)` with the identity `w(t) = c·t` proved separately.

No source edits were performed; the inconsistency remains as documented.

## Decision memo

**Recommendation**: pursue option (b) as a parallel parent only, while leaving the existing 14-state ramp parent untouched.

Reasons:
1. Source reality is 13-state constant-`w`. Forcing a 14-state autonomous ramp requires new RHS code that does not yet exist and would change the deployed dynamics.
2. Explicit-time formulation `ẋ = F13(t, x)` with an external constant parameter `c` and the algebraic identity `w(t) = w0 + c·t` is a faithful transcription of the current probe/exporter semantics.
3. Initial domain: the mechanical 12-ball (`q,dq`) plus bounded `c` (`c^{2} ≤ 3`) can be retained; the extra state `w` becomes a derived quantity, so the initial box shrinks from 14 to 13 dimensions. Terminal statement must be restated over the image of the explicit-time flow on `[0,1]` rather than an autonomous 14-state flowpipe.
4. The change is non-silent: any consumer of the old `RampRhsPremise` or `Fin 14` coordinate map must be re-typed. This review does **not** perform that retyping.

**Minimal theorem signature (architecture only)**

```lean
-- Prospective explicit-time parent (not yet formalized)
theorem RouteBP8_ExplicitTime13_Parent
  (F13 : ℝ → ℝ^{13} → ℝ^{13})          -- time-dependent RHS
  (c : ℝ)                            -- constant ramp rate
  (x0 : ℝ^{13})                       -- initial (q,dq,w0)
  (h_fullX0 : FullX0_mech (x0.q, x0.dq) ∧ c^{2} ≤ 3)
  (h_w : ∀ t, sol(t).w = x0.w + c * t)
  (h_rhs : ∀ t, sol'(t) = F13 t sol(t))
  : ∀ t ∈ [0,1], sol(t) ∈ certified_tube_13(t)
```

(The signature is illustrative; exact Lean encoding, interval enclosure, and coverage arguments remain future leaves.)

## Admission label and requested action

- **admission_label**: `architecture_only`
- The comparison and decision are complete for this leaf. No theorem has been proved, no source has been bound, and no flowpipe coverage is claimed.
- Requested action: leave `T-P8-002` pending. Coordinator may open a follow-up leaf that formalizes the explicit-time signature above, or that supplies a true 14-state RHS; either path must still pass source-binding, interval, and coverage gates independently. Do not rewrite the existing 14-state parent or promote any registry entry on the basis of this memo.

## Provenance

- Claimed by 流川枫 on 2026-11-06T11:16:00Z (roster notes agent unavailable for new dispatch; claim preserves historical provenance only).
- All evidence drawn from existing documentation; no new computational artifacts produced.
- Forbidden actions observed: no source edits, no silent target-theorem change, no coverage claim.
