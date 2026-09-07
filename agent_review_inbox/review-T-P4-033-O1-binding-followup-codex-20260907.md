# T-P4-033 O1 — same-object inverse and block-key binding follow-up

Scope is restricted to the `h_inv_def`/source-key join and the true-DH D-block
projection. The generic port identity is intentionally not repeated.

## Current rev-505 finding

State rev 505 records the conditional API target
`M_DD_inv = (M_DD45 M)⁻¹` and the required `(mu,q)`/block/source/state
bindings, but no actual `h_inv_def` proof field or same-object receipt is
attached to the candidate. Thus the adapter remains open at the binding
boundary, even though the underlying Mathlib theorem is available.

## Minimal projection and inverse target

The projection must be formed before determinant and inversion:

```lean
import Mathlib.Data.Real.Basic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

set_option autoImplicit false
open scoped Matrix

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

theorem det_to_same_keyed_left_inverse
    {Mu Q : Type}
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

The minimal alternative is to remove the independent `M_DD_inv` parameter
and define it directly as `(M_DD45_at M mu q)⁻¹`. If an external inverse is
retained, `h_inv_def` is not optional: `det ≠ 0` proves the canonical inverse
identity, not an identity for an unrelated matrix with the same dimensions.

## What must be keyed together

The receipt supplying `hdet`, the receipt defining `M_DD45_at`, and the
receipt supplying `M_DD_inv` must share:

- exact-real `M` source and revision/hash;
- the same `mu` semantics and the same `q` (or one explicitly uniform cell);
- the same projection `Didx=(1,2,3,6)` in one-based source coordinates,
  represented by `![0,1,2,5]` in `Fin 6`;
- `source_key` equality, including matrix source, coordinate order, and
  regularization/coefficient semantics;
- `state_key` equality, including evaluator state, cell/domain, q-axis order,
  and exact/deployed parameter mode.

The key equalities are receipt-level obligations; the Lean kernel only sees
their consequence when all premises are instantiated with the same `M mu q`
and the same `M_DD45_at` expression. A pair of equal hash strings does not
prove `h_inv_def`, and a block hash does not prove that its rows/columns have
the declared orientation.

## Exact obstruction / required receipt

The remaining obstruction is concrete:

```text
OPEN: no authoritative h_inv_def binding
      M_DD_inv = (M_DD45_at M mu q)⁻¹
      under the same source_key and state_key as hdet.
```

The required receipt may take either form:

1. a typed definition receipt declaring
   `M_DD_inv(mu,q) := (M_DD45_at M mu q)⁻¹`; or
2. an exact equality receipt for the named candidate matrix `M_DD_inv`, plus
   exact `hdet : (M_DD45_at M mu q).det ≠ 0`.

If the source only provides a direct exact left-inverse witness for the same
projected block, that witness can bypass determinant conversion. Otherwise a
determinant number, a full `6×6` determinant, a Float64 inverse, or an
inverse from another `(mu,q)` is insufficient. No O1 verified or registry
promotion status follows from this adapter alone.
