---
kind: companion_log
task_id: T-P5-024
source_agent: 狂蛮魔尊
created_at: 2026-09-07T09:47:00-06:00
related_review: review-T-P5-024-kuangmanmozun-20260907T0945
---

# T-P5-024 协作摘要

- 当前完成：把 `T-P5-020` 的 centered residual consumer 从“分别估计 `N/Q` 与 `||x+y||²/Q` 再相乘”改成了直接联合估计，证明 exact-rational `25 ||x+y||² N <= 144 Q²`。
- 发现的问题：旧条件 `2720*ell2 <= 457*mu²` 支付了两个不可能同时达到的 worst direction；新的同一 `Q` 联合条件只需 `144*ell2 <= 25*mu²`，允许的 centered gain 精确提高 `4250/4113` 倍，约 3.33%。
- 反例边界：不能继续把常数压到 `23/4`；取 `(x4,x5,y4,y5)=(0,15,0,14)` 时精确有 `4UN-23Q²=924201500160017/10^12>0`。
- 给形式化 Agent 的建议：不要重做 `T-P5-023` cell/path transport；只需新增一个 `block45_joint_residual_metric` exact-rational child，再让已有 `ell2_path` 直接进入 `144*ell2_path <= 25*mu²`。矩阵正定可以用 review 里给出的四个 exact leading principal minors，或改写成 rational LDL/SOS。
- 给 source/P8 lane 的建议：更好的 consumer 常数不能替代 connecting-cell-chain、Jacobian/increment source binding、distal-coordinate variation、anchor bias 与 same-domain flowpipe coverage；这些 premise 仍必须单独提供。
- 关联任务/Review：`T-P5-024`、`review-T-P5-024-kuangmanmozun-20260907T0945.md`、`T-P5-020`、`T-P5-023`。

当前仅为 pending mathematical child，待封不觉独立验证 / 待梁智炜收割与最终整合。
