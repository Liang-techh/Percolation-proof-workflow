---
kind: task_claim
task_id: T-P5-247-AFFINE-GLN-CHART-COVARIANCE
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T13:03:00Z
inspected_commit: bc7357f28503e98343a825626dd07fe30755e6d2
status: completed
admission_label: pending
review_commit: a25de2d6e01b16133af9dc40d46efcfef6731ef8
companion_commit: de4d08f691fa853c85fce78633e86cd9d7ed89e3
---

# Claim — T-P5-247 affine GL(n) chart covariance

认领 T-P5-246 明确留下的最小独立数学 seam：把 translation-only covariance 提升为一般可逆仿射坐标 `y=Pz+h` 的 exact quadratic/source transport，并给出不需要 `P^{-1}` 的 fraction-free reverse transport。

已完成：证明 source ellipsoid、quadratic Lyapunov target 与 S-lemma block 在 augmented affine congruence 下严格交换；顺序换 chart 与一次合成 chart 完全一致；有理 `P` 下用 `det(P)`/`adj(P)` 给出无除法逆向证书；metric-relative strict reserve 保持，而 raw Euclidean eigenvalue margin 不应跨 chart 比较。结果见对应 immutable review 与中文 companion handoff。数学 only：未做 provenance/receipt/admission/re-audit，未声称 Lean/kernel、source binding、coverage、Float64 或 parent closure。