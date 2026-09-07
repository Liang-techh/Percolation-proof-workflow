---
kind: github_focused_lean_receipt_batch_draft
task_id: T-P4-ANTHROPIC-BODY6-FOCUSED-LEAN-BATCH
source_agent: codex-local
date: 2026-09-07
status: TASK_BOUNDARY_ONLY_NOT_EXECUTED
---

# Focused Lean receipt batch draft

This file is a publication/task-boundary draft only.  No target was compiled,
no GitHub job was run, no comparator was executed, and no verified registry or
workflow state was modified.

The batch contains three disjoint focused targets.  One of the three is
explicitly assigned to the independent GitHub lane for 流川枫.

## Batch allocation

### 1. Anthropic countable-cover topology adapter

- Lane: `FOCUSED_LEAN_LANE`
- Target:
  `examples/anthropic_flt_countable_cover_adapter/AnthropicFLTCountableCoverAdapter.lean`
- Review/provenance:
  `examples/anthropic_flt_countable_cover_adapter/REVIEW.md`
- Declarations:
  - `AnthropicFLTCountableCoverAdapter.second_countable_from_countable_open_embedding_cover`
  - `AnthropicFLTCountableCoverAdapter.sampled_patch_missing_target_point`
- Boundary: the generic countable open-embedding cover API only yields
  second-countability; it does not yield Route-B numerical coverage,
  flowpipe enclosure, or admission.
- Provenance contract: retain Anthropic FLT commit
  `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef` and the exact source blob hash
  recorded in the review.

### 2. BODY6 active-energy origin adapter

- Lane: `FOCUSED_LEAN_LANE`
- Target:
  `examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ACTIVEENERGYORIGIN20260907.lean`
- Review context:
  `examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_20260907_REVIEW.md`
- Focused declarations:
  `normalized_origin_attempt`, `offset_origin_attempt`,
  `raw_origin_attempt`, `shifted_origin_attempt`,
  `raw_lifted_origin_rejected_attempt`,
  `shifted_lifted_origin_rejected_attempt`,
  `normalized_lifted_origin_attempt`, and
  `bound_active_body6_obstruction_attempt`.
- Boundary: normalized/raw/shifted energy candidates remain distinct;
  active-domain membership requires the explicit `V(0,0)` source identity.
  This target does not close BODY6 source binding, full coverage, PSD, or
  flow validity.

### 3. P4 BODY6 Schur-to-scalar adapter

- Lane: `LIUCHUANFENG_INDEPENDENT_GITHUB_LANE` (approximately 1/3 of batch)
- Target:
  `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_Body6SchurScalarAdapter.lean`
- Review:
  `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_Body6SchurScalarAdapter.review.md`
- Focused declarations:
  `RouteBP4032Body6SchurScalarAdapter.toSchurPMIComparison`,
  `RouteBP4032Body6SchurScalarAdapter.conditional_body6_scalar_margin`,
  `RouteBP4032Body6SchurScalarAdapter.missing_comparison_witness`, and
  `RouteBP4032Body6SchurScalarAdapter.negative_scale_witness`.
- Boundary: the adapter consumes an externally supplied BODY6 remainder
  margin and explicit same-domain normalization/target premises; it does not
  identify the `Fin 3` front with a physical/P4 port, prove source binding,
  coverage, PSD, or full P4 closure.

## Shared focused receipt contract

Each target must produce a separate receipt.  A batch-level green summary is
not sufficient.  The receipt must bind:

1. target path, exact declaration names, and source file SHA-256;
2. repository commit, `lean-toolchain`, Lean version, Lake manifest, and
   Mathlib revision;
3. the exact focused command, stdout, stderr, and process exit code;
4. `#print axioms` output for only the listed declarations, with
   `sorryAx`/`admit`/unapproved nonstandard axioms classified explicitly;
5. a declaration-position placeholder scan for `sorry`, `admit`, `axiom`,
   `opaque`, `native_decide`, and `unsafe`;
6. for imported external material, source repository/commit/blob provenance;
7. an explicit statement that the result remains a candidate receipt and does
   not change the verified registry.

The runner must use the pinned project owning the import closure.  If that
environment is unavailable or source hashes drift, status is
`BUILD_ENV_BLOCKED` or `REJECTED`, not a substituted local PASS.  No package-
wide build or broad regression is part of this batch.

## Admission boundary

Until every target has its own exit-0, acceptable axiom audit, clean
placeholder scan, and provenance-bound receipt, the batch remains
`PENDING_FOCUSED_RECEIPT`.  A successful compile alone does not imply
`LEAN_VERIFIED`, source/coverage validity, comparator acceptance, formal
certificate validity, or registry eligibility.  The 流川枫 lane is independent
and must return its own receipt; its result cannot substitute for either
focused lane or alter the registry directly.
