---
kind: companion_log
task_id: GH-MATH-P4-JOINT6-ACTUAL-RESIDUAL-NEXT
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T04:10:00Z
review_commit: f7a80a3bbdcb404edc2a94dbb03700dd0a251ae3
status: blocked-exact-source-packet
---

# 柳冠一协作留言：principal compact joint6 的 signed defect 已压成单分母桥

本轮按梁智炜明确派工继续处理 `A u + h v = p + z_B` 的 principal compact / physical joint-6 分支，没有混用 lift joint6、preconditioned row6 或 state-library residual。

目前仍没有找到一份把同一 cell 的 `A,h,p,z_B`、实际 `u_hat/v_hat`（或 signed balance defect）、physical observable 绑定、同一 `A` 的 det lower 和完整 signed numerator 同时绑在一起的 source packet，因此 deployed 实例仍是明确 obstruction，不能冒充已闭合。

数学上本轮把剩余接口缩得更小。令 `Delta=det(A)`、observable 为

`O = k^T u + beta v + gamma`。

若实际 solve 满足

`A u_hat + h v_hat = p + z_B^a + e`，

而 contract 使用 `z_B^c`，physical observable 实际读取 `v_obs`，则有精确 signed identity

`Delta (O_obs - O_c(v_hat))`
` = k^T adj(A)e`
` + k^T adj(A)(z_B^a-z_B^c)`
` + Delta beta (v_obs-v_hat)`。

所以 solver defect、`z_B` context defect、observable scalar binding defect 可以在同一个 numerator 中先做 signed cancellation，再 enclosure。若 `|Delta|>=delta>0` 且整个右侧绝对值 `<=E`，目标 mismatch `<=B` 只需无除法 gate

`E <= B delta`。

如果 runtime 不暴露内部 solver residual，也可以直接从同源字段重构

`e_c := A u_hat + h v_hat - (p+z_B^c)`，

然后使用更短的

`epsilon_total = k^T adj(A)e_c + Delta beta(v_obs-v_hat)`。

因此下一步 producer 不需要再造新的 generic residual theorem；最短动作是交付一份 principal compact 同 cell packet：

`(cellKey,A,h,p,z_B,u_hat,v_hat,k,beta,gamma,Delta,delta)`

并补 `v_obs` 绑定以及 signed residual `e`，或允许由这些字段直接重构 `e_c`。缺其中任一关键绑定都继续按 obstruction 处理。

正式数学推导、最小 theorem statements、checker leaf 和未闭合边界已写入 review commit `f7a80a3bbdcb404edc2a94dbb03700dd0a251ae3`。当前不改 P4/P8 parent，不改 admission/registry，不声称 Lean/kernel 或独立验证完成。