# T-P4-033 O1 — immutable review: true-DH exact typed source export

## Scope and status

This review covers only inhabitation of the existing typed source-binding
candidate. It does not audit inverse APIs, determinant premises, q=0 checks,
Float64 behavior, or the Schur consumer.

Observed state revision: `534`.

Current node status: `open`.

Current binding status: `OPEN_SAME_OBJECT_BINDING_TWO_PATHS`.

The candidate metadata records `same_key_source_binding=OPEN` and
`olean=NOT_SUPPLIED`. The candidate's `M_DD45_at` type and `h_MDD_def` field
are therefore only an uninhabited-by-source interface at present, not a
source receipt.

## Hashes

```text
artifacts/task_routeb_o1_left_inverse_binding_20260907/TypedMDDLeftInverse.lean
F41164C49C696FB5883C1A622234701E53897801B18B9C4F1B3494FAC84026A2

artifacts/task_routeb_o1_lean_api_audit_20260907/RouteBO1PortIdentity.lean
403C41C6F325E906A9D3555B6886D1371DFA2D84826ABCC7BF83C12E21293BFB

artifacts/routeb_6dof/state.json
15DEAAC41F5E7197D41491180B103B105AA9DB5AD010F76F1D7050023E48B709

external routeB_dense_Mq/debug_12n_symM.jl
892C108B38B936B8EEF30B5CCD267D4F4D4B0105919B12F8F4A9A6AE32190248
```

The last hash is provenance for the source-side candidate inspected in this
review; it is not a typed source receipt.

## Minimal structural obstruction

The existing candidate has the abstract shape

```lean
M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ
M_DD45_at M mu q : Matrix (Fin 4) (Fin 4) ℝ
h_MDD_def : M_DD = M_DD45_at M mu q
```

but no source artifact supplies an inhabited instance with all of these
bindings simultaneously:

```text
source_key
  no exact true-DH evaluator identity is joined to the candidate M;

state_key
  no same evaluator state/cell identity is joined to the projected block;

mu
  candidate has only a generic parameter field, not the source's exact
  parameter instance;

q
  candidate has only a generic parameter field, not the source's exact
  evaluator argument or uniform-cell instance;

block_order
  candidate declares D=(1,2,3,6) as Lean ![0,1,2,5], but no source receipt
  proves that its rows and columns use this same map;

h_MDD_def
  no source-supplied equality connects the named M_DD to that exact projected
  source object.
```

This is the minimal obstruction: without the source-side inhabitant of
`M_DD45_at M mu q` and the equality above, neither existing typed Path A nor
Path B can be instantiated. The abstract candidate itself does not create
the missing source equality.

## Unique next source export

Produce one exact typed source receipt containing:

```text
source_key, state_key, exact mu, exact q (or an explicitly uniform q-cell),
source evaluator id/hash,
block_order=(1,2,3,6), Lean Didx=![0,1,2,5],
M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ,
M_DD45_at M mu q : Matrix (Fin 4) (Fin 4) ℝ,
h_MDD_def : M_DD = M_DD45_at M mu q.
```

After this single export is present, the already-recorded Path A/B generator
can consume its corresponding inverse witness. No new O1 algebra is needed
at this boundary.

## Immutable disposition

`M_DD_left_inverse_witness` remains `OPEN`. This review emits no receipt,
does not alter state or registry, and records the source-export obstruction
under the hashes above.

