kind: review_result
review_id: review-T-P8-011-INTERVAL-LOCAL-ENDPOINT-ADAPTER-liuchuanafeng-20261109T0514Z
source_agent: 流川枫
created_at: 2026-11-09T05:14:00Z
inspected_commit: ea585b74cadf798a7f1fb586bfbb81a9176b9b0e
inspected_paths:
  - examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean
  - agent_review_inbox/task_queue.md
  - docs/routeb-p8-flowpipe-binding-next.md
task: T-P8-011
question: Audit the interval-local endpoint adapter (endpoint_eq_of_zero_derivative_on_interval and ramp_endpoint_on_interval) for exact hypotheses, boundary relative to global HasDerivAt theorems, and residual obligations for P8 source binding. Deliver architecture memo only.
admission_label: architecture_only
evidence_level: document_inspection_only

## Summary
The interval-local seam correctly weakens the global ∀t HasDerivAt assumptions of the compiled candidate to ContinuousOn on Icc, HasDerivAt on Ioo, and explicit IntervalIntegrable premises. The two integral identities remain explicit frontiers that must still be discharged by a future source/flowpipe agent. No ODE existence, source binding, coverage, or admission is obtained or claimed.

## Architecture Audit

### Global vs interval-local
- Global theorems (ramp_c_constant, ramp_w_eq_mul, state_tail_reconstruction, state_terminal_one) assume HasDerivAt everywhere on ℝ. They are stronger than needed for a finite-horizon [0,1] transfer and are convenient for the abstract compiled_candidate sidecar.
- Interval-local theorems:
  - endpoint_eq_of_zero_derivative_on_interval: uses ContinuousOn on Icc, HasDerivAt 0 on Ioo, IntervalIntegrable of the zero function, and the fundamental theorem of calculus identity to conclude f b = f a.
  - ramp_endpoint_on_interval: composes the above for c with an explicit integral premise (∫ c = c0*(b-a)) plus ContinuousOn/HasDerivAt for w, yielding c b = c0 ∧ w b = w a + c0*(b-a).
- Both correctly leave the integral identities as premises rather than smuggling regularity or existence.

### Residual obligations (still open)
1. Bind the ContinuousOn / HasDerivAt / IntervalIntegrable hypotheses to the actual deployed 13-state (or future 14-state) RHS on the concrete interval [0,1].
2. Discharge the explicit integral identity for the ramp coordinate from the source contract (or from a verified flowpipe enclosure).
3. Connect the resulting endpoint identity to the terminal residual/energy comparison and any first-exit or Picard continuation chain.
4. Resolve the prior S1/S2 semantic incompatibility between 13-state constant-w source and 14-state ramp parent (see T-P8-002 decision memo).

### Recommendation
Keep the interval-local adapter as an architecture_only / pending calculus child. It is the correct next refinement after the global candidate, but it does not close any source, coverage, or admission gate. A pinned Lean compile/axiom receipt remains the responsibility of the designated Lean lane; this review performs no compilation.

### Boundaries respected
- No source edits, no Lean/Julia execution, no registry or state mutation.
- Forbidden actions avoided: no claim of P8 reachability, no source equality, no coverage, no registry promotion.
- admission_label remains architecture_only.

## Commands / checkers
None executed (document inspection only).

## Next
Coordinator may harvest as pending architecture refinement. Concrete interval binding and integral discharge remain open for source/math agents; pinned compile receipt remains open for Lean agents. Do not close P8.
