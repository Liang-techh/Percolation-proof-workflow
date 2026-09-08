---
kind: companion_log
task_id: GH-MATH-P4-ACTIVE-V-FUNCTION-ENVELOPE
source_agent: Godel the 6th
created_at: 2026-09-08
integration_status: pending
admission_label: pending
proof_status: EXACT_RATIONAL_UNIFORM_OBSTRUCTION_UNCOMPILED
candidate_path: examples/routeb_active_v_function_envelope/NEW_envelope.py
candidate_sha256: 389EC909A21601FDECFA81AF47E56971031101B30648C6CF2B8FA241828ECBC9
review_path: examples/routeb_active_v_function_envelope/NEW_REVIEW.md
review_sha256: 5A07FAF561C94603F4F7AB496E1D40BAF1B8748285D09CE784B2D233456779E8
result_path: examples/routeb_active_v_function_envelope/NEW_RESULT.json
result_sha256: 71743CE600E1CAAF8BD4F8A4A1E55D7C6972B3644C03374BA4B0323F5DBB88F5
lean_compile_status: not_run
source_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

本 companion 收割 exact rational function-level audit：固定 pinned ideal-real
`Vfull_DH`、同一 block-only `X0`、`r=3/20` 后，脚本以 source-hash 锁定的质量/重力
多项式逐项界给出
`uniform_W_lower=32462895903/6400000000`，而记录的
`initial_storage_upper=492033745203/25600000000000`，严格差为
`129359549866797/25600000000000 > 0`。因此现有 raw candidate 与该初始上界在
整个 X0 上不相容；这是 pending 的数学 obstruction，不是 runtime/Lean theorem。
该结果不选择 active V、不改阈值、不写 registry；仍需确认 active source/config
是否等于该 ideal expression，并保持 `formal_certificate_allowed=false`。
