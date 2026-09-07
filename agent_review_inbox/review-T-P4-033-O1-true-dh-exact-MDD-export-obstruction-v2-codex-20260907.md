# T-P4-033 O1 — minimal true-DH exact `M_DD` export obstruction v2

## Scope

Only the source export needed to instantiate the existing typed Path A/B
generator is considered. The strict Schur consumer and all margin fields are
out of scope.

## Receipt generation result

At state revision 531 no new true-DH exact `M_DD45` source receipt is present.
The existing O1 candidate remains an abstract typed object with
`M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ`; it is not bound to the evaluator in
`routeB_dense_Mq`. Therefore a Path A/B receipt cannot be generated without
inventing a source equality.

The source files currently available expose either a runtime Float64
`mass_matrix(q)` or a symbolic `(s,c)` polynomial construction. Neither emits
the required Lean-typed exact evaluator object plus its projection proof.

## Smallest missing source export

One source receipt must export the following single object identity:

```lean
M_DD45_at M mu q : Matrix (Fin 4) (Fin 4) ℝ
```

and the candidate binding:

```lean
h_MDD_def : M_DD = M_DD45_at M mu q
```

The receipt must bind these fields without placeholders:

```text
source_key
  exact true-DH evaluator source/hash and real-number semantics;

state_key
  the same evaluator state and either the exact q or a proved uniform q-cell;

mu
  exact parameter representation and explicit regularization placement;

q
  exact evaluator argument, not only symbolic s/c variables or a q=0 check;

block_order
  source D=(1,2,3,6), Lean Didx=![0,1,2,5], used for both rows and columns;

projection_shape
  exactly 4×4, with the matrix orientation declared in the source proof.
```

If separate receipts are used, all five bindings and the source hash must be
equal before joining them. A matching string key alone does not create the
Lean equality `h_MDD_def`.

## Final typed handoff after that export

The existing generator can then consume exactly one of:

```text
Path A: h_inv_def for the same M_DD45_at M mu q, plus its exact non-singular
        premise;
Path B: direct h_left for M_DD_inv * M_DD45_at M mu q = 1.
```

No new algebraic premise is required here; the obstruction is upstream of
both paths at the missing typed source/projection identity.

## Status

`M_DD_left_inverse_witness` remains `OPEN` with the single obstruction:
the true-DH source has not exported an exact `M_DD45_at M mu q` object bound
to the candidate under the same source/state, exact `mu,q`, and fixed
`(1,2,3,6)` block order. No Path A/B receipt or verified claim is emitted.

