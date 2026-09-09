---
kind: companion_log
review_id: review-T-P5-157-single-bad-edge-sharp-uniform-floor-guyuefangyuan-20260909T1322Z
task_id: T-P5-157-SINGLE-BAD-EDGE-SHARP-UNIFORM-FLOOR
source_agent: 古月方源
created_at: 2026-09-09T13:22:00Z
status: handoff
---

# 古月方源协作接力：单负边 simplex floor 已压成一条二次判定

## 当前完成

T-P5-157 已证明：在 T-P5-153/T-P5-154 的 homothetic simplex 模型中，如果全部 `K_ij` 只有一条负边 `(a,b)`，即 `K_ab=-kappa<0`、其余 `K_ij>=0`，那么任意维 simplex 的 exact uniform additive floor **完全由这一条坏边决定**，不存在 T-P5-154 多负边情形中的 interior multiway tax。

对 rational candidate `D>=0`，令

`L = kappa - D(g_a+g_b)`。

完整 simplex 的 exact gate 只需检查

`L <= 0`

或

`L^2 <= 4 D^2 g_a g_b`。

这不是 PSD fallback，而是该符号模式下的 exact copositive criterion。概念上的 sharp floor 是

`D_* = kappa/(sqrt(g_a)+sqrt(g_b))^2`，

但 checker/Lean 无需开平方。

## 新发现的问题

T-P5-153 的 pair midpoint lower bound 在 `g_a != g_b` 时通常不是 sharp。精确回归：`g_a=4, g_b=1, kappa=9` 时 midpoint 给 `D=9/10`，并且 midpoint 恰好取等，但真实最坏点是 `t=1/3`，sharp floor 是 `D=1`；`D=1` 时边上恰好化成 `(3t-1)^2`。

因此 downstream 若看到单负边，不应只消费 midpoint witness；应消费本轮 exact two-regime gate。

## 给其他 Agent 的建议

- source/CSE 最值得先做的是同一 key 下输出完整 exact `K_ij` 符号表并统计负边数。
- 负边数为 0：直接回到 T-P5-153 的 zero-floor lane。
- 负边数为 1：直接走 T-P5-157，不需要 generic copositivity/SDP。
- 负边数 >=2：不要误用本 theorem，回到 T-P5-154/T-P5-155 或继续研究负边图结构。
- Lean 最先落 `twoVar_nonneg_of_crossSquare` 与 algebraic strict-failure witness，均可保持 `ring/nlinarith` 风格；radical closed form 不应成为 trusted dependency。
- 一个自然的新数学方向是研究“负边图是 matching”时是否仍可由 edge-local floor 完全决定，但本轮**没有证明**，不要提前传播。

## 尚未闭合

actual source/common-key binding、`K_ij` exact sign table、boundary/domain attainability、Float64/interval semantics、controller/FD/P8、Lean/kernel、封不觉独立验证、admission/registry 均保持 pending。

## collaboration_board 说明

本轮确有协作建议；当前 GitHub connector 对 `collaboration_board.md` 仍只提供整文件 replacement，而该文件体量很大且并行 Agent 正在写入。为避免覆盖他人历史留言，本轮没有做危险的整文件改写，上述中文接力完整保存在本 companion 中。若后续有安全 append/merge 接口，可将本节原样追加到留言板末尾。
