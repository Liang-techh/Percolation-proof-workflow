# Route-B source fork canonical audit

日期：2026-09-06  
范围：只读比较 `C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq` 与同一项目中的 `robot_final` source fork，并以 `.routeB_final_stage` 作辅助参照。本文是审计记录，不是 certificate、registry 或 theorem admission。

## 结论摘要

当前没有足够证据把任一 fork 无条件命名为“物理/形式 canonical source”。最稳妥的分层结论是：

- `dhport_lib.jl` 是两 fork 同字节的共同 source anchor；其 DH/frame/mass/potential/central-FD 语义可作为共同 deployed-source 事实。
- `routeB_dense_Mq` 保留了较多历史调试、侧车与 Fourier 入口；它是 exact Fourier sidecar provenance 的自然入口，但不因此成为全部 Route-B Julia 的 canonical 目录。
- `robot_final` 对三个 proof-facing Julia 文件有实质更新，尤其是 interval directed-rounding/guard、branch-and-bound receipt/proof-weight 分离和 PMI block/source metadata。若下游读取这些文件，应把 `robot_final` 视为较新的 candidate implementation；但其相对 `routeB_dense_Mq` 的语义差异必须随 receipt/hash 显式记录，不能静默覆盖旧结果。
- Fourier exact payload 的聚合/局部 enclosure 证据只证明 sidecar 或局部 interval seam；没有证明 Julia Float64 执行函数等于 exact-real Fourier evaluator，也没有关闭全域 source binding、P4 条件实例化或 P8 flowpipe/coverage。

## 1. 比较对象与方法

事实：本审计只读取文件列表、SHA-256、文本差异和已有只读审计产物；没有运行 Julia/MATLAB、SOS solver、trajectory、全局 branch-and-bound、全仓回归，也没有写外部源、certificate、registry 或 workflow state。唯一新增文件是本文档。

比较目录：

```text
target = C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized
fork A = target\routeB_dense_Mq
fork B = target\robot_final
auxiliary = target\.routeB_final_stage
```

顶层 Julia 文件统计（按文件名比较）：fork A 245 个，fork B 42 个；同名 41 个，其中 38 个同哈希、3 个不同哈希。fork A 还包含 204 个历史/debug/compact audit 文件；fork B 另有 `routeB_p3_dh_trig_center_binding.jl`，说明两目录不是简单镜像。

## 2. 哈希结果

以下为本次读取到的 SHA-256；相同值表示字节相同，不表示数学语义已经被证明。

| 文件 | `routeB_dense_Mq` | `robot_final` | 判断 |
|---|---|---|---|
| `dhport_lib.jl` | `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936` | 同左 | 同字节共同 anchor |
| `routeB_interval_bounds.jl` | `7c7b7254a00b5ce21f6b9f512d5de7145ca8386e0420ecf71e92a5aeb5ca789f` | `03679c7b686842ef9504886614e3498fb9fbf4a6c1466f8e44dcc505d21e3609` | 实质分叉 |
| `routeB_interval_branch_bound.jl` | `c5349534fe1d01d87fb886bae94ea05f373bcbe4e24b9a2c12411a31234c0590` | `5ff1d1b04e21c8f1cdf748105f29259c2fd475923925516171f2b412a007d2a7` | 实质分叉 |
| `routeB_pmi_certificate.jl` | `235f4876ed1a3343f6d84f83c0079b4d279886585dc36aeb55b9fc0289177a77` | `c1b1759161dce5e5740283a5ff379f6e87fb95d25b5be21a425b382ccd604ea5` | 实质分叉 |
| `routeB_descriptor_residual_interface.jl` | `d3d21705e5e904a080e4b86dc4c380788d2323c155570a8e7b40d62b11bb0a24` | 同左 | 同字节 |
| `routeB_export_traj.jl` | `35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf` | 同左 | 同字节 |
| `routeB_analytic_interval_branch_bound.jl` | `f9a4a3c38957f3f67021e6b09b21ace8f9523163539928a5763b2963c36f1fb3` | 同左 | 同字节 |
| `routeB_spectral_analysis.jl` | `be883e23fc5c90c17b487f7f2d0a2e46f2bc25acf49f37cbd19e18b8c1682d7f` | 同左 | 同字节 |
| `routeB_Mq_M0.csv` | `28d98ad71d1d6c2cbe830872cad9077f2f7b4e2d932794217eb68868fd2e2b40` | 同左 | 同字节 snapshot |

Fourier sidecar 只在 fork A 中发现，哈希为：`routeB_fourier_rational_probe.py` = `9460181770e47be0ecbde43a8a29ef285da1168c3121fab18d5378c671401a7b`；`routeB_analytic_fourier_dynamics_probe.py` = `a340d353f326b12a43564e5f0d45723a433611914038219e9e92d57fe177a9ce`；`routeB_fourier_mass_full_rational.csv` = `a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8`；`routeB_fourier_potential_rational.csv` = `4ebbb10e32639f54b18f259cbb762c04f2be842a856cae85e1fe94dad5478b6c`。这些是 exact sidecar 输入，不是 Julia runtime receipt。

## 3. DH、Fourier 与 interval 分支

### DH / deployed mass semantics（事实）

两 fork 的 `dhport_lib.jl` 同字节。已有 source audit 对其记录为：六行 `[theta_offset,d,a,alpha]`，`theta=q_i+offset_i`；`Tc[1]=I`，每步左到右前缀递推；当前 step 前的 parent z-axis 被取出；COM 是相邻 origin 的 midpoint；Jacobian 使用祖先截断；质量项为 translational Gram 加 `Ri*(I_val/3 I)*Ri'`，最后才加 `1e-6 I`；`C/G` 使用 `h=1e-5` central finite differences。两 fork 因共同 `dhport_lib.jl` 在这些文本语义上无差异。

### Fourier branch（事实与边界）

`routeB_dense_Mq` 携带 Gaussian-rational Fourier generator 和 aggregate CSV；已有短审计复核了有限 coefficient aggregation，且固定单盒上的 36 个 mass entries 曾得到 Fourier-cell subset canonical-natural-interval 的局部 PASS。该结果只覆盖 exact sidecar/局部 enclosure 关系。

推断：因 generator 使用同一 DH 参数、parent-axis、COM/Jacobian 与 `I_val/3` 结构，它是共同 `dhport_lib.jl` 的合理 exact-algebra precursor；但“合理 precursor”不是 `Float64 mass_matrix(q) = exact Fourier evaluator(q)` 的函数级证明。尚缺三角函数、矩阵乘法求和顺序、Float64 累加与旋转惯量乘法的误差桥。

remain open：body-labelled trace 尚未从 deployed Julia `mass_matrix` 的实际累加点同运行导出；aggregate sidecar 旁路重聚合不能替代 source execution provenance。另有历史 membership checker 的失败方向属于 dependency-inflated expression interval 与 function-range outer interval 的错误/过强比较，不能直接解释成 DH 反例；但正确方向的 source membership 仍未形成全域 theorem。

### interval branch（事实）

`robot_final/routeB_interval_bounds.jl` 相对 A 增加或改变了：

- `pi`/`2pi` 的 RoundDown/RoundUp 双端点与临界点相交 guard；
- `TRIG_DOMAIN_LIMIT = 100`，超域 fail-closed；
- `sum_down/sum_up`、定向乘积/平方/sqrt、坐标 outward expansion；
- midpoint/radius 的有限性与区间内检查；
- Cholesky/solve 相关聚合使用定向舍入。

`robot_final/routeB_interval_branch_bound.jl` 相对 A 增加或改变了：

- runtime Float64 `p_w` 与 exact proof weights 的显式分离和一致性检查；
- 13 维 receipt 坐标顺序、节点/分裂/叶分类 metadata；
- 对 coverage tree 的 fail-closed 观测接口。

推断：B 版更适合被选作 proof-facing interval candidate，因为它减少了端点、求和和 proof-weight 混用风险；但代码增强本身只提高了可审计性/潜在 enclosure soundness，不能证明任何已经运行的旧 CSV 是由 B 版生成，也不能证明其全局 coverage 已完成。

### PMI branch（事实）

`robot_final/routeB_pmi_certificate.jl` 将 PMI block 调用改为带 `semantic_name`/`source_role`，并把 `D0,c1,c2` 返回和 metadata 写入 scalar auxiliary artifacts；A 版没有这些同等字段。两版的共同源审计仍指出 PMI block 的 `f1/f2` 含 `kc*q5/kc*q4`，而 `dhport_lib.jl` 的实际 `tau` 没有相应项。

推断：B 版更利于 P4 residual decomposition 和 provenance，但 metadata 不是动力学等价证明；`kc` mismatch 仍需显式 residual。

## 4. canonical source 选择风险

1. **目录级 canonical 风险。** A 有完整历史实验面，B 是较小、较新的 proof-facing fork；按目录名或文件数量选 canonical 都不可靠。应采用逐文件 manifest，而不是把整个目录当作单一版本。
2. **共同 anchor 与分叉文件混用风险。** `dhport_lib.jl`/exporter/descriptor 同字节，但 interval/branch/PMI 不同；把 A 的 CSV 与 B 的程序直接配对会产生 receipt hash 不一致或隐性语义漂移。
3. **Fourier provenance 风险。** Fourier sidecar 主要挂在 A；若 B 被选作 interval canonical，必须明确 sidecar 仍以同哈希输入、且只作为 exact precursor，不能把 A 的 Fourier 文件名自动绑定到 B 的 runtime。
4. **时间/快照风险。** 目标树含 `.routeB_final_stage`、backup 和 restore copies；同名文件的存在不构成 lineage。没有 commit/ref 或完整生成 manifest 时，不能从 mtime 推断 canonical ancestry。
5. **结果回放风险。** 旧结果可能来自 A、B 或更早的 backup。任何 P3/P4/P8 receipt 都应绑定实际 source path、每个相关 Julia hash、输入 CSV hash、参数、区间 arithmetic 与生成器版本。

建议的当前选择：把共同 `dhport_lib.jl` 作为 deployed physical anchor；把 B 的三个分叉文件作为“candidate proof-facing implementation”；把 A 的 Fourier generator/CSV 作为“pinned exact sidecar”；在 source comparator 和同运行 receipt 完成前，整体 canonical status 保持 `OPEN`/`PENDING`，不作 registry promotion。

## 5. 对 P3 / P4 / P8 的影响

### P3 interval coverage

事实：B 的 interval 和 branch 文件新增了 directed-rounding、trigonometric domain guard、exact proof-weight check 与 receipt schema；这直接影响区间端点、root box、节点分类和 coverage evidence 的可追溯性。A 的旧输出不能仅凭同名文件复用为 B 的结果。

推断：若旧 P3 CSV 未绑定 B hash，它们最多是历史 numerical/interval evidence；即使 B 版运行成功，也仍需证明 root domain、每个 leaf 的 enclosure、未解析节点和最终 coverage status。P3 因此是“实现候选更清晰，admission 仍 open”，不是已关闭。

### P4 descriptor / condition bridge

事实：B 的 PMI metadata 为 `D0,c1,c2,D_elim_c` 和 block source role 提供了更清楚的导出面；现有 comparator 已发现 source 侧 `M0[5,5]`、`h=1e-5`、`l45`、`D_elim_c`、六坐标 domain 与 coverage 中存在未绑定/不匹配字段。已有 P4 Lean 侧为 conditional exact-real bridge，不是 DH/Float64/SOS theorem。

推断：选 B 可减少 P4 provenance ambiguity，但不能关闭 `l45`/`D_elim_c` 的函数级 source binding，也不能消除 PMI `kc` discrepancy。P4 保持 conditional/open。

### P8 reachability / flowpipe

事实：相关 true-DH slice/cross-check 明确保留 `full_dh_validated=false`、`coverage_complete=false`；它们与 primary central-FD source、interval coverage、residual absorption 和 terminal transfer 是不同层。当前没有因 fork hash 差异而产生新的 full-horizon theorem evidence。

推断：B 的 receipt/interval improvements 只能改善 P8 输入 provenance 和局部 enclosure 可审计性，不能把 finite-time slice、linearized cross-check、Monte Carlo trajectory 或 partial flowpipe 升格为全域 reachability。P8 仍 open，且应拒绝使用未绑定 fork 的旧 flowpipe receipt。

## 6. 事实、推断、remain open 清单

**事实**：共同 `dhport_lib.jl` 和多数导出/描述文件同哈希；三份核心 proof-facing Julia 文件不同；B 引入定向舍入/guard、proof-weight 分离、receipt 与 PMI semantic metadata；A 携带 Fourier sidecar；已有只读材料记录 fail-closed、未注册和未运行全局任务。

**推断**：B 是较强的 proof-facing candidate，A 是较强的 Fourier-sidecar provenance candidate；最佳工程选择是逐文件 canonical manifest，而不是二选一的整目录复制。该推断需要 source comparator/receipt 验证，不能作为形式事实。

**remain open**：

- deployed Float64 DH/frame/mass/potential/central-FD 与 exact-real/Fourier source 的函数级等价或有方向误差界；
- actual Julia body trace 与 Fourier body trace 的同运行 provenance；
- B interval implementation 对所有声明域的完整覆盖、未解析 leaf 处理和终端转移；
- P4 的 `M0[5,5]`、`h`、`l45`、`D_elim_c`、六坐标 domain 及 `kc` discrepancy 的显式绑定；
- P8 full-DH flowpipe、global coverage、residual absorption 与 terminal-transfer proof；
- 可复现的 source lineage/commit/ref 及每个既有 CSV 的真实生成 fork。

在这些项目关闭前，禁止把任一 fork 或其旧结果标作已验证 canonical certificate source；保持 `source_binding=OPEN`、`coverage=OPEN`、registry 不变。

## 7. 审计边界核验

本轮没有读取或修改外部项目之外的 workflow state，也没有注册 candidate/certificate。文档写入路径为：

`C:\Users\z5242\Desktop\重构版\工作流\docs\routeb-source-fork-canonical-audit.md`

