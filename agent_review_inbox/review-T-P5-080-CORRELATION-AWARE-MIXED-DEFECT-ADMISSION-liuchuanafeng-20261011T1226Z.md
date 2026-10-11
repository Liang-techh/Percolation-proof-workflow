---
kind: review_result
review_id: review-T-P5-080-CORRELATION-AWARE-MIXED-DEFECT-ADMISSION-liuchuanafeng-20261011T1226Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-11T12:26:00Z
claimed_at: 2026-10-11T12:25:00Z
inspected_commit: 8c1a49069d48a65a95b0422b132d010383cca963
inspected_paths:
  - agent_review_inbox/claim-T-P5-080-CORRELATION-AWARE-MIXED-DEFECT-ADMISSION-liuchuanafeng-20261011T1225Z.md
  - agent_review_inbox/claim-T-P5-080-correlation-aware-mixed-defect-kuangmanmozun-20260908T0808.md
  - agent_review_inbox/review-T-P5-080-correlation-aware-mixed-defect-kuangmanmozun-20260908T0822.md
  - agent_review_inbox/companion-T-P5-080-correlation-aware-mixed-defect-kuangmanmozun-20260908T0825.md
task_id: T-P5-080-CORRELATION-AWARE-MIXED-DEFECT
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
lean_rerun: false
deployed_source_packet: false
float64_semantics: false
same_key_cell_coverage: false
ode_continuation: false
proposed_integration_target: documentation
requested_action: harvest_pending_admission_audit_do_not_promote
---

# T-P5-080-CORRELATION-AWARE-MIXED-DEFECT: admission audit remains pending

## Question

Does the published T-P5-080 mathematical interface (signed/correlation-aware relative-defect factor `kappa_corr = q - 2 h gamma + h^2 K` under the hypotheses `Q(a) <= q V`, `Q(e_r) <= K V`, `<a, e_r>_W >= gamma V`; signed post-relative affine energy recurrence `Q(d_plus) <= A V + B` with `A = kappa_corr + 2 h J1 + h^2 E1`, `B = 2 h J0 + h^2 E0`; rational floor certificate `B <= (1-A) Vfloor`; exact rational sharpness and antiparallel counterexamples; signed-Gram handoff before absolute values) supply a deployed source packet, certified margins, Float64 semantics, same-key cell coverage, ODE continuation, a pinned Lean receipt that upgrades beyond `compiled_candidate`, or registry admission?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The interface is a source-independent mathematical refinement of the independent-envelope gates of T-P5-078/T-P5-075, valid only when a concrete source theorem supplies the signed correlation/cross-term hypotheses on the same weighted quadratic form and source cell. It does not bind to any deployed evaluator, source packet, or runtime semantics.

## Evidence inspected (read-only)

1. **Existing claim by this agent.** The claim at `claim-T-P5-080-CORRELATION-AWARE-MIXED-DEFECT-ADMISSION-liuchuanafeng-20261011T1225Z.md` explicitly bounds the work to admission audit only: do not compile, repair, create sidecars, or promote; do not edit registry/state/formal proofs. Roster still marks 流川枫 unavailable for new dispatch; this does not rewrite it.

2. **Mathematical review and companion by 狂蛮魔尊.** `review-T-P5-080-correlation-aware-mixed-defect-kuangmanmozun-20260908T0822.md` and `companion-T-P5-080-correlation-aware-mixed-defect-kuangmanmozun-20260908T0825.md` record the exact identities:
   - Relative: `Q(a - h e_r) <= (q - 2 h gamma + h^2 K) V` when the three scalar hypotheses hold (Theorem 1.1); strict contraction if `0 <= kappa_corr < 1`.
   - Relation to T-P5-078: the independent-envelope worst case is `q + 2 h sqrt(q K) + h^2 K`; improvement requires `gamma > -sqrt(q K)` from a source theorem, not from norm data or sampling.
   - Sharp rational example: `q = K = 1/4`, `h = 1`, `gamma = 0` yields `kappa_corr = 1/2` (attained by orthogonal `a = (1/2, 0)`, `e_r = (0, 1/2)`), while the independent factor is 1 (boundary only). Antiparallel witness `e_r = (-1/2, 0)` recovers the independent factor of 1.
   - Persistent: under `Q(e_0) <= E1 V + E0` and `<b, e_0>_W >= -(J1 V + J0)`, the update satisfies `Q(d_plus) <= A V + B` with the stated A, B (Theorem 4.1); invariant level when `0 <= A < 1` and `B < (1-A) Vstar`.
   - Floor: `B <= (1-A) Vfloor` certifies the asymptotic floor without division.
   - Signed-Gram handoff: bounds on `<a, e_0>` and `<e_r, e_0>` yield the J packet without forming b first; absolute-value entrywise bounds erase the cancellation.
   - Explicit fail-closed rules: wrong sign on the correlation inequality does not control the dangerous cross term; different weights are not interchangeable; cross information must share the source cell; no improvement without correlation evidence.
   - Explicitly: no upgrade of deployed SCC/source, Float64/FD/controller, P8/ODE coverage, Lean/kernel, admission, registry, or parent closure. Status is pending mathematical child.

3. **No supporting artifacts for admission.** No deployed source packet realizing the signed correlation hypotheses on a common cell, no certified numeric margins tied to an actual residual, no Float64 semantics, no same-key cell coverage, no ODE continuation proof, and no Lean receipt (even compiled_candidate) appear in the inspected inbox files for this task.

## Boundary compliance

- Did not compile, repair, or create new sidecars.
- Did not edit registry, state, formal proofs, or task_queue.
- Did not promote any candidate to verified or close parent tasks.
- Admission remains `pending`; architecture_only mathematical interface only.

## Integration target and requested action

- Target: documentation / pending metadata only.
- Requested action: harvest as a pending admission audit. Do not treat the mathematical correlation-aware factor or affine recurrence as source-bound or admitted. Leave the task open for further source-binding or independent verification work by active agents. If no signed source theorem is available, continue to use the independent-envelope gates of T-P5-078/T-P5-075.
