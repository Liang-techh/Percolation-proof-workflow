# Body-6：零构型之后的域修复／margin 请求分叉

状态：**OPEN_UNCOMPILED**。未运行 Lean/Lake，未取得内核验证或 registry admission。

新增 `NEW_BODY6_SLICE_DOMAINREPAIR20260907.lean`（118 行）及本定向 review。
唯一直接 import 为 `NEW_BODY6_SLICE_ENTRYMARGIN20260907`。
本叶保留其精确零方向障碍，区分域与 margin 的请求形状和真正已证明的 margin 家族。

## 两个请求分支

`DomainMarginRequest D mu : Prop` 有两个构造分支：

| 分支 | 请求条件 | 不能据此推断 |
| --- | --- | --- |
| `nonstrict` | `mu=0` | R 在域内已经 PSD |
| `strict` | `mu>0` 且零构型不属于 D | 域内已经存在统一正 margin |

非严格请求也允许在不含零构型的域上使用；排除零构型没有强制选择正 margin。
请求结构不包含 margin 证明，不能被当成证明已完成或准入状态。

## 零方向与 source-binding 前提的保留

`ExactPhysicalFamily D R` 要求域内每个 q 的候选 R 满足实际条目绑定
`ExactSourceEntries q (3/20) (1/60) (R q)`。
body-6、front `{0,1,2}`、有序 tail `{3,4}` 及 `offset=7/200` 均由继承的 source 系数定义固定。

`contains_zero_forces_zero_margin_attempt` 明确消费：

- `CenterOffsetTarget`；
- 实际固定质量与已除惯量的 `SourceWeightsTarget (3/20) (1/60)`；
- `0∈D`；
- `ExactPhysicalFamily D R`；
- 一个已经提供的 `UniformMargin D R mu`。

它通过 exact entries 将 `R(0)` 替换为实际 source 系数表达，再调用旧
`source_zero_no_positive_margin_attempt`。该旧障碍来自精确向量 `(0,-19,40)`、平方范数 1961 和零构型上的 `R*u=0`。
因此 mu 不能严格为正；另一方面已提供的 `RemainderMargin` 要求 `mu≥0`，合起来得到 **mu=0**。

这不是无条件证明域内 PSD，只是约束一个已经成立的 margin 家族所能使用的 mu。
`positive_uniform_excludes_zero_attempt` 给出相应必要条件：绑定真实 source 且已成立的统一正 margin，要求零构型不在域内。
没有省略中心／权重前提，也没有把未编译的 source 链升级成内核验证结果。

## 请求与证书分开

`SourceDomainMarginCertificate D R mu` 保存五部分：中心前提、实际权重绑定、域内精确 source 条目绑定、请求分支、已证明的 uniform margin 家族。

`strict_domain_certificate_attempt` 必须接收 `mu>0`、排除零构型的证据以及外部 `UniformMargin D R mu`。
`nonstrict_domain_certificate_attempt` 则必须接收外部 `UniformMargin D R 0`。
没有任何构造器仅凭改变请求分支、缩小域或 source binding 自动生成 margin。

## 删除零构型的含义

`punctured D = D \ {0}`，`punctured_excludes_zero_attempt` 只证明新域不含零构型。
`existing_margin_restricts_attempt` 允许把一个已经证明的 margin 家族限制到这个子域，mu 保持原值。
它不会把 `mu=0` 提升为正数，也不会给尚未证明 margin 的域创造新的见证。

## 排除零构型仍不够：精确抽象反例

定义新域

\[
D_{away}=\{q_{n+1}:n\in\mathbb N\},
\quad q_k=(k,0,0,0,0,0),
\]

并复用抽象矩阵族 `counterR(q)=I₃/(q0+1)`。
此域的第 0 坐标至少为 1，所以明确不含零构型；每点精确正 margin 为 `1/(n+2)`。
但它不存在共同正 margin：任取 `mu>0`，选自然数 `n>1/mu`，便有 `1/(n+2)<mu`，与基向量检验要求的 `mu≤1/(n+2)` 矛盾。

对应定理为 `away_counter_excludes_zero_attempt`、`away_counter_pointwise_positive_attempt` 和
`away_counter_no_uniform_positive_attempt`。
这说明排除零构型，甚至再加上逐点正 margin，也不足以自动得到无限域的统一正 margin。

此族是独立抽象反例，**不是实际 body-6 source 余项或跨块数据**。
该域是无限、无界的；本叶没有反驳带额外紧致性、连续性及相应严格正性前提的其他定理。
实际 body-6 的其余退化构型和域内 margin 下界仍需单独研究。

## mu=0 请求也不是 PSD 证明

`zero_request_does_not_prove_psd_attempt` 使用另一个明确的抽象矩阵 `R=-I₃`：基向量上的二次型为 -1，因此不满足 `RemainderMargin R 0`。
该例只说明“选择非严格请求”不等于“完成 PSD 证明”，不是 source 反例。

## 仍需补足的域修复证据

1. 明确配置域及其成员／排除证明；不能仅凭“避开奇异点”的名称声明实际域已修复。
2. 候选 R 在域内的精确 source 系数绑定，以及中心／实际权重前提。
3. 对严格分支，新的共同正 margin 见证或上一叶要求的域内九项不等式家族；排除零构型只是必要条件之一。
4. 对非严格分支，真正的域内 PSD／零 margin 见证；零方向障碍没有自动提供该证据。
5. 独立的 coverage 和 Lean 验证。没有从有限样本或分支命名推广至全域。

## 定向检查与变更范围

只执行一次小型精确检查：核对 `mu*(n+2)-1=(mu*n-1)+2*mu` 的代数差为零，以及抽象 `-I₃` 的基向量二次型为 -1。
复用了旧零方向 proof attempt，没有重算旧 source 表、重复 PSD 筛选或运行宽回归。

静态检查确认直接 import 文件存在，新 sidecar 未见 `sorry`、`admit`、`axiom` 或 `opaque`。
未执行 Lean/Lake；这些检查不能替代编译、依赖闭包或内核验证。

sidecar 实际字节 SHA-256：
`72d50f91912814f6c37ba5960598f4e34c75aff489518847418055a874d08d80`。

本次仅新增这两个文件，没有改 registry、StateStore、共享脚本或既有叶。
未声称域修复已经成功、实际全域 PSD／正 margin、完整矩阵性质、Fourier、coverage 或准入完成。
