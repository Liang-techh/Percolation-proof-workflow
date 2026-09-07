# O2 T-P4-036.2：single-leaf `InRectBox` witness provenance/handoff

## Scope

本 review 只处理一个 leaf 的 receipt-to-Lean handoff、exact-real
`InRectBox` witness，以及 parent/sibling coverage join 的最小 typed
接口。没有扫描全域 partition，也没有把该 leaf 提升为 true-DH、
Float64/libm、DAG 或 coverage 证明。

## Authority boundary

当前可定位到的单 leaf 来源是
`artifacts/routeb_agent_p3_coverage_next_20260906T091543Z/p3_coverage_bridge_audit.json`
中的 `p3_candidate` / `cell_id == "1"`。该 receipt 自身的
`claim_boundary` 是 read-only recorded numeric replay，并明确写明
“no formal or true-DH theorem claim”。因此本 handoff 的状态被严格固定为

```text
ENDPOINT_PROVENANCE_ONLY
```

这表示：在“把 receipt 端点作为精确有理数矩形输入”的条件下，可以构造
真实的 lower-corner point-in-box witness；它不表示该点可达、是运行时
authoritative trajectory leaf，或已完成 sibling/全域 coverage。若要进入
`AUTHORITATIVE_ENDPOINT_LEAF`，仍需要 source-bound 的 accepted leaf record，
而不是仅有该候选 replay。

## Handoff artifact

最小 JSON Schema 与单 leaf fixture：

- [routeb-theta2-leaf-handoff-v1.schema.json](C:/Users/z5242/Desktop/重构版/工作流/artifacts/routeb_theta2_leaf_handoff_20260907/routeb-theta2-leaf-handoff-v1.schema.json)
- [theta2_leaf_1_endpoint_handoff.json](C:/Users/z5242/Desktop/重构版/工作流/artifacts/routeb_theta2_leaf_handoff_20260907/theta2_leaf_1_endpoint_handoff.json)

Schema 的最小必需字段是：

```text
schema, authority_status, claim_boundary, leaf_id,
coordinate_order, box_lo, box_hi, source, witness
```

其中：

- `box_lo` / `box_hi` 是 canonical 13-coordinate order 下的 exact
  rational/decimal strings；
- `source.receipt_sha256` 绑定原始 receipt，`source.leaf_pointer` 固定为
  `p3_candidate`；
- `witness.kind = lower_corner`，且生成器额外检查
  `witness.point == box_lo` 的 exact `Fraction` 相等性；
- JSON Schema 只约束形状，point 与 `box_lo` 的相等性由生成器 fail-closed
  检查。

本次 provenance hashes：

```text
source receipt sha256
  87CF832BF5D9D266A532EEA4DC54B9365FF9E4A5E709031907C8E9A97BDDC7D6
handoff JSON sha256
  9453049983A4F59D0438CE0F51EDD6BC6F6C0E6FDEA91522B524A5828C6709ED
schema sha256
  F5191ED71F3A369414803ACCBD4ABE07639F71A3BD1CB3C2BCE03E6C3A77DAB6
generator sha256
  37F7541D2475395669C9B75EC149A7BCC5859820867192B69C3BF7ECBCA4E12B
```

## Lean target and receipt

现有生成器 [routeb_theta2_receipt_to_lean.py](C:/Users/z5242/Desktop/重构版/工作流/scripts/routeb_theta2_receipt_to_lean.py)
现在接受该 handoff schema；命令如下：

```powershell
python scripts\routeb_theta2_receipt_to_lean.py `
  --input artifacts\routeb_theta2_leaf_handoff_20260907\theta2_leaf_1_endpoint_handoff.json `
  --output artifacts\routeb_fd8_tensor_christoffel_enclosure_20260906\mathlib\DownstreamTest\Theta2LeafHandoffAdapterGenerated.lean
```

生成的 Lean target 是
[Theta2LeafHandoffAdapterGenerated.lean](C:/Users/z5242/Desktop/重构版/工作流/artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib/DownstreamTest/Theta2LeafHandoffAdapterGenerated.lean)。
其中 `receiptLeaf1Witness` 是 receipt 的 13 维 `box_lo`，并有真实闭合目标：

```lean
theorem receipt_leaf1_witness_in_rectbox :
    InRectBox (receiptLeaf1.toRectBox) receiptLeaf1Witness := by
  intro i
  fin_cases i <;> norm_num [InRectBox, receiptLeaf1,
    ReceiptLeaf13.toRectBox, receiptLeaf1Witness]
```

这不是原先的 `∀ x, hx -> InRectBox ... x` 恒等转述；它具体证明了 lower
corner point 落在该矩形中。

Pinned root：
`artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib`。

单目标命令在该 root 下返回 `exit_code=0`，未运行 Lean/Lake 全项目回归：

```powershell
lake env lean -o .lake\build\lib\lean\DownstreamTest\Theta2LeafHandoffAdapterGenerated.olean `
  DownstreamTest\Theta2LeafHandoffAdapterGenerated.lean
```

成对 receipt：

```text
Lean source sha256
  248DACF3BF0749574477EFAB6DFF71DA0DC4684BB05FC1B5210FF5F7C66D17CB
Lean olean sha256
  45D911A0AB09382793845DE801D21DA10ABBA668BB925ED1DE158F45031A325B
```

编译输出的 `#print axioms` 对 witness、parent-lift 和 join projection
均为：

```text
[propext, Classical.choice, Quot.sound]
```

这只是该 pinned Mathlib 环境的 kernel axiom boundary；没有声明
Float64/libm 或动力学语义。

## 最小 parent/sibling typed child

同一生成文件只增加接口，不伪造缺失的 parent/sibling receipt：

```lean
def BoxSubset (child parent : RectBox13) : Prop :=
  ∀ i, parent.lo i ≤ child.lo i ∧ child.hi i ≤ parent.hi i

def CoverageJoin2 (parent child sibling : RectBox13) : Prop :=
  BoxSubset child parent ∧
  BoxSubset sibling parent ∧
  ∀ x, InRectBox parent x →
    InRectBox child x ∨ InRectBox sibling x
```

已编译的最小 transport 是：

```lean
theorem receipt_leaf1_witness_parent_lift
    {parent : RectBox13}
    (hparent : BoxSubset (receiptLeaf1.toRectBox) parent) :
    InRectBox parent receiptLeaf1Witness :=
  in_rectbox_parent_of_child hparent receipt_leaf1_witness_in_rectbox
```

以及 join 的 typed projection：

```lean
theorem coverage_join2_child_or_sibling
    (hjoin : CoverageJoin2 parent child sibling)
    (hx : InRectBox parent x) :
    InRectBox child x ∨ InRectBox sibling x :=
  hjoin.2.2 x hx
```

这里没有具体的 `parent`、`sibling` endpoint 或 partition disjointness
receipt，因此 join 仍是可复用的 conditional child，不是 sibling coverage
closure。

## Remaining handoff gap

本次已关闭的是：

```text
recorded exact endpoint -> exact ℚ -> RectBox13 -> concrete lower-corner
State13 -> InRectBox witness
```

仍保持 open 的是：

```text
source-bound authoritative dynamic leaf
trajectory/entry membership
Float64/libm enclosure
DAG/finite DH propagation
parent/sibling endpoint records and coverage join premises
```

因此该 review 不改变 O2 formal gate 或全域 coverage 状态。
