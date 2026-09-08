---
kind: review_result
review_id: review-GH-LEAN-BODY6-PATHCONTRACT-RECEIPT-HANDOFF-20260908T113233
task_id: GH-LEAN-BODY6-PATHCONTRACT-RECEIPT
source_agent: codex-local
created_at: 2026-09-08T11:32:33-06:00
inspected_commit: b4f4f35093c375615dfe024cb40bf51ee70a07b1
proof_status: OPEN_UNCOMPILED
integration_status: pending
admission_label: pending
compile_performed: false
registry_mutation: false
formal_certificate_allowed: false
requested_action: Schedule the isolated BODY6 packet in the next authorized GitHub Lean execution; keep physical-instance admission separate.
---

# BODY6 下一次 GitHub execution packet

新增 examples/routeb_b45_source_comparator_lean/ 下三个文件：

- NEW_BODY6_PATHCONTRACT_HANDOFF_Inputs20260908.json：固定 source commit、
  Lean/Mathlib pin、16 个项目模块的源路径/hash/import 与拓扑编译顺序。
- NEW_BODY6_PATHCONTRACT_HANDOFF_Execute20260908.md：隔离 overlay 布局、fresh
  OLean 入口、API/Fin/source 风险、receipt 字段及失败分类。
- NEW_BODY6_PATHCONTRACT_HANDOFF_Receipt20260908.json：默认 NOT_RUN/MISSING/
  pending；所有 physical field witnesses 均为空，不冒充运行结果。

仅读取文件、git/哈希及静态 import；没有执行本机/远程 Lean/Lake 或 comparator。
旧 candidate/probe 未改，未写 state/registry/shared adapter。

## 固定输入

Candidate SHA256：ff5e2dfbcf0375d96cce232c739e0098381ce5b1828f7142dae23ac3e86a68fc。
Probe SHA256：78cd395e47fc5edc7e781ba1574562ddcb8fa41135c0c3e8613cdcbfd7e98206。
两者均位于上述 inspected commit。Target pin 从 local_fkg 文件锁读取为
Lean v4.32.0、Mathlib 81a5d257c8e410db227a6665ed08f64fea08e997；没有执行版本探测。

16 个静态项目模块全部唯一解析，无未解模块；项目 closure 止于 Mathlib，
没有把它声称为完整 Lean/Mathlib closure。runner 必须记录真实完整依赖、
cache/lock 身份并与项目清单对账。目录里旧 OLean 不作为输入证据。

## 执行终点

只依拓扑顺序编译这条 typed contract/probe 的项目依赖，获取两个原 theorem
及 probe wrapper 的类型/axiom 输出。该 closure 不含 AXIS/STEP6 第六列证明链，
所以成功不能提供 sourceIdentity 的实际 witness。

五个字段 projection/inclusion/physicalIdentity/sourceIdentity/canonicalCap 必须
在相同 embed/qOf/domain/Omega/path/rows/physicalRow/cap 下各自取得真实实例。
Prop structure、#check、假设 h 和 wrapper 均不是 physical inhabitant。
Canonical 值等式也不是 raw body/Fin/频率/系数标签 provenance。

没有 approved comparator 时返回 COMPARATOR_MISSING，不制造通过输出。
环境/资源失败、API 错误、哈希或 statement 不符、公理问题须分别分类。
即便以后编译成功，也只允许 compiled_candidate/pending；下一次排班不得
据此修改 registry/state 或宣称物理 VERIFIED。本轮仅交付执行材料。
