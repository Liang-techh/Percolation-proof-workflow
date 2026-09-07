# Body-6 front 5×5: minimal source velocity / Gram leaves

本轮只推进可复用的小叶：真实 parent origin/axis 与活跃索引、COM offset 的速度列分解、Gram 对称性，以及左上 `5×5` 内零基索引 `{3,4}` 的 `2×2` 小块。**没有完成整个左上块的显式/Fourier 展开，没有运行 Lean/Lake；全部 Lean 文件仍为 UNCOMPILED proof attempts。**

## 新文件与依赖

| 文件 | 全部直接 Lean imports / 用途 |
| --- | --- |
| `NEW_BODY6_SLICE_VGRAM_Core20260907.lean` | `NEW_BODY6_SLICE_AXIS_Core20260907`；纯 cross 分解、Lagrange identity、Gram 对称性 |
| `NEW_BODY6_SLICE_VGRAM_Source20260907.lean` | 新 Core、`NEW_BODY6_SLICE_AXIS_Geometry20260907`、`RouteBO1PerBodyExactSource`；真实速度列、两个 origin 叶、全部活跃 guard、source mass→Gram 结构等式 |
| `NEW_BODY6_SLICE_VGRAM_Tail20260907.lean` | 新 Source；只处理 index 3、4 的两个非零速度列、三个独立 Gram 项和转置 |
| `NEW_BODY6_SLICE_VGRAM_Consumer20260907.lean` | 新 Tail、旧 `NEW_BODY6_SLICE_STEP6_Bridge20260907`；将先前真实 endpoint/center 候选接入 `CenterOffsetTarget` |
| `NEW_BODY6_SLICE_VGRAM_check20260907.py` | 只读 symbolic DH 检查；复用旧 axis checker 的源码文本解析 helper，但不执行其 `main()` |
| 本 review | 范围、契约、检查、开放叶与建议 child |

Core 的传递数学依赖只到此前纯旋转 Core 和 Mathlib。Source/Tail 没有导入 body Fourier literal/evaluator；Consumer 才为既有 center proof attempt 引入旧 STEP6 bridge 的传递依赖。该旧 bridge 会导入此前数据定义，但本轮没有展开/检查其 610 行，也没有让数据参与 source 几何推导。

本轮所有写入都限于指定目录下这六个新文件。未修改 state、registry、shared scripts、之前的 body-6 文件或其他任务文件。没有执行 comparator、git add 或 git commit。

## Parent origin、axis 与 active/inactive 契约

- human body 6 固定为 `5 : Fin 6`。
- 左上块使用 `i,j : Fin 5`，通过 `frontJoint : Fin 5 → Fin 6` 显式保留 `.val`；其范围是零基 `0..4`。
- 每个 `i : Fin 6` 的 lever arm 使用 `origins (prevOrigin i)`，`prevOrigin i : Fin 7` 的值为 `i.val`，不是 `i+1`。
- 轴使用 `(sourceContract q).axes i`，它是此前 source-axis seam 确定的 parent frame 第三列。
- 对第六刚体，所有六个 joints 都满足 `i.val ≤ 5`。`all_six_active_attempt` 与 `no_inactive_body6_joint_attempt` 明确排除了 inactive 分支；列为零只能来自几何，不能来自错误的活跃性判断。
- `sourceV q i` 直接定义为真实 `bodyJv ... body=5` 的第 `i` 列，没有用候选 Fourier 表重定义速度。

## 一条通用 COM-offset 分解

以下记号均为零基。令 `h=7/200`、`p=o₅`，既有 endpoint/center 目标给出

\[
c_6=o_5+h z_5.
\]

于是对全部六个活跃关节，

\[
v_i=z_i\times(c_6-o_i)
   =\underbrace{z_i\times(o_5-o_i)}_{b_i}
      +h(z_i\times z_5).
\]

`displaced_velocity_split_attempt` 是任意实向量/实数上的纯代数叶。`source_velocity_decomposition_attempt` 使用真实 `bodyJv_active_formula` 和显式 `CenterOffsetTarget` 接线。

这条式子保留前 3 列真实的 `b₀,b₁,b₂`；它们没有被设为零。本轮只给出 `FirstThreeLeverTarget` 作为下一步具体局部公式的接口，尚未提供 witness。把这个接口的参数直接设成 `baseV` 自身会成为没有推进的定义重述，不能当作完成了局部 source 展开。

## 两个最小 origin 叶

从真实 DH step 的第四列，只展开一次任意 prefix `F` 的矩阵乘法：

\[
o_4=o_3+\frac{19}{100}z_3,\qquad o_5=o_4.
\]

`origin_step3_attempt` 使用 zero-based step 3 的 `a=0,d=19/100`；`origin_step4_attempt` 使用 step 4 的 `a=d=0`。`terminal_origin3_attempt`、`terminal_origin4_attempt` 通过 source origin slot 与 source parent axis 定义接线。没有展开前五步全位置表。

这只消去 `b₃,b₄`，得到

\[
v_3=h(z_3\times z_5),\qquad v_4=h(z_4\times z_5).
\]

这两列一般不为零。第六列 `v₅=0` 没有被用来推出它们为零。

## Gram 的通用叶与 source 接线

Core 的一般 Lagrange identity 保留不同 lever arms：

\[
(u\times p)\cdot(v\times r)
=(u\cdot v)(p\cdot r)-(u\cdot r)(p\cdot v).
\]

共同轴情形是

\[
[h(u\times w)]\cdot[h(v\times w)]
=h^2\big[(u\cdot v)(w\cdot w)-(u\cdot w)(v\cdot w)\big].
\]

`front_linear_symmetric_attempt` 对所有 `i,j : Fin 5` 给出速度 Gram 对称性。真实 `source_mass_gram_attempt` 与 `front_source_gram_attempt` 只展开实际质量/惯量定义，得到

\[
M^6_{ij}=\frac3{20}\,v_i\cdot v_j+\frac1{60}\,z_i\cdot z_j.
\]

惯量已是 `I_val/3=1/60`，不额外乘质量，不再除三，也不含 `mu I`。这个 all-entry source→Gram 结构等式不是 all-entry Gram→Fourier 证明。`source_mass_symmetric_attempt` 也只给出结构对称性。

## 左上块中可先封装的 2×2 小块

新 Tail 使用既有六轴 seam，加上 `z₃·z₃=z₄·z₄=1` 与 `z₃·z₄=0` 的纯旋转证明候选。记 `t=q 4`，即 human 第五关节角，则

\[
\|v_3\|^2=h^2\sin^2t,\qquad
\|v_4\|^2=h^2=\frac{49}{40000},\qquad
v_3\cdot v_4=0.
\]

`velocity4_nonzero_attempt` 还明确给出 `sourceV q 4 ≠ 0` 的候选，防止将末列消项外推。`v₃·v₄=0` 来自 Lagrange identity 和轴正交性，不是因为其中某一速度列被假设为零。

因此，以 **零基 `(i,j)=(3,3),(4,4),(3,4),(4,3)`** 表示的 source mass 小块候选为

\[
\begin{bmatrix}
\frac1{60}+\frac{147}{800000}\sin^2t & 0\\
0 & \frac{40441}{2400000}
\end{bmatrix}.
\]

这是 CSV 一基 row/col `{4,5}` 的位置，但推导没有读取 CSV。交叉 mass 为零同时需要 linear Gram 零和 angular Gram 零；本轮分别保留了这两个证明叶。

Consumer 的 `front_tail_block_attempt` 将这四个 entry candidate 合并；仅消费已有 center 候选，没有使用第六列 Fourier theorem 来推导这些值。

## 已执行的定向检查

```text
python -B examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_VGRAM_check20260907.py
```

检查器从固定 source 文件读取相位、`a/d`、`alpha`，按真实右乘和 pre-step parent-axis 约定构造 DH origins/axes，再取 `c₆=(o₅+o₆)/2`。以 exact rational polynomial 运算核对：

- center offset、两个尾部 origin 关系；
- 全六列共 18 个 COM-offset 速度分解坐标残差；
- `v₃,v₄` 的 cross 形式，以及第六列的独立几何零；
- `V₃₃,V₄₄,V₃₄`、angular `W₃₄` 和 source `M₃₃,M₄₄,M₃₄` 的七个小叶。

结果均通过。后七个余项对精确单位圆关系 `s_k²+c_k²=1` 化简后均为零；检查给出 `V₄₄=49/40000>0`。没有数值容差、采样、拟合或 610-row/Fourier 对比。静态检查保留 Fin 5→Fin 6/prevOrigin/active guard；新 Lean 文件没有 `sorry/admit/axiom/opaque` 声明。

该检查不验证 Lean tactics、import closure 或 kernel。源码级结果与数学表达式检查不等同于本机 Lean 验证。

```text
Core SHA-256:     cab1f65f759215abe1f79c33226e9f3c14fd610a84dac69b1e2a054a5731c9b3
Source SHA-256:   8df1f68077d7651238295791d7ac56208e6d9a122ca3f3e9719d76af37b229f6
Tail SHA-256:     1d54d6721c36c9689bf81ec08ba0914eb7b4eb7e0a58c83647f20e9800fb8c6f
Consumer SHA-256: 72c1b3f28529c966560a894b5f0c99cf0fa8cf6602a721f69047ae2fde2f7b53
```

## 未闭合前提与下一小叶

| 层 | 仍然开放 |
| --- | --- |
| 真实 source | 既有 endpoint/center/axis/prefix 及本轮全部 Lean tactic 尚未核验；Tail 在独立文件中继续显式要求 `CenterOffsetTarget` |
| 左上 `5×5` | 前 3 列具体 `baseV` 的低复杂局部表达式及其真实 origin 绑定；剩余 12 个上三角 entry 尚未展开 |
| Fourier/CSV | 没有新增 Gram→Fourier、literal/fold 或旧 evaluator 接线证明；没有重做 610 行核对 |
| Coverage | 本轮两个对角和一对转置零项不供应全 25/36-entry coverage；四项全域零补集的整体接口仍未填满 |
| Lean | 未运行 Lean/Lake；仍缺 pinned toolchain/Mathlib/import closure、编译与 axiom receipts |
| Registry | 不运行 comparator、不写 state/registry；没有正式准入证据 |

建议仅作为后续 DAG child 拆分，不实际登记：

1. `body6_velocity_offset_and_tail_origins`：本轮通用列分解与两个真实 origin 叶。
2. `body6_front_tail_gram`：本轮 `{3,4}` 小块，保留 center/axis 依赖与未编译状态。
3. `body6_first_three_levers`：下一独立数学叶，明确 `zᵢ×(o₅−oᵢ)` 在共同旋转坐标下的三个具体向量，再通过通用 offset 分解得到 `v₀,v₁,v₂`。
4. `body6_front_remaining_gram`：仅在上一个叶得到真实 source 接线后，推导其余 12 个上三角项；Gram/Fourier 与 coverage 继续分开。

当前状态保持 `lean_lake_run=false`、`source_gram_proven=false`、`full_source_binding_proven=false`、`source_coverage_proven=false`、`registry_eligible=false`、`registry_status=pending`、`formal_certificate_allowed=false`。
