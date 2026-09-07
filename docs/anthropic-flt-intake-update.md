# Anthropic FLT intake catalog update

本次 intake 只扩展声明级候选，不写入 `state` 或 registry，也不把静态扫描结果标为 verified。
依据已提交的线性代数/连续算子扫描报告，最高价值且非数论的候选为：

| classification | 声明 | source path / lines | 复用边界 |
|---|---|---|---|
| 1 | `Module.continuous_bilinear_of_finite_free` | `Definitions/Def_Mathlib_IsModuleTopology.lean:147-165` | 有限自由双线性连续性；须在目标 pin 上声明级重编译。 |
| 2 | `IsModuleTopology.continuousLinearEquiv` | `Definitions/Def_Mathlib_IsModuleTopology.lean:362-375` | 模块拓扑 staging adapter；须协调目标已有 class/instance。 |
| 1 | `Submodule.Quotient.continuousLinearEquiv` | `Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean:5-18` | 子模商的连续线性 transport；不提供 flowpipe 或覆盖。 |
| 1 | `Submodule.quotientPiContinuousLinearEquiv` | `Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean:20-37` | 有限指标积商 transport；保留 `Fintype`/拓扑加群契约。 |
| 1 | `ExtPushout` (`extPushoutRel`, `mk`, `inl`, `inr`, `proj`, `lift`, `hom_ext`) | `Definitions/Def_LinearMap_ExtPushout.lean:12-129` | 纯模块 pushout/quotient；按整段最小摘取并重命名。 |

分类含义固定为：1 是声明接口足够通用、只等待当前环境编译；2 是需要轻量 API/class/namespace 适配后再编译；3 是 architecture-only，不登记为通用定理。`P2M/Util.lean` 保持 classification 3，仅借鉴 statement/proof-solution 分层与 elaboration 工具的架构。

每个候选都绑定扫描时的 `source_commit`、相对 `source path`/行段、Lean toolchain 与 Mathlib revision。当前快照为
`aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`，Lean `4.33.1`，Mathlib `v4.33.0`，manifest revision
`db584cd6d46c92f209a44c0f1c829460d327499d`。`Def_Mathlib_*` 是 FLT staging 源，不应描述成 Mathlib 原文；需保留 Anthropic/FLT attribution。

所有候选的 `admission_status` 均为 `pending`：静态路径、声明名、行段和 provenance 不是编译证据。只有在目标 Mathlib pin 上完成最小 probe/依赖闭包、核对 typeclass 与域假设，并经过显式 admission 流程后，才可讨论后续状态；本模块不会执行这些写入或 promotion。
