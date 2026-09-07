# T-P4-033 O0-R1/R2：same-key exact `K, Br, Cf` obstruction

日期：2026-09-07  
范围：只检查 O0 reduction 所需的同键 exact-real `K`、`Br`、`Cf`；不消费
ledger，不作 Schur closure，不运行 Lean/Lake。

## 结论

当前没有发现一个可消费的 canonical source/receipt，同时提供

```text
K  = exact-real bound for ||M_DD^{-1}||,
Br = exact bound for ||M_BD,r||,
Cf = exact bound for ||DeltaM_DB,f||,
```

并且共享同一 `source_key`、`state_key`、块索引和 norm convention。因此 O0-R1/R2
仍为 obstruction；已有 `rho_F^2`、`rho_27`、`rho_56` 或 Float64/interval 数值不能
替代这三个字段中的任何一个。

## 现有材料实际提供的内容

| 字段 | 现有证据 | 能否消费 |
|---|---|---|
| `K` | `RouteBExactResolventPremise` 只有调用接口；`proves_exact_real_bound` 默认是 `false`。O0 rounding receipt 明确记载 `M_DD_inverse_bound=false`。 | 否。没有 authoritative exact-real inverse receipt。 |
| `Br` | rounding bridge 只给出 `M_BD_shift=0`；没有 `||M_BD,r||` 的 exact upper bound。 | 否。零移位只证明两侧块相等，不给出块的大小。 |
| `Cf` | rounding bridge 只给出 `M_DB_shift=0`；没有 `||DeltaM_DB,f||` 的 exact upper bound。 | 否。零移位只证明差分结构，不给出 `C_f` 的范数上界。 |
| key binding | 文件 hash、CSV 行和现有 port candidates 可作为 provenance 线索，但没有把 `K/Br/Cf` 绑定到同一 canonical `source_key/state_key` 的 receipt。 | 否。hash 不是 same-key mathematical binding。 |

## 精确最小缺口

要使 reduction 的 child 可消费，至少需要一个 canonical receipt 包含以下字段；每一
项都必须指向同一键：

```text
source_key : nonempty canonical source snapshot key
state_key  : exact q/cell/state (or an explicitly declared uniform-domain key)
norm       : one fixed induced norm convention, shared by K, Br, Cf
blocks     : B=(4,5), D=(1,2,3,6), with row/column orientation fixed

K          : exact rational >= 0
K_statement: ||(M_DD^r)^(-1)||_norm <= K
K_authority: proves_exact_real_bound = true

Br         : exact rational >= 0
Br_statement: ||M_BD,r||_norm <= Br

Cf         : exact rational >= 0
Cf_statement: ||DeltaM_DB,f||_norm <= Cf

zero_shift_authority:
  dB = 0 and dC = 0 under the same source_key/state_key
```

此外，若 receipt 直接输出 weighted `epsilon_R`，还必须附同键的 metric conversion
字段（正的 exact `s`，以及已证明的 `B_up >= beta I`、`s^2 <= beta`，或等价的直接
weighted inequality）。这不是现有 `rho_F^2` candidate 的隐含结论。

## 判定边界

当前唯一可从 O0 rounding bridge 直接继承的是 exact regularizer `delta` 及在 common
base 假设下的 off-diagonal zero-shift 条件。该条件不能构造 `Br` 或 `Cf`，也不能把
数值 `K` 升格为 exact-real `K`。因此本 child 返回：

```text
OBSTRUCTION_NO_SAME_KEY_EXACT_K_BR_CF_RECEIPT
formal_certificate_allowed = false
registry_eligible = false
```

本 review 仅新增 inbox 文件；未修改主 state、registry 或源代码。

