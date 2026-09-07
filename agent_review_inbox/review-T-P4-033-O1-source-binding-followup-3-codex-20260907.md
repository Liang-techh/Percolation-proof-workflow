# T-P4-033 O1 — same-key true-DH `M_DD` source binding follow-up

## Scope

This review only advances the typed `M_DD`/`M_DD_inv` binding. It does not
re-audit the port identity or any norm/Schur consumer.

## Current evidence

At state revision 520 the typed adapter is recorded as a compiled candidate
with compiler exit code 0, but its OLean is not supplied and
`same_key_source_binding` remains `OPEN`. The O1 interface receipt and the
typed candidate contain the projection/type adapter only; neither contains an
authoritative true-DH source receipt for the current evaluator.

The external `routeB_dense_Mq` directory contains symbolic/interval probes
which mention the D-block equation, but no receipt was found that exports the
current exact-real evaluator as a typed `Matrix (Fin 6) (Fin 6) ℝ` object and
joins its projected D block to the candidate under the same source/state key.
Those probes therefore cannot instantiate `h_MDD_def` or `h_inv_def` by
themselves.

## Exact object that the source receipt must export

The source side must expose one exact evaluator object

```lean
M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ
```

and bind the candidate block to

```lean
M_DD45_at M mu q : Matrix (Fin 4) (Fin 4) ℝ
```

where the D order is the fixed true-DH order `(1,2,3,6)`, represented in
Lean by `Didx = ![0, 1, 2, 5]`. The source receipt must carry, as fields rather
than prose-only metadata:

```text
source_key        exact source/evaluator revision and hash
state_key         exact state, q or uniform q-cell, and parameter mode
mu, q             exact serialized parameters used by M
block_order       (1,2,3,6), with the declared zero-based Fin map
matrix_shape      4 x 4 projected D block
regularization   the exact M convention used by M_DD45_at
```

Key equality is necessary for joining receipts, but it is not a Lean matrix
equality. The receipt must additionally export one of the following typed
proof surfaces.

## Two and only two consumable proof surfaces

### Path A — canonical inverse

```lean
h_MDD_def : M_DD = M_DD45_at M mu q
h_inv_def  : M_DD_inv = (M_DD45_at M mu q)⁻¹
hdet       : (M_DD45_at M mu q).det ≠ 0
```

These instantiate the existing target:

```lean
rw [h_inv_def, h_MDD_def]
exact Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr hdet)
```

The determinant must be that exact projected 4×4 block. A full 6×6
determinant, Float64 inverse, or a determinant from another `(mu,q)` does not
instantiate this path.

### Path B — direct same-object left inverse

```lean
h_MDD_def : M_DD = M_DD45_at M mu q
h_left    : M_DD_inv * M_DD45_at M mu q =
  (1 : Matrix (Fin 4) (Fin 4) ℝ)
```

Then the adapter is only:

```lean
rw [h_MDD_def]
exact h_left
```

This path does not require a determinant, but the product must use the same
projected object and the same fixed D orientation.

## Exact obstruction

The remaining mathematical/source obligation is one authoritative receipt
instantiating Path A or Path B. In particular, the missing export is the
same-key exact `M_DD45_at M mu q` binding (or an explicit matrix equality for
`M_DD`) together with either `h_inv_def + hdet` or direct `h_left`.

Until that export exists, keep `M_DD_left_inverse_witness = OPEN` and retain
`formal_certificate_allowed = false`, regardless of the typed candidate's
compiler exit code.

