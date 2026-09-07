# Route-B O1 body-4 Gram 六项局部修复

日期：2026-09-07。状态：`EXPERIMENTAL_REPAIR_UNCOMPILED`。

本轮只新增本 review 和 `NEW_REPAIR_20260907_BODY4_GRAM_ALGEBRA.lean`。
没有修改旧 attempt、targets、旧 review、state、主 adapter、registry 或其他 agent 文件。
未运行、安装或探测本机 Lean/Lake；未进行远端编译。Lean elaboration/kernel 检查证据为 **0**。

这是旧 review 的独立 successor，不覆盖旧版。旧 review 的 SHA-256 为
`9641D8336AFC705B292C460C25679BF70805515FAFD3B02FD386B457E11F8E86`。

## 六项交付

全部声明属于 `RouteBO1Body4SourceGramRepair20260907`，均为未编译 proof attempt。

| 定理名 | 保留的原目标或 helper 接口 | 本次具体调整 |
|---|---|---|
| `basis_dot` | `Body4BasisDotTarget` | 局部 `expand (u v : V3)` 先把 `Fin 3` 求和变成三个左结合乘积；`change` 固定向量投影后的实数表达式；`ring` 分解出单位圆因子，再 `rw` 消去。 |
| `basis_cross` | `Body4BasisCrossTarget` | `funext` 后明确三个分量的 scalar goal。前两项直接 `ring`，第三项显式分解为 `(r*t' - t*r')*(sin²+cos²)`，减少一个 tactic 链同时处理不同目标的依赖。 |
| `linear_gram` | `Body4LinearGramTarget` | `fin_cases` 后先 `dsimp only [vcol, gv]`，再应用基底内积；局部向量零值等式统一 inactive 行列。其余多项式由 `ring` 处理，唯一非平凡格 `(2,2)` 显式提出 `e²`。 |
| `angular_gram` | `Body4AngularGramTarget` | 同样分离索引归约和基底改写；保留 active joint 3 的整列及 `(0,3)/(3,0)` 余弦项；唯一非平凡格 `(3,3)` 显式使用单位圆。 |
| `inertia` | `Body4InertiaTarget` | 显式 `Body` 索引 `3`、`Fin 3` 行列与 `ℝ` 常数，先固定 statement 再归约 source 常数向量。行列变量用 `row/col`，避免与 targets 中的 `b` 函数混用。 |
| `diagonal_angular_sum` | `(u v : V3)` 的一般化 helper | 给 `inertia.2` 一个完整局部类型 `hI`；逐行把内层和改写为 `if col = row then ... else 0`，消去非对角项，再用 `Finset.mul_sum` 提出 `1/15`。无须展开九个坐标或引入新的矩阵 API。 |

最后一项的旧接口可直接由以下表达式获得，未改变其数学结论：

```lean
RouteBO1Body4SourceGramRepair20260907.diagonal_angular_sum
  (wcol q i) (wcol q j)
```

这只是未来调用示意；本轮没有修改旧 `source_gram` 或 adapter。

新模块只直接导入 `RouteBO1Body4SourceGramTargets`，没有导入旧
`RouteBO1Body4SourceGramProofAttempt`，因此不要求旧 attempt 的全部 36 个声明先通过。
原 targets 的传递依赖仍须能编译；新模块并不是独立于这些依赖的 Lake 项目。
仅打开 ExactSource 与 Targets 两个命名空间，`Q6/Joint/Axis` 来自前者，
`V3/dot/vec` 来自后者；这里 `V3` 是 `Fin 3 → ℝ`，不是另一些模块的 `Fin 3`。

五项 target 的类型保持原样，第六项仅对普通向量参数作一般化。
未把任何未完成 target 或最终等式变成新增假设，未重新定义 Gram 表。

## 数学与源码边界

本轮检查的 source 定义为 `BodySemanticCore.linkMass` 及
`RouteBO1PerBodyExactSource.routeBMass/routeBInertiaScalar/routeBInertia`。
body-4 使用零基 `3`，质量为 `2/5`，惯量对角项已为 `1/15`。
双重求和的指标顺序保持 `u row * inertia row col * v col`。

没有在六项局部目标中发现需要加强假设的数学矛盾或 source 常数缺失。
但 `vcol/wcol` 是 targets 中给出的候选坐标；求出它们的 Gram 表不能建立
它们与 source Jacobian 的相等关系。接到 `Body4SourceGramTarget` 的最小语义证明接口仍是：

```lean
Body4JvTarget
Body4JwTarget
```

必须给这两个原目标提供实际通过 elaboration 的证明，才能用本轮的 Gram 表和
惯量收缩把 source `bodyMass/linkMass` 化到 `gv/gw`。其上游仍涉及 prefix columns、
source origins/axes、COM 与 displacement；本轮没有验证这些几何桥接。
旧 attempt 存在这些名字或脚本，不代表这些接口已完成。

特别是 joint `3` 对 body `3` 是 active：`vcol q 3 = 0` 应由平行向量叉积证明，
不能使用仅在 `3 < j.val` 下成立的 inactive 结论；`wcol q 3` 通常非零。
本轮 `basis_cross` 可服务该几何证明，但没有直接建立该 source 断言。

即使上述 source Gram 接口以后通过，还需独立完成 `Body4GramToPiecewiseTarget`
的标量/三角归一化才能抵达 expected-entry seam；trace fold、`h_body_4`、
Float64 绑定、总矩阵和 registry admission 均不在本轮交付结论中。

## 已执行的检查与未执行的检查

执行了一次内存内 SymPy 精确代数检查，未创建额外脚本或输出文件：

- 任意实符号的基底内积因式分解及三个叉积分量，余项精确为零。
- 两张各 36 格的候选 Gram 表：35 格各为环恒等式，剩余分别为
  `(2,2): e²*(sin²φ+cos²φ-1)` 与 `(3,3): sin²φ+cos²φ-1`。
- 任意三维向量下，`I = identity/15` 的双线性收缩等于内积的 `1/15`。

该命令退出码为 0；这里的退出码仅属于 Python/SymPy。
它检查手工转录的精确多项式恒等式，不解析 Lean，也不验证 source Jacobian，
更不构成 Lean theorem、olean 或 kernel 证据。

本轮静态文本检查针对六个 theorem、五个原 target 类型、一个一般向量 helper、
直接导入、占位 token 及行尾空白。没有将静态检查计为编译成功。
末尾六条 `#print axioms` 是未来检查入口，均未执行。

仍须在一致的 Lean/Mathlib 环境核对以下具体接口：

1. 原 targets 及其传递 imports 是否可 elaboration。若上游失败，记录首个原文件诊断，
   不改上游，不把上游声明作为新增公理。
2. `expand` 中的 `Fin.sum_univ_succ` 是否将索引与加法关联规范化到预期形状；
   三个 `change` 分量是否与当前向量表示定义等同。
3. 两个 Gram proof 的 `dsimp only` 是否完全消掉有限索引 `match`；
   `simp only [← hzero, basis_dot]` 是否只留下标量表达式；
   `try ring` 后是否确实仅留下注释所标的一格。SymPy 支持该数学分支计数，
   但未观察 Lean 实际剩余 goal。
4. 双重求和中 `Finset.sum_congr`、`if col = row` 的 singleton 简化及
   `Finset.mul_sum` 的 elaboration。这里用了明确的行列方向与类型，
   仍不能替代实际运行。
5. 整模块成功后检查全部六个声明及传递依赖的占位情况和 axiom 输出；
   不接受仅有声明文本、局部 `#print` 输出或有错误的整模块日志。

以上是静态风险清单，不是已观察到的 Lean 错误。当前没有 Lean 日志或成功声明清单。

## 文件身份与写入范围

本轮开始读取时的 Git HEAD：`f54e04a3215a65a945036556fe8d5268b50930cf`。

| 文件 | SHA-256 |
|---|---|
| `NEW_REPAIR_20260907_BODY4_GRAM_ALGEBRA.lean` | `B508CA7FB043B2E365E4A99650D9C60C7B4420E01DC221401C13768EABD0D94E` |
| 旧 `RouteBO1Body4SourceGramProofAttempt.lean` | `8D8477F64347B6875B0995D2094FB6F8E8ABA837BC25FFDEF53310EB98B1A322` |
| 原 `RouteBO1Body4SourceGramTargets.lean` | `2D0D2794EDFE745D63A2970C36B53765F3B4BD747480107B1EAB51CF2E2C3CA9` |
| `RouteBO1PerBodyExactSource.lean` | `C09B84677ADEF121488B3CEB53E886D0EF0B028C7979D91F8A7F9BA0FBFCD553` |
| `BodySemanticCore.lean` | `FE15F6CA9993F55FC56E6D2C9CCA5FA8C7F6E9530B9B900A6F111ED96715149C` |

这些哈希仅绑定列出的输入与本次 Lean sidecar，不表示已审计整个 import 闭包。
工作期间观察到其他任务新增 `examples/routeb_fixed_lambda_fold/`；未读取或写入其中内容。
本轮工具写入仅为上述两个新文件，不撤销、提交或注册任何并发变更。
