---
kind: companion_log
task_id: T-P5-184-PSD-Z-MATRIX-MONOTONE-RANGE-SOLVE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T20:41:00Z
parent_review: review-T-P5-184-PSD-Z-MATRIX-MONOTONE-RANGE-SOLVE-kuangmanmozun-20260909T2038Z.md
parent_review_commit: a851e8ba5abd1fbb8578d668f9c00a14eeb2b879
status: pending
---
# 协作留言 — T-P5-184

本轮已查看 `README.md`、`task_queue.md`、`collaboration_board.md` 和最新消息。当前没有发现梁智炜对“狂蛮魔尊”的新点名；古月方源已认领 T-P5-183，因此本轮没有进入其 complementary/nonzero-residual transport，而是只处理 T-P5-182 的 exact `R=0` 单调 range-solve 缺口。

## 新数学结论

若 `P` 是对称半正定 Z-matrix（即所有非对角元 `P_ij<=0`），`f>=0` 且普通线性方程 `P x=f` 有解，则把任意解按坐标分成 `x=x^+-x^-` 后，负部自动满足 `P x^-=0`，所以 `P x^+=f` 且 `x^+>=0`。

因此在这个符号区间内：

`f in range(P)` 当且仅当存在 `y>=0` 使 `P y=f`。

矩阵列版本同样成立：若 `F>=0` 且 `P X=F`，则逐项截断 `Y=X_+` 后仍有 `P Y=F`。

## 对 T-P5-182 的直接作用

T-P5-182 需要 `P Y=-B^T` 且 `Y>=0`。若实际 packet 额外满足：

- `P` 对称半正定；
- `P` 非对角元全都 `<=0`；
- `B<=0`；
- `range(B^T) subseteq range(P)`；

那么不需要再跑 LP/Farkas。任取普通有理解 `P X=-B^T`，直接做 `Y=X_+` 即得到所需单调 transport，然后可无损进入 T-P5-182 的 Schur/copositivity descent。

## 反例边界

- 去掉 Z 符号：`P=[[2,1],[1,2]]`、`f=(0,1)`，唯一解 `(-1/3,2/3)`，不存在非负解。
- 去掉 PSD：`P=[[1,-2],[-2,1]]`、`f=(1,0)`，唯一解 `(-1/3,-2/3)`，不存在非负解。
- 去掉普通 range consistency：`P=[[1,-1],[-1,1]]`、`f=(1,0)` 本身无解。
- 去掉 `f>=0`：即使 `P=I`，负分量 RHS 也不可能由非负解产生。

因此该结果只能作为 exact sign-gated fast path；sign gate 不满足时应回到 T-P5-182 的一般 Farkas 路线或 T-P5-183，不得报告数学 FAIL。

## 后续建议

真实 packet 到达后，最便宜的顺序是先 exact screen `P_ij<=0` 与 `B<=0`；通过后只做普通有理 range solve，再 positive-part 截断并直接复核 `P Y=-B^T`。如果区间重化后某些 off-diagonal 跨过 0，则另开 interval/sign-uncertain child，不要把“小的正泄漏”当作 exact Z-matrix。

本轮没有升级 source binding、coverage、Float64/runtime、Lean/kernel、封不觉独立验证、registry/admission 或 P5/P8/M4 parent closure。
