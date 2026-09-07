# Body-6 前三列 × tail：质量／惯量加权 mixed block

状态：**UNCOMPILED PROOF ATTEMPT**。未运行 Lean/Lake，未取得内核验证或准入凭据。

本叶只把已有 mixed `3×2` 的速度 Gram 与 axis Gram 按权重相加，给出六项显式表及实际 `sourceBodyMass` 的条件式接口。已有 self3 与 tail `2×2` 自块不重算、不拼接；本叶直接需要的是 mixed 接口中已经接好的前三列和 tail 列。

## 新文件与直接依赖

| 文件 | 直接 import / 用途 |
| --- | --- |
| `NEW_BODY6_SLICE_MASSMIX_Core20260907.lean` | `NEW_BODY6_SLICE_MIXED_Core20260907`；六项代数加权与固定标量特化 |
| `NEW_BODY6_SLICE_MASSMIX_Source20260907.lean` | 新 Core、`NEW_BODY6_SLICE_MIXED_Source20260907`；实际 source 的条件式加权接口 |
| 本 REVIEW | 公式、前提、范围与检查证据 |

没有添加 CSV、共享脚本或 registry/state 修改。

## 定义域与索引

- 配置为任意 `q : Fin 6 → ℝ`；没有采样、网格或局部角度区间前提。
- body 为 `(5 : Fin 6)`，即通常从 1 开始编号的第 6 个刚体。
- 行为 `i : Fin 3`，经 `firstJoint` 映射至关节索引 `0,1,2`。
- 列为 `t : Fin 2`，经 `tailJoint` 映射至关节索引 `3,4`。
- 本表不包含关节索引 5；不产生完整 `5×5` 或 `6×6` 矩阵结论。

## 六项显式表

以下 `q` 下标采用 Lean 的从 0 开始编号。记

\[
\phi=q_1+q_2,\quad C=\cos\phi,\ S=\sin\phi,\quad
c_y=\cos q_3,\ s_y=\sin q_3,\ c_z=\cos q_4,\ s_z=\sin q_4,
\]
\[
A=\operatorname{radial}(q),\quad K=\operatorname{projAlong}(q),\quad
E=\operatorname{projAcross}(q),\quad d=19/100,
\quad D=Cc_z-Sc_y s_z,\quad \lambda=mh^2+\kappa.
\]

其中继承的标量定义为
\[
Q=\tfrac{21}{100}\sin q_1+\tfrac{19}{100}S,\quad
P=\tfrac{21}{100}\cos q_1+\tfrac{19}{100}C,\quad
A=\tfrac{2}{25}+Q,\quad K=PC+QS,\quad E=QC-PS.
\]

新 Core 的 `explicitMixed` 为

\[
\begin{pmatrix}
mh s_z(Ac_y+Cs_y/20)+\lambda C-mh^2Dc_z &
mh\{c_z(As_y-Cc_y/20)+Ss_z/20\}+\lambda Ss_y\\
-mh s_y s_z(K+hc_z) & mh(Kc_yc_z+Es_z)+\lambda c_y\\
-mh s_y s_z(d+hc_z) & (mhdc_z+\lambda)c_y
\end{pmatrix}.
\]

`weighted_table_attempt` 尝试证明此表逐项等于
`m * velocityEntry q h i t + kappa * axisEntry q i t`。
它保留速度项中的 `h²` 修正。axis 表中为零的项并不使对应质量项自动为零。

Core 对任意实数 `h,m,kappa` 写出恒等式，不额外假定正性，也不凭这些参数声明实际 source 常数。
固定标量特化 `routeBMixedTable` 使用

\[
h=7/200,\qquad m=3/20,\qquad\kappa=1/60,
\]
\[
mh=21/4000,\qquad mh^2=147/800000,\qquad
\lambda=40441/2400000.
\]

`kappa` 对应已除以 3 的 `routeBInertiaScalar`，不再乘质量，也不加入总矩阵的正则项。

## Source seam 与显式前提

`SourceWeightsTarget m kappa` 明确要求实际 body-6 的
`routeBMass 5 = m` 与 `routeBInertiaScalar 5 = kappa`。
新代码没有构造或发布一个无条件的该 target 见证。

`MixedMassTarget m kappa` 的左侧是实际
`sourceBodyMass q 5 (firstJoint i) (tailJoint t)`，右侧是新表在 `offset` 下的值。

1. `source_weight_values_attempt` 从权重绑定前提提取 `3/20 = m` 与 `1/60 = kappa`。
2. `mixed_mass_from_gram_attempt` 消费 `SourceWeightsTarget`、`MixedVelocityTarget` 和 `MixedAxisTarget` 三个证明前提，并使用已有 `source_mass_gram_attempt`。这个底层接口以速度 Gram 证明为前提，不另列 `CenterOffsetTarget`。
3. `source_weighted_mixed_attempt` 明确保留 `hc : CenterOffsetTarget` 和 `hw : SourceWeightsTarget m kappa`，通过已有 mixed source 定理尝试取得 Gram 证明。
4. `source_routeB_mixed_table_attempt` 即使固定为 `3/20` 与 `1/60`，仍明确要求 `CenterOffsetTarget` 与固定权重的 `SourceWeightsTarget`。

这些是 Lean 证明项接口；Python 结果、CSV 系数或数值样本不能代替上述前提。
继承的几何证明和新 tactic 脚本都尚未在本叶获得编译验证。

## 本次有限检查

运行一次内联 Python/SymPy 精确代数检查：独立转写已有
`velocityEntry = h * tripleEntry + h² * (axisEntry - frontLastDot * tailLastDot)`，
再与新表六项逐项比较。把三角函数值作为自由符号，六个展开差均为精确零；未使用单位圆恒等式或随机样本。
另以精确有理数核对上列 `mh`、`mh²` 和 `lambda`。

此检查只支持独立转写公式的代数一致性，不解析或编译 Lean，不验证实际 DH/source 几何，也不证明任何 Fourier 系数覆盖。
新两份 Lean 文件静态搜索未见 `sorry`、`admit`、`axiom` 或 `opaque`；这不等价于编译通过或依赖闭包的公理审计。
没有执行旧 610 行 Fourier 检查、source 重建或重复 self3/tail 检查。

SHA-256（两份 Lean 文件的实际字节）：

| 文件 | SHA-256 |
| --- | --- |
| `NEW_BODY6_SLICE_MASSMIX_Core20260907.lean` | `4687a9a47fb24f8f14a13288ce90cc1396db3f04b54e02f4f6e34caf2850ad7d` |
| `NEW_BODY6_SLICE_MASSMIX_Source20260907.lean` | `1e4ce5f456278b753655f59066595f4e6ad1045a5687af7bf0072dc23d9659ba` |

## 保持开放的边界

- `LEAN_VERIFIED`：未取得；没有运行 Lean/Lake。
- `CenterOffsetTarget`、source 权重绑定：继续作为上层显式前提。
- 完整 self/mixed/tail 矩阵组装、完整 source 证明：本叶未完成或声称。
- Fourier、coverage、comparator、registry：全部保持原有 fail-closed 边界；无准入状态修改。
