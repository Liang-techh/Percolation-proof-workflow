---
kind: companion_log
review_id: companion-T-P5-206-multisupport-error-allocation-kuangmanmozun-20260910T0231Z
task_id: T-P5-206-MULTISUPPORT-ERROR-ALLOCATION
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T02:31:35Z
related_review: agent_review_inbox/review-T-P5-206-MULTISUPPORT-ERROR-ALLOCATION-kuangmanmozun-20260910T0231Z.md
admission_label: pending
---

# 狂蛮魔尊协作留言 — T-P5-206

- 当前完成：沿 T-P5-204 留下的多生成器误差分配缝隙，给出一个不与古月方源 T-P5-205 重复的数学 closure。若 `C0` 与各 `Q_k` 属于同一 selector/source key，且已经有若干联合安全 anchor `v^(r)`，那么只要存在 `alpha_r>=0`、`sum alpha_r<=1`，并且请求误差 `Delta` 逐坐标不超过 `sum_r alpha_r v^(r)`，即可由一个显式 copositive-cone 分解证明 `C0-sum_k Delta_k Q_k` 仍 copositive。
- 最实用的特例：若只知道每个单独方向的安全端点 `C0-tau_k Q_k`，则同时误差必须按共享预算分配，安全充分条件为 `sum_k Delta_k/tau_k<=1`；等价的无除法版本是找 `alpha_k>=0` 使 `Delta_k<=alpha_k tau_k` 且 `sum alpha_k<=1`。
- 反例：单维 `C0=1, Q1=Q2=1` 中，两个单独方向都允许到 `tau=1`，但 `(Delta1,Delta2)=(1,1)` 会得到 `-1`，因此绝不能把各生成器的独立容差同时取满。更强地，对任意给定正 `tau_k`，取 `Q_k=1/tau_k`，真实安全区恰好就是该 simplex；所以仅凭单轴证书无法普遍推出更大的联合区。
- 改进路线：把安全联合点作为 rational anchors 存成矩阵 `V`，以后新的误差向量只需解线性规划 `V alpha>=t d, alpha>=0, 1^T alpha<=1`，即可给出可消费的联合误差比例；LP 失败只表示 anchor 库不足，不代表 Lyapunov 数学失败。若发现新的 pairwise/higher-order 安全点，可直接加入 anchor 库扩大可认证区域。
- 发现的问题：必须维持同一个 `C0/Q_k` 的 source/configuration/selector key；不同 sector 的 anchor 不能混合。`tau_k=0` 时不能用除法式 simplex。当前没有 actual P5 source、coverage、Float64、Lean/kernel 或 admission 升级。
- 给其他 Agent 的建议：古月方源继续 T-P5-205 的 reference-reserve extraction，不要重复本轮 allocation；若 T-P5-205 给出共享 `R,mu,kappa_k`，其 weighted simplex 可以作为本轮 anchor 库的新安全点。Lean 槽未来优先形式化显式分解 theorem，而非先做几何/优化库。
- 建议的下一步：只有实际 sector packet 显示 `Q_k` 存在 disjoint block/support 结构时，才继续强攻“何时联合安全区真正分解成 Cartesian product / product of simplices”；否则当前 anchor-polytope LP 已足够作为 sound rational allocator。
