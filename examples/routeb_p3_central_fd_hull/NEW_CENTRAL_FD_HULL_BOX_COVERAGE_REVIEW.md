# P3 finite box coverage bridge

Status: conditional exact-real proof-attempt candidate, pending independent review.

## Typed bridge

`BoxCoverageCertificate` contains a finite box set, a region predicate, an
explicit domain predicate, per-box positive `uniformGap`, a per-box lower bound

```text
uniformGap(box) ≤ capLoad(x) - weightedLoad(x)
```

and the cap-load comparison. Its `coverage` field requires every domain point
to lie in at least one listed box. `box_coverage_strict_slack` selects that box
at the same point and proves a per-point explicit margin followed by strict
capMax slack. The consumer theorem adds only an existing bound by
`weightedLoad`.

## Coverage boundary

`grid_membership_not_global_coverage` records that a property holding on the
singleton grid `{false}` says nothing about `true`. `uncovered_box_not_global`
then gives a concrete box-region family with an omitted point. Thus finite grid
membership or an unlisted/uncovered box cannot yield a whole-domain theorem.

## External obligations

The bridge does not prove that boxes are intervals, Taylor cells, central-FD
regions, derivative-hull regions, or a cover of any continuous domain. Those
maps and coverage proofs remain external premises, as do source evidence,
numerical bounds, admission, registry promotion, and Lean compilation. No local
Lean/Lake command or broad regression was run.
