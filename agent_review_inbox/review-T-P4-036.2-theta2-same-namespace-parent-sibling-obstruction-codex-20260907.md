# O2 T-P4-036.2：theta2 leaf-1 same-namespace parent/sibling obstruction

## Scope and immutability

本记录只检查当前 `routeb-theta2` namespace 及 leaf-1 的直接 exact-real
handoff 链。GCN-F1/F2 记录不作为证据，只保留为 candidate/authority 对比。
没有重复 leaf-1 Lean 编译，没有运行 Lean/Lake 或全域回归，也没有修改
formal gate。

本文件是新的 immutable review；以下 hash 是写入时对实际文件内容的
SHA-256 绑定。

## Same-namespace search result

当前同 namespace 的 JSON 记录只有：

1. [theta2_leaf_1_endpoint_handoff.json](C:/Users/z5242/Desktop/重构版/工作流/artifacts/routeb_theta2_leaf_handoff_20260907/theta2_leaf_1_endpoint_handoff.json)
2. [theta2_leaf_1_coverage_join_obstruction.json](C:/Users/z5242/Desktop/重构版/工作流/artifacts/routeb_theta2_leaf_handoff_20260907/theta2_leaf_1_coverage_join_obstruction.json)

第 2 项是 obstruction metadata，不是 parent/sibling endpoint record。
第 1 项的实际结构是：

```text
schema = routeb-theta2-leaf-handoff-v1
leaf_id = 1
coordinate_order length = 13
box_lo/box_hi = present
source = present
witness = lower_corner
parent = absent
sibling = absent
source_interval_membership = absent
CoverageJoin2 premise = absent
authority_status = ENDPOINT_PROVENANCE_ONLY
```

因此当前 theta2 namespace 没有可供 typed transport 使用的 canonical
13-coordinate parent 或 sibling endpoint，也没有 child-to-parent/sibling
linkage。

## Exact authority test

要把该 leaf 接到已有 Lean-side interfaces，至少应存在如下同 namespace
数据：

```text
parent: leaf id + canonical 13D box_lo/box_hi + source/hash
sibling: leaf id + canonical 13D box_lo/box_hi + source/hash
child linkage: child=theta2 leaf-1, parent id, sibling id
source_interval_membership: accepted source-bound premise
join premise: CoverageJoin2 parent child sibling
```

现有 handoff 仅能证明：

```text
recorded exact endpoint -> exact ℚ -> RectBox13
-> concrete lower-corner InRectBox witness
```

不能证明：

```text
theta2 child ⊆ parent
theta2 sibling ⊆ parent
∀ x ∈ parent, x ∈ child ∨ x ∈ sibling
```

后面三项需要实际 endpoint 和 linkage receipt；不能从
`coordinate_order`、leaf id 或 metadata review 推出。

## Existing Lean boundary

[Theta2LeafHandoffAdapterGenerated.lean](C:/Users/z5242/Desktop/重构版/工作流/artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib/DownstreamTest/Theta2LeafHandoffAdapterGenerated.lean)
中只有抽象 typed definitions：

```lean
def BoxSubset (child parent : RectBox13) : Prop :=
  ∀ i, parent.lo i ≤ child.lo i ∧ child.hi i ≤ parent.hi i

def CoverageJoin2 (parent child sibling : RectBox13) : Prop :=
  BoxSubset child parent ∧
  BoxSubset sibling parent ∧
  ∀ x, InRectBox parent x →
    InRectBox child x ∨ InRectBox sibling x
```

该文件没有定义 concrete `receiptParent` 或 `receiptSibling`，所以
`receipt_leaf1_witness_parent_lift` 仍要求外部传入 `BoxSubset`；
`coverage_join2_child_or_sibling` 仍要求外部传入完整 `CoverageJoin2`。

这不是编译失败，而是输入 provenance 缺口。

## Candidate-only comparison

已知的 GCN-F1/F2：

- [F1 leaf_witness.json](C:/Users/z5242/Desktop/重构版/工作流/artifacts/task_routeb_gcn_f1_leaf_current/leaf_witness.json)
  和 [F2 neighbor_witness.json](C:/Users/z5242/Desktop/重构版/工作流/artifacts/task_routeb_gcn_f2_neighbor_current/neighbor_witness.json)
  确实带 parent/sibling-like linkage；
- F2 的 `right_shared_endpoint` 指向 F1，且两者有 source input hashes；
- 但二者 status 分别是 `CANDIDATE_EXACT_RATIONAL_REPLAY` 与
  `CANDIDATE_EXACT_RATIONAL_NEIGHBOR_REPLAY`；
- `source_interval_membership_proved=false`、`coverage=false`、
  `formal_certificate_allowed=false`；
- 其 namespace 是 GCN，payload 是 6 个 q intervals，不是当前 O2
  theta2 leaf-1 的 13D `RectBox13`。

所以它们只能说明“candidate linkage schema 可以存在”，不能补充当前
theta2 namespace 的 authority。

## Stop conclusion

本次的严格结论是：

```text
same-namespace canonical 13D parent endpoint: NOT FOUND
same-namespace canonical 13D sibling endpoint: NOT FOUND
same-namespace child linkage: NOT FOUND
same-namespace source interval membership: NOT FOUND
concrete CoverageJoin2 premise: NOT FOUND
O2 theta2 leaf-1 status: KEEP ENDPOINT_PROVENANCE_ONLY
```

下一步只有在出现新的同 namespace source-bound record 后，才可创建
`receiptParent`/`receiptSibling` 并证明 `BoxSubset`；在此之前，不应把
GCN candidate 或 topology metadata 连接进 O2 typed coverage。

## Actual hashes

```text
theta2 leaf-1 endpoint handoff
  9453049983A4F59D0438CE0F51EDD6BC6F6C0E6FDEA91522B524A5828C6709ED
theta2 coverage obstruction instance
  943E58062B521D65BB78655F667EC5AF5E74330A5C6CA482A9F7B6D8DE4EF5E4
theta2 leaf handoff schema
  F5191ED71F3A369414803ACCBD4ABE07639F71A3BD1CB3C2BCE03E6C3A77DAB6
theta2 coverage obstruction schema
  15CD40A03B7CAD0842BCD868746E2C5DFC3C029B906E8D72DB92CC15DCFC5D6C
current generated Lean adapter source (read-only hash; not recompiled)
  248DACF3BF0749574477EFAB6DFF71DA0DC4684BB05FC1B5210FF5F7C66D17CB
GCN-F1 candidate record
  117894EE0162236D13A3C745D2BD1B3A90B5EC1D9672DBF3B5939881E8B1BE27
GCN-F2 candidate record
  24FCA1CA375FF93964768632F3A661EE3B7B7E292D1EB6E6FDDA0838871576DE
```
