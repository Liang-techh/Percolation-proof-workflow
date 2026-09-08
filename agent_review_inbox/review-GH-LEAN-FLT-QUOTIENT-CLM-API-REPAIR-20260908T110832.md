---
kind: review_result
review_id: review-GH-LEAN-FLT-QUOTIENT-CLM-API-REPAIR-20260908T110832
task_id: GH-LEAN-FLT-QUOTIENT-CLM-API-REPAIR
source_agent: codex-local
created_at: 2026-09-08T11:08:32-06:00
inspected_commit: 113ae2a079a29641b7e3c6906cf25100c01883da
artifact_path: examples/anthropic_flt_quotient_transport_sidecar/NEW_QUOTIENT_CLM_API_REPAIR_20260908.lean
artifact_sha256: 777d4ae6cd3fa60fb0f988f5b1e263e2cb07536f7ed83113f99aa102615e9e97
probe_path: examples/anthropic_flt_quotient_transport_sidecar/NEW_QUOTIENT_CLM_API_Probe20260908.lean
probe_sha256: 159ddb493ca734675fc6f211e021ca05addb3cb442e6dab5ef71e7c6bd8c936b
proof_status: OPEN_UNCOMPILED
integration_status: pending
admission_label: pending
proposed_integration_target: external_catalog_pending_only
compile_performed: false
registry_mutation: false
formal_certificate_allowed: false
---

# 两个 quotient CLM 的隔离 probe / GitHub handoff

仅新增上述 probe 与本 review。没有修改旧候选、state、registry 或 shared
adapter，没有运行 Lean/Lake、workflow 或 registry/catalog integrator。
候选或 probe 后续通过也只供 external catalog pending，不自动标 VERIFIED。

## 静态类型核对

本轮重读原候选并通过 git show 读取 Anthropic 快照
aa2d8b34692b16c70f699536de0d8e75b9a3e9ef 中
Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean 的两个定义。
手工逐项核对以下 binders 一致；没有运行跨 pin statement comparator。

| 原接口 | 候选保留的前提 |
|---|---|
| Submodule.Quotient.continuousLinearEquiv | {R}, Ring R；显式 G/H；AddCommGroup、Module R、TopologicalSpace；显式 G'/H'/e/h，其中 e:G≃L[R]H，h:map e G'=H' |
| Submodule.quotientPiContinuousLinearEquiv | {R,ι}、CommRing R、依赖族 {G}；各分量 AddCommGroup/Module/TopologicalSpace/IsTopologicalAddGroup；Fintype ι、DecidableEq ι；p:Πi,Submodule R(G i) |

第一项不额外要求 topological additive group；第二项不能删除该条件或有限性。
候选所有变量均在各自 def 内显式声明，autoImplicit=false。旧文件的
quotient_transport_mk 未声明参数问题不在这个两定义候选内；probe 也不复制
该额外 lemma。两个 wrapper 各自拥有完整 binders，只消费已有定义。

## Probe 内容与边界

NEW_QUOTIENT_CLM_API_Probe20260908 导入候选，并用 checkQuotientType 与
checkProductType 将两项写成完整显式目标类型；#check @ 两个原定义，
#print axioms 两个原定义与两个 wrapper。
它不创建实际 G'/H'/e/h 或 p 的物理实例，不证明商空间对应真实约束域。
连续线性等价不蕴含 isometry、norm 常数、闭性/完备性、正性、动力学或覆盖。

## Import 与 target pin

命名目标 checkout 的当前 git HEAD 再次读为
0df444a360eaa60ab8c11dca51a86af692955474；候选目标 Lean v4.33.1。
这不是 executable/version 或 compiled proof 的运行证据。
候选仅直接导入 Mathlib.LinearAlgebra.Quotient.Pi 和
Mathlib.Topology.Algebra.Module.Equiv；本轮确认该 checkout 两个源码文件存在，
并读取它们的直接 public imports。没有穷尽验证传递 tactic/实例闭包。

未测试的重点：continuous_quot_lift/Continuous.quotient_lift、
Submodule.quotientPi_aux.invFun 的可展开性、continuous_finsetSum 的显式参数、
convert tactic 的传递可用性、dependent Pi 的加法拓扑实例。旧四-import smoke
的历史成功不证明此二-import 文件通过；发生错误须保留准确日志，不能以升级
pin、扩大前提或追加 sorry 来修复。只缺明确 tactic import 时，可另申请新 repair。

## Apache / provenance

候选头保留 Imperial College London FLT staging 路径
FLT/Mathlib/Topology/Algebra/Module/Quotient.lean，经 Anthropic 快照转入本地。
本轮核对本地 ATTRIBUTION.md:53：© 2025 Salvatore Mercuri，authors
Salvatore Mercuri、Kevin Buzzard、Pietro Monticone。不是纯数论搬运，也不把
第三方 attribution 简化为 Anthropic 独有。
后续隔离包携带 artifacts/anthropic_fermats_last_theorem 下 LICENSE、NOTICE、
ATTRIBUTION.md 与候选修改说明；保留 upstream Mathlib db584cd... 与 target
0df444... 的区别。Git blob/pin/notice 详见已有 handoff，本轮不修改它。

## GitHub agent 的精确检查入口（未执行）

1. 显式 checkout 候选/probe 所在 Git SHA，或导入带上述 SHA256 的 overlay。
   inspected HEAD 不是文件已提交证明。固定 Lean v4.33.1、Mathlib 完整 revision，
   锁住依赖及 GitHub actions SHA；不要用本地 path dependency 猜测远端布局。
2. 建立隔离包，获取匹配 pin 的 Mathlib build/cache。将两个源以原模块名放在
   包根，创建独立 out 目录，把它加入 LEAN_PATH；保留 Lake 提供的依赖路径。
3. 仅执行两个模块的编译，不引入 pairing/数论或主工程构建：

```text
lake env lean -DwarningAsError=true -o out/NEW_QUOTIENT_CLM_API_REPAIR_20260908.olean NEW_QUOTIENT_CLM_API_REPAIR_20260908.lean
lake env lean -DwarningAsError=true -o out/NEW_QUOTIENT_CLM_API_Probe20260908.olean NEW_QUOTIENT_CLM_API_Probe20260908.lean
```

第一条生成的 OLean 必须是第二条实际解析到的模块；不接受旧本机同名 OLean。
out/LEAN_PATH/setup 是前置条件，以上命令不自动完成 pin 安装或目录创建。
4. 返回 source/probe SHA、实际 Lean --version、Mathlib checkout/lock hashes、
   完整 command/cwd/search paths、exit 与日志 URL/hash、两个 OLean hashes、
   @ 类型输出及四个 axioms 输出。若额外公理/sorryAx/哈希不符，明确拒绝；
   缺证据保持 pending。不要把文本无 placeholder 当作 kernel axiom 审计。
5. source statement comparator 与应用域/实例验证单列，编译通过仅记录
   compiled candidate in external catalog pending；本轮不写 external catalog。
