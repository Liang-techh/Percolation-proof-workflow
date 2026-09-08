---
kind: review_result
review_id: review-GH-LEAN-BODY5-API-REPAIR-LOCAL-20260908T094207
task_id: GH-LEAN-BODY5-API-REPAIR
source_agent: codex-local
created_at: 2026-09-08T09:42:07-06:00
inspected_commit: 97ce842068a036050fced394494403c2d133126d
inspected_paths:
  - examples/routeb_b45_source_comparator_lean/NEW_BODY5_API_REPAIR_Independent20260908.lean
candidate_sha256: a6bcf446b60f3d93c92f6bb946a56c75ec7d761289b30cc7878b3705186c092a
proof_status: OPEN_UNCOMPILED
integration_status: pending
admission_label: pending
parsed: false
elaborated: false
kernel_checked: false
axioms_checked: false
verified: false
final_integration: false
registry_promoted: false
formal_certificate_allowed: false
requested_action: Obtain a separately authorized pinned GitHub compile receipt before considering admission; do not promote from this envelope.
---

# 独立 body-5 API repair 候选封套

仅封装候选元数据；不重做数学、不修改候选或其他文件、不运行本机 Lean/Lake，
不启动 GitHub workflow。候选当前为 untracked 文件，因此 inspected HEAD 不是
“该候选已包含于此 commit”的声明；候选身份由独立 SHA-256 绑定。

## 候选声明

全部在 namespace `NEW_BODY5_API_REPAIR_Independent20260908`，共 14 个：

```text
perm_map_sum
seeded_sum
flat_pairs_sum
coordinate_sum_congr
coordinates3
coordinates6
decode_map
decode_encode
row_perm
q3_membership
filter_perm
phase3
q3_product
q3_fold_pairs
```

上述清单来自源文本，不表示 Lean 已解析或接受这些声明。

## 最小 GitHub pinned compile receipt 字段

后续独立授权的远程检查至少需记录：

1. GitHub repository、实际 checkout commit SHA、workflow 文件路径与 blob SHA、
   run URL/run ID/run attempt/job ID；外部 actions 使用不可变 commit pin。
2. 候选路径与 SHA-256，实际编译 checkout/补丁 artifact 的身份；必须说明本候选
   如何进入 checkout，并逐字节与本封套绑定，不能仅凭 inspected HEAD。
3. `lean-toolchain` 原文与哈希、Lean 版本，Mathlib repository/revision，
   lake manifest/lock 哈希，直接和传递项目 imports 的源文件哈希清单。
4. 工作目录、完整编译命令、模块搜索路径与相关环境设置、开始/结束时间、
   exit code、完整 stdout/stderr artifact URL 与 SHA-256；不得把缓存成功当作
   对这份候选源的当前编译，须交代缓存/重建策略。
5. 产生的候选及必要依赖 `.olean` 路径与 SHA-256；14 个完整限定声明名称、
   elaborated 类型或可复核类型输出，以及逐声明 `#print axioms` 输出及其哈希。
6. 明确的 scope/status：编译、kernel/axiom 检查分别是否完成；如另行申请
   comparator admission，还需 statement/source/DAG 绑定与 comparator 命令、
   exit code 0、精确独立行 `Your solution is okay!` 及完整输出哈希。

本轮以上运行、环境 pin、输出和 OLean 字段均未获取，不能用占位值表示通过。
这份清单是接收要求，不是对任何 GitHub workflow 的现状描述或运行授权。

## Admission 边界

即使后续编译成功，也只接受精确声明及其显式参数范围。`q3_fold_pairs` 仍以
source 编码 Perm 为前提；不产生 16 行源绑定 witness、旧 classical-filter
target、G1/G2 witness、最终 h_body_5、数值执行一致性或连续域 coverage。
编译 receipt 不自动注册；来源缺失保持 pending，证据存在但哈希/声明不符应
rejected，由独立 admission gate 决定。不得修改 state/registry 来把本封套提升。

本次仅读取候选 SHA、HEAD、时间与 theorem 行，并新增本 review_result 文件。
