# T-P4-033 O1 — true-DH exact `M_DD45` export obstruction

## Scope

This is a structural obstruction for the source-binding step only. It does
not repeat the O1 port algebra or the Mathlib API review.

## Finding

At state revision 527 there is still no same-key true-DH exact source receipt
that can instantiate the typed candidate's

```lean
M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ
M_DD45_at M mu q : Matrix (Fin 4) (Fin 4) ℝ
```

The nearest source artifacts do not have that type boundary:

- `debug_11_dhport.jl` evaluates `mass_matrix(q)` as a runtime Float64
  `6×6` array;
- `debug_12n_symM.jl` constructs a symbolic polynomial object in independent
  `s_i,c_i` variables and only performs a q=0 numerical comparison;
- the P3 trig-chain contract supplies phase/interval facts but does not bind
  the resulting true-DH matrix evaluator or its D projection.

Consequently neither Path A nor Path B can currently be emitted as a typed
source receipt. The existing generator correctly remains fail-closed.

## Missing structural fields

The missing source export must provide all of the following in one normalized
receipt (or in components joined with exact equality checks):

```text
source_key
  exact true-DH evaluator identity, revision/hash, and real-valued semantics;
  current symbolic/probe provenance is not enough.

state_key
  the exact evaluator state and either the fixed q or a proved uniform q-cell;
  a q=0 comparison does not supply a cell-wide state key.

mu
  the exact regularization parameter and its placement in M_DD;
  Float64 literals or an unstated `+mu I` convention do not bind the object.

q
  the exact parameter term used by the evaluator, or a theorem that the same
  typed object is uniform over the declared cell.

block_order
  source one-based D=(1,2,3,6), Lean `Didx = ![0,1,2,5]`, with rows and
  columns both using that order and a 4×4 shape declaration.
```

The source side must also expose the matrix equality surface

```lean
h_MDD_def : M_DD = M_DD45_at M mu q
```

for the candidate's named `M_DD`. An entry dump without a proof/equality
binding to the exact evaluator is insufficient.

## Path A/B boundary after the export

Once the above object is exported, exactly one of these can be consumed:

```lean
Path A:
  h_inv_def : M_DD_inv = (M_DD45_at M mu q)⁻¹
  hdet      : (M_DD45_at M mu q).det ≠ 0

Path B:
  h_left    : M_DD_inv * M_DD45_at M mu q =
    (1 : Matrix (Fin 4) (Fin 4) ℝ)
```

Both paths retain the same `source_key`, `state_key`, exact `(mu,q)`, and
block order. No determinant, inverse, or direct left-inverse claim from a
different state or from a Float64 solve can be joined.

## Status

`M_DD_left_inverse_witness` remains `OPEN` for the single structural reason
above: the current true-DH source has not exported the exact typed
`M_DD45_at M mu q` object and its fixed-order binding. No Path A/B receipt,
Lean verification claim, or registry promotion is produced by this review.

