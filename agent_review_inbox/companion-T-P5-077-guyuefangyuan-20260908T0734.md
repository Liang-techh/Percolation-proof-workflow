---
kind: companion_log
review_id: review-T-P5-077-anchor-localized-invariant-ball-guyuefangyuan-20260908T0731
task_id: T-P5-077-ANCHOR-LOCALIZED-INVARIANT-BALL
source_agent: 古月方源
created_at: 2026-09-08T07:34:00-06:00
integration_status: pending
---

# T-P5-077 中文协作接力

- 当前完成：把 T-P5-074/075/076 之间最后一个明确的 domain/self-map 数学缺口压成 exact-rational gate。若同一 weighted SCC packet 在 source box `B={|x_i-c_i|<=H_i}` 上成立，并且 anchor 有 `Q_W(F(c))<=B0`，则由强单调性直接得到 `mu^2 Q_W(c-x*)<=B0`，无需除法或平方根。
- 关键新 gate：对候选 Lyapunov level `Vstar`，每个坐标计算 `R_i = mu^2*w_i*H_i^2 - mu^2*Vstar - B0`。只要 `R_i>=0` 且 `4*mu^2*Vstar*B0 <= R_i^2`，就严格数学地推出整个 root-centered sublevel `Q_W(x-x*)<=Vstar` 都留在 source box 内。它保留了 root offset 与 state offset 的 cross term，不会像只检查 `A+C<=T` 那样产生假阳性。
- 反例提醒：`F(x)=x-1/2, c=0, B0=Vstar=1/4, H=3/4` 时，粗糙的 `A+C<=H^2` 会通过，但 sublevel 中 `x=1` 已经跑出 box；新的平方 gate 会以 `1/256 < 1/4` 精确拒绝。
- 与 T-P5-075 拼接：若再有 `B0<=mu^2*Vstar`，anchor 自身就在 root sublevel；配合 T-P5-075 的 defective-corrector barrier，每一步都重新落回同一 sublevel，因此可以真正做 induction，保证后续每一步仍处在 T-P5-074/076 的 source-valid box 中。
- 给 source lane 的建议：下一步优先找一个真实 SCC/cell 的同键 `W,mu,Lambda` 后，在一个方便的 rational anchor 直接给出 `B0>=Q_W(F(c))` 和 box halfwidth `H_i`。这是成本很低但能决定 corrector local closure 是否可能的 packet。不要先做大规模 solver/Float64 审计。
- 给 Lean lane 的建议：最小首件是纯标量 `scaled_two_square_sum_le_of_gate`，然后是 `strong_mono_anchor_root_localization_sq`；两者都不需要 matrix API 或 sqrt。苏梦辰当前已经认领 T-P5-076 Lean child，本轮不抢占。
- 边界：root existence 仍必须由 T-P5-074 的 existence layer 或其他同域 theorem 提供；containment gate 失败只能标 `NOT_CERTIFIED_BY_ANCHOR_LOCALIZED_BALL`，不能解释成不稳定或不可逆。
- 关联：`T-P5-074-WEIGHTED-STRONG-MONOTONE-SCC`、`T-P5-075-DAMPED-CORRECTOR-ENERGY`、`T-P5-076-WEIGHTED-GRAM-LIPSCHITZ`、`T-P5-077-ANCHOR-LOCALIZED-INVARIANT-BALL`。

共享 `collaboration_board.md` 当前 GitHub contents 写接口仍是整文件 replacement，无法安全做原子 append；为避免并行 Agent 之间覆盖历史留言，本轮中文协作建议先持久化在本 companion，供梁智炜收割时安全追加到留言板末尾。
