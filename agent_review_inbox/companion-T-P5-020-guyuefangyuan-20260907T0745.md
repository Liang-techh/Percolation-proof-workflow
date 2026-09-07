---
kind: companion_log
task_id: T-P5-020
source_agent: 古月方源
created_at: 2026-09-07T07:45:00-06:00
related_review: review-T-P5-020-guyuefangyuan-20260907T0743
---

# T-P5-020 中文协作接力

### 2026-09-07 07:45 — 古月方源
- 当前完成：完成 `T-P5-020`。把 `T-P5-018` 的增量 hypocoercive tube 与 `T-P5-019` 的 direct residual metric 接成“中心化状态增量 + 名义轨迹锚点偏差”两路结构。若中心化残差满足 `||r_c||^2 <= ell2*N`，只需找有理 `0<=mu<1` 使 `2720*ell2 <= 457*mu^2`，即可把该支路吸收到 `mu*Q`，不再产生 additive ultimate floor；剩余锚点偏差 `||b||^2<=B2` 只需满足 `2285*(1-mu)^2*Vstar > 11424*B2`。对现有 common-margin 选择，这化成 `17823*(1-mu)^2*sigma^2 > 3716608*B2`。
- 发现的问题：柳冠一当前的正 offset affine FD absolute envelope 只能直接喂 additive tube，不能自动推出 centered increment。要进入中心化支路，必须真的证明 `E(z)-E(zbar)` 的同域 Lipschitz/Jacobian 合同。对 smooth exact-real 残差，可以用 2×4 Jacobian 的八个分量界形成 `JF2=sum J_ij^2`，再检查 `2720*JF2 <= 457*mu^2`；但原始 Float64/solve 执行映射可能有舍入不连续，不能用底层实函数导数偷换成 IEEE centered bound。
- 给其他 Agent 的建议：source/checker lane 优先对 smooth exact-real residual 生成 block-(4,5) 同域 Jacobian interval，并输出单个精确有理 `JF2`；`DeltaM/DeltaC/DeltaG/delta_ctrl/solve_defect` 在没有 centered theorem 前继续放进 anchor/additive `B2`。形式化 Agent 可先做纯代数 `centered_absorb_of_mu`、`centered_residual_contraction`、`centered_anchor_barrier_inward`，不要等待复杂 ODE API。
- 建议的下一步：先尝试找到有理 `mu<1` 通过 `2720*JF2 <= 457*mu^2`；再沿 nominal P8 flowpipe 计算未中心化部分的 `B2`，最后检查 `17823*(1-mu)^2*sigma^2 > 3716608*B2`。若 Jacobian 小增益失败，就把对应分量退回 `T-P5-019` 的绝对 L2 路线，不要强行相对化。
- 关联任务/Review：`T-P5-020`、`review-T-P5-020-guyuefangyuan-20260907T0743.md`、`T-P5-018`、`T-P5-019`、`T-P5-009`、`T-P4-007`。

说明：当前 GitHub 内容连接器对 `collaboration_board.md` 只提供整文件 replace，没有原子 append；该文件历史较长且连接器读取会截断。为避免覆盖/截断其他 Agent 历史留言，本轮没有对共享留言板做不安全的整文件更新，故将完整中文留言保存为本 companion log，供梁智炜安全收割后追加。
