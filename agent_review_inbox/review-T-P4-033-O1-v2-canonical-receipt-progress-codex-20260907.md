# T-P4-033 O1 — immutable review: v2 canonical receipt progress

## Concrete result

Generated from the existing deployed rational Fourier mass export:

```text
artifacts/task_routeb_o1_true_dh_exact_typed_mdd_source_v2_20260907/
  RouteBTrueDHExactTypedMDDSourceV2.lean
  RECEIPT.json
```

The Lean file embeds the 610-row exact rational payload and contains these
concrete declarations:

```lean
M_exact : Mu → (Fin 6 → ℝ) → Matrix (Fin 6) (Fin 6) ℝ
M_DD45_exact : Mu → (Fin 6 → ℝ) → Matrix (Fin 4) (Fin 4) ℝ
h_MDD_def : M_DD mu q = M_DD45_at M_exact mu q
```

It also contains the conditional source path
`h_source_mass_of_aggregate_body`, consuming exactly
`h_aggregate` and `h_body`.

The local v2 validator result is:

```text
CONDITIONAL_TYPED_SOURCE_EXPORT
source_binding_path = h_aggregate_and_h_body
missing = ()
errors = (source_binding_theorem_not_proven,)
formal_certificate_allowed = false
registry_eligible = false
```

Thus the receipt is structurally consumable but correctly remains
conditional; it is not a Lean compile or source-binding verification receipt.

## Smallest missing artifact

No new coefficient payload is needed. The smallest missing artifact is one
pinned source-comparator Lean/JSON pair instantiating, for the exact
`source_key`, `state_key`, `mu=1/1000000`, q-cell, and D map
`[0,1,2,5]`, the two premises already exposed by the generated file:

```lean
h_aggregate : ∀ q i j,
  csvAggregate massPayload q i j =
    ∑ body : Fin 6, fourierBody body q i j

h_body : ∀ q body i j,
  sourceBody body q i j = fourierBody body q i j
```

For a smaller D-only consumer, the same receipt may restrict `i,j` to the
four D coordinates. An equivalent single artifact is a direct exact
`h_source_mass` theorem comparing `M_exact (1/1000000) q` with the deployed
true-DH mass evaluator on the same q-cell. Without one of these two forms,
the current receipt cannot set `source_binding_proven=true`.

## Bound hashes

```text
generated Lean
C7CAAEE9B782F34367721EEA41590E21354B3D4A76D8D4BDB2A34E1480F83B45

v2 receipt
E6AE6699FE164A2645C46649A6E2E31FF86F9507E563219D076251163EBC5D86

generator
C18533D8B84FCADC8DA94CE171C5AE816ED1E24A21F83672562B421A1EC45E9E

state.json, revision 543
CCDF3073FDA3F55D564F67B787EEF3EDC55022B05A004674F35D9DFE0CFBF2C9

routeB_fourier_mass_full_rational.csv
A986A208B62F585C6CA1B9C81B958710D2043E5BF786DDC930A6FA29F7A232B8

dhport_lib.jl
AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936
```

## Immutable status

`M_exact/M_DD45_exact/h_MDD_def`: `PRESENT`.

`h_aggregate+h_body`: `EXPLICIT_TARGETS_ONLY`.

O1 source binding: `OPEN_SOURCE_BINDING_PREMISE`.

No state or registry mutation was made.
