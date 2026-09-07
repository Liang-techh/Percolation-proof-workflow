# T-P4-033 O1 — immutable review: source-side typed inhabitant search

## Scope and disposition

This review covers only whether the real deployed source or existing exact
artifacts inhabit the O1 source-side interface

```lean
M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ
M_DD45_at M mu q : Matrix (Fin 4) (Fin 4) ℝ
h_MDD_def : M_DD = M_DD45_at M mu q
```

No determinant, q=0, Float64, or generic inverse audit is performed here.

Observed state revision: `536`.

O1 node `120deab092c243b6a43356e63c8b56f4` remains `open`. Its current
metadata is `same_key_source_binding=OPEN`, `olean=NOT_SUPPLIED`, and
`canonical_receipt=false`.

## Search result

No inspected deployed-source or exact-artifact file contains a same-key typed
export of the required object and equality.

The exact snapshot `ReferenceMass.lean` and
`routeB_fourier_mass_full_rational.csv` provide literal/reference mass data
and Fourier coefficients. They do not export a function of type
`Mu → Q → Matrix (Fin 6) (Fin 6) ℝ`, nor a source-keyed equality to its
`D=(1,2,3,6)` projection. The deployed `dhport_lib.jl` and symbolic
`debug_12n_symM.jl` likewise do not provide a Lean-typed, same-key source
receipt. The only occurrences of `M_DD45_at` and `h_MDD_def` in the inspected
workspace are the abstract O1 candidate/interface and state metadata; they
are not source inhabitants.

## Minimal obstruction

The existing candidate is structurally usable but cannot be inhabited from
the available source. The missing conjunction is:

```text
source_key, state_key,
exact mu and exact q (or a declared uniform q-cell),
source evaluator M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ,
block order D=(1,2,3,6) with Lean map ![0,1,2,5],
h_MDD_def : M_DD = M_DD45_at M mu q.
```

In particular, the current abstract `M_DD45_at` definition does not prove
that the deployed source's rows/columns use the same D map, and it does not
join `M`, `mu`, and `q` to the recorded source/state key. Therefore no
verifiable Path A/B typed source witness can be generated from current
artifacts. The correct status is structural `OPEN`, not a failed algebraic
proof and not a verified receipt.

## Minimal interface change

Require the source exporter to emit one canonical receipt with an actual Lean
definition/theorem (not metadata-only strings):

```text
schema: routeb.o1.true_dh_exact_typed_mdd_source.v1
source_key, state_key
mu: exact Lean term or canonical exact encoding
q: exact Lean term or explicit uniform cell
evaluator: M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ
block_order_one_based: [1,2,3,6]
didx_zero_based: [0,1,2,5]
projection: M_DD45_at M mu q : Matrix (Fin 4) (Fin 4) ℝ
binding theorem: h_MDD_def : M_DD = M_DD45_at M mu q
```

The receipt must carry the source artifact hash and the exact same
`source_key/state_key/mu/q` values consumed by O1. Once present, the existing
typed candidate can be instantiated without changing the O1 algebra.

## Hashes

```text
artifacts/routeb_6dof/state.json
E7997AA9FF4AA6FC9213A376889AAF86DAE285D06C2CFBB4FD19248A8CE46940

artifacts/task_routeb_o1_left_inverse_binding_20260907/TypedMDDLeftInverse.lean
F41164C49C696FB5883C1A622234701E53897801B18B9C4F1B3494FAC84026A2

artifacts/task_routeb_o1_lean_api_audit_20260907/RouteBO1PortIdentity.lean
403C41C6F325E906A9D3555B6886D1371DFA2D84826ABCC7BF83C12E21293BFB

examples/routeb_source_binding_audit/snapshots/current_exact/ReferenceMass.lean
B77E00AB3CF236EDC143FA963ABA362A8279F2CA6CAECAF5277726FAC0C91607

examples/routeb_source_binding_audit/snapshots/current_exact/routeB_fourier_mass_full_rational.csv
A986A208B62F585C6CA1B9C81B958710D2043E5BF786DDC930A6FA29F7A232B8

external routeB_dense_Mq/dhport_lib.jl
AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936

external routeB_dense_Mq/debug_12n_symM.jl
892C108B38B936B8EEF30B5CCD267D4F4D4B0105919B12F8F4A9A6AE32190248
```

## Immutable status

`M_DD45_at` source inhabitant: `NOT FOUND`.

`M_DD_left_inverse_witness`: `OPEN` pending the single canonical typed
source export above. This review emits no receipt and does not modify state or
registry.
