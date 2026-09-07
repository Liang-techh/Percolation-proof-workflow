# O2 T-P4-036.2：source-bound parent/sibling candidate finding

## Scope

本次只寻找与 parent/sibling endpoint 有关的 source/hash-bound record，且不
重复 leaf-1 Lean 编译。结论区分“存在 hash-bound 候选记录”和“可作为 O2
authoritative coverage premise”。

## Finding

找到一对可复现的 source/hash-bound GCN candidate records：

1. [GCN-F1 leaf_witness.json](C:/Users/z5242/Desktop/重构版/工作流/artifacts/task_routeb_gcn_f1_leaf_current/leaf_witness.json)
   的 `status=CANDIDATE_EXACT_RATIONAL_REPLAY`，含
   `parent_leaf_id=cell16/a2=0/a3=0/a4=0/a5=0`。
2. [GCN-F2 neighbor_witness.json](C:/Users/z5242/Desktop/重构版/工作流/artifacts/task_routeb_gcn_f2_neighbor_current/neighbor_witness.json)
   的 `status=CANDIDATE_EXACT_RATIONAL_NEIGHBOR_REPLAY`，明确给出
   `f1_leaf_id`、同一 `parent_leaf_id` 和
   `adjacency=right_shared_endpoint`。

F2 的 q1 区间是

```text
[-1.206312953125, -1.198686859375]
```

F1 的 q1 区间是

```text
[-1.213939046875, -1.206312953125]
```

两者共享精确 endpoint `-1.206312953125`，q2--q6 保持一致。两份
record 都带有 source input hashes；F2 还绑定 F1 witness、checker、
frontier receipt、neighbor exporter 和 canonical `routeB_interval_bounds.jl`。

## 为什么仍不能进入 O2 typed coverage

这对记录不是当前 O2 theta2 leaf-1 的 authoritative parent/sibling，理由
是明确且独立的：

```text
F1/F2: source_interval_membership_proved = false
F1/F2: coverage = false
F1/F2: formal_certificate_allowed = false
F2: global_tree_run = false
```

并且它们是 GCN-F1/F2 namespace 的 6 个 q-coordinate interval-matrix
sidecar，不是 O2 handoff 所需的 canonical 13-coordinate `RectBox13`。
当前 O2 leaf-1 handoff 的 q2 区间约为 `[-0.07743,-0.06743]`，而该 GCN
pair 的 q2 区间约为 `[-1.371587,-1.355377...]`，不存在可直接复用的
leaf identity 或 box inclusion。

所以本次的准确结论是：

```text
source/hash-bound parent/sibling CANDIDATE：找到
source/hash-bound authoritative O2 parent/sibling：仍未找到
可实例化 CoverageJoin2：不能
O2 authority status：保持 ENDPOINT_PROVENANCE_ONLY
```

## 新增最小 obstruction schema

为了避免把 candidate pair 误当 authority，新增了 fail-closed obstruction：

- [coverage-join obstruction schema](C:/Users/z5242/Desktop/重构版/工作流/artifacts/routeb_theta2_leaf_handoff_20260907/routeb-theta2-coverage-join-obstruction-v1.schema.json)
- [leaf-1 obstruction instance](C:/Users/z5242/Desktop/重构版/工作流/artifacts/routeb_theta2_leaf_handoff_20260907/theta2_leaf_1_coverage_join_obstruction.json)

实例状态为：

```text
BLOCKED_AUTHORITY_NOT_ADMISSIBLE
```

它保留了两个 candidate record 的路径、实际 record hash、witness
commitment hash 和阻塞原因，并要求以下字段才能清除 obstruction：

```text
同一 O2 namespace 的 canonical 13D parent endpoint
同一 O2 namespace 的 canonical 13D sibling endpoint
child-parent/child-sibling 显式 linkage
accepted authority status 与 source interval membership
parent coverage join 的 typed premise 或等价 receipt
```

## Provenance hashes

```text
GCN-F1 record
  117894EE0162236D13A3C745D2BD1B3A90B5EC1D9672DBF3B5939881E8B1BE27
GCN-F1 CHECK_RESULT
  D886D5A2B4C66A45D3CD582B55CBCF0C17E3A213F6905CA15DC3D4B349B34464
GCN-F2 record
  24FCA1CA375FF93964768632F3A661EE3B7B7E292D1EB6E6FDDA0838871576DE
GCN-F2 CHECK_RESULT
  7F753251D5DA53AFF677FE2B5BDDCB914D6324DFA7FE0F5D3665D6D2F9073F6C
O2 leaf-1 handoff
  9453049983A4F59D0438CE0F51EDD6BC6F6C0E6FDEA91522B524A5828C6709ED
```

未进行 Lean/Lake 编译或全域回归；本次只新增 provenance obstruction
记录，未改变 O2 formal/coverage gate。
