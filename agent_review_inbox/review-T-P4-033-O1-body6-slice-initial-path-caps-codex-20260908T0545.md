---
kind: review_result
review_id: review-T-P4-033-O1-body6-slice-initial-path-caps-codex-20260908T0545
task_id: T-P4-033-O1-body6-slice
source_agent: codex-body6-math-lane
created_at: 2026-09-08T05:45:00Z
inspected_paths:
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_INITIALPATHCAPS20260907.lean
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_INITIALPATHCAPS20260907.review.md
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
proposed_integration_target: P4.O1.source_comparator.h_body_6.initial_to_full_path_cap
requested_action: retain separated initial/full-path/growth/shift contracts; require integrated-growth or direct full-cap evidence before transfer
---

# BODY6 initial-to-full path cap boundary

The sidecar separates four predicates that are often incorrectly conflated:
`InitialSetCap`, `InitialPathCap`, `FullPathCap`, and `IntegratedGrowth`.  An
initial-set cap becomes an initial-path cap only after an explicit path-start
membership proof.  A full-path cap requires either a direct all-time bound or
an independently established integrated-growth inequality plus a uniform
growth budget.

The final consumer composes this with the existing full-state projection and
shift identity, requiring the exact budget `(a+beta)+B ≤ bar`.  It does not
derive growth from a derivative name, a CSV scalar, or an initial receipt.

The smooth hump `8*t*(1-t)` gives an exact logical counterexample: initial cap,
nonnegativity, and terminal zero do not imply a full-path cap.  The sidecar
also records that a nonnegative unshifted cap cannot pay the current
`B=4079979/400000` shift at fixed `bar=1`.

Status remains `OPEN_UNCOMPILED/pending`; no ODE, continuation, source binding,
flowpipe, registry promotion, or formal-gate change is claimed.
