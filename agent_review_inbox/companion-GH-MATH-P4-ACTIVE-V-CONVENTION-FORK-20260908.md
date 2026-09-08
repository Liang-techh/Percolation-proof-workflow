---
kind: companion_log
task_id: GH-MATH-P4-ACTIVE-V-FUNCTION-ENVELOPE
source_agent: Godel the 6th
created_at: 2026-09-08
integration_status: pending
admission_label: pending
proof_status: CONDITIONAL_CONVENTION_FORK_CENTERED_CANDIDATE
candidate_path: examples/routeb_active_v_function_envelope/NEW_CONVENTION_check.py
candidate_sha256: 3D8181CA125ED3925F85467CD7DE793DE3044C329C078AB3810EAF8F441B4337
review_path: examples/routeb_active_v_function_envelope/NEW_CONVENTION_REVIEW.md
review_sha256: 853E510E2724561F698180BBE729BDE15C6F1CEBDD3A3D1657EB9A2877AF34CE
result_path: examples/routeb_active_v_function_envelope/NEW_CONVENTION_RESULT.json
result_sha256: 4FEAE94228E22EDB9910EB000CBDFAE8685A5295C5B0D02FD4459F2DB44B11D5
lean_compile_status: not_run
source_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

该 companion 消费既有 raw envelope，不重跑其多项式审计，并显式比较 raw、shifted、
cross 与 centered conventions。结论是 raw/shifted/cross 在当前 `u` 与阈值下均
不相容；只有明确不同函数 `F=W-a` 的 centered branch 满足理想初始上界
`F<=27/4000<u`。这不授权静默替换 active V、保留旧阈值或改写 consumer；必须先
取得同一 runtime/source 的函数身份、参数和后续 barrier/coercivity witnesses，
因此仍为 pending。
