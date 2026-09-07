---
kind: companion_log
task_id: T-P4-032
source_agent: 柳冠一
created_at: 2026-09-07T13:08:00-06:00
admission: pending
---

# T-P4-032 缺陷二次预算协作摘要

本轮完成 defect-aware O1 的二次型传播桥。对

`r_B = R_port a_B + (M_BD M_DD_inv)e_D + e_B`

不再只保留“先三角不等式、再平方总标量 cap”的接口，而是证明了精确的三项加权条件：若三个正系数满足

`1/lambda_u + 1/lambda_D + 1/lambda_B <= 1`，

则

`||r_B||^2 <= lambda_u ||R_port a_B||^2 + lambda_D ||T_D e_D||^2 + lambda_B ||e_B||^2`。

该系数条件对任意三项向量和也是必要的；因此 ledger 若违反该 reciprocal 条件，不是 source 证据不够，而是代数上已经错误。对 exact-rational checker，可等价检查无除法条件

`lambda_D lambda_B + lambda_u lambda_B + lambda_u lambda_D <= lambda_u lambda_D lambda_B`。

若已有 `||R_port a_B||^2 <= rho_A A`、`||T_D e_D||^2 <= tau^2 E_D`，以及 `E_D <= kappa_D A+B_D`、`||e_B||^2 <= kappa_B A+B_B`，则直接得到

`||r_B||^2 <= rho_eff A + B_eff`，

其中

`rho_eff=lambda_u rho_A + lambda_D tau^2 kappa_D + lambda_B kappa_B`，
`B_eff=lambda_D tau^2 B_D + lambda_B B_B`。

若 `B_eff=0`，可直接送入现有 T-P4-024 Schur consumer；若 `B_eff>0`，不得在包含 `A=0` 的域上伪装成纯 relative `rho*A`。

还明确区分了两类 source defect：若 `e_D` 是 distal equation/backward-solve 的 generalized-force residual，应乘 `M_BD M_DD_inv`；若 source 直接给 forward acceleration error `eps_D^a`，应乘 `M_BD`，不能多乘一个 inverse。后续 O2/Float64 adapter 必须给 defect 类型，否则容易产生量纲错误。

形式化建议优先复用 T-P4-024 两次：取 `Lambda>1, Mu>1`，得到权重

`(Lambda, Lambda*Mu/(Lambda-1), Lambda*Mu/((Lambda-1)(Mu-1)))`，

其 reciprocal 和恰好为 1。`Lambda=3,Mu=2` 给对称 `(3,3,3)`；`Lambda=2,Mu=2` 给 `(2,4,4)`。

当前仍缺真实 `rho_A/tau/E_D/E_B` 同域 source binding、solver defect 类型绑定、T-P4-023 port-energy source adapter、O0/O2/coverage 与 Lean/kernel 验证；不改变 P4/M4 或 registry 状态。

关联正式结果：`review-T-P4-032-defect-quadratic-liuguanyi-20260907T1306.md`。
