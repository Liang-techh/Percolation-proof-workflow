---
kind: review_result
review_id: R-FLT-SPECTRAL-PAIRING-TRANSPORT-20260908T190522Z
task_id: T-FLT-SPECTRAL-PAIRING-TRANSPORT-20260908
source_agent: Codex-FLT-spectral-linear-transport-lane
created_at: 2026-09-08T19:05:22Z
inspected_commit: a21f4dcd88d8efeb075f9e23e861a347528f126e
inspected_path: artifacts/anthropic_fermats_last_theorem
status: SOURCE_INSPECTED_PENDING_ADAPTER
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

# 两个 bounded transport 候选：spectral submodule / pairing

本轮仅写本 immutable review；定点阅读两个 public wrapper 与两个 solution 的
固定 Git 对象，不复制 proof body，不运行 Lean/Lake，不修改 state/registry。
不重复 quotient、T1/L1、S1/F1。两条均已在大 catalog 中出现；本轮固化的是
exact binder/consumer 边界，不宣称首次发现，也不升级历史旁证。

分类 1 = 泛型契约直接可用；2 = target pin/import/namespace/API 轻改候选；
3 = 当前 Route-B 实际语义仍仅架构。三者均非编译/准入标签。

| ID | Exact declaration | Generic / target / Route-B |
|---|---|---|
| SP | ContinuousLinearMap.map_eigenspace_orthogonal_le_of_commute | 1 / 2 / 3，待真实算子与块绑定 |
| PT | TransportGlue.exists_pairing_of_linearEquiv | 1 / 2 / 3，待 pairing 与完整对偶双射绑定 |

## SP：交换算子保持 eigenspace 与 orthogonal complement

完整 binder 按 source 顺序：

- 隐式 𝕜 E : Type*；[RCLike 𝕜] [NormedAddCommGroup E]
  [InnerProductSpace 𝕜 E] [CompleteSpace E]。
- 隐式 T : E →L[𝕜] E；显式 hT : IsCompactOperator T；
  显式 hT' : (T : E →ₗ[𝕜] E).IsSymmetric。
- 显式 S : E →L[𝕜] E；hST : S.comp T = T.comp S。
- 显式 μ : 𝕜；hμ : μ ≠ 0。

令 V = eigenspace (T : Module.End 𝕜 E) μ。输出恰为：

`V.map (S : Module.End 𝕜 E) ≤ V ∧
 (Vᗮ).map (S : Module.End 𝕜 E) ≤ Vᗮ`。

Type* 是多 universe 源参数，不缩成 Type 0；本轮未用 Lean 核对 elaborated
level 参数顺序。无需 S symmetric、S compact、S invertible、finite dimensional E，
也没有假定 μ 确实有非零 eigenvector。μ≠0 不意味着 V≠⊥。
保持公开 compactness/nonzero 前提，即使已读 solution 中 hT/hμ 未被显式使用，
也不能在同一 signature/receipt 中静默删掉；若做更强泛化需新声明及独立审核。

证明结构的只读观察：源由 T 对称得到 adjoint T=T，将 commutation 传给 adjoint S，
然后分别证明 eigenspace preservation 与 orthogonal preservation。这里不复制实现。

最小目标 consumer：选择真实 T/S/μ 并证明上述 instances/条件；若现 DAG 的块叫 W，
必须另证 W=V，不能凭矩阵位置/数值 eigenvectors 或 rational toy model 绑定。
公开结果是两个包含关系，不自动是 S(V)=V 或 surjectivity。
不输出 spectral gap、projection operator、orthogonal decomposition completeness、
eigenbasis、norm bound、energy dissipation、PSD 或 Lyapunov decay。

Route-B DAG 建议仅作为条件型 submodule-preservation 叶：
输入 T symmetry/compactness、S/T commutation、μ非零与 W=V 的证据，
输出 W 与 Wᗮ 的 map containment。要推 trajectory 留在块内还需真实 dynamics
operator 识别、演化/ODE regularity 与存在唯一性等义务，不能由 algebraic containment
直接生成 flowpipe/coverage/terminal-transfer 证书。

target adapter 采用独立 namespace，固定 𝕜/E 的真实结构与内积；不得以
有限维 ℚ 上 toy eigenspace sidecar 冒充此 RCLike complete inner-product contract。
候选 imports 应围绕 eigenspace、adjoint、orthogonal submodule、compact operator
定点裁剪；source Mathlib 总入口不是已验证最小闭包。

## PT：沿线性等价运输 balanced perfect pairing

完整 type binders 为 **{𝒪 A A' M N : Type}**，即 source Type 0，
不是 Type*。若未来推广 universe 必须另标 generalization，不能与原签名混淆。

完整 instances：
[CommRing 𝒪] [CommRing A] [CommRing A'] [Algebra 𝒪 A] [Algebra 𝒪 A']；
[AddCommGroup M] [Module 𝒪 M] [Module A M] [IsScalarTower 𝒪 A M]；
[AddCommGroup N] [Module 𝒪 N] [Module A' N] [IsScalarTower 𝒪 A' N]。

显式参数按 source 顺序：

1. s : M ≃ₗ[𝒪] N；φ : A → A'；hφ : Function.Surjective φ。
2. hs : ∀ a : A, ∀ m : M, s (a • m) = φ a • s m。
3. B : M →ₗ[𝒪] M →ₗ[𝒪] 𝒪。
4. hB : ∀ a : A, ∀ m n : M, B (a • m) n = B m (a • n)。
5. hBbij : Function.Bijective B。

输出存在 B' : N →ₗ[𝒪] N →ₗ[𝒪] 𝒪，三项合取：

- ∀ n n' : N, B' n n' = B (s.symm n) (s.symm n')；
- ∀ a' : A', ∀ n n' : N, B' (a' • n) n' = B' n (a' • n')；
- Function.Bijective B'。

φ 是**普通函数**加 surjectivity 与 hs，不是 RingHom/AlgHom；勿暗增结构。
hB 是平衡 scalar-action 条件，不是 B m n = B n m 的对称性。
hBbij 是 curried 线性映射 `M → (M →ₗ[𝒪] 𝒪)` 到完整**代数对偶**的双射；
非退化通常只给 injectivity，不能直接替代 surjectivity。
source 不需要有限维、field、topology、continuity、norm、inner product 或 positivity。

最小目标 consumer：具体 s/φ/hs/B/hB/hBbij，显式返回代表元公式、平衡条件与双射。
建议单独保存 B' evaluation lemma 与双射声明，避免只留下 exists 包装而失去
实际 pairing identity。所有都仍是待 target 检查的 contract，不在本轮产生 witness。

Route-B 可用于固定代数坐标变化的 residual pairing/dual-channel transport。
但实际 energy 需要另证对称、正定/强制性、范数相容和 source identification。
复 bilinear pairing 不等于 sesquilinear inner product。
若 s 随 q/t 变化，固定点公式不提供 derivative terms 或连续可微坐标共轭；
也不提供 condition number、uniform bound、FD remainder 或 flowpipe。

DAG 建议：只提出 perfect-pairing transport 条件叶，显式挂接其所有输入；
当 hBbij 只有“非退化”文本而无真实对偶满射证明时保持 pending，不强制集成。

## 固定 source pin / blobs / attribution

共同 repo：`https://github.com/anthropics/fermats-last-theorem`；commit
`aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`；Lean v4.33.1；Mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d`。

| 路径 | Git blob |
|---|---|
| Theorems/Thm_ContinuousLinearMap_map_eigenspace_orthogonal_le_of_commute.lean | 963357d9aa90e92542b7a39923a0ed6508c9ca08 |
| P2M/Sol/S_ContinuousLinearMap_map_eigenspace_orthogonal_le_of_commute.lean | eba829798335659835b4741843c9cc626f0805ff |
| Theorems/Thm_TransportGlue_exists_pairing_of_linearEquiv.lean | 18d4430aa11248a7234cae703884080355e41ff3 |
| P2M/Sol/S_TransportGlue_exists_pairing_of_linearEquiv.lean | 7f373250e03e28c41b7ff07d3d094d63b68b9564 |

来源为 Apache-2.0；保留 Anthropic NOTICE（© 2026 Anthropic, PBC）、LICENSE
与第三方 ATTRIBUTION。本轮两个 exact solution-path 名称检索未命中 attribution
专属条目；不据此声称无第三方贡献，也不编造 Imperial 原文件或作者。
任何后续复制/改编须保留完整 source notice 和所用 Mathlib 模块归属。

目标 baseline：Lean v4.33.1 / Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474`，与 upstream Mathlib 不同。
本轮只审核 source，不证明 target 的 API/olean/current compiler 环境可用。

## Admission / 执行事实

只读 git show 四个固定路径、git ls-tree、精确 attribution rg、HEAD/UTC 时间。
首组 memory rg 无命中令 shell exit 1，不是 Lean failure；第二组固定 source 读取
整体 exit 0。没有新 candidate/proof body、compiler diagnostics、公理输出或 OLean。

后续需要：准确 candidate SHA/target pin/lock/import closure；独立编译和 fresh import；
完整声明/universe comparator；最终声明的 #print axioms/允许公理审计；
对应 Route-B inputs 的 source/domain bindings。旧 catalog、同目录历史 sidecar 或
静态 closure 都不能替代这些 receipts。
本 review 仅请求 pending catalog 元数据，不运行 intake/integration、不建立 verified DAG 节点。
