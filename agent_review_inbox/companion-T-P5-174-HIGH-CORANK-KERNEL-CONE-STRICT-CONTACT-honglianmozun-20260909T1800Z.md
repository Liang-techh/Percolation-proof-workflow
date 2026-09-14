---
kind: companion_log
review_id: companion-T-P5-174-high-corank-kernel-cone-strict-contact-honglianmozun-20260909T1800Z
task_id: T-P5-174-HIGH-CORANK-KERNEL-CONE-STRICT-CONTACT
source_agent: 红莲魔尊
created_at: 2026-09-09T18:00:00Z
related_review: review-T-P5-174-high-corank-kernel-cone-strict-contact-honglianmozun-20260909T1758Z
status: pending
---
# 红莲魔尊协作留言：T-P5-174

- 当前完成：补上 T-P5-173 明确留下的 higher-corank contact 分支。若 active energy block `A>=0`，零能量集合精确等于 `ker A`；严格 active/inactive KKT contact 只需解线性系统 `Az=0, z>0, Rz>0`。
- 新的 exact checker：有理解可以统一缩放为 `Az=0, z>=1, Rz>=1`。若不存在严格 contact，则存在精确对偶 obstruction `u>=0, v>=0, sum(u)+sum(v)=1, Ah=u+R^T v`。这说明某个非负约束组合落进 `range(A)`，因而与所有 flat energy directions 正交；不需要 pseudoinverse 或 eigenvector。
- 关键边界：`adj(A)=0` 不能解释为“没有 contact”。给出的 rank-1/3x3 PSD active block 有 corank 2、adjugate 全零，但 `z=(1,1,1)` 仍给出真实 strict contact；反例同时构造了 full copositive matrix。另一个 full PSD 例子证明 positive zero contact 可以存在而 strict inactive residual 永远为 0，对偶 obstruction 会精确抓住这一点。
- 给其他 Agent 的建议：corank-one 继续优先用 T-P5-173 determinant/adjugate fast path；只有 adjugate 全零或已知 kernel 维数更高时才切到 T-P5-174 的线性 primal/dual packet。不要为了选一个 kernel representative 引入 pseudoinverse。
- 建议的下一步：若后续要做 symbolic `D` 且 high-corank locus 随 `D` 改变，应单独处理参数化 kernel stratification；本轮没有声称该 bilinear `(D,z)` 问题仍是 LP，也没有触碰 source/coverage/Lean/admission。
- 关联任务/Review：`T-P5-174`、`T-P5-173`、`T-P5-171`、`T-P5-170`。
