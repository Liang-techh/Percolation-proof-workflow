---
kind: review_result
review_id: review-GH-LEAN-BODY5-API-REPAIR-SLICE-PENDING-poincare-20260908
task_id: GH-LEAN-BODY5-API-REPAIR-SLICE-PENDING
source_agent: Poincare the 6th
created_at: 2026-09-08T12:08:00-06:00
status: OPEN_UNCOMPILED
integration_status: pending
admission_label: pending
candidate_path: examples/routeb_b45_source_comparator_lean/NEW_BODY5_API_REPAIR_Q3FromFull20260908.lean
candidate_sha256: 36c2a7c3ce4852441605c972f3f71b86c6d03833ee2a8c1ac6e41bb87e41b9da
source_artifact: examples/routeb_b45_source_comparator_lean/NEW_BODY5_API_REPAIR_SliceCore20260908.lean
source_artifact_sha256: 32232d3abaec56aa5fe5804c05ac8acf5234404e64fb74376d37264e6437338d
requested_action: pinned Lean compile after source contracts are frozen; preserve permutation multiplicity and explicit q3 binding
---

# Body-5 API repair — pending q3 slice interface

This bounded candidate supplies generic `List.Perm` sum transport, seeded folds,
double-sum congruence, decode transport, and a q3 slice entry point derived from
the complete coded permutation. It preserves duplicate partner positions and
does not infer the concrete 16-row/6-entry table, conjugate identity, or source
coverage from a partial list.

The candidate is not compiled in this envelope. Required follow-up includes the
actual `bodyTraceRows5` permutation, the empty constant-filter witness, q3
representative binding, and any downstream G1/G2/isometry obligations. The two
source files and their hashes are retained for later pinned Lean execution; no
Route-B node, registry entry, or admission flag is changed by this result.
