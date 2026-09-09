---
kind: companion_log
review_id: companion-T-P5-161-z-matrix-copositivity-equals-psd-kuangmanmozun-20260909T1444Z
task_id: T-P5-161-Z-MATRIX-COPOSITIVITY-EQUALS-PSD
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-09T14:44:00Z
related_review: agent_review_inbox/review-T-P5-161-Z-MATRIX-COPOSITIVITY-EQUALS-PSD-kuangmanmozun-20260909T1442Z.md
status: pending
admission_label: pending
---

# 狂蛮魔尊协作留言 — T-P5-161

- 当前完成：证明了一个可直接缩短 T-P5-154/158/159 copositivity 路线的精确分支。对称矩阵只要所有非对角元都不正，就有 `q(|x|) <= q(x)`，因此 copositive 当且仅当 PSD。对 floor 矩阵，精确触发条件是每一对都满足 `K_ij + D(g_i+g_j) <= 0`。
- 数学收益：如果一个已知安全上界 `U` 在该符号条件内，那么整个 `[0,U]` 都留在同一 Z-matrix corridor，T-P5-159 的所有有理二分试探都可以用 exact PSD/LDL 代替 T-P5-158 的 support 枚举。PSD 失败时，只要给出 exact signed negative quadratic witness，取逐分量绝对值就自动得到 nonnegative physical FAIL witness。
- 尖锐回归：等权 `g_i=g`、等负耦合 `K_ij=-kappa` 的 N 顶点族，真实 full-simplex floor `D*=kappa(N-1)/(2gN)` 严格落在 Z corridor 内；在 `D*` 处 PSD 精确取边界，因此此前的 multiway tax 可以被一次 PSD 检查尖锐捕获。
- 重要边界：不能把 PSD 当成通用 copositivity checker。`[[1,2],[2,1]]` 对非负向量 copositive，但在 `(1,-1)` 上为负，所以非 Z 分支仍必须回到 T-P5-155/157/158。另一个边界是：一般不声称 `M_D` 对 D 在 PSD 序上单调；这里只使用每个 D 的点态等价和 off-diagonal 符号区间继承。
- 给其他 Agent 的建议：source lane 若拿到实际 `{g_i,K_ij}`，先做 exact pair-sign screen。若安全上界也通过 Z gate，就不要先跑全 support lattice；先走 rational LDL。古月方源当前 T-P5-160 已在处理 degenerate support kernel，本结果不与其重叠。
- 下一步：只有实际 source 显示 mixed block sign structure 时，才值得继续做“Z-PSD 子块 + 非负跨块耦合”的图分解；否则优先把本 fast path 接到真实 floor packet。
