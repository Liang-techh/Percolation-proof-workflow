# O1 aggregate exact adapter / keyed regrouping layers

日期：2026-09-07  
范围：只定义 `CsvMassRow` / `BodyTraceRow` 到已落地
`KeyedCoeffRow`/`CoeffPair` 的 exact target，并分层 keyed finite-sum
regrouping。没有重复 CSV 审计、没有 `sorry`、没有数据 theorem admission。

## Exact adapter target

接口文件：
`artifacts/task_routeb_o1_keyed_regrouping_20260907/RouteBO1KeyedRegroupingInterface.lean`

公共 carrier 为：

```lean
abbrev CoeffPair := ℚ × ℚ
structure KeyedCoeffRow where
  key : FourierKey
  coeff : CoeffPair
```

payload 的 source-shaped row 只含 key 与有理实/虚系数；adapter target 是：

```lean
PayloadCsvAdapterTarget csv payload :=
  ∀ n : Fin 610, payload n = (csv n).toKeyedCoeffRow
```

其中

```text
toKeyedCoeffRow.key    = { row, col, frequency }
toKeyedCoeffRow.coeff  = (realCoeff, imagCoeff)
```

body trace 的 source-shaped row 还保留 `body : Fin 6`；adapter target 是：

```lean
BodyTraceAdapterTarget traceRows trace :=
  ∀ n : Fin 727,
    trace n = { body := (traceRows n).body,
               key := (traceRows n).toKeyedCoeffRow.key,
               coeff := (traceRows n).toKeyedCoeffRow.coeff }
```

`RationalTag.toRat` 只表达 exact rational lift
`numerator / denominator : ℚ`。它不是 Float64、libm 或运行时解析证明。

## 可证明分层

1. **Orientation layer**

   ```lean
   FiniteSumOrientationTarget trace :=
     ∀ k,
       traceCoeffBodySum trace k = traceCoeffRowSum trace k
   ```

   该层只处理 `Fin 6` body-major 外和与 `Fin 727` row-major keyed
   filter 的有限和换序。它依赖 trace 的 body label 与有限索引类型，不依赖
   payload CSV 数值。

2. **Key-equality layer**

   ```lean
   KeyEqualityTarget payload trace :=
     ∀ k, payloadCoeff payload k = traceCoeffRowSum trace k
   ```

   该层是 source-bound 的真正数据接口：需要两个 adapter target，以及
   payload 与 trace 在每个 `FourierKey` 上的 exact coefficient equality。
   当前只给出 proposition target，没有数据证明。

3. **Regrouping layer**

   ```lean
   keyed_regrouping_of_orientation_and_key_equality
   ```

   已给出无 `sorry` 的泛型蕴含：orientation 加 key equality 推出
   `KeyedRegroupingTarget`。这不是 610/727 数据 theorem，也不证明两个
   现有 source 文件的函数相等。

4. **Real-lift layer**

   ```lean
   RealLiftTarget :=
     ∀ q k, realLift k (payloadCoeff payload k) q =
       realLift k (traceCoeffBodySum trace k) q
   ```

   `real_lift_of_keyed_regrouping` 已给出 exact `ℚ → ℝ` coefficient equality
   的泛型重写。这里的 `Real.sin`/`Real.cos` 只是 exact-real expression；
   不含 Float64、libm enclosure、DAG evaluation 或 coverage。

## 当前边界与最小缺口

- 已落地：公共 `KeyedCoeffRow` carrier、两个 source-shaped exact adapter
  target、orientation/key-equality/regrouping/real-lift 的 typed 分层。
- 未落地：两个 adapter 的 source proof、完整 610/727 source-bound
  `KeyEqualityTarget`、以及 orientation 的具体 trace proof。
- 不纳入本 receipt：CSV 重审、Float64/libm、DH semantics、O2 coverage、
  synthetic row/instance。
- 因而状态仍是 `INTERFACE_ONLY_UNPROVED`；只允许把两个泛型 lemma 作为
  algebraic bridge 使用，不能注册为 aggregate theorem。

## Receipt binding

详见：
`artifacts/task_routeb_o1_keyed_regrouping_20260907/interface_receipt.json`

本 review 与 receipt 应在接口文件变更后一起重算 SHA-256；本文件不复用旧
source/olean receipt，也没有声称新的 Lean compile receipt。

本轮实际 binding：

```text
interface source SHA-256: 6FA9B4FD73515730E68D5E447F5CAEA5874BDCC44D71DB1DFBEF1DEBB09734F5
interface receipt SHA-256: EBEB453642789ACAFBD53F721A7692B87DA2A3E8683447B5D4ECBBBD7AC50B60
```
