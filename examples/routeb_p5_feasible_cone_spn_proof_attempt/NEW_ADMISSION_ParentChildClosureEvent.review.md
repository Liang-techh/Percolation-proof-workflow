# Admission：parent/child closure → append-only event

日期：2026-09-07。状态：**OPEN_UNCOMPILED**。
新增 `NEW_ADMISSION_ParentChildClosureEvent.lean` 与本 review。
只进行静态契约审查；不运行本地 Lean/Lake，不读取或写入实际 registry 状态。
未修改原 transition、共享脚本或 registry。

## 现有接口的实际边界

直接消费 `RouteBFixedLambdaAppendOnlyRegistryTransition.AppendOnlyVerifiedRegistryEvent`。
旧 event 已要求 verified-entry evidence、final/kernel admission、comparator/source 绑定、
独立 promotion authorization、fresh entry ID 等。新契约包裹原 event，不重新制造这些证据。

现有 `ParentClosureComplete` 只要求 parent_entry_id 与 closure_digest 非空。
它不证明该 parent 在当前快照中、其 hash/statement 匹配，或其数学/工作流 closure 已完成。
旧 `AppendOnlyTransitionRelation` 另要求 event.parent_entries=before；新包装保留这一关系。

## 最小的额外 typed 证据

`EventContext` 仅整理旧 event 的依赖参数。
`ParentReady` 独立要求：

- event.parent_entries 与实际传入 before 相等；
- expected parent 属于 before；
- parent witness 的 ID/artifact hash/statement digest 与该 parent 全部一致；
- 外部 `parentClosed parent closureDigest` 证明。

`ChildReceipt` 保存 parent/child 完整 identity、snapshot digest，以及可缺失的 closure/kernel/comparator
receipt digests。`ReceiptFieldsComplete` 明确要求 snapshot 非空与后三个 digest 均存在且非空。
`BoundChildReceipt` 另要求 parent/child identities 与当前 parent/event 精确相等、
snapshot 绑定、child closure 证明，以及 `receiptValidForEvent` 的完整外部验证/绑定证明。

字段存在性只是最低层，不是 receipt 有效性的充分条件。
`ClosurePolicy` 的四个谓词提供外部 authority 接口：parentClosed、childClosed、snapshotMatches、
receiptValidForEvent。最后一个必须验证 receipt 对这个具体 event 的旧 evidence bundle、
kernel/comparator、digest/pin 等真实绑定；本文件不计算哈希，也不把任意非空字符串当作验证成功。
该 policy 的正确实现及与权威 closure/receipt 状态的对应关系仍是外部义务。

## Fail-closed transition

`ChildReady` 必须指向实际 `some receipt` 及其完整绑定证明。
`closureDecision` 分别接收 `Option ParentReady` 与 `Option ChildReady`：
仅两者都是 some 时构造 `ClosureApproved`；缺任何证明直接返回 none。
它不对外部谓词猜测、搜索或默认判真，也不调用 comparator/Lean。

新增 proof attempts 覆盖：

- parent proof 缺失、child proof 缺失 → none；
- parent 明确未关闭 → none；
- receipt 不存在 → 不可能有 ChildReady；
- child receipt 字段不完整 → 不可能有 ChildReady，因此 decision=none；
- kernel receipt digest 为 none → receipt 不完整；
- event 快照与 before 不一致 → none。

`approvedAppendRequest` 只能从 ClosureApproved 生成原 `.append event` 请求。
`approved_append_relation` 保留 `after=before++[event.identity]` 与快照一致性；
原 event 的 authorization、证据 bundle 和 freshness 字段没有被替换或删除。
这只是证明级 wrapper，尚未接入真实 dispatcher。原旧 API 本身未修改，
因此不能声称所有调用路径已强制经过这个额外 gate。

## Missing、incomplete 与 rejected 的区别

本 decision 的 none 仅表示“不产生追加事件”，不写状态，也不自动区分 pending/rejected。
缺少权威 closure/receipt 证据通常仍需等待，不能仅凭缺失就断言证据为假；
已有明确不完整/不匹配/无效证据则可由上层按其审计规则拒绝。
证明 `parentClosed` 不成立和没有拿到它的证明是不同情况，二者在新 gate 都不会获得追加许可。
compiled-only 或 comparator acceptance 不能代替 parent/child closure，也不绕过旧独立授权。

本叶没有证明 parent DAG 的全部祖先关闭、closure 的数学语义、真实快照 digest 或实际 receipt 完整性；
这些必须由 ClosurePolicy 的权威绑定覆盖。也不提供并发原子提交或避免快照读取后的竞争，
真实存储层需对同一 before 快照实现条件式提交。

新文件跨目录导入 fixed-lambda sidecar；模块解析及整条导入链的 elaboration/kernel/public axiom
检查均未运行。没有当前 Lean 验证、数学 admission 或 VERIFIED/registry promotion 声明。
