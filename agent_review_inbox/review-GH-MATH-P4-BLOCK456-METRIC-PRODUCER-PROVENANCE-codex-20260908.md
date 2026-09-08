---
kind: review_result
review_id: review-GH-MATH-P4-BLOCK456-METRIC-PRODUCER-PROVENANCE-codex-20260908
task_id: GH-MATH-P4-BLOCK456-METRIC-PRODUCER-PROVENANCE
agent: codex-producer-provenance-lane
source_agent: codex-producer-provenance-lane
created_at: 2026-09-08T09:27:11-06:00
status: pending
integration_status: pending
admission_label: pending
proof_status: hash_matched_source_reconstruction_and_conditional_sign_transport
producer_commit_status: not_found_in_examined_local_history
producer_bytes_status: reconstructible_with_exact_recorded_sha256
runtime_receipt_status: not_verified
lean_compile_status: not_run
registry_eligible: false
registry_mutation: false
final_integration: false
proposed_integration_target: P4.block456.metric_producer_provenance
requested_action: retain hash-matched historical source reconstruction and sign-only semantic delta; require dependency/runtime/operator and domain evidence before consuming historical CSV budgets
---

# Block456 producer provenance：旧字节可重建，差异仅为全局端口反号

## 结论

两份 CSV 记录的旧 producer **并非已经证明不可恢复**：在内存中对当前 `.jl`
执行下述唯一局部替换，得到 11370 bytes，SHA-256 **精确等于**两份 CSV/report
记录的 `29710d03c34b8ef7362132a062888b84b17bb92a16a79e37a44818addbe9c90f`。
当前文件为 11548 bytes，SHA 为
`62df8b89f8025081dba985c35863c6f427dde71c225f50e1dba949f0f60bf129`。

因此，在通常的 SHA-256 内容标识假设下，已恢复与记录哈希一致的完整旧源码字节；
其与当前源码的差别仅为 **正 gain 改成负的 physical residual port** 以及相应注释/缩进。
没有发现旧 producer commit；不能把字节恢复称为找到了历史 commit 或运行 receipt。

三种孤立端口范数平方在实数数学上均不受全局反号影响；这不是 block45 weighted
left/right scaling 修正的同一种差异。**不能因此自动升级历史 CSV 为当前有效 receipt**。

本轮仅新增本 immutable review_result。没有写回恢复的 `.jl`、修改旧 review/source、
运行 producer、运行全覆盖/回归、执行 Lean、修改 state/registry 或提交 git commit。

## 1. 精确字节恢复配方

输入目录：
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/`。

当前文件 `routeB_compact_block456_port_bi_partition_probe.jl` 第 136–140 行：

```julia
    R_gain = [sum(M[BIDX[i], DIDX[k]] * Z[k, j] for k in 1:3)
              for i in 1:3, j in 1:3]
    # The reduced descriptor has v=-M_DD^-1*DeltaM_DB*a_B, so the
    # residual port is R_port=-M_BD*M_DD^-1*DeltaM_DB.
    R = [-R_gain[i, j] for i in 1:3, j in 1:3]
```

仅将以上整个 LF 字节片段（含最后换行）替换为：

```julia
    R = [sum(M[BIDX[i], DIDX[k]] * Z[k, j] for k in 1:3)
         for i in 1:3, j in 1:3]
```

只读 Python stdin 检查确认被替换片段恰出现一次，其他字节全部保留。
结果为上述旧 SHA。没有将该候选写到磁盘，没有执行 Julia。
当前文件本来就是 LF；直接 LF 规范化不改变当前 SHA，而转为 CRLF 得
`d765978e47beb641ff5f8c2557343ad4a81ed0aba9dd073468c7af574dfe08d7`，不等于旧 SHA。
第二行错误保留 14 空格而非 9 空格会得
`6553903cc804e70f55f8750c4c447651d692e680c8e99d48310e45a454669178`，也不匹配。
这给出了可复现、字节级限定的解释，不只是凭报告猜测符号修正。

## 2. Git provenance 的实际可见范围

- 在上述 6dof 项目目录执行 `git rev-parse --show-toplevel` 和路径历史查询均报
  `fatal: not a git repository (or any of the parent directories): .git`。
  外部 source 目录没有可直接查询的祖先 git repository。
- 工作流仓库是非 shallow 仓库；remote 为
  `https://github.com/Liang-techh/Percolation-proof-workflow.git`。
  本轮没有 fetch、网络查询或修改 refs。
- 在工作流仓库查询所有本地 refs 的目标 producer 路径历史，没有命中；
  `git rev-list --all --objects` 按 producer 文件名筛选也没有命名对象命中。
  这不是对其他机器、未抓取 refs、不可达对象、所有改名历史或备份的不存在证明。
- 相关 sign-consumer review 的本地历史 commit 为
  `ce3e6e614de2ea6f5276b9bb4803fba6c411e51a`，时间
  `2026-09-07T15:02:39-06:00`，消息为
  `T-P4-030: propagate corrected port sign through energy and co-state consumers`。
  它记录的是消费者 review，不是旧 producer commit，不能充当其运行时间证明。
- 前轮 matching-budget review 由
  `20d05498e72774e2009a2e5a0d03b684e388050e` 收入历史；本 review 对其中
  “producer 哈希未对齐”障碍作增量澄清，不改写旧 review。

不需要证明不可恢复或寻找更多备份：此次已用局部逆补丁得到与保存哈希完全一致的字节。
仍未定位当时 producer 的 commit、调用日志、环境快照或可信执行者身份。

## 3. CSV / report / cover 一致性

以下 SHA 均由本轮只读原始字节计算：

| 文件 | SHA-256 |
|---|---|
| 当前 `.jl` | `62df8b89f8025081dba985c35863c6f427dde71c225f50e1dba949f0f60bf129` |
| 内存恢复的旧 `.jl` | `29710d03c34b8ef7362132a062888b84b17bb92a16a79e37a44818addbe9c90f` |
| `routeB_compact_block456_port_bi_partition_probe.csv` | `1af8d59bf7253f992f13ad9318ea16ad5adb8cfa387dc5866b2f41ca4836dce4` |
| `routeB_compact_block456_port_bi_partition_probe_eta27.csv` | `35549e624dba0417fc48314a327ba4211f9c3aae39b8bce97924830cd2568df7` |
| `P5_COMPACT_BLOCK456_PORT_BI_PARTITION_PROBE.md` | `7560ab2c47712a96114232e0a1936785daa636efeedc98956bf46e2cd258334e` |
| `P5_COMPACT_BLOCK456_PORT_BI_PARTITION_PROBE_ETA27.md` | `0f290a7bdce71f72f6c12320b6c9a0e6bdd2fa4d6202f67856c1b27f123f28b8` |
| `routeB_compact_qbox_cover_depth3.csv` | `85b907bf8d12f46ee003731c5518a00a9a106c8f5a12e492037ae8fc52b04fdf` |

两份 CSV footer 与两份 report 均记录相同的旧 source SHA 和上述 cover SHA；
**当前 cover 的原始字节哈希确实匹配**，但本轮仅哈希 cover，没有重审几何覆盖。

每份 CSV 有 2560 个数据行、2560 个唯一 `(eta,depth,box_id)` key，depth 均为 3，
status 均为 RESOLVED，eta 分别为 5.6 与 2.7。两份报告记载 LIMIT=0。
三个 rho² 字段均能解析为有限非负 Fraction；三个 pivot 字段均为正。
每列逐行最大值与 CSV summary 精确一致，summary 中三个最大值的字符串亦出现在对应 report。

| eta | max rho² Euclidean | max rho² B-Cholesky | max rho² M0 |
|---|---:|---:|---:|
| 5.6 | 约 0.0451310853 | 约 0.0553736810 | 约 0.5895772978 |
| 2.7 | 约 0.0111444673 | 约 0.0165413413 | 约 0.1923526282 |

这是 artifact 内部一致性，不是 producer 重算、浮点向外包络证明或 coverage 验证。

## 4. 恢复前后语义：反号可以运输什么

设 A=M_DD(q)，Delta=M_DC(q)-M_DC(0)，G=M_CC(q)，P=diag(bdiag)，C=(4,5,6)。
旧程序内部 `R_old=M_CD A^-1 Delta`，当前程序 `R_new=-R_old`。
旧源码的其余字节（包括三种 whitening、optional branches、输出格式）未变。

| 列 | 所用算子 | 正确的条件预算 |
|---|---|---|
| `rho2_upper` | R P^(-1/2) | `||R a||² <= gamma_e a'P a` |
| `rho2_bchol_upper` | LB^(-1) DB R，LB LB'=DB G DB | `(R a)'G^(-1)(R a) <= gamma_b ||a||²` |
| `rho2_m0_upper` | L0^(-1) R P^(-1/2)，L0 L0'=M0_CC | `(R a)'M0_CC^(-1)(R a) <= gamma_m0 a'P a` |

对同一个 H、a 和任意实 R，`(-R a)'H(-R a)=(R a)'H(R a)`。
因此若旧匹配预算已经有效，则其孤立端口平方可运输到当前负号 residual。
这不依赖重跑全覆盖；但本轮没有证明旧预算有效，也没有证明浮点执行的结果逐 bit 相同。
特别是 `ell+R_new*a=ell-R_old*a`；含固定 ell 的 combined square、线性功率、
co-state 配对不能把旧正号原样保留。

`P5_COMPACT_PORT_METRIC_ORIENTATION_AUDIT.md` 明确点名的是
`routeB_compact_port_bi_partition_probe.jl`（文件名没有 block456）。它修正 weighted
left/right scaling，并将那个 producer 的旧 weighted CSV 标成 stale candidates。
本轮 block456 的哈希匹配逆补丁没有任何 left/right scaling 改动，M0 whitening 已在左侧。
不能仅因字段也叫 rho2_m0_upper 就把另一 producer 的失效原因移植过来。
反过来，也不能因本例仅差全局反号就跳过本例自己的 receipt admission。

两份 report 的“B-Cholesky 数字更大，因此更差”叙述还需保持限定：这两列的输入、输出
metric 不同，裸 scalar 大小不是同一个算子预算的强弱比较。

## 5. Optional M0-Cholesky / RESOLVED 边界

恢复的旧版本与当前版本在这一控制流上完全相同：

1. A-Cholesky 不成功 -> UNKNOWN_CHOL；solve 返回 nothing -> UNKNOWN_SOLVE；
   非正 bdiag -> UNKNOWN_BDIAG；外层捕获 exception -> ERROR_*。
2. optional B-Cholesky 失败，保留 `rho2_bchol=Inf,bchol_pivot_lower=-Inf`。
3. optional M0-Cholesky 失败，保留 `rho2_m0=Inf,m0_pivot_lower=-Inf`。
4. 两项 optional 的失败均不阻止最终 `status="RESOLVED"`。
   summary 的 resolved/unknown 只统计 status，因此不能据此推断 matching metric 成功。

本轮检查的实际 5120 行没有这些非有限 rho 或非正 pivot 情况；这是必要数据筛选通过，
不是 factor/enclosure witness。实际消费仍需有限非负 gamma、严格正的有效 pivot、
同一 nominal reference 的 Cholesky/solve 正确性，以及正确的算子范数外包。

## 6. 为什么仍不能升级 receipt

最小剩余障碍从“旧 source 字节不明”缩小为“运行及数学绑定不明”：

- 当前源码在所有盒计算结束后才 `sha256(read(@__FILE__))`，cover 也在结果计算后读来哈希；
  这是路径当时的文件哈希，不是已装载/已使用内容的原子快照。
  未证明历史运行过程中 source/cover 没有变化；这是格式缺口，不是篡改指控。
- source SHA 不绑定被 include 的 `routeB_interval_bounds.jl`、其依赖、
  analytic mass CSV、MASS_REGULARIZER、Julia/BigFloat precision/rounding 或运行环境。
  本轮没有展开读取/认证这些依赖，也没有补造其历史哈希。
- norm sums 未各自显式置于 up closure 中；最终向上乘法不足以一般性补偿此前低估。
  需要实际 ambient rounding 和完整外包机制的证据；本轮不声称已发现一次具体舍入错误。
- 十进制序列化、同一 H=M0_CC^-1、真实 r_C=R_new a_C、cell membership、
  q1=q6=0 slice 的推广条件，以及目标域覆盖仍须绑定。cover 字节一致只固定了输入文件。
- SHA 匹配无法单独证明历史 CSV 确实由该字节和正确依赖执行得到。

后续可选择审查历史 runtime/dependency receipt 并给出显式 sign-transport adapter；
也可另行授权产生完整新 receipt。但本轮不执行任一路径、不要求为单纯反号盲目重算。
历史 CSV 保持 candidate / pending，**没有 verified、registry admission 或 P4/P5 closure**。

## 7. 复核方式与交付边界

检查采用 git 只读查询、PowerShell 文件读取和 Python 标准库
hashlib/csv/io/Fraction 的 stdin 脚本（`python -B -`）。
没有导入或执行 producer/其库，没有创建恢复源码、数据、脚本或测试输出文件。
只新增本 review；保留旧 artifacts 和旧 review 原样，后续更正应使用新 review_id。
