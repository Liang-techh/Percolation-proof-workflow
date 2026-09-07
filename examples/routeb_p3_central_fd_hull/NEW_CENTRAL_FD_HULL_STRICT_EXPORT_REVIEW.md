# P3 final strict-margin export boundary

Status: `OPEN_UNCOMPILED`; conditional exact-real proof-attempt candidate.

## Target/consumer contract

`StrictMarginExportContract` requires an explicit domain-to-covered predicate,
`coverage`, a common scalar `commonMu`, `common_mu_positive`, the weighted
margin `weightedLoad + commonMu ≤ capMaxLoad` on covered points, and
`consumer ≤ weightedLoad` on domain points.

`strict_margin_export` returns the quantitative margin, weighted strict
inequality, and consumer strict inequality. `strict_export_implies_comparator`
packages only the `comparatorAccepted` predicate.

## Admission boundary

`registryAdmission` is defined separately as comparator acceptance plus an
independent `receiptAccepted` proposition. The theorem
`strict_export_does_not_imply_registry_admission` shows that strict inequality
alone cannot establish admission when receipt acceptance is absent.

## Obstructions

`zero_common_mu_obstruction` records why a zero common margin cannot yield
strictness. `missing_coverage_obstruction` leaves an explicit Boolean domain
point outside the covered predicate, so no whole-domain export is justified.

No registry mutation, numerical/source assertion, interval coverage upgrade,
or Lean compilation claim is made. No local Lean/Lake command or broad
regression was run.
