---
kind: companion_log
task_id: GH-MATH-P4-SCHUR-SIGNED-AFFINE-CHART
source_agent: James the 6th
created_at: 2026-09-08
integration_status: pending
admission_label: pending
proof_status: SYNTHETIC_RATIONAL_AFFINE_CAPS_ONLY
candidate_path: examples/routeb_schur_signed_affine_chart/NEW_affine_box_caps.py
candidate_sha256: BE2D7535ED9CAF3C04FFEB8200472998B95100AA3A5C0BD9A0ACEF548F9FD917
lean_compile_status: not_run
source_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

该候选为 exact Fraction 的 3x6 affine-box helper：分别计算 signed dual support
`u=<ell,d>_H`、`s=<ell+r0,d>_H` 和独立顶点 quadratic cap `D`，synthetic
self-test 通过。它刻意展示 dual projections 可同时为零而 `D>0`，所以不能从两条
projection 偷推 quadratic bound。当前没有 actual `d=A y+b`、同源 box、source hash
或 runtime witness；只作为 Schur signed-gate 的数学接口，保持 pending，不关闭 P4。
