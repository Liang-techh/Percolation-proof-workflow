# O2 theta2 source-bound proof bridge contract

日期：2026-09-07  
范围：仅定义 `TypedExternalPremises` 的 source-bound proof bridge 元数据与
fail-closed Python 接口；不生成 synthetic triple，不自动构造任何 proof。

## Receipt fields

`routeb-theta2-external-premises-v1` 现在额外要求：

```text
proof_bridge.schema = routeb-theta2-proof-bridge-v1
proof_bridge.status = EXPLICIT_PROOFS_REQUIRED
proof_bridge.lean_module_path
proof_bridge.lean_module_sha256
proof_bridge.membership_proof_symbol
proof_bridge.coverage_join_proof_symbol
```

Python validator 会检查 Lean module 文件存在并重新计算其 SHA-256；proof symbol
只作为 source-bound handoff 名称校验，绝不通过字符串查找或反射生成证明。

## Python fail-closed result

`validate_theta2_external_premises` 的返回边界为：

```text
proof_bridge.status = EXPLICIT_PROOFS_REQUIRED
source_interval_membership_receipt_bound = true
coverage_join_premise_receipt_bound = true
structural_receipt_is_not_proof = true
dynamics_interval_membership_proven = false
coverage_join_theorem_proven = false
formal_certificate_allowed = false
registry_promoted = false
```

缺少 bridge 字段、Lean module path/hash mismatch、错误 status 或未知字段均拒绝。

## Lean contract

`Theta2ExternalPremisesAdapter.lean` 增加了：

```lean
inductive ProofBridgeStatus
  | explicitProofsRequired

structure SourceBoundProofBridgeRef where
  schema : String
  status : ProofBridgeStatus
  leanModule : HashFileRef
  membershipProofSymbol : String
  coverageJoinProofSymbol : String
```

`TypedExternalPremises` 仍然必须由调用方提供：

```lean
membershipProof : SourceIntervalMembership child
coverageJoinProof : CoverageJoin2 parent child sibling
```

`source_interval_membership_transport` 与 `coverage_join2_transport` 仅投影这些
显式 proof fields。receipt metadata、文件 hash、BoxSubset 或 structural split
不会替代 dynamics proof 或 CoverageJoin2 theorem proof。

## Focused evidence

```text
Python validator
  src/percolation_workflow/coverage_receipt.py
  SHA-256 D252C25B3C14D622F9C2B4E10347D203746E8C2A30DFD8D13EEC80961BB847AC

external-premises schema
  artifacts/routeb_theta2_leaf_handoff_20260907/routeb-theta2-external-premises-v1.schema.json
  SHA-256 77F0884DAAB7D973AB739E2DF7C6809EAFC4C74A87BC1C46C838D19791D161D9

Lean adapter source (not compiled)
  artifacts/routeb_theta2_leaf_handoff_20260907/Theta2ExternalPremisesAdapter.lean
  SHA-256 06B51F6B43B6A2DDB1800935FF1B430C093EFDF960C5455F50EB9CAC814F17B0

focused check
  AST parse: PASS
  empty external-premises receipt rejected: PASS
  valid proof-bridge instance: NOT PRESENT
  synthetic triple/proof: NOT CREATED
```

状态：`PROOF_BRIDGE_METADATA_READY`、`EXPLICIT_PROOFS_REQUIRED`、
`NO_AUTOMATIC_PROOF_CONSTRUCTION`、`NO_SYNTHETIC_ADMISSION`。

