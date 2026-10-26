---
kind: review_result
review_id: review-T-P8-009-INTERVAL-LOCAL-RAMP-CALCULUS-ADMISSION-liuchuanafeng-20261026T1617Z
task_id: T-P8-009
parent_task_id: T-P8-007
source_agent: 流川枫
created_at: 2026-10-26T16:17:00Z
inspected_commit: 37c7f967a8a00fde41c407dda1af7d2a94fa0155
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: none (inbox-only audit; no registry/state/formal mutation)
---

# T-P8-009 — interval-local ramp calculus refinement admission audit

## Scope and boundary

Independent inbox-only admission audit of the open interval-local/end-point refinement of the ramp-tail calculus. Confirms whether a separate Lean child, exact API obstruction, pinned receipt covering the refinement, source binding, coverage, or registry admission exists. Does not construct new theorems, compile, alter the compiled candidate, or modify registry/state/formal proofs.

Matches the claim `claim-T-P8-009-INTERVAL-LOCAL-RAMP-CALCULUS-ADMISSION-liuchuanafeng-20261026T1420Z`. Roster notes historical unavailability of 流川枫; this result preserves provenance and does not rewrite prior authorship or roster.

## Inspected evidence

- Task queue (`agent_review_inbox/task_queue.md`): T-P8-009 status `open`, owner 苏梦辰; scope to deliver a separate Lean child or exact API obstruction without altering the already compiled candidate or claiming ODE existence. Forbidden: source binding, flowpipe coverage, first-exit closure, or registry promotion from the abstract calculus child.
- Prior review `agent_review_inbox/review-T-P8-007-choupizhu-20260906T2307.md`: admission_label `compiled_candidate` for the stronger global-ℝ `HasDerivAt` version; explicitly leaves the interval-local/end-point formulation as an open refinement. Focused CI (run 34085393805) covered only the global theorems; blob hashes recorded for that snapshot.
- Current sidecar `examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean` (blob SHA a5846b79339119c01df13356e74fea2b54946291):
  - Retains the original global theorems (`ramp_c_constant`, `ramp_w_eq_mul`, `ramp_reconstruction`, `state_tail_reconstruction`, `state_terminal_one`).
  - Adds interval-local seam: `endpoint_eq_of_zero_derivative_on_interval` (ContinuousOn on Icc, HasDerivAt on Ioo, explicit zero-integrability premise) and `ramp_endpoint_on_interval` (transfers endpoint using derivative + explicit integral identity for c).
  - Comments and README state these are an adapter surface with undischarged integral/source premises; not an admission claim. No separate child file exists.
- `verify.sh` (blob 89144cf54bcdc1d71db8230b9387103c5298b1cf) greps only the five original global theorems; does not audit the new interval-local theorems or their axioms.
- lean-toolchain pins `leanprover/lean4:v4.32.0`.
- No additional review_result, pinned CI receipt, or separate sidecar found that independently verifies the interval-local theorems under a fresh focused compile. No source binding, domain coverage, flowpipe, or registry entry associated with T-P8-009.
- Older claim by 苏梦辰 (2026-09-07) intended a separate portable sidecar; that separate child is not present.

## Findings

The interval-local refinement has been exposed as co-located lemmas inside the existing P8 ramp sidecar rather than delivered as a separate Lean child. The lemmas correctly leave the interval-integral identities as explicit premises, preserving the boundary that they do not smuggle ODE existence or source regularity. However:

- This does not constitute the task's required separate Lean child.
- The original compiled_candidate receipt and verify.sh do not cover the new theorems; no new pinned receipt (exit code, #print axioms, placeholder scan) for the interval-local seam is present in the inbox.
- No exact API obstruction documenting why a separate child is impossible was found.
- Source binding, coverage, and registry admission remain absent, as required by the task forbidden list.

The stronger global version remains a compiled_candidate; the interval-local refinement remains an open leaf.

## Admission label

`pending`

No promotion of the co-located lemmas, no alteration of the existing compiled_candidate status, and no change to registry or formal gates. Further work (separate child with independent pinned receipt, or documented obstruction) is required before any stronger label.

## Requested action

None. This is an inbox-only audit result for the next harvest. Do not treat as proof or registry input.
