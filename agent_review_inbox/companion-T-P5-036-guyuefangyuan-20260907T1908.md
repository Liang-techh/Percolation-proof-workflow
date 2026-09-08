---
kind: companion_log
task_id: T-P5-036
review_id: review-T-P5-036-guyuefangyuan-20260907T1906
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-07T19:08:00-06:00
integration_status: pending
---

# T-P5-036 中文协作接力

- 当前完成：在 `T-P5-035` 的 joint reserve 上继续保留残差分量方向，精确证明
  `Q >= (27/50)V + (101/500)(x4+y4)^2 + (1/6)(x5+y5)^2`。
- 关键收益：残差第 4 分量的 Young 收费从 `3/2*l4^2` 降为 `125/101*l4^2`，第 5 分量保持 `3/2*l5^2`。在现有 `Vstar=1/4` 上，新的纯有理 first-exit gate 是
  `25000 E4 + 30300 E5 < 2727`；如果主要误差集中在第 4 分量，可认证容量相对旧 scalar-L2 gate 增加精确 `303/250 = 1.212`，即 21.2%。
- 增量 tube：若分别有 `(Dl4)^2 <= mu4 Vd + nu4 dc^2`、`(Dl5)^2 <= mu5 Vd + nu5 dc^2`，在 `Kc=1/12` 边界只需检查
  `6250(mu4+12nu4) + 7575(mu5+12nu5) < 2727`。
- 接近极限：固定第 5 方向 reserve 为 `1/6` 时，第 4 方向的精确临界值约为 `0.2020579837`；本轮选的简单有理数 `101/500=0.202` 距该端点相对仅约 0.0287%。`203/1000` 已有显式有理反例 `(11,13,6,6)`，所以不要继续在这一单参数 diagonal slice 上浪费主算力。
- 给 source/P8 数学 lane 的建议：后续 residual checker 尽量输出 `E4,E5` 或 `(mu4,nu4,mu5,nu5)`，不要过早压成一个 `L2`/`(mu,nu)`；如果还能保留符号相关性或完整 `2x2` metric，再优先尝试 `T-P5-026` 的 SPN/direct-power consumer。
- 给 Lean lane 的建议：最小形式化只需 `block45_componentwise_joint_reserve`、`componentwise_residual_completion_101_500`、`block45_componentwise_iss` 三个 theorem。第一个可直接用 review 中给出的 exact rational `LDL^T` 四平方；不要调用浮点 eigenvalue。
- 与并行任务关系：红莲魔尊的 `T-P5-037` 明确负责 scalar/isotropic coupled completion，本轮只做 componentwise anisotropic reserve，两者不抢占。
- 尚未闭合：真实 source/Float64/FD/solve 绑定、同域 `E4/E5`、P8 coverage、ODE first-exit、Lean compile/axiom、receipt/provenance/admission、P5/P8/M4 parent 均保持 open。

由于共享 `collaboration_board.md` 当前通过 contents API 只能整文件替换，且多人正在高频并发提交；在无法获得安全原子 append 的情况下，本轮没有覆盖留言板历史。请梁智炜下一次安全收割时，将以上“保留 residual 分量预算、不要过早 scalarize”的建议追加到留言板末尾。
