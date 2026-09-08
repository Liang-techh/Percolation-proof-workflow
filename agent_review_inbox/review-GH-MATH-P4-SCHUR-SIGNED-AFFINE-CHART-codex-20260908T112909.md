---
kind: review_result
review_id: review-GH-MATH-P4-SCHUR-SIGNED-AFFINE-CHART-codex-20260908T112909
task_id: GH-MATH-P4-SCHUR-SIGNED-AFFINE-CHART
source_agent: codex-signed-affine-chart-interface
created_at: 2026-09-08T11:29:09-06:00
integration_status: pending
admission_label: pending
proof_status: FIXED_RATIONAL_CHART_CAPS_WITH_MISSING_ACTUAL_SOURCE_PACKET
affine_chart_source_witness_found: false
actual_dual_interval_bounds_found: false
actual_quadratic_defect_bound_found: false
source_binding_proven: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
requested_action: provide same-configuration actual measurement and defect-map identities before consuming the isolated signed dual and quadratic bound interface
---

# Signed affine chart：精确 box 消费器已隔离，actual source packet 仍缺

## 1. 交付与 scope

新增 `examples/routeb_schur_signed_affine_chart/NEW_affine_box_caps.py` 与本 review。
它只处理**固定有理 3x6 affine chart、固定 SPD metric/dual vectors、六维有理 box**，
导出两条 signed dual intervals 和一个独立计算的 quadratic D cap。
不是实际 source evaluator、source admission 或已编译 Lean theorem。

本轮读取已有 `review-GH-MATH-P4-SCHUR-SIGNED-AFFINE-CHART-20260908T110210.md`
和 `examples/routeb_p4_schur_joint_threshold_lean/NEW_REASSIGNED_20260908_ACTUAL_DEFECT_GATES.lean`。
消费最新 actual/capture 缺失结论，不重做 rank、Young 或旧 analytic remainder 审计。
没有运行本机 Lean/Lake、Julia、source producer 或全回归。

固定 Route-B candidate configuration 为 half_active_vanis2 full-state domain、
设计 mu=1/1000000、FD h=1/100000、corrected DH force chart，C=(4,5,6)。
本轮刷新 domain SHA
`28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e`
与 DH centered bridge SHA
`3045ea1923148c90c8473c8402c7522e99eeda2c1590a494322ca3950d76a107`，均未变。
该配置是 intended binding，不是本轮实际运行或 source acceptance。

## 2. source affine chart 所需身份

令实际返回 acceleration 为 ahat，analytic corrected residual 与 measurement 为

```text
z_A=M_A*ahat-F_A
   =(M_R*ahat-F_R)+(M_A-M_R)*ahat+(F_R-F_A),
y=X*z_A in R6.
```

要连到 actual port defect d∈R3，须额外证明某个同源 map J_d 和 offset b：

```text
d=J_d*z_A+b,
A=J_d*X^-1,
d=A*y+b.                                               (C)
```

J_d 不能因为维度合适就取坐标投影；它需要从指定 actual/reference residual 和 defect
convention 推导。b 必须保留 controller/reference/nominal acceleration 差异，不能默认零。
X^-1 只用于 measurement chart transport，不是 force metric H。
source 还需绑定 r_actual=r0+d、l_actual=ell+r_actual，且所有向量为同一坐标和单位。

若仅有 y_solve=X*(M_R*ahat-F_R)，还缺 y_model；不得把它改名为上式 y。
如果测量为 yhat=y+xi，则 d=A*yhat+(b-A*xi)；offset correction 及其 bounds 必须保留。
定义 y:=d、A:=I 的 tautological chart 不符合本任务 measurement 意义，也不给 enclosure。

## 3. 两条 dual projections 的精确 enclosure

固定同源对称正定 H=M0_CC^-1，令

```text
u=ell^T H d,
s=(ell+r0)^T H d,
D=d^T H d.
```

注意这里 u/s 是 scalar dual projections，不是 principal route 的 acceleration 向量。
对于固定 chart，设

```text
a_u=A^T H ell,       b_u=ell^T H b,
a_s=A^T H(ell+r0),   b_s=(ell+r0)^T H b.
```

若已证明同一个 y 满足 lo_j<=y_j<=hi_j，则对于 v=u 或 s，

```text
v_lower=b_v+sum_j min(a_vj*lo_j,a_vj*hi_j),
v_upper=b_v+sum_j max(a_vj*lo_j,a_vj*hi_j).
```

这是固定 affine function 在完整 box 的精确 extrema；signed offset b_v 和系数负号
保留，不把 v_upper 强制换成正 absolute norm。
source 集合若比 box 更小，这是有效但可能保守的包络；不能反称 box 角点是 source 状态。

A、b、H、ell、r0 若随状态变化，单次 freeze 数值不构成全 cell bounds。
本轮 Python 明确只接受固定 rational coefficients；实际变量系数必须另有同域全量
包络/相关性证明或分区绑定，本文件没有偷偷实现此推广。

## 4. Quadratic D 必须独立取得

同一 chart 下

```text
D(y)=y^T A^T H A y+2 b^T H A y+b^T H b.
```

本轮 fixed-box checker 通过精确 Sylvester leading-minor 条件检查 H SPD，
再计算六维 box 的全部 64 个 endpoint vertices 的 D 值，取最大 Dcap。
因为 affine pullback 的 Hessian 为 2 A^T H A>=0，每个 box 点是 vertices 的 convex
combination，convexity 给 D(y)<=max_vertex D；反向由 vertex 属于 box，故这是该
固定 rational box 模型的精确 maximum。degenerate intervals 允许，重复 vertices 无害。
这不是重新做 source row rank 或广泛数值回归。

有限算法不认证 H 等于 source reference，也不认证 actual y 在 box 内。
两个 dual intervals 本身不能决定 D：它们可能遗漏与 ell、ell+r0 都正交的 defect 方向。
独立的 D evidence 可以来自本类完整 quadratic enclosure，或其他同源有效二次型证明；
不能由两个 signed scalar cap 凭空生成。

## 5. 直接接到现有 signed Schur gates

仅列接线，不重做已审计的 threshold/Young 推导：

```text
L=ell^T H ell, c0=ell^T H r0,
Qactual=(r0+d)^T H(r0+d),
Pactual=beta-L-2(c0+u)-Qactual,
P0=beta-(ell+r0)^T H(ell+r0),
Pactual=P0-2s-D.
```

把同域 exporter 的 upper endpoints 传为 U=u_upper、S=s_upper、Dcap，
若另证同一点/同域 allocation

```text
2U<=beta-L-2c0-E_A,
2S+Dcap<=P0-t,
```

即可消费现有 `joint_of_signed_defect_caps` 所写的条件结论：
`E_A-Qactual<=Pactual` 且 `t<=Pactual`。
本轮仅检查该 theorem statement，不运行/宣称其编译。
beta、E_A、t、P0 不由本 box checker 产生；必须有相同 reference/normalization/domain 身份。
两条 signed projections 与 D 共用同一 d；禁止把相异 payload 的最有利数字拼在一起。

## 6. 隔离定向检查

`NEW_affine_box_caps.py` 只接受 Fraction tuple，拒绝浮点、错误形状、反向 box 和非 SPD H。
不载入外部源，不写数据文件；source_bound/runtime_verified/registry_eligible 恒为 false。
普通与 -O self-test 均 exit 0，所有 guards 用显式异常，不依赖可移除 assert。

合成例：H=I3、A=[I3,0]、b=(-2,0,0)、ell=e1、r0=e2，
y1..3∈[-1/4,1/4]，其余 y 坐标为0，导出

```text
u in [-9/4,-7/4], s in [-5/2,-3/2], Dcap=83/16.
```

signed 上界为负，说明保留符号而非自动替换为 magnitude；offset 被删掉会改变 dual 与 D。
另一合成 chart 只让 y3∈[-1,1] 进入 defect 第三分量，取 b=0、相同 ell/r0：
两个 dual 都恒为零，但 Dcap=1，确认需要独立 D bound。
这些都是抽象 box 例，不声称物理状态或 source 反例。

复现，仅 stdout：

```powershell
python -B examples/routeb_schur_signed_affine_chart/NEW_affine_box_caps.py --self-test
python -B -O examples/routeb_schur_signed_affine_chart/NEW_affine_box_caps.py --self-test
```

## 7. 字段级最小 obstruction

| actual packet 字段 | 当前材料能否填充 |
|---|---|
| 同配置实际 ahat、M_R/F_R 与 z_A refinement | 没有 actual capture；最新 handoff 只是未执行 capture specification |
| signed y=Xz_A enclosure | 缺失；analytic radius/solve-only residual 不等于此 y |
| d=J_d z_A+b 与 A=J_d X^-1 | 缺少 actual/reference port identity，不能默认投影或 b=0 |
| ell/r0/l_actual 与 H=M0_CC^-1 | 有 symbolic 候选，缺本 intended runtime/source/domain 的同一性 |
| 两条 actual dual interval | 固定 rational box 算法已交付，但缺实际 coefficients 与合法 y enclosure |
| actual D bound | 算法独立计算 quadratic cap，但无实际 chart 输入与 source 包络 |
| beta/E_A/t 与 signed gate | 仍需同状态分配及 physical margin comparison，不能由旧 nominal eta row 搬入 |

此前 affine-source review 已报告同样缺失的 actual/source packet；本轮新增的是隔离
可执行 fixed-chart bound 接口，不是 source witness。domain/centered bridge hashes 未变，
没有证据支持将旧名义/其他域的 remainder 拿来填上述字段；本轮不重复其旧数组审计。

最短下一步是 actual valuation/refinement -> 同源 J_d/b 与 metric/reference -> signed y
包络 -> dual/D exporter -> 已有 signed gates。缺第一步时，新增合成数值不解除 obstruction。
只新增指定 examples/NEW_* 与本 inbox review，保持 pending；无 VERIFIED、source
admission、state/registry 改动或 physical closure。
