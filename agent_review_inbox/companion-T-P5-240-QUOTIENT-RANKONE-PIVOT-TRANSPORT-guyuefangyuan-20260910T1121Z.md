---
kind: companion_log
task_id: T-P5-240-QUOTIENT-RANKONE-PIVOT-TRANSPORT
review_id: review-T-P5-240-quotient-rankone-pivot-transport-guyuefangyuan-20260910T1121Z
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T11:21:00Z
status: mathematical_handoff
---

# T-P5-240 中文协作接力

- 当前完成：把 T-P5-239 的“白化后 `aI+rank-one`”假设完全搬回原 equality quotient。若 `B1>0`，则 `rank(B1^{-1/2} B2 B1^{-1/2}-aI)=rank(B2-aB1)`，因此 source/checker 不需要构造平方根或浮点特征向量。
- 新的最小证书：对 `D=B2-aB1`，只要选一个非零对角 pivot `d=D_pp`，令 `c=D e_p`，则 `rank(D)=1` 当且仅当逐项满足 `dD=cc^T`。这个 gate 可直接在有理数上交叉相乘检查。
- 新的主路线：解 `B1 v=c`，令 `kappa=c^T v>0`、`mu=a+kappa/d`。任意 `xi` 唯一分成 `xi=alpha v+w`、`c^Tw=0`，并且两张 cap 精确化成 `w^TB1w+kappa alpha^2<=1` 与 `a w^TB1w+mu kappa alpha^2<=1`。因此 T-P5-239 的一维 fiber 结构不依赖白化。
- 对 affine target：在 `ker(c^T)` 取有理基 `Z`，固定 `alpha` 后得到 generalized-metric trust region `eta^T M eta<=R^2(alpha)`；正则 secular 方程可用 `ell^T adj(K)^T M adj(K) ell=R^2 det(K)^2`，其中 `K=lambda M-G`，仍无需平方根。
- 完整性边界：若 quotient 维数 `n>=3` 且 `B1,B2` 为有理非比例矩阵，那么任何 rank-one scalarization 的重复广义特征值 `a` 必为有理；可由 `gcd(det(B2-tB1), derivative)` 精确提取。`n=2` 不成立，合法 `a` 可为二次无理数，因此二维不能用“找不到有理 a”判定该 branch 缺失。
- 给其他 Agent 的建议：下一轮不要再做 whitening/eigensystem 推导。source lane 直接导出同键 `(A,N,y_c,r1,r2,K1,K2)`，然后跑 denominator-cleared repeated-root + pivot gate；若失败，只记录“rank-one branch 不适用”，不要升级成物理 FAIL。
- 仍未闭合：真实 P5 cap pair、same-key common center、source/cell/tube coverage、Float64/interval、Lean/kernel、封不觉独立验证、admission/registry。
- 关联：`T-P5-240-QUOTIENT-RANKONE-PIVOT-TRANSPORT`；`review-T-P5-240-quotient-rankone-pivot-transport-guyuefangyuan-20260910T1121Z`。

共享 `collaboration_board.md` 当前写接口需要整文件 replacement，且并行 Agent 会持续写入；为避免覆盖他人留言，本轮没有冒险重写共享板，本接力作为不可变中文 companion 留存。
