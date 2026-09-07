# Body-6 tail inverse／solve certificate

状态：**OPEN_UNCOMPILED**。所有新增结论均为 proof attempts；未运行 Lean/Lake，未取得内核验证或 registry admission。

新增 `NEW_BODY6_SLICE_TAILSOLVECERT20260907.lean`（107 行）及本定向 review。
直接导入 `NEW_BODY6_SLICE_EXACTSCHURCOEFF20260907`，消费已有精确 Schur seam 中的 tail inverse 证据。

## 三个对象严格区分

| 对象 | 类型 | 必需含义 |
| --- | --- | --- |
| B | `Fin 2 → Fin 2 → ℝ` | `B = sourceTail q`，实际 body-6 tail |
| D | `Fin 2 → Fin 2 → ℝ` | `D = inverseTail (q 4) offset m kappa`，需有乘积证据才是 B 的逆 |
| Y、V | `Fin 2 → Fin 3 → ℝ` | 任意右端列族及 `V=D*Y=solvedRight ... Y` |

V 是矩形的已求解列，不能与 B 或 D 混同，也不在本接口中再次求逆。
实际 body 索引为 5，即通常编号的 body-6；内部 tail 顺序为 `{3,4}`。
`q 4` 使用从 0 开始编号，offset 始终为既有 `7/200`。

## SourceTailInverseCertificate 的完整绑定

证书参数一次固定 `q,m,kappa,B,D`，字段显式保存：

1. `CenterOffsetTarget`；
2. 实际 `SourceWeightsTarget m kappa`；
3. `kappa > 0`、`m ≥ 0`、`offset² ≥ 0`；
4. B 与同一 q 的 `sourceTail` 等式；
5. D 与同一 `q 4/offset/m/kappa` 的 `inverseTail` 等式；
6. 两个实际表达分母 `kappa+m*offset²*sin²(q 4)` 与 `kappa+m*offset²` 严格为正；
7. 全部条目上的 `B*D=I₂` 与 `D*B=I₂`。

因此不能在证书里混用另一个配置、权重或偏移的逆表，也不能仅凭相同维度将任意 D 命名为逆矩阵。

`inverse_certificate_from_exact_seam_attempt` 从精确 Schur 契约的
`tailCore.tailAdapter.leftInverse/rightInverse` 字段提取两侧乘积证明，另保留中心、权重、符号前提。
它没有从 R 的系数恒等式、PSD 或 uniform margin 反推逆矩阵性质。

## 由逆证据到求解列

`BD_identity_solves_attempt` 是一个小型有限和引理：只要已有全部条目的 `B*D=I₂`，
就能对任意 `y : Fin 2 → ℝ` 得到 `B*(D*y)=y`。
证明消费两列单位矩阵等式，不重新推导 tail 主子式、Gram 或倒数表。

`SourceTailSolveCertificate` 保存：

- 完整的 `SourceTailInverseCertificate`；
- 逐项 `Vaj = action2 D Y[:,j] a`；
- `ColumnSolveEvidence B Y V`，即每列 `B*V[:,j]=Y[:,j]`。

`solvedRight_certificate_attempt` 用既有 `inverse_action_formula_attempt` 将同参数的
`solvedRight` 接到 D 的矩阵作用，再使用 `BD_identity_solves_attempt` 填写列求解义务。
证书中的 Y 可以是任意实列族；它不因此获得实际 mixed source 的绑定。
需要实际 Schur 消元时，仍须另有 `SourceBlockBinding` 对 Y 的条目和方向绑定。

## 求解列证据不能单独升级成逆证据

`ColumnSolveEvidence` 只描述指定 Y 的列，不量化全部实右端。
这些列若未证明张成整个 tail 空间，即使 V 的确等于 D*Y，也不能仅从 `B*V=Y` 得到 `B*D=I₂`。
本叶没有提供从独立 `ColumnSolveEvidence` 到逆证书的无前提转换。

## 三个精确抽象反例

以下均为独立实矩阵控制例，**不是实际 body-6 参数或 source 数据**，不反驳带完整前提的 source 逆定理。

1. **零分母**：取抽象 `z=0,h=1,m=1,kappa=0`，原表为 `diag(0,1)`。
   Lean 的实数除法全定义使倒数表也成为 `diag(0,1)`，但其乘积 `(0,0)` 项为 0，单位矩阵要求为 1。
   `denominator_zero_counterexample_attempt` 明确记录第一分母为零与乘积失败；该实例不满足 `kappa > 0`。
2. **正分母但 D 错误**：取抽象 `z=0,h=1,m=1,kappa=2`，原表为 `diag(2,3)`，两个分母均为正。
   若擅自选择 `D=I₂`，`B*D` 的 `(0,0)` 项为 2 而非 1。
   `positive_denominators_wrong_D_attempt` 说明分母正性和相同形状不能替代 D 的表达绑定或乘积证明。
3. **列求解通过但 D 不是逆**：仍取 `B=diag(2,3)`，令 `D=0`、`Y=V=0`。
   此时 V 与 D*Y 一致且所有指定列都满足 B*V=Y，但 B*D=0≠I₂。
   `solved_columns_not_inverse_attempt` 同时保存作用一致性、列求解成功与逆乘积失败。

## 定向检查与开放义务

一次小型 Python/SymPy 精确检查核对上述三个抽象控制例：
零分母例使用显式模仿 Lean 的 `inv0(0)=0` 约定；其 `BD00=0`，错误单位逆例 `BD00=2`；
零列例精确满足 B*V=Y 而 B*D 不等于单位矩阵。
没有把 SymPy 的通常零除行为误当成 Lean 实数零倒数语义。

静态检查确认直接 import 文件存在，新增 sidecar 未见 `sorry`、`admit`、`axiom` 或 `opaque`。
这不构成 Lean 编译、依赖闭包或内核公理验证。没有执行 Lean/Lake、旧数学检查或宽回归。

sidecar 实际字节 SHA-256：
`0579d89d67df19704270877ba1554e15753235b3456abd37835e2a3de6878320`。

仍未闭合：无条件中心／权重见证、任意候选 B/D/Y/V 的绑定、实际余项 margin、配置域 coverage、Lean 验证及 registry admission。
本次仅新增这两个文件，未修改 registry、StateStore、共享脚本或旧叶；没有宣称完整 body-6 PSD、Fourier 或全系统消元正确性。
