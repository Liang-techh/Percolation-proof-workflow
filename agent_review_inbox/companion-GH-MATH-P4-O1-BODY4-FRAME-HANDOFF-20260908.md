---
kind: companion_log
task_id: GH-MATH-P4-O1-BODY4-FRAME-HANDOFF
source_agent: Sartre the 6th
created_at: 2026-09-08
integration_status: pending
admission_label: pending
proof_status: CONDITIONAL_SOURCE_JACOBIAN_SKELETON_UNCOMPILED
candidate_path: examples/routeb_o1_body4_source_gram_proof_attempt/NEW_SOURCE_JACOBIAN_20260908_FRAME_HANDOFF.lean
candidate_sha256: 8EBF458E0812B63A911EE4EB64A5A621D6F1ACA074EB7950D7746BEA09A64512
review_path: examples/routeb_o1_body4_source_gram_proof_attempt/NEW_SOURCE_JACOBIAN_20260908_FRAME_HANDOFF_REVIEW.md
review_sha256: 2EE47D6CE7E3B54FDBFB49406142A70D6FB9E46E007877BE319E29F085B756B9
lean_compile_status: not_run
source_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

本 companion 将 O1 body-4 的新条件接线纳入 percolation DAG，不修改原候选或
state。其依赖链为：

`Body4PrefixColumnsTarget + Body4Slot4TranslationTarget`
→ source axes/COM/displacements
→ `SourceGeometry`
→ `Body4JvTarget ∧ Body4JwTarget`。

新增的 joint-3 分支只消费 slot-4 translation，可条件性推出线性 Jacobian 列为
零；`inactive_columns` 与 lift 的 dot/cross laws 仍是独立 seam。两个 frame target
没有 inhabitant，PORTS 及本文件均未编译；不提供 source mass/trace/Gram witness，
故只进入 pending，不能关闭 body-4 source theorem。
