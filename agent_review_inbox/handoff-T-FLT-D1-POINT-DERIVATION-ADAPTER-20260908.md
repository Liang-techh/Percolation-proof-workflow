---
kind: handoff
task_id: T-FLT-D1-POINT-DERIVATION-ADAPTER
source_agent: 梁智炜
created_at: 2026-09-08T18:40:00Z
integration_status: pending
admission_label: pending
status: READY_FOR_PINNED_LEAN
registry_eligible: false
formal_certificate_allowed: false
artifact_path: examples/anthropic_flt_derivation_adapter/D1_POINT_DERIVATION_HANDOFF.json
requested_action: compile the metadata-defined D1 adapter against an exact target pin; preserve theorem boundary and return real axiom/comparator receipt
---

# D1 pinned Lean handoff

The machine-readable packet is
`examples/anthropic_flt_derivation_adapter/D1_POINT_DERIVATION_HANDOFF.json`.
It binds the Anthropic FLT source repository at commit
`aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`, source file
`Definitions/Def_Algebra_PointDerivations.lean`, Git blob
`a6a95f7e3170eb079c42c30deaa06a562d42f53d`, and the four declaration names.

This is a handoff, not a proof result. The Lean lane must separately establish
the target import/pin, compile output, declaration-level `#print axioms`, and
statement comparator result. No source proof body is copied here, and no
Route-B residual, norm, coverage, or flowpipe claim is implied.
