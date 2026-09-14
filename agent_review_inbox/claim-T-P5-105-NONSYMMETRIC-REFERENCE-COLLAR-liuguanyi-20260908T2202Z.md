---
kind: task_claim
task_id: T-P5-105-NONSYMMETRIC-REFERENCE-COLLAR
source_agent: 柳冠一
created_at: 2026-09-08T22:02:00Z
inspected_commit: 051e08b78f19539124b37d5a2e9a910ec999d025
status: claimed
integration_status: pending
admission_label: pending
---

# Claim — T-P5-105-NONSYMMETRIC-REFERENCE-COLLAR

本轮未发现梁智炜对“柳冠一”的更新点名。为避免重复 T-P5-104 的对称刚度 generic collar、T-P5-103 的 reference identity、以及其他 Agent 当前 K_path / Lean lane，本 Agent 认领一个最小跨层数学 obligation：

> 将 T-P5-104 的 general-time nominal-reference collar 接到 T-P5-018 已固定的真实 2×2 Route-B reference block，其中实际 stiffness `B` 非对称，必须保留 `B=K-A` 的 skew part；同时给出 reference storage 到 P5-098 hybrid `pB` budget 的 division-free bridge。

边界：只做 exact-real/rational mathematics 和 typed bridge；不做 source admission、provenance re-audit、Lean receipt、Float64/FD/controller/solve、P8 coverage 或 registry mutation。
