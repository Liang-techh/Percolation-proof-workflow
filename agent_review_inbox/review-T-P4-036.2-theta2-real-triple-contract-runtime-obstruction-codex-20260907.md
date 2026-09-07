# O2 theta2 canonical triple：真实 contract 生成边界与最小 patch 修正

日期：2026-09-07  
范围：只检查当前 real branch-driver exporter 与
`routeb-theta2-canonical-coverage-v1` 单 triple contract；不做 GCN、geometry-only
审计，不运行 Julia/Lean/Lake，也不宣称 O2 closure。

## 结论

本次没有生成真实 theta2 triple JSON。当前环境中 `julia` 不存在
（receipt：`JULIA_NOT_FOUND`），且在工作流仓库和 real branch-driver 目录中均未找到
`routeB_theta2_canonical_triple_*.json`。因此不能把合成 fixture、旧 leaf-1 endpoint、
GCN candidate 或 geometry receipt 冒充 parent/child/sibling triple。

当前 branch driver 已包含 exporter patch，但它目前只能被称为
“potentially contract-shaped exporter”，尚不能单凭它产出
`READY_STRUCTURAL_CANONICAL_TRIPLE` 的真实 provenance contract。

## 当前实现的可消费字段

`canonical_triple_json` 已按现有 validator 的 structural shape 写出：

```text
schema = routeb-theta2-canonical-coverage-v1
coordinate_order = q1..q6,dq1..dq6,w
source = receipt_sha256 + generator_sha256 + interval_source_sha256
parent/child/sibling = id + 13 个 box_lo/box_hi endpoint
child.parent_id = sibling.parent_id = parent.id
linkage = split_axis + split_cut + adjacency=shared_face
source_interval_membership = status + receipt_sha256
coverage_join = kind=CoverageJoin2 + premise_receipt_sha256
```

实际 branch traversal 中只有当 `P3_BB_TRIPLE_CELL_ID` 等于本轮新分裂产生的某个
child id 时，才会保存 parent/child/sibling record。root id `1` 没有 parent，不能作为
triple child；未来运行必须选择实际生成的 child id（例如首次 split 后的 `2` 或 `3`，
以实际 traversal 为准），不能手填一个不存在的 id。

## 两个当前的真实入场缺口

### 1. receipt hash 尚未与文件内容绑定

当前实现的 `valid_sha256_text` 只检查环境变量是否为 64 位十六进制文本。于是调用者
只要提供任意格式正确的：

```text
P3_BB_SOURCE_RECEIPT_SHA256
P3_BB_GENERATOR_SHA256
P3_BB_INTERVAL_SOURCE_SHA256
P3_BB_MEMBERSHIP_RECEIPT_SHA256
P3_BB_COVERAGE_JOIN_SHA256
```

就可能得到结构上可通过 validator 的 `READY_STRUCTURAL_CANONICAL_TRIPLE`；当前
exporter 没有确认相应 receipt 文件存在，也没有重新读取文件计算 SHA-256。这会把
“hash-shaped metadata”误当成真实 provenance，必须 fail-closed。

最小修正是为上述五类 hash 增加对应 path 环境变量，并在 READY 分支前执行：

```text
path = strip(get(ENV, PATH_ENV, ""))
isfile(path)                         -- 否则 PENDING_EXTERNAL_PREMISES
expected = valid_sha256_text(HASH_ENV)
actual = bytes2hex(SHA.sha256(read(path)))
lowercase(actual) == lowercase(expected) -- 否则 PENDING_EXTERNAL_PREMISES
```

建议的 path 名称为：

```text
P3_BB_SOURCE_RECEIPT_PATH
P3_BB_GENERATOR_PATH
P3_BB_INTERVAL_SOURCE_PATH
P3_BB_MEMBERSHIP_RECEIPT_PATH
P3_BB_COVERAGE_JOIN_PATH
```

`P3_BB_GENERATOR_PATH` 应指向本次实际运行的 branch-driver source；source receipt
应指向既有 traversal/run manifest，而不是正在写出的 triple 文件本身，以避免
self-hash cycle。路径检查与 hash 检查失败时只能输出已有的
`PENDING_EXTERNAL_PREMISES` obstruction，不能输出 READY JSON。

### 2. schema 名没有证明 theta2 namespace

当前 exporter 固定写入 `routeb-theta2-canonical-coverage-v1`，但没有写入或检查
theta2 namespace anchor。generic local/global branch box 因此可能被标成 theta2；尤其
global root 的 q2 区间不是 `[-3/20,3/20]`，而现有 validator 只检查 13 个 coordinate
名称和 parent/child/sibling 的 split geometry。

最小 contract correction 是增加并强制检查：

```json
"namespace": {
  "name": "theta2",
  "anchor": {"coordinate": "q2", "lo": "-3/20", "hi": "3/20"}
}
```

validator/exporter 应要求 parent 的 q2 区间满足
`-3/20 <= parent.q2.lo <= parent.q2.hi <= 3/20`；child 与 sibling 随 parent
inherit 该 subset。这个 anchor 只建立 exact-real theta2 namespace 对齐，不能替代
Float64/libm enclosure、DAG semantics、source interval membership 或 CoverageJoin2
定理前提。

如果暂时不修改 validator，exporter 至少必须在形成 READY JSON 前做同一 q2 subset
检查，并在 JSON 中携带上述 `namespace` 对象；否则当前 validator 的 structural
success 不能称为 theta2 success。

## 真实生成后的最小验收顺序

```text
1. Julia branch traversal 产生实际 child id 和 parent/sibling endpoint。
2. exporter 读取五个 receipt path，逐个重算并比对 SHA-256。
3. exporter 检查 theta2 namespace q2 anchor，失败则 pending。
4. 只对 READY JSON 运行 validate_canonical_coverage_triple。
5. 记录 source JSON hash 与 exporter source hash 成对 receipt。
```

第 4 步的成功仍只代表：exact-rational box subset 与 shared-face split geometry
结构成立，并且 receipt 字段形状合格。现有 validator 明确返回
`dynamics_interval_membership_proven=false`、`coverage_join_theorem_proven=false`、
`formal_certificate_allowed=false`、`registry_promoted=false`；这些边界保持不变。

## Hash-bound evidence

```text
current real branch driver
  C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\routeB_interval_branch_bound.jl
  SHA-256 E4BA40D259AAC57CACCBB47A8EBA0A433B407DAAFBB30225E748E29CF532889C

pre-patch backup routeB_interval_branch_bound.jl.bak_20260907_o2_triple
  SHA-256 C5349534FE1D01D87FB886BAE94EA05F373BCBE4E24B9A2C12411A31234C0590

canonical triple validator source
  src/percolation_workflow/coverage_receipt.py
  SHA-256 B47913A5146B3A9CC496FF7DDB5569361263A1B8002A33AD3023005D83B19F38

canonical triple validator tests
  tests/test_coverage_receipt.py
  SHA-256 B8CBEF52C0C23F1E9705366A29C5B223532EED937F7F8E50264D95C3FBA08CEC

current theta2 leaf-1 endpoint handoff (not a triple)
  artifacts/routeb_theta2_leaf_handoff_20260907/theta2_leaf_1_endpoint_handoff.json
  SHA-256 9453049983A4F59D0438CE0F51EDD6BC6F6C0E6FDEA91522B524A5828C6709ED

real theta2 canonical triple JSON
  NOT FOUND; Julia runtime unavailable
```

状态：`O2_COVERAGE_OPEN / REAL_TRIPLE_NOT_GENERATED / PATCH_CORRECTION_REQUIRED`。

