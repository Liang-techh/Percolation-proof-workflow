# P4：entrywise absolute bounds → quadratic upper bound

日期：2026-09-07。新增 `NEW_P4_032_EntrywiseQuadratic.lean` 与本 review。
状态为 **未编译的 source-independent skeleton**。未运行 Lean/Lake、浮点特征值、
source checker；未修改旧文件、state、registry、共享脚本，也未重写 residual_load_cap。

## 显式系数条件

对任意实数 2×2 矩阵 S，外部提供非负矩阵 A 及全部四项精确界：

```text
Aij≥0， |Sij|≤Aij。
```

令 `c=(A01+A10)/2`，`b0=A00+c`，`b1=A11+c`。新证明脚本依次得到：

```text
rᵀSr ≤ A00*r0² + (A01+A10)*|r0*r1| + A11*r1²
      ≤ b0*r0² + b1*r1²
      ≤ k*||r||₂²， 若 b0≤k 且 b1≤k。
```

第二步只使用 `2|r0||r1|≤r0²+r1²` 和非负系数；没有 PSD 或对称性前提。
`norm2_sq_coordinates` 明确连接前轮 Euclidean `WithLp.toLp 2` 范数与两个坐标平方和，
没有把原始 Pi 函数空间的默认范数当成 ℓ₂。

提供三种候选 constructor：

- `ofEntryBounds`：接受外部 k≥0 和两个 row budget 比较。
- `ofEntryMax`：取 `k=max(A00+c,A11+c)`，并由 A≥0 证明 k≥0。
- `ofUniformBound`：若 s≥0 且全部 `|Sij|≤s`，取 **k=2s**。

它们输出 `NonnegativeUpperBound S`，同时携带 k、k≥0 和既有
`QuadraticUpperBound S k`。下游使用同一个 packet 的 `.k`、`.nonnegative`、`.upper`，
即可填入上一轮 QuadraticLoad 的对应参数；没有重新证明 load 传播定理。

## 精确含义与限制

这是二次型的上界证据，不提供 S 的 PSD 下界。S 可非对称、不定或负定。
不能从 k≥0 或非负绝对系数表推断 `rᵀSr≥0`。也没有把 A 声称为 S 的 Loewner 上界。
`k=max(b0,b1)` 是可检查的充分界，不声称最优；分别取两个 off-diagonal 条目的绝对
上界可能丢失反对称部分的相消，因此不是精确特征值替代物。

若 A/s 来自有理或 interval exporter，必须给出真实 S 条目的精确绝对值上界证明；
浮点近似、采样最大值、数值特征值或未经认证的舍入均不自动构成 `hEntries`。
本轮没有给实际 S、A、s 或 k 填入数值。

精确剩余前提：实际 SBB 及其坐标/normalization 身份、四项 entrywise bounds 的正式
证明、与下游相同 SBB 的匹配、真实 residual cap/LoadBinding 与域有效性；以及本文件
及所导入前轮 skeleton 的 elaboration/kernel、公理检查。

本轮只读核对本地 Mathlib 的 `EuclideanSpace.real_norm_sq_eq` 与 `PiLp.toLp_apply`
声明，未执行证明脚本。末尾 `#print axioms` 没有运行输出；不声称 Lean compile、
source/coverage/Schur/PMI closure 或 registry admission。
