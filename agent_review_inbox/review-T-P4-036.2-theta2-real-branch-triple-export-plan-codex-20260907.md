# O2 T-P4-036.2：真实 branch traversal triple export plan

## Scope

本 review 只寻找真实 branch traversal 产生的同 theta2 namespace
`routeb-theta2-canonical-coverage-v1` parent/child/sibling JSON。GCN、
geometry-only partition 和手写 fixture 均不作为 authority。本次没有运行
branch exporter、回归或 Lean 编译。

## Result: no real theta2 triple receipt

定向检索当前 contract/schema 与真实 branch 输出后，找到的是：

```text
src/percolation_workflow/coverage_receipt.py
  validator implementation only
tests/test_coverage_receipt.py
  synthetic validator fixture only
routeB_interval_branch_bound.jl
  generic branch driver, no theta2 triple JSON
routeB_partition_coverage.json
  geometry metadata only
routeb_theta2_leaf_handoff_20260907/
  leaf-1 handoff + obstruction, no parent/sibling
```

没有找到真实 traversal 生成的
`routeb-theta2-canonical-coverage-v1` JSON，因此本次不产生
contract-compatible 假 receipt。

## Existing producer gap

真实 branch driver 的内部 `BBNode` 已包含：

```text
id, depth, q[6], dq[6], w, eta, sf, parent
```

并且 `split_node` 在内存中创建两个 child；但它当前持久化的 CSV header
只有：

```text
id,parent,depth,status,p_lo,p_hi,h_lo,h_center,h_hi,center_enclosed,kappa
```

当前 opt-in `weighted_payload` 可以输出一个 selected cell 的
`box_lo/box_hi`，但不能输出 parent 与 sibling，也没有 split axis/cut、
同一 triple 的 run receipt 或 external premise hashes。因此已有 traversal
不能直接供 validator 消费。

## 最小 exporter patch 方案

不需要把 parent/sibling 加进 `BBNode`；最小修改是在 branch split event
建立一个独立 triple ledger。

### 1. 保存 canonical 13D endpoint

增加一个只读 helper：

```julia
canonical_box(n::BBNode) = (
    lo = vcat([x.lo for x in n.q], [x.lo for x in n.dq], [n.w.lo]),
    hi = vcat([x.hi for x in n.q], [x.hi for x in n.dq], [n.w.hi]),
)
```

使用现有 `json_value(::BigFloat)` 序列化为字符串，固定：

```text
q1,q2,q3,q4,q5,q6,dq1,dq2,dq3,dq4,dq5,dq6,w
```

不得经由 `Float64` 或普通 JSON number。

### 2. 在 split event 保存 parent/child/sibling linkage

当前 `split_node` 只返回两个 `BBNode`。最小改法是同时返回
`split_index`，并在给 child 分配 id 后写入：

```julia
triple_ledger[n.id] = (
    parent = n,
    child_ids = [a.id, b.id],
    split_index = j,
    split_cut = cut,
)
```

`split_axis` 映射为：

```text
1..6  -> q1..q6
7..12 -> dq1..dq6
13    -> w
```

`cut` 必须从实际两个 child 的共享 endpoint 取得，而不是从启发式参数
重算；对于可能反向返回的 `split_interval` 两个 child，导出顺序可按
endpoint orientation 归一化，或保留 child/sibling 任一方向让 validator
检查。

### 3. 只在三方 endpoint 齐全时导出 canonical JSON

选定一个 child 后，导出对象应严格形如：

```text
schema = routeb-theta2-canonical-coverage-v1
coordinate_order = canonical 13 names
source = receipt_sha256 + generator_sha256 + interval_source_sha256
parent = {id, box_lo[13], box_hi[13]}
child = {id, parent_id, box_lo[13], box_hi[13]}
sibling = {id, parent_id, box_lo[13], box_hi[13]}
linkage = {split_axis, split_cut, adjacency=shared_face}
source_interval_membership = {status, receipt_sha256}
coverage_join = {kind=CoverageJoin2, premise_receipt_sha256}
```

`source.receipt_sha256` 应绑定 branch traversal run manifest，而不是绑定
正在写出的 triple 文件自身，避免 self-hash cycle。manifest 至少应固定
branch driver source、interval source、参数、selected parent id、child ids
和 traversal output hash。

### 4. fail-closed external premises

branch geometry 本身不能填充以下字段：

```text
source_interval_membership.status
source_interval_membership.receipt_sha256
coverage_join.premise_receipt_sha256
```

exporter 应要求这些 external receipt path 已存在并通过 SHA-256 读取；
缺失时只输出 `PENDING_EXTERNAL_PREMISES` obstruction，不能输出会通过
validator 的 `ACCEPTED/PROVEN` canonical triple。这样可以保持 validator
的结构性结果与 dynamics/coverage theorem 边界分离。

## Direct Lean consumer mapping

三方 endpoint 进入 Lean 后的最小 mapping 是：

```text
parent.box_lo/box_hi  -> RectBox13 parent
child.box_lo/box_hi   -> RectBox13 child
sibling.box_lo/box_hi -> RectBox13 sibling
endpoint inequalities -> BoxSubset child parent
                         BoxSubset sibling parent
split-cover premise    -> CoverageJoin2 premise
```

其中前三项和 `BoxSubset` 是可 formalize 的 exact-rational transport；
`source_interval_membership` 与 `CoverageJoin2` premise 仍是外部 receipt
输入。validator 的结构性成功也不自动声称 Lean theorem 已证明。

## Current O2 leaf-1 boundary

[theta2_leaf_1_endpoint_handoff.json](C:/Users/z5242/Desktop/重构版/工作流/artifacts/routeb_theta2_leaf_handoff_20260907/theta2_leaf_1_endpoint_handoff.json)
仍只有 child endpoint + lower-corner witness：

```text
parent endpoint: absent
sibling endpoint: absent
child linkage: absent
source interval membership: absent
CoverageJoin2 premise: absent
authority_status: ENDPOINT_PROVENANCE_ONLY
```

因此本次没有升级 authority，也没有将 GCN/geometry-only 数据接入
theta2 namespace。

## Actual hashes

```text
canonical triple validator source
  B47913A5146B3A9CC496FF7DDB5569361263A1B8002A33AD3023005D83B19F38
canonical triple validator tests
  B8CBEF52C0C23F1E9705366A29C5B223532EED937F7F8E50264D95C3FBA08CEC
real branch driver source
  C5349534FE1D01D87FB886BAE94EA05F373BCBE4E24B9A2C12411A31234C0590
geometry partition receipt
  E2051669922B1213162CFEC4F82EF21E5B5B0DE951AD6CCDF176E972905B713A
current O2 leaf-1 handoff
  9453049983A4F59D0438CE0F51EDD6BC6F6C0E6FDEA91522B524A5828C6709ED
current theta2 Lean adapter source (not recompiled)
  248DACF3BF0749574477EFAB6DFF71DA0DC4684BB05FC1B5210FF5F7C66D17CB
```

本 review 只提交真实 exporter 的最小 patch 方案；在新的 traversal
receipt 产生前，O2 coverage 保持 open。
