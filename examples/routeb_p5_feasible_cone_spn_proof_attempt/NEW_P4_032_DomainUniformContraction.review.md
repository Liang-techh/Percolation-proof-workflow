# P4 true-DH/K-path：domain-uniform contraction 定向审阅

日期：2026-09-07。新增 `NEW_P4_032_DomainUniformContraction.lean` 与本 review。
状态：**UNCOMPILED bounded source-independent proof attempt**。
仅静态/纸面审阅，不运行 Lean/Lake 或大回归，不修改原模块与共享脚本。

## 必须先澄清的有限域量词

固定有限域上，若每点 rho(x)<1，则必有共同的 rhoBar<1：非空域可取有限最大值。
所以“一个固定有限域每点严格收缩、却不存在统一 rhoBar<1”的反例不可能成立。
`finite_strict_majorant` 用 Finset 归纳与 max 表达这一事实，空域可取 rhoBar=0。

本轮有限点反例是**参数化的两点实例族**：每个实例各有自己的严格常数与有限 cap，
但不能从点态条件得到对整个族共同有效的常数和 cap。
另给 N 上的单一无限域反例，满足题目中“没有统一 rhoBar”的字面条件。

## 精确实数反例

定义 `E_n=2^n`、`gap_n=0.5^n`、`rho_n=1-gap_n`，统一取 B=1。
Lean 中 0.5 是精确实数常量，不使用 Float。
`dyadic_point` 给出：

```text
0 ≤ E_n, 0 ≤ rho_n < 1,
E_n = 1 + rho_n*E_n。
```

其核心身份是 gap_n*E_n=1；证明只用乘法与自然数幂。
`dyadic_energy_growth` 给出 E_n≥n+1，`dyadic_exceeds` 使任何有限实数 cap 都被某点超过。
`no_dyadic_uniform_rho` 用 Archimedean 性质及该增长证明不存在 rhoBar<1 覆盖所有 n，
不构造含变量分母的阈值。

`twoPoint n` 是 Fin 2 上的实例：锚点为 E=1、rho=0；另一点为 E_n、rho_n；两点 B 均为 1。
`twoPoint_closed` 提供完整 pointwise closure 证据。
`two_point_family_counterexample`：给定任意 C，存在某个两点实例，其第二点 E>C。
`no_family_uniform_rho` 排除覆盖全部 n 和两个点的共同 rhoBar<1。

例如 n=2 的实例是 (E,rho)=(1,0)、(4,0.75)，均满足闭合等式。
该实例自身可取 rhoBar=0.75、cap=4；它只反驳小于 4 的候选 cap。
任意 cap 都可被击败依赖的是“随后选择 n”的量词，而不是声称这一固定实例无界。

## 消费 uniform 输入的 typed bridge

`BudgetField X` 固定 domain、energy、bias、rho 四个函数。
`PointwiseClosure f` 要求域内每点 E/B/rho 非负、rho<1 和 E≤B+rho*E。
`UniformBudget f` 对同一个 f 保存全部明确证据：

```text
0≤rhoBar<1, 0≤biasBar, 0≤cap,
∀x∈domain, rho(x)≤rhoBar,
∀x∈domain, B(x)≤biasBar,
biasBar≤(1-rhoBar)*cap。
```

`uniform_cap` 先利用 E(x)≥0 将 rho(x) 替换成 rhoBar，再替换 B(x)，
最后调用原 `DivisionFreeContraction.allocated_upper_bound`，输出域内 E(x)≤cap。
没有重复该标量收缩/消去证明，也未建立新的 Schur/PMI 正分支。
E≥0 在这里用于对 rho 的单调替换，不能因前轮标量消去不需要它就从此接口删除。

包中没有默认参数、可选证据或由点态 strict 自动生成 uniform 输入的路径；
缺少全域比较或 allocation 就不能构造此消费者所需的证明包。
这一 fail-closed 含义仅属于显式类型前提，不是经过运行验证的准入系统声明。

## 必要性与剩余边界

反例证明“点态严格收缩 + 统一 B”不足以保证统一 cap；
它不声称 uniform rhoBar<1 是每个具体受限模型有界的必要条件。
例如额外 E 上界或 B 与 gap 同时衰减，仍可能在无统一 rhoBar 时给出有界结果。

定理要求的 domain 谓词是调用者指定的；类型绑定同一函数不等于证明它们来自 true-DH、
K-path、某个 normalization 或真实 source。域外点没有结论，有限采样也不提供全域量词。
没有 true-DH/source/coverage/admission/registry 绑定或验证声明。

证明脚本含 Archimedean API、Finset 归纳及 tactic elaboration，尚待实际 Lean/kernel 检查；
`#print axioms` 未执行。无变量除法、倒数、sqrt、浮点近似或数值回归。
