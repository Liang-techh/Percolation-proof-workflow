# O2 theta2 exporter binding receipt

日期：2026-09-07  
范围：仅验证 canonical 13D triple exporter 的 namespace 与 hash-file binding；不生成或接纳 synthetic triple。

## Result

已对 real branch driver 做最小修正。exporter 当前在 READY payload 中携带：

```json
"namespace": {
  "name": "theta2",
  "anchor": {"coordinate": "q2", "lo": "-3/20", "hi": "3/20"}
}
```

在写 READY JSON 前，parent 的 q2 区间必须满足：

```text
-3/20 <= parent.q2.lo <= parent.q2.hi <= 3/20
```

这与当前 validator 的 theta2 namespace gate 对齐；child/sibling 仍由 parent subset
和 shared-face split 检查约束。

## Hash-file binding

exporter 不再只接受 64 位 hex 文本。以下每个 hash 都要求相应 path 存在，并通过
`SHA.sha256(read(path))` 重算后逐字节比对；任一项缺失、文件不存在或 mismatch，均只
产生 `PENDING_EXTERNAL_PREMISES`：

```text
P3_BB_SOURCE_RECEIPT_SHA256    <-> P3_BB_SOURCE_RECEIPT_PATH
P3_BB_GENERATOR_SHA256         <-> P3_BB_GENERATOR_PATH
P3_BB_INTERVAL_SOURCE_SHA256   <-> P3_BB_INTERVAL_SOURCE_PATH
P3_BB_MEMBERSHIP_RECEIPT_SHA256<-> P3_BB_MEMBERSHIP_RECEIPT_PATH
P3_BB_COVERAGE_JOIN_SHA256     <-> P3_BB_COVERAGE_JOIN_PATH
```

`P3_BB_GENERATOR_PATH` 应指向实际运行的 branch-driver source；source receipt path
应指向既有 run/traversal manifest，不能指向正在写出的 triple 文件。

## Static evidence

```text
real branch driver after correction
  C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\routeB_interval_branch_bound.jl
  SHA-256 A2BD89C923AB646BCB138372E4C74A5980AFE5D5906F21080B6781E03051869C

canonical validator currently enforcing namespace gate
  src/percolation_workflow/coverage_receipt.py
  SHA-256 2729DEF47A499C360F216C4578DE57E57C20C20BED63D9A0638E6DC888F7C8CA

canonical triple output
  NOT GENERATED; no synthetic artifact created
```

状态：`EXPORTER_NAMESPACE_BOUND`、`EXPORTER_HASH_FILE_BOUND`、
`REAL_TRIPLE_STILL_OPEN`。

