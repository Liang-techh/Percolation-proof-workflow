# P4：defect cap 到 quadratic Schur/PMI residual load

日期：2026-09-07。仅新增 `NEW_P4_032_QuadraticLoad.lean` 与本 review。
**未编译、source-independent skeleton**；没有运行 Lean/Lake、数值特征值或求解器，
没有修改旧文件、state、registry、共享脚本。导入前轮 norm budget，未重做三角不等式。

## 最小二次型接口

`quadratic SBB rB = Σi Σj rB[i]*SBB[i,j]*rB[j]`，其中 SBB 是任意实数 2×2 矩阵。
不要求对称、PSD 或正定。范数继续使用前轮明确的 Euclidean ℓ₂ `norm2`。

`quadratic_cap` 接受以下全部显式前提：

```text
0≤rB_cap，0≤k，||rB||₂≤rB_cap，
rBᵀ SBB rB ≤ k*||rB||₂²。
```

输出 `rBᵀ SBB rB ≤ k*rB_cap²`。平方比较使用 cap 的非负性；乘以 k 时使用 k≥0。
不能仅给 k<0 的二次型上界就照搬同一 cap 代入，因为负系数会反转范数平方的序。
也不能把 cap 平方后反推原始范数 cap 具有正确符号。

局部、单点的 quadratic upper bound 已足够；可选 `QuadraticUpperBound SBB k`
将同样上界量化到所有向量，作为外部 proof-valued evidence。它不是数值最大特征值
报告，也没有提供 PSD 下界。一个不定或负定矩阵仍可能满足这样的上界。
本轮没有实现从浮点谱估计、矩阵 entries 或其他 operator evidence 生成该证明的算法。

## 将 budget 传入 load

`LoadBinding` 将真正的 Schur/PMI residual load 联系保留为外部前提：

```text
residualLoad ≤ baseLoad + weight*(rBᵀ SBB rB)。
```

另外要求 `weight≥0`。`residual_load_cap` 得到：

```text
residualLoad ≤ baseLoad + (weight*k)*rB_cap²。
```

load 可以正是二次型，也可以有已证明的 baseline/weight 上界；本文件不声称实际
Schur 消元、PMI normalization 或某个完整 residual 自动满足这条关系。
其他交叉项、源残差分量及其坐标权重必须已在 LoadBinding 中得到处理。
不能用这个抽象接口删掉它们，也没有自动增加一次 normalization。

`defect_quadratic_load` 实际调用前轮 `operator_budget`，取

```text
rB_cap = rho*alpha + tau*deltaD + deltaB，
R = Rport，T = MBD*MDDinv（在 O1 特化时）。
```

它保留 defect identity、R/T 作用界、加速度与两个 defect 范数 cap 的全部参数，
并得到

```text
residualLoad ≤ baseLoad + (weight*k)*(rho*alpha + tau*deltaD + deltaB)²。
```

没有置零 eD/eB，平方中的 cross terms 全部保留。显式 hcap 虽可由有效的前轮
范数预算推得，仍保留在本消费接口中，避免独立 cap 使用时丢失符号要求。

`allocated_load` 还要求外部证明右端总预算不超过 available，才输出
`residualLoad≤available`。它不等同于完成 Schur/PMI 矩阵条件或任何 absorption theorem。
`on_domain_load` 只在同一个 x∈D 上组合对应 SBB/rB/load 的各项前提，不认证域覆盖。

## 精确剩余前提

- 前轮 defect identity/norm budget 的真实绑定及所需作用界、cap；或独立给出同域范数 cap。
- 实际 SBB 与二次型身份、k≥0，以及局部或全向量 quadratic upper bound 的正式证明。
- 实际 load 的 LoadBinding、weight≥0；若要消费可用余量，还需预算 allocation 不等式。
- generalized-force/PMI normalization、source-domain、coverage、下游 Schur/PMI/absorption
  前提。这里没有从二次型上界反推 PSD 或构造逆矩阵。
- 本文件及前轮 skeleton 的 elaboration/kernel 与公理检查。
  所有 `#print axioms` 均未执行，没有 Lean compile 或 registry/admission 声明。
