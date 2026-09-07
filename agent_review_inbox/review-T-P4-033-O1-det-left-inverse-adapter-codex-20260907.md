# T-P4-033 O1 — determinant to exact D-block left-inverse adapter

范围仅为把同一 exact-real true-DH D block 的 non-singular premise 接到
O1 已有目标 `M_DD_inv * M_DD = 1`。不重审 port identity 主链。

## 结论

当前 pinned Mathlib API 足够完成该 adapter。对
`A : Matrix (Fin 4) (Fin 4) ℝ`，使用：

```lean
import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

theorem det_to_canonical_left_inverse
    (A : Matrix (Fin 4) (Fin 4) ℝ)
    (hdet : A.det ≠ 0) :
    A⁻¹ * A = (1 : Matrix (Fin 4) (Fin 4) ℝ) := by
  exact Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr hdet)
```

这一路径已在 pinned Mathlib 下定向编译通过（exit 0）。这里的逆是
Mathlib canonical `A⁻¹`，不是任意名为 `M_DD_inv` 的矩阵。

## 同一 `M_DD_inv` 的最小目标

先在 block extraction 之后取 determinant；不能对完整 `6×6` 矩阵的
determinant 代替 D-block determinant：

```lean
def blockExtract {ι κ : Type}
    (A : Matrix (Fin 6) (Fin 6) ℝ)
    (rows : ι → Fin 6) (cols : κ → Fin 6) :
    Matrix ι κ ℝ := fun i j => A (rows i) (cols j)

def Didx : Fin 4 → Fin 6 := ![0, 1, 2, 5]

def M_DD45 (M : Matrix (Fin 6) (Fin 6) ℝ) :=
  blockExtract M Didx Didx
```

若现有 O1 candidate 已把 `M_DD_inv` 作为独立变量传入，最小可消费
adapter 是：

```lean
theorem det_to_same_named_left_inverse
    (M : Matrix (Fin 6) (Fin 6) ℝ)
    (M_DD_inv : Matrix (Fin 4) (Fin 4) ℝ)
    (h_inv_def : M_DD_inv = (M_DD45 M)⁻¹)
    (hdet : (M_DD45 M).det ≠ 0) :
    M_DD_inv * M_DD45 M =
      (1 : Matrix (Fin 4) (Fin 4) ℝ) := by
  rw [h_inv_def]
  exact Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr hdet)
```

因此有两个等价实现选择：

1. 直接定义 `M_DD_inv := (M_DD45 M)⁻¹`，只需 `hdet`；或
2. 保留 candidate 的显式 `M_DD_inv` 参数，并附上
   `h_inv_def : M_DD_inv = (M_DD45 M)⁻¹`。

若既没有 `h_inv_def`，也没有直接的
`h_inv_left : M_DD_inv * M_DD45 M = 1` receipt，则
`det(M_DD45 M) ≠ 0` 单独不能推出关于这个任意 `M_DD_inv` 的目标；这是
本窄瓶颈的唯一实质 obstruction。

## 同一 `(mu,q)` 的 typed 目标

不要让 inverse witness 脱离 evaluator 参数。最小 keyed 版本为：

```lean
variable {Mu Q : Type}

def M_DD45_at
    (M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ)
    (mu : Mu) (q : Q) : Matrix (Fin 4) (Fin 4) ℝ :=
  M_DD45 (M mu q)

theorem det_to_same_keyed_left_inverse
    (M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ)
    (mu : Mu) (q : Q)
    (M_DD_inv : Matrix (Fin 4) (Fin 4) ℝ)
    (h_inv_def : M_DD_inv = (M_DD45_at M mu q)⁻¹)
    (hdet : (M_DD45_at M mu q).det ≠ 0) :
    M_DD_inv * M_DD45_at M mu q =
      (1 : Matrix (Fin 4) (Fin 4) ℝ) := by
  rw [h_inv_def]
  exact Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr hdet)
```

这里 `hdet`、`h_inv_def`、最终左逆式绑定的是同一个 `M`、同一个
`mu`、同一个 `q`、同一个 `Didx` 投影。不能把 exact `mu` 的 determinant
与 deployed `mu` 的 inverse，或另一个 q/cell 的 block，拼接成该目标。

## Receipt/key 最小字段

- `source_key`：必须覆盖 exact-real descriptor source、`M`/`M0` 版本、
  block coordinate order、`Didx=(1,2,3,6)`（one-based）及矩阵 hash。
- `state_key`：必须覆盖同一 evaluator state、同一 exact `mu` 语义、同一
  `(mu,q)` 或明确的 cell/domain key；若是 cell-uniform receipt，需说明
  `det(M_DD45_at M mu q)` 在该全域不穿过 0。
- `block extraction`：receipt 目标必须是
  `(M_DD45_at M mu q).det ≠ 0`，并绑定 `Matrix (Fin 4) (Fin 4) ℝ`；
  full `6×6` determinant 不可替代。
- `inverse binding`：要么记录 `M_DD_inv` 的定义为同一 block 的
  `nonsing_inv`，要么给出 exact equality `h_inv_def`；仅有一个数值逆、
  `det ≠ 0` 或另一个 key 下的 inverse hash 都不够。
- `formal boundary`：Lean compile receipt 需证明上述 theorem 使用的是
  同一 candidate/source/state key；本 adapter 通过后仍只补齐
  `h_inv_left` premise，不改变 O1 主链或 registry 状态。

## Status

数学/API obstruction 已缩减为 `M_DD_inv` 的同对象绑定。若该
`h_inv_def` 或直接左逆 receipt 尚未存在，状态应保持
`M_DD_left_inverse_witness = OPEN`；不能把 `det ≠ 0` 自动记为已有
candidate 的 `h_inv_left`，也不能据此标记 O1 verified。
