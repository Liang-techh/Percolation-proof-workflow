---
kind: handoff
review_id: H-FLT-S1-AVERAGING-CLM-20260908T183924Z
task_id: T-FLT-S1-AVERAGING-CLM-HANDOFF-20260908
source_agent: Codex-FLT-spectral-topology-lane
created_at: 2026-09-08T18:39:24Z
inspected_commit: dd1892785dcfa0f1f342090a8811b462ee5cada0
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

# S1：加权 averaging CLM 的独立 metadata handoff

只记录类型、source 与未来 receipt contract；不含 proof body，不产生 Lean candidate。
发布后不改写本 envelope，修订应另建 review_id。Route-B 只能是 pending adapter。

## Exact source statement

声明：`ContinuousLinearMap.exists_forall_apply_eq_integral_smul_apply_of_forall_norm_le_of_continuous`。

全部 parameters/instances：

- C : Type*；Group C、TopologicalSpace C、IsTopologicalGroup C、CompactSpace C、
  T2Space C、MeasurableSpace C、BorelSpace C。
- μ : Measure C；μ.IsHaarMeasure、IsProbabilityMeasure μ。
- H : Type*；NormedAddCommGroup H、InnerProductSpace ℂ H、CompleteSpace H。
- S : C →* (H →L[ℂ] H)；B : ℝ；hSb : ∀ c : C, ‖S c‖ ≤ B。
- hSc : ∀ v : H, Continuous (fun c : C => S c v)。
- w : C → ℂ；hw : Continuous w。

结果存在 A : H →L[ℂ] H，满足下列四项的合取，顺序对应 source：

1. ∀ v : H，A v = ∫ c, w c • S c v ∂μ。
2. ∀ M : ℝ，(∀ c : C, ‖w c‖ ≤ M) → ∀ v : H，‖A v‖ ≤ M * B * ‖v‖。
3. ∀ L : Submodule ℂ H，IsClosed (L : Set H) →
   (∀ c : C, L.map (S c : H →ₗ[ℂ] H) ≤ L) → L.map (A : H →ₗ[ℂ] H) ≤ L。
4. ∀ T : H →L[ℂ] H，(∀ c : C, T.comp (S c) = (S c).comp T) → T.comp A = A.comp T。

## 不可静默改变的契约

Haar 与 probability 是公开 statement 的两个独立 instances，原样保留。
不要以“只用了有限积分”为由在同一 receipt 中删 Haar、改非规范化 measure；
若要推广，需另立 theorem/type/receipt，norm bound 的测度因子也应重新推导。
μ 的总质量规范化不可被样本平均或数值 quadrature 默认替代。

hSc 是每个 v 的强连续，不是 operator-norm continuity；hSb 是所有 c 的统一
算子范数界，不能用有限样本代替。两者均必须绑定实际 S；S 必须是指定 monoid hom，
不是无结构算子列表。w 连续、H 完备、L closed 及 T 的逐 c commutation 都不能漏掉。
源没有另列 B≥0、M≥0 参数，不应改变 binder 后声称 exact signature。

没有要求 C 交换、S unitary、w character 或 H 有限维；也没有输出
A²=A、self-adjoint、PSD、正交性或 spectral projection。
保留不变子空间与交换性不意味着 symmetry projector。

## Immutable upstream provenance

```text
repository: https://github.com/anthropics/fermats-last-theorem
commit: aa2d8b34692b16c70f699536de0d8e75b9a3e9ef
source_lean: leanprover/lean4:v4.33.1
source_mathlib: db584cd6d46c92f209a44c0f1c829460d327499d
statement_path: Theorems/Thm_ContinuousLinearMap_exists_forall_apply_eq_integral_smul_apply_of_forall_norm_le_of_continuous.lean
statement_blob: fc2883e4dc3cd1388f09af3f38c0b86fcee9c93f
solution_path: P2M/Sol/S_ContinuousLinearMap_exists_forall_apply_eq_integral_smul_apply_of_forall_norm_le_of_continuous.lean
solution_blob: a555937bec46e08feb42df1ba9e97457f68f2881
license: Apache-2.0
```

保留 Anthropic NOTICE（© 2026 Anthropic, PBC）以及 LICENSE/完整 ATTRIBUTION；
前轮 exact-path attribution 搜索未返回专属条目，不推断无第三方来源。
分类：exact 通用契约 1；目标小范围 adaptation 2；Route-B projector/flowpipe 用途 3。

## 最小 target receipt 清单：全部 REQUIRED / NOT_PRODUCED

目标 baseline 为 Lean v4.33.1、Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474`；本轮仅重读 checkout HEAD/toolchain 文件，
没有运行编译器验证 distribution。source/target Mathlib pin 必须分栏。

| Receipt | 最少内容 | 当前状态 |
|---|---|---|
| Target pin | compiler version/commit 或 distribution hash；Mathlib commit；完整依赖 lock；真实 LEAN_PATH/search order | NOT_PRODUCED |
| Candidate identity | 新 namespace/全限定 theorem 名、实际 source SHA-256、与上述 blob 的适配差异、完整类型与 universe binder | NO_CANDIDATE |
| Import/build | 实际解析的模块/源/OLean hashes，fresh isolated candidate+import probe 的命令、stdout/stderr、exit 0 | NOT_RUN |
| Axiom | 对最终 theorem 实际执行 #print axioms 或等价依赖枚举，保存完整公理集及 allowlist 审核，拒绝 sorryAx/未经许可新公理 | NOT_RUN |
| Comparator | exact statement/proof 名与 hashes、保留全部四项输出/instances/universes 的严格比较、checker 配置/version/命令/退出码/完整输出 | NOT_RUN |

source wrapper import Mathlib、P2M.Util 与 solution；solution 也 import Mathlib。
最小 target imports 尚未确定。未来只为 Bochner-integral/CLM/closed-subspace 所需
闭包构建小 adapter，不能把单条 Mathlib import 当作小闭包，也不默认整仓构建。
可消费 exact-lock 缓存，但缓存来源/哈希与真实 import resolution 必须入 receipt。

若使用当前 workflow comparator，必须同时保存 exit 0 和独立完整行
`Your solution is okay!`；日志 marker 或 P2M type-eq 输出不单独构成接受。
允许的标准公理应事先配置，不能将“grep 未见 axiom”作为公理集审计。

## Route-B pending adapter 与动作范围

未来另绑定实际 C/μ/H/S/B/w、物理变量映射、real/complex 识别；需要作用于 dynamics
时另交真实 T 的 commutation。投影需新增 idempotence/orthogonality 等证明。
没有 ODE、flowpipe、Poincare、覆盖、FD remainder 或 terminal-transfer theorem。
本 handoff 只请求 pending catalog 元数据，不请求 DAG theorem、编译或 registry promotion。

本轮只读 git ls-tree/source review、target HEAD/toolchain、Get-FileHash，shell exit 0。
依据 review：review-T-FLT-AVERAGING-FOURIER-TOPOLOGY-SCAN-20260908T183253Z.md，SHA-256
`f58bc2a08f8a5d491abb5951329267fb711215058ef1055eff43dc7e59a04659`。
lean/lake/remote compile 均未运行；所有 receipt 状态不可默认为成功。
