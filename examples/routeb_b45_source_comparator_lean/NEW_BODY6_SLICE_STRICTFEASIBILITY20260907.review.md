# Body-6：排除零构型之后的严格 margin feasibility

状态：**OPEN_UNCOMPILED**。未运行 Lean/Lake，未取得内核验证或 registry admission。

新增 `NEW_BODY6_SLICE_STRICTFEASIBILITY20260907.lean`（110 行）及本定向 review。
唯一直接 import 为 `NEW_BODY6_SLICE_DOMAINREPAIR20260907`。
本叶将严格可行性与域排除条件分开，并增加有限单元覆盖的充分路径；没有验证任何实际候选域已经可行。

## 严格与非严格是不同谓词

\[
\operatorname{StrictMarginFeasible}(D,R)
\iff \exists\mu>0,\ \forall q\in D,\operatorname{RemainderMargin}(R(q),\mu).
\]

`NonstrictPSD D R` 定义为 `UniformMargin D R 0`。
`strict_implies_nonstrict_attempt` 将已证明的正 margin 降到 0；代码没有反向转换。
feasible 在这里要求真正的存在性证明，不能仅凭“避开零点”“uniform”或“feasible”的名称填入。

## 充分路径一：同域统一九项下界

`same_domain_nine_entries_feasible_attempt` 要求一个明确的共同 `mu>0`，以及

\[
\forall q\in D,\quad
\operatorname{NineEntryLowerBound}(R(q),\mu,\beta(q)).
\]

它消费上一叶已给出的九项充分条件到 `RemainderMargin` 的转换。
beta 可随 q 改变，mu 必须相同；所有条目不等式与对称性必须在同一 D 上成立。
若九项对角占优条件过强，仍可通过其他严谨方法给出正 margin；本叶不把这套充分条件当作必要条件。

## 充分路径二：有限单元覆盖

`FiniteCellMarginCover D R K cells rho` 明确分离三个证明字段：

| 字段 | 精确要求 |
| --- | --- |
| `cover` | 每个 `q∈D` 都属于某个 `k∈K` 对应的 `cells k` |
| `positive` | 每个选中单元的 `rho(k)>0` |
| `cellMargin` | 对每个选中 k、每个 `q∈D∩cells(k)`，都有 `RemainderMargin (R q) (rho k)` |

`K : Finset Config` 只作为有限单元标签集合。标签本身即使是某个配置，也不意味着检查该中心点就证明了整单元。
cells 无需互不相交；全称 `cellMargin` 必须成立于每个相应域交集。

`finite_cells_feasible_attempt` 从有限个正 rho 中取得共同正下界 mu，再对每个 q 使用 cover 选出的单元，将该点的单元 margin 降到 mu，得到整个 D 上的严格可行性。
复用的有限下界构造以 1 为初值逐项取 min，因此不声明所得 mu 最优。
若 K 为空，则 cover 只能覆盖空 D；此时结论为空域上的真命题，不能报告为物理域已验证。

`finite_cell_cover_from_entries_attempt` 允许以每个单元内全部点的九项下界来填写 `cellMargin`。
也允许其他真正的 `RemainderMargin` 证明填写这一字段，不强制采用九项充分条件。

**不能省略的区别**：有限点集上的正 margin 只验证这些点；有限单元覆盖则还要证明域覆盖和每个单元所有点上的下界。代码没有从 sampled PSD 或中心点证据自动产生这两个证明字段。

## 接回实际 source 的可行性契约

`SourceStrictFeasibilityContract D R` 保存中心偏移、实际固定权重绑定、
`ExactPhysicalFamily D R`、零构型排除证据与独立 `StrictMarginFeasible D R` 见证。
实际 body-6、front `{0,1,2}`、tail `{3,4}` 与 offset 的绑定均继承旧 source 系数定义。

`source_feasibility_excludes_zero_attempt` 复用原零方向障碍，证明实际 source 上已经成立的严格可行性要求 `0∉D`。
反向构造器 `source_feasibility_contract_attempt` 同时要求域排除和可行性见证，绝不只凭排除条件生成可行性。

`feasible_source_certificate_consumer_attempt` 从完整契约提取一个真正的共同正 mu，构造既有 `SourceDomainMarginCertificate D R mu`。
中心／实际权重和域内精确 source 绑定一直保留，未生成无条件 source 见证。

## 远离零点仍没有统一正 margin

本叶复用 DOMAINREPAIR 的精确抽象反例：

\[
D_{away}=\{(n+1,0,0,0,0,0):n\in\mathbb N\},\qquad
R(q)=\frac{1}{q_0+1}I_3.
\]

`away_counter_coordinate_gap_attempt` 明确证明每个域内点的第 0 坐标至少为 1，故该域不仅删除了零点，而且在这一坐标上与零分离。
每点有正 margin `1/(n+2)`，但这些值趋近于零，原精确 Archimedean 反证排除了任何共同正 mu。

`away_nonstrict_not_strict_attempt` 将三种事实合并：域不含零构型、域内有统一非严格 PSD、却没有严格统一 margin 可行性。
它复用原反例证明，没有重新运行无穷域推导或网格扫描。

这是独立的抽象实矩阵族，不是实际 body-6 的 source 数据或候选 Schur 数值。
域无界；反例没有排除加入适当紧致性、连续性及严格正性假设后的其他结论。
它只说明 domain exclusion、坐标分离和逐点正 margin 都不能单独替代共同下界证据。

## 当前仍缺少的实际可行性数据

1. 明确的候选域 D 及其成员、排除与必要 coverage 证明。
2. 域内候选 R 的实际 source 系数绑定，及中心偏移／实际权重见证。
3. 一个同域 uniform 九项见证，或真实有限单元覆盖与各单元正下界，或其他完整正 margin 证明。
4. 所有导入和新增 Lean 脚本的编译及内核验证。

本叶没有提供实际 cells、rho、mu 或域内数值表；不能据构造器的存在宣称实际严格 margin feasibility 已完成。
非严格分支仍需 `UniformMargin D R 0` 的实际证明，不能因未找到正 margin 就认定 PSD。

## 定向检查与变更范围

仅做小型精确代数核对：`rho*N − mu*N = (rho−mu)*N` 的展开差为零，配合非负平方和说明降 margin 的方向。
未测试任何 source 点或单元，没有 sampled PSD、旧数学回归或宽回归。

静态检查确认直接 import 文件存在，新 sidecar 未见 `sorry`、`admit`、`axiom` 或 `opaque`。
没有运行 Lean/Lake；未验证依赖闭包、实际 coverage 或内核证明。

sidecar 实际字节 SHA-256：
`a24595758ee169d9d9340eec71d226ebf71ea0c773e624741428834e8f545122`。

本次只新增这两个文件，未修改共享脚本、StateStore、registry 或既有叶。
实际域的严格可行性、完整矩阵 PSD、Fourier、coverage、Lean 验证与 registry admission 均保持未闭合。
