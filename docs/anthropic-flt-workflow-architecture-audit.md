# Anthropic FLT workflow architecture audit

审查对象：`upstream/anthropic-fermats-last-theorem`。本审查只读上游文件并把结果映射到本仓库现有的 theorem DAG、frontier、registry、obstruction tracking；没有运行 Lean、Lake、comparator、nanoda 或 docs build，没有改动 state/registry，也没有搬运数论证明。

## 结论摘要

上游最值得复用的是分层边界：

1. Lean source 是 theorem statement 的权威来源，证明模块的显式 import 是 citation edge 的可审计来源。
2. 从 source 派生 build-time graph，再生成只读文档数据；派生数据不反向成为证明状态。
3. comparator、second-kernel、source/toolchain/attribution 都是独立 evidence lanes，不能互相替代，也不能直接注册 theorem。
4. 路线文字、landmark 和 exact-strength 说明适合作为导航/审计 overlay，不适合作为闭合条件或调度真值。

这与本仓库当前的 fail-closed 设计相容：`WorkflowState`/registry 继续是权威状态；上游结构最多作为 external read-only projection、candidate receipt 输入或文档导出层。

## 上游架构的静态形状

### 1. `PROOF-PATH.md`：人工路线与边界说明

`PROOF-PATH.md:3-7` 明确了一个很好的 source-of-truth 规则：定理在 `Theorems/`，证明在 `P2M/Sol/`，证明模块中 `import Theorems.Thm_...` 的定理就是它引用的 theorem；文字与 Lean 不一致时以 Lean 为准。后半部分还逐项写出 named theorem 的实际假设和未覆盖的更强版本（`PROOF-PATH.md:81-97`）。

它不是 DAG 数据库，而是：

- proof route 的章节目录；
- 对关键节点的人工 landmark 选择来源；
- “这个名字到底证明了什么”的 scope/strength ledger；
- 对 imported/adapted material 的阅读入口。

可直接迁移的结构是“路线文档引用 canonical node IDs，并单独记录 exact strength / not claimed”。不能直接迁移的是把章节编号、文字中出现的名字或人类叙述当成依赖边；上游 `graphdata.py` 也需要用人工 `landmark_stages.json` 覆盖自动推断的 stage（`graphdata.py:125-150`），这本身说明路线不是自动证明事实。

### 2. `P2M/Util.lean`：证明适配器工具，不是 workflow state

`P2M/Util.lean:3-21` 的 `p2m_exact_reverting` 会回退显式上下文、按目标类型 elaboration 一个 proof term，并拒绝未赋值 metavariable。`#p2m_type_eq` / `#p2m_type_eq_warn`（`P2M/Util.lean:23-56`）检查 statement 与 proof card 的类型相等或发出非致命 warning；`p2m_ns`、`p2m_open`、`p2m_export`、`p2m_alias` 等命令处理 namespace/alias 兼容层（`P2M/Util.lean:58-127`）。

可直接迁移的只有这个原则：把“statement identity/type equality”作为 adapter gate，并把 proof-card 与实现 proof 解耦。它适合映射为本仓库的 statement index / comparator manifest 字段，或作为一个 Lean-side preflight。

只能架构借鉴的部分：这些宏依赖 Lean elaborator、P2M namespace 和具体 port 约定；它们不是 DAG edge validator、不是 axiom audit、不是 registry admission。`p2m_exact_reverting` 的成功也不能推出 theorem 已进入 `LEAN_VERIFIED`。

### 3. `tools/docs-site/gen`：三阶段派生 pipeline

上游 generator 清晰分成：

- `extract.py`：只读扫描 `Theorems/`、`P2M/Sol/`、`Definitions/`，流式输出 `thm.jsonl`、`sol.jsonl`、`def.jsonl`（`extract.py:1-18`）。它记录 qualified name、context、imports、proof tail、helper 数、axiom print 次数和 definition declarations；解析规则是针对 `p2m_exact_reverting` tail 的文本启发式（`extract.py:37-83`）。
- `graphdata.py`：从 JSONL 构造 citation DAG，检查未匹配 statement/citation、计算反向 adjacency、BFS depth、topological order、整数 bitset closure 的 `below`/height，并记录 definition/statement hop 与 edge provenance（`graphdata.py:32-120`、`graphdata.py:180-200`）。
- `render.py`：读取 `graph.json` 产生静态页面、shards、定义索引、路线页和图；数学文本先由 KaTeX 严格解析，生成英文层还会做相对链接/HTML 白名单处理（`render.py:223-265`、`render.py:268-354`）。
- `selfcheck.py` / `qa_filetest.py`：分别做输出禁词、绝对路径、外链、raw TeX、markup 和 `file://` 浏览器行为检查（`selfcheck.py:1-28`；`qa_filetest.py:1-16`）。

这条“extract -> graph -> render -> selfcheck/QA”的分离可以直接迁移为本仓库的 read-only graph export pipeline。特别值得保留：流式中间 JSONL、明确的 build 目录、失败记录而不是静默丢弃、图快照 hash，以及生成层不写 workflow state。

不能直接迁移的是 parser 本身：它假设固定目录、固定 theorem/proof 命名和特定 P2M tail；它只读 import 文本，不是 Lean kernel dependency proof。对本仓库，应继续使用已有的 `graph.py` 编译声明图/definition projection，并把上游 parser 作为外部 FLT 适配器，而不是替代当前图导入器。

### 4. `html/data` 与图形运行时：高效只读 projection

本次静态检查到的上游生成规模是 29,511 个 theorem node、106,853 条 citation edge、1,450 个 definition module；`html/data` 采用平行数组和压缩稀疏行边表：

- `meta.js` 保存 `names`、`root`、`depth`、`below`、`height`、`parent`、`pkind`、`via`、`stage`、`lm`、`dup`、`defs` 等元数据；
- `edges.js` 保存 `off` + `dst`，其中 `off[i]:off[i+1]` 是 node `i` 直接引用的 theorem IDs；
- `site.js:39-55` 在浏览器端从 CSR 反推出 `citedBy`；
- `titles.js` 与 `data/shard/NNN.js` 将可选标题/大块 theorem record 与主元数据分离；256 个 shard 通过 name hash 懒加载（`site.js:158-168`）；
- definition declarations 另存为 `ddecl.js`，用于 source/field links，不混入 theorem citation edge。

这套“immutable snapshot + parallel arrays/CSR + reverse index + lazy shards”可直接迁移到只读 frontier/DAG 报告或静态审计页面。`depth`/`height`/`below` 也可作为现有 frontier closability 的解释性指标。

但它不能成为权威 DAG：上游页面把所有 theorem 标为 proved，`stage`/`landmark` 是路线标签，definition dotted edge 是展示关系；它没有 `NodeStatus`、attempt、lease、evidence stage、obstruction gate 或 registry freshness。Graphviz/WebAssembly、classic global scripts 和 `file://` 兼容是展示实现，只能借鉴，不能进入核心状态模型。

### 5. `verification/comparator`：独立的 statement/proof 对照门

`config.json:1-3` 固定 challenge/solution module、theorem names 和 permitted axioms。`Challenge.lean` 只声明目标并使用 `sorry`，`Solution.lean` 从 `Theorems.Thm_fermat_last_theorem` 导入实际结果，再以 binder-for-binder 的 wrapper 对照 challenge（`Challenge.lean:3-14`；`Solution.lean:3-12`）。

`run.sh` 的可迁移契约是：

- comparator command/config/toolchain 必须由可信 coordinator 固定；
- challenge、solution、lakefile、config、toolchain 和实际 source inputs 要形成可重放的 hash-bound bundle；
- 成功同时要求 exit code 0 与日志最后的精确 acceptance line `Your solution is okay!`（`run.sh:52-75`）；
- wrapper project 与被验证 tree 隔离，且成功结果只产生 verification evidence。

这与本仓库 `comparator.py`、`verification.py`、`CandidateReceiptAudit` 和显式 registry promotion gate 是高度同构的，属于可直接迁移的接口思想，甚至不需要搬上游脚本。

只能借鉴的部分是脚本实现：它会 clone/build comparator 与 lean4export，建立 symlink farm，并且注明完整 comparator 约需约 15 小时、约 230 GB resident memory（`run.sh:1-14`）。本次没有运行它。它的资源模型、Linux/bash 假设和外部工具获取不应进入普通 frontier 调度；若要运行，必须另设显式 expensive verification lane。

### 6. `verification/nanoda`：可选 second-kernel evidence lane

nanoda 配置固定导出文件、线程数、允许 axioms、要 pretty-print/check 的 declaration 和精确成功输出（`nanoda-config.json:1-31`）。`run.sh` 先重用 comparator 的 export/wrapper，再以 pinned commit、明确 patch set、export hash、run status 和 `Checked <n> declarations with no errors` 作为独立检查结果（`run.sh:1-14`、`run.sh:27-63`）。patch 文件中的 instrumentation 只增加 per-declaration START/DONE 日志；其它 E1-E3 是搜索顺序/缓存工程改动，脚本明确声称不改变 typing rules（`patches/instrumentation.diff:4-21`）。

可直接迁移：把 second-kernel 结果作为带 revision、patch set、input/export hash 的可选 receipt，且与默认 Lean/comparator 结果分栏保存。只能架构借鉴：Rust patch、内置 declaration 列表和极高内存/磁盘/时间需求。nanoda 不应自动改变 node status，也不应成为所有 frontier item 的先决条件。

### 7. `ATTRIBUTION.md`：file-level provenance ledger

`ATTRIBUTION.md:1-8` 说明了方法、覆盖范围、匹配阈值和局限；表格区分 whole file、port、adapted、portions，并保留 upstream path、commit、copyright holder、authors（例如 `ATTRIBUTION.md:106-134` 的 intermediate FLT port 与 flt-regular 项目）。它还明确指出 source tree coverage、未记录 commit、line matching threshold 等不确定性（`ATTRIBUTION.md:136-142` 及 §5）。

可直接迁移：将 attribution/provenance 作为每个 external candidate、source bundle、definition import 的 metadata，并记录 `repository/commit/license/toolchain/mathlib_revision`、覆盖类型、来源文件和验证状态。必须保留“不确定/未重查”状态，不能把 attribution 表当作 theorem validity。

只能借鉴：上游的数十页逐文件表和特定 line-matching 规则不适合塞进 registry；本仓库只需可查询的 manifest/receipt 引用和一个审计文档。FLT、Imperial FLT、flt-regular 及 Mathlib 的证明材料均不在本次迁移范围。

## 对本仓库四个核心面的映射

| 目标面 | 可吸收的上游结构 | 必须保持的本仓库边界 |
|---|---|---|
| theorem DAG | canonical names；显式 citation edges；definition/statement hop 单独标注；`depth`/`height`/closure；图 snapshot hash | 优先使用 `graph.py` 的 compiled declaration graph 和 `graph_artifacts`；HTML/PROOF-PATH 只能是外部 projection；任何新 edge 影响已 verified node 时仍需显式 invalidation |
| frontier | 将 route stage、landmark、closure size 作为解释性排序/视图字段；CSR 快照便于 UI | 不把 stage/landmark 当 eligible；继续由 `WorkflowState.frontier()`、obstruction gate 和 `build_frontier_cut()` 决定可调度性 |
| registry | comparator config、challenge/solution mirror、exact acceptance line、source/toolchain/axiom/export hashes、独立 receipt | 编译或 comparator 成功都只到 `compiled_candidate` / `SOURCE_COMPARATOR_PENDING`；必须经过当前 `LEAN_VERIFIED`、依赖闭合、manifest freshness 和 coordinator-only `_register_verified` |
| obstruction tracking | 将失败日志、QA failure、second-kernel progress 保存为 evidence；route 的 exact-strength 文字可生成 manual-review reason | 上游没有 obstruction semantics；不得从“页面未覆盖”“stage 未赋值”推断数学 blocker。继续使用显式 `math_lane`/`math_bottleneck`、diagnostic-only repair record 和 fail-closed unknown 分类 |

一个关键差异是 edge 语义：上游 citation edge 是 proof module 的 theorem import；本仓库 `graph.py` 还会把 compiled declaration 的 type/value dependencies 经过 definition/helper 投影为研究 DAG。两者可以并列保存并通过 `edge_provenance` 区分，不能无标签合并成一个“已证明依赖”。

## 低风险最小集成顺序

以下顺序不要求搬任何 FLT 数论，也不要求改变现有 state/registry schema：

1. **先做 provenance-only intake。** 继续使用 `external_catalog.py` / `advisory_reuse.py` 的只读边界；若需要，增加 `proof_path_ref`、`attribution_ref`、source commit/toolchain/Mathlib pin 字段。外部条目仍只能是 advisory，纯数论条目保持 provenance-only。
2. **增加纯函数 graph snapshot adapter。** 输入上游 `html/data` 或经过人工确认的 source-derived JSON，输出 canonical names、CSR edge arrays、reverse index、root、source digest、edge origin 和 counts。检查 duplicate/dangling/self edge、root existence、offset monotonicity、snapshot hash；不写 `WorkflowState`。
3. **只把 snapshot 投影到现有 frontier receipt。** 以 `project_frontier_receipt()` / `build_frontier_cut()` 的模式，把 `depth`、`below`、landmark/stage 和 source digest 作为 advisory rows；不创建 attempt、不改 evidence stage、不改 scheduler eligibility。
4. **加入路线/landmark overlay。** 解析 `PROOF-PATH.md` 的章节和 canonical names，生成 `route_stage`、`landmark_source`、`exact_strength_note` 的只读索引。人工 override 要显式落盘并带来源；缺失或冲突应报告为 review，而不是自动补边。
5. **复用 comparator sidecar 契约。** 将上游 config 的 module/name/axiom 字段映射到现有 `build_comparator_manifest()`；保留 source/OLean hashes、toolchain/Mathlib pins、strict-admission/axiom report、exact acceptance line 和 receipt self-hash。结果默认 `registry_status=pending`。
6. **最后才启用 nanoda lane。** 只有在 comparator/Lean evidence 已有且用户明确要求时，记录 pinned nanoda revision、patch list、export hash、stdout/stderr 和 resource metadata。它是 second-kernel receipt，不是 registry promotion，也不应阻塞无关的 frontier 工作。
7. **可选做静态 UI 导出。** 以现有权威 state/DAG 生成 CSR/shards/route pages；单向导出，禁止从 HTML data 反写 state。selfcheck/QA 作为发布前检查，不作为 theorem admission。

在第 2 步之前没有必要复制上游 `gen/`；在第 5 步之前没有必要接入 comparator 脚本；在第 6 步之前没有必要获取 nanoda。这样能把风险限制在纯函数、可丢弃的 build artifacts 和 provenance metadata 内。

## 明确不迁移项

- `P2M/Sol` 中的 FLT/Imperial FLT/flt-regular 数论证明和任何 proof term；
- `P2M/Util.lean` 的 namespace/export 宏作为 Python workflow API；
- `html` 静态站点的 classic-global/Graphviz/WebAssembly/KaTeX 运行时作为核心状态依赖；
- comparator/nanoda 的长 build、clone、symlink farm、Rust patches 和机器资源假设；
- 从 landmark、页面颜色、`proved` badge 或生成英文文本推导 `LEAN_VERIFIED`、registry entry 或数学 obstruction；
- 用 `ATTRIBUTION.md` 的历史/版权记录替代当前 source hash、toolchain pin、axiom/strict-admission 和 exact comparator receipt。

## 审查状态

本次只新增本文件。上游文件保持不变；本仓库现有未跟踪的 `examples/routeb_fourier_payload_lean/` 也未触碰。未运行长 build 或任何会生成/修改验证状态的命令。
