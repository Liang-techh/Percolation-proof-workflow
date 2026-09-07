# O1 keyed coefficient regrouping — minimal Lean target

日期：2026-09-07  
范围：只定义 610-row payload 与 727-row body trace 的 keyed coefficient
regrouping target；不重复数据审计、不写 `sorry`、不宣称 theorem。

## Existing type check

现有接口可以承载主要索引结构：

```text
610 payload rows -> Fin 610
727 body-trace rows -> Fin 727
six bodies -> Fin 6
matrix row/col -> Fin 6
frequency -> Fin 6 -> Int
```

`RouteBExactAggregationB45.FourierKey` 已承载 `(row, col, frequency)`；
`Full610AggregateComparator.CsvMassRow` 承载 payload atom；
`BodyTraceEvaluator.BodyTraceRow` 承载 body-labelled trace atom。

当前缺口不是索引，而是两个 row 类型没有共同的 keyed coefficient carrier，且
payload/trace 都有 real/imag 分量。最小修正是统一到：

```text
KeyedCoeffRow = { key : FourierKey, coeff : CoeffPair }
CoeffPair = { real : ℚ, imag : ℚ }
```

## Lean target

新增 [RouteBO1KeyedRegroupingInterface.lean](C:/Users/z5242/Desktop/重构版/工作流/artifacts/task_routeb_o1_keyed_regrouping_20260907/RouteBO1KeyedRegroupingInterface.lean)，定义：

```lean
payloadCoeff : (Fin 610 → PayloadRow) → FourierKey → CoeffPair
traceCoeff : (Fin 727 → TraceRow) → Fin 6 → FourierKey → CoeffPair
traceCoeffBodySum : (Fin 727 → TraceRow) → FourierKey → CoeffPair

KeyedRegroupingTarget payload trace :=
  ∀ k, payloadCoeff payload k = traceCoeffBodySum trace k

FiniteSumOrientationTarget trace :=
  ∀ k, traceCoeffBodySum trace k =
    ∑ n : Fin 727, if trace[n].key = k then trace[n].coeff else 0
```

这是最小 source-bound target。它只固定 finite-sum orientation 和 coefficient
类型，不提供 payload/trace equality。文件无数据实例、无 `sorry`、无 theorem proof。

## Minimum source obligation

要关闭 target，外部 source bridge 仍须提供：

```text
1. payload CSV row -> PayloadRow 的 exact key/coefficient lift；
2. body-trace row -> TraceRow 的 exact body/key/coefficient lift；
3. keyed equality：forall k, payloadCoeff payload k = traceCoeffBodySum trace k；
4. 若采用 row-major fold，证明 body-major -> trace-row-major 的有限和换序。
```

现有 116-key B45 exact sidecar 只能说明一个已编码子集的 finite-map equality，不能
自动升级为完整 610/727 function-level equality。

## Receipt

```text
interface source
  artifacts/task_routeb_o1_keyed_regrouping_20260907/RouteBO1KeyedRegroupingInterface.lean
  SHA-256: F28732714476A7020E90F53EA7C7DD3AD081A3F955BBBCE630320D7A3C68F5CB

interface receipt
  artifacts/task_routeb_o1_keyed_regrouping_20260907/interface_receipt.json
  SHA-256: EA6319ED51EDCBB11D7D039DF994F8BA31203CC2867869A208EB036BDE782A79

synthetic data instance: NOT CREATED
proof/theorem admission: NOT CLAIMED
```

状态：`O1_KEYED_TARGET_DEFINED`、`COMMON_CARRIER_MINIMUM_GAP_EXPLICIT`、
`SOURCE_EQUALITY_OPEN`。
