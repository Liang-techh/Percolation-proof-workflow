# O1 human body-5 source / piecewise / trace-fold minimal decomposition

日期：2026-09-07。状态：`OPEN_UNPROVEN_BODY5_SOURCE_TRACE_DECOMPOSITION`。
仅处理 human body 5 / zero-based body `4`。新增独立 targets、receipt、review；
主 adapter、body-3/4、generated evaluator、CSV、state/registry 均不由本轮修改。
没有运行 Lean/Lake、安装工具链、发起远程编译或产生本地编译声明。

## 先固定两个旧证据问题

1. 既有 geometry review 第 4 节以及 `O1_BODY_5_SOURCE_BRIDGE_RECEIPT.json`
   的 `entry_2_3` 字段误写了 `(2,3)/(3,2)=cos(q3)/30`。正确值为 **0**。
   既有 `body_5_piecewise`、57-row CSV、target checker 公式和 geometry review
   第 3 节的 Gw 一致：`et · z3=0`，且 `v3=0`。本轮只在 sidecar 勘误。
   若真增加这两个有 cos(q3) 的 entry，会额外增加 4 行，得到 61 行而非 57 行。
2. 旧 review 中 adapter hash `25F099...` 已不是当前文件 hash；当前为
   `6B50AE63...399EF`。旧 source bridge receipt 的 adapter hash 与当前一致。
   本 receipt 逐项绑定本次读取的文件；旧 review 的无 support mismatch 结论
   只能用于已有 piecewise/CSV，不能覆盖其错误的 prose entry。

另外，实际 `traceRowContribution` 参数顺序是 **body, row, col, q, record**。
本 sidecar 按当前定义调用，没有复用 body-4 sidecar 的调用方式。

## 最短可证明链与真实缺口

```text
既有 sourceContract → frame-slot accessors
  → G1: origins 0..5 + parent axes 0..4
  → G2: actual bodyJv/bodyJw = cylindrical-basis columns
  → G3: isotropic inertia + lift isometry → sourceBodyMass = body5Gram
  → G4: finite scalar trig algebra → existing body_5_piecewise

既有 bodyTraceRows.foldl
  → F2: arbitrary-seed body guards → bodyTraceRows5.foldl
  → F1 + F3: exact tagged-row permutation → 7 constants + 25 pairs
  → F4: phase / conjugate / entry guards → same body_5_piecewise

two conditional handoffs → existing h_body_5_of_entry_targets
```

这些箭头是证明工作清单，不是已验证依赖图。G1--G4、F1--F4 均未交付证明。
新 Lean 文件中的两个 `*_handoff_candidate` 只串联显式给定的等式前提，
也没有经过 elaboration。特别是声明 `P → Q` 为 Prop 不等于证明该蕴含。

### G1--G3：把 source 几何缩到所需列

令 `phi=q1+q2`，在 `(er,et,e3)` 正交基下写列向量。`body5Lift` 将局部
三坐标送回世界坐标，只依赖 q0；`Body5LiftIsometryTarget` 隔离掉 q0。

```text
A = 2/25 + (21/100)sin(q1) + (19/100)sin(phi)
P = (21/100)cos(q1) + (19/100)cos(phi)
Q = (21/100)sin(q1) + (19/100)sin(phi)

v0 = (-1/20, A, 0)       w0 = (0,0,1)
v1 = (P, 0, -Q)          w1 = (0,1,0)
v2 = (19/100)(cos(phi),0,-sin(phi))
                         w2 = (0,1,0)
v3 = 0                   w3 = (sin(phi),0,cos(phi))
v4 = 0                   w4 = (-sin(q3)cos(phi),cos(q3),sin(q3)sin(phi))
v5 = 0                   w5 = 0 [inactive, not source axis 5]
```

`Body5GeometryTarget` 直接约束真实 `(sourceContract q).origins/axes`。
可复用现有 `source_origin_function_eq_frame_contract` 和
`source_axis_function_eq_frame_contract`，再只算 origin 0..5、axis 0..4。
无需计算 slot-5 的完整 orientation、slot-6 或 source axis 5。

证明 `o5=o4` 用 **zero-based step 4** 的 `a4=d4=0`；证明 `v3=0` 则用
`c4-o3=(19/100)z3`。两者不是同一个原因。q3 是 step 3 的转角，并通过
**slot 4 的 parent axis** `z4` 进入 w4；q4 旋转不改变本体 COM，joint 5 inactive。

先用 `bodyCom_midpoint`、`bodyJv_active_formula`、`bodyJw_active_formula`
关闭 G2 的 active 列；joint 5 分别用现有 inactive lemmas。
G3 展开 `sourceBodyMass_eq_bodyMass`，代入 `m4=3/10`、对角惯量 `kappa4=1/30`，
消去惯量双重和，再用 lift isometry 得到 `body5Gram`。
这些现有 Lean 名称只是复用入口，本轮没有刷新它们的编译状态。

### G4：只留下有限个三角恒等式

全体 36 entry 归为既有 19 个非零 entry 与 17 个零 entry；不必逐项重复推导。
对称性在 source Gram 与 literal trace 两边各自有来源，不能用 source 对称性
代替 trace 的转置行覆盖。

- `G00=(3/10)(A²+1/400)+1/30`：展开平方，用
  `sin² x=(1-cos(2x))/2` 与 `2 sin x sin y=cos(x-y)-cos(x+y)`。
- `G11`、`G12`、`G22`：用 `P²+Q²`、`P cos(phi)+Q sin(phi)`，
  化为 q2 的 cos 和常数；分别得到既有 `8609/150000`、`13249/300000`。
- `G04` 与转置：仅角速度贡献 `sin(phi)sin(q3)/30`。
- `G14,G24` 与转置：仅角速度贡献 `cos(q3)/30`。
- `G23=G32=G34=G43=0`；所有含 inactive joint 5 的 entry 为 0。

建议先关 q3 product-to-sum 这个最小标量叶，再关 G4 的有限 entry，最后攻 G1。
G1 是仍需真正 source 绑定的主要数学/形式化缺口；G4 不应再次包含矩阵 prefix 展开。

## q3 conjugate pairs 的确切符号

以下频率只写 `(q1,q2,q3)`，完整频率为 `(0,u,v,w,0,0)`，每行保持自身
body/row/col 标签。所有 q3 行的 imaginary coefficient 都为 0。

| entry（zero-based） | 正代表及其整体取负 partner | 每个 atom 的 real coefficient | 合并后 |
|---|---|---|---|
| `(0,4),(4,0)` | `(1,1,-1)` 与 `(-1,-1,1)` | `+1/120` | `+cos(phi-q3)/60` |
| `(0,4),(4,0)` | `(1,1,1)` 与 `(-1,-1,-1)` | `-1/120` | `-cos(phi+q3)/60` |
| `(1,4),(4,1),(2,4),(4,2)` | `(0,0,1)` 与 `(0,0,-1)` | `+1/60` | `cos(q3)/30` |

这给出 8 个代表、8 对、16 行。`±(1,1,-1)` 表示整个向量一起取负，
不是对三个坐标独立选择正负。`Body5Q3ExactPairsTarget` 以原始 rational tags
和 `List.Perm` 固定这 8 个代表；`Body5Q3ProductToSumTarget` 与 G04 接合。
q3 三角项不来自 Jv[4]，也不出现在 `(2,3)/(3,2)`。

对于其余 17 对，统一使用已有 real atom 约定
`a cos(theta) - b sin(theta)`。共轭对和为 `2a cos(theta)-2b sin(theta)`；
G00 的正频率 imaginary coefficients 是 `-63/12500`、`-57/12500`，
所以合并后的 sine 项为正。零频 7 行只计算一次，不能作为自配对翻倍。

## F1--F4：有限 fold 的最小证明安排

F1 的 `Body5ExactPartitionTarget` 同时要求：57 行、7 常数、25 正代表；
原始 entry/frequency keys `Nodup`；body/frequency support、分母非零；
constant imaginary numerator 为 0；以及原始整行记录的 `List.Perm`。
`body5Conjugate` 仅定义候选 partner；必须通过这个 Perm 目标确认它确实是
generated list 中的原行（含分母标签），不能从“每行存在 partner”直接推到 fold。

F2 对任意 accumulator `seed` 消去 body-5 前后的四个/一个 block。
用 append 的 fold 恒等式和 off-body guard 即可，不展开其他 body 的 trig。
不能只证明“每个 off-block 从 0 开始 fold 为 0”，那没有交代实际 prefix accumulator。

F3 先证明通用加法恒等式
`foldl (acc + contribution) seed = seed + sum(map contribution)`，再对 F1 的
Perm 用有限和交换律，展开 `flatMap`，得到 `body5PairedValue`。
F4 消去 row/col guards，以 `Body5PhaseTarget` 和 `Body5ConjugateAtomTarget`
化简；q3 先单独走上表，其余 17 对、7 常数做 exact rational normalization。
也可直接枚举 body-5 的 57 行；无需全局 727 行的 trig 展开。

无需新增 Fourier 唯一性、正交积分、级数收敛或概率论前提。
当前 evaluator 定义本来就是 exact-real atom；如需要解释成复指数的实部，
已有 `realFourierAtom_complex_re_target` 是可复用入口，不必再建一条证明分支。

## 本轮验证及严格边界

仅运行一次有针对性的 Python/SymPy 1.14.0 精确 Laurent 代数诊断，无浮点采样：

- CSV 57 个唯一 key，原始 numerator/denominator 标签与 generated Lean 57 行逐行同序；
  7 常数 + 25 共轭对的多重集恢复，q3 的 8 对精确标签一致。
- 使用读取的 DH 参数和 phase offsets 重建前 5 步，核对 6 origins、5 parent axes、
  5 active Jv columns 与上述公式；joint 5 的 inactive 性按既有 guard 定义审阅。
- 直接解析当前 adapter 的 19 个 piecewise branches，检查全部 36 entry 的
  local Gram = piecewise = frozen CSV Laurent polynomial；`(2,3)/(3,2)=0`。

诊断用 `sin(theta)=(t-t^-1)/(2i)`、`cos(theta)=(t+t^-1)/2` 和独立形式变量，
不构成对 Lean 文件、真实执行器、Float64/libm 或 O1 source theorem 的验证。
DH 参数是按所读定义手工转录进诊断；Lean sidecar 未经解析器/elaborator 验证。
既有 `check_routeb_o1_body5_target.py` 把 Fraction 转为 Python complex；本轮没有重跑
或修改它。本轮的代数诊断保持 exact rational，但也不能升级既有 checker 的证明等级。

PATH 查询发现 `.elan/bin` 下的 lean.exe/lake.exe 入口，但没有执行；
可用工具链及 Mathlib 环境未核实。`lean_compiled=false`、`axioms_checked=false`，
所有 source/fold/q3 theorem targets 保持 `OPEN/UNPROVEN`，registry 保持不提升。

目标文件：`examples/routeb_b45_source_comparator_lean/RouteBO1Body5SourceTraceTargets.lean`。
证据记录位于 `examples/routeb_b45_source_comparator_lean/`，文件名前缀为
`O1_BODY_5_SOURCE_TRACE_DECOMPOSITION_RECEIPT_20260907_`，后接内容 SHA-256 的前 12 位。
本 review 同样采用日期与内容哈希文件名；receipt 固定本 review 的完整 SHA-256。
二者按 write-once 快照保存并设置 Windows 只读属性；后续补证另建快照。
只读属性并非 WORM 存储保证，内容哈希用于检测修改，不能证明其中数学结论。
未来只有在受控环境中实际补齐叶证明、编译并检查依赖/axioms、取得同 key receipt 后，
才能重新评估 `h_body_5`；本轮不提交或启动该编译流程。
