# Quotient CLM：two-definition repair candidate

状态 `OPEN_UNCOMPILED / pending`。没有运行本机或远程 Lean/Lake；没有编译、
elaboration、kernel/axiom 审计或 VERIFIED 结论。仅新增候选与本 review，旧文件、
toolchain、registry/state 不变。

## 精确范围

新 namespace FLTQuotientCLMAPIRepair 只有两个 def：
quotientContinuousLinearEquiv 与 quotientPiContinuousLinearEquiv。
每个声明自带完整参数与 typeclass binders；不依赖前一个 def 的参数作用域。
旧 sidecar 的 quotient_transport_mk 不复制、不声称已修复或已验证。
它引用未声明的 G/G'/H'/e/h，是 autoImplicit=false 下的独立风险；省略该额外
lemma 不删减本次要求的两个 quotient equivalence。

第一项保留 Ring、两侧 AddCommGroup/Module/TopologicalSpace、连续线性等价 e
及 mapped-submodule 等式。第二项保留 CommRing、每分量的 AddCommGroup/Module/
TopologicalSpace/IsTopologicalAddGroup、Fintype 与 DecidableEq。没有引入额外
正性、闭性或可逆矩阵假设，也没有删除有限性或双向连续性。

## 当前 pin 与最小 imports

本轮只读确认命名 checkout
artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib 的 HEAD 为
`0df444a360eaa60ab8c11dca51a86af692955474`，toolchain 文件为
`leanprover/lean4:v4.33.1`。没有调用 Lean executable 验证版本。

候选使用 LinearAlgebra.Quotient.Pi 与 Topology.Algebra.Module.Equiv 两个
targeted imports；证明体基于已有 FLTTransportPairingSmoke 的 current-pin
适配。旧 smoke 有四个 imports 且包含 pairing，所以它的历史通过记录不能
认证本文件的两模块闭包。`convert` tactic 的传递可用性、quotient lifting、
Submodule.quotientPi_aux.invFun 展开及 continuous_finsetSum 的显式类型参数，
是后续实际编译应优先检查的点。

若只是缺 tactic import，可在后续授权 repair 中显式引入对应模块；不能用
完整项目导入或加强数学前提来掩盖未识别的 API 错误。本轮不调整任何 pin。

## Provenance 与 attribution

来源为 Anthropic FLT commit `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef` 的
Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean，经当前本地 smoke
适配。其 upstream Mathlib 记录为 `db584cd6d46c92f209a44c0f1c829460d327499d`，
与目标 pin 不同。没有跨 pin statement comparator receipt。

本地 ATTRIBUTION.md 指明此文件整体源自 Imperial College London FLT staging
的 FLT/Mathlib/Topology/Algebra/Module/Quotient.lean：© 2025 Salvatore Mercuri，
authors Salvatore Mercuri, Kevin Buzzard, Pietro Monticone，Apache-2.0。
候选头保留 attribution 与修改说明；后续打包还须携带
artifacts/anthropic_fermats_last_theorem 下的 LICENSE、NOTICE 和 ATTRIBUTION.md，
不能仅依赖头部一句许可证名称。详尽 pin/字节 provenance 见同目录
NEW_QUOTIENT_CLM_PINNED_HANDOFF_20260908.md；本轮不改历史材料。

## 后续 handoff / admission

在独立授权的 pinned 环境编译此新模块，再单独 audit 两个完整限定名称：
FLTQuotientCLMAPIRepair.quotientContinuousLinearEquiv 与
FLTQuotientCLMAPIRepair.quotientPiContinuousLinearEquiv。
保存 source/import/manifest/OLean hashes、Lean/Mathlib pins、命令与 exit/log、
elaborated types 和 #print axioms；文本无 placeholder 不等于依赖无公理。

即使未来通过，只得到商空间的连续线性等价，不给 norm/isometry、正性、实际
domain/source identity、动力学下降、覆盖或 PDE 结论，不自动注册。
