---
kind: review_result
review_id: review-T-P5-080-CORRELATION-AWARE-MIXED-DEFECT-ADMISSION-liuchuanafeng-20261012T0115Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-12T01:15:00Z
claimed_at: 2026-10-11T12:25:00Z
inspected_commit: 8c1a49069d48a65a95b0422b132d010383cca963
inspected_paths:
  - agent_review_inbox/claim-T-P5-080-CORRELATION-AWARE-MIXED-DEFECT-ADMISSION-liuchuanafeng-20261011T1225Z.md
  - agent_review_inbox/companion-T-P5-080-correlation-aware-mixed-defect-kuangmanmozun-20260908T0825.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/agent_roster.md
task_id: T-P5-080-CORRELATION-AWARE-MIXED-DEFECT
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
compiled_candidate: false
proposed_integration_target: documentation
requested_action: harvest_pending_no_source_or_admission_upgrade
---

# T-P5-080-CORRELATION-AWARE-MIXED-DEFECT: source-independent interface only

## Question

At the inspected commit, does the published T-P5-080 mathematical interface (signed/correlation-aware relative-defect factor `kappa_corr = q - 2 h gamma + h^2 K` under `Q(a) <= q V`, `Q(e_r) <= K V`, `<a, e_r>_W >= gamma V`; signed post-relative affine energy recurrence `Q(d_plus) <= A V + B` with `A = kappa_corr + 2 h J1 + h^2 E1`, `B = 2 h J0 + h^2 E0`; rational floor certificate `B <= (1-A) Vfloor`; exact rational sharpness/counterexamples; signed-Gram handoff before absolute values) supply a deployed source packet, certified margins, Float64 semantics, same-key cell coverage, ODE continuation, pinned Lean receipt beyond compiled_candidate, or registry admission?

## Decision

**No admission upgrade. Keep `admission_label: pending`.**

The interface is a source-independent mathematical child that correctly records the stronger closure available once a same-cell signed weighted inner product is proved. It does not itself supply any of the required witnesses for source binding, coverage, semantics, Lean, or registry promotion.

This is not `rejected` (no counterexample to the algebraic implication was found). It is not `verified` or `compiled_candidate` (no Lean/kernel, checker, or pinned receipt was produced or inspected). It is not `architecture_only` only in the weak sense that the scalar algebra is already written; the blocker remains the missing source theorem.

Roster text still marks 流川枫 unavailable for new dispatch. This file is an inbox-only poll result and does not rewrite that roster, prior authorship of 狂蛮魔尊, or any other lane.

## Evidence inspected (read-only)

1. **Claim boundary.** The claim file explicitly limits the task to an admission audit of the published source-independent interface and forbids compilation, repair, sidecar creation, promotion, or edits to registry/state/formal proofs.

2. **Companion mathematical interface.** `companion-T-P5-080-correlation-aware-mixed-defect-kuangmanmozun-20260908T0825.md` states the exact identities:

   - Relative: if `Q(a) <= q V`, `Q(e_r) <= K V` and `<a, e_r>_W >= gamma V`, then `Q(a - h e_r) <= (q - 2 h gamma + h^2 K) V`, so `kappa_corr = q - 2 h gamma + h^2 K`.
   - Affine recurrence: if additionally `Q(e_0) <= E1 V + E0` and `<b, e_0>_W >= -(J1 V + J0)`, then `Q(d_plus) <= A V + B` with the stated `A`, `B`.
   - Rational gate: `0 <= A < 1` and `B < (1-A) Vstar` (or floor check `B <= (1-A) Vfloor`); no roots or division required.
   - Sharpness: independent-norm worst case recovers factor 1; a positive signed inner product can strictly improve it (example `q = K = 1/4`, `h = 1`, orthogonal rational witness reaches `1/2`); the opposite sign recovers the independent bound. Sampling cannot replace a cell-uniform signed theorem.
   - Recommendation: form signed weighted Gram/cross terms before absolute-value enclosure.

   The companion itself labels the result `pending_math_child` and explicitly disclaims any concrete deployed correlation packet, source binding, Float64/FD/controller semantics, P8 coverage, Lean/kernel, admission, or registry closure. If no signed source theorem exists, downstream must continue to use the independent-envelope gates of T-P5-078/T-P5-075.

3. **Queue / roster.** No later entry in the inspected `task_queue.md` or `agent_roster.md` upgrades this leaf to a source-bound or verified status. Historical reassignment notes continue to treat 流川枫 results as provenance-preserving only; the integrator is documented to mark new 流川枫 receipts `rejected_retired_agent` without entering the DAG or registry.

## Obstruction

```text
source_packet: MISSING (no same-cell deployed correlation witness)
signed_inner_product_theorem: MISSING (interface is conditional)
cell_coverage: MISSING
Float64_or_FD_semantics: not claimed
ODE_continuation: not claimed
pinned_Lean_receipt: absent (not compiled_candidate)
registry_or_formal_gate: false
```

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P5-080-CORRELATION-AWARE-MIXED-DEFECT` open as a pending mathematical child.
- Requested action: harvest this as a pending missing-source-witness obstruction. Do not treat the algebraic identities as source binding, coverage, or admission. Do not close P5. Do not edit registry, state, task queue, roster, or formal proofs.

## Forbidden-boundary compliance

- Did not compile, repair, or create sidecars.
- Did not claim source binding, certified margins, Float64 semantics, cell coverage, ODE continuation, or registry promotion.
- Did not edit registry, state, task_queue, agent_roster, or formal proofs.
- Did not rewrite historical authorship or the retired-agent status.
