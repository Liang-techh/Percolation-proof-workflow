# P4：Schur/PMI absorption 的标量负分支

日期：2026-09-07。新增 `NEW_P4_032_AbsorptionObstruction.lean` 与本 review。
**UNCOMPILED bounded source-independent proof attempt**：仅静态检查和纸面代数审阅，
未运行 Lean/Lake 或公理检查，不宣称 Lean 验证、source/coverage/admission/registry 结果。
没有修改共享脚本或旧模块，没有重复 absorption 正分支。

## 1. rho_eff≥1 排除正 slack

`no_positive_slack`：若 rho≥1，则不存在 delta>0 满足 rho+delta≤1。
`no_effective_slack` 使用前轮原有的 `Slack p delta` 类型，直接接到 `rhoEff p`。
这是指定单位能量系数通道的严格 gate；没有宣称所有 Schur/PMI 方法均不可能。

## 2. residual 上界本身不限制能量

`ResidualFeasible rho B E q` 仅保存 E≥0、q≥0、q≤rho*E+B。
对于任意 rho≥0、B≥0 和任意有限实数候选上界 C，取精确实数

```text
E = max(0,C)+1, q = 0。
```

则 E>C，而 q≤rho*E+B 仍然成立。
`residual_only_counterexample` 给出此显式见证，`no_residual_only_cap`
将其写成不存在对全部可行标量点统一有效的有限实数 energy cap。
结论也适用于 rho<1，包括 rho=B=0；它说明缺少 energy 与 q 的闭合关系。

`residual_only_affine_counterexample` 对任意固定非负 base、a、b 令 C=a*base+b，
给出 E>a*base+b 的反例；因此不能仅由 residual 上界推出这种有限 affine energy bound。
候选参数必须先固定，不能依赖所选 E。一般 C 定理实际还允许负 C；
affine 包装中的非负字段保留预算语义，不是反例代数必需条件。

`effective_residual_only_counterexample` 调用原有
`effective_coefficients_nonnegative`，把反例接到原 `Parameters` 的 rhoEff/biasEff。
不重排 rhoEff/B_eff，也不构造新的权重或物理参数。

## 3. rho≥1 时，即使加反馈闭合仍不能统一有界

固定任意 rho≥1、B≥0、base≥0 和有限实数 C，取

```text
E = q = max(0,C)+1。
```

此时 q=E≤rho*E+B，且 E≤base+q。
`feedback_counterexample` 复用前轮 `FeedbackBinding`，给出上述反例；
`no_feedback_cap` 排除这个完整标量可行类上的统一有限 energy cap。
同样可令 C 为任意预先固定的 affine 表达式，包括 a*base+b。

`unit_feedback_ray` 单独记录精确边界 rho=1、B=base=0：任意 t≥0，E=q=t。
因此把严格 gate 改成 rho≤1，哪怕没有 additive bias，也不足以闭合能量上界。

`uniform_feedback_cap_requires_strict` 给出必要条件：在 B/base 非负时，
若对所有满足 residual budget 和 feedback 的标量点确实存在统一有限 cap，
则必须 rho<1。此文件不重复该条件下的充分性证明或除法公式。

## 量词与适用边界

这里否定的是“仅凭列出的标量前提，对全部可行点推出统一有限上界”。
不是否定每个单独实数 E 有上界，也不是否定附加约束后的具体 source 可能有界。
没有构造力/加速度缺陷、矩阵、轨迹或物理可实现反例；原有 typed 分支的更多结构
可能排除这些标量见证，必须另行证明，不能由本 obstruction 自动判断。

正 slack 不存在只阻断前轮指定的 absorption 通道；它不直接判定矩阵非 PSD、
PMI 不可行、动力学不稳定或其他方法不存在。
全文件使用精确实数与 max，没有浮点近似、sqrt、除零或数值抽样。
证明脚本及导入链均待 elaboration/kernel 检查，`#print axioms` 只是未执行的审计入口。
