kind: claim
task_id: GH-MATH-P4-ACTIVE-V-SOURCE-NEXT
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T05:50:00Z
inspected_commit: b0850d66339fa3d4830f5dfbd49b48aec099e9a5
target: actual runtime/source active V identity / anchor-shift normalization / same initial_storage_upper binding
status: claimed

scope:
  - Follow the explicit 梁智炜 assignment in task_queue.md and identify the repository-local runtime/source producer of the active storage V, without changing the active V formula.
  - Determine its anchor/constant-shift convention and whether the same value-level convention is bound to initial_storage_upper.
  - Give the smallest exact bridge into Body6SliceActualStorage, separating derivative equality from value normalization.
  - Prove the exact constant-shift/anchor criterion and record a counterexample showing that sharing only an upper cap cannot identify the additive normalization.
  - If the runtime selector or same-value binding is absent, return the precise source obstruction and the smallest missing witness rather than inventing a convention.

dependencies:
  - agent_review_inbox/task_queue.md assignment GH-MATH-P4-ACTIVE-V-SOURCE-NEXT
  - T-P4-ACTIVE-ENERGY-ORIGIN
  - GH-MATH-P4-ACTIVE-ENERGY-NORMALIZATION
  - existing Body6SliceActualStorage / active-energy origin sidecars

non_overlap:
  - No admission, receipt, registry promotion, or generic provenance audit.
  - No replacement of the active V by a centered, shifted, or cross-term storage unless source identity proves that is the deployed convention.
  - No takeover of P5 reference/collar tasks currently owned by other mathematical agents.

expected_output:
  - immutable review_result with source paths inspected, actual/candidate active-V equality, exact anchor/shift lemma, initial_storage_upper value-level binding outcome, candidate theorem/bridge, failure boundary, and remaining source witness.
