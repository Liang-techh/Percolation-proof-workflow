# T-P4-033 O1 — typed inverse/projection binding only

This review isolates the remaining `M_DD_inv` binding seam. It does not
restate or re-audit the port identity theorem.

## Exact projection that must be shared

Use the true-DH source matrix at the same exact parameters and project first:

```lean
def blockExtract {ι κ : Type}
    (A : Matrix (Fin 6) (Fin 6) ℝ)
    (rows : ι → Fin 6) (cols : κ → Fin 6) :
    Matrix ι κ ℝ := fun i j => A (rows i) (cols j)

def Didx : Fin 4 → Fin 6 := ![0, 1, 2, 5]

def M_DD45 (M : Matrix (Fin 6) (Fin 6) ℝ) :
    Matrix (Fin 4) (Fin 4) ℝ := blockExtract M Didx Didx

def M_DD45_at {Mu Q : Type}
    (M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ)
    (mu : Mu) (q : Q) : Matrix (Fin 4) (Fin 4) ℝ :=
  M_DD45 (M mu q)
```

`Didx = ![0,1,2,5]` is the Lean zero-based representation of the source
one-based order `(1,2,3,6)`. The order is part of the matrix object and must
not be replaced by a permutation unless a separate permutation theorem is
provided.

## Path A — typed canonical inverse

The minimal adapter into the existing generic O1 premise is:

```lean
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

theorem bind_typed_MDD_inverse
    {Mu Q : Type}
    (M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ)
    (mu : Mu) (q : Q)
    (M_DD : Matrix (Fin 4) (Fin 4) ℝ)
    (M_DD_inv : Matrix (Fin 4) (Fin 4) ℝ)
    (h_MDD_def : M_DD = M_DD45_at M mu q)
    (h_inv_def : M_DD_inv = (M_DD45_at M mu q)⁻¹)
    (hdet : (M_DD45_at M mu q).det ≠ 0) :
    M_DD_inv * M_DD =
      (1 : Matrix (Fin 4) (Fin 4) ℝ) := by
  rw [h_inv_def, h_MDD_def]
  exact Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr hdet)
```

`h_MDD_def` is essential because the current generic theorem has a separate
`M_DD` parameter. If the candidate instead defines that parameter directly as
`M_DD45_at M mu q`, then `h_MDD_def` disappears, but the resulting expression
must still be definitionally the same projection.

## Path B — direct same-key left-inverse receipt

If the source supplies a direct exact witness, determinant conversion is not
needed. The receipt must target the generic matrix after the same projection
binding:

```lean
theorem bind_direct_same_key_left_inverse
    {Mu Q : Type}
    (M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ)
    (mu : Mu) (q : Q)
    (M_DD : Matrix (Fin 4) (Fin 4) ℝ)
    (M_DD_inv : Matrix (Fin 4) (Fin 4) ℝ)
    (h_MDD_def : M_DD = M_DD45_at M mu q)
    (h_left : M_DD_inv * M_DD45_at M mu q =
      (1 : Matrix (Fin 4) (Fin 4) ℝ)) :
    M_DD_inv * M_DD =
      (1 : Matrix (Fin 4) (Fin 4) ℝ) := by
  rw [h_MDD_def]
  exact h_left
```

Thus the admissible alternatives are exactly:

```text
A. h_MDD_def + h_inv_def + exact hdet
B. h_MDD_def + direct exact h_left
```

A determinant claim with no inverse definition, or an inverse definition with
no binding of the generic `M_DD` to the projected block, cannot discharge the
existing O1 premise.

## Same-key requirement

For separate block and inverse receipts, require explicit equality of:

```text
inv.source_key   = block.source_key
inv.state_key    = block.state_key
inv.mu           = block.mu
inv.q            = block.q
inv.block_order  = block.block_order = (1,2,3,6)
```

`source_key` must cover the exact-real source matrix/evaluator revision,
coordinate order and projection convention. `state_key` must cover the same
evaluator state, exact `mu` semantics, and q-cell/domain. These key equalities
are receipt-level joins; they do not replace `h_MDD_def`, `h_inv_def`, or
`h_left`, because metadata equality alone is not a Lean equality of matrices.

The determinant receipt, when Path A is used, must be exactly:

```text
det(M_DD45_at M mu q) != 0
```

under those same keys. A full `6×6` determinant, Float64 inverse, different
`mu`, different `q`, or a permuted D ordering is not a valid substitute.

## Status / obstruction

The Mathlib/API layer is closed by `Matrix.nonsing_inv_mul`. The remaining
obstruction is the absence of one of the two same-key typed receipts above,
in particular the missing binding of the generic `M_DD` and named
`M_DD_inv` to the same exact `(mu,q)` projected object. Until that receipt is
present, keep `M_DD_left_inverse_witness = OPEN`; no O1 verified or registry
status follows.
