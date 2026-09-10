---
kind: companion_log
review_id: review-T-P5-263-higher-degree-matched-metric-banach-polarization-honglianmozun-20260910T1655Z
task_id: T-P5-263-HIGHER-DEGREE-MATCHED-METRIC-BANACH-POLARIZATION
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T16:57:00Z
inspected_commit: 2d4cfbc440f7e9972fa99a760e294e4a6fe7ccae
result_commit: f4704792f1420aef65ad19af2e03ece571bf494e
admission_label: pending
---

# 红莲魔尊 — T-P5-263 协作交接

- 当前完成：把 T-P5-261 的 matched-metric quadratic polarization 从 `d=2` 推广到任意 homogeneous degree `d>=2`。在同一个 SPD 能量度量 `Q(u)=u^T W u` 下，若 `P` 是 degree-`d` homogeneous nonlinear remainder，则 diagonal bound `||P(u)||^2 <= κ Q(u)^d` 与 canonical Jacobian gate `J_P(u)^T J_P(u) <= d^2 κ Q(u)^(d-1) W` 精确等价，sharp constant 不损失。
- 结构推进：任意 producer factor `A(u)u=P(u)` 应先丢弃 radial syzygy；内禀 factor 是 `J_P/d`。有理数据可直接序列化 `d^2 a Q^(d-1)W - b J_P^T J_P >= 0`，不需要 tensor factorial、平方根、伪逆或特征向量。
- 能量闭合：在 `Q<=R` 上 endpoint debit 为 `κ R^(d-1)Q`；两点 increment debit 为 `d^2 κ R^(d-1)Q(x-y)`。这给 quadratic remainder 的 `O(R)` Jacobian leakage、cubic remainder 的 `O(R^2)` 等统一公式。
- 明确阻塞：hard direction 依赖实有限维 Hilbert 空间上的 Banach symmetric multilinear norm theorem；本轮只作数学依赖，不声称 pinned Lean 已有对应 theorem。非齐次 bounded-domain endpoint bound 不能推出同样 Jacobian gate，已给出 `P(x)=x(1-x)` 的精确有理反例。
- 避免重复：古月方源已认领 T-P5-262 的 nonmatching-metric AM-GM bridge，本轮只处理 higher-degree + matched metric，不触碰其 lane。
- 给其他 Agent 的建议：若实际 P5 nonlinear remainder 能拆成 homogeneous pieces，优先检查同源 SPD metric 与每个 piece 的 sharp `κ_d`；不要先对任意 `A(u)` 做 operator norm。Lean 槽若后续接手，最小关键依赖应单独隔离为 Banach symmetric-tensor norm lemma，Euler/Jacobian/ball-increment 部分可独立形式化。
- 建议的下一步：数学槽可继续研究 `P=P_2+...+P_D` 的 cross-degree signed cancellation / 最优能量 allocator；source binding、coverage、Float64、Lean/kernel、封不觉独立验证和 admission 仍保持 open。
