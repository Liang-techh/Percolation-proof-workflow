# Body-6 first-three × tail mixed velocity/axis Gram

本轮仅新增一个 `3×2` 混合块：前三列 source indices `0,1,2`，尾部列 source indices `3,4`。输出两份 Lean 候选和本 review。**全部 UNCOMPILED / NOT_RUN；没有本机 Lean/Lake 验证，没有展开完整 `5×5/6×6` 或 610 行 Fourier，也没有 coverage/registry 准入。**

## 文件和依赖

| 文件 | 直接 imports / 职责 |
| --- | --- |
| `NEW_BODY6_SLICE_MIXED_Core20260907.lean` | `NEW_BODY6_SLICE_LEVER_Core20260907`；source-independent 六项 axis/triple/velocity 表、有限和与 cross 传递 |
| `NEW_BODY6_SLICE_MIXED_Source20260907.lean` | 新 Core、`NEW_BODY6_SLICE_LEVER_Source20260907`；复用真实前三列和尾部列，接到带 center 前提的混合 source 接口 |
| 本 review | 精确公式、证明范围、检查和未闭合边界 |

Source 经已有 LEVER Source 访问 VGRAM Source 和 AXIS Geometry；它只消费原来的 `source_velocity3_attempt`、`source_velocity4_attempt` 与 `source_first_velocity_local_attempt`，没有重新证明 tail 范数、origin 或 DH prefix。Core 的传递依赖只到已有纯旋转/cross/lever 代数及 Mathlib，不导入 source evaluator 或 CSV。

本轮只写上述三个新文件。旧 lever/tail/center 文件、state、registry、shared scripts 和其他任务文件均未修改；没有执行 comparator 或 git add/commit。

## 索引与方向

- `i : Fin 3` 经已有 `firstJoint` 映射到零基 source joint `0..2`。
- `t : Fin 2` 经新 `tailJoint t := ⟨t.val+3,...⟩` 映射到零基 source joint `3,4`。
- `a : Fin 3` 是笛卡尔分量，source body 固定为 `5 : Fin 6`。
- 正向 Gram 顺序是 first-three × tail；反向仅用 dot 对称性得到，不能把 `Fin 2` 值 `0/1` 直接当作 source 列号。
- 目标对所有 `q : Fin 6 → ℝ` 成立的候选，没有改为 `q=0`、cell 内或数值采样陈述。

## 一个通用混合 identity

记 `x=angleSum q=q 1+q 2`、`y=q 3`、`z=q 4`，所有角索引为 Lean 零基。令

\[
B_i=baseLocal(q,i),\quad W_i=firstAxis(i),\quad
T_t=localAxis(q,3+t),\quad S=localAxis(q,5).
\]

与此前保持相同的 source 列分解：

\[
L_i=B_i+h(W_i\times S),\qquad U_t=h(T_t\times S),\qquad h=7/200.
\]

Core 中 h 是任意实数，Source 才实例化为已有 `offset=7/200`。由 `S·S=1` 和一般 Lagrange identity，

\[
L_i\cdot U_t
=h\,B_i\cdot(T_t\times S)
 +h^2\big[W_i\cdot T_t-(W_i\cdot S)(T_t\cdot S)\big].
\]

`mixed_cross_identity_attempt` 是这个任意向量版本，显式要求 `S·S=1`。具体 Core 的 `last_unit_attempt` 消费此前局部 axis 5 的单位范数候选。没有删除 `h²` 修正，也没有将前三个 lever 或尾部速度设为零。

## 两张明确的 3×2 有限表

记 `c=cos x,s=sin x`，并沿用已有 LEVER Core 的 `A=radial q,P=height q,Q=reach q`。再定义

\[
\kappa=Pc+Qs,\qquad\lambda=Qc-Ps.
\]

轴点积表 `axisEntry`：

\[
\mathcal A_{it}=W_i\cdot T_t=
\begin{bmatrix}
c&s\sin y\\
0&\cos y\\
0&\cos y
\end{bmatrix}.
\]

三重积表 `tripleEntry`：

\[
\mathcal T_{it}=B_i\cdot(T_t\times S)=
\begin{bmatrix}
\sin z(A\cos y+c\sin y/20)&
\cos z(A\sin y-c\cos y/20)+s\sin z/20\\
-\kappa\sin y\sin z&\kappa\cos y\cos z+\lambda\sin z\\
-(19/100)\sin y\sin z&(19/100)\cos y\cos z
\end{bmatrix}.
\]

另外两个明确向量是

\[
f_i=W_i\cdot S=
\begin{bmatrix}c\cos z-s\cos y\sin z\\\sin y\sin z\\\sin y\sin z\end{bmatrix},
\qquad
g_t=T_t\cdot S=\begin{bmatrix}\cos z\\0\end{bmatrix}.
\]

最终 `velocityEntry q h i t` 精确为 `h*T_it+h²*(A_it−f_i*g_t)`。它是六个混合速度 Gram 的有限表达，没有引入任何 Fourier row 或系数标签。

Core 的证明拆分为：一般 mixed cross identity；有限 axis 表；front/tail 与 S 的点积；保持方向的 pitch cross covariance；两个 tail cross 局部向量；六项 triple 表；最后组合。有限 case 数分别是 `3×2`，没有展开其他 matrix entries。

## 真实 source seam 与 center 前提

新 Source 只做下列接线：

```text
已有 source_first_velocity_local_attempt (hc)
已有 source_velocity3/4_attempt (hc) + source_axis_local_attempt
  → 前三列和尾部列统一 yaw 表达
  → yaw_isometry_attempt
  → Core 的六项混合 velocity 表
```

`source_tail_velocity_local_attempt` 通过 `fin_cases t` 分别消费已存在的 v₃/v₄ 形式，仅补 yaw cross/缩放的传递。没有重算它们的 origin、范数或 tail mass 块。

接口分为：

```lean
source_mixed_axis_attempt : MixedAxisTarget

source_mixed_velocity_attempt
  (hc : CenterOffsetTarget) : MixedVelocityTarget

source_mixed_gram_interface_attempt
  (hc : CenterOffsetTarget) : MixedAxisTarget ∧ MixedVelocityTarget
```

轴点积自身不需要 center。所有 source 速度混合结果（包括可选的反向 dot）都显式保留 `CenterOffsetTarget`；本轮没有从旧 center 候选自动供应或隐藏这个参数。`MixedVelocityTarget` 的左端是已有真实 `sourceV`，不是用局部公式重新定义的 source。

## 定向 exact 检查

本轮通过只读内存 Python/SymPy 检查六个局部位置，未新增 checker 文件，也没有执行旧 tail/lever/Fourier checker。检查令 `A,P,Q,h` 为自由实多项式变量，以三个正弦/余弦对表示 x/y/z，并以精确有理系数的单位圆关系化简。

对每个 `(i,t)∈Fin 3×Fin 2`，分别核对：

1. `W_i·T_t - A_it`；
2. `B_i·(T_t×S) - T_it`；
3. `(B_i+h(W_i×S))·(h(T_t×S)) - [h*T_it+h²*(A_it−f_i*g_t)]`。

总共 18 个 polynomial remainder 均为零，h 未固定，因而同时涵盖 h=7/200 的实例。该检查没有读取 CSV、没有 source-DH 重放、没有数值采样或容差；仅核对独立书写的本轮有限数学公式，不验证 Lean tactics 或 import closure。

静态检查两份新 Lean 无 `sorry/admit/axiom/opaque` 声明。文件身份：

```text
Core SHA-256:   59e55b9a6774234b7a3e65df1531637047992c7ad1a2d9ad34b8aafb5adf5495
Source SHA-256: 811fe5d5ae4edaf5519e8c415a81ea7513fe6f55a861a8be0c89f2c43a1d50e8
```

## 尚未闭合的范围

- 本轮及所有既有 source/yaw/lever/tail 候选都尚无本机 Lean 编译、kernel 或 axiom receipt；接口有完整候选代码不等于 source proof 已获验证。
- `CenterOffsetTarget` 在所有 source velocity 接口中保持显式。
- 只处理六个正向 velocity 和六个 axis entries，以及可选的 dot 转置；没有重新处理前 3 列自身的 `3×3` Gram，也没有处理 tail 自身的 `2×2` Gram。
- 没有添加质量/惯量加权后的 mixed mass theorem，没有 Gram→Fourier/CSV/legacy trace 接线，更没有完整 `5×5/6×6` coverage 或 registry witness。
- 下一独立小叶可选 `body6_first_three_self_gram`，或在保留相同前提下组合这六项的质量/惯量权重；这些只是后续建议，不创建 DAG child、不写 state。

最终状态：**Core/Source/REVIEW 三个新文件完成；六项有限代数检查通过；未编译、未准入。** 保持 `lean_lake_run=false`、`source_mixed_gram_proven=false`、`coverage_proven=false`、`registry_eligible=false`、`registry_status=pending`、`formal_certificate_allowed=false`。
