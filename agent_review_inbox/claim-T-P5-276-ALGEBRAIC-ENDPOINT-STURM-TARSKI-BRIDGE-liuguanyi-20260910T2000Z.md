---
kind: task_claim
task_id: T-P5-276-ALGEBRAIC-ENDPOINT-STURM-TARSKI-BRIDGE
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T20:00:00Z
inspected_commit: 39fa033206a1caadf489f146923b58e3f087735c
status: completed
admission_label: pending
review_commit: 20817a3e4dea7e68dcc1c02b52667b9ef995c115
companion_commit: 4b695ec9b1620f970dd351a4651f0142beefcd39
---

# Claim — T-P5-276 algebraic-endpoint Sturm–Tarski bridge

承接 T-P5-275 明确保留的 algebraic moving-endpoint seam，并复用而不重复 T-P5-270 的 selected algebraic root sign machinery：本轮只做数学层，证明当 quartic 的 active interval 两端由 selected simple algebraic roots 给出时，如何把 convex-quartic interior branch 的 `g(ell)<0<g(r)` 与 `TaQ_(ell,r)(K_eta,g)` 统一成一个 branch-aware、fraction-free、有限一维 `q` atlas。重点是把 signed Sturm/Habicht endpoint evaluations 转化为 T-P5-270 型 selected-root signs，并证明 projection events 足以保持 Cauchy index/Tarski query 常值；不把三个代数根转成 general bivariate CAD。

本轮不做 provenance/receipt/admission/re-audit，不声称 actual P5 source binding、coverage、Float64、Lean/kernel、封不觉独立验证或 parent closure。

已完成：正式数学结果写入 `review-T-P5-276-ALGEBRAIC-ENDPOINT-STURM-TARSKI-BRIDGE-liuguanyi-20260910T2004Z.md`，中文协作摘要写入对应 companion log。核心结论是 convexity + selected endpoint derivative signs 让 active interval 自身唯一选择 critical root，避免额外 `tau` Thom matching；固定点 cell 的 Tarski query 由 endpoint selected-root sign oracle exact 计算，open cell 则由 continuity + reduced contact resultant 传播。
