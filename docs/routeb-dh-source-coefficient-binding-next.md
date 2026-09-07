# Route-B P3 真实 DH 系数绑定：下一步 source map 与 610-row payload

状态：`DRAFT — TARGETED READ-ONLY INSPECTION ONLY`（2026-09-06）。

本轮只读检查了 canonical Route-B 源码、Fourier/CSV 生成链和现有 Lean
payload；没有修改外部项目、state、registry 或任何已有文件。本文件是下一
个可执行 child theorem/receipt 的边界说明，不是 `LEAN_VERIFIED` 声明。

## 1. 当前阶段性结论

现有 `examples/routeb_fourier_payload_lean` 已经把冻结的 610 行质量矩阵
CSV 作为字面量 `ℚ × ℚ` 表重构进 Lean，并证明了行数、key 唯一性、support
完整性、32 个非空矩阵项和 lookup 等数据层事实。它没有定义
`exactizedDHSourceCoeff`，也没有证明该 source map 等于 CSV map。

因此当前最短缺口不是再做数值试验，而是补一个 exact-real DH Laurent/Fourier
递归，并逐行证明：

```text
exactizedDHSourceCoeff i j ν = frozenCsvCoeff i j ν
```

在 `payloadTable.rows` 上成立。若目标仍是六个 body 的逐项分解，则还必须
增加 body-level trace；610-row aggregate CSV 本身没有 body 字段，SHA-256
也不能反推出被求和前的六个 body summand。

## 2. Canonical source 的 exactized Laurent/Fourier map

以下索引采用源码的一基约定；Lean 中再映射为 `Fin 6` 的零基索引。

### 2.1 固定参数与单步 DH Laurent 原子

从 `dhport_lib.jl`：

```text
DH offset/pi/2 = [ 0, -1,  1,  0,  0,  0 ]
alpha/pi/2    = [-1,  0,  1, -1,  1,  0 ]
d             = [1/10, 0, 1/20, 19/100, 0, 7/100]
a             = [2/25, 21/100, 0, 0, 0, 0]
m             = [1, 4/5, 3/5, 2/5, 3/10, 3/20]
I_val         = [1, 3/5, 7/20, 1/5, 1/10, 1/20]
```

令 `z_k = exp(I q_k)`，`ε_k = exp(I offset_k*pi/2)`，则

```text
C_k(q) = (ε_k z_k + conj(ε_k) z_k⁻¹)/2
S_k(q) = (-I ε_k z_k + I conj(ε_k) z_k⁻¹)/2.
```

这正是 `routeB_fourier_rational_probe.py:86-92` 的 Gaussian-rational
dictionary 操作。因所有 offset/alpha 是 `pi/2` 的整数倍，`ε_k`、`cos(alpha)`、
`sin(alpha)` 只取 `1,-1,I,-I,0`，而 `a,d,m,I_val` 是有限小数，所有
Laurent 系数可留在 `ℚ(i)`。

第 `k` 个 exact DH step 是

```text
A_k = [ C_k, -S_k ca_k,  S_k sa_k, a_k C_k
        S_k,  C_k ca_k, -C_k sa_k, a_k S_k
         0,       sa_k,       ca_k, d_k
         0,        0,          0,   1   ].
```

### 2.2 frame、parent-axis、COM/Jacobian 递归

定义 `T_0 = I`，`T_k = T_{k-1} A_k`。令 `o_0=0`，
`o_k = col_4(T_k)[1:3]`，`ζ_k = col_3(T_{k-1})[1:3]`。这里 `ζ_k` 必须是
当前 DH step 之前的 parent-frame 轴；这是 Julia `fk_frames` 在第 36 行的
语义，也是 Fourier probe 第 123-128 行显式匹配的语义。

对 body `b`：

```text
p_b       = (o_{b-1} + o_b)/2
Jv_b[:,k] = ζ_k × (p_b - o_{k-1})   if k ≤ b, otherwise 0
Jw_b[:,k] = ζ_k                       if k ≤ b, otherwise 0.
```

先保留与 Julia 完全同形的旋转项：

```text
M̂_rc(q) = Σ_b [ m_b (Jv_bᵀ Jv_b)_rc
               + (Jw_bᵀ R_b ((I_val_b/3)I₃) R_bᵀ Jw_b)_rc ].
```

然后在 exact-real child theorem 中证明 `R_bᵀR_b=I` 及各向同性惯量化简，
得到 probe 第 143-149 行实际构造的等价形式

```text
M̂_rc(q) = Σ_b [ m_b Σ_ℓ Jv_b[ℓ,r] Jv_b[ℓ,c]
               + (I_val_b/3) Σ_ℓ Jw_b[ℓ,r] Jw_b[ℓ,c] ].
```

`M̂` 是未加 regularizer 的有限 Fourier/Laurent map。部署语义若固定为默认
值，则目标函数是

```text
M_exactized_rc(q) = Eval(M̂_rc, q) + (1/1,000,000) · [r=c].
```

610 行只编码 `M̂` 的非零 Fourier atoms；`1e-6 I` 不应伪造为 CSV 行，而应
在聚合定理中单独加到零频对角项。

## 3. 610 行 payload 的逐项对应方案

每一行 CSV 的语义固定为：

```text
CSV (row,col,ν1..ν6, real_num/real_den, imag_num/imag_den)
↔ Lean Row(entry=(row-1,col-1), frequency=ν,
          coefficient=(real_num/real_den, imag_num/imag_den)).
```

对每个 payload row `r`，child theorem 的最小目标是：

```lean
theorem p3_exactized_mass_row
    (r : Row) (hr : r ∈ payloadTable.rows) :
    exactizedDHSourceCoeff r.entry.1 r.entry.2 r.frequency = r.coefficient
```

现有生成器按 `(row,col)` 分块；下面是完整的 32 个非空块和 610 行计数。
Lean block 名是零基，CSV entry 是一基：

| Lean block | CSV entry | source coefficient | rows |
|---|---:|---|---:|
| `payloadRows00` | (1,1) | `M̂₁₁` | 99 |
| `payloadRows01` | (1,2) | `M̂₁₂` | 44 |
| `payloadRows02` | (1,3) | `M̂₁₃` | 34 |
| `payloadRows03` | (1,4) | `M̂₁₄` | 34 |
| `payloadRows04` | (1,5) | `M̂₁₅` | 28 |
| `payloadRows05` | (1,6) | `M̂₁₆` | 12 |
| `payloadRows10` | (2,1) | `M̂₂₁` | 44 |
| `payloadRows11` | (2,2) | `M̂₂₂` | 25 |
| `payloadRows12` | (2,3) | `M̂₂₃` | 25 |
| `payloadRows13` | (2,4) | `M̂₂₄` | 16 |
| `payloadRows14` | (2,5) | `M̂₂₅` | 18 |
| `payloadRows15` | (2,6) | `M̂₂₆` | 4 |
| `payloadRows20` | (3,1) | `M̂₃₁` | 34 |
| `payloadRows21` | (3,2) | `M̂₃₂` | 25 |
| `payloadRows22` | (3,3) | `M̂₃₃` | 11 |
| `payloadRows23` | (3,4) | `M̂₃₄` | 8 |
| `payloadRows24` | (3,5) | `M̂₃₅` | 6 |
| `payloadRows25` | (3,6) | `M̂₃₆` | 4 |
| `payloadRows30` | (4,1) | `M̂₄₁` | 34 |
| `payloadRows31` | (4,2) | `M̂₄₂` | 16 |
| `payloadRows32` | (4,3) | `M̂₄₃` | 8 |
| `payloadRows33` | (4,4) | `M̂₄₄` | 3 |
| `payloadRows35` | (4,6) | `M̂₄₆` | 2 |
| `payloadRows40` | (5,1) | `M̂₅₁` | 28 |
| `payloadRows41` | (5,2) | `M̂₅₂` | 18 |
| `payloadRows42` | (5,3) | `M̂₅₃` | 6 |
| `payloadRows44` | (5,5) | `M̂₅₅` | 1 |
| `payloadRows50` | (6,1) | `M̂₆₁` | 12 |
| `payloadRows51` | (6,2) | `M̂₆₂` | 4 |
| `payloadRows52` | (6,3) | `M̂₆₃` | 4 |
| `payloadRows53` | (6,4) | `M̂₆₄` | 2 |
| `payloadRows55` | (6,6) | `M̂₆₆` | 1 |

合计 `99+44+...+1=610`。空块为 `(4,5),(5,4),(5,6),(6,5)`；这些是
aggregate support 为空的事实，不能单独推出每个 body 的贡献都为零，因为
body-level cancellation 尚未被记录。

完成上述逐行定理后，可直接实例化现有
`conditional_source_csv_equality_on_support`，得到 source map 与
`frozenCsvCoeff` 在 support 上相等，再由 `evalMatrix_congr_on_support` 得到
Fourier evaluator 相等。若要声明全域 map 相等，还要同时证明 exactized map
在 support 外为零。

## 4. 为什么当前 Julia Route-B 不能直接成为 Lean theorem

| 当前操作 | 位置/影响 | 阻断性质 |
|---|---|---|
| `Matrix{Float64}`、`zeros`、小数 literal | `dhport_lib.jl:32,48,52` | 把 exact rational algebra 换成 IEEE 浮点执行；尚无逐操作语义/误差证明。 |
| `cos`/`sin` 与矩阵乘法 | `dhport_lib.jl:37-40` | 需要证明 Julia 计算等于 exact-real DH step；乘法次序和舍入也要固定。 |
| `Ri * Ii * Ri'` | `dhport_lib.jl:51-58` | exact probe 直接使用各向同性化简；必须先证明正交性与该化简。 |
| `M += ...` 与 `Float64(regularization)` | `dhport_lib.jl:58-60` | 累加顺序、舍入和可选 regularization 参数不是 610 个 exact rational 行。 |
| 中心有限差分 `h=1e-5` | `dhport_lib.jl:73-99` | `C/G` 不是 exact derivative；需要单独的 `O(h²)` remainder/enclosure。 |
| `Mq \ (tau-Cdq-Gq)` | `dhport_lib.jl:102-109` | 数值线性求解边界，不是 Laurent coefficient map；应从 P3 source leaf 分离。 |
| `Float64` 转换、采样与 rounding | Fourier/interval 辅助链 | 采样检查或向上取整的数值 receipt 不能证明函数/系数恒等式。 |

特别地，`routeB_analytic_fourier_dynamics_probe.py` 生成的是 exact-rational
并行接口；它自己的说明明确说不替换 canonical 的 finite-difference
`dhport_lib.jl`。其 `evaluate` 和随机检查仍把系数转为 Python float，因此
这些检查只能作为诊断，不能充当 Lean source theorem。

## 5. 最小可执行 child theorem 与 receipt

### 5.1 推荐的 child theorem 分层

先做 exact-real mass leaf，不把 Float64、FD、solve 或 P3 flowpipe 混入：

1. 复用/固定单步 Laurent normal form：`fourierCos`、`fourierSin`、DH step
   matrix 和 `z=exp(Iq)` 的 phase bridge。
2. 复用/固定 parent-axis frame recursion：证明 `T_k=T_{k-1}A_k`、
   `ζ_k=col_3(T_{k-1})`、COM midpoint 和 index round-trip。
3. 定义 `bodyMassLaurent b i j`，证明六 body 的 exact Laurent sum 等于
   `M̂_ij`；另证旋转各向同性化简。
4. 对 610 个 literal rows 证明 `p3_exactized_mass_row`；由表的
   `support_complete` 汇总为 `p3_exactized_mass_support` 和 evaluator equality。
5. 单独加 regularizer bridge：`M_exactized = Eval(M̂)+1/10^6 I`。

若要复用已有六-body aggregate bridge，则需要 source-side 新证据：

```text
routeB_fourier_mass_body_trace.csv
body,row,col,nu1,...,nu6,real_num,real_den,imag_num,imag_den
```

每个 `(row,col,ν)` 的 aggregate coefficient 必须等于所有 body trace
coefficient 之和，并记录 sparse omission/zero 约定。没有该 trace 时，
最小 child theorem 应直接证明 aggregate exactized map，不应伪造 body attribution。

### 5.2 最小 receipt 字段

```json
{
  "status": "PENDING|COMPILED_CANDIDATE|PASS_EXACT_REAL_SOURCE_MAP",
  "statement": "p3_exactized_mass_row plus support/evaluator bridge",
  "source_paths": ["dhport_lib.jl", "routeB_fourier_rational_probe.py",
                   "routeB_analytic_fourier_dynamics_probe.py"],
  "source_sha256": {},
  "aggregate_csv_sha256": "...",
  "payload_generator_sha256": "...",
  "payload_rows": 610,
  "index_convention": "one_based_csv_to_zero_based_Fin6",
  "fourier_domain": "Gaussian-rational Laurent coefficients",
  "regularizer": "1/1000000 diagonal, outside CSV rows",
  "body_trace": "missing|present_and_aggregates",
  "float64_bridge": "open",
  "finite_difference_bridge": "open",
  "solve_bridge": "out_of_scope",
  "lean_toolchain": "...",
  "mathlib_commit": "...",
  "lean_source_sha256": {},
  "olean_sha256": {},
  "axioms_report": "...",
  "registry_status": "pending"
}
```

## 6. 本轮已核对的 hash 与检查清单

当前 canonical 输入 hash：

| 文件 | SHA-256 |
|---|---|
| `routeB_dense_Mq/dhport_lib.jl` | `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936` |
| `routeB_dense_Mq/routeB_fourier_rational_probe.py` | `9460181770e47be0ecbde43a8a29ef285da1168c3121fab18d5378c671401a7b` |
| `routeB_dense_Mq/routeB_analytic_fourier_dynamics_probe.py` | `a340d353f326b12a43564e5f0d45723a433611914038219e9e92d57fe177a9ce` |
| `routeB_dense_Mq/routeB_fourier_mass_full_rational.csv` | `a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8` |
| frozen `snapshots/current_exact/routeB_fourier_mass_full_rational.csv` | 同上 |
| `examples/routeb_fourier_payload_lean/generate_payload.py` | `ea0af32c80e007212d2d4f84b808f46ff3ccb044cae3296feed79fe76afc7d32` |
| `examples/routeb_fourier_payload_lean/PayloadRows.lean` | `fdc529ce3873ef08ada9ce570b27bff99a6feb0d0e60d63c55debafbdc04fe19` |

已验证（本轮只读检查所得）：

- canonical `dhport_lib.jl` 使用六步 DH 链、parent-frame 当前轴、COM midpoint、
  `I_val/3` 各向同性惯量和默认 `1e-6 I`；
- canonical `C/G` 使用 `h=1e-5` 中心差分，`exact_ddq` 使用矩阵反斜杠；
- exact-rational Fourier exporter 的 full mass CSV 有 610 行、32 个非空
  `(row,col)` block；current external CSV 与 frozen snapshot hash 一致；
- payload 的 610 literal rows、610 unique keys、32 nonempty entries 和四个
  empty entries 已由现有 Lean 文件声明/证明；
- 现有 payload 仍明确把 exactized DH map equality 留为 open obligation；
- 现有 full-610 aggregate bridge 即使有编译 receipt，也仍以 aggregate/body
  comparator premise 为条件，不关闭 physical DH 或 Julia Float64 binding。

尚未验证、因此必须保持 open/pending：

- exact Laurent recursion 与 canonical Julia `Float64` 执行的函数等价；
- `Ri(I/3)Ri'` 化简与所有 frame/axis/index 约定的完整 Lean 实例化；
- 610 行每一行与 `exactizedDHSourceCoeff` 的 kernel-checked equality；
- 610 行的 body-level attribution/trace；
- finite-difference `C/G`、`Mq \ rhs`、interval/rounding、P3 coverage、flowpipe、
  SOS/Gram 和最终物理 Route-B theorem。

## 7. 已检查文件

外部项目（只读）：

```text
C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\dhport_lib.jl
C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\routeB_fourier_rational_probe.py
C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\routeB_analytic_fourier_dynamics_probe.py
C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\routeB_analytic_fourier_to_cs_polynomial.py
C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\routeB_fourier_mass_full_rational.csv
```

工作流现有文件（只读）：

```text
examples\routeb_fourier_payload_lean\generate_payload.py
examples\routeb_fourier_payload_lean\ExactCoefficientBridge.lean
examples\routeb_fourier_payload_lean\FiniteTableReification.lean
examples\routeb_fourier_payload_lean\PayloadRows.lean
examples\routeb_fourier_payload_lean\Payload.lean
examples\routeb_fourier_payload_lean\README.md
examples\routeb_fourier_payload_lean\PAYLOAD_METADATA.json
examples\routeb_fourier_payload_lean\REPORT.md
examples\routeb_fourier_payload_lean\verify.sh
examples\routeb_source_binding_audit\REPORT.md
examples\routeb_source_binding_audit\SHA256SUMS.csv
examples\routeb_source_binding_audit\snapshots\current_exact\reference.json
examples\routeb_b45_fourier_normal_form\FourierNormalForm.lean
examples\routeb_b45_frame_recursion\FrameRecursion.lean
examples\routeb_b45_full_610_aggregate_lean\Full610AggregateComparator.lean
```

最终 admission：`P3_REAL_DH_COEFFICIENT_BINDING = PENDING`。完成 exact-real
source map child theorem 只能关闭 aggregate coefficient seam；它不会自动
关闭 Float64、finite differences、solve、coverage 或 registry promotion。
