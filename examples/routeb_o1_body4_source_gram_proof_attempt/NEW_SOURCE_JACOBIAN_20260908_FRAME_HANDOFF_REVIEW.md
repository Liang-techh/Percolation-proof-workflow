# Body-4 frame-to-source Jacobian handoff

状态：`CONDITIONAL_SOURCE_JACOBIAN_SKELETON_UNCOMPILED`。
`integration_status: pending`；`admission: pending`。
配对文件：`NEW_SOURCE_JACOBIAN_20260908_FRAME_HANDOFF.lean`。
没有运行 Lean/Lake，没有编译、kernel 或 VERIFIED 结论。

## 本轮实际增量

已有 20260907 bridge 尝试展开 DH geometry；20260908 PORTS 将 axes/displacements
作为显式条件。新文件只导入 PORTS 候选，补上更上游的条件接线：

```
Body4PrefixColumnsTarget + Body4Slot4TranslationTarget
  -> source axes + source COM + source displacements
  -> PORTS.SourceGeometry
  -> Body4JvTarget / Body4JwTarget
```

这不是无条件 source theorem。两个 frame 目标没有在新文件中给出 inhabitant；
PORTS 本身也未编译，导入它只复用候选脚本，不是认可其证明已通过。
新文件不导入原完整 Gram proof attempt 或 Gram repair，不复制 DH 矩阵展开。
prefix target 的 X/Y 列未使用；本接线只读取其 Z/origin 两列。

`source_com_of_frames` 用实际 `source_body4_com_uses_slots_3_4`，
再用 slot-4 translation 与 slot-3 origin/axis 归约 midpoint。
`source_displacements_of_frames` 用实际 `source_prev_origin_slot` 与显式
`activeJoint -> prefixSlot` 等式，避免把局部 displacement 定义当作源值。

## 索引与更短的 joint-3 分支

- human body 4 明确是 `(3 : Body)`，COM 取 origin slots 3、4。
- active joints 是 0、1、2、3；PORTS 的 active guard 为 `j.val <= 3`。
- 新 `joint3_linear_of_translation` 仅消费 translation 目标：
  `O4 = O3 + (19/100) Z3`，所以 `midpoint(O3,O4)-O3 = (19/200) Z3`。
  实际 source Jv 由 parent-slot adapter 化为 `cross3 Z3 ((19/200) Z3)`，
  再由平行叉积得到零。这条更短接线不需要 prefix 显式坐标或 lift isometry。
- 新 `joint3_angular_of_prefix` 只消费 prefix 目标，保留
  `vec q (sin(phi q)) 0 (cos(phi q))`；绝不把 active joint 3 当作 inactive。
- `inactive_columns` 对严格 `3 < j.val` 调用 semantic core 的两个 inactive
  引理，覆盖 joints 4、5，无几何前提，也不是从 Gram 缺行反推。

## lift 与 source/mass 边界

`lift_laws` 显式并列 PORTS 的欧氏 dot 保持与定向 cross 运输。
裸 `Fin 3 -> Real` 默认 Pi/sup 范数的 metric Isometry 并未声明。
内积保持本身不能给出叉积方向，也不能绑定 source columns。
`vcol/wcol` 已由 vec 给出世界坐标，不能再 lift 一次。

已阅读 `RouteBO1PerBodyExactSource.lean`：sourceBodyMass 经
`contractMass (sourceContract q)` 定义，并有到 bodyMass 的原有接缝。
本轮没有导出 `Body4SourceGramTarget`、expected-entry、trace 或 h_body。
后续质量 2/5、已除三惯量对角 1/15、局部 Gram 表、惯量收缩仍须分别接线；
不能把局部 Gram 恒等式或本轮条件 Jacobian 端点当成完整 source theorem。
精确实数 source 接线也不等于外部运行时或 PDE 验证。

## 静态审阅与后续验证

读取了原 targets、原完整 proof attempt、20260907 bridge、20260908 PORTS
及其 review、Gram algebra repair、PerBodyExactSource、BodySemanticCore、
SourceContractIndexAdapter。仅做文本/类型接口比对、禁止占位符扫描、SHA-256
与写入范围检查；新 Lean 文本没有 sorry/admit/axiom/unsafe 声明。
这不是 elaboration，也不是传递依赖 axiom 审计。

后续在一致的已配置 Lean/Mathlib 环境中需要核验：

1. 原 import 闭包和未编译 PORTS 能加载；新模块需要同目录及原 adapter 的搜索路径。
2. prefix target 的 conjunction 投影、Fin proof-irrelevance/parent-slot 改写可 elaboration。
3. COM/displacement 的有限坐标归约与 ring、contractJv/bodyJv 的定义等价可 elaboration。
4. 条件 Jv/Jw 端点与 joint-3 更短分支的 axiom 输出和退出码。
5. 两个原 frame 目标的无前提证据另行完成；不能把条件证明升级为已闭合 source theorem。

`#print axioms` 只是写入的未来检查命令，未执行。没有安装、探测或运行 Lean/Lake，
没有调用远端编译或运行回归。

SHA-256（字节身份，不是证明）：

| 文件 | SHA-256 |
|---|---|
| 新 FRAME_HANDOFF.lean | 8EBF458E0812B63A911EE4EB64A5A621D6F1ACA074EB7950D7746BEA09A64512 |
| 导入 BODY4_PORTS.lean | 95997701CD6AC1DE61537121F91E629A9E030FA45B36F6FCA5E85422DEABBE42 |
| 原 Body4SourceGramTargets.lean | 2D0D2794EDFE745D63A2970C36B53765F3B4BD747480107B1EAB51CF2E2C3CA9 |

写操作仅新增本配对 Lean 与 REVIEW。没有修改 state、registry、共享 adapter、
旧 attempts/reviews 或其他 agent 文件。工作树存在并发变更及其他未跟踪 olean，
均未触碰，也未当作本轮编译证据。没有对其他 agent 发送消息或写入 inbox。
