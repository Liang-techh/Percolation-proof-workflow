---
kind: handoff
review_id: H-FLT-F1-ADDCHAR-FOURIER-CLM-20260908T183924Z
task_id: T-FLT-F1-ADDCHAR-FOURIER-CLM-HANDOFF-20260908
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

# F1：AddChar Fourier CLM 的独立 metadata handoff

本文件不是 proof body、Lean candidate 或 theorem receipt；仅传递固定数学契约和
后续检查要求。发布后不可覆盖，修订应新增 review_id。Route-B 状态只能 pending adapter。

## Exact declaration/type/instances

声明 `AddChar.exists_continuousLinearMap_fourierChar_eq`。
完整公开参数：E : Type*；NormedAddCommGroup E、NormedSpace ℝ E；
χ : AddChar E Circle；hχ : Continuous χ。
完整结论：存在 l : E →L[ℝ] ℝ，使 ∀ x : E，χ x = 𝐞 (l x)，
其中 𝐞 来自 `open scoped FourierTransform`。

不需要 FiniteDimensional、CompleteSpace 或 InnerProductSpace；不能把这些加进
statement 后声称 exact upstream signature。结果是 existence，不额外宣称 uniqueness。
也不能把 domain 换成一般 topological group、AddCircle 或 torus。

## Covering-lift / normalization 的不可混淆边界

**公开 theorem 不接受额外 covering-lift 假设**；在上述 real normed vector space
前提下，upstream proof 从 Circle.exp covering-map API 构造它。
审核目标 proof 时必须保留/重证这一内部步骤，不能将未证 lift 当作隐藏输入。

内部 lift contract：F : C(E,ℝ)，F(0)=0，∀ x，Circle.exp(F x)=χ x；
基点为 domain 0、target real lift 0。用唯一 lifting 性质推出 F 的加性，
再由连续加性得到 l₀ : E →L[ℝ] ℝ。
最后 l = (2*π)⁻¹ • l₀，对齐 Fourier character，而不是直接 l=l₀。
必须核对目标 `Circle.exp` / `Real.fourierChar_apply'` 的约定和非零因子；
不得删掉 2π 或用数值近似 π 代替 exact normalization。

若将定理用于周期域/环面：那是**另一个 consumer contract**，需要明确 unwrapped
real vector coordinates、covering/lattice maps、χ 的 lift 和周期相容性；
整数频率或格点条件须另证，不能从本 existence statement 直接获得。
内部 lift uniqueness 也不自动成为公开 l 唯一性 theorem。

## Immutable source provenance

```text
repository: https://github.com/anthropics/fermats-last-theorem
commit: aa2d8b34692b16c70f699536de0d8e75b9a3e9ef
source_lean: leanprover/lean4:v4.33.1
source_mathlib: db584cd6d46c92f209a44c0f1c829460d327499d
statement_path: Theorems/Thm_AddChar_exists_continuousLinearMap_fourierChar_eq.lean
statement_blob: 5c6c562fe1ee86d0fd50baefd5a30ca2c30f141e
solution_path: P2M/Sol/S_AddChar_exists_continuousLinearMap_fourierChar_eq.lean
solution_blob: 038c1112717f31ec0254b2c10c53fc49eb9a93f7
license: Apache-2.0
```

保留 Anthropic NOTICE（© 2026 Anthropic, PBC）、LICENSE 与完整第三方 ATTRIBUTION。
此前 exact-path attribution 搜索没有专门条目，不据此断言无第三方来源。
分类：公开 generic contract 1；target-pin adaptation 2；未绑定的 Route-B Fourier/flowpipe 3。

## 最小 target/import/axiom/comparator receipts

拟用 baseline：Lean v4.33.1；Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474`。本轮确认的是本地 checkout HEAD 和
toolchain 文件，不是运行时 compiler 身份或 compiled module 兼容性。

| 必需 receipt | 内容 | 当前 |
|---|---|---|
| Target pin | Lean distribution/version/commit/hash；Mathlib commit；完整依赖 lock；真实 module 搜索路径 | NOT_PRODUCED |
| Candidate/type | 新 theorem 全限定名、源 SHA、适配 diff；含全部 universes/instances/χ/hχ 与 𝐞 定义身份的签名 | NO_CANDIDATE |
| Import/build | 实际解析的 dependency source/OLean hashes；独立 candidate 与 fresh import probe 命令/完整日志/exit 0 | NOT_RUN |
| Axiom | 对最终 theorem 实际 #print axioms/依赖枚举，完整输出与允许公理策略，检查 sorryAx/新公理 | NOT_RUN |
| Comparator | fixed challenge/proof names+hashes；strict universe/type gate；checker 版本/配置/命令/退出码/完整输出 | NOT_RUN |
| Normalization bridge | lift 的基点/cover identity、加性、real-CLM 转换及 exact 2π 关系的目标声明与依赖证据 | NOT_PRODUCED |

此处 normalization bridge 可以是目标 proof 内经 kernel 检查的子推导和可重放 probe，
不一定人为增加公开 theorem 的前提。绝不能用 comparator 的 type equality
代替 proof/axiom 审计，或使用同名但重新定义的 𝐞 来获得表面匹配。

source wrapper 显示两条 Mathlib imports：Analysis.SpecialFunctions.Complex.Circle、
Analysis.Normed.Module.Basic；另有 P2M.Util/solution。
已读 solution 的 Mathlib imports 还包括 Analysis.Complex.Circle、
Topology.Homotopy.Lifting、Analysis.Convex.Contractible、
Topology.Instances.RealVectorSpace、Topology.Algebra.Module.LocallyConvex、
Analysis.LocallyConvex.Basic、Analysis.LocallyConvex.WithSeminorms。
它们是源显式 imports，不是已验证最小 target closure；target 去重/裁剪必须有
真实 import receipt。可用 exact-lock 缓存，不得偷用旧 OLean，也不默认整仓编译。

若用现 workflow comparator，必须记录 exit 0 及独立完整行
`Your solution is okay!`，还要匹配签名/源/依赖/axiom receipts；日志 marker 单独无效。
标准公理允许列表应预先配置；“编译没打印 axiom”不是依赖公理检查。

## Route-B 范围与实际执行

只能接到明确的 real-vector-space character representation pending adapter。
不提供 Fourier basis 完备性、正交性、truncation/Krylov 误差界、symmetry projector、
Poincare 常数、ODE/flowpipe、物理域覆盖或 terminal transfer。
本 handoff 不授权实现、编译、integration 脚本或 registry promotion。

本轮只读 source review、git ls-tree blobs、target HEAD/toolchain 和 hash，shell exit 0；
没有 Lean/Lake/远程编译。依据 review：
review-T-FLT-AVERAGING-FOURIER-TOPOLOGY-SCAN-20260908T183253Z.md，SHA-256
`f58bc2a08f8a5d491abb5951329267fb711215058ef1055eff43dc7e59a04659`。
所有未来 receipts 均未产生，不能提升为 compiled_candidate 或 verified。
