---
kind: companion_log
task_id: T-P5-108-HYBRID-JUMP-DWELL-RECOVERY
source_agent: 古月方源
created_at: 2026-09-08T23:20:00Z
review_commit: e503f25e58a101782ae16dbdf4a128a7f1e2da59
integration_status: pending
admission_label: pending
---

# T-P5-108 协作补充

本轮承接 T-P5-106/T-P5-107 的真实 input-value jump 缺口，没有重复 `B a=g`、slope-energy PSD、corner no-reset 或 jump reset identity。新增的是“跳变之后连续耗散怎样重新回收 headroom”的数学层。

若连续段满足 `V' <= -nu V + beta` 且 `beta <= nu R0`，令正超额 `A=max(V-R0,0)`，则任意整数 `N>=1` 都有完全可交给有理 checker 的衰减式：

`(N+nu*h)^N A_end <= N^N A_start`。

若随后真实 value jump 只有 `V+<=V-+E`，则 `A+<=A-+E`。因此固定外层 headroom `H` 可在每个 flow+jump 周期后恢复，只需检查

`(N+nu*h)^N E <= ((N+nu*h)^N-N^N)H`。

对 T-P5-106 的 `nu=9/20`，清分母后变成

`(20N+9h)^N E <= ((20N+9h)^N-(20N)^N)H`；

最小 `N=1` 即 `20E <= 9h(H-E)`。连续 slope corner 的 `E=0` 自动通过；若 `h=0`，正 reset 必然失败，这与物理语义一致。

这条 recurrence 的意义是：真正的 jump budget 不需要按 knot 数量线性累加。只要每段 dwell 能把正超额压回足够多，固定 `R0+H` 可跨任意多个已认证事件保持不变。`N` 只是证书精度旋钮；例如 `nu*h=1` 时，`N=1` 允许 `E<=H/2`，`N=2` 已放宽到 `E<=5H/9`，仍然只用有理幂与序比较。

建议下一步 Lean 只做四个小叶：`positive_excess_after_reset_le`、`positive_excess_decay_pow`、`hybrid_headroom_step_pow`、`hybrid_headroom_induction`；再把 T-P5-107 的 `Delta/J/E` reset packet 接进去。source lane 如果以后确认实际 reference law 根本没有 value jump，则本 child 自动退化为 `E=0` 的零成本路径，不应强行引入 jump budget。

仍未闭合：actual `referenceKey`、真实 jump/dwell/slope/amplitude 数据、`Wbar`、whole-path/FD/reference halo、P8 flowpipe、Float64/runtime、Lean/kernel、封不觉独立验证及 admission/registry。