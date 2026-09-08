---
kind: review_result
review_id: review-GH-MATH-P4-BLOCK456-MATCHING-METRIC-BUDGET-PROVENANCE-codex-20260908
task_id: GH-MATH-P4-BLOCK456-MATCHING-METRIC-BUDGET-PROVENANCE
agent: 梁智炜
source_agent: coordinator
created_at: 2026-09-08
status: pending
integration_status: pending
admission_label: pending
proof_status: provenance_correction_only
lean_compile_status: not_run
registry_eligible: false
registry_mutation: false
final_integration: false
---

# Matching-metric budget review 的 provenance 更正

James 的原始 review 保持不变。其第 7 节把已读取的
`review-GH-MATH-P4-DIRECT-BLOCK456-METRIC-TRANSPORT-codex-20260908T090216.md`
SHA-256 写成了带空格的字符串，不能作为权威文件身份。

当前工作树对该文件执行 `Get-FileHash -Algorithm SHA256` 得到的精确值为：

```text
3A6A5C87109CD54BEEB71FFFCA70FDE9876EBF05186A09160A86DAA0CD520EEA
```

本记录只修正 provenance，不修改原 review 的数学结论，不把 matching-metric
budget、interval producer 或 source binding 提升为 verified；仍保持
`pending` / `formal_certificate_allowed=false`。
