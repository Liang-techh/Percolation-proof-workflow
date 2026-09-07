# O1 aggregate keyed regrouping — orientation layer

日期：2026-09-07  
范围：只攻有限和 orientation。保留现有 `Fin 610` payload、`Fin 727`
trace、`Fin 6` body interface；不改 body targets，不实例化 synthetic 数据，
不运行本机 Lean/Lake。

## 新增 exact generic lemma

接口文件：
`artifacts/task_routeb_o1_keyed_regrouping_20260907/RouteBO1KeyedRegroupingInterface.lean`

最小 generic statement：

```lean
theorem sum_body_filter_eq_row_filter
    {α β M : Type*} [Fintype α] [Fintype β] [AddCommMonoid M]
    [DecidableEq α]
    (body : β → α) (p : β → Prop) [DecidablePred p]
    (coeff : β → M) :
    (∑ a : α, ∑ n : β,
      if body n = a then if p n then coeff n else 0 else 0) =
      ∑ n : β, if p n then coeff n else 0
```

证明草稿已写入且不含 `sorry`：先用 `Fintype.sum_comm` 交换有限和，再对
trace index 做 `Finset.sum_congr`；内层 `Finset.univ` 上唯一命中的 body label
由 `simp` 消去。

现有 O1 carrier 的 specialization：

```lean
theorem finite_sum_orientation_generic
    (trace : TraceIndex → TraceRow) :
    FiniteSumOrientationTarget trace
```

其中 `α = BodyIndex = Fin 6`、`β = TraceIndex = Fin 727`、
`M = CoeffPair = ℚ × ℚ`、
`body n = (trace n).body`、
`p n := (trace n).key = k`。

## 证明边界

- 这是纯 exact finite-sum algebra；不依赖 payload、CSV 内容、source hash、
  coefficient key equality 或 body-trace adapter proof。
- `finite_sum_orientation_generic` 给出 orientation target 的泛型证明，
  但不是当前 727-row source 的运行时/数据 receipt。
- `KeyEqualityTarget` 以及 `KeyedRegroupingTarget` 仍然 open；尤其没有从
  orientation 推出 payload 与 trace 的 keyed coefficient 相等。
- 不覆盖 Float64、libm、DAG、DH semantics、coverage 或任何 theorem admission。

## 静态检查范围

仅检查接口符号、receipt JSON 结构、无 `sorry/admit/axiom` 与无默认零值
数据实例；没有运行 Lean/Lake，也没有重复 CSV 审计。

## Receipt

详见：
`artifacts/task_routeb_o1_keyed_regrouping_20260907/interface_receipt.json`

本轮 source/receipt hash 在最终文件落盘后重算；当前 receipt 明确标记
`finite_sum_orientation_provided = false`（source-bound data proof 未提供）
与 `generic_orientation_lemma_provided = true`（泛型代数 lemma 已写入）为
两个不同边界。

本轮实际 hash：

```text
interface source SHA-256: F86C15A5ED37B26DECA0746236EA1CD93A3F2207D4F1B53BC4D9ABE3A3588C43
interface receipt SHA-256: 6328B68F6C6E31320DBB9FE612E8538BA8A6B4129D38290F2C21AD7958B8CE60
```
