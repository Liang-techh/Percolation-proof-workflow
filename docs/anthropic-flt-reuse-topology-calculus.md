# Anthropic FLT：topology / calculus / transport 复用扫描

状态：只读扫描报告；不是 Lean build、定理验证、registry admission 或代码迁移。

扫描对象：`upstream/anthropic-fermats-last-theorem`。扫描重点为 calculus、derivation、topological/quotient、continuous map、transport/adapter；纯数论结论不列为复用候选。

## 1. Provenance 与边界

- upstream `HEAD`：`aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`，提交标题为 `Fermat's Last Theorem in Lean 4 (Lean 4.33.1, Mathlib v4.33.0)`。
- upstream 工具链：`leanprover/lean4:v4.33.1`；Lake 中 Mathlib revision 为 `db584cd6d46c92f209a44f1c829460d327499d`。
- 所列候选文件的当前工作树 blob 与上述 `HEAD` 对应 blob 一致；但 upstream 工作树整体不干净，扫描时约有 62,669 个 Git 状态条目，表现为大量已跟踪路径删除及未跟踪重建文件。因此下表的 provenance 绑定到“commit + 相对路径 + 当前文件 hash”，不能解释为一个干净 checkout 的可复现 build 结果。
- 未运行 upstream 全仓 Lean build、Comparator、Nanoda 或任何 registry/state 操作；本报告不宣称 `LEAN_VERIFIED`，也不将候选自动注册。
- 复用等级：
  - **直接复用（1）**：声明的抽象类型和目标 API 已接近 Route-B；仍须在目标仓库的 pinned 环境中做最小独立编译。
  - **轻度改造（2）**：可保留接口/证明骨架，但需替换标量、实例、命名或目标关系。
  - **仅架构借鉴（3）**：数学域或依赖过重；只能借鉴 proof seam、transport 结构或 adapter 组织，不能搬 theorem 作为 Route-B 结论。

## 2. 候选逐条审计

### 2.1 商空间与连续 map：优先级最高

| 等级 | 精确相对路径 | 符号 / 定理名 | 依赖风险 | 对 Route-B / P8 / P3 的适配价值 |
|---|---|---|---|---|
| 直接复用（1） | `Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean` | `Submodule.Quotient.continuousLinearEquiv`（约第 5 行）；`Submodule.quotientPiContinuousLinearEquiv`（约第 20 行） | 文件 `import Mathlib`；前者依赖 `continuous_quot_lift` 与商拓扑，后者还要求逐坐标 `AddCommGroup`、`Module`、`TopologicalSpace`、`IsTopologicalAddGroup`、`Fintype`、`DecidableEq`。若 Route-B 的 quotient 不是 `Submodule` 商，需先给出等价建模。 | 最适合把有限维误差/约束空间的商表示与坐标积表示连接起来。P8 可用于把 quotient-level flowpipe 映射回坐标产品；P3 可用于有限 cell 的商/积坐标适配。不能提供覆盖、残差或轨迹包含本身。 |
| 轻度改造（2） | `Definitions/Def_Mathlib_Topology_Algebra_ContinuousMonoidHom.lean` | `ContinuousAddEquiv.toIntContinuousLinearEquiv`；`ContinuousAddEquiv.quotientPi`；`ContinuousMulEquiv.piUnique`；`ContinuousMulEquiv.piEquivPiSubtypeProd`；`ContinuousMulEquiv.units_map` | 依赖上一文件；`quotientPi` 固定为 `ℤ`-线性化并要求有限指标及拓扑加群，`units_map` 需要拓扑单/群结构。Route-B 的实数向量/椭球/区间对象通常不能原样套用。 | 为 Route-B 的产品分块、坐标投影、子类型拆分提供轻量 adapter 形状。P8 的状态/扰动分块和 P3 的 cell 分解可借鉴；应先改成目标标量的 `ContinuousLinearEquiv` 或直接使用 Mathlib 的实数版本。 |
| 直接复用（1，低优先级） | `Definitions/Def_Mathlib_Topology_Bases.lean` | `TopologicalSpace.secondCountableTopology_of_countable_cover'`（约第 5 行） | 只证明可数开嵌入覆盖推出第二可数性；要求 `Countable` 指标、每块 `SecondCountableTopology`、`IsOpenEmbedding` 和全覆盖。它不是区间算术的 finite coverage lemma。 | 若未来 P3/P8 需要把 chart/cell 覆盖放进连续动力系统的拓扑层，可直接复用其覆盖接口；当前 numeric P3 coverage 不能由它关闭，P8 flowpipe 也没有因此获得。 |
| 轻度改造（2） | `Definitions/Def_Mathlib_Topology_Algebra_UniformRing.lean` | `UniformSpace.Completion.mapSemialgHom`；`mapSemialgHom_apply`；`mapSemialgHom_coe`（约第 6、26、32 行） | 依赖 UniformSpace completion、`IsTopologicalRing`、`IsUniformAddGroup` 和连续/一致连续 ring hom；与 Route-B 的 Euclidean interval arithmetic 并不相同。 | 如果把精确模型、完成空间或离散层级包装成 completion，提供“先证明连续 map，再 lift 到 completion”的 adapter 模板；P8/P3 仅有架构价值，不能替代 directed-rounding 或 enclosure 证明。 |

### 2.2 Derivation / calculus：可借鉴 seam，不可直接承接 PDE/ODE 结论

| 等级 | 精确相对路径 | 符号 / 定理名 | 依赖风险 | 对 Route-B / P8 / P3 的适配价值 |
|---|---|---|---|---|
| 仅架构借鉴（3） | `Definitions/Def_Algebra_PointDerivations.lean` | `Algebra.PointDerivations`（约第 9 行）；`PointDerivations.mem_iff`、`apply_mul`、`apply_one`、`apply_algebraMap`、`ev_smul`；`PointDerivations.map`、`map_id`、`map_comp`（约第 28–60 行） | 这是 algebraic point derivation：需要 `Field k`、`CommRing A`、`Algebra k A`、evaluation ring hom `ev` 和线性目标模块；`ev_smul` 另需 `ev.comp (algebraMap k A) = RingHom.id k`。它不是 `HasDerivAt`、时间导数或链式法则。 | Route-B 若将方向导数/端口残差编码成带 evaluation 的线性 map，可借鉴“predicate = Leibniz law + map functoriality”的接口；P8/P3 只能得到 adapter 组织启发，不能把 `apply_mul` 当作实际 DH/ODE derivative identity。 |
| 仅架构借鉴（3） | `Definitions/Def_AutomorphicForm_ArchDerivCasimirComplexAPI.lean` | `hasDerivAt_ofReal_mul_const`、`hasDerivAt_cexp_ofReal_mul_const`、`hasDerivAt_archFlowMatrixComplex_apply`；`IsArchSmoothAtComplex.archDerivAtComplex`、`differentiableAt_flow`；`archDerivAtComplex_add`、`archDerivAtComplex_smul`；`archDerivAtComplex_comp_mul_right/left`（约第 25–306 行） | 依赖 `Definitions/Def_AutomorphicForm_ArchDerivCasimirComplex.lean`，并进一步依赖 `ArchDirComplex`、复矩阵指数、`AdelicGL2`、`InfinitePlace.IsComplex` 和 `IsArchSmoothAtComplex`。导数只沿特定群流在 `t=0` 计算。 | 这是最清晰的“定义 flow → 证明 `HasDerivAt`/`HasFDerivAt` → 定义沿流 derivative → 证明 add/smul/translation compatibility”模板。P8 可借鉴将实际状态流的 chain-rule seam 单独封装；Route-B 可借鉴导数 identity 与动力学 map 解耦；P3 的静态 enclosure 不会因此得到 flowpipe 证明。 |
| 仅架构借鉴（3） | `Definitions/Def_AlgebraicCurve_ComplexLineIntegral.lean` | `Place.dCoordFn`、`Place.readDifferential`、`Place.IsPrimitiveAlong`、`pathIntegral`、`pathIntegral_def`、`pathPeriodLattice`（约第 19–97 行） | 依赖 `Place`、Kähler differential、复 chart/path；`IsPrimitiveAlong` 是 predicate，文件中的定义/展开不足以证明目标系统的 fundamental theorem of calculus 或轨迹积分界。 | 可借鉴“路径参数化、被积对象、primitive predicate、积分输出”分层。P8 若需从连续轨迹积分导出 storage budget，可参考这种分层，但必须在 Route-B 重新证明绝对连续性、chain rule、可积性和误差界。 |
| 仅架构借鉴（3） | `Definitions/Def_AlgebraicCurve_CellDissection.lean` | `RadialRegion`（含 `hcont : Continuous r`）；`RadialRegion.K`、`Kint`、`arcIcc`、`arcSet`；`Cell.carrier`、`interior'`、`arc`；`CellDissection.skeleton`（约第 11–150 行） | 依赖复平面 chart、`Place`、路径和前一行积分模块；`K`/`Kint` 是特定径向几何，不是 Route-B 的 rectangular/ellipsoidal box。 | 可借鉴 cell/interior/boundary/skeleton 的几何分层，以及将 chart map 与 coverage 证据分开。P3 可借鉴 cell 边界 bookkeeping；P8 可借鉴 flowpipe 分片的结构，但不能把 `Continuous r` 或 cell 定义当作全域覆盖。 |
| 仅架构借鉴（3） | `Definitions/Def_AlgebraicCurve_LogDeRhamH1.lean` | `logForms`、`LogDeRham.cocycles`、`coboundaries`、`H1.mk`；`pullbackForm`、`pullbackForm_D`、`pullbackPair`、`H1.map`、`H1.map_mk`（约第 100–289 行） | 依赖 `Ω[F⁄K]`、`Derivation`、场扩张、valuation/pole 条件和 quotient `H1`；文件后半还引入 characteristic-`p` Frobenius/Cartier。`pullbackForm_D` 是 Kähler derivation transport，不是实分析 chain rule。 | 对 Route-B 最有用的是“先在 carrier/cocycle 层证明 map 保持 predicate，再通过 quotient 的 `mkQ` 定义 map，并单独给出 `map_mk`”。P8/P3 可将其作为 witness quotient 或 certificate equivalence 的 proof architecture；不得复用其数学结论。 |

### 2.3 Transport / adapter：证明关系保持后再过 quotient 或 inverse limit

| 等级 | 精确相对路径 | 符号 / 定理名 | 依赖风险 | 对 Route-B / P8 / P3 的适配价值 |
|---|---|---|---|---|
| 仅架构借鉴（3） | `Definitions/Def_AdicCompletionRingFunctoriality.lean` | `levelMapₐ`、`levelMapₐ_mk`、`factorPow_levelMapₐ`、`levelMapₐ_id`、`levelMapₐ_comp`、`levelMapₐ_surjective_of_surjective`；`mapₐ`、`evalₐ_mapₐ`、`mapₐ_of`、`mapₐ_id`、`mapₐ_comp`；`levelEquiv`、`mapₐ_bijective`（约第 21–209 行） | 依赖 `Definitions.Def_PolynomialCompletion`、Ideal powers、`AlgHom`、有限层 quotient 和 completion lift。Route-B 的 nested boxes/interval leaves 不是 adic completion，不能按名称匹配。 | 很适合借鉴“level map → transition compatibility → inverse-limit lift → evaluation theorem → id/comp congruence”的 adapter DAG。P8 可对应多层 flowpipe enclosure 的 refinement map；P3 可对应 cell refinement 的 restriction map；但必须在目标对象上重新证明 coverage/refinement 关系。 |
| 仅架构借鉴（3） | `Definitions/Def_AdicCompletionRestrictScalars.lean` | `levelRestrictScalarsEquiv`、`levelRestrictScalarsEquiv_mk`、`transitionMap_levelRestrictScalarsEquiv`、`restrictScalarsEquiv`、`restrictScalarsEquiv_of`、`restrictScalarsEquiv_symm_of`（约第 13–64 行） | 依赖 `AdicCompletion.Algebra`、submodule quotient、scalar restriction 和 transition map；没有一般拓扑连续性或 interval semantics。 | 可借鉴“每层先构造等价，再证明 transition square commute，最后组装全局等价”的 transport/adapter 结构。对 P8 的坐标/标量变换和 P3 的 exact-vs-runtime coefficient seam 有启发，但不是直接 theorem。 |
| 仅架构借鉴（3） | `Definitions/Def_NumberField_PlaceTransport.lean` | `transport_apply`、`transport_coe`、`continuous_transport`、`valued_transport`、`transport_mem_adicCompletionIntegers_iff`（约第 20 行以后） | 依赖 number-field `HeightOneSpectrum`、valuation、adic completion、代数自同构；`continuous_transport` 的连续性来自 valuation/uniformity 事实。 | 这是“等式/共轭关系 → transport map → coe/value compatibility → continuity”链条的直接样例。P8 可借鉴先证明 invariant/value compatibility 再证连续；P3 可借鉴 transport 后的 enclosure predicate 保持，但实数 box/ellipsoid 需重写。 |
| 仅架构借鉴（3） | `Definitions/Def_AlgebraicCurve_CurveModelTransport.lean` | `functionFieldHomOfIso`、`functionFieldIsoOfIso`；`closedPointsEquivOfIso`；`CurveModel.transport`、`transport_ffEquiv`、`transport_placeOfPoint`、`transport_pointEquivPlace`（约第 24–216 行） | 依赖 Scheme、generic point/stalk、`IsIntegral`、`IsProper`、`SmoothOfRelativeDimension`、function field 和 closed points；transport 定义中有大量隐含 instance 负担。 | 可借鉴“从底层 isomorphism 构造 carrier map，证明 canonical maps commute，再给 transport object 的 simp/API”。P8/P3 仅可借鉴 canonicalization 和 provenance-preserving coordinate change；不能移植 scheme theorem。 |
| 仅架构借鉴（3） | `Definitions/Def_AlgebraicGeometry_RigKerDualNumberBaseTransport.lean` | `BaseTransport.specMap_comp_specMap`、`idOver`；`RigidifiedLineBundle.pullbackAlong_*`；`baseTransportCarrierIso`、`baseTransportCarrier`、`baseTransport`；`baseTransport_mk`、`baseTransport_mul`、`baseTransport_one`（约第 20–241 行） | 依赖 Scheme base change、monoidal pullback、rigidified line bundle、dual numbers，以及 quotient relation 的 `Quotient.map`/`Quotient.sound`。这是最重的 adapter 依赖之一。 | 对 Route-B 很有价值的只是标准 seam：先做 carrier-level iso，再证明 relation preservation，最后定义 quotient map，并提供 `*_mk`/operation compatibility。P8 可用于 certificate quotient transport；P3 可用于把 leaf witness 的等价关系 transport 到另一坐标层。数学域本身不可直接复用。 |
| 仅架构借鉴（3） | `Definitions/Def_AlgebraicCurve_PlaceCompletion.lean` | `kw_ffgc_uniformContinuous_withValMapAlgebraMap`；`kw_ffgc_adicCompletionComap`；`kw_ffgc_continuous_adicCompletionComap`；`kw_ffgc_continuousSMul_adicCompletionComap`（约第 70、114、122、307 行） | 依赖 valuation subring、Dedekind domain、adic completion、divisor/push-pull 和 finite-dimensional field extension；文件导出的连续性是非 Archimedean completion 语境。 | 可借鉴“先证 uniform continuity，再得到 completion map 连续，再把 scalar action 连续化”的层级。P8/P3 只有 proof-plumbing 价值，不能替代实数连续流、区间 enclosure 或 directed rounding。 |

## 3. 结论与建议的最小 acquisition 顺序

1. 先只取得 `Def_Mathlib_Topology_Algebra_Module_Quotient.lean` 的两个 quotient-continuous API；在目标环境中以一个最小 real finite-dimensional quotient 例子验证 typeclass 和商拓扑假设。
2. 如需有限积/坐标分块，再取得 `Def_Mathlib_Topology_Algebra_ContinuousMonoidHom.lean` 中的 `ContinuousAddEquiv.quotientPi` 证明形状，但优先改写成目标标量的 `ContinuousLinearEquiv`，避免无意引入 `ℤ`-module。
3. 对 calculus seam，参考 `ArchDerivCasimirComplexAPI` 的 flow/`HasDerivAt`/smoothness 分层；不要取得其 `AdelicGL2`、复矩阵或 automorphic-form 域。
4. 对 quotient adapter，参考 `LogDeRhamH1` 与 `RigKerDualNumberBaseTransport` 的 carrier-preservation → quotient-map → `map_mk`/operation-compatibility 顺序；Route-B 仍需独立证明实际 DH dynamics、storage derivative、coverage 和 flowpipe。
5. `AdicCompletionRingFunctoriality` 只在未来确实采用多层 refinement/inverse-limit 对象时再作结构参考；不能仅凭 `levelMapₐ_comp` 类似命名认定它适用于 P3/P8。

当前建议的实际复用集仅限：

- quotient continuous equivalence：`Submodule.Quotient.continuousLinearEquiv`、`Submodule.quotientPiContinuousLinearEquiv`；
- 可数开覆盖的纯拓扑接口：`TopologicalSpace.secondCountableTopology_of_countable_cover'`（低优先级）；
- 其余列为轻改造或架构借鉴，不能作为 Route-B/P8/P3 的已证明输入。

## 4. Provenance、Apache attribution 与 admission 注意事项

- upstream `formalization.yaml` 和 `NOTICE` 将项目标为 Apache-2.0；仓库还包含 Mathlib、Imperial College London FLT 和 flt-regular 的第三方来源。下游若复制源码、proof block 或非平凡结构，不应只记录“来自 Anthropic FLT”，还要保留源 commit、相对路径、符号范围、Lean/Mathlib pin 及适用许可证。
- `ATTRIBUTION.md` 明确列出的本扫描相关第三方文件包括：
  - `Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean` → `FLT/Mathlib/Topology/Algebra/Module/Quotient.lean`，作者列为 Salvatore Mercuri、Kevin Buzzard、Pietro Monticone；
  - `Definitions/Def_Mathlib_Topology_Algebra_ContinuousMonoidHom.lean` → `FLT/Mathlib/Topology/Algebra/ContinuousMonoidHom.lean`，作者列为 Salvatore Mercuri、Kevin Buzzard；
  - `Definitions/Def_Mathlib_Topology_Algebra_UniformRing.lean` → `FLT/Mathlib/Topology/Algebra/UniformRing.lean`，作者列为 Kevin Buzzard、Salvatore Mercuri；
  - `Definitions/Def_Mathlib_Topology_Bases.lean` → `FLT/Mathlib/Topology/Bases.lean`，作者列为 Kevin Buzzard；
  - quotient 基础辅助文件 `Definitions/Def_Mathlib_RingTheory_Ideal_Quotient_Basic.lean` → `FLT/Mathlib/RingTheory/Ideal/Quotient/Basic.lean`，作者列为 Salvatore Mercuri、Kevin Buzzard。
- 上述 `Def_Mathlib_*` 文件的复用应携带 Imperial FLT/Mathlib 的 Apache notice；若复制的只是接口思想而非源码，仍应保存 provenance 记录，避免把“架构借鉴”误记为原创或直接 theorem 复用。
- `ATTRIBUTION.md` 没有对本报告其余所列文件给出同名逐文件第三方行；这只能说明当前 attribution 表未列出该精确文件，不能证明所有 imports 或局部 proof 都无第三方来源。任何实际复制前仍需检查目标版本的 `NOTICE`、`ATTRIBUTION.md`、文件头和相似代码来源。
- Apache-2.0 允许在满足许可证、版权和 notice 条件下修改和再分发，但不授予把上游 theorem 的数学假设、域、边界条件、正则性或 normalization 自动迁移到 Route-B 的许可。许可证合规与数学 admission 是两条独立边界。
- Route-B 当前的 provenance/registry policy 仍应 fail-closed：候选源码、目标 statement、hash、toolchain/mathlib pin、依赖/axiom 报告和最小编译证据齐全前保持 pending；“上游已 machine-checked”不等于本地目标已编译或 P8/P3 已关闭。

## 5. 非候选项

未将 FLT 的 Frey curve、modularity、Galois representation、Hecke、Kummer、regular-prime 或其他纯数论 theorem 纳入 Route-B/P8/P3 复用集。它们即使是 upstream 的正式 Lean 结论，也不对应当前动力学、连续 map、商空间、导数 identity、interval coverage 或 flowpipe obligation。
