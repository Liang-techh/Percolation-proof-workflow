---
kind: task_claim
task_id: T-P5-035
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-07T17:52:00-06:00
inspected_commit: ef81e9d0f507af8cb1b815c5fd5846892a5c2c64
status: active
---

# T-P5-035 claim — near-boundary exact block-(4,5) coercivity

认领一个与其他 source / Lean lane 不重叠的最小数学 child：在 `T-P5-034` 已证明 `Q >= (15/16)V` 且 exact 反例排除 `Q >= (47/50)V` 的基础上，继续寻找显式 exact-rational SOS / scaled-diagonal-dominance 证书，尽量逼近已知 `47/50` 失败边界，并只更新 Lyapunov residual consumer 的算术常数。

边界：不做 provenance、receipt、admission、Float64/source binding、ODE/flowpipe、P8 coverage，也不抢占现有 Lean 编译任务。完成后写新的 immutable `review_result`。
