# P4 true-DH/K-path：无除法标量收缩接口定向审阅

日期：2026-09-07。新增 `NEW_P4_032_DivisionFreeContraction.lean` 与本定向 review。
状态：**UNCOMPILED bounded proof attempt**。仅文件静态检查及纸面代数审阅；
未运行 Lean/Lake、公理检查或广泛回归。未修改原模块或共享脚本。

## 核心接口与不重复范围

该文件仅依赖 Mathlib，处理已经闭合的单条标量不等式，
不导入或重建 SchurPMIAbsorption 的参数包、typed residual 分支、
Schur 恒等式、加权 Cauchy、rho_eff/B_eff 重排或反馈消元链。

`closure_iff_scaled` 给出任意实数上的恒等重排：

```text
E ≤ B+rho*E  ↔  (1-rho)*E ≤ B。
```

重排本身不需要符号条件。
`division_free_contraction` 保留请求中的 E≥0、B≥0、rho<1，输出上述缩放界。
`allocated_upper_bound` 在 rho<1 且调用者提供 `B≤(1-rho)*cap` 时推出 E≤cap，
仅通过正数乘法消去。Lean 声明和证明中均无除法、倒数或 sqrt。
E、B 的非负性不是这个上界消去步骤的必要条件。

## 负条件必须分别解释

| 情况 | 精确结论 | 对应接口 |
| --- | --- | --- |
| rho≥1、B≥0 | 标量可行类无统一有限 E 上界 | `noncontractive_counterexample` / `no_noncontractive_uniform_cap` |
| rho=1 | 闭合不等式等价于 B≥0，与 E 无关 | `critical_closure_iff` |
| rho>1 | 重排后约束是 `-B≤(rho-1)*E`，控制下侧 | `closure_iff_lower_form` |
| rho<1、E≥0、B<0 | 前提不相容，没有可行 E；不能称为无界反例 | `negative_bias_inconsistent` |
| rho<1、缺 E≥0 | 仍可控制 E 上界，但不保证非负性或下界 | `allocated_upper_bound` / `missing_energy_sign_no_lower_bound` |

因此不能把“B<0”或“缺 E≥0”单独记录为有限**上界**不存在的条件。
通常的实数上界 B/(1-rho) 在 rho<1 时对任意实数 B、E 都成立；
这里将消费者写成无除法 allocation 形式。
`feasible_nonnegative_energy_requires_nonnegative_bias` 进一步说明：
当 E≥0、rho≤1 且闭合成立时，B≥0 已是推论。

## 精确实数见证

对于 rho≥1、B≥0，给定任意有限实数候选 C，取
`E=max(0,C)+1`，则 E≥0、E>C 且 E≤B+rho*E。
这排除对全部此类标量可行点统一有效的有限 cap，也排除预先固定的有限 affine cap。
反例没有声称 rho=1、B<0 也存在可行点；该边界实际上不可行。

`negative_bias_signed_witness` 取 rho=0、B=-1、E=-1，闭合成立且所有可行 E 都满足 E≤-1。
这直接反驳“负 B 或负 E 自动破坏有限上界”的错误解释。

`missing_energy_sign_no_lower_bound` 固定 rho=B=0，对任意候选下界 L 取
`E=min(0,L)-1`。闭合仍成立，且 E<0、E<L；上界 E≤0 并未丢失。
因此缺 E≥0 阻碍的是非负能量解释和从单侧上界升级到双侧大小控制。

## true-DH/K-path 接入边界

调用者必须先在相同状态、域、能量/度量与归一化下证明实际的
`E≤B+rho*E`；本文件不从 true-DH、K-path 或任何样本生成该前提。
若要覆盖整个域，需要逐点闭合证据，并使 rho/B/cap 的选择对目标域统一有效。
单点 rho<1 不自动提供全域一致的正收缩余量。

反例仅针对列出的实数可行类，不是物理轨迹或 typed force/accel 的可实现反例，
也不排除附加结构使具体 source 有界。
新证明脚本待 elaboration/kernel 检查；没有 Lean 验证、source/coverage/admission/registry 结论。
