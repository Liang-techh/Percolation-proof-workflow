# Minimal row-space consumer with defect

状态 `OPEN_UNCOMPILED / pending`。未运行本机或远程 Lean/Lake，未声称编译、
kernel/axiom 验证或 VERIFIED。仅新增 companion candidate 与本 review。

候选导入已有 NEW_ROWSPACE_RECOVERY_20260908；不修改原候选，不重复 principal
restriction，不实例化 DH source，不修改 state、registry、共享脚本或构建配置。

## 最小 seam 与量词

以线性映射组合表达矩阵分解 L*Y=P，即 `L.comp Y=P`。观测约定为
`Y x=b+e`，故恢复恒等式是 `P x=L b+L e`；若使用 e=b-Yx 的另一约定，符号
必须相应改变，不能混用。

四个声明位于 RouteBP4RowspaceMinimalConsumer：

- recover_with_defect：固定 L 的精确加性恢复。
- exists_uniform_recovery：从 ∃L,L.comp Y=P，推出 ∃同一个 L，对所有 x,b,e
  满足观测关系均可恢复；不会把 ∀x∃L 偷换成 ∃L∀x。
- coordinate_defect_bound：给定同一个 L 上的 |coordinate(L e)|≤delta，推出
  |coordinate(P x)-coordinate(L b)|≤delta。
- finite_coordinate_defect_bound：X=Real^n、观测=Real^m、输出=Real^k，逐输出
  坐标恢复并消费 |(Le)_i|≤delta_i；零维空间也未排除。

这里不计算 L，也不从行 rank、核包含或数值消元自动提取 L。旧候选负责行组合/
核恢复层；新 consumer 只消费显式因子分解。这两个层之间的 witness 仍需外部
提供，不能因 import 旧候选就宣称已经构造。没有矩阵逆或 Schur complement。

## defect 界与 source/domain 边界

存在 L 不给出任何放大率。标量 Y=epsilon、P=1、L=1/epsilon（epsilon≠0）
满足 LY=P，但观测 defect e 被放大成 e/epsilon。故 |e|≤delta 不能直接代替
|Le|≤delta；需要同一 L 的系数界/算子范数界及匹配范数。

可在后续具体有限矩阵 witness 下证明 |(Le)_i|≤Σ_j |L_ij| epsilon_j；本轮
没有形式化该额外不等式，也不把有限矩阵的 entries 与 LinearMap 自动绑定。
finite consumer 中矩阵尺寸只是标准基解释；实际 `Matrix.mul` 到 `.comp` 的
桥接没有实现，避免引入不必要 API。

所有定理是对线性空间上的查询点成立的代数条件式，不构造物理 X、source rows、
domain membership、观测数据权威性、noise/remainder 估计或路径覆盖。应用时
必须在同一 source/domain 上提供 hFactor、hObs、hError；物理映射或控制参数
依赖需要逐实例绑定。global hFactor 是强前提，域上点态等式不能自动冒充它。

## import / repair 风险

直接只有 `import NEW_ROWSPACE_RECOVERY_20260908`；其传递 imports 包括 Real、
LinearAlgebra.Basic 与 Finset 求和模块。新 consumer 自身只用 LinearMap.comp、
map_add、congrArg、函数逐点加法、add_sub_cancel_left 与绝对值界，未增加 tactic。
这不是最小闭包证明；导入旧候选意味着旧候选所有声明也须先通过 elaboration。

后续最小检查顺序：旧模块 → recover_with_defect → exists_uniform_recovery →
两个误差 consumer。重点检查 `.comp` 的函数应用归约与 Fin 函数逐点加法的
`change`。没有必要为此导入完整 Mathlib、使用 native_decide 或扩大数学假设。
若要彻底独立 smoke test，可未来授权拆出只含 Real/LinearMap 基础的叶；本轮
不创建第二份重复 API。任何通过声明仍需 pinned source/import/OLean/axiom
receipt，不能自动升级为 DH 或 registry 结论。
