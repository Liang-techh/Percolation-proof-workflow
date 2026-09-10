---
kind: task_claim
task_id: T-P5-279-ONE-SIDED-CUBIC-LOWER-SUPPORT
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T20:50:00Z
inspected_commit: e91c53591227cb1d4197c5580d0e3c12dcc2b09e
status: claimed
admission_label: pending
---

# Claim — T-P5-279 one-sided cubic lower support

承接 T-P5-278 明确保留的 signed cubic remainder lane，但不重复 generic root solver、secant cone 或 quadratic graph-tube elimination。本轮只做数学层：在 one-sided clamp fiber 上保留三阶导数的方向符号，研究如何由 directional third-derivative lower bound 直接产生 sharp cubic Lyapunov lower support，从而避免把 odd cubic 信息先绝对值化再形成 naive sextic tube gate。目标包括：orientation-aware Taylor integral theorem、两侧 fiber 的非对称组合、fraction-free cubic critical-point reduction、严格 separation regression，以及明确 fail-closed 边界。

本轮不做 provenance/receipt/admission/re-audit，不声称 actual P5 source binding、coverage、Float64、Lean/kernel、封不觉独立验证或 parent closure。