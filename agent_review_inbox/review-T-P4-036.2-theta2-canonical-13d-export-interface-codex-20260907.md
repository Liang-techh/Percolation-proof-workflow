# O2 T-P4-036.2：canonical 13D parent/sibling export interface

## Scope

本 review 只处理当前 theta2 leaf-1 所需的 canonical 13-coordinate
`RectBox13` parent/sibling endpoint 导出接口。没有运行 exporter、回归、
Lean/Lake 编译，也没有把 GCN candidate 接入 O2。

## 当前 source-side 结构

### Branch driver

[routeB_interval_branch_bound.jl](C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_interval_branch_bound.jl)
的 `BBNode` 内部确实有：

```text
id, depth, q[6], dq[6], w, eta, sf, parent
```

`split_node` 生成两个带同一 parent 的 child，并保留 split interval；但
当前持久化 branch CSV 的 header 是：

```text
id,parent,depth,status,p_lo,p_hi,h_lo,h_center,h_hi,center_enclosed,kappa
```

它没有 `box_lo[13]`、`box_hi[13]`、`sibling_id`、`split_axis` 或
`split_cut`。因此内部内存结构接近所需数据，现有 receipt 却无法直接
构造 `RectBox13`。

### Geometry partition exporter

[routeB_partition_coverage_audit.jl](C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_final/routeB_partition_coverage_audit.jl)
和对应 [routeB_partition_coverage.json](C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_final/routeB_partition_coverage.json)
只输出：

```text
13 axes, zero split, product_cell_count=8192
geometry_coverage_complete=true
dynamics_coverage_complete=false
partition_rule / proof_obligation
```

它没有 leaf endpoint、parent/sibling linkage、source interval membership
或 interval classification，故只能作为几何规则 metadata。

### Selected-cell payload

branch driver 的 opt-in payload helper 可以写出 canonical 13D
`box_lo`/`box_hi`，但当前只对一个显式选定 cell 导出；没有同时导出其
parent/sibling endpoints 或 parent coverage relation。这是最小接口可复用的
起点，但不是当前 O2 的 coverage receipt。

## 最小可消费 export contract

若要直接喂现有 Lean-side：

```lean
RectBox13 := { lo : Fin 13 → ℝ, hi : Fin 13 → ℝ, ordered : ∀ i, lo i ≤ hi i }
BoxSubset child parent :=
  ∀ i, parent.lo i ≤ child.lo i ∧ child.hi i ≤ parent.hi i
```

source exporter 对一个 parent/child/sibling triple 的最小 JSON 应为：

```json
{
  "schema": "routeb-theta2-canonical-coverage-v1",
  "coordinate_order": ["q1", "q2", "q3", "q4", "q5", "q6",
    "dq1", "dq2", "dq3", "dq4", "dq5", "dq6", "w"],
  "source": {
    "receipt_sha256": "<64 lowercase hex>",
    "generator_sha256": "<64 lowercase hex>",
    "interval_source_sha256": "<64 lowercase hex>"
  },
  "parent": {
    "id": "<parent id>",
    "box_lo": ["<13 exact strings>"],
    "box_hi": ["<13 exact strings>"]
  },
  "child": {
    "id": "<theta2 leaf-1 id>",
    "parent_id": "<parent id>",
    "box_lo": ["<13 exact strings>"],
    "box_hi": ["<13 exact strings>"]
  },
  "sibling": {
    "id": "<sibling id>",
    "parent_id": "<parent id>",
    "box_lo": ["<13 exact strings>"],
    "box_hi": ["<13 exact strings>"]
  },
  "linkage": {
    "split_axis": "<canonical coordinate>",
    "split_cut": "<exact rational string>",
    "adjacency": "shared_face"
  },
  "source_interval_membership": {
    "status": "<accepted status>",
    "receipt_sha256": "<64 lowercase hex>"
  },
  "coverage_join": {
    "kind": "CoverageJoin2",
    "premise_receipt_sha256": "<64 lowercase hex>"
  }
}
```

真正直接喂 `BoxSubset` 的字段只有三组 `box_lo`/`box_hi` 与相同的
`coordinate_order`；`split_axis`/`split_cut` 只能辅助检查几何相邻，不能
单独推出 inclusion。`CoverageJoin2` 还必须有 parent 内每个点落入 child
或 sibling 的 premise；shared-face metadata 本身不等价于该 premise。

## 当前缺口

当前 theta2 leaf-1 handoff
[theta2_leaf_1_endpoint_handoff.json](C:/Users/z5242/Desktop/重构版/工作流/artifacts/routeb_theta2_leaf_handoff_20260907/theta2_leaf_1_endpoint_handoff.json)
只有 child 的 13D endpoints 与 lower-corner witness：

```text
parent endpoint: absent
sibling endpoint: absent
parent_id/sibling_id linkage: absent
source interval membership: absent
CoverageJoin2 premise receipt: absent
authority_status: ENDPOINT_PROVENANCE_ONLY
```

因此可执行的最小 exporter 变更不是“再导出一个 witness point”，而是
让 branch traversal 在创建两个 child 时持久化一个 triple：

```text
parent box + child A box + child B box
parent/child/sibling IDs
split axis/cut
canonical order
one source receipt hash set
classification/pending fields
```

对 O2 来说，还必须把 child A/B 重新映射到同一 theta2 namespace；现有
GCN 六维 candidate 不能填充这个映射。

## Authority boundary

即使新增上述 endpoint export，Lean 可 formalize 的部分也只是：

```text
exact strings -> ℚ -> ℝ
endpoint ordering -> RectBox13.ordered
endpoint containment -> BoxSubset
```

`source_interval_membership.status`、运行时语义与 parent coverage premise
仍需外部 source/hash-bound receipt；metadata review 或 geometry
`product_cell_count=8192` 不能替代它们。

## Hashes bound in this review

```text
branch driver source
  C5349534FE1D01D87FB886BAE94EA05F373BCBE4E24B9A2C12411A31234C0590
partition exporter source
  40C19E56DCB6988E424237AD318C0843A59E7B5190F25E3BE5BB0966178F4A4D
partition geometry JSON
  E2051669922B1213162CFEC4F82EF21E5B5B0DE951AD6CCDF176E972905B713A
branch CSV currently persisted
  9CD652A40B73A1399FB7775B7A5E2DEAB4E0D5C574CB64C376B5CC63DDA9609D
partition CSV currently persisted
  230AF31BAA11ADA8DB514489DC8EE3A0306AE9B45B251ED8D72B9C92399B9C9A
interval source referenced by payload
  7C7B7254A00B5CE21F6B9F512D5DE7145CA8386E0420ECF71E92A5AEB5CA789F
current O2 leaf-1 handoff
  9453049983A4F59D0438CE0F51EDD6BC6F6C0E6FDEA91522B524A5828C6709ED
```

本 review 只提交了最小接口与结构性缺口，没有生成新 endpoint 数据，
没有修改 source、state、DAG、registry 或 formal gate。
