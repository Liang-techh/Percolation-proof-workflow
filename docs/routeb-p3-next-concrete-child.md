# Route-B P3 `strict_true_dh_bounds`: next concrete child

日期：2026-09-06。范围仅为本地已有 examples/docs 与 external Route-B
source/artifact 的只读审计。本轮没有修改 external project、persistent state、
registry，也没有运行 Julia、Lean、全局 branch-and-bound 或其他长计算。

## 判定

`P3.strict_true_dh_bounds` 当前仍是
`open_global_coverage`。已有 `routeB_interval_bounds.jl` 使用 256-bit
directed `BigFloat` 做 interval/Taylor 候选计算；已有
`examples/routeb_b45_2_float64_seam_lean` 证明了一个带假设的
Float64 sampling/FD error interface。但二者之间没有 canonical-source
semantic bridge。因此当前不能把 interval 输出称为对 deployed Julia
`mass_matrix`/`arm_MCG`/`exact_ddq` 的 true-DH certificate。

## 最小可执行 child theorem

优先实现一个**单个固定 box、单个质量矩阵 entry** 的 source-to-interval
定理，不把 `C/G`、finite difference 或 solve 混入第一步：

```text
P3.child.mass_entry_float64_to_exact_interval
```

设 `B : Box (Fin 6)` 是一个明确的 rational endpoint box，`(i,j)` 是固定
矩阵坐标。定义三层对象：

```text
M_dh_exact : Box (Fin 6) -> Fin 6 -> Fin 6 -> IntervalRat
M_julia64  : Float64^6 -> Fin 6 -> Fin 6 -> Float64
M_eval_I   : Box (Fin 6) -> Fin 6 -> Fin 6 -> IntervalRat
```

其中 `M_dh_exact` 必须是 exact-real DH recursion（rational DH parameters、
exact `sin/cos` enclosure、COM midpoint、parent-frame axis、`I_val/3`），
`M_eval_I` 必须是当前 directed interval implementation 的同一语义；
regularizer `1/10^6` 单独作为对角项加入，而不能藏在 CSV payload 中。

最小目标为：

```text
source_box_hash = H(B, i, j, parameters, regularizer, interval_precision)
∧ Float64Input(qhat) ∈ B
∧ IEEE64_trace_receipt(M_julia64, qhat, i, j)
∧ ExactDHIntervalSound(M_dh_exact, B)
∧ EvaluatorAgreement(M_eval_I, M_dh_exact, B)
  ⟹
  M_julia64(qhat,i,j) ∈ M_eval_I(B,i,j)
  ∧ ∀ q ∈ B, M_dh_exact(q,i,j) ∈ M_eval_I(B,i,j).
```

第一版允许 `IEEE64_trace_receipt` 作为显式 premise；它不能由普通
`Float64` 数值输出或 solver `OPTIMAL` 字符串自动生成。定理先只要求一个
entry，成功后再按相同接口扩展到 36 个 `M` entries。这样得到的是可组合的
P3 leaf，而不是未经绑定的全局 coverage 声明。

### 后续 child 顺序

1. `mass_entry_float64_to_exact_interval`：上述单 entry bridge；
2. `mass_matrix_all_entries_box`：36 entries + symmetry/regularizer；
3. `fd_CG_box_bridge`：对 `q ± h e_k` 的 M/potential exact enclosure，显式
   `h=1/100000`、二阶 remainder 和两次 Float64 sample rounding；
4. `solve_residual_box_bridge`：不是证明 `M\\rhs` 等于 exact solve，而是给出
   `M a-rhs` 的 outward residual enclosure，并记录 conditioning/roundoff；
5. `strict_true_dh_box`：组合 M/C/G/solve guards，再由 branch-and-bound
   负责所有 intersecting boxes 的 coverage。

## 必需的 source hash 与 receipt 字段

### 当前审计输入 hash

以下是现场读取的当前 bytes；一旦任一 hash 改变，child receipt 必须失效：

| source/artifact | SHA-256 |
|---|---|
| `routeB_dense_Mq/dhport_lib.jl` | `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936` |
| `routeB_dense_Mq/routeB_interval_bounds.jl` | `7c7b7254a00b5ce21f6b9f512d5de7145ca8386e0420ecf71e92a5aeb5ca789f` |
| `routeB_dense_Mq/routeB_interval_branch_bound.jl` | `c5349534fe1d01d87fb886bae94ea05f373bcbe4e24b9a2c12411a31234c0590` |
| `routeB_dense_Mq/routeB_Mq_M0.csv` | `28d98ad71d1d6c2cbe830872cad9077f2f7b4e2d932794217eb68868fd2e2b40` |
| `routeB_dense_Mq/P3_INTERVAL_BOUNDS.md` | `c880805fa443aa9fd7766a8903c988a223cfabd812ffb07fcffb30b27a4e1392` |
| `robot_final/verify_interval_artifacts.py` | `c84bcfa151b4d18e041f2c3120709f8e0989aea192d1e0359b351256128a09d5` |

### Child receipt contract

```json
{
  "schema_version": "routeb-p3-mass-entry-bridge-v1",
  "status": "PENDING|COMPILED_CANDIDATE|PASS_CONDITIONAL_SOURCE_BRIDGE",
  "statement_id": "P3.child.mass_entry_float64_to_exact_interval",
  "source_root": "external 6dof_sos_optimized working tree",
  "source_hashes": {},
  "box": {
    "endpoint_encoding": "exact rational text",
    "lo": [], "hi": [], "coordinate_order": ["q1","q2","q3","q4","q5","q6"]
  },
  "entry": {"row_zero_based": 0, "col_zero_based": 0},
  "dh_parameters_hash": "...",
  "regularizer": "1/1000000 diagonal",
  "interval_precision_bits": 256,
  "rounding": "directed endpoints; direction authenticated",
  "float64_trace": {
    "runtime": "Julia version + platform",
    "operation_trace_hash": "...",
    "finite_normal_no_overflow": true,
    "sin_cos_rounding_witness": "...",
    "matrix_multiply_accumulation_witness": "..."
  },
  "exact_real_model": {
    "definition_hash": "...",
    "parent_axis_semantics": "T_(k-1) column 3",
    "com_position": "(o_(b-1)+o_b)/2",
    "inertia_model": "I_val/3 isotropic"
  },
  "evaluator_agreement": {"proof_or_checker": "...", "exit_code": 0},
  "interval_result": {"lo": "...", "hi": "..."},
  "lean_toolchain": "...",
  "lean_source_sha256": {},
  "olean_sha256": "...",
  "axiom_report": "no sorry, no admit, no nonstandard axiom",
  "registry_status": "pending",
  "global_coverage": false,
  "formal_certificate_allowed": false
}
```

`status=PASS_CONDITIONAL_SOURCE_BRIDGE` 仍不等于 `VERIFIED`：只有在所有
entries、全域 branch coverage、residual absorption、P8 flowpipe、terminal
transfer、comparator 和 pinned full-project Lean/CI 都闭合后，才允许进入
verified registry。

## 第一不可绕过阻塞

**阻塞是 canonical Julia `Float64` DH 计算到 exact-real/interval 模型的
语义绑定缺失，而不是当前 interval 算法缺少更多 branch 节点。**

具体缺口是：`dhport_lib.jl` 在 `Matrix{Float64}` 上执行 `sin/cos`、矩阵
乘法与累加，并以 `Float64` regularizer 返回 `M`；`arm_MCG` 用
`h=1e-5` 中心差分形成 `C/G`；`exact_ddq` 用 `Mq \\ rhs` 求解。当前
`routeB_interval_bounds.jl` 重新以 directed `BigFloat` 评估 DH chain，且
其中的 Float64 权重/谱候选明确只是 diagnostic。即使 local box 的 interval
结果为正，也没有定理说明它包住 deployed function。

因此下一步不能通过增加采样、branch 深度或重复回归绕过；必须先产出上述
单 entry 的 trace/rounding witness 和 exact-model agreement proof。若不愿
证明逐操作 IEEE trace，唯一诚实替代是把 canonical source 改成一个显式
exact/interval kernel 并重新冻结 source；这将改变数学/实现范围，当前不应
未经单独决策执行。

## 证据边界

- `routeB_interval_branch_bound.jl` 的 `P_W_PROOF=(3/2,4/5)` 解决了 proof
  domain 权重的一个表示问题，但不提供 DH source binding。
- `routeb_b45_2_float64_seam_lean` 的 compiled receipt 只验证条件式
  rounding/FD interface；其 README 明确把 deployed DH/source equality、
  Float64 trigonometry、solver residual 留作 premises/open obligations。
- `routeb_dh-source-coefficient-binding-next.md` 已把 exact Laurent/Fourier
  aggregate map 与 canonical Float64 source 分开；它不能替代本 P3 box-wise
  runtime bridge。
- 当前 external receipt 的 `exit_code=0`、`coverage_complete=false`、
  `formal_certificate_allowed=false`，且 `P3.strict_true_dh_bounds` 仍为
  `open_global_coverage`；没有任何 registry mutation。

结论：本 child 可实际执行、范围最小且能直接被后续 P3/P4 消费；在它关闭前，
`P3_REAL_DH_COEFFICIENT_BINDING` 和 `P3.strict_true_dh_bounds` 必须保持
`PENDING/open`。
