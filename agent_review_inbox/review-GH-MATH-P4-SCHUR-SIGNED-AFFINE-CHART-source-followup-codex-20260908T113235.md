---
kind: review_result
review_id: review-GH-MATH-P4-SCHUR-SIGNED-AFFINE-CHART-source-followup-codex-20260908T113235
task_id: GH-MATH-P4-SCHUR-SIGNED-AFFINE-CHART
source_agent: codex-affine-actual-source-field-audit
created_at: 2026-09-08T11:32:35-06:00
integration_status: pending
admission_label: pending
proof_status: ACTUAL_HELPER_INPUTS_MISSING_FIELD_MATRIX
actual_affine_helper_instantiated: false
source_binding_proven: false
actual_dual_bounds_found: false
actual_quadratic_bound_found: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
requested_action: supply the actual measurement refinement, port affine map and matching metric before exporting any real helper inputs; reject same-name/dimension substitution
---

# Actual affine helper 输入核对：没有可实例化 packet

## 1. 本轮直接检查

只查 actual/source 输入，不扩展、不执行 synthetic Fraction helper。
读取新协调 companion 与三个现有 payload 的实际字段/形状/source_hashes，
并定向列出 runtime/refinement/capture/physical bridge 候选文件。
runtime 相关结果仍为前轮未执行 capture/refinement specs，没有实际运行 tuple。

外部目录为
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_formal_v1/interval_bounds`。
本轮 raw hashes：

- half_active_vanis2_domain_probe.json：
  `28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e`；
- physical_acceleration_bridge_v1.json：
  `01022d32673ad10e9b1b1da398da15ce624c3f077734c2343e1ec9813fc6bede`；
- force_balance_bridge_dh_v1.json：
  `3045ea1923148c90c8473c8402c7522e99eeda2c1590a494322ca3950d76a107`。

三个 formal 字段均 false。这里只固定 inspected bytes，不重新认证 producer/模型/运行。
本轮只新增本 review；无 helper 修改、新 synthetic 测试、Lean/Lake、Julia 或全回归。

## 2. Exact missing-field matrix

目标是同一 vanis2 configuration 下 d=A*y+b，d∈R3、y∈R6、H=M0_CC^-1，
ell/r0 为同一 actual/reference residual 拆分，且已有 helper 只接受固定有理系数。

| 所需字段 | 实际 payload 中最接近的字段 | 精确不兼容/缺口 | 最小待交 witness |
|---|---|---|---|
| configuration/Omega | domain.angle_radii/velocity_radius/scope；DH bridge.controller、epsilon、domain hash | 有候选域和 gain tokens；没有同次 runtime configuration/valuation | target mu/h bits、effective runtime globals、domain 与调用身份 |
| X | domain.preconditioner，6x6 rational | 只固定矩阵字节，不证明 actual measurement 使用此 X | y=Xz_A 的 actual identity；加载/索引/单位绑定 |
| z_A/actual ahat | capture specification；bridge.substitution 字符串 | 无 M_R/F_R/ahat capture 或 solve/model refinement | z_A=e_solve+(M_A-M_R)ahat+(F_R-F_A)，带有效界 |
| y 与六维 lo/hi | domain.rhs_intervals、forcing_radius、acceleration_radius | 是 forcing/acceleration 等其他量；不是 y=Xz_A 的 signed box | 同一 Omega 上逐分量 lo<=Xz_A<=hi |
| A:R6→R3 | centered bridge.linear_map_A_shape=[6,13]；physical.raw_from_lift_matrix=6x6；physical.S=4x3 | 分别是状态线性 acceleration map、lift transform、远端 complement；均非此 3x6 port-defect map | actual d=J_d z_A+b 与 A=J_d X^-1 |
| b∈R3 | controller offsets、physical bridge lift 坐标 | 未声明 actual/reference port 的 affine offset；不能默认 b=0 | 同一 residual 定义推导 b，含 reference/controller差异与 mismatch |
| H∈R3x3 | physical.S_metric=3x3 | S_metric 是 complement 的 energy metric；同维数不等于 block456 nominal inverse | H=M0_CC^-1 的 exact reference/order/一次 mu 身份及 SPD |
| ell,r0∈R3 | centered expression、lift/nominal参数 | 未供给本 y/d 对应的三维 nominal/port向量及 l_actual 身份 | r_actual=r0+d、l_actual=ell+r_actual，同单位/同域 |
| u interval | 没有该字段 | 不能以正 forcing radius 或 storage 参数改名 | u=ell^THd 的同源 signed lower/upper |
| s interval | 没有该字段 | 同上；需 ell+r0 与相同 d | s=(ell+r0)^THd 的同源 signed lower/upper |
| D upper | physical.energy_target=4x4、domain.contraction_matrix/acceleration_radius | 是不同二次型/对象，不是 d^THd | 同 A,b,H,y 的独立 quadratic enclosure |
| E_A,beta,t,P0 | 上述三个 payload 无完整一组字段 | 同 domain hash 不给 Schur target/storage normalization | 同点 E_A,beta,t，P0=beta-||ell+r0||_H²，适用域 |
| fixed-chart contract | helper 只处理 constant rational A,b,H,ell,r0 | 实际 source 若随 x 变，单点 frozen coefficients 不足 | 常系数身份或经证明的同域扩展/分区证据；不能直接塞入一个采样值 |

上述“没有”只针对本轮实际字段与被消费的 runtime specs，不扩大到整个机器。
特别重要的同维错接是 physical.S_metric：它虽然正好 3x3，但其 reference 来自
old MDD/complement，而不是目标 M0_CC inverse。没有 source identity，不允许拿它填 H。

## 3. 现有 metadata 能连接哪一段

DH centered bridge 的 source_hashes 确实引用这个 vanis2 domain 和同 analytic M/C/G。
这建立候选文件之间的内容指针，不建立 actual solve semantics。
它只输出 rows=[4,5]，且 unresolved_obligations 明确含 physical acceleration lift
代入 A*x/delta_a、Fourier equality-ideal 与 positivity/flowpipe。

physical acceleration bridge 的 source_hashes 只指向 M0 decimal CSV 与 rational
complement CSV，没有 runtime input、X-projected residual 或 vanis2 actual refinement。
它的 raw_acceleration_order/lift_order 是坐标定义，不提供 actual lift 的取值。

因此不能由三份 payload 的字段名拼出 helper 的合法实参。
即使从它们选出数值矩阵使 Python 接受 shape/SPD，那也只会构造一个新合成实例，
不是本任务所要求的 actual source packet。本轮没有这样做。

## 4. Signed-gate consumer 的正确对接顺序

1. **实际输入层**：固定同次或全域 runtime/model 语义，取得 ahat、z_A refinement，
   证明 actual y=Xz_A 的 signed enclosure；不要仅交 y_solve。
2. **port affine 层**：从 actual/reference residual 推出 d=J_d z_A+b，保持 defect sign、
   joint6/远端项和 measurement mismatch；再建立 d=A*y+b。
3. **共同 metric/对象层**：绑定 H=M0_CC^-1、ell/r0/l_actual、E_A/beta/t 的同配置、
   reference、单位、normalization 和 domain。维度相同不能取代这些身份。
4. **bound 层**：确认固定-chart 前提或另有有效扩展，导出 U>=u、S>=s 与独立 Dcap>=D。
   两条 dual 不决定正交 defect 的 D，不得互相替代；本轮不再重复该合成反例。
5. **gate 层**：调用现有 signed gates 时提供两条实际恒等式
   Pactual=beta-L-2(c0+u)-Qactual、Pactual=P0-2s-D，
   再交 `2U<=beta-L-2c0-E_A`、`2S+Dcap<=P0-t`。
   输出只是相应 conditional binding/target；源/轨迹/registry admission 另行处理。

L=ell^THell、c0=ell^THr0；所有 caps 必须同源。不能先选对 gate 最有利的数字再倒填
不同来源的 A/y/b/H，不能把未经认证 analytic radius 挪作 actual y box。

## 5. 最短 obstruction / reopen 条件

第一不可跳过缺口是 **actual y=Xz_A 与 d 的 source-map 身份**；
没有它，后续 dual/D helper 的 synthetic pass 不产生 source 事实。
重开时最少交同配置实际 refinement、signed y enclosure、J_d/b 身份和 matching H/ell/r0，
然后才能生成 helper input/export。无需重新扩展 helper 或重算旧 remainder/rank/Young。

本轮未找到可实例化 packet，未生成 NEW_SOURCE 数据以免将占位数据伪装为实际输入。
仅提交本 exact missing-field review；保持 pending，无 VERIFIED、source admission 或旧文件改动。
