# O2 T-P4-036.2：leaf-1 parent/sibling authority stop

## Scope

只核查 leaf-1 handoff 所需的 parent/sibling endpoint provenance 与 typed
coverage join 前提；没有重跑 leaf-1 Lean 编译，也没有做全域扫描或 formal
gate 变更。

## 判定

当前只能保持：

```text
ENDPOINT_PROVENANCE_ONLY
```

原因不是 Lean transport 缺失，而是没有找到同时满足以下条件的
parent/sibling record：

```text
同一 canonical 13-coordinate order
同一 source/runtime semantics
source/hash-bound endpoint payload
accepted/non-pending classification
可指向 leaf-1 的 parent、sibling id 与 box_lo/box_hi
```

因此不能诚实地产生 `BoxSubset child parent` 的具体证据，也不能实例化
`CoverageJoin2 parent child sibling`。

## 定向检查结果

### 1. 当前 source-bound local payload

[routeb_p3_source_bound_payload_current.json](C:/Users/z5242/Desktop/重构版/工作流/artifacts/task_routeb_local_box_replay_current/routeb_p3_source_bound_payload_current.json)

```text
schema: routeb-p3-source-bound-payload-v1
evidence_level: E2 rigorous-numerical local replay candidate
strict_certificate: false
payload: cell_id = 1 only
run_contract.global_tree_run: false
run_contract.regression_suite_run: false
```

该文件含 source file hashes 和一个新的 cell-1 local box，但 payload 没有
parent_id、sibling_ids 或 sibling endpoint。它是 source-bound provenance，
不是 accepted authoritative leaf/coverage record。

对应报告
[P3_INTERVAL_BRANCH_BOUND_current_local_radius1e3_meanvalue_mass_weighted_depth8_nodes512.md](C:/Users/z5242/Desktop/重构版/工作流/artifacts/task_routeb_local_box_replay_current/P3_INTERVAL_BRANCH_BOUND_current_local_radius1e3_meanvalue_mass_weighted_depth8_nodes512.md)
虽写有 `coverage_complete=true`，但自身明确标为
“directed-interval candidate”，并说明尚未成为 theorem；不能承担 parent
或 sibling authority。

### 2. 唯一具有 parent/sibling 拓扑的 receipt

[audit_topology receipt](C:/Users/z5242/Desktop/重构版/工作流/artifacts/task_routeb_math_bottleneck_audit_current/routeB_interval_coverage_receipt_audit_topology.json)
给出：

```text
run_status = INCOMPLETE
coverage_complete = false
fail_closed = true
node 1: parent 0, children [2, 3], INTERNAL_SPLIT
node 2: parent 1, no children, UNKNOWN_DOMAIN_BOUNDARY
node 3: parent 1, no children, UNKNOWN_DOMAIN_BOUNDARY
```

这只证明 receipt 中存在树形关系，不提供可接受的 `RectBox13` endpoint
handoff：child classification 不是 resolved/accepted positive leaf，且
receipt 没有和当前 leaf-1 handoff 的 source-bound endpoint 建立 pointer。

其 SHA-256：

```text
0D191AD5F86D15F492AE7060E41AE0CBF42BB47E7DBF94AD273FFA32E5F32E5D
```

### 3. 其余定向 receipts

[negative payload](C:/Users/z5242/Desktop/重构版/工作流/artifacts/task_routeb_math_bottleneck_audit_current/routeB_interval_coverage_receipt_audit_negative_payload.json)
只有一个 `BOX_BRACKET_STRICTLY_NEGATIVE` node，没有 sibling join；

[exact encoding probe](C:/Users/z5242/Desktop/重构版/工作流/artifacts/task_routeb_math_bottleneck_audit_current/routeB_interval_coverage_receipt_audit_exact_encoding_probe.json)
是 `PENDING_UNEVALUATED`，`boxes_evaluated=0`；

[root exact-weight probe](C:/Users/z5242/Desktop/重构版/工作流/artifacts/task_routeb_root_exact_weight_fix_current/routeB_interval_coverage_receipt_root_exact_weight_probe.json)
只有 `UNKNOWN_DOMAIN_BOUNDARY` root leaf，且不是 leaf-1 的 endpoint
record。

三者均为 `run_status=INCOMPLETE`、`coverage_complete=false`、
`fail_closed=true`，不能补出 authoritative parent/sibling。

对应 hashes：

```text
negative payload       800119DE73D36CBC24F9652CA9CD687C975B9FF47535FB70A1474877AFAA1C7C
exact encoding probe   3159A69E9D4976836FF9BADD5F51F424ACC11488429749A6D25C97BD4D8C5062
root exact-weight      3BCD16A18AAB404D5868E28DCEAF65DD7A150C888185DE7326EE889220C5D3A3
```

## Typed join 的精确缺口

已有 adapter 中的最小接口是：

```lean
def BoxSubset (child parent : RectBox13) : Prop :=
  ∀ i, parent.lo i ≤ child.lo i ∧ child.hi i ≤ parent.hi i

def CoverageJoin2 (parent child sibling : RectBox13) : Prop :=
  BoxSubset child parent ∧
  BoxSubset sibling parent ∧
  ∀ x, InRectBox parent x →
    InRectBox child x ∨ InRectBox sibling x
```

要关闭一个具体 child，至少需要新的 authoritative handoff 提供：

```text
parent box + parent source/hash
sibling box + sibling source/hash
child-to-parent endpoint inequalities
same coordinate_order and leaf-id linkage
```

其中 `parent/sibling` 的 endpoint inequalities 可以在 Lean 中 formalize；
但“该 parent 由两个 sibling/children 覆盖”以及 endpoint 与运行时 leaf
分类一致，必须由外部 receipt/exporter 提供 source-bound evidence。当前
topology metadata 不足以承担这个 premise。

## Provenance conclusion

当前 leaf-1 的有效链仍然只有：

```text
recorded endpoint -> exact ℚ -> RectBox13 -> concrete InRectBox witness
```

尚不能延伸为：

```text
authoritative parent/sibling endpoints -> BoxSubset -> CoverageJoin2
```

因此本次没有修改 leaf-1 adapter、没有重复编译，并将 O2 parent/sibling
coverage join 保持 open。

## Examined artifact hashes

```text
source-bound local payload
  028C0E2F1DE5FC0D84BCA8B8F7043073CA02424E5C402889ECE69B94F6F8FF6B
local candidate report
  43FB96BF0427E735A948C15C4A500CF25E291DF1850EB5F77A10DD0ABD8FB86A
leaf-1 handoff fixture
  9453049983A4F59D0438CE0F51EDD6BC6F6C0E6FDEA91522B524A5828C6709ED
```
