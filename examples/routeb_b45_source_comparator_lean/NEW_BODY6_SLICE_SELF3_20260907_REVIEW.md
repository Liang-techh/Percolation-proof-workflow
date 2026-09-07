# Body-6 first-three self axis/velocity Gram

本轮只处理前三列自身的 `3×3` 块，给出明确有限表、通用 yaw/isometry 接口与真实 source 接线。**不假设前三列为零，所有 source velocity 结果显式保留 `CenterOffsetTarget`。全部 Lean 文件未编译；没有运行 Lean/Lake。**

## 输出与依赖

| 文件 | 全部直接 imports / 职责 |
| --- | --- |
| `NEW_BODY6_SLICE_SELF3_Core20260907.lean` | `NEW_BODY6_SLICE_LEVER_Core20260907`；三列稀疏坐标模板、六个独立 Gram 项、yaw 传递及 source-independent offset 表 |
| `NEW_BODY6_SLICE_SELF3_Source20260907.lean` | 新 Core、`NEW_BODY6_SLICE_LEVER_Source20260907`；消费已有真实前三列局部式并连接 self axis/velocity targets |
| 本 review | 公式、精确范围、检查、开放前提 |

Core 的传递依赖只到已有纯 lever/cross/rotation 代数和 Mathlib。Source 复用 LEVER Source 的 origin/axis/velocity 接线，不引入 MIXED Core/Source、VGRAM Tail/Consumer 或 STEP6 Fourier/data consumer。

本轮只新增这三个指定目录内的文件，未修改旧 source/lever/tail、state、registry、shared scripts 或其他任务文件。没有重新展开 DH、重做 mixed/tail 或 Fourier 检查，没有执行 comparator、git add/commit。

## 精确坐标，不消掉 offset

两边索引均为 `i,j : Fin 3`，通过已有 `firstJoint` 保留 `.val`，对应零基 source joints `0,1,2`。body 仍是 human body 6，即 `5 : Fin 6`；`a : Fin 3` 表示笛卡尔分量。

令 `φ=q 1+q 2`、`y=q 3`、`z=q 4`，沿用已有 lever 记号 `A=radial q`、`P=height q`、`Q=reach q`。第六轴的局部坐标记为

\[
\begin{aligned}
X&=\cos\phi\cos y\sin z+\sin\phi\cos z,\\
Y&=\sin y\sin z,\\
Z&=\cos\phi\cos z-\sin\phi\cos y\sin z.
\end{aligned}
\]

前三个局部 parent axes 是 `W₀=(0,0,1)`、`W₁=W₂=(0,1,0)`。于是完整 local velocity 继续为

\[
L_i=B_i+h(W_i\times(X,Y,Z)),\quad h=7/200.
\]

引入六个标量

\[
\begin{array}{ll}
a=1/20+hY,& b=A+hX,\\
p=P+hZ,& r=Q+hX,\\
u=(19/100)\cos\phi+hZ,&v=(19/100)\sin\phi+hX.
\end{array}
\]

则三个完整列恰为

\[
L_0=(-a,b,0),\qquad L_1=(p,0,-r),\qquad L_2=(u,0,-v).
\]

这些是坐标稀疏性，不是零向量假设。六个标量都保留相应 h 项；没有把 `baseLocal` 当成完整速度，也没有利用 axis Gram 中的零项来推断 velocity Gram 为零。

## 显式有限表

轴 Gram 是

\[
G^{axis}=\begin{bmatrix}1&0&0\\0&1&1\\0&1&1\end{bmatrix}.
\]

速度 Gram 是

\[
G^{vel}=\begin{bmatrix}
a^2+b^2&-ap&-au\\
-ap&p^2+r^2&pu+rv\\
-au&pu+rv&u^2+v^2
\end{bmatrix}.
\]

`templateColumns` 与 `templateGram` 对任意六个实标量定义这个结构。`template_gram_attempt` 只展开三项有限和并做多项式归约；`template_symmetric_attempt` 利用显式表的转置一致性。`yaw_template_gram_attempt` 将该模板推广到任意共同 yaw 后的向量，消费已有 `yaw_isometry_attempt`。

`velocity_template_attempt` 把固定的真实局部列表达映射到这些标量；`local_self_velocity_gram_attempt` 输出 `selfVelocityEntry`。**这些局部坐标/Gram 计算不需要新增 `X²+Y²+Z²=1` 前提，也不需要额外三角平方恒等式。** source yaw 的等距性仍依赖其已有旋转证明候选，不能据此声称整个 source 链不需要三角知识。

九个 entry 中只有六个独立项；对称性提供另外三个。所有定义完整保留 off-diagonal velocity 项 `−ap、−au、pu+rv`。

## 真实 source 接线和 center 边界

Source 使用已有 `source_first_axis_local_attempt` 与 `source_first_velocity_local_attempt`，没有重新证明 parent origins 或 lever。新 `source_first_template_attempt` 把该真实速度列的共同 yaw 表达转为上面的稀疏模板。

具体接口是：

```lean
source_self_axis_attempt : SelfAxisTarget

source_self_velocity_attempt
  (hc : CenterOffsetTarget) : SelfVelocityTarget

source_self_gram_interface_attempt
  (hc : CenterOffsetTarget) : SelfAxisTarget ∧ SelfVelocityTarget
```

其中 velocity 左端精确为

```lean
∀ q (i j : Fin 3),
  dot3 (sourceV q (firstJoint i)) (sourceV q (firstJoint j)) =
    selfVelocityEntry q offset i j
```

`offset` 来自之前 source 层的 `7/200`。新代码没有自动供应/隐藏 center witness；所有 source velocity 及 transpose theorem 都保留 hc。轴接口自身不需要 center。q 的域仍为任意 `Fin 6 → ℝ`，没有缩到 cell 或单点。

## 定向 exact/static 检查

使用只读内存 Python/SymPy，令 `A,P,Q,C,S,X,Y,Z,h` 为自由多项式变量；`C,S` 对应 `cos φ,sin φ`，但检查不使用任何单位圆约束。分别计算

1. `B_i+h(W_i×(X,Y,Z))` 与 `(-a,b,0)/(p,0,-r)/(u,0,-v)` 的九个坐标残差；
2. 三个已知 first axes 两两点积与显式 axis 表的九个残差；
3. 三个模板列两两点积与显式 velocity 表的九个残差。

27 个 exact polynomial residual 全部为零。检查未读取 CSV、未重放 source DH、未执行 mixed/tail checker，也没有数值采样或容差。静态检查两份新 Lean 无 `sorry/admit/axiom/opaque` 声明。

该检查验证独立转写的有限数学表，不解析或 kernel-check Lean tactic，不是 source theorem receipt。

```text
Core SHA-256:   f13a94fa4989a87e00e18e552a42ef6c9b294f3d7ae389bb51cb4b0e367d980b
Source SHA-256: 228fbb3621cdd600c607da9dbb076ba2efe012bc49383a4a1a9b0bfcea6aec64
```

## 仍开放的范围

- 所有新旧 Lean import、source/yaw/lever/center proof-attempt 均尚无本机编译与 axiom receipt；不能把本轮代数检查提升为已验证 source。
- `CenterOffsetTarget` 对 source velocity 仍是显式前提，未在本轮闭合。
- 只交付此 `3×3` self block 的 axis/velocity 接口；不重新处理 mixed `3×2` 或 tail `2×2`，也没有把它们合成为完整 `5×5/6×6`。
- 没有质量/惯量加权 mass theorem、Gram→Fourier/CSV/legacy trace 接线、全 coverage 或 registry witness。
- 后续可以单独考虑将 self/mixed/tail 的 source 接口按正确权重组合，但这必须继续区别数学候选、Lean 编译、source binding、coverage 和 registry 准入；本轮不创建 DAG child、不修改 state。

最终状态：**Core/Source/REVIEW 三个 scoped 新文件完成，27 个有限代数残差通过，全部 Lean 未编译。** `lean_lake_run=false`、`source_self_gram_proven=false`、`coverage_proven=false`、`registry_eligible=false`、`registry_status=pending`、`formal_certificate_allowed=false`。
