---
kind: review_result
task_id: T-P3-004
source_agent: Codex
created_at: 2026-09-06T00:00:00-06:00
integration_status: pending
---

# T-P3-004 source-semantic adapter design audit

## Scope and judgment

This is a read-only, fail-closed design review for the smallest admissible
adapter from the canonical Julia/DH source manifest to Lean/checker semantics.
I inspected the existing source-binding audit snapshots and the read-only
manifest checker, and I did not run any full interval search, mutate
authoritative state, touch registry data, or change any external source.

The correct conclusion is still `pending`. The current artifacts are enough to
state the semantic premises and the input contract, but not enough to claim
that hash equality itself proves Julia/DH semantic equivalence.

## Inspected evidence

Inspected paths:

- `agent_review_inbox/task_queue.md`
- `agent_review_inbox/review-T-P3-003-source-manifest.md`
- `examples/routeb_source_binding_audit/REPORT.md`
- `examples/routeb_source_binding_audit/SHA256SUMS.csv`
- `examples/routeb_source_binding_audit/snapshots/current_exact/reference.json`
- `examples/routeb_source_binding_audit/snapshots/current_exact/ReferenceMass.lean`
- `examples/routeb_source_binding_audit/snapshots/current_exact/ChristoffelPower.lean`
- `examples/routeb_source_binding_audit/snapshots/current_exact/PotentialSlice.lean`
- `examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl`
- `examples/routeb_source_binding_audit/snapshots/original_target/routeB_fourier_mass_full_rational.csv`
- `examples/routeb_source_binding_audit/snapshots/original_target/routeB_fourier_potential_rational.csv`
- `examples/routeb_source_binding_audit/snapshots/original_target/routeB_fourier_rational_probe.py`
- `scripts/routeb_source_binding_manifest.py`
- `docs/routeb-source-binding-manifest-README.md`

The minimal manifest checker is explicitly read-only and fail-closed. It
verifies the 14-state order, checks the declared metadata fields, requires the
literal `float64_marker: true`, and hashes only the declared source files under
`--source-root`. It does not establish semantic equivalence and it does not
promote anything into an authoritative registry.

## Smallest admissible semantic adapter

The smallest adapter I can defend from the available evidence has this shape:

1. canonical source manifest is treated as a provenance input, not a proof;
2. Lean/checker semantics are admitted through explicit premises, not inferred
   from identical hashes;
3. the source-order contract remains fixed to `q1..q6, v1..v6, w, c`;
4. arithmetic remains explicit: the current exact sidecar uses
   `fractions.Fraction`, while the Julia source uses `Float64`, and that gap
   must remain visible in the adapter;
5. coordinate and finite-difference conventions stay explicit, including the
   fixed regularizer and the fixed finite-difference step already recorded in
   the source audit;
6. the adapter must preserve `pending` admission and never upgrade a compiled
   or checked artifact into a verified source-binding claim on its own.

That is the right boundary for a disjoint `examples/routeb_source_semantic_adapter/`
style sidecar if one is created later. The adapter can carry premises such as:

- declared source-root identity;
- manifest/receipt metadata equality;
- declared coordinate order equality;
- declared arithmetic contract equality;
- checker-side acceptance of the manifest inputs;
- explicit non-claim that hash equality implies semantic equality.

## What the adapter must not do

The adapter must not:

- run a full interval search;
- infer semantic equivalence from SHA-256 agreement;
- silently replace the authoritative source root;
- mutate registry or admission state;
- conflate documentary provenance with a checker-level proof;
- erase the distinction between exact rational reconstruction and Julia
  `Float64` execution.

## Admission boundary

The present evidence supports only a `pending` admission label. The available
artifacts are enough for a read-only bridge description, but not enough for a
semantic binding theorem. In particular, the adapter still needs a separate
machine-checkable receipt if it is ever to connect canonical Julia/DH source
manifest data to Lean/checker semantics beyond provenance.

## Recommendation

Keep the work item as a review-only deliverable unless a dedicated
`examples/routeb_source_semantic_adapter/` sidecar is explicitly introduced.
If that sidecar is created later, it should be minimal, disjoint, and premise-
driven, with the coordinate/order/arithmetics contract spelled out in the file
header and with `pending` preserved as the admission status.
