# P3 receipt to interval-enclosure adapter

Status: conditional exact-real proof-attempt candidate, pending independent review.

## Adapter contract

`IntervalReceiptPayload` retains optional receipt metadata: box source, lower
and upper endpoints, rounding-soundness claim, artifact hash, checker
exit/output, and coverage mapping. `MathEnclosureEvidence` must additionally
match every metadata field and supply the mathematical facts that metadata
cannot provide:

- endpoint order;
- positive gap lower bound and gap inequality;
- cap-load upper bound and capMax transfer;
- rounding soundness and same-point coverage.

`adaptReceipt` constructs `IntervalEnclosureCertificate` only from that full
evidence record. The adapter does not infer any inequality from a hash or
checker result.

## Fail-closed and forged boundary

Missing receipt fields or a missing coverage mapping make
`MathEnclosureEvidence` impossible, so the adapter has no input; this is
formalized by `missing_receipt_field_blocks_adapter` and
`missing_coverage_mapping_blocks_adapter`. The forged
receipt has complete-looking metadata and checker acceptance but endpoints
`lower = 1`, `upper = 0`; `forged_metadata_not_adaptable` records that endpoint
order still blocks construction.

No solver/sample/grid result is treated as interval soundness. No numerical
payload, source validation, continuous coverage, admission, registry
promotion, or Lean compilation claim is made. No local Lean/Lake command or
broad regression was run.
