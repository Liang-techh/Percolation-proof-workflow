# Route-B P4 decimal/source-binding audit

Status: **PENDING** (true-DH source binding remains pending).

Target: exported `routeB_Mq_M0.csv[4,4]` (Julia indexing).

| Layer | Result | Evidence |
|---|---|---|
| decimal spelling equality | PASS | `0.116667666666667` = `116667666666667/1000000000000000` as a decimal spelling |
| Float64 value equality | PASS | IEEE-754 bits `3fbdddeea4d57eac` |
| true-DH mass equality | **PENDING** | no exact DH/Float64 execution-to-real bridge or regularization witness |

The exact rational leaf proves only the decimal reification. It does not prove that the Julia DH implementation evaluates to this real number, nor that the exported snapshot was generated from the canonical source under the claimed semantics.

CSV SHA-256: `28d98ad71d1d6c2cbe830872cad9077f2f7b4e2d932794217eb68868fd2e2b40`
Julia source SHA-256: `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`

No external project, persistent state, registry, or P4 admission flag was modified.