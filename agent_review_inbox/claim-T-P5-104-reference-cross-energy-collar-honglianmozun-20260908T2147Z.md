---
kind: task_claim
task_id: T-P5-104-REFERENCE-CROSS-ENERGY-COLLAR
agent: 红莲魔尊
source_agent: 红莲魔尊
coordinator: 梁智炜
created_at: 2026-09-08T21:47:00Z
status: claimed
upstream:
  - P5-103-ACTUAL-REFERENCE-CONTEXT-BINDING
  - T-P5-100-BASE-STORAGE-COLLAR-MATH
---

# Claim — T-P5-104 reference cross-energy collar

P5-103 已把 nominal reference 压缩为 constant-coefficient generator + initial identity，但一般时刻仍缺一个不把整条 reference trajectory 当 primitive 的能量上界。本轮只推进这一数学缺口：对
`M qbar'' + D qbar' + K qbar = f(t)` 构造带 `q^T M v` cross term 的 reference Lyapunov storage，给出 exact derivative、division/sqrt-free forcing absorption 与 first-exit collar gate，并记录 raw mechanical energy 无法给 strict pointwise decay 的精确 obstruction。

Non-overlap: 不做 P5-103 source 字段搜索或 Lean formalization；不做狂蛮魔尊已认领的 certificate K-path composition；不做 provenance/receipt/admission/re-audit；不声明 actual reference/source/coverage 已绑定。
