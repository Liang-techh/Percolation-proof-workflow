---
kind: review_result
review_id: R-FLT-AVERAGING-FOURIER-TOPOLOGY-SCAN-20260908T183253Z
task_id: T-FLT-AVERAGING-FOURIER-TOPOLOGY-SCAN-20260908
source_agent: Codex-FLT-spectral-topology-lane
created_at: 2026-09-08T18:32:53Z
inspected_commit: 855a2107de07a692fbeef1cb0af5061e219769a3
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

# 新增 FLT spectral / topology 入口：平均、Fourier、inducing、biscalar

本轮只新增此 immutable review。避开已完成的 P2M、quotient、derivation 和
既有 eigenspace-orthogonal theorem 复述；不复制实现，不修改 registry/state，
不运行 Lean/Lake 或远程编译。修订必须新增 review_id。

由现有 intake catalog 定点读取三个源文件（两个 theorem/solution 对与一个
definition 文件的选定段），而非整仓扫描。以下是 exact 源契约与适配判断，
不是新 theorem receipt。

## 分类

1 = exact 通用数学契约可直接消费；2 = 需要小范围 import/namespace/API 适配；
3 = 当前 Route-B 只可借鉴架构，或缺实质识别前提。
这些等级不是编译/准入等级；全体仍 pending、registry_eligible=false。

| ID | 声明 | generic contract / current-pin candidate | Route-B 当前边界 |
|---|---|---|---|
| S1 | ContinuousLinearMap.exists_forall_apply_eq_integral_smul_apply_of_forall_norm_le_of_continuous | 1 / 2 | 有条件 averaging leaf；实际 symmetry/projection 仍为 3 |
| F1 | AddChar.exists_continuousLinearMap_fourierChar_eq | 1 / 2 | 实向量空间 character 表示可用；环面 Fourier 识别仍为 3 |
| T1 | Topology.IsInducing.topologicalModule；Submodule/Pi instances | 1 / 2 | 传递 topology instances，不给物理域或范数界 |
| L1 | LinearMap.changeScalars、LinearEquiv.changeScalars | 1 / 2 | 双标量相容后重用同一映射；不自动是 continuous/isometric |

## S1：带权 representation 平均算子

完整声明名：
`ContinuousLinearMap.exists_forall_apply_eq_integral_smul_apply_of_forall_norm_le_of_continuous`。

参数/instances 原样保留：

- C : Type*，Group C、TopologicalSpace C、IsTopologicalGroup C、CompactSpace C、
  T2Space C、MeasurableSpace C、BorelSpace C；μ : Measure C，
  μ.IsHaarMeasure、IsProbabilityMeasure μ。
- H : Type*，NormedAddCommGroup H、InnerProductSpace ℂ H、CompleteSpace H。
- S : C →* (H →L[ℂ] H)，B : ℝ；hSb : ∀ c, ‖S c‖ ≤ B；
  hSc : ∀ v : H, Continuous (fun c => S c v)。这是逐向量强连续，
  不要改写成源要求 operator-norm continuous。
- w : C → ℂ，hw : Continuous w。

输出存在 A : H →L[ℂ] H，带**四项**合取：

1. ∀ v，A v = ∫ c, w c • S c v ∂μ；
2. ∀ M : ℝ，(∀ c, ‖w c‖ ≤ M) → ∀ v，‖A v‖ ≤ M * B * ‖v‖；
3. ∀ L : Submodule ℂ H，IsClosed (L : Set H) →
   (∀ c, L.map (S c : H →ₗ[ℂ] H) ≤ L) → L.map (A : H →ₗ[ℂ] H) ≤ L；
4. ∀ T : H →L[ℂ] H，(∀ c, T.comp (S c) = (S c).comp T) → T.comp A = A.comp T。

没有另给 B≥0/M≥0 参数；源 proof 由 norm bound 推导所需非负性。
C 不要求交换，H 不要求有限维，S 不要求 unitary，w 不要求 character。
**A 不因此必为 projection、self-adjoint、PSD、idempotent 或 spectral projector。**

已读 solution：构造 Bochner integral 线性映射，使用 compact weight bound 得到
连续性；用 closed-subspace double orthogonal 证明不变性；通过积分与 CLM 交换证明
commutation。源公开类型的 Haar/probability 条件应原样保留，即使部分 proof 步骤
可能只用有限测度，也不能在 intake 中静默弱化。

最小 Route-B adapter：明确 C、μ 的规范化、H 的复 Hilbert 表示、实际 S 与
uniform B、强连续证据、w，再接四项输出。若目标是实状态应另有 real/complex
识别；若目标是投影还需 w/S/measure 下的幂等和正交条件；若作用于 dynamics，
必须由真实算子提供 commutation witness。它不是 ODE 存在、DH、FD remainder
或矩阵残差界。优先级：可作为 symmetry-average 通用候选，不直接登记 P7 证书。

## F1：连续 additive character 的实线性表示

声明 `AddChar.exists_continuousLinearMap_fourierChar_eq`：
E : Type*，NormedAddCommGroup E、NormedSpace ℝ E；
χ : AddChar E Circle，hχ : Continuous χ；
输出 ∃ l : E →L[ℝ] ℝ，∀ x，χ x = 𝐞 (l x)，其中 𝐞 使用 scoped FourierTransform。

没有有限维、CompleteSpace 或内积前提；但必须是实赋范向量空间。
已读 solution 经 Circle.exp covering lift 得到连续加性实函数，再转 real CLM，
最后乘 (2*π)⁻¹ 与 Fourier character 约定对齐；不能丢掉这一 normalization。
公开结论只声明存在，不把证明中的 lift uniqueness 偷升级为公开 uniqueness theorem。

最小 Route-B adapter：在明确的 unwrapped real vector coordinates 上绑定连续
additive χ，再消费 l。AddCircle/torus 本身不是实向量空间；若需整数频率/周期
格点，必须先给 covering lift、lattice compatibility 和频率规范化，不可直接套用。
不产生 Fourier truncation、Krylov error、正交基完备性或动力学等价。

API 风险：wrapper 只显示两条 Mathlib imports，但 solution 还使用 covering map、
homotopy lifting、contractibility、locally-convex modules 等模块；需要核对实际
目标闭包，不可按 wrapper 的 import 数量宣称轻量或已经编译。

## T1：沿 inducing linear map 传递 topology structure

定义文件中的 `IsTopologicalModule R M` **自定义 class** 仅 extends
ContinuousSMul R M、ContinuousAdd M。不要与名字相近的 IsModuleTopology 混为一谈。

`Topology.IsInducing.topologicalModule` 的 exact 参数：
F : Type*；R : Type*，Ring R、TopologicalSpace R；
M : Type*，AddCommGroup M、Module R M、TopologicalSpace M、IsTopologicalModule R M；
H : Type*，AddCommGroup H、Module R H、TopologicalSpace H；
FunLike F H M、LinearMapClass F R H M；f : F，hf : Topology.IsInducing ⇑f；
输出 IsTopologicalModule R H。

此处不额外假设 f injective、IsEmbedding、surjective、IsTopologicalRing R，
也不能把仅 continuous f 冒充 inducing。结论不是 Hausdorffness 或 norm preservation。

伴随 instances：

- `Submodule.instIsTopologicalModuleSubtypeMem (S : Submodule R M)`：
  在上述 R/M ambient hypotheses 下返回 IsTopologicalModule R S；
- `Pi.instTopologicalModule`：ι : Type*，R 为带 topology 的 Ring；
  对每个 i，AddCommGroup (M i)、Module R (M i)、TopologicalSpace (M i)、
  IsTopologicalModule R (M i)；返回 IsTopologicalModule R ((i : ι) → M i)。
  **没有 Fintype ι 前提**；本条与先前 finite-product quotient 不同。

最小 Route-B adapter：证明指定坐标/约束空间 topology 确实由 f inducing，
或直接使用 submodule/product topology 的 instances。目标已有 class 是否冲突
未查编译；建议保留 namespace 或只消费 ContinuousSMul/ContinuousAdd 两个字段。
不整体导入整个 mixed-definition 文件，避免重复全局 class/instance 与标量 diamond。

## L1：IsBiscalar 保持同一函数的换标量

定义 `IsBiscalar (R S : Type*) (f : A → B)` 的前提：Semiring R/S，
AddCommMonoid A/B，Module R A/B，Module S A/B；字段：
∀ r a，f(r • a)=r • f(a)，及 ∀ s a，f(s • a)=s • f(a)。

`LinearMap.changeScalars`：A/B : Type*，S' : Type*，S : Type*，Semiring S'/S，
AddCommMonoid A/B，Module S A/B、Module S' A/B；
f : A →ₗ[S] B，IsBiscalar S S' f；输出 A →ₗ[S'] B。
`LinearMap.changeScalars_apply S' f a` 的结论为 changeScalars S' f a = f a。

`LinearEquiv.changeScalars`：同样的 scalar/module instances，f : A ≃ₗ[S] B，
IsBiscalar S S' f；输出 A ≃ₗ[S'] B。
没有 IsScalarTower、代数嵌入、topology 或 norm 前提；它依靠显式双标量相容，
不是任意 real-linear map 自动升级成 complex-linear map。

Route-B 候选：对已经同时兼容两套标量作用的固定坐标映射复用函数/逆映射；
实复分拆必须先证明第二条 smul law。若目标是 CLM/isometry/energy transport，
另交连续性、范数或 pairing 等式；不能从此 algebra-only 输出推导。

## Exact source pin / blobs / provenance

共同 repo：`https://github.com/anthropics/fermats-last-theorem`；commit
`aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`；source Lean v4.33.1；source Mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d`。
这是 source pin，不等于 Route-B target Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474` 的可用性证据。

| 路径 | 固定 Git blob |
|---|---|
| Theorems/Thm_ContinuousLinearMap_exists_forall_apply_eq_integral_smul_apply_of_forall_norm_le_of_continuous.lean | fc2883e4dc3cd1388f09af3f38c0b86fcee9c93f |
| P2M/Sol/S_ContinuousLinearMap_exists_forall_apply_eq_integral_smul_apply_of_forall_norm_le_of_continuous.lean | a555937bec46e08feb42df1ba9e97457f68f2881 |
| Theorems/Thm_AddChar_exists_continuousLinearMap_fourierChar_eq.lean | 5c6c562fe1ee86d0fd50baefd5a30ca2c30f141e |
| P2M/Sol/S_AddChar_exists_continuousLinearMap_fourierChar_eq.lean | 038c1112717f31ec0254b2c10c53fc49eb9a93f7 |
| Definitions/Def_Mathlib_IsModuleTopology.lean | 19de92891ffc7fb5c69636e0403041b58059880f |

Apache-2.0；保留 source LICENSE/NOTICE/ATTRIBUTION。
ATTRIBUTION.md 第 39 行将 Def_Mathlib_IsModuleTopology 整文件归于以下第三方来源：

- FLT/Mathlib/Topology/Algebra/Module/ModuleTopology.lean，© 2024 Kevin Buzzard；
  authors Kevin Buzzard、Pietro Monticone、Salvatore Mercuri、Matthew Jasper、
  Ruben Van de Velde、William Coram。
- FLT/Mathlib/Algebra/Algebra/Tower.lean，© 2025 Salvatore Mercuri；
  authors Salvatore Mercuri、Kevin Buzzard。
- FLT/Deformations/ContinuousRepresentation/IsTopologicalModule.lean，
  © 2025 Javier López-Contreras；author Javier López-Contreras。

该 entry 是文件级来源，不把每个新挑选声明强行分配给某位未核实作者。
S1/F1 的 exact-path attribution 搜索未返回专门条目；保留 Anthropic 仓库 NOTICE
（© 2026 Anthropic, PBC）及完整第三方清单，不由“无命中”推断无第三方贡献。

## 执行与 integration boundary

实际仅运行 Get-Content、固定 commit 的 git show/ls-tree、精确 attribution rg，
并读 Git HEAD/UTC 时间。最后固定对象读取调用 exit 0。首个 memory rg 无命中导致
所在 shell exit 1，不是编译失败。大 definition 输出曾截断，已另取前 81 行完整
覆盖 T1/L1；未声称审核后面的 quotient/moduleTopology 全部内容。

没有 .lean 写入、Lean/Lake、OLean、当前 compiler diagnostics 或 axioms audit。
source 精确类型和 blob 只是可追溯性，不自动使历史 catalog 的 classification=1
成为 target theorem receipt。

建议将四条登记为 pending metadata，S1/F1 可优先进入单模块 proof/API 审核，
T1/L1 先做目标现有 API 去重；不整仓编译、不自动创建 verified theorem 或 registry entry。
