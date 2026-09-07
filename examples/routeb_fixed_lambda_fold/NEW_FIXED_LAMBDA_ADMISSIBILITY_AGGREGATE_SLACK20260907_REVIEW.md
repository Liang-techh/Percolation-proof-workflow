# Aggregate positive slack review

## Scope and status

This sidecar adds the quantitative aggregate slack layer after the reserve
lower-bound certificate.  It does not repeat total-reserve aggregation,
one-witness strictness, `0 < Σdelta ≤ Σreserve`, strict final export, digest,
or cardinality results.

No Lean or Lake command was run.  This is an uncompiled bounded proof attempt,
not a kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `ExternalTotalMarginSlackPremise` explicitly supplies
  `totalMargin = externalTotalMargin` and
  `totalReserve + Σdelta ≤ externalTotalMargin`.
- `AggregateSlackCertificate` sets `sigma = Σdelta` and proves
  `0 < sigma` and `sigma ≤ totalMargin − totalReserve`, consuming the prior
  quantitative positive-Σdelta certificate rather than duplicating it.
- `aggregate_slack_to_final_strict_consumer` uses explicit total equalities and
  `hshared_lambda` to transfer `0 < sigma ≤ finalMargin − finalLoad`, while
  retaining the existing final strict load `<` margin condition.

The external reserve-plus-delta premise is necessary: `delta ≤ reserve` by
itself is a lower bound on reserve and cannot imply positive margin minus
reserve slack.

## Remaining boundaries

The aggregate margin equality, reserve-plus-delta bound, total adapters, and
fixed-lambda equality are external premises.  No source/CSV binding, digest,
receipt minimum, complete/true-DH coverage, residual/PDE/trajectory closure,
Lean compilation, comparator acceptance, or registry eligibility is inferred.

No state, registry, receipt, or shared script was modified.
