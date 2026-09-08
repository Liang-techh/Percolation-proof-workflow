---
kind: review_result
review_id: review-GH-LEAN-FLT-QUOTIENT-CLM-API-REPAIR-HANDOFF-20260908T111356
task_id: GH-LEAN-FLT-QUOTIENT-CLM-API-REPAIR
source_agent: codex-local
created_at: 2026-09-08T11:13:56-06:00
inspected_commit: 8fd0f132c2e4cf4ac99438aa8dc295a7f6592b1b
proof_status: OPEN_UNCOMPILED
integration_status: pending
admission_label: pending
proposed_integration_target: external_catalog_pending_only
compile_performed: false
registry_mutation: false
formal_certificate_allowed: false
---

# 已提交双 quotient probe 的精确 overlay handoff

仅新增本 review。未运行本机或远程 Lean/Lake、receipt、GitHub workflow，未修改
候选、probe、state/registry/shared adapter。未作 compiled/VERIFIED 结论。

## 1. 已提交身份与字节

本轮 git ls-tree HEAD 确认两个文件存在于上述 inspected commit，且针对它们的
git status 为空。原路径前缀 E=examples/anthropic_flt_quotient_transport_sidecar/。

| 对象 | Git blob SHA-1 | 当前文件 SHA-256 |
|---|---|---|
| E/NEW_QUOTIENT_CLM_API_REPAIR_20260908.lean | eeaf00791c7786e7e2ad8779e8d61f27a7574025 | 777d4ae6cd3fa60fb0f988f5b1e263e2cb07536f7ed83113f99aa102615e9e97 |
| E/NEW_QUOTIENT_CLM_API_Probe20260908.lean | d3968f99dcc65d7bbd802dc719f591eb5a99c5ae | 159ddb493ca734675fc6f211e021ca05addb3cb442e6dab5ef71e7c6bd8c936b |

候选直接 imports 的本地 SHA-256（相对下述 Mathlib checkout）：

```text
Mathlib/LinearAlgebra/Quotient/Pi.lean
ff73c44599c96aa489cfaa44781b24ed0acd35cc2476f052323cfd03c3e000c4
Mathlib/Topology/Algebra/Module/Equiv.lean
d5593d64f0471169b7de08bde927e7bb370b7d0c46a610f0abb1fdca6ba01c69
lean-toolchain
a0ada3782cd088719516bbfdf37b9e7032230e211bf424b85d952ee650c51091
```

这两个 import 文件的 git diff 为空；未穷尽确认所有传递依赖或整个 checkout 干净。
跨平台 EOL 转换可改变工作树 SHA；runner 应同时记录 Git blob 与实际编译字节，
若与上述 SHA 不同须明确解释并重新绑定，不能静默声称一致。

## 2. 两套 pin 与原始 source hash

Target checkout：artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib。
本轮只读 HEAD=0df444a360eaa60ab8c11dca51a86af692955474，toolchain 文件为
leanprover/lean4:v4.33.1。没有运行 Lean --version。

Source repo=https://github.com/anthropics/fermats-last-theorem，commit
aa2d8b34692b16c70f699536de0d8e75b9a3e9ef；本轮 git ls-tree 确认
Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean 的 Git blob 为
eab66288efedd1e634203abb927805413a716aa7（Git SHA-1，不冒充 SHA-256）。
upstream Mathlib db584cd6d46c92f209a44c0f1c829460d327499d 来自既有 intake
记录，不能用 target pin 覆写 source provenance。runner 提取源 blob 后再记录其
原始字节 SHA-256；本轮未生成该 SHA-256，也未执行 upstream 编译。

保留 Imperial FLT staging 的 ©2025 Salvatore Mercuri 与 authors Salvatore
Mercuri、Kevin Buzzard、Pietro Monticone，以及 Anthropic commit/path。随 overlay
携带 intake 的 LICENSE/NOTICE/ATTRIBUTION.md，当前 SHA-256 分别为：

```text
LICENSE: 746bc52848eabf8765635fe532e0680756a10b18e7b3fb26e7433ab4edf34034
NOTICE: 42b1821f19a6aaa25e6811d22ab8f2fdc6433d4a37bc810b1cfafa5b6dd6b0b6
ATTRIBUTION.md: 698fb76c8d80b2ed78ebd48b271f2ee5815b3654fb8ec5c699b21b16ce0d9698
```

## 3. 隔离 overlay 布局与入口

GitHub agent 在独立临时目录建立下列布局，不向原目录写入构建产物：

```text
quotient-clm-probe/
  lean-toolchain                     # v4.33.1
  lakefile.toml                      # mathlib git require: exact target SHA
  lake-manifest.json                 # runner生成并记录全部resolved revisions
  NEW_QUOTIENT_CLM_API_REPAIR_20260908.lean
  NEW_QUOTIENT_CLM_API_Probe20260908.lean
  provenance/{LICENSE,NOTICE,ATTRIBUTION.md,source-object-manifest.json}
  out/                               # fresh project OLean only
  logs/
```

不复制含本地 path dependency 的历史 lakefile；不拉入 Anthropic P2M/纯数论。
Mathlib build/cache 必须匹配精确 pin，记录取得方式；out 加入项目 LEAN_PATH，
同时保留 Lake 的依赖路径，并记录最终模块解析路径。然后仅执行：

```text
lake env lean -DwarningAsError=true -o out/NEW_QUOTIENT_CLM_API_REPAIR_20260908.olean NEW_QUOTIENT_CLM_API_REPAIR_20260908.lean
lake env lean -DwarningAsError=true -o out/NEW_QUOTIENT_CLM_API_Probe20260908.olean NEW_QUOTIENT_CLM_API_Probe20260908.lean
```

上述为未执行 handoff，不是两行即可自动建立环境的脚本。第二条必须加载第一条
新 OLean，不能拾取旧本机缓存。不要全仓 build、更新 pin 或执行 registry integrator。

## 4. 必需 receipt 字段

- execution：repo/checkout SHA、GitHub run/job/attempt URL、workflow/actions SHA、
  overlay 清单/hash、runner、时间、实际 Lean version、Mathlib HEAD、所有 lock hashes。
- inputs：候选/probe/import/source 的 Git对象与 SHA-256；递归 import manifest 或
  精确 immutable Mathlib tree + resolved dependency revisions + 所有本地 override。
  本 review 两个直接 import hashes 不能替代完整闭包身份。
- outputs：每条 command/cwd/LEAN_PATH、exit、完整 stdout/stderr URL/hash、新 OLean
  hashes；两个 @定义类型与四个 #print axioms 输出，检查 sorryAx/额外公理。
- comparator：两个 source→renamed candidate 声明映射，source/target pin，完整
  参数/typeclass/结论对照，实际 comparator command/version/exit/log/hash。
  尚无执行则标 missing/manual-only，不因 probe wrappers 类型可用就填 accepted。
  跨 pin 类型比较必须说明桥接方法，不能导入两版 Mathlib 混在一个环境。
- disposition：compile_status 与 source/comparator/admission 分列；成功只允许
  compiled candidate、external catalog pending。缺 receipt 为 pending，已有材料
  hash/statement 不符则明确拒绝，不自动写 registry 或宣称物理定理。

## 5. 最小 API 风险与 repair 建议

probe 的两个 wrapper 完整声明所有 binders，无旧 quotient_transport_mk 问题。
第一项保持 Ring/G/H topological spaces/e/map-submodule equality；第二项保持
CommRing、dependent modules、IsTopologicalAddGroup、Fintype/DecidableEq。
type wrappers 不证明给定 e、p 或物理 quotient 有实际 source/domain 实例。

两个 targeted imports 是否完整提供 convert tactic 与 quotient continuity
instances 未编译确认；重点是 quotientPi_aux.invFun 展开、continuous_finsetSum
显式参数、dependent Pi 类型推断。若仅缺 tactic，建议另建新 repair 显式添加
Mathlib.Tactic.Convert（先核对该 pin 模块），不要改旧候选或加强数学前提。
若结构字段/API 变更，记录精确错误再局部适配；不得用 sorry/native_decide、
漂移 pin、完整 Mathlib 导入掩盖原因。此处仅风险清单，非观察到的 Lean 错误。
