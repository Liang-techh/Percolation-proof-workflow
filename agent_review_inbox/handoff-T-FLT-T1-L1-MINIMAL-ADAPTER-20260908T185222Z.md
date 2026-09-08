---
kind: handoff
review_id: H-FLT-T1-L1-MINIMAL-ADAPTER-20260908T185222Z
task_id: T-FLT-T1-L1-MINIMAL-ADAPTER-20260908
source_agent: Codex-FLT-topology-linear-interface-lane
created_at: 2026-09-08T18:52:22Z
inspected_commit: dc0e6b77c1c9eb8162517198e1ccc0dd62451059
inspected_path: artifacts/anthropic_fermats_last_theorem
status: METADATA_ONLY_PENDING_ADAPTER
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

# T1 / L1：最小 target adapter contract

独立 bounded handoff，仅此文件写入；没有 proof body、Lean implementation、编译、
registry/state 修改。发布后修订应新增 review_id，不覆盖本文件。

分类口径：1 exact generic contract 可直接消费；2 目标 namespace/import/API 轻改；
3 仅架构或未绑定的 Route-B 用途。均不代表 verified 或 compiled_candidate。
T1/L1 为通用契约 1、目标候选 2；物理 topology/energy/trajectory 推论仍为 3。

## T1 exact 源参数（无遗漏的 typeclass contract）

源 class `IsTopologicalModule`：
R : Type*，Ring R、TopologicalSpace R；M : Type*，AddCommGroup M、Module R M、
TopologicalSpace M；class 仅 extends ContinuousSMul R M 与 ContinuousAdd M。
它不是 `IsModuleTopology`，不表示当前 topology 等于 moduleTopology。

声明 `Topology.IsInducing.topologicalModule`：

- 隐式 F : Type*；显式 R : Type*，实例 Ring R、TopologicalSpace R。
- 隐式 M : Type*；实例 AddCommGroup M、Module R M、TopologicalSpace M、
  IsTopologicalModule R M。
- 隐式 H : Type*；实例 AddCommGroup H、Module R H、TopologicalSpace H。
- 实例 FunLike F H M、LinearMapClass F R H M。
- 显式 f : F；显式 hf : Topology.IsInducing ⇑f。
- 输出 IsTopologicalModule R H。

源 Type* 是 universe-polymorphic；没有显式 universe 同一性约束或有限维约束。
本轮核对的是源码 binder，不声称已用 #check/@ 检查 elaborated universe 参数顺序；
未来 comparator 必须对完整 universe 泛化做检查，不以 Type 0 实例代替。

无需 Injective f、Surjective f、IsEmbedding f、IsTopologicalRing R、T2Space 或
FiniteDimensional；不可擅自增加这些前提后声称 exact signature。
反过来，只知道 Continuous f 不能代替 IsInducing f。

## T1 最小目标接口

优先不引入全局 source class，而用目标已有字段构造局部 consumer：
沿用 R/M/H/F/f/hf 参数，将 ambient assumption 展开为
[ContinuousSMul R M] [ContinuousAdd M]，输出
`ContinuousSMul R H ∧ ContinuousAdd H`。
这是**建议的新 contract**，不是已存在/已编译的声明。若需要保持 source 结果，
在独立 namespace 中另证该字段对与 source class 的显式打包/拆包 bridge。

source proof 所依赖的 inducing 连续性传递 API 在当前 target 的
Mathlib/Topology/Algebra/MulAction.lean:190 有
`Topology.IsInducing.continuousSMul`；
Mathlib/Topology/Algebra/Module/Basic.lean:111 也有相应调用。
这是静态入口证据，不是完整类型/闭包兼容性证明。目标侧优先核对该模块和
ContinuousAdd 的 inducing transport，不整文件导入 Def_Mathlib_IsModuleTopology。

最小正例应覆盖 f : H →ₗ[R] M 的实例化和 submodule inclusion；保持独立 universe。
Route-B 必须先说明 H 的 topology 与真实物理/坐标 topology 一致且由 f inducing。
不能从结果推出 Hausdorffness、norm equivalence、isometry、闭子空间、紧性、
坐标单射、边界/轨迹覆盖或任何 Poincare/flowpipe 结论。

## L1 exact 源参数与结果

source `IsBiscalar (R S : Type*) {A B : Type*}`：
Semiring R/S、AddCommMonoid A/B、Module R A/B、Module S A/B；显式 f : A → B。
两个字段为 ∀ r a, f (r • a) = r • f a 和 ∀ s a, f (s • a) = s • f a。
没有 IsScalarTower、Algebra、SMulCommClass 或 topology 假设。

`LinearMap.changeScalars` 的共同 section binder：
隐式 A B : Type*，显式 S' : Type*，隐式 S : Type*；
[Semiring S'] [Semiring S] [AddCommMonoid A] [AddCommMonoid B]
[Module S A] [Module S B] [Module S' A] [Module S' B]；
显式 f : A →ₗ[S] B；实例 [IsBiscalar S S' f]；结果 A →ₗ[S'] B。
`LinearMap.changeScalars_apply` 再接显式 a : A，结果 changeScalars S' f a = f a。

`LinearEquiv.changeScalars` 使用同样 section type/module binders；
显式 f : A ≃ₗ[S] B，实例 [IsBiscalar S S' f]；结果 A ≃ₗ[S'] B。
来源保留原 inverse 函数；本 review 不复制实现。
所有 Type* 保持多 universe；不擅自将 A/B 或 S/S' 固定为同一 universe。

## L1 最小目标接口与 target-native 替代

建议避免新增全局 IsBiscalar：保留共同 binders 与 f，显式接收
`hS' : ∀ (s : S') (a : A), f (s • a) = s • f a`，
输出 S'-linear map/equiv，并交付 apply 等式（equiv 另交 inverse-apply 等式）。
已有 f 的 S-linearity 已提供第一条 scalar law；hS' 不能省略。
这仍是待实现的 contract，需经 bridge 才能称对应 source API。

定点检查发现 target 已有可优先利用的 API，而非新增另一个 FLT 定理：

- `LinearMap.restrictScalars`，Mathlib/Algebra/Module/LinearMap/Defs.lean:425；
- `LinearEquiv.restrictScalars`，Mathlib/Algebra/Module/Equiv/Basic.lean:48。

两者在 Semiring R/S、AddCommMonoid M/M₂、Module R M/M₂、Module S M/M₂、
**LinearMap.CompatibleSMul M M₂ R S** 的前提下，将 S-linear map/equiv
转为 R-linear map/equiv。map 的 `coe_restrictScalars` 保留 underlying function。
这是更小的 target-native 接口选择，分类 1（满足其前提时），但 provenance 是
target Mathlib，不可冒充 FLT 新 theorem。
它的 CompatibleSMul 是整个模块对的相容 contract，不能未经证明替代
source 的单个 f 的 IsBiscalar/hS' 条件；若只有单映射相容，则保留显式 hS' 路线。

对于 ℂ→ℝ 限制标量这类标准场景优先检查 target-native 实例；
对于 ℝ→ℂ 升级，普通 real-linear map 不自动 complex-linear，仍须完整 hS'。
无 topology/norm 输入的 L1 输出不提供 continuity、boundedness、isometry、
positivity、quadratic pairing 保持或 coordinate-dependent derivative/energy 公式。
不因“同一函数”就推导不同标量/范数结构的物理意义相同。

未开展额外 spectral theorem 搜索：本 bounded task 的高价值动作是目标 API 去重，
不是引入第三个大证明或重复已收割 eigenspace/quotient 结果。

## Source/target pins 与第三方 attribution

```text
source_repository: https://github.com/anthropics/fermats-last-theorem
source_commit: aa2d8b34692b16c70f699536de0d8e75b9a3e9ef
source_path: Definitions/Def_Mathlib_IsModuleTopology.lean
source_blob: 19de92891ffc7fb5c69636e0403041b58059880f
source_lean: leanprover/lean4:v4.33.1
source_mathlib: db584cd6d46c92f209a44c0f1c829460d327499d
target_lean_baseline: leanprover/lean4:v4.33.1
target_mathlib: 0df444a360eaa60ab8c11dca51a86af692955474
```

target HEAD 本轮只读重核；source/target Mathlib 不同，不能把 source 成功或
历史 target sidecar receipt 迁移给尚不存在的 T1/L1 adapter。

source ATTRIBUTION.md:39 将整个 definition 文件归于：

- FLT/Mathlib/Topology/Algebra/Module/ModuleTopology.lean，© 2024 Kevin Buzzard；
  authors Kevin Buzzard、Pietro Monticone、Salvatore Mercuri、Matthew Jasper、
  Ruben Van de Velde、William Coram。
- FLT/Mathlib/Algebra/Algebra/Tower.lean，© 2025 Salvatore Mercuri；
  authors Salvatore Mercuri、Kevin Buzzard。
- FLT/Deformations/ContinuousRepresentation/IsTopologicalModule.lean，
  © 2025 Javier López-Contreras；author Javier López-Contreras。

Apache-2.0，保留 LICENSE/NOTICE/ATTRIBUTION。该 provenance 是整文件映射，
不编造某条 theorem 的唯一作者或 Imperial 源独立 commit。
若改用 target-native restrictScalars，则另保留该 Mathlib 文件头/许可证；
例如已读 Equiv/Basic 头为 © 2020 Anne Baanen，列有 Nathaniel Thomas、Jeremy Avigad、
Johannes Hölzl、Mario Carneiro、Anne Baanen、Frédéric Dupuis、Heather Macbeth。

## 下一步最小 evidence gate（本轮全部未执行）

1. 新候选完整 types/universe binders 与 source→consumer bridge，绑定实际 SHA。
2. 精确 target distribution/Mathlib/lock、真实 imports 与 OLean 身份；只检查小闭包。
3. 正例编译与 fresh import；不能用正文/静态 rg 代替 compiler output。
4. 对 exported declarations 显式 #print axioms/依赖枚举，检查 sorryAx/未授权公理。
5. 严格 comparator 匹配选定 contract（source 版与字段化版不得混同），记录全部
   参数、universes、source hashes、命令/配置/退出码/日志；通过也不自动 registry promotion。

实际命令仅 git show 固定 source 前 74 行、精确 attribution rg、target 文件阅读/
API rg、git rev-parse、UTC 时间；两组 shell exit 0。没有新编译错误或通过记录。
metadata 仅请求 pending catalog 附件；没有运行 integration 脚本。
