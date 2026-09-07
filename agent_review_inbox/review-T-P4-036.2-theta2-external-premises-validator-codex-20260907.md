# O2 theta2 external-premises validator contract

日期：2026-09-07  
范围：仅实现并核验 `routeb-theta2-external-premises-v1` 的 Python
fail-closed validator；不生成有效 sidecar、synthetic triple 或 theorem receipt。

## Implementation

已在 `src/percolation_workflow/coverage_receipt.py` 增加：

```python
validate_theta2_external_premises(
    document,
    *,
    base_dir=None,
    canonical_triple=None,
)
```

它严格检查：

```text
schema = routeb-theta2-external-premises-v1
claim_boundary = source-bound receipt references only
namespace = theta2; anchor = q2, -3/20 .. 3/20
triple_ref = distinct parent_id/child_id/sibling_id
               + triple_receipt_path + triple_receipt_sha256
source_interval_membership = accepted status
                               + receipt_path + receipt_sha256
coverage_join = kind CoverageJoin2
                + premise_receipt_path + premise_receipt_sha256
```

每个 path 必须是现有文件；每个 hash 都通过 `hashlib.sha256(path.read_bytes())`
重算并逐字节比对。未知字段也会拒绝，以防额外塞入未经定义的 proof/准入标记。

传入 `canonical_triple` 时，validator 另外调用现有 structural validator，并检查
三个 ID 与 `triple_ref` 一致；不传入时仍只验证 external sidecar 的文件绑定。

## Proof boundary

返回结果显式包含：

```text
source_interval_membership_receipt_bound = true
coverage_join_premise_receipt_bound = true
structural_receipt_is_not_proof = true
dynamics_interval_membership_proven = false
coverage_join_theorem_proven = false
formal_certificate_allowed = false
registry_promoted = false
```

Lean 侧 `Theta2ExternalPremisesAdapter.lean` 的
`TypedExternalPremises` 仍要求调用方显式提供：

```lean
membershipProof : SourceIntervalMembership child
coverageJoinProof : CoverageJoin2 parent child sibling
```

Python receipt hash、structural box/split 检查和 metadata 均不会自动构造上述两个
proof fields。

## Focused receipt

```text
Python source
  src/percolation_workflow/coverage_receipt.py
  SHA-256 0CBD83262ECF4BE1EF0B1C11BB5D261D7002597CE62A8FAE48738E85C1FC7C31

external-premises schema
  artifacts/routeb_theta2_leaf_handoff_20260907/routeb-theta2-external-premises-v1.schema.json
  SHA-256 9242FB4606921D6039F86AF7E52EE1741A92B6B759439E7E3DC62CE84ACDFCA

focused check
  AST parse: PASS
  empty receipt rejected: PASS (EMPTY_FAIL_CLOSED_OK)
  valid external-premises instance: NOT PRESENT
  synthetic triple: NOT CREATED
```

状态：`VALIDATOR_IMPLEMENTED`、`PATH_HASH_FAIL_CLOSED`、
`PROOF_FIELDS_EXPLICIT`、`NO_SYNTHETIC_ADMISSION`。

