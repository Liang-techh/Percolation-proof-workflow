# Anthropic FLT：线性代数与连续算子复用扫描

扫描对象：`C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropic-fermats-last-theorem`。
本报告只做静态源文件扫描；没有运行全仓 `lake build`，没有修改目标仓库的
`state`、registry 或任何 Lean 源文件。

## 结论摘要

- 最值得抽取的是 `Definitions/Def_Mathlib_IsModuleTopology.lean`：它给出
  `LinearEquiv` 到 `ContinuousLinearEquiv` 的有限维/模块拓扑桥、有限自由模块双线性连续性、
  标量改变和有限维坐标 homeomorph。对 PDE/算子仓库，建议按声明级别复用，而不是整文件复制。
- `Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean` 的两个商空间传输定义，
  以及 `Definitions/Def_Mathlib_RightActionInstances.lean` 的 `LinearMap.baseChange` /
  `LinearEquiv.baseChange`，是干净的线性传输工具。
- `Definitions/Def_ArtinL_EulerFactor.lean` 中的 `charpolyRev` 块是真正有限维线性代数，尤其
  `charpolyRev_conj` 可用于相似变换不变量；但文件的 namespace 和后半段是 Artin L 函数语境，
  应按最小行段改名后抽取。
- 没有发现与数论无关、可直接提供一般 `spectrum`/`eigenvalue`/`eigenspace` 理论的本地模块。
  `LanglandsTunnell...SpectralOperators3` 只是把特定 L² 子空间上的算子集合打包，适合作为架构
  借鉴，不应当登记为通用谱定理。

## 版本、快照与依赖基线

目标快照的 git remote 是
`https://github.com/anthropics/fermats-last-theorem.git`，当前提交为
`aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`。仓库声明的工具链是 Lean `4.33.1`，Mathlib
是 `v4.33.0`，manifest 固定到
`db584cd6d46c92f209a44c0f1c829460d327499d`。下文的行号均针对该快照。

这些候选源文件大多写成 `import Mathlib`，所以“依赖”首先表示源码中的声明依赖，而不是已经
验证过的最小 Mathlib import 集。真正落地时应在目标仓库建立一个只含候选声明的 probe 文件，
再把 umbrella import 缩小；本扫描没有以成功 build 代替该验证。

仓库的 `ATTRIBUTION.md` 与 `NOTICE` 还特别说明：`Def_Mathlib_*` 是 Imperial College London
FLT 项目的 staging 文件，不等同于 Mathlib 原文件；相关行段应同时保留 Anthropic 快照、FLT
源路径、上游作者/许可证和 Mathlib revision provenance。仓库总体许可证为 Apache-2.0。

## A. 直接复用候选

这里的“直接复用”是指声明的数学接口已足够通用，目标项目只需满足相同 typeclass 契约；仍需
在目标 Mathlib pin 上做一次声明级编译确认。

| 来源与最小摘取范围 | 声明/定理 | 契约与可复用内容 | 源码依赖与 provenance 建议 |
|---|---|---|---|
| `Definitions/Def_Mathlib_IsModuleTopology.lean:147-165` | `Module.continuous_bilinear_of_finite_free` | 对有限自由 `A`，把 `A →ₗ[R] B →ₗ[R] C` 传成 `Continuous (fun ab => bil ab.1 ab.2)`；适合有限模态/坐标空间中的连续双线性项。要求 `IsTopologicalSemiring R`、两个模块的 `IsModuleTopology`。 | 源文件只显式 `import Mathlib`；符号依赖 `Module.Free/Finite`、`Module.Basis`、`continuous_bilinear_of_pi_fintype`。provenance：保留 Anthropic path/commit，并回指 `ATTRIBUTION.md` 所列 `FLT/Mathlib/Topology/Algebra/Module/ModuleTopology.lean`。 |
| `Definitions/Def_Mathlib_IsModuleTopology.lean:257-285` | `moduleTopology.trans`、`IsModuleTopology.trans` | 在 `Module.Finite R S` 和 `IsModuleTopology R S` 下，证明 `moduleTopology R M = moduleTopology S M`，并给出两种标量拓扑的等价；这是有限标量扩张/限制下的拓扑 transport 核心。 | 依赖 `Algebra R S`、`IsScalarTower R S M`、有限性和 `continuous_bilinear_of_finite_left`。这是 FLT staging 内容，不能标成“Mathlib 原 theorem”；保存 FLT 上游路径与版本。 |
| `Definitions/Def_Mathlib_IsModuleTopology.lean:362-375` | `IsModuleTopology.continuousLinearEquiv`（全局短名 `continuousLinearEquiv`） | 任意 `A ≃ₗ[R] B` 在两端采用模块拓扑时，自动构造 `A ≃L[R] B`，正反向连续性均由线性连续性得到；是 ContinuousLinearMap/Equiv 的首选桥。 | 依赖 `IsModuleTopology.continuous_of_linearMap`、`ContinuousLinearEquiv`、`LinearEquiv`。建议只抽取该定义及其所需的 `IsModuleTopology` API，不复制后续 number-field 实例。 |
| `Definitions/Def_Mathlib_IsModuleTopology.lean:480-491` | `IsModuleTopology.Module.Basis.equivFun_homeo` | 对有限维 `K`-模块 `R`，构造 `R ≃L[K] (Fin (Module.finrank K R) → K)`；适合把有限维范数/连续估计搬到坐标空间，再显式处理坐标范数。 | 契约含 `Field K`、`Module.Finite K R`、两端 `IsTopologicalRing` 和 `IsModuleTopology K R`。依赖 `Module.finBasisOfFinrankEq` 与 `Module.Basis.equivFun`；先确认目标项目的 normed-space 实例与该旧接口是否仍匹配。 |
| `Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean:5-18` | `Submodule.Quotient.continuousLinearEquiv` | 若 `e : G ≃L[R] H` 把 `G'` 映到 `H'`，则得到 `(G ⧸ G') ≃L[R] (H ⧸ H')`；连续性通过 quotient lift 显式传递。适合商掉 kernel/边界空间后的线性 transport。 | 依赖 `Submodule.Quotient.equiv`、`continuous_quot_mk`、`continuous_quot_lift`。源码只 `import Mathlib`；可按该 14 行定义做独立 probe。 |
| `Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean:20-37` | `Submodule.quotientPiContinuousLinearEquiv` | 对有限指标族，给出 `((i : ι) → G i) ⧸ Submodule.pi univ p ≃L[R] ((i : ι) → G i ⧸ p i)`；是有限积商空间的连续线性 transport。 | 依赖 `Fintype ι`、`DecidableEq ι`、各分量 `IsTopologicalAddGroup`、`Submodule.quotientPi`。不要把 `Fintype` 放宽成任意无限积而不重做拓扑证明。 |
| `Definitions/Def_ArtinL_EulerFactor.lean:14-54` | `ArtinL.charpolyRev`、`charpolyRev_eq_reverse_charpoly`、`charpolyRev_toMatrix`、`charpolyRev_conj`、`charpolyRev_ne_zero`、`charpolyRev_mulVecLin` | 在 `[Field K] [FiniteDimensional K W]` 下，将 `LinearMap` 的 characteristic polynomial reverse 封装成 basis-independent API；`charpolyRev_conj` 给出 `e.conj T` 下不变，`charpolyRev_mulVecLin` 接回矩阵表示。适用于有限维谱/特征多项式不变量。 | 最小数学块只需 `import Mathlib` 的 `LinearMap.charpoly`、`LinearEquiv.charpoly_conj`、`Matrix.charpolyRev`、`LinearMap.toMatrix`；当前文件额外导入两个 Artin/变形文件是下游需要，不应随块复制。建议新 namespace（例如 `FiniteDimensionalOperator`），并把 `ArtinL` 名称与 L 函数定义分离。 |
| `Definitions/Def_LinearMap_ExtPushout.lean:12-129` | `LinearMap.extPushoutRel`、`ExtPushout`、`mk/inl/inr/proj`、`range_inl_eq_ker_proj`、`lift`、`hom_ext` | 纯模块论的 pushout/quotient 构造：给定 `p` 和 kernel 上的 `δ`，提供生成元、投影、泛性质和 kernel-range 识别；适合拼接有限维约束、消去 kernel 或构造边界商。 | 只依赖 `Mathlib`、`CommRing B`、`AddCommGroup`、`Module`；没有拓扑或数论假设。最小摘取应保留 `extPushoutRel` 到 `hom_ext` 的整段，因为 lift 泛性质依赖前面的 quotient API。 |

## B. 轻改后复用候选

这些声明本身通用，但命名空间、typeclass 或局部实例带有上游工程假设；建议复制数学结构并改名，
而不是把全局实例直接带入目标项目。

| 来源与最小摘取范围 | 声明/定理 | 需要的轻改 | 依赖与 provenance |
|---|---|---|---|
| `Definitions/Def_Mathlib_IsModuleTopology.lean:7-24,37-63` | `IsTopologicalModule`、`Topology.IsInducing.topologicalModule`、`IsBiscalar`、`LinearMap.changeScalars`、`LinearEquiv.changeScalars` | `IsTopologicalModule` 和 `IsBiscalar` 是上游自定义 class；若目标已有同义 class，应改成 adapter lemma，避免重复定义或 instance diamond。 | 依赖 `ContinuousSMul`、`ContinuousAdd`、`LinearMap`/`LinearEquiv`。`ATTRIBUTION.md` 将整文件指向 FLT ModuleTopology、Algebra/Tower 和 `IsTopologicalModule` 文件；应逐块记录而非笼统写“来自 Mathlib”。 |
| `Definitions/Def_Mathlib_IsModuleTopology.lean:377-431` | `continuousLinearEquivOfIsBiscalar`、`continuousAlgEquivOfIsBiscalar`、`continuousAlgEquivOfAlgEquiv` | 适合同一底层函数同时有两套 scalar action 的 transport；目标若已有 `NormedSpace`/`ContinuousLinearMap` 结构，应把 `IsBiscalar` 改成目标的 scalar-compatibility predicate。 | 依赖前述 `changeScalars` 和 `IsModuleTopology.continuous_of_linearMap`；保持 `continuousAlgEquivOfIsBiscalar_apply`（:411-418）作为 simp 边界。 |
| `Definitions/Def_Mathlib_RightActionInstances.lean:57-93,107-149,158-162` | `Algebra.TensorProduct.comm`、`Module.TensorProduct.comm`、`LinearMap.baseChange`、`LinearMap.baseChange_id`、`LinearMap.baseChange_comp`、`LinearEquiv.baseChange`、`Algebra.TensorProduct.basis` | 当前放在 `TensorProduct.RightActions` namespace，并安装 scoped `Module.Finite/Free` 与 topology instances；目标若只需要代数 transport，应只取 `baseChange`/`basis`，不要启用整组 scoped instances。 | 依赖 `TensorProduct.comm`、`LinearMap.baseChange`、`Module.Finite/Free`。这是 `ATTRIBUTION.md` 中的 `FLT/Hacks/RightActionInstances.lean` staging；保留该 provenance，并单独记录 scoped-instance 风险。 |
| `Definitions/Def_Mathlib_Topology_Algebra_ContinuousMonoidHom.lean:6-19` | `ContinuousAddEquiv.toIntContinuousLinearEquiv`、`ContinuousAddEquiv.quotientPi` | `ℤ`-线性结构和 `AddSubgroup.toIntSubmodule` 对 PDE 实数/复数空间通常不合适；可改成目标标量环的专用桥，或仅借用 quotientPi 的构造方式。 | 依赖 `Submodule.quotientPiContinuousLinearEquiv` 和 `IsTopologicalAddGroup`；文件额外依赖 `Def_Mathlib_Topology_Algebra_Module_Quotient`。 |
| `Definitions/Def_Mathlib_Topology_Algebra_RestrictedProduct_Equiv.lean:82-91,214-228,340-348` | `LinearEquiv.restrictedProductCongrRight`、`LinearEquiv.restrictedProductCongrLeft'`、`LinearEquiv.restrictedProductCongrLeft`、`LinearEquiv.restrictedProductCongr` | 目标若不是 restricted product，不应引入这些定义；可把“逐点 equiv + eventually maps-to + filter/index reindex”抽象成有限/可数 transport helper。文件中的 `#adaptation_note`（:137-139、:264-267）明确指出 `to_additive` 在 Mathlib 4.28 曾失败，当前版本需重新核对。 | 依赖 `RestrictedProduct.Basic`、Filter 的 map/comap、逐点 `LinearEquiv`；`TopologicalSpace` 版本还需额外导入 `...RestrictedProduct_TopologicalSpace`。provenance 回指 ATTRIBUTION 中的 FLT RestrictedProduct 三个文件。 |

## C. 架构借鉴，不建议直接注册为通用 theorem

| 来源与最小摘取范围 | 声明/定理 | 借鉴点 | 边界 |
|---|---|---|---|
| `Definitions/Def_Mathlib_MeasureTheory_Function_L2KernelOperator.lean:114-152,182-211` | `kernelIntegralLM`、`norm_kernelIntegralLM_apply_le`、`kernelIntegralₗ`、`kernelIntegralCLM`、`norm_kernelIntegralCLM_le`、`norm_kernelIntegralₗ_le` | 展示了先定义 algebraic `LinearMap`，再用显式 bilinear norm bound 构造 `→L`，最后把 operator norm bound 作为 API 的分层方式。对积分算子、PDE resolvent 或 Lyapunov operator 很有参考价值。 | 固定为 `Lp ℂ 2`、有限测度、Schur/Hölder 估计；这不是一般核算子 theorem，也不证明自伴、谱分解或有限维性。依赖 `MeasureTheory`、`Lp`、`ENNReal`、Hölder。 |
| `Definitions/Def_Mathlib_MeasureTheory_Function_L2KernelOperator.lean:455-464` | `isCompactOperator_kernelIntegralCLM`、`finiteDimensional_of_kernelIntegralCLM_eq_id` | 给出“核算子紧 + 等于 identity ⇒ 空间有限维”的反证/门槛模式；可作为无限维算子不可能性检查的架构。 | 结论依赖前面 `compactKernels_eq_top` 的完整 L² 紧性证明，不能把该两行单独摘成有限维 transport 事实。 |
| `Definitions/Def_LanglandsTunnell_CubicInduction_SpectralOperators3.lean:8-31` | `IsSpectralTranslation3`、`IsCuspLift3`、`spectralGenerators3`、`spectralOperators3` | 把“生成算子集合”和“伴随关系定义的闭包”分开，并把算子类型显式写成 `V →L[ℂ] V`；可借鉴为谱方法的 operator-family 数据结构。 | 所有类型绑定到 adelic `GL 3`、cuspidal subspace、特定 smoothing/translation；没有一般谱、eigenvector、compact-resolvent 或 self-adjoint theorem。 |
| `Definitions/Def_Deformations_MatrixRepresentation.lean:11-21` | `Deformation.matrixRepresentation`、`matrixRepresentation_apply` | 把 `G →* GL n k` 规范转为 `Representation k G (n → k)`，并通过 `Matrix.mulVecLin` 暴露作用；可用作有限维离散算子/群作用的表示层。 | 仅有有限指标 `n`、`Field k` 和 `Group G`，没有连续性、范数或谱结论；目标若研究 `ContinuousLinearMap`，需另加 boundedness/continuity 层。 |

## 谱、特征值与有限维范数传输的负筛选

1. `ArtinL.charpolyRev` 块是本仓库中最接近通用谱接口的内容，但它提供的是 characteristic
   polynomial reverse 及相似变换不变量，不是 `spectrum` 集合、eigenvalue 存在性或谱半径估计。
2. `LanglandsTunnell...SpectralOperators3` 的 “spectral” 只是领域命名；其 operator family
   依赖特定 cuspidal L² 空间，不能替代 Mathlib 的 self-adjoint/compact operator API。
3. `GoodReductionJacobian_NsmulEigenSubdatum` 等命中是层/截面上的 eigen 条件；
   `AlgebraicGeometry_DoubleComplex` 中的 `BoundedSpectralSequence` 是谱序列命题，均不属于线性
   算子谱理论，已排除。
4. 未观察到一个可从该仓库直接抽出的通用“有限维范数等价”“isometry ⇒ norm preservation”
   定理包。有限维范数传输应优先组合 Mathlib 现有 `ContinuousLinearEquiv`、
   `Module.Basis.equivFun`、`FiniteDimensional` 和目标项目自己的 norm 结构；不要从
   `Module.Basis.equivFun_homeo` 的拓扑连续性自动升级出等距或定量常数为 1。

## 建议的最小摘取顺序

1. 先做一个只导入 Mathlib 的 probe：`continuousLinearEquiv`、
   `Submodule.Quotient.continuousLinearEquiv`、`LinearEquiv.baseChange`、
   `charpolyRev_conj` 四组分别编译，记录目标 Mathlib pin 下的实际 import 和 namespace。
2. 若目标确实采用模块拓扑，再加入 `Module.continuous_bilinear_of_finite_free`、
   `moduleTopology.trans` 和 `Module.Basis.equivFun_homeo`；把 `IsTopologicalModule`/
   `IsBiscalar` 作为显式 adapter 层，不把所有全局实例复制过去。
3. 需要商空间时整段摘取 quotient 定义及其前置 `Submodule.Quotient` API；需要 kernel/边界
   pushout 时整段摘取 `ExtPushout` 的 `mk` 到 `hom_ext`，并在目标项目中重新命名 namespace。
4. 对谱路线只抽取 `charpolyRev` 的 14-54 行；保留 `Field`、`FiniteDimensional`、basis-independent
   共轭定理这三个 admission 条件。L² 核算子和 restricted product 仅作为设计参考，暂不纳入
   verified registry 或 theorem catalog。

## Provenance 与 admission 规则

- 每个摘取项至少记录：Anthropic 仓库 URL、快照 commit、仓库相对 path、精确行段、声明名、
  当前 Mathlib revision/toolchain、实际 probe 的 imports、上游 FLT 文件（若 `ATTRIBUTION.md`
  指明）、许可证和是否改名/改证明。
- `Def_Mathlib_*` 不应写成“Mathlib 原文直接复用”：本快照的 provenance 是 Imperial FLT
  staging 文件，且 `ATTRIBUTION.md` 明列了作者与对应 FLT 路径。只有 Mathlib API 本身才标为
  “依赖 Mathlib v4.33.0”；若重写证明，应标记为 adapted/reproved。
- `P2M/Sol/*` 和对应 `Theorems/Thm_*` 多数是带 `p2m_exact_reverting` 的领域证明包装；本扫描
  没有把它们当作可复用线性代数 theorem。不能因为 theorem 名称含 `finrank`、`norm` 或
  `continuousLinearEquiv` 就跳过其数论/几何前提。
- 本文的“直接复用/轻改/架构借鉴”是静态筛选，不是当前目标项目的编译或 registry admission
  结论；真正接纳仍需 source hash、依赖闭包、Mathlib pin 和目标域假设的单独验证。
