# Route-B O1 human body-4：source-side Gram 最小交接

状态：`OPEN_BODY4_SOURCE_GRAM_CHILD_TARGETS_UNCOMPILED`。本轮新增独立
`RouteBO1Body4SourceGramTargets.lean`，只定义待证 `Prop`，没有提供这些命题的
inhabitant。终点是既有 `h_body_4_expected_entry_target` 和等价展开形式
`h_body_4_source_expanded_target`；`h_body_4_trace_fold_target` 与 `h_body_4`
仍在本轮范围之外。没有运行本机 Lean/Lake，没有提交 GitHub 任务或修改 CI。

本 review 为冻结的 revision 1：定稿后不原地更新，由配套 immutable receipt
绑定内容 SHA-256。后续发现或远端编译结果应新增带独立文件名的 successor
review/receipt 并引用本版哈希；不得把本版 OPEN 状态改写成完成状态。

## 1. 源绑定、索引和精确常数

输入是当前 `RouteBO1PerBodyTraceAdapter.lean`、
`RouteBO1PerBodyExactSource.lean`、`RealDHStep.lean`、
`FrameSlotAccessor.lean`、`SourceContract{,Index}Adapter.lean`、
`BodySemanticCore.lean`，以及既有 body-4 geometry review。
当前文件哈希以配套 JSON 为准；旧 geometry review 正文中的 adapter 哈希
`25F099...` 与当前 `6B50AE...` 不同，不能把旧 provenance 当作当前绑定。

| 数学对象 | Lean 索引/定义 | 本轮取值 |
|---|---|---|
| human body-4 | `Body := Fin 6` | `body4 = 3` |
| human joint 1/2/3/4 | `Joint := Fin 6` | `j = 0/1/2/3` |
| 角度 | `t=q 0, x=q 1, y=q 2` | `phi q = x+y` |
| 原点槽 | `Fin 7` | `o_j` 读 slot `j`，COM 读 slots `3,4` |
| 父轴 | `(sourceContract q).axes j` | `zAxis (routeBFrameSlot q (prevOrigin j))` |
| 空间分量 | `Axis := Fin 3`，`embed3 a : Fin 4` | `a=0/1/2` 为世界坐标 x/y/z |
| Jacobian | `bodyJv ... 3 a j` / `bodyJw ... 3 a j` | **先空间分量 a，后 joint j** |
| Gram/mass | `G i j` | 两个索引都是 joint |
| 质量/惯量 | `routeBMass 3`, `routeBInertia 3 a b` | `2/5`, `if a=b then 1/15 else 0` |

`1/15` 已是 source 中 `I_val/3`；不得再除以 3，也不增加旋转惯量假设。
命题对所有 `q : Q6` 成立，没有增加小角、qcell 或非零分母假设。
receipt 的 state key 仅保留来源合同，不限制这些恒等式的定义域。

令 `er=(cos t,sin t,0)`、`et=(-sin t,cos t,0)`、`ez=(0,0,1)`。
Lean 的 `vec q r u z = r er + u et + z ez` 用显式世界坐标定义。

```text
b = 21/100 sin x       c = 21/100 cos x
d = 1/20              e = 19/200
A = 2/25 + b + e sin(phi)     Lean: aa q
P = c + e cos(phi)            Lean: pp q
Q = b + e sin(phi)            Lean: qq q
```

## 2. 缩小 prefix 目标：slots 0..3 的空间列 + slot 4 的平移列

source 的四个 DH 参数行如下，列顺序是 `(ct,st,ca,sa,a,d)`：

```text
k=0: (cos t,   sin t, 0,-1,  2/25,  1/10)
k=1: (sin x,  -cos x, 1, 0, 21/100, 0)
k=2: (-sin y,  cos y, 0, 1,  0,     1/20)
k=3: (cos q3, sin q3, 0,-1,  0,     19/100)
```

先按 `prefixFrame` 的现有左结合形式做结构展开：
`F0=I, F1=I*T0, F2=(I*T0)*T1, F3=((I*T0)*T1)*T2, F4=F3*T3`。
`Body4PrefixColumnsTarget` 只要求每个空间行 `a` 的四个列值：

| slot | 第 0 列 X | 第 1 列 Y | 第 2 列 Z | 第 3 列 O |
|---|---|---|---|---|
| 0 | 世界 ex | 世界 ey | ez | 0 |
| 1 | er | -ez | et | `(2/25)er+(1/10)ez` |
| 2 | `sin x er+cos x ez` | `cos x er-sin x ez` | et | `(2/25+b)er+(1/10+c)ez` |
| 3 | `cos(phi)er-sin(phi)ez` | et | `sin(phi)er+cos(phi)ez` | `o2+d et` |

特别注意 slot 3 的 Y 列为 **+et**，Z 列中为 **+cos(phi)ez**。
在小的 `Fin 4` 乘法和 `Fin 3` 坐标层展开 `Matrix.mul_apply`，归并
`sin_add/cos_add` 后再 `ring`；不要让 `ring_nf` 穿过整条 source list/fold。
结构展开本身不需要改写矩阵结合律。

`T3[:,3]=(0,0,19/100,1)` 给出单独子目标
`origin F4 = origin F3 + (19/100) zAxis F3`。
这一步对 prefix 的顶端三行直接做 4 项乘法即可，不需要证明 F4 的旋转列，
也不需要展开 q3 的三角式。`q 3` 从这一列已经消失；`q 4,q 5` 从未进入。

然后复用 `source_origin_function_eq_frame_contract`、
`source_parent_axis_slot`、`source_body4_com_uses_slots_3_4`，将以上列式传到
真正的 `(sourceContract q).origins/.axes`。不能停留在另造的几何模型等式。
既有桥接引理只是读取到的源码依赖，本轮没有重新确认其编译状态。

## 3. COM、Jv/Jw 和 inactive 的不同原因

`z0=ez, z1=z2=et, z3=sin(phi)er+cos(phi)ez`；`c3=o3+e z3`。

```text
c3       = A er + d et + (1/10+P) ez
c3-o0    = A er + d et + (1/10+P) ez
c3-o1    = Q er + d et + P ez
c3-o2    = e sin(phi) er + d et + e cos(phi) ez
c3-o3    = e z3

Jv[:,0]  = -d er + A et
Jv[:,1]  = P er - Q ez
Jv[:,2]  = e cos(phi) er - e sin(phi) ez
Jv[:,3]  = 0
Jv[:,4]  = Jv[:,5] = 0

Jw[:,0]  = ez
Jw[:,1]  = Jw[:,2] = et
Jw[:,3]  = z3
Jw[:,4]  = Jw[:,5] = 0
```

`j=3` 满足 active guard，Jv 的零来自 `z3 × (e z3)=0`。
`j=4,5` 的两种 Jacobian 零必须用 `bodyJv_zero_of_inactive` /
`bodyJw_zero_of_inactive`，假设为 `3 < j.val`。不能将 `j=3` 归为 inactive。
因此线速度列最多支持 `{0,1,2}`，角速度列最多支持 `{0,1,2,3}`；
这里不声称在每个 q 上这些列都非零。

只需两个通用坐标引理（已作为独立 Prop 给出）：

```text
dot(vec(r,u,z),vec(r',u',z')) = rr' + uu' + zz'
cross(vec(r,u,z),vec(r',u',z'))
  = vec(uz'-zu', zr'-rz', ru'-ur')
```

前者和后者的证明只在 q0 的 `sin²+cos²=1` 上归约。这样 q0 从 Gram
消去，不必分别证明大量笛卡尔分量的取消式。

## 4. Gram 层：6 个线速度上三角公式 + 小的角速度表

```text
Gv00=A²+d²              Gv01=-d P
Gv02=-d e cos(phi)      Gv11=P²+Q²
Gv12=e(P cos(phi)+Q sin(phi))
Gv22=e²
```

用对称性给出转置项；其余 Gv 项均为零。Gw 的 active 4×4 表为

```text
[[1, 0, 0, cos(phi)],
 [0, 1, 1, 0],
 [0, 1, 1, 0],
 [cos(phi), 0, 0, 1]]
```

任一索引为 4/5 时两种 Gram 均为零。Lean 的 `gv/gw` 已明确给出完整
`Joint × Joint` 定义，不能只完成 active 4×4 就关闭最终 `∀ i j`。
尤其质量矩阵 `(0,3)` 和 `(3,3)` 保留惯量贡献。

先将 inertia 双重求和用对角 guard 降为
`(1/15) * ∑ a, Jw a i * Jw a j`，再代入 Jv/Jw 和 dot 表，得到

```text
sourceBodyMass q 3 i j = (2/5) gv q i j + (1/15) gw q i j
```

这是 `Body4SourceGramTarget`，与最后的三角展开完全分开。

## 5. 只把困难的三角归并分成三个用途

1. Unit circle / addition：q0 的 basis 引理、slot 3 列式、phi 的单位长度。
2. 一个混合点积：`sin x sin(x+y)+cos x cos(x+y)=cos y`。
3. `(0,0)` 的两个平方和一个乘积：
   `sin² x=(1-cos(2x))/2`，同式用于 phi；
   `sin x sin(x+y)=(cos y-cos(2x+y))/2`。

先将 `x-(x+y)=-y`、`x+(x+y)=2x+y`、`2*(x+y)=2x+2y`
作实数环等式改写，再使用 cosine parity；不要要求 ring 自动发现三角恒等式。
所需数学事实对应 Mathlib 的单位圆、加减角、双角恒等式；agent 应在其 pinned
checkout 中核对具体引理名和乘法排列，本轮未调用本机 Lean 查询。

中间二次量为

```text
K = b sin(phi)+c cos(phi) = (21/100)cos y
P²+Q² = 441/10000 + 361/40000 + (399/10000)cos y
e(P cos(phi)+Q sin(phi)) = 361/40000 + (399/20000)cos y
```

`Body4Scalar00Target` 是唯一七项 scalar child。先展开

```text
A²+d² = (2/25)²+d² + (4/25)b + (4/25)e sin(phi)
         + b² + 2be sin(phi) + e² sin²(phi)
```

乘 `2/5`、加 `1/15` 后，常数项为
`(2/5)*((2/25)²+d²+(21/100)²/2+e²/2)+1/15=48511/600000`。
七项和完整 mass 表严格对接 adapter 已有定义：

```text
M00=48511/600000 + (42/3125)sin x + (19/3125)sin(x+y)
    -(441/50000)cos(2x) + (399/50000)cos y
    -(399/50000)cos(2x+y) -(361/200000)cos(2x+2y)
M01=M10=-(19/10000)cos(x+y)-(21/5000)cos x
M02=M20=-(19/10000)cos(x+y)
M03=M30=(1/15)cos(x+y)
M11=211/2400+(399/25000)cos y
M12=M21=21083/300000+(399/50000)cos y
M22=21083/300000, M33=1/15, otherwise=0
```

`M11` 的常数 `211/2400=(2/5)*(441/10000+361/40000)+1/15`；
`M12/M22` 的常数 `21083/300000=(2/5)*(361/40000)+1/15`。
其余 entry 只有有理数整理。目标文件不复制 mass piecewise，直接引用
`body_4_piecewise`，避免另造 RHS 后漏掉 adapter 对接。

## 6. 给 GitHub Lean agent 的证明顺序

所有名字均在 `RouteBO1Body4SourceGramTargets`；下表省略公共前缀 `Body4`。
26 个 Prop 是细粒度检查点，不需要创建 26 个独立文件或工作流。

| 顺序 | 待提供的 Target inhabitant | 依赖/最小工作 |
|---|---|---|
| 1 | `UnitCircle`, `AngleAddition`, `MixedTrig`, `SquareTrig`, `ProductTrig` | 标准实数三角事实，可独立完成 |
| 2 | `PrefixSlots` | `routeBFrameSlot/prefixFrame` 结构展开 |
| 3 | `PrefixColumns`, `Slot4Translation` | 2、四个 exact DH 行、addition |
| 4 | `SourceOrigins`, `SourceAxes` | 3、现有 source slot/parent-axis 桥接 |
| 5 | `Com`, `Displacements` | 4、slots 3/4 中点、有理数环整理 |
| 6 | `BasisDot`, `BasisCross` | UnitCircle，空间坐标三项展开 |
| 7 | `Inactive`, `Jv`, `Jw` | 4/5/6、active guard 与 inactive 引理 |
| 8 | `LinearGram`, `AngularGram` | 6/7 的列式、UnitCircle(phi)；先 10 个上三角格再对称/补零 |
| 9 | `Inertia`, `SourceGram` | source 定义、对角求和消去、7/8 |
| 10 | `QuadraticReduction`, `Scalar00` | MixedTrig / SquareTrig / ProductTrig 和 ring |
| 11 | `GramToPiecewise` | 10，加全部 i/j guard 的有限分支 |
| 12 | `ExpectedEntryHandoff`, `ExpandedHandoff` | 9→11 等式传递；展开 source 定义 |

`LinearGram/AngularGram` 的正式 statement 已针对显式 `vcol/wcol`；其自身
无需 Jv/Jw source equality，故步骤 8 可与 7 并行，步骤 9 才合并两支。
最后 expected-entry 的候选证明形状（必须由远端实际编译）是：

```lean
-- h_source : Body4SourceGramTarget
-- h_normal : Body4GramToPiecewiseTarget
-- goal : Body4ExpectedEntryHandoffTarget
intro q i j
exact (h_source q i j).trans (h_normal q i j)
```

此处没有 trace-fold premise；即使该终点将来编译成功，也不能据此声称
`h_body_4` 已关闭。

## 7. 远端构建与回执要求

该目录当前没有独立 lakefile/lean-toolchain；既有 CI 只执行带
`CI_PORTABLE=1` 的 `verify.sh`，所以仅加入本文件不会自动得到编译证据。
source comparator 的 `COMPILATION_STATUS.md` 记录的是未完成尝试，所记环境
为 Lean 4.33.1 / Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`；
当前 `examples/local_fkg/lean-toolchain` 则写着 4.32.0。不得混用不同版本 olean。

给 agent 的指令：在 GitHub 的隔离工作区核对并固定一个可重建的环境，记录
Lean/toolchain、Mathlib SHA、repo commit 和依赖哈希；从源码按下列次序建立
同一环境下的导入链，而不是复制旧的绝对 output/run 路径：

```text
Mathlib
  FourierNormalForm -> FrameRecursion -> RealDHStep
    -> FrameOriginAxis -> FramePrefixIndex -> FrameSlotAccessor
  BodySemanticCore -> BodyContractCore
  (FrameSlotAccessor, BodyContractCore) -> SourceContractAdapter
    -> SourceContractIndexAdapter / SourceBodyMassExtensionalProbe
    -> RouteBO1PerBodyExactSource
  BodyTraceEvaluator  [adapter 的导入依赖；本轮不要求证明其 fold]
  -> RouteBO1PerBodyTraceAdapter -> RouteBO1Body4SourceGramTargets
```

若导入链不能构建，应回报实际编译诊断并保持 child open，不得用新增 axiom、
占位证明或假设最终 source equality 来跨越。回传实际 theorem 名/statement、
完整编译 exit code、每个最终 inhabitant 的 `#print axioms`、源文件占位审计、
源码/olean 哈希。仅编译这些 Prop 定义还不能算 child theorem 完成。
本交接不授权修改主 adapter、body-3/5、registry 或合并发布；这些文件保持原接口。

## 8. 本轮有限验证和修改边界

新增 `scripts/check_routeb_o1_body4_source_gram.py`，以四个 source DH 参数行
为人工转录输入，从 prefix 矩阵、COM、cross product 重算到 6×6 mass。
SymPy 1.14.0 在 `QQ` 上对四个 unit-circle 方程做多项式余式检查，273 个
标量差式余式均为零，包括 48 个 prefix 空间分量、Jv/Jw、两种 Gram 和全部
36 个 mass entry。没有浮点采样、CSV 检查或 Lean 解析；它只检查所写数学
模型的代数一致性，不能替代 source 转录绑定、三角事实的 Lean 证明或编译。

命令：`python scripts/check_routeb_o1_body4_source_gram.py`（只读、输出到 stdout）。
配套 receipt：`examples/routeb_b45_source_comparator_lean/O1_BODY_4_SOURCE_GRAM_TARGETS_RECEIPT.json`。
本轮只新增该 Lean 文件、检查脚本、本 review 和 receipt。工作区期间出现其他
任务的文件变动；本轮没有编辑、回退或吸收它们，最终边界以这四个新增文件为准。
