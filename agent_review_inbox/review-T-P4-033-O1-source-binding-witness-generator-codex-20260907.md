# T-P4-033 O1 — minimal typed source-binding witness generator

## Result

The current state has no same-key exact `M_DD45_at` source receipt, so no
witness can be instantiated now. I added a fail-closed generator:

```text
agent_review_inbox/generate_routeb_o1_mdd_binding_witness.py
```

It accepts a normalized receipt with `components.source`, `components.block`,
and `components.inverse`. It rejects missing or unequal
`source_key/state_key`, exact `(mu,q)`, source hash, and the fixed D projection
before emitting any Lean target.

## Accepted typed input surface

All three components must carry equal values for:

```text
source_key
state_key
mu_ident
q_ident
block_order_one_based = [1,2,3,6]
didx_zero_based = [0,1,2,5]
```

The source component additionally supplies `M_ident`, `source_sha256`, and
the exact projected determinant statement for Path A. The block component
supplies the exact `h_MDD_def` statement. The inverse component supplies
either the exact `h_inv_def` statement (Path A) or exact `h_left` statement
(Path B).

The generator checks these statements against the fixed typed expressions;
it does not infer them from metadata or hashes.

## Generated targets

Path A emits the minimal target:

```lean
h_MDD_def : M_DD = M_DD45_at M mu q
h_inv_def  : M_DD_inv = (M_DD45_at M mu q)⁻¹
hdet       : (M_DD45_at M mu q).det ≠ 0
⊢ M_DD_inv * M_DD = (1 : Matrix (Fin 4) (Fin 4) ℝ)
```

with `Matrix.nonsing_inv_mul` as the final proof step. Path B emits:

```lean
h_MDD_def : M_DD = M_DD45_at M mu q
h_left    : M_DD_inv * M_DD45_at M mu q =
  (1 : Matrix (Fin 4) (Fin 4) ℝ)
⊢ M_DD_inv * M_DD = (1 : Matrix (Fin 4) (Fin 4) ℝ)
```

The generator status is only `READY_TYPED_*_TARGET_NOT_VERIFIED`; it never
creates a verified receipt or changes state/registry.

## Current obstruction

Running this generator against a real source receipt is not yet possible:
the required `components.source/block/inverse` envelope is absent. The exact
missing source obligation is therefore still an authoritative true-DH export
of `M_DD45_at M mu q` (or an equality to the candidate `M_DD`) under the same
source/state key and fixed D order, followed by either Path A's `h_inv_def`
and projected `det ≠ 0`, or Path B's direct `h_left`.

No O1 status is advanced from this generator alone.
