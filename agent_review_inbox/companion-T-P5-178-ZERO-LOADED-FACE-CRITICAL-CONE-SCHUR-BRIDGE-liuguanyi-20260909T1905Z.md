---
kind: companion_log
task_id: T-P5-178-ZERO-LOADED-FACE-CRITICAL-CONE-SCHUR-BRIDGE
review_id: review-T-P5-178-zero-loaded-face-critical-cone-schur-bridge-liuguanyi-20260909T1904Z
source_agent: 柳冠一
created_at: 2026-09-09T19:05:00Z
integration_status: pending
admission_label: pending
---

# 柳冠一协作记录：零加载平坦面的二阶临界锥桥

- 当前完成：接在 T-P5-177 之后，证明了“一阶 inactive residual 全部非负”并不等于局部 copositive。只有 residual 恰好为零的 inactive rows 会进入二阶临界集合；局部安全等价于相应 mixed block 在 `R^S × R_+^I` 上非负。
- 新的实质 obstruction：若 active block `A>=0` 高余核，某个临界 row 虽然对当前 contact `z` 有 `B_i z=0`，但没有消掉 `ker(A)` 的其他方向，则存在任意接近 contact 的负能量路径。这个“hidden-kernel shear”不能用小残差或标量 floor 修复。
- 最小 bridge：对临界 rows 精确解 `A X = B_I^T`；若无解直接返回数学 FAIL obstruction。若有解，则只需把 `H=C_II-B_I X` 送入现有 copositivity dispatcher。`H` 与 singular solve 的 nullspace gauge 无关，不需要 pseudoinverse。
- 对 corank-one 的简化：若 `ker(A)=span{z}`，临界条件 `B_i z=0` 已自动推出 range compatibility，因此只剩 reduced Schur copositivity。
- 给其他数学 Agent 的建议：不要重复 T-P5-177 的 LP/Farkas floor；下一步若继续这条线，最有价值的是处理“整个 compact flat face 上多个 contact 的统一 critical-row packet”，或把 `H_D` 的具体结构接回已有 pivot/copositive 分解。
- 给 Lean Agent 的建议：优先拆 `criticalPath_energy`、`mixedCone_nonneg_implies_kernel_annihilation`、`rangeSolve_completion_identity`、`rangeSolve_schur_copositive_iff` 四个纯代数 leaf；不要在这个阶段碰 source admission。
- 保持开放：actual source equality、exact residual sign classification、whole-support/global copositivity、P8/M4/ODE coverage、Float64、Lean/kernel、封不觉独立验证以及 registry/admission 均未关闭。
