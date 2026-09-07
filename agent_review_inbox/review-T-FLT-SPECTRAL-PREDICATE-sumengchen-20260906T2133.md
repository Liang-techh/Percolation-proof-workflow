---
kind: review_result
review_id: T-FLT-SPECTRAL-PREDICATE-SUMENGCHEN-20260906T2133
task_id: T-FLT-SPECTRAL-PREDICATE
source_agent: 苏梦辰
created_at: 2026-09-06T21:33:00-06:00
integration_status: pending
admission_label: architecture_only
---

# Provenance/version reconciliation for T-FLT-SPECTRAL-PREDICATE

## Exact question

Do the two recently integrated reviews for `T-FLT-SPECTRAL-PREDICATE` independently review the same Lean artifact, and can their evidence be treated as one coherent current-sidecar admission record?

## Inspected commit / paths

Current main inspected at:

- `79c2e82c9e1b064712e8e7dd11eba287539ffe03`

Compared against the commit explicitly recorded by 星宿仙尊:

- `725c3a9dd60aca6aad5277bf2c102b429dfd5973`

Paths:

- `agent_review_inbox/review-T-FLT-SPECTRAL-PREDICATE-xingxiuxianzun-20260906T2123.md`
- `agent_review_inbox/review-T-FLT-spectral-predicate.md`
- `examples/anthropic_flt_spectral_predicate_sidecar/AnthropicFLTSpectralPredicateSidecar.lean`
- `examples/anthropic_flt_spectral_predicate_sidecar/README.md`
- `agent_review_inbox/task_queue.md`
- `docs/agent-review-integration-log.md`

## Evidence

### 1. The 星宿仙尊 review is internally source-bound to an older sidecar version

At commit `725c3a9d...`, the Lean file has Git blob SHA:

- `b851cea7cb225ad134c10618a67a8ade4d8a00a8`

and contains the generic abstraction:

- `eigenspaceSet (T : V →ₗ[R] V) (μ : R) : Set V := {v | T v = μ • v}`
- `range_eq_eigenspaceSet`
- `exists_injective_range_eq_eigenspaceSet`

This matches the theorem names and source hash recorded by 星宿仙尊.

The review file itself currently has Git blob SHA:

- `62566f51e3d9d5b1ccaa04d86714577b6de01a2d`

### 2. Current main contains a materially different Lean artifact

At current main `79c2e82c...`, the same Lean path has Git blob SHA:

- `e2d768a837fb3d5ca8562d52b8dd8dd07cf072a8`

The current theorem is instead a concrete `Fin 2 → ℚ` model using Mathlib's canonical eigenspace API:

- `operatorFamily`
- `scalarPredicate`
- `eigenspacePredicate`
- `range_eq_eigenspace_of_operatorFamily`
- `eigenspacePredicate_iff`

The current README also explicitly describes a concrete range-to-eigenspace equality over `Fin 2 → ℚ`.

### 3. The second review corresponds to the current concrete artifact, but its metadata is incomplete

`agent_review_inbox/review-T-FLT-spectral-predicate.md` has Git blob SHA:

- `6877dcab248de5b5a4e5d87c13ff4d6349cdae5c`

It describes the current concrete theorem and records focused Lean compile exit code `1`, blocked by a missing Mathlib `.olean` file. However, its YAML header lacks the README-required fields:

- `review_id`
- `created_at`
- inspected commit/source commit
- explicit `admission_label`

The integration marker therefore records `created_at: unknown` and `source_commit: unknown`.

### 4. Git comparison confirms the sidecar changed after the 星宿仙尊-inspected commit

`compare 725c3a9d... -> 79c2e82c...` reports the Lean file as modified with:

- 69 additions
- 57 deletions

and also reports modifications to the sidecar README/lakefile plus creation of the later Codex review.

Therefore the two reviews are not two independent reviews of one identical theorem body. They are reviews of two different versions of the same task/path, although both preserve the same high-level boundary: self-contained local abstraction, not direct Anthropic FLT theorem reuse, and no registry/Route-B promotion.

## Commands / checker evidence

Repository evidence only; no Lean/kernel claim is made in this review.

- fetch current main branch -> `79c2e82c9e1b064712e8e7dd11eba287539ffe03`
- fetch Lean sidecar at `725c3a9d...` -> blob `b851cea7...`
- fetch Lean sidecar at current main -> blob `e2d768a8...`
- compare commits `725c3a9d...` to `79c2e82c...` -> sidecar materially modified
- fetch both review files and current README

No local compile was executed by 苏梦辰. No exit code or `#print axioms` output is claimed here.

## Conclusion

Admission effect remains **none**.

The current task should remain `reviewed_pending`. The current concrete sidecar has a genuine eigenspace proposition, but focused Lean/kernel evidence is still absent because the available compile attempt stopped at an incomplete Mathlib dependency.

The important correction is provenance wording: the two integrated reviews should not be described as independent validation of the same exact artifact. The 星宿仙尊 review is valid for the older generic sidecar at commit `725c3a9d...`; the Codex review describes the later concrete canonical-eigenspace version on main.

## Proposed integration

Documentation/provenance only:

1. Keep both original review files immutable.
2. Treat this review as the version-reconciliation companion record.
3. If integration log wording is updated later, say that two reviews cover successive predicate-sidecar versions and agree only on the admission boundary, not that both independently validated an identical Lean file.
4. Do not promote registry/DAG/state from this finding.

Requested admission label for this review: `architecture_only`.

## Unresolved blockers

1. The current concrete sidecar still needs a focused Lean compile after the Mathlib object files are available.
2. Exact `#print axioms` output for `range_eq_eigenspace_of_operatorFamily` is still missing.
3. The current concrete-sidecar review lacks durable `review_id`, `created_at`, inspected commit, and explicit admission label; because the original review is already integrated/immutable, repair should be through a new companion record rather than rewriting it.
4. Direct Anthropic FLT theorem reuse remains unproven.

## Response / handoff

苏梦辰 did not claim a stale `open` queue entry because `T-P3-002`, `T-P4-002`, and `T-P8-002` already have review files in the inbox. Instead, this pass reconciled the newest spectral-predicate evidence. Main currently contains a different theorem body from the one inspected by 星宿仙尊; both versions are useful, but their provenance must stay versioned. The next useful action is focused Lean compilation of the **current** `e2d768a8...` sidecar, with exact commit/blob binding and `#print axioms` captured in a new review_result.
