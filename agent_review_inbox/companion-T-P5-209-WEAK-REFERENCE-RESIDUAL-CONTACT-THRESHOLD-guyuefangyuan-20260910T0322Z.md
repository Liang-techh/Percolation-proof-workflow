---
kind: companion_log
review_id: companion-T-P5-209-weak-reference-residual-contact-threshold-guyuefangyuan-20260910T0322Z
task_id: T-P5-209-WEAK-REFERENCE-RESIDUAL-CONTACT-THRESHOLD
source_agent: 古月方源
agent: 古月方源
created_at: 2026-09-10T03:22:00Z
related_review: review-T-P5-209-weak-reference-residual-contact-threshold-guyuefangyuan-20260910T0320Z
review_commit: 9b453f8e99d0736e55393d6458036b8a3658a17c
status: handoff
---

# 古月方源协作留言 — T-P5-209

本轮补上了 T-P5-208 严格 copositive reference 之外的一条弱参考精确分支：阈值不一定由“正 debit energy 的零接触”达到，也可能由一个始终保持零能量的公共零点，在某个 inactive residual 上先触零而决定。

给后续数学/实现 Agent 的建议：遇到弱 reference 时先检查所有已知 reference zero `z`。若 `z^TQz>0`，任何正半径立即失败；若 `z^TQz=0`，必须继续检查 `Cz >= t Qz`，不能只做 zero-set inclusion。固定公共零支撑上 `M(t)[S,S]z_S=0` 对所有 `t` 恒成立，因此 active determinant 可能恒等于零；这时不要卡在 determinant/root 分支，而应扫描 inactive residual `C[J,S]z_S-tQ[J,S]z_S` 的线性根。若某一正 `Q` residual 在全局 copositive 的候选处恰好触零，则该候选就是 exact ray endpoint。

精确回归建议保留：`C=[[1,1],[1,0]]`, `Q=[[0,1],[1,0]]` 的阈值严格为 `1`，但端点所有零状态的 `Q` energy 都是 `0`，所以 T-P5-208 的 positive-debit contact 不会出现；真正的 sharpness 是 `z=e2` 上第一坐标 residual `1-t` 触零。另一个防误判例子是 `C=diag(1,0)` 配同一个 `Q`：虽然 reference zero 上 `q(z)=0`，但 `Cz=0<Qz`，所以任何正 `t` 都失败。

若公共零点进一步满足完整 `Qz=0`，本轮 Level-1 residual branch 不再给约束，应把它交回 T-P5-179/T-P5-183 类型的 critical/tangent 二阶降维，而不是误报 PASS。建议 Lean 首叶优先做 `positiveRay_zeroFace_residual_domination` 与 `zeroDebit_residualContact_exactRayThreshold`，两者都只需现有 copositive zero-contact perturbation。

说明：本轮已读取 `collaboration_board.md`。当前 GitHub 连接器对该共享大文件仍只提供整文件 replacement，没有原子 append；为避免覆盖其他 Agent 的并行留言，这条中文协作信息写入 immutable companion log，未重写共享留言板。
