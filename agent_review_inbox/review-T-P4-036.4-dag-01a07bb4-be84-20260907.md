---
kind: review_result
task_id: T-P4-036.4
source_agent: 01a07bbd-be84-7471-b20d-5b0b39fc5d40
created_at: 2026-09-07
integration_status: pending
---

独立 source-order review：deployed `dhport_lib.jl` 的有限传播应按
`T_prev -> A_i -> T_i -> (R_i,o_i,z_i) -> pcom/J -> M/P` 分层。`z_i` 必须在
当前 link 的 `A_i` 之前从父变换提取，不能改用 `T_i` 的 z 轴。

最小接口：

- D1 `DHLinkFiniteDAGEnclosure(i,T_prev_box,theta_box,alpha_box,trig_box,schedule)`
  输出 `A_i,T_i,o_i,z_i` 的 outward boxes；
- D2 `DHChainFiniteGeometryEnclosure(Bq)` 输出六 link 的 geometry、COM、`Jv/Jw`；
- D3 `DHChainFloat64EvaluatorEnclosure(Bq,mu)` 沿源码顺序输出 `M,P`，保留
  `Ri*Ii*Ri'`、`Jv'Jv`、`Jw'*(Ri*Ii*Ri')*Jw` 和 `M += contribution` 的分组。

`mass_matrix` 与 `potential` 在源码中各自重新调用 `fk_frames`；抽象 DAG 可以
共享接口，但 runtime receipt 必须记录两次调用，除非另有缓存等价性证明。中心差分
还要复制 `q±h e_k` 的 evaluator DAG，随后才进入 `C/G` 和 backslash solve。

所需 receipt 至少包括 source/hash、line contract、DH/parameter hashes、phase vectors、
`mu/h` bit patterns、operation schedule hash、runtime/libm/BLAS/rounding/FMA/threading、
每个 box 的输入输出和 coverage、finite/non-NaN/no-overflow 标志。

状态：`T-P4-036.4=OPEN`、`INTERFACE_DRAFT__UNCOMPILED=true`；该 review 不关闭
O2、不改变 `required_node_ids`、不进入 registry，也不改变
`formal_certificate_allowed=false`。
