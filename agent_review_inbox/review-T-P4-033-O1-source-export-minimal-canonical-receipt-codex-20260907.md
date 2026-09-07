# T-P4-033 O1 — immutable review: exact source export and minimal receipt patch

## Scope

Only the O1 source-side inhabitant was checked. This review does not revisit
determinant, q=0, or generic inverse premises.

State revision checked: `539`.

## Finding: partial exact export exists, typed same-key inhabitant does not

The deployed source has an exact coefficient-side constructor. The current
`routeB_fourier_rational_probe.py` builds a 6x6 mass dictionary with rational
Gaussian coefficients; `source_result.json` records matrix shape 6x6, body
semantics, and B45/D45 index conventions. The body-trace receipt also gives a
compiled exact aggregation sidecar.

These artifacts are not yet an O1 inhabitant. The compiled full-610 bridge is
conditional on `h_aggregate` and `h_body`; its own contract does not supply
either premise. The body-trace receipt explicitly leaves `mass_matrix`
source-binding and true-DH descriptor binding open. The exact-real source
comparator candidate defines DH/frame/body bridges but has no pinned compiled
receipt. Consequently no artifact currently supplies, under one canonical
source/state key,

```lean
M : Mu → Q → Matrix (Fin 6) (Fin 6) ℝ
M_DD45_at M mu q : Matrix (Fin 4) (Fin 4) ℝ
h_MDD_def : M_DD = M_DD45_at M mu q
```

The correct O1 status is therefore `OPEN_TYPED_SOURCE_INHABITANT`, not a
failed algebraic theorem and not a verified source receipt.

## Minimal source-evaluator generation patch

The source exporter should emit one generated Lean file and one JSON receipt
from the same run. The smallest useful Lean surface is:

```lean
abbrev Mu := ℚ
abbrev Q6 := Fin 6 → ℝ
abbrev Mat6 := Matrix (Fin 6) (Fin 6) ℝ

def M_exact (mu : Mu) (q : Q6) : Mat6 :=
  fun i j => evalExactFourier mass_coeff i j q +
    if i = j then (mu : ℝ) else 0

def M_DD45_exact (mu : Mu) (q : Q6) :
    Matrix (Fin 4) (Fin 4) ℝ :=
  M_DD45_at M_exact mu q

def M_DD := M_DD45_exact mu q

theorem h_MDD_def : M_DD = M_DD45_at M_exact mu q := by
  rfl
```

`evalExactFourier` must be the real `cos/sin` evaluator for the exported
rational coefficients, not an opaque runtime callback. The exporter must
also state whether `M_exact` is the unregularized mass or the authoritative
regularized mass; for the current source contract it must record
`M_authoritative = M_fourier + mu * I`, with `mu = 1/1000000` and the
regularizer outside the body sum.

The generated file is source-inhabiting only when its definition is tied to
the deployed source by one of these two explicit statements:

```lean
-- preferred direct source path
h_source_mass : ∀ q ∈ q_cell,
  M_exact (1/1000000) q = M_true_DH q

-- existing Fourier path, requiring both existing seams
h_aggregate : ∀ i j, csvAggregate payload q i j =
  csvAggregateBodySum fourierBody q i j
h_body : ∀ body i j, bodyContribution Jv Jw body i j =
  fourierBody body q i j
```

The receipt must reject the export if neither binding statement is emitted;
`h_MDD_def` alone only defines the projection and does not establish source
identity.

## Minimum canonical receipt fields

```text
schema: routeb.o1.true_dh_exact_typed_mdd_source.v2
source_key:
  routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8
  |mu=1/1000000|contract=exp(i*nu*q)
state_key:
  routeb-qcell:center=(0,0,0,0,0,0)|radius=1/1000
  |B=(4,5)|D=(1,2,3,6)
  |orientation=M_BD[B,D],DeltaM_DB[D,B]|norm=induced_infinity
mu_exact: 1/1000000
q_domain: exact point or the above exact uniform q-cell
matrix_type: Matrix (Fin 6) (Fin 6) ℝ
evaluator_definition: M_exact
regularization: M_authoritative = M_fourier + mu * I
block_order_one_based: [1,2,3,6]
didx_zero_based: [0,1,2,5]
bidx_zero_based: [3,4]
projection_type: Matrix (Fin 4) (Fin 4) ℝ
projection_term: M_DD45_at M_exact mu q
binding_theorem: h_MDD_def
source_binding_theorem: h_source_mass or (h_aggregate and h_body)
lean_file_hash: <generated Lean export SHA-256>
coefficient_payload_hash: a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8
deployed_source_hash: aebe6db09b2d943448c5d701631109dba8f5ee070cc66593e5dbaca26485936
```

The `source_key`, `state_key`, `mu_exact`, `q_domain`, and both block maps
must be compared byte-for-byte against the O1 consumer. Hashes are
provenance only and cannot replace `h_source_mass`, `h_aggregate`, or
`h_body`.

## Immutable disposition

`M_DD45_at` direct typed source inhabitant: `NOT PRESENT`.

Available exact coefficient/body export: `PARTIAL_SOURCE_EXPORT`.

O1 `M_DD_left_inverse_witness`: `OPEN` pending the generated Lean export,
its pinned compile/comparator receipt, and one explicit source-binding
statement above. No state or registry mutation was made.

## Bound artifact hashes

```text
artifacts/routeb_6dof/state.json
9F83F046A89D0C2E6C3BFD5F7511FC413D7F39E916385E57DBF0C4F94136BBBD

artifacts/task_routeb_o1_left_inverse_binding_20260907/TypedMDDLeftInverse.lean
F41164C49C696FB5883C1A622234701E53897801B18B9C4F1B3494FAC84026A2

artifacts/routeb_agent_body_trace_lean_20260906T081507Z/source_result.json
BEC94C198A629A3E53031899B543610286513EC3CF585C2712DC21D93BD91A87

artifacts/routeb_agent_body_trace_lean_20260906T081507Z/receipt.json
242FBC731304A14D23E11F67C8F79913400A10203215B551953CA3DA74329B50

artifacts/routeb_agent_body_trace_lean_20260906T081507Z/RouteBExactAggregationB45.lean
2E5D684AF1BE9F34B8DF168CCBA91E38565C1FFAD8FAD546A0E2B22FC39BEFA6

examples/routeb_b45_full_610_aggregate_lean/Full610AggregateComparator.lean
504A6947C0A627CEE42F4DF9304D332082E3668A3F26C34C9FEBC07B3BC56FE4

examples/routeb_b45_full_610_aggregate_lean/Full610AggregateComparator.olean
6232006CA5C4B330973B3E59FA87F365A76A4D058DD98E708CB343A0B03870A6

examples/routeb_b45_source_comparator_lean/SourceBodyMassExtensionalProbe.lean
BC2A2136576AC0A726F168492789A24703642D44865C1CCE6AE9EEF57955F76B

external routeB_dense_Mq/routeB_fourier_rational_probe.py
9460181770E47BE0ECBDE43A8A29EF285DA1168C3121FAB18D5378C671401A7B

external routeB_dense_Mq/routeB_analytic_fourier_dynamics_probe.py
A340D353F326B12A43564E5F0D45723A433611914038219E9E92D57FE177A9CE

external routeB_dense_Mq/routeB_fourier_mass_full_rational.csv
A986A208B62F585C6CA1B9C81B958710D2043E5BF786DDC930A6FA29F7A232B8

external routeB_dense_Mq/dhport_lib.jl
AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936
```
