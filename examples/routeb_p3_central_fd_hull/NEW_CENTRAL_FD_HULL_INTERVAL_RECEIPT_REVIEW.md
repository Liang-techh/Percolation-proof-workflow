# P3 interval payload / receipt boundary

Status: conditional exact-real proof-attempt candidate, pending independent review.

## Typed receipt contract

`IntervalPayloadReceipt` explicitly retains, per box, the source identifier,
lower and upper endpoints, rounding-soundness claim, artifact hash, checker exit code,
checker output, and a point-to-box coverage mapping. Optional fields
make missing evidence representable rather than silently defaulting it.

`receiptReadyAt` requires all per-box metadata, the exact accepted checker
status (`exit = 0` and `Your solution is okay!`), and the positive rounding
claim. `coverageWitnessAt` separately requires an actual mapped box in the
listed set whose region contains the point.

## Metadata/enclosure boundary

`forgedReceipt` has complete-looking metadata and an accepted checker result,
but its exact-real endpoints are `lower = 1` and `upper = 0`. The theorem
`receipt_metadata_does_not_imply_enclosure` therefore records that receipt
metadata cannot replace the mathematical endpoint enclosure or interval
soundness proof.

## Fail-closed behavior

`missing_required_field_fail_closed` rejects a receipt with any missing source,
endpoint, rounding, hash, checker, or output field. A missing coverage mapping
is rejected by `missing_coverage_mapping_fail_closed`. No source, numerical,
interval, coverage, admission, registry, or Lean compilation claim is inferred
from metadata. No local Lean/Lake command or broad regression was run.
