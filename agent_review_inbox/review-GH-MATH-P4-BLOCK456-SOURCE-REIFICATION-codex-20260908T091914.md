---
kind: review_result
review_id: review-GH-MATH-P4-BLOCK456-SOURCE-REIFICATION-codex-20260908T091914
task_id: GH-MATH-P4-BLOCK456-SOURCE-REIFICATION
source_agent: Codex-block456-source-reification
created_at: "2026-09-08T09:19:14.9673679-06:00"
inspected_commit: f907e960361438942831cfd7ff0661b0d3314b40
inspected_paths:
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_factorized_descriptor_model.jl
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_analytic_mass_full_cs_polynomial.csv
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl
  - agent_review_inbox/review-GH-MATH-P4-DIRECT-BLOCK456-METRIC-TRANSPORT-codex-20260908T090216.md
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
registry_mutation: false
source_binding: false
final_integration: false
requested_action: construct the seven-row complete extraction and nine-entry origin/source binding at the recorded hashes; then obtain a pinned Lean constant/inverse receipt; no source closure or registry promotion from CSV arithmetic
---

# Block456 nominal source reification: seven rows and nine entries

**最小结论：可以把数据切片缩到 7 条 CSV 记录、一个固定索引嵌入和一次有理 regularizer。
但还没有 source-to-Lean 见证。** 所需常量和每个条目的来源已明确；剩余缺口不是重新算逆矩阵，
而是证明“实际 source 原点块就是这份完整记录按指定语义求和并加一次 mu 的结果”。

本轮只读取 front matter 所列四个输入及 Git/时间元数据，只新增本 review_result。
没有打开其他 source、运行 Julia include/Lean/Lake、全回归或 source pipeline；没有修改旧 review、
state、registry、共享 adapter。以下是 exact contract 设计和有理数据检查，均非 Lean/source closure。

## 1. 原始 source 的具体语义

`routeB_factorized_descriptor_model.jl:8–19,54–78,188` 给出：

- `Q=Rational{BigInt}`；`num` 与 `den` 用 BigInt 解析后 `//`，不是 Float64 decimal。
- `Mdirect` 来自同目录 `routeB_analytic_mass_full_cs_polynomial.csv`。
- 每条记录有 row,col、12 个交替 cos/sin 指数、num,den；Julia 行列号为 1..6。
- `e1,e2` 对应 joint 1，`e3,e4` 对应 joint 2，依此到 `e11,e12` 对应 joint 6。
  loader 明确拒绝 joint 1 和 joint 6 的任何非零指数；其余映射到
  `CS=(c2,s2,c3,s3,c4,s4,c5,s5)`。
- `M[i,j] += p` 是累加，不是最后一条覆盖、不自动镜像三角、不移除同键重复项。
  CSV load 本身没有加入 mu。

`routeB_compact_block456_descriptor_structure_audit.jl:16–22,37–51` 给出：

```text
CIDX456=[4,5,6], DIDX456=[1,2,3], MU456=Q(1,1000000),
ORIGIN456=(c2,c3,c4,c5 -> 1; s2,s3,s4,s5 -> 0),
M0CC456[i,j]=origin_value456(Mdirect[CIDX456[i],CIDX456[j]])
             + (i==j ? MU456 : 0).
```

`origin_value456` 要求 substitution 后无变量，否则报错。`M0CC456` 是常矩阵，不能用未代入的
`M_CC(q)` 代替。`MDD456` 独立加 MU456；`MDC/MCD/M0DC` 不加 cross-block regularizer。
父文件 `mu=Q(1,1000000)` 与 `force_split_direct/kinetic_direct/descriptor_aux` 的同值 mu
用于分别描述正则化的动力学/能量等式；不是在已完成 M0CC456 后再加第二次 mu 的指令。

在本轮允许读取的三份 source 中，命名 `M0_CC^-1` 的具体变量没有被定义；descriptor 末尾只有
`det(Matrix{Q}(M0CC456)) != 0` 的 assertion。下面 H 是给这个已定义块提出的精确逆常量，
不是声称已读取或执行一个 Julia `inv` 结果。其后续使用位置只由先前 metric review 描述。

## 2. 完整最小切片：7 条，不仅是 6 条非零贡献

当前文件有 297 个物理行：表头加 296 条非空记录。完整扫描中满足 row,col 均在 {4,5,6}
的记录**恰好**如下。行号含表头，不能只以“搜到了这些记录”替代 completeness witness。

| CSV 物理行 | (row,col) | 对应 monomial coefficient | 原点贡献 |
|---|---|---|---|
| 269 | (4,4) | `560441/4800000` | `560441/4800000` |
| 270 | (4,4) | `(147/1600000)*s5^2` | 0 |
| 271 | (4,4) | `(-147/1600000)*c5^2` | `-147/1600000` |
| 272 | (4,6) | `(1/60)*c5` | `1/60` |
| 289 | (5,5) | `40147/800000` | `40147/800000` |
| 296 | (6,4) | `(1/60)*c5` | `1/60` |
| 297 | (6,6) | `1/60` | `1/60` |

其他四个 C×C 条目 (4,5),(5,4),(5,6),(6,5) 没有记录，由完整筛选和初始零累加器得到零。
镜像项 (4,6)/(6,4) 各自来自记录，不能只凭矩阵“应当对称”补另一项。
原点规则是所有 sin 指数为零时保留 coefficient，否则为零；cos 的正指数不会令项消失。
这里使用自然数幂与 `0^0=1`。跳过所有非常数 monomial 会漏掉 271/272/296，给出错误矩阵。

于是未正则化原点块为

```text
B0 = [ 7/60    0                1/60 ]
     [ 0       40147/800000     0    ]
     [ 1/60    0                1/60 ].
```

这一有限求和不需要 circle ideal reduction、三角加角公式、所有 body Jacobian 或全 q 的 mass theorem。
只要求选定 source 的原点求值语义和该切片的完整性。更强的 all-q DH/source theorem 是另一义务。

## 3. 拟导出的 Lean 常量与索引合同

以下是待实现的类型/常量规格，不是已存在或已编译的声明；矩阵所有有理文字须在 `ℚ` 中解释。

```lean
-- Proposed constants only; no new .lean file is created by this review.
def cIdx : Fin 3 → Fin 6 := ![3, 4, 5]
def muQ : ℚ := 1 / 1000000
def KQ : Matrix (Fin 3) (Fin 3) ℚ :=
  ![![350003 / 3000000, 0, 1 / 60],
    ![0, 200739 / 4000000, 0],
    ![1 / 60, 0, 50003 / 3000000]]
def HQ : Matrix (Fin 3) (Fin 3) ℚ :=
  ![![50003000000 / 5000400003, 0, -50000000000 / 5000400003],
    ![0, 4000000 / 200739, 0],
    ![-50000000000 / 5000400003, 0, 350003000000 / 5000400003]]
```

Julia local index 1,2,3 分别对应 Lean Fin 3 的 0,1,2；`cIdx i` 再对应全空间 Fin 6 的 3,4,5。
必须证明/固定 `cIdx(i).val+1 = CIDX456[i.val+1]`，对行与列均使用同一个嵌入。
不能将 Julia 的 [4,5,6] 原样放进 Fin 6；6 越界，4/5 的含义也已偏一。
还需 `cIdx` injective，保证抽取 `mu*I6` 就是 `mu*I3`，无需对 cross-block 额外补零项。

精确结论规格：`KQ=B0+muQ*I3`，`KQ*HQ=I3`，`HQ*KQ=I3`。
向实数导出时逐项使用有理数的 canonical cast，`K i j=(KQ i j : ℝ)`、
`H i j=(HQ i j : ℝ)`、`muR=(muQ : ℝ)`。不要用 `Float.ofScientific`、近似十进制或中间 Float64。
矩阵乘法与该 cast 的交换、两边单位矩阵恒等式是有限求和的 algebra leaves。

## 4. 最小 evidence DAG 与非循环 source contract

| 见证 | 精确义务 | 不能用什么替代 |
|---|---|---|
| R0 bytes identity | 绑定以下 hashes 的两个 Julia 文件和 CSV 字节及读取路径 | 相同文件名、目录或任意 metadata 字符串 |
| R1 parse/selection | 整个 296-row list 按 loader 语义解码；筛选 C×C 后等于上述有序 7-row list | 只写 7 个想要的数、只证明它们存在 |
| R2 origin evaluation | 证明 source 原点 9 个条目等于该筛选 list 的有理 origin fold | 外部脚本退出码、`mass_identity` 的打印文本 |
| R3 block/regularizer | source 的 C 顺序为 cIdx，mu_source=cast muQ；其块定义为 raw origin block 加一次 diagonal mu | 常量同名、只检查 mu>0、对已有 K 再加 mu |
| R4 constant arithmetic | originFold=B0，KQ=B0+muQ I，KQ/HQ 双边 inverse；导出实数等式 | 近似逆、仅 determinant 非零 |
| R5 inverse semantics | target 所指逆是 R3 的同一个 source block 的数学逆；以唯一性识别 H | 把任意矩阵命名为 sourceInv，或只验证候选 HQ |

R0 本身是 artifact provenance，不是 Lean 中的语义定理。R1 可以选择一个已验证 parser，或者
明确披露信任边界的 audited reifier；后者即使生成的有理常量通过 kernel 检查，也不能声称
已经获得完整 byte-parser/Julia-runtime correctness。不能将该边界藏在 `by native_decide` 或一个 hash 字符串中。

最弱的后续数学接口可以只要求**原点的九条等式**，无需复刻整个 Julia 模块：令 `S0` 表示该 source
的未正则化原点质量矩阵，`sourceM0` 表示其 source-defined regularized C block，要求

```text
hOrigin: forall i j, S0(cIdx i,cIdx j) = cast(originFold(selectedRows,i,j)),
hMu:     mu_source = cast(muQ),
hBlock:  forall i j, sourceM0(i,j) = S0(cIdx i,cIdx j)
                                    + (if i=j then mu_source else 0).
```

这些等式必须从 R0–R3 实际交付，不得作为新增公理填洞。R4 随后推出 `sourceM0=K`。
若 inverse API 暴露 `sourceInv*sourceM0=I`，由 `K*H=I` 直接得到
`sourceInv=sourceInv*(K*H)=(sourceInv*K)*H=H`。若使用 Lean 的 matrix inverse，则需先交付
K 的 nonsingularity/合法逆语义，再调用其 inverse-uniqueness 接口，不能依赖 totalized inverse
在奇异情况下的默认值。该阶段不需要平方根；SPD/LDL 与 whitening 由先前 metric contract 另接。

此三份 source 的顶层 include 还会读取 Jacobian/Coriolis/gravity 等其他文件并产生报告输出；
本轮没有读取它们，也没有执行 include。对原点 M0 的局部数学 reification 可以隔离 `load_mass`
语义，不需运行这些支路；但不能因此声称整个 Julia 程序已执行成功或完成完整 dependency audit。

## 5. 精确 missing-witness obstruction

现有输入给出生成公式、数据与先前数学 review，没有提供 R1–R3 的 Lean 定理/来源见证。
下面三个反模型说明 R4 不能独自补齐缺口；它们不是机器人轨迹反例。

1. **regularizer provenance 丢失：** K 与 K+mu I 都是正定矩阵，但对角条目相差恰好 `1/1000000`。
   即使 K*H=I 已通过 kernel，也不能推出实际 source 若用了 K+mu I 就有 inverse H。漏加与重复加
   regularizer 都不能由“SPD 且 inverse 可算”检测为 source identity。
2. **排列丢失：** C=(4,6,5) 的块为 P^T K P，仍同样 SPD 且 determinant 不变；其 local (1,1)
   条目（零基第二坐标）与 K 的对应条目差 `80441/2400000`。仅固定集合 {4,5,6} 不足。
   若做排列，residual 的三个坐标也须同步运输，不能只换矩阵。
3. **切片 completeness 丢失：** 漏掉第 271 行会把 M44 增加 `147/1600000`。即使其他六条都有 hash、
   原点求值正确且结果仍为可逆矩阵，也不等于 loader 对完整文件的累加结果。

所以最小 obstruction 是“source 原点九条等式及其完整记录/索引/regularizer 来源未证明”。
这不是矩阵条目未知，也不是需要更多数值采样。当前可以交付这份精确合同，不能标记 source closure。
即使后续 R0–R5 都完成，仍只绑定**这个固定 source 的 nominal mass block**；它不自动证明
all-q DH 一致性、执行 residual、total_eq456 的域内成立、beta allocation、coverage 或 registry admission。

## 6. 本轮检查、身份及后续 receipt

一次内存内 Fraction 检查读取指定 CSV：296 条记录均为 16 字段、行列 1..6、自然数指数、正分母，
joint 1/6 指数均为零；C×C 完整筛选恰为所列七条；原点求和为 B0；加一次 mu 后得到 KQ；
两个 3×3 inverse products 均精确为 I。另核对排列差值。命令退出码 0。
这是 independent exact-rational data check，不是 Lean parser、Julia execution 或 source theorem。
本 review_result 的 YAML/状态字段另做静态解析，不运行任何 ingestion/state mutation。

| 输入 | SHA-256 |
|---|---|
| `routeB_factorized_descriptor_model.jl` | `C3007D5E30FEEB963A86B9589ADE3CA7D95B16316E753E8D18B007AA044CD427` |
| `routeB_analytic_mass_full_cs_polynomial.csv` | `1A1DB0B737ABAC58AFAE06E95766D2DA91C12425FE1BE388364F1DCA7DB59451` |
| `routeB_compact_block456_descriptor_structure_audit.jl` | `9E67520934801C87D0BBE14C550F755AFE80FFD6EACD1B6572FC65C52FC6CD79` |
| 前序 metric review | `3A6A5C87109CD54BEEB71FFFCA70FDE9876EBF05186A09160A86DAA0CD520EEA` |

inspected_commit 仅记录本地工作区基线，外部三份 source 由各自 hash 绑定，不宣称属于该 commit。
下一份 pinned receipt 应逐项报告 R1–R5 哪些已形式化、哪些仍是外部信任：固定 Lean/Mathlib 和
候选源码/输入 hashes，完整构建日志与退出码，所有 source-origin/block/inverse theorem 的 axiom
输出和 placeholder scan，以及实际 source/olean hashes。仅证明 KQ*HQ=I 的绿色日志应标为
constant-arithmetic child，不能升级为 source-bound nominal block。状态保持 pending/OPEN_UNCOMPILED。
