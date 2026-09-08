---
kind: review_result
review_id: R-FLT-BLOCK456-PROJECTOR-API-PLAN-20260908T191944Z
task_id: T-FLT-BLOCK456-PROJECTOR-API-PLAN-20260908
source_agent: Codex-FLT-block456-projector-interface-lane
created_at: 2026-09-08T19:19:44Z
inspected_commit: 282de6327682b3c6aca64dfd310e9b05be163e71
inspected_path: agent_review_inbox/handoff-T-FLT-SP-BLOCK456-SPECIALIZATION-20260908T191254Z.md
status: PENDING_API_DESIGN_NO_IMPLEMENTATION
integration_status: pending
admission_label: pending
registry_eligible: false
registry_promoted: false
lean_run: false
lake_run: false
kernel_checked: false
axioms_checked: false
source_binding: false
requested_action: catalog_pending_metadata_only
---

# Block456 projector bridge：最小 API 方案与 no-go gate

本轮完整审阅指定 handoff 与 catalog 对应条目，只写本 immutable review。
不创建 .lean/proof body、不运行 Lean/Lake、remote compile 或 integration，
不修改 state/registry。修订应另建 review_id。

## 决策

建议优先做**坐标选择 projector 的小型条件接口**，不要将 nominal mass 重新命名为
projector。该接口在数学上合法，但对真实 Route-B 能否使用，取决于实际 transport
矩阵两个 cross blocks 是否精确为零。若它们不为零，就停止该 exact-invariance 路线。

分类：FLT 通用 invariant-subspace 声明 1；下面新 index/projector adapter 2；
当前没有 actual-source commutation witness，Route-B 使用仍是 3/pending。
catalog 中 classification=1 是泛型复用等级，不是 current theorem receipt。
catalog 的“nonzero eigenspace”描述应按 exact theorem 理解为 μ≠0；不保证 eigenspace 非零。

## A. 固定对象与 index contract

以下名称均为 **proposed**，尚未创建，不能作为现有 Lean API 引用：
namespace `RouteBBlock456ProjectorCandidate`。

- scalar 𝕜 : Type u，[RCLike 𝕜]；实际 consumer 选标准 ℝ 或 ℂ。
- E := EuclideanSpace 𝕜 (Fin 6)，U := EuclideanSpace 𝕜 (Fin 3)。
- `embed456 : Fin 3 → Fin 6`，值为 3、4、5；对应 human joints 4、5、6。
- `I456 : Set (Fin 6)` 为 range embed456；`I123` 为其补集。
- `include456 : U →L[𝕜] E`：在 I456 填入 U 坐标，其余为零。
- `extract456 : E →L[𝕜] U`：第 a 坐标取 x(embed456 a)。
- `project456 : E →L[𝕜] E` := include456.comp extract456。
- `W456 : Submodule 𝕜 E`：I456 外坐标为零；W123 同理。

所有 function/CLM coercions、Fin 值范围与 EuclideanSpace 表示均待 pinned elaboration。
不能以未明确 ℓ² norm 的 plain function space、三维 block port 或 full-state 空间替换。

## B. 最小候选 theorem 名与精确结论（无 proof body）

| Proposed theorem | 输入/结论 |
|---|---|
| `embed456_injective` | Function.Injective embed456 |
| `extract_include456` | extract456.comp include456 = ContinuousLinearMap.id 𝕜 U |
| `include_extract456_apply` | ∀ x j，project456 x j = if j∈I456 then x j else 0 |
| `range_include456_eq_W456` | LinearMap.range include456.toLinearMap = W456 |
| `project456_idempotent` | project456.comp project456 = project456 |
| `project456_symmetric` | project456.toLinearMap.IsSymmetric |
| `project456_compact` | IsCompactOperator project456，由有限维连续性接线 |
| `eigenspace_project456_one` | eigenspace project456.toLinearMap (1:𝕜) = W456 |
| `orthogonal_W456_eq_W123` | W456ᗮ = W123，在标准 Euclidean/Hermitian 内积下 |

这些是坐标结构叶，不含任何 physical-source 参数。
如只求极小 consumer，可先证明 apply、symmetric、compact、eigenspace 与 orthogonal
五个必要入口；include/extract 的其他 identities 用于明确外部 index/source bridge，
不应变成一整套无关 regression。

## C. Matrix / commutator bridge：真正的 source gate

明确 A : Matrix (Fin 6) (Fin 6) 𝕜；S_A : E →L[𝕜] E，
`matrix_apply` contract 为 ∀ x i，S_A x i = ∑ j, A i j * x j。
这固定列向量左乘及 row/col 方向，不能静默换为 row-vector convention。
令 p_j 为 I456 的 0/1 指示系数，则
`(A P − P A) i j = A i j * (p_j − p_i)`。

提出 `commute_project456_iff_cross_zero`：
S_A.comp project456 = project456.comp S_A，等价于以下两个合取：

- ∀ i∈I123，∀ j∈I456，A i j=0（456 输入不流入 123 输出）；
- ∀ i∈I456，∀ j∈I123，A i j=0（123 输入不流入 456 输出）。

该等价与 apply contract 需要 Lean 证明，当前只是精确 target specification。
注意只有第一组零项时可得 W456 的单向保持，但不保证 W123 保持或 commutation；
此时不要强迫套用返回两个子空间保持的 FLT theorem，可另用单向 coordinate lemma。
同块内部 A46/A64 非零不阻碍与 selector P 交换；不要把同块交叉项与 cross-block 项混淆。

source consumer 必须给出 actual operator name、matrix-entry identities、index convention、
参数域和 ∀ z∈D 的 exact cross-zero witnesses。若 A(z) 随状态变化，这只得到
每个 z 的线性算子保持，尚不是非线性流保持。

## D. FLT 消费器：精确 attribution，而非新增物理证明

source declaration：`ContinuousLinearMap.map_eigenspace_orthogonal_le_of_commute`。
完整 generic inputs：{𝕜 E : Type*}、RCLike 𝕜、NormedAddCommGroup E、
InnerProductSpace 𝕜 E、CompleteSpace E；{T : E →L[𝕜] E}；
hT : IsCompactOperator T；hT' : T.toLinearMap.IsSymmetric；
S : E →L[𝕜] E；hST : S.comp T=T.comp S；μ : 𝕜；hμ : μ≠0。
输出 eigenspace(T,μ).map S≤eigenspace(T,μ) 及其 orthogonal complement 的同类包含。

proposed `block456_partition_preserved_of_cross_zero` 将 T=project456、μ=1，
通过 B/C 的 lemmas 提供 compact/symmetric/commute、RCLike 的 1≠0 与 hAlign，
返回 W456.map S_A≤W456 ∧ W123.map S_A≤W123。
不删除 source 的 compact/μ≠0 binder；若改用 historical sharpened theorem，
应另选声明身份/receipt。

**最小性判断**：selector 路线中的 cross-zero 事实上也能直接推出 containment，
因此 FLT 在此是通用 API 的复用接线，不新增有关实际 dynamics 的数学信息。
如果 direct coordinate lemma 更容易审计，可将 FLT consumer 保留为可选兼容叶，
不为了使用外部 theorem 人为扩展 DAG。

## E. 明确 no-go 判据

1. 无 actual S/A identity：只能交通用结构候选，不接 physical DAG。
2. 在目标域找到任意 exact cross-block A i j≠0：selector commutation 失败；
   浮点近似零或 small commutator 不满足 exact theorem。
3. 把真实 mass T 的整个 W456 当单 μ eigenspace，但 T|W456 不是 μI：alignment 失败。
   先前 handoff 记录 nominal block 的 1/60 同块 off-diagonal 正是该路线的障碍；
   不等同于第 2 条 selector no-go，也未在本轮重新证明外部 source 数据。
4. 实际 W 是多个 eigenvalues 的子空间和：单 eigenspace contract 不适用，应另立 sum 接口。
5. 换成 dense energy metric 却沿用 Wᗮ=W123：需 metric bridge，否则不接；
   coordinate selector 的 self-adjointness 也依赖选定内积。
6. 输入是 affine/nonlinear dynamics 而无 vector-field/forcing/trajectory 契约：
   不能将 pointwise CLM containment 升级为 flowpipe 或 invariant manifold。

auxiliary P 的 0/1 spectrum 不构成物理 mass/operator 的 spectral gap；
没有 quantitative decay、coercivity、ODE existence、FD remainder、coverage 或终端传递。

## Provenance / imports / 下一步

repo https://github.com/anthropics/fermats-last-theorem；commit
aa2d8b34692b16c70f699536de0d8e75b9a3e9ef；source Lean v4.33.1；Mathlib
db584cd6d46c92f209a44c0f1c829460d327499d。
Theorems/Thm_ContinuousLinearMap_map_eigenspace_orthogonal_le_of_commute.lean：
blob 963357d9aa90e92542b7a39923a0ed6508c9ca08；
P2M/Sol/S_ContinuousLinearMap_map_eigenspace_orthogonal_le_of_commute.lean：
blob eba829798335659835b4741843c9cc626f0805ff。
Apache-2.0；保留 Anthropic NOTICE（©2026 Anthropic, PBC）与完整第三方 ATTRIBUTION，
不为此 solution 编造未查到的专属作者。

target baseline Lean v4.33.1 / Mathlib 0df444a360eaa60ab8c11dca51a86af692955474。
历史 spectral module 的 Adjoint、Compact.Basic、Eigenspace.Basic imports 可作起点，
另需 EuclideanSpace、matrix→CLM、finite-dimensional compactness 的实际 target API。
不宣称已找到最小闭包；本轮不跑 #check、Lean 或 Lake。

下一步最小义务：先由 owner 指定 actual S/A 与域 D，并定点检查 exact cross-block
zeros；若通过，再获授权实现 B/C 的小叶与可选 FLT consumer，绑定源码/target hashes，
获得 focused compile/import/type/axiom/comparator receipt。未指定 S 前无需大规模实现。

实际检查仅 Get-Content 指定 handoff/catalog、Get-FileHash、Git HEAD/UTC，shell exit 0。
输入 handoff SHA-256：4c1b80f1a38ae6f84ab05b843361b814badd695d4eb6a206f60114ad144a9517。
没有新候选或 proof receipt；全部 pending metadata，不运行 integration 或 promotion。
