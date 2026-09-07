# Body-6 tail `{3,4}` 质量／惯量加权 self Gram

状态：**UNCOMPILED PROOF ATTEMPT**。未执行 Lean/Lake，未获得内核验证或准入凭据。

本叶在已有真实 body-6 tail 速度与 axis Gram 接口之上，显式引入质量 `m` 和已除惯量 `kappa`，给出三项独立表达式及完整 `2×2` 表。旧 tail 文件已有固定常数的质量项尝试；本叶增加的是独立参数化、`h²` 修正表以及保留权重绑定前提的 source seam，不重新推导 DH 几何。

## 文件与直接依赖

| 新文件 | 直接依赖与用途 |
| --- | --- |
| `NEW_BODY6_SLICE_MASSTAIL_Core20260907.lean` | `NEW_BODY6_SLICE_VGRAM_Core20260907`；标量修正、加权表、对称性和固定常数特化 |
| `NEW_BODY6_SLICE_MASSTAIL_Source20260907.lean` | 新 Core、`NEW_BODY6_SLICE_VGRAM_Tail20260907`；复用真实 tail Gram，连接实际 `sourceBodyMass` |
| 本 REVIEW | 三项表、前提、检查证据与开放边界 |

没有直接导入 first-three self3 或 mixed `3×2` 模块，没有重做这些块或拼接完整矩阵。没有修改旧文件、共享脚本、state 或 registry。

## 定义域与真实列顺序

- source 配置是任意 `q : Fin 6 → ℝ`，无数值样本、角度网格或区间限制。
- body 是 `(5 : Fin 6)`，即从 1 开始编号的第 6 刚体。
- `tailJoint : Fin 2 → Fin 6` 按顺序将 `0,1` 映射到 `3,4`，不是 `4,5`。
- 以下 `z = q 4` 使用 Lean 的从 0 开始编号，故是通常编号的第五个关节角。
- 两列均为实际活动列；非对角 Gram 为零不表示速度列为零。

## 保留 h² 修正的三项独立表

继承的 tail axis Gram 为 `A = I₂`，两列对终端单位轴的内积向量为
`p = (cos z, 0)`。Core 明确写出

\[
G_v=h^2(A-pp^T)
=\begin{pmatrix}h^2\sin^2z&0\\0&h^2\end{pmatrix},
\qquad
M_{\rm tail}=mG_v+\kappa A.
\]

| 实际关节索引 | 速度 Gram | axis Gram | 加权项 |
| --- | --- | --- | --- |
| `(3,3)` | `h² sin² z` | `1` | `kappa + m h² sin² z` |
| `(3,4)` | `0` | `0` | `0` |
| `(4,4)` | `h²` | `1` | `kappa + m h²` |

`(4,3)` 由对称性等于 `(3,4)`；Core 也显式存放两个零，Source 对全部四项连接实际 Gram。

`velocity_correction_table_attempt` 尝试通过 `sin² z + cos² z = 1` 化简修正表；
`weighted_table_attempt` 尝试证明逐项加权；
`corrected_weighted_table_attempt` 将未化简的修正直接连接到加权显式表。
因此 `h²` 项没有被忽略，也没有把 `(3,3)` 错当成常数 `kappa + m h²`。

Core 的 `h,m,kappa` 是任意实数；这些恒等式不需要正性前提，也不产生正定性结论。

实际标量特化是

\[
h=\frac7{200},\quad m=\frac3{20},\quad\kappa=\frac1{60},\quad
mh^2=\frac{147}{800000},
\]
\[
M_{\rm tail}=
\begin{pmatrix}
\frac1{60}+\frac{147}{800000}\sin^2(q\,4)&0\\
0&\frac{40441}{2400000}
\end{pmatrix}.
\]

`kappa` 对应实际 `routeBInertiaScalar 5`，已经包含惯量除以 3 的约定；不再除以 3，不再乘质量，也不加入全矩阵正则项。

## Source seam 与前提

`SourceWeightsTarget m kappa` 要求实际 `routeBMass 5 = m` 和
`routeBInertiaScalar 5 = kappa`。它在本叶独立命名空间中定义，避免为了共用小前提而导入 mixed 块；没有构造无条件权重见证。

`TailAxisTarget` 与 `TailVelocityTarget` 均量化所有 `q` 及 `i,j : Fin 2`。
对应 source 证明尝试消费旧 tail 的 `source_axis33_attempt`、`source_axis34_attempt`、
`source_axis44_attempt`、`velocity_gram33_attempt`、`velocity_gram34_zero_attempt` 与
`velocity_gram44_attempt`；反向非对角项仅用 dot 对称性。

`tail_mass_from_gram_attempt` 的底层前提是权重绑定、速度 Gram 和 axis Gram 的证明项，使用已有 `source_mass_gram_attempt` 连接实际 `sourceBodyMass`。
底层函数不额外要求中心偏移，因为已将速度 Gram 本身作为前提。

`source_weighted_tail_attempt` 明确要求 `hc : CenterOffsetTarget` 和 `hw : SourceWeightsTarget m kappa`，并通过旧 tail 速度接口消费 `hc`。
即使固定为实际常数，`source_routeB_tail_table_attempt` 仍保留这两个前提。
Python 检查或 CSV 数据不能代替任一 Lean 证明前提。

## 本次检查及证据限制

按请求先执行一次内联 Python/SymPy 精确符号核对，再新增 Lean 文件：

1. `h²(I₂ − ppᵀ)` 与对角速度表的四项差经三角恒等式化简均为精确零。
2. `m * velocityTable + kappa * I₂` 与新加权表的四项展开差均为精确零。
3. 精确有理数核对 `mh² = 147/800000`、`kappa + mh² = 40441/2400000`。

这是独立转写的有限代数检查；没有运行旧检查脚本，没有重建实际 source/DH，没有重做 self3、mixed 或 Fourier 数据检查。它不解析或编译 Lean，也不验证继承几何接口。

新两份 Lean 文件的直接 import 对应文件均存在；静态搜索未见 `sorry`、`admit`、`axiom` 或 `opaque`。这不构成编译通过、依赖闭包公理审计或内核验证证据。

| Lean 文件 | 实际字节 SHA-256 |
| --- | --- |
| `NEW_BODY6_SLICE_MASSTAIL_Core20260907.lean` | `06e1be44dc8efe984e168aafeb9c44dd8f386e4d25df20643b2ee08101bf62ac` |
| `NEW_BODY6_SLICE_MASSTAIL_Source20260907.lean` | `d432db353c67f8fe43ecdca2c3dd0b3fa07e50eba25160447550220171d5de3b` |

## 开放边界

- 本叶和所调用的 proof attempts 未在本次执行中编译；不声明 `LEAN_VERIFIED`。
- 上层实际 source 接口继续保留中心偏移及实际权重绑定前提。
- 仅覆盖 body-6 的有序 `{3,4}` tail `2×2`，不声称完整 `5×5`／`6×6` 矩阵。
- Fourier、coverage、comparator、registry 均维持 fail-closed；未构造准入凭据或变更状态。
