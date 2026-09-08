# Row-space recovery seam

状态：`OPEN_UNCOMPILED / pending`。仅 source-independent Lean 候选；未运行
本机或远程 Lean/Lake，没有 compiled/VERIFIED 或 kernel/axiom 审计声明。

新增 `NEW_ROWSPACE_RECOVERY_20260908.lean`，namespace RouteBP4RowspaceRecovery。
本轮只处理 recovery，不重复 principal restriction 或 Schur 消元。

## 四个窄接口

X 是任意实向量空间，row_i 与 coordinate 是显式线性泛函，s 是有限行索引集。

1. `recover_from_combination`：给定查询点 x 处
   coordinate(x)=Σ weight_i row_i(x) 与 row_i(x)=rhs_i，推出
   coordinate(x)=Σ weight_i rhs_i。没有求解权重或自动建立行空间成员。
2. `kernel_on_of_combination`：在指定差向量域 K 上，行组合恒等式推出
   “所有选定行取零 ⇒ coordinate 取零”。没有证明全空间核包含或逆方向。
3. `coordinate_eq_of_kernel_on`：若 x-y∈K、核包含在 K 上有效、x/y 的选定行
   取值相同，则 coordinate(x)=coordinate(y)。关键是对差向量使用线性性。
4. `recover_on_domain`：给定物理候选域 D、D-D⊂K 的显式证明、参考状态∈D、
   参考状态满足相同 rhs 与已知 coordinate=value，恢复其他满足行方程的 x∈D。

不需要 X 有限维、矩阵可逆、行独立或 rhs=0；但不提供可行参考状态的存在性。
核包含本身只给坐标在纤维上唯一，若没有参考值或行组合 rhs，就不能凭空给出
数值坐标。s 为空也允许，此时相应前提依然必须成立，不能从空行恢复任意坐标。

## 域限制不是装饰

仅在原域 D 上知道 kernel 条件，并不足以把它用于 x-y。
精确例子：X=Real，D={1,2}，所有 row 都为零，coordinate=id。
D 上“row z=0 ⇒ coordinate z=0”并不成立，故不能充当合格证据。
更能区分差域的例子为 X=Real²，D={(1,0),(1,1)}，row(x,y)=x，
coordinate(x,y)=y：D 上 kernel 条件因 row≠0 而真，但两点 row 相同、coordinate
不同。它们的差 (0,-1) 不在 D，且违反 kernel 条件。这说明必须另给 D-D⊂K
及 K 上的核包含。上述例子为纸面精确说明，未作为 Lean 编译测试执行。

## Source 与 admission 边界

调用者必须绑定物理 X/嵌入、实际坐标线性性、source rows、选定行索引、rhs、
weight 或 kernel witness、原域及差域，并在有参数依赖时逐参数建立这些前提。
非线性物理状态可先提升为线性未知量，但提升关系与可实现性是额外外部义务。
不能将任意自由提升向量自动认作真实加速度或 DH state。

有限行求和只在证据索引上使用 Finset；不把源 CSV 的重复记录做去重 admission。
这里不存在 CSV/JSON 导入、source key 权威性、路径覆盖或 registry promotion。
核包含 ⇒ 行空间成员的逆向定理没有实现，也不借用未说明的维数/对偶性条件。

## Import 与检查风险

直接 imports 为 Mathlib.Data.Real.Basic、Mathlib.LinearAlgebra.Basic 与
Mathlib.Algebra.BigOperators.Group.Finset.Basic。候选仅用 rw、simp、有限和 congr/
zero、线性 map_sub 与 sub_eq_zero；无 linarith、inverse、decide/native_decide。
当前环境中的 Set/LinearMap 传递导入及 map_sub elaboration 未测试，故这
是最小化尝试，不是已确认的 import 闭包。后续可先检查两个有限和叶，再检查
差向量消去；Real 已显式导入，不依赖线性代数模块偶然提供它。

没有新增公理或占位证明；文本检查不替代完整依赖公理报告。只新增候选与本
review，不修改 state、registry、shared scripts 或构建配置。
