---
task_id: GH-LEAN-BODY4-FINITE-SUM-RECEIPT-HANDOFF
status: HANDOFF_PREPARED_NOT_RUN
integration_status: pending
admission: pending
candidate_compiled: false
frame_handoff_closed: false
---

# Body4 finite-sum pinned compile handoff review

仅新增两份 handoff 文件及本 NEW_REVIEW；未修改 candidate、state、registry 或旧文件。
没有 GitHub dispatch、没有在本机运行 Lean/Lake、没有声称候选已编译。

## 交付

- `examples/routeb_o1_body4_source_gram_proof_attempt/NEW_FINITE_SUM_20260908_COMPILE_HANDOFF.json`
  SHA-256: 630D9EFBE5C751A680E5EBB23205740BF7A37FC7F67D32905E59A9ABC90E1D22。
  完整仓库内 import DAG、16 模块拓扑序/路径/哈希、三个 snapshot 哈希、pin、端点清单。
- 同目录 `NEW_FINITE_SUM_20260908_COMPILE_HANDOFF.md`
  SHA-256: 3E9FCD90982C6C4EB8BB55444A08AF4A24150E93C58719AFF43FACC235F0127E。
  GitHub agent 隔离命令、审计模块文本、receipt 字段和 failure taxonomy。

原候选 `NEW_FINITE_SUM_20260908_STEP3_TRANSLATION.lean` 保持
A7144407F5AA2C5F8BC4F30D2327B39CB22F1A587A0F0A141B5E22605A344B8E。
本轮逐项重新计算 16 个模块 + 3 个 snapshot SHA，0 mismatch；JSON 可解析。
这只是文件与 import-line 静态校验，不是 parser/kernel/编译证据。

## Pin 与依赖风险

沿用 accessor/comparator 历史记录的 Lean 4.33.1
（819816b2e0a3bf405af45ae5c7af2491d8f5bee6）、Mathlib
0df444a360eaa60ab8c11dca51a86af692955474。远端必须先检查 Mathlib 的
lean-toolchain 与该 pin 一致；不符立即 ENV_PIN_MISMATCH，不自动换版本。
local_fkg / 工作流 lake update / 历史 run oleans 均不可混用。

仓库内闭包为候选 + 15 imports，包含 SourceBodyMassExtensionalProbe；
其 COMPILATION_STATUS 仍缺完整成功证据。必须先编译依赖，不能因有限和简单而跳过。
外部根为 Mathlib；其全传递依赖按指定提交的 committed lake-manifest 与 Lean
distribution 绑定。没有谎称本机逐个读取/核验整个 Mathlib 闭包；远端 receipt
必须补实际 lockfile hash、各外部包 revisions、library roots/cache provenance。

## Receipt 判定门槛

新鲜 RUN 中按拓扑序重建，不编辑输入，不复用旧 repo oleans。记录每一阶段
命令、退出码、耗时、日志/输入/olean 哈希。未执行的阶段 exit_code=null。
单独 audit 模块消费原 Body4Slot4TranslationTarget，并打印七个候选声明及
exact_endpoint 的 axioms；特别补上原候选 print 列表遗漏的 source_row_translation。
允许 axiom 集合只能是 {propext, Classical.choice, Quot.sound} 的子集。
sorryAx 或未批准 custom axiom 失败；文本扫描标记必须逐条解释，不是仅看退出码0。

分开记录 hash/pin/import 缺失、依赖编译失败、候选失败、timeout、资源失败、
axiom 审计失败与 receipt 不完整。成功上限是 COMPILED_CANDIDATE_PENDING_REVIEW。
不触发 registry promotion，不自动消费 FRAME_HANDOFF，不证明 PrefixColumnsTarget、
source Gram/mass/trace 或 Julia Float64。没有 comparator 执行，不能伪造 acceptance。

完整命令仅作为交接文本，未在本机测试；GitHub agent 需保留真实失败诊断，
不能把本 handoff 当成可执行环境已经建立或编译一定成功的承诺。
