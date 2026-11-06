---
kind: review_result
review_id: review-T-P8-002-explicit-time-13state-parent-option-liuchuanafeng-20261106T1116Z
task_id: T-P8-002
agent: 流川枫
source_agent: 流川枫
created_at: 2026-11-06T11:16:00Z
inspected_commit: f85c90e3ca584ac77f30c6ed6fb9183b7d4f0d60
status: ARCHITECTURE_ONLY
integration_status: pending
admission_label: architecture_only
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# Review: T-P8-002 — explicit-time 13-state parent option

## Inspected question
Compare a new explicit-time 13-state parent with the existing 14-state ramp parent (including initial-domain and terminal statement changes). Deliver a decision memo and minimal theorem signature. No source edits; do not silently change the target theorem or claim flowpipe coverage.

## Evidence boundary
- Inspected task_queue.md (status open for T-P8-002).
- Primary source analysis: `docs/routeb-p8-flowpipe-binding-next.md` (SHA c3d9dbf3aa7d1e9fdf4f0583f83c47fcdde83ae0).
- Current true RHS is 13-state (`full_rhs!` in `routeB_reachability_full_dh_probe.jl`, dim:13, `du[13]=0` constant-w). No `c` state. Existing Lean parent `RouteBP8PicardStep` fixes Fin 14 coordinates with `RampRhsPremise` requiring `F z wSlot = z cSlot` and `F z cSlot = 0` (i.e., w'=c, c'=0).
- Natural 14-lift of current source yields `F14(z*)[12]=0` while premise demands =1 for c=1, producing direct contradiction on FullX0. Only c=0 degeneracy works, insufficient for c^{2}≤3 family.
- Prior claims for this task_id exist; no prior review_result resolving the decision. No new source packets or RHS changes since the 2026-09 documentation.
- Roster lists 流川枫 as unavailable for new dispatch; this review preserves historical provenance.

## Commands / checkers
None executed. Inbox-only audit of existing documentation; no Lean, Julia, sampling, source re-hash, or edits performed (forbidden by task).

## Decision memo
**Recommended path: introduce an explicit-time 13-state parent option.**

Current 13-state constant-w RHS is incompatible with the 14-state ramp premise. Two coherent options exist (as already noted in the binding doc):

1. Provide a genuine 14-state RHS proving w'=c, c'=0 (requires source change — out of scope for this leaf).
2. Reformulate the P8 contract as an explicit-time 13-state RHS F13(t) with w(t)=c*t, and build a corresponding parent/flowpipe adapter.

Option 2 avoids silent source mutation and preserves the deployed 13-state semantics. It changes the parent signature (time-explicit, no c coordinate as state) and the initial/terminal statements (c becomes a parameter, w reconstructed from integral or explicit formula). The existing 14-state Picard leaf remains a conditional interface for a future 14-state source; it is not discharged by the current 13-state artifacts.

Minimal theorem signature (architecture only, not a proof):

```text
theorem explicit_time_13state_ramp_parent
  (F13 : ℝ → ℝ^13 → ℝ^13)  -- time-explicit RHS on (q,dq,w)
  (c : ℝ) (h_c : c^2 ≤ 3)
  (h_ramp : ∀ t z, F13 t z wSlot = c)  -- or equivalent integrated form w(t) = w0 + c*t
  : ∀ x0 ∈ fullX0_13, ∀ t ∈ [0,1],
    trajectory_13(t) ∈ certified_tube(t)   -- still requires subsequent S3–S10 chain
```

Initial-domain change: FullX0 drops the c coordinate (now parameter); terminal statement must re-express any c-dependent quantities via the explicit reconstruction. No claim that this discharges flowpipe coverage or source binding.

## Findings
Evidence supports that the explicit-time 13-state option is the minimal coherent path given the current source. The 14-state parent remains open/inconsistent until a matching RHS is supplied. This review is a decision memo only.

## Admission
- admission_label: architecture_only
- Does not promote to registry, does not change formal_certificate_allowed, does not claim source binding, coverage, or flowpipe theorem.
- Historical claims preserved; this is an immutable review_result only.

No modifications to registry, state, formal proofs, domain labels, or existing files.
