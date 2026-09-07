# Body-6 first three source lever columns

本轮只新增前三个真实 lever 列 `b_i=z_i×(o₅−o_i)` 的共同 yaw/local-vector 表达和 typed source 接线，并给出保留 COM-offset 的速度/Gram 接口。**没有将前三列设为零，没有重做 v₃/v₄ tail 或 610 行 Fourier。全部 Lean 文件仍为 UNCOMPILED / NOT_RUN。**

## 文件清单与直接依赖

| 新文件 | 职责及直接依赖 |
| --- | --- |
| `NEW_BODY6_SLICE_LEVER_Core20260907.lean` | 具体局部 origins/base vectors、yaw 的减法/线性/cross 传递、局部 cross 叶；只导入 source-independent `NEW_BODY6_SLICE_VGRAM_Core20260907` |
| `NEW_BODY6_SLICE_LEVER_Source20260907.lean` | 导入新 Core 与 `NEW_BODY6_SLICE_VGRAM_Source20260907`；真实 origin/axis 接线、具体 `FirstThreeLeverTarget`、保持 center 前提的完整前三列及 Gram 接口 |
| `NEW_BODY6_SLICE_LEVER_check20260907.py` | 只读 exact symbolic 检查；复用已有 axis checker 的 source 文本解析 helper 与输入哈希，不执行旧 checker 的 `main()` |
| 本 review | 公式、范围、复用边界、检查、剩余前提 |

Source 的关键传递依赖是之前的 source axis geometry、`RouteBO1PerBodyExactSource` 与真实 DH/frame slot 定义；不导入 VGRAM Tail/Consumer 或 STEP6 Fourier/data consumer。本轮没有直接/间接新增对 body CSV 的依赖。既有 DH 定义中的 `FourierNormalForm` 模块用于固定相位/常数，它不是 body mass 的 610 行数据表。

所有写入都限于指定目录下这四个新文件。未修改旧 tail/center/axis 文件、state、registry、shared scripts 或其他任务文件；未运行 comparator，也未执行 git add/commit。

## 精确索引和局部表示

以下 `q 0,...,q 5`、`b₀,b₁,b₂`、`z_i,o_i` 均用零基索引。令

\[
\phi=q_1+q_2,\quad
Q=\frac{21}{100}\sin q_1+\frac{19}{100}\sin\phi,\quad
P=\frac{21}{100}\cos q_1+\frac{19}{100}\cos\phi,\quad
A=\frac2{25}+Q.
\]

`phi` 对应 human 角 `q₂+q₃`。用已有 `Y= yawLift(q 0)` 表示共同绕世界竖轴的旋转，则

\[
\begin{aligned}
o_0&=Y(0,0,0),\\
o_1&=Y(2/25,0,1/10),\\
o_2&=Y(2/25+(21/100)\sin q_1,0,1/10+(21/100)\cos q_1),\\
o_3&=Y(2/25+(21/100)\sin q_1,1/20,1/10+(21/100)\cos q_1),\\
o_5&=Y(A,1/20,1/10+P).
\end{aligned}
\]

前三个 parent axes 是 `z₀=Y(0,0,1)`、`z₁=z₂=Y(0,1,0)`。它们来自此前真实 source-axis seam，不是从 Fourier 支持猜出的值。

`i : Fin 3` 通过 `firstJoint : Fin 3 → Fin 6` 保留 `.val`；其 parent origin 通过 `prevOrigin (firstJoint i) : Fin 7` 读取。`first_parent_slot_attempt` 显式连接这个 slot 与局部 parent slot，未进行 `i+1` 偏移，也未把 `Fin 3` 分量索引误当成 body index。

## 三个具体 lever 向量

定义 `B_i=baseLocal q i`，则

\[
\boxed{
B_0=(-1/20,A,0),\qquad
B_1=(P,0,-Q),\qquad
B_2=((19/100)\cos\phi,0,-(19/100)\sin\phi)
}
\]

真实 source 目标是

```lean
∀ q (i : Fin 3),
  baseV q (firstJoint i) = yawLift (q 0) (baseLocal q i)
```

此处 `baseV` 始终是之前定义的真实 `sourceZ q i × (terminalO q − parentO q i)`。新代码没有重定义 source，也没有将 `baseV` 自身当作“局部显式式”填入接口。

`first_three_lever_target_attempt` 将上述具体向量接回已有

```lean
FirstThreeLeverTarget (fun q i => yawLift (q 0) (baseLocal q i))
```

这个候选没有 `CenterOffsetTarget` 前提，因为 `b_i` 仅使用 `o₅−o_i`。前三列没有被设为零：`B₀` 有固定分量 `−1/20`，并有 source 候选 `‖b₀‖²=1/400+A²` 与 `b₀≠0`；局部 `‖B₂‖²=361/10000`。`B₁` 完整保留 P/Q，不添加零假设；本轮没有另外扩展其范数/下界证明。

## 最小 source 推导与已有叶的复用

`prefix_origin_local_attempt` 只展开 origins slots 0–3 的有界 DH prefix。随后 `source_origin_local_attempt` 使用已有 `source_origin_slot_attempt` 连接真实 source origins。

`source_end_local_attempt` **直接消费**上一轮的

```text
terminal_origin3_attempt: o5 = o3 + (19/100) z3
```

及已有 `source_axis_local_attempt` 的 axis 3，不重做 `o₅=o₄`、尾部 velocity3/velocity4 或 tail Gram。新 Core 的 `end_from_slot3_attempt` 只把这些已给定局部向量作线性组合。

之后 `source_first_base_local_attempt` 依次连接：

```text
真实 first parent origin + terminal origin + first parent axis
  → yaw 下的 lever 差向量
  → yaw_cross_attempt
  → local_lever_cross_attempt
  → 具体 B0/B1/B2 的 source seam
```

cross 的 yaw 传递显式使用了保持方向的旋转代数，不能只凭 dot isometry 推出 cross covariance。新 `yaw_cross_attempt` 用有限分量展开和 `sin²+cos²=1` 给出候选代码。

## 完整速度保留 offset，Gram 只给接口

令 `h=7/200`，`W_i=firstAxis i`，`W₅` 为已有轴局部表达，则

\[
v_i=b_i+h(z_i\times z_5)
   =Y\big[B_i+h(W_i\times W_5)\big],\quad i=0,1,2.
\]

`velocityLocal` 保留上式两个加项；`source_first_velocity_local_attempt` 继续显式要求已有 `CenterOffsetTarget`。它消费上一轮 `source_velocity_decomposition_attempt`，不重证 center，不把 b 当作完整 v，也不丢掉 offset cross 项。

`source_first_base_gram_attempt` 提供 `b_i·b_j=B_i·B_j`；`source_first_velocity_gram_attempt` 提供带 center 前提的 `v_i·v_j=velocityLocal_i·velocityLocal_j`，均对任意 `q` 和 `i,j : Fin 3` 成立的候选。这里没有展开剩余质量矩阵项，没有供应全部 `5×5`、`6×6` 或 Fourier coverage。

## Exact checker 的范围与结果

执行：

```text
python -B examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_LEVER_check20260907.py
```

检查器从已锁定的真实 DH source 文件解析相位偏移及 a/d/alpha，按右乘顺序只构造到 slot 5。只检查当前前三列，没有调用旧 tail checker 或读取 CSV。

结果通过：

- origins 0、1、2、5 的 12 个局部坐标残差为零多项式；前三个 parent axes 的局部式匹配。
- 三个 lever 的 9 个坐标残差在精确单位圆关系下为零。
- 消费 `c₆=o₅+h z₅` 后，三个 offset velocity 的 9 个坐标残差为零；这是对该 center 前提的使用，不是 center source 证明。
- `‖b₀‖²=1/400+A²` 与 `‖b₂‖²=361/10000` 的符号余项为零。
- 静态检查保留 `FirstThreeLeverTarget` 与 `CenterOffsetTarget` 边界；两份新 Lean 文件没有 `sorry/admit/axiom/opaque` 声明。

没有数值采样或容差，没有重做 v₃/v₄ tail、610-row coefficient audit 或任何 comparator。Python 中对应公式是独立转写的数学表达式；上述检查没有解析/elaborate/kernel-check Lean。

```text
Core SHA-256:   fd54bf1330623fb04d0bd09d44c52d615dd546aeae0ab2f07bf95fa6b3db2f5b
Source SHA-256: d5e397318e3c58dcb2540fb63f8300693f49b1490e660f2e20e07ba246c5a143
```

## 未闭合前提及建议下一 child

| 层 | 未闭合边界 |
| --- | --- |
| Source lever | 新 yaw/cross/local-origin 及既有 origin/axis seam 全部仍未编译；无 kernel/axiom receipts |
| Center | b_i 不需要 center；完整 v_i 与其 Gram 接口仍要求 `CenterOffsetTarget`，只消费已存在的候选 |
| Tail | 仅复用既有 terminal-origin 关系，不修改、不重查 v₃/v₄ tail；其已有 Lean 状态不因本轮检查改变 |
| Mass / Fourier | 尚未展开前三列与尾部列的 mass Gram 项；没有新的 CSV/literal/Fourier/legacy trace 证明 |
| Coverage / registry | 没有全 `5×5`/36-entry coverage、零补集或 registry 准入证据 |
| Lean | 未运行 Lean/Lake；import closure、工具链、tactic/API 和 axiom 审计仍待未来获授权的核验 |

建议下一 DAG child 为 `body6_first_three_offset_gram`：消费当前三个 `B_i`、保持的 offset 项及旧 tail 局部列，优先做前三列与尾部列的混合 Gram；本轮不创建/更新任何 DAG 节点。

交付状态：**四个新文件完成；定向符号检查通过；source/Lean/coverage/registry 正式证据仍 fail-closed。** 保持 `lean_lake_run=false`、`source_levers_proven=false`、`source_mass_coverage_proven=false`、`registry_eligible=false`、`registry_status=pending`、`formal_certificate_allowed=false`。
