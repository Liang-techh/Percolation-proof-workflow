# T-P4-033 O1 — immutable review: source-comparator minimum gap

## Concrete progress

The v2 source-comparator target is now present at:

```text
artifacts/task_routeb_o1_true_dh_exact_typed_mdd_source_v2_20260907/
  RouteBO1SourceComparatorV2.lean
  SOURCE_COMPARATOR_RECEIPT.json
```

It reuses the existing concrete `M_exact` export and exposes exactly:

```lean
h_aggregate : ∀ q i j,
  csvAggregate massPayload q i j =
    ∑ body : Fin 6, fourierBody body q i j

h_body : ∀ q body i j,
  sourceBody body q i j = fourierBody body q i j
```

The consumer theorem `h_source_mass_from_comparator` is the exact bridge to
the existing `M_exact`.

## Evidence status

The current artifact-local exact checker reports:

```text
aggregate_equals_sum_body_exact = true
aggregate_vs_direct_mismatch_count = 0
aggregate_vs_direct_max_abs_fraction = 0
aggregate rows = 610
body-trace rows = 727
```

This is data-level evidence for `h_aggregate`; the finite-key to real
cos/sin function lift is still not a pinned Lean theorem. `h_body` is not
proved: there is no pinned Lean theorem equating each exact DH/source body
mass evaluator with the corresponding body-labelled Fourier evaluator under
the same source/state key.

The comparator JSON therefore remains:

```text
status = OPEN_H_BODY_SOURCE_COMPARATOR
h_aggregate = DATA_LEVEL_EXACT_PASS_FUNCTION_LEVEL_LEAN_OPEN
h_body = OPEN_MISSING_EXACT_DH_LEAN_THEOREM
source_binding_proven = false
```

The Lean comparator is an uncompiled candidate; no verification claim is
made.

## Smallest executable correction

Emit one pinned source-comparator artifact for the current trace that:

1. encodes the 610 aggregate and 727 body-labelled rational rows;
2. proves the finite-key equality and its real `cos/sin` function lift as
   `h_aggregate`; and
3. proves, for bodies `1..6` and the exact D coordinates
   `[0,1,2,5]`, the six `h_body` equalities from the exact DH `bodyMass`/
   `sourceBody` definition to the trace evaluator.

The existing `routeb_agent_body_trace_sink_current` artifact already supplies
the exact payload and checksum for steps 1 and the coefficient portion of
step 2. It does not supply step 3. After step 3 and the function lift are
pinned, set `source_binding_proven=true` and rerun the existing v2 validator.

## Hashes

```text
RouteBO1SourceComparatorV2.lean
94BB9FB5EB318E77EFC3766947F024E3476EA42008571F04F0BEA468F38D4A8F

SOURCE_COMPARATOR_RECEIPT.json
<computed after this review update>

current body trace CSV
AE1F9CD7978C4CF23626B5C097EAAF4A2C70DE9C8B86A31A61DB12997CF4C3B9

current aggregate CSV
8FFB1A1ABDB9DC7AA3F7849CACCA63D1BA8249A6D87C7949AF1FF9DBBD134856

current exact checker result
11E84251109CFC297D806287AF783607C9765B2C6AC6B27CB0B91A636DE23073

deployed dhport source
AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936

exact Fourier generator
9460181770E47BE0ECBDE43A8A29EF285DA1168C3121FAB18D5378C671401A7B

state.json, revision 547
A0C896C64D2180BA5535D62AB2E1F0041C3362069E23A43D9F0BAB71461ADB28
```

## Immutable disposition

`h_aggregate`: exact coefficient/data evidence present; Lean function lift
open.

`h_body`: exact DH source theorem missing.

O1 source binding remains `OPEN_H_BODY_SOURCE_COMPARATOR`. No state or
registry mutation was made.
