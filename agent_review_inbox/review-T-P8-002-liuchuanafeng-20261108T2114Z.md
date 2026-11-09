kind: review_result
review_id: review-T-P8-002-liuchuanafeng-20261108T2114Z
source_agent: 流川枫
created_at: 2026-11-08T21:14:00Z
inspected_commit: 85bf39a095787663beb8b228ab40abf04c2fa7eb
inspected_paths:
  - docs/routeb-p8-flowpipe-binding-next.md
  - agent_review_inbox/task_queue.md
  - examples/routeb_p8_rhs_payload_generator/
task: T-P8-002
question: Compare a new explicit-time 13-state parent with the existing 14-state ramp parent, including initial-domain and terminal statement changes. Deliver decision memo and minimal theorem signature.
admission_label: architecture_only
evidence_level: document_inspection_only

## Summary
The existing 14-state RampRhsPremise (w'=c, c'=0) is semantically incompatible with the current deployed 13-state true-DH RHS (du[13]=0, constant w, no c state). A new explicit-time 13-state parent is the minimal coherent alternative that preserves the source without inventing a 14-state RHS. This remains architecture_only / pending; no flowpipe coverage, source binding, or registry promotion is claimed or achieved.

## Decision Memo

### Current incompatibility (from docs/routeb-p8-flowpipe-binding-next.md)
- Lean parent uses Fin 14: q1..q6, dq1..dq6, w, c with RampRhsPremise requiring F z wSlot = z cSlot and F z cSlot = 0.
- Real source (routeB_reachability_full_dh_probe.jl full_rhs!) is dim:13, reads w=u[13], writes du[13]=0, no c.
- Natural lift of 13-state source to 14-state yields contradiction for nonzero c (e.g., z* with c=1, FullX0 holds but ramp premise fails).
- Only the degenerate c=0 subfamily is consistent; it does not cover the original c^{2}≤3 family.

### Options
1. **14-state ramp parent (status quo)**: Requires providing a true 14-state RHS with w'=c, c'=0 and binding it. Currently blocked; source does not implement it. Terminal statements stay time-independent ramp. Initial domain can keep c^{2}≤3.
2. **Explicit-time 13-state parent (recommended for coherence with current source)**:
   - State: (q, v, w) ∈ ℝ^{13}, time t explicit.
   - Dynamics: F13(t, z) where mechanical part is true-DH, and w(t) = c * t (c constant parameter, not state).
   - Initial domain: full 12-ball energy + w(0)=0 (or explicit initial w), c as external parameter with c^{2}≤3.
   - Terminal: at T=1, w(1)=c, trajectory in certified tube that accounts for the known linear ramp in w.
   - Minimal theorem signature sketch:
     ```lean
     theorem explicit_time_13state_parent
       (F13 : ℝ → ℝ^{13} → ℝ^{13})
       (c : ℝ) (hc : c^2 ≤ 3)
       (x0 : ℝ^{12}) (hx0 : FullX0_mech x0)
       (traj : [0,1] → ℝ^{13})
       (hsol : IsSolutionOf F13 traj)
       (hw : ∀ t, traj t 12 = c * t)  -- w slot
       : ReachableTube traj  -- or whatever the terminal statement becomes
     ```
   - Advantages: Matches existing source exactly; no need to invent c-state or change Julia RHS.
   - Changes required: New parent theorem (do not silently edit existing 14-state), adapter from 13-state flowpipe to any terminal residual/energy comparison, explicit treatment of c as parameter rather than state.

### Recommendation
Prefer option 2 (explicit-time 13-state) as the next architecture step. It resolves the S1/S2 semantic binding blocker identified in the binding doc without source mutation. The 14-state route remains available if a genuine 14-state RHS is later supplied and proven.

### Boundaries respected
- No source edits.
- No claim of flowpipe coverage, true-DH binding, interval enclosure, or registry promotion.
- admission_label remains architecture_only (decision memo only).
- All subsequent steps still require independent source binding, RHS interval receipt, Picard/flowpipe existence, coverage, and comparator gates.

## Commands / checkers
None executed (document inspection only). No Lean, Julia, or checker runs performed in this round.

## Next
Coordinator may harvest this as pending architecture decision. Concrete parent formalization and source binding remain open for Lean/math agents. Do not close P8 or promote any receipt.
