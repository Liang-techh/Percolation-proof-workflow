---
kind: companion_log
review_id: companion-T-P5-207-copositive-error-polar-cuts-honglianmozun-20260910T0248Z
task_id: T-P5-207-COPOSITIVE-ERROR-POLAR-CUTS
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T02:48:26Z
related_review: agent_review_inbox/review-T-P5-207-COPOSITIVE-ERROR-POLAR-CUTS-honglianmozun-20260910T0248Z.md
related_result_commit: 5855b175ab9794baab7c72a878942d5d95b2d0ac
admission_label: pending
---

# 红莲魔尊协作留言 — T-P5-207

- 本轮没有发现梁智炜对红莲魔尊的新点名；此前明确分配的 `T-P5-100-BASE-STORAGE-COLLAR-MATH` 已由红莲魔尊完成并已有后续 Lean 修复，因此没有重复该 lane。
- 当前推进的是 T-P5-206 的互补数学层：T206 用安全 anchors 从内侧逼近联合 support-error 安全区；T207 证明每个非负状态 `y` 都给出一条精确外侧 cut：`Delta·q(y)<=c0(y)`。违反 cut 的同一个 `y` 就是负 Lyapunov 能量 witness。
- 若参考矩阵 `C0` 在归一化正交锥上严格 copositive，则联合误差安全区恰好是 ratio body `conv{q(y)/c0(y)}` 的 level-one polar；若 `C0` 有零能量方向，则不能做除法，必须先执行 zero-face gate：只要某个零能量方向上 `q_k>0`，任何安全预算都必须令 `Delta_k=0`。
- 对 rational 数据，任一严格不安全的 rational `Delta` 都存在 rational 非负状态 witness；因此 FAIL 侧可以落成纯有理 cut，不需要 eigenvector、sqrt、inverse 或 pseudoinverse。
- 最实用的新接口是双侧 bracket：T206 anchor LP 给 `t_in<=theta(d)`，T207 witness cuts 给 `theta(d)<=t_out`。若某个 rational safe anchor `t_*d` 与一个 witness 满足 `c0(w)=t_* d·q(w)`，则立即得到 exact ray threshold `theta(d)=t_*`，trusted packet 只需交叉相乘检查。
- 精确 2×2 回归显示真实安全区一般不是 polytope：`C0=I`, `Q1=diag(1,0)`, `Q2=[[0,1],[1,0]]` 时，安全区恰为 `a+b^2<=1`。因此 finite anchor 库或 finite witness 库都不能默认升级成全局 closure；只能保持 `inner ⊆ true E ⊆ outer`，直到某条 queried ray 两侧相遇或另有全局 theorem。
- 给其他数学 Agent 的建议：若后续实际 sector packet 出现候选联合误差 `Delta`，失败时优先保留对应 rational state cut，而不是只记录“copositivity FAIL”；这条 cut 可复用来缩紧所有后续 support-budget 查询。若安全，则把该点加入 T206 anchor 库。这样同一 sector 会逐步形成可复用的内外夹逼库。
- 本轮没有做 provenance、receipt、admission、Lean/kernel 或 source promotion；actual P5 source binding、coverage、Float64/interval 与物理语义均保持 pending。