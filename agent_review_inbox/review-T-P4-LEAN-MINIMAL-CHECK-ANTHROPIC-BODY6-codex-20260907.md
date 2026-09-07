---
kind: github_receipt_task_draft
task_id: T-P4-LEAN-MINIMAL-CHECK-ANTHROPIC-BODY6
source_agent: codex-local
date: 2026-09-07
status: TASK_DRAFT_NOT_EXECUTED
---

# Minimal Lean / axiom / placeholder check task

This is a task description and future GitHub receipt publication draft only.
No local Lean/Lake command, comparator, or registry mutation was performed in
the preparation of this file.

## Targets

1. Anthropic countable-cover adapter

   - File: `examples/anthropic_flt_countable_cover_adapter/AnthropicFLTCountableCoverAdapter.lean`
   - Review/provenance: `examples/anthropic_flt_countable_cover_adapter/REVIEW.md`
   - Required declarations:
     - `AnthropicFLTCountableCoverAdapter.second_countable_from_countable_open_embedding_cover`
     - `AnthropicFLTCountableCoverAdapter.sampled_patch_missing_target_point`
   - Provenance pin in the source/review: Anthropic FLT commit
     `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`; preserve the source blob
     recorded by the review.

2. BODY6 active-energy adapter

   - File: `examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ACTIVEENERGYORIGIN20260907.lean`
   - Review context: `examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_20260907_REVIEW.md`
   - Minimal theorem set for the focused axiom audit:
     - `normalized_origin_attempt`
     - `offset_origin_attempt`
     - `raw_origin_attempt`
     - `shifted_origin_attempt`
     - `raw_lifted_origin_rejected_attempt`
     - `shifted_lifted_origin_rejected_attempt`
     - `origin_potential_ledger_attempt`
     - `origin_potential_offset_attempt`
     - `normalized_lifted_origin_attempt`
     - `bound_active_origin_attempt`
     - `bound_active_body6_obstruction_attempt`
   - Preserve the source distinctions already stated in the review: this is an
     active-energy/origin adapter and does not silently establish full BODY6
     source binding, coverage, PSD, flow validity, or a full regularized
     six-body certificate.

## Focused check protocol

The runner must first resolve the pinned Lean/Lake project and record its
`cwd`, `lean-toolchain`, Lake manifest, Lean version, Mathlib revision, and
source commit/hash.  If the imported dependency graph or pinned environment
is unavailable, return `BUILD_ENV_BLOCKED`; do not substitute an unpinned
global Lean installation.

For the Anthropic adapter, use the owning pinned reusable Lean project and run
only the target file, for example from that project root:

```text
lake env lean ../anthropic_flt_countable_cover_adapter/AnthropicFLTCountableCoverAdapter.lean
```

For the BODY6 adapter, run only the target file in the pinned project that
owns its imported Route-B graph.  Do not run a package-wide build or broad
regression.  Capture stdout, stderr, and exit code separately for each target.

The axiom pass is a focused scratch audit: print axioms for only the listed
declarations, capture the output, and classify any `sorryAx`, `admit`, or
nonstandard/unapproved axiom according to the project policy.  The existing
source `#print axioms` lines are evidence targets, not proof of a successful
local run.

The placeholder pass is source-only and must be syntax-aware enough not to
mistake prose or `#print axioms` for declarations.  Reject declarations that
contain `sorry`, `admit`, `axiom`, `opaque`, `native_decide`, or `unsafe` in
the forbidden declaration positions.  A clean text scan is not a substitute
for the kernel axiom output.

## Receipt acceptance boundary

Publish a GitHub receipt only if each focused target has exit code `0`, the
named declarations are present, the focused axiom audit is acceptable, the
placeholder scan is clean, and the environment/source provenance is pinned.
The receipt must include target paths, declaration names, source hashes,
toolchain/Mathlib pin, exact commands, stdout/stderr artifact hashes, exit
codes, and the axiom/placeholder results.

Until those fields exist, status remains `PENDING` (or `REJECTED` for a
present but mismatched/malformed receipt).  A successful compile or clean
placeholder scan alone does not imply `LEAN_VERIFIED`, comparator acceptance,
formal certificate validity, or registry eligibility.

No verified registry or workflow state may be modified by this task.  This
file is a handoff/publication draft, not a runtime receipt.
