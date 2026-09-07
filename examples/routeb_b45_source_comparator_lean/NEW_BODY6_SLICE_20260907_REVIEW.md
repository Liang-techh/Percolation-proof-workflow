# Body-6 independent Fourier/source slice — 2026-09-07

本轮将缺口从“只有参数化 canonical rows”推进为“独立 body-6 exact 构造、完整 610 行带标签 Lean 数据候选和具体 source seam”。所有 Lean 文件均 **UNCOMPILED / NOT_RUN**。没有运行 Lean、Lake、Julia，也没有核验导入链的本机编译状态。Python 数据检查不构成 source binding、source coverage、`h_body_6` 或 registry 证明。

## 新增文件与证据层

| 文件 | 作用 |
| --- | --- |
| `NEW_BODY6_SLICE_20260907.py` | 只计算第六刚体；默认只读复算，`--emit` 仅独占创建三个同前缀输出，拒绝覆盖 |
| `NEW_BODY6_SLICE_20260907.csv` | 独立计算后序列化的 body=6 exact Gaussian-rational 完整 Fourier 表 |
| `NEW_BODY6_SLICE_20260907.json` | 输入哈希、逐条目精确频率支持、负控、数据检查及 fail-closed admission |
| `NEW_BODY6_SLICE_20260907Data.lean` | 610 行 literal `BodyTraceRow`、保留分子分母标签的 canonical map、23 行第六列 filter |
| `NEW_BODY6_SLICE_20260907.lean` | 标签/支持契约、全域 source seam、12 个未编译 theorem 候选及明确未提供的叶子 |
| 本 review | 数学契约、差异解释、检查结果及下一步最小缺口 |

所有新增均在指定目录内。未修改旧 sidecar、旧 receipt、旧 canonical CSV、shared adapter、generated evaluator、body-5 文件、state、registry 或共享脚本。开始时 `state.json` 已有修改；结束时 git 还显示其他并行任务的共享脚本与新文件变更，本轮没有触碰或回退这些变更。指定目录下 `git diff --name-only` 为空；本轮六个文件是新增未跟踪文件。

## 610-row 负控的精确结论

旧 `O1_BODY_6_SUPPORT_TARGET.json` 的状态仍是 `OPEN_BODY_LABEL_SEMANTIC_MISMATCH`，本轮不改它，也不把旧 aggregate-shaped 桶作为 `h_body_6` 证据。

不过，新构造对旧结论补充了一个可复核的区别：

1. frozen aggregate 与 body=6 数据的支持集相同，都是 610 个键。
2. 它们有 **57 个精确系数键不同**，并非同一系数表。
3. 新脚本直接形成第六刚体 Gram，得到的表与已有 canonical CSV、旧 trace CSV 中 body=6 的系数逐键完全一致。
4. 因而“610 行且支持像 aggregate”不能单独证明误标；也不能证明 source binding。旧桶仍不是一个已获准的 human-body-6 source theorem。

具体负控，CSV 一基 `(row,col,nu)=(1,1,(0,-2,-2,0,0,0))`：

| 数据 | 实部 | 虚部 |
| --- | --- | --- |
| 独立 human body-6 系数 | `-699/512000` | `0` |
| frozen aggregate 系数 | `-63683/12800000` | `0` |

aggregate 仍被明确排除为 body-6 payload，不能重标签准入。数据来源独立于 aggregate，但依赖同一 pinned Python Fourier arithmetic；它不是另一个经过证明的算术解释器。

## Source seam 与物理契约

目标固定为全域函数等式：

```lean
∀ (q : Fin 6 → ℝ) (i j : Fin 6),
  RouteBO1PerBodyExactSource.sourceBodyMass q (5 : Fin 6) i j =
    NEW_BODY6_SLICE_20260907.sliceEvaluator q i j
```

`sourceBodyMass q 5` 的 `5` 是第六刚体的零基索引，不是 human body 5，也不是角坐标切片。`q` 的六个实数分量任意；仅在 `q=0` 或 `|q_k|≤1/1000` 上证明不满足当前全域 consumer。

质量为 `3/20`；世界坐标各向同性惯量为 `(1/60) I₃`，即已完成 `I_val/3`，不再乘质量或再除三。第六 DH 参数 `a₆=0, d₆=7/100`；轴取每步 DH 变换前的 parent z-axis。用零基 `o_i,z_i` 表示：

\[
o_6=o_5+\frac7{100}z_5,\qquad
c_6=\frac{o_5+o_6}{2}=o_5+\frac7{200}z_5,
\]
\[
v_i=z_i\times(c_6-o_i),\qquad
G^6_{ij}=\frac3{20}\sum_a v_i^av_j^a+
\frac1{60}\sum_a z_i^az_j^a,\quad i,j=0,\ldots,5.
\]

新脚本只构造 DH frames/axes、这个 center 和 36 个第六刚体 Gram 条目；没有调用旧 `build()`/`main()`、没有 body 累加器、没有 aggregate 减其他刚体、没有数值拟合。精确 Fourier arithmetic 取自 SHA-256 锁定的 `source_snapshot/routeB_fourier_rational_probe.py`。新计算中的 endpoint/center identity、`v_5=0` 在系数字典层检查；其 Lean source 版本仍待证明。

Lean 候选接线：

```text
Body6EndpointTarget [OPEN]
  → endpoint_to_center_attempt
  → center_to_source_gram_attempt
  → Body6SourceGramTarget

Body6SourceGramTarget + AllEntriesGramFourierTarget [OPEN]
  → source_binding_seam_attempt
  → SourceBindingTarget

SourceBindingTarget + LegacyTraceBindingTarget [OPEN]
  → legacy_consumer_seam_attempt
  → unchanged h_body_6 function equality
```

上述箭头是本轮未编译的条件式证明代码；绝不把参数 `hg`、`hf`、`ht` 的存在当成已有证据。没有构造无条件的 `SourceBindingTarget` 或 `LegacyConsumerTarget` inhabitant。

## 支持、标签和系数契约

- CSV body 标签全部是 `6`；row/col 为 `1..6`。生成 Lean 时各减一且只减一次，`Fin` 索引用显式 `⟨n, by decide⟩`，避免把越界数字按模解释。
- `nu1..nu6` 为整数，对应 Lean `q 0..q 5`。完整带符号频率全部保留；当前候选的 `nu1=nu6=0`。
- 系数是约分的实/虚有理数，分母严格正，零必须 `0/1`；标签保留原 numerator/denominator。完全零 Gaussian coefficient 不输出；重复键拒绝，不能靠覆盖消重。
- 规范 CSV 为 UTF-8 无 BOM、LF、末尾换行、无引号最短十进制整数，以 body/row/col/六个频率排序。
- atom 为 `a*cos(Σ nu_k*q_k) - b*sin(Σ nu_k*q_k)`，对应 `Re((a+i*b)*exp(i*nu·q))`。正负频率并存，不加额外因子二。
- body slice 不含 `mu*I`。`mu=1/1000000` 只属于 aggregate consumer context。独立 body6 export key 与原 aggregate `source_key`、cell `state_key` 分开。
- manifest 列出全部 36 个条目的频率列表；CSV 与 Lean literal 提供每个键的精确系数。不存在阈值截断、频率裁剪或采样推断零补集。

精确条目行数矩阵（CSV 一基）：

```text
99 44 34 34 28 12
44 25 25 16 18  4
34 25 11  8  6  4
34 16  8  3  0  2
28 18  6  0  1  0
12  4  4  2  0  1
```

共有 32 个非空条目。空条目精确为 `(4,5),(5,4),(5,6),(6,5)`。这是候选数据的零补集；source 在这些位置为零须由 `SourceBindingTarget` 与 `EmptyFourierTarget` 推出，不能从缺行直接宣称。`AllEntriesGramFourierTarget` 量化全部 36 项，不能用仅支持内等式替代。

## 先攻 23-row 第六列

令 `φ=q₂+q₃`，此处角标为 human 一基。`v_5=0` 给出第六列只有角惯量项，候选显式式为：

\[
G^6_{:,6}=\frac1{60}
\begin{bmatrix}
\cos\phi\cos q_5-\sin\phi\cos q_4\sin q_5\\
\sin q_4\sin q_5\\
\sin q_4\sin q_5\\
\cos q_5\\
0\\
1
\end{bmatrix}.
\]

每个分量的 Fourier 行数是 `12,4,4,2,0,1`，共 23 行。该公式与独立完整表的第六列已经按 exact dictionary equality 核对。第六行/列并集是 45 行数据；转置接线后可覆盖 11 个矩阵位置，包括两个零位置。

这是很小的形式化入口，但它与 aggregate 的第六列相同，因为前五个刚体 joint 6 不活跃。因此第六列恒等式不能代替 body 标签鉴别，尤其 `(6,6)=1/60` 无法识别 aggregate 冒充。

最小下一步是补 `Body6EndpointTarget` 的真实 DH source witness、`SourceAxisDotTarget` 的六个 source 轴点积以及 `SixthColumnFourierTarget` 的 23-row 三角折叠；`SixthColumnFilterTarget` 连接小列表与完整 evaluator。`sixth_slice_seam_attempt` 已明确列出 source Gram、轴点积、Fourier 叶的依赖。先完成这一列仍不等于完成整个 `h_body_6`：余下左上 `5×5` 上三角是 15 个位置，其中 14 个非零、1 个零；还需全矩阵对称性、零补集和 source-to-Fourier 证明。

完整 consumer 的另一个独立缺口是 `LegacyTraceBindingTarget`：Python 逐键相等和新旧 CSV 哈希相等没有证明 Lean map/sum 与旧全列表 `foldl` 相等。后续需 literal/list reification、body 标签排除及有限加法 fold 的接线。

## 已执行的针对性检查

运行 `python -B examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_20260907.py --emit`，成功独占创建三个新数据文件；随后默认只读复算成功，三个输出逐字节一致。结果：610 行、32 非空、36 个独立构造条目、57 个 aggregate 差异键、transpose/conjugacy、`nu1=nu6=0`、23-row 显式式、完整 Lean literal 到 CSV 的 Python 文本解码均通过。

另外在内存中检查错 body 标签、零分母、未约分系数和重复键，四种均被拒绝。Lean 文本的显式 body=5 标签与 610 行计数检查通过。一次独立文本检查受到 Windows 默认 GBK 解码影响，显式 UTF-8 重跑后通过；这不是 Lean 执行。新 Lean 文件没有 `sorry`、`admit`、`axiom` 或 `opaque` 声明。

关键 SHA-256：

```text
CSV:       46f59e5db4d74a03d5106cee4bd501090dbeec51cc897edcfd68e559ac939c7c
Data.lean: e26bb7bbed18325eee215060d37a16b2a5e71762e2689f464874a1aa1fe5a657
seam.lean: 8c7bf133203f0d5104c1ba36e433d117388c36309bed18ad91fac47506542cea
```

这些是文件身份，不是编译收据。未执行 Lean/Lake；未声称任何本机 Lean 验证。后续编译须在获得相应任务授权的环境中核验 pinned toolchain、Mathlib/import closure 与 axiom report。本轮 JSON 保持 `source_binding_proven=false`、`source_support_coverage_proven=false`、`lean_reification_proven=false`、`h_body_6_proven=false`、`comparator_accepted=false`、`registry_eligible=false`、`registry_status=pending`、`formal_certificate_allowed=false`。没有推进 O1 aggregate、M_DD45、left inverse 或正式证书准入。
