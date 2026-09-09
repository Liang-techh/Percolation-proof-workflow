---
kind: companion_log
review_id: companion-T-P5-173-root-free-strict-complementarity-minor-gates-kuangmanmozun-20260909T1744Z
task_id: T-P5-173-ROOT-FREE-STRICT-COMPLEMENTARITY-MINOR-GATES
source_agent: 狂蛮魔尊
created_at: 2026-09-09T17:44:00Z
related_review: review-T-P5-173-root-free-strict-complementarity-minor-gates-kuangmanmozun-20260909T1742Z
status: pending
---
# 狂蛮魔尊协作留言：T-P5-173

- 当前完成：补上 T-P5-171 明确留下的 strict-complementarity 缝隙。对 copositive 零接触，正支撑对应的主块自动是普通 PSD；若该主块 corank=1，则不需要求特征向量或伪逆，只取任意一个 adjugate 列就能得到正的 kernel witness。
- 新的 checker 接口：固定 active support `S` 和 anchor `a`，令 `w_i=Cof_{a,i}(A)`。`det(A)=0` 且所有 `w_i>0` 就给出正 kernel；对每个 inactive `j`，KKT residual `M[j,S]w` 精确等于“把 A 的第 a 行替换成 M[j,S] 后的 determinant”。因此 strict complementarity 等价于这些 row-replacement determinant 全部严格大于 0。
- 与 T-P5-172 的连接：上述 cofactor 与 row-replacement determinant 都是原矩阵 pencil 的 square minors，所以在 `M_D=M_0+D L_g`、`rank(L_g)<=2` 下全部仍然只是二次多项式。可以只用有理 isolating interval 检查严格正号；即使 sharp floor 是无理数，也不需要在证书里保存根号或代数数 nullvector。
- 关键反例：corank>1 时 adjugate 可以整体为 0，但 strict contact 仍真实存在，所以 adjugate gate 失败只能报告“corank-one 分支不适用”，不能报告没有 strict contact；另外 inactive determinant 仅为 0 时，contact support 可能连续扩张，不能把 `>=0` 当 strict complementarity。
- 给其他 Agent 的建议：古月方源的 T-P5-172 可直接作为二次多项式 interval-sign 后端；Lean 槽若后续形式化，只需拆成 active-face PSD、adjugate kernel、row-replacement determinant 三个纯代数 lemma。封不觉未明确退回前，不建议把算力投入 provenance/receipt/re-audit。
- 建议的下一步：如果实际 source candidate 落入 corank-one contact，就优先产出 `{p_S,w_i,h_j}` 的 exact rational coefficient packet；若 adjugate 列全零，则另开 higher-corank kernel-basis + strict residual LP child，不要使用 pseudoinverse 掩盖退化。
- 关联任务/Review：`T-P5-173`、`T-P5-171`、`T-P5-172`、`T-P5-169`。