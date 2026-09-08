# Body-4 source Jacobian ports — review

状态：`CONDITIONAL_SOURCE_JACOBIAN_SKELETON_UNCOMPILED`；`admission=pending`。
配对文件：`NEW_SOURCE_JACOBIAN_20260908_BODY4_PORTS.lean`。
读取时 HEAD：`6509984f9a045c441df64e088b704ee341a1316d`。

## 本轮增量

已有 20260907 bridge 含 DH-prefix 展开与无前提目标的候选脚本，但未编译。
本轮不重写它，而将索引、lift、active/inactive 接线隔离为只导入原
`RouteBO1Body4SourceGramTargets` 的可独立审阅模块。
复用旧 bridge 的局部证明文本不代表旧证明已通过验证。
新模块不导入旧 geometry/proof attempt 或 Gram repair，避免以其候选声明充当已验证事实。

端点保持原类型，且明确条件：

```lean
structure SourceGeometry : Prop where
  axes : Body4SourceAxesTarget
  displacements : Body4DisplacementsTarget

theorem jacobians_of_source_geometry (h : SourceGeometry) :
    Body4JvTarget ∧ Body4JwTarget
```

本文件没有提供 `SourceGeometry` 的无前提 inhabitant。不能把这个条件端点标记为
无条件 source Jacobian theorem 已完成。新增 `geometry_of_source_targets` 允许用原
source origins、axes、COM 目标组合 displacement，显式揭示 source 证据入口。
该构造器实际只用 origins 0..3；其输入沿用已有完整 origins target，不另造弱化源定义。

## 索引与几何边界

- human body 4 = `(3 : Fin 6)`；COM 端点是 origin slots 3、4。
- `Fin 4 → Joint` 保留值，parent slot 同值；`active_guard` 是 ≤ 3，
  `activeJoint_roundtrip` 消去 Fin 包装。不能改为 < 3。
- joint 3 是 active。其 displacement 是 `e * prefixZ q 3`，
  `joint3_cross_zero` 用平行叉积推出 Jv=0；Jw 保留
  `vec q (sin(phi q)) 0 (cos(phi q))`。没有用 inactive cutoff 得到这列。
- joints 4、5 由真实 `bodyJv_zero_of_inactive/bodyJw_zero_of_inactive`
  和严格条件 `3 < j.val` 得零，不从 Gram 表或 Fourier 缺行反推。
- source 接线调用 `bodyJv_active_formula/bodyJw_active_formula`；
  axes 和 COM-minus-parent-origin 必须来自同一个真实 `sourceContract q`。

缺失的无条件几何证据仍是：从实际 DH prefix 的 origin/z 列与 slot-4 平移，
经现有 source/frame adapter 得到 axes、COM、displacements。
现有 20260907 bridge 给出这些步骤的未编译候选，不能据文本认定缺口已关闭。
slot 4 平移应使用 `F4 = F3 * T3` 与 `T3[:,3]=(0,0,19/100,1)`，
而父轴来自 slot 3；后续验证不可偷换为 slot 4 的轴。

## lift / isometry

`lift q u = vec q (u 0) (u 1) (u 2)`。
`lift_cross` 单独处理定向叉积运输，`lift_dot_isometry` 单独处理欧氏内积保持。
后者不是裸 `Fin 3 → ℝ` 默认 Pi/sup 范数的 metric Isometry；
仅内积保持也不能推出叉积方向保持。二者的三角叶使用单位圆恒等式。

`source_column_dots` 明确先消费 source Jacobian 等式，再将 source 列内积改写为
局部 vcol/wcol 内积。vcol/wcol 已是世界坐标，不再施加第二次 lift。
该端点没有声称局部 Gram 恒等式就是 `Body4SourceGramTarget`。

已读取精确 source 定义：`sourceBodyMass` 经 `contractMass(sourceContract q)`
连接真实 bodyMass；后续 mass 端点仍需质量 2/5、已除三的惯量对角 1/15、
局部 Gram 表及惯量收缩。不得再除三。expected-entry、trace、六体汇总、
外部 source provenance 和 registry admission 均不在本轮完成范围。

## 检查与待验证

本轮仅做静态读取、声明/依赖与写入范围检查；没有运行、安装或探测 Lean/Lake，
没有远端编译，没有运行数值或符号检查。编译与 kernel 证据为零。
`#print axioms` 只是未来检查命令，未执行；无新增 sorry/admit/axiom/unsafe 声明
仅是本文件文本检查，不代表传递依赖已审计。

后续需在一致的 Lean/Mathlib 环境验证：
1. 原 targets/import 闭包可加载。
2. lift 的有限坐标归约、Fin roundtrip 和 parent-slot 改写可 elaboration。
3. geometry 构造器的 conjunction 投影、函数外延与四个 displacement 分支。
4. 条件端点、joint-3 特例、source_column_dots 的函数改写。
5. source geometry 无前提证据另行完成后，才可组合为无条件 Jacobian 端点；
   检查 axiom 输出、完整退出码和源码身份，不以声明文本代替 kernel 证据。

## 读取与身份

读取了原 targets、`RouteBO1PerBodyExactSource.lean`、旧
`RouteBO1Body4SourceGramProofAttempt.lean`、
`NEW_REPAIR_20260907_BODY4_GRAM_ALGEBRA.lean`、20260907 bridge 及其 review，
以及实际路径下的 `BodySemanticCore.lean`、`SourceContractIndexAdapter.lean`。
一次按 targets 同目录寻找 index adapter 未命中，随后通过文件枚举定位并读取正确文件。

SHA-256（只绑定文件字节，不是编译证明）：

| 文件 | SHA-256 |
|---|---|
| 新 PORTS.lean | 95997701CD6AC1DE61537121F91E629A9E030FA45B36F6FCA5E85422DEABBE42 |
| RouteBO1Body4SourceGramTargets.lean | 2D0D2794EDFE745D63A2970C36B53765F3B4BD747480107B1EAB51CF2E2C3CA9 |
| RouteBO1PerBodyExactSource.lean | C09B84677ADEF121488B3CEB53E886D0EF0B028C7979D91F8A7F9BA0FBFCD553 |
| 旧 20260907 BODY4_BRIDGE.lean | F6C2EBB98CC50F4183B348EC95CFA722AEA6F3E72E31375E49B42F4B5A99628E |

本轮写操作仅新增配对的 PORTS.lean 与 PORTS_REVIEW.md。
未修改 state、registry、共享 adapter、旧 attempt/review 或其他 agent 文件。
工作树已有其他 agent 的两个 body6 .olean 未跟踪文件；未读取为编译证据，也未触碰。
最终状态还出现 state.json、其他 review 与 q6 目录的并发变更；没有写入或恢复它们，
不声称整个工作树在本轮期间保持不变。
静态检查发现首次文本提取使用了错误的注释分隔符，导致局部引理未加入新文件；
已在本轮新文件内补回并逐段复查。这是编辑修正，不是 Lean 诊断。
