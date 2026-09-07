# O1 body-4 tagged trace fold — minimal Lean targets

日期：2026-09-07  
范围：只细化 human body-4（zero-based body `3`）的 tagged trace fold；不改
source geometry，不重做 CSV 审计，不运行本机 Lean/Lake，不宣称 fold 已证。

## 现有 source/evaluator seam

`BodyTraceEvaluator` 的单行语义是：

```lean
traceRowContribution body row col q r :=
  if r.body = body ∧ r.row = row ∧ r.col = col then
    traceAtom r q
  else 0
```

`bodyTraceEvaluator` 是 `bodyTraceRows.foldl`，body-4 目标使用
`body_4_piecewise` 与 body label `3`。本轮新增目标文件只引用这些接口，
没有复制或修改 row data / geometry。

## Guard 分层

新增文件：
`examples/routeb_b45_source_comparator_lean/RouteBO1Body4TraceFoldTargets.lean`

### 1. block/body guard

```lean
Body4PartitionGuardTarget
```

要求 body-4 block 中每行 `r.body = 3`，prefix（body 1--3）与 suffix
（body 5--6）每行 `r.body ≠ 3`。这只是 `foldl` 分块消去的 source-bound
前提。

### 2. row/col/frequency guard

```lean
Body4KeyGuard r i j ν₂ ν₃ :=
  r.body = 3 ∧ r.row = i ∧ r.col = j ∧
  r.frequency = [0, ν₂, ν₃, 0, 0, 0]
```

实际 Lean 中用 `body4Frequency` 的函数等式表达，不依赖 vector literal。
`Body4RowColFrequencyGuardTarget` 还显式要求 real/imag rational tag 的
denominator 非零；`Body4PhaseReductionTarget` 将 guarded phase 降到
`ν₂*q₁ + ν₃*q₂`。

### 3. guard elimination

```lean
Body4EntryGuardReductionTarget
Body4OffBlockGuardReductionTarget
```

前者把 body-4 block 中的三重 guard 降为 row/col guard；后者把 block 外的
贡献降为零。这两项是 finite fold 前的最小 guard obligations。

## Conjugate atom pairing

```lean
ConjugateTaggedPairTarget r s
```

要求：

- body、row、col 相同；
- `s.frequency = -r.frequency`；
- real coefficient exact lift 相同；
- imaginary coefficient exact lift 取负；
- 四个 rational denominator 均非零。

```lean
ConjugateAtomPairTarget r s :=
  ConjugateTaggedPairTarget r s ∧
  ∀ q, traceAtom s q = traceAtom r q
```

`Body4ConjugatePairWitnessTarget` 只接受来自现有 `bodyTraceRows4` 的两行；
没有生成 partner。`Body4ConjugatePairCoverageTarget` 只表达“每行有候选
partner”，不表达 pair disjointness 或 exhaustive partition；后两者仍是
fold 证明的明确缺口。

## Finite fold targets

```lean
body4BlockFold q i j :=
  bodyTraceRows4.foldl
    (fun acc r => acc + traceRowContribution 3 q i j r) 0

Body4FullToBlockFoldTarget :=
  ∀ q i j, bodyTraceEvaluator 3 q i j = body4BlockFold q i j

Body4BlockFoldTarget :=
  ∀ q i j, body_4_piecewise q i j = body4BlockFold q i j
```

前者需要 block partition、off-block guard 与 `List.foldl_append` 风格的
精确消去；后者需要 row/col/frequency guard、conjugate pair 的不重不漏
分解以及各 pair 的 exact-real atom 化简。二者合取才形成
`Body4FoldCompositionTarget`，并最终对接既有
`h_body_4_trace_fold_target` 的 `Body4TraceFoldHandoffTarget`。

## 明确未关闭项

- 没有 source expansion proof；
- 没有 body-4 pair witness、disjointness 或 exhaustive partition proof；
- 没有 `bodyTraceRows4.foldl` 的实际 reduction proof；
- 没有 full 727-row fold receipt；
- 没有 Float64/libm/DAG/coverage 或 formal admission claim。

## Receipt

对应 receipt：
`examples/routeb_b45_source_comparator_lean/O1_BODY_4_TRACE_FOLD_TARGETS_RECEIPT.json`

依赖 hash 绑定到当前 `RouteBO1PerBodyTraceAdapter.lean` 与
`BodyTraceEvaluator.lean`；本轮只新增 targets/review/receipt，未改变 source
geometry。
