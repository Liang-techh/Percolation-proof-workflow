---
kind: review_result
task_id: T-FLT-INFRA-REGISTRY
source_agent: Codex
integration_status: pending
---

审计对象是 `C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem` 的固定 commit `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`。

结论先说：这套仓库的“证明内容”本身不适合直接迁移，但它的基础设施切分很适合借鉴到本地 theorem DAG / frontier / verified registry / obstruction tracking。最有价值的是它把“文本层证据”和“可升格的状态”严格分离了，且每一步都有可重放的输入边界。

可迁移到本地的结构

1. comparator 的双边对照契约

`verification/comparator/Challenge.lean` 与 `verification/comparator/Solution.lean` 把同一条定理写成 binder-for-binder 的对照：

- Challenge 侧只给出 Mathlib 引入和 `sorry`，用于固定语句边界；
- Solution 侧只依赖 `Theorems.Thm_fermat_last_theorem`，用于固定实现边界；
- `verification/comparator/config.json` 明确白名单：`challenge_module`, `solution_module`, `theorem_names`, `permitted_axioms`, `enable_nanoda=false`。

这很适合本地的 verified registry：

- registry 条目应当同时保存“挑战句式”和“解决句式”；
- promote 之前只允许与白名单契约一致的桥接；
- 语句一致性要单独作为一类证据，而不是混在证明完成状态里。

2. FinalCheck 的最小公理门

`FinalCheck.lean` 只有两件事：`#print axioms fermat_last_theorem` 和一个到 `FermatLastTheorem` 的桥接定理。它把“最终成果是否只依赖允许的公理”压成极小的核验点。

这可直接借到本地 registry：

- 对每个候选定理保留一个 FinalCheck 风格的最小门文件；
- 只检查允许公理、桥接命题和最终导出，不把中间辅助 lemma 一起升格；
- 任何“候选通过”都只能进入 pending，不能直接进入 verified。

3. PROOF-PATH 的 route/landmark 语义

`PROOF-PATH.md` 做得最值得复用的是它把整套证明拆成 7 个阶段，并且每个阶段都明确指出：

- 该阶段的 theorem 名称；
- 该 theorem 的职责；
- 哪些 classical inputs 的“强度”是被证明的，哪些没有被证明。

这正对应本地的 DAG / frontier 设计：

- DAG 节点最好有 stage 字段；
- frontier 只应吸收“当前 stage 已完成且契约闭合”的节点；
- landmark 不应只是“名字出现过”，而应当有手工审核过的阶段归属；
- obstruction tracking 应该记录“这一步证明了什么强度，没证明什么强度”。

4. docs-site 的 graph extraction / render / selfcheck

`tools/docs-site/gen/extract.py`、`graphdata.py`、`render.py`、`selfcheck.py` 这条链的设计很适合本地文档或 registry 站点：

- `extract.py` 只读 `.lean` 文本，生成 `thm.jsonl` / `sol.jsonl` / `def.jsonl`，不运行 Lean；
- `graphdata.py` 只从 JSONL 和 route 文本计算图结构，显式区分 citation edges、statement hops、definition hops、depth、below、landmarks、stage；
- `render.py` 把可视化和文档生成与 proof 内容解耦，且把数学与 HTML 片段做了严格净化；
- `selfcheck.py` 作为输出门，扫描 forbidden tokens、绝对路径、裸 URL、hex-like tokens、raw TeX 和可疑 markup。

本地 theorem DAG/frontier 可以直接借鉴：

- 抽取层只做文本化事实提取，不做语义升格；
- 图层只做可追踪的关系计算；
- 渲染层只做展示；
- selfcheck 层负责阻断“生成出来但不该被发布”的内容。

不能直接升格的证据

1. comparator / FinalCheck 只能说明“命题和公理边界一致”，不能说明本地 registry 已经 verified。

证据点：

- `Challenge.lean` 的证明体是 `sorry`；
- `config.json` 只是白名单配置，不是核验本体；
- `FinalCheck.lean` 只是 axioms print 和桥接，不含独立核验逻辑。

所以本地如果要升格，必须另有核验步骤；不能把这种对照文件本身当成 verified proof。

2. `PROOF-PATH.md` 的 stage 描述是 route 文本，不是机器证明。

它明确写了“the Lean is right”之类的叙述，但这仍然是人工整理的路线说明。能借鉴的是阶段划分与强度标注，不是把 prose 当作 machine-checked evidence。

3. docs-site 的 DAG 是文本抽取图，不是逻辑依赖图的完整真值表。

`extract.py` 和 `graphdata.py` 明说了几个边界：

- citation edge 只是 `import Theorems.Thm_…` 的上界；
- `below` 是 import closure 计数，不是最小语义依赖集；
- statement hops / definition hops 只是从已知节点扩展出来的可达性补丁；
- `selfcheck.py` 只能阻止输出污染，不能证明图的语义正确。

所以本地 registry 不能把“可达”误当成“已证明依赖闭包完整”，也不能把“已渲染”误当成“已验证”。

4. NOTICE / ATTRIBUTION 证明的是 provenance 和 license，不是正确性。

`NOTICE` 明确了 Apache-2.0、Mathlib、FLT project、flt-regular 以及 web bundle 的第三方来源；`ATTRIBUTION.md` 进一步按文件列出处和 extent。它们是必须保留的 provenance 证据，但不能上升为 theorem validity 证据。

适合本地直接复用的契约

- `challenge` / `solution` 双文件模式；
- `permitted_axioms` 显式白名单；
- `FinalCheck` 作为最小门；
- route/stage/landmark 的人工审核表；
- 抽取-图计算-渲染-selfcheck 四段式流水线；
- provenance 与 license 单独登记，且与 verified 状态分离；
- “pending / rejected / verified” 三态，不允许由编译产物直接跳 verified。

已核对的路径与命令

- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem rev-parse aa2d8b3`
- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem show aa2d8b3:verification/comparator/Challenge.lean`
- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem show aa2d8b3:verification/comparator/Solution.lean`
- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem show aa2d8b3:verification/comparator/config.json`
- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem show aa2d8b3:FinalCheck.lean`
- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem show aa2d8b3:PROOF-PATH.md`
- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem show aa2d8b3:formalization.yaml`
- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem show aa2d8b3:NOTICE`
- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem show aa2d8b3:ATTRIBUTION.md`
- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem show aa2d8b3:tools/docs-site/README.md`
- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem show aa2d8b3:tools/docs-site/gen/extract.py`
- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem show aa2d8b3:tools/docs-site/gen/graphdata.py`
- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem show aa2d8b3:tools/docs-site/gen/render.py`
- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem show aa2d8b3:tools/docs-site/gen/selfcheck.py`
- `git -C C:\Users\z5242\Desktop\重构版\工作流\upstream\anthropics-fermats-last-theorem show aa2d8b3:tools/docs-site/gen/build.py`

Provenance / license

- 目标仓库 commit: `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`
- 项目声明：`formalization.yaml` 记载项目为 “Fermat's Last Theorem in Lean 4”，作者 `Anthropic`，license `Apache-2.0`
- `NOTICE` 记载第三方来源：FLT project、flt-regular、Mathlib，以及 docs-site bundle 里的 KaTeX 和 Graphviz 组件及其许可证
- `ATTRIBUTION.md` 是逐文件 provenance 表，区分了 FLT project、flt-regular 和 Mathlib 的材料范围与 extent

约束说明

- 未运行全仓 build。
- 未修改 `state / registry / task_queue`。
- 这里只新增本 review 文件。
