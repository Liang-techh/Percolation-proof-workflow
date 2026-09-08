---
kind: review_result
review_id: R-FLT-DERIVATION-CALCULUS-SCAN-20260908T182536Z
task_id: T-FLT-DERIVATION-CALCULUS-SCAN-20260908
source_agent: Codex-FLT-calculus-interface-lane
created_at: 2026-09-08T18:25:36Z
inspected_commit: 268baa20cba8afd174fad79d3909a3cc47eb33d9
inspected_path: artifacts/anthropic_fermats_last_theorem
status: SOURCE_INSPECTED_NOT_COMPILED
integration_status: pending
admission_label: pending
registry_eligible: false
registry_promoted: false
lean_run: false
lake_run: false
kernel_checked: false
axioms_checked: false
comparator_accepted: false
requested_action: catalog_pending_metadata_only
---

# FLT derivation / calculus：非数论候选定点筛选

只新增本 immutable review；未复制实现或 proof body，未修改任何 Lean、registry、
state 或 shared adapter，未运行本机/远程 Lean/Lake。发布后的修订应另建 review_id。

起点是现有 `artifacts/task_FLT_calculus_derivation_20260908/{SOURCE_AUDIT.md,candidates.json}`
和 topology scan，以及 differentiable-coordinate adapter。随后只读取选定路径的
固定 Git blob。文件名检索曾因宽泛 pullback/continuous 关键词产生大量数论命中，
已缩为通用命名空间前缀；没有读取这些数论文件，也没有整仓内容扫描或构建。
未找到的 REPORT.md 是检索路径错误，不是 Lean 错误。

## 分类口径与建议

1 = exact 数学契约可直接消费；不等于目标环境已编译。
2 = 小范围 namespace/import/API 适配后值得尝试的通用候选。
3 = 对 Route-B 仅架构参考或前提不适用，不应生成 theorem receipt。
明确区分“通用代数/分析契约级别”和“Route-B 当前落地级别”。

| ID | exact 声明 | 通用契约 / 目标接线分类 | Route-B 优先级 |
|---|---|---|---|
| D1 | Algebra.PointDerivations.map、map_comp、map_id、map_apply_coe | 1 / 2；物理导数识别未供给 | 高：代数 observable derivative 的线性输出映射 |
| D2 | AlgebraicCurve.Differential.pullbackAlong_comp | 1（Kähler 范畴）/ 3（真实导数） | 低：generator/span-induction 证明结构 |
| C1 | ContinuousMap.ae_eq_zero_of_forall_mem_starSubalgebra_integral_mul_eq_zero | 2 | 中：完整测试代数下 residual 唯一性，非有限采样证书 |
| C2 | ContinuousMap.exists_continuous_monoidHom_forall_sum_eq_zero_of_compactSpace | 3（本轮仅 wrapper screening） | 低：紧交换群上的关系保持 character |
| A1 | Algebra.exists_bijOn_eval_differentiableOn_pi_of_smooth_of_kaehlerDifferential | 3 | 低：局部 chart 义务分解；不是 DH chart witness |

本轮不强行推荐“通用 Fréchet chain rule 来自 FLT”：已查 FLT 候选的 algebraic
differential 不是 HasFDerivAt。历史 Mathlib-only chain-rule sidecar 另有来源和证据，
不混进本次 FLT theorem provenance。

## D1：point derivation 的线性后复合

源 definition file：`Definitions/Def_Algebra_PointDerivations.lean`。
精确基础类型：k : Type u，A : Type v，Field k、CommRing A、Algebra k A，
ev : A →+* k，M : Type w，AddCommGroup M、Module k M。

`Algebra.PointDerivations k A ev M : Submodule k (A →ₗ[k] M)`，其成员定义**恰为**：
对所有 a b : A，D(a*b) = ev(a) • D(b) + ev(b) • D(a)。
这里 ev 是 RingHom，不是自动指定的 AlgHom；定义/map_comp 不额外假设
ev.comp(algebraMap k A) = RingHom.id k。

令 M' : Type w'、M'' : Type w（源 map_comp 的 M'' 与 M 共用 w），
各有 AddCommGroup 和 Module k：

- `map (ev) (φ : M →ₗ[k] M')` 的类型为
  `↥(PointDerivations k A ev M) →ₗ[k] ↥(PointDerivations k A ev M')`。
- `map_apply_coe ev φ D a`：`(map ev φ D : A →ₗ[k] M') a = φ (D.1 a)`。
- `map_id ev D`：`map ev (LinearMap.id : M →ₗ[k] M) D = D`。
- `map_comp ev φ ψ D`，ψ : M' →ₗ[k] M''：
  `map ev (ψ.comp φ) D = map ev ψ (map ev φ D)`。

source 同时有 mem_iff、apply_mul、apply_one、apply_algebraMap。
`ev_smul` **另需** hev : ev.comp(algebraMap k A) = RingHom.id k，不能把这个前提
错加到所有 map 定理，或在使用 ev_smul 时漏掉。

最小 Route-B adapter：选择具体实代数 A、ev_q、真实 derivative/jet D_q，先证明
D_q 的 k-linearity 和 evaluation-Leibniz law，再将固定线性输出 φ 后复合。
需要单独识别 D_q 与物理 observable 的导数；源不提供连续性、norm bound、
时变 φ 的导数项、FD remainder 或 flowpipe。特别地不能将 map_comp 当作
q-dependent coordinate change 的完整 chain rule。

实现适配范围：definition 小模块及其必要 algebra imports，独立 namespace；
源总 import Mathlib，最小传递 import closure 未验证。本轮没有移植代码。

## D2：Kähler pullback composition

源声明 `AlgebraicCurve.Differential.pullbackAlong_comp`，完整参数：
K F F' F'' : Type*；Field K/F/F'/F''；Algebra K F、Algebra K F'、Algebra K F''；
φ : F →ₐ[K] F'，ψ : F' →ₐ[K] F''，ω : Ω[F⁄K]。
结论精确为：

`pullbackAlong (ψ.comp φ) ω = pullbackAlong ψ (pullbackAlong φ ω)`。

依赖 definition 的 `pullbackAlong φ : Ω[F⁄K] →ₗ[K] Ω[F'⁄K]` 通过 φ 建立
algebraAlong/isScalarTower，再用 KaehlerDifferential.map 与 restrictScalars。
本条 composition **不需要** traceAlong 的 SeparableAlong 前提，不与 trace 分支混合。
源 generator law 为 pullbackAlong φ (D K F f) = D K F' (φ f)，
scalar law 为 pullbackAlong φ (f • ω) = φ f • pullbackAlong φ ω。
已读 solution 用 generator law、scalar law、span_range_derivation 和 span_induction；
不是实范空间中的链式法则。

Route-B 仅借鉴“先 generator 等式，再 span 扩张”的架构。
除非另证 chosen differential module 与物理 derivative 的识别和解析正则性，
不生成 DH/Poincare/trajectory theorem 节点。源 Field F 假设也不能直接套在一般
smooth-function algebra 上。

## C1：连续 residual 的零积分判别

完整声明：`ContinuousMap.ae_eq_zero_of_forall_mem_starSubalgebra_integral_mul_eq_zero`。
X : Type*，TopologicalSpace X、CompactSpace X、T2Space X、MeasurableSpace X、
BorelSpace X；μ : Measure X，IsFiniteMeasure μ；
A : StarSubalgebra ℂ C(X,ℂ)，hA : A.SeparatesPoints；β : C(X,ℂ)；
h : 对所有 f ∈ A，`∫ x, f x * β x ∂μ = 0`。
结论：`(β : X → ℂ) =ᵐ[μ] 0`。

积分假设原样是乘法 f*β，不是把假设改写成内积或仅要求有限 basis 正交。
star-subalgebra 的闭包提供 star β；已读 proof 先证明积分泛函连续，
用 Stone-Weierstrass 密度扩展到 star β，再从 norm-square 零积分推出 a.e. zero。

最小 Route-B adapter：明确 compact X、finite Borel μ、完整分点 star algebra A、
continuous residual β 和**所有**测试函数的精确积分恒等式；实 residual 可先明确
嵌入 ℂ 的接口并证明相应积分转换。
返回仅 a.e. zero，不是每点零、support 覆盖、矩阵 PSD、有限 Monte Carlo 或
有限模态截断误差证书；若需 pointwise，必须另给足够的测度 support 及连续性推论。
这是潜在 residual uniqueness 叶，不给定 Poincare 常数或强制性估计。

源四个 Mathlib imports：Topology.ContinuousMap.StoneWeierstrass、
MeasureTheory.Integral.Bochner.ContinuousLinearMap、MeasureTheory.Function.L2Space、
Analysis.RCLike.Lemmas。wrapper 另含 P2M.Util 和 solution import。
proof 的直接数学步骤未用 p2m tactic；可考虑独立 namespace/targeted imports 的轻改，
但 fun_prop、integral coercions、star/complex norm 等 API 仍须 pinned runner 检查。

## C2：紧交换群上的 character 保存所有有限关系

声明 `ContinuousMap.exists_continuous_monoidHom_forall_sum_eq_zero_of_compactSpace`：
G : Type*，CommGroup G、TopologicalSpace G、IsTopologicalGroup G、CompactSpace G、
T2Space G；f : C(G,ℂ)，hf : f ≠ 0；R : Set (G →₀ ℂ)；
hR : 对所有 r ∈ R 和 x : G，`r.sum (fun g c => c * f (x*g)) = 0`。
输出：存在 χ : G →* ℂˣ，Continuous χ，且对所有 r ∈ R，
`r.sum (fun g c => c * ((χ g : ℂˣ) : ℂ)) = 0`。

这里只读 exact wrapper，没有审核 solution/import 闭包；保持 3。
可参考周期配置群的 shift-relations/character 组织，但一般 Route-B phase space
不是紧交换群；没有范数误差界、unit-modulus 的显式结论、特定频率选择或轨迹绑定。
wrapper 的 `attribute [-simp] MeasureTheory.L2.kernelIntegralLM_apply` 也是 target
API/import 风险，不可视为小 import surface 已经成立。

## A1：复代数 evaluation chart

声明 `Algebra.exists_bijOn_eval_differentiableOn_pi_of_smooth_of_kaehlerDifferential`。
S : Type（源不是任意 Type u），CommRing S、IsDomain S、Algebra ℂ S、
**Algebra.FiniteType ℂ S**；hsm : Algebra.Smooth ℂ S；n : ℕ；
hrank : Module.rank S (KaehlerDifferential ℂ S) = n；
σ₀ : S →ₐ[ℂ] ℂ，t : Fin n → S；
hdt : (RingHom.ker σ₀.toRingHom) • ⊤ ⊔
Submodule.span S (Set.range (fun i => KaehlerDifferential.D ℂ S (t i))) = ⊤，
其中 ⊤ 是 Submodule S (KaehlerDifferential ℂ S)。

精确输出：存在 r : ℝ、U : Set (S →ₐ[ℂ] ℂ)，满足以下合取：

1. 0 < r 且 σ₀ ∈ U；
2. σ ↦ (i ↦ σ(t i)) 在 U 上 BijOn 到 Metric.ball (i ↦ σ₀(t i)) r；
3. 每个 s : S 都有 F : (Fin n → ℂ) → ℂ，在该 ball 上 DifferentiableOn ℂ，
   且所有 σ ∈ U 满足 σ(s) = F(i ↦ σ(t i))；
4. 每个 σ ∈ U 存在 fs : Finset S、ε : ℝ、0 < ε，使任意 σ' : S →ₐ[ℂ] ℂ
   若所有 s ∈ fs 满足 ‖σ'(s)-σ(s)‖ < ε，则 σ' ∈ U。

没有实 DH chart、inverse differentiability、Jacobian norm/Hessian bound 或 flow coverage。
现 `AnthropicFLTDifferentiableCoordinateAdapter.package_upstream_coordinate_conclusion`
额外接收 hSource : UpstreamCoordinateConclusion，仅打包已给结论；其签名也未保留
FiniteType 实例。不能将这个 packaging theorem 当作从 smooth/rank/hdt 推出 chart 的证明。
最小 Route-B 用途只是将 chart 存在、微分表达式、覆盖与逆映射义务分栏，保持 3。

## 不纳入实数 Route-B 的命中：正特征 derivation

`Derivation.add_mulLeft_pow_char`：R/F : Type u/v，CommRing R/F、Algebra R F，
p : ℕ、Fact p.Prime、CharP F p，d : Derivation R F F，a : F；结论为
`(d.toLinearMap + LinearMap.mulLeft R a)^p = d.toLinearMap^p +
LinearMap.mulLeft R (a^p + (d.toLinearMap^(p-1)) a)`。
虽是通用代数声明，但 CharP 与实/复 Route-B 不兼容；分类 3 / 不移植。
不得把这个 p 次幂恒等式用于 characteristic-zero Lie derivative。

## 固定 source/provenance manifest

共同源：`https://github.com/anthropics/fermats-last-theorem`；commit
`aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`；Lean v4.33.1；Mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d`。以下均为 git ls-tree 返回的 blob，
不是目标 candidate SHA 或 OLean hash。

| 路径 | Git blob |
|---|---|
| Definitions/Def_Algebra_PointDerivations.lean | a6a95f7e3170eb079c42c30deaa06a562d42f53d |
| Definitions/Def_AlgebraicCurve_DifferentialPushPull.lean | b31e104c520fae0dccaf9b5146c4893b057007fd |
| Theorems/Thm_AlgebraicCurve_Differential_pullbackAlong_comp.lean | 265374336a1293d80f7b816496e3c2c6b7f9a549 |
| P2M/Sol/S_AlgebraicCurve_Differential_pullbackAlong_comp.lean | f5be332dd3f8bc8580139ed8ad5a6153f4a7af72 |
| Theorems/Thm_ContinuousMap_ae_eq_zero_of_forall_mem_starSubalgebra_integral_mul_eq_zero.lean | df8dc832a4a2b82a578b78265b593bb2194ab329 |
| P2M/Sol/S_ContinuousMap_ae_eq_zero_of_forall_mem_starSubalgebra_integral_mul_eq_zero.lean | 77ed09d73bc76b3b9fd2e1a10ffa2b9fe5b1b88a |
| Theorems/Thm_ContinuousMap_exists_continuous_monoidHom_forall_sum_eq_zero_of_compactSpace.lean | 651ba38f7add1d4e51f3e6efdb86f9441f4a7bfc |
| Theorems/Thm_Algebra_exists_bijOn_eval_differentiableOn_pi_of_smooth_of_kaehlerDifferential.lean | 258acd99b2b98065e948b27f966c410b91c8a263 |
| Theorems/Thm_Derivation_add_mulLeft_pow_char.lean | 598b5012c4565398a1e77f9720fb2ccd9e7b67a1 |

来源归属：仓库 NOTICE 为 Copyright 2026 Anthropic, PBC / Apache-2.0，
并要求保留第三方 FLT/Mathlib ATTRIBUTION。对本次 D1、D2、C1、A1 精确路径的
ATTRIBUTION 文本检索未返回专门条目；不据此推断“无第三方贡献”或编造作者。
后续代码 intake 必须保留仓库 LICENSE/NOTICE/ATTRIBUTION 与所用 Mathlib 模块归属。
本轮没有复制代码，仅在 review 记录类型契约与来源。

## 证据、执行与 admission

实际检查：Get-Content 已有 scan/adapter；git show <fixed commit>:<selected path>；
git ls-tree 固定路径；rg 精确 attribution 名称。最后各组固定对象读取的 shell exit 0。
没有 compiler invocation、axiom output、new OLean、comparator run 或 candidate receipt。
existing SOURCE_AUDIT.md 所述 Mathlib-only 编译属于历史旁证，不能升级上述 FLT 候选。

建议只 intake D1/C1 为 pending 通用 API 候选，D2/C2/A1 保持 architecture-only 附注，
正特征条目注明不适用。未来若获授权，优先为 D1 做局部 import/API leaf，
为 C1 做完整类型/密度前提绑定；仍不可省略源 snapshot、目标 pin、import/axiom 审计。
本 review 不请求运行 integration 脚本，不请求新 theorem DAG 或 registry promotion。
