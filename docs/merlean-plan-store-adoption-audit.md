# MerLean `plan_store` adoption audit

审计范围：MerLean 当前 `master` 的 `src/plan_store/store.py`、`lean_sync.py`、`README.md`、`config.py`，以及本地 `percolation_workflow` 的 `model.py`、`store.py`、`graph.py`、`registry.py`。本审计为只读分析；没有复制 MerLean 仓库、修改实现或运行长测试。

审计日期：2026-09-06。

## 结论

不能把 MerLean `plan_store` 直接替换进本系统。可以借鉴其数据形状和若干纯图算法，作为一个**只读/派生的兼容投影层**，但权威状态仍必须由本地 `WorkflowState` 和带校验的 checkpoint 掌管；Lean 编译结果、证明 receipt、admission gate 和 verified registry 不能由 MerLean 状态字段推断或覆盖。

MerLean 的设计重点是“statement plan graph + Lean 依赖同步 + 语义检索”。本系统还需要更严格的研究级 admission：源代码/声明绑定、精确 statement identity、编译环境与 manifest 新鲜度、checker/comparator receipt、覆盖/余项/flowpipe/terminal-transfer 等数学证据，以及无 `sorry`/不受允许 axiom 的 kernel 证据。两者不是同一个完成状态。

## 上游实现要点

- `store.py` 用 Mem0 2.x 作为图的持久化后端，在本地嵌入 Qdrant；formal node 的 metadata 包含 `statement_id`、`type`、`name`、`content`、`dependencies`、`dependents`、`proof`、`anchor`、`mathlib_types`、`lean_path`、`hierarchy_level`、`corrections`、`status`、`do_not_import`、`declarations_defined`、`imports` 和 source span。关闭时另写 `statements.json`、`progress.json`、`analytics.json`。
- 同一文件提供 deterministic topo order、dependency cycle 检查、forward dependency cone、levels/levels_grouped、反向 dependents 重算，以及 status history/subagent metrics。这些正好对应 theorem DAG、失效传播、frontier 分层和 agent history 的一部分。
- `Note`/`Summary` 是嵌入检索用的 informal nodes，不进入 graph、topo、status、export 或 `sync-lean`。Note 另带 `confidence`、`source`、`evidence`、`method`、`caveats`、`related` 和时间字段；这个“研究判断与形式证明分离”的结构值得保留。
- `lean_sync.py` 从真实 `.lean` 文件做符号级使用分析，把声明、imports、source lines 映射回 statement，并将 Lean-derived edges 视为权威。这比只依赖人工 theorem dependencies 更适合检测漏边和 stale graph。
- `config.py` 将每个目标的数据放在目标旁的 `<target>_data`，使用 OpenAI LLM/embedding、embedded Qdrant、history DB，并固定 embedding model/dimension；模型或维度变更需要重新嵌入。

参考：

- [MerLean `src/plan_store/store.py`](https://raw.githubusercontent.com/MerLeanProver/MerLean/master/src/plan_store/store.py)
- [MerLean `src/plan_store/lean_sync.py`](https://raw.githubusercontent.com/MerLeanProver/MerLean/master/src/plan_store/lean_sync.py)
- [MerLean `src/plan_store/README.md`](https://raw.githubusercontent.com/MerLeanProver/MerLean/master/src/plan_store/README.md)
- [MerLean `src/plan_store/config.py`](https://raw.githubusercontent.com/MerLeanProver/MerLean/master/src/plan_store/config.py)
- [MerLean repository README, current `master`](https://github.com/MerLeanProver/MerLean/blob/master/README.md)

## 值得借鉴的字段与算法

### 1. DAG 节点的可审计投影字段

可将以下字段映射为本系统的派生视图，而不是替换本地模型：

| MerLean 字段 | 本地对应/用途 | 接入条件 |
|---|---|---|
| `statement_id`, `name`, `content`, `type` | `ProofNode.id/name/statement` 与 theorem kind | 保留本地 canonical statement identity |
| `dependencies`, `dependents` | `ProofNode.dependencies` 与 registry invalidation | 依赖必须可追溯到 edge origin；Lean 同步不能静默抹掉人工/数学依赖 |
| `proof`, `anchor`, `lean_path`, source span | proof sketch、证明工件、Lean 声明位置 | 只作 provenance，不能当作已验证证明 |
| `declarations_defined`, `imports`, `mathlib_types` | 本地 `graph.py` 的声明图/类型信息 | 标记 extractor 版本、commit、文件 hash 和是否完整 |
| `hierarchy_level` | frontier 层级、并行分组 | 作为调度提示；实际可关闭性仍由 `model.py` 的依赖状态决定 |
| `corrections`, `do_not_import` | repair history、禁止复用记录 | 不得绕过 registry admission |
| status history、subagent metrics | 本地 attempt/agent history 的展示投影 | 只记观察事实，不升级证明状态 |

本地已有的 [model.py](../src/percolation_workflow/model.py)、[store.py](../src/percolation_workflow/store.py)、[graph.py](../src/percolation_workflow/graph.py) 已覆盖这些概念的大部分，并且额外有 checkpoint checksum、attempt history、frontier closability、cycle validation 和证据阶段，因此应采用 adapter/projection，而非重写。

### 2. 纯图算法

值得移植思想或用现有本地实现对齐：

1. deterministic topological ordering；
2. cycle detection；
3. forward dependency cone，用于父节点/下游 registry 失效传播；
4. dependency levels，用于识别同层独立 frontier；
5. 从依赖边重算 `dependents`，避免双向索引漂移。

这些算法可以生成 `statements.json`/`progress.json`/`analytics.json` 的派生快照，但快照不能反向成为权威写入入口。

### 3. Lean graph reconciliation

可以借鉴 `lean_sync.py` 的最小能力：扫描实际 Lean 声明，记录 `declarations_defined`、`imports`、source spans，并把声明使用关系映射为候选 DAG edge。接入本系统时必须保留 edge provenance，例如 `lean_type`、`lean_value`、`import`、`constructor`、`manual`、`external`，并把解析失败、未定位声明和 extractor 版本不匹配记录为 pending/blocked。

本地 [graph.py](../src/percolation_workflow/graph.py) 已有 declaration graph、reachable graph 和 elaborated types 的边界；MerLean 的同步结果应进入该层作为候选/审计输入，而不是直接改写 verified 节点或 registry。

### 4. Informal notes 与语义检索

Note 的 provenance 形状值得借鉴，用来保存 proof sketch、阻断原因、agent 结论和外部来源。正式节点与 Note 必须分桶，Note 只能辅助 frontier 排序/检索，不能构成 theorem dependency 或 verified evidence。

语义检索可作为非关键路径的辅助功能；关键调度路径必须有无 API、无向量库时仍可用的 deterministic fallback。

## 不能直接接入的部分

### Mem0/Qdrant 不能成为权威状态库

MerLean `config.py` 强制 OpenAI API key，并把 embedding/LLM/Qdrant/history DB 作为核心运行依赖。模型或 embedding 维度改变还需重建向量库。对于我们的长期研究状态，这会引入网络、费用、凭据、模型漂移和不可复现性；也不应让向量数据库承担事务 checkpoint、receipt 完整性或 registry 原子更新。

另一个工程风险是 `store.py` 的加载依赖大上限 `top_k` 的 Mem0 retrieval，且 `close()` 对持久化/关闭异常采取吞掉错误的策略。该行为不符合本地 [store.py](../src/percolation_workflow/store.py) 的 checksum/fail-closed 要求：状态写入失败必须可见，不能留下“看起来成功”的证明进度。

### `completed`/`completed_axiom` 不能映射为 verified

MerLean 将 `completed` 与 `completed_axiom` 纳入 completed IDs，并且 `sync-lean` 的无 sorry/可选 build 状态可以推动其完成。这对通用 plan graph 有用，但对本系统不充分：

- 无 `sorry` 不等于正确绑定到目标定理；
- Lean 文件可编译不等于外部数值/SOS/DH 证据已经 exactized 并绑定；
- axiom 结果不能自动进入 kernel-verified theorem registry；
- 不能跳过 comparator、manifest freshness、coverage、remainder、flowpipe、terminal transfer 等 admission 条件。

本地 [registry.py](../src/percolation_workflow/registry.py) 和 [model.py](../src/percolation_workflow/model.py) 的边界必须保持：只有明确成功的 attempt、匹配 statement identity、来源证据、子节点闭合、comparator/verification manifest 和显式 Lean-verified evidence stage 同时成立时，才可注册。编译候选、外部研究结论、`EVIDENCE_COMPLETE`、`completed_axiom` 和 Note 都必须停留在 pending/rejected/非 registry 层。

### 不能直接采用其 graph-authoritative 假设

MerLean 的原则是“graph == Lean dependency graph”。我们的 theorem DAG 还表达数学分解、外部 source binding、checker receipts 和物理/分析前提；有些依赖不会出现在 Lean declaration usage 中。因此 Lean edges 应是一个带 provenance 的强证据层，而不是删除所有数学依赖的唯一规范图。若两者不一致，标记冲突并阻断 parent closure，不能静默覆盖。

### 不能直接采用 reset/delete 和自动 close 语义

`reset`/`delete` 适合 plan-store 生命周期，不适合我们的持久研究状态。任何失效应走可追溯的 invalidation event，保留 attempt、Lean error、receipt 和 agent history；registry promotion 必须与派生视图写出分离。

## 依赖与许可证注意事项

- 直接运行上游 `plan_store` 至少会带入 Mem0 2.x、spaCy、Qdrant、python-dotenv、OpenAI API 凭据和相应模型配置；这不是当前 percolation workflow 的必要依赖。
- embedding 结果绑定模型和维度；不能把不同模型的向量混在同一个库中。离线/CI 环境应能完全绕过语义检索。
- 上游 README 标明 MerLean 及其相关组件采用 Apache-2.0，并在仓库提供 `NOTICE`。若未来复制任何代码而不是仅借鉴接口/算法，必须固定 upstream commit、保留原版权/NOTICE、记录文件来源和本地改动；本审计没有复制代码，也没有新增第三方依赖。
- GitHub `master` 是可变引用；实现级借用前应下载并记录具体 commit、许可证文件和依赖锁定信息，不应只记录 branch 名。

## 最小集成边界

建议的最小方案是一个无外部依赖的**只读 MerLean-compatible projection**：

1. 输入本地 `WorkflowState`，输出 formal nodes、informal notes、topo/levels/cone/cycles 和可选 `statements.json`/`progress.json`/`analytics.json`；
2. 输出中保留本地 `status`、`evidence_stage`、receipt IDs、source hashes、manifest identity 和 `registry_status`，不把字段压扁成 MerLean 的 completed；
3. 对 Lean 同步只调用/复用本地 `graph.py` 的声明图能力，输出带 edge provenance 的审计结果；解析不完整即 pending；
4. Notes/Summary 仅供检索、解释和 agent 规划，不进入 DAG、frontier closure 或 registry；
5. 投影函数必须不修改传入 `WorkflowState`，不写 authoritative checkpoint，不调用 registry promotion；
6. 任何 projection 与本地 DAG、Lean graph、manifest 或 receipt 不一致时，产生冲突诊断并保持 fail-closed；
7. 语义搜索作为可插拔 sidecar，默认 deterministic lexical/metadata 查询，不能阻塞 Lean verification 或 CI。

因此，MerLean 最适合提升我们“组织和检索研究状态”的能力；它不能提升 kernel 证明强度，也不能替代本地 admission/registry。真正的集成收益应集中在 DAG 视图、依赖变更审计、frontier 分层、失效锥和带 provenance 的研究笔记上。

## 明确的验证边界

MerLean `plan_store` 的 node status 是计划管理事实，不是 Lean kernel 事实。本系统只有在 Lean 编译/检查通过、声明和目标 identity 匹配、禁止 axiom/sorry 条件满足，并且所需外部数学 receipt 与全局 comparator/admission gate 均通过后，才允许把节点写入 verified registry。任何从 MerLean 导入的节点先标记为外部/待审计状态；不能因其 `completed`、`completed_axiom`、有 `.lean` 文件或 `sync-lean` 成功而关闭 theorem parent。
