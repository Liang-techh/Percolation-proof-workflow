# O2 theta2 external-premises typed interface

日期：2026-09-07  
范围：仅为真实 canonical 13D parent/child/sibling triple 接入
`source_interval_membership` 与 `CoverageJoin2` 提供最小 schema/Lean interface。
没有创建 triple 实例，没有使用 synthetic/GCN/geometry-only 数据。

## Added contract

Schema：

`artifacts/routeb_theta2_leaf_handoff_20260907/routeb-theta2-external-premises-v1.schema.json`

它要求：

```text
namespace.name = theta2
namespace.anchor = coordinate q2, lo -3/20, hi 3/20
triple_ref = parent_id + child_id + sibling_id
             + triple_receipt_path + triple_receipt_sha256
source_interval_membership = accepted status + receipt_path + receipt_sha256
coverage_join = kind CoverageJoin2
                + premise_receipt_path + premise_receipt_sha256
```

Schema 只校验字段形状、常量和 hash 文本格式。path 的存在性与文件内容 hash 必须由
exporter/runtime binding 完成；该 schema 本身不声称已经验证任何 receipt。

## Lean-facing interface

Adapter：

`artifacts/routeb_theta2_leaf_handoff_20260907/Theta2ExternalPremisesAdapter.lean`

最小类型为：

```text
HashFileRef
CanonicalTripleRef
SourceIntervalMembershipReceipt
CoverageJoin2Receipt
TypedExternalPremises parent child sibling
```

核心边界是：

```lean
membershipProof : SourceIntervalMembership child
coverageJoinProof : CoverageJoin2 parent child sibling
```

两者都必须由 source-bound bridge 的调用方显式提供。adapter 只提供：

```lean
source_interval_membership_transport
coverage_join2_transport
coverage_join2_child_or_sibling
```

没有 `axiom`、`sorry` 或 synthetic constructor。`String` 类型的 SHA-256 仅是 provenance
metadata，不是文件 hash 的 Lean 证明；文件 hash binding 仍在外部 runtime/schema
层完成。`CoverageJoin2` 的 structural `BoxSubset`/split-cover 也不等于 dynamics
interval membership proof。

## Dependency order for a real handoff

```text
real exporter JSON
  -> namespace + exact 13D geometry validation
  -> five hash/path bindings
  -> external-premises sidecar schema validation
  -> source-bound proofs supplied to TypedExternalPremises
  -> Lean projections / downstream use
```

在最后两步之前，不能把 `source_interval_membership.status` 或
`coverage_join.premise_receipt_sha256` 升级为 theorem。当前没有真实 triple，故本接口
没有被实例化或编译；不运行 Lean/Lake，也不做全域 coverage。

## Hash receipt

```text
external-premises schema
  SHA-256 9242FB4606921D6039F86AF7E52EE1741A92B6B759439E7E3DC62CE84ACDFCA

Lean adapter source (uncompiled interface)
  SHA-256 DECB1CBC61E770132CBCFF1F81595A0D2BE42B16E648A52DEC439EB36AA80706

namespace/hash-bound real branch exporter
  SHA-256 A2BD89C923AB646BCB138372E4C74A5980AFE5D5906F21080B6781E03051869C

canonical triple instance
  NOT PRESENT; no synthetic triple generated
```

状态：`EXTERNAL_PREMISE_SCHEMA_READY`、`LEAN_TYPED_INTERFACE_READY`、
`REAL_TRIPLE_INSTANCE_OPEN`。

